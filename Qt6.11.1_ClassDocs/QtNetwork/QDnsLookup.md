# QDnsLookup

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QDnsLookup` 是 Qt Network 的“DnsLookup”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QDnsLookup` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QDnsLookup>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

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

- `enum Error { NoError, ResolverError, OperationCancelledError, InvalidRequestError, InvalidReplyError, …, TimeoutError }`
- `enum Protocol { Standard, DnsOverTls }`
- `enum Type { A, AAAA, ANY, CNAME, MX, …, TXT }`

### 属性

- `(since 6.8) authenticData : bool`
- `error : Error`
- `errorString : QString`
- `name : QString`
- `nameserver : QHostAddress`
- `(since 6.6) nameserverPort : quint16`
- `(since 6.8) nameserverProtocol : Protocol`
- `type : Type`

### 公有函数

- `QDnsLookup(QObject *parent = nullptr)`
- `QDnsLookup(QDnsLookup::Type type, const QString &name, QObject *parent = nullptr)`
- `QDnsLookup(QDnsLookup::Type type, const QString &name, const QHostAddress &nameserver, QObject *parent = nullptr)`
- `(since 6.6) QDnsLookup(QDnsLookup::Type type, const QString &name, const QHostAddress &nameserver, quint16 port, QObject *parent = nullptr)`
- `(since 6.8) QDnsLookup(QDnsLookup::Type type, const QString &name, QDnsLookup::Protocol protocol, const QHostAddress &nameserver, quint16 port = 0, QObject *parent = nullptr)`
- `virtual ~QDnsLookup()`
- `QBindable<QString> bindableName()`
- `QBindable<QHostAddress> bindableNameserver()`
- `QBindable<quint16> bindableNameserverPort()`
- `QBindable<QDnsLookup::Protocol> bindableNameserverProtocol()`
- `QBindable<QDnsLookup::Type> bindableType()`
- `QList<QDnsDomainNameRecord> canonicalNameRecords() const`
- `QDnsLookup::Error error() const`
- `QString errorString() const`
- `QList<QDnsHostAddressRecord> hostAddressRecords() const`
- `bool isAuthenticData() const`
- `bool isFinished() const`
- `QList<QDnsMailExchangeRecord> mailExchangeRecords() const`
- `QString name() const`
- `QList<QDnsDomainNameRecord> nameServerRecords() const`
- `QHostAddress nameserver() const`
- `quint16 nameserverPort() const`
- `QDnsLookup::Protocol nameserverProtocol() const`
- `QList<QDnsDomainNameRecord> pointerRecords() const`
- `QList<QDnsServiceRecord> serviceRecords() const`
- `void setName(const QString &name)`
- `void setNameserver(const QHostAddress &nameserver)`
- `void setNameserver(QDnsLookup::Protocol protocol, const QHostAddress &nameserver, quint16 port = 0)`
- `(since 6.6) void setNameserver(const QHostAddress &nameserver, quint16 port)`
- `void setNameserverPort(quint16 port)`
- `void setNameserverProtocol(QDnsLookup::Protocol protocol)`
- `(since 6.8) void setSslConfiguration(const QSslConfiguration &sslConfiguration)`
- `void setType(QDnsLookup::Type)`
- `QSslConfiguration sslConfiguration() const`
- `QList<QDnsTextRecord> textRecords() const`
- `(since 6.8) QList<QDnsTlsAssociationRecord> tlsAssociationRecords() const`
- `QDnsLookup::Type type() const`

### 公有槽函数

- `void abort()`
- `void lookup()`

### 信号

- `void finished()`
- `void nameChanged(const QString &name)`
- `void nameserverChanged(const QHostAddress &nameserver)`
- `void nameserverPortChanged(quint16 port)`
- `void nameserverProtocolChanged(QDnsLookup::Protocol protocol)`
- `void typeChanged(QDnsLookup::Type type)`

### 静态公有成员

- `(since 6.8) quint16 defaultPortForProtocol(QDnsLookup::Protocol protocol)`
- `(since 6.8) bool isProtocolSupported(QDnsLookup::Protocol protocol)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 58 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QDnsLookup::Error`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDnsLookup` 暴露的类型声明 `错误`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Error`。
- 属性名：`QDnsLookup`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QDnsLookup::Protocol`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDnsLookup` 暴露的类型声明 `Protocol`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Protocol`。
- 属性名：`QDnsLookup`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QDnsLookup::Type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDnsLookup` 暴露的类型声明 `类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Type`。
- 属性名：`QDnsLookup`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only, since 6.8] authenticData : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QDnsLookup` 的状态/能力属性。通常通过 `authenticData()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`authenticData`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] error : Error`

**API 类别：** 属性说明

**中文解读：** 这是 `QDnsLookup` 的状态/能力属性。通常通过 `error()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`Error`。
- 属性名：`error`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] errorString : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QDnsLookup` 的状态/能力属性。通常通过 `errorString()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`errorString`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] name : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QDnsLookup` 的配置属性。初始化或状态切换时通过 `setName(...)` 设置，之后用 `name()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`name`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] nameserver : QHostAddress`

**API 类别：** 属性说明

**中文解读：** 这是 `QDnsLookup` 的配置属性。初始化或状态切换时通过 `setNameserver(...)` 设置，之后用 `nameserver()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QHostAddress`。
- 属性名：`nameserver`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable, since 6.6] nameserverPort : quint16`

**API 类别：** 属性说明

**中文解读：** 这是 `QDnsLookup` 的配置属性。初始化或状态切换时通过 `setNameserverPort(...)` 设置，之后用 `nameserverPort()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`quint16`。
- 属性名：`nameserverPort`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable, since 6.8] nameserverProtocol : Protocol`

**API 类别：** 属性说明

**中文解读：** 这是 `QDnsLookup` 的配置属性。初始化或状态切换时通过 `setNameserverProtocol(...)` 设置，之后用 `nameserverProtocol()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Protocol`。
- 属性名：`nameserverProtocol`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] type : Type`

**API 类别：** 属性说明

**中文解读：** 这是 `QDnsLookup` 的配置属性。初始化或状态切换时通过 `setType(...)` 设置，之后用 `type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Type`。
- 属性名：`type`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QDnsLookup::QDnsLookup(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDnsLookup` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDnsLookup::QDnsLookup(QDnsLookup::Type type, const QString &name, QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDnsLookup` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `type`：类型为 `QDnsLookup::Type`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDnsLookup::QDnsLookup(QDnsLookup::Type type, const QString &name, const QHostAddress &nameserver, QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDnsLookup` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `type`：类型为 `QDnsLookup::Type`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `nameserver`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QDnsLookup::QDnsLookup(QDnsLookup::Type type, const QString &name, const QHostAddress &nameserver, quint16 port, QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDnsLookup` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `type`：类型为 `QDnsLookup::Type`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `nameserver`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `port`：类型为 `quint16`。没有默认值，调用时必须提供。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QDnsLookup::QDnsLookup(QDnsLookup::Type type, const QString &name, QDnsLookup::Protocol protocol, const QHostAddress &nameserver, quint16 port = 0, QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDnsLookup` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `type`：类型为 `QDnsLookup::Type`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `protocol`：类型为 `QDnsLookup::Protocol`。没有默认值，调用时必须提供。传入 `QDnsLookup::Protocol` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `nameserver`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `port`：类型为 `quint16`。默认值为 `0`。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QDnsLookup::~QDnsLookup()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDnsLookup` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QDnsLookup::abort()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `abort`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QDnsDomainNameRecord> QDnsLookup::canonicalNameRecords() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canonicalNameRecords`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`QList<QDnsDomainNameRecord>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept, since 6.8] quint16 QDnsLookup::defaultPortForProtocol(QDnsLookup::Protocol protocol)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `defaultPortForProtocol`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`quint16`。
- 参数 `protocol`：类型为 `QDnsLookup::Protocol`。没有默认值，调用时必须提供。传入 `QDnsLookup::Protocol` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QDnsLookup::finished()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDnsLookup` 发出的通知信号 `finished`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QDnsHostAddressRecord> QDnsLookup::hostAddressRecords() const`

**API 类别：** 成员函数说明

**中文解读：** `QDnsLookup::hostAddressRecords` 用于计算、查询或取得与“host、Address、Records”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QDnsHostAddressRecord>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QDnsHostAddressRecord>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDnsLookup::isFinished() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isFinished`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.8] bool QDnsLookup::isProtocolSupported(QDnsLookup::Protocol protocol)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isProtocolSupported`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `protocol`：类型为 `QDnsLookup::Protocol`。没有默认值，调用时必须提供。传入 `QDnsLookup::Protocol` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QDnsLookup::lookup()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `lookup`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QDnsMailExchangeRecord> QDnsLookup::mailExchangeRecords() const`

**API 类别：** 成员函数说明

**中文解读：** `QDnsLookup::mailExchangeRecords` 用于计算、查询或取得与“mail、Exchange、Records”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QDnsMailExchangeRecord>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QDnsMailExchangeRecord>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QDnsLookup::nameChanged(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDnsLookup` 发出的通知信号 `nameChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QDnsDomainNameRecord> QDnsLookup::nameServerRecords() const`

**API 类别：** 成员函数说明

**中文解读：** `QDnsLookup::nameServerRecords` 用于计算、查询或取得与“名称、Server、Records”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QDnsDomainNameRecord>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QDnsDomainNameRecord>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QDnsDomainNameRecord> QDnsLookup::pointerRecords() const`

**API 类别：** 成员函数说明

**中文解读：** `QDnsLookup::pointerRecords` 用于计算、查询或取得与“pointer、Records”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QDnsDomainNameRecord>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QDnsDomainNameRecord>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QDnsServiceRecord> QDnsLookup::serviceRecords() const`

**API 类别：** 成员函数说明

**中文解读：** `QDnsLookup::serviceRecords` 用于计算、查询或取得与“service、Records”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QDnsServiceRecord>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QDnsServiceRecord>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] void QDnsLookup::setNameserver(const QHostAddress &nameserver, quint16 port)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNameserver`。调用它会改变 `QDnsLookup` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `nameserver`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `port`：类型为 `quint16`。没有默认值，调用时必须提供。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QDnsLookup::setSslConfiguration(const QSslConfiguration &sslConfiguration)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSslConfiguration`。调用它会改变 `QDnsLookup` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `sslConfiguration`：类型为 `const QSslConfiguration &`。没有默认值，调用时必须提供。传入 `const QSslConfiguration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslConfiguration QDnsLookup::sslConfiguration() const`

**API 类别：** 成员函数说明

**中文解读：** `QDnsLookup::sslConfiguration` 用于计算、查询或取得与“ssl、Configuration”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslConfiguration`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslConfiguration`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QDnsTextRecord> QDnsLookup::textRecords() const`

**API 类别：** 成员函数说明

**中文解读：** `QDnsLookup::textRecords` 用于计算、查询或取得与“文本、Records”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QDnsTextRecord>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QDnsTextRecord>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QList<QDnsTlsAssociationRecord> QDnsLookup::tlsAssociationRecords() const`

**API 类别：** 成员函数说明

**中文解读：** `QDnsLookup::tlsAssociationRecords` 用于计算、查询或取得与“tls、Association、Records”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QDnsTlsAssociationRecord>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QDnsTlsAssociationRecord>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QDnsLookup::typeChanged(QDnsLookup::Type type)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDnsLookup` 发出的通知信号 `typeChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `type`：类型为 `QDnsLookup::Type`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<QString> bindableName()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableName`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<QString>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<QHostAddress> bindableNameserver()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableNameserver`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<QHostAddress>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<quint16> bindableNameserverPort()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableNameserverPort`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<quint16>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<QDnsLookup::Protocol> bindableNameserverProtocol()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableNameserverProtocol`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<QDnsLookup::Protocol>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<QDnsLookup::Type> bindableType()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableType`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<QDnsLookup::Type>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDnsLookup::Error error() const`

**API 类别：** 公有函数

**中文解读：** `QDnsLookup::error` 用于计算、查询或取得与“错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDnsLookup::Error`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDnsLookup::Error`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString errorString() const`

**API 类别：** 公有函数

**中文解读：** `QDnsLookup::errorString` 用于计算、查询或取得与“错误、字符串”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isAuthenticData() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isAuthenticData`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString name() const`

**API 类别：** 公有函数

**中文解读：** `QDnsLookup::name` 用于计算、查询或取得与“名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QHostAddress nameserver() const`

**API 类别：** 公有函数

**中文解读：** `QDnsLookup::nameserver` 用于计算、查询或取得与“nameserver”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QHostAddress`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QHostAddress`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint16 nameserverPort() const`

**API 类别：** 公有函数

**中文解读：** `QDnsLookup::nameserverPort` 用于计算、查询或取得与“nameserver、Port”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `quint16`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint16`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDnsLookup::Protocol nameserverProtocol() const`

**API 类别：** 公有函数

**中文解读：** `QDnsLookup::nameserverProtocol` 用于计算、查询或取得与“nameserver、Protocol”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDnsLookup::Protocol`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDnsLookup::Protocol`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setName(const QString &name)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setName`。调用它会改变 `QDnsLookup` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setNameserver(const QHostAddress &nameserver)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setNameserver`。调用它会改变 `QDnsLookup` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `nameserver`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setNameserver(QDnsLookup::Protocol protocol, const QHostAddress &nameserver, quint16 port = 0)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setNameserver`。调用它会改变 `QDnsLookup` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `protocol`：类型为 `QDnsLookup::Protocol`。没有默认值，调用时必须提供。传入 `QDnsLookup::Protocol` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `nameserver`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `port`：类型为 `quint16`。默认值为 `0`。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setNameserverPort(quint16 port)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setNameserverPort`。调用它会改变 `QDnsLookup` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `port`：类型为 `quint16`。没有默认值，调用时必须提供。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setNameserverProtocol(QDnsLookup::Protocol protocol)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setNameserverProtocol`。调用它会改变 `QDnsLookup` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `protocol`：类型为 `QDnsLookup::Protocol`。没有默认值，调用时必须提供。传入 `QDnsLookup::Protocol` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setType(QDnsLookup::Type)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setType`。调用它会改变 `QDnsLookup` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `Type`：类型为 `QDnsLookup::`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDnsLookup::Type type() const`

**API 类别：** 公有函数

**中文解读：** `QDnsLookup::type` 用于计算、查询或取得与“类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDnsLookup::Type`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDnsLookup::Type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void nameserverChanged(const QHostAddress &nameserver)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `nameserverChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `nameserver`：类型为 `const QHostAddress &`。没有默认值，调用时必须提供。传入 `const QHostAddress &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void nameserverPortChanged(quint16 port)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `nameserverPortChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `port`：类型为 `quint16`。没有默认值，调用时必须提供。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void nameserverProtocolChanged(QDnsLookup::Protocol protocol)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `nameserverProtocolChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `protocol`：类型为 `QDnsLookup::Protocol`。没有默认值，调用时必须提供。传入 `QDnsLookup::Protocol` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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

`QDnsLookup` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
