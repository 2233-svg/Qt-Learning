# QDnsMailExchangeRecord
> Qt 6.11.1 · Qt Network · 来自 `QDnsMailExchangeRecord`

## 作用定位
`QDnsMailExchangeRecord` 表示 MX 记录，给出邮件交换主机和优先级。

## API 速查
| API | 是做什么的 |
|---|---|
| `exchange()` | 返回目标邮件主机名。|
| `preference()` | 返回优先级，数值小者优先。|
| `timeToLive()` | 返回 TTL。|

## 使用场景
邮件投递程序选择域的 SMTP 目标。

## 常见坑与经验
- MX 目标是主机名，不是可直接连接的 IP；还要查 A/AAAA。
- 邮件安全需要 TLS、身份与反垃圾策略，MX 查询只是路由第一步。

## 知识点覆盖
MX、优先级、邮件路由、后续解析、TLS。
