# QSslDiffieHellmanParameters
> Qt 6.11.1 · Qt Network · 来自 `QSslDiffieHellmanParameters`

## 作用定位
`QSslDiffieHellmanParameters` 保存 TLS 服务端使用的有限域 Diffie-Hellman 参数。

## API 速查
| API | 是做什么的 |
|---|---|
| `defaultParameters()` | 使用 Qt 默认安全参数。|
| `fromEncoded()` | 从 PEM/DER 导入参数。|
| `isValid()` / `errorString()` | 校验参数。|

## 使用场景
需要兼容特定服务端 TLS 策略时配置 DH 参数。

## 常见坑与经验
- 普通应用使用默认值；自行加载弱参数会直接削弱前向保密。

## 知识点覆盖
DH、前向保密、参数验证、TLS 服务端。
