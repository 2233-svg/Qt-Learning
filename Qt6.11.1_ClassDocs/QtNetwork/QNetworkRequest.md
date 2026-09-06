# QNetworkRequest

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkRequest` 描述一次网络请求：URL、请求头、缓存策略、优先级和传输相关属性都放在这里。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkRequest` 描述一次网络请求：URL、请求头、缓存策略、优先级和传输相关属性都放在这里。

**内部模型：** 它是值类型，创建后传给 QNetworkAccessManager；请求对象本身不代表连接或响应。响应状态和错误要从 QNetworkReply 读取。

**适用场景：** 需要设置 URL、Content-Type、Authorization、User-Agent、缓存或重定向策略时使用。

**典型调用链：** 构造 URL -> setRawHeader/setHeader -> 按需设置属性 -> manager.get/post/request -> 从 reply 读取结果。

**先记住的坑：** 不要把敏感 token 写入日志；Content-Type 要和 body 匹配；URL 编码参数应使用 QUrlQuery；请求头和响应头是两个不同对象。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkRequest>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

它是值类型，创建后传给 QNetworkAccessManager；请求对象本身不代表连接或响应。响应状态和错误要从 QNetworkReply 读取。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

需要设置 URL、Content-Type、Authorization、User-Agent、缓存或重定向策略时使用。 使用时通常按这个过程组织：构造 URL -> setRawHeader/setHeader -> 按需设置属性 -> manager.get/post/request -> 从 reply 读取结果。

```cpp
QNetworkRequest request(QUrl("https://example.com/api"));
request.setHeader(QNetworkRequest::ContentTypeHeader,
                  QStringLiteral("application/json"));
request.setRawHeader("Authorization", "Bearer token");
QNetworkReply *reply = manager->post(request, jsonData);
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Attribute { HttpStatusCodeAttribute, HttpReasonPhraseAttribute, RedirectionTargetAttribute, ConnectionEncryptedAttribute, CacheLoadControlAttribute, …, UserMax }`
- `enum CacheLoadControl { AlwaysNetwork, PreferNetwork, PreferCache, AlwaysCache }`
- `enum KnownHeaders { ContentDispositionHeader, ContentTypeHeader, ContentLengthHeader, LocationHeader, LastModifiedHeader, …, ServerHeader }`
- `enum LoadControl { Automatic, Manual }`
- `enum Priority { HighPriority, NormalPriority, LowPriority }`
- `enum RedirectPolicy { ManualRedirectPolicy, NoLessSafeRedirectPolicy, SameOriginRedirectPolicy, UserVerifiedRedirectPolicy }`
- `enum TransferTimeoutConstant { DefaultTransferTimeoutConstant }`

### 公有函数

- `QNetworkRequest()`
- `QNetworkRequest(const QUrl &url)`
- `QNetworkRequest(const QNetworkRequest &other)`
- `~QNetworkRequest()`
- `QVariant attribute(QNetworkRequest::Attribute code, const QVariant &defaultValue = QVariant()) const`
- `(since 6.2) qint64 decompressedSafetyCheckThreshold() const`
- `bool hasRawHeader(QAnyStringView headerName) const`
- `QVariant header(QNetworkRequest::KnownHeaders header) const`
- `(since 6.8) QHttpHeaders headers() const`
- `(since 6.5) QHttp1Configuration http1Configuration() const`
- `QHttp2Configuration http2Configuration() const`
- `int maximumRedirectsAllowed() const`
- `QObject * originatingObject() const`
- `QString peerVerifyName() const`
- `QNetworkRequest::Priority priority() const`
- `QByteArray rawHeader(QAnyStringView headerName) const`
- `QList<QByteArray> rawHeaderList() const`
- `void setAttribute(QNetworkRequest::Attribute code, const QVariant &value)`
- `(since 6.2) void setDecompressedSafetyCheckThreshold(qint64 threshold)`
- `void setHeader(QNetworkRequest::KnownHeaders header, const QVariant &value)`
- `(since 6.8) void setHeaders(QHttpHeaders &&newHeaders)`
- `(since 6.8) void setHeaders(const QHttpHeaders &newHeaders)`
- `(since 6.5) void setHttp1Configuration(const QHttp1Configuration &configuration)`
- `void setHttp2Configuration(const QHttp2Configuration &configuration)`
- `void setMaximumRedirectsAllowed(int maxRedirectsAllowed)`
- `void setOriginatingObject(QObject *object)`
- `void setPeerVerifyName(const QString &peerName)`
- `void setPriority(QNetworkRequest::Priority priority)`
- `void setRawHeader(const QByteArray &headerName, const QByteArray &headerValue)`
- `void setSslConfiguration(const QSslConfiguration &config)`
- `(since 6.11) void setTcpKeepAliveIdleTimeBeforeProbes(std::chrono::seconds idle)`
- `(since 6.11) void setTcpKeepAliveIntervalBetweenProbes(std::chrono::seconds interval)`
- `(since 6.11) void setTcpKeepAliveProbeCount(int probes)`
- `void setTransferTimeout(int timeout)`
- `(since 6.7) void setTransferTimeout(std::chrono::milliseconds duration = DefaultTransferTimeout)`
- `void setUrl(const QUrl &url)`
- `QSslConfiguration sslConfiguration() const`
- `void swap(QNetworkRequest &other)`
- `(since 6.11) std::chrono::seconds tcpKeepAliveIdleTimeBeforeProbes() const`
- `(since 6.11) std::chrono::seconds tcpKeepAliveIntervalBetweenProbes() const`
- `(since 6.11) int tcpKeepAliveProbeCount() const`
- `int transferTimeout() const`
- `(since 6.7) std::chrono::milliseconds transferTimeoutAsDuration() const`
- `QUrl url() const`
- `bool operator!=(const QNetworkRequest &other) const`
- `QNetworkRequest & operator=(const QNetworkRequest &other)`
- `bool operator==(const QNetworkRequest &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QNetworkRequest::Attribute`

**作用与语义：**

`QNetworkRequest`和 `QNetworkReply` 的属性代码。
属性是额外的元数据，用于控制请求的行为，并将回复中的更多信息反馈给应用程序。属性也可扩展，允许自定义实现传递自定义值。
下表解释了默认属性码、关联的`QVariant`类型、如果该属性缺失的默认值，以及该值是否用于请求或回复。
- `QNetworkRequest::HttpStatusCodeAttribute`：`0`;仅回复，类型：`QMetaType::Int`（无默认）表示从HTTP服务器接收的HTTP状态码（如200、304、404、401等）。如果连接不是基于HTTP，则不存在该属性。
- `QNetworkRequest::HttpReasonPhraseAttribute`：`1`;仅回复，类型：`QMetaType::QByteArray`（无默认）表示来自HTTP服务器的HTTP理由短语（如“Ok”、“Found”、“Not Found”、“Access Denied”等）。这是状态码的人类可读表示（见上文）。如果连接不是基于HTTP，则该属性不存在。注意：使用HTTP/2时不使用理由短语。
- `QNetworkRequest::RedirectionTargetAttribute`：`2`;仅回复，类型：`QMetaType::QUrl`（无默认）如果存在，表示服务器正在将请求重定向到不同的URL。网络访问API默认会执行重定向，除非使用`QNetworkRequest::ManualRedirectPolicy`。此外，如果使用`QNetworkRequest::UserVerifiedRedirectPolicy`，则该属性将在未执行重定向时被设置。返回的URL可能是相对的。使用`QUrl::resolved()`将其创建一个绝对URL。
- `QNetworkRequest::ConnectionEncryptedAttribute`：`3`;仅回复，类型：`QMetaType::Bool`（默认：false）表示数据是否通过加密（安全）连接获得。
- `QNetworkRequest::CacheLoadControlAttribute`：`4`;仅请求，类型：`QMetaType::Int`（默认：`QNetworkRequest::PreferNetwork`）控制缓存的访问方式。可能的值为`QNetworkRequest::CacheLoadControl`。注意默认`QNetworkAccessManager`实现不支持缓存。然而，某些后端可能使用该属性修改请求（例如缓存代理）。
- `QNetworkRequest::CacheSaveControlAttribute`：`5`;仅请求，类型：`QMetaType::Bool`（默认：true）控制获得的数据是否应保存为缓存以备将来使用。如果值为假，获得的数据不会自动缓存。如果为真，数据可以缓存，前提是可缓存（可缓存内容取决于所用协议）。
- `QNetworkRequest::SourceIsFromCacheAttribute`：`6`;仅回复，类型：`QMetaType::Bool`（默认：false）表示数据是否来自缓存。
- `QNetworkRequest::DoNotBufferUploadDataAttribute`：`7`;仅请求，类型：`QMetaType::Bool`（默认：false）表示`QNetworkAccessManager`代码是否允许缓冲上传数据，例如执行HTTP POST时。使用该标志处理顺序上传数据时，必须设置`ContentLengthHeader`首部。
- `QNetworkRequest::HttpPipeliningAllowedAttribute`：`8`;仅请求，类型：`QMetaType::Bool`（默认：false）表示`QNetworkAccessManager`代码是否允许对此请求使用 HTTP 流水线。
- `QNetworkRequest::HttpPipeliningWasUsedAttribute`: `9`；仅限回复，类型：`QMetaType::Bool` 指示在接收此回复时是否使用了 HTTP 管道技术。
- `QNetworkRequest::CustomVerbAttribute`: `10`；仅限请求，类型：`QMetaType::QByteArray` 保存要发送的自定义 HTTP 动词的值（用于除 GET、POST、PUT 和 DELETE 之外的其他动词）。此动词在调用 `QNetworkAccessManager::sendCustomRequest()` 时设置。
- `QNetworkRequest::CookieLoadControlAttribute`: `11`；仅限请求，类型：`QMetaType::Int`（默认：`QNetworkRequest::Automatic`） 指示是否在请求中发送 'Cookie' 头。当创建跨域 XMLHttpRequest 时，如果创建请求的 JavaScript 未显式将 withCredentials 设置为 true，该属性会被 Qt WebKit 设置为 false。详情请参阅此处。（该值在 4.7 引入。）
- `QNetworkRequest::CookieSaveControlAttribute`: `13`；仅限请求，类型：`QMetaType::Int`（默认：`QNetworkRequest::Automatic`） 指示是否将从服务器收到的 'Cookie' 头保存为回复的一部分。当创建跨域 XMLHttpRequest 时，如果创建请求的 JavaScript 未显式将 withCredentials 设置为 true，该属性会被 Qt WebKit 设置为 false。详情请参阅此处。（该值在 4.7 引入。）
- `QNetworkRequest::AuthenticationReuseAttribute`: `12`；仅限请求，类型：`QMetaType::Int`（默认：`QNetworkRequest::Automatic`） 指示是否在请求中使用缓存的授权凭据（如果可用）。如果设置为 `QNetworkRequest::Manual`，并且认证机制为 'Basic' 或 'Digest'，Qt 不会使用请求 URL 的任何缓存凭据发送 'Authorization' HTTP 头。当创建跨域 XMLHttpRequest 时，如果创建请求的 JavaScript 未显式将 withCredentials 设置为 true，该属性会被 Qt WebKit 设置为 `QNetworkRequest::Manual`。详情请参阅此处。（该值在 4.7 引入。）
- `QNetworkRequest::BackgroundRequestAttribute`: `17`；类型：`QMetaType::Bool`（默认：false） 指示这是后台传输，而非用户发起的传输。根据平台不同，后台传输可能受不同策略约束。
- `QNetworkRequest::Http2AllowedAttribute`: `19`；仅限请求，类型：`QMetaType::Bool`（默认：true） 指示 `QNetworkAccessManager` 代码是否被允许在此请求中使用 HTTP/2。这适用于 SSL 请求或如果设置了 Http2CleartextAllowedAttribute 的“明文”HTTP/2。
- `QNetworkRequest::Http2WasUsedAttribute`: `20`；仅限回复，类型：`QMetaType::Bool`（默认：false） 指示在接收此回复时是否使用了 HTTP/2。（该值在 5.9 引入。）
- `QNetworkRequest::EmitAllUploadProgressSignalsAttribute`: `18`；仅限请求，类型：`QMetaType::Bool`（默认：false） 指示是否应触发所有上传信号。默认情况下，uploadProgress 信号仅每 100 毫秒触发一次。（该值在 5.5 引入。）
- `QNetworkRequest::OriginalContentLengthAttribute`: `21`；仅限回复，类型 `QMetaType::Int` 保存原始 content-length 属性，在数据被压缩且请求标记为自动解压时，该属性将被作废并从头部移除。（该值在 5.9 引入。）
- `QNetworkRequest::RedirectPolicyAttribute`：`22`;仅请求，类型：`QMetaType::Int`，应为`QNetworkRequest::RedirectPolicy`值之一（默认值：`NoLessSafeRedirectPolicy`）。（该值于 5.9 版本引入。）
- `QNetworkRequest::Http2DirectAttribute`：`23`;仅请求，类型：`QMetaType::Bool`（默认：false）如果设置，该属性将强制`QNetworkAccessManager`在不进行初始HTTP/2协议协商的情况下使用HTTP/2协议。使用该属性意味着事先知道某服务器支持HTTP/2。该属性支持SSL，若设置了Http2CleartextAllowedAttribute，则支持“明文”HTTP/2。如果服务器不支持HTTP/2，且指定了HTTP/2直接，`QNetworkAccessManager`放弃，不尝试回退到HTTP/1.1。如果 Http2AllowedAttribute 和 Http2DirectAttribute 都被设置，Http2DirectAttribute 将优先。（该值于 5.11 版本引入。）
- `QNetworkRequest::AutoDeleteReplyOnFinishAttribute`：`25`;仅请求，类型：`QMetaType::Bool`（默认：false）如果设置，该属性会`QNetworkAccessManager`在发出“完成”后删除`QNetworkReply`。（该值于 5.14 版本引入。）
- `QNetworkRequest::ConnectionCacheExpiryTimeoutSecondsAttribute`：在`26`;仅请求，类型：`QMetaType::Int` 设置在处理最后一个待处理请求后，TCP连接（HTTP1和HTTP2）何时关闭。（该值于6.3版本引入。）
- `QNetworkRequest::Http2CleartextAllowedAttribute`：`27`;仅请求，类型：`QMetaType::Bool`（默认：false）如果设置，该属性会告诉`QNetworkAccessManager`尝试通过明文（也称为h2c）升级到HTTP/2。直到Qt 7，该属性的默认值可以通过设置QT_NETWORK_H2C_ALLOWED环境变量被覆盖为真。如果Http2AllowedAttribute未被设置，该属性将被忽略。（该值于6.3版本引入。）
- `QNetworkRequest::UseCredentialsAttribute`：`28`;仅请求，类型：`QMetaType::Bool`（默认：false）表示底层的XMLHttp请求跨站访问控制请求是否应使用凭证发起。对同源请求无影响。这仅影响WebAssembly平台。（该值于6.5引入。）
- `QNetworkRequest::FullLocalServerNameAttribute`：`29`;仅请求，类型：QMetaType：：String 包含用于底层`QLocalSocket`的完整本地服务器名称。当`QLocalSocket`仅仅使用简单名称的行为时，`QNetworkAccessManager`会用该属性连接特定的本地服务器。`QNetworkRequest`中的 URL 仍必须使用 Unix http： 或本地 http： 方案。URL 中的主机名将用作 HTTP 请求中的 Host 头。（该值于 6.8 版本引入。）
- `QNetworkRequest::User`：有`1000`;特殊类型。QVariants中可以传递从User到UserMax的类型的更多信息。Network Access的默认实现会忽略该范围内的任何请求属性，且不会在回复中生成该范围内的任何属性。该范围保留给`QNetworkAccessManager`的扩展。
- `QNetworkRequest::UserMax`：`32767`;特殊类型。参见用户。

### `enum QNetworkRequest::CacheLoadControl`

**作用与语义：**

控制`QNetworkAccessManager`的缓存机制。
- `QNetworkRequest::AlwaysNetwork`：`0`;始终从网络加载，不检查缓存是否有有效条目（类似于浏览器中的“重新加载”功能）;此外，强制中间缓存重新验证。
- `QNetworkRequest::PreferNetwork`：`1`;默认值;如果缓存的条目比网络条目更早，则从网络加载。这不会从缓存中返回过期数据，但会重新验证已过期的资源。
- `QNetworkRequest::PreferCache`：`2`;如果有缓存，则从缓存加载，否则从网络加载。注意，这可能会从缓存中返回可能过期（但非过期）的项目。
- `QNetworkRequest::AlwaysCache`：`3`;仅从缓存加载，若未缓存（即离线模式）则提示错误

### `enum QNetworkRequest::KnownHeaders`

**作用与语义：**

已知 `QNetworkRequest` 解析的头类型列表。每个已知头也以其完整的 HTTP 名称的原始形式表示。
- `QNetworkRequest::ContentDispositionHeader`: `6`; 对应 HTTP 的 Content-Disposition 头，包含一个字符串，该字符串包含处置类型（例如 attachment）和一个参数（例如 filename）。
- `QNetworkRequest::ContentTypeHeader`: `0`; 对应 HTTP 的 Content-Type 头，包含一个字符串，该字符串包含媒体（MIME）类型及任何辅助数据（例如 charset）。
- `QNetworkRequest::ContentLengthHeader`: `1`; 对应 HTTP 的 Content-Length 头，包含传输数据的字节长度。
- `QNetworkRequest::LocationHeader`: `2`; 对应 HTTP 的 Location 头，包含表示数据实际位置的 URL，包括重定向的目标 URL。
- `QNetworkRequest::LastModifiedHeader`: `3`; 对应 HTTP 的 Last-Modified 头，包含一个 `QDateTime`，表示内容的最后修改日期。
- `QNetworkRequest::IfModifiedSinceHeader`: `9`; 对应 HTTP 的 If-Modified-Since 头，包含一个 `QDateTime`。通常附加在 `QNetworkRequest` 上。如果资源自此时间以来未更改，服务器应发送 304（未修改）响应。
- `QNetworkRequest::ETagHeader`: `10`; 对应 HTTP 的 ETag 头，包含一个 `QString`，表示内容的最后修改状态。
- `QNetworkRequest::IfMatchHeader`: `11`; 对应 HTTP 的 If-Match 头，包含一个 `QStringList`。通常附加在 `QNetworkRequest` 上。如果资源不匹配，服务器应发送 412（前置条件失败）响应。
- `QNetworkRequest::IfNoneMatchHeader`: `12`; 对应 HTTP 的 If-None-Match 头，包含一个 `QStringList`。通常附加在 `QNetworkRequest` 上。如果资源匹配，服务器应发送 304（未修改）响应。
- `QNetworkRequest::CookieHeader`: `4`; 对应 HTTP 的 Cookie 头，包含一个 `QList`<`QNetworkCookie`>，表示要发送回服务器的 cookie。
- `QNetworkRequest::SetCookieHeader`: `5`; 对应 HTTP 的 Set-Cookie 头，包含一个 `QList`<`QNetworkCookie`>，表示服务器发送的需本地存储的 cookie。
- `QNetworkRequest::UserAgentHeader`: `7`; HTTP 客户端发送的 User-Agent 头。
- `QNetworkRequest::ServerHeader`: `8`; HTTP 客户端接收到的 Server 头。

### `enum QNetworkRequest::LoadControl`

**作用与语义：**

表示请求加载机制的某个方面是否被手动覆盖，例如被 Qt WebKit 覆盖。
- `QNetworkRequest::Automatic`：`0`;默认值：表示默认行为。
- `QNetworkRequest::Manual`：`1`;表示行为已被手动覆盖。

### `enum QNetworkRequest::Priority`

**作用与语义：**

该枚举列出了可能的网络请求优先级。
- `QNetworkRequest::HighPriority`：`1`;高优先级
- `QNetworkRequest::NormalPriority`：`3`;普通优先级
- `QNetworkRequest::LowPriority`：`5`;低优先级

### `enum QNetworkRequest::RedirectPolicy`

**作用与语义：**

指示网络访问API是否应自动跟随HTTP重定向响应。
- `QNetworkRequest::ManualRedirectPolicy`：`0`;不遵循任何重定向。
- `QNetworkRequest::NoLessSafeRedirectPolicy`：`1`;默认值：仅允许“http”->“http”、“http” ->“https”或“https” ->“https”重定向。
- `QNetworkRequest::SameOriginRedirectPolicy`：`2`;要求使用相同的协议、主机和端口。注意，http://example.com 和 http://example.com:80 在此策略下会失败（隐式/显式端口被视为不匹配）。
- `QNetworkRequest::UserVerifiedRedirectPolicy`：`3`;客户端通过处理重定向()信号决定是否跟随每个重定向，对`QNetworkReply`对象发出redirectAllowed()以允许重定向，或通过中止/完成该重定向以拒绝重定向。例如，这可以用来询问用户是否接受重定向，或根据某些应用特定的配置做出决定。
注意：当 Qt 处理重定向时，出于遗留和兼容性原因，当服务器返回 301 或 302 响应时，无论原始方法为何，Qt 都会通过 GET 发出重定向请求，除非是 HEAD。

### `enum QNetworkRequest::TransferTimeoutConstant`

**作用与语义：**

一个常量，可用于启用预设值的传输超时。
- `QNetworkRequest::DefaultTransferTimeoutConstant`：`30000`;传输超时（毫秒）。如果`setTransferTimeout()`被调用且无参数。

### `QNetworkRequest::QNetworkRequest()`

**作用与语义：**

构造一个没有请求URL的QNetworkRequest对象。使用`setUrl()`设置一个URL。

### `[explicit] QNetworkRequest::QNetworkRequest(const QUrl &url)`

**作用与语义：**

构建一个QNetworkRequest对象，`url`作为请求的URL。

### `QNetworkRequest::QNetworkRequest(const QNetworkRequest &other)`

**作用与语义：**

创建`other`副本。

### `[noexcept] QNetworkRequest::~QNetworkRequest()`

**作用与语义：**

处理`QNetworkRequest`物品。

### `QVariant QNetworkRequest::attribute(QNetworkRequest::Attribute code, const QVariant &defaultValue = QVariant()) const`

**作用与语义：**

返回与代码`code`关联的属性。如果该属性尚未设置，则返回`defaultValue`。
注意：该功能不适用于`QNetworkRequest::Attribute`中列出的默认设置。

### `[since 6.2] qint64 QNetworkRequest::decompressedSafetyCheckThreshold() const`

**作用与语义：**

返回档案炸弹检定的阈值。
如果回复的解压长度小于此，Qt 会直接解压，无需进一步检查。

### `bool QNetworkRequest::hasRawHeader(QAnyStringView headerName) const`

**作用与语义：**

如果该网络请求中存在原始头部`headerName`，则返回`true`。
注意：在 6.7 之前的 Qt 版本中，该功能仅使用 `QByteArray`。

### `QVariant QNetworkRequest::header(QNetworkRequest::KnownHeaders header) const`

**作用与语义：**

如果该请求中`header`已知的网络头部存在，返回该值。如果不存在，返回QVariant()（即无效变体）。

### `[since 6.8] QHttpHeaders QNetworkRequest::headers() const`

**作用与语义：**

返回该网络请求中设置的头部。

### `[since 6.5] QHttp1Configuration QNetworkRequest::http1Configuration() const`

**作用与语义：**

返回`QNetworkAccessManager`当前用于该请求底层HTTP/1连接的参数。

### `QHttp2Configuration QNetworkRequest::http2Configuration() const`

**作用与语义：**

返回`QNetworkAccessManager`当前用于该请求及其底层HTTP/2连接的参数。这要么是应用程序事先设置的配置，要么是默认配置。
`QNetworkAccessManager`使用的默认值是：
- 连接级流量控制的窗口大小为2147483647八位元组
- 溪流级流量控制的窗口大小为214748364八位节
- 最大帧尺寸为16384
默认情况下，服务器推送被禁用，Huffman 压缩和字符串索引被启用。

### `int QNetworkRequest::maximumRedirectsAllowed() const`

**作用与语义：**

返回该请求允许遵循的最大重定向次数。

### `QObject *QNetworkRequest::originatingObject() const`

**作用与语义：**

返回发起该网络请求的对象引用;如果未设置或对象已被销毁，返回`nullptr`。

### `QString QNetworkRequest::peerVerifyName() const`

**作用与语义：**

返回由`setPeerVerifyName`设置的证书验证主机名称。默认情况下，返回一个空字符串。

### `QNetworkRequest::Priority QNetworkRequest::priority() const`

**作用与语义：**

将此请求的优先权归还。

### `QByteArray QNetworkRequest::rawHeader(QAnyStringView headerName) const`

**作用与语义：**

返回原始的`headerName`头。如果不存在此类头部，则返回空`QByteArray`，可能与存在但无内容的头部无法区分（使用`hasRawHeader()`来判断该头是否存在）。
原始头部可以用`setRawHeader()`或`setHeader()`设置。
注意：在6.7之前的Qt版本中，该功能仅使用`QByteArray`。

### `QList<QByteArray> QNetworkRequest::rawHeaderList() const`

**作用与语义：**

返回该网络请求中设置的所有原始头部列表。列表按头部设置顺序排列。

### `void QNetworkRequest::setAttribute(QNetworkRequest::Attribute code, const QVariant &value)`

**作用与语义：**

将与代码`code`关联的属性设置为值`value`。如果属性已经设置，则丢弃之前的值。特别地，如果`value`是无效`QVariant`，则该属性为未设置。

### `[since 6.2] void QNetworkRequest::setDecompressedSafetyCheckThreshold(qint64 threshold)`

**作用与语义：**

设定档案炸弹检定的`threshold`。
一些支持的压缩算法可以在极小的压缩文件中编码出极其庞大的解压文件。这只有在解压后内容极其单调时才可能实现，而真实文件若以善意传输，这种情况很少发生：执行如此高压缩比的文件通常是缓冲区超载攻击或拒绝服务攻击（占用过多内存）的有效载体。因此，解压到巨大体积的文件，尤其是从极小压缩形式中解压的文件，最好被视为疑似恶意软件而被排除。
如果回复的解压大小大于该阈值（默认为10 MiB，即10 * 1024 * 1024），Qt会检查压缩比：如果压缩比过大（GZip和Deflate为40：1，Brotli和ZStandard为100：1），则该回复将被视为错误。将阈值设置为`-1`会禁用此检查。

### `void QNetworkRequest::setHeader(QNetworkRequest::KnownHeaders header, const QVariant &value)`

**作用与语义：**

将已知`header`头的值设置为`value`，覆盖之前设置的任何头部。该操作还设置等效的原始 HTTP 头部。

### `[since 6.8] void QNetworkRequest::setHeaders(QHttpHeaders &&newHeaders)`

**作用与语义：**

将`newHeaders`设置为该网络请求中的头部，覆盖之前设置的任何头部。
如果某些头对应已知头，则会解析这些值，并设置相应的解析形式。

### `[since 6.8] void QNetworkRequest::setHeaders(const QHttpHeaders &newHeaders)`

**作用与语义：**

将`newHeaders`设置为该网络请求中的头部，覆盖之前设置的任何头部。
如果某些头对应已知头，则会解析这些值，并设置相应的解析形式。

### `[since 6.5] void QNetworkRequest::setHttp1Configuration(const QHttp1Configuration &configuration)`

**作用与语义：**

从`configuration`设置请求的HTTP/1参数。

### `void QNetworkRequest::setHttp2Configuration(const QHttp2Configuration &configuration)`

**作用与语义：**

从`configuration`设置请求的HTTP/2参数。
注意：必须在提出请求前设置好配置。
注意：HTTP/2 在单一 HTTP/2 连接中复用多个流。这意味着`QNetworkAccessManager`会使用第一个请求中发现的配置，来自发送到同一主机的一系列请求。

### `void QNetworkRequest::setMaximumRedirectsAllowed(int maxRedirectsAllowed)`

**作用与语义：**

设置该请求`maxRedirectsAllowed`允许遵循的最大重定向次数。

### `void QNetworkRequest::setOriginatingObject(QObject *object)`

**作用与语义：**

允许设置指向发起请求的`object`的引用。
例如，Qt WebKit 将发起对象设置为发起请求的 QWebFrame。

### `void QNetworkRequest::setPeerVerifyName(const QString &peerName)`

**作用与语义：**

将`peerName`设置为证书验证的主机名，而不是用于TCP连接的主机名。

### `void QNetworkRequest::setPriority(QNetworkRequest::Priority priority)`

**作用与语义：**

将此请求的优先级设置为`priority`。
注意：`priority`只是给网络访问管理器的一个提示。它可以使用也可以不使用。目前它用于HTTP决定应先发送哪个请求给服务器。

### `void QNetworkRequest::setRawHeader(const QByteArray &headerName, const QByteArray &headerValue)`

**作用与语义：**

将头部`headerName`设置为值为`headerValue`。如果`headerName`对应于已知头部（参见 `QNetworkRequest::KnownHeaders`），则会解析原始格式，并设置相应的“煮熟”头部。
还会将已知的首部`LastModifiedHeader`设置为解析日期的`QDateTime`对象。
注意：设置同一个头部重复会覆盖之前的设置。为了实现多个同名 HTTP 头的行为，你应将两个值连接起来，用逗号（“，”）分隔，并设置一个单一原始头部。
注意：自Qt 6.8起，头字段名称通过转换为小写字母进行规范化。

**官方示例：**

```cpp
 request.setRawHeader(QByteArray("Last-Modified"), QByteArray("Sun, 06 Nov 1994 08:49:37 GMT"));
```

### `void QNetworkRequest::setSslConfiguration(const QSslConfiguration &config)`

**作用与语义：**

将该网络请求的 SSL 配置设置为`config`。适用的设置包括私钥、本地证书、TLS 协议（例如 TLS 1.3）、CA 证书以及 SSL 后端允许使用的密码。

### `[since 6.11] void QNetworkRequest::setTcpKeepAliveIdleTimeBeforeProbes(std::chrono::seconds idle)`

**作用与语义：**

如果TCP保持在线功能已开启，则将连接在TCP开始发送保活探测前的空闲时间设置为`idle`。

### `[since 6.11] void QNetworkRequest::setTcpKeepAliveIntervalBetweenProbes(std::chrono::seconds interval)`

**作用与语义：**

如果启用了TCP保持在线功能，设置单个保持活探测之间的时间为`interval`。

### `[since 6.11] void QNetworkRequest::setTcpKeepAliveProbeCount(int probes)`

**作用与语义：**

设置TCP在断开连接前应发送的最大保持活数`probes`如果TCP保持活功能已开启。

### `void QNetworkRequest::setTransferTimeout(int timeout)`

**作用与语义：**

将`timeout`设置为毫秒级的传输超时。

### `[since 6.7] void QNetworkRequest::setTransferTimeout(std::chrono::milliseconds duration = DefaultTransferTimeout)`

**作用与语义：**

设置超时`duration`，如果没有数据交换，则中止传输。
如果在超时结束前没有传输任何字节，传输将被中止。为零表示没有设置定时器。如果没有参数，超时为`QNetworkRequest::DefaultTransferTimeout`。如果未调用该函数，超时被禁用，值为零。

### `void QNetworkRequest::setUrl(const QUrl &url)`

**作用与语义：**

设置该网络请求所指的URL为`url`。

### `QSslConfiguration QNetworkRequest::sslConfiguration() const`

**作用与语义：**

返回该网络请求的SSL配置。默认情况下，这和`QSslConfiguration::defaultConfiguration()`相同。

### `[noexcept] void QNetworkRequest::swap(QNetworkRequest &other)`

**作用与语义：**

将该网络请求与`other`交换。该操作非常快速且从未失败。

### `[since 6.11] std::chrono::seconds QNetworkRequest::tcpKeepAliveIdleTimeBeforeProbes() const`

**作用与语义：**

如果TCP保持功能已开启，返回连接在TCP开始发送保活探测前需要保持空闲的时间。

### `[since 6.11] std::chrono::seconds QNetworkRequest::tcpKeepAliveIntervalBetweenProbes() const`

**作用与语义：**

如果启用了TCP保持在线功能，返回单个保持活探测之间的时间。

### `[since 6.11] int QNetworkRequest::tcpKeepAliveProbeCount() const`

**作用与语义：**

如果启用了TCP保持在线功能，返回TCP在断开连接前应发送的最大探测次数。

### `int QNetworkRequest::transferTimeout() const`

**作用与语义：**

返回传输时使用的超时，单位为毫秒。
如果`transferTimeoutAsDuration()`.count()无法用`int`表示，则该函数返回`INT_MAX`/`INT_MIN`。

### `[since 6.7] std::chrono::milliseconds QNetworkRequest::transferTimeoutAsDuration() const`

**作用与语义：**

返回超时时间，逾时如果没有数据交换，传输将中止。
默认时长为零，意味着不使用超时。

### `QUrl QNetworkRequest::url() const`

**作用与语义：**

返回该网络请求所指的URL。

### `bool QNetworkRequest::operator!=(const QNetworkRequest &other) const`

**作用与语义：**

如果此对象与 `other` 不同，则返回 `false`。

### `QNetworkRequest &QNetworkRequest::operator=(const QNetworkRequest &other)`

**作用与语义：**

创建了`other`的副本。

### `bool QNetworkRequest::operator==(const QNetworkRequest &other) const`

**作用与语义：**

如果该对象与`other`相同（即拥有相同的URL、相同头部和相同的元数据设置），返回`true`。

### `const std::chrono::std::chrono::milliseconds QNetworkRequest::DefaultTransferTimeout`

**作用与语义：**

传输超时为`QNetworkRequest::TransferTimeoutConstant`毫秒。如果调用`setTransferTimeout()`且未进行参数。

## 6. 深入实践与常见坑

### 生命周期和资源边界

manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

### 状态和错误边界

请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

### 线程边界

QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

### 最容易出现的错误

不要把敏感 token 写入日志；Content-Type 要和 body 匹配；URL 编码参数应使用 QUrlQuery；请求头和响应头是两个不同对象。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QNetworkRequest` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
