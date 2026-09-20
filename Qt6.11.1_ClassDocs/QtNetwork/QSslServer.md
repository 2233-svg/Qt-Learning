# QSslServer
> Qt 6.11.1 · Qt Network · 来自 `QSslServer`

## 作用定位
`QSslServer` 是接受 TLS 连接的服务器类，创建 `QSslSocket` 会话。

## API 速查
| API | 是做什么的 |
|---|---|
| `listen()` | 开始监听 TLS 服务端口。|
| `setSslConfiguration()` | 配置证书、私钥和协议。|
| `pendingSslConnections()` | 取得等待处理的 TLS socket。|
| `newConnection()` | 通知新连接。|

## 使用场景
受控环境的小型 TLS 服务、测试服务器、设备管理端。

## 常见坑与经验
- 生产服务还需协议解析、会话限流、证书轮换、日志脱敏和安全更新。

## 知识点覆盖
TLS 服务端、证书私钥、连接接受、会话安全、部署。
