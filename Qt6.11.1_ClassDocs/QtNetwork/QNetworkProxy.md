# QNetworkProxy

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkProxy` 是 Qt Network 的“网络代理”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkProxy` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkProxy>`
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

```cpp
// manager、reply 和事件循环必须在正确线程中存活。
QNetworkReply *reply = manager->get(request);
connect(reply, &QNetworkReply::finished, this, [reply] {
    const QByteArray body = reply->readAll();
    reply->deleteLater();
});
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `flags Capabilities`
- `enum Capability { TunnelingCapability, ListeningCapability, UdpTunnelingCapability, CachingCapability, HostNameLookupCapability, …, SctpListeningCapability }`
- `enum ProxyType { NoProxy, DefaultProxy, Socks5Proxy, HttpProxy, HttpCachingProxy, FtpCachingProxy }`

### 公有函数

- `QNetworkProxy()`
- `QNetworkProxy(QNetworkProxy::ProxyType type, const QString &hostName = QString(), quint16 port = 0, const QString &user = QString(), const QString &password = QString())`
- `QNetworkProxy(const QNetworkProxy &other)`
- `~QNetworkProxy()`
- `QNetworkProxy::Capabilities capabilities() const`
- `bool hasRawHeader(const QByteArray &headerName) const`
- `QVariant header(QNetworkRequest::KnownHeaders header) const`
- `(since 6.8) QHttpHeaders headers() const`
- `QString hostName() const`
- `bool isCachingProxy() const`
- `bool isTransparentProxy() const`
- `QString password() const`
- `quint16 port() const`
- `QByteArray rawHeader(const QByteArray &headerName) const`
- `QList<QByteArray> rawHeaderList() const`
- `void setCapabilities(QNetworkProxy::Capabilities capabilities)`
- `void setHeader(QNetworkRequest::KnownHeaders header, const QVariant &value)`
- `(since 6.8) void setHeaders(QHttpHeaders &&newHeaders)`
- `(since 6.8) void setHeaders(const QHttpHeaders &newHeaders)`
- `void setHostName(const QString &hostName)`
- `void setPassword(const QString &password)`
- `void setPort(quint16 port)`
- `void setRawHeader(const QByteArray &headerName, const QByteArray &headerValue)`
- `void setType(QNetworkProxy::ProxyType type)`
- `void setUser(const QString &user)`
- `void swap(QNetworkProxy &other)`
- `QNetworkProxy::ProxyType type() const`
- `QString user() const`
- `bool operator!=(const QNetworkProxy &other) const`
- `QNetworkProxy & operator=(const QNetworkProxy &other)`
- `bool operator==(const QNetworkProxy &other) const`

### 静态公有成员

- `QNetworkProxy applicationProxy()`
- `void setApplicationProxy(const QNetworkProxy &networkProxy)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QNetworkProxy::Capabilityflags QNetworkProxy::Capabilities`

**作用与语义：**

这些标志表示某个代理服务器支持的功能。
`QNetworkProxy` 在创建对象时默认设置不同的能力（参见 `QNetworkProxy::ProxyType` 中的默认列表）。不过，在创建对象后，可以用 `setCapabilities()` 更改能力。
`QNetworkProxy`支持的功能包括：
- `QNetworkProxy::TunnelingCapability`：`0x0001`;能够开启透明的隧道TCP连接到远程主机。代理服务器逐字中继传输内容，不进行缓存。
- `QNetworkProxy::ListeningCapability`：`0x0002`;能够创建监听套接字并等待来自远程主机的 TCP 连接。
- `QNetworkProxy::UdpTunnelingCapability`：`0x0004`;能够通过代理服务器向远程主机传递UDP数据报。
- `QNetworkProxy::CachingCapability`：`0x0008`;缓存传输内容的能力。该功能针对每个协议和代理类型而定。例如，HTTP 代理可以通过“GET”命令缓存传输的网络数据内容。
- `QNetworkProxy::HostNameLookupCapability`：`0x0010`;能够连接以对远程主机名称进行查找并连接，而非仅要求应用程序进行名称查找并请求连接到IP地址。
- `QNetworkProxy::SctpTunnelingCapability`：`0x00020`;能够向远程主机开放透明的隧道SCTP连接。
- `QNetworkProxy::SctpListeningCapability`：`0x00040`;能够创建监听套接字并等待来自远程主机的SCTP连接。
能力类型是QFlag的typedef<Capability>。它存储能力值的或组合。

### `enum QNetworkProxy::ProxyType`

**作用与语义：**

本枚举描述了Qt中提供的网络代理类型。
Qt 理解两种类型的代理：透明代理和缓存代理。第一类是能够处理任意数据传输的代理，而第二类只能处理特定请求。缓存代理仅适用于可用的特定类。
- `QNetworkProxy::NoProxy`：`2`;不使用代理
- `QNetworkProxy::DefaultProxy`：`0`;代理基于应用代理集确定，使用`setApplicationProxy()`
- `QNetworkProxy::Socks5Proxy`：`1`;`Socks5` 代理使用。
- `QNetworkProxy::HttpProxy`：`3`;使用 HTTP 透明代理
- `QNetworkProxy::HttpCachingProxy`：`4`;仅代理HTTP请求
- `QNetworkProxy::FtpCachingProxy`：`5`;仅代理FTP请求
下表列出了不同的代理类型及其功能。由于每种代理类型都有不同的功能，在选择代理类型之前了解它们非常重要。
- `Proxy type`：描述;默认能力
- `SOCKS 5`：适用于任何连接的通用代理。支持 TCP、UDP、绑定端口（输入连接）及认证;`TunnelingCapability`、`ListeningCapability`、`UdpTunnelingCapability`、`HostNameLookupCapability`
- `HTTP`：通过“CONNECT”命令实现，仅支持外出TCP连接;支持认证;`TunnelingCapability`、`CachingCapability`、`HostNameLookupCapability`
- `Caching-only HTTP`：使用普通 HTTP 命令实现，仅在 HTTP 请求上下文中有用（参见 `QNetworkAccessManager`）;`CachingCapability`，`HostNameLookupCapability`
- `Caching FTP`：通过FTP代理实现，仅在FTP请求中有用（参见 `QNetworkAccessManager`）;`CachingCapability`，`HostNameLookupCapability`
另外请注意，你不应该把应用默认代理（`setApplicationProxy()`）设置为没有`TunnelingCapability`功能的代理。如果设置了，`QTcpSocket`就不会知道如何开启连接。

### `QNetworkProxy::QNetworkProxy()`

**作用与语义：**

构建一个带有`DefaultProxy`类型的QNetworkProxy。
代理类型由`applicationProxy()`决定，默认为`NoProxy`或如果配置了系统范围的代理。

### `QNetworkProxy::QNetworkProxy(QNetworkProxy::ProxyType type, const QString &hostName = QString(), quint16 port = 0, const QString &user = QString(), const QString &password = QString())`

**作用与语义：**

构建包含`type`、`hostName`、`port`、`user`和`password`的QNetworkProxy。
代理类型`type`的默认能力是自动设置的。

### `QNetworkProxy::QNetworkProxy(const QNetworkProxy &other)`

**作用与语义：**

复制了`other`。

### `[noexcept] QNetworkProxy::~QNetworkProxy()`

**作用与语义：**

摧毁`QNetworkProxy`物体。

### `[static] QNetworkProxy QNetworkProxy::applicationProxy()`

**作用与语义：**

返回应用级网络代理。
如果`QAbstractSocket`或`QTcpSocket`具有`QNetworkProxy::DefaultProxy`类型，则使用该函数返回的`QNetworkProxy`。

### `QNetworkProxy::Capabilities QNetworkProxy::capabilities() const`

**作用与语义：**

返回该代理服务器的功能。

### `bool QNetworkProxy::hasRawHeader(const QByteArray &headerName) const`

**作用与语义：**

如果该代理正在使用原始头部`headerName`，返回`true`。如果代理类型不是 `HttpProxy` 或 `HttpCachingProxy`，返回 `false`。

### `QVariant QNetworkProxy::header(QNetworkRequest::KnownHeaders header) const`

**作用与语义：**

如果该代理正在使用已知网络头部`header`，返回该值。如果不存在，返回QVariant()（即无效变体）。

### `[since 6.8] QHttpHeaders QNetworkProxy::headers() const`

**作用与语义：**

返回该网络请求中设置的头部。
如果代理不是类型`HttpProxy`或类型`HttpCachingProxy`，则返回默认构造`QHttpHeaders`。

### `QString QNetworkProxy::hostName() const`

**作用与语义：**

返回代理主机的主机名称。

### `bool QNetworkProxy::isCachingProxy() const`

**作用与语义：**

如果该代理支持`QNetworkProxy::CachingCapability`功能，返回`true`。
在Qt 4.4中，该能力与代理类型绑定，但自Qt 4.5起，可以通过调用`setCapabilities()`来移除代理缓存功能。

### `bool QNetworkProxy::isTransparentProxy() const`

**作用与语义：**

如果该代理支持TCP连接的透明隧道，返回`true`。这与`QNetworkProxy::TunnelingCapability`能力相符。
在Qt 4.4中，该能力与代理类型绑定，但自Qt 4.5起，可以通过调用`setCapabilities()`来移除代理缓存功能。

### `QString QNetworkProxy::password() const`

**作用与语义：**

返回用于认证的密码。

### `quint16 QNetworkProxy::port() const`

**作用与语义：**

返回代理主机的端口。

### `QByteArray QNetworkProxy::rawHeader(const QByteArray &headerName) const`

**作用与语义：**

返回原始的首部`headerName`。如果不存在此类头部或代理类型不属于`HttpProxy`或`HttpCachingProxy`，则返回一个空的`QByteArray`，这可能与存在但无内容的头部无法区分（使用`hasRawHeader()`来判断该头是否存在）。
原始头部可以用`setRawHeader()`或`setHeader()`设置。

### `QList<QByteArray> QNetworkProxy::rawHeaderList() const`

**作用与语义：**

返回该网络代理中设置的所有原始头部列表。列表按头部设置顺序排列。
如果代理不是类型`HttpProxy`或`HttpCachingProxy`，则返回空`QList`。

### `[static] void QNetworkProxy::setApplicationProxy(const QNetworkProxy &networkProxy)`

**作用与语义：**

将应用级网络代理设置为`networkProxy`。
如果`QAbstractSocket`或`QTcpSocket`具有`QNetworkProxy::DefaultProxy`类型，则使用带有该函数的`QNetworkProxy`集。如果你想更灵活地决定使用哪个代理，可以使用`QNetworkProxyFactory`类。
设置带有该功能的默认代理值会覆盖用 `QNetworkProxyFactory::setApplicationProxyFactory` 设置的应用代理，并禁用系统代理的使用。

### `void QNetworkProxy::setCapabilities(QNetworkProxy::Capabilities capabilities)`

**作用与语义：**

将该代理的能力设置为`capabilities`。

### `void QNetworkProxy::setHeader(QNetworkRequest::KnownHeaders header, const QVariant &value)`

**作用与语义：**

将已知`header`头的值设置为`value`，覆盖之前设置的任何头部。该操作还会设置等效的原始HTTP头。
如果代理不是类型`HttpProxy`或`HttpCachingProxy`，则无效。

### `[since 6.8] void QNetworkProxy::setHeaders(QHttpHeaders &&newHeaders)`

**作用与语义：**

将`newHeaders`设置为该网络请求中的头部，覆盖之前设置的任何头部。
如果某些头对应已知头，则会解析这些值，并设置相应的解析形式。
如果代理不是类型`HttpProxy`或`HttpCachingProxy`，则无效。

### `[since 6.8] void QNetworkProxy::setHeaders(const QHttpHeaders &newHeaders)`

**作用与语义：**

将`newHeaders`设置为该网络请求中的头部，覆盖之前设置的任何头部。
如果某些头对应已知头，则会解析这些值，并设置相应的解析形式。
如果代理不是类型`HttpProxy`或`HttpCachingProxy`，则无效。

### `void QNetworkProxy::setHostName(const QString &hostName)`

**作用与语义：**

将代理主机的主机名称设置为`hostName`。

### `void QNetworkProxy::setPassword(const QString &password)`

**作用与语义：**

将代理认证密码设置为`password`。

### `void QNetworkProxy::setPort(quint16 port)`

**作用与语义：**

将代理主机的端口设置为`port`。

### `void QNetworkProxy::setRawHeader(const QByteArray &headerName, const QByteArray &headerValue)`

**作用与语义：**

将`headerName`的头设置为值为`headerValue`。如果`headerName`对应于已知头部（见`QNetworkRequest::KnownHeaders`），则会解析原始格式，并设置相应的“煮熟”头部。
还将已知的LastModifiedHeader设置为解析日期的`QDateTime`对象。
注意：设置同一个头部重复会覆盖之前的设置。为了实现多个同名 HTTP 头的行为，你应将两个值连接起来，用逗号（“，”）分隔，并设置一个单一原始头部。
如果代理不是类型`HttpProxy`或`HttpCachingProxy`，则无效。

**官方示例：**

```cpp
 request.setRawHeader(QByteArray("Last-Modified"), QByteArray("Sun, 06 Nov 1994 08:49:37 GMT"));
```

### `void QNetworkProxy::setType(QNetworkProxy::ProxyType type)`

**作用与语义：**

将该实例的代理类型设置为`type`。
注意，如果已有`setCapabilities()`设置了任何能力，改变代理类型并不会改变该`QNetworkProxy`对象所包含的能力集合。

### `void QNetworkProxy::setUser(const QString &user)`

**作用与语义：**

将代理认证的用户名设置为`user`。

### `[noexcept] void QNetworkProxy::swap(QNetworkProxy &other)`

**作用与语义：**

将该网络代理实例与`other`交换。此操作非常快速且从未失败。

### `QNetworkProxy::ProxyType QNetworkProxy::type() const`

**作用与语义：**

返回该实例的代理类型。

### `QString QNetworkProxy::user() const`

**作用与语义：**

返回用于认证的用户名。

### `bool QNetworkProxy::operator!=(const QNetworkProxy &other) const`

**作用与语义：**

比较该网络代理的价值与`other`，如果两者不同，`true`返回。

### `QNetworkProxy &QNetworkProxy::operator=(const QNetworkProxy &other)`

**作用与语义：**

将网络代理`other`的值分配给该网络代理。

### `bool QNetworkProxy::operator==(const QNetworkProxy &other) const`

**作用与语义：**

将该网络代理的价值与`other`进行比较，并在两者相同（代理类型、服务器以及用户名和密码）时返回`true`。

### `flags Capabilities`

**作用与语义：**

这些标志表示某个代理服务器支持的功能。
`QNetworkProxy` 在创建对象时默认设置不同的能力（参见 `QNetworkProxy::ProxyType` 中的默认列表）。不过，在创建对象后，可以用 `setCapabilities()` 更改能力。
`QNetworkProxy`支持的功能包括：
- `QNetworkProxy::TunnelingCapability`：`0x0001`;能够开启透明的隧道TCP连接到远程主机。代理服务器逐字中继传输内容，不进行缓存。
- `QNetworkProxy::ListeningCapability`：`0x0002`;能够创建监听套接字并等待来自远程主机的 TCP 连接。
- `QNetworkProxy::UdpTunnelingCapability`：`0x0004`;能够通过代理服务器向远程主机传递UDP数据报。
- `QNetworkProxy::CachingCapability`：`0x0008`;缓存传输内容的能力。该功能针对每个协议和代理类型而定。例如，HTTP 代理可以通过“GET”命令缓存传输的网络数据内容。
- `QNetworkProxy::HostNameLookupCapability`：`0x0010`;能够连接以对远程主机名称进行查找并连接，而非仅要求应用程序进行名称查找并请求连接到IP地址。
- `QNetworkProxy::SctpTunnelingCapability`：`0x00020`;能够向远程主机开放透明的隧道SCTP连接。
- `QNetworkProxy::SctpListeningCapability`：`0x00040`;能够创建监听套接字并等待来自远程主机的SCTP连接。
能力类型是QFlag的typedef<Capability>。它存储能力值的或组合。

### `enum Capability { TunnelingCapability, ListeningCapability, UdpTunnelingCapability, CachingCapability, HostNameLookupCapability, …, SctpListeningCapability }`

**作用与语义：**

这些标志表示某个代理服务器支持的功能。
`QNetworkProxy` 在创建对象时默认设置不同的能力（参见 `QNetworkProxy::ProxyType` 中的默认列表）。不过，在创建对象后，可以用 `setCapabilities()` 更改能力。
`QNetworkProxy`支持的功能包括：
- `QNetworkProxy::TunnelingCapability`：`0x0001`;能够开启透明的隧道TCP连接到远程主机。代理服务器逐字中继传输内容，不进行缓存。
- `QNetworkProxy::ListeningCapability`：`0x0002`;能够创建监听套接字并等待来自远程主机的 TCP 连接。
- `QNetworkProxy::UdpTunnelingCapability`：`0x0004`;能够通过代理服务器向远程主机传递UDP数据报。
- `QNetworkProxy::CachingCapability`：`0x0008`;缓存传输内容的能力。该功能针对每个协议和代理类型而定。例如，HTTP 代理可以通过“GET”命令缓存传输的网络数据内容。
- `QNetworkProxy::HostNameLookupCapability`：`0x0010`;能够连接以对远程主机名称进行查找并连接，而非仅要求应用程序进行名称查找并请求连接到IP地址。
- `QNetworkProxy::SctpTunnelingCapability`：`0x00020`;能够向远程主机开放透明的隧道SCTP连接。
- `QNetworkProxy::SctpListeningCapability`：`0x00040`;能够创建监听套接字并等待来自远程主机的SCTP连接。
能力类型是QFlag的typedef<Capability>。它存储能力值的或组合。

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

`QNetworkProxy` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
