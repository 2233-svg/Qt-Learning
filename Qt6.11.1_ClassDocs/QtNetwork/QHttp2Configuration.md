# QHttp2Configuration

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QHttp2Configuration` 是 Qt Network 的“Http2Configuration”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QHttp2Configuration` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QHttp2Configuration>`
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
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QHttp2Configuration()`
- `QHttp2Configuration(const QHttp2Configuration &other)`
- `QHttp2Configuration(QHttp2Configuration &&other)`
- `~QHttp2Configuration()`
- `bool huffmanCompressionEnabled() const`
- `(since 6.9) unsigned int maxConcurrentStreams() const`
- `unsigned int maxFrameSize() const`
- `bool serverPushEnabled() const`
- `unsigned int sessionReceiveWindowSize() const`
- `void setHuffmanCompressionEnabled(bool enable)`
- `(since 6.9) void setMaxConcurrentStreams(unsigned int value)`
- `bool setMaxFrameSize(unsigned int size)`
- `void setServerPushEnabled(bool enable)`
- `bool setSessionReceiveWindowSize(unsigned int size)`
- `bool setStreamReceiveWindowSize(unsigned int size)`
- `unsigned int streamReceiveWindowSize() const`
- `void swap(QHttp2Configuration &other)`
- `QHttp2Configuration & operator=(QHttp2Configuration &&other)`
- `QHttp2Configuration & operator=(const QHttp2Configuration &other)`

### 相关非成员函数

- `bool operator!=(const QHttp2Configuration &lhs, const QHttp2Configuration &rhs)`
- `bool operator==(const QHttp2Configuration &lhs, const QHttp2Configuration &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QHttp2Configuration::QHttp2Configuration()`

**作用与语义：**

默认构建一个 QHttp2Configuration 对象。
这种配置具有以下数值：
- 服务器推送被禁用
- 启用Huffman字符串压缩
- 连接级流量控制窗口大小为65535个八位字节
- 溪流水位流量控制窗口大小为65535八位字节
- 帧大小为16384个八位元组

### `QHttp2Configuration::QHttp2Configuration(const QHttp2Configuration &other)`

**作用与语义：**

复制构造此QHttp2配置。

### `[noexcept] QHttp2Configuration::QHttp2Configuration(QHttp2Configuration &&other)`

**作用与语义：**

从`other`移动构造出该QHttp2配置。

### `[noexcept] QHttp2Configuration::~QHttp2Configuration()`

**作用与语义：**

毁灭者。

### `bool QHttp2Configuration::huffmanCompressionEnabled() const`

**作用与语义：**

如果启用了 HPACK 中的 Huffman 编码，返回`true`。

### `[since 6.9] unsigned int QHttp2Configuration::maxConcurrentStreams() const`

**作用与语义：**

返回最大并发流数。

### `unsigned int QHttp2Configuration::maxFrameSize() const`

**作用与语义：**

返回HTTP/2帧的最大有效载荷大小。默认（初始）值为16384个八位元组。

### `bool QHttp2Configuration::serverPushEnabled() const`

**作用与语义：**

如果启用了服务器推送，则返回true。
注意：默认情况下，`QNetworkAccessManager`会通过“设置”帧禁用服务器推送。

### `unsigned int QHttp2Configuration::sessionReceiveWindowSize() const`

**作用与语义：**

返回连接级流控制的窗口大小。`QNetworkAccessManager`默认值为2147483647八位元组。

### `void QHttp2Configuration::setHuffmanCompressionEnabled(bool enable)`

**作用与语义：**

如果`enable` `true`，HPACK压缩还会额外使用Huffman编码压缩字符串。默认启用。
注意：该参数只影响`QNetworkAccessManager`发送的“HEADERS”帧。

### `[since 6.9] void QHttp2Configuration::setMaxConcurrentStreams(unsigned int value)`

**作用与语义：**

设置`value`为发送SETTINGS帧时将向对等端宣布的最大并发流数。

### `bool QHttp2Configuration::setMaxFrameSize(unsigned int size)`

**作用与语义：**

设置 `QNetworkAccessManager` 发送初始 SETTINGS 帧时将向服务器通告的最大帧大小。
注意：虽然该`size`要求在16384至16777215含范围内，但实际载荷帧的有效载荷大小可能小于16384。
成功时`true`有回报，`false`其他情况。

### `void QHttp2Configuration::setServerPushEnabled(bool enable)`

**作用与语义：**

如果`enable` `true`，远程服务器可能会提前使用服务器推送发送响应。

### `bool QHttp2Configuration::setSessionReceiveWindowSize(unsigned int size)`

**作用与语义：**

设置连接级流量控制的窗口大小。`size`不能为0，且不得超过2147483647个八位元组。
成功时`true`退货，`false`其他情况。

### `bool QHttp2Configuration::setStreamReceiveWindowSize(unsigned int size)`

**作用与语义：**

设置溪流流量控制的窗口大小。`size`不能为0，且不得超过2147483647个八位元组。
成功时回报`true`，`false`其他情况。

### `unsigned int QHttp2Configuration::streamReceiveWindowSize() const`

**作用与语义：**

返回流级流量控制的窗口大小。默认值为`QNetworkAccessManager` 214748364字节（参见RFC 7540）。

### `[noexcept] void QHttp2Configuration::swap(QHttp2Configuration &other)`

**作用与语义：**

将该配置与`other`交换。此操作非常快速且从未出错。

### `[noexcept] QHttp2Configuration &QHttp2Configuration::operator=(QHttp2Configuration &&other)`

**作用与语义：**

Move-Assign `other`到这个`QHttp2Configuration`。

### `QHttp2Configuration &QHttp2Configuration::operator=(const QHttp2Configuration &other)`

**作用与语义：**

将`other`分配到该`QHttp2Configuration`。

### `[noexcept] bool operator!=(const QHttp2Configuration &lhs, const QHttp2Configuration &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 没有相同的 HTTP/2 参数集，则返回 `true`。

### `[noexcept] bool operator==(const QHttp2Configuration &lhs, const QHttp2Configuration &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 拥有相同的 HTTP/2 参数集合，则返回 `true`。

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

`QHttp2Configuration` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
