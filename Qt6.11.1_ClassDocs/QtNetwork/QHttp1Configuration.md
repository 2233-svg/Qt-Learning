# QHttp1Configuration
> Qt 6.11.1 · Qt Network · 来自 `QHttp1Configuration`

## 作用定位
`QHttp1Configuration` 是 HTTP/1.1 连接策略配置值类型，主要控制连接复用与管线化等低层行为。

## API 速查
| API | 是做什么的 |
|---|---|
| `setNumberOfConnectionsPerHost()` | 控制每主机并发连接数。|
| `setPipeliningAllowed()` | 控制是否允许 HTTP/1.1 pipeline。|

## 使用场景
诊断老旧 HTTP/1.1 服务或在受控网络中调整并发行为。

## 常见坑与经验
- Pipeline 在现实代理和服务端兼容性上有历史问题，默认策略通常更稳。
- 不要把增加并发当成吞吐万能药，服务端限流与本地资源也会受影响。

## 知识点覆盖
HTTP/1.1、连接池、管线化、并发、兼容性。
