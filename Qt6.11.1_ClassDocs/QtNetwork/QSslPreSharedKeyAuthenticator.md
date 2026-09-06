# QSslPreSharedKeyAuthenticator

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QSslPreSharedKeyAuthenticator` 是 Qt Network 的“SslPreShared键认证器”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QSslPreSharedKeyAuthenticator` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QSslPreSharedKeyAuthenticator>`
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

- `QSslPreSharedKeyAuthenticator()`
- `QSslPreSharedKeyAuthenticator(const QSslPreSharedKeyAuthenticator &authenticator)`
- `~QSslPreSharedKeyAuthenticator()`
- `QByteArray identity() const`
- `QByteArray identityHint() const`
- `int maximumIdentityLength() const`
- `int maximumPreSharedKeyLength() const`
- `QByteArray preSharedKey() const`
- `void setIdentity(const QByteArray &identity)`
- `void setPreSharedKey(const QByteArray &preSharedKey)`
- `void swap(QSslPreSharedKeyAuthenticator &other)`
- `QSslPreSharedKeyAuthenticator & operator=(QSslPreSharedKeyAuthenticator &&authenticator)`
- `QSslPreSharedKeyAuthenticator & operator=(const QSslPreSharedKeyAuthenticator &authenticator)`

### 相关非成员函数

- `bool operator!=(const QSslPreSharedKeyAuthenticator &lhs, const QSslPreSharedKeyAuthenticator &rhs)`
- `bool operator==(const QSslPreSharedKeyAuthenticator &lhs, const QSslPreSharedKeyAuthenticator &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QSslPreSharedKeyAuthenticator::QSslPreSharedKeyAuthenticator()`

**作用与语义：**

构建一个默认的QSslPreSharedKeyAuthenticator对象。
身份提示、身份和密钥将初始化为空字节数组;身份和密钥的最大长度将初始化为0。

### `QSslPreSharedKeyAuthenticator::QSslPreSharedKeyAuthenticator(const QSslPreSharedKeyAuthenticator &authenticator)`

**作用与语义：**

构建一个 QSslPreSharedKeyAuthenticator 对象，作为 `authenticator` 的副本。

### `[noexcept] QSslPreSharedKeyAuthenticator::~QSslPreSharedKeyAuthenticator()`

**作用与语义：**

摧毁`QSslPreSharedKeyAuthenticator`物体。

### `QByteArray QSslPreSharedKeyAuthenticator::identity() const`

**作用与语义：**

返回PSK客户端身份。

### `QByteArray QSslPreSharedKeyAuthenticator::identityHint() const`

**作用与语义：**

返回服务器提供的PSK身份提示。该提示的解释由应用程序自行决定。

### `int QSslPreSharedKeyAuthenticator::maximumIdentityLength() const`

**作用与语义：**

返回PSK客户端身份的最大长度（字节）。
注意：可以设置长度大于 maximumIdentityLength();在这种情况下，只有第一个 maximumIdentityLength() 字节会被发送到服务器。

### `int QSslPreSharedKeyAuthenticator::maximumPreSharedKeyLength() const`

**作用与语义：**

返回预共享密钥的最大长度（字节单位）。
注意：可以设置长度大于最大PreSharedKeyLength();此时，只有第一个最大PreSharedKeyLength()字节实际发送给服务器。

### `QByteArray QSslPreSharedKeyAuthenticator::preSharedKey() const`

**作用与语义：**

返回预共享密钥。

### `void QSslPreSharedKeyAuthenticator::setIdentity(const QByteArray &identity)`

**作用与语义：**

将 PSK 客户端身份（以通知服务器）设置为 `identity`。
注意：可以设置长度大于`maximumIdentityLength()`的身份;在这种情况下，只有前`maximumIdentityLength()`字节会实际发送给服务器。

### `void QSslPreSharedKeyAuthenticator::setPreSharedKey(const QByteArray &preSharedKey)`

**作用与语义：**

将预共享密钥设置为`preSharedKey`。
注意：可以设置长度大于`maximumPreSharedKeyLength()`的键;在这种情况下，实际上只有前`maximumPreSharedKeyLength()`字节会发送到服务器。

### `[noexcept] void QSslPreSharedKeyAuthenticator::swap(QSslPreSharedKeyAuthenticator &other)`

**作用与语义：**

将这个身份验证器与`other`交换。这个操作非常快，从未出错。

### `[noexcept] QSslPreSharedKeyAuthenticator &QSslPreSharedKeyAuthenticator::operator=(QSslPreSharedKeyAuthenticator &&authenticator)`

**作用与语义：**

Move将`QSslPreSharedKeyAuthenticator`对象`authenticator`赋值到该对象，并返回对移动实例的引用。

### `QSslPreSharedKeyAuthenticator &QSslPreSharedKeyAuthenticator::operator=(const QSslPreSharedKeyAuthenticator &authenticator)`

**作用与语义：**

将`QSslPreSharedKeyAuthenticator`对象 `authenticator` 分配给该对象，并返回对该副本的引用。

### `bool operator!=(const QSslPreSharedKeyAuthenticator &lhs, const QSslPreSharedKeyAuthenticator &rhs)`

**作用与语义：**

如果认证器对象`lhs`不等于`rhs`，返回`true`;否则`false`。

### `bool operator==(const QSslPreSharedKeyAuthenticator &lhs, const QSslPreSharedKeyAuthenticator &rhs)`

**作用与语义：**

如果认证器对象`lhs`等于`rhs`，则返回`true`;否则`false`。
两个认证对象当且仅当它们具有相同的身份提示、身份、预共享密钥、身份的最大长度和预共享密钥的最大长度时，才是相等的。

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

`QSslPreSharedKeyAuthenticator` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
