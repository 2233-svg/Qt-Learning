# QtTaskTree::QTcpSocketWrapper
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QTcpSocketWrapper`

## 作用定位

`QTcpSocketWrapper` 把一次 TCP socket 操作包装成 TaskTree 任务。它可设置地址、端口和要发送的数据，启动后通过 socket 信号判断完成结果。

## 类说明

- 头文件：`#include <qtcpsocketwrappertask.h>`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `setAddress()` | 设置目标地址。 |
| `setPort()` | 设置目标端口。 |
| `setData()` | 设置要发送的数据。 |
| `socket()` | 访问底层 `QTcpSocket`。 |
| `start()` | 启动连接/发送流程。 |
| `started()` | 任务开始。 |
| `done(result)` | socket 操作结束并报告结果。 |

## 使用场景
- 简单 TCP 探测或发送命令。
- 把 socket 操作纳入更大的 TaskTree 流程。
- 与 barrier/timeout 组合实现连接检查。

## 常见坑与经验
- TCP 连接和写入都是异步的，不能 `start()` 后马上假设数据已发完。
- socket 错误和远端协议错误要分开处理。
- 复杂协议建议封装更明确的任务类，不要把全部协议状态塞进 wrapper 外部。

## 知识点覆盖

- QTcpSocket 异步接入
- 地址/端口/数据配置
- socket 错误和任务结果
