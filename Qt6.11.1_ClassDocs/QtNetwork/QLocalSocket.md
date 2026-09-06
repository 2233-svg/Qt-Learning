# QLocalSocket

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QLocalSocket` 是 Qt Network 的“Local套接字”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QLocalSocket` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QLocalSocket>`
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

创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum LocalSocketError { ConnectionRefusedError, PeerClosedError, ServerNotFoundError, SocketAccessError, SocketResourceError, …, UnknownSocketError }`
- `enum LocalSocketState { UnconnectedState, ConnectingState, ConnectedState, ClosingState }`
- `(since 6.2) enum SocketOption { NoOptions, AbstractNamespaceOption }`
- `flags SocketOptions`

### 属性

- `(since 6.2) socketOptions : SocketOptions`

### 公有函数

- `QLocalSocket(QObject *parent = nullptr)`
- `virtual ~QLocalSocket()`
- `void abort()`
- `QBindable<QLocalSocket::SocketOptions> bindableSocketOptions()`
- `void connectToServer(QIODeviceBase::OpenMode openMode = ReadWrite)`
- `void connectToServer(const QString &name, QIODeviceBase::OpenMode openMode = ReadWrite)`
- `void disconnectFromServer()`
- `QLocalSocket::LocalSocketError error() const`
- `bool flush()`
- `QString fullServerName() const`
- `bool isValid() const`
- `qint64 readBufferSize() const`
- `QString serverName() const`
- `void setReadBufferSize(qint64 size)`
- `void setServerName(const QString &name)`
- `bool setSocketDescriptor(qintptr socketDescriptor, QLocalSocket::LocalSocketState socketState = ConnectedState, QIODeviceBase::OpenMode openMode = ReadWrite)`
- `void setSocketOptions(QLocalSocket::SocketOptions option)`
- `qintptr socketDescriptor() const`
- `QLocalSocket::SocketOptions socketOptions() const`
- `QLocalSocket::LocalSocketState state() const`
- `bool waitForConnected(int msecs = 30000)`
- `bool waitForDisconnected(int msecs = 30000)`

### 重实现的公有函数

- `virtual qint64 bytesAvailable() const override`
- `virtual qint64 bytesToWrite() const override`
- `virtual bool canReadLine() const override`
- `virtual void close() override`
- `virtual bool isSequential() const override`
- `virtual bool open(QIODeviceBase::OpenMode openMode = ReadWrite) override`
- `virtual bool waitForBytesWritten(int msecs = 30000) override`
- `virtual bool waitForReadyRead(int msecs = 30000) override`

### 信号

- `void connected()`
- `void disconnected()`
- `void errorOccurred(QLocalSocket::LocalSocketError socketError)`
- `void stateChanged(QLocalSocket::LocalSocketState socketState)`

### 重实现的保护函数

- `virtual qint64 readData(char *data, qint64 c) override`
- `virtual qint64 readLineData(char *data, qint64 maxSize) override`
- `virtual qint64 skipData(qint64 maxSize) override`
- `virtual qint64 writeData(const char *data, qint64 c) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QLocalSocket::LocalSocketError`

**作用与语义：**

LocalServerError枚举表示可能发生的错误。最近的错误可以通过调用`QLocalSocket::error()`检索。
- `QLocalSocket::ConnectionRefusedError`：`QAbstractSocket::ConnectionRefusedError`;连接被对等端拒绝（或超时）。
- `QLocalSocket::PeerClosedError`：`QAbstractSocket::RemoteHostClosedError`;远程套接字关闭了连接。注意，客户端套接字（即该套接字）在发送远程关闭通知后会关闭。
- `QLocalSocket::ServerNotFoundError`：`QAbstractSocket::HostNotFoundError`;未找到本地套接字名称。
- `QLocalSocket::SocketAccessError`：`QAbstractSocket::SocketAccessError`;套接字操作失败，因为应用程序缺乏所需的权限。
- `QLocalSocket::SocketResourceError`：`QAbstractSocket::SocketResourceError`;本地系统资源耗尽（例如套接字过多）。
- `QLocalSocket::SocketTimeoutError`：`QAbstractSocket::SocketTimeoutError`;套筒操作超时。
- `QLocalSocket::DatagramTooLargeError`：`QAbstractSocket::DatagramTooLargeError`;数据报大于操作系统的限制（最低可达8192字节）。
- `QLocalSocket::ConnectionError`：`QAbstractSocket::NetworkError`;连接发生错误。
- `QLocalSocket::UnsupportedSocketOperationError`：`QAbstractSocket::UnsupportedSocketOperationError`;请求的套接字操作不被本地操作系统支持。
- `QLocalSocket::OperationError`：`QAbstractSocket::OperationError`;在套筒处于不允许操作的状态下尝试操作。
- `QLocalSocket::UnknownSocketError`：`QAbstractSocket::UnknownSocketError`;发生了未识别错误。

### `enum QLocalSocket::LocalSocketState`

**作用与语义：**

该枚举描述了套筒可能处于的不同状态。
- `QLocalSocket::UnconnectedState`：`QAbstractSocket::UnconnectedState`;套接字未连接。
- `QLocalSocket::ConnectingState`：`QAbstractSocket::ConnectingState`;套接字已开始建立连接。
- `QLocalSocket::ConnectedState`：`QAbstractSocket::ConnectedState`;建立联系。
- `QLocalSocket::ClosingState`：`QAbstractSocket::ClosingState`;套接字即将关闭（数据可能仍在等待写入）。

### `[since 6.2] enum QLocalSocket::SocketOptionflags QLocalSocket::SocketOptions`

**作用与语义：**

本枚举描述了可用于连接服务器的可能选项。目前，在Linux和Android上，它用于指定连接到绑定抽象地址的套接字的服务器。
- `QLocalSocket::NoOptions`：`0x00`;尚未设置任何选项。
- `QLocalSocket::AbstractNamespaceOption`：`0x01`;套接字会尝试连接到一个抽象地址。该标志仅限于Linux和Android。在其他平台上则被忽略。
这个枚举是在Qt 6.2引入的。
SocketOptions 类型是 QFlags 的 typedef<SocketOption>。它存储 SocketOption 值的 OR 组合。

### `[bindable, since 6.2] socketOptions : SocketOptions`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含套筒选项。
选项必须在套接字处于`UnconnectedState`状态时设置。

**如何使用：** 调用 `socketOptions()` 读取当前值；它不会修改应用状态。

### `QLocalSocket::QLocalSocket(QObject *parent = nullptr)`

**作用与语义：**

创建一个新的本地套接字。`parent`参数传递给`QObject`的构造函数。

### `[virtual noexcept] QLocalSocket::~QLocalSocket()`

**作用与语义：**

摧毁套接字，必要时关闭连接。

### `void QLocalSocket::abort()`

**作用与语义：**

中止当前连接并重置套接字。与`disconnectFromServer()`不同，该函数会立即关闭套接字，清除写入缓冲区中的任何待处理数据。

### `[override virtual] qint64 QLocalSocket::bytesAvailable() const`

**作用与语义：**

重装：`QIODevice::bytesAvailable()` const.

### `[override virtual] qint64 QLocalSocket::bytesToWrite() const`

**作用与语义：**

重装：`QIODevice::bytesToWrite()` const.

### `[override virtual] bool QLocalSocket::canReadLine() const`

**作用与语义：**

重装：`QIODevice::canReadLine()` const.

### `[override virtual] void QLocalSocket::close()`

**作用与语义：**

重装：`QIODevice::close()`。
关闭套接字的I/O设备，并调用`disconnectFromServer()`关闭套接字连接。
请参见 `QIODevice::close()` 关于 I/O 设备关闭时发生的动作描述。

### `void QLocalSocket::connectToServer(QIODeviceBase::OpenMode openMode = ReadWrite)`

**作用与语义：**

尝试连接`serverName()`。必须在打开连接前调用`setServerName()`。或者你也可以使用 connectToServer（const `QString` &name， OpenMode openMode）;
套接字在给定的`openMode`中打开，首先进入`ConnectingState`。如果建立连接，`QLocalSocket`进入`ConnectedState`并发出`connected()`。
调用该函数后，套接字可以发出`errorOccurred()`来表示发生错误。

### `void QLocalSocket::connectToServer(const QString &name, QIODeviceBase::OpenMode openMode = ReadWrite)`

**作用与语义：**

设置服务器`name`并尝试连接它。
套接字在给定`openMode`中打开，首先进入`ConnectingState`。如果建立连接，`QLocalSocket`进入`ConnectedState`并发出`connected()`。
调用该函数后，套接字可以发出`errorOccurred()`来表示发生错误。

### `[signal] void QLocalSocket::connected()`

**作用与语义：**

该信号是在`connectToServer()`被调用并成功建立连接后发出的。

### `void QLocalSocket::disconnectFromServer()`

**作用与语义：**

尝试关闭套接字。如果有待写入的数据，`QLocalSocket`会进入`ClosingState`并等待所有数据写入。最终，它会进入`UnconnectedState`并发出`disconnected()`信号。

### `[signal] void QLocalSocket::disconnected()`

**作用与语义：**

当套接字断开时，该信号会发出。

### `QLocalSocket::LocalSocketError QLocalSocket::error() const`

**作用与语义：**

返回最后一次发生的错误类型。

### `[signal] void QLocalSocket::errorOccurred(QLocalSocket::LocalSocketError socketError)`

**作用与语义：**

该信号是在错误发生后发出的。`socketError`参数描述了发生的错误类型。
`QLocalSocket::LocalSocketError`不是注册元类型，所以对于队列中的连接，你需要用`Q_DECLARE_METATYPE()`和 `qRegisterMetaType()` 来注册。

### `bool QLocalSocket::flush()`

**作用与语义：**

该函数尽可能多地从内部写入缓冲区写入套接字，且不阻塞。如果写入了任何数据，该函数返回`true`;否则返回 false。
如果你需要`QLocalSocket`立即开始发送缓冲数据，可以调用该函数。成功写入的字节数取决于操作系统。在大多数情况下，你不需要调用这个函数，因为一旦控制返回事件循环，系统会自动开始发送数据`QLocalSocket`。如果没有事件循环，则调用`waitForBytesWritten()`。

### `QString QLocalSocket::fullServerName() const`

**作用与语义：**

返回该套接字连接的服务器路径。
注意：该函数的返回值是针对特定平台的。

### `[override virtual] bool QLocalSocket::isSequential() const`

**作用与语义：**

重装：`QIODevice::isSequential()` const.

### `bool QLocalSocket::isValid() const`

**作用与语义：**

如果套接字有效且准备好使用，返回`true`;否则返回`false`。
注意：套接字的状态必须`ConnectedState`才能进行读写。

### `[override virtual] bool QLocalSocket::open(QIODeviceBase::OpenMode openMode = ReadWrite)`

**作用与语义：**

重实现自：`QIODevice::open`（QIODeviceBase：：OpenMode 模式）。
相当于`connectToServer`（OpenMode 模式）。套接字在由 `setServerName()` 定义的服务器中以指定`openMode`开启。
注意，与大多数其他`QIODevice`子类不同，open() 不能直接打开设备。如果套接字已经连接，或者连接服务器未定义，则该函数返回 false，其他情况下为真。`connected()` 或 `errorOccurred()` 信号将在设备实际打开（或连接失败）时发出。
详情请参见`connectToServer()`。

### `qint64 QLocalSocket::readBufferSize() const`

**作用与语义：**

返回内部读取缓冲区的大小。这限制了客户端在调用`read()`或`readAll()`之前能接收的数据量。读取缓冲区大小为0（默认值）意味着缓冲区没有大小限制，确保不会丢失数据。

### `[override virtual protected] qint64 QLocalSocket::readData(char *data, qint64 c)`

**作用与语义：**

从本地套接字接收缓冲区复制最多 `c` 字节到 `data`，返回读取字节数，失败返回 -1。它由 `QIODevice::read()` 间接调用；应在 `readyRead()` 后读取，并处理断开和 `errorOccurred()`。

### `[override virtual protected] qint64 QLocalSocket::readLineData(char *data, qint64 maxSize)`

**作用与语义：**

重新实现：`QIODevice::readLineData`（char *data， qint64 maxSize）.

### `QString QLocalSocket::serverName() const`

**作用与语义：**

返回对等节点的名称，如`setServerName()`指定，若未调用或`setServerName()` `connectToServer()`失败，则返回空 `QString`。

### `void QLocalSocket::setReadBufferSize(qint64 size)`

**作用与语义：**

将`QLocalSocket`内部读取缓冲区的大小设置为`size`字节。
如果缓冲区大小受限于某个大小，`QLocalSocket`不会缓冲超过该大小的数据。例外情况下，缓冲区大小为0意味着读取缓冲区是无限的，所有入站数据都被缓冲。这是默认设置。
如果你只在特定时间点读取数据（例如在实时流媒体应用中），或者想保护套接字免受过多数据接收，避免最终导致内存不足，这个选项非常有用。

### `void QLocalSocket::setServerName(const QString &name)`

**作用与语义：**

设置连接节点的对`name`。在Windows上，名称是命名管道的名称;在Unix上，名称是本地域套接字的名称。
当套筒未连接时必须调用该函数。

### `bool QLocalSocket::setSocketDescriptor(qintptr socketDescriptor, QLocalSocket::LocalSocketState socketState = ConnectedState, QIODeviceBase::OpenMode openMode = ReadWrite)`

**作用与语义：**

用本地套接字描述符`socketDescriptor`初始化`QLocalSocket`。如果`socketDescriptor`被接受为有效的套接字描述符，返回`true`;否则返回`false`。套接字以`openMode`指定的模式打开，进入`socketState`指定的套接字状态。
注意：无法用相同的本地套接字描述符初始化两个本地套接字。

### `[override virtual protected] qint64 QLocalSocket::skipData(qint64 maxSize)`

**作用与语义：**

重装：`QIODevice::skipData`（qint64 maxSize）。

### `qintptr QLocalSocket::socketDescriptor() const`

**作用与语义：**

如果有本地套接字描述符，返回`QLocalSocket`对象的本地套接字描述符;否则返回 -1。
当`QLocalSocket`处于`UnconnectedState`时，套接字描述符不可用。描述符的类型取决于平台：
- 在Windows上，返回的值是Winsock 2的套接字句柄。
- 在INTEGRITY中，返回的值是`QTcpSocket`套接字描述符，类型由`socketDescriptor`定义。
- 在所有其他类 UNIX 操作系统中，类型是表示套接字的文件描述符。

### `QLocalSocket::LocalSocketState QLocalSocket::state() const`

**作用与语义：**

返回套筒的状态。

### `[signal] void QLocalSocket::stateChanged(QLocalSocket::LocalSocketState socketState)`

**作用与语义：**

每当`QLocalSocket`的状态发生变化时，该信号都会发出。`socketState`参数即为新状态。
QLocalSocket：：SocketState 不是注册元类型，因此对于排队连接，你需要用 `Q_DECLARE_METATYPE()` 和 `qRegisterMetaType()` 来注册。

### `[override virtual] bool QLocalSocket::waitForBytesWritten(int msecs = 30000)`

**作用与语义：**

重实现自：`QIODevice::waitForBytesWritten`（int msecs）。

### `bool QLocalSocket::waitForConnected(int msecs = 30000)`

**作用与语义：**

等待套接字连接，最多可达`msecs`毫秒。如果连接已建立，该函数返回`true`;否则返回`false`。如果返回`false`，你可以调用`error()`来确定错误原因。
以下示例等待最多一秒以建立连接：
如果`msecs`为-1，该函数不会超时。

**官方示例：**

```cpp
 socket->connectToServer("market");
 if (socket->waitForConnected(1000))
     qDebug("Connected!");
```

### `bool QLocalSocket::waitForDisconnected(int msecs = 30000)`

**作用与语义：**

等待套接字断开连接，最多可达`msecs`毫秒。如果连接成功断开，该函数返回`true`;否则返回`false`（如果操作超时、发生错误或该`QLocalSocket`已断开）。如果返回`false`，你可以调用`error()`来确定错误原因。
以下示例等待连接关闭最多一秒钟：
如果`msecs`为-1，该函数不会超时。

**官方示例：**

```cpp
 socket->disconnectFromServer();
 if (socket->state() == QLocalSocket::UnconnectedState
     || socket->waitForDisconnected(1000)) {
     qDebug("Disconnected!");
 }
```

### `[override virtual] bool QLocalSocket::waitForReadyRead(int msecs = 30000)`

**作用与语义：**

重实现自：`QIODevice::waitForReadyRead`（int msecs）。
该功能会阻塞，直到数据可用且`readyRead()`信号已发出。该函数在`msecs`毫秒后超时;默认超时为30000毫秒。
如果数据可用，函数返回`true`;否则返回`false`（如果发生错误或操作超时）。

### `[override virtual protected] qint64 QLocalSocket::writeData(const char *data, qint64 c)`

**作用与语义：**

把最多 `c` 字节加入本地套接字发送缓冲区，返回已接受字节数，失败返回 -1。数据可能稍后才写入系统；用 `bytesWritten()` 或在确有阻塞需要时用 `waitForBytesWritten()` 判断进度。

### `(since 6.2) enum SocketOption { NoOptions, AbstractNamespaceOption }`

**作用与语义：**

本枚举描述了可用于连接服务器的可能选项。目前，在Linux和Android上，它用于指定连接到绑定抽象地址的套接字的服务器。
- `QLocalSocket::NoOptions`：`0x00`;尚未设置任何选项。
- `QLocalSocket::AbstractNamespaceOption`：`0x01`;套接字会尝试连接到一个抽象地址。该标志仅限于Linux和Android。在其他平台上则被忽略。
这个枚举是在Qt 6.2引入的。
SocketOptions 类型是 QFlags 的 typedef<SocketOption>。它存储 SocketOption 值的 OR 组合。

### `flags SocketOptions`

**作用与语义：**

本枚举描述了可用于连接服务器的可能选项。目前，在Linux和Android上，它用于指定连接到绑定抽象地址的套接字的服务器。
- `QLocalSocket::NoOptions`：`0x00`;尚未设置任何选项。
- `QLocalSocket::AbstractNamespaceOption`：`0x01`;套接字会尝试连接到一个抽象地址。该标志仅限于Linux和Android。在其他平台上则被忽略。
这个枚举是在Qt 6.2引入的。
SocketOptions 类型是 QFlags 的 typedef<SocketOption>。它存储 SocketOption 值的 OR 组合。

### `QBindable<QLocalSocket::SocketOptions> bindableSocketOptions()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含套筒选项。
选项必须在套接字处于`UnconnectedState`状态时设置。

**如何使用：** 调用 `bindableSocketOptions()` 取得 `socketOptions` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `void setSocketOptions(QLocalSocket::SocketOptions option)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含套筒选项。
选项必须在套接字处于`UnconnectedState`状态时设置。

**如何使用：** 调用 `setSocketOptions(...)` 修改 `socketOptions`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QLocalSocket::SocketOptions socketOptions() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含套筒选项。
选项必须在套接字处于`UnconnectedState`状态时设置。

**如何使用：** 调用 `socketOptions()` 读取当前值；它不会修改应用状态。

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

`QLocalSocket` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
