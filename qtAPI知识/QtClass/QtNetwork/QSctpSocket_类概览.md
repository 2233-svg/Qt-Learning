# QSctpSocket：可靠多流 SCTP 套接字

> Qt 6.11.1  
> 头文件：`#include <QSctpSocket>`  
> 模块：`Qt6::Network`  
> 继承：`QAbstractSocket -> QTcpSocket -> QSctpSocket`  
> 平台边界：Windows 不支持

## 它解决什么问题

TCP 把数据看成连续字节流，UDP 保留消息边界但不保证可靠交付。SCTP 试图同时提供可靠、有序的消息传输、多流和拥塞控制；同一关联中的一个流出现丢包时，不必阻塞其他流。

`QSctpSocket` 允许应用在两种模式间选择：

- **TCP emulation**：把 SCTP 当作连续字节流使用，适合复用 `QTcpSocket` 风格代码；
- **datagram 模式**：每次 `writeDatagram()` 发送一条消息，每次 `readDatagram()` 取出一条消息，并通过 read/write channel 访问不同 SCTP 流。

默认是 datagram 模式。模式必须在连接建立前通过 `setMaximumChannelCount()` 选择，连接建立后不应再改变。

## 实际使用场景

### 1. 多流消息通信

```cpp
auto *socket = new QSctpSocket(this);
socket->setMaximumChannelCount(16);
socket->connectToHost(QHostAddress::LocalHost, 1973);

connect(socket, &QAbstractSocket::connected, this, [socket] {
    qInfo() << "read channels:" << socket->readChannelCount()
            << "write channels:" << socket->writeChannelCount();

    socket->writeDatagram(QNetworkDatagram(
        QByteArray("event"), QHostAddress::LocalHost, 1973));
});

connect(socket, &QIODevice::readyRead, this, [socket] {
    while (socket->hasPendingDatagrams()) {
        const QNetworkDatagram datagram = socket->readDatagram();
        if (datagram.isValid())
            consumeMessage(datagram.data());
    }
});
```

当前读写 channel 分别由 `QIODevice::setCurrentReadChannel()` 和 `QIODevice::setCurrentWriteChannel()` 控制。每个 channel 的缓冲独立，业务可以把控制、状态和数据放到不同流。

### 2. 作为 TCP 风格字节流

```cpp
auto *socket = new QSctpSocket(this);
socket->setMaximumChannelCount(-1);
socket->connectToHost("example.internal", 1973);

connect(socket, &QIODevice::readyRead, this, [socket] {
    const QByteArray bytes = socket->readAll();
    consumeByteStream(bytes);
});
```

负数会开启连续字节流模式。此时不能通过 `readDatagram()` 取得消息边界，也不能把一次 `write()` 与对端的一次 `read()` 视为一一对应。

## 关键 API 语义与边界

### `maximumChannelCount()` 是配置值，不是实际连接值

- 返回 `-1`：当前为 TCP emulation；
- 返回 `0`：datagram 模式，通道数交给对端/端点协商；
- 返回正数：应用愿意支持的最大通道数。

连接建立后，最终实际通道数应通过 `readChannelCount()` 和 `writeChannelCount()` 查询。系统和远端 endpoint 可能进一步限制数量。

### 只能在 `UnconnectedState` 选择模式

`setMaximumChannelCount()` 只能在 `UnconnectedState` 调用。典型顺序是：构造 -> 设置 count -> 设置必要 socket 选项 -> `connectToHost()`。连接开始后再改 count 可能无效或不符合 API 前置条件。

### datagram 模式仍可使用 QIODevice，但边界语义不同

`read()`、`readLine()`、`write()` 等标准 `QIODevice` API 在 datagram 模式可用，但它们使用当前 channel 的字节流视图，不能替代 `readDatagram()`/`writeDatagram()` 对消息边界的表达。需要保留消息边界时应使用 datagram API。

`readyRead()` 表示当前读 channel 有数据可读。处理该信号时应持续消费 pending datagram；如果槽返回时仍有数据未读，Qt 不会简单地依靠下一次 `readyRead()` 保证再次通知。

### `QNetworkDatagram` 失败值和发送语义

`readDatagram()` 失败时返回无效的 `QNetworkDatagram`，先检查 `isValid()` 再读取地址和数据。`writeDatagram()` 把一条报文放入当前写 channel 的发送缓冲，成功返回 true，失败返回 false；它不等于数据已经到达对端。

### 关闭与线程

`close()`、`disconnectFromHost()` 由派生类重写以适配 SCTP。析构时连接会在需要时关闭。socket 只能在所属线程中使用，跨线程应通过 queued 信号槽，并把 socket 的线程归属和事件循环一起设计。

## API 速查表

### 构造、状态与模式

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `explicit QSctpSocket(QObject *parent = nullptr)` | 创建处于 `UnconnectedState` 的 SCTP socket，默认设为 datagram 模式。 | 连接前调用 `setMaximumChannelCount()` 选择模式。 |
| `~QSctpSocket() noexcept` | 销毁 socket，必要时关闭连接。 | 不应在其他线程直接销毁仍由其线程处理的 socket。 |
| `bool isInDatagramMode() const` | 判断是否处于 datagram 模式。 | false 表示 TCP emulation；与连接状态无关。 |
| `int maximumChannelCount() const` | 返回模式和最大通道配置。 | `-1` 是连续字节流，`0` 是协商值，正数是 datagram 上限。 |
| `void setMaximumChannelCount(int count)` | 设置 datagram 最大通道数或切换 TCP emulation。 | 只允许在 `UnconnectedState` 调用；负数切换连续字节流。 |

### SCTP 消息读写

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `QNetworkDatagram readDatagram()` | 从当前读 channel 读取一条 SCTP 消息，并返回数据、发送方地址和端口等信息。 | 失败返回无效 datagram；需在 datagram 模式使用。 |
| `bool writeDatagram(const QNetworkDatagram &datagram)` | 把一条消息写入当前写 channel 的发送缓冲。 | true 只表示成功排入本地发送流程，不代表对端已接收。 |
| `readChannelCount()` | 继承自 `QIODevice`，读取实际可用读 channel 数。 | 连接建立后查看协商结果；与 maximum 配置不同。 |
| `writeChannelCount()` | 继承自 `QIODevice`，读取实际可用写 channel 数。 | 连接建立后查看协商结果；由远端和系统共同影响。 |
| `setCurrentReadChannel(index)` | 选择后续读取使用的 channel。 | index 必须在实际读 channel 范围内。 |
| `setCurrentWriteChannel(index)` | 选择后续发送使用的 channel。 | index 必须在实际写 channel 范围内。 |
| `currentReadChannel()` / `currentWriteChannel()` | 查询当前读写 channel。 | channel 选择是读写侧独立的。 |

### 重写和连接控制

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `void close()` | 关闭 SCTP socket 和相关 I/O。 | 重写 `QAbstractSocket::close()`；关闭后按状态信号处理清理。 |
| `void disconnectFromHost()` | 请求断开 SCTP 关联。 | 重写基类断开行为；可能经历 Closing 状态后完成。 |
| `protected qint64 readData(char *data, qint64 maxSize)` | 为 `QIODevice::read()` 提供字节读取实现。 | 应用通常调用公共 `read()`/`readAll()`，不直接调用 protected 函数。 |
| `protected qint64 readLineData(char *data, qint64 maxlen)` | 为 `QIODevice::readLine()` 提供读取实现。 | 在 datagram 模式使用时不要把行边界当作 SCTP 消息边界。 |

### 继承的关键连接 API

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `connectToHost(host, port)` | 异步建立 SCTP 关联。 | 应在此前完成模式选择；成功后检查实际 channel 数。 |
| `waitForConnected(msecs)` | 阻塞等待连接完成。 | 只适合明确允许阻塞的线程；GUI 线程中谨慎使用。 |
| `state()` / `error()` / `errorString()` | 查询连接状态和最近错误。 | 返回值是状态，不是异常；错误后按策略重连或终止。 |
| `readyRead()` | 当前读 channel 有数据可读。 | datagram 模式中循环读取 pending 消息。 |
| `bytesWritten(bytes)` | 有字节写入底层发送缓冲时通知。 | 不代表对端已经处理消息。 |

