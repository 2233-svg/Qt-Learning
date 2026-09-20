# QDnsLookup
> Qt 6.11.1 · Qt Network · 来自 `QDnsLookup`

## 作用定位
`QDnsLookup` 执行可指定记录类型的 DNS 查询，适用于 A/AAAA 以外的 MX、SRV、TXT、TLSA 等记录。

## API 速查
| API | 是做什么的 |
|---|---|
| `setName()` | 设置要查询的域名。|
| `setType()` | 设置记录类型。|
| `setNameserver()` | 指定 DNS 服务器。|
| `lookup()` | 异步开始查询。|
| `finished()` | 查询结束。|
| `error()` / `errorString()` | 查询错误。|
| `hostAddressRecords()` 等 | 读取不同类型结果。|

## 使用场景
服务发现使用 SRV、邮件路由读取 MX、功能开关读取 TXT。

## 常见坑与经验
- 不同 DNS resolver 对记录和超时的表现不同，失败路径必须完整。
- 记录结果有 TTL 和缓存语义；不应无限期缓存。

## 知识点覆盖
DNS 记录、异步解析、TTL、服务发现、错误处理、nameserver。
