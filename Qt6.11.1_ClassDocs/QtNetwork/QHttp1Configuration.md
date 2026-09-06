# QHttp1Configuration

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QHttp1Configuration` 是 Qt Network 的“Http1Configuration”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QHttp1Configuration` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QHttp1Configuration>`
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

- `QHttp1Configuration()`
- `QHttp1Configuration(const QHttp1Configuration &other)`
- `QHttp1Configuration(QHttp1Configuration &&other)`
- `~QHttp1Configuration()`
- `qsizetype numberOfConnectionsPerHost() const`
- `void setNumberOfConnectionsPerHost(qsizetype number)`
- `void swap(QHttp1Configuration &other)`
- `QHttp1Configuration & operator=(QHttp1Configuration &&other)`
- `QHttp1Configuration & operator=(const QHttp1Configuration &other)`

### 相关非成员函数

- `(since 6.5) size_t qHash(const QHttp1Configuration &key, size_t seed = 0)`
- `(since 6.5) bool operator!=(const QHttp1Configuration &lhs, const QHttp1Configuration &rhs)`
- `(since 6.5) bool operator==(const QHttp1Configuration &lhs, const QHttp1Configuration &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QHttp1Configuration::QHttp1Configuration()`

**作用与语义：**

默认情况下，构造一个 QHttp1Configuration 对象。

### `QHttp1Configuration::QHttp1Configuration(const QHttp1Configuration &other)`

**作用与语义：**

复制构造此 QHttp1Configuration。

### `[noexcept] QHttp1Configuration::QHttp1Configuration(QHttp1Configuration &&other)`

**作用与语义：**

从`other`中Move-构造出该QHttp1配置。
注意：移除对象`other`处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `[noexcept] QHttp1Configuration::~QHttp1Configuration()`

**作用与语义：**

毁灭者。

### `qsizetype QHttp1Configuration::numberOfConnectionsPerHost() const`

**作用与语义：**

返回每个 http（s） `host`：port 组合所用连接数。默认为六（6）。

### `void QHttp1Configuration::setNumberOfConnectionsPerHost(qsizetype number)`

**作用与语义：**

将每个 http host-port 组合所使用的连接数（最小：1，最大：255）设置为 `number`。
如果`number`≤0，则不做任何事。如果`number`>255，则使用255。

### `[noexcept] void QHttp1Configuration::swap(QHttp1Configuration &other)`

**作用与语义：**

将该HTTP/1配置与`other`交换。此操作非常快速且从未失败。

### `[noexcept] QHttp1Configuration &QHttp1Configuration::operator=(QHttp1Configuration &&other)`

**作用与语义：**

Move-Assign `other`到这个`QHttp1Configuration`。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `QHttp1Configuration &QHttp1Configuration::operator=(const QHttp1Configuration &other)`

**作用与语义：**

Copy-assign `other`到该`QHttp1Configuration`。

### `[noexcept, since 6.5] size_t qHash(const QHttp1Configuration &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept, since 6.5] bool operator!=(const QHttp1Configuration &lhs, const QHttp1Configuration &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 不表示相同的 HTTP/1 参数集，则返回 `true`。

### `[noexcept, since 6.5] bool operator==(const QHttp1Configuration &lhs, const QHttp1Configuration &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 表示相同的 HTTP/1 参数集合，则返回 `true`。

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

`QHttp1Configuration` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
