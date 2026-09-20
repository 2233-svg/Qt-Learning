# QSslCipher
> Qt 6.11.1 · Qt Network · 来自 `QSslCipher`

## 作用定位
`QSslCipher` 描述 TLS 协商出的或可配置的密码套件。

## API 速查
| API | 是做什么的 |
|---|---|
| `name()` | 套件名称。|
| `protocol()` | 对应 TLS 协议。|
| `usedBits()` / `supportedBits()` | 查询密钥强度信息。|

## 使用场景
连接诊断、合规审计。

## 常见坑与经验
- 不要仅用 bit 数判断安全；协议版本、密钥交换和实现补丁都重要。

## 知识点覆盖
密码套件、TLS 协商、密钥强度、合规。
