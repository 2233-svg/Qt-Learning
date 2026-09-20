# QNetworkDatagram
> Qt 6.11.1 · Qt Network · 来自 `QNetworkDatagram`

## 作用定位
`QNetworkDatagram` 是一个 UDP 数据报值对象，包含载荷、目的地、发送方、端口、接口和 hop limit 等元数据。

## API 速查
| API | 是做什么的 |
|---|---|
| `data()` | 读取数据报负载。|
| `senderAddress()` / `senderPort()` | 读取发送端。|
| `destinationAddress()` / `destinationPort()` | 读取接收目的地。|
| `setData()` | 设置待发送负载。|
| `setDestination()` | 设置待发送目标。|
| `interfaceIndex()` | 查询接收网络接口。|
| `hopLimit()` | 查询/设置 TTL 或 hop limit。|

## 使用场景
使用 `receiveDatagram()` 取得包含来源地址的完整消息，回复时根据 `senderAddress()` 和 `senderPort()` 构造目标。

## 常见坑与经验
- sender 元数据只能信任为网络层来源，不能取代业务认证。
- 接收数据报的目标地址在多播/多网卡环境中特别有用。

## 知识点覆盖
UDP 元数据、来源地址、网络接口、TTL、数据报安全。
