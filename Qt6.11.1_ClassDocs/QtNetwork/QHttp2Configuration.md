# QHttp2Configuration
> Qt 6.11.1 · Qt Network · 来自 `QHttp2Configuration`

## 作用定位
`QHttp2Configuration` 配置 HTTP/2 的流、窗口和服务器推送等低层连接行为。

## API 速查
| API | 是做什么的 |
|---|---|
| `setSessionReceiveWindowSize()` | 设置会话接收窗口。|
| `setStreamReceiveWindowSize()` | 设置单流接收窗口。|
| `setMaxFrameSize()` | 设置最大帧大小。|
| `setServerPushEnabled()` | 控制服务器推送。|

## 使用场景
极高吞吐或协议调试场景；普通 API 客户端保持 Qt 默认配置。

## 常见坑与经验
- 不同服务端对非常规参数兼容性不一，只有性能测量证明需要才调整。
- HTTP/2 多路复用不等于无限并发，应用层仍要控制请求队列。

## 知识点覆盖
HTTP/2、流控、多路复用、帧、服务器推送、性能调优。
