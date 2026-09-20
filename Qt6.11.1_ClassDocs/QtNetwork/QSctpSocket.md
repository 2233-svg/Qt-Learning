# QSctpSocket
> Qt 6.11.1 · Qt Network · 来自 `QSctpSocket`

## 作用定位
`QSctpSocket` 提供 SCTP socket：它兼具消息边界、多流和可靠传输特性，适合协议确实需要避免单一流队头阻塞的场景。

## API 速查
| API | 是做什么的 |
|---|---|
| `connectToHost()` | 建立 SCTP association。|
| `writeDatagram()` | 发送带流信息的数据报。|
| `readDatagram()` | 读取完整 SCTP 消息。|
| `setMaximumChannelCount()` | 限制可用 SCTP streams。|

## 使用场景
使用 SCTP 的专用通信系统或电信协议；普通网络客户端优先 TCP/UDP。

## 常见坑与经验
- 平台与网络设备对 SCTP 支持不如 TCP 普遍，部署前实测。
- 不要误把 SCTP 的 datagram API 当成 UDP：可靠性和连接模型不同。

## 知识点覆盖
SCTP、多流、消息边界、可靠传输、平台兼容性。
