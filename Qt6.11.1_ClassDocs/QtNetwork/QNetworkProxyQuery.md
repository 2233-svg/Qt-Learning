# QNetworkProxyQuery

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkProxyQuery` 是 Qt Network 的“网络代理查询”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkProxyQuery` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkProxyQuery>`
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

### 公有类型

- `enum QueryType { TcpSocket, UdpSocket, SctpSocket, TcpServer, UrlRequest, SctpServer }`

### 公有函数

- `QNetworkProxyQuery()`
- `QNetworkProxyQuery(const QUrl &requestUrl, QNetworkProxyQuery::QueryType queryType = UrlRequest)`
- `QNetworkProxyQuery(quint16 bindPort, const QString &protocolTag = QString(), QNetworkProxyQuery::QueryType queryType = TcpServer)`
- `QNetworkProxyQuery(const QString &hostname, int port, const QString &protocolTag = QString(), QNetworkProxyQuery::QueryType queryType = TcpSocket)`
- `QNetworkProxyQuery(const QNetworkProxyQuery &other)`
- `~QNetworkProxyQuery()`
- `int localPort() const`
- `QString peerHostName() const`
- `int peerPort() const`
- `QString protocolTag() const`
- `QNetworkProxyQuery::QueryType queryType() const`
- `void setLocalPort(int port)`
- `void setPeerHostName(const QString &hostname)`
- `void setPeerPort(int port)`
- `void setProtocolTag(const QString &protocolTag)`
- `void setQueryType(QNetworkProxyQuery::QueryType type)`
- `void setUrl(const QUrl &url)`
- `void swap(QNetworkProxyQuery &other)`
- `QUrl url() const`
- `bool operator!=(const QNetworkProxyQuery &other) const`
- `QNetworkProxyQuery & operator=(const QNetworkProxyQuery &other)`
- `bool operator==(const QNetworkProxyQuery &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QNetworkProxyQuery::QueryType`

**作用与语义：**

描述一个`QNetworkProxyQuery`查询的类型。
- `QNetworkProxyQuery::TcpSocket`：`0`;一个普通的输出TCP套接字
- `QNetworkProxyQuery::UdpSocket`：`1`;基于数据报的UDP套接字，可发送至多个目的地
- `QNetworkProxyQuery::SctpSocket`：`2`;一个面向消息的外出SCTP套接字
- `QNetworkProxyQuery::TcpServer`：`100`;一个监听来自网络的 TCP 服务器
- `QNetworkProxyQuery::UrlRequest`：`101`;更复杂的请求，涉及加载一个URL。
- `QNetworkProxyQuery::SctpServer`：`102`;一个SCTP服务器，监听来自网络的连接

### `QNetworkProxyQuery::QNetworkProxyQuery()`

**作用与语义：**

构建一个默认的QNetworkProxyQuery对象。默认情况下，查询类型将为`QNetworkProxyQuery::TcpSocket`。

### `[explicit] QNetworkProxyQuery::QNetworkProxyQuery(const QUrl &requestUrl, QNetworkProxyQuery::QueryType queryType = UrlRequest)`

**作用与语义：**

构建一个带有 URL `requestUrl` 的 QNetworkProxyQuery，并将查询类型设置为 `queryType`。

### `[explicit] QNetworkProxyQuery::QNetworkProxyQuery(quint16 bindPort, const QString &protocolTag = QString(), QNetworkProxyQuery::QueryType queryType = TcpServer)`

**作用与语义：**

构造类型为 `queryType` 的 QNetworkProxyQuery，并将协议标签设置为`protocolTag`。该构造器适合`QNetworkProxyQuery::TcpSocket`查询，因为它将本地端口号设置为 `bindPort`。
注意，`bindPort`类型为quint16，以表示请求的确切端口号。在此上下文中不允许使用-1（未知）的值。

### `QNetworkProxyQuery::QNetworkProxyQuery(const QString &hostname, int port, const QString &protocolTag = QString(), QNetworkProxyQuery::QueryType queryType = TcpSocket)`

**作用与语义：**

构造类型为`queryType`的QNetworkProxyQuery，并将协议标签设置为`protocolTag`。该构造器适合查询`QNetworkProxyQuery::TcpSocket`，因为它将对等主机名设置为`hostname`，对等端的端口号为`port`。

### `QNetworkProxyQuery::QNetworkProxyQuery(const QNetworkProxyQuery &other)`

**作用与语义：**

构建一个QNetworkProxyQuery对象，该对象是`other`的副本。

### `[noexcept] QNetworkProxyQuery::~QNetworkProxyQuery()`

**作用与语义：**

摧毁了这个`QNetworkProxyQuery`物体。

### `int QNetworkProxyQuery::localPort() const`

**作用与语义：**

返回接收来自远程服务器的入站数据包的套接字端口号，如果端口未知则返回-1。

### `QString QNetworkProxyQuery::peerHostName() const`

**作用与语义：**

返回请求的外接连接的主机名或IP地址，如果远程主机名未知，则返回空字符串。
如果查询类型`QNetworkProxyQuery::UrlRequest`，该函数返回被请求URL的宿主组件。

### `int QNetworkProxyQuery::peerPort() const`

**作用与语义：**

返回发出请求的端口号，若端口号未知则返回-1。
如果查询类型为`QNetworkProxyQuery::UrlRequest`，该函数返回被请求URL的端口号。一般来说，框架会从默认值填充端口号。

### `QString QNetworkProxyQuery::protocolTag() const`

**作用与语义：**

返回该`QNetworkProxyQuery`对象的协议标签，若协议标签未知，则返回空 `QString`。
对于类型为`QNetworkProxyQuery::UrlRequest`的查询，该函数返回URL方案组件的值。

### `QNetworkProxyQuery::QueryType QNetworkProxyQuery::queryType() const`

**作用与语义：**

返回查询类型。

### `void QNetworkProxyQuery::setLocalPort(int port)`

**作用与语义：**

设置套接字希望本地使用的端口号，以便从远程服务器接收到`port`的进站数据包。本地端口最常用于`QNetworkProxyQuery::TcpServer`和`QNetworkProxyQuery::UdpSocket`查询类型。
有效值为0到65535（0表示任意端口号可接受）或-1，表示本地端口号未知或不适用。
在某些情况下，对于特殊协议，本地端口号也可以用于类型为`QNetworkProxyQuery::TcpSocket`的查询。当这种情况发生时，套接字表示它希望在连接远程主机时使用`port`端口号。

### `void QNetworkProxyQuery::setPeerHostName(const QString &hostname)`

**作用与语义：**

将请求的外接连接的主机名设置为`hostname`。空主机名可用来表示远程主机未知。
在`QNetworkProxyQuery::UdpSocket`或`QNetworkProxyQuery::TcpServer`查询类型情况下，对等主机名称也可用于指示输入连接的预期源地址。

### `void QNetworkProxyQuery::setPeerPort(int port)`

**作用与语义：**

将请求的输出连接端口号设置为`port`。有效值为1到65535，或表示远程端口号未知的-1。
对于`QNetworkProxyQuery::UdpSocket`或`QNetworkProxyQuery::TcpServer`查询类型，对等端口号也可用于表示预期的输入连接端口号。

### `void QNetworkProxyQuery::setProtocolTag(const QString &protocolTag)`

**作用与语义：**

将该`QNetworkProxyQuery`对象的协议标签设置为`protocolTag`。
协议标签是一个任意字符串，指示通过套接字通信的是哪个协议，如“http”、“xmpp”、“telnet”等。后端使用协议标签返回更针对该协议的请求：例如，HTTP连接可能使用缓存HTTP代理服务器，而其他连接则使用更强大的SOCKSv5代理服务器。

### `void QNetworkProxyQuery::setQueryType(QNetworkProxyQuery::QueryType type)`

**作用与语义：**

将该对象的查询类型设置为`type`。

### `void QNetworkProxyQuery::setUrl(const QUrl &url)`

**作用与语义：**

将该`QNetworkProxyQuery`对象的URL组件设置为`url`。设置URL还会设置协议标签、远程主机名和端口号。这样做是为了方便实现决定所用代理服务器的代码。

### `[noexcept] void QNetworkProxyQuery::swap(QNetworkProxyQuery &other)`

**作用与语义：**

将该网络代理查询实例与`other`交换。此操作非常快且从未失败。

### `QUrl QNetworkProxyQuery::url() const`

**作用与语义：**

在查询类型为`QNetworkProxyQuery::UrlRequest`时返回该`QNetworkProxyQuery`对象的URL组件。

### `bool QNetworkProxyQuery::operator!=(const QNetworkProxyQuery &other) const`

**作用与语义：**

如果该`QNetworkProxyQuery`对象不包含与`other`相同的数据，返回`true`。

### `QNetworkProxyQuery &QNetworkProxyQuery::operator=(const QNetworkProxyQuery &other)`

**作用与语义：**

复制`other`的内容。

### `bool QNetworkProxyQuery::operator==(const QNetworkProxyQuery &other) const`

**作用与语义：**

如果该`QNetworkProxyQuery`对象包含与`other`相同的数据，返回`true`。

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

`QNetworkProxyQuery` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
