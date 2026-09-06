# QNetworkAccessManager

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkAccessManager` 是 Qt 异步网络请求的调度中心，通常一个应用或一个网络服务对象持有一个实例。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkAccessManager` 是 Qt 异步网络请求的调度中心，通常一个应用或一个网络服务对象持有一个实例。

**内部模型：** 请求返回 QNetworkReply，真正结果通过 finished/readyRead/errorOccurred 等事件通知。manager 不会同步返回响应，也不应在每个请求里重复创建。

**适用场景：** HTTP/HTTPS GET、POST、上传下载、代理、缓存和 cookie 管理使用。必须在有事件循环的线程中运行。

**典型调用链：** 创建 manager -> 构造 QNetworkRequest -> get/post -> 连接 reply/manager 信号 -> 读取状态码和 body -> deleteLater reply。

**先记住的坑：** 不要在 finished 前释放 reply；检查 HTTP 状态码和 network error 两套错误；HTTPS 要处理 sslErrors；大响应使用 readyRead 分段读取。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkAccessManager>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

请求返回 QNetworkReply，真正结果通过 finished/readyRead/errorOccurred 等事件通知。manager 不会同步返回响应，也不应在每个请求里重复创建。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

HTTP/HTTPS GET、POST、上传下载、代理、缓存和 cookie 管理使用。必须在有事件循环的线程中运行。 使用时通常按这个过程组织：创建 manager -> 构造 QNetworkRequest -> get/post -> 连接 reply/manager 信号 -> 读取状态码和 body -> deleteLater reply。

```cpp
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QUrl>

QNetworkAccessManager *manager = new QNetworkAccessManager(this);
QNetworkReply *reply = manager->get(QNetworkRequest(QUrl("https://example.com")));
connect(reply, &QNetworkReply::finished, this, [reply] {
    const QByteArray body = reply->readAll();
    reply->deleteLater();
});
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Operation { HeadOperation, GetOperation, PutOperation, PostOperation, DeleteOperation, CustomOperation }`

### 公有函数

- `QNetworkAccessManager(QObject *parent = nullptr)`
- `virtual ~QNetworkAccessManager()`
- `void addStrictTransportSecurityHosts(const QList<QHstsPolicy> &knownHosts)`
- `bool autoDeleteReplies() const`
- `QAbstractNetworkCache * cache() const`
- `void clearAccessCache()`
- `void clearConnectionCache()`
- `void connectToHost(const QString &hostName, quint16 port = 80)`
- `void connectToHostEncrypted(const QString &hostName, quint16 port = 443, const QSslConfiguration &sslConfiguration = QSslConfiguration::defaultConfiguration())`
- `void connectToHostEncrypted(const QString &hostName, quint16 port, const QSslConfiguration &sslConfiguration, const QString &peerName)`
- `QNetworkCookieJar * cookieJar() const`
- `QNetworkReply * deleteResource(const QNetworkRequest &request)`
- `void enableStrictTransportSecurityStore(bool enabled, const QString &storeDir = QString())`
- `QNetworkReply * get(const QNetworkRequest &request)`
- `(since 6.7) QNetworkReply * get(const QNetworkRequest &request, QIODevice *data)`
- `(since 6.7) QNetworkReply * get(const QNetworkRequest &request, const QByteArray &data)`
- `QNetworkReply * head(const QNetworkRequest &request)`
- `bool isStrictTransportSecurityEnabled() const`
- `bool isStrictTransportSecurityStoreEnabled() const`
- `QNetworkReply * post(const QNetworkRequest &request, QIODevice *data)`
- `QNetworkReply * post(const QNetworkRequest &request, QHttpMultiPart *multiPart)`
- `QNetworkReply * post(const QNetworkRequest &request, const QByteArray &data)`
- `(since 6.8) QNetworkReply * post(const QNetworkRequest &request, std::nullptr_t nptr)`
- `QNetworkProxy proxy() const`
- `QNetworkProxyFactory * proxyFactory() const`
- `QNetworkReply * put(const QNetworkRequest &request, QIODevice *data)`
- `QNetworkReply * put(const QNetworkRequest &request, QHttpMultiPart *multiPart)`
- `QNetworkReply * put(const QNetworkRequest &request, const QByteArray &data)`
- `(since 6.8) QNetworkReply * put(const QNetworkRequest &request, std::nullptr_t nptr)`
- `QNetworkRequest::RedirectPolicy redirectPolicy() const`
- `QNetworkReply * sendCustomRequest(const QNetworkRequest &request, const QByteArray &verb, QIODevice *data = nullptr)`
- `QNetworkReply * sendCustomRequest(const QNetworkRequest &request, const QByteArray &verb, QHttpMultiPart *multiPart)`
- `QNetworkReply * sendCustomRequest(const QNetworkRequest &request, const QByteArray &verb, const QByteArray &data)`
- `void setAutoDeleteReplies(bool shouldAutoDelete)`
- `void setCache(QAbstractNetworkCache *cache)`
- `void setCookieJar(QNetworkCookieJar *cookieJar)`
- `void setProxy(const QNetworkProxy &proxy)`
- `void setProxyFactory(QNetworkProxyFactory *factory)`
- `void setRedirectPolicy(QNetworkRequest::RedirectPolicy policy)`
- `void setStrictTransportSecurityEnabled(bool enabled)`
- `void setTransferTimeout(int timeout)`
- `(since 6.7) void setTransferTimeout(std::chrono::milliseconds duration = QNetworkRequest::DefaultTransferTimeout)`
- `QList<QHstsPolicy> strictTransportSecurityHosts() const`
- `virtual QStringList supportedSchemes() const`
- `int transferTimeout() const`
- `(since 6.7) std::chrono::milliseconds transferTimeoutAsDuration() const`

### 信号

- `void authenticationRequired(QNetworkReply *reply, QAuthenticator *authenticator)`
- `void encrypted(QNetworkReply *reply)`
- `void finished(QNetworkReply *reply)`
- `void preSharedKeyAuthenticationRequired(QNetworkReply *reply, QSslPreSharedKeyAuthenticator *authenticator)`
- `void proxyAuthenticationRequired(const QNetworkProxy &proxy, QAuthenticator *authenticator)`
- `void sslErrors(QNetworkReply *reply, const QList<QSslError> &errors)`

### 保护函数

- `virtual QNetworkReply * createRequest(QNetworkAccessManager::Operation op, const QNetworkRequest &originalReq, QIODevice *outgoingData = nullptr)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QNetworkAccessManager::Operation`

**作用与语义：**

表示该回复正在处理的操作。
- `QNetworkAccessManager::HeadOperation`：`1`;检索头部操作（用`head()`创建）
- `QNetworkAccessManager::GetOperation`：`2`;检索头部并下载内容（用`get()`创建）
- `QNetworkAccessManager::PutOperation`：`3`;上传内容操作（用`put()`创建）
- `QNetworkAccessManager::PostOperation`：`4`;通过HTTP POST（用`post()`创建）发送HTML表单内容进行处理
- `QNetworkAccessManager::DeleteOperation`：`5`;删除内容操作（用`deleteResource()`创建）
- `QNetworkAccessManager::CustomOperation`：`6`;自定义操作（用`sendCustomRequest()`创建）

### `[explicit] QNetworkAccessManager::QNetworkAccessManager(QObject *parent = nullptr)`

**作用与语义：**

构建一个 QNetworkAccessManager 对象，作为网络访问 API 的核心，并将 `parent` 设定为父对象。

### `[virtual noexcept] QNetworkAccessManager::~QNetworkAccessManager()`

**作用与语义：**

它会销毁`QNetworkAccessManager`对象并释放所有资源。注意，从该类返回的`QNetworkReply`对象的父对象设为该对象，这意味着如果你不调用`QObject::setParent()`，它们会被删除。

### `void QNetworkAccessManager::addStrictTransportSecurityHosts(const QList<QHstsPolicy> &knownHosts)`

**作用与语义：**

在 HSTS 缓存中添加 HTTP 严格传输安全策略。`knownHosts` 包含已知拥有`QHstsPolicy`信息的主机。
注意：策略过期会从缓存中移除已知主机（如果之前存在的话）。
注意：在处理HTTP响应时，`QNetworkAccessManager`也可以更新HSTS缓存，移除或更新退出策略或引入新的`knownHosts`。因此，当前实现是服务器驱动的，客户端代码可以提供`QNetworkAccessManager`已知或发现的策略，但这些信息可以被“严格传输安全”响应头覆盖。

### `[signal] void QNetworkAccessManager::authenticationRequired(QNetworkReply *reply, QAuthenticator *authenticator)`

**作用与语义：**

每当最终服务器在交付请求内容前请求认证时，都会发出该信号。连接到该信号的槽应填满`authenticator`对象内容的凭据（可通过检查`reply`对象确定）。
`QNetworkAccessManager`会在内部缓存凭证，如果服务器再次要求认证，也会发送相同的值，但不会发出AuthenticationRequired()信号。如果拒绝凭证，该信号会再次发出。
注意：要避免请求发送凭证，必须不调用 setUser() 或 setPassword() 对 `authenticator` 对象。这样会导致 `finished()` 信号发出带有错误 `AuthenticationRequiredError` 的`QNetworkReply`。
注意：无法使用队列连接连接该信号，因为如果信号返回时认证器未输入新信息，连接将失败。

### `bool QNetworkAccessManager::autoDeleteReplies() const`

**作用与语义：**

如果`QNetworkAccessManager`当前配置为自动删除QNetworkRereplyes，则返回true;否则返回false。

### `QAbstractNetworkCache *QNetworkAccessManager::cache() const`

**作用与语义：**

返回用于存储从网络获取数据的缓存。

### `void QNetworkAccessManager::clearAccessCache()`

**作用与语义：**

清除内部的认证数据缓存和网络连接。
这个功能对做自动测试很有用。

### `void QNetworkAccessManager::clearConnectionCache()`

**作用与语义：**

清除网络连接的内部缓存。与`clearAccessCache()`不同，认证数据被保留。

### `void QNetworkAccessManager::connectToHost(const QString &hostName, quint16 port = 80)`

**作用与语义：**

在端口`port`发起`hostName`与主机的连接。此功能有助于在HTTP请求发出前完成与主机的TCP握手，从而降低网络延迟。
注意：该功能无法报告错误。

### `void QNetworkAccessManager::connectToHostEncrypted(const QString &hostName, quint16 port = 443, const QSslConfiguration &sslConfiguration = QSslConfiguration::defaultConfiguration())`

**作用与语义：**

通过`sslConfiguration`发起与`port`端口 `hostName` 提供的主机的连接。此功能有助于在 HTTPS 请求发出前完成与主机的 TCP 和 SSL 握手，从而降低网络延迟。
注意：预连接 HTTP/2 连接可以通过在允许协议列表中调用 setAllowedNextProtocols() 来实现`sslConfiguration` `QSslConfiguration::ALPNProtocolHTTP2`。使用 HTTP/2 时，每个主机只需连接一次，也就是说，多个主机多次调用此方法不会导致更快的网络事务。
注意：该功能无法报告错误。

### `void QNetworkAccessManager::connectToHostEncrypted(const QString &hostName, quint16 port, const QSslConfiguration &sslConfiguration, const QString &peerName)`

**作用与语义：**

在端口`port`发起`hostName`与主机的连接，使用`sslConfiguration`，`peerName`设置为用于证书验证的主机名。此功能有助于在发送HTTPS请求前完成与主机的TCP和SSL握手，从而降低网络延迟。
注意：预连接 HTTP/2 连接可以通过调用 setAllowedNextProtocols() 在允许协议列表中`sslConfiguration` `QSslConfiguration::ALPNProtocolHTTP2`实现。使用 HTTP/2 时，每个主机只需一次连接，也就是说，每台主机多次调用此方法不会导致更快的网络事务。
注意：该功能无法报告错误。

### `QNetworkCookieJar *QNetworkAccessManager::cookieJar() const`

**作用与语义：**

返回用于存储从网络获取的Cookie以及即将发送的Cookie的`QNetworkCookieJar`。

### `[virtual protected] QNetworkReply *QNetworkAccessManager::createRequest(QNetworkAccessManager::Operation op, const QNetworkRequest &originalReq, QIODevice *outgoingData = nullptr)`

**作用与语义：**

返回一个新的`QNetworkReply`对象以处理操作`op`和请求`originalReq`。对于获取请求和首`outgoingData`请求，设备总是为0，但在这些操作中传递给`post()`和`put()`的值（`QByteArray`变体会传递`QBuffer`对象）。
默认实现调用在 `setCookieJar()` 的 cookie jar 上`QNetworkCookieJar::cookiesForUrl()`，以获取发送到远程服务器的 cookie。
返回的对象必须处于开放状态。

### `QNetworkReply *QNetworkAccessManager::deleteResource(const QNetworkRequest &request)`

**作用与语义：**

发送删除由`request` URL识别的资源的请求。
注意：此功能目前仅适用于HTTP，执行HTTP DELETE请求。

### `void QNetworkAccessManager::enableStrictTransportSecurityStore(bool enabled, const QString &storeDir = QString())`

**作用与语义：**

如果`enabled` `true`，内部HSTS缓存将使用持久存储来读写HSTS策略。`storeDir`定义了该存储器的位置。默认位置由`QStandardPaths::CacheLocation`定义。如果没有可写的QStandartPaths：：CacheLocation且`storeDir`为空字符串，存储将位于程序的工作目录中。
注意：如果在启用持久存储时，HSTS缓存已包含HSTS策略，这些策略将在存储中保留。如果缓存和存储包含相同的已知主机，缓存中的策略被视为更为最新（因此会覆盖存储中的先前值）。如果不希望出现此行为，请先启用HSTS存储，再启用严格传输安全。默认情况下，HSTS策略的持久存储是被禁用的。

### `[signal] void QNetworkAccessManager::encrypted(QNetworkReply *reply)`

**作用与语义：**

当SSL/TLS会话成功完成初始握手时，该信号会发出。此时，尚未传输任何用户数据。该信号可用于对证书链进行额外检查，例如通知用户网站证书发生变化。`reply`参数指定了哪个网络响应负责。如果回复不符合预期标准，则应通过连接该信号的槽函数调用`QNetworkReply::abort()`来中止。可用的SSL配置可以通过`QNetworkReply::sslConfiguration()`方法进行检查。
在内部，`QNetworkAccessManager`可以开启多个连接到服务器的连接，以便并行处理请求。这些连接可以被重复使用，这意味着加密()信号不会被发出。这意味着你只有在`QNetworkAccessManager`生命周期内第一次连接到某个站点时才有保证接收到该信号。

### `[signal] void QNetworkAccessManager::finished(QNetworkReply *reply)`

**作用与语义：**

每当待处理的网络回复结束时，该信号就会发出。`reply`参数中会包含刚刚完成的回复的指针。该信号与`QNetworkReply::finished()`信号同步发射。
有关该对象将处于的状态信息，请参见`QNetworkReply::finished()`。
注意：不要删除连接该信号的槽函数中的`reply`对象。请使用`deleteLater()`。

### `QNetworkReply *QNetworkAccessManager::get(const QNetworkRequest &request)`

**作用与语义：**

发布请求获取目标`request`内容，并返回一个新的`QNetworkReply`对象，每当有新数据到达时发出`readyRead()`信号。
内容及相关报头将被下载。

### `[since 6.7] QNetworkReply *QNetworkAccessManager::get(const QNetworkRequest &request, QIODevice *data)`

**作用与语义：**

注意：带有消息主体的 get 请求不会被缓存。
注意：如果请求被重定向，消息主体仅在状态码为308时被保留。

### `[since 6.7] QNetworkReply *QNetworkAccessManager::get(const QNetworkRequest &request, const QByteArray &data)`

**作用与语义：**

注意：带有消息主体的 get 请求不会被缓存。
注意：如果请求被重定向，消息主体仅在状态码为308时被保留。

### `QNetworkReply *QNetworkAccessManager::head(const QNetworkRequest &request)`

**作用与语义：**

发布请求获取`request`的网络头部，并返回一个新的`QNetworkReply`对象，该对象将包含这些头部。
该函数以关联的HTTP请求（HEAD）命名。

### `bool QNetworkAccessManager::isStrictTransportSecurityEnabled() const`

**作用与语义：**

如果启用了HTTP严格传输安全（HSTS），则返回为真。默认情况下，HSTS是被禁用的。

### `bool QNetworkAccessManager::isStrictTransportSecurityStoreEnabled() const`

**作用与语义：**

如果HSTS缓存使用永久存储来加载和存储HSTS策略，则返回为真。

### `QNetworkReply *QNetworkAccessManager::post(const QNetworkRequest &request, QIODevice *data)`

**作用与语义：**

向`request`指定的目的地发送HTTP POST请求，返回一个新的`QNetworkReply`对象，该对象将包含服务器发送的回复。`data`设备的内容将上传到服务器。
`data`必须开放阅读，并且必须有效直到`finished()`信号发出。
注意：在非HTTP和HTTPS协议上发送POST请求未定义，且很可能失败。

### `QNetworkReply *QNetworkAccessManager::post(const QNetworkRequest &request, QHttpMultiPart *multiPart)`

**作用与语义：**

将`multiPart`消息的内容发送到`request`指定的目的地。
这可用于通过HTTP发送MIME多部分消息。

### `QNetworkReply *QNetworkAccessManager::post(const QNetworkRequest &request, const QByteArray &data)`

**作用与语义：**

将`data`字节数组的内容发送到`request`指定的目的地。

### `[since 6.8] QNetworkReply *QNetworkAccessManager::post(const QNetworkRequest &request, std::nullptr_t nptr)`

**作用与语义：**

发送`request`指定的POST请求，但没有正体，并返回一个新的`QNetworkReply`对象。

### `[signal] void QNetworkAccessManager::preSharedKeyAuthenticationRequired(QNetworkReply *reply, QSslPreSharedKeyAuthenticator *authenticator)`

**作用与语义：**

如果SSL/TLS握手协商PSK密文套件，就会发出该信号，因此需要PSK认证。`reply`对象是协商此类密码套件的`QNetworkReply`。
使用PSK时，客户端必须向服务器发送有效的身份和有效的预共享密钥，以便SSL握手继续。应用程序可以通过根据需求填写传递的`authenticator`对象，在连接到该信号的槽中提供这些信息。
注意：忽视该信号或未提供所需凭证，将导致握手失败，连接将被终止。
注意：`authenticator`对象归回复所有，应用程序不得删除。

### `QNetworkProxy QNetworkAccessManager::proxy() const`

**作用与语义：**

返回使用该`QNetworkAccessManager`对象发送的请求将使用的`QNetworkProxy`。代理的默认值为`QNetworkProxy::DefaultProxy`。

### `[signal] void QNetworkAccessManager::proxyAuthenticationRequired(const QNetworkProxy &proxy, QAuthenticator *authenticator)`

**作用与语义：**

每当代理请求认证且`QNetworkAccessManager`找不到有效的缓存凭证时，都会发出该信号。连接到该信号的槽应在`authenticator`对象中填充代理`proxy`的凭证。
`QNetworkAccessManager`会在内部缓存凭证。下次代理请求认证时，`QNetworkAccessManager`会自动发送相同的凭证，不再发出代理认证必需信号。
如果代理拒绝凭证，`QNetworkAccessManager`会再次发出信号。

### `QNetworkProxyFactory *QNetworkAccessManager::proxyFactory() const`

**作用与语义：**

返回该`QNetworkAccessManager`对象用来确定请求代理的代理工厂。
注意，该函数返回的指针由`QNetworkAccessManager`管理，随时可能被删除。

### `QNetworkReply *QNetworkAccessManager::put(const QNetworkRequest &request, QIODevice *data)`

**作用与语义：**

将`data`内容上传到目标`request`，并返回一个新的`QNetworkReply`对象，该对象将开放以供回复。
`data`在调用该函数时必须打开以读取，并且必须保持有效直到该回复发出`finished()`信号。
是否能从返回的对象中读取任何内容取决于协议。对于HTTP，服务器可能会发送一个小的HTML页面，表示上传成功（或未成功）。其他协议的回复中可能会包含内容。
注意：对于 HTTP，该请求将发送 PUT 请求，大多数服务器不允许此请求。表单上传机制，包括通过 HTML 表单上传文件，均使用 POST 机制。

### `QNetworkReply *QNetworkAccessManager::put(const QNetworkRequest &request, QHttpMultiPart *multiPart)`

**作用与语义：**

将`multiPart`消息的内容发送到`request`指定的目的地。
这可用于通过HTTP发送MIME多部分消息。

### `QNetworkReply *QNetworkAccessManager::put(const QNetworkRequest &request, const QByteArray &data)`

**作用与语义：**

将`data`字节数组的内容发送到`request`指定的目的地。

### `[since 6.8] QNetworkReply *QNetworkAccessManager::put(const QNetworkRequest &request, std::nullptr_t nptr)`

**作用与语义：**

发送`request`指定的PUT请求，但没有正体，并返回一个新的`QNetworkReply`对象。

### `QNetworkRequest::RedirectPolicy QNetworkAccessManager::redirectPolicy() const`

**作用与语义：**

返回创建新请求时使用的重定向策略。

### `QNetworkReply *QNetworkAccessManager::sendCustomRequest(const QNetworkRequest &request, const QByteArray &verb, QIODevice *data = nullptr)`

**作用与语义：**

向`request` URL标识的服务器发送自定义请求。
用户有责任向服务器发送符合 HTTP 规范的有效 `verb`。
这种方法提供了发送动词的手段，除了通过`get()`或`post()`等常见的动词，例如发送HTTP OPTIONS命令。
如果`data`未空，`data`设备的内容将被上传到服务器;此时，数据必须处于可读取状态，并且必须在该回复发出`finished()`信号前保持有效。
注意：此功能目前仅支持 HTTP（S） 平台。

### `QNetworkReply *QNetworkAccessManager::sendCustomRequest(const QNetworkRequest &request, const QByteArray &verb, QHttpMultiPart *multiPart)`

**作用与语义：**

向`request` URL标识的服务器发送自定义请求。
将`multiPart`消息的内容发送到`request`指定的目的地。
这可以用来发送自定义动词的MIME多部分消息。

### `QNetworkReply *QNetworkAccessManager::sendCustomRequest(const QNetworkRequest &request, const QByteArray &verb, const QByteArray &data)`

**作用与语义：**

将`data`字节数组的内容发送到`request`指定的目的地。

### `void QNetworkAccessManager::setAutoDeleteReplies(bool shouldAutoDelete)`

**作用与语义：**

启用或禁用自动删除`QNetworkReplies`。
将 `shouldAutoDelete` 设为真等同于将 `QNetworkRequest::AutoDeleteReplyOnFinishAttribute` 属性设置为 true，除非该属性已在`QNetworkRequest`中明确设置`QNetworkRequests`传递给该 `QNetworkAccessManager` 实例。

### `void QNetworkAccessManager::setCache(QAbstractNetworkCache *cache)`

**作用与语义：**

将管理器的网络缓存设置为指定的`cache`。缓存用于管理器调度的所有请求。
使用该函数将网络缓存对象设置为实现额外功能的类，比如将 Cookie 保存到永久存储。
注意：`QNetworkAccessManager`拥有`cache`对象的所有权。
`QNetworkAccessManager`默认没有固定缓存。Qt提供了一个简单的磁盘缓存，`QNetworkDiskCache`，可以使用。

### `void QNetworkAccessManager::setCookieJar(QNetworkCookieJar *cookieJar)`

**作用与语义：**

将管理器的 cookie jar 设置为指定的`cookieJar`。管理器发送的所有请求都会使用该 cookie jar。
使用这个函数将 cookie jar 对象设置为实现额外功能的类，比如将 cookie 保存到永久存储。
注意：`QNetworkAccessManager`对`cookieJar`对象拥有所有权。
如果`cookieJar`与该`QNetworkAccessManager`在同一线程中，它会设置`cookieJar`的父节点，使得该对象被删除时，cookie jar 也会被删除。如果你想在不同`QNetworkAccessManager`对象之间共享 cookie jar，调用该函数后，可以将 cookie jar 的父节点设置为 0。
`QNetworkAccessManager`默认不实现任何自己的Cookie策略：只要Cookie格式良好且符合最低安全要求（cookie域匹配请求，cookie路径匹配请求），它接受服务器发送的所有Cookie。为了实现自己的安全策略，覆盖`QNetworkCookieJar::cookiesForUrl()`并`QNetworkCookieJar::setCookiesFromUrl()`虚拟函数。`QNetworkAccessManager`检测到新Cookie时调用这些函数。

### `void QNetworkAccessManager::setProxy(const QNetworkProxy &proxy)`

**作用与语义：**

将未来请求中使用的代理设置为`proxy`。这不会影响已发送的请求。如果代理请求认证，`proxyAuthenticationRequired()`信号将被发出。
包含此功能的代理集将用于`QNetworkAccessManager`发出的所有请求。在某些情况下，可能需要根据发送的请求类型或目的主机选择不同的代理。如果是这样，你应该考虑使用`setProxyFactory()`。

### `void QNetworkAccessManager::setProxyFactory(QNetworkProxyFactory *factory)`

**作用与语义：**

设置该类的代理工厂为`factory`。代理工厂用于确定针对特定请求的更具体代理列表，而不是试图对所有请求使用相同的代理值。
`QNetworkAccessManager`发送的所有查询类型都将为`QNetworkProxyQuery::UrlRequest`。
例如，代理工厂可以应用以下规则：
- 如果目标地址位于本地网络（例如，主机名无点或IP地址位于组织范围内），返回`QNetworkProxy::NoProxy`
- 如果请求是FTP，返回FTP代理
- 如果请求是HTTP或HTTPS，则返回HTTP代理
- 否则，返回 SOCKSv5 代理服务器
`factory`对象的生命周期由`QNetworkAccessManager`管理。必要时它会删除该对象。
注意：如果用`setProxy()`设置了特定代理，出厂设置将不会被使用。

### `void QNetworkAccessManager::setRedirectPolicy(QNetworkRequest::RedirectPolicy policy)`

**作用与语义：**

将管理器的重定向策略设置为指定的`policy`。该策略将影响管理器后续创建的所有请求。
使用该功能在管理器层面启用或禁用 HTTP 重定向。
注意：创建请求时，QNetworkRequest：：RedirectAttributePolicy 优先级最高，其次是管理者的策略。
默认值为`QNetworkRequest::NoLessSafeRedirectPolicy`。依赖手动重定向处理的客户端被鼓励在代码中明确设置此策略。

### `void QNetworkAccessManager::setStrictTransportSecurityEnabled(bool enabled)`

**作用与语义：**

如果`enabled` `true`，`QNetworkAccessManager`遵循HTTP严格传输安全策略（HSTS，RFC6797）。处理请求时，`QNetworkAccessManager`会自动将“http”方案替换为“https”，并为HSTS主机使用安全传输。如果明确设置，端口80被端口443替代。
启用HSTS后，对于每个包含HSTS头部且通过安全传输接收的HTTP响应，`QNetworkAccessManager`会更新其HSTS缓存，要么记住策略有效的主机，要么移除HSTS策略过期或禁用的主机。

### `void QNetworkAccessManager::setTransferTimeout(int timeout)`

**作用与语义：**

将`timeout`设置为毫秒级的传输超时。

### `[since 6.7] void QNetworkAccessManager::setTransferTimeout(std::chrono::milliseconds duration = QNetworkRequest::DefaultTransferTimeout)`

**作用与语义：**

设置超时`duration`，如果没有数据交换，则中止传输。
如果在超时结束前没有传输任何字节，传输将被中止。0表示没有设置定时器。如果没有提供参数，超时为`QNetworkRequest::DefaultTransferTimeout`。如果未调用该函数，超时被禁用，值为零。为执行请求设置的请求专用非零超时覆盖该值。这意味着如果`QNetworkAccessManager`启用超时，则需要禁用该超时才能执行无超时请求。

### `[signal] void QNetworkAccessManager::sslErrors(QNetworkReply *reply, const QList<QSslError> &errors)`

**作用与语义：**

如果SSL/TLS会话在设置过程中遇到错误，包括证书验证错误，该信号会发出。`errors`参数包含错误列表，`reply`是遇到这些错误的`QNetworkReply`。
为了表明错误不致命且连接应继续，应从连接该信号的槽函数调用`QNetworkReply::ignoreSslErrors()`函数。如果未调用，SSL会话将在交换任何数据（包括URL）之前被解开。
该信号可用于向用户显示错误消息，提示安全可能受到威胁，并显示SSL设置（参见sslConfiguration()以获取）。如果用户在分析远程证书后决定继续，该槽函数应调用ignoreSslErrors()。

### `QList<QHstsPolicy> QNetworkAccessManager::strictTransportSecurityHosts() const`

**作用与语义：**

返回HTTP严格传输安全策略列表。如果HSTS缓存是从“严格传输安全”响应头部更新的，该列表可能与最初通过`addStrictTransportSecurityHosts()`设置的有所不同。

### `[virtual] QStringList QNetworkAccessManager::supportedSchemes() const`

**作用与语义：**

列出访问管理器支持的所有URL方案。
重新实现此方法，在`QNetworkAccessManager`子类中提供你自己的支持方案。例如，当子类支持新协议时，这是必要的。

### `int QNetworkAccessManager::transferTimeout() const`

**作用与语义：**

返回传输时使用的超时，单位为毫秒。

### `[since 6.7] std::chrono::milliseconds QNetworkAccessManager::transferTimeoutAsDuration() const`

**作用与语义：**

返回超时时间，逾时如果没有数据交换，传输将中止。
默认时长为零，意味着不使用超时。

## 6. 深入实践与常见坑

### 生命周期和资源边界

manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

### 状态和错误边界

请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

### 线程边界

QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

### 最容易出现的错误

不要在 finished 前释放 reply；检查 HTTP 状态码和 network error 两套错误；HTTPS 要处理 sslErrors；大响应使用 readyRead 分段读取。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QNetworkAccessManager` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
