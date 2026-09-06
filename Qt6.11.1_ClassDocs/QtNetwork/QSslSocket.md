# QSslSocket

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QSslSocket` 是 Qt Network 的“Ssl套接字”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QSslSocket` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QSslSocket>`
- 继承自：QTcpSocket
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

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

- `enum PeerVerifyMode { VerifyNone, QueryPeer, VerifyPeer, AutoVerifyPeer }`
- `enum SslMode { UnencryptedMode, SslClientMode, SslServerMode }`

### 公有函数

- `QSslSocket(QObject *parent = nullptr)`
- `virtual ~QSslSocket()`
- `void connectToHostEncrypted(const QString &hostName, quint16 port, QIODeviceBase::OpenMode mode = ReadWrite, QAbstractSocket::NetworkLayerProtocol protocol = AnyIPProtocol)`
- `void connectToHostEncrypted(const QString &hostName, quint16 port, const QString &sslPeerName, QIODeviceBase::OpenMode mode = ReadWrite, QAbstractSocket::NetworkLayerProtocol protocol = AnyIPProtocol)`
- `(since 6.0) void continueInterruptedHandshake()`
- `qint64 encryptedBytesAvailable() const`
- `qint64 encryptedBytesToWrite() const`
- `void ignoreSslErrors(const QList<QSslError> &errors)`
- `bool isEncrypted() const`
- `QSslCertificate localCertificate() const`
- `QList<QSslCertificate> localCertificateChain() const`
- `QSslSocket::SslMode mode() const`
- `QList<QOcspResponse> ocspResponses() const`
- `QSslCertificate peerCertificate() const`
- `QList<QSslCertificate> peerCertificateChain() const`
- `int peerVerifyDepth() const`
- `QSslSocket::PeerVerifyMode peerVerifyMode() const`
- `QString peerVerifyName() const`
- `QSslKey privateKey() const`
- `QSsl::SslProtocol protocol() const`
- `QSslCipher sessionCipher() const`
- `QSsl::SslProtocol sessionProtocol() const`
- `void setLocalCertificate(const QSslCertificate &certificate)`
- `void setLocalCertificate(const QString &path, QSsl::EncodingFormat format = QSsl::Pem)`
- `void setLocalCertificateChain(const QList<QSslCertificate> &localChain)`
- `void setPeerVerifyDepth(int depth)`
- `void setPeerVerifyMode(QSslSocket::PeerVerifyMode mode)`
- `void setPeerVerifyName(const QString &hostName)`
- `void setPrivateKey(const QSslKey &key)`
- `void setPrivateKey(const QString &fileName, QSsl::KeyAlgorithm algorithm = QSsl::Rsa, QSsl::EncodingFormat format = QSsl::Pem, const QByteArray &passPhrase = QByteArray())`
- `void setProtocol(QSsl::SslProtocol protocol)`
- `void setSslConfiguration(const QSslConfiguration &configuration)`
- `QSslConfiguration sslConfiguration() const`
- `QList<QSslError> sslHandshakeErrors() const`
- `bool waitForEncrypted(int msecs = 30000)`

### 重实现的公有函数

- `virtual bool atEnd() const override`
- `virtual qint64 bytesAvailable() const override`
- `virtual qint64 bytesToWrite() const override`
- `virtual bool canReadLine() const override`
- `virtual void close() override`
- `virtual void connectToHost(const QString &hostName, quint16 port, QIODeviceBase::OpenMode openMode = ReadWrite, QAbstractSocket::NetworkLayerProtocol protocol = AnyIPProtocol) override`
- `virtual void disconnectFromHost() override`
- `virtual void resume() override`
- `virtual void setReadBufferSize(qint64 size) override`
- `virtual bool setSocketDescriptor(qintptr socketDescriptor, QAbstractSocket::SocketState state = ConnectedState, QIODeviceBase::OpenMode openMode = ReadWrite) override`
- `virtual void setSocketOption(QAbstractSocket::SocketOption option, const QVariant &value) override`
- `virtual QVariant socketOption(QAbstractSocket::SocketOption option) override`
- `virtual bool waitForBytesWritten(int msecs = 30000) override`
- `virtual bool waitForConnected(int msecs = 30000) override`
- `virtual bool waitForDisconnected(int msecs = 30000) override`
- `virtual bool waitForReadyRead(int msecs = 30000) override`

### 公有槽函数

- `void ignoreSslErrors()`
- `void startClientEncryption()`
- `void startServerEncryption()`

### 信号

- `void alertReceived(QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`
- `void alertSent(QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`
- `void encrypted()`
- `void encryptedBytesWritten(qint64 written)`
- `void handshakeInterruptedOnError(const QSslError &error)`
- `void modeChanged(QSslSocket::SslMode mode)`
- `void newSessionTicketReceived()`
- `void peerVerifyError(const QSslError &error)`
- `void preSharedKeyAuthenticationRequired(QSslPreSharedKeyAuthenticator *authenticator)`
- `void sslErrors(const QList<QSslError> &errors)`

### 静态公有成员

- `(since 6.1) QString activeBackend()`
- `(since 6.1) QList<QString> availableBackends()`
- `(since 6.1) QList<QSsl::ImplementedClass> implementedClasses(const QString &backendName = {})`
- `(since 6.1) bool isClassImplemented(QSsl::ImplementedClass cl, const QString &backendName = {})`
- `(since 6.1) bool isFeatureSupported(QSsl::SupportedFeature ft, const QString &backendName = {})`
- `(since 6.1) bool isProtocolSupported(QSsl::SslProtocol protocol, const QString &backendName = {})`
- `(since 6.1) bool setActiveBackend(const QString &backendName)`
- `long sslLibraryBuildVersionNumber()`
- `QString sslLibraryBuildVersionString()`
- `long sslLibraryVersionNumber()`
- `QString sslLibraryVersionString()`
- `(since 6.1) QList<QSsl::SupportedFeature> supportedFeatures(const QString &backendName = {})`
- `(since 6.1) QList<QSsl::SslProtocol> supportedProtocols(const QString &backendName = {})`
- `bool supportsSsl()`

### 重实现的保护函数

- `virtual qint64 readData(char *data, qint64 maxlen) override`
- `virtual qint64 skipData(qint64 maxSize) override`
- `virtual qint64 writeData(const char *data, qint64 len) override`

### 相关非成员函数

- `(since 6.0) enum class AlertLevel { Warning, Fatal, Unknown }`
- `(since 6.0) enum class AlertType { CloseNotify, UnexpectedMessage, BadRecordMac, RecordOverflow, DecompressionFailure, …, UnknownAlertMessage }`
- `(since 6.1) enum class ImplementedClass { Key, Certificate, Socket, DiffieHellman, EllipticCurve, …, DtlsCookie }`
- `(since 6.1) enum class SupportedFeature { CertificateVerification, ClientSideAlpn, ServerSideAlpn, Ocsp, Psk, …, Alerts }`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSslSocket::PeerVerifyMode`

**作用与语义：**

描述`QSslSocket`的对等验证模式。默认模式为AutoVerifyPeer，根据套接字的QSocket：：SslMode选择合适的模式。
- `QSslSocket::VerifyNone`：`0`;`QSslSocket`不会向对端请求证书。如果你不想知道连接另一端的身份，可以设置此模式。连接仍是加密的，且如果请求，套接字仍会向对端发送本地证书。
- `QSslSocket::QueryPeer`：`1`;`QSslSocket`会向对等方请求证书，但不要求该证书必须有效。当你希望向用户显示对等证书详情而不影响实际的SSL握手时，这非常有用。此模式是服务器的默认模式。注意：在Schannel中，该值的作用与VerifyNone相同。
- `QSslSocket::VerifyPeer`：`2`;`QSslSocket` 会在 SSL 握手阶段向对方请求证书，并要求该证书有效。失败时，会`QSslSocket`发出`QSslSocket::sslErrors()`信号。此模式是客户端的默认模式。
- `QSslSocket::AutoVerifyPeer`：`3`;`QSslSocket`会自动使用QueryPeer表示服务器套接字，VerifyPeer表示客户端套接字。

### `enum QSslSocket::SslMode`

**作用与语义：**

描述`QSslSocket`可用的连接模式。
- `QSslSocket::UnencryptedMode`：`0`;套接字未加密。其行为与`QTcpSocket`相同。
- `QSslSocket::SslClientMode`：`1`;套接字是客户端SSL套接字。它要么已经加密，要么处于SSL握手阶段（见`QSslSocket::isEncrypted()`）。
- `QSslSocket::SslServerMode`：`2`;套接字是服务器端的SSL套接字。它要么已经加密，要么处于SSL握手阶段（参见 `QSslSocket::isEncrypted()`）。

### `[explicit] QSslSocket::QSslSocket(QObject *parent = nullptr)`

**作用与语义：**

构造一个 QSslSocket 对象。`parent` 传递给 `QObject` 的构造函数。新套接字的 `cipher` 套件设置为静态方法 defaultCiphers() 返回的那个。

### `[virtual noexcept] QSslSocket::~QSslSocket()`

**作用与语义：**

摧毁了`QSslSocket`。

### `[static, since 6.1] QString QSslSocket::activeBackend()`

**作用与语义：**

返回`QSslSocket`及相关类使用的后端名称。如果活动后端未被显式设置，该函数返回`QSslSocket`从可用后端列表中隐式选择的默认后端名称。
注意：在隐式选择默认后端时，`QSslSocket` 会优先选择 OpenSSL 后端（如果有的话）。如果没有 Schannel 后端，Windows 隐式选择 Schannel 后端，在 Darwin 平台上选择 Secure Transport。如果找不到自定义 TLS 后端，则使用该后端。如果找不到其他后端，则选择“仅证书”后端。有关 TLS 插件的更多信息，请参见“从源构建 Qt 时启用和禁用 SSL 支持”。

### `[signal] void QSslSocket::alertReceived(QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`

**作用与语义：**

如果收到来自对等端的警报消息，`QSslSocket`会发出该信号。`level`表示警报是致命还是警告。`type`是解释为何发送警报的代码。当有警报消息的文本描述时，会以`description`形式提供。
注意：该信号主要用于信息和调试目的，不需要在应用程序中处理。如果警报是致命的，底层后端会处理并关闭连接。
注意：并非所有后端都支持此功能。

### `[signal] void QSslSocket::alertSent(QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`

**作用与语义：**

如果向对等端发送了警报消息，`QSslSocket`会发出该信号。`level`描述该信号是警告还是致命错误。`type`给出警报消息的代码。当有警报消息的文本描述时，会以`description`形式提供。
注意：该信号主要用于信息性，可用于调试，通常不需要应用程序执行任何操作。
注意：并非所有后端都支持此功能。

### `[override virtual] bool QSslSocket::atEnd() const`

**作用与语义：**

重装：`QIODevice::atEnd()` const.

### `[static, since 6.1] QList<QString> QSslSocket::availableBackends()`

**作用与语义：**

返回当前可用后端的名称。这些名称为小写，例如“openssl”、“securetransport”、“schannel”（类似于 Qt 中已有的 TLS 后端功能名称）。

### `[override virtual] qint64 QSslSocket::bytesAvailable() const`

**作用与语义：**

重装：`QAbstractSocket::bytesAvailable()` const.
返回可立即读取的已解密字节数量。

### `[override virtual] qint64 QSslSocket::bytesToWrite() const`

**作用与语义：**

重装：`QAbstractSocket::bytesToWrite()` const.
返回等待加密并写入网络的未加密字节数量。

### `[override virtual] bool QSslSocket::canReadLine() const`

**作用与语义：**

重装：`QIODevice::canReadLine()` const.
如果你能读取一行解密字符（以一个ASCII '\n'结尾）的当代行，返回`true`;否则返回为false。

### `[override virtual] void QSslSocket::close()`

**作用与语义：**

重装：`QAbstractSocket::close()`。

### `[override virtual] void QSslSocket::connectToHost(const QString &hostName, quint16 port, QIODeviceBase::OpenMode openMode = ReadWrite, QAbstractSocket::NetworkLayerProtocol protocol = AnyIPProtocol)`

**作用与语义：**

重实现自：`QAbstractSocket::connectToHost`（const QString &hostName， quint16 port， QIODeviceBase：：OpenMode openMode， QAbstractSocket：：NetworkLayerProtocol 协议）。
尝试在给定`port`上与`hostName`建立连接。`protocol`参数可用于指定使用哪种网络协议（例如，IPv4 或 IPv6）。
套接字在给定`openMode`中打开，首先进入`HostLookupState`，然后对`hostName`进行主机名查询。如果查找成功，`hostFound()`会被发射，`QAbstractSocket`进入`ConnectingState`。然后它尝试连接到查找返回的地址或多个地址。最后，如果建立连接，`QAbstractSocket`进入`ConnectedState`并发出`connected()`。
在任何时刻，套筒都可以发出`errorOccurred()`来表示发生了错误。
`hostName`可以是字符串形式的IP地址（例如，“43.195.83.32”），也可以是主机名（例如，“example.com”）。`QAbstractSocket`只有在需要时才会进行查找。`port`按本地字节顺序排列。

### `void QSslSocket::connectToHostEncrypted(const QString &hostName, quint16 port, QIODeviceBase::OpenMode mode = ReadWrite, QAbstractSocket::NetworkLayerProtocol protocol = AnyIPProtocol)`

**作用与语义：**

在`port`上与设备`hostName`启动加密连接，使用`mode`作为`OpenMode`。这相当于先调用`connectToHost()`建立连接，然后再调用`startClientEncryption()`。`protocol`参数可用于指定使用哪种网络协议（例如：IPv4或IPv6）。
`QSslSocket`首先进入HostLookupState。然后，在进入事件循环或waitFor...函数后，进入ConnectingState，发出`connected()`，然后发起SSL客户端握手。每当状态发生变化时，`QSslSocket`会发出信号`stateChanged()`。
发起SSL客户端握手后，如果无法确认对端身份，会发出`sslErrors()`信号。如果你想忽略错误继续连接，必须在连接到`sslErrors()`信号的槽函数内调用`ignoreSslErrors()`，或在进入加密模式之前。如果未调用`ignoreSslErrors()`，连接会中断，信号`disconnected()`发出，`QSslSocket`返回UnconnectedState。
如果SSL握手成功，`QSslSocket`会发出`encrypted()`。
注意：上述示例表明，文本可以在请求加密连接后立即写入套接字，且在`encrypted()`信号尚未发出之前。在这种情况下，文本会被排队到对象中，并在连接建立且`encrypted()`信号发出后写入套接字。
`mode`默认是`ReadWrite`。
如果你想在连接的服务器端创建`QSslSocket`，应该在通过`QTcpServer`接收到来的连接后直接联系`startServerEncryption()`。

**官方示例：**

```cpp
 QSslSocket socket;
 connect(&socket, &QSslSocket::encrypted, receiver, &Receiver::socketEncrypted);

 socket.connectToHostEncrypted("imap", 993);
 socket->write("1 CAPABILITY\r\n");
```

### `void QSslSocket::connectToHostEncrypted(const QString &hostName, quint16 port, const QString &sslPeerName, QIODeviceBase::OpenMode mode = ReadWrite, QAbstractSocket::NetworkLayerProtocol protocol = AnyIPProtocol)`

**作用与语义：**

除了 connectToHostEncrypted 的原始行为外，这种重载方法还允许在证书验证中使用不同的主机名（`sslPeerName`），而不是用于 TCP 连接的主机名（`hostName`）。

### `[since 6.0] void QSslSocket::continueInterruptedHandshake()`

**作用与语义：**

如果应用程序在收到`handshakeInterruptedOnError()`信号后仍想结束握手，必须调用该函数。该调用必须通过附加在信号上的槽函数进行。信号-槽连接必须是直接的。

### `[override virtual] void QSslSocket::disconnectFromHost()`

**作用与语义：**

重装：`QAbstractSocket::disconnectFromHost()`。
尝试关闭套接字。如果有待写入的数据，`QAbstractSocket`会进入`ClosingState`并等待所有数据写入。最终，它会进入`UnconnectedState`并发出`disconnected()`信号。

### `[signal] void QSslSocket::encrypted()`

**作用与语义：**

当`QSslSocket`进入加密模式时，该信号会被发射。该信号发出后，`QSslSocket::isEncrypted()`将返回真值，所有后续的传输都将被加密。

### `qint64 QSslSocket::encryptedBytesAvailable() const`

**作用与语义：**

返回等待解密的加密字节数。通常，这个函数返回0，因为`QSslSocket`会尽快解密输入数据。

### `qint64 QSslSocket::encryptedBytesToWrite() const`

**作用与语义：**

返回等待写入网络的加密字节数量。

### `[signal] void QSslSocket::encryptedBytesWritten(qint64 written)`

**作用与语义：**

当`QSslSocket`将其加密数据写入网络时，该信号会发出。`written`参数包含成功写入的字节数。

### `[signal] void QSslSocket::handshakeInterruptedOnError(const QSslError &error)`

**作用与语义：**

如果发现证书验证错误且`QSslConfiguration`启用了早期错误报告，`QSslSocket`会发出该信号。应用程序应检查`error`，决定是否继续握手，或中止握手并向对端发送警报消息。信号-槽函数连接必须是直接的。

### `[slot] void QSslSocket::ignoreSslErrors()`

**作用与语义：**

该槽函数告诉`QSslSocket`在`QSslSocket`握手阶段忽略错误，继续连接。如果你想在握手阶段发生错误继续连接，必须从连接`sslErrors()`的槽函数中调用该槽函数，或在握手阶段前调用。如果你不在错误时或握手前调用该槽函数，`sslErrors()`信号发出后连接将被中断。
如果SSL握手阶段没有错误（即对等端身份无碍确认），`QSslSocket`不会发出`sslErrors()`信号，无需调用此功能。
警告：请务必让用户检查`sslErrors()`信号报告的错误，只有在用户确认继续时才调用此方法。如果出现意外错误，应中止连接。未检查实际错误就调用此方法，很可能会对你的应用构成安全风险。请务必小心使用！
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
sslSocket， qOverload<>（&QSslSocket：：ignoreSslErrors））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
sslSocket， [receiver = sslSocket]() { receiver->ignoreSslErrors(); }）;


更多示例和方法，请参见连接超载槽位。

### `void QSslSocket::ignoreSslErrors(const QList<QSslError> &errors)`

**作用与语义：**

该方法只`QSslSocket`忽略`errors`中给出的错误。
注意：由于大多数SSL错误与证书相关，因此大多数SSL错误必须设置与该SSL错误相关的预期证书。例如，如果你想连接到使用自签名证书的服务器，请考虑以下摘要：
多次调用该函数会替换之前调用中传递的错误列表。你可以通过调用该函数时用空列表清除你想忽略的错误列表。

**官方示例：**

```cpp
 QList<QSslCertificate> cert = QSslCertificate::fromPath("server-certificate.pem"_L1);
 QSslError error(QSslError::SelfSignedCertificate, cert.at(0));
 QList<QSslError> expectedSslErrors;
 expectedSslErrors.append(error);

 QSslSocket socket;
 socket.ignoreSslErrors(expectedSslErrors);
 socket.connectToHostEncrypted("server.tld", 443);
```

### `[static, since 6.1] QList<QSsl::ImplementedClass> QSslSocket::implementedClasses(const QString &backendName = {})`

**作用与语义：**

该函数返回由后端实现的后端特定类，名称为 `backendName`。空`backendName`被理解为对当前激活后端的查询。

### `[static, since 6.1] bool QSslSocket::isClassImplemented(QSsl::ImplementedClass cl, const QString &backendName = {})`

**作用与语义：**

如果后端实现了名为 `backendName` 的类`cl`，则返回为真。空 `backendName` 被理解为对当前激活后端的查询。

### `bool QSslSocket::isEncrypted() const`

**作用与语义：**

如果套接字加密，返回`true`;否则返回 false。
加密套接字在数据写入网络前，通过调用`write()`或`putChar()`写入的所有数据进行加密，并在从网络接收数据时解密所有入站数据，在你调用`read()`、`readLine()`或`getChar()`之前。
`QSslSocket`进入加密模式时会发出`encrypted()`。
你可以调用`sessionCipher()`，查找用于加密和解密数据的密码。

### `[static, since 6.1] bool QSslSocket::isFeatureSupported(QSsl::SupportedFeature ft, const QString &backendName = {})`

**作用与语义：**

如果某个功能`ft`由名为`backendName`的后端支持，则返回为真。空`backendName`被理解为对当前活跃后端的查询。

### `[static, since 6.1] bool QSslSocket::isProtocolSupported(QSsl::SslProtocol protocol, const QString &backendName = {})`

**作用与语义：**

如果`protocol`由名为`backendName`的后端支持，则返回为真。空`backendName`被理解为对当前激活后端的查询。

### `QSslCertificate QSslSocket::localCertificate() const`

**作用与语义：**

返回套接字的本地`certificate`，若未分配本地证书则返回空证书。

### `QList<QSslCertificate> QSslSocket::localCertificateChain() const`

**作用与语义：**

返回套接字的本地`certificate`链，若未分配本地证书则返回空列表。

### `QSslSocket::SslMode QSslSocket::mode() const`

**作用与语义：**

返回套接字当前模式;要么是`UnencryptedMode`，`QSslSocket`行为与`QTcpSocket`相同，要么是`SslClientMode`或`SslServerMode`，客户端要么协商，要么处于加密模式。
当模式切换时，`QSslSocket`会发出`modeChanged()`。

### `[signal] void QSslSocket::modeChanged(QSslSocket::SslMode mode)`

**作用与语义：**

当`QSslSocket`从`QSslSocket::UnencryptedMode`切换到`QSslSocket::SslClientMode`或`QSslSocket::SslServerMode`时，会发出该信号。`mode`是新的模式。

### `[signal] void QSslSocket::newSessionTicketReceived()`

**作用与语义：**

如果TLS 1.3协议在握手时协商完成，`QSslSocket`在收到NewSessionTicket消息后发出该信号。会话和会话工单的生命周期提示会在套接字配置中更新。该会话可用于未来TLS连接中的会话恢复（及缩短握手）。
注意：此功能仅在OpenSSL后端启用，且需要OpenSSL v.1.1及以上版本。

### `QList<QOcspResponse> QSslSocket::ocspResponses() const`

**作用与语义：**

该功能返回服务器在TLS握手期间通过OCSP订书钉发送的在线证书状态协议响应。如果没有收到明确的响应或完全没有响应，列表为空。

### `QSslCertificate QSslSocket::peerCertificate() const`

**作用与语义：**

返回对等方的数字证书（即你连接主机的直接证书），如果对方未分配证书，则返回空证书。
对等证书在握手阶段会自动检查，因此此功能通常用于获取显示或连接诊断目的的证书。它包含关于对等方的信息，包括主机名、证书发行方和对等方的公钥。
由于对等证书是在握手阶段设置的，因此从连接到`sslErrors()`信号或`encrypted()`信号的槽函数访问对等证书是安全的。
如果返回空证书，可能意味着SSL握手失败，或者你连接的主机没有证书，或者表示没有连接。
如果你想查看对方完整的证书链，可以用`peerCertificateChain()`一次性获取所有证书。

### `QList<QSslCertificate> QSslSocket::peerCertificateChain() const`

**作用与语义：**

返回对等方的数字证书链，或一个空白的证书列表。
对等证书在握手阶段自动检查。此功能通常用于获取显示或连接诊断的证书。证书包含关于对等方和证书发行方的信息，包括主机名称、发行者名称和发行者公钥。
在握手阶段，对等证书会在`QSslSocket`中设置，因此从连接到`sslErrors()`信号或`encrypted()`信号的槽函数调用此功能是安全的。
如果返回空列表，可能意味着SSL握手失败，或者你连接的主机没有证书，或者表示没有连接。
如果你只想获得对等节点的直接证书，可以用`peerCertificate()`。

### `int QSslSocket::peerVerifyDepth() const`

**作用与语义：**

返回对等方证书链中SSL握手阶段需检查的最大证书数，若未设置最大深度则返回0（默认），表示应检查整个证书链。
证书按发出顺序检查，先是对等方自身的证书，然后是其发行方的证书，依此类推。

### `[signal] void QSslSocket::peerVerifyError(const QSslError &error)`

**作用与语义：**

`QSslSocket`在SSL握手期间，在加密尚未建立之前多次发出该信号，以表明在确认对等端身份时发生了错误。`error`通常表示`QSslSocket`无法安全识别对等端。
该信号能提前提示异常。通过连接该信号，您可以在握手完成前手动选择从连接槽内断开连接。如果未采取任何操作，`QSslSocket`将继续发出`QSslSocket::sslErrors()`。

### `QSslSocket::PeerVerifyMode QSslSocket::peerVerifyMode() const`

**作用与语义：**

返回套接字的验证模式。该模式决定`QSslSocket`应向对端请求证书（即客户端向服务器请求证书，或服务器向客户端请求证书），以及是否要求该证书有效。
默认模式是`AutoVerifyPeer`，告诉`QSslSocket`客户端使用`VerifyPeer`，服务器使用`QueryPeer`。

### `QString QSslSocket::peerVerifyName() const`

**作用与语义：**

返回证书验证的不同主机名，由`setPeerVerifyName`或`connectToHostEncrypted`设置。

### `[signal] void QSslSocket::preSharedKeyAuthenticationRequired(QSslPreSharedKeyAuthenticator *authenticator)`

**作用与语义：**

`QSslSocket`在协商PSK密码套件时会发出该信号，因此需要PSK认证。
使用PSK时，客户端必须向服务器发送有效的身份和有效的预共享密钥，才能继续SSL握手。应用程序可以通过根据需求填写传递的`authenticator`对象，在连接到该信号的槽函数中提供这些信息。
注意：忽视该信号或未提供所需凭证，将导致握手失败，连接将被终止。
注意：`authenticator`对象归套接字所有，应用程序不得删除。

### `QSslKey QSslSocket::privateKey() const`

**作用与语义：**

返回该套接字的私钥。

### `QSsl::SslProtocol QSslSocket::protocol() const`

**作用与语义：**

返回套接字的SSL协议。默认情况下，使用`QSsl::SecureProtocols`。

### `[override virtual protected] qint64 QSslSocket::readData(char *data, qint64 maxlen)`

**作用与语义：**

从已经解密的 SSL 接收缓冲区复制最多 `maxlen` 字节到 `data`，返回读取字节数，失败返回 -1。它由 `QIODevice::read()` 间接调用；客户端通常应等到 `encrypted()` 且收到 `readyRead()` 后再读取。

### `[override virtual] void QSslSocket::resume()`

**作用与语义：**

重装：`QAbstractSocket::resume()`。
在套接字暂停后继续传输数据。如果该套接字被调用了“setPauseMode（`QAbstractSocket::PauseOnSslErrors`）;”并收到`sslErrors()`信号，则必须调用该方法才能让套接字继续。
继续在套接字上传输数据。该方法应仅在套接字被设置为通知暂停且收到通知后使用。目前唯一支持的通知是`QSslSocket::sslErrors()`。如果套接字未暂停，调用此方法会导致行为未定义。

### `QSslCipher QSslSocket::sessionCipher() const`

**作用与语义：**

返回套接字的密码`cipher`，如果连接未加密，则返回空密码。会话的套接字密码在握手阶段设置。密码用于加密和解密通过套接字传输的数据。
`QSslSocket`还提供了设置有序密码列表的函数，这些列表最终会在握手阶段中选择会话密码。该有序列表必须在握手阶段开始前就已存在。

### `QSsl::SslProtocol QSslSocket::sessionProtocol() const`

**作用与语义：**

返回套接字的SSL/TLS协议，如果连接未加密，则返回未知协议。会话的套接字协议在握手阶段设置。

### `[static, since 6.1] bool QSslSocket::setActiveBackend(const QString &backendName)`

**作用与语义：**

如果后端名称为`backendName`，则返回为真。`backendName`必须是`availableBackends()`返回的名称之一。
注意：应用程序不能同时混合不同的后端。这意味着在使用`QSslSocket`类或相关类（如 `QSslCertificate` 或 `QSslKey`）之前，必须选择非默认后端。

### `void QSslSocket::setLocalCertificate(const QSslCertificate &certificate)`

**作用与语义：**

将套接字的本地证书设置为`certificate`。如果你需要向对方确认身份，本地证书是必需的。它与私钥一起使用;如果你设置了本地证书，也必须设置私钥。
本地证书和私钥对服务器套接字总是必要，但如果服务器需要客户端认证，客户端套接字很少使用本地证书和私钥。
注意：macOS 上的 Secure Transport SSL 后端可能会通过导入本地证书和密钥来更新默认密钥链（默认可能是你的登录密钥链）。这也可能导致系统对话框出现，并在应用使用这些私钥时请求权限。如果不希望出现此类行为，请将QT_SSL_USE_TEMPORARY_KEYCHAIN环境变量设置为非零值;这会提示`QSslSocket`使用自己的临时密钥链。

### `void QSslSocket::setLocalCertificate(const QString &path, QSsl::EncodingFormat format = QSsl::Pem)`

**作用与语义：**

将套接字的本地`certificate`设置为文件`path`中的第一个，并根据指定的 `format` 进行解析。

### `void QSslSocket::setLocalCertificateChain(const QList<QSslCertificate> &localChain)`

**作用与语义：**

设置在SSL握手期间向对等端展示的证书链`localChain`。

### `void QSslSocket::setPeerVerifyDepth(int depth)`

**作用与语义：**

在SSL握手阶段，将对端证书链中需要检查的最大证书数量设置为`depth`。设置深度为0意味着不设置最大深度，表示应检查整个证书链。
证书按发出顺序检查，先是对等方自身的证书，然后是其发行方的证书，依此类推。

### `void QSslSocket::setPeerVerifyMode(QSslSocket::PeerVerifyMode mode)`

**作用与语义：**

将套接字的验证模式设置为`mode`。该模式决定`QSslSocket`应向对端请求证书（即客户端向服务器请求证书，或服务器向客户端请求证书），以及是否要求该证书有效。
默认模式是`AutoVerifyPeer`，告诉`QSslSocket`客户端使用`VerifyPeer`，服务器使用`QueryPeer`。
加密开始后设置此模式不会影响当前连接。

### `void QSslSocket::setPeerVerifyName(const QString &hostName)`

**作用与语义：**

为证书验证设置一个不同的主机名，由`hostName`给出，而不是用于TCP连接的主机。

### `void QSslSocket::setPrivateKey(const QSslKey &key)`

**作用与语义：**

将套接字的私有`key`设置为`key`。私钥和本地`certificate`被需要向SSL对等端证明身份的客户端和服务器使用。
如果你创建 SSL 服务器套接字，密钥和本地证书都是必需的。如果你创建 SSL 客户端套接字，那么如果客户端必须向 SSL 服务器识别自己，密钥和本地证书是必需的。

### `void QSslSocket::setPrivateKey(const QString &fileName, QSsl::KeyAlgorithm algorithm = QSsl::Rsa, QSsl::EncodingFormat format = QSsl::Pem, const QByteArray &passPhrase = QByteArray())`

**作用与语义：**

读取文件`fileName`中的字符串，并使用指定的`algorithm`和编码`format`解码，构建SSL密钥。如果编码密钥被加密，`passPhrase`用于解密。
套接字的私钥设置为构造密钥。私钥和本地`certificate`被客户端和服务器使用，他们需要向SSL对等方证明身份。
如果你创建 SSL 服务器套接字，密钥和本地证书都是必需的。如果你创建 SSL 客户端套接字，那么如果客户端必须向 SSL 服务器识别自己，密钥和本地证书是必需的。

### `void QSslSocket::setProtocol(QSsl::SslProtocol protocol)`

**作用与语义：**

将套接字的 SSL 协议设置为 `protocol`。这会影响下一次发起的握手;在已加密的套接字上调用此功能不会影响套接字的协议。

### `[override virtual] void QSslSocket::setReadBufferSize(qint64 size)`

**作用与语义：**

重制版本：`QAbstractSocket::setReadBufferSize`（qint64 尺寸）。
将`QSslSocket`内部读取缓冲区的大小设置为`size`字节。
将`QAbstractSocket`内部读取缓冲区的大小设置为`size`字节。
如果缓冲区大小被限制在某个特定大小，`QAbstractSocket`不会缓冲超过这个大小的数据。例外情况下，缓冲区大小为0意味着读取缓冲区是无限的，所有输入数据都被缓冲。这是默认值。
如果你只在特定时间点读取数据（例如在实时流媒体应用中），或者想保护套接字免受过多数据接收，避免最终导致内存不足，这个选项非常有用。
只有`QTcpSocket`使用`QAbstractSocket`的内部缓冲区;`QUdpSocket`完全不使用缓冲，而是依赖操作系统提供的隐式缓冲。因此，调用该函数对`QUdpSocket`没有影响。

### `[override virtual] bool QSslSocket::setSocketDescriptor(qintptr socketDescriptor, QAbstractSocket::SocketState state = ConnectedState, QIODeviceBase::OpenMode openMode = ReadWrite)`

**作用与语义：**

重实现自：`QAbstractSocket::setSocketDescriptor`（qintptr socketDescriptor， QAbstractSocket：： SocketState socketState， QIODeviceBase：：OpenMode openMode）.
用本地套接字描述符`socketDescriptor`初始化`QSslSocket`。如果`socketDescriptor`被接受为有效的套接字描述符，返回`true`;否则返回`false`。套接字以`openMode`指定的模式打开，进入`state`指定的套接字状态。
注意：无法用相同的本地套接字描述符初始化两个套接字。
用本地套接字描述符`socketDescriptor`初始化`QAbstractSocket`。如果`socketDescriptor`被接受为有效的套接字描述符，返回`true`;否则返回`false`。套接字以`openMode`指定的模式打开，进入`socketState`指定的套接字状态。读取和写缓冲区被清除，丢弃所有待处理的数据。
注意：无法用相同的本地套接字描述符初始化两个抽象套接字。

### `[override virtual] void QSslSocket::setSocketOption(QAbstractSocket::SocketOption option, const QVariant &value)`

**作用与语义：**

重实现自：`QAbstractSocket::setSocketOption`（QAbstractSocket：：SocketOption option，const QVariant &value）。
将给定`option`设置为`value`描述的值。
将给定`option`设置为`value`描述的值。
注意：由于选项设置在内部套接字上，选项仅在套接字已被创建时生效。这只有在调用`bind()`后或`connected()`已发出时才会生效。

### `void QSslSocket::setSslConfiguration(const QSslConfiguration &configuration)`

**作用与语义：**

将套接字的 SSL 配置设置为 `configuration` 的内容。该函数将本地证书、密码、私钥和 CA 证书设置为存储在 `configuration` 中的证书。
无法设置与SSL状态相关的字段。

### `[override virtual protected] qint64 QSslSocket::skipData(qint64 maxSize)`

**作用与语义：**

重构版本：`QAbstractSocket::skipData`（qint64 maxSize）。

### `[override virtual] QVariant QSslSocket::socketOption(QAbstractSocket::SocketOption option)`

**作用与语义：**

重实现自：`QAbstractSocket::socketOption`（QAbstractSocket：：SocketOption 选项）。
返回`option`期权的价值。
返回`option`期权的价值。

### `QSslConfiguration QSslSocket::sslConfiguration() const`

**作用与语义：**

返回套接字的 SSL 配置状态。套接字的默认 SSL 配置是使用默认密码、默认 CA 证书，不使用本地私钥或证书。
SSL配置还包含可能随时变化且未预警的字段。

### `[signal] void QSslSocket::sslErrors(const QList<QSslError> &errors)`

**作用与语义：**

`QSslSocket`在SSL握手后发出该信号，表示在建立对等端身份时发生了一个或多个错误。这些错误通常表明`QSslSocket`无法安全识别对等端。除非采取任何措施，否则该信号发出后连接将被中断。
如果你想在发生错误的情况下继续连接，必须从连接到该信号的槽函数内调用`QSslSocket::ignoreSslErrors()`。如果你需要以后访问错误列表，可以调用`sslHandshakeErrors()`。
`errors`包含一个或多个错误，阻止`QSslSocket`验证对等端的身份。
注意：连接该信号时不能使用`Qt::QueuedConnection`，否则调用`QSslSocket::ignoreSslErrors()`也无效。

### `QList<QSslError> QSslSocket::sslHandshakeErrors() const`

**作用与语义：**

返回最近发生的SSL错误列表。这与`QSslSocket`通过`sslErrors()`信号传递的列表相同。如果连接已加密且无错误，该函数将返回一个空列表。

### `[static] long QSslSocket::sslLibraryBuildVersionNumber()`

**作用与语义：**

返回编译时正在使用的SSL库的版本号。如果没有SSL支持，则返回-1。

### `[static] QString QSslSocket::sslLibraryBuildVersionString()`

**作用与语义：**

返回编译时正在使用的SSL库的版本字符串。如果没有SSL支持，则返回空值。

### `[static] long QSslSocket::sslLibraryVersionNumber()`

**作用与语义：**

返回正在使用的SSL库的版本号。注意，这是运行时使用的库版本，而非编译时。如果没有SSL支持，则返回-1。

### `[static] QString QSslSocket::sslLibraryVersionString()`

**作用与语义：**

返回正在使用的SSL库的版本字符串。注意，这是运行时使用的库版本，而非编译时。如果没有SSL支持，则返回空值。

### `[slot] void QSslSocket::startClientEncryption()`

**作用与语义：**

启动针对客户端连接的延迟 SSL 握手。当套接字处于 `ConnectedState` 但仍处于 `UnencryptedMode` 时，可以调用此函数。如果尚未连接，或者已经加密，该函数无效。实现 STARTTLS 功能的客户端通常会使用延迟 SSL 握手。大多数其他客户端可以通过使用 `connectToHostEncrypted()` 来避免直接调用此函数，该函数会自动执行握手。

### `[slot] void QSslSocket::startServerEncryption()`

**作用与语义：**

启动针对服务器连接的延迟 SSL 握手。当套接字处于 `ConnectedState` 但仍处于 `UnencryptedMode` 时，可以调用此函数。如果尚未连接或已经加密，则函数无效。对于服务器套接字，调用此函数是启动 SSL 握手的唯一方式。大多数服务器会在收到连接时立即调用此函数，或者在收到进入 SSL 模式的协议特定命令后调用（例如，服务器可能在收到字符串 "STARTTLS\r\n" 时调用此函数）。实现 SSL 服务器的最常见方法是创建 `QTcpServer` 的子类并重新实现 `QTcpServer::incomingConnection()`。返回的套接字描述符随后传递给 `QSslSocket::setSocketDescriptor()`。

### `[static, since 6.1] QList<QSsl::SupportedFeature> QSslSocket::supportedFeatures(const QString &backendName = {})`

**作用与语义：**

该函数返回由名为 `backendName` 的后端支持的功能。空 `backendName` 被理解为对当前激活后端的查询。

### `[static, since 6.1] QList<QSsl::SslProtocol> QSslSocket::supportedProtocols(const QString &backendName = {})`

**作用与语义：**

如果有名为 `backendName` 的后端，该函数返回该后端支持的 TLS 协议版本列表。空 `backendName` 被理解为对当前活跃后端的查询。否则，该函数返回空列表。

### `[static] bool QSslSocket::supportsSsl()`

**作用与语义：**

如果该平台支持 SSL，返回 `true`;否则返回 false。如果平台不支持 SSL，套接字将在连接阶段失败。

### `[override virtual] bool QSslSocket::waitForBytesWritten(int msecs = 30000)`

**作用与语义：**

重装：`QAbstractSocket::waitForBytesWritten`（int msecs）。

### `[override virtual] bool QSslSocket::waitForConnected(int msecs = 30000)`

**作用与语义：**

重实现自：`QAbstractSocket::waitForConnected`（int msecs）。
等待套筒连接，或`msecs`毫秒，以先到者为准。如果连接已建立，该函数返回`true`;否则返回`false`。
等待套接字连接，最多可达`msecs`毫秒。如果连接已建立，该函数返回`true`;否则返回`false`。如果返回`false`，你可以调用`error()`来确定错误原因。
以下示例等待最多一秒以建立连接：
如果 msecs 为 -1，该函数不会超时。
注意：该函数可能会比 `msecs` 稍长，具体取决于完成主机查找所需的时间。
注意：多次调用这些函数不会累计时间。如果函数超时，连接进程将被中止。
注意：该功能在Windows上可能会随机失效。如果你的软件能在Windows上运行，建议使用事件循环和`connected()`信号。

### `[override virtual] bool QSslSocket::waitForDisconnected(int msecs = 30000)`

**作用与语义：**

重装：`QAbstractSocket::waitForDisconnected`（int msecs）。
等待套接字断开连接或`msecs`毫秒，以先到者为准。如果连接断开，该函数返回`true`;否则返回`false`。
等待套接字断开连接，最多可达`msecs`毫秒。如果连接成功断开，该函数返回`true`;否则返回`false`（如果操作超时、发生错误或该`QAbstractSocket`已断开）。如果返回`false`，你可以调用`error()`来确定错误原因。
以下示例等待连接关闭最多一秒钟：
如果 msecs 为 -1，该函数不会超时。
注意：该功能在Windows上可能会随机失效。如果你的软件能在Windows上运行，可以考虑使用事件循环和`disconnected()`信号。

### `bool QSslSocket::waitForEncrypted(int msecs = 30000)`

**作用与语义：**

等待套接字完成SSL握手并发出`encrypted()`毫秒，或`msecs`毫秒，以先到者为准。如果已发出`encrypted()`，该函数返回为true;否则（例如套接字断开或SSL握手失败），则返回false。
以下示例等待最多一秒钟以实现套接字加密：
如果 msecs 为 -1，该函数不会超时。

**官方示例：**

```cpp
 socket->connectToHostEncrypted("imap", 993);
 if (socket->waitForEncrypted(1000))
     qDebug("Encrypted!");
```

### `[override virtual] bool QSslSocket::waitForReadyRead(int msecs = 30000)`

**作用与语义：**

重实现自：`QAbstractSocket::waitForReadyRead`（int msecs）。

### `[override virtual protected] qint64 QSslSocket::writeData(const char *data, qint64 len)`

**作用与语义：**

把最多 `len` 字节交给 SSL 层加密并排入发送缓冲区，返回已接受字节数，失败返回 -1。握手完成前写入的数据会排队；`bytesWritten()` 表示写出进度，不能据此假定对端已经处理。

### `[since 6.0] enum class AlertLevel`

**作用与语义：**

描述警报消息的级别。
该枚举描述了发送或接收的警报消息的级别。
- `QSslSocket::AlertLevel::Warning`：`0`;非致命警报信息
- `QSslSocket::AlertLevel::Fatal`：`1`;致命警报消息，底层后端会正确处理此类警报并关闭连接。
- `QSslSocket::AlertLevel::Unknown`：`2`;严重程度未知的警报。
该枚举是在Qt 6.0中引入的。

### `[since 6.0] enum class AlertType`

**作用与语义：**

枚举警报消息可能包含的代码。
有关可能的值及其含义，请参见RFC 8446第6节。
- `QSslSocket::AlertType::CloseNotify`：`0`;,
- `QSslSocket::AlertType::UnexpectedMessage`：`10`
- `QSslSocket::AlertType::BadRecordMac`：`20`
- `QSslSocket::AlertType::RecordOverflow`：`22`
- `QSslSocket::AlertType::DecompressionFailure`：`30`
- `QSslSocket::AlertType::HandshakeFailure`：`40`
- `QSslSocket::AlertType::NoCertificate`：`41`
- `QSslSocket::AlertType::BadCertificate`：`42`
- `QSslSocket::AlertType::UnsupportedCertificate`：`43`
- `QSslSocket::AlertType::CertificateRevoked`：`44`
- `QSslSocket::AlertType::CertificateExpired`：`45`
- `QSslSocket::AlertType::CertificateUnknown`：`46`
- `QSslSocket::AlertType::IllegalParameter`：`47`
- `QSslSocket::AlertType::UnknownCa`：`48`
- `QSslSocket::AlertType::AccessDenied`：`49`
- `QSslSocket::AlertType::DecodeError`：`50`
- `QSslSocket::AlertType::DecryptError`：`51`
- `QSslSocket::AlertType::ExportRestriction`：`60`
- `QSslSocket::AlertType::ProtocolVersion`：`70`
- `QSslSocket::AlertType::InsufficientSecurity`：`71`
- `QSslSocket::AlertType::InternalError`：`80`
- `QSslSocket::AlertType::InappropriateFallback`：`86`
- `QSslSocket::AlertType::UserCancelled`：`90`
- `QSslSocket::AlertType::NoRenegotiation`：`100`
- `QSslSocket::AlertType::MissingExtension`：`109`
- `QSslSocket::AlertType::UnsupportedExtension`：`110`
- `QSslSocket::AlertType::CertificateUnobtainable`：`111`
- `QSslSocket::AlertType::UnrecognizedName`：`112`
- `QSslSocket::AlertType::BadCertificateStatusResponse`：`113`
- `QSslSocket::AlertType::BadCertificateHashValue`：`114`
- `QSslSocket::AlertType::UnknownPskIdentity`：`115`
- `QSslSocket::AlertType::CertificateRequired`：`116`
- `QSslSocket::AlertType::NoApplicationProtocol`：`120`
- `QSslSocket::AlertType::UnknownAlertMessage`：`255`
该枚举是在Qt 6.0中引入的。

### `[since 6.1] enum class ImplementedClass`

**作用与语义：**

枚举TLS后端实现的类。
`QtNetwork`中，有些类具有后端特定实现，因此可以保持不实现。枚举中的枚举器表示哪个类在后端有可运行的实现。
- `QSslSocket::ImplementedClass::Key`：`0`;`QSslKey`级。
- `QSslSocket::ImplementedClass::Certificate`：`1`;`QSslCertificate`级。
- `QSslSocket::ImplementedClass::Socket`：`2`;`QSslSocket`级。
- `QSslSocket::ImplementedClass::DiffieHellman`：`3`;`QSslDiffieHellmanParameters`级。
- `QSslSocket::ImplementedClass::EllipticCurve`：`4`;`QSslEllipticCurve`级。
- `QSslSocket::ImplementedClass::Dtls`：`5`;`QDtls`级。
- `QSslSocket::ImplementedClass::DtlsCookie`：`6`;`QDtlsClientVerifier`级。
这个枚举是在Qt 6.1引入的。

### `[since 6.1] enum class SupportedFeature`

**作用与语义：**

枚举TLS后端可能支持的功能。
`QtNetwork` TLS 相关类有公共 API，但某些后端可能未实现，例如我们的 SecureTransport 后端不支持服务器端 ALPN。SupportedFeature 枚举的枚举表示某功能被支持。
- `QSslSocket::SupportedFeature::CertificateVerification`：`0`;表示`QSslCertificate::verify()`由后端实现。
- `QSslSocket::SupportedFeature::ClientSideAlpn`：`1`;客户端ALPN（应用层协议协商）。
- `QSslSocket::SupportedFeature::ServerSideAlpn`：`2`;服务器端ALPN。
- `QSslSocket::SupportedFeature::Ocsp`：`3`;OCSP 订书（在线证书状态协议）。
- `QSslSocket::SupportedFeature::Psk`：`4`;预先共享密钥。
- `QSslSocket::SupportedFeature::SessionTicket`：`5`;会议票。
- `QSslSocket::SupportedFeature::Alerts`：`6`;关于发送和接收的警报消息的信息。
这个枚举是在Qt 6.1引入的。

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

`QSslSocket` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
