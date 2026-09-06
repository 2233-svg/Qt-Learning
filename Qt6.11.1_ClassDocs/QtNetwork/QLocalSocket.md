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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 44 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QLocalSocket::LocalSocketError`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QLocalSocket` 暴露的类型声明 `Local、Socket、错误`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:LocalSocketError`。
- 属性名：`QLocalSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QLocalSocket::LocalSocketState`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QLocalSocket` 暴露的类型声明 `Local、Socket、State`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:LocalSocketState`。
- 属性名：`QLocalSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] enum QLocalSocket::SocketOptionflags QLocalSocket::SocketOptions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QLocalSocket` 暴露的类型声明 `Socket、Optionflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SocketOptionflags QLocalSocket::SocketOptions`。
- 属性名：`QLocalSocket`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable, since 6.2] socketOptions : SocketOptions`

**API 类别：** 属性说明

**中文解读：** 这是 `QLocalSocket` 的配置属性。初始化或状态切换时通过 `setSocketOptions(...)` 设置，之后用 `socketOptions()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`SocketOptions`。
- 属性名：`socketOptions`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QLocalSocket::QLocalSocket(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLocalSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QLocalSocket::~QLocalSocket()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLocalSocket` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLocalSocket::abort()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `abort`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] qint64 QLocalSocket::bytesAvailable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `bytesAvailable`，返回 `QLocalSocket` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] qint64 QLocalSocket::bytesToWrite() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `bytesToWrite`，返回 `QLocalSocket` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QLocalSocket::canReadLine() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canReadLine`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QLocalSocket::close()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `close`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLocalSocket::connectToServer(QIODeviceBase::OpenMode openMode = ReadWrite)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `connectToServer`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `openMode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。传入 `QIODeviceBase::OpenMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLocalSocket::connectToServer(const QString &name, QIODeviceBase::OpenMode openMode = ReadWrite)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `connectToServer`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `openMode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。传入 `QIODeviceBase::OpenMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QLocalSocket::connected()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLocalSocket` 发出的通知信号 `connected`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLocalSocket::disconnectFromServer()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `disconnectFromServer`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QLocalSocket::disconnected()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLocalSocket` 发出的通知信号 `disconnected`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QLocalSocket::LocalSocketError QLocalSocket::error() const`

**API 类别：** 成员函数说明

**中文解读：** `QLocalSocket::error` 用于计算、查询或取得与“错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QLocalSocket::LocalSocketError`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLocalSocket::LocalSocketError`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QLocalSocket::errorOccurred(QLocalSocket::LocalSocketError socketError)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLocalSocket` 发出的通知信号 `errorOccurred`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `socketError`：类型为 `QLocalSocket::LocalSocketError`。没有默认值，调用时必须提供。传入 `QLocalSocket::LocalSocketError` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QLocalSocket::flush()`

**API 类别：** 成员函数说明

**中文解读：** `QLocalSocket::flush` 用于计算、查询或取得与“刷新”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QLocalSocket::fullServerName() const`

**API 类别：** 成员函数说明

**中文解读：** `QLocalSocket::fullServerName` 用于计算、查询或取得与“full、Server、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QLocalSocket::isSequential() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSequential`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QLocalSocket::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QLocalSocket::open(QIODeviceBase::OpenMode openMode = ReadWrite)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `open`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `openMode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。传入 `QIODeviceBase::OpenMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QLocalSocket::readBufferSize() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLocalSocket` 的核心操作 `readBufferSize`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] qint64 QLocalSocket::readData(char *data, qint64 c)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLocalSocket` 的核心操作 `readData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `c`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] qint64 QLocalSocket::readLineData(char *data, qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLocalSocket` 的核心操作 `readLineData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QLocalSocket::serverName() const`

**API 类别：** 成员函数说明

**中文解读：** `QLocalSocket::serverName` 用于计算、查询或取得与“server、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLocalSocket::setReadBufferSize(qint64 size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setReadBufferSize`。调用它会改变 `QLocalSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qint64`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLocalSocket::setServerName(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setServerName`。调用它会改变 `QLocalSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QLocalSocket::setSocketDescriptor(qintptr socketDescriptor, QLocalSocket::LocalSocketState socketState = ConnectedState, QIODeviceBase::OpenMode openMode = ReadWrite)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSocketDescriptor`。调用它会改变 `QLocalSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `socketDescriptor`：类型为 `qintptr`。没有默认值，调用时必须提供。传入 `qintptr` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `socketState`：类型为 `QLocalSocket::LocalSocketState`。默认值为 `ConnectedState`。传入 `QLocalSocket::LocalSocketState` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `openMode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。传入 `QIODeviceBase::OpenMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] qint64 QLocalSocket::skipData(qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** `QLocalSocket::skipData` 用于计算、查询或取得与“skip、数据访问”相关的操作。调用时要先确认当前状态和 `maxSize` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qintptr QLocalSocket::socketDescriptor() const`

**API 类别：** 成员函数说明

**中文解读：** `QLocalSocket::socketDescriptor` 用于计算、查询或取得与“socket、Descriptor”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qintptr`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qintptr`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QLocalSocket::LocalSocketState QLocalSocket::state() const`

**API 类别：** 成员函数说明

**中文解读：** `QLocalSocket::state` 用于计算、查询或取得与“state”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QLocalSocket::LocalSocketState`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLocalSocket::LocalSocketState`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QLocalSocket::stateChanged(QLocalSocket::LocalSocketState socketState)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLocalSocket` 发出的通知信号 `stateChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `socketState`：类型为 `QLocalSocket::LocalSocketState`。没有默认值，调用时必须提供。传入 `QLocalSocket::LocalSocketState` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QLocalSocket::waitForBytesWritten(int msecs = 30000)`

**API 类别：** 成员函数说明

**中文解读：** `QLocalSocket::waitForBytesWritten` 用于计算、查询或取得与“等待、For、字节、Written”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。默认值为 `30000`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QLocalSocket::waitForConnected(int msecs = 30000)`

**API 类别：** 成员函数说明

**中文解读：** `QLocalSocket::waitForConnected` 用于计算、查询或取得与“等待、For、Connected”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。默认值为 `30000`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QLocalSocket::waitForDisconnected(int msecs = 30000)`

**API 类别：** 成员函数说明

**中文解读：** `QLocalSocket::waitForDisconnected` 用于计算、查询或取得与“等待、For、Disconnected”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。默认值为 `30000`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QLocalSocket::waitForReadyRead(int msecs = 30000)`

**API 类别：** 成员函数说明

**中文解读：** `QLocalSocket::waitForReadyRead` 用于计算、查询或取得与“等待、For、Ready、读取”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。默认值为 `30000`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] qint64 QLocalSocket::writeData(const char *data, qint64 c)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLocalSocket` 的核心操作 `writeData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `const char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `c`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.2) enum SocketOption { NoOptions, AbstractNamespaceOption }`

**API 类别：** 公有类型

**中文解读：** 这是 `QLocalSocket` 暴露的类型声明 `Socket、Option`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags SocketOptions`

**API 类别：** 公有类型

**中文解读：** 这是 `QLocalSocket` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<QLocalSocket::SocketOptions> bindableSocketOptions()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableSocketOptions`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<QLocalSocket::SocketOptions>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSocketOptions(QLocalSocket::SocketOptions option)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSocketOptions`。调用它会改变 `QLocalSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `option`：类型为 `QLocalSocket::SocketOptions`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QLocalSocket::SocketOptions socketOptions() const`

**API 类别：** 公有函数

**中文解读：** `QLocalSocket::socketOptions` 用于计算、查询或取得与“socket、Options”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QLocalSocket::SocketOptions`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLocalSocket::SocketOptions`。
- 参数：无。

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

`QLocalSocket` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
