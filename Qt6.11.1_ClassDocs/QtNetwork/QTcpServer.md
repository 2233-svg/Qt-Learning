# QTcpServer
> Qt 6.11.1 · Qt Network · 来自 `QTcpServer`

## 作用定位
`QTcpServer` 监听本地端口并把每个传入 TCP 连接作为 `QTcpSocket` 交给应用。

## API 速查
| API | 是做什么的 |
|---|---|
| `listen()` | 开始监听地址和端口。|
| `newConnection()` | 有待接受连接时发出。|
| `nextPendingConnection()` | 取出下一个连接 socket。|
| `close()` | 停止监听新连接。|
| `setMaxPendingConnections()` | 限制待处理连接队列。|
| `incomingConnection()` | 重实现以自定义接入逻辑。|

## 使用场景
本机开发服务、小型设备协议服务器、测试桩。连接到来后立刻取出 socket、设置 parent 并交给会话对象。

## 常见坑与经验
- `newConnection()` 后应循环取空 pending 队列，不只取一次。
- `close()` 不会自动断开已接受客户端，需自行管理会话。
- 公开监听地址需考虑认证、输入长度限制和 DoS 防护。

## 知识点覆盖
监听、accept、连接队列、会话管理、服务器安全、背压。
