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

### 相关非成员函数

- `Constant Value Description`
- `QDtls::QDtlsError::NoError 0 No error occurred, the last operation was successful.`
- `QDtls::QDtlsError::InvalidInputParameters 1 Input parameters provided by a caller were invalid.`
- `QDtls::QDtlsError::InvalidOperation 2 An operation was attempted in a state that did not permit it.`
- `QDtls::QDtlsError::UnderlyingSocketError 3 QUdpSocket::writeDatagram() failed, QUdpSocket::error() and QUdpSocket::errorString() can provide more specific information.`
- `QDtls::QDtlsError::RemoteClosedConnectionError 4 TLS shutdown alert message was received.`
- `QDtls::QDtlsError::PeerVerificationError 5 Peer's identity could not be verified during the TLS handshake.`
- `QDtls::QDtlsError::TlsInitializationError 6 An error occurred while initializing an underlying TLS backend.`
- `QDtls::QDtlsError::TlsFatalError 7 A fatal error occurred during TLS handshake, other than peer verification error or TLS initialization error.`
- `QDtls::QDtlsError::TlsNonFatalError 8 A failure to encrypt or decrypt a datagram, non-fatal, meaning QDtls can continue working after this error.`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 44 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QDtls::HandshakeState`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDtls` 暴露的类型声明 `Handshake、State`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:HandshakeState`。
- 属性名：`QDtls`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QDtls::QDtls(QSslSocket::SslMode mode, QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDtls` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `mode`：类型为 `QSslSocket::SslMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QDtls::~QDtls()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDtls` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDtls::abortHandshake(QUdpSocket *socket)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `abortHandshake`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `socket`：类型为 `QUdpSocket *`。没有默认值，调用时必须提供。传入 `QUdpSocket *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDtls::GeneratorParameters QDtls::cookieGeneratorParameters() const`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::cookieGeneratorParameters` 用于计算、查询或取得与“cookie、Generator、Parameters”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDtls::GeneratorParameters`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDtls::GeneratorParameters`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QDtls::decryptDatagram(QUdpSocket *socket, const QByteArray &dgram)`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::decryptDatagram` 用于计算、查询或取得与“decrypt、Datagram”相关的操作。调用时要先确认当前状态和 `socket`、`dgram` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `socket`：类型为 `QUdpSocket *`。没有默认值，调用时必须提供。传入 `QUdpSocket *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dgram`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDtls::doHandshake(QUdpSocket *socket, const QByteArray &dgram = {})`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::doHandshake` 用于计算、查询或取得与“do、Handshake”相关的操作。调用时要先确认当前状态和 `socket`、`dgram` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `socket`：类型为 `QUdpSocket *`。没有默认值，调用时必须提供。传入 `QUdpSocket *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dgram`：类型为 `const QByteArray &`。默认值为 `{}`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslConfiguration QDtls::dtlsConfiguration() const`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::dtlsConfiguration` 用于计算、查询或取得与“dtls、Configuration”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslConfiguration`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslConfiguration`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDtlsError QDtls::dtlsError() const`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::dtlsError` 用于计算、查询或取得与“dtls、错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDtlsError`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDtlsError`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDtls::dtlsErrorString() const`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::dtlsErrorString` 用于计算、查询或取得与“dtls、错误、字符串”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDtls::handleTimeout(QUdpSocket *socket)`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::handleTimeout` 用于计算、查询或取得与“handle、超时”相关的操作。调用时要先确认当前状态和 `socket` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `socket`：类型为 `QUdpSocket *`。没有默认值，调用时必须提供。传入 `QUdpSocket *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDtls::HandshakeState QDtls::handshakeState() const`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::handshakeState` 用于计算、查询或取得与“handshake、State”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDtls::HandshakeState`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDtls::HandshakeState`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QDtls::handshakeTimeout()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDtls` 发出的通知信号 `handshakeTimeout`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDtls::ignoreVerificationErrors(const QList<QSslError> &errorsToIgnore)`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::ignoreVerificationErrors` 用于执行与“ignore、Verification、Errors”相关的操作。调用时要先确认当前状态和 `errorsToIgnore` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `errorsToIgnore`：类型为 `const QList<QSslError> &`。没有默认值，调用时必须提供。传入 `const QList<QSslError> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDtls::isConnectionEncrypted() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isConnectionEncrypted`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint16 QDtls::mtuHint() const`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::mtuHint` 用于计算、查询或取得与“mtu、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `quint16`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint16`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QHostAddress QDtls::peerAddress() const`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::peerAddress` 用于计算、查询或取得与“peer、Address”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QHostAddress`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QHostAddress`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint16 QDtls::peerPort() const`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::peerPort` 用于计算、查询或取得与“peer、Port”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `quint16`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint16`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QSslError> QDtls::peerVerificationErrors() const`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::peerVerificationErrors` 用于计算、查询或取得与“peer、Verification、Errors”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QSslError>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QSslError>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDtls::peerVerificationName() const`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::peerVerificationName` 用于计算、查询或取得与“peer、Verification、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QDtls::pskRequired(QSslPreSharedKeyAuthenticator *authenticator)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDtls` 发出的通知信号 `pskRequired`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `authenticator`：类型为 `QSslPreSharedKeyAuthenticator *`。没有默认值，调用时必须提供。传入 `QSslPreSharedKeyAuthenticator *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDtls::resumeHandshake(QUdpSocket *socket)`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::resumeHandshake` 用于计算、查询或取得与“恢复运行、Handshake”相关的操作。调用时要先确认当前状态和 `socket` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `socket`：类型为 `QUdpSocket *`。没有默认值，调用时必须提供。传入 `QUdpSocket *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslCipher QDtls::sessionCipher() const`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::sessionCipher` 用于计算、查询或取得与“session、Cipher”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslCipher`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslCipher`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSsl::SslProtocol QDtls::sessionProtocol() const`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::sessionProtocol` 用于计算、查询或取得与“session、Protocol”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSsl::SslProtocol`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSsl::SslProtocol`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDtls::setCookieGeneratorParameters(const QDtls::GeneratorParameters &params)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCookieGeneratorParameters`。调用它会改变 `QDtls` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `params`：类型为 `const QDtls::GeneratorParameters &`。没有默认值，调用时必须提供。传入 `const QDtls::GeneratorParameters &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDtls::setDtlsConfiguration(const QSslConfiguration &configuration)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDtlsConfiguration`。调用它会改变 `QDtls` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `configuration`：类型为 `const QSslConfiguration &`。没有默认值，调用时必须提供。传入 `const QSslConfiguration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDtls::setMtuHint(quint16 mtuHint)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMtuHint`。调用它会改变 `QDtls` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mtuHint`：类型为 `quint16`。没有默认值，调用时必须提供。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDtls::setPeer(const QHostAddress &address, quint16 port, const QString &verificationName = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPeer`。调用它会改变 `QDtls` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `address`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `port`：类型为 `quint16`。没有默认值，调用时必须提供。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `verificationName`：类型为 `const QString &`。默认值为 `{}`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDtls::setPeerVerificationName(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPeerVerificationName`。调用它会改变 `QDtls` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDtls::shutdown(QUdpSocket *socket)`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::shutdown` 用于计算、查询或取得与“shutdown”相关的操作。调用时要先确认当前状态和 `socket` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `socket`：类型为 `QUdpSocket *`。没有默认值，调用时必须提供。传入 `QUdpSocket *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslSocket::SslMode QDtls::sslMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QDtls::sslMode` 用于计算、查询或取得与“ssl、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslSocket::SslMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslSocket::SslMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QDtls::writeDatagramEncrypted(QUdpSocket *socket, const QByteArray &dgram)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDtls` 的核心操作 `writeDatagramEncrypted`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `socket`：类型为 `QUdpSocket *`。没有默认值，调用时必须提供。传入 `QUdpSocket *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dgram`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum class QDtlsError`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDtls` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GeneratorParameters`

**API 类别：** 公有类型

**中文解读：** 这是 `QDtls` 的 `Generator、Parameters` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Constant Value Description`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDtls` 的 `Constant` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDtls::QDtlsError::NoError 0 No error occurred, the last operation was successful.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDtls` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:QDtlsError::NoError 0 No error occurred, the last operation was successful.`。
- 属性名：`QDtls`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDtls::QDtlsError::InvalidInputParameters 1 Input parameters provided by a caller were invalid.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDtls` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:QDtlsError::InvalidInputParameters 1 Input parameters provided by a caller were invalid.`。
- 属性名：`QDtls`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDtls::QDtlsError::InvalidOperation 2 An operation was attempted in a state that did not permit it.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDtls` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:QDtlsError::InvalidOperation 2 An operation was attempted in a state that did not permit it.`。
- 属性名：`QDtls`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDtls::QDtlsError::UnderlyingSocketError 3 QUdpSocket::writeDatagram() failed, QUdpSocket::error() and QUdpSocket::errorString() can provide more specific information.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDtls` 的核心操作 `writeDatagram`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QDtls::QDtlsError::UnderlyingSocketError 3`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDtls::QDtlsError::RemoteClosedConnectionError 4 TLS shutdown alert message was received.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDtls` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:QDtlsError::RemoteClosedConnectionError 4 TLS shutdown alert message was received.`。
- 属性名：`QDtls`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDtls::QDtlsError::PeerVerificationError 5 Peer's identity could not be verified during the TLS handshake.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDtls` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:QDtlsError::PeerVerificationError 5 Peer's identity could not be verified during the TLS handshake.`。
- 属性名：`QDtls`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDtls::QDtlsError::TlsInitializationError 6 An error occurred while initializing an underlying TLS backend.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDtls` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:QDtlsError::TlsInitializationError 6 An error occurred while initializing an underlying TLS backend.`。
- 属性名：`QDtls`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDtls::QDtlsError::TlsFatalError 7 A fatal error occurred during TLS handshake, other than peer verification error or TLS initialization error.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDtls` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:QDtlsError::TlsFatalError 7 A fatal error occurred during TLS handshake, other than peer verification error or TLS initialization error.`。
- 属性名：`QDtls`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDtls::QDtlsError::TlsNonFatalError 8 A failure to encrypt or decrypt a datagram, non-fatal, meaning QDtls can continue working after this error.`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDtls` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 属性类型：`:QDtlsError::TlsNonFatalError 8 A failure to encrypt or decrypt a datagram, non-fatal, meaning QDtls can continue working after this error.`。
- 属性名：`QDtls`；读取和写入权限以签名前缀和对应访问函数为准。
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

`QDtls` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
