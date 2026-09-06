# QNetworkDatagram

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkDatagram` 是 Qt Network 的“网络Datagram”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkDatagram` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkDatagram>`
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

- `QNetworkDatagram()`
- `QNetworkDatagram(const QByteArray &data, const QHostAddress &destinationAddress = QHostAddress(), quint16 port = 0)`
- `QNetworkDatagram(const QNetworkDatagram &other)`
- `void clear()`
- `QByteArray data() const`
- `QHostAddress destinationAddress() const`
- `int destinationPort() const`
- `int hopLimit() const`
- `uint interfaceIndex() const`
- `bool isNull() const`
- `bool isValid() const`
- `QNetworkDatagram makeReply(const QByteArray &payload) &&`
- `QNetworkDatagram makeReply(const QByteArray &payload) const &`
- `QHostAddress senderAddress() const`
- `int senderPort() const`
- `void setData(const QByteArray &data)`
- `void setDestination(const QHostAddress &address, quint16 port)`
- `void setHopLimit(int count)`
- `void setInterfaceIndex(uint index)`
- `void setSender(const QHostAddress &address, quint16 port = 0)`
- `void swap(QNetworkDatagram &other)`
- `QNetworkDatagram & operator=(const QNetworkDatagram &other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QNetworkDatagram::QNetworkDatagram()`

**作用与语义：**

创建一个无有效载荷数据且目标地址未定义的QNetworkDatagram对象。
有效载荷可以通过使用 `setData()` 进行修改，目的地址也可以用 `setDestination()` 设置。
如果目标地址未定义，`QUdpSocket::writeDatagram()`会尝试通过 `QUdpSocket::connectToHost()` 向最后关联的地址发送数据报。

### `QNetworkDatagram::QNetworkDatagram(const QByteArray &data, const QHostAddress &destinationAddress = QHostAddress(), quint16 port = 0)`

**作用与语义：**

创建 QNetworkDatagram 对象，并将 `data` 设置为有效载荷数据，同时将 `destinationAddress` 和 `port` 作为数据报的目的地地址。

### `QNetworkDatagram::QNetworkDatagram(const QNetworkDatagram &other)`

**作用与语义：**

创建`other`数据报的副本，包括有效载荷和元数据。
要创建适合发送回复的数据报，请使用`QNetworkDatagram::makeReply()`;

### `void QNetworkDatagram::clear()`

**作用与语义：**

清除该`QNetworkDatagram`对象中的有效载荷数据和元数据，将它们重置为默认值。

### `QByteArray QNetworkDatagram::data() const`

**作用与语义：**

返回该数据报的数据有效载荷。对于从网络接收的数据报，它包含该数据报的有效载荷。对于输出数据报，则是要发送的数据报。
注意，数据报可以传输时没有数据，因此返回的`QByteArray`可能是空的。

### `QHostAddress QNetworkDatagram::destinationAddress() const`

**作用与语义：**

返回与该数据报关联的目的地址。对于从网络接收到的数据报，它是对等节点发送数据报的地址，可以是该机器的本地地址，也可以是多播或广播地址。对于外发数据报，它应发送到的数据报地址。
如果该数据报未设置目标地址，返回的对象将报告为`QHostAddress::isNull()`。

### `int QNetworkDatagram::destinationPort() const`

**作用与语义：**

返回与该数据报关联的目的地端口号。对于从网络接收的数据报，它是对等节点发送数据报的本地端口号。对于外发数据报，则是数据报应发送到的对等端口。
如果该数据报没有关联目标地址，该函数返回 -1。

### `int QNetworkDatagram::hopLimit() const`

**作用与语义：**

返回与该数据报相关的跳数限制。跳数限制是指在数据报过期前允许转发该IP数据包的节点数量，并向数据报发送方发送错误。在IPv4中，这个值通常被称为“存活时间”（TTL）。
如果该数据报是从网络接收到的，则是接收后剩余的数据报跳数，每个转发该数据包的节点都会减少1。值为-1表示跳数限制计数未被获取。
如果这是一个发出数据报，发送时应在IP头中设置这个值。值为-1表示操作系统应选择该值。

### `uint QNetworkDatagram::interfaceIndex() const`

**作用与语义：**

返回该数据报关联的接口索引。接口索引是一个正数，唯一标识操作系统中的网络接口。该数字与`QNetworkInterface::index()`返回的接口值相匹配。
如果该数据报是从网络接收的，则是数据包接收接口的索引。如果是输出数据报，则是数据报应发送接口的索引。
值为0表示接口索引未知。

### `bool QNetworkDatagram::isNull() const`

**作用与语义：**

如果该`QNetworkDatagram`对象为空，则返回真。该函数与`isValid()`相反。

### `bool QNetworkDatagram::isValid() const`

**作用与语义：**

如果该`QNetworkDatagram`对象有效，则返回为真。有效的`QNetworkDatagram`对象至少包含一个发送方或接收方地址。有效的数据报可以包含空有效载荷。

### `QNetworkDatagram QNetworkDatagram::makeReply(const QByteArray &payload) &&`

**作用与语义：**

创建一个新`QNetworkDatagram`表示对该入站数据报的回复，并将有效载荷数据设置为`payload`。该函数是将数据报返回给原始发送方的非常方便的方式。
该函数特别方便，因为它会自动将该数据报的参数复制到新的数据报：
- 该数据报的发送地址和端口被复制到新数据报的目的地址和端口;
- 该数据报的接口索引（如有）被复制到新数据报的接口索引;
- 只有当该地址是IPv6全局（非组播）地址时，该数据报的目的地址和端口才会被复制到新数据报的发送地址和端口;
- 新数据报的跳数限制被重置为默认值（-1）;
如果`QNetworkDatagram`在未来的Qt版本中被修改以携带更多元数据，该函数会根据需要复制该元数据。
如果该数据报是IPv4地址，其目的地址不会被复制，因为在不对分配给该机器的所有地址进行详尽搜索的情况下，无法区分IPv4广播地址与普通IPv4地址。尝试发送发送方地址等于广播地址的数据报很可能会失败。不过这不会影响通信，因为拥有多个IPv4地址的网络接口较少见，因此操作系统选择的地址很可能是对等端能够理解的。
注意：该函数包含rvalue和lvalue引用的限定符重载，因此在调用`makeReply`前最好确保该对象是r值，以便更好地利用移动语义。为实现这一点，上述示例将使用：

**官方示例：**

```cpp
     void Server::readPendingDatagrams()
     {
         while (udpSocket->hasPendingDatagrams()) {
             QNetworkDatagram datagram = udpSocket->receiveDatagram();
             QByteArray replyData = processThePayload(datagram.data());
             udpSocket->writeDatagram(datagram.makeReply(replyData));
         }
     }
```

### `QHostAddress QNetworkDatagram::senderAddress() const`

**作用与语义：**

返回与该数据报关联的发送地址。对于从网络接收的数据报，它是发送数据报的对等节点的地址。对于发出数据报，它是发送时要使用的本地地址。
如果该数据报未设置发送地址，返回对象将报告为真`QHostAddress::isNull()`。

### `int QNetworkDatagram::senderPort() const`

**作用与语义：**

返回与该数据报关联的发送方端口号。对于从网络接收的数据报，它是对等节点发送数据报的端口号。对于输出数据报，则是数据报应从的本地端口。
如果该数据报没有关联发送地址，该函数返回 -1。

### `void QNetworkDatagram::setData(const QByteArray &data)`

**作用与语义：**

将该数据报的数据有效载荷设置为`data`。通常不需要对接收到的数据报调用此函数。对于输出数据报，该函数将数据设置为发送到网络中。
由于数据报可以空，空`QByteArray`是`data`的有效值。

### `void QNetworkDatagram::setDestination(const QHostAddress &address, quint16 port)`

**作用与语义：**

将与该数据报关联的目的地址设置为地址`address`和端口号`port`。目标地址和端口号通常由`QUdpSocket`在接收时设置，因此无需在接收到的数据报上调用此功能。
对于外发数据报，该函数可用于设置数据报应发送的地址。它可以是用于与对等方通信的单播地址，也可以是发送给一组设备的广播或多播地址。

### `void QNetworkDatagram::setHopLimit(int count)`

**作用与语义：**

将该数据报关联的跳数限制设置为`count`。跳数限制是指在数据包到期前允许转发该IP数据包的节点数量，且错误信息返回给数据报发送方。在IPv4中，该值通常称为“存活时间”（TTL）。
通常不需要对从网络接收到的数据报调用此功能。
如果这是一个发出的数据包，发送时应在IP头部设置这个值。该值的有效范围是1到255。该函数也接受-1的值，表示操作系统应选择该值。

### `void QNetworkDatagram::setInterfaceIndex(uint index)`

**作用与语义：**

将该数据报关联的接口索引设置为`index`。接口索引是一个正数，唯一标识操作系统中的网络接口。该数字与`QNetworkInterface::index()`返回的接口值相匹配。
通常不需要对从网络接收到的数据报调用此功能。
如果这是一个发出的数据包，则该数据报应通过接口的索引。值为0表示操作系统应根据其他因素选择接口。
注意，接口索引也可以用`QHostAddress::setScopeId()`设置IPv6目的地址，然后再用`setDestination()`设置。如果目的地址和`index`设置的范围ID不同且都不是零，操作系统将通过哪个接口发送数据报则未定义。

### `void QNetworkDatagram::setSender(const QHostAddress &address, quint16 port = 0)`

**作用与语义：**

将与该数据报关联的发送地址设置为地址`address`和端口号`port`。发送方地址和端口号通常由`QUdpSocket`在接收时设置，因此无需在接收数据报时调用此功能。
对于外出数据报，该函数可用于设置数据报应携带的地址。地址`address`通常必须是分配给该机器的本地地址之一，可以通过`QNetworkInterface`获得。如果未设置，操作系统会根据目标选择最合适的地址。
端口号 `port` 必须是与套接字关联的端口号（如果存在的话）。0 的值可以用来表示操作系统应选择端口号。

### `[noexcept] void QNetworkDatagram::swap(QNetworkDatagram &other)`

**作用与语义：**

将该数据报与`other`交换。该操作非常快且从未失败。

### `QNetworkDatagram &QNetworkDatagram::operator=(const QNetworkDatagram &other)`

**作用与语义：**

复制`other`数据报，包括有效载荷和元数据。
要创建适合发送回复的数据报，请使用 `QNetworkDatagram::makeReply()`;

### `QNetworkDatagram makeReply(const QByteArray &payload) const &`

**作用与语义：**

创建一个新`QNetworkDatagram`表示对该入站数据报的回复，并将有效载荷数据设置为`payload`。该函数是将数据报返回给原始发送方的非常方便的方式。
该函数特别方便，因为它会自动将该数据报的参数复制到新的数据报：
- 该数据报的发送地址和端口被复制到新数据报的目的地址和端口;
- 该数据报的接口索引（如有）被复制到新数据报的接口索引;
- 只有当该地址是IPv6全局（非组播）地址时，该数据报的目的地址和端口才会被复制到新数据报的发送地址和端口;
- 新数据报的跳数限制被重置为默认值（-1）;
如果`QNetworkDatagram`在未来的Qt版本中被修改以携带更多元数据，该函数会根据需要复制该元数据。
如果该数据报是IPv4地址，其目的地址不会被复制，因为在不对分配给该机器的所有地址进行详尽搜索的情况下，无法区分IPv4广播地址与普通IPv4地址。尝试发送发送方地址等于广播地址的数据报很可能会失败。不过这不会影响通信，因为拥有多个IPv4地址的网络接口较少见，因此操作系统选择的地址很可能是对等端能够理解的。
注意：该函数包含rvalue和lvalue引用的限定符重载，因此在调用`makeReply`前最好确保该对象是r值，以便更好地利用移动语义。为实现这一点，上述示例将使用：

**官方示例：**

```cpp
     void Server::readPendingDatagrams()
     {
         while (udpSocket->hasPendingDatagrams()) {
             QNetworkDatagram datagram = udpSocket->receiveDatagram();
             QByteArray replyData = processThePayload(datagram.data());
             udpSocket->writeDatagram(datagram.makeReply(replyData));
         }
     }
```

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

`QNetworkDatagram` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
