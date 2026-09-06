# QDtls

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QDtls` 是 Qt Network 的“Dtls”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QDtls` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QDtls>`
- 继承自：QObject
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

创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `GeneratorParameters`
- `enum HandshakeState { HandshakeNotStarted, HandshakeInProgress, PeerVerificationFailed, HandshakeComplete }`

### 公有函数

- `QDtls(QSslSocket::SslMode mode, QObject *parent = nullptr)`
- `virtual ~QDtls()`
- `bool abortHandshake(QUdpSocket *socket)`
- `QDtls::GeneratorParameters cookieGeneratorParameters() const`
- `QByteArray decryptDatagram(QUdpSocket *socket, const QByteArray &dgram)`
- `bool doHandshake(QUdpSocket *socket, const QByteArray &dgram = {})`
- `QSslConfiguration dtlsConfiguration() const`
- `QDtlsError dtlsError() const`
- `QString dtlsErrorString() const`
- `bool handleTimeout(QUdpSocket *socket)`
- `QDtls::HandshakeState handshakeState() const`
- `void ignoreVerificationErrors(const QList<QSslError> &errorsToIgnore)`
- `bool isConnectionEncrypted() const`
- `quint16 mtuHint() const`
- `QHostAddress peerAddress() const`
- `quint16 peerPort() const`
- `QList<QSslError> peerVerificationErrors() const`
- `QString peerVerificationName() const`
- `bool resumeHandshake(QUdpSocket *socket)`
- `QSslCipher sessionCipher() const`
- `QSsl::SslProtocol sessionProtocol() const`
- `bool setCookieGeneratorParameters(const QDtls::GeneratorParameters &params)`
- `bool setDtlsConfiguration(const QSslConfiguration &configuration)`
- `void setMtuHint(quint16 mtuHint)`
- `bool setPeer(const QHostAddress &address, quint16 port, const QString &verificationName = {})`
- `bool setPeerVerificationName(const QString &name)`
- `bool shutdown(QUdpSocket *socket)`
- `QSslSocket::SslMode sslMode() const`
- `qint64 writeDatagramEncrypted(QUdpSocket *socket, const QByteArray &dgram)`

### 信号

- `void handshakeTimeout()`
- `void pskRequired(QSslPreSharedKeyAuthenticator *authenticator)`

### 相关非成员函数

- `enum class QDtlsError { NoError, InvalidInputParameters, InvalidOperation, UnderlyingSocketError, RemoteClosedConnectionError, …, TlsNonFatalError }`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDtls::HandshakeState`

**作用与语义：**

描述了当前DTLS握手的状态。
本枚举描述了`QDtls`连接DTLS握手的当前状态。
- `QDtls::HandshakeNotStarted`：`0`;还没做成。
- `QDtls::HandshakeInProgress`：`1`;已启动握手，目前未发现错误。
- `QDtls::PeerVerificationFailed`：`2`;无法确定对等者的身份。
- `QDtls::HandshakeComplete`：`3`;握手成功完成，加密连接建立。

### `[explicit] QDtls::QDtls(QSslSocket::SslMode mode, QObject *parent = nullptr)`

**作用与语义：**

创建QDtls对象，`parent`传递给`QObject`构造函数。`mode` `QSslSocket::SslServerMode`用于服务器端的DTLS连接，或`QSslSocket::SslClientMode`客户端。

### `[virtual noexcept] QDtls::~QDtls()`

**作用与语义：**

摧毁`QDtls`物体。

### `bool QDtls::abortHandshake(QUdpSocket *socket)`

**作用与语义：**

中止正在进行的握手。如果有握手正在进行`socket`，则返回true;否则，设置合适的错误并返回false。

### `QDtls::GeneratorParameters QDtls::cookieGeneratorParameters() const`

**作用与语义：**

返回当前的哈希算法和秘密，要么是默认的，要么是之前通过调用`setCookieGeneratorParameters()`设置的。
如果 Qt 配置支持默认哈希算法，则`QCryptographicHash::Sha256`，否则`QCryptographicHash::Sha1`。默认秘密来自后端专用的强密码学伪随机数生成器。

### `QByteArray QDtls::decryptDatagram(QUdpSocket *socket, const QByteArray &dgram)`

**作用与语义：**

解密`dgram`并返回其内容为明文。必须完成握手后，数据报才能解密。根据TLS消息的类型，连接可能会写入`socket`，而必须是有效的指针。

### `bool QDtls::doHandshake(QUdpSocket *socket, const QByteArray &dgram = {})`

**作用与语义：**

启动或继续 DTLS 握手。`socket` 必须是有效的指针。启动服务器端 DTLS 握手时，`dgram` 必须包含从 `QUdpSocket` 读取的初始 ClientHello 消息。如果未发现错误，该函数返回`true`。握手状态可以用 `handshakeState()` 测试。返回`false`表示发生了错误，请使用`dtlsError()`获取更详细的信息。
注意：如果无法确认对等端的身份，错误设置为`QDtlsError::PeerVerificationError`。如果你想忽略验证错误并继续连接，必须先调用`ignoreVerificationErrors()`然后`resumeHandshake()`。如果无法忽略错误，则必须调用`abortHandshake()`。

**官方示例：**

```cpp
 if (!dtls.doHandshake(&socket, dgram)) {
     if (dtls.dtlsError() == QDtlsError::PeerVerificationError)
         dtls.abortAfterError(&socket);
 }
```

### `QSslConfiguration QDtls::dtlsConfiguration() const`

**作用与语义：**

返回默认的DTLS配置或之前调用`setDtlsConfiguration()`时设置的配置。

### `QDtlsError QDtls::dtlsError() const`

**作用与语义：**

返回连接或`QDtlsError::NoError`遇到的最后一次错误。

### `QString QDtls::dtlsErrorString() const`

**作用与语义：**

返回连接或空字符串遇到的最后错误的文本描述。

### `bool QDtls::handleTimeout(QUdpSocket *socket)`

**作用与语义：**

如果握手过程中发生超时，`handshakeTimeout()`信号会被发出。应用程序必须调用handleTimeout()来重传握手消息;handleTimeout() 返回超时时`true`，否则返回false。`socket`必须是有效的指针。

### `QDtls::HandshakeState QDtls::handshakeState() const`

**作用与语义：**

返回当前握手状态，`QDtls`。

### `[signal] void QDtls::handshakeTimeout()`

**作用与语义：**

丢包可能导致握手阶段超时。此时`QDtls`发出握手Timeout()信号。调用`handleTimeout()`以重传握手消息：

**官方示例：**

```cpp
 DtlsClient::DtlsClient()
 {
     // Some initialization code here ...
     connect(&clientDtls, &QDtls::handshakeTimeout, this, &DtlsClient::handleTimeout);
 }

 void DtlsClient::handleTimeout()
 {
     clientDtls.handleTimeout(&clientSocket);
 }
```

### `void QDtls::ignoreVerificationErrors(const QList<QSslError> &errorsToIgnore)`

**作用与语义：**

该方法只`QDtls`忽略`errorsToIgnore`中给出的错误。
例如，如果你想连接到使用自签名证书的服务器，请考虑以下片段：
你也可以在遇到`QDtlsError::PeerVerificationError`错误后调用该函数`doHandshake()`，然后通过调用`resumeHandshake()`恢复握手。
后续调用该函数会替换之前调用中传递的错误列表。你可以通过调用该函数时用空列表清除你想忽略的错误列表。

**官方示例：**

```cpp
 QList<QSslCertificate> cert = QSslCertificate::fromPath("server-certificate.pem"_L1);
 QSslError error(QSslError::SelfSignedCertificate, cert.at(0));
 QList<QSslError> expectedSslErrors;
 expectedSslErrors.append(error);

 QDtls dtls;
 dtls.ignoreVerificationErrors(expectedSslErrors);
 dtls.doHandshake(udpSocket);
```

### `bool QDtls::isConnectionEncrypted() const`

**作用与语义：**

如果 DTLS 握手成功完成，则返回 `true`。

### `quint16 QDtls::mtuHint() const`

**作用与语义：**

返回之前由`setMtuHint()`设定的值。默认值为0。

### `QHostAddress QDtls::peerAddress() const`

**作用与语义：**

返回由`setPeer()`或`QHostAddress::Null`设置的对等端地址。

### `quint16 QDtls::peerPort() const`

**作用与语义：**

返回对等端的端口号，设置为`setPeer()`，即0。

### `QList<QSslError> QDtls::peerVerificationErrors() const`

**作用与语义：**

返回在确定对等端身份时发现的错误。
如果你想在发生错误的情况下继续连接，必须致电`ignoreVerificationErrors()`。

### `QString QDtls::peerVerificationName() const`

**作用与语义：**

返回由`setPeer()`或`setPeerVerificationName()`设置的主机名。默认值为空字符串。

### `[signal] void QDtls::pskRequired(QSslPreSharedKeyAuthenticator *authenticator)`

**作用与语义：**

`QDtls`在协商PSK密码套件时会发出该信号，因此需要PSK认证。
使用PSK时，客户端必须向服务器发送有效的身份和有效的预共享密钥，以便TLS握手继续。应用程序可以通过根据需求填写传递的`authenticator`对象，在连接到该信号的槽中提供这些信息。
注意：忽视该信号或未提供所需凭证，将导致握手失败，连接将被终止。
注意：`authenticator`对象归`QDtls`所有，应用程序不得删除。

### `bool QDtls::resumeHandshake(QUdpSocket *socket)`

**作用与语义：**

如果握手过程中忽略了对等验证错误，resumeHandshake() 会恢复并完成握手并返回`true`。`socket` 必须是有效的指针。如果握手无法恢复，返回`false`。

### `QSslCipher QDtls::sessionCipher() const`

**作用与语义：**

返回该连接所使用的密码学`cipher`，若连接未加密则返回空密码。会话密码在握手阶段选择。密码用于加密和解密数据。
`QSslConfiguration` 提供了设置有序密码列表的函数，握手阶段最终将从中选择会话密码。该有序列表必须在握手阶段开始前就已存在。

### `QSsl::SslProtocol QDtls::sessionProtocol() const`

**作用与语义：**

返回该连接使用的DTLS协议版本，或如果连接尚未加密，则返回UnknownProtocol。连接的协议在握手阶段选择。
`setDtlsConfiguration()`可以在握手开始前设置首选版本。

### `bool QDtls::setCookieGeneratorParameters(const QDtls::GeneratorParameters &params)`

**作用与语义：**

设置密码学哈希算法和`params`的秘密。该函数仅用于服务器端`QDtls`连接。成功时返回`true`。
注意：该函数必须在握手开始前调用。

### `bool QDtls::setDtlsConfiguration(const QSslConfiguration &configuration)`

**作用与语义：**

从`configuration`设置连接的TLS配置，成功时返回`true`。
注意：该函数必须在握手开始前调用。

### `void QDtls::setMtuHint(quint16 mtuHint)`

**作用与语义：**

`mtuHint` 是最大传输单元（MTU），由应用程序发现或猜测。应用程序无需设置此值。

### `bool QDtls::setPeer(const QHostAddress &address, quint16 port, const QString &verificationName = {})`

**作用与语义：**

设置对等端的地址、`port`和主机名，成功时返回`true`。`address`不得为空、多播或广播。`verificationName`是用于证书验证的主机名。

### `bool QDtls::setPeerVerificationName(const QString &name)`

**作用与语义：**

设置用于证书验证的主机`name`，成功时返回`true`。
注意：该函数必须在握手开始前调用。

### `bool QDtls::shutdown(QUdpSocket *socket)`

**作用与语义：**

发送加密的关机警报消息并关闭DTLS连接。握手状态变为`QDtls::HandshakeNotStarted`。`socket`必须是有效的指针。该函数成功时返回`true`。

### `QSslSocket::SslMode QDtls::sslMode() const`

**作用与语义：**

服务器端连接返回`QSslSocket::SslServerMode`，客户端返回`QSslSocket::SslClientMode`。

### `qint64 QDtls::writeDatagramEncrypted(QUdpSocket *socket, const QByteArray &dgram)`

**作用与语义：**

加密`dgram`并将加密数据写入`socket`。返回写入字节数，错误时返回-1字节数。必须完成握手后才能写入加密数据。`socket`必须是有效的指针。

### `enum class QDtlsError`

**作用与语义：**

描述了可以通过 `QDtls` 和 `QDtlsClientVerifier` 发现的错误。
该枚举描述了`QDtlsClientVerifier`类和`QDtls`类对象可能遇到的一般性和TLS特有错误。
- `QDtls::QDtlsError::NoError`：`0`;未发生错误，最后一次操作成功。
- `QDtls::QDtlsError::InvalidInputParameters`：`1`;调用者提供的输入参数无效。
- `QDtls::QDtlsError::InvalidOperation`：`2`;在不允许的状态下尝试了一次手术。
- `QDtls::QDtlsError::UnderlyingSocketError`：`3`;`QUdpSocket::writeDatagram()`未通过，`QUdpSocket::error()`和`QUdpSocket::errorString()`可以提供更具体的信息。
- `QDtls::QDtlsError::RemoteClosedConnectionError`：`4`;收到TLS关闭警报信息。
- `QDtls::QDtlsError::PeerVerificationError`：`5`;在TLS握手过程中无法验证对等端的身份。
- `QDtls::QDtlsError::TlsInitializationError`：`6`;初始化底层TLS后端时发生错误。
- `QDtls::QDtlsError::TlsFatalError`：`7`;在TLS握手过程中发生了致命错误，除了对等验证错误或TLS初始化错误外。
- `QDtls::QDtlsError::TlsNonFatalError`：`8`;数据报未能加密或解密，非致命，意味着`QDtls`在此错误后仍可继续工作。

### `GeneratorParameters`

**作用与语义：**

这是 `QDtlsClientVerifier::GeneratorParameters` 的别名，保存 DTLS Cookie 生成所用的哈希算法和密钥。它只用于服务器端，并应在握手开始前传给 `setCookieGeneratorParameters()`；密钥应由密码学安全随机源生成并定期轮换。

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

`QDtls` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
