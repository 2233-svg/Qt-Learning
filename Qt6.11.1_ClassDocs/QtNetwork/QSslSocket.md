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

### 相关非成员函数

- `Constant Value Description`
- `QSslSocket::AlertLevel::Warning 0 Non-fatal alert message`
- `QSslSocket::AlertLevel::Fatal 1 Fatal alert message, the underlying backend will handle such an alert properly and close the connection.`
- `QSslSocket::AlertLevel::Unknown 2 An alert of unknown level of severity.`
- `QSslSocket::AlertType::CloseNotify 0 ,`
- `QSslSocket::AlertType::UnexpectedMessage 10`
- `QSslSocket::AlertType::BadRecordMac 20`
- `QSslSocket::AlertType::RecordOverflow 22`
- `QSslSocket::AlertType::DecompressionFailure 30`
- `QSslSocket::AlertType::HandshakeFailure 40`
- `QSslSocket::AlertType::NoCertificate 41`
- `QSslSocket::AlertType::BadCertificate 42`
- `QSslSocket::AlertType::UnsupportedCertificate 43`
- `QSslSocket::AlertType::CertificateRevoked 44`
- `QSslSocket::AlertType::CertificateExpired 45`
- `QSslSocket::AlertType::CertificateUnknown 46`
- `QSslSocket::AlertType::IllegalParameter 47`
- `QSslSocket::AlertType::UnknownCa 48`
- `QSslSocket::AlertType::AccessDenied 49`
- `QSslSocket::AlertType::DecodeError 50`
- `QSslSocket::AlertType::DecryptError 51`
- `QSslSocket::AlertType::ExportRestriction 60`
- `QSslSocket::AlertType::ProtocolVersion 70`
- `QSslSocket::AlertType::InsufficientSecurity 71`
- `QSslSocket::AlertType::InternalError 80`
- `QSslSocket::AlertType::InappropriateFallback 86`
- `QSslSocket::AlertType::UserCancelled 90`
- `QSslSocket::AlertType::NoRenegotiation 100`
- `QSslSocket::AlertType::MissingExtension 109`
- `QSslSocket::AlertType::UnsupportedExtension 110`
- `QSslSocket::AlertType::CertificateUnobtainable 111`
- `QSslSocket::AlertType::UnrecognizedName 112`
- `QSslSocket::AlertType::BadCertificateStatusResponse 113`
- `QSslSocket::AlertType::BadCertificateHashValue 114`
- `QSslSocket::AlertType::UnknownPskIdentity 115`
- `QSslSocket::AlertType::CertificateRequired 116`
- `QSslSocket::AlertType::NoApplicationProtocol 120`
- `QSslSocket::AlertType::UnknownAlertMessage 255`
- `QSslSocket::ImplementedClass::Key 0 Class QSslKey.`
- `QSslSocket::ImplementedClass::Certificate 1 Class QSslCertificate.`
- `QSslSocket::ImplementedClass::Socket 2 Class QSslSocket.`
- `QSslSocket::ImplementedClass::DiffieHellman 3 Class QSslDiffieHellmanParameters.`
- `QSslSocket::ImplementedClass::EllipticCurve 4 Class QSslEllipticCurve.`
- `QSslSocket::ImplementedClass::Dtls 5 Class QDtls.`
- `QSslSocket::ImplementedClass::DtlsCookie 6 Class QDtlsClientVerifier.`
- `QSslSocket::SupportedFeature::CertificateVerification 0 Indicates that QSslCertificate::verify() is implemented by the backend.`
- `QSslSocket::SupportedFeature::ClientSideAlpn 1 Client-side ALPN (Application Layer Protocol Negotiation).`
- `QSslSocket::SupportedFeature::ServerSideAlpn 2 Server-side ALPN.`
- `QSslSocket::SupportedFeature::Ocsp 3 OCSP stapling (Online Certificate Status Protocol).`
- `QSslSocket::SupportedFeature::Psk 4 Pre-shared keys.`
- `QSslSocket::SupportedFeature::SessionTicket 5 Session tickets.`
- `QSslSocket::SupportedFeature::Alerts 6 Information about alert messages sent and received.`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 139 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QSslSocket::PeerVerifyMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSslSocket` 暴露的类型声明 `Peer、Verify、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PeerVerifyMode`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QSslSocket::SslMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSslSocket` 暴露的类型声明 `Ssl、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SslMode`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QSslSocket::QSslSocket(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QSslSocket::~QSslSocket()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.1] QString QSslSocket::activeBackend()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `activeBackend`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSslSocket::alertReceived(QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 发出的通知信号 `alertReceived`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `level`：类型为 `QSsl::AlertLevel`。没有默认值，调用时必须提供。传入 `QSsl::AlertLevel` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `QSsl::AlertType`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `description`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSslSocket::alertSent(QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 发出的通知信号 `alertSent`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `level`：类型为 `QSsl::AlertLevel`。没有默认值，调用时必须提供。传入 `QSsl::AlertLevel` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `QSsl::AlertType`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `description`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSslSocket::atEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::atEnd` 用于计算、查询或取得与“按位置访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.1] QList<QString> QSslSocket::availableBackends()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `availableBackends`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QList<QString>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] qint64 QSslSocket::bytesAvailable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `bytesAvailable`，返回 `QSslSocket` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] qint64 QSslSocket::bytesToWrite() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `bytesToWrite`，返回 `QSslSocket` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSslSocket::canReadLine() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canReadLine`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QSslSocket::close()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `close`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QSslSocket::connectToHost(const QString &hostName, quint16 port, QIODeviceBase::OpenMode openMode = ReadWrite, QAbstractSocket::NetworkLayerProtocol protocol = AnyIPProtocol)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `connectToHost`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `hostName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `port`：类型为 `quint16`。没有默认值，调用时必须提供。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `openMode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。传入 `QIODeviceBase::OpenMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `protocol`：类型为 `QAbstractSocket::NetworkLayerProtocol`。默认值为 `AnyIPProtocol`。传入 `QAbstractSocket::NetworkLayerProtocol` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslSocket::connectToHostEncrypted(const QString &hostName, quint16 port, QIODeviceBase::OpenMode mode = ReadWrite, QAbstractSocket::NetworkLayerProtocol protocol = AnyIPProtocol)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `connectToHostEncrypted`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `hostName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `port`：类型为 `quint16`。没有默认值，调用时必须提供。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `protocol`：类型为 `QAbstractSocket::NetworkLayerProtocol`。默认值为 `AnyIPProtocol`。传入 `QAbstractSocket::NetworkLayerProtocol` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslSocket::connectToHostEncrypted(const QString &hostName, quint16 port, const QString &sslPeerName, QIODeviceBase::OpenMode mode = ReadWrite, QAbstractSocket::NetworkLayerProtocol protocol = AnyIPProtocol)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `connectToHostEncrypted`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `hostName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `port`：类型为 `quint16`。没有默认值，调用时必须提供。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sslPeerName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `mode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `protocol`：类型为 `QAbstractSocket::NetworkLayerProtocol`。默认值为 `AnyIPProtocol`。传入 `QAbstractSocket::NetworkLayerProtocol` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QSslSocket::continueInterruptedHandshake()`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::continueInterruptedHandshake` 用于执行与“continue、Interrupted、Handshake”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QSslSocket::disconnectFromHost()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `disconnectFromHost`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSslSocket::encrypted()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 发出的通知信号 `encrypted`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QSslSocket::encryptedBytesAvailable() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::encryptedBytesAvailable` 用于计算、查询或取得与“encrypted、字节、可用量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QSslSocket::encryptedBytesToWrite() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::encryptedBytesToWrite` 用于计算、查询或取得与“encrypted、字节、转换输出、写入”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSslSocket::encryptedBytesWritten(qint64 written)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 发出的通知信号 `encryptedBytesWritten`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `written`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSslSocket::handshakeInterruptedOnError(const QSslError &error)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 发出的通知信号 `handshakeInterruptedOnError`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `error`：类型为 `const QSslError &`。没有默认值，调用时必须提供。错误输出对象或错误状态。解析/执行后要检查它，而不能只看主返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QSslSocket::ignoreSslErrors()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `ignoreSslErrors`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslSocket::ignoreSslErrors(const QList<QSslError> &errors)`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::ignoreSslErrors` 用于执行与“ignore、Ssl、Errors”相关的操作。调用时要先确认当前状态和 `errors` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `errors`：类型为 `const QList<QSslError> &`。没有默认值，调用时必须提供。传入 `const QList<QSslError> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.1] QList<QSsl::ImplementedClass> QSslSocket::implementedClasses(const QString &backendName = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `implementedClasses`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QList<QSsl::ImplementedClass>`。
- 参数 `backendName`：类型为 `const QString &`。默认值为 `{}`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.1] bool QSslSocket::isClassImplemented(QSsl::ImplementedClass cl, const QString &backendName = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isClassImplemented`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `cl`：类型为 `QSsl::ImplementedClass`。没有默认值，调用时必须提供。传入 `QSsl::ImplementedClass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `backendName`：类型为 `const QString &`。默认值为 `{}`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSslSocket::isEncrypted() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEncrypted`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.1] bool QSslSocket::isFeatureSupported(QSsl::SupportedFeature ft, const QString &backendName = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isFeatureSupported`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `ft`：类型为 `QSsl::SupportedFeature`。没有默认值，调用时必须提供。传入 `QSsl::SupportedFeature` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `backendName`：类型为 `const QString &`。默认值为 `{}`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.1] bool QSslSocket::isProtocolSupported(QSsl::SslProtocol protocol, const QString &backendName = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isProtocolSupported`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `protocol`：类型为 `QSsl::SslProtocol`。没有默认值，调用时必须提供。传入 `QSsl::SslProtocol` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `backendName`：类型为 `const QString &`。默认值为 `{}`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslCertificate QSslSocket::localCertificate() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::localCertificate` 用于计算、查询或取得与“local、Certificate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslCertificate`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslCertificate`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QSslCertificate> QSslSocket::localCertificateChain() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::localCertificateChain` 用于计算、查询或取得与“local、Certificate、Chain”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QSslCertificate>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QSslCertificate>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::SslMode QSslSocket::mode() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::mode` 用于计算、查询或取得与“模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslSocket::SslMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslSocket::SslMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSslSocket::modeChanged(QSslSocket::SslMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 发出的通知信号 `modeChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QSslSocket::SslMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSslSocket::newSessionTicketReceived()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 发出的通知信号 `newSessionTicketReceived`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QOcspResponse> QSslSocket::ocspResponses() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::ocspResponses` 用于计算、查询或取得与“ocsp、Responses”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QOcspResponse>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QOcspResponse>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslCertificate QSslSocket::peerCertificate() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::peerCertificate` 用于计算、查询或取得与“peer、Certificate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslCertificate`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslCertificate`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QSslCertificate> QSslSocket::peerCertificateChain() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::peerCertificateChain` 用于计算、查询或取得与“peer、Certificate、Chain”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QSslCertificate>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QSslCertificate>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSslSocket::peerVerifyDepth() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::peerVerifyDepth` 用于计算、查询或取得与“peer、Verify、Depth”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSslSocket::peerVerifyError(const QSslError &error)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 发出的通知信号 `peerVerifyError`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `error`：类型为 `const QSslError &`。没有默认值，调用时必须提供。错误输出对象或错误状态。解析/执行后要检查它，而不能只看主返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::PeerVerifyMode QSslSocket::peerVerifyMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::peerVerifyMode` 用于计算、查询或取得与“peer、Verify、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslSocket::PeerVerifyMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslSocket::PeerVerifyMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSslSocket::peerVerifyName() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::peerVerifyName` 用于计算、查询或取得与“peer、Verify、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSslSocket::preSharedKeyAuthenticationRequired(QSslPreSharedKeyAuthenticator *authenticator)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 发出的通知信号 `preSharedKeyAuthenticationRequired`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `authenticator`：类型为 `QSslPreSharedKeyAuthenticator *`。没有默认值，调用时必须提供。传入 `QSslPreSharedKeyAuthenticator *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslKey QSslSocket::privateKey() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::privateKey` 用于计算、查询或取得与“private、Key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslKey`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslKey`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSsl::SslProtocol QSslSocket::protocol() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::protocol` 用于计算、查询或取得与“protocol”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSsl::SslProtocol`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSsl::SslProtocol`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] qint64 QSslSocket::readData(char *data, qint64 maxlen)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 的核心操作 `readData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `maxlen`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QSslSocket::resume()`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::resume` 用于执行与“恢复运行”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslCipher QSslSocket::sessionCipher() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::sessionCipher` 用于计算、查询或取得与“session、Cipher”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslCipher`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslCipher`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSsl::SslProtocol QSslSocket::sessionProtocol() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::sessionProtocol` 用于计算、查询或取得与“session、Protocol”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSsl::SslProtocol`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSsl::SslProtocol`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.1] bool QSslSocket::setActiveBackend(const QString &backendName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setActiveBackend`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `backendName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslSocket::setLocalCertificate(const QSslCertificate &certificate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLocalCertificate`。调用它会改变 `QSslSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `certificate`：类型为 `const QSslCertificate &`。没有默认值，调用时必须提供。传入 `const QSslCertificate &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslSocket::setLocalCertificate(const QString &path, QSsl::EncodingFormat format = QSsl::Pem)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLocalCertificate`。调用它会改变 `QSslSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `format`：类型为 `QSsl::EncodingFormat`。默认值为 `QSsl::Pem`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslSocket::setLocalCertificateChain(const QList<QSslCertificate> &localChain)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLocalCertificateChain`。调用它会改变 `QSslSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `localChain`：类型为 `const QList<QSslCertificate> &`。没有默认值，调用时必须提供。传入 `const QList<QSslCertificate> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslSocket::setPeerVerifyDepth(int depth)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPeerVerifyDepth`。调用它会改变 `QSslSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `depth`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslSocket::setPeerVerifyMode(QSslSocket::PeerVerifyMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPeerVerifyMode`。调用它会改变 `QSslSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QSslSocket::PeerVerifyMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslSocket::setPeerVerifyName(const QString &hostName)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPeerVerifyName`。调用它会改变 `QSslSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `hostName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslSocket::setPrivateKey(const QSslKey &key)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPrivateKey`。调用它会改变 `QSslSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QSslKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslSocket::setPrivateKey(const QString &fileName, QSsl::KeyAlgorithm algorithm = QSsl::Rsa, QSsl::EncodingFormat format = QSsl::Pem, const QByteArray &passPhrase = QByteArray())`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPrivateKey`。调用它会改变 `QSslSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `algorithm`：类型为 `QSsl::KeyAlgorithm`。默认值为 `QSsl::Rsa`。传入 `QSsl::KeyAlgorithm` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `QSsl::EncodingFormat`。默认值为 `QSsl::Pem`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `passPhrase`：类型为 `const QByteArray &`。默认值为 `QByteArray()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslSocket::setProtocol(QSsl::SslProtocol protocol)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setProtocol`。调用它会改变 `QSslSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `protocol`：类型为 `QSsl::SslProtocol`。没有默认值，调用时必须提供。传入 `QSsl::SslProtocol` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QSslSocket::setReadBufferSize(qint64 size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setReadBufferSize`。调用它会改变 `QSslSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qint64`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSslSocket::setSocketDescriptor(qintptr socketDescriptor, QAbstractSocket::SocketState state = ConnectedState, QIODeviceBase::OpenMode openMode = ReadWrite)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSocketDescriptor`。调用它会改变 `QSslSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `socketDescriptor`：类型为 `qintptr`。没有默认值，调用时必须提供。传入 `qintptr` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `state`：类型为 `QAbstractSocket::SocketState`。默认值为 `ConnectedState`。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。
- 参数 `openMode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。传入 `QIODeviceBase::OpenMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QSslSocket::setSocketOption(QAbstractSocket::SocketOption option, const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSocketOption`。调用它会改变 `QSslSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `option`：类型为 `QAbstractSocket::SocketOption`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslSocket::setSslConfiguration(const QSslConfiguration &configuration)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSslConfiguration`。调用它会改变 `QSslSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `configuration`：类型为 `const QSslConfiguration &`。没有默认值，调用时必须提供。传入 `const QSslConfiguration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] qint64 QSslSocket::skipData(qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::skipData` 用于计算、查询或取得与“skip、数据访问”相关的操作。调用时要先确认当前状态和 `maxSize` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QVariant QSslSocket::socketOption(QAbstractSocket::SocketOption option)`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::socketOption` 用于计算、查询或取得与“socket、Option”相关的操作。调用时要先确认当前状态和 `option` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `option`：类型为 `QAbstractSocket::SocketOption`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslConfiguration QSslSocket::sslConfiguration() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::sslConfiguration` 用于计算、查询或取得与“ssl、Configuration”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslConfiguration`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslConfiguration`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSslSocket::sslErrors(const QList<QSslError> &errors)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 发出的通知信号 `sslErrors`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `errors`：类型为 `const QList<QSslError> &`。没有默认值，调用时必须提供。传入 `const QList<QSslError> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QSslError> QSslSocket::sslHandshakeErrors() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::sslHandshakeErrors` 用于计算、查询或取得与“ssl、Handshake、Errors”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QSslError>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QSslError>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] long QSslSocket::sslLibraryBuildVersionNumber()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sslLibraryBuildVersionNumber`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`long`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QSslSocket::sslLibraryBuildVersionString()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sslLibraryBuildVersionString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] long QSslSocket::sslLibraryVersionNumber()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sslLibraryVersionNumber`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`long`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QSslSocket::sslLibraryVersionString()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sslLibraryVersionString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QSslSocket::startClientEncryption()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `startClientEncryption`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QSslSocket::startServerEncryption()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `startServerEncryption`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.1] QList<QSsl::SupportedFeature> QSslSocket::supportedFeatures(const QString &backendName = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `supportedFeatures`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QList<QSsl::SupportedFeature>`。
- 参数 `backendName`：类型为 `const QString &`。默认值为 `{}`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.1] QList<QSsl::SslProtocol> QSslSocket::supportedProtocols(const QString &backendName = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `supportedProtocols`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QList<QSsl::SslProtocol>`。
- 参数 `backendName`：类型为 `const QString &`。默认值为 `{}`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QSslSocket::supportsSsl()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `supportsSsl`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSslSocket::waitForBytesWritten(int msecs = 30000)`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::waitForBytesWritten` 用于计算、查询或取得与“等待、For、字节、Written”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。默认值为 `30000`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSslSocket::waitForConnected(int msecs = 30000)`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::waitForConnected` 用于计算、查询或取得与“等待、For、Connected”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。默认值为 `30000`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSslSocket::waitForDisconnected(int msecs = 30000)`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::waitForDisconnected` 用于计算、查询或取得与“等待、For、Disconnected”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。默认值为 `30000`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSslSocket::waitForEncrypted(int msecs = 30000)`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::waitForEncrypted` 用于计算、查询或取得与“等待、For、Encrypted”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。默认值为 `30000`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSslSocket::waitForReadyRead(int msecs = 30000)`

**API 类别：** 成员函数说明

**中文解读：** `QSslSocket::waitForReadyRead` 用于计算、查询或取得与“等待、For、Ready、读取”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。默认值为 `30000`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] qint64 QSslSocket::writeData(const char *data, qint64 len)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslSocket` 的核心操作 `writeData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `const char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `len`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] enum class AlertLevel`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] enum class AlertType`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] enum class ImplementedClass`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] enum class SupportedFeature`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Constant Value Description`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的 `Constant` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertLevel::Warning 0 Non-fatal alert message`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertLevel::Warning 0 Non-fatal alert message`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertLevel::Fatal 1 Fatal alert message, the underlying backend will handle such an alert properly and close the connection.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertLevel::Fatal 1 Fatal alert message, the underlying backend will handle such an alert properly and close the connection.`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertLevel::Unknown 2 An alert of unknown level of severity.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertLevel::Unknown 2 An alert of unknown level of severity.`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::CloseNotify 0 ,`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::CloseNotify 0 ,`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::UnexpectedMessage 10`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::UnexpectedMessage 10`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::BadRecordMac 20`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::BadRecordMac 20`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::RecordOverflow 22`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::RecordOverflow 22`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::DecompressionFailure 30`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::DecompressionFailure 30`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::HandshakeFailure 40`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::HandshakeFailure 40`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::NoCertificate 41`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::NoCertificate 41`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::BadCertificate 42`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::BadCertificate 42`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::UnsupportedCertificate 43`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::UnsupportedCertificate 43`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::CertificateRevoked 44`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::CertificateRevoked 44`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::CertificateExpired 45`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::CertificateExpired 45`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::CertificateUnknown 46`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::CertificateUnknown 46`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::IllegalParameter 47`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::IllegalParameter 47`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::UnknownCa 48`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::UnknownCa 48`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::AccessDenied 49`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::AccessDenied 49`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::DecodeError 50`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::DecodeError 50`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::DecryptError 51`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::DecryptError 51`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::ExportRestriction 60`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::ExportRestriction 60`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::ProtocolVersion 70`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::ProtocolVersion 70`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::InsufficientSecurity 71`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::InsufficientSecurity 71`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::InternalError 80`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::InternalError 80`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::InappropriateFallback 86`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::InappropriateFallback 86`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::UserCancelled 90`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::UserCancelled 90`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::NoRenegotiation 100`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::NoRenegotiation 100`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::MissingExtension 109`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::MissingExtension 109`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::UnsupportedExtension 110`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::UnsupportedExtension 110`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::CertificateUnobtainable 111`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::CertificateUnobtainable 111`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::UnrecognizedName 112`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::UnrecognizedName 112`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::BadCertificateStatusResponse 113`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::BadCertificateStatusResponse 113`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::BadCertificateHashValue 114`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::BadCertificateHashValue 114`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::UnknownPskIdentity 115`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::UnknownPskIdentity 115`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::CertificateRequired 116`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::CertificateRequired 116`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::NoApplicationProtocol 120`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::NoApplicationProtocol 120`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::AlertType::UnknownAlertMessage 255`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:AlertType::UnknownAlertMessage 255`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::ImplementedClass::Key 0 Class QSslKey.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:ImplementedClass::Key 0 Class QSslKey.`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::ImplementedClass::Certificate 1 Class QSslCertificate.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:ImplementedClass::Certificate 1 Class QSslCertificate.`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::ImplementedClass::Socket 2 Class QSslSocket.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:ImplementedClass::Socket 2 Class QSslSocket.`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::ImplementedClass::DiffieHellman 3 Class QSslDiffieHellmanParameters.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:ImplementedClass::DiffieHellman 3 Class QSslDiffieHellmanParameters.`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::ImplementedClass::EllipticCurve 4 Class QSslEllipticCurve.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:ImplementedClass::EllipticCurve 4 Class QSslEllipticCurve.`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::ImplementedClass::Dtls 5 Class QDtls.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:ImplementedClass::Dtls 5 Class QDtls.`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::ImplementedClass::DtlsCookie 6 Class QDtlsClientVerifier.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:ImplementedClass::DtlsCookie 6 Class QDtlsClientVerifier.`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::SupportedFeature::CertificateVerification 0 Indicates that QSslCertificate::verify() is implemented by the backend.`

**API 类别：** 相关非成员函数

**中文解读：** `QSslSocket::verify` 用于计算、查询或取得与“verify”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslSocket::SupportedFeature::CertificateVerification 0 Indicates that`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslSocket::SupportedFeature::CertificateVerification 0 Indicates that`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::SupportedFeature::ClientSideAlpn 1 Client-side ALPN (Application Layer Protocol Negotiation).`

**API 类别：** 相关非成员函数

**中文解读：** `QSslSocket::ALPN` 用于计算、查询或取得与“ALPN”相关的操作。调用时要先确认当前状态和 `Negotiation` 的有效范围；返回类型是 `QSslSocket::SupportedFeature::ClientSideAlpn 1 Client-side`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslSocket::SupportedFeature::ClientSideAlpn 1 Client-side`。
- 参数 `Negotiation`：类型为 `Application Layer Protocol`。没有默认值，调用时必须提供。传入 `Application Layer Protocol` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::SupportedFeature::ServerSideAlpn 2 Server-side ALPN.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:SupportedFeature::ServerSideAlpn 2 Server-side ALPN.`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::SupportedFeature::Ocsp 3 OCSP stapling (Online Certificate Status Protocol).`

**API 类别：** 相关非成员函数

**中文解读：** `QSslSocket::stapling` 用于计算、查询或取得与“stapling”相关的操作。调用时要先确认当前状态和 `Protocol` 的有效范围；返回类型是 `QSslSocket::SupportedFeature::Ocsp 3 OCSP`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslSocket::SupportedFeature::Ocsp 3 OCSP`。
- 参数 `Protocol`：类型为 `Online Certificate Status`。没有默认值，调用时必须提供。传入 `Online Certificate Status` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::SupportedFeature::Psk 4 Pre-shared keys.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:SupportedFeature::Psk 4 Pre-shared keys.`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::SupportedFeature::SessionTicket 5 Session tickets.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:SupportedFeature::SessionTicket 5 Session tickets.`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::SupportedFeature::Alerts 6 Information about alert messages sent and received.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QSslSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:SupportedFeature::Alerts 6 Information about alert messages sent and received.`。
- 属性名：`QSslSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
