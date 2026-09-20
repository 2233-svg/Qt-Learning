# QNetworkAccessManager：异步网络访问的中心对象

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkAccessManager>`  
> CMake：`Qt6::Network`  
> 继承：`QObject`

## 它解决什么问题

`QNetworkAccessManager` 负责把 `QNetworkRequest` 变成实际的网络操作，并返回对应的 `QNetworkReply`。它集中管理一组请求共用的配置：

- 代理与代理工厂；
- Cookie Jar；
- HTTP 缓存；
- HSTS 策略及其持久化；
- 重定向策略、自动删除 reply 和传输超时；
- 认证、TLS 错误和完成通知。

它是异步 API 的调度中心，不是一个“请求函数调用完就得到响应”的同步客户端。`get()`、`post()` 等函数只负责排队并返回 reply；响应体、状态码、头部和错误要在 reply 的信号或 `finished()` 中读取。

## 实际使用场景

- 一个桌面应用共享一个 manager，发起 REST、文件下载和上传请求。
- 一个 API 客户端统一使用代理、Cookie、缓存、TLS 和超时策略。
- 通过认证回调响应 HTTP/代理认证挑战。
- 通过 `QNetworkDiskCache` 和 HSTS store 保持跨请求、跨进程启动的部分网络状态。
- 通过派生 `createRequest()` 记录请求、注入统一行为或接入自定义协议实现。

一个 manager 通常足够整个应用使用，但它只能在自己所属的线程中调用。需要多个线程并发访问时，应为每个线程创建属于该线程的 manager，而不是从多个线程直接调用同一个实例。

## 基本下载流程

```cpp
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>

auto *manager = new QNetworkAccessManager(this);

QObject::connect(manager, &QNetworkAccessManager::finished,
                 this, [](QNetworkReply *reply) {
    if (reply->error() == QNetworkReply::NoError)
        qDebug() << reply->readAll();
    else
        qWarning() << reply->errorString();

    reply->deleteLater();
});

manager->get(QNetworkRequest(
    QUrl(QStringLiteral("https://example.com/data.json"))));
```

也可以把处理连接到单个 reply 的 `readyRead()`、`downloadProgress()`、`errorOccurred()` 和 `finished()`。不要在 `finished()` 槽里直接 `delete reply`；使用 `deleteLater()`，让 Qt 在安全的事件循环时机销毁它。

## 请求并发与连接复用

manager 会对收到的请求排队，实际并行数取决于协议。Qt 6.11.1 桌面 HTTP 对同一个 host/port 通常同时执行 6 个请求；该数字不是应用级保证，也不应当作为服务端限流或业务并发控制。

HTTP/1.1 和 HTTP/2 连接会被复用。`clearConnectionCache()` 只清理连接，不清理认证数据；`clearAccessCache()` 同时清理认证数据和网络连接，适合测试、注销或切换身份时使用。

## 关键语义与边界

### reply 的所有权

manager 创建的 `QNetworkReply` 默认以 manager 为父对象，manager 析构时会一并销毁仍归它所有的 reply。请求完成后，应用负责在适当时机释放 reply，通常是 `reply->deleteLater()`。

`setAutoDeleteReplies(true)` 会让未来请求的 reply 在发出 `finished()` 后自动删除；单个 request 上显式设置 `AutoDeleteReplyOnFinishAttribute` 可以覆盖 manager 的默认值。启用后不要把 reply 裸指针保存到 finished 之后，也不要在 finished 槽中再次删除它。

### 上传设备与 multipart 的生命周期

使用 `post()`、`put()` 或 `sendCustomRequest()` 上传 `QIODevice` 时，设备必须在调用时已打开供读取，并一直有效到该 reply 的 `finished()`。manager 不应被假定为会替应用延长任意设备的生命周期。

`QHttpMultiPart` 也必须存活到请求完成。常见做法是在取得 reply 后把 multipart 设为 reply 的子对象：

```cpp
auto *multipart = new QHttpMultiPart(QHttpMultiPart::FormDataType);
// append parts ...

QNetworkReply *reply = manager->post(request, multipart);
multipart->setParent(reply);
```

`QHttpPart` 不拥有其 body device；使用 `setBodyDevice()` 时，底层 device 也必须保持有效到请求结束。异步上传中不要把 stack 上的临时 `QBuffer`、文件或 multipart 当作长期有效对象。

### 认证回调必须同步填写

`authenticationRequired()` 和 `proxyAuthenticationRequired()` 传入的 `QAuthenticator` 必须在信号返回前填写。不能用 queued connection，否则网络栈在回调返回时还拿不到凭据。

manager 会缓存成功使用的凭据；后续同一服务器或代理再次挑战时可能自动复用而不发信号。服务端拒绝后才会再次发信号。若回调不设置 user/password，服务器认证会失败并以 `AuthenticationRequiredError` 结束。

### 预连接接口不能报告错误

`connectToHost()` 和 `connectToHostEncrypted()` 只用于提前完成 TCP 或 TCP+TLS 握手，让随后的 HTTP 请求降低首包延迟。它们没有返回 reply，也没有错误报告接口；真正请求仍需通过 `get()` 等函数观察结果。

HTTPS 版本的 `peerName` 重载允许将证书验证名设置为指定值。启用 HTTP/2 预连接时，TLS 配置应包含 `QSslConfiguration::ALPNProtocolHTTP2`；HTTP/2 每个 host 通常一条连接就足够，多次预连接不会线性提速。

### HSTS 是管理器级策略

HSTS 默认关闭。`setStrictTransportSecurityEnabled(true)` 后，manager 会根据服务端响应和 `addStrictTransportSecurityHosts()` 提供的已知策略限制不安全访问。服务端返回的 `Strict-Transport-Security` 可能更新、覆盖或移除已有策略。

`enableStrictTransportSecurityStore(true, dir)` 开启持久化 store；默认目录是 `QStandardPaths::CacheLocation`，传入空目录且该位置不可写时可能退回工作目录。若已有内存策略，开启 store 时会保留并可能覆盖同 host 的旧磁盘值。若希望启动时优先读取 store，应在启用 HSTS 前开启 store。

### 缓存和 Cookie 是可插拔对象，manager 取得所有权

`setCache()` 和 `setCookieJar()` 都会取得传入对象的所有权。对象与 manager 同线程时，manager 会把它们设为子对象。交出后不要再用独立 owner 删除。

如果要在多个 manager 间共享 cookie jar 或 cache，必须明确解除父子关系并处理线程限制；同一个 QObject 不能同时属于多个线程，也不能被多个 manager 无同步地并发使用。

### 代理配置只影响未来操作

`setProxy()` 影响未来请求；已经发送的请求不受影响。需要按 URL、协议或目标主机选择不同代理时，使用 `setProxyFactory()`。代理认证通过 `proxyAuthenticationRequired()` 处理。

### 默认超时是空闲传输超时

manager 级 `setTransferTimeout()` 只在指定时间内没有字节传输时中止操作，不是从请求开始到完成的总耗时。请求级非零 timeout 会覆盖 manager 级设置；若 manager 已启用 timeout，要让某个请求无超时，不能只依靠请求默认值，而应明确在 manager/request 层设置为 0。

### SSL 错误不能盲目忽略

`sslErrors()` 只报告证书或 TLS 错误；调用 `ignoreSslErrors()` 会绕过对应检查，应仅对明确可接受、经过验证的错误使用，不能用来“修复”生产证书问题。`encrypted()` 表示初始握手完成且尚未发送用户数据，但连接复用时不保证每个 reply 都发出该信号。

## 各操作的语义

| 操作 | 语义 |
| --- | --- |
| `head()` | 只取得响应头，不请求响应体。 |
| `get()` | 取得响应头和响应体；Qt 6.7 起可带 GET body，但带 body 的 GET 不缓存，重定向时只有 308 保留 body。 |
| `post()` | 提交数据；HTTP 表单通常使用 POST。顺序 `QIODevice` 必须保持有效。 |
| `put()` | 上传到目标 URL；HTTP 服务端常常不允许 PUT，是否返回响应体由协议决定。 |
| `deleteResource()` | 发送资源删除操作；当前主要用于 HTTP DELETE。 |
| `sendCustomRequest()` | 发送自定义 HTTP 方法，例如 OPTIONS；verb 必须符合 HTTP 规范，当前主要支持 HTTP(S)。 |

## 常见误区

- **把 `get()` 返回值当作响应数据**：返回的是异步 `QNetworkReply`。
- **在 `finished()` 里直接 delete reply**：使用 `deleteLater()`。
- **上传临时设备后立即离开作用域**：设备必须活到 reply 完成。
- **认证信号使用 queued connection**：凭据来不及填入，认证失败。
- **以为 `clearConnectionCache()` 会清掉密码**：它保留认证数据；需要 `clearAccessCache()`。
- **把 manager 的并行数当作业务并发上限**：协议和平台会影响实际调度。
- **以为 `connectToHost()` 能报告错误**：预连接接口没有错误报告。
- **用 `ignoreSslErrors()` 绕过未知证书问题**：这会削弱 TLS 安全边界。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 枚举 | `Operation` | 描述 reply 的操作类型。 |
| 枚举值 | `HeadOperation` | `head()` 创建的只取头部操作。 |
| 枚举值 | `GetOperation` | `get()` 创建的下载操作。 |
| 枚举值 | `PutOperation` | `put()` 创建的上传操作。 |
| 枚举值 | `PostOperation` | `post()` 创建的提交操作。 |
| 枚举值 | `DeleteOperation` | `deleteResource()` 创建的删除操作。 |
| 枚举值 | `CustomOperation` | `sendCustomRequest()` 创建的自定义方法操作。 |
| 构造/析构 | `QNetworkAccessManager(parent)` / `~QNetworkAccessManager()` | 创建网络访问中心；析构释放资源并删除仍归其所有的 reply、cache、cookie jar 等子对象。 |
| 方案 | `supportedSchemes()` | 返回 manager 支持的 URL scheme；可重写以声明自定义协议支持。 |
| 连接缓存 | `clearAccessCache()` | 清理认证数据和网络连接缓存。 |
| 连接缓存 | `clearConnectionCache()` | 只清理网络连接缓存，认证数据保留。 |
| 代理 | `proxy()` / `setProxy(proxy)` | 读取/设置未来请求使用的静态代理；已发请求不变。 |
| 代理 | `proxyFactory()` / `setProxyFactory(factory)` | 读取/设置按 query 选代理的 factory；返回指针由 manager 管理，不能自行删除。 |
| 缓存 | `cache()` / `setCache(cache)` | 读取/设置 `QAbstractNetworkCache`；manager 取得传入 cache 的所有权。 |
| Cookie | `cookieJar()` / `setCookieJar(jar)` | 读取/设置 Cookie Jar；manager 取得 jar 所有权。 |
| HSTS | `setStrictTransportSecurityEnabled(enabled)` / `isStrictTransportSecurityEnabled()` | 启用/查询 HSTS 执行；默认关闭。 |
| HSTS store | `enableStrictTransportSecurityStore(enabled, storeDir)` | 启用/禁用 HSTS 持久化；空目录使用标准缓存目录或平台回退目录。 |
| HSTS store | `isStrictTransportSecurityStoreEnabled()` | 查询 HSTS 持久化 store 是否启用。 |
| HSTS | `addStrictTransportSecurityHosts(knownHosts)` | 导入已知策略；过期策略会移除同 host 记录，服务端响应可更新已有策略。 |
| HSTS | `strictTransportSecurityHosts()` | 返回当前 manager 的 HSTS 策略列表。 |
| HEAD | `head(request)` | 异步发送 HEAD，只取得响应头。 |
| GET | `get(request)` | 异步下载响应头和正文。 |
| GET | `get(request, QIODevice *data)` | Qt 6.7 起发送带设备 body 的 GET；设备须保持有效，带 body 的 GET 不缓存。 |
| GET | `get(request, QByteArray data)` | Qt 6.7 起发送带字节 body 的 GET；重定向时仅 308 保留 body。 |
| POST | `post(request, QIODevice *data)` | 上传顺序设备内容；设备调用时须可读并保持有效到 finished。 |
| POST | `post(request, QByteArray data)` | 上传字节数组内容。 |
| POST | `post(request, QHttpMultiPart *multiPart)` | 发送 MIME multipart；multipart 和其 body device 必须保持有效到请求完成。 |
| POST | `post(request, nullptr)` | Qt 6.8 起发送无 body 的 POST，避免与空字节数组重载混淆。 |
| PUT | `put(request, QIODevice *data)` | 上传设备内容；响应体是否可读由协议决定。 |
| PUT | `put(request, QByteArray data)` | 上传字节数组内容。 |
| PUT | `put(request, QHttpMultiPart *multiPart)` | 发送 MIME multipart PUT；multipart 及 body device 需保持有效。 |
| PUT | `put(request, nullptr)` | Qt 6.8 起发送无 body 的 PUT。 |
| DELETE | `deleteResource(request)` | 异步发送资源删除操作；当前主要支持 HTTP DELETE。 |
| 自定义 | `sendCustomRequest(request, verb, QIODevice *data)` | 发送自定义 HTTP 方法；设备须可读并保持有效到完成。 |
| 自定义 | `sendCustomRequest(request, verb, QByteArray data)` | 发送自定义方法及字节 body。 |
| 自定义 | `sendCustomRequest(request, verb, QHttpMultiPart *multiPart)` | 发送自定义方法的 MIME multipart；当前主要用于 HTTP(S)。 |
| 预连接 | `connectToHost(host, port)` | 提前建立 TCP 连接以降低后续 HTTP 延迟；没有错误报告。 |
| 预连接 | `connectToHostEncrypted(host, port, sslConfiguration)` | 提前建立 TCP+TLS；没有错误报告。 |
| 预连接 | `connectToHostEncrypted(host, port, sslConfiguration, peerName)` | 用指定证书验证名提前建立 HTTPS 连接；没有错误报告。 |
| 重定向 | `redirectPolicy()` / `setRedirectPolicy(policy)` | 读取/设置未来请求的默认重定向策略。 |
| reply 生命周期 | `autoDeleteReplies()` / `setAutoDeleteReplies(autoDelete)` | 读取/设置未来 reply 是否在 finished 后自动删除；request attribute 可逐请求覆盖。 |
| 超时 | `transferTimeout()` / `setTransferTimeout(int)` | 读取/设置无字节传输进展的超时；0 禁用。 |
| 超时 | `transferTimeoutAsDuration()` / `setTransferTimeout(milliseconds)` | Qt 6.7 起的 duration 版本；默认无参数为 30000 ms。 |
| 认证 | `authenticationRequired(reply, authenticator)` | 服务器认证挑战；必须同步填写 authenticator，不能 queued。 |
| 代理认证 | `proxyAuthenticationRequired(proxy, authenticator)` | 代理认证挑战；manager 可能缓存成功凭据。 |
| 完成 | `finished(reply)` | 任意 pending reply 完成；不要直接 delete reply，使用 deleteLater。 |
| TLS | `encrypted(reply)` | 初始 TLS 握手成功且尚未发送用户数据；连接复用时不保证每个 reply 都有。 |
| TLS | `sslErrors(reply, errors)` | 报告 TLS/证书错误；只有明确验证后才考虑 ignoreSslErrors。 |
| PSK | `preSharedKeyAuthenticationRequired(reply, authenticator)` | PSK 握手需要凭据时发出；authenticator 由 reply 所有，不能删除。 |
| 扩展 | `createRequest(op, request, outgoingData)` | 受保护虚函数；自定义 reply/协议或注入行为的扩展点，返回对象必须处于打开状态。 |
| 扩展 | `supportedSchemesImplementation()` | 受保护槽，供 `supportedSchemes()` 的默认实现获取支持的 schemes。 |

## 相关类型

- `QNetworkRequest`：单次请求的 URL、头部和请求级策略。
- `QNetworkReply`：异步响应、正文、错误和 reply-side 属性。
- `QNetworkCookieJar`：Cookie 存储和 URL 选择策略。
- `QAbstractNetworkCache`：缓存后端接口。
- `QNetworkProxy` / `QNetworkProxyFactory`：静态或按查询选择代理。
- `QHstsPolicy`：HSTS 主机策略。
