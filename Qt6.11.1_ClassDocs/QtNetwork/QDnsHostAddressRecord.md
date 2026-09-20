# QDnsHostAddressRecord
> Qt 6.11.1 · Qt Network · 来自 `QDnsHostAddressRecord`

## 作用定位
`QDnsHostAddressRecord` 表示 DNS A 或 AAAA 记录，包含地址、名称与 TTL。

## API 速查
| API | 是做什么的 |
|---|---|
| `value()` | 返回 `QHostAddress`。|
| `name()` | 返回记录名称。|
| `timeToLive()` | 返回 DNS TTL。|

## 使用场景
从 `QDnsLookup::hostAddressRecords()` 读取多地址服务端点，并按地址族或策略尝试连接。

## 常见坑与经验
- 多个地址并不保证任意顺序最优；连接策略应考虑 Happy Eyeballs 或超时回退。
- TTL 是缓存上限提示，不代表连接持续时间。

## 知识点覆盖
A/AAAA、TTL、多地址、IPv4/IPv6、连接回退。
