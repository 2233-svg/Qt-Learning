# QHostAddress

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** IP 地址值类型，负责 IPv4/IPv6 地址的解析、比较和格式化。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QHostAddress`：IP 地址值类型，负责 IPv4/IPv6 地址的解析、比较和格式化。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QHostAddress>`
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

创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

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

- `flags ConversionMode`
- `enum ConversionModeFlag { StrictConversion, ConvertV4MappedToIPv4, ConvertV4CompatToIPv4, ConvertLocalHost, ConvertUnspecifiedAddress, TolerantConversion }`
- `enum SpecialAddress { Null, LocalHost, LocalHostIPv6, Broadcast, AnyIPv4, …, Any }`

### 公有函数

- `QHostAddress()`
- `QHostAddress(QHostAddress::SpecialAddress address)`
- `QHostAddress(const QString &address)`
- `QHostAddress(const Q_IPV6ADDR &ip6Addr)`
- `QHostAddress(const quint8 *ip6Addr)`
- `QHostAddress(const sockaddr *sockaddr)`
- `QHostAddress(quint32 ip4Addr)`
- `QHostAddress(const QHostAddress &address)`
- `(since 6.8) QHostAddress(QHostAddress &&other)`
- `~QHostAddress()`
- `void clear()`
- `bool isBroadcast() const`
- `bool isEqual(const QHostAddress &other, QHostAddress::ConversionMode mode = TolerantConversion) const`
- `bool isGlobal() const`
- `bool isInSubnet(const QHostAddress &subnet, int netmask) const`
- `bool isInSubnet(const std::pair<QHostAddress, int> &subnet) const`
- `bool isLinkLocal() const`
- `bool isLoopback() const`
- `bool isMulticast() const`
- `bool isNull() const`
- `(since 6.6) bool isPrivateUse() const`
- `bool isSiteLocal() const`
- `bool isUniqueLocalUnicast() const`
- `int protocol() const`
- `QString scopeId() const`
- `void setAddress(quint32 ip4Addr)`
- `void setAddress(QHostAddress::SpecialAddress address)`
- `bool setAddress(const QString &address)`
- `void setAddress(const Q_IPV6ADDR &ip6Addr)`
- `void setAddress(const quint8 *ip6Addr)`
- `void setAddress(const sockaddr *sockaddr)`
- `void setScopeId(const QString &id)`
- `void swap(QHostAddress &other)`
- `quint32 toIPv4Address(bool *ok = nullptr) const`
- `Q_IPV6ADDR toIPv6Address() const`
- `QString toString() const`
- `bool operator!=(QHostAddress::SpecialAddress other) const`
- `bool operator!=(const QHostAddress &other) const`
- `QHostAddress & operator=(QHostAddress::SpecialAddress address)`
- `QHostAddress & operator=(const QHostAddress &address)`
- `bool operator==(QHostAddress::SpecialAddress other) const`
- `bool operator==(const QHostAddress &other) const`

### 静态公有成员

- `std::pair<QHostAddress, int> parseSubnet(const QString &subnet)`

### 相关非成员函数

- `size_t qHash(const QHostAddress &key, size_t seed = 0)`
- `bool operator!=(QHostAddress::SpecialAddress lhs, const QHostAddress &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QHostAddress &address)`
- `bool operator==(QHostAddress::SpecialAddress lhs, const QHostAddress &rhs)`
- `QDataStream & operator>>(QDataStream &in, QHostAddress &address)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QHostAddress::ConversionModeFlagflags QHostAddress::ConversionMode`

**作用与语义：**

- `QHostAddress::StrictConversion`: `0`；在比较两个不同协议的 `QHostAddress` 对象时，不将 IPv6 地址转换为 IPv4，因此它们将始终被视为不同。
- `QHostAddress::ConvertV4MappedToIPv4`: `1`；在比较时转换 IPv4 映射的 IPv6 地址 (RFC 4291 第 2.5.5.2 条)。因此 `QHostAddress`("::ffff:192.168.1.1") 将等同于 `QHostAddress`("192.168.1.1")。
- `QHostAddress::ConvertV4CompatToIPv4`: `2`；在比较时转换 IPv4 兼容的 IPv6 地址 (RFC 4291 第 2.5.5.1 条)。因此 `QHostAddress`("::192.168.1.1") 将等同于 `QHostAddress`("192.168.1.1")。
- `QHostAddress::ConvertLocalHost`: `8`；在比较时将 IPv6 回环地址转换为其 IPv4 等效地址。因此，例如 `QHostAddress`("::1") 将等同于 `QHostAddress`("127.0.0.1")。
- `QHostAddress::ConvertUnspecifiedAddress`: `4`；所有未指定的地址将相等，即 `AnyIPv4`、`AnyIPv6` 和任意地址。
- `QHostAddress::TolerantConversion`: `0xff`；设置前面三项标志。
ConversionMode 类型是 QFlags<ConversionModeFlag> 的 typedef。它存储 ConversionModeFlag 值的 OR 组合。

### `QHostAddress::QHostAddress()`

**作用与语义：**

构造一个空主机地址对象，即对任何主机或接口都无效的地址。

### `QHostAddress::QHostAddress(QHostAddress::SpecialAddress address)`

**作用与语义：**

为`address`构造一个QHostAddress对象。

### `[explicit] QHostAddress::QHostAddress(const QString &address)`

**作用与语义：**

基于字符串`address`构造IPv4或IPv6地址（例如，“127.0.0.1”）。

### `[explicit] QHostAddress::QHostAddress(const Q_IPV6ADDR &ip6Addr)`

**作用与语义：**

构建带有IPv6地址`ip6Addr`的主机地址对象。

### `[explicit] QHostAddress::QHostAddress(const quint8 *ip6Addr)`

**作用与语义：**

构建带有IPv6地址`ip6Addr`的主机地址对象。
`ip6Addr`必须是网络字节序（大端序）的16字节阵列。

### `[explicit] QHostAddress::QHostAddress(const sockaddr *sockaddr)`

**作用与语义：**

利用本地结构`sockaddr`指定的地址构造IPv4或IPv6地址。

### `[explicit] QHostAddress::QHostAddress(quint32 ip4Addr)`

**作用与语义：**

构建带有IPv4地址`ip4Addr`的主机地址对象。

### `QHostAddress::QHostAddress(const QHostAddress &address)`

**作用与语义：**

构建给定`address`的副本。

### `[constexpr noexcept, since 6.8] QHostAddress::QHostAddress(QHostAddress &&other)`

**作用与语义：**

从`other`移动构建一个新的QHost地址。
注意：移除对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `[noexcept] QHostAddress::~QHostAddress()`

**作用与语义：**

销毁主机地址对象。

### `void QHostAddress::clear()`

**作用与语义：**

将主机地址设置为空，并将协议设置为`QAbstractSocket::UnknownNetworkLayerProtocol`。

### `bool QHostAddress::isBroadcast() const`

**作用与语义：**

如果地址是IPv4广播地址，返回`true`，否则`false`返回。IPv4广播地址为255.255.255.255。
注意，该函数不会返回IPv4网络本地广播地址的true。为此，请使用`QNetworkInterface`获取本地机器的广播地址。

### `bool QHostAddress::isEqual(const QHostAddress &other, QHostAddress::ConversionMode mode = TolerantConversion) const`

**作用与语义：**

如果该主机地址与给出的`other`地址相同，返回`true`;否则返回`false`。
参数`mode`控制不同协议地址之间执行哪些转换。如果没有`mode`，默认执行`TolerantConversion`。

### `bool QHostAddress::isGlobal() const`

**作用与语义：**

如果地址是IPv4或IPv6全局地址，返回`true`，否则`false`。全局地址是指不为特殊用途（如环回或多播）或未来用途保留的地址。
请注意，IPv6 唯一的本地单播地址被视为全局地址（参见 `isUniqueLocalUnicast()`），RFC 1918 保留给本地网络的 IPv4 地址也被视为全局地址。
还要注意，IPv6 站点本地地址已被弃用，在新应用中应视为全局地址。该功能对站点本地地址同样适用。

### `bool QHostAddress::isInSubnet(const QHostAddress &subnet, int netmask) const`

**作用与语义：**

如果该IP属于网络前缀`subnet`和网掩码`netmask`描述的子网，返回`true`。
`netmask`参数是前缀长度——用于识别地址网络部分的前导位数。IPv4的有效值范围为0到32;IPv6的有效值范围为0到128。
如果一个IP位于该子网中最低和最高的地址之间，则该IP被视为属于该子网。在IP版本4中，最低地址是网络地址，最高地址是广播地址。
`subnet`参数不必是实际的网络地址（子网中最低的地址）。它可以是属于该子网的任何有效IP。特别地，如果它等于该对象持有的IP地址，该函数总是返回true（前提是前缀长度是有效值）。

### `bool QHostAddress::isInSubnet(const std::pair<QHostAddress, int> &subnet) const`

**作用与语义：**

如果该IP属于`subnet`描述的子网，返回`true`。`subnet`的`QHostAddress`成员包含网络前缀，整数（第二）成员包含网络掩码（前缀长度）。

### `bool QHostAddress::isLinkLocal() const`

**作用与语义：**

如果地址是IPv4或IPv6链路本地地址，返回`true`，否则`false`返回。
IPv4 链路本地地址是网络 169.254.0.0/16 中的地址。IPv6 链路本地地址是网络 fe80：：/10 中的地址。更多信息请参见 IANA IPv6 地址空间注册表。

### `bool QHostAddress::isLoopback() const`

**作用与语义：**

如果地址是IPv6环回地址，还是任一IPv4环回地址，返回`true`。

### `bool QHostAddress::isMulticast() const`

**作用与语义：**

如果地址是IPv4或IPv6多播地址，返回`true`，否则`false`。

### `bool QHostAddress::isNull() const`

**作用与语义：**

如果该主机地址对任何主机或接口都无效，返回`true`。
默认构造函数会创建一个空地址。

### `[since 6.6] bool QHostAddress::isPrivateUse() const`

**作用与语义：**

返回`true`地址是IPv6唯一的本地单播地址，还是RFC 1918为本地网络保留的IPv4地址，否则`false`。

### `bool QHostAddress::isSiteLocal() const`

**作用与语义：**

如果地址是IPv6站点本地地址，返回`true`，否则`false`返回。
IPv6 站点本地地址是指网络中的 fec0：：/10。更多信息请参见 IANA IPv6 地址空间注册表。
IPv6 站点本地地址已被弃用，不应依赖于新应用。新应用不应依赖该功能，应将站点本地地址视为全局地址（这也是 `isGlobal()` 返回为真的原因）。站点本地地址已被唯一本地地址（ULA）取代。

### `bool QHostAddress::isUniqueLocalUnicast() const`

**作用与语义：**

如果地址是IPv6唯一的本地单播地址，返回`true`，否则`false`返回。
IPv6 唯一的本地单播地址是网络 fc00：：/7 中的一个地址。更多信息请参见 IANA IPv6 地址空间注册表。
注意，唯一本地单播地址也算作全局地址。RFC 4193 规定，实际上，“应用程序可以将这些地址视为全局范围地址。”只有路由器需要注意这个区别。

### `[static] std::pair<QHostAddress, int> QHostAddress::parseSubnet(const QString &subnet)`

**作用与语义：**

解析`subnet`中包含的IP和子网信息，返回该网络的网络前缀及其前缀长度。
IP 地址和网罩必须用斜杠（/）分隔。
该函数支持以下参数：
- 123.123.123/n 其中 n 是介于0到32之间的任意值
- 123.123.123.123/255.255.255.255
- <ipv6-address>/n 其中 n 是任意介于0到128之间的值
对于 IP 版本 4，该函数也接受缺少尾部组件（例如少于 4 个八位元组，如“192.168.1”），后面或不加点。如果网罩也缺失，则设置为实际传递的八位元组数（在上述示例中，3 个八位元组为 24）。

### `int QHostAddress::protocol() const`

**作用与语义：**

返回主机地址的网络层协议。

### `QString QHostAddress::scopeId() const`

**作用与语义：**

返回IPv6地址的范围ID。对于IPv4地址，或者地址不包含范围ID，返回空`QString`。
IPv6 范围 ID 规定了非全局 IPv6 地址的可达范围，限制了该地址可使用的区域。所有 IPv6 地址都关联到这样的可达范围。范围 ID 用于消除那些不保证全局唯一性的地址。
IPv6规定了以下四个可达层级：
- 节点本地：仅用于与同一接口上服务通信的地址（例如环回接口“：：1”）。
- 链路本地：网络接口（链路）本地的地址。你的主机上每个IPv6接口总有一个链路本地地址。链路本地地址（“fe80...”）由本地网络适配器的MAC地址生成，且不保证是唯一。
- 全球地址：用于全球可路由地址，例如互联网上的公共服务器。
在使用链路本地或站点本地地址进行IPv6连接时，必须指定范围ID。链路本地地址的范围ID通常与接口名称（例如，“eth0”、“en1”）或编号（例如，“1”、“2”）相同。

### `void QHostAddress::setAddress(quint32 ip4Addr)`

**作用与语义：**

设置`ip4Addr`指定的IPv4地址。

### `void QHostAddress::setAddress(QHostAddress::SpecialAddress address)`

**作用与语义：**

设置`address`指定的特殊地址。

### `bool QHostAddress::setAddress(const QString &address)`

**作用与语义：**

设置由`address`指定的字符串表示（例如“127.0.0.1”）指定的IPv4或IPv6地址。如果地址成功解析，返回`true`并设置地址;否则返回`false`。

### `void QHostAddress::setAddress(const Q_IPV6ADDR &ip6Addr)`

**作用与语义：**

设置`ip6Addr`指定的IPv6地址。

### `void QHostAddress::setAddress(const quint8 *ip6Addr)`

**作用与语义：**

设置`ip6Addr`指定的IPv6地址。
`ip6Addr`必须是网络字节顺序为16字节的数组（高阶字节优先）。

### `void QHostAddress::setAddress(const sockaddr *sockaddr)`

**作用与语义：**

设置本地结构指定的IPv4或IPv6地址`sockaddr`。返回`true`地址，如果地址成功解析，则设置地址;否则返回`false`。

### `void QHostAddress::setScopeId(const QString &id)`

**作用与语义：**

将地址的IPv6范围ID设置为`id`。如果地址协议不是IPv6，这个函数不起作用。范围ID可以设置为接口名称（如“eth0”或“en1”）或表示接口索引的整数。如果`id`是接口名称，`QtNetwork`会在调用操作系统网络函数前使用`QNetworkInterface::interfaceIndexFromName()`转换为接口索引。

### `[noexcept] void QHostAddress::swap(QHostAddress &other)`

**作用与语义：**

将该主机地址与`other`交换。此操作非常快速且从未失败。

### `quint32 QHostAddress::toIPv4Address(bool *ok = nullptr) const`

**作用与语义：**

它会以号码的形式返回IPv4地址。
例如，如果地址是127.0.0.1，返回的值是2130706433（即0x7f000001）。
如果`protocol()`是`IPv4Protocol`，或者协议是`IPv6Protocol`，且IPv6地址是IPv4映射地址（RFC4291），这个值是有效的。在这种情况下，`ok`将设置为true。否则，它将被设置为false。

### `Q_IPV6ADDR QHostAddress::toIPv6Address() const`

**作用与语义：**

返回IPv6地址作为Q_IPV6ADDR结构。该结构由16个无符号字符组成。
如果`protocol()`是`IPv6Protocol`，该值有效。如果协议是`IPv4Protocol`，则该地址作为IPv4映射的IPv6地址返回。（RFC4291）。

**官方示例：**

```cpp
 Q_IPV6ADDR addr = hostAddr.toIPv6Address();
 // addr contains 16 unsigned characters

 for (int i = 0; i < 16; ++i) {
     // process addr[i]
 }
```

### `QString QHostAddress::toString() const`

**作用与语义：**

返回地址为字符串。
例如，如果地址是IPv4地址127.0.0.1，返回的字符串是“127.0.0.1”。对于IPv6，字符串格式将遵循RFC5952推荐。对于`QHostAddress::Any`，返回其IPv4地址（“0.0.0.0”）。

### `bool QHostAddress::operator!=(QHostAddress::SpecialAddress other) const`

**作用与语义：**

如果该主机地址与给定的`other`地址不同，返回`true`;否则返回`false`。

### `bool QHostAddress::operator!=(const QHostAddress &other) const`

**作用与语义：**

如果该主机地址与给定的`other`地址不同，返回`true`;否则返回`false`。

### `QHostAddress &QHostAddress::operator=(QHostAddress::SpecialAddress address)`

**作用与语义：**

将特殊地址`address`分配给该对象，并返回对该对象的引用。

### `QHostAddress &QHostAddress::operator=(const QHostAddress &address)`

**作用与语义：**

将另一个主机`address`分配给该对象，并返回对该对象的引用。

### `bool QHostAddress::operator==(QHostAddress::SpecialAddress other) const`

**作用与语义：**

如果该主机地址与给出的`other`地址相同，则返回`true`;否则返回`false`。

### `bool QHostAddress::operator==(const QHostAddress &other) const`

**作用与语义：**

如果该主机地址与给出的`other`地址相同，返回`true`;否则返回`false`。该操作符仅调用`isEqual`（其他，`StrictConversion`）。

### `[noexcept] size_t qHash(const QHostAddress &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `bool operator!=(QHostAddress::SpecialAddress lhs, const QHostAddress &rhs)`

**作用与语义：**

如果特殊地址 `lhs` 与主机地址 `rhs` 相同，则返回 `false`；否则返回 `true`。

### `QDataStream &operator<<(QDataStream &out, const QHostAddress &address)`

**作用与语义：**

将主机地址`address`写入流`out`并返回流的引用。

### `bool operator==(QHostAddress::SpecialAddress lhs, const QHostAddress &rhs)`

**作用与语义：**

如果特殊地址`lhs`与主机地址`rhs`相同，返回`true`;否则返回`false`。

### `QDataStream &operator>>(QDataStream &in, QHostAddress &address)`

**作用与语义：**

从流`in`读取主机地址`address`并返回流的引用。

### `flags ConversionMode`

**作用与语义：**

- `QHostAddress::StrictConversion`: `0`；在比较两个不同协议的 `QHostAddress` 对象时，不将 IPv6 地址转换为 IPv4，因此它们将始终被视为不同。
- `QHostAddress::ConvertV4MappedToIPv4`: `1`；在比较时转换 IPv4 映射的 IPv6 地址 (RFC 4291 第 2.5.5.2 条)。因此 `QHostAddress`("::ffff:192.168.1.1") 将等同于 `QHostAddress`("192.168.1.1")。
- `QHostAddress::ConvertV4CompatToIPv4`: `2`；在比较时转换 IPv4 兼容的 IPv6 地址 (RFC 4291 第 2.5.5.1 条)。因此 `QHostAddress`("::192.168.1.1") 将等同于 `QHostAddress`("192.168.1.1")。
- `QHostAddress::ConvertLocalHost`: `8`；在比较时将 IPv6 回环地址转换为其 IPv4 等效地址。因此，例如 `QHostAddress`("::1") 将等同于 `QHostAddress`("127.0.0.1")。
- `QHostAddress::ConvertUnspecifiedAddress`: `4`；所有未指定的地址将相等，即 `AnyIPv4`、`AnyIPv6` 和任意地址。
- `QHostAddress::TolerantConversion`: `0xff`；设置前面三项标志。
ConversionMode 类型是 QFlags<ConversionModeFlag> 的 typedef。它存储 ConversionModeFlag 值的 OR 组合。

### `enum ConversionModeFlag { StrictConversion, ConvertV4MappedToIPv4, ConvertV4CompatToIPv4, ConvertLocalHost, ConvertUnspecifiedAddress, TolerantConversion }`

**作用与语义：**

- `QHostAddress::StrictConversion`: `0`；在比较两个不同协议的 `QHostAddress` 对象时，不将 IPv6 地址转换为 IPv4，因此它们将始终被视为不同。
- `QHostAddress::ConvertV4MappedToIPv4`: `1`；在比较时转换 IPv4 映射的 IPv6 地址 (RFC 4291 第 2.5.5.2 条)。因此 `QHostAddress`("::ffff:192.168.1.1") 将等同于 `QHostAddress`("192.168.1.1")。
- `QHostAddress::ConvertV4CompatToIPv4`: `2`；在比较时转换 IPv4 兼容的 IPv6 地址 (RFC 4291 第 2.5.5.1 条)。因此 `QHostAddress`("::192.168.1.1") 将等同于 `QHostAddress`("192.168.1.1")。
- `QHostAddress::ConvertLocalHost`: `8`；在比较时将 IPv6 回环地址转换为其 IPv4 等效地址。因此，例如 `QHostAddress`("::1") 将等同于 `QHostAddress`("127.0.0.1")。
- `QHostAddress::ConvertUnspecifiedAddress`: `4`；所有未指定的地址将相等，即 `AnyIPv4`、`AnyIPv6` 和任意地址。
- `QHostAddress::TolerantConversion`: `0xff`；设置前面三项标志。
ConversionMode 类型是 QFlags<ConversionModeFlag> 的 typedef。它存储 ConversionModeFlag 值的 OR 组合。

### `enum SpecialAddress { Null, LocalHost, LocalHostIPv6, Broadcast, AnyIPv4, …, Any }`

**作用与语义：**

- `QHostAddress::Null`: `0`；空地址对象。等同于 `QHostAddress()`。另请参见 `QHostAddress::isNull()`。
- `QHostAddress::LocalHost`: `2`；IPv4 本地主机地址。等同于 `QHostAddress`("127.0.0.1")。
- `QHostAddress::LocalHostIPv6`: `3`；IPv6 本地主机地址。等同于 `QHostAddress`("::1")。
- `QHostAddress::Broadcast`: `1`；IPv4 广播地址。等同于 `QHostAddress`("255.255.255.255")。
- `QHostAddress::AnyIPv4`: `6`；IPv4 任意地址。等同于 `QHostAddress`("0.0.0.0")。绑定此地址的套接字将仅在 IPv4 接口上监听。
- `QHostAddress::AnyIPv6`: `5`；IPv6 任意地址。等同于 `QHostAddress`("::")。绑定此地址的套接字将仅在 IPv6 接口上监听。
- `QHostAddress::Any`: `4`；双栈任意地址。绑定此地址的套接字将在 IPv4 和 IPv6 接口上都监听。

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

`QHostAddress` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
