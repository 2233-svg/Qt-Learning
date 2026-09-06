# QSctpServer

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QSctpServer` 是 Qt Network 的“Sctp服务器”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QSctpServer` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QSctpServer>`
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

- `QSctpServer(QObject *parent = nullptr)`
- `virtual ~QSctpServer()`
- `int maximumChannelCount() const`
- `QSctpSocket * nextPendingDatagramConnection()`
- `void setMaximumChannelCount(int count)`

### 重实现的保护函数

- `virtual void incomingConnection(qintptr socketDescriptor) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QSctpServer::QSctpServer(QObject *parent = nullptr)`

**作用与语义：**

构建一个QSctpServer对象。
设置数据报的操作模式。`parent`参数传递给`QObject`的构造函数。

### `[virtual noexcept] QSctpServer::~QSctpServer()`

**作用与语义：**

销毁`QSctpServer`对象。如果服务器监听连接，套接字会自动关闭。

### `[override virtual protected] void QSctpServer::incomingConnection(qintptr socketDescriptor)`

**作用与语义：**

重实现自：`QTcpServer::incomingConnection`（qintptr socketDescriptor）。
当有新的连接可用时，`QTcpServer`调用该虚拟函数。`socketDescriptor`参数是接受连接的本地套接字描述符。
基础实现创建`QTcpSocket`，设置套接字描述符，然后将`QTcpSocket`存储在待处理连接的内部列表中。最后`newConnection()`被输出。
重新实现该函数以改变连接可用时服务器的行为。
如果该服务器使用`QNetworkProxy`，那么该`socketDescriptor`可能无法与本地套接字函数一起使用，只能与`QTcpSocket::setSocketDescriptor()`一起使用。
注意：如果在该方法的重实现中创建了另一个套接字，需要通过调用`addPendingConnection()`将其添加到待处理连接机制中。
注意：如果你想将一个新连接作为另一个线程中的新 `QTcpSocket` 对象处理，你必须将`socketDescriptor`传递给另一个线程，在那里创建`QTcpSocket`对象并使用其`setSocketDescriptor()`方法。

### `int QSctpServer::maximumChannelCount() const`

**作用与语义：**

返回被接受套接字能够支持的最大通道数。
值为0（默认值）意味着连接通道数量由远程端点设定。
如果`QSctpServer`在 TCP 仿真模式下运行，返回 -1。

### `QSctpSocket *QSctpServer::nextPendingDatagramConnection()`

**作用与语义：**

返回下一个待处理的数据报模式连接，作为连接`QSctpSocket`对象。
数据报模式连接提供面向消息的多流通信。
套接字是作为服务器的子节点创建的，这意味着当`QSctpServer`对象被销毁时，它会自动被删除。不过，完成后显式删除该对象仍然是个好主意，以避免浪费内存。
如果没有待处理的数据报模式连接，该函数返回空。
注意：返回的`QSctpSocket`对象不能从其他线程使用。如果你想使用来自其他线程的输入连接，需要覆盖`incomingConnection()`。

### `void QSctpServer::setMaximumChannelCount(int count)`

**作用与语义：**

将服务器在数据报模式下支持的最大信道数设为`count`。如果`count`为0，则使用端点最大信道数值。负 `count` 设定TCP仿真模式。
只有当`QSctpServer`处于UnconnectedState时才调用此方法。

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

`QSctpServer` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
