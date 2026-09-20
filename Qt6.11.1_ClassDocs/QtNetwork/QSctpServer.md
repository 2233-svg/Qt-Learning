# QSctpServer
> Qt 6.11.1 · Qt Network · 来自 `QSctpServer`

## 作用定位
`QSctpServer` 监听 SCTP 连接，并返回 `QSctpSocket` 处理各 association。

## API 速查
| API | 是做什么的 |
|---|---|
| `listen()` | 绑定 SCTP 服务端口。|
| `newConnection()` | 有待处理 association。|
| `nextPendingDatagramConnection()` | 取得新 SCTP socket。|
| `setMaximumChannelCount()` | 限制每连接流数量。|

## 使用场景
仅用于确定部署环境支持 SCTP 的专用服务端。

## 常见坑与经验
- 与 TCP server 一样，接受连接后仍需限制并发、协议长度和认证。
- SCTP 很少作为通用公网服务首选，监控与故障回退必须提前设计。

## 知识点覆盖
SCTP 服务端、association、多流限制、部署风险、安全边界。
