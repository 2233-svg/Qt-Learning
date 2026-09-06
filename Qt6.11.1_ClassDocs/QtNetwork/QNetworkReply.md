# QNetworkReply

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** 一次异步网络请求的响应对象，负责提供响应头、状态、数据、进度和错误通知。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkReply`：一次异步网络请求的响应对象，负责提供响应头、状态、数据、进度和错误通知。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkReply>`
- 继承自：QIODevice
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

```cpp
// manager、reply 和事件循环必须在正确线程中存活。
QNetworkReply *reply = manager->get(request);
connect(reply, &QNetworkReply::finished, this, [reply] {
    const QByteArray body = reply->readAll();
    reply->deleteLater();
});
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum NetworkError { NoError, ConnectionRefusedError, RemoteHostClosedError, HostNotFoundError, TimeoutError, …, UnknownServerError }`
- `RawHeaderPair`

### 公有函数

- `virtual ~QNetworkReply()`
- `QVariant attribute(QNetworkRequest::Attribute code) const`
- `QNetworkReply::NetworkError error() const`
- `bool hasRawHeader(QAnyStringView headerName) const`
- `QVariant header(QNetworkRequest::KnownHeaders header) const`
- `(since 6.8) QHttpHeaders headers() const`
- `void ignoreSslErrors(const QList<QSslError> &errors)`
- `bool isFinished() const`
- `bool isRunning() const`
- `QNetworkAccessManager * manager() const`
- `QNetworkAccessManager::Operation operation() const`
- `QByteArray rawHeader(QAnyStringView headerName) const`
- `QList<QByteArray> rawHeaderList() const`
- `const QList<QNetworkReply::RawHeaderPair> & rawHeaderPairs() const`
- `qint64 readBufferSize() const`
- `QNetworkRequest request() const`
- `virtual void setReadBufferSize(qint64 size)`
- `void setSslConfiguration(const QSslConfiguration &config)`
- `QSslConfiguration sslConfiguration() const`
- `QUrl url() const`

### 重实现的公有函数

- `virtual void close() override`
- `virtual bool isSequential() const override`

### 公有槽函数

- `virtual void abort() = 0`
- `virtual void ignoreSslErrors()`

### 信号

- `void downloadProgress(qint64 bytesReceived, qint64 bytesTotal)`
- `void encrypted()`
- `void errorOccurred(QNetworkReply::NetworkError code)`
- `void finished()`
- `void metaDataChanged()`
- `void preSharedKeyAuthenticationRequired(QSslPreSharedKeyAuthenticator *authenticator)`
- `void redirectAllowed()`
- `void redirected(const QUrl &url)`
- `(since 6.3) void requestSent()`
- `(since 6.3) void socketStartedConnecting()`
- `void sslErrors(const QList<QSslError> &errors)`
- `void uploadProgress(qint64 bytesSent, qint64 bytesTotal)`

### 保护函数

- `QNetworkReply(QObject *parent = nullptr)`
- `virtual void ignoreSslErrorsImplementation(const QList<QSslError> &errors)`
- `void setAttribute(QNetworkRequest::Attribute code, const QVariant &value)`
- `void setError(QNetworkReply::NetworkError errorCode, const QString &errorString)`
- `void setFinished(bool finished)`
- `void setHeader(QNetworkRequest::KnownHeaders header, const QVariant &value)`
- `(since 6.8) void setHeaders(const QHttpHeaders &newHeaders)`
- `(since 6.8) void setHeaders(QHttpHeaders &&newHeaders)`
- `void setOperation(QNetworkAccessManager::Operation operation)`
- `void setRawHeader(const QByteArray &headerName, const QByteArray &value)`
- `void setRequest(const QNetworkRequest &request)`
- `virtual void setSslConfigurationImplementation(const QSslConfiguration &configuration)`
- `void setUrl(const QUrl &url)`
- `(since 6.8) void setWellKnownHeader(QHttpHeaders::WellKnownHeader name, QByteArrayView value)`
- `virtual void sslConfigurationImplementation(QSslConfiguration &configuration) const`

### 重实现的保护函数

- `virtual qint64 writeData(const char *data, qint64 len) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QNetworkReply::NetworkError`

**作用与语义：**

表示请求处理过程中发现的所有可能错误条件。
- `QNetworkReply::NoError`：`0`;无错误条件。
注意：当HTTP协议返回重定向时，不会报告错误。你可以检查是否存在带有`QNetworkRequest::RedirectionTargetAttribute`属性的重定向。
- `QNetworkReply::ConnectionRefusedError`：`1`;远程服务器拒绝连接（服务器不接受请求）
- `QNetworkReply::RemoteHostClosedError`：`2`;远程服务器提前关闭连接，未收到和处理完整回复
- `QNetworkReply::HostNotFoundError`：`3`;未找到远程主机名称（主机名无效）
- `QNetworkReply::TimeoutError`：`4`;与远程服务器的连接超时
- `QNetworkReply::OperationCanceledError`：`5`;该操作在完成前通过调用`abort()`或`close()`被取消。
- `QNetworkReply::SslHandshakeFailedError`：`6`;SSL/TLS握手失败，加密信道无法建立。`sslErrors()`信号本应发出。
- `QNetworkReply::TemporaryNetworkFailureError`：`7`;连接因网络断开而中断，但系统已开始漫游至另一个接入点。请求应重新提交，连接恢复后将立即处理。
- `QNetworkReply::NetworkSessionFailedError`：`8`;连接因断开网络连接或未能启动网络而中断。
- `QNetworkReply::BackgroundRequestNotAllowedError`：`9`;由于平台政策，目前不允许背景调查请求。
- `QNetworkReply::TooManyRedirectsError`：`10`;在执行重定向时，达到了最大限制。该限制默认设置为50，或由QNetworkRequest：：setMaxRedirectsAllowed()设定。（该值于5.6版本引入。）
- `QNetworkReply::InsecureRedirectError`：`11`;在执行重定向时，网络访问API检测到从加密协议（https）重定向到未加密协议（http）。（该值于5.6版本引入。）
- `QNetworkReply::ProxyConnectionRefusedError`：`101`;代理服务器的连接被拒绝（代理服务器不接受请求）
- `QNetworkReply::ProxyConnectionClosedError`：`102`;代理服务器提前关闭连接，未收到并处理完整回复
- `QNetworkReply::ProxyNotFoundError`：`103`;未找到代理主机名（代理主机名无效）
- `QNetworkReply::ProxyTimeoutError`：`104`;与代理的连接超时或代理未及时回复请求
- `QNetworkReply::ProxyAuthenticationRequiredError`：`105`;代理方要求认证以响应请求，但未接受任何提供的凭证（如有）
- `QNetworkReply::ContentAccessDenied`：`201`;对远程内容的访问被拒绝（类似于HTTP错误403）
- `QNetworkReply::ContentOperationNotPermittedError`：`202`;不允许对远程内容进行操作
- `QNetworkReply::ContentNotFoundError`：`203`;服务器端找不到远程内容（类似于HTTP错误404）
- `QNetworkReply::AuthenticationRequiredError`：`204`;远程服务器需要认证才能提供内容，但提供的凭证未被接受（如果有的话）
- `QNetworkReply::ContentReSendError`：`205`;请求需要再次发送，但失败，例如因为上传数据无法第二次读取。
- `QNetworkReply::ContentConflictError`：`206`;由于与当前资源状态冲突，请求无法完成。
- `QNetworkReply::ContentGoneError`：`207`;请求的资源不再在服务器上可用。
- `QNetworkReply::InternalServerError`：`401`;服务器遇到了意外状况，导致无法满足请求。
- `QNetworkReply::OperationNotImplementedError`：`402`;服务器不支持满足请求所需的功能。
- `QNetworkReply::ServiceUnavailableError`：`403`;此时服务器无法处理该请求。
- `QNetworkReply::ProtocolUnknownError`：`301`;网络访问API无法接受请求，因为协议尚未公开
- `QNetworkReply::ProtocolInvalidOperationError`：`302`;请求的操作对该协议无效
- `QNetworkReply::UnknownNetworkError`：`99`;检测到未知的网络相关错误
- `QNetworkReply::UnknownProxyError`：`199`;检测到一个未知的代理相关错误
- `QNetworkReply::UnknownContentError`：`299`;检测到与远程内容相关的未知错误
- `QNetworkReply::ProtocolFailure`：`399`;检测到协议出现故障（解析错误、无效或意外响应等）
- `QNetworkReply::UnknownServerError`：`499`;检测到与服务器响应相关的未知错误

### `QNetworkReply::RawHeaderPair`

**作用与语义：**

RawHeaderPair 是一个标准化:p air<`QByteArray`，`QByteArray`>第一个`QByteArray`是标题名，第二个是头部。

### `[explicit protected] QNetworkReply::QNetworkReply(QObject *parent = nullptr)`

**作用与语义：**

创建带有父`parent`的QNetworkReply对象。
你不能直接实例化 QNetworkReply 对象。用 `QNetworkAccessManager` 函数来实现这一点。

### `[virtual noexcept] QNetworkReply::~QNetworkReply()`

**作用与语义：**

删除该回复并释放与之相关的资源。如果仍有任何网络连接，它们将被关闭。

### `[pure virtual slot] void QNetworkReply::abort()`

**作用与语义：**

立即中止操作并关闭所有仍然开放的网络连接。仍在上传的也被中止。
`finished()`信号也会被发射。

### `QVariant QNetworkReply::attribute(QNetworkRequest::Attribute code) const`

**作用与语义：**

返回与代码`code`关联的属性。如果该属性未被设置，则返回无效`QVariant`（类型`QMetaType::UnknownType`）。
你可以预期`QNetworkRequest::Attribute`中列出的默认值会应用到该函数返回的值上。

### `[override virtual] void QNetworkReply::close()`

**作用与语义：**

重实现自：`QIODevice::close()`。
关闭该设备进行读取。未读取数据会被丢弃，但网络资源直到完成才会丢弃。特别是，如果上传正在进行中，上传会一直进行直到完成。
当所有操作结束且网络资源被释放时，`finished()`信号才会发出。

### `[signal] void QNetworkReply::downloadProgress(qint64 bytesReceived, qint64 bytesTotal)`

**作用与语义：**

该信号用于表示网络请求中下载部分的进展（如果有的话）。如果该请求没有下载，则该信号会发出一次，且`bytesReceived`和`bytesTotal`的值均为0。
`bytesReceived`参数表示接收的字节数，`bytesTotal`表示预计下载的字节总数。如果未知下载字节数，`bytesTotal`为-1。
当`bytesReceived`等于`bytesTotal`时，下载结束。此时，`bytesTotal`不会是-1。
注意，`bytesReceived`和`bytesTotal`的值可能与`size()`、通过`read()`或`readAll()`获得的字节总数或头部（ContentLengthHeader）的值不同。原因可能是协议开销，或者下载过程中数据被压缩。

### `[signal] void QNetworkReply::encrypted()`

**作用与语义：**

当SSL/TLS会话成功完成初始握手时，该信号会发出。此时，尚未传输任何用户数据。该信号可用于对证书链进行额外检查，例如通知用户网站证书发生变化。如果回复不符合预期标准，应通过连接该信号的槽函数调用`QNetworkReply::abort()`来终止。可用的SSL配置可以通过`QNetworkReply::sslConfiguration()`方法进行检查。
内部，`QNetworkAccessManager` 可能开启多个连接，以便服务器并行处理请求。这些连接可以被重复使用，这意味着加密()信号不会被发出。这意味着你只有在`QNetworkAccessManager`生命周期内第一次连接到某个站点时才有保证接收到该信号。

### `QNetworkReply::NetworkError QNetworkReply::error() const`

**作用与语义：**

返回处理请求时发现的错误。如果未发现错误，返回`NoError`。

### `[signal] void QNetworkReply::errorOccurred(QNetworkReply::NetworkError code)`

**作用与语义：**

当回复检测到处理错误时，会发出该信号。随后可能会发出`finished()`信号，表示连接已结束。
`code`参数包含检测到的错误代码。调用`errorString()`以获取错误条件的文本表示。
注意：不要删除连接到该信号的槽函数中的物体。请使用`deleteLater()`。

### `[signal] void QNetworkReply::finished()`

**作用与语义：**

该信号在回复处理完成后发出。该信号发出后，回复的数据或元数据将不再更新。
除非`close()`或`abort()`被调用，否则回复仍可读取，因此可以通过调用`read()`或`readAll()`来检索数据。特别是，如果由于`readyRead()`没有调用`read()`，调用`readAll()`会在一个`QByteArray`中检索全部内容。
该信号与`QNetworkAccessManager::finished()`同步发射，该信号的响应参数为该对象。
注意：不要删除连接到该信号槽中的物体。使用`deleteLater()`。
你也可以用`isFinished()`在收到 finished() 信号之前就检查`QNetworkReply`是否已经完成。

### `bool QNetworkReply::hasRawHeader(QAnyStringView headerName) const`

**作用与语义：**

如果原始的名称头 `headerName` 是由远程服务器发送的，返回`true`。
注意：在 6.7 之前的 Qt 版本中，该功能仅取`QByteArray`。

### `QVariant QNetworkReply::header(QNetworkRequest::KnownHeaders header) const`

**作用与语义：**

如果该头部是由远程服务器发送的，返回已知头部的值`header`。如果未发送头部，返回无效`QVariant`。

### `[since 6.8] QHttpHeaders QNetworkReply::headers() const`

**作用与语义：**

返回由远程服务器发送的头部。

### `[virtual slot] void QNetworkReply::ignoreSslErrors()`

**作用与语义：**

如果调用该函数，与网络连接相关的SSL错误将被忽略，包括证书验证错误。
警告：请务必让用户检查`sslErrors()`信号报告的错误，只有在用户确认继续后才调用此方法。如果出现意外错误，应中止回复。未检查实际错误就调用此方法，很可能会对你的应用构成安全风险。请格外小心使用！
该功能可从连接`sslErrors()`信号的槽函数调用，以指示发现的错误。
注意：如果`QNetworkAccessManager`启用了HTTP严格传输安全，该功能不会产生影响。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
networkReply， qOverload<>（&QNetworkReply：：ignoreSslErrors））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
networkReply， [receiver = networkReply]() { receiver->ignoreSslErrors(); }）;


更多示例和方法，请参见连接超载槽位。

### `void QNetworkReply::ignoreSslErrors(const QList<QSslError> &errors)`

**作用与语义：**

如果调用该函数，`errors`中给出的SSL错误将被忽略。
注意：由于大多数SSL错误与证书相关，因此大多数SSL错误必须设置与该SSL错误相关的预期证书。例如，如果你想向使用自签名证书的服务器发出请求，请考虑以下摘要：
多次调用该函数会替换之前调用中传递的错误列表。你可以通过调用该函数时用空列表清除你想忽略的错误列表。
注意：如果`QNetworkAccessManager`启用了HTTP严格传输安全，该功能不会产生影响。

**官方示例：**

```cpp
 QList<QSslCertificate> cert = QSslCertificate::fromPath("server-certificate.pem"_L1);
 QSslError error(QSslError::SelfSignedCertificate, cert.at(0));
 QList<QSslError> expectedSslErrors;
 expectedSslErrors.append(error);

 QNetworkReply *reply = manager.get(QNetworkRequest(QUrl("https://server.tld/index.html")));
 reply->ignoreSslErrors(expectedSslErrors);
 // here connect signals etc.
```

### `[virtual protected] void QNetworkReply::ignoreSslErrorsImplementation(const QList<QSslError> &errors)`

**作用与语义：**

该虚拟方法旨在实现覆盖`ignoreSslErrors()`行为。`ignoreSslErrors()` 是该方法的公开包装。`errors`包含用户希望忽略的错误。

### `bool QNetworkReply::isFinished() const`

**作用与语义：**

回复结束或中止后返回`true`。

### `bool QNetworkReply::isRunning() const`

**作用与语义：**

退货`true`是在请求还在处理中，回复既未完成也未中止时进行。

### `[override virtual] bool QNetworkReply::isSequential() const`

**作用与语义：**

重装：`QIODevice::isSequential()` const.

### `QNetworkAccessManager *QNetworkReply::manager() const`

**作用与语义：**

返回用于创建该`QNetworkReply`对象的`QNetworkAccessManager`。最初，它也是父对象。

### `[signal] void QNetworkReply::metaDataChanged()`

**作用与语义：**

每当该回复中的元数据发生变化时，都会发出该信号。元数据是指任何非内容（数据）本身的信息，包括网络头部。在大多数情况下，元数据在收到第一个字节时已完全已知。然而，在数据处理过程中，也可以接收头部或其他元数据的更新。

### `QNetworkAccessManager::Operation QNetworkReply::operation() const`

**作用与语义：**

返回了本回复中发布的操作。

### `[signal] void QNetworkReply::preSharedKeyAuthenticationRequired(QSslPreSharedKeyAuthenticator *authenticator)`

**作用与语义：**

如果SSL/TLS握手协商PSK密码套件，就会发出该信号，因此需要PSK认证。
使用PSK时，客户端必须向服务器发送有效的身份和有效的预共享密钥，以便SSL握手继续。应用程序可以通过根据需求填写传递的`authenticator`对象，在连接到该信号的槽函数中提供这些信息。
注意：忽视该信号或未提供所需凭证，将导致握手失败，连接将被终止。
注意：`authenticator`对象归回复所有，应用程序不得删除。

### `QByteArray QNetworkReply::rawHeader(QAnyStringView headerName) const`

**作用与语义：**

返回由远程服务器发送的头部`headerName`原始内容。如果没有此类头部，返回一个空字节数组，可能与空头部无法区分。使用`hasRawHeader()`验证服务器是否发送了该头部字段。
注意：在 6.7 之前的 Qt 版本中，该功能仅取`QByteArray`。

### `QList<QByteArray> QNetworkReply::rawHeaderList() const`

**作用与语义：**

返回由远程服务器发送的头部字段列表，按发送顺序排列。重复的头部会被跳过。

### `const QList<QNetworkReply::RawHeaderPair> &QNetworkReply::rawHeaderPairs() const`

**作用与语义：**

返回原始头部对列表。

### `qint64 QNetworkReply::readBufferSize() const`

**作用与语义：**

返回读取缓冲区的大小，单位为字节。

### `[signal] void QNetworkReply::redirectAllowed()`

**作用与语义：**

当处理`redirected()`信号的客户端代码验证了新 URL 后，会发出该信号以允许重定向继续。该协议适用于重定向策略设置为 `QNetworkRequest::UserVerifiedRedirectPolicy` 的网络请求。

### `[signal] void QNetworkReply::redirected(const QUrl &url)`

**作用与语义：**

如果请求中未设置`QNetworkRequest::ManualRedirectPolicy`，且服务器以3xx状态（具体为301、302、303、305、307或308状态码）响应，且位置头部有有效URL，表示HTTP重定向，则会发出该信号。`url`参数包含服务器在位置头部返回的新重定向URL。

### `QNetworkRequest QNetworkReply::request() const`

**作用与语义：**

返回为本回复发布的请求。特别注意，请求的URL可能与回复不同。

### `[signal, since 6.3] void QNetworkReply::requestSent()`

**作用与语义：**

该信号在请求发送时会发出1次或多次。对于自定义进度或超时处理非常有用。

### `[protected] void QNetworkReply::setAttribute(QNetworkRequest::Attribute code, const QVariant &value)`

**作用与语义：**

将属性 `code` 设置为值为 `value`。如果之前设置过`code`，则该属性将被覆盖。如果 `value` 是无效的`QVariant`，则该属性将被取消设置。

### `[protected] void QNetworkReply::setError(QNetworkReply::NetworkError errorCode, const QString &errorString)`

**作用与语义：**

将错误条件设置为`errorCode`。可读消息被设置为`errorString`。
调用 setError() 不会发出 `errorOccurred`（`QNetworkReply::NetworkError`） 信号。

### `[protected] void QNetworkReply::setFinished(bool finished)`

**作用与语义：**

把回复设置为`finished`。
设置完后，回复的数据不得发生变化。

### `[protected] void QNetworkReply::setHeader(QNetworkRequest::KnownHeaders header, const QVariant &value)`

**作用与语义：**

将已知的头部`header`设置为值`value`。对应的头部原始形式也会被设置。

### `[protected, since 6.8] void QNetworkReply::setHeaders(const QHttpHeaders &newHeaders)`

**作用与语义：**

将`newHeaders`设为该网络回复中的头部，覆盖之前设置的任何头部。
如果某些头对应已知头，它们会被解析，并设置相应的解析形式。

### `[protected, since 6.8] void QNetworkReply::setHeaders(QHttpHeaders &&newHeaders)`

**作用与语义：**

将`newHeaders`设为该网络回复中的头部，覆盖之前设置的任何头部。
如果某些头对应已知头，它们会被解析，并设置相应的解析形式。

### `[protected] void QNetworkReply::setOperation(QNetworkAccessManager::Operation operation)`

**作用与语义：**

将该对象的相关操作设置为`operation`。该值将由`operation()`返回。
注意：该操作应在创建该对象时设置，且不得再次更改。

### `[protected] void QNetworkReply::setRawHeader(const QByteArray &headerName, const QByteArray &value)`

**作用与语义：**

将原始首部`headerName`设置为值为`value`。如果`headerName`之前被设置，则会被覆盖。多个同名的HTTP头在功能上等价于一个将值串接并用逗号分隔的单一头部。
如果`headerName`匹配已知头部，`value`值将被解析，并设置相应的解析形式。

### `[virtual] void QNetworkReply::setReadBufferSize(qint64 size)`

**作用与语义：**

将读取缓冲区的大小设置为`size`字节。读取缓冲区是存放正在从网络下载的数据的缓冲区，在读取`QIODevice::read()`之前。将缓冲区大小设置为0，缓冲区大小将无限大。
当缓冲区满（即`bytesAvailable()`返回`size`或更多）时，`QNetworkReply`会尝试停止从网络读取，从而导致下载速度相应降低。如果缓冲区大小不受限制，`QNetworkReply`会尽快从网络下载。
与`QAbstractSocket::setReadBufferSize()`不同，`QNetworkReply`无法保证读取缓冲区大小的精度。也就是说，`bytesAvailable()`可以返回超过`size`。

### `[protected] void QNetworkReply::setRequest(const QNetworkRequest &request)`

**作用与语义：**

将该对象的相关请求设置为`request`。该值将由`request()`返回。
注意：请求应在创建该对象时设置，且不得再次更改。

### `void QNetworkReply::setSslConfiguration(const QSslConfiguration &config)`

**作用与语义：**

将与该请求关联的网络连接设置为`config`的SSL配置（如可能）。

### `[virtual protected] void QNetworkReply::setSslConfigurationImplementation(const QSslConfiguration &configuration)`

**作用与语义：**

提供这种虚拟方法是为了实现覆盖`setSslConfiguration()`行为。`setSslConfiguration()` 是该方法的公包。如果你覆盖了该方法，请使用 `configuration` 来设置 SSL 配置。

### `[protected] void QNetworkReply::setUrl(const QUrl &url)`

**作用与语义：**

将正在处理的URL设置为`url`。通常，URL与发布请求的URL匹配，但由于各种原因，它可能不同（例如，文件路径被设置为绝对或规范）。

### `[protected, since 6.8] void QNetworkReply::setWellKnownHeader(QHttpHeaders::WellKnownHeader name, QByteArrayView value)`

**作用与语义：**

将头部`name`设置为值为`value`。如果`name`之前被设置过，则会被覆盖。

### `[signal, since 6.3] void QNetworkReply::socketStartedConnecting()`

**作用与语义：**

该信号在套接字连接时发出0次或更多次，然后才发送请求。对于自定义进度或超时处理非常有用。

### `QSslConfiguration QNetworkReply::sslConfiguration() const`

**作用与语义：**

如果使用SSL，返回与该回复相关的SSL配置和状态。该文件将包含远程服务器的证书、通往证书授权中心的证书链以及正在使用的加密密码。
对等方的证书及其证书链在`sslErrors()`发出时（如果已经发出）就会被知道。

### `[virtual protected] void QNetworkReply::sslConfigurationImplementation(QSslConfiguration &configuration) const`

**作用与语义：**

该虚拟方法旨在实现覆盖`sslConfiguration()`行为。`sslConfiguration()` 是该方法的公共包装器。配置将在 `configuration` 返回。

### `[signal] void QNetworkReply::sslErrors(const QList<QSslError> &errors)`

**作用与语义：**

如果SSL/TLS会话在设置过程中遇到错误，包括证书验证错误，该信号会发出。`errors`参数包含错误列表。
为了表明错误不致命且连接应继续，应从连接该信号的槽函数调用`ignoreSslErrors()`函数。如果未调用，SSL会话将在交换任何数据（包括URL）之前被撕毁。
该信号可用于向用户显示错误信息，提示安全可能受到威胁，并显示SSL设置（参见获取`sslConfiguration()`）。如果用户在分析远程证书后决定继续，槽函数应调用`ignoreSslErrors()`。

### `[signal] void QNetworkReply::uploadProgress(qint64 bytesSent, qint64 bytesTotal)`

**作用与语义：**

该信号用于表示网络请求中上传部分的进展（如果有的话）。如果该请求没有上传，则该信号不会发出。
`bytesSent`参数表示上传的字节数，`bytesTotal`表示要上传的字节总数。如果无法确定上传字节数，`bytesTotal`为-1。
上传结束时`bytesSent`等于`bytesTotal`。此时，`bytesTotal`不会是-1。

### `QUrl QNetworkReply::url() const`

**作用与语义：**

返回已下载或上传内容的 URL。注意，该 URL 可能与原始请求不同。如果请求中启用了重定向功能，该函数返回网络 API 正在访问的当前 URL，即请求重定向到的资源的 URL。

### `[override virtual protected] qint64 QNetworkReply::writeData(const char *data, qint64 len)`

**作用与语义：**

实现 `QIODevice` 的写入入口，但普通 `QNetworkReply` 是由网络后端提供数据的只读顺序设备，应用不应向回复对象写数据。要发送请求正文，应把数据传给 `QNetworkAccessManager` 的 `post()`、`put()` 或 `sendCustomRequest()`。

### `RawHeaderPair`

**作用与语义：**

RawHeaderPair 是一个标准化:p air<`QByteArray`，`QByteArray`>第一个`QByteArray`是标题名，第二个是头部。

## 6. 深入实践与常见坑

### 生命周期和资源边界

manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

### 状态和错误边界

请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

### 线程边界

QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

### 最容易出现的错误

不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QNetworkReply` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
