# QSslKey

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QSslKey` 是 Qt Network 的“Ssl键”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QSslKey` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QSslKey>`
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

- `QSslKey()`
- `QSslKey(Qt::HANDLE handle, QSsl::KeyType type = QSsl::PrivateKey)`
- `QSslKey(QIODevice *device, QSsl::KeyAlgorithm algorithm, QSsl::EncodingFormat encoding = QSsl::Pem, QSsl::KeyType type = QSsl::PrivateKey, const QByteArray &passPhrase = QByteArray())`
- `QSslKey(const QByteArray &encoded, QSsl::KeyAlgorithm algorithm, QSsl::EncodingFormat encoding = QSsl::Pem, QSsl::KeyType type = QSsl::PrivateKey, const QByteArray &passPhrase = QByteArray())`
- `QSslKey(const QSslKey &other)`
- `~QSslKey()`
- `QSsl::KeyAlgorithm algorithm() const`
- `void clear()`
- `Qt::HANDLE handle() const`
- `bool isNull() const`
- `int length() const`
- `void swap(QSslKey &other)`
- `QByteArray toDer(const QByteArray &passPhrase = QByteArray()) const`
- `QByteArray toPem(const QByteArray &passPhrase = QByteArray()) const`
- `QSsl::KeyType type() const`
- `bool operator!=(const QSslKey &other) const`
- `QSslKey & operator=(const QSslKey &other)`
- `bool operator==(const QSslKey &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QSslKey::QSslKey()`

**作用与语义：**

构造一个空密钥。

### `[explicit] QSslKey::QSslKey(Qt::HANDLE handle, QSsl::KeyType type = QSsl::PrivateKey)`

**作用与语义：**

从有效的本地密钥`handle`构造 QSslKey。`type` 指定密钥是公有还是私钥。
QSslKey 会获得该密钥的所有权，你不能使用原生库释放密钥。

### `QSslKey::QSslKey(QIODevice *device, QSsl::KeyAlgorithm algorithm, QSsl::EncodingFormat encoding = QSsl::Pem, QSsl::KeyType type = QSsl::PrivateKey, const QByteArray &passPhrase = QByteArray())`

**作用与语义：**

通过使用指定的`algorithm`和`encoding`格式从`device`读取和解码数据来构建QSslKey。`type`规定密钥是公的还是私有的。
如果密钥是加密的，那么`passPhrase`会用来解密。
构造完成后，使用`isNull()`检查`device`是否提供了有效的密钥。

### `QSslKey::QSslKey(const QByteArray &encoded, QSsl::KeyAlgorithm algorithm, QSsl::EncodingFormat encoding = QSsl::Pem, QSsl::KeyType type = QSsl::PrivateKey, const QByteArray &passPhrase = QByteArray())`

**作用与语义：**

通过解码字节数组中的字符串，`encoded`使用指定的`algorithm`和`encoding`格式来构造 QSslKey。`type` 指定密钥是公键还是私钥。
如果密钥被加密，则`passPhrase`用于解密。
构造完成后，使用`isNull()`检查`encoded`是否包含有效的密钥。

### `QSslKey::QSslKey(const QSslKey &other)`

**作用与语义：**

制造了一个与`other`一模一样的复制品。

### `[noexcept] QSslKey::~QSslKey()`

**作用与语义：**

摧毁`QSslKey`物体。

### `QSsl::KeyAlgorithm QSslKey::algorithm() const`

**作用与语义：**

返回密钥算法。

### `void QSslKey::clear()`

**作用与语义：**

清除此密钥的内容，使其为 null 密钥。

### `Qt::HANDLE QSslKey::handle() const`

**作用与语义：**

返回指向本地密钥柄的指针（如果有的话），否则就`nullptr`。
你可以将该句号与原生 API 一起使用，访问密钥的扩展信息。
警告：该函数的使用很可能不可移植，且其返回值可能因平台及次要Qt版本而异。

### `bool QSslKey::isNull() const`

**作用与语义：**

如果这是空键，返回`true`;否则为假。

### `int QSslKey::length() const`

**作用与语义：**

返回密钥的长度（以位为单位），如果密钥为空，则返回-1。

### `[noexcept] void QSslKey::swap(QSslKey &other)`

**作用与语义：**

将这个SSL密钥与`other`交换。这个操作非常快，从未失败过。

### `QByteArray QSslKey::toDer(const QByteArray &passPhrase = QByteArray()) const`

**作用与语义：**

返回DER编码中的密钥。
`passPhrase`论证应省略，因为DER无法加密。它将在未来Qt版本中被移除。

### `QByteArray QSslKey::toPem(const QByteArray &passPhrase = QByteArray()) const`

**作用与语义：**

返回PEM编码中的密钥。如果密钥是私钥且`passPhrase`非空，结果被`passPhrase`加密。

### `QSsl::KeyType QSslKey::type() const`

**作用与语义：**

返回密钥类型（即公钥或私钥）。

### `bool QSslKey::operator!=(const QSslKey &other) const`

**作用与语义：**

如果该键不等于键`other`，返回`true`;否则返回`false`。

### `QSslKey &QSslKey::operator=(const QSslKey &other)`

**作用与语义：**

将`other`的内容复制到该密钥中，使两个密钥完全相同。
返回了对该`QSslKey`的引用。

### `bool QSslKey::operator==(const QSslKey &other) const`

**作用与语义：**

如果该键等于 `other`，则返回 `true`;否则返回 `false`。

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

`QSslKey` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
