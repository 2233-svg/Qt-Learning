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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QUdpSocket::QUdpSocket(QObject *parent = nullptr)`

**作用与语义：**

创建一个 QUdpSocket 对象。
`parent`传递给`QObject`构造者。

### `[virtual noexcept] QUdpSocket::~QUdpSocket()`

**作用与语义：**

摧毁套接字，必要时关闭连接。

### `bool QUdpSocket::hasPendingDatagrams() const`

**作用与语义：**

如果至少有一个数据报等待读取，返回`true`;否则返回`false`。

### `bool QUdpSocket::joinMulticastGroup(const QHostAddress &groupAddress)`

**作用与语义：**

在操作系统选择的默认接口上加入由`groupAddress`指定的组。套接字必须处于BoundState，否则会发生错误。
请注意，如果你试图加入 IPv4 组，你的套接字不能被绑定为 IPv6（或在双模式中使用 `QHostAddress::Any`）。你必须使用 `QHostAddress::AnyIPv4`。
如果成功，该函数返回`true`;否则返回`false`并相应设置套接字错误。
注意：并非所有操作系统都支持在没有选择接口的情况下加入IPv6组。请考虑在指定接口处使用超载功能。

### `bool QUdpSocket::joinMulticastGroup(const QHostAddress &groupAddress, const QNetworkInterface &iface)`

**作用与语义：**

加入接口`iface`上的组播组地址`groupAddress`。

### `bool QUdpSocket::leaveMulticastGroup(const QHostAddress &groupAddress)`

**作用与语义：**

保留由`groupAddress`指定的组播组，保留操作系统选择的默认接口。套接字必须处于BoundState，否则会发生错误。
该函数如果成功，返回`true`;否则返回`false`并相应设置套接字错误。
注意：该函数应使用与传递给`joinMulticastGroup()`相同的参数调用。

### `bool QUdpSocket::leaveMulticastGroup(const QHostAddress &groupAddress, const QNetworkInterface &iface)`

**作用与语义：**

离开接口`iface` `groupAddress`指定的组播组。
注意：该函数应使用传递给`joinMulticastGroup()`相同的参数。

### `QNetworkInterface QUdpSocket::multicastInterface() const`

**作用与语义：**

返回多播数据报的出接口接口。这对应IPv4套接字的IP_MULTICAST_IF套接字选项和IPv6套接字的套接字IPV6_MULTICAST_IF选项。如果之前未设置过接口，该函数返回无效`QNetworkInterface`。套接字必须处于BoundState，否则返回无效`QNetworkInterface`。

### `qint64 QUdpSocket::pendingDatagramSize() const`

**作用与语义：**

返回第一个待处理的UDP数据报大小。如果没有可用的数据报，该函数返回-1。

### `qint64 QUdpSocket::readDatagram(char *data, qint64 maxSize, QHostAddress *address = nullptr, quint16 *port = nullptr)`

**作用与语义：**

接收不超过`maxSize`字节的数据报并存储在`data`中。发送方的主机地址和端口存储在*`address`和*`port`（除非指针`nullptr`）。
成功时返回数据报大小;否则返回-1。
如果`maxSize`太小，剩余数据报将丢失。为避免数据丢失，先调用`pendingDatagramSize()`确定待处理数据报的大小，然后再尝试读取。如果`maxSize`为0，数据报将被丢弃。

### `QNetworkDatagram QUdpSocket::receiveDatagram(qint64 maxSize = -1)`

**作用与语义：**

接收不超过`maxSize`字节的数据报，并在`QNetworkDatagram`对象中返回，同时发送方的主机地址和端口。如果可能，该函数还会尝试确定数据报的目的地址、端口以及接收时的跳数。
失败时，返回一个报告无效的`QNetworkDatagram`。
如果`maxSize`太小，剩余数据报将丢失。如果`maxSize`为0，数据报将被丢弃。如果`maxSize`为-1（默认值），该函数将尝试读取整个数据报。

### `void QUdpSocket::setMulticastInterface(const QNetworkInterface &iface)`

**作用与语义：**

将多播数据报的输出接口设置为接口`iface`。这对应于IPv4套接字的IP_MULTICAST_IF套接字选项和IPv6套接字的IPV6_MULTICAST_IF套接字选项。套接字必须处于BoundState，否则该函数无效。

### `qint64 QUdpSocket::writeDatagram(const char *data, qint64 size, const QHostAddress &address, quint16 port)`

**作用与语义：**

将大小为`size`的数据`data`报发送到主机地址`address`端口`port`。成功时返回发送的字节数;否则返回-1。
数据报总是写成一个块。数据报的最大大小高度依赖于平台，但最低可达8192字节。如果数据报过大，该函数返回-1，`error()`返回DatagramTooLargeError。
通常不建议发送超过512字节的数据报，因为即使成功发送，也很可能在到达最终目的地前被IP层分段。
警告：在连接的 UDP 套接字上调用此函数可能导致错误且无法发送数据包。如果你使用连接的套接字，请使用 `write()` 发送数据报。

### `qint64 QUdpSocket::writeDatagram(const QNetworkDatagram &datagram)`

**作用与语义：**

利用网络接口和跳数限制，将数据报发送`datagram`到`datagram`中的主机地址和端口号。如果目标地址和端口号未设置，该功能会发送到已传递给`connectToHost()`的地址。
如果目的地址是IPv6，且作用域ID非空，但`datagram`中与接口索引不同，操作系统将选择发送哪种接口是未定义的。
函数如果成功返回发送的字节数，遇到错误则返回-1字节数。
警告：在连接的 UDP 套接字上调用该函数可能导致错误且无法发送数据包。如果您使用连接套接字，请使用 `write()` 发送数据报。

### `qint64 QUdpSocket::writeDatagram(const QByteArray &datagram, const QHostAddress &host, quint16 port)`

**作用与语义：**

将数据报发送到主机地址`host`和端口`port` `datagram`。
函数如果成功返回发送的字节数，遇到错误则返回-1字节数。

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
