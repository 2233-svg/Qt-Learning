# QDnsServiceRecord
> Qt 6.11.1 · Qt Network · 来自 `QDnsServiceRecord`

## 作用定位
`QDnsServiceRecord` 表示 SRV 记录，描述某服务的目标主机、端口、优先级和权重。

## API 速查
| API | 是做什么的 |
|---|---|
| `target()` | 返回服务主机名。|
| `port()` | 返回服务端口。|
| `priority()` | 返回故障切换优先级。|
| `weight()` | 返回同优先级负载分配权重。|
| `timeToLive()` | 返回 TTL。|

## 使用场景
通过 `_service._tcp.example.com` 发现多个服务节点。

## 常见坑与经验
- 权重不是简单排序值，应在同优先级节点间随机按权重选择。
- 目标名为 `.` 通常表示服务明确不可用。

## 知识点覆盖
SRV、服务发现、优先级、权重、故障切换、TTL。
