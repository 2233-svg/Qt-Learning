# QUdpSocket
> Qt 6.11.1 · Qt Network · 来自 `QUdpSocket`

## 作用定位
`QUdpSocket` 提供 UDP 数据报收发和多播。每个读操作对应一个完整 datagram，消息边界由协议保留。

## API 速查
| API | 是做什么的 |
|---|---|
| `bind()` | 绑定本地端口/地址。|
| `writeDatagram()` | 发送一个数据报。|
| `hasPendingDatagrams()` | 判断是否有完整数据报可读。|
| `receiveDatagram()` | 读取一个 `QNetworkDatagram`。|
| `readDatagram()` | 读取字节及发送方信息。|
| `joinMulticastGroup()` | 加入多播组。|
| `leaveMulticastGroup()` | 离开多播组。|

## 使用场景
局域网发现、低延迟遥测、广播控制、DNS 类协议。

## 常见坑与经验
- UDP 可能丢包、重复、乱序且受 MTU 限制；可靠性必须由协议层设计。
- `readyRead()` 时循环读尽所有 datagram，否则事件会反复触发。

## 知识点覆盖
UDP、数据报边界、丢包乱序、MTU、多播、广播。
