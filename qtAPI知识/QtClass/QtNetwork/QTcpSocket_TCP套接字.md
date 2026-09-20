# QTcpSocket：面向连接的 TCP 字节流

> Qt 6.11.1  
> 头文件：`#include <QTcpSocket>`  
> 模块：`Qt6::Network`  
> 继承：`QAbstractSocket -> QTcpSocket`

## 它解决什么问题

`QTcpSocket` 是 Qt 对 TCP 客户端和已接受 TCP 连接的封装。它把操作系统的 TCP socket 接入 `QIODevice`，因此可以使用 `connectToHost()`、`read()`、`readAll()`、`write()`、`readyRead()`、`bytesWritten()` 和 `disconnected()` 等统一 API。

TCP 提供的是可靠、有序的字节流，不提供消息边界。一次 `write()` 不对应一次对端 `readyRead()`，一次 `readyRead()` 也可能包含半条消息或多条消息。应用协议必须自行定义 framing，例如固定长度、长度前缀、分隔符或独立序列化格式。

`QTcpSocket` 自己新增的公开 API 主要只有构造和析构；连接、状态、代理、缓冲、等待和绝大多数读写行为来自 `QAbstractSocket`。阅读该类时，不能只看本类的两个构造函数而忽略基类状态机。

## 实际使用场景

### 1. 异步 TCP 客户端

```cpp
auto *socket = new QTcpSocket(this);

connect(socket, &QAbstractSocket::connected, this, [socket] {
    socket->write("GET /status\n");
});
connect(socket, &QIODevice::readyRead, this, [socket] {
    static QByteArray buffer;
    buffer += socket->readAll();

    while (const qsizetype end = buffer.indexOf('\n'); end >= 0) {
        const QByteArray line = buffer.left(end);
        buffer.remove(0, end + 1);
        handleLine(line);
    }
});
connect(socket, &QAbstractSocket::errorOccurred, this,
        [socket](QAbstractSocket::SocketError) {
    qWarning() << socket->errorString();
});

socket->connectToHost("example.com", 9000);
```

真实项目中，`buffer` 应属于连接对象而不是函数内的静态变量；示例只突出“TCP 必须自己组帧”。多个客户端同时存在时，每个 socket 都需要独立的解析缓冲。

### 2. 接入 `QTcpServer` 的客户端

服务器调用 `nextPendingConnection()` 得到一个已经处于 `ConnectedState` 的 `QTcpSocket`。应用通常为它连接 `readyRead()` 和 `disconnected()`，在断开后 `deleteLater()`。

```cpp
auto *client = server->nextPendingConnection();
connect(client, &QIODevice::readyRead, this, [client] {
    consumeClientBytes(client);
});
connect(client, &QAbstractSocket::disconnected,
        client, &QObject::deleteLater);
```

返回对象属于服务器线程，不能直接拿到另一个线程使用。跨线程服务应重写 `QTcpServer::incomingConnection()`，在目标线程重新创建 socket 并接管描述符。

### 3. 半关闭和优雅退出

发送完协议中的最后一段数据后调用 `disconnectFromHost()`，Qt 会尽量发送待写缓冲，再进入 `ClosingState`，完成后发出 `disconnected()`。如果协议要求立即丢弃连接和未发送数据，使用 `abort()`。

不要把“对方暂时没有数据”当作连接结束。TCP 没有消息结束标记；必须由协议 framing、对端关闭或应用级状态决定。

### 4. 阻塞式 TCP 工作线程

没有事件循环时可以调用 `waitForConnected()`、`waitForReadyRead()` 和 `waitForBytesWritten()`。这适合专用 I/O 线程，不适合 GUI 线程。读取协议时，`waitForReadyRead()` 只保证有一段字节可读，不保证一条完整业务消息已经到达。

## 关键 API 语义与边界

### TCP 是流，不是消息队列

`readyRead()` 表示读缓冲出现新字节。它不提供 packet boundary，也不承诺每次只发出一次。应用应在槽中尽量读取当前可用数据，并把不完整的数据留在自己的解析缓冲中。

`bytesAvailable()` 是当前 Qt 层可读字节数；`bytesToWrite()` 是尚未发送的 Qt 层字节数。两者都不是网络链路上“已经到达对端”或“已经被业务消费”的证明。

### `write()` 的返回值和发送完成

`write()` 通常只是把数据放入发送缓冲，返回接受到缓冲的字节数。真正写到操作系统或网络时会发出 `bytesWritten()`。需要确认至少有数据写出时可用 `waitForBytesWritten()`，但不要把它误读成对端已经读取。

### 连接、绑定和地址

主机名连接会经历 `HostLookupState` 和 `ConnectingState`；成功后进入 `ConnectedState` 并发出 `connected()`。连接 IP 地址时跳过 DNS，但仍然是异步连接。

TCP socket 也支持 `bind()`。它通常用于在多网卡机器上选择外发本地地址或固定本地端口。`bind()` 成功后进入 `BoundState`，随后再连接对端。端口为 0 时由系统选择临时端口。

### 缓冲限制

`setReadBufferSize()` 只限制 Qt 层接收缓冲。0 表示无限缓冲，是默认值；正数可以帮助实时流应用施加背压，防止应用处理过慢导致内存持续增长。它不等同于 OS 的 `SO_RCVBUF`，后者应使用 `setSocketOption(ReceiveBufferSizeSocketOption, value)`。

### 对象线程归属

`QTcpSocket` 是 QObject，所有成员调用和信号处理都应在其所属线程进行。把 socket 移到另一个线程后，必须让目标线程有事件循环，异步通知才能正常工作。一个 socket 不能被多个线程并发读写而不做同步。

### 平台与阻塞限制

Qt 文档指出，Windows 上 `waitForBytesWritten()` 和 `waitForDisconnected()` 可能偶发失败；跨平台 GUI 应优先使用事件驱动模式。`waitForConnected()` 的超时时间可能因 DNS 查找略微超过给定值，`-1` 表示不超时。

## API 速查表

### QTcpSocket 自身 API

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `explicit QTcpSocket(QObject *parent = nullptr)` | 创建一个 TCP socket。 | 初始状态为 `UnconnectedState`；parent 决定对象所有权和线程归属。 |
| `virtual ~QTcpSocket()` | 销毁 TCP socket。 | 会释放底层连接资源；若在信号槽中销毁，应使用 `deleteLater()`。 |

### 继承的核心 API

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `connectToHost(hostName, port, openMode, protocol)` | 异步解析并连接 TCP 对端。 | 成功后 `connected()`；失败后 `errorOccurred()`。 |
| `connectToHost(address, port, openMode)` | 使用已知地址连接。 | 不需要 DNS，但仍异步。 |
| `disconnectFromHost()` | 优雅关闭，尽量发送完待写数据。 | 可能先进入 `ClosingState`。 |
| `abort()` | 立即关闭并丢弃未发送数据。 | 不适合需要保证尾部数据发出的场景。 |
| `bind(address, port, mode)` | 绑定 TCP socket 的本地端点。 | 适合固定本地端口或选择多网卡出口。 |
| `read(char *, qint64)`、`readAll()`、`readLine()` | 从 TCP 字节流读取。 | 不提供消息边界，必须自行组帧。 |
| `write(const char *, qint64)`、`write(const QByteArray &)` | 将数据放入发送缓冲。 | 返回值不表示对端已经收到。 |
| `bytesAvailable()` | 查询当前可读字节数。 | 配合 `readyRead()`；不代表完整业务消息。 |
| `bytesToWrite()` | 查询等待发送的字节数。 | 配合 `bytesWritten()`；不代表对端已消费。 |
| `setReadBufferSize(qint64 size)` | 设置 Qt 接收缓冲上限。 | 0 为无限；只影响 Qt 层，不影响 OS socket 缓冲。 |
| `state()`、`error()`、`errorString()` | 查询连接状态和最近错误。 | 错误码用于分类，文本用于诊断。 |
| `localAddress()`、`localPort()` | 查询本地端点。 | 端口未确定时通常为 0。 |
| `peerAddress()`、`peerPort()`、`peerName()` | 查询对端端点和连接时的主机名。 | 非 `ConnectedState` 时地址可能为 Null、端口为 0。 |
| `setSocketOption()`、`socketOption()` | 读写 OS socket 选项。 | 具体支持受平台和协议影响；socket 创建后才有确定效果。 |
| `setProxy()`、`proxy()` | 设置或查询该 TCP socket 的代理。 | `NoProxy` 明确禁用；连接开始后再改不会重建当前连接。 |
| `waitForConnected()`、`waitForReadyRead()`、`waitForBytesWritten()`、`waitForDisconnected()` | 阻塞等待连接、数据、写出或断开。 | 专用工作线程使用；GUI 线程会冻结界面。 |

### 相关信号

| 信号 | 语义 | 使用边界 |
| --- | --- | --- |
| `hostFound()` | DNS 查找完成。 | 可能在 `connectToHost()` 调用期间直接发出。 |
| `connected()` | TCP 连接建立。 | 本机连接可能同步发出。 |
| `readyRead()` | 有新的字节可读。 | 继承自 QIODevice；不代表完整消息。 |
| `bytesWritten(qint64 bytes)` | 至少一部分数据已写出。 | 不代表远端应用已经读取。 |
| `disconnected()` | 连接已关闭。 | 可连接到 `deleteLater()`。 |
| `errorOccurred(SocketError)` | 发生 socket 错误。 | 配合 `errorString()` 诊断。 |
| `stateChanged(SocketState)` | 状态发生变化。 | 适合记录状态机，不要靠轮询替代。 |

### 派生扩展构造函数

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `protected QTcpSocket(QTcpSocketPrivate &dd, QObject *parent = nullptr)` | Qt 私有实现使用的派生构造入口。 | 普通应用不应依赖私有数据结构。 |
| `protected QTcpSocket(QAbstractSocket::SocketType type, QTcpSocketPrivate &dd, QObject *parent = nullptr)` | 为特殊 socket 类型提供的内部构造入口。 | 供 Qt 或深度定制的派生实现使用。 |
| `using QAbstractSocket::bind` | 将基类 bind 重载引入 QTcpSocket。 | Qt 6 的兼容性声明。 |
| `bind(QHostAddress::SpecialAddress, quint16, BindMode)` | 以特殊地址便捷绑定。 | Qt 6 兼容接口；具体地址语义由 QHostAddress 决定。 |
