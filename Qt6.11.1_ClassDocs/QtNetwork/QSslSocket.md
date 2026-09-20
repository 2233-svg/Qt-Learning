# QSslSocket
> Qt 6.11.1 · Qt Network · 来自 `QSslSocket`

## 作用定位
`QSslSocket` 在 TCP socket 上提供 TLS 加密、证书校验和加密流读写。

## API 速查
| API | 是做什么的 |
|---|---|
| `connectToHostEncrypted()` | 连接并开始客户端 TLS 握手。|
| `startClientEncryption()` | 在已有连接上启动 TLS。|
| `startServerEncryption()` | 作为服务端启动 TLS。|
| `encrypted()` | 握手和验证成功。|
| `sslErrors()` | 报告证书/握手问题。|
| `setSslConfiguration()` | 设置会话 TLS 策略。|
| `peerCertificate()` | 读取对端证书。|

## 使用场景
TLS 加密的自定义 TCP 协议、SMTP/IMAP 的 SSL 连接、mTLS。

## 常见坑与经验
- `connected()` 仅 TCP 成功，`encrypted()` 才表示 TLS 已建立。
- 不要在生产中忽略 SSL errors；错误是抵抗中间人攻击的关键防线。

## 知识点覆盖
TLS socket、握手、证书验证、mTLS、加密流、错误处理。
