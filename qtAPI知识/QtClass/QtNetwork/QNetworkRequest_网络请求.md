# QNetworkRequest：一次网络请求的 URL、头与传输策略

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkRequest>`  
> CMake：`Qt6::Network`  
> 类型：隐式共享值类型

## 它解决什么问题

`QNetworkRequest` 是交给 `QNetworkAccessManager` 的请求描述：目标 URL、HTTP 头、缓存与 Cookie 行为、重定向策略、SSL 配置、协议偏好、超时和优先级等都在这里定义。

它不执行网络 I/O。调用 `manager.get(request)`、`post()`、`put()` 或 `sendCustomRequest()` 时，管理器读取当前请求对象的值并创建 `QNetworkReply`；随后再修改原 `QNetworkRequest` 不会回头改变已经发出的操作。

## 实际使用场景

- 给单个 HTTP 请求设置 `Accept`、`Content-Type`、条件请求头和自定义业务头。
- 设置缓存偏好、禁止自动缓存，或判断回复是否来自缓存。
- 约束允许的重定向方向，避免 HTTPS 降级或跨源跳转。
- 为特定请求配置 TLS、HTTP/1、HTTP/2、传输空闲超时和优先级。
- 在 WebAssembly 或本地 HTTP 协议场景中使用平台特定属性。

把 request 视为“提交前的不可变配置快照”最容易维护。需要发送相似请求时，使用 `QNetworkRequestFactory` 生成多个独立 request，而不是在多线程间共享并修改同一个对象。

## 基本工作流

```cpp
#include <QNetworkAccessManager>
#include <QNetworkRequest>

QNetworkRequest request(
    QUrl(QStringLiteral("https://api.example.com/v1/items")));
request.setHeader(QNetworkRequest::UserAgentHeader,
                  QStringLiteral("ExampleClient/1.0"));
request.setRawHeader("Accept", "application/json");
request.setAttribute(QNetworkRequest::RedirectPolicyAttribute,
                     QNetworkRequest::NoLessSafeRedirectPolicy);
request.setTransferTimeout(std::chrono::seconds(20));

QNetworkReply *reply = manager.get(request);
```

请求一旦提交，所有状态读取、错误处理、数据读取和删除策略都围绕 `reply` 展开。若 request 设置 `AutoDeleteReplyOnFinishAttribute`，`finished` 发出后 reply 可能由 manager 自动销毁，槽中不要保留裸指针等待以后使用。

## 关键语义与边界

### 头部：已知头、raw 头和 `QHttpHeaders`

`KnownHeaders` 为常见 HTTP 头提供 Qt 类型化表示，例如 `ContentLengthHeader` 对应字节数、`LastModifiedHeader` 对应 `QDateTime`、`CookieHeader` / `SetCookieHeader` 对应 `QList<QNetworkCookie>`。

`setHeader()` / `header()` 适合这些已知类型；`setRawHeader()` / `rawHeader()` 适合任意字节形式头。Qt 6.8 起，`setHeaders()` / `headers()` 提供 `QHttpHeaders` 批量接口。读取不存在的已知头返回无效 `QVariant`，不存在的 raw header 返回空 `QByteArray`，需要时先用 `hasRawHeader()` 区分“没有该头”和“该头值为空”。

不要将语义上不可逗号合并的重复 HTTP 头手工拼接。特别是多条 `Set-Cookie` 应使用能保留多值的接口或单独头字段，而不是简单字符串拼接。

### Attribute 的默认值有两层含义

`attribute(code, defaultValue)` 只返回实际存入 request 的值，未设置时原样返回你传入的 `defaultValue`；它**不会自动代入** `Attribute` 文档中列出的框架行为默认值。

因此，若业务逻辑需要判断“是否显式配置”，调用 `attribute(code)` 并检查 `QVariant::isValid()`；若需要实际传输行为，需结合该 attribute 的文档默认值和 manager 配置判断。

### 缓存、Cookie 与认证是独立开关

- `CacheLoadControlAttribute` 决定读缓存倾向，`CacheSaveControlAttribute` 决定结果是否可自动写缓存。
- `CookieLoadControlAttribute` 和 `CookieSaveControlAttribute` 控制发出/接收 Cookie，使用 `Automatic` 或 `Manual`。
- `AuthenticationReuseAttribute` 为 `Manual` 时，Basic/Digest 请求不会自动复用该 URL 的已缓存认证头。

没有安装适当 cache 后端或缓存型代理时，缓存偏好不意味着一定有命中。`SourceIsFromCacheAttribute` 是 reply 侧结果，不能在发出前当作预测。

### 重定向要显式选择安全模型

默认 `NoLessSafeRedirectPolicy` 只允许 `http -> http`、`http -> https`、`https -> https`，阻止 HTTPS 降级。`SameOriginRedirectPolicy` 要求协议、主机和端口完全相同，`http://example.com` 与 `http://example.com:80` 也被视为不匹配。

`ManualRedirectPolicy` 完全不自动跟随；`UserVerifiedRedirectPolicy` 要求应用响应 `QNetworkReply::redirected()`，再调用 `redirectAllowed()` 或终止 reply。注意兼容性规则：Qt 自动处理 301/302 时，除 HEAD 外会用 GET 发起后续请求，即使原方法是 POST。

### 超时是“没有数据进展”而非总时限

`setTransferTimeout()` 的 timer 在指定时间内没有任何字节传输时中止请求。它不是整个请求从开始到结束的墙钟上限；慢但持续有数据进展的下载不会因此超时。

未调用时请求级超时关闭，值为 0。显式传入 0 同样禁用 timer；无参数调用使用 `DefaultTransferTimeout`，即 30000 ms。`transferTimeout()` 的 `int` 版本在值无法表示时会饱和到 `INT_MAX` / `INT_MIN`，需要精确时使用 `transferTimeoutAsDuration()`。

### HTTP 版本与连接会话

`Http2AllowedAttribute` 默认允许 HTTP/2。`Http2DirectAttribute` 只应在已知服务端支持 HTTP/2 时设置：若服务端不支持，Qt 不会回退到 HTTP/1.1。明文 h2c 还需要 `Http2CleartextAllowedAttribute`，且后者在 HTTP/2 被禁用时没有作用。

`setHttp1Configuration()`（Qt 6.5 起）和 `setHttp2Configuration()` 作用于连接建立。相同 host:port 的会话一旦由第一条请求建立，后续请求不能重新定义那条已存在连接的配置；把这些设置放在目标主机的第一条请求之前。

### SSL、证书名称与上传缓冲

`setSslConfiguration()` 为此 request 覆盖默认 TLS 配置。`setPeerVerifyName()` 设置用于证书验证的主机名，默认是 null 字符串；仅在明确知道验证名应与 URL host 不同的受控场景设置，不能用它绕过证书验证。

`DoNotBufferUploadDataAttribute=true` 禁止 manager 缓冲上传数据。若上传 `QIODevice` 是顺序设备，必须同时设置 `ContentLengthHeader`，否则 manager 无法正确发送内容长度。

### Qt 6.11 TCP keep-alive

`tcpKeepAliveIdleTimeBeforeProbes()`、`tcpKeepAliveIntervalBetweenProbes()` 和 `tcpKeepAliveProbeCount()` 及其 setter 自 Qt 6.11 起可为请求配置 TCP keep-alive 探测参数。它们是对底层连接的偏好，最终效果还受操作系统和网络后端支持限制；不要把它们当作应用协议心跳的替代品。

## Attribute 速查

| Attribute | 方向与要点 |
| --- | --- |
| `HttpStatusCodeAttribute` | reply：HTTP 状态码；非 HTTP 时不存在。 |
| `HttpReasonPhraseAttribute` | reply：HTTP 原因短语；HTTP/2 不使用。 |
| `RedirectionTargetAttribute` | reply：重定向目标，可能是相对 URL，需用 `resolved()` 绝对化。 |
| `ConnectionEncryptedAttribute` | reply：是否经加密连接取得，默认 `false`。 |
| `CacheLoadControlAttribute` | request：缓存读取策略，默认 `PreferNetwork`。 |
| `CacheSaveControlAttribute` | request：是否允许自动保存到缓存，默认 `true`。 |
| `SourceIsFromCacheAttribute` | reply：是否来自缓存，默认 `false`。 |
| `DoNotBufferUploadDataAttribute` | request：禁用上传缓冲；顺序上传设备必须指定 `Content-Length`。 |
| `HttpPipeliningAllowedAttribute` | request：允许 HTTP pipelining，默认 `false`。 |
| `HttpPipeliningWasUsedAttribute` | reply：实际是否使用 HTTP pipelining。 |
| `CustomVerbAttribute` | request：自定义 HTTP 方法，由 `sendCustomRequest()` 设置。 |
| `CookieLoadControlAttribute` | request：发送 Cookie 的自动/手动控制。 |
| `AuthenticationReuseAttribute` | request：复用认证缓存的自动/手动控制。 |
| `CookieSaveControlAttribute` | request：保存响应 Cookie 的自动/手动控制。 |
| `MaximumDownloadBufferSizeAttribute` / `DownloadBufferAttribute` / `SynchronousRequestAttribute` / `ResourceTypeAttribute` | 内部属性；应用代码不要依赖。 |
| `BackgroundRequestAttribute` | request：标记后台传输，平台可能施加不同策略。 |
| `EmitAllUploadProgressSignalsAttribute` | request：默认 upload progress 约每 100 ms 发一次；设为真要求全部信号。 |
| `Http2AllowedAttribute` / `Http2WasUsedAttribute` | request：允许 HTTP/2（默认真） / reply：实际使用 HTTP/2。 |
| `OriginalContentLengthAttribute` | reply：自动解压后原始 `Content-Length`。 |
| `RedirectPolicyAttribute` | request：重定向策略，默认 `NoLessSafeRedirectPolicy`。 |
| `Http2DirectAttribute` | request：直接使用 HTTP/2，不协商也不回退；须事先确认服务端支持。 |
| `AutoDeleteReplyOnFinishAttribute` | request：`finished` 发出后由 manager 删除 reply，默认 `false`。 |
| `ConnectionCacheExpiryTimeoutSecondsAttribute` | request：最后一个待处理请求后多久关闭对应 HTTP/1/HTTP/2 TCP 连接。 |
| `Http2CleartextAllowedAttribute` | request：允许 h2c 升级，默认 `false`；依赖 `Http2AllowedAttribute`。 |
| `UseCredentialsAttribute` | 仅 WebAssembly：跨站 XHR 是否使用凭据；同源无影响。 |
| `FullLocalServerNameAttribute` | request：Qt 6.8 起，为 `unix+http` / `local+http` 指定完整本地服务名；URL host 仍用于 HTTP Host 头。 |
| `User` ... `UserMax` | 扩展保留范围；默认网络访问实现忽略。 |

## 常见误区

- **请求发出后继续改 request**：不会修改已经创建的 reply。
- **把 transfer timeout 当作总下载时限**：它只检测无字节进展。
- **依靠 `attribute()` 自动返回框架默认**：函数只返回已设置值或调用方提供的 default。
- **将 `Http2DirectAttribute` 当作“优先 HTTP/2”**：它是强制且无回退。
- **启用自动删 reply 后延迟使用裸指针**：`finished` 后对象可能已被销毁。
- **禁用上传缓冲却不设置顺序设备的长度**：请求无法正确处理。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 构造 | `QNetworkRequest()` / `QNetworkRequest(url)` | 创建无 URL / 指定 URL 的请求描述。 |
| 值语义 | 拷贝构造、拷贝/移动赋值、`swap(other)` | 隐式共享值操作；发出后修改原对象不影响已提交请求。 |
| 比较 | `operator==(other)` / `operator!=(other)` | 比较请求描述值。 |
| URL | `url()` / `setUrl(url)` | 读取/设置目标 URL。 |
| 批量头 | `headers()` / `setHeaders(const QHttpHeaders &)` / `setHeaders(QHttpHeaders &&)` | Qt 6.8 起读写结构化 HTTP 头。 |
| 已知头 | `header(known)` / `setHeader(known, value)` | 读写 `KnownHeaders` 的类型化表示；不存在读取无效 `QVariant`。 |
| 原始头 | `hasRawHeader(name)` / `rawHeader(name)` / `rawHeaderList()` / `setRawHeader(name, value)` | 管理 raw HTTP 头；Qt 6.7 前部分查询参数为 `QByteArray`。 |
| 属性 | `attribute(code, defaultValue)` / `setAttribute(code, value)` | 读取/设置 attribute；读取不会代入框架文档默认值。 |
| SSL | `sslConfiguration()` / `setSslConfiguration(config)` | 读取/设置此请求 TLS 配置；仅在启用 SSL 的构建中提供。 |
| TLS 名称 | `peerVerifyName()` / `setPeerVerifyName(name)` | 读取/设置证书验证名；默认 null 字符串。 |
| 关联 | `originatingObject()` / `setOriginatingObject(object)` | 附加来源 QObject 标记，供调用方关联请求来源；不用于资源所有权。 |
| 调度 | `priority()` / `setPriority(priority)` | 设置高、普通、低优先级。 |
| 重定向 | `maximumRedirectsAllowed()` / `setMaximumRedirectsAllowed(max)` | 读取/设置最多允许的跳转数。 |
| HTTP/1 | `http1Configuration()` / `setHttp1Configuration(config)` | Qt 6.5 起；为新建 HTTP/1 会话配置，连接已建立后无法重定义。 |
| HTTP/2 | `http2Configuration()` / `setHttp2Configuration(config)` | 为新建 HTTP/2 会话配置，连接已建立后无法重定义。 |
| 解压防护 | `decompressedSafetyCheckThreshold()` / `setDecompressedSafetyCheckThreshold(threshold)` | Qt 6.2 起；设置归档炸弹解压检查阈值。 |
| TCP keep-alive | `tcpKeepAliveIdleTimeBeforeProbes()` / `setTcpKeepAliveIdleTimeBeforeProbes()` | Qt 6.11 起；读取/设置空闲多久后开始探测。 |
| TCP keep-alive | `tcpKeepAliveIntervalBetweenProbes()` / `setTcpKeepAliveIntervalBetweenProbes()` | Qt 6.11 起；读取/设置探测间隔。 |
| TCP keep-alive | `tcpKeepAliveProbeCount()` / `setTcpKeepAliveProbeCount()` | Qt 6.11 起；读取/设置探测次数。 |
| 超时 | `setTransferTimeout(int)` / `setTransferTimeout(milliseconds)` | 设置无传输进展超时；0 禁用，无参数为 30000 ms。 |
| 超时 | `transferTimeout()` / `transferTimeoutAsDuration()` | 读取超时；后者避免 `int` 饱和。 |
| 常量 | `DefaultTransferTimeoutConstant` / `DefaultTransferTimeout` | 默认预设 transfer timeout，均表示 30000 ms。 |

## 相关类型

- `QNetworkAccessManager`：提交 request 并产生 reply。
- `QNetworkReply`：携带请求执行结果及 reply-side attributes。
- `QNetworkRequestFactory`：批量生成带共同配置的 request。
- `QHttpHeaders`、`QSslConfiguration`、`QHttp1Configuration`、`QHttp2Configuration`：请求的结构化子配置。
