# QDtls
> Qt 6.11.1 · Qt Network · 来自 `QDtls`

## 作用定位
`QDtls` 在 UDP 数据报上建立 DTLS 会话，提供 TLS 类似的认证与加密，同时保留数据报边界。

## API 速查
| API | 是做什么的 |
|---|---|
| `doHandshake()` | 处理/发送握手数据报。|
| `encryptDatagram()` | 加密应用数据报。|
| `decryptDatagram()` | 解密收到的数据报。|
| `handshakeState()` | 查询握手状态。|
| `dtlsError()` | 查询 DTLS 错误。|

## 使用场景
安全遥测、实时 UDP 协议、设备通信。

## 常见坑与经验
- DTLS 仍需处理丢包、重传、MTU 和会话超时；加密不等于可靠传输。
- 对端验证失败不能通过忽略错误绕过。

## 知识点覆盖
DTLS、UDP、安全握手、重传、证书验证。
