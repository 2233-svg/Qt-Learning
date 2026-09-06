# QSslDiffieHellmanParameters

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QSslDiffieHellmanParameters` 是 Qt Network 的“SslDiffieHellmanParameters”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QSslDiffieHellmanParameters` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QSslDiffieHellmanParameters>`
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

### 公有类型

- `enum Error { NoError, InvalidInputDataError, UnsafeParametersError }`

### 公有函数

- `QSslDiffieHellmanParameters()`
- `QSslDiffieHellmanParameters(const QSslDiffieHellmanParameters &other)`
- `QSslDiffieHellmanParameters(QSslDiffieHellmanParameters &&other)`
- `~QSslDiffieHellmanParameters()`
- `QSslDiffieHellmanParameters::Error error() const`
- `QString errorString() const`
- `bool isEmpty() const`
- `bool isValid() const`
- `void swap(QSslDiffieHellmanParameters &other)`
- `QSslDiffieHellmanParameters & operator=(QSslDiffieHellmanParameters &&other)`
- `QSslDiffieHellmanParameters & operator=(const QSslDiffieHellmanParameters &other)`

### 静态公有成员

- `QSslDiffieHellmanParameters defaultParameters()`
- `QSslDiffieHellmanParameters fromEncoded(QIODevice *device, QSsl::EncodingFormat encoding = QSsl::Pem)`
- `QSslDiffieHellmanParameters fromEncoded(const QByteArray &encoded, QSsl::EncodingFormat encoding = QSsl::Pem)`

### 相关非成员函数

- `size_t qHash(const QSslDiffieHellmanParameters &key, size_t seed = 0)`
- `bool operator!=(const QSslDiffieHellmanParameters &lhs, const QSslDiffieHellmanParameters &rhs)`
- `QDebug operator<<(QDebug debug, const QSslDiffieHellmanParameters &dhparam)`
- `bool operator==(const QSslDiffieHellmanParameters &lhs, const QSslDiffieHellmanParameters &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSslDiffieHellmanParameters::Error`

**作用与语义：**

描述了一个`QSslDiffieHellmanParameters`错误。
- `QSslDiffieHellmanParameters::NoError`：`0`;未发生错误。
- `QSslDiffieHellmanParameters::InvalidInputDataError`：`1`;给定的输入数据无法用于构造`QSslDiffieHellmanParameters`对象。
- `QSslDiffieHellmanParameters::UnsafeParametersError`：`2`;Diffie-Hellman参数不安全，不应使用。

### `QSslDiffieHellmanParameters::QSslDiffieHellmanParameters()`

**作用与语义：**

构造一个空的 QSslDiffieHellmanParameters 实例。
如果在`QSslConfiguration`对象上设置空的QSslDiffieHellmanParameters实例，则Diffie-Hellman协商将被禁用。

### `QSslDiffieHellmanParameters::QSslDiffieHellmanParameters(const QSslDiffieHellmanParameters &other)`

**作用与语义：**

制造了一个与`other`一模一样的复制品。

### `[noexcept] QSslDiffieHellmanParameters::QSslDiffieHellmanParameters(QSslDiffieHellmanParameters &&other)`

**作用与语义：**

来自`other`的移动构造。
注意：移除对象`other`处于部分形成状态，唯一有效的操作是销毁和赋予新值。

### `[noexcept] QSslDiffieHellmanParameters::~QSslDiffieHellmanParameters()`

**作用与语义：**

摧毁`QSslDiffieHellmanParameters`物体。

### `[static] QSslDiffieHellmanParameters QSslDiffieHellmanParameters::defaultParameters()`

**作用与语义：**

返回`QSslSocket`使用的默认`QSslDiffieHellmanParameters`。
目前这是RFC 3526中的2048位MODP组。

### `[noexcept] QSslDiffieHellmanParameters::Error QSslDiffieHellmanParameters::error() const`

**作用与语义：**

返回导致`QSslDiffieHellmanParameters`对象无效的错误。

### `[noexcept] QString QSslDiffieHellmanParameters::errorString() const`

**作用与语义：**

返回导致`QSslDiffieHellmanParameters`对象无效的错误，以实现人类可读的描述。

### `[static] QSslDiffieHellmanParameters QSslDiffieHellmanParameters::fromEncoded(QIODevice *device, QSsl::EncodingFormat encoding = QSsl::Pem)`

**作用与语义：**

通过从`device`中读取PEM或DER形式，构造`QSslDiffieHellmanParameters`对象，`encoding`规定。
在返回的对象上使用`isValid()`方法检查Diffie-Hellman参数是否有效且加载正确。
特别地，如果`device` `nullptr`或未开放读取，将返回无效对象。

### `[static] QSslDiffieHellmanParameters QSslDiffieHellmanParameters::fromEncoded(const QByteArray &encoded, QSsl::EncodingFormat encoding = QSsl::Pem)`

**作用与语义：**

使用字节数组 `encoded` 构建一个`QSslDiffieHellmanParameters`对象，形式为 PEM 或 DER 格式，`encoding`规定。
对返回的对象使用`isValid()`方法检查Diffie-Hellman参数是否有效且加载正确。

### `[noexcept] bool QSslDiffieHellmanParameters::isEmpty() const`

**作用与语义：**

如果是空的`QSslDiffieHellmanParameters`实例，返回`true`。
在基于`QSslSocket`的服务器上设置空的`QSslDiffieHellmanParameters`实例会禁用Diffie-Hellman密钥交换。

### `[noexcept] bool QSslDiffieHellmanParameters::isValid() const`

**作用与语义：**

如果这是有效的`QSslDiffieHellmanParameters`，则返回`true`;否则为假。
该方法应在构造`QSslDiffieHellmanParameters`对象后使用以确定其有效性。
如果`QSslDiffieHellmanParameters`对象无效，你可以使用`error()`方法来确定导致该对象无法构建的错误。

### `[noexcept] void QSslDiffieHellmanParameters::swap(QSslDiffieHellmanParameters &other)`

**作用与语义：**

将`QSslDiffieHellmanParameters`与`other`交换。这个操作非常快，从不失败。

### `[noexcept] QSslDiffieHellmanParameters &QSslDiffieHellmanParameters::operator=(QSslDiffieHellmanParameters &&other)`

**作用与语义：**

移动分配`other`到该`QSslDiffieHellmanParameters`实例。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `QSslDiffieHellmanParameters &QSslDiffieHellmanParameters::operator=(const QSslDiffieHellmanParameters &other)`

**作用与语义：**

将`other`的内容复制到这个`QSslDiffieHellmanParameters`中，使两者`QSslDiffieHellmanParameters`完全相同。
返回了对此`QSslDiffieHellmanParameters`的引用。

### `[noexcept] size_t qHash(const QSslDiffieHellmanParameters &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] bool operator!=(const QSslDiffieHellmanParameters &lhs, const QSslDiffieHellmanParameters &rhs)`

**作用与语义：**

如果 `lhs` 不等于 `rhs`，则返回 `true`；否则返回 `false`。

### `QDebug operator<<(QDebug debug, const QSslDiffieHellmanParameters &dhparam)`

**作用与语义：**

将 Diffie-Hellman 参数集写入调试对象 `debug` `dhparam` 进行调试。
Diffie-Hellman 参数将以 Base64 编码的 DER 形式表示。

### `[noexcept] bool operator==(const QSslDiffieHellmanParameters &lhs, const QSslDiffieHellmanParameters &rhs)`

**作用与语义：**

如果 `lhs` 等于 `rhs`，则返回 `true`；否则返回 `false`。

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

`QSslDiffieHellmanParameters` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
