# QAbstractSocket
> Qt 6.11.1 · Qt Network · 来自 `QAbstractSocket`

## 作用定位
`QAbstractSocket` 是 TCP、SCTP 等面向连接 socket 的公共异步 I/O 基类，提供连接状态、读写缓冲、错误、代理与地址信息。

## API 速查
| API | 是做什么的 |
|---|---|
| `connectToHost()` | 异步发起连接。|
| `disconnectFromHost()` | 正常关闭连接。|
| `abort()` | 立即中止连接。|
| `state()` / `stateChanged()` | 查询或监听连接状态。|
| `connected()` / `disconnected()` | 监听建立或断开。|
| `readyRead()` | 有字节可读。|
| `bytesWritten()` | 已写入系统缓冲。|
| `errorOccurred()` | 报告 socket 错误。|
| `setSocketOption()` | 设置低层 socket 选项。|

## 使用场景
以信号驱动协议状态机：连接后写握手包，`readyRead()` 将字节累积到接收缓冲后按长度字段或分隔符拆帧。

## 常见坑与经验
- TCP 是字节流，`readyRead()` 不等于收到一条完整业务消息。
- `waitFor...()` 会阻塞线程；GUI 中必须用信号异步模式。
- `bytesWritten()` 不是对端已处理确认，只表示本地写缓冲的进展。

## 知识点覆盖
异步 socket、连接状态、字节流、协议分帧、缓冲、阻塞与事件循环。
