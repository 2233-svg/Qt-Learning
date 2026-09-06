# QLocalServer

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QLocalServer` 是 Qt Network 的“Local服务器”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QLocalServer` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QLocalServer>`
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

- `enum SocketOption { NoOptions, UserAccessOption, GroupAccessOption, OtherAccessOption, WorldAccessOption, AbstractNamespaceOption }`
- `flags SocketOptions`

### 属性

- `socketOptions : SocketOptions`

### 公有函数

- `QLocalServer(QObject *parent = nullptr)`
- `virtual ~QLocalServer()`
- `QBindable<QLocalServer::SocketOptions> bindableSocketOptions()`
- `void close()`
- `QString errorString() const`
- `QString fullServerName() const`
- `virtual bool hasPendingConnections() const`
- `bool isListening() const`
- `bool listen(const QString &name)`
- `bool listen(qintptr socketDescriptor)`
- `(since 6.3) int listenBacklogSize() const`
- `int maxPendingConnections() const`
- `virtual QLocalSocket * nextPendingConnection()`
- `QAbstractSocket::SocketError serverError() const`
- `QString serverName() const`
- `(since 6.3) void setListenBacklogSize(int size)`
- `void setMaxPendingConnections(int numConnections)`
- `void setSocketOptions(QLocalServer::SocketOptions options)`
- `qintptr socketDescriptor() const`
- `QLocalServer::SocketOptions socketOptions() const`
- `bool waitForNewConnection(int msec = 0, bool *timedOut = nullptr)`

### 信号

- `void newConnection()`

### 静态公有成员

- `bool removeServer(const QString &name)`

### 保护函数

- `(since 6.8) void addPendingConnection(QLocalSocket *socket)`
- `virtual void incomingConnection(quintptr socketDescriptor)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QLocalServer::SocketOptionflags QLocalServer::SocketOptions`

**作用与语义：**

本枚举描述了可用于创建套接字的可能选项。这改变了支持套接字访问权限的平台（Linux、Windows）上的访问权限。GroupAccess 和 OtherAccess 的含义可能因平台而略有不同。在 Linux 和 Android 上，可以使用抽象地址的套接字;对于此类套接字来说，套接字权限没有意义。
- `QLocalServer::NoOptions`：`0x0`;未设置访问限制。
- `QLocalServer::UserAccessOption`：`0x01`;访问仅限于创建该套接字的进程的同一用户。
- `QLocalServer::GroupAccessOption`：`0x2`;访问仅限于同一组，但不限于在 Linux 上创建该套接字的用户。在 Windows 上，访问仅限进程的主组
- `QLocalServer::OtherAccessOption`：`0x4`;在 Linux 上，除了创建该套接字的用户和组外，所有人都可以访问。在 Windows 上，所有人都可以访问。
- `QLocalServer::WorldAccessOption`：`0x7`;无访问限制。
- `QLocalServer::AbstractNamespaceOption`：`0x8`;监听套接字将在抽象命名空间中创建。该标志是Linux专用的。在其他平台，为了代码的可移植性，该标志等同于WorldAccessOption。
SocketOptions 类型是 QFlags 的 typedef<SocketOption>。它存储 SocketOption 值的 OR 组合。

### `[bindable] socketOptions : SocketOptions`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含控制套接字如何操作的套接字选项。
例如，套接字可能会限制用户ID可以连接到该套接字的权限。
这些选项必须在`listen()`被调用前设置好。
在某些情况下，比如Linux上的Unix域套接字，对该套接字的访问由文件系统权限决定，并基于umask创建。设置访问标志会覆盖该权限，并根据指定限制或允许访问。
其他基于 Unix 的操作系统，如 macOS，不承认 Unix 域套接字的文件权限，默认使用 WorldAccess，这些权限标志不会生效。
在 Windows 上，`UserAccessOption` 足以让非提升进程连接到由同一用户运行的提升进程创建的本地服务器。`GroupAccessOption` 指进程的主组（参见 Windows 文档中的 TokenPrimaryGroup）。`OtherAccessOption` 指的是著名的“Everyone”组。
在 Linux 平台上，可以在抽象命名空间中创建一个 socket，该命名空间与文件系统无关。使用这种 socket 意味着忽略权限选项。在其他平台上`AbstractNamespaceOption`相当于 `WorldAccessOption`。
默认情况下，任何标志都未被设置，访问权限是平台默认设置。

**如何使用：** 调用 `socketOptions()` 读取当前值；它不会修改应用状态。

### `[explicit] QLocalServer::QLocalServer(QObject *parent = nullptr)`

**作用与语义：**

创建一个新的本地套接字服务器，并使用给定的 `parent`。

### `[virtual noexcept] QLocalServer::~QLocalServer()`

**作用与语义：**

销毁`QLocalServer`对象。如果服务器正在监听连接，则会自动关闭连接。
任何仍然连接的客户端QLocalSocket必须断开连接或重新父级，然后服务器才会被删除。

### `[protected, since 6.8] void QLocalServer::addPendingConnection(QLocalSocket *socket)`

**作用与语义：**

`QLocalServer::incomingConnection()`调用该函数，将该`socket`添加到待处理的入站连接列表中。
注意：如果你不想破坏待处理连接机制，别忘了从重构`incomingConnection()`调用该成员。该函数在套接字添加后发出`newConnection()`信号。

### `void QLocalServer::close()`

**作用与语义：**

停止监听来电连接。现有连接不受影响，但任何新连接都会被拒绝。

### `QString QLocalServer::errorString() const`

**作用与语义：**

返回与当前`serverError()`报告错误相符的人类可读消息。如果没有合适的字符串可用，则返回一个空字符串。

### `QString QLocalServer::fullServerName() const`

**作用与语义：**

返回服务器监听的完整路径。
注意：这取决于特定平台。

### `[virtual] bool QLocalServer::hasPendingConnections() const`

**作用与语义：**

如果服务器有待处理连接，返回`true`;否则返回`false`。

### `[virtual protected] void QLocalServer::incomingConnection(quintptr socketDescriptor)`

**作用与语义：**

当有新连接可用时，`QLocalServer`调用该虚拟函数。`socketDescriptor` 是接受连接的本地套接字描述符。
基础实现创建`QLocalSocket`，设置套接字描述符，然后将`QLocalSocket`存储在待处理连接的内部列表中。最后`newConnection()`被发出。
重新实现该函数以改变连接可用时服务器的行为。

### `bool QLocalServer::isListening() const`

**作用与语义：**

如果服务器正在监听`true`连接，返回`false`。

### `bool QLocalServer::listen(const QString &name)`

**作用与语义：**

告诉服务器监听`name`的来电连接。如果服务器已经监听，listen() 将失败。成功时返回`true`，否则`false`。
`name`可以是一个单一名称，`QLocalServer`会确定正确的平台特定路径。`serverName()`会返回传入 listen() 的名称。
通常你会直接输入像“foo”这样的名称，但在Unix上，这也可以是路径，比如“/tmp/foo”，在Windows上也可以是管道路径，比如“\\.\pipe\foo”。
注意：在Unix上，如果服务器之前崩溃且未关闭，listen() 会导致 AddressInUseError 失败。要创建新服务器，应先移除该文件。在 Windows 上，两个本地服务器可以同时监听同一个管道，但每个入站连接都会指向其中任意一个。

### `bool QLocalServer::listen(qintptr socketDescriptor)`

**作用与语义：**

指示服务器监听`socketDescriptor`的入站连接。如果服务器当前监听，属性返回`false`。成功时返回`true`;否则返回`false`。套接字必须准备好接受新的连接，且不调用任何额外的平台特定函数。套接字设置为非阻塞模式。
`serverName()`，如果平台支持`fullServerName()`可以返回带有名称的字符串;否则返回空的`QString`。特别是，Linux 支持的抽象命名空间中的套接字地址如果包含不可打印字符，就不会生成有用的名称。

### `[since 6.3] int QLocalServer::listenBacklogSize() const`

**作用与语义：**

返回待接受连接的队列大小。

### `int QLocalServer::maxPendingConnections() const`

**作用与语义：**

返回最大待处理接受连接数。默认为30。

### `[signal] void QLocalServer::newConnection()`

**作用与语义：**

每当有新连接可用时，该信号都会发出。

### `[virtual] QLocalSocket *QLocalServer::nextPendingConnection()`

**作用与语义：**

返回下一个待处理连接，作为连接`QLocalSocket`对象。
套接字是作为服务器的子节点创建的，这意味着当`QLocalServer`对象被销毁时，它会自动被删除。使用完毕后明确删除该对象仍然是个好主意，以避免浪费内存。
如果在没有待处理连接的情况下调用该函数，`nullptr`返回。

### `[static] bool QLocalServer::removeServer(const QString &name)`

**作用与语义：**

移除可能导致调用`listen()`失败的服务器实例，成功时返回`true`;否则返回`false`。该函数旨在从崩溃中恢复，前提是之前的服务器实例尚未清理。
在 Windows 上，这个函数没有作用;在 Unix 上，它会移除 `name` 给出的套接字文件。
警告：请谨慎避免移除运行实例的套接字。

### `QAbstractSocket::SocketError QLocalServer::serverError() const`

**作用与语义：**

返回上次或`NoError`次发生的错误类型。

### `QString QLocalServer::serverName() const`

**作用与语义：**

如果服务器正在监听连接，则返回服务器名称;否则返回 QString()。

### `[since 6.3] void QLocalServer::setListenBacklogSize(int size)`

**作用与语义：**

将待办队列大小设置为可接受的连接`size`。操作系统可能会减少或忽略该值。默认情况下，队列大小为50。
注意：该属性必须在调用`listen()`之前设置。

### `void QLocalServer::setMaxPendingConnections(int numConnections)`

**作用与语义：**

将待接受连接的最大数量设置为`numConnections`。`QLocalServer`在调用`nextPendingConnection()`前最多只接受`numConnections`个入站连接。
注意：尽管`QLocalServer`在达到最大待处理连接数后停止接受新连接，操作系统仍可能将其留在队列中，导致客户端发出已连接信号。

### `qintptr QLocalServer::socketDescriptor() const`

**作用与语义：**

返回服务器用来监听指令的本地套接字描述符，如果服务器未监听，则返回-1。
描述符的类型取决于平台：
- 在Windows上，返回的值是Winsock 2的套接字句柄。
- 在INTEGRITY中，返回的值是`QTcpServer`套接字描述符，类型由`socketDescriptor`定义。
- 在所有其他类 UNIX 操作系统中，类型是表示监听套接字的文件描述符。

### `QLocalServer::SocketOptions QLocalServer::socketOptions() const`

**作用与语义：**

返回套筒上的套筒选项设置。
注意：属性socketOptions的Getter函数。

### `bool QLocalServer::waitForNewConnection(int msec = 0, bool *timedOut = nullptr)`

**作用与语义：**

最多等待`msec`毫秒，或直到有来电连接可用。如果有连接可用，返回`true`;否则返回`false`。如果操作超时且`timedOut`未`nullptr`，*timedOut 将设置为 true。
这是一个阻塞函数调用。在单线程的 GUI 应用中不建议使用它，因为整个应用程序会停止响应，直到函数返回。waitForNewConnection() 主要在没有事件循环时非常有用。
非阻断的替代方案是连接到`newConnection()`信号。
如果 msec 为 -1，该函数不会超时。

### `enum SocketOption { NoOptions, UserAccessOption, GroupAccessOption, OtherAccessOption, WorldAccessOption, AbstractNamespaceOption }`

**作用与语义：**

本枚举描述了可用于创建套接字的可能选项。这改变了支持套接字访问权限的平台（Linux、Windows）上的访问权限。GroupAccess 和 OtherAccess 的含义可能因平台而略有不同。在 Linux 和 Android 上，可以使用抽象地址的套接字;对于此类套接字来说，套接字权限没有意义。
- `QLocalServer::NoOptions`：`0x0`;未设置访问限制。
- `QLocalServer::UserAccessOption`：`0x01`;访问仅限于创建该套接字的进程的同一用户。
- `QLocalServer::GroupAccessOption`：`0x2`;访问仅限于同一组，但不限于在 Linux 上创建该套接字的用户。在 Windows 上，访问仅限进程的主组
- `QLocalServer::OtherAccessOption`：`0x4`;在 Linux 上，除了创建该套接字的用户和组外，所有人都可以访问。在 Windows 上，所有人都可以访问。
- `QLocalServer::WorldAccessOption`：`0x7`;无访问限制。
- `QLocalServer::AbstractNamespaceOption`：`0x8`;监听套接字将在抽象命名空间中创建。该标志是Linux专用的。在其他平台，为了代码的可移植性，该标志等同于WorldAccessOption。
SocketOptions 类型是 QFlags 的 typedef<SocketOption>。它存储 SocketOption 值的 OR 组合。

### `flags SocketOptions`

**作用与语义：**

本枚举描述了可用于创建套接字的可能选项。这改变了支持套接字访问权限的平台（Linux、Windows）上的访问权限。GroupAccess 和 OtherAccess 的含义可能因平台而略有不同。在 Linux 和 Android 上，可以使用抽象地址的套接字;对于此类套接字来说，套接字权限没有意义。
- `QLocalServer::NoOptions`：`0x0`;未设置访问限制。
- `QLocalServer::UserAccessOption`：`0x01`;访问仅限于创建该套接字的进程的同一用户。
- `QLocalServer::GroupAccessOption`：`0x2`;访问仅限于同一组，但不限于在 Linux 上创建该套接字的用户。在 Windows 上，访问仅限进程的主组
- `QLocalServer::OtherAccessOption`：`0x4`;在 Linux 上，除了创建该套接字的用户和组外，所有人都可以访问。在 Windows 上，所有人都可以访问。
- `QLocalServer::WorldAccessOption`：`0x7`;无访问限制。
- `QLocalServer::AbstractNamespaceOption`：`0x8`;监听套接字将在抽象命名空间中创建。该标志是Linux专用的。在其他平台，为了代码的可移植性，该标志等同于WorldAccessOption。
SocketOptions 类型是 QFlags 的 typedef<SocketOption>。它存储 SocketOption 值的 OR 组合。

### `QBindable<QLocalServer::SocketOptions> bindableSocketOptions()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含控制套接字如何操作的套接字选项。
例如，套接字可能会限制用户ID可以连接到该套接字的权限。
这些选项必须在`listen()`被调用前设置好。
在某些情况下，比如Linux上的Unix域套接字，对该套接字的访问由文件系统权限决定，并基于umask创建。设置访问标志会覆盖该权限，并根据指定限制或允许访问。
其他基于 Unix 的操作系统，如 macOS，不承认 Unix 域套接字的文件权限，默认使用 WorldAccess，这些权限标志不会生效。
在 Windows 上，`UserAccessOption` 足以让非提升进程连接到由同一用户运行的提升进程创建的本地服务器。`GroupAccessOption` 指进程的主组（参见 Windows 文档中的 TokenPrimaryGroup）。`OtherAccessOption` 指的是著名的“Everyone”组。
在 Linux 平台上，可以在抽象命名空间中创建一个 socket，该命名空间与文件系统无关。使用这种 socket 意味着忽略权限选项。在其他平台上`AbstractNamespaceOption`相当于 `WorldAccessOption`。
默认情况下，任何标志都未被设置，访问权限是平台默认设置。

**如何使用：** 调用 `bindableSocketOptions()` 取得 `socketOptions` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `void setSocketOptions(QLocalServer::SocketOptions options)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含控制套接字如何操作的套接字选项。
例如，套接字可能会限制用户ID可以连接到该套接字的权限。
这些选项必须在`listen()`被调用前设置好。
在某些情况下，比如Linux上的Unix域套接字，对该套接字的访问由文件系统权限决定，并基于umask创建。设置访问标志会覆盖该权限，并根据指定限制或允许访问。
其他基于 Unix 的操作系统，如 macOS，不承认 Unix 域套接字的文件权限，默认使用 WorldAccess，这些权限标志不会生效。
在 Windows 上，`UserAccessOption` 足以让非提升进程连接到由同一用户运行的提升进程创建的本地服务器。`GroupAccessOption` 指进程的主组（参见 Windows 文档中的 TokenPrimaryGroup）。`OtherAccessOption` 指的是著名的“Everyone”组。
在 Linux 平台上，可以在抽象命名空间中创建一个 socket，该命名空间与文件系统无关。使用这种 socket 意味着忽略权限选项。在其他平台上`AbstractNamespaceOption`相当于 `WorldAccessOption`。
默认情况下，任何标志都未被设置，访问权限是平台默认设置。

**如何使用：** 调用 `setSocketOptions(...)` 修改 `socketOptions`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QLocalServer` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
