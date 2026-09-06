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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDnsLookup::Error`

**作用与语义：**

显示在处理DNS查询过程中发现的所有可能错误条件。
- `QDnsLookup::NoError`：`0`;无错误条件。
- `QDnsLookup::ResolverError`：`1`;系统DNS解析器初始化时发生错误。
- `QDnsLookup::OperationCancelledError`：`2`;查找被中止，使用`abort()`方法。
- `QDnsLookup::InvalidRequestError`：`3`;请求的DNS查询无效。
- `QDnsLookup::InvalidReplyError`：`4`;服务器返回的回复无效。
- `QDnsLookup::ServerFailureError`：`5`;服务器在处理请求时遇到内部故障（SERVFAIL）。
- `QDnsLookup::ServerRefusedError`：`6`;服务器出于安全或策略原因拒绝处理请求（拒绝）。
- `QDnsLookup::NotFoundError`：`7`;请求的域名不存在（NXDOMAIN）。
- `QDnsLookup::TimeoutError`：`8`;服务器未能及时联系或未及时回复（自6.6版本起）。

### `enum QDnsLookup::Protocol`

**作用与语义：**

表示被查询的DNS服务器类型。
- `QDnsLookup::Standard`：`0`;常规、未加密的DNS，使用UDP并在需要时退回TCP（默认端口：53）
- `QDnsLookup::DnsOverTls`：`1`;基于TLS的加密DNS（DoT，依RFC 7858规定），TCP上的加密DNS（默认端口：853）

### `enum QDnsLookup::Type`

**作用与语义：**

表示所执行的 DNS 查找类型。
- `QDnsLookup::A`：`1`;IPv4地址记录。
- `QDnsLookup::AAAA`：`28`;IPv6地址记录。
- `QDnsLookup::ANY`：`255`;任何记录。
- `QDnsLookup::CNAME`：`5`;正史姓名记录。
- `QDnsLookup::MX`：`15`;邮件交换记录。
- `QDnsLookup::NS`：`2`;名称服务器记录。
- `QDnsLookup::PTR`：`12`;指针记录。
- `QDnsLookup::SRV`：`33`;服役记录。
- `QDnsLookup::TLSA (since Qt 6.8)`：`52`;TLS协会记录。
- `QDnsLookup::TXT`：`16`;文本记录。

### `[read-only, since 6.8] authenticData : bool`

**作用与语义：**

该属性决定了回复是否被解析器认证。
`QDnsLookup`不自行执行认证。相反，它信任被查询的名称服务器执行认证并报告。应用程序负责判断其配置的服务器是否值得信赖`setNameserver()`;如果未设置服务器，`QDnsLookup`会遵守系统配置，决定是否可信响应。
即使`error()`表示发生了解析器错误，该属性仍可被设置。

**如何使用：** 调用 `authenticData()` 读取当前值；它不会修改应用状态。

### `[read-only] error : Error`

**作用与语义：**

该属性表示如果DNS查询失败或`NoError`时发生的错误类型。

**如何使用：** 调用 `error()` 读取当前值；它不会修改应用状态。

### `[read-only] errorString : QString`

**作用与语义：**

该属性包含了如果DNS查询失败时错误的人类可读描述。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `[bindable] name : QString`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该房产名称值得查询。
如果查找的名称为空，`QDnsLookup`会尝试解析DNS的根域名。该查询通常在`QDnsLookup::type`设置为`NS`时进行。
注意：该名称将使用 IDNA 编码，这意味着它不适合查询与 DNS-SD 规范兼容的 SRV 记录。

**如何使用：** 调用 `name()` 读取当前值；它不会修改应用状态。

### `[bindable] nameserver : QHostAddress`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于 DNS 查询的名称服务器。

**如何使用：** 调用 `nameserver()` 读取当前值；它不会修改应用状态。

### `[bindable, since 6.6] nameserverPort : quint16`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于 DNS 查询的名称服务器端口号。
值为0表示应使用默认端口`QDnsLookup` `nameserverProtocol()`。
注意：将端口号设置为非默认值（53）可能导致名称解析失败，具体取决于操作系统的限制和防火墙，如果使用的`nameserverProtocol()` `QDnsLookup::Standard`。值得注意的是，`QDnsLookup`使用的 Windows API 无法处理替代端口号。

**如何使用：** 调用 `nameserverPort()` 读取当前值；它不会修改应用状态。

### `[bindable, since 6.8] nameserverProtocol : Protocol`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含发送 DNS 查询时所使用的协议。

**如何使用：** 调用 `nameserverProtocol()` 读取当前值；它不会修改应用状态。

### `[bindable] type : Type`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含DNS查找类型。

**如何使用：** 调用 `type()` 读取当前值；它不会修改应用状态。

### `[explicit] QDnsLookup::QDnsLookup(QObject *parent = nullptr)`

**作用与语义：**

构建一个QDnsLookup对象，并将`parent`设为父对象。
`type`属性将默认归`QDnsLookup::A`。

### `QDnsLookup::QDnsLookup(QDnsLookup::Type type, const QString &name, QObject *parent = nullptr)`

**作用与语义：**

为给定的`type`和`name`构造一个QDnsLookup对象，并将`parent`设为父对象。

### `QDnsLookup::QDnsLookup(QDnsLookup::Type type, const QString &name, const QHostAddress &nameserver, QObject *parent = nullptr)`

**作用与语义：**

构建一个QDnsLookup对象，用于查询记录类型`type`的`name`，使用运行在默认DNS端口上的DNS服务器`nameserver`，并将`parent`设为父对象。

### `[since 6.6] QDnsLookup::QDnsLookup(QDnsLookup::Type type, const QString &name, const QHostAddress &nameserver, quint16 port, QObject *parent = nullptr)`

**作用与语义：**

构建一个QDnsLookup对象，用于查询记录类型`type`的`name`，使用运行在端口`port`上的DNS服务器`nameserver`，并将`parent`设为父对象。
注意：将端口号设置为非默认值（53）可能导致名称解析失败，具体取决于操作系统的限制和防火墙，前提是使用的`nameserverProtocol()` `QDnsLookup::Standard`。值得注意的是，QDnsLookup 使用的 Windows API 无法处理备用端口号。

### `[since 6.8] QDnsLookup::QDnsLookup(QDnsLookup::Type type, const QString &name, QDnsLookup::Protocol protocol, const QHostAddress &nameserver, quint16 port = 0, QObject *parent = nullptr)`

**作用与语义：**

构建一个QDnsLookup对象，利用运行在端口`port`的DNS服务器`nameserver`发出记录类型`type`的`name`查询，并将`parent`设为父对象。
如果支持，查询将通过`protocol`发送。使用`isProtocolSupported()`检查是否支持。
注意：将端口号设置为非默认值（53）可能导致名称解析失败，具体取决于操作系统的限制和防火墙，前提是`nameserverProtocol()` `QDnsLookup::Standard`。值得注意的是，QDnsLookup 使用的 Windows API 无法处理备用端口号。

### `[virtual noexcept] QDnsLookup::~QDnsLookup()`

**作用与语义：**

摧毁`QDnsLookup`物体。
即使`QDnsLookup`对象未完成，删除它也是安全的，你永远不会收到它的结果。

### `[slot] void QDnsLookup::abort()`

**作用与语义：**

中止DNS查找操作。
如果查询已经完成，则不做任何操作。

### `QList<QDnsDomainNameRecord> QDnsLookup::canonicalNameRecords() const`

**作用与语义：**

返回与此查询相关的规范名称记录列表。

### `[static noexcept, since 6.8] quint16 QDnsLookup::defaultPortForProtocol(QDnsLookup::Protocol protocol)`

**作用与语义：**

返回协议`protocol`的标准（默认）端口号。

### `[signal] void QDnsLookup::finished()`

**作用与语义：**

该属性决定了回复是否被解析器认证。
`QDnsLookup`不自行执行认证。相反，它信任被查询的名称服务器执行认证并报告。应用程序负责判断其配置的服务器是否值得信赖`setNameserver()`;如果未设置服务器，`QDnsLookup`会遵守系统配置，决定是否可信响应。
即使`error()`表示发生了解析器错误，该属性仍可被设置。

**如何使用：** 调用 `finished()` 读取当前值；它不会修改应用状态。

### `QList<QDnsHostAddressRecord> QDnsLookup::hostAddressRecords() const`

**作用与语义：**

返回与此查询相关的主机地址记录列表。

### `bool QDnsLookup::isFinished() const`

**作用与语义：**

无论回复已结束还是中止，都会返回。

### `[static, since 6.8] bool QDnsLookup::isProtocolSupported(QDnsLookup::Protocol protocol)`

**作用与语义：**

如果`QDnsLookup`支持使用`protocol`的DNS查询，则返回为真。

### `[slot] void QDnsLookup::lookup()`

**作用与语义：**

执行DNS查询。
完成后`finished()`信号会发出。

### `QList<QDnsMailExchangeRecord> QDnsLookup::mailExchangeRecords() const`

**作用与语义：**

返回与此查询相关的邮件交换记录列表。
记录是根据RFC 5321排序的，所以如果你用它们连接服务器，应该按照列出的顺序尝试。

### `[signal] void QDnsLookup::nameChanged(const QString &name)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该房产名称值得查询。
如果查找的名称为空，`QDnsLookup`会尝试解析DNS的根域名。该查询通常在`QDnsLookup::type`设置为`NS`时进行。
注意：该名称将使用 IDNA 编码，这意味着它不适合查询与 DNS-SD 规范兼容的 SRV 记录。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `name` 的变化，不要把它当作普通函数主动调用。

### `QList<QDnsDomainNameRecord> QDnsLookup::nameServerRecords() const`

**作用与语义：**

返回与此查询相关的名称服务器记录列表。

### `QList<QDnsDomainNameRecord> QDnsLookup::pointerRecords() const`

**作用与语义：**

返回与该查找关联的指针记录列表。

### `QList<QDnsServiceRecord> QDnsLookup::serviceRecords() const`

**作用与语义：**

返回与此查询相关的服务记录列表。
记录是根据RFC 2782排序的，所以如果你用它们连接服务器，应该按照列表的顺序尝试。

### `[since 6.6] void QDnsLookup::setNameserver(const QHostAddress &nameserver, quint16 port)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于 DNS 查询的名称服务器。

**如何使用：** 调用 `setNameserver(...)` 修改 `nameserver`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[since 6.8] void QDnsLookup::setSslConfiguration(const QSslConfiguration &sslConfiguration)`

**作用与语义：**

设置`sslConfiguration`用于外出DNS-over-TLS连接。

### `QSslConfiguration QDnsLookup::sslConfiguration() const`

**作用与语义：**

返回当前的SSL配置。

### `QList<QDnsTextRecord> QDnsLookup::textRecords() const`

**作用与语义：**

返回与此查找相关的文本记录列表。

### `[since 6.8] QList<QDnsTlsAssociationRecord> QDnsLookup::tlsAssociationRecords() const`

**作用与语义：**

返回与此查询相关的TLS关联记录列表。
根据基于DNS的命名实体认证（DANE）标准，若无法确认DNS回复的真实性，该字段应忽略且不得用于验证某服务器的认证实体。更多信息请参见 `isAuthenticData()`。

### `[signal] void QDnsLookup::typeChanged(QDnsLookup::Type type)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含DNS查找类型。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `type` 的变化，不要把它当作普通函数主动调用。

### `QBindable<QString> bindableName()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该房产名称值得查询。
如果查找的名称为空，`QDnsLookup`会尝试解析DNS的根域名。该查询通常在`QDnsLookup::type`设置为`NS`时进行。
注意：该名称将使用 IDNA 编码，这意味着它不适合查询与 DNS-SD 规范兼容的 SRV 记录。

**如何使用：** 调用 `bindableName()` 取得 `name` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<QHostAddress> bindableNameserver()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于 DNS 查询的名称服务器。

**如何使用：** 调用 `bindableNameserver()` 取得 `nameserver` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<quint16> bindableNameserverPort()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于 DNS 查询的名称服务器端口号。
值为0表示应使用默认端口`QDnsLookup` `nameserverProtocol()`。
注意：将端口号设置为非默认值（53）可能导致名称解析失败，具体取决于操作系统的限制和防火墙，如果使用的`nameserverProtocol()` `QDnsLookup::Standard`。值得注意的是，`QDnsLookup`使用的 Windows API 无法处理替代端口号。

**如何使用：** 调用 `bindableNameserverPort()` 取得 `nameserverPort` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<QDnsLookup::Protocol> bindableNameserverProtocol()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含发送 DNS 查询时所使用的协议。

**如何使用：** 调用 `bindableNameserverProtocol()` 取得 `nameserverProtocol` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<QDnsLookup::Type> bindableType()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含DNS查找类型。

**如何使用：** 调用 `bindableType()` 取得 `type` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QDnsLookup::Error error() const`

**作用与语义：**

该属性表示如果DNS查询失败或`NoError`时发生的错误类型。

**如何使用：** 调用 `error()` 读取当前值；它不会修改应用状态。

### `QString errorString() const`

**作用与语义：**

该属性包含了如果DNS查询失败时错误的人类可读描述。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `bool isAuthenticData() const`

**作用与语义：**

该属性决定了回复是否被解析器认证。
`QDnsLookup`不自行执行认证。相反，它信任被查询的名称服务器执行认证并报告。应用程序负责判断其配置的服务器是否值得信赖`setNameserver()`;如果未设置服务器，`QDnsLookup`会遵守系统配置，决定是否可信响应。
即使`error()`表示发生了解析器错误，该属性仍可被设置。

**如何使用：** 调用 `isAuthenticData()` 读取当前值；它不会修改应用状态。

### `QString name() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该房产名称值得查询。
如果查找的名称为空，`QDnsLookup`会尝试解析DNS的根域名。该查询通常在`QDnsLookup::type`设置为`NS`时进行。
注意：该名称将使用 IDNA 编码，这意味着它不适合查询与 DNS-SD 规范兼容的 SRV 记录。

**如何使用：** 调用 `name()` 读取当前值；它不会修改应用状态。

### `QHostAddress nameserver() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于 DNS 查询的名称服务器。

**如何使用：** 调用 `nameserver()` 读取当前值；它不会修改应用状态。

### `quint16 nameserverPort() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于 DNS 查询的名称服务器端口号。
值为0表示应使用默认端口`QDnsLookup` `nameserverProtocol()`。
注意：将端口号设置为非默认值（53）可能导致名称解析失败，具体取决于操作系统的限制和防火墙，如果使用的`nameserverProtocol()` `QDnsLookup::Standard`。值得注意的是，`QDnsLookup`使用的 Windows API 无法处理替代端口号。

**如何使用：** 调用 `nameserverPort()` 读取当前值；它不会修改应用状态。

### `QDnsLookup::Protocol nameserverProtocol() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含发送 DNS 查询时所使用的协议。

**如何使用：** 调用 `nameserverProtocol()` 读取当前值；它不会修改应用状态。

### `void setName(const QString &name)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该房产名称值得查询。
如果查找的名称为空，`QDnsLookup`会尝试解析DNS的根域名。该查询通常在`QDnsLookup::type`设置为`NS`时进行。
注意：该名称将使用 IDNA 编码，这意味着它不适合查询与 DNS-SD 规范兼容的 SRV 记录。

**如何使用：** 调用 `setName(...)` 修改 `name`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setNameserver(const QHostAddress &nameserver)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于 DNS 查询的名称服务器。

**如何使用：** 调用 `setNameserver(...)` 修改 `nameserver`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setNameserver(QDnsLookup::Protocol protocol, const QHostAddress &nameserver, quint16 port = 0)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于 DNS 查询的名称服务器。

**如何使用：** 调用 `setNameserver(...)` 修改 `nameserver`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setNameserverPort(quint16 port)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于 DNS 查询的名称服务器端口号。
值为0表示应使用默认端口`QDnsLookup` `nameserverProtocol()`。
注意：将端口号设置为非默认值（53）可能导致名称解析失败，具体取决于操作系统的限制和防火墙，如果使用的`nameserverProtocol()` `QDnsLookup::Standard`。值得注意的是，`QDnsLookup`使用的 Windows API 无法处理替代端口号。

**如何使用：** 调用 `setNameserverPort(...)` 修改 `nameserverPort`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setNameserverProtocol(QDnsLookup::Protocol protocol)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含发送 DNS 查询时所使用的协议。

**如何使用：** 调用 `setNameserverProtocol(...)` 修改 `nameserverProtocol`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setType(QDnsLookup::Type)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含DNS查找类型。

**如何使用：** 调用 `setType(...)` 修改 `type`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QDnsLookup::Type type() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含DNS查找类型。

**如何使用：** 调用 `type()` 读取当前值；它不会修改应用状态。

### `void nameserverChanged(const QHostAddress &nameserver)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于 DNS 查询的名称服务器。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `nameserver` 的变化，不要把它当作普通函数主动调用。

### `void nameserverPortChanged(quint16 port)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于 DNS 查询的名称服务器端口号。
值为0表示应使用默认端口`QDnsLookup` `nameserverProtocol()`。
注意：将端口号设置为非默认值（53）可能导致名称解析失败，具体取决于操作系统的限制和防火墙，如果使用的`nameserverProtocol()` `QDnsLookup::Standard`。值得注意的是，`QDnsLookup`使用的 Windows API 无法处理替代端口号。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `nameserverPort` 的变化，不要把它当作普通函数主动调用。

### `void nameserverProtocolChanged(QDnsLookup::Protocol protocol)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含发送 DNS 查询时所使用的协议。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `nameserverProtocol` 的变化，不要把它当作普通函数主动调用。

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
