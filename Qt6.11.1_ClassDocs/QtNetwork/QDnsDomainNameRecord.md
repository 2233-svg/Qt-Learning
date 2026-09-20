# QDnsDomainNameRecord
> Qt 6.11.1 · Qt Network · 来自 `QDnsDomainNameRecord`

## 作用定位
`QDnsDomainNameRecord` 表示 DNS 中值为域名的记录，例如 CNAME、NS 或 PTR 查询结果。

## API 速查
| API | 是做什么的 |
|---|---|
| `name()` | 返回查询到的记录名。|
| `value()` | 返回目标域名。|
| `timeToLive()` | 返回 TTL。|

## 使用场景
诊断域名别名链、读取名称服务器、反向查询结果。

## 常见坑与经验
- CNAME 目标仍可能需继续解析 A/AAAA。
- 不能用 PTR 作为安全身份验证依据。

## 知识点覆盖
CNAME、NS、PTR、别名链、TTL、DNS 安全边界。
