# QHostAddress：IPv4/IPv6 数字地址与子网语义

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHostAddress>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 类型：隐式共享的值类型

## 它解决什么问题

`QHostAddress` 以平台无关的方式保存一个 IPv4 或 IPv6 **数字地址**，并提供地址族、地址分类、IPv6 scope、子网匹配和转换能力。它是 `QTcpSocket`、`QTcpServer`、`QUdpSocket`、`QNetworkDatagram` 等网络 API 的地址值类型。

它不解析主机名，也不做 DNS 查询。`QHostAddress("api.example.com")` 不是解析域名的写法；字符串构造和 `setAddress(const QString &)` 只接受数值 IPv4/IPv6 地址。需要正向或反向名称解析时使用 `QHostInfo`，需要查询特定 DNS 记录时使用 `QDnsLookup`。

## 实际使用场景

- 用数值 IPv4/IPv6 地址连接 socket，或绑定监听地址。
- 判断候选地址是否在本地子网、是否为 loopback、链路本地、多播、广播或私有地址。
- 处理 IPv6 link-local 地址并设置 interface scope ID。
- 在地址白名单、访问控制或服务发现中精确区分严格地址相等与 IPv4/IPv6 兼容形式相等。

地址分类 API 是语义分类工具，不是完整安全策略。比如“私有地址”不自动意味着可信，“全局地址”也不自动意味着公网可路由或安全。

## 构造、解析与特殊地址

```cpp
QHostAddress v4(u"192.0.2.10"_qs);
if (v4.isNull())
    return; // 文本不是有效数值地址

QHostAddress v6(u"fe80::1"_qs);
v6.setScopeId(u"en0"_qs); // 链路本地 IPv6 连接需要 scope

QHostAddress listenAddress(QHostAddress::Any);
```

| `SpecialAddress` | 含义 |
| --- | --- |
| `Null` | 空地址，与默认构造相同。 |
| `Broadcast` | IPv4 全局广播 `255.255.255.255`。 |
| `LocalHost` | IPv4 loopback `127.0.0.1`。 |
| `LocalHostIPv6` | IPv6 loopback `::1`。 |
| `AnyIPv4` | IPv4 未指定地址 `0.0.0.0`。 |
| `AnyIPv6` | IPv6 未指定地址 `::`。 |
| `Any` | 双栈 any 地址语义，用于监听全部 IPv4/IPv6 接口。 |

`Any` 的实际双栈监听结果仍受平台和 socket IPv6-only 设置影响。服务端若必须保证同时覆盖 IPv4 与 IPv6，应按目标平台实际绑定行为验证，而非只凭枚举名称假设。

## 严格比较与宽松比较

`operator==` 使用 `StrictConversion`：IPv4 与任何 IPv6 表示形式都不同。需要逻辑上把兼容形式视作同一个 endpoint 时，明确调用 `isEqual()`：

```cpp
const QHostAddress v4(u"192.0.2.1"_qs);
const QHostAddress mapped(u"::ffff:192.0.2.1"_qs);

const bool strict = (v4 == mapped); // false
const bool tolerant = v4.isEqual(mapped); // true，默认 TolerantConversion
```

`ConversionMode` 可组合：

- `ConvertV4MappedToIPv4`：将 `::ffff:a.b.c.d` 视作 IPv4。
- `ConvertV4CompatToIPv4`：将 `::a.b.c.d` 视作 IPv4。
- `ConvertUnspecifiedAddress`：将 `AnyIPv4`、`AnyIPv6`、`Any` 视作相等。
- `ConvertLocalHost`：将 `::1` 与 `127.0.0.1` 视作相等。
- `TolerantConversion`：启用上述宽松转换。
- `StrictConversion`：完全不转换。

访问控制、缓存 key、连接表和审计日志应先定义哪种地址等价关系是业务正确的。用宽松比较去检查黑名单或去重，可能会让同一 endpoint 有两套可绕过/可冲突的文本表示；用严格比较则可能重复处理同一个逻辑 endpoint。

## IPv6 scope 与接口

IPv6 link-local（通常 `fe80::/10`）和非全局范围地址不能只靠 128 位地址唯一确定路径。连接或发送时必须设置 `scopeId()`，通常是接口名（如 `en0`）或接口 index 字符串。

`setScopeId()` 只对 IPv6 有效。Qt 会将接口名转换为 `QNetworkInterface` 的 index 供系统网络 API 使用。它与 `QNetworkDatagram::setInterfaceIndex()` 共同表达出接口选择；两者若同时设置且冲突，发送接口的结果不应被依赖。

## 子网与地址分类

`isInSubnet()` 用 `(network prefix, prefix length)` 判断成员关系；`parseSubnet()` 可解析如 `192.168.10.0/24`、`2001:db8::/32` 的配置文本并返回网络前缀和长度。IPv4 还支持缩写尾部组件；没有显式掩码时，缩写中给出的 octet 数决定 prefix length。

`isBroadcast()` 只检查全局 IPv4 广播 `255.255.255.255`，不检查某个接口的定向广播地址；后者应从 `QNetworkAddressEntry::broadcast()` 获取。

常用分类关系：

- `isLoopback()`：本机回环地址。
- `isLinkLocal()`：只在本链路可达的地址；IPv6 通常必须带 scope。
- `isMulticast()`：多播地址。
- `isPrivateUse()`：Qt 6.6 起，IPv4 RFC 1918 私有地址或 IPv6 ULA。
- `isUniqueLocalUnicast()`：IPv6 `fc00::/7` 的 ULA；它在 Qt 的 `isGlobal()` 语义下仍可能为真。
- `isSiteLocal()`：旧 IPv6 `fec0::/10`，已弃用；新程序不应依赖，Qt 也视它为 global。

## 转换与序列化边界

`toIPv4Address(&ok)` 仅对 IPv4 或 IPv4-mapped IPv6 有效。忽略 `ok` 会把不可转换地址误读为数值 0。`toIPv6Address()` 对 IPv4 返回其 IPv4-mapped IPv6 形式；这不意味着原始地址族已变成 IPv6。

`toString()` 对 IPv6 使用 RFC 5952 推荐文本格式；对 `Any` 返回 IPv4 表示 `0.0.0.0`。因此字符串不适合单独保存 “Any 是双栈” 或原始输入格式等额外语义。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 枚举 | `SpecialAddress` | `Null`、`Broadcast`、loopback、`AnyIPv4`、`AnyIPv6`、`Any` 等预定义地址。 |
| 枚举 | `ConversionModeFlag` / `ConversionMode` | 控制 `isEqual()` 跨 IPv4/IPv6 兼容表示的折算方式；默认是宽松模式。 |
| 地址族 | `NetworkLayerProtocol` / `protocol()` | 返回 IPv4、IPv6、Any 或 Unknown；在转换前确认地址族。 |
| 构造 | `QHostAddress()` | 创建 `Null` 地址。 |
| 构造 | `QHostAddress(quint32)` | 以数值构造 IPv4 地址。 |
| 构造 | `QHostAddress(const quint8 *)` / `QHostAddress(const Q_IPV6ADDR &)` | 以 16 字节网络字节序或 `Q_IPV6ADDR` 构造 IPv6。 |
| 构造 | `QHostAddress(const sockaddr *)` | 从原生 socket 地址构造；调用方确保指针和地址族有效。 |
| 构造 | `QHostAddress(const QString &)` | 解析数值 IPv4/IPv6 文本，不做 DNS。 |
| 构造 | `QHostAddress(SpecialAddress)` | 构造预定义特殊地址。 |
| 设置 | `setAddress(...)` 的 IPv4、IPv6、`sockaddr`、字符串、特殊地址重载 | 改写当前值；字符串重载以 `bool` 报告解析成功，IPv6 字节指针必须指向 16 个网络字节序字节。 |
| 清空 | `clear()` / `isNull()` | 重置或检查 `Null` 地址与 Unknown 协议。 |
| 文本与数值 | `toString()` | 输出规范化数字地址；不保留输入格式，`Any` 输出 `0.0.0.0`。 |
| 文本与数值 | `toIPv4Address(bool *ok = nullptr)` | 转为 IPv4 整数；只对 IPv4 或 IPv4-mapped IPv6 有效，务必检查 `ok`。 |
| 文本与数值 | `toIPv6Address()` | 返回 16 字节 IPv6；IPv4 会转换为 IPv4-mapped IPv6 表示。 |
| scope | `scopeId()` / `setScopeId(const QString &)` | 获取/设置 IPv6 scope；link-local 连接通常必须设，IPv4 调用 setter 无效果。 |
| 比较 | `isEqual(const QHostAddress &, ConversionMode = TolerantConversion)` | 以指定宽松规则比较地址。 |
| 比较 | `operator==` / `operator!=` | 采用严格转换比较；与 `isEqual()` 默认语义不同。 |
| 比较 | 与 `SpecialAddress` 的 `==` / `!=` | 直接和预定义地址比较。 |
| 子网 | `isInSubnet(const QHostAddress &, int)` | 判断是否属于给定网络前缀；前缀长度应与地址族有效范围匹配。 |
| 子网 | `isInSubnet(const std::pair<QHostAddress, int> &)` | 使用 `parseSubnet()` 返回值直接判断。 |
| 子网 | `parseSubnet(const QString &)` | 解析 `address/prefix` 或掩码形式的子网文本，返回网络前缀和 prefix length。 |
| 分类 | `isLoopback()` / `isGlobal()` / `isLinkLocal()` | 判断常用可达范围；`isGlobal()` 不等价于“公网可用”。 |
| 分类 | `isSiteLocal()` / `isUniqueLocalUnicast()` / `isPrivateUse()` | 区分弃用 site-local、IPv6 ULA 和 IPv4/IPv6 私有用途；`isPrivateUse()` 为 Qt 6.6 起。 |
| 分类 | `isMulticast()` / `isBroadcast()` | 多播或全局 IPv4 广播判断；接口定向广播另查 `QNetworkAddressEntry`。 |
| 值操作 | 复制/移动构造、复制/移动 `operator=`、`swap()` | 值类型管理与高效交换。 |
| 容器 | `qHash(const QHostAddress &, size_t)` | 用作 Qt 哈希容器 key；哈希等价关系应与所选比较策略一致。 |
| 流 | `QDataStream <<` / `>>` | 序列化与反序列化地址值；按 Qt data stream 版本管理持久格式兼容性。 |
| 调试 | `QDebug << address` | 输出调试表示。 |

## 一句话总结

`QHostAddress` 是数字 IP 地址和子网语义的值对象：它不做 DNS，IPv6 link-local 必须关心 scope，而严格 `==` 与默认宽松 `isEqual()` 的差异会直接影响双栈程序的正确性。
