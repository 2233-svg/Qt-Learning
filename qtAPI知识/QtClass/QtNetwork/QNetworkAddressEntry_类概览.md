# QNetworkAddressEntry：网络接口上的一个 IP 地址及其属性

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkAddressEntry>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 类型：值类型，由 `QNetworkInterface::addressEntries()` 返回

## 它解决什么问题

`QNetworkAddressEntry` 表示一个接口上的单个 IPv4 或 IPv6 地址，并将它与子网掩码/前缀长度、IPv4 广播地址、DNS 发布适宜性和地址生命周期绑定在一起。

单独的 `QHostAddress` 只能说明“是什么地址”；它不能说明该地址属于哪个子网、是否仍是首选源地址、何时失效，或是否应向 DNS 发布。需要做接口选择、地址发布或 IPv6 生命周期感知时，应使用此类型。

## 实际使用场景

- 枚举接口地址，选择与目标子网相匹配的本机地址。
- UDP 绑定或多播发送前，找到正确的接口/地址与前缀信息。
- 服务发现或动态 DNS 注册时，排除临时 IPv6 隐私地址。
- 网络诊断界面显示地址、前缀、广播地址和剩余有效期。

它是一个快照值，不会持续追踪系统配置变化。接口地址可能在返回后马上因 DHCP、VPN、Wi-Fi 切换或 IPv6 临时地址轮换而失效；长期任务应在实际使用前重新枚举或处理 socket 失败。

## IP、子网和广播

`ip()` 读取地址，`netmask()` 与 `prefixLength()` 表示其子网：

- IPv4 前缀长度应为 0 到 32；IPv6 为 0 到 128。
- `setNetmask()` 会同步计算 prefix length；`setPrefixLength()` 也会同步构造 netmask。
- 无法确定 prefix 时，`prefixLength()` 返回 `-1`，`netmask()` 为 null address。
- `broadcast()` 仅对 IPv4 有意义，通常可由 IP 与 netmask 推导；IPv6 没有广播概念，返回空地址，应使用相应多播地址。

设置不适合当前地址族的前缀长度，或设置不合法的长度，等价于设为 `-1`，即“不存在/未知前缀”。不要把这个对象当作系统网络配置的写入接口：修改它只改当前值对象，不会改变操作系统接口设置。

## DNS 发布适宜性

`dnsEligibility()` 表示系统或 Qt 对该地址是否适合发布到 DNS 等名称解析服务的判断：

| 状态 | 处理建议 |
| --- | --- |
| `DnsEligible` | 可作为候选发布地址，但应用仍需验证地址可从目标网络到达。 |
| `DnsIneligible` | 不应发布，也不应向第三方传递；可仅作为出站包源地址。 |
| `DnsEligibilityUnknown` | 系统无法判断；若必须发布，应用需要有明确且安全的额外策略。 |

动态 DHCP 地址可能仍适合发布；加密生成的临时 IPv6 地址通常不适合。这个标志不是 DNS 注册权限或公网可达性的证明。

## Preferred 与 Valid lifetime

IPv6 等地址可在“仍有效”和“仍应作为新连接源地址”之间有一段差异：

- `preferredLifetime()` 到期后，地址变为 deprecated；通常不应再作为新出站通信的首选源地址。
- `validityLifetime()` 到期后，地址从网络栈移除，不再是本机有效目的地址。
- 当 lifetime 不可知时，两个 getter 都返回 `QDeadlineTimer::Forever`，但必须同时用 `isLifetimeKnown()` 区分“确实永久”与“未知”。
- `isPermanent()` 在无法获知信息时也返回 `true`，因此它不是“绝对静态地址”的证明。

`setAddressLifetime()` 后，即使两个 deadline 都是 `Forever`，`isLifetimeKnown()` 也会变为真；`clearAddressLifetime()` 则恢复“未知”状态。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 枚举 | `DnsEligibilityStatus` | `DnsEligible`、`DnsIneligible`、`DnsEligibilityUnknown`；用于 DNS 发布候选判断，不等于公网可达性。 |
| 构造与赋值 | `QNetworkAddressEntry()`、复制/移动构造、`operator=`、`swap()` | 创建、复制、移动或交换地址项值。 |
| 比较 | `operator==` / `operator!=` | 比较地址项值状态。 |
| IP | `ip()` / `setIp(const QHostAddress &)` | 获取/设置此值对象的 IPv4 或 IPv6 地址；不修改系统接口配置。 |
| 子网 | `netmask()` / `setNetmask(const QHostAddress &)` | 获取/设置 netmask；设置时同步 prefix length。 |
| 子网 | `prefixLength()` / `setPrefixLength(int)` | 获取/设置前缀；IPv4 0-32、IPv6 0-128，不合法等价于无前缀（`-1`）。 |
| 广播 | `broadcast()` / `setBroadcast(const QHostAddress &)` | IPv4 广播地址；IPv6 始终不适用，应使用多播。 |
| DNS | `dnsEligibility()` / `setDnsEligibility(DnsEligibilityStatus)` | 获取/设置 DNS 发布适宜性；未知时不能简单按 eligible 处理。 |
| 生命周期 | `isLifetimeKnown()` | 生命周期信息是否可得；未知时两个 deadline getter 仍返回 `Forever`。 |
| 生命周期 | `preferredLifetime()` | 地址停止作为新出站包首选源地址的 deadline。 |
| 生命周期 | `validityLifetime()` | 地址从网络栈移除的 deadline。 |
| 生命周期 | `setAddressLifetime(QDeadlineTimer preferred, QDeadlineTimer validity)` | 设置两种 lifetime，并令 `isLifetimeKnown()` 为真。 |
| 生命周期 | `clearAddressLifetime()` | 清空 lifetime 信息，令 `isLifetimeKnown()` 为假。 |
| 生命周期 | `isPermanent()` / `isTemporary()` | 判断地址是否有到期时间；信息未知时 `isPermanent()` 也为真，不能当作绝对保证。 |
| 调试 | `operator<<(QDebug, const QNetworkAddressEntry &)` | Qt 6.2 起输出调试表示。 |
| 协作 | `QNetworkInterface::addressEntries()` | 从某个接口取得该类的快照列表。 |

## 一句话总结

`QNetworkAddressEntry` 把 IP 与子网、DNS 发布适宜性和生命周期放在同一个快照中：选地址时既看地址值，也要看前缀、临时性与系统信息是否可信。
