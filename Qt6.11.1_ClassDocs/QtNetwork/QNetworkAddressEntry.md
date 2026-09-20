# QNetworkAddressEntry
> Qt 6.11.1 · Qt Network · 来自 `QNetworkAddressEntry`

## 作用定位
`QNetworkAddressEntry` 表示一个网络接口上的 IP 地址及其子网、广播、DNS 生命周期信息。

## API 速查
| API | 是做什么的 |
|---|---|
| `ip()` | 返回该接口 IP 地址。|
| `netmask()` | 返回子网掩码。|
| `broadcast()` | 返回 IPv4 广播地址。|
| `prefixLength()` | 返回 CIDR 前缀长度。|
| `dnsEligibility()` | 查询地址 DNS 使用资格。|
| `isLifetimeKnown()` | 查询租约时间是否可得。|

## 使用场景
计算本地子网、选择绑定地址、诊断 DHCP/IPv6 地址状态。

## 常见坑与经验
- IPv6 没有传统 broadcast，不能假定 `broadcast()` 有值。
- 多个地址可能同属一个接口，选择时要排除 link-local 或临时地址视业务而定。

## 知识点覆盖
IP 配置、子网掩码、CIDR、广播、IPv6、多地址接口。
