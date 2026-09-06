# QSslServer

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QSslServer` 是 Qt Network 的“Ssl服务器”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QSslServer` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QSslServer>`
- 继承自：QTcpServer
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

### 公有函数

- `QSslServer(QObject *parent = nullptr)`
- `virtual ~QSslServer() override`
- `int handshakeTimeout() const`
- `void setHandshakeTimeout(int timeout)`
- `void setSslConfiguration(const QSslConfiguration &sslConfiguration)`
- `QSslConfiguration sslConfiguration() const`

### 信号

- `void alertReceived(QSslSocket *socket, QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`
- `void alertSent(QSslSocket *socket, QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`
- `void errorOccurred(QSslSocket *socket, QAbstractSocket::SocketError socketError)`
- `void handshakeInterruptedOnError(QSslSocket *socket, const QSslError &error)`
- `void peerVerifyError(QSslSocket *socket, const QSslError &error)`
- `void preSharedKeyAuthenticationRequired(QSslSocket *socket, QSslPreSharedKeyAuthenticator *authenticator)`
- `void sslErrors(QSslSocket *socket, const QList<QSslError> &errors)`
- `void startedEncryptionHandshake(QSslSocket *socket)`

### 重实现的保护函数

- `virtual void incomingConnection(qintptr socket) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QSslServer::QSslServer(QObject *parent = nullptr)`

**作用与语义：**

构建一个带有给定`parent`的新QSslServer。

### `[override virtual noexcept] QSslServer::~QSslServer()`

**作用与语义：**

毁了`QSslServer`。
所有开路连接均关闭。

### `[signal] void QSslServer::alertReceived(QSslSocket *socket, QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`

**作用与语义：**

如果`socket`收到来自对等端的警报消息，`QSslServer`会发出此信号。`level` 表示该警报是致命还是警告。`type`是解释为何发送警报的代码。当有警报消息的文本描述时，会以`description`形式提供。
注意：该信号主要用于信息和调试目的，不需要在应用程序中处理。如果警报是致命的，底层后端会处理并关闭连接。
注意：并非所有后端都支持此功能。

### `[signal] void QSslServer::alertSent(QSslSocket *socket, QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`

**作用与语义：**

如果`socket`向对端发送了警报消息，`QSslServer`会发出该信号。`level`描述是警告还是致命错误。`type`给出警报消息的代码。当有警报消息的文本描述时，会以`description`形式提供。
注意：该信号主要用于信息性，可用于调试，通常不需要应用程序执行任何操作。
注意：并非所有后端都支持此功能。

### `[signal] void QSslServer::errorOccurred(QSslSocket *socket, QAbstractSocket::SocketError socketError)`

**作用与语义：**

该信号是在握手过程中发生错误后发出的。`socketError`参数描述了发生的错误类型。
如果套接字握手未达到加密状态，该信号发出后该`socket`会自动删除。但如果该`socket`成功加密，则会入`QSslServer`的待处理连接队列中。当用户调用`QTcpServer::nextPendingConnection()`时，用户有责任销毁`socket`，否则`socket`不会被销毁，直到`QSslServer`对象被销毁。如果`socket`在插入待处理连接队列后发生错误，该信号不会发出，`socket`也不会被移除或销毁。
注意：连接该信号时不能使用`Qt::QueuedConnection`，否则信号处理时`socket`已经被销毁。

### `[signal] void QSslServer::handshakeInterruptedOnError(QSslSocket *socket, const QSslError &error)`

**作用与语义：**

如果`socket`发现证书验证错误且`QSslConfiguration`启用早期错误报告，`QSslServer`会发出该信号。应用程序应检查`error`，决定是否继续握手，或中止握手并向对端发送警报消息。信号-槽函数连接必须是直接的。

### `int QSslServer::handshakeTimeout() const`

**作用与语义：**

返回当前配置的握手超时。

### `[override virtual protected] void QSslServer::incomingConnection(qintptr socket)`

**作用与语义：**

重实现自：`QTcpServer::incomingConnection`（qintptr socketDescriptor）。
当新连接建立时会被调用。
将`socket`转化为`QSslSocket`。
当有新连接可用时，`QTcpServer`调用该虚拟函数。`socketDescriptor`参数是接受连接的本地套接字描述符。
基础实现创建`QTcpSocket`，设置套接字描述符，然后将`QTcpSocket`存储在待处理连接的内部列表中。最后`newConnection()`被发出。
重新实现该函数以改变连接可用时服务器的行为。
如果该服务器使用 `QNetworkProxy`，则该`socketDescriptor`可能无法与本地套接字函数一起使用，应仅与 `QTcpSocket::setSocketDescriptor()` 一起使用。
注意：如果在该方法的重实现中创建了另一个套接字，需要通过调用`addPendingConnection()`将其添加到待处理连接机制中。
注意：如果你想将一个新连接作为另一个线程中的新`QTcpSocket`对象处理，你必须将`socketDescriptor`传递给另一个线程，在那里创建`QTcpSocket`对象并使用其`setSocketDescriptor()`方法。

### `[signal] void QSslServer::peerVerifyError(QSslSocket *socket, const QSslError &error)`

**作用与语义：**

`QSslServer`可以在SSL握手过程中多次发出该信号，在加密尚未建立之前，以表明在确认对等端身份时发生了错误。`error`通常表示`socket`无法安全识别对等端。
该信号能让您提前发现异常。通过连接该信号，您可以在握手完成前手动选择从连接槽内断开连接。如果未采取任何行动，`QSslServer`将继续发出`sslErrors()`。

### `[signal] void QSslServer::preSharedKeyAuthenticationRequired(QSslSocket *socket, QSslPreSharedKeyAuthenticator *authenticator)`

**作用与语义：**

`QSslServer`在协商PSK密码套件时`socket`会发出该信号，因此需要PSK认证。
使用PSK时，服务器必须提供有效的身份和有效的预共享密钥，才能继续SSL握手。应用程序可以通过根据需求填写传递`authenticator`对象，在连接到该信号的槽中提供这些信息。
注意：忽视该信号或未提供所需凭证，将导致握手失败，连接将被终止。
注意：`authenticator`对象归`socket`所有，应用程序不得删除。

### `void QSslServer::setHandshakeTimeout(int timeout)`

**作用与语义：**

将所有来电握手的 `timeout` 设置成毫秒级。
这在客户端（无论是恶意还是意外）连接到服务器但未尝试通信或发起握手的情况下尤为重要。`QSslServer` 会在`timeout`毫秒后自动终止连接。
默认情况下，超时为5000毫秒（5秒）。
注意：底层TLS框架现在或未来可能有自己的超时逻辑，但该函数不会影响这些。
注意：传递给该函数的`timeout`只适用于新连接。如果客户端已经连接，它将使用连接时设定的超时值。

### `void QSslServer::setSslConfiguration(const QSslConfiguration &sslConfiguration)`

**作用与语义：**

设置`sslConfiguration`用于后续所有进来连接。
必须在 `listen()` 前调用此设备，以确保所有握手过程中所需的配置均已使用。

### `QSslConfiguration QSslServer::sslConfiguration() const`

**作用与语义：**

返回当前的SSL配置。

### `[signal] void QSslServer::sslErrors(QSslSocket *socket, const QList<QSslError> &errors)`

**作用与语义：**

`QSslServer`在SSL握手后发出该信号，表示在建立对等端身份时发生了一个或多个错误。这些错误通常表明`socket`无法安全识别对等端。除非采取任何措施，否则该信号发出后连接将被中断。
如果你想在发生错误的情况下继续连接，必须从连接到该信号的槽函数内调用`QSslSocket::ignoreSslErrors()`。如果你以后需要访问错误列表，可以调用 sslHandshakeErrors()。
`errors`包含一个或多个错误，阻止`QSslSocket`验证对等端的身份。
注意：连接该信号时不能使用`Qt::QueuedConnection`，或者调用`QSslSocket::ignoreSslErrors()`也无效。

### `[signal] void QSslServer::startedEncryptionHandshake(QSslSocket *socket)`

**作用与语义：**

当客户端连接到`socket`发起TLS握手时，该信号会发出。

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

`QSslServer` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
