# QTcpServer

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QTcpServer` 是 Qt Network 的“Tcp服务器”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QTcpServer` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QTcpServer>`
- 继承自：QObject
- 直接派生类：QSctpServer、QSslServer

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

### 公有函数

- `QTcpServer(QObject *parent = nullptr)`
- `virtual ~QTcpServer()`
- `void close()`
- `QString errorString() const`
- `virtual bool hasPendingConnections() const`
- `bool isListening() const`
- `bool listen(const QHostAddress &address = QHostAddress::Any, quint16 port = 0)`
- `(since 6.3) int listenBacklogSize() const`
- `int maxPendingConnections() const`
- `virtual QTcpSocket * nextPendingConnection()`
- `void pauseAccepting()`
- `QNetworkProxy proxy() const`
- `void resumeAccepting()`
- `QHostAddress serverAddress() const`
- `QAbstractSocket::SocketError serverError() const`
- `quint16 serverPort() const`
- `(since 6.3) void setListenBacklogSize(int size)`
- `void setMaxPendingConnections(int numConnections)`
- `void setProxy(const QNetworkProxy &networkProxy)`
- `bool setSocketDescriptor(qintptr socketDescriptor)`
- `qintptr socketDescriptor() const`
- `bool waitForNewConnection(int msec = 0, bool *timedOut = nullptr)`

### 信号

- `void acceptError(QAbstractSocket::SocketError socketError)`
- `void newConnection()`
- `(since 6.4) void pendingConnectionAvailable()`

### 保护函数

- `void addPendingConnection(QTcpSocket *socket)`
- `virtual void incomingConnection(qintptr socketDescriptor)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QTcpServer::QTcpServer(QObject *parent = nullptr)`

**作用与语义：**

构建一个QTcpServer对象。
`parent`传递给`QObject`构造者。

### `[virtual noexcept] QTcpServer::~QTcpServer()`

**作用与语义：**

销毁`QTcpServer`对象。如果服务器监听连接，套接字会自动关闭。
任何仍然连接的客户端 `QTcpSocket`，必须在服务器被删除前断开连接或重新父级。

### `[signal] void QTcpServer::acceptError(QAbstractSocket::SocketError socketError)`

**作用与语义：**

当接受新连接导致错误时，该信号会发出。`socketError`参数描述了发生的错误类型。

### `[protected] void QTcpServer::addPendingConnection(QTcpSocket *socket)`

**作用与语义：**

`QTcpServer::incomingConnection()`调用该函数，将`socket`添加到待处理的入连接列表中。
注意：如果你不想破坏待处理连接机制，别忘了调用重实现`incomingConnection()`中的这个成员。该函数在套接字添加后发出`pendingConnectionAvailable()`信号。

### `void QTcpServer::close()`

**作用与语义：**

服务器会关闭。服务器将不再监听入站连接。

### `QString QTcpServer::errorString() const`

**作用与语义：**

返回对最后一次错误的人类可读描述。

### `[virtual] bool QTcpServer::hasPendingConnections() const`

**作用与语义：**

如果服务器有待处理连接，返回`true`;否则返回`false`。

### `[virtual protected] void QTcpServer::incomingConnection(qintptr socketDescriptor)`

**作用与语义：**

当有新连接可用时，`QTcpServer`调用该虚拟函数。`socketDescriptor`参数是接受连接的本地套接字描述符。
基础实现创建`QTcpSocket`，设置套接字描述符，然后将`QTcpSocket`存储在待处理连接的内部列表中。最后`newConnection()`被发出。
重新实现该函数以改变连接可用时服务器的行为。
如果该服务器使用 `QNetworkProxy`，那么该 `socketDescriptor` 可能无法与原生套接字函数一起使用，只能与 `QTcpSocket::setSocketDescriptor()` 一起使用。
注意：如果在该方法的重新实现中创建了另一个套接字，需要通过调用`addPendingConnection()`将其添加到待处理连接机制中。
注意：如果你想作为另一个线程中的新`QTcpSocket`对象处理一个新连接，你必须把`socketDescriptor`传递给另一个线程，在那里创建`QTcpSocket`对象并使用其`setSocketDescriptor()`方法。

### `bool QTcpServer::isListening() const`

**作用与语义：**

如果服务器当前正在监听输入连接，返回`true`;否则返回`false`。

### `bool QTcpServer::listen(const QHostAddress &address = QHostAddress::Any, quint16 port = 0)`

**作用与语义：**

告诉服务器监听地址`address`和端口`port`的来电连接。如果`port`为0，会自动选择端口。如果`address`为`QHostAddress::Any`，服务器将在所有网络接口监听。
成功时返回`true`;否则返回`false`。

### `[since 6.3] int QTcpServer::listenBacklogSize() const`

**作用与语义：**

返回待接受连接的队列大小。

### `int QTcpServer::maxPendingConnections() const`

**作用与语义：**

返回最大待处理接受连接数。默认为30。

### `[signal] void QTcpServer::newConnection()`

**作用与语义：**

每当有新连接可用时，无论该连接是否已被添加到待处理连接队列，都会发出该信号。

### `[virtual] QTcpSocket *QTcpServer::nextPendingConnection()`

**作用与语义：**

返回下一个待处理连接，作为连接`QTcpSocket`对象。
套接字作为服务器的子节点创建，这意味着当`QTcpServer`对象被销毁时，它会自动被删除。使用完毕后显式删除该对象仍然是一个好主意，以避免浪费内存。
如果在没有待处理连接的情况下调用该函数，`nullptr` 会返回。
注意：返回的`QTcpSocket`对象不能从其他线程使用。如果你想使用来自其他线程的输入连接，需要覆盖`incomingConnection()`。

### `void QTcpServer::pauseAccepting()`

**作用与语义：**

暂停接受新连接。排队的连接将继续排队。

### `[private signal, since 6.4] void QTcpServer::pendingConnectionAvailable()`

**作用与语义：**

每当有新连接加入待处理连接队列时，都会发出该信号。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `QNetworkProxy QTcpServer::proxy() const`

**作用与语义：**

返回该套接字的网络代理。默认情况下使用`QNetworkProxy::DefaultProxy`。

### `void QTcpServer::resumeAccepting()`

**作用与语义：**

简历接受新连接。

### `QHostAddress QTcpServer::serverAddress() const`

**作用与语义：**

如果服务器正在监听连接，返回地址;否则返回`QHostAddress::Null`。

### `QAbstractSocket::SocketError QTcpServer::serverError() const`

**作用与语义：**

返回最后一次发生的错误代码。

### `quint16 QTcpServer::serverPort() const`

**作用与语义：**

如果服务器正在监听连接，返回端口;否则返回0。

### `[since 6.3] void QTcpServer::setListenBacklogSize(int size)`

**作用与语义：**

将待办队列大小设置为可接受的连接`size`。操作系统可能会减少或忽略该值。默认情况下，队列大小为50。
注意：该属性必须在调用`listen()`之前设置。

### `void QTcpServer::setMaxPendingConnections(int numConnections)`

**作用与语义：**

将待处理接受连接的最大数量设定为`numConnections`。`QTcpServer`在调用`nextPendingConnection()`前最多接受`numConnections`条入站连接。默认限制为30条待处理连接。
客户端在服务器达到最大待处理连接数后仍可能连接（即`QTcpSocket`仍可发出connected()信号）。`QTcpServer`会停止接受新连接，但操作系统仍可能将其保留在队列中。

### `void QTcpServer::setProxy(const QNetworkProxy &networkProxy)`

**作用与语义：**

将该套接字的显式网络代理设置为`networkProxy`。
要禁用该套接字的代理，请使用`QNetworkProxy::NoProxy`代理类型：

**官方示例：**

```cpp
 server->setProxy(QNetworkProxy::NoProxy);
```

### `bool QTcpServer::setSocketDescriptor(qintptr socketDescriptor)`

**作用与语义：**

设置该服务器在监听`socketDescriptor`连接时应使用的套接字描述符。如果套接字成功设置，返回`true`;否则返回`false`。
假设槽函数处于监听状态。

### `qintptr QTcpServer::socketDescriptor() const`

**作用与语义：**

返回服务器用来监听指令的本地套接字描述符，如果服务器未监听，则返回-1。
如果服务器使用 `QNetworkProxy`，返回的描述符可能无法与本地套接字函数一起使用。

### `bool QTcpServer::waitForNewConnection(int msec = 0, bool *timedOut = nullptr)`

**作用与语义：**

最多等待`msec`毫秒，或直到有来电连接。如果有连接，返回`true`;否则返回`false`。如果超时且`timedOut`未`nullptr`，*`timedOut`将设置为true。
这是一个阻塞函数调用。在单线程的 GUI 应用中不建议使用它，因为整个应用程序会停止响应，直到函数返回。waitForNewConnection() 主要用于无事件循环时。
非阻断的替代方案是连接到`newConnection()`信号。
如果 msec 为 -1，该函数不会超时。

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

`QTcpServer` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
