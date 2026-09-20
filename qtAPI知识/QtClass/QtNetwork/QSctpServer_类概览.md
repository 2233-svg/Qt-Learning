# QSctpServer：接收 SCTP 关联并分发到对应模式

> Qt 6.11.1  
> 头文件：`#include <QSctpServer>`  
> 模块：`Qt6::Network`  
> 继承：`QTcpServer -> QSctpServer`  
> 平台边界：Windows 不支持

## 它解决什么问题

SCTP（Stream Control Transmission Protocol）是面向连接、可靠、有序并支持多流的传输协议。它同时保留了 UDP 风格的消息边界和 TCP 风格的可靠传输，还能让多个逻辑流独立传输。

`QSctpServer` 在 `QTcpServer` 的监听和待处理连接模型上增加 SCTP 接入能力。服务端可以选择：

- TCP emulation 模式：把 SCTP 连接暴露为连续字节流，使用 `nextPendingConnection()` 获取 `QTcpSocket *`；
- datagram 模式：保留消息边界和多流能力，使用 `nextPendingDatagramConnection()` 获取 `QSctpSocket *`。

该类只在 Qt 支持 SCTP 的平台上可用，Qt 6.11.1 文档明确说明 Windows 平台不支持它。跨平台程序应在构建配置和运行时能力检测中把这一点当作平台差异处理。

## 实际使用场景

### 1. datagram 模式的多流服务器

```cpp
auto *server = new QSctpServer(this);
server->setMaximumChannelCount(16);

if (!server->listen(QHostAddress::Any, 1973)) {
    qWarning() << server->errorString();
    return;
}

connect(server, &QTcpServer::newConnection, this, [server] {
    while (server->hasPendingConnections()) {
        QSctpSocket *socket = server->nextPendingDatagramConnection();
        if (!socket)
            break;
        // 连接已处于 ConnectedState
        handleSctp(socket);
    }
});
```

`count` 是服务端准备支持的最大通道数，不一定等于最终协商出的通道数。连接建立后，应在 socket 上读取 `readChannelCount()` 和 `writeChannelCount()` 查看实际值。

### 2. TCP emulation 模式

```cpp
auto *server = new QSctpServer(this);
server->setMaximumChannelCount(-1);
server->listen(QHostAddress::Any, 1973);

connect(server, &QTcpServer::newConnection, this, [server] {
    while (server->hasPendingConnections()) {
        QTcpSocket *socket = server->nextPendingConnection();
        if (socket)
            handleByteStream(socket);
    }
});
```

这种模式可以复用普通 TCP 的读写代码，但应用看不到 SCTP 的消息边界、多流和更完整的协议能力。

## 关键 API 语义与边界

### `setMaximumChannelCount()` 必须在监听前调用

只有在服务器处于未连接状态时才能调用 `setMaximumChannelCount()`。应先设置模式和通道上限，再调用 `listen()`。负数选择 TCP emulation，`0` 使用对端/端点的值，正数选择 datagram 模式并给出通道上限。

### 两套 pending connection API 不能混用理解

- TCP emulation：用继承自 `QTcpServer` 的 `nextPendingConnection()`；
- datagram 模式：用 `nextPendingDatagramConnection()`。

`hasPendingConnections()` 只表示有待处理连接，不会告诉你当前连接属于哪种应用模式；服务端自身的配置决定应该调用哪一个取出函数。

### 返回 socket 的线程归属

`nextPendingDatagramConnection()` 返回的 `QSctpSocket` 是 server 的子对象，会随 server 自动删除。它仍然属于 server 所在线程，不能取出后直接在另一个线程使用。若需要跨线程接管，应重写 `incomingConnection()`，在那里按自定义线程/对象归属规则处理 socket descriptor。

### OS backlog 与 Qt pending 队列是两回事

`listen()` 的 backlog 和 Qt `QTcpServer` 待处理连接队列分别由操作系统和 Qt 管理。调大其中一个不会自动改变另一个；高并发服务还应检查 `setMaxPendingConnections()`、`newConnection()` 消费速度及系统 SCTP 配置。

## API 速查表

### 生命周期与模式

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `explicit QSctpServer(QObject *parent = nullptr)` | 创建 SCTP 服务端，并设置初始 datagram 操作模式。 | 仍需先设置通道策略，再调用继承的 `listen()`。 |
| `~QSctpServer() noexcept` | 销毁 server。 | 正在监听时会自动关闭监听 socket；子 socket 也按 QObject 父子关系销毁。 |
| `void setMaximumChannelCount(int count)` | 设置服务端准备支持的最大通道数，并选择模式。 | 只能在未连接状态调用；负数为 TCP emulation，0 为端点协商值，正数为 datagram 模式。 |
| `int maximumChannelCount() const` | 查询服务端模式/通道上限配置。 | `-1` 表示 TCP emulation，`0` 表示使用对端值，正数是配置的上限，不保证是最终协商数。 |

### 接收连接

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `QTcpSocket *nextPendingConnection()` | TCP emulation 模式取出下一个已连接 socket。 | 继承自 `QTcpServer`；只适合连续字节流模式。 |
| `QSctpSocket *nextPendingDatagramConnection()` | datagram 模式取出下一个已连接 SCTP socket。 | 无 pending datagram 连接时返回 `nullptr`；返回对象是 server 子对象且不能直接跨线程使用。 |
| `protected void incomingConnection(qintptr socketDescriptor)` | 处理新到达的底层连接描述符。 | 重写点；Qt 在新连接到达时调用，适合自定义 socket 创建和线程接管。 |

### 继承的关键 API

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `listen(address, port)` | 开始监听 SCTP 端点。 | 应在 `setMaximumChannelCount()` 之后调用；失败时查看 `errorString()`。 |
| `isListening()` | 判断 server 是否正在监听。 | 不代表 pending 队列为空或已有客户端可读。 |
| `hasPendingConnections()` | 判断是否存在待处理连接。 | 取出连接后应继续循环，直到返回空或队列为空。 |
| `newConnection()` | 有新连接进入 Qt pending 队列时发出。 | 槽中应尽快消费连接，避免队列积压。 |
| `setMaxPendingConnections(count)` | 设置 Qt 层待处理连接队列上限。 | 与 OS listen backlog 不是同一个参数。 |
| `close()` | 停止监听。 | 已取出的 socket 生命周期由其自身和 QObject 父子关系继续决定。 |

