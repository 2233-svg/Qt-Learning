# QDnsTextRecord
> Qt 6.11.1 · Qt Network · 来自 `QDnsTextRecord`

## 作用定位
`QDnsTextRecord` 表示 TXT 记录，以多段字节串保存域名附加元数据。

## API 速查
| API | 是做什么的 |
|---|---|
| `values()` | 返回 TXT 的字节串片段。|
| `name()` | 返回记录名。|
| `timeToLive()` | 返回 TTL。|

## 使用场景
读取 SPF、域验证、配置提示或服务能力标志。

## 常见坑与经验
- TXT 不是可靠机密存储，也不应当作未签名配置源直接执行。
- 多段值的组合方式按具体协议定义，不能盲目以空格拼接。

## 知识点覆盖
TXT、字节编码、域验证、配置安全、TTL。
