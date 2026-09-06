# QHstsPolicy

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QHstsPolicy` 是 Qt Network 的“HstsPolicy”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QHstsPolicy` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QHstsPolicy>`
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

- `enum PolicyFlag { IncludeSubDomains }`
- `flags PolicyFlags`

### 公有函数

- `QHstsPolicy()`
- `QHstsPolicy(const QDateTime &expiry, QHstsPolicy::PolicyFlags flags, const QString &host, QUrl::ParsingMode mode = QUrl::DecodedMode)`
- `QHstsPolicy(const QHstsPolicy &other)`
- `~QHstsPolicy()`
- `QDateTime expiry() const`
- `QString host(QUrl::ComponentFormattingOptions options = QUrl::FullyDecoded) const`
- `bool includesSubDomains() const`
- `bool isExpired() const`
- `void setExpiry(const QDateTime &expiry)`
- `void setHost(const QString &host, QUrl::ParsingMode mode = QUrl::DecodedMode)`
- `void setIncludesSubDomains(bool include)`
- `void swap(QHstsPolicy &other)`
- `QHstsPolicy & operator=(const QHstsPolicy &other)`

### 相关非成员函数

- `bool operator!=(const QHstsPolicy &lhs, const QHstsPolicy &rhs)`
- `bool operator==(const QHstsPolicy &lhs, const QHstsPolicy &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QHstsPolicy::PolicyFlagflags QHstsPolicy::PolicyFlags`

**作用与语义：**

- `QHstsPolicy::IncludeSubDomains`: `1`；指示策略是否必须包含子域。
PolicyFlags 类型是 QFlags<PolicyFlag> 的 typedef。它存储 PolicyFlag 值的 OR 组合。

### `QHstsPolicy::QHstsPolicy()`

**作用与语义：**

构建一个无效（已过期）的策略，空主机名和未包含子域。

### `QHstsPolicy::QHstsPolicy(const QDateTime &expiry, QHstsPolicy::PolicyFlags flags, const QString &host, QUrl::ParsingMode mode = QUrl::DecodedMode)`

**作用与语义：**

构造带有`expiry`的QHstsPolicy（UTC中）;`flags`是一个值，表示该策略是否也必须包含子域，`host`数据的解释是根据`mode`进行的。

### `QHstsPolicy::QHstsPolicy(const QHstsPolicy &other)`

**作用与语义：**

创建`other`对象的副本。

### `[noexcept] QHstsPolicy::~QHstsPolicy()`

**作用与语义：**

毁灭者。

### `QDateTime QHstsPolicy::expiry() const`

**作用与语义：**

返回保单的到期日（UTC单位）。

### `QString QHstsPolicy::host(QUrl::ComponentFormattingOptions options = QUrl::FullyDecoded) const`

**作用与语义：**

根据`options`格式返回给定策略的主机。

### `bool QHstsPolicy::includesSubDomains() const`

**作用与语义：**

如果该策略也包含子域名，返回`true`。

### `bool QHstsPolicy::isExpired() const`

**作用与语义：**

如果该政策有有效到期日且该日期大于QDateTime：：currentGetDateTimeUtc()，请返回`true`。

### `void QHstsPolicy::setExpiry(const QDateTime &expiry)`

**作用与语义：**

将政策的到期日（UTC单位）设定为`expiry`。

### `void QHstsPolicy::setHost(const QString &host, QUrl::ParsingMode mode = QUrl::DecodedMode)`

**作用与语义：**

设置主机，`host`数据根据`mode`参数解释。

### `void QHstsPolicy::setIncludesSubDomains(bool include)`

**作用与语义：**

设置该策略是否包含子域以进行`include`。

### `[noexcept] void QHstsPolicy::swap(QHstsPolicy &other)`

**作用与语义：**

把这个政策换成`other`。这个操作非常快，从不失败。

### `QHstsPolicy &QHstsPolicy::operator=(const QHstsPolicy &other)`

**作用与语义：**

复制赋值操作员，复制`other`。

### `bool operator!=(const QHstsPolicy &lhs, const QHstsPolicy &rhs)`

**作用与语义：**

如果两个策略`lhs`和`rhs`的托管日期或到期日不相同，或者对是否包含或排除子域名不一致，返回`true`。

### `bool operator==(const QHstsPolicy &lhs, const QHstsPolicy &rhs)`

**作用与语义：**

如果两个保单`lhs`和`rhs`在是否包含或排除子域名时，是否拥有相同的主机和到期日，返回`true`。

### `enum PolicyFlag { IncludeSubDomains }`

**作用与语义：**

- `QHstsPolicy::IncludeSubDomains`: `1`；指示策略是否必须包含子域。
PolicyFlags 类型是 QFlags<PolicyFlag> 的 typedef。它存储 PolicyFlag 值的 OR 组合。

### `flags PolicyFlags`

**作用与语义：**

- `QHstsPolicy::IncludeSubDomains`: `1`；指示策略是否必须包含子域。
PolicyFlags 类型是 QFlags<PolicyFlag> 的 typedef。它存储 PolicyFlag 值的 OR 组合。

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

`QHstsPolicy` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
