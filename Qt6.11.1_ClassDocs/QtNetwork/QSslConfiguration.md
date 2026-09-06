# QSslConfiguration

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QSslConfiguration` 是 Qt Network 的“SslConfiguration”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QSslConfiguration` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QSslConfiguration>`
- 继承自：未在类页中列出
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
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum NextProtocolNegotiationStatus { NextProtocolNegotiationNone, NextProtocolNegotiationNegotiated, NextProtocolNegotiationUnsupported }`

### 公有函数

- `QSslConfiguration()`
- `QSslConfiguration(const QSslConfiguration &other)`
- `~QSslConfiguration()`
- `void addCaCertificate(const QSslCertificate &certificate)`
- `void addCaCertificates(const QList<QSslCertificate> &certificates)`
- `bool addCaCertificates(const QString &path, QSsl::EncodingFormat format = QSsl::Pem, QSslCertificate::PatternSyntax syntax = QSslCertificate::PatternSyntax::FixedString)`
- `QList<QByteArray> allowedNextProtocols() const`
- `QMap<QByteArray, QVariant> backendConfiguration() const`
- `QList<QSslCertificate> caCertificates() const`
- `QList<QSslCipher> ciphers() const`
- `QSslDiffieHellmanParameters diffieHellmanParameters() const`
- `bool dtlsCookieVerificationEnabled() const`
- `QList<QSslEllipticCurve> ellipticCurves() const`
- `QSslKey ephemeralServerKey() const`
- `(since 6.0) bool handshakeMustInterruptOnError() const`
- `bool isNull() const`
- `QSslCertificate localCertificate() const`
- `QList<QSslCertificate> localCertificateChain() const`
- `(since 6.0) bool missingCertificateIsFatal() const`
- `QByteArray nextNegotiatedProtocol() const`
- `QSslConfiguration::NextProtocolNegotiationStatus nextProtocolNegotiationStatus() const`
- `bool ocspStaplingEnabled() const`
- `QSslCertificate peerCertificate() const`
- `QList<QSslCertificate> peerCertificateChain() const`
- `int peerVerifyDepth() const`
- `QSslSocket::PeerVerifyMode peerVerifyMode() const`
- `QByteArray preSharedKeyIdentityHint() const`
- `QSslKey privateKey() const`
- `QSsl::SslProtocol protocol() const`
- `QSslCipher sessionCipher() const`
- `QSsl::SslProtocol sessionProtocol() const`
- `QByteArray sessionTicket() const`
- `int sessionTicketLifeTimeHint() const`
- `void setAllowedNextProtocols(const QList<QByteArray> &protocols)`
- `void setBackendConfiguration(const QMap<QByteArray, QVariant> &backendConfiguration = QMap<QByteArray, QVariant>())`
- `void setBackendConfigurationOption(const QByteArray &name, const QVariant &value)`
- `void setCaCertificates(const QList<QSslCertificate> &certificates)`
- `void setCiphers(const QList<QSslCipher> &ciphers)`
- `(since 6.0) void setCiphers(const QString &ciphers)`
- `void setDiffieHellmanParameters(const QSslDiffieHellmanParameters &dhparams)`
- `void setDtlsCookieVerificationEnabled(bool enable)`
- `void setEllipticCurves(const QList<QSslEllipticCurve> &curves)`
- `(since 6.0) void setHandshakeMustInterruptOnError(bool interrupt)`
- `void setLocalCertificate(const QSslCertificate &certificate)`
- `void setLocalCertificateChain(const QList<QSslCertificate> &localChain)`
- `(since 6.0) void setMissingCertificateIsFatal(bool cannotRecover)`
- `void setOcspStaplingEnabled(bool enabled)`
- `void setPeerVerifyDepth(int depth)`
- `void setPeerVerifyMode(QSslSocket::PeerVerifyMode mode)`
- `void setPreSharedKeyIdentityHint(const QByteArray &hint)`
- `void setPrivateKey(const QSslKey &key)`
- `void setProtocol(QSsl::SslProtocol protocol)`
- `void setSessionTicket(const QByteArray &sessionTicket)`
- `void setSslOption(QSsl::SslOption option, bool on)`
- `void swap(QSslConfiguration &other)`
- `bool testSslOption(QSsl::SslOption option) const`
- `bool operator!=(const QSslConfiguration &other) const`
- `QSslConfiguration & operator=(const QSslConfiguration &other)`
- `bool operator==(const QSslConfiguration &other) const`

### 静态公有成员

- `QSslConfiguration defaultConfiguration()`
- `QSslConfiguration defaultDtlsConfiguration()`
- `void setDefaultConfiguration(const QSslConfiguration &configuration)`
- `void setDefaultDtlsConfiguration(const QSslConfiguration &configuration)`
- `QList<QSslCipher> supportedCiphers()`
- `QList<QSslEllipticCurve> supportedEllipticCurves()`
- `QList<QSslCertificate> systemCaCertificates()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSslConfiguration::NextProtocolNegotiationStatus`

**作用与语义：**

描述下一协议协商（NPN）或应用层协议协商（ALPN）的状态。
- `QSslConfiguration::NextProtocolNegotiationNone`：`0`;尚未协商出应用协议。
- `QSslConfiguration::NextProtocolNegotiationNegotiated`：`1`;已协商出下一协议（见 `nextNegotiatedProtocol()`）。
- `QSslConfiguration::NextProtocolNegotiationUnsupported`：`2`;客户端和服务器无法就共同的下一个应用协议达成一致。

### `QSslConfiguration::QSslConfiguration()`

**作用与语义：**

构造一个空的SSL配置。该配置不包含有效的设置，状态为空。调用该构造器后，`isNull()`返回为真。
一旦调用任何 setter 方法，`isNull()` 将返回 false。

### `QSslConfiguration::QSslConfiguration(const QSslConfiguration &other)`

**作用与语义：**

复制`other`的配置和状态。如果`other`空，这个对象也是空。

### `[noexcept] QSslConfiguration::~QSslConfiguration()`

**作用与语义：**

释放`QSslConfiguration`持有的任何资源。

### `void QSslConfiguration::addCaCertificate(const QSslCertificate &certificate)`

**作用与语义：**

为该配置的CA证书数据库添加`certificate`。证书数据库必须在SSL握手前设置。CA证书数据库由套接字在握手阶段用于验证对等方证书。
注意：默认配置使用系统CA证书数据库。如果没有该数据库（iOS上常见情况），默认数据库为空。

### `void QSslConfiguration::addCaCertificates(const QList<QSslCertificate> &certificates)`

**作用与语义：**

为该配置的CA证书数据库增加`certificates`。证书数据库必须在SSL握手前设置。套接字在握手阶段使用CA证书数据库来验证对等方证书。
注意：默认配置使用系统CA证书数据库。如果没有该数据库（iOS上常见情况），默认数据库为空。

### `bool QSslConfiguration::addCaCertificates(const QString &path, QSsl::EncodingFormat format = QSsl::Pem, QSslCertificate::PatternSyntax syntax = QSslCertificate::PatternSyntax::FixedString)`

**作用与语义：**

搜索`path`中所有文件，查找指定`format`编码的证书，并将其添加到该套接字的CA证书数据库中。`path`必须是与一个或多个文件匹配的文件或模式，符合`syntax`的规定。如果将一个或多个证书添加到套接字的CA证书数据库，返回该文件`true`;否则返回`false`。
CA证书数据库在握手阶段被套接字用于验证对等方证书。
为了更精准的控制，使用`addCaCertificate()`。

### `QList<QByteArray> QSslConfiguration::allowedNextProtocols() const`

**作用与语义：**

该功能返回允许通过下一协议协商（NPN）或应用层协议协商（ALPN）TLS扩展与服务器协商的协议，这些扩展由`setAllowedNextProtocols()`设定。

### `QMap<QByteArray, QVariant> QSslConfiguration::backendConfiguration() const`

**作用与语义：**

返回后端专用配置。
只有`setBackendConfigurationOption()`或`setBackendConfiguration()`设置的选项会被返回。后端的内部标准配置不会被报告。

### `QList<QSslCertificate> QSslConfiguration::caCertificates() const`

**作用与语义：**

返回该连接的CA证书数据库。CA证书数据库在握手阶段被套接字用于验证对等方证书。握手前可以用`setCaCertificates()`或`addCaCertificate()`和`addCaCertificates()`进行修改。

### `QList<QSslCipher> QSslConfiguration::ciphers() const`

**作用与语义：**

返回该连接当前的密码密码套件。该列表用于握手阶段选择会话密码。返回的密码列表按偏好递减排序。（即列表中第一个密码是最优先的密码）。会话密码是列表中第一个也得到对等方支持的密码。
默认情况下，握手阶段可以选择本系统SSL库支持的任何密码，具体支持的密码可能因系统而异。该系统SSL库支持的密码列表由`supportedCiphers()`返回。您可以通过调用`setCiphers()`来限制用于选择该套接字会话密码的密码列表，并调用支持的密码子集。你可以通过调用`setCiphers()`并返回`supportedCiphers()`返回的列表来恢复使用整个密码集。

### `[static] QSslConfiguration QSslConfiguration::defaultConfiguration()`

**作用与语义：**

返回默认的SSL配置，用于新的SSL连接。
默认的SSL配置包括：
- 无本地证书和私钥
- 协议`SecureProtocols`
- 系统的默认CA证书列表
- 等于SSL库支持且128位及以上SSL密码列表的密码列表

### `[static] QSslConfiguration QSslConfiguration::defaultDtlsConfiguration()`

**作用与语义：**

返回新的DTLS连接中使用的默认DTLS配置。
默认的DTLS配置包括：
- 无本地证书和私钥
- 协议DtlsV1_2OrLater
- 系统的默认CA证书列表
- 等于SSL库支持的TLS 1.2密码列表，这些密码使用128个或以上的秘密位。

### `QSslDiffieHellmanParameters QSslConfiguration::diffieHellmanParameters() const`

**作用与语义：**

检索当前的Diffie-Hellman参数集合。
如果未设置Diffie-Hellman参数，`QSslConfiguration`对象默认使用RFC 3526中的2048位MODP组。
注意：默认参数可能会在未来的Qt版本中发生变化。请查阅你所使用的Qt版本的文档，以了解该版本使用的默认值。

### `bool QSslConfiguration::dtlsCookieVerificationEnabled() const`

**作用与语义：**

如果服务器端套接字启用了DTLS的cookie验证，该功能会返回为真。

### `QList<QSslEllipticCurve> QSslConfiguration::ellipticCurves() const`

**作用与语义：**

返回该连接当前的椭圆曲线列表。该列表在握手阶段用于选择椭圆曲线（使用椭圆曲线密码时）。返回的曲线列表按偏好递减排序（即列表中第一个曲线最优）。
默认情况下，握手阶段可以选择该系统SSL库支持的任何曲线，但这些曲线可能因系统而异。该系统SSL库支持的曲线列表由QSslSocket返回：：supportedEllipticCurves()。
你可以通过调用支持密码子集的`setEllipticCurves()`来限制用于选择该套接字会话密码的曲线列表。你可以通过调用 `setEllipticCurves()`，QSslSocket：：supportedEllipticCurves()返回的列表，恢复使用整个密码集。

### `QSslKey QSslConfiguration::ephemeralServerKey() const`

**作用与语义：**

返回用于前向保密密码算法的临时服务器密钥，例如 DHE-RSA-AES128-SHA。
临时密钥仅在客户端模式（即`QSslSocket::SslClientMode`）运行时可用。在服务器模式运行或使用无正向保密的密码算法时，返回空密钥。临时服务器密钥将在发出加密()信号之前设置。

### `[since 6.0] bool QSslConfiguration::handshakeMustInterruptOnError() const`

**作用与语义：**

如果验证回拨会提前发出`QSslSocket::handshakeInterruptedOnError()`，且握手结束前，则返回为true。
注意：该函数对除OpenSSL外的所有后端均返回false。

### `bool QSslConfiguration::isNull() const`

**作用与语义：**

如果这是空`QSslConfiguration`对象，返回`true`。
如果一个`QSslConfiguration`对象是默认构造且没有调用过设置器方法，则该对象为空。

### `QSslCertificate QSslConfiguration::localCertificate() const`

**作用与语义：**

返回证书，在SSL握手过程中向对方展示。

### `QList<QSslCertificate> QSslConfiguration::localCertificateChain() const`

**作用与语义：**

返回证书链，在SSL握手过程中向对等方展示。

### `[since 6.0] bool QSslConfiguration::missingCertificateIsFatal() const`

**作用与语义：**

如果代码`QSslError::NoPeerCertificate`的错误无法被忽略，则返回为真。
注意：除了OpenSSL外，所有TLS后端都返回false。

### `QByteArray QSslConfiguration::nextNegotiatedProtocol() const`

**作用与语义：**

如果启用了下一协议协商（NPN）或应用层协议协商（ALPN）TLS扩展，该功能返回与服务器协商的协议。为了启用NPN/ALPN扩展，连接服务器前需要显式调用`setAllowedNextProtocols()`。
如果无法协商协议或扩展未启用，该函数返回的`QByteArray`为空。

### `QSslConfiguration::NextProtocolNegotiationStatus QSslConfiguration::nextProtocolNegotiationStatus() const`

**作用与语义：**

该函数返回下一协议协商（NPN）或应用层协议协商（ALPN）的状态。如果该功能未通过`setAllowedNextProtocols()`启用，该函数返回`NextProtocolNegotiationNone`。状态将在发送加密()信号前设置。

### `bool QSslConfiguration::ocspStaplingEnabled() const`

**作用与语义：**

如果 OCSP 订书钉由 setOCSPStaplingEnabled()启用，则返回 true;否则返回 false（默认值）。

### `QSslCertificate QSslConfiguration::peerCertificate() const`

**作用与语义：**

返回对等方的数字证书（即你连接主机的直接证书），如果对方未分配证书，则返回空证书。
对等证书在握手阶段会自动检查，因此此功能通常用于获取显示或连接诊断目的的证书。它包含关于对等方的信息，包括主机名、证书发行方和对等方的公钥。
由于对等证书是在握手阶段设置的，因此从连接到 `QSslSocket::sslErrors()` 信号、`QNetworkReply::sslErrors()` 信号或`QSslSocket::encrypted()`信号的槽函数访问对等证书是安全的。
如果返回空证书，可能意味着SSL握手失败，或者你连接的主机没有证书，或者表示没有连接。
如果你想查看对等方的完整证书链，可以用`peerCertificateChain()`一次性获取所有证书。

### `QList<QSslCertificate> QSslConfiguration::peerCertificateChain() const`

**作用与语义：**

返回对等方的数字证书链，从对等方的直接证书开始，到CA的证书结束。
对等证书在握手阶段自动检查。此功能通常用于获取显示或连接诊断的证书。证书包含关于对等方和证书发行方的信息，包括主机名称、发行者名称和发行者公钥。
由于对等证书是在握手阶段设置的，因此从连接到`QSslSocket::sslErrors()`信号、`QNetworkReply::sslErrors()`信号或`QSslSocket::encrypted()`信号的槽函数访问对等证书是安全的。
如果返回空列表，可能意味着SSL握手失败，或者你连接的主机没有证书，或者表示没有连接。
如果你只想获得对等节点的直接证书，可以用`peerCertificate()`。

### `int QSslConfiguration::peerVerifyDepth() const`

**作用与语义：**

返回对等方证书链中SSL握手阶段需检查的最大证书数，若未设置最大深度则返回0（默认），表示应检查整个证书链。
证书按发出顺序检查，先是对等方自身的证书，然后是其发行方的证书，依此类推。

### `QSslSocket::PeerVerifyMode QSslConfiguration::peerVerifyMode() const`

**作用与语义：**

返回验证模式。该模式决定`QSslSocket`是否应向对端请求证书（即客户端向服务器请求证书，或服务器向客户端请求证书），以及是否要求该证书有效。
默认模式是 AutoVerifyPeer，告诉`QSslSocket`客户端使用 VerifyPeer，服务器使用 QueryPeer。

### `QByteArray QSslConfiguration::preSharedKeyIdentityHint() const`

**作用与语义：**

返回身份提示。

### `QSslKey QSslConfiguration::privateKey() const`

**作用与语义：**

返回分配给该连接的SSL密钥，如果还没有分配，则返回空密钥。

### `QSsl::SslProtocol QSslConfiguration::protocol() const`

**作用与语义：**

返回该SSL配置的协议设置。

### `QSslCipher QSslConfiguration::sessionCipher() const`

**作用与语义：**

返回套接字的密码`cipher`，如果连接未加密，则返回空密码。会话的套接字密码在握手阶段设置。该密码用于加密和解密通过套接字传输的数据。
SSL基础设施还提供设置有序密码列表的功能，握手阶段最终从中选择会话密码。该有序列表必须在握手阶段开始前就已完成。

### `QSsl::SslProtocol QSslConfiguration::sessionProtocol() const`

**作用与语义：**

返回套接字的SSL/TLS协议，如果连接未加密，则返回未知协议。会话的套接字协议在握手阶段设置。

### `QByteArray QSslConfiguration::sessionTicket() const`

**作用与语义：**

如果`QSsl::SslOptionDisableSessionPersistence`关闭，该函数返回SSL握手中使用的会话工单，格式为ASN.1，适合例如持久保存到磁盘。如果未使用会话工单或未关闭`QSsl::SslOptionDisableSessionPersistence`，该功能返回空`QByteArray`。
注意：在将会话工单持久化到磁盘或类似内容时，请小心不要暴露该会话，因为会谈信息可能被窃听到用会话参数加密的数据。

### `int QSslConfiguration::sessionTicketLifeTimeHint() const`

**作用与语义：**

如果`QSsl::SslOptionDisableSessionPersistence`关闭，该函数返回服务器发送的会话工单寿命提示（可能是0）。如果服务器未发送会话工单（例如恢复会话时或服务器不支持时）或`QSsl::SslOptionDisableSessionPersistence`未关闭，该函数返回-1。

### `void QSslConfiguration::setAllowedNextProtocols(const QList<QByteArray> &protocols)`

**作用与语义：**

该函数通过下一协议协商（NPN）或应用层协议协商（ALPN）TLS扩展，设置允许的`protocols`与服务器协商;`protocols`中的每个元素必须定义一个允许的协议。必须在连接前明确调用该函数，以通过SSL握手发送NPN/ALPN扩展。协商是否成功可以通过`nextProtocolNegotiationStatus()`查询。

### `void QSslConfiguration::setBackendConfiguration(const QMap<QByteArray, QVariant> &backendConfiguration = QMap<QByteArray, QVariant>())`

**作用与语义：**

设置或清除后端特定的配置。
如果没有`backendConfiguration`参数，该函数会清除后端特定的配置。关于支持选项的更多信息可见于`setBackendConfigurationOption()`文档中。

### `void QSslConfiguration::setBackendConfigurationOption(const QByteArray &name, const QVariant &value)`

**作用与语义：**

在后端特定配置中将选项`name`设置为`value`。
OpenSSL（>= 1.0.2）后端支持的选项可在支持的配置文件命令文档中提供。`value`参数的预期类型是所有选项的 `QByteArray`。示例展示了如何使用部分选项。
注意：后端专用配置将在通用配置之后应用。使用后端特定配置重新设置通用配置选项，将覆盖通用配置选项。

### `void QSslConfiguration::setCaCertificates(const QList<QSslCertificate> &certificates)`

**作用与语义：**

将该套接字的CA证书数据库设置为`certificates`。证书数据库必须在SSL握手前设置。CA证书数据库在握手阶段被套接字用于验证对方证书。
注意：默认配置使用系统CA证书数据库。如果没有该数据库（iOS上常见情况），默认数据库为空。

### `void QSslConfiguration::setCiphers(const QList<QSslCipher> &ciphers)`

**作用与语义：**

将该套接字的密码套件设置为`ciphers`，必须包含`supportedCiphers()`返回列表中的部分密码子集。
限制密码套件必须在握手阶段之前完成，该阶段选择会话密码。

### `[since 6.0] void QSslConfiguration::setCiphers(const QString &ciphers)`

**作用与语义：**

将该配置的密码密码套件设置为`ciphers`，即一个以冒号分隔的密码套件名称列表。密码按偏好顺序排列，从最优选的密码开始。`ciphers`中的每个密码名称必须是`supportedCiphers()`返回列表中的密码名称。限制密码套件必须在握手阶段之前完成，该阶段选择会话密码。
注意：在Schannel后端，密码顺序被忽略，Schannel在握手过程中选择最安全的顺序。

### `[static] void QSslConfiguration::setDefaultConfiguration(const QSslConfiguration &configuration)`

**作用与语义：**

设置用于新SSL连接的默认SSL配置，设置为`configuration`。现有连接不受此调用影响。

### `[static] void QSslConfiguration::setDefaultDtlsConfiguration(const QSslConfiguration &configuration)`

**作用与语义：**

将新的 DTLS 连接中的默认 DTLS 配置设置为`configuration`。现有连接不受此调用影响。

### `void QSslConfiguration::setDiffieHellmanParameters(const QSslDiffieHellmanParameters &dhparams)`

**作用与语义：**

设置一套自定义的Diffie-Hellman参数，使该套接字在作为服务器时使用`dhparams`。
如果没有设置Diffie-Hellman参数，`QSslConfiguration`对象默认使用RFC 3526中的2048位MODP组。
自6.7版本起，如果TLS后端支持，你可以提供空的Diffie-Hellman参数来使用自动选择（参见openssl的SSL_CTX_set_dh_auto）。
注意：默认参数可能会在未来的Qt版本中发生变化。请查阅你所使用的Qt版本的文档，以了解该版本使用的默认值。

### `void QSslConfiguration::setDtlsCookieVerificationEnabled(bool enable)`

**作用与语义：**

当 `enable` 为真时，此功能可实现 DTLS 的 Cookie 验证。

### `void QSslConfiguration::setEllipticCurves(const QList<QSslEllipticCurve> &curves)`

**作用与语义：**

将该套接字使用的椭圆曲线列表设置为`curves`，该列表必须包含`supportedEllipticCurves()`返回的曲线子集。
限制椭圆曲线必须在握手阶段之前完成，握手阶段选择会话密码。

### `[since 6.0] void QSslConfiguration::setHandshakeMustInterruptOnError(bool interrupt)`

**作用与语义：**

如果`interrupt`为真且底层后端支持该选项，证书验证过程中发现的错误会立即通过发出`QSslSocket::handshakeInterruptedOnError()`报告。这允许停止未完成的握手，并向对等端发送适当的警报消息。在这种情况下，应用程序无需采取特殊操作。`QSslSocket`在发送警报消息后关闭连接。如果应用程序在检查错误后想继续握手，必须从其槽函数函数调用`QSslSocket::continueInterruptedHandshake()`。信号-槽函数连接必须是直接的。
注意：当启用中断握手时，原本由`QSslSocket::peerVerifyError()`报告的错误仅由`QSslSocket::handshakeInterruptedOnError()`报告。
注意：即使握手继续，这些错误在发出`QSslSocket::sslErrors()`信号时也会被报告（因此在相应功能槽中必须忽略）。

### `void QSslConfiguration::setLocalCertificate(const QSslCertificate &certificate)`

**作用与语义：**

设置在SSL握手期间向对等方展示的证书为`certificate`。
连接建立后设置证书不会生效。
证书是SSL过程中使用的身份识别手段。本地证书由远程端用来验证本地用户的身份与其认证机构列表的关系。在大多数情况下，如HTTP网页浏览中，只有服务器向客户端识别，因此客户端不会发送证书。

### `void QSslConfiguration::setLocalCertificateChain(const QList<QSslCertificate> &localChain)`

**作用与语义：**

在SSL握手期间，将证书链设置为`localChain`。
连接建立后设置证书链无效。
证书是SSL过程中使用的身份识别手段。本地证书由远程端用来验证本地用户的身份与其认证机构列表的关系。在大多数情况下，如HTTP网页浏览中，只有服务器向客户端识别，因此客户端不会发送证书。
与`QSslConfiguration::setLocalCertificate()`不同这种方法允许你指定验证证书所需的中间证书。列表中的第一项必须是叶子证书。

### `[since 6.0] void QSslConfiguration::setMissingCertificateIsFatal(bool cannotRecover)`

**作用与语义：**

如果`cannotRecover`为真，且验证模式为`QSslSocket::VerifyPeer`或`QSslSocket::AutoVerifyPeer`（客户端套接字），则缺失节点的证书将被视为不可恢复的错误，无法忽视。关闭连接前，会向对端发送适当的警报消息。
注意：只有Qt配置并构建OpenSSL后端时才可用。

### `void QSslConfiguration::setOcspStaplingEnabled(bool enabled)`

**作用与语义：**

如果`enabled`为真，客户端 `QSslSocket` 在发起握手时会向对等方发送证书状态请求。握手过程中`QSslSocket`会验证服务器的响应。该值必须在握手开始前设置。

### `void QSslConfiguration::setPeerVerifyDepth(int depth)`

**作用与语义：**

在SSL握手阶段，将对端证书链中需要检查的最大证书数量设置为`depth`。设置深度为0意味着不设置最大深度，表示应检查整个证书链。
证书按发出顺序检查，先是对等方自身的证书，然后是其发行方的证书，依此类推。

### `void QSslConfiguration::setPeerVerifyMode(QSslSocket::PeerVerifyMode mode)`

**作用与语义：**

将验证模式设置为`mode`。该模式决定`QSslSocket`是否应向对端请求证书（即客户端向服务器请求证书，或服务器向客户端请求证书），以及是否要求该证书有效。
默认模式是 AutoVerifyPeer，它告诉`QSslSocket`客户端使用 VerifyPeer，服务器使用 QueryPeer。

### `void QSslConfiguration::setPreSharedKeyIdentityHint(const QByteArray &hint)`

**作用与语义：**

将预共享密钥认证的身份提示设置为`hint`。这会影响下一次发起的握手;调用该函数对已加密的套接字不会影响套接字的身份提示。
身份提示仅用于`QSslSocket::SslServerMode`！

### `void QSslConfiguration::setPrivateKey(const QSslKey &key)`

**作用与语义：**

将连接的私有`key`设置为`key`。私钥和本地`certificate`被需要向SSL对等端证明身份的客户端和服务器使用。
如果你创建 SSL 服务器套接字，密钥和本地证书都是必需的。如果你创建 SSL 客户端套接字，那么如果客户端必须向 SSL 服务器识别自己，密钥和本地证书是必需的。

### `void QSslConfiguration::setProtocol(QSsl::SslProtocol protocol)`

**作用与语义：**

将该配置的协议设置设置为`protocol`。
连接建立后设置协议无效。

### `void QSslConfiguration::setSessionTicket(const QByteArray &sessionTicket)`

**作用与语义：**

将会话工单设置为用于SSL握手。`QSsl::SslOptionDisableSessionPersistence`必须关闭才能实现此功能，且`sessionTicket`必须采用`sessionTicket()`返回的ASN.1格式。

### `void QSslConfiguration::setSslOption(QSsl::SslOption option, bool on)`

**作用与语义：**

启用或禁用SSL兼容性`option`。如果`on`为真，则`option`被启用。如果`on`为假，则`option`被禁用。

### `[static] QList<QSslCipher> QSslConfiguration::supportedCiphers()`

**作用与语义：**

返回该系统支持的密码学密码列表。该列表由系统的 SSL 库设置，且可能因系统而异。

### `[static] QList<QSslEllipticCurve> QSslConfiguration::supportedEllipticCurves()`

**作用与语义：**

返回该系统支持的椭圆曲线列表。该列表由系统的SSL库设置，且可能因系统而异。

### `[noexcept] void QSslConfiguration::swap(QSslConfiguration &other)`

**作用与语义：**

将该SSL配置实例与`other`交换。此操作非常快速且从未失败。

### `[static] QList<QSslCertificate> QSslConfiguration::systemCaCertificates()`

**作用与语义：**

该函数提供操作系统提供的CA证书数据库。该函数返回的CA证书数据库用于初始化默认`QSslConfiguration`上`caCertificates()`返回的数据库。

### `bool QSslConfiguration::testSslOption(QSsl::SslOption option) const`

**作用与语义：**

如果启用了指定的SSL兼容性`option`，返回`true`。

### `bool QSslConfiguration::operator!=(const QSslConfiguration &other) const`

**作用与语义：**

如果`QSslConfiguration`与`other`不同，返回`true`。如果任何状态或环境不同，两个`QSslConfiguration`对象被视为不同。

### `QSslConfiguration &QSslConfiguration::operator=(const QSslConfiguration &other)`

**作用与语义：**

复制`other`的配置和状态。如果`other`空，这个对象也是空。

### `bool QSslConfiguration::operator==(const QSslConfiguration &other) const`

**作用与语义：**

如果该`QSslConfiguration`对象等于`other`，则返回`true`。
如果两个`QSslConfiguration`对象的设置和状态完全相同，则它们被视为相等。

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

`QSslConfiguration` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
