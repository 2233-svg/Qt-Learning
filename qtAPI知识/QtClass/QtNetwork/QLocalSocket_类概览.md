# QLocalSocket：本机进程间通信的字节流连接

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLocalSocket>`  
> CMake：`Qt6::Network`  
> 继承：`QIODevice`

## 它解决什么问题

`QLocalSocket` 是面向连接、顺序字节流的本地 IPC 通道。客户端用它连接 `QLocalServer`；服务端通过 `QLocalServer::nextPendingConnection()` 得到它。Windows 上底层通常是命名管道，Unix 上通常是 Unix domain socket。

它继承 `QIODevice`，因此应用通过 `write()`、`readAll()`、`read()`、`readyRead()`、`bytesWritten()` 等通用 I/O 接口传输数据。它提供的是连续字节流，**没有消息边界**：一次 `write()` 不保证对应对端一次 `readyRead()` 或一次 `read()`。

## 实际使用场景

- 已运行实例接收第二个进程发来的命令。
- GUI 前端与本机后台服务交换请求和结果。
- 同机插件或工具进程的轻量 RPC。

适合本机单跳通信；需要远程网络、TLS、代理或 TCP 兼容时应使用 `QTcpSocket`、`QSslSocket` 或 HTTP API。

## 推荐使用方式

用事件驱动方式连接、读写和处理失败。下面用换行作为协议消息边界；生产协议还应限制单条消息大小。

```cpp
#include <QLocalSocket>
#include <QDebug>

QLocalSocket socket;

QObject::connect(&socket, &QLocalSocket::connected, &socket, [&socket] {
    socket.write("open /tmp/report.txt\n");
});

QObject::connect(&socket, &QLocalSocket::readyRead, &socket, [&socket] {
    while (socket.canReadLine()) {
        const QByteArray reply = socket.readLine();
        qDebug() << "reply:" << reply;
    }
});

QObject::connect(&socket, &QLocalSocket::errorOccurred, &socket,
                 [&socket](QLocalSocket::LocalSocketError error) {
    qWarning() << error << socket.errorString();
});

socket.connectToServer(QStringLiteral("com.example.mytool"));
```

`connectToServer()` 是异步发起：调用后会先进入 `ConnectingState`，成功后进入 `ConnectedState` 并发出 `connected()`，失败则发出 `errorOccurred()`。不要在调用后立刻假定连接已经可写。

## 关键语义与边界

### 为协议自行定义消息边界

本类传输的是流。可靠的协议至少选择一种分帧方式：

- 换行或其他明确分隔符；
- 固定长度头部加 payload 长度；
- 自描述格式，但仍要限定最大缓冲长度。

不要把一次 `readyRead()` 当成一条完整消息，也不要信任对端提供的长度字段。未受限的 `readAll()` 容易让恶意或故障对端耗尽内存。

### 正常断开与强制中止不同

`disconnectFromServer()` 会请求关闭：若写缓冲区仍有数据，状态先转为 `ClosingState`，待数据写完才转为 `UnconnectedState` 并发出 `disconnected()`。

`abort()` 则立即关闭，丢弃写缓冲区中尚未发送的数据。超时、取消或错误恢复需要快速停止时用它；希望尽量送达已经 `write()` 的数据时用 `disconnectFromServer()`。

`close()` 会关闭 I/O 设备并调用 `disconnectFromServer()`，所以通常也保留待发送数据，而不是 `abort()`。

### `open()` 不等于已连通

这个类重写的 `open()` 可能只开始连接，不会直接打开实际通道。只要 socket 尚未连接且已经设置服务端名称，它可能返回 `true`；真正成功或失败稍后通过 `connected()` / `errorOccurred()` 告知。

因此客户端通常直接调用 `connectToServer()`，并把后续逻辑写在信号槽中，而不是只根据 `open()` 的返回值判定连接结果。

### 缓冲与发送时机

`write()` 先进入 Qt 的内部写缓冲。通常回到事件循环后会自动开始发送，不必每次写入后调用 `flush()`。`flush()` 是不阻塞的“尽可能多写出”；只有确实写出某些数据时才返回 `true`。没有事件循环时，使用 `waitForBytesWritten()`。

`setReadBufferSize(size)` 限制内部读取缓冲的大小，适合对吞吐和内存实施背压。其正确值取决于协议：过小会降低吞吐，设置无限或不消费数据则可能造成内存压力。

### 平台和抽象命名空间

`setServerName()` 的语义随平台变化：Windows 是命名管道名，Unix 是本地域 socket 名称。Linux/Android 连接抽象命名空间地址时，必须在仍处于 `UnconnectedState` 时设置 `AbstractNamespaceOption`；其他平台会忽略该选项。

### 阻塞 API 与线程

`waitForConnected()`、`waitForReadyRead()`、`waitForBytesWritten()`、`waitForDisconnected()` 都会阻塞到完成或超时（默认 30 秒）。没有事件循环的工作线程可使用；GUI 线程中使用会冻结界面，也会妨碍本应靠事件循环处理的槽。

`QLocalSocket::LocalSocketError` 不是自动注册的元类型。若把 `errorOccurred(QLocalSocket::LocalSocketError)` 用于跨线程 queued connection，需显式 `Q_DECLARE_METATYPE` 和 `qRegisterMetaType`。

### 原生描述符接管

`setSocketDescriptor()` 用已有原生描述符初始化 socket，并设定初始状态和打开模式。一个原生描述符不能同时用于两个 `QLocalSocket`；未连接时 `socketDescriptor()` 返回 `-1`。这属于底层集成接口，调用者必须保证描述符类型、生命周期和线程模型匹配当前平台。

## 状态与错误

| 状态 | 含义 |
| --- | --- |
| `UnconnectedState` | 未连接，适合配置 server name 与 socket options。 |
| `ConnectingState` | 已开始建立连接，等待 `connected()` 或错误。 |
| `ConnectedState` | 通道已建立，可进行异步读写。 |
| `ClosingState` | 正在优雅关闭，写缓冲区可能仍在发送。 |

常见错误包括：`ConnectionRefusedError`（被拒绝或超时）、`ServerNotFoundError`（本地端点不存在）、`SocketAccessError`（权限不足）、`SocketResourceError`（本机资源耗尽）、`OperationError`（状态不允许当前调用）。错误发生后读取 `error()` 和 `errorString()`；错误字符串适合日志，不适合用作程序分支。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 枚举 | `LocalSocketError` | 最近一次失败的错误类别；包括拒绝、端点不存在、权限、资源、超时、非法状态等。跨线程 queued signal 前需注册为元类型。 |
| 枚举 | `LocalSocketState` | `Unconnected`、`Connecting`、`Connected`、`Closing` 四态；状态变化用 `stateChanged()` 观察。 |
| 枚举 | `SocketOption` / `SocketOptions` | Qt 6.2 起可配置连接选项。 |
| 枚举值 | `NoOptions` | 不设置特殊连接选项。 |
| 枚举值 | `AbstractNamespaceOption` | Linux/Android 连接抽象命名空间；其他平台忽略，且必须在未连接时设置。 |
| 构造/析构 | `QLocalSocket(parent)` / `~QLocalSocket()` | QObject 生命周期；析构时必要情况下关闭连接。 |
| 连接 | `connectToServer(openMode)` | 使用已设置的 `serverName()` 异步连接；未设置名称时不能成功建立目标连接。 |
| 连接 | `connectToServer(name, openMode)` | 设置名称并异步连接；成功由 `connected()` 通知，失败由 `errorOccurred()` 通知。 |
| 连接 | `setServerName(name)` / `serverName()` | 设置/读取逻辑端点名；Windows 是管道名，Unix 是本地域 socket 名称。 |
| 连接 | `fullServerName()` | 返回平台相关的完整端点名称或路径。 |
| 关闭 | `disconnectFromServer()` | 优雅关闭；等待写缓冲发送，期间可能处于 `ClosingState`。 |
| 关闭 | `abort()` | 立即关闭并丢弃未发送写缓冲。 |
| 关闭 | `close()` | 关闭 I/O 设备并调用优雅断开。 |
| 状态 | `state()` | 返回当前连接状态。 |
| 状态 | `isValid()` | 查询底层 socket 当前是否有效；仍应结合 `state()` 和错误信息处理失败。 |
| 错误 | `error()` | 返回最近的 `LocalSocketError`。 |
| 错误 | `errorOccurred(error)` | 异步错误信号；错误文本通过继承的 `errorString()` 获取。 |
| 状态信号 | `connected()` / `disconnected()` | 已连接 / 已断开时发出。 |
| 状态信号 | `stateChanged(state)` | 状态迁移时发出。 |
| 缓冲 | `flush()` | 非阻塞地尽量把内部写缓冲送入系统；通常无需手动调用。 |
| 缓冲 | `readBufferSize()` / `setReadBufferSize(size)` | 读取缓冲上限；用来平衡内存占用与吞吐。 |
| 描述符 | `setSocketDescriptor(descriptor, state, openMode)` | 接管一个原生描述符；同一描述符不能初始化两个 socket。 |
| 描述符 | `socketDescriptor()` | 返回原生描述符；`UnconnectedState` 时为 `-1`。 |
| 选项 | `setSocketOptions(options)` / `socketOptions()` | 设置/读取连接选项；只能在 `UnconnectedState` 配置。 |
| 选项 | `bindableSocketOptions()` | Qt 6.2 起，返回 `QProperty` 绑定接口。 |
| 阻塞等待 | `waitForConnected(msecs)` | 阻塞到连接成功、失败或超时；默认 30000 ms。 |
| 阻塞等待 | `waitForDisconnected(msecs)` | 阻塞到已断开或超时。 |
| 阻塞等待 | `waitForReadyRead(msecs)` | 重写 `QIODevice`；阻塞等待可读数据或超时。 |
| 阻塞等待 | `waitForBytesWritten(msecs)` | 重写 `QIODevice`；阻塞等待写缓冲有进展或超时。 |
| QIODevice 重写 | `bytesAvailable()` / `bytesToWrite()` / `canReadLine()` | 查询本 socket 的可读/待写字节与换行可用性；处理流数据仍需自行分帧。 |
| QIODevice 重写 | `isSequential()` | 返回顺序设备属性，不能随机 seek。 |
| QIODevice 重写 | `open(openMode)` | 可能只开始异步连接，不保证调用返回时已经连通。 |
| 受保护重写 | `readData()` / `readLineData()` / `skipData()` / `writeData()` | `QIODevice` 的底层扩展点；普通应用使用公共 `read`/`write`，不直接调用。 |

## 相关类型

- `QLocalServer`：本地 socket 的监听端和服务端接入器。
- `QIODevice`：提供通用读写、缓冲与 `readyRead()` / `bytesWritten()` 信号。
- `QTcpSocket`：需要跨机器 TCP 通信时的对应类型。
