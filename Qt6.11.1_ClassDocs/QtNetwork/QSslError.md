# QSslError

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QSslError` 是 Qt Network 的“Ssl错误”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QSslError` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QSslError>`
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

- `enum SslError { NoError, UnableToGetIssuerCertificate, UnableToDecryptCertificateSignature, UnableToDecodeIssuerPublicKey, CertificateSignatureFailed, …, OcspStatusUnknown }`

### 公有函数

- `QSslError()`
- `QSslError(QSslError::SslError error)`
- `QSslError(QSslError::SslError error, const QSslCertificate &certificate)`
- `QSslError(const QSslError &other)`
- `~QSslError()`
- `QSslCertificate certificate() const`
- `QSslError::SslError error() const`
- `QString errorString() const`
- `void swap(QSslError &other)`
- `bool operator!=(const QSslError &other) const`
- `QSslError & operator=(const QSslError &other)`
- `bool operator==(const QSslError &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSslError::SslError`

**作用与语义：**

描述SSL握手过程中可能出现的所有识别错误。
- `QSslError::NoError`：`0`
- `QSslError::UnableToGetIssuerCertificate`：`1`
- `QSslError::UnableToDecryptCertificateSignature`：`2`
- `QSslError::UnableToDecodeIssuerPublicKey`：`3`
- `QSslError::CertificateSignatureFailed`：`4`
- `QSslError::CertificateNotYetValid`：`5`
- `QSslError::CertificateExpired`：`6`
- `QSslError::InvalidNotBeforeField`：`7`
- `QSslError::InvalidNotAfterField`：`8`
- `QSslError::SelfSignedCertificate`：`9`
- `QSslError::SelfSignedCertificateInChain`：`10`
- `QSslError::UnableToGetLocalIssuerCertificate`：`11`
- `QSslError::UnableToVerifyFirstCertificate`：`12`
- `QSslError::CertificateRevoked`：`13`
- `QSslError::InvalidCaCertificate`：`14`
- `QSslError::PathLengthExceeded`：`15`
- `QSslError::InvalidPurpose`：`16`
- `QSslError::CertificateUntrusted`：`17`
- `QSslError::CertificateRejected`：`18`
- `QSslError::SubjectIssuerMismatch`：`19`
- `QSslError::AuthorityIssuerSerialNumberMismatch`：`20`
- `QSslError::NoPeerCertificate`：`21`
- `QSslError::HostNameMismatch`：`22`
- `QSslError::UnspecifiedError`：`-1`
- `QSslError::NoSslSupport`：`23`
- `QSslError::CertificateBlacklisted`：`24`
- `QSslError::CertificateStatusUnknown`：`25`
- `QSslError::OcspNoResponseFound`：`26`
- `QSslError::OcspMalformedRequest`：`27`
- `QSslError::OcspMalformedResponse`：`28`
- `QSslError::OcspInternalError`：`29`
- `QSslError::OcspTryLater`：`30`
- `QSslError::OcspSigRequred`：`31`
- `QSslError::OcspUnauthorized`：`32`
- `QSslError::OcspResponseCannotBeTrusted`：`33`
- `QSslError::OcspResponseCertIdUnknown`：`34`
- `QSslError::OcspResponseExpired`：`35`
- `QSslError::OcspStatusUnknown`：`36`

### `QSslError::QSslError()`

**作用与语义：**

构造一个无错误且默认证书的QSslError对象。

### `[explicit] QSslError::QSslError(QSslError::SslError error)`

**作用与语义：**

构造一个QSslError对象。参数指定发生的`error`。

### `QSslError::QSslError(QSslError::SslError error, const QSslCertificate &certificate)`

**作用与语义：**

构造一个QSslError对象。这两个参数分别指定了发生的`error`，以及错误与哪个`certificate`相关。

### `QSslError::QSslError(const QSslError &other)`

**作用与语义：**

制造了一个与`other`一模一样的复制品。

### `[noexcept] QSslError::~QSslError()`

**作用与语义：**

摧毁`QSslError`物体。

### `QSslCertificate QSslError::certificate() const`

**作用与语义：**

返回与该错误相关的证书，或者如果错误与任何证书无关，则返回空证书。

### `QSslError::SslError QSslError::error() const`

**作用与语义：**

返回错误类型。

### `QString QSslError::errorString() const`

**作用与语义：**

返回一个简短且易于理解的本地错误描述。

### `[noexcept] void QSslError::swap(QSslError &other)`

**作用与语义：**

将该错误实例与`other`交换。该操作非常快速且从未失败。

### `bool QSslError::operator!=(const QSslError &other) const`

**作用与语义：**

如果误差不等于 `other`，返回 `true`;否则返回 false。

### `QSslError &QSslError::operator=(const QSslError &other)`

**作用与语义：**

将`other`的内容分配给该错误。

### `bool QSslError::operator==(const QSslError &other) const`

**作用与语义：**

如果误差等于 `other`，则返回 `true`;否则返回 `false`。

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

`QSslError` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
