# QDtlsClientVerifier
> Qt 6.11.1 · Qt Network · 来自 `QDtlsClientVerifier`

## 作用定位
`QDtlsClientVerifier` 帮 DTLS 服务端在分配会话资源前验证客户端 cookie，降低伪造源地址造成的资源耗尽。

## API 速查
| API | 是做什么的 |
|---|---|
| `verifyClient()` | 验证或生成 DTLS cookie 挑战。|
| `verifiedHello()` | 取得验证通过的 ClientHello 信息。|

## 使用场景
公网 DTLS 服务端接收未知客户端前的地址验证。

## 常见坑与经验
- 它解决的是地址验证，不替代后续身份认证与访问授权。

## 知识点覆盖
DTLS cookie、抗放大攻击、无状态验证、DoS 防护。
