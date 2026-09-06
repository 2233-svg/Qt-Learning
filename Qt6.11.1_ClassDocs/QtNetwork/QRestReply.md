# QRestReply

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QRestReply` 是 Qt Network 的“Rest响应”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QRestReply` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QRestReply>`
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

- `QRestReply(QNetworkReply *reply)`
- `QRestReply(QRestReply &&other)`
- `~QRestReply()`
- `QNetworkReply::NetworkError error() const`
- `QString errorString() const`
- `bool hasError() const`
- `int httpStatus() const`
- `bool isHttpStatusSuccess() const`
- `bool isSuccess() const`
- `QNetworkReply * networkReply() const`
- `QByteArray readBody()`
- `std::optional<QJsonDocument> readJson(QJsonParseError *error = nullptr)`
- `QString readText()`
- `QRestReply & operator=(QRestReply &&other)`

### 相关非成员函数

- `QDebug operator<<(QDebug debug, const QRestReply &reply)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QRestReply::QRestReply(QNetworkReply *reply)`

**作用与语义：**

创建QRestReply，并将包裹后的`QNetworkReply`初始化为`reply`。

### `[noexcept] QRestReply::QRestReply(QRestReply &&other)`

**作用与语义：**

从`other`中构造出回答。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `[noexcept] QRestReply::~QRestReply()`

**作用与语义：**

摧毁了这个`QRestReply`物体。

### `QNetworkReply::NetworkError QRestReply::error() const`

**作用与语义：**

返回最后一个错误（如有）。错误包括网络和协议错误，但不包括服务器成功响应HTTP状态的情况。

### `QString QRestReply::errorString() const`

**作用与语义：**

返回一个人类可读的网络错误描述。

### `bool QRestReply::hasError() const`

**作用与语义：**

返回是否发生了错误。这包括网络和协议错误等错误，但排除服务器成功响应HTTP错误状态的情况（例如，`500 Internal Server Error`）。使用`httpStatus()`或`isHttpStatusSuccess()`获取HTTP状态信息。

### `int QRestReply::httpStatus() const`

**作用与语义：**

返回服务器响应中收到的HTTP状态。如果不可用（状态行尚未收到），值为0。
注意：HTTP 状态的报告是根据收到的 HTTP 响应来表示的。在收到状态后，可能会发生`error()`，例如在收到长响应时网络断开。这些可能的后续错误并未通过报告的 HTTP 状态来表示。

### `bool QRestReply::isHttpStatusSuccess() const`

**作用与语义：**

返回HTTP状态是否介于200至299之间。

### `bool QRestReply::isSuccess() const`

**作用与语义：**

返回HTTP状态是否在200至299之间，且接收响应时是否发生其他错误（例如接收正体数据时突然断开连接）。该函数是检查响应是否被视为成功的便捷方式。

### `QNetworkReply *QRestReply::networkReply() const`

**作用与语义：**

返回指向被该对象包裹的底层`QNetworkReply`的指针。

### `QByteArray QRestReply::readBody()`

**作用与语义：**

返回接收到的数据作为`QByteArray`。
调用该函数会消耗目前接收到的数据，任何进一步的响应调用都会返回空，直到接收到更多数据。

### `std::optional<QJsonDocument> QRestReply::readJson(QJsonParseError *error = nullptr)`

**作用与语义：**

返回接收到的数据作为`QJsonDocument`。
返回的值会被`std::optional`包裹。如果从接收到的数据转换失败（空数据或 JSON 解析错误），`std::nullopt`返回，`error` 填充详细信息。
调用该函数会消耗接收到的数据，任何进一步的响应数据调用都会返回空。
该函数返回`std::nullopt`，如果回复未完成，不会消耗任何数据。如果 `error` 被通过，则设置为 `QJsonParseError::NoError`，以区分此情况与实际错误。

### `QString QRestReply::readText()`

**作用与语义：**

返回接收到的数据作为`QString`。
接收到的数据会被解码成`QString`（UTF-16）。如果有，解码会使用Content-Type头部的字符集参数来确定源编码。如果`QStringConverter`无法获得或不支持编码信息，默认使用UTF-8。
调用该函数会消耗目前接收到的数据。如果没有新数据可用，或者`QStringConverter`不支持译码，或者译码有错误（例如字符无效），则返回默认构造值。

### `[noexcept] QRestReply &QRestReply::operator=(QRestReply &&other)`

**作用与语义：**

Move-assign `other`并返回该回复的引用。
注意：移除对象`other`处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `QDebug operator<<(QDebug debug, const QRestReply &reply)`

**作用与语义：**

将`reply`写入`debug`对象以供调试。

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

`QRestReply` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
