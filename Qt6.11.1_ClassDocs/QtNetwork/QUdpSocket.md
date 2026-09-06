# QUdpSocket

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** UDP 套接字，负责无连接数据报的绑定、发送和接收。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QUdpSocket`：UDP 套接字，负责无连接数据报的绑定、发送和接收。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QUdpSocket>`
- 继承自：QAbstractSocket
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

创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

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

### 公有函数

- `QUdpSocket(QObject *parent = nullptr)`
- `virtual ~QUdpSocket()`
- `bool hasPendingDatagrams() const`
- `bool joinMulticastGroup(const QHostAddress &groupAddress)`
- `bool joinMulticastGroup(const QHostAddress &groupAddress, const QNetworkInterface &iface)`
- `bool leaveMulticastGroup(const QHostAddress &groupAddress)`
- `bool leaveMulticastGroup(const QHostAddress &groupAddress, const QNetworkInterface &iface)`
- `QNetworkInterface multicastInterface() const`
- `qint64 pendingDatagramSize() const`
- `qint64 readDatagram(char *data, qint64 maxSize, QHostAddress *address = nullptr, quint16 *port = nullptr)`
- `QNetworkDatagram receiveDatagram(qint64 maxSize = -1)`
- `void setMulticastInterface(const QNetworkInterface &iface)`
- `qint64 writeDatagram(const char *data, qint64 size, const QHostAddress &address, quint16 port)`
- `qint64 writeDatagram(const QNetworkDatagram &datagram)`
- `qint64 writeDatagram(const QByteArray &datagram, const QHostAddress &host, quint16 port)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 15 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[explicit] QUdpSocket::QUdpSocket(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QUdpSocket` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QUdpSocket::~QUdpSocket()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QUdpSocket` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QUdpSocket::hasPendingDatagrams() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasPendingDatagrams`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QUdpSocket::joinMulticastGroup(const QHostAddress &groupAddress)`

**API 类别：** 成员函数说明

**中文解读：** `QUdpSocket::joinMulticastGroup` 用于计算、查询或取得与“join、Multicast、Group”相关的操作。调用时要先确认当前状态和 `groupAddress` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `groupAddress`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QUdpSocket::joinMulticastGroup(const QHostAddress &groupAddress, const QNetworkInterface &iface)`

**API 类别：** 成员函数说明

**中文解读：** `QUdpSocket::joinMulticastGroup` 用于计算、查询或取得与“join、Multicast、Group”相关的操作。调用时要先确认当前状态和 `groupAddress`、`iface` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `groupAddress`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `iface`：类型为 `const QNetworkInterface &`。没有默认值，调用时必须提供。传入 `const QNetworkInterface &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QUdpSocket::leaveMulticastGroup(const QHostAddress &groupAddress)`

**API 类别：** 成员函数说明

**中文解读：** `QUdpSocket::leaveMulticastGroup` 用于计算、查询或取得与“leave、Multicast、Group”相关的操作。调用时要先确认当前状态和 `groupAddress` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `groupAddress`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QUdpSocket::leaveMulticastGroup(const QHostAddress &groupAddress, const QNetworkInterface &iface)`

**API 类别：** 成员函数说明

**中文解读：** `QUdpSocket::leaveMulticastGroup` 用于计算、查询或取得与“leave、Multicast、Group”相关的操作。调用时要先确认当前状态和 `groupAddress`、`iface` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `groupAddress`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `iface`：类型为 `const QNetworkInterface &`。没有默认值，调用时必须提供。传入 `const QNetworkInterface &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkInterface QUdpSocket::multicastInterface() const`

**API 类别：** 成员函数说明

**中文解读：** `QUdpSocket::multicastInterface` 用于计算、查询或取得与“multicast、Interface”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkInterface`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkInterface`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QUdpSocket::pendingDatagramSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QUdpSocket::pendingDatagramSize` 用于计算、查询或取得与“pending、Datagram、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QUdpSocket::readDatagram(char *data, qint64 maxSize, QHostAddress *address = nullptr, quint16 *port = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QUdpSocket` 的核心操作 `readDatagram`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `address`：类型为 `QHostAddress *`。默认值为 `nullptr`。传入 `QHostAddress *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `port`：类型为 `quint16 *`。默认值为 `nullptr`。传入 `quint16 *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkDatagram QUdpSocket::receiveDatagram(qint64 maxSize = -1)`

**API 类别：** 成员函数说明

**中文解读：** `QUdpSocket::receiveDatagram` 用于计算、查询或取得与“receive、Datagram”相关的操作。调用时要先确认当前状态和 `maxSize` 的有效范围；返回类型是 `QNetworkDatagram`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkDatagram`。
- 参数 `maxSize`：类型为 `qint64`。默认值为 `-1`。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QUdpSocket::setMulticastInterface(const QNetworkInterface &iface)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMulticastInterface`。调用它会改变 `QUdpSocket` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `iface`：类型为 `const QNetworkInterface &`。没有默认值，调用时必须提供。传入 `const QNetworkInterface &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QUdpSocket::writeDatagram(const char *data, qint64 size, const QHostAddress &address, quint16 port)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QUdpSocket` 的核心操作 `writeDatagram`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `const char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `size`：类型为 `qint64`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `address`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `port`：类型为 `quint16`。没有默认值，调用时必须提供。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QUdpSocket::writeDatagram(const QNetworkDatagram &datagram)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QUdpSocket` 的核心操作 `writeDatagram`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `datagram`：类型为 `const QNetworkDatagram &`。没有默认值，调用时必须提供。传入 `const QNetworkDatagram &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QUdpSocket::writeDatagram(const QByteArray &datagram, const QHostAddress &host, quint16 port)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QUdpSocket` 的核心操作 `writeDatagram`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `datagram`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `host`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `port`：类型为 `quint16`。没有默认值，调用时必须提供。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QUdpSocket` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
