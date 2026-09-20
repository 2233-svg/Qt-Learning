# QNetworkReply：异步网络响应

> Qt 6.11.1  
> 头文件：`#include <QNetworkReply>`  
> 模块：`Qt6::Network`  
> 继承：`QIODevice -> QNetworkReply`  
> 类型性质：抽象的网络响应基类

## 它解决什么问题

`QNetworkAccessManager` 负责发起请求，而 `QNetworkReply` 负责承载这一次请求的结果：响应头、响应体、上传和下载进度、重定向、TLS 状态以及错误。它是一个 `QIODevice`，所以响应体可以像文件或套接字一样通过 `read()`、`readAll()`、`bytesAvailable()` 和 `readyRead()` 读取。

它解决的核心问题是：网络数据不是一次性返回的，应用需要在事件循环中逐步接收数据，同时知道“响应头何时到达”“还有多少数据”“请求是否完成”“失败发生在哪一层”。`QNetworkReply` 把这些状态统一成可连接的信号和可查询的 API。

通常不直接构造它。`QNetworkAccessManager::get()`、`post()`、`put()`、`sendCustomRequest()` 等函数返回具体的 `QNetworkReply` 对象。应用负责连接信号、读取数据、处理错误，并在结束后通过 `deleteLater()` 释放对象。

一个响应的典型生命周期是：

```text
manager 发起请求
    -> socketStartedConnecting()（可能 0 次或多次）
    -> requestSent()（可能 1 次或多次）
    -> metaDataChanged() / readyRead()
    -> uploadProgress() / downloadProgress()
    -> errorOccurred()（如果失败，可能随后 finished）
    -> finished()
```

`finished()` 之后不会再有新的响应数据或元数据更新。若没有调用 `close()` 或 `abort()`，响应仍然可以在 `finished()` 槽中用 `readAll()` 读完。

## 实际使用场景

### 1. 小响应一次性读取

适合 JSON、配置文件、短文本和小图片。不要在 `readyRead()` 中读取一部分后又假设一次 `finished()` 就代表服务器已经返回完整语义；完整内容应在 `finished()` 时读取。

```cpp
auto *reply = manager->get(QNetworkRequest(QUrl("https://example.com/data.json")));
connect(reply, &QNetworkReply::finished, this, [reply] {
    const QByteArray body = reply->readAll();
    if (reply->error() != QNetworkReply::NoError) {
        qWarning() << reply->errorString();
    } else {
        consumeJson(body);
    }
    reply->deleteLater();
});
```

### 2. 大文件或流式响应

把 `readyRead()` 连接到写文件的槽，持续读取 `readAll()`，避免把整个响应体积压在内存中。可调用 `setReadBufferSize()` 限制 Qt 在用户读取前暂存的数据量；但该限制不是严格的字节上限，`bytesAvailable()` 可能略大于设置值。

```cpp
connect(reply, &QIODevice::readyRead, this, [reply, file] {
    file->write(reply->readAll());
});
connect(reply, &QNetworkReply::finished, this, [reply, file] {
    file->flush();
    const bool ok = reply->error() == QNetworkReply::NoError;
    reply->deleteLater();
    emit downloadDone(ok);
});
```

### 3. 上传进度和下载进度

`uploadProgress(bytesSent, bytesTotal)` 只针对有上传内容的请求发出；`downloadProgress(bytesReceived, bytesTotal)` 针对下载部分发出。`bytesTotal == -1` 表示总大小未知，不能把它直接当作除数或百分比。

进度值描述的是网络 API 观察到的传输量，不一定等于最终 `readAll()` 的字节数。例如内容解压、协议开销处理或传输编码可能使进度数值和应用层数据大小不同。

### 4. 人工确认重定向

为请求设置 `QNetworkRequest::UserVerifiedRedirectPolicy` 后，收到 `redirected(url)` 时检查新 URL，例如限制 scheme、域名和端口；确认后发出 `redirectAllowed()`。不发出该信号，重定向不会继续。

不要只检查字符串前缀来判断安全 URL。应解析 `QUrl` 的 scheme、host、port，并明确是否允许从 HTTPS 跳到 HTTP。`TooManyRedirectsError` 和 `InsecureRedirectError` 都属于网络请求失败。

### 5. TLS 证书检查

`encrypted()` 表示 TLS 初始握手成功，此时还没有发送用户数据，可在该信号中检查 `sslConfiguration()`，若不符合应用要求就 `abort()`。但连接可能被 `QNetworkAccessManager` 复用，因此一个 reply 不一定收到 `encrypted()`；需要全局观察时还应考虑 manager 的 `encrypted()` 信号。

收到 `sslErrors(errors)` 时，只有在应用明确检查错误、用户或策略确认继续的情况下，才调用 `ignoreSslErrors(errors)` 或无参数版本。无条件忽略证书错误会破坏 TLS 的身份认证。

## 关键 API 语义与边界

### 响应体是顺序设备

`QNetworkReply::isSequential()` 返回 `true`。响应体通常只能向前读取，不能像普通文件那样随意 seek。`readyRead()` 只表示当前有数据可读，不代表 HTTP 消息已经完整。

### `close()` 和 `abort()` 不一样

- `close()` 关闭 reply 的读取设备，未读数据会丢弃，但底层网络资源不会立即终止；正在进行的上传仍可能继续，资源完成释放后才发出 `finished()`。
- `abort()` 立即中止操作和仍在使用的网络连接，正在上传的数据也会被取消，并最终发出 `finished()`；通常错误会是 `OperationCanceledError`。

`errorOccurred()` 或 `finished()` 的槽中不要直接 `delete reply`。Qt 文档明确要求使用 `reply->deleteLater()`，否则信号分发或 manager 的内部处理可能访问已销毁对象。

### 头部有两套读取方式

- `header(KnownHeaders)` 读取 Qt 能识别的标准头部，返回 `QVariant`；服务器没有发送该头时返回无效 `QVariant`。
- `rawHeader(name)` 读取原始字节；空 `QByteArray` 既可能表示“没有该头”，也可能表示“该头存在但值为空”，需用 `hasRawHeader(name)` 区分。
- `rawHeaderList()` 按服务器发送顺序返回头名，重复头名会被跳过。
- `rawHeaderPairs()` 保留原始头名和值的成对数据。
- `headers()` 从 Qt 6.8 起提供 `QHttpHeaders` 形式的头部视图。

### 请求 URL 和当前 URL 可能不同

`request()` 返回最初提交给 reply 的请求；`url()` 返回当前下载或上传资源的 URL。启用重定向后，`url()` 可能已经是最终地址，因此记录审计信息时应同时保存原始请求 URL 和当前 URL。

### 属性不是所有时候都存在

`attribute(code)` 在 reply 尚未设置某属性时返回无效 `QVariant`。文档列出的请求默认值由网络访问实现使用，但调用方不应把任意无效属性强行转换为有效数据；先检查 `isValid()` 或目标类型。

### 自定义派生类的保护 API

如果实现自定义协议或 reply，构造函数、`writeData()`、`setOperation()`、`setRequest()`、`setError()`、`setFinished()`、`setUrl()`、`setHeader()`、`setRawHeader()`、`setHeaders()`、`setWellKnownHeader()` 和 `setAttribute()` 用来把内部结果填入基类状态。

`setError()` 只设置错误状态和文本，不会自动发出 `errorOccurred()`；派生实现需要按自己的异步状态机发出正确通知。`setFinished(true)` 也只是更新完成状态，完成信号的发送时机仍由实现负责。

## API 速查表

### 成员类型与错误码

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `enum NetworkError` | 统一表示网络层、代理层、内容层、协议层和服务器层错误。 | `NoError` 为 0；`OperationCanceledError` 表示被 `abort()` 或 `close()` 取消；HTTP 重定向本身通常不产生错误。 |
| `NoError` | 请求处理没有发现错误。 | 仍应结合 HTTP 状态码和业务响应判断成功，网络无错误不等于业务成功。 |
| `ConnectionRefusedError` | 目标主机拒绝连接。 | 可能是服务未监听、端口策略或中间设备拒绝。 |
| `RemoteHostClosedError` | 远端关闭连接。 | 可能发生在收到部分响应之后。 |
| `HostNotFoundError` | 主机名解析失败。 | 检查 DNS、代理设置和 URL 主机名。 |
| `TimeoutError` | 网络操作超时。 | 不等于总耗时一定达到某固定值，具体受请求与传输进展影响。 |
| `OperationCanceledError` | 操作被取消。 | 常见来源是 `abort()` 或 `close()`。 |
| `SslHandshakeFailedError` | TLS 握手失败。 | 通常应结合 `sslErrors()` 和 `errorString()` 定位。 |
| `TemporaryNetworkFailureError` | 临时网络失败。 | 可能适合重试，但要设置退避和次数上限。 |
| `NetworkSessionFailedError` | 网络会话不可用。 | 常见于移动或受会话管理的平台环境。 |
| `BackgroundRequestNotAllowedError` | 后台请求被平台策略禁止。 | 属于运行环境限制，不一定是服务器问题。 |
| `TooManyRedirectsError` | 重定向次数超过限制。 | 默认上限或请求设置决定限制。 |
| `InsecureRedirectError` | 检测到 HTTPS 到 HTTP 的不安全重定向。 | 不要为方便而无条件放宽。 |
| `ProxyConnectionRefusedError`、`ProxyConnectionClosedError`、`ProxyNotFoundError`、`ProxyTimeoutError`、`ProxyAuthenticationRequiredError` | 代理连接或代理认证失败。 | 先确认实际使用的代理类型和凭据。 |
| `ContentAccessDenied`、`ContentOperationNotPermittedError`、`ContentNotFoundError`、`AuthenticationRequiredError`、`ContentReSendError`、`ContentConflictError`、`ContentGoneError` | 访问内容或内容操作失败。 | 不要仅凭枚举替代 HTTP 状态码和响应体诊断。 |
| `ProtocolUnknownError`、`ProtocolInvalidOperationError`、`ProtocolFailure` | 协议不支持、操作无效或协议处理失败。 | 可能是 URL scheme 或请求方法不被后端支持。 |
| `InternalServerError`、`OperationNotImplementedError`、`ServiceUnavailableError` | 服务器端处理失败。 | 适合按业务策略重试，不能无限重试。 |
| `UnknownNetworkError`、`UnknownProxyError`、`UnknownContentError`、`UnknownServerError` | 对应层的未分类错误。 | 同时查看 `errorString()`、日志和服务端状态。 |
| `using RawHeaderPair` | `std::pair<QByteArray, QByteArray>`，first 是头名，second 是头值。 | 用于保留原始头部的成对表示。 |

### 生命周期、请求与响应状态

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `protected QNetworkReply(QObject *parent = nullptr)` | 构造 reply 基类。 | 通常由 `QNetworkAccessManager` 或自定义派生类调用，不能直接实例化抽象 reply。 |
| `protected QNetworkReply(QNetworkReplyPrivate &dd, QObject *parent)` | 供 Qt 私有实现使用的派生构造入口。 | 普通应用不应依赖私有实现细节。 |
| `virtual ~QNetworkReply()` | 销毁 reply。 | 通过 `deleteLater()` 与 Qt 事件循环配合。 |
| `QNetworkAccessManager *manager() const` | 返回创建该 reply 的 manager。 | 初始时 manager 也是 parent；不要把 reply 转移给另一个 manager。 |
| `QNetworkAccessManager::Operation operation() const` | 返回请求操作类型，如 `GetOperation`、`PostOperation`。 | 这是请求动作，不是 HTTP 状态码。 |
| `QNetworkRequest request() const` | 返回最初提交的请求。 | 与重定向后的 `url()` 可能不同。 |
| `QUrl url() const` | 返回当前访问 URL。 | 启用重定向后可能是最终 URL。 |
| `NetworkError error() const` | 返回已记录的错误码。 | 无错误返回 `NoError`；同时查看 `errorString()`。 |
| `bool isRunning() const` | 请求仍在处理且未完成或中止时为 `true`。 | 不表示底层 socket 一直在发送数据。 |
| `bool isFinished() const` | reply 已完成或已中止时为 `true`。 | 可在收到 `finished()` 前查询。 |
| `void abort()` | 立即中止请求、连接和上传。 | 纯虚槽；调用后仍应等待 `finished()` 再清理。 |
| `void close()` | 关闭 reply 的读取设备。 | 未读数据丢弃；上传和底层资源可能继续到完成。 |
| `bool isSequential() const` | 返回顺序设备语义。 | 不要假设可随机 seek。 |

### 响应体、缓冲和头部

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `qint64 readBufferSize() const` | 查询 reply 下载缓冲目标大小。 | 0 通常表示不限大小。 |
| `virtual void setReadBufferSize(qint64 size)` | 设置下载数据在应用读取前的缓冲目标。 | 0 表示不限；限制可能使下载节流，但不能保证 `bytesAvailable()` 精确等于 size。 |
| `QVariant header(QNetworkRequest::KnownHeaders header) const` | 读取 Qt 认识的标准响应头。 | 未发送时返回无效 `QVariant`。 |
| `bool hasRawHeader(QAnyStringView headerName) const` | 判断服务器是否发送了指定原始头。 | Qt 6.7 起参数为 `QAnyStringView`；适合区分空头值和缺失。 |
| `QByteArray rawHeader(QAnyStringView headerName) const` | 获取指定原始头值。 | 缺失和空值都可能返回空字节数组。 |
| `QList<QByteArray> rawHeaderList() const` | 按发送顺序返回原始头名列表。 | 重复头名会跳过。 |
| `const QList<RawHeaderPair> &rawHeaderPairs() const` | 返回原始头名值对。 | 返回引用只在 reply 仍存活且未被后续状态替换时使用；不要跨 reply 生命周期保存。 |
| `QHttpHeaders headers() const` | 获取 `QHttpHeaders` 形式的响应头。 | Qt 6.8 起提供；需要 `QHttpHeaders` 相关头文件。 |
| `QVariant attribute(QNetworkRequest::Attribute code) const` | 查询响应属性。 | 未设置时是无效 `QVariant`；先检查有效性。 |

### TLS 相关 API

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `QSslConfiguration sslConfiguration() const` | 获取 reply 使用的 TLS 配置和握手状态。 | 可检查对端证书、证书链和密码套件；在 `sslErrors()` 时证书信息应已可用。 |
| `void setSslConfiguration(const QSslConfiguration &config)` | 尝试设置此网络连接的 TLS 配置。 | 是否能在当前阶段修改取决于实现和连接状态。 |
| `void ignoreSslErrors()` | 忽略该连接报告的 TLS 错误。 | 高风险 API；应先检查错误并获得明确策略或用户确认。 |
| `void ignoreSslErrors(const QList<QSslError> &errors)` | 仅忽略给定的 TLS 错误集合。 | 比无参数版本更窄，但仍不能把未知错误默认为可忽略。 |

### 信号

| 信号 | 触发时机 | 使用重点 |
| --- | --- | --- |
| `socketStartedConnecting()` | socket 开始连接，可能 0 次或多次。 | Qt 6.3 起，可用于连接阶段计时。 |
| `requestSent()` | 请求已发送，可能 1 次或多次。 | Qt 6.3 起；不要把它当作响应开始。 |
| `metaDataChanged()` | 响应元数据变化。 | 头部通常在首字节前已知，但协议实现可能中途更新。 |
| `finished()` | 所有网络处理完成。 | 之后无更多数据或元数据更新；不要直接 delete，使用 `deleteLater()`。 |
| `errorOccurred(NetworkError code)` | reply 检测到错误。 | `finished()` 通常随后到达；读取 `errorString()` 获取文本。 |
| `encrypted()` | TLS 初始握手成功。 | 连接复用时可能不发出；可在此检查证书后 `abort()`。 |
| `sslErrors(const QList<QSslError> &errors)` | TLS 校验发现错误。 | 只有确认继续时才在同步回调中调用 `ignoreSslErrors()`。 |
| `preSharedKeyAuthenticationRequired(QSslPreSharedKeyAuthenticator *)` | TLS PSK 认证需要应用提供信息。 | 在信号返回前填写 authenticator；不要使用 queued connection 延后填写。 |
| `redirected(const QUrl &url)` | 收到可处理的 3xx 重定向。 | 配合重定向策略验证 URL；不代表已经完成跳转。 |
| `redirectAllowed()` | 应用确认重定向。 | 只用于 `UserVerifiedRedirectPolicy` 流程。 |
| `uploadProgress(qint64 bytesSent, qint64 bytesTotal)` | 上传进度变化。 | 没有上传内容时不发；总量未知时 total 为 -1。 |
| `downloadProgress(qint64 bytesReceived, qint64 bytesTotal)` | 下载进度变化。 | 总量未知时 total 为 -1；进度不一定等于最终应用层字节数。 |

### 自定义派生类的保护 API

| API | 用途 | 实现注意 |
| --- | --- | --- |
| `virtual qint64 writeData(const char *data, qint64 len)` | 重写 QIODevice 的写入接口。 | reply 通常是只读响应设备，只有自定义协议才需要实现写入语义。 |
| `void setOperation(Operation operation)` | 设置请求操作。 | 应在自定义 reply 建立时设置正确。 |
| `void setRequest(const QNetworkRequest &request)` | 设置关联请求。 | 影响 `request()` 返回值。 |
| `void setError(NetworkError code, const QString &text)` | 设置错误码与错误文本。 | 不会自动发出 `errorOccurred()`。 |
| `void setFinished(bool finished)` | 更新完成状态。 | 不等于自动发出 `finished()`。 |
| `void setUrl(const QUrl &url)` | 更新当前访问 URL。 | 重定向或自定义协议状态变化时使用。 |
| `void setHeader(KnownHeaders header, const QVariant &value)` | 设置标准响应头。 | 供 `header()` 读取。 |
| `void setRawHeader(const QByteArray &name, const QByteArray &value)` | 设置原始响应头。 | 供 raw header API 读取。 |
| `void setHeaders(const QHttpHeaders &headers)` | Qt 6.8 起设置完整头部集合。 | const 重载会复制数据。 |
| `void setHeaders(QHttpHeaders &&headers)` | Qt 6.8 起移动设置完整头部集合。 | 传入对象之后不应继续依赖其内容。 |
| `void setWellKnownHeader(QHttpHeaders::WellKnownHeader name, QByteArrayView value)` | Qt 6.8 起设置已知 HTTP 头。 | 适合自定义 HTTP reply 的结构化头部填充。 |
| `void setAttribute(Attribute code, const QVariant &value)` | 设置响应属性。 | 属性的类型和含义必须与 `QNetworkRequest::Attribute` 约定一致。 |
| `virtual void sslConfigurationImplementation(QSslConfiguration &) const` | 自定义 `sslConfiguration()` 的底层实现。 | 重写时将配置写入引用参数。 |
| `virtual void setSslConfigurationImplementation(const QSslConfiguration &)` | 自定义 TLS 配置设置行为。 | 只在自定义 TLS 传输实现中需要。 |
| `virtual void ignoreSslErrorsImplementation(const QList<QSslError> &)` | 自定义忽略 TLS 错误行为。 | 公共包装函数是 `ignoreSslErrors()`。 |
