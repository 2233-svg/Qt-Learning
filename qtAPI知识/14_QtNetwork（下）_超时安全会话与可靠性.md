# Qt Network（下）：超时、安全会话与可靠性

> 适用版本：Qt 6.11.1  
> 核心类型：`QNetworkRequest`、`QNetworkReply`、`QSslConfiguration`、`QNetworkCookieJar`、`QNetworkDiskCache`、`QNetworkProxy`

上篇建立了异步 HTTP 基础。本篇关注真实应用必然遇到的问题：请求如何结束、哪些失败能重试、证书错误怎样处理，以及如何管理 Cookie、缓存、代理、并发和测试。

## 1. 一次请求需要哪些终止条件

```text
成功：网络完成 + 预期 HTTP 状态 + 合法响应
失败：DNS/TCP/TLS/HTTP/解析/业务错误
取消：用户或上层不再需要结果
超时：一段时间无传输，或超过业务总截止时间
过期：结果回来时，界面已经发起更新一代请求
```

只处理成功与失败还不够。取消不是应该弹窗的故障，过期响应也不应覆盖新结果。

## 2. 传输超时不是总截止时间

Qt 6.7+ 可设置一段时间没有任何字节传输就中止：

```cpp
using namespace std::chrono_literals;

m_manager->setTransferTimeout(30s); // Manager 默认值

QNetworkRequest request(url);
request.setTransferTimeout(10s);    // 非零请求值覆盖 Manager
```

它检测的是**连续无数据交换的时间**。如果服务端每 9 秒发一个字节，请求可能远超 10 秒仍不触发。因此业务总截止时间需另设定时器。

### 2.1 总截止时间

```cpp
QNetworkReply *reply = m_manager->get(request);
auto *deadline = new QTimer(reply);
deadline->setSingleShot(true);
deadline->start(15s);

connect(deadline, &QTimer::timeout, reply, [reply] {
    reply->setProperty("timedOut", true);
    reply->abort();
});

connect(reply, &QNetworkReply::finished, this, [reply] {
    if (reply->property("timedOut").toBool())
        qWarning() << "请求超过总截止时间";
    reply->deleteLater();
});
```

定时器是 Reply 的子对象，Reply 销毁会自动取消定时器。`abort()` 后仍会发 `finished()`，统一清理仍放在那里。

### 2.2 零超时的含义

Manager 的传输超时默认是 0，即禁用。若 Manager 已设置非零超时，请求设置 0 不一定能绕过它；要执行无超时请求，需要按文档语义调整 Manager 配置。更稳妥的是按用途建立配置明确的网络客户端，而不是临时修改共享 Manager 后忘记恢复。

## 3. 用户取消与对象销毁

```cpp
class RequestHandle : public QObject
{
    Q_OBJECT

public:
    explicit RequestHandle(QNetworkReply *reply, QObject *parent = nullptr)
        : QObject(parent), m_reply(reply) {}

public slots:
    void cancel()
    {
        if (m_reply && !m_reply->isFinished())
            m_reply->abort();
    }

private:
    QPointer<QNetworkReply> m_reply;
};
```

`QPointer` 在 Reply 被删除后自动变空，避免取消按钮持有悬空裸指针。

完成处理要区分：

```cpp
if (reply->error() == QNetworkReply::OperationCanceledError) {
    emit requestCanceled(); // 通常不作为错误弹窗
} else if (reply->error() != QNetworkReply::NoError) {
    emit requestFailed(reply->errorString());
}
```

窗口关闭时，如果结果没有任何消费者，通常应取消其请求。全局同步任务则不应因为一个页面关闭而被误取消；所有权应与真正业务生命周期对齐。

## 4. 防止旧响应覆盖新响应

搜索框每次输入都发请求时，响应顺序可能与请求顺序不同：

```text
请求 A 发出 ─────────────────────→ A 返回
    请求 B 发出 ───→ B 返回
```

若 A 最后更新界面，会把较新的 B 覆盖。解决方法：

```cpp
const quint64 generation = ++m_searchGeneration;
QNetworkReply *reply = m_manager->get(request);

connect(reply, &QNetworkReply::finished, this,
        [this, reply, generation] {
    const auto cleanup = qScopeGuard([reply] { reply->deleteLater(); });
    if (generation != m_searchGeneration)
        return; // 过期响应，不再应用
    applySearchResult(reply->readAll());
});
```

也可以在发新请求时 abort 旧请求。代数标记仍值得保留，因为取消与完成可能在事件队列中交错。

## 5. 重试不是“失败后再发一次”

重试前同时判断：

1. 错误是否瞬时，例如暂时断网、连接重置、503。
2. 方法/操作是否幂等，重复执行会不会创建两笔订单。
3. 是否还有重试预算和总截止时间。
4. 服务端是否给出 `Retry-After`。
5. 用户是否已经取消。

### 5.1 通常不自动重试的情况

- 400、401、403、404 等确定性客户端/权限错误；
- JSON 结构不符合协议；
- TLS 证书验证失败；
- 非幂等 POST 且没有幂等键；
- 用户主动取消。

### 5.2 指数退避和抖动

```cpp
const int cappedAttempt = qMin(attempt, 6);
const int baseMs = 250 * (1 << cappedAttempt);
const int jitterMs = QRandomGenerator::global()->bounded(0, 250);
const int delayMs = qMin(baseMs + jitterMs, 30'000);

QTimer::singleShot(delayMs, context, [=] {
    sendAgain();
});
```

抖动避免大量客户端同一时刻重新冲击服务。退避必须有最大次数、最大延迟和总时间预算。

### 5.3 幂等键

必须重试“创建订单”类 POST 时，与服务端约定唯一幂等键：

```cpp
request.setRawHeader("Idempotency-Key", operationId.toUtf8());
```

服务端必须缓存该键对应结果。仅客户端添加 Header 而服务端不支持，并不能防止重复创建。

## 6. HTTP 重定向策略

Qt 的常见策略：

| 策略                           | 行为                                     |
| ---------------------------- | -------------------------------------- |
| `ManualRedirectPolicy`       | 不自动跟随                                  |
| `NoLessSafeRedirectPolicy`   | 默认；允许 http→http、http→https、https→https |
| `SameOriginRedirectPolicy`   | 协议、主机、端口都必须相同                          |
| `UserVerifiedRedirectPolicy` | 每次由客户端处理 redirected 后决定                |

设置单请求策略：

```cpp
request.setAttribute(
    QNetworkRequest::RedirectPolicyAttribute,
    QNetworkRequest::SameOriginRedirectPolicy);
```

用户确认策略：

```cpp
connect(reply, &QNetworkReply::redirected,
        this, [reply](const QUrl &target) {
    if (isAllowedRedirect(target))
        reply->redirectAllowed();
    else
        reply->abort();
});
```

安全检查至少比较 scheme、host、port，并判断 Authorization、Cookie 或上传 body 是否可能被带到不可信目标。Qt 对 301/302 的兼容行为可能把非 HEAD 请求改为 GET，涉及写操作时不要盲目自动跟随。

## 7. TLS：不要用 ignoreSslErrors 修复生产问题

```cpp
connect(reply, &QNetworkReply::sslErrors,
        this, [reply](const QList<QSslError> &errors) {
    for (const QSslError &error : errors)
        qWarning() << error.errorString();
    // 默认不调用 ignoreSslErrors()，让连接失败
});
```

证书错误可能表示：

- 系统时间错误；
- 证书过期或主机名不匹配；
- 缺少受信任中间证书；
- 企业代理替换证书；
- 真正的中间人攻击。

无参数 `ignoreSslErrors()` 等于接受所有报告的证书问题，会使 HTTPS 的身份验证失效。开发环境也应安装正确的测试 CA，或仅针对明确证书和明确错误做严格受限处理。

### 7.1 TLS 配置

```cpp
QSslConfiguration ssl = QSslConfiguration::defaultConfiguration();
ssl.setProtocol(QSsl::TlsV1_2OrLater);
request.setSslConfiguration(ssl);
```

不要随意清空默认 CA。自签名体系应把专用 CA 加入配置并验证主机名，而不是忽略错误。

### 7.2 HSTS

```cpp
m_manager->setStrictTransportSecurityEnabled(true);
m_manager->enableStrictTransportSecurityStore(
    true, QStandardPaths::writableLocation(QStandardPaths::CacheLocation));
```

HSTS 会记住服务端通过安全连接声明的策略，并把相关 http 请求升级为 https。持久化目录要符合应用数据策略。HSTS 与 `ignoreSslErrors()` 存在安全语义冲突，应以严格验证为基础。

## 8. 认证

HTTP Basic/Digest 等挑战会触发：

```cpp
connect(m_manager, &QNetworkAccessManager::authenticationRequired,
        this, [this](QNetworkReply *reply, QAuthenticator *auth) {
    const Credentials credentials = credentialsFor(reply->url());
    auth->setUser(credentials.user);
    auth->setPassword(credentials.password);
});
```

该回调返回前必须填好 `QAuthenticator`，不能用 queued connection 等待另一个线程稍后填写。若需要用户交互，通常先取消请求、异步收集凭据，再重新发起，而不是在信号槽里开启阻塞对话框。

Manager 会缓存凭据。退出登录时应清理访问/认证缓存，并删除应用自己的 token。

Bearer/OAuth token 通常直接放 Header。遇到 401 时只允许一个刷新操作在途，其他请求排队；刷新成功后按幂等规则重发，失败则统一结束会话，避免“每个请求都同时刷新 token”的风暴。

## 9. Cookie 会话

`QNetworkAccessManager` 使用 `QNetworkCookieJar` 管理 Cookie，同一 Manager 的请求可共享会话。

```cpp
auto *jar = new QNetworkCookieJar(m_manager);
m_manager->setCookieJar(jar);
```

默认 CookieJar 主要是内存行为。需要跨启动持久化时应实现受控存储：

- 只保存允许持久化的 Cookie；
- 保留 domain、path、secure、expiry 等属性；
- 对敏感会话加密或交给系统凭据设施；
- 退出登录清除服务端会话和本地 Cookie；
- 不把不同账户/租户共用同一个 Jar。

Cookie 不是普通字符串字典，其匹配和过期规则应交给 Cookie API。

## 10. HTTP 缓存

启用磁盘缓存：

```cpp
auto *cache = new QNetworkDiskCache(m_manager);
cache->setCacheDirectory(
    QStandardPaths::writableLocation(QStandardPaths::CacheLocation)
    + QStringLiteral("/http"));
cache->setMaximumCacheSize(100 * 1024 * 1024);
m_manager->setCache(cache);
```

每请求控制：

```cpp
request.setAttribute(QNetworkRequest::CacheLoadControlAttribute,
                     QNetworkRequest::PreferCache);
request.setAttribute(QNetworkRequest::CacheSaveControlAttribute, true);
```

缓存遵从 HTTP 元信息，不等于完整离线数据库。需要确定性离线体验时，应把业务数据放入自己的持久层，记录版本、更新时间和同步状态。

不要缓存包含隐私或鉴权数据的响应，除非协议 Header 和本地安全策略明确允许。登出时评估是否清除缓存。

## 11. 系统代理与自定义代理

让 Qt 使用系统代理配置：

```cpp
QNetworkProxyFactory::setUseSystemConfiguration(true);
```

固定代理：

```cpp
QNetworkProxy proxy(QNetworkProxy::HttpProxy,
                    QStringLiteral("proxy.example.com"), 8080);
m_manager->setProxy(proxy);
```

需要按 URL 动态选择时使用 `QNetworkProxyFactory`。代理认证由 `proxyAuthenticationRequired` 同步填写凭据。

企业环境应测试 PAC、认证代理、无代理列表、HTTPS 隧道和证书替换。不要在源码硬编码代理密码。

## 12. 并发控制与请求合并

Manager 会按协议和 host 调度连接，但业务层仍需要限制：

- 同一资源的重复请求；
- 大文件同时下载数；
- API 服务的速率限制；
- UI 搜索抖动。

搜索可先 debounce：

```cpp
m_searchTimer.setSingleShot(true);
m_searchTimer.setInterval(250);
connect(&m_searchTimer, &QTimer::timeout,
        this, &Controller::startSearch);

void Controller::queryChanged(const QString &query)
{
    m_pendingQuery = query;
    m_searchTimer.start(); // 重启计时
}
```

相同 GET 可按规范化 URL 和相关 Header 形成 key，多个调用者共享一个在途请求结果。但取消要用订阅计数：一个调用者离开不应把其他调用者仍需要的共享 Reply abort。

## 13. 压缩响应与资源上限

服务端压缩可以显著减少带宽，但极高压缩比内容可能造成内存压力。Qt 6 提供解压安全阈值相关属性，可按可信度调整；更重要的是应用仍要限制：

- 最大响应字节数；
- JSON 数组/嵌套规模；
- 下载磁盘配额；
- 单 host 并发数；
- 解码后的图像尺寸。

不要只信任 `Content-Length`，它可能缺失或不代表解压后大小。流式读取时持续累计并在超过上限后 `abort()`。

## 14. 线程边界

`QNetworkAccessManager` 是 QObject，只能从其所属线程使用；它创建的 Reply 也在该线程。GUI 应用通常直接把 Manager 放在 GUI 线程，因为 API 本身异步，不会因为等待网络而阻塞界面。

不要为了“网络不能在主线程”机械移动 QNAM。真正可能耗时的是收到数据后的大规模解压、图像处理或 JSON/业务计算，这部分可把纯字节/值对象交给工作线程处理，再排队回 GUI 线程。

若确实创建专用网络线程，Manager 必须在该线程构造或正确移动，所有调用通过 queued signal/invoke 进入该线程，Reply 也只在那里操作。复杂度通常高于收益。

## 15. Qt 6.11 TCP Keepalive 延伸

Qt 6.11 为 `QNetworkRequest` 增加了 keepalive 探测参数，例如：

```cpp
request.setTcpKeepAliveIdleTimeBeforeProbes(60s);
request.setTcpKeepAliveIntervalBetweenProbes(10s);
request.setTcpKeepAliveProbeCount(3);
```

TCP keepalive 检测长时间静默连接是否已经失效，不替代应用级 HTTP 超时、心跳或总截止时间。默认参数与平台支持可能不同，只有长连接和特殊网络环境需要定制。

## 16. 错误模型应保留结构

不要只向 UI 发一个拼接字符串。可定义：

```cpp
enum class ErrorKind {
    Canceled,
    Timeout,
    Offline,
    Tls,
    Authentication,
    Http,
    Parse,
    Business
};

struct ApiError
{
    ErrorKind kind;
    QNetworkReply::NetworkError networkError;
    int httpStatus = 0;
    QString code;
    QString userMessage;
    QString diagnosticMessage;
    bool retryable = false;
};
```

用户信息、诊断信息和重试判断因此分离。UI 不需要理解 `HostNotFoundError`，日志也不必显示不友好的用户文案。

## 17. 可观测性与隐私

每次请求建议记录：

```text
request id、方法、去敏后的 host/path、耗时、状态码、错误分类、重试次数、响应大小
```

默认不要记录：

```text
Authorization、Cookie、完整查询参数、请求/响应正文、个人信息、密码、token
```

日志中的 URL 也可能含 token 或搜索内容。建立 Header 和字段白名单比事后找敏感词更可靠。

## 18. 测试网络层

### 18.1 不依赖公网

单元/集成测试应使用本地假服务器或可替换 transport，覆盖：

- 200 合法 JSON；
- 204 空正文；
- 400/401/404/429/500/503；
- 响应延迟和分块传输；
- 连接中途断开；
- 非法 JSON、字段缺失、超大响应；
- 重定向链与循环；
- 取消和截止时间；
- 并发响应乱序；
- TLS 测试证书。

真实外部 API 只适合少量端到端测试，因为公网、配额和第三方变化会让测试不稳定。

### 18.2 注入 Manager 或传输接口

```cpp
class ApiTransport
{
public:
    virtual ~ApiTransport() = default;
    virtual RequestHandle *getUsers(QObject *context) = 0;
};
```

UI/业务测试注入 fake，Qt Network 实现在集成测试中验证。不要试图伪造 `QNetworkReply` 的所有内部行为来测试每一层。

## 19. 常见错误

### 19.1 把 transfer timeout 当总耗时

持续有少量字节时不会触发。需要总截止时间就增加单独 QTimer。

### 19.2 对所有 POST 自动重试

可能产生重复订单、支付或消息。必须有幂等语义或服务端幂等键。

### 19.3 生产中 ignoreSslErrors

使客户端无法确认服务器身份，HTTPS 安全性基本失效。

### 19.4 旧搜索响应覆盖新响应

用 generation/request id 或取消旧请求，完成时再次确认结果仍然需要。

### 19.5 在认证信号中异步填写 authenticator

信号返回时凭据必须已经填入；queued 回调太晚。需要交互就取消后重新发起。

### 19.6 把缓存当离线数据库

HTTP 缓存可能被淘汰且受服务端 Header 控制。业务离线数据应有独立模型和同步策略。

### 19.7 跨线程直接调用 Manager

即使类文档标记某些函数 reentrant，单个 QObject 实例仍有线程归属。调用必须在 Manager 所属线程。

## 20. API 速查

| API                                   | 关键用途              |
| ------------------------------------- | ----------------- |
| `setTransferTimeout()`                | 无字节交换超时           |
| `QTimer` + `abort()`                  | 业务总截止时间           |
| `OperationCanceledError`              | 识别取消              |
| `RedirectPolicyAttribute`             | 单请求重定向策略          |
| `redirectAllowed()`                   | 用户验证模式下允许跳转       |
| `sslErrors()`                         | 报告 TLS 验证问题       |
| `setSslConfiguration()`               | 单请求 TLS 配置        |
| `setStrictTransportSecurityEnabled()` | 启用 HSTS           |
| `authenticationRequired()`            | 同步填写服务认证凭据        |
| `QNetworkCookieJar`                   | Cookie 会话         |
| `QNetworkDiskCache`                   | HTTP 磁盘缓存         |
| `QNetworkProxyFactory`                | 系统或动态代理           |
| `QPointer<QNetworkReply>`             | 安全保存可取消 Reply 引用  |
| TCP keepalive setters                 | Qt 6.11 长连接失效探测参数 |

## 21. 自测题

1. transfer timeout 与总截止时间有何区别？
2. abort 后是否还要处理 finished？
3. 为什么搜索请求需要 generation 标记？
4. 哪些 POST 可以安全自动重试？
5. Qt 默认重定向策略会允许 https 跳回 http 吗？
6. 为什么不能用 ignoreSslErrors 解决证书部署问题？
7. authenticationRequired 能否用 queued connection 稍后填写凭据？
8. QNetworkDiskCache 是否等价于业务离线数据库？
9. 异步 QNAM 为什么通常无需搬到工作线程？
10. TCP keepalive 是否能替代 HTTP 总截止时间？

## 22. 参考答案

1. transfer timeout 检测连续无字节交换；总截止时间限制从发起到结束的整体时长。
2. 要。abort 会使操作结束并发出 finished，统一清理仍在那里完成。
3. 并发响应可能乱序，旧请求最后回来时不能覆盖更新结果。
4. 本身幂等的操作，或服务端真正支持唯一幂等键且仍在重试预算内的操作。
5. 不允许。默认 NoLessSafe 策略禁止从 https 降级到 http。
6. 它跳过身份验证，使中间人也可能被接受；应修复证书链、信任根、主机名或系统时间。
7. 不能。信号返回前就必须填好 authenticator。
8. 不等价。HTTP 缓存可被淘汰且由缓存语义控制，业务离线数据需要自己的持久层。
9. QNAM 已异步等待网络，不阻塞事件循环；只把真正昂贵的后处理移到工作线程即可。
10. 不能。Keepalive 检测静默 TCP 连接，和业务请求总时限不是同一层语义。

## 23. 本篇结论

生产级网络层不是一组散落的 `get()` 调用，而是一套有边界的状态机：

```text
构造请求
  → 限流/合并/鉴权
  → 发送并设置传输超时与总截止时间
  → 成功、失败、取消、过期四类收尾
  → 仅对可重试且幂等的操作做有预算退避
  → 严格 TLS 与重定向策略
  → 结构化错误、脱敏日志和可替换测试传输
```

当生命周期、身份验证和重试策略集中在 ApiClient/Transport 层时，UI 只处理加载、数据、空状态和可理解的错误，网络行为也才能被系统测试。
