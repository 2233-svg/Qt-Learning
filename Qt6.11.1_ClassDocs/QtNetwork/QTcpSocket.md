# QTcpSocket
> Qt 6.11.1 · Qt Network · 来自 `QTcpSocket`

## 作用定位
`QTcpSocket` 是 TCP 客户端 socket，继承 `QAbstractSocket` 并提供可靠、有序的双向字节流。

## API 速查
| API | 是做什么的 |
|---|---|
| `connectToHost()` | 连接远端主机和端口。|
| `write()` | 将字节排入发送缓冲。|
| `readyRead()` | 有接收字节可读。|
| `flush()` | 尝试立即将写缓冲交给系统。|
| `setSocketDescriptor()` | 接管已有 native socket。|

## 使用场景
自定义长连接协议、设备网关、Redis/SMTP 等非 HTTP 客户端。

## 常见坑与经验
- 需要自行定义消息边界、版本和最大包长。
- 重连应有退避与取消策略，不能在 `disconnected()` 里无延迟死循环。

## 知识点覆盖
TCP、长连接、协议分帧、重连、背压、可靠传输。
