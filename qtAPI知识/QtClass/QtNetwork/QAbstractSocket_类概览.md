# QAbstractSocket：统一的套接字状态机

> Qt 6.11.1  
> 头文件：`#include <QAbstractSocket>`  
> 模块：`Qt6::Network`  
> 继承：`QIODevice -> QAbstractSocket`  
> 类型性质：TCP、UDP、SCTP 套接字的抽象基类

## 它解决什么问题

`QAbstractSocket` 把不同网络协议共有的部分统一起来：连接、绑定、本地和对端地址、读写缓冲、套接字状态、错误、代理以及同步等待。`QTcpSocket`、`QUdpSocket` 和 `QSctpSocket` 在它之上提供具体协议行为。

它最重要的价值不是“替应用选择 TCP 还是 UDP”，而是提供一套统一的 `QIODevice` 风格接口和状态机。应用可以用 `readyRead()`、`bytesWritten()`、`connected()`、`disconnected()` 等信号组织异步代码，也可以在没有事件循环的工作线程中使用 `waitForConnected()`、`waitForReadyRead()` 等阻塞 API。

连接型套接字的状态通常按下面的顺序推进：

```text
UnconnectedState
    -> HostLookupState
    -> ConnectingState
    -> ConnectedState
    -> ClosingState
    -> UnconnectedState
```

`connectToHost()` 是异步调用，成功后发出 `connected()`；失败时发出 `errorOccurred()`。DNS 结果可能命中缓存，所以 `hostFound()` 有时会直接在 `connectToHost()` 调用期间发出。只有处于 `ConnectedState` 时，连接型套接字才可以进行正常读写。

UDP 是无连接协议，但 `connectToHost()` 仍可以为 UDP 建立“虚拟连接”：Qt 记住对端地址，之后可用 `read()` 和 `write()` 进行收发；这并不改变 UDP 没有可靠、有序、消息确认语义的事实。

## 实际使用场景

### 1. 异步 TCP 客户端

通常直接使用 `QTcpSocket`，但所有状态和大部分操作都来自本类：

```cpp
auto *socket = new QTcpSocket(this);
connect(socket, &QAbstractSocket::connected, this, [socket] {
    socket->write("hello\n");
});
connect(socket, &QIODevice::readyRead, this, [socket] {
    const QByteArray data = socket->readAll();
    processReply(data);
});
connect(socket, &QAbstractSocket::errorOccurred, this,
        [socket](QAbstractSocket::SocketError) {
    qWarning() << socket->errorString();
});
socket->connectToHost("example.com", 1234);
```

### 2. 服务器接受的连接转移到工作线程

`QTcpServer::nextPendingConnection()` 返回的 `QTcpSocket` 属于服务器线程，不能直接在另一个线程使用。需要在目标线程创建新的 `QTcpSocket`，再用 `setSocketDescriptor()` 接管传入的原生描述符。代理场景下，描述符可能不是可供普通原生 socket API 操作的真实套接字，只应交给 Qt 套接字接口。

### 3. 限制 TCP 接收缓冲

默认 `readBufferSize()` 为 0，表示 Qt 层不限制接收缓冲。实时流、协议解析器或不希望内存无限增长的程序可以设置正数；当应用不及时读取时，Qt 会减少继续向应用缓冲数据的速度。

这个设置只影响 Qt/QIODevice 层缓冲，不等同于操作系统的 `SO_RCVBUF`。后者通过 `setSocketOption(ReceiveBufferSizeSocketOption, value)` 设置。

### 4. 无事件循环的阻塞客户端

在专用工作线程中，可以这样写：

```cpp
socket->connectToHost(host, port);
if (!socket->waitForConnected(5000)) {
    reportError(socket->errorString());
    return;
}

socket->write(request);
if (!socket->waitForBytesWritten(5000) ||
    !socket->waitForReadyRead(5000)) {
    reportError(socket->errorString());
    return;
}
const QByteArray response = socket->readAll();
```

阻塞函数会阻塞调用线程。不要把它们放在 GUI 线程，否则窗口和事件处理会一起卡住。Windows 上 `waitForBytesWritten()` 和 `waitForDisconnected()` 可能出现偶发失败，跨平台应用更适合使用事件循环和信号。

### 5. 套接字选项和代理

`LowDelayOption` 可映射 TCP_NODELAY，`KeepAliveOption` 可启用保活，发送/接收缓冲选项映射到操作系统 socket 选项。套接字必须已经创建，选项才有确定作用；通常在 `bind()` 成功后或 `connected()` 发出后再设置。

`setProxy()` 设置单个套接字的显式代理。默认 `DefaultProxy` 会使用应用级代理或代理工厂；`NoProxy` 才是明确禁用代理。已经开始连接后再修改代理不会改变当前连接。

## 关键 API 语义与边界

### 异步状态优先，阻塞 API 只放在合适线程

异步模式下，状态通过 `stateChanged()`，连接成功通过 `connected()`，断开通过 `disconnected()`，错误通过 `errorOccurred()` 通知。不要只依赖一次 `connectToHost()` 调用后的即时 `state()`，因为 DNS 和连接建立都是异步过程。

阻塞函数的 `msecs` 单位是毫秒；`-1` 表示不超时。`waitForConnected()` 可能因为主机名解析而略微超过给定时间；超时后连接过程会被中止。`waitForReadyRead()` 返回 `false` 时，应区分超时、断开和错误，结合 `state()`、`error()` 和 `errorString()` 判断。

### 优雅断开与立即中止

- `disconnectFromHost()` 进入 `ClosingState`，尽量先发送完待写数据，随后进入 `UnconnectedState` 并发出 `disconnected()`。
- `abort()` 立即中止连接并丢弃待写数据。
- `close()` 关闭 QIODevice，并调用 `disconnectFromHost()`，因此一般是优雅关闭。

远端关闭时，Qt 可能先发出 `errorOccurred(RemoteHostClosedError)`，此时状态仍可能是 `ConnectedState`，之后再发出 `disconnected()`。

### 绑定语义依协议和平台而变

`bind(address, port, mode)` 成功后进入 `BoundState`。端口为 0 时由操作系统选择临时端口。对 UDP，绑定地址和端口后，收到数据会触发继承自 `QIODevice` 的 `readyRead()`；对 TCP，绑定通常用于服务器监听前选择本地地址，或在多网卡机器上指定外发接口。

`ShareAddress`、`DontShareAddress` 和 `ReuseAddressHint` 的具体效果受操作系统影响。`DefaultForPlatform` 让 Qt 选择平台默认策略；跨平台服务端不要只凭枚举名称推断端口复用行为，应在目标系统验证。

### 缓冲区分为 Qt 层和操作系统层

`setReadBufferSize()` 只控制 Qt 内部接收缓冲。0 表示不限大小，适合不希望丢数据但可能带来内存增长；正数可施加背压。Qt 文档特别指出，`QUdpSocket` 不使用该 Qt 内部缓冲，而依赖操作系统提供的 UDP 缓冲，因此对 UDP 调用它没有效果。

`bytesAvailable()` 是 Qt 当前可读字节数，`bytesToWrite()` 是等待写出的 Qt 缓冲字节数。`flush()` 通常不需要调用，控制权回到事件循环时 Qt 会自动发送；没有事件循环时可用 `waitForBytesWritten()`。

### 原生描述符不是永远可用

`socketDescriptor()` 在未连接状态通常返回 `-1`。使用代理时，返回的描述符可能是 Qt 内部代理连接，不能直接交给原生 socket 函数。`setSocketDescriptor()` 会清空读写缓冲、设置状态和打开模式；同一个原生描述符不能同时初始化两个 `QAbstractSocket`。

### `pauseMode` 是 TLS 扩展点

默认 `PauseNever`。若设置 `PauseOnSslErrors`，套接字在收到 `QSslSocket::sslErrors()` 后暂停传输，处理完证书策略后必须调用 `resume()`。该设置必须在连接服务器之前完成；未暂停时调用 `resume()` 属于未定义行为。

## API 速查表

### 成员类型

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `enum SocketType` | 标记底层协议类型。 | `TcpSocket`、`UdpSocket`、`SctpSocket`、`UnknownSocketType = -1`；通常由具体派生类确定。 |
| `enum NetworkLayerProtocol` | 选择 IPv4、IPv6 或任意 IP 协议。 | `IPv4Protocol`、`IPv6Protocol`、`AnyIPProtocol`、`UnknownNetworkLayerProtocol = -1`。 |
| `enum SocketError` | 描述套接字、代理、SSL 和临时网络错误。 | `UnknownSocketError = -1`；错误码本身不是可读文本，配合 `errorString()`。 |
| `enum SocketState` | 描述套接字所处阶段。 | `UnconnectedState`、`HostLookupState`、`ConnectingState`、`ConnectedState`、`BoundState`、`ListeningState`、`ClosingState`。 |
| `enum SocketOption` | 选择操作系统或 IP/TCP socket 选项。 | 选项是否支持取决于平台和底层协议。 |
| `enum BindFlag` | 控制绑定地址复用策略。 | `DefaultForPlatform = 0x0`、`ShareAddress = 0x1`、`DontShareAddress = 0x2`、`ReuseAddressHint = 0x4`。 |
| `using BindMode = QFlags<BindFlag>` | 组合绑定标志。 | 用按位或组合；实际复用效果仍由平台决定。 |
| `enum PauseMode` | 控制遇到通知时是否暂停传输。 | `PauseNever = 0x0`、`PauseOnSslErrors = 0x1`。 |
| `using PauseModes = QFlags<PauseMode>` | 组合暂停标志。 | 当前主要支持 TLS 错误暂停。 |

### 错误码

| API | 含义 |
| --- | --- |
| `ConnectionRefusedError` | 目标主机拒绝连接。 |
| `RemoteHostClosedError` | 远端关闭连接。 |
| `HostNotFoundError` | 主机名无法解析。 |
| `SocketAccessError` | 访问底层 socket 被拒绝。 |
| `SocketResourceError` | 本地 socket 资源不足。 |
| `SocketTimeoutError` | socket 操作超时。 |
| `DatagramTooLargeError` | UDP 报文超过平台或路径允许的大小。 |
| `NetworkError` | 一般网络错误。 |
| `AddressInUseError` | 地址或端口已被占用。 |
| `SocketAddressNotAvailableError` | 请求的本地地址不可用。 |
| `UnsupportedSocketOperationError` | 当前协议或平台不支持该操作。 |
| `UnfinishedSocketOperationError` | 操作尚未完成。 |
| `ProxyAuthenticationRequiredError` | 代理要求认证。 |
| `SslHandshakeFailedError` | TLS 握手失败。 |
| `ProxyConnectionRefusedError`、`ProxyConnectionClosedError`、`ProxyConnectionTimeoutError`、`ProxyNotFoundError`、`ProxyProtocolError` | 代理连接或代理协议失败。 |
| `OperationError` | 操作无法执行。 |
| `SslInternalError`、`SslInvalidUserDataError` | TLS 内部或用户数据错误。 |
| `TemporaryError` | 临时错误，可能适合按策略重试。 |
| `UnknownSocketError` | 未分类错误。 |

### 构造、连接和关闭

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `QAbstractSocket(SocketType socketType, QObject *parent)` | 初始化抽象套接字的协议类型。 | 通常由派生类构造函数调用。 |
| `virtual ~QAbstractSocket()` | 销毁套接字并释放关联资源。 | QObject parent 会影响对象生命周期。 |
| `void connectToHost(const QString &hostName, quint16 port, OpenMode mode = ReadWrite, NetworkLayerProtocol protocol = AnyIPProtocol)` | 异步解析主机并建立连接。 | 状态依次经过查找和连接；端口按本机字节序传入。 |
| `void connectToHost(const QHostAddress &address, quint16 port, OpenMode mode = ReadWrite)` | 使用已知地址异步连接。 | 不需要 DNS，但仍是异步连接。 |
| `bool bind(const QHostAddress &address, quint16 port = 0, BindMode mode = DefaultForPlatform)` | 绑定本地地址和端口。 | 成功后进入 `BoundState`；port 为 0 时系统选择端口。 |
| `bool bind(quint16 port = 0, BindMode mode = DefaultForPlatform)` | 绑定任意本地地址。 | Qt 6 文档中为便捷重载；Qt 7 还提供 `SpecialAddress` 重载。 |
| `void disconnectFromHost()` | 尽量发送完待写数据后优雅断开。 | 可能先进入 `ClosingState`。 |
| `void abort()` | 立即中止连接并丢弃待写数据。 | 与 `disconnectFromHost()` 的可靠发送语义不同。 |
| `void close()` | 关闭 QIODevice 并请求断开 socket。 | 通常相当于关闭设备加优雅断开。 |
| `bool isValid() const` | 查询 socket 是否有效且可使用。 | 读写前仍须确认状态为 `ConnectedState`。 |

### 状态、地址和缓冲

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `SocketType socketType() const` | 返回底层协议类型。 | 由 `QTcpSocket`、`QUdpSocket` 等决定。 |
| `SocketState state() const` | 返回当前状态。 | 配合 `stateChanged()` 使用。 |
| `SocketError error() const` | 返回最近一次错误。 | 配合 `errorString()` 获取文本。 |
| `QHostAddress localAddress() const` | 查询本地地址。 | 不可用时返回 `QHostAddress::Null`。 |
| `quint16 localPort() const` | 查询本地端口。 | 不可用时返回 0。 |
| `QHostAddress peerAddress() const` | 查询已连接对端地址。 | 非 `ConnectedState` 时返回 `QHostAddress::Null`。 |
| `quint16 peerPort() const` | 查询对端端口。 | 非 `ConnectedState` 时返回 0。 |
| `QString peerName() const` | 返回 `connectToHost()` 传入的主机名。 | 未调用连接函数时为空，不一定是反向 DNS 名称。 |
| `qint64 bytesAvailable() const` | 查询当前可读字节数。 | 继承 QIODevice 的读缓冲概念。 |
| `qint64 bytesToWrite() const` | 查询等待发送的字节数。 | 回到事件循环或调用 `flush()` 后发送。 |
| `qint64 readBufferSize() const` | 查询 Qt 内部读缓冲限制。 | 0 表示无限；QUdpSocket 不使用该缓冲。 |
| `void setReadBufferSize(qint64 size)` | 设置 Qt 内部读缓冲限制。 | 正数可限制内存，0 恢复无限。 |
| `bool flush()` | 尝试立即发送已缓冲数据。 | 通常不必调用；无事件循环时更适合 `waitForBytesWritten()`。 |

### 原生 socket 和选项

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `qintptr socketDescriptor() const` | 返回原生 socket 描述符。 | 不可用时为 -1；代理场景下不保证可交给原生 API。 |
| `bool setSocketDescriptor(qintptr descriptor, SocketState state = ConnectedState, OpenMode mode = ReadWrite)` | 用已有描述符初始化 Qt socket。 | 会清空 Qt 读写缓冲；同一描述符不能被两个抽象套接字接管。 |
| `void setSocketOption(SocketOption option, const QVariant &value)` | 设置操作系统 socket 选项。 | socket 创建后才有确定效果，通常在 bind 或 connected 后设置。 |
| `QVariant socketOption(SocketOption option)` | 读取 socket 选项。 | 不支持或平台不提供时返回值可能无效。 |
| `LowDelayOption` | TCP_NODELAY，减少小包等待。 | 只对支持的连接型协议有意义。 |
| `KeepAliveOption` | SO_KEEPALIVE，启用保活探测。 | 是否探测以及间隔受系统配置影响。 |
| `MulticastTtlOption` | 设置组播 TTL。 | 主要用于 UDP 组播。 |
| `MulticastLoopbackOption` | 控制本机是否接收自己发出的组播。 | 由平台网络栈决定细节。 |
| `TypeOfServiceOption` | 设置 IP 服务类型或流量类别。 | 平台可能忽略或限制。 |
| `SendBufferSizeSocketOption`、`ReceiveBufferSizeSocketOption` | 设置 OS 层发送或接收缓冲。 | 不影响 Qt/QIODevice 缓冲；分别对应 SO_SNDBUF 和 SO_RCVBUF。 |
| `PathMtuSocketOption` | 查询路径最大传输单元。 | 可能无法获得，某些系统支持设置。 |
| `KeepAliveIdleOption`、`KeepAliveIntervalOption`、`KeepAliveCountOption` | 设置保活空闲时间、间隔和探测次数。 | 平台支持情况不同。 |

### 代理、暂停和同步等待

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `PauseModes pauseMode() const` | 查询暂停策略。 | 默认 `PauseNever`。 |
| `void setPauseMode(PauseModes mode)` | 设置 TLS 错误等通知后的暂停行为。 | 必须在连接前调用；`PauseOnSslErrors` 后要调用 `resume()`。 |
| `void resume()` | 恢复暂停的传输。 | 只应在确实暂停后调用，否则行为未定义。 |
| `void setProxy(const QNetworkProxy &proxy)` | 设置该 socket 的显式代理。 | `NoProxy` 禁用；连接开始后修改不影响当前连接。 |
| `QNetworkProxy proxy() const` | 查询该 socket 的显式代理。 | `DefaultProxy` 表示使用应用代理配置或工厂。 |
| `QString protocolTag() const` | 查询代理工厂使用的协议标签。 | 为空时使用默认语义。 |
| `void setProtocolTag(const QString &tag)` | 设置代理查询使用的协议标签。 | 应在连接前设置。 |
| `bool waitForConnected(int msecs = 30000)` | 阻塞等待连接建立。 | `-1` 永不超时；GUI 线程慎用，Windows 可能略超时。 |
| `bool waitForReadyRead(int msecs = 30000)` | 阻塞等待可读数据。 | 失败可能是超时、断开或错误。 |
| `bool waitForBytesWritten(int msecs = 30000)` | 阻塞等待至少一个字节写出。 | Windows 上可能偶发失败，优先事件驱动。 |
| `bool waitForDisconnected(int msecs = 30000)` | 阻塞等待断开。 | 已经断开时返回 false；可先检查状态。 |

### 信号

| 信号 | 语义 | 使用重点 |
| --- | --- | --- |
| `hostFound()` | 主机名解析成功。 | 可能直接在 `connectToHost()` 调用期间发出。 |
| `connected()` | 连接建立成功。 | 本地主机连接可能从 `connectToHost()` 直接发出。 |
| `disconnected()` | 连接已关闭。 | 优雅断开完成后发出。 |
| `stateChanged(SocketState socketState)` | 状态改变。 | 需要跨线程 queued 连接时注意注册元类型。 |
| `errorOccurred(SocketError socketError)` | 发生套接字错误。 | 配合 `errorString()`；需要跨线程传递时注册相应元类型。 |
| `proxyAuthenticationRequired(const QNetworkProxy &, QAuthenticator *)` | 代理要求认证。 | 必须在信号返回前填写 authenticator，不能延迟到 queued 槽。 |

### 保护函数与非成员 API

| API | 用途 | 实现注意 |
| --- | --- | --- |
| `protected qint64 readData(char *data, qint64 maxlen)` | 实现 QIODevice 读取。 | 通常由具体协议类实现。 |
| `protected qint64 readLineData(char *data, qint64 maxlen)` | 实现按行读取。 | 需保持 QIODevice 返回值契约。 |
| `protected qint64 skipData(qint64 maxSize)` | 跳过输入数据。 | Qt 版本支持情况以基类契约为准。 |
| `protected qint64 writeData(const char *data, qint64 len)` | 实现 QIODevice 写入。 | 具体协议将其放入发送缓冲。 |
| `protected void setSocketState(SocketState state)` | 更新状态并触发状态通知。 | 自定义派生类应维护合法状态迁移。 |
| `protected void setSocketError(SocketError error)` | 设置最近一次错误。 | 不等同于自动发出 `errorOccurred()`。 |
| `protected void setLocalPort(quint16 port)`、`setLocalAddress(const QHostAddress &address)` | 设置本地端点信息。 | 自定义实现填充状态用。 |
| `protected void setPeerPort(quint16 port)`、`setPeerAddress(const QHostAddress &address)`、`setPeerName(const QString &name)` | 设置对端信息。 | 与 `peer*()` 查询保持一致。 |
| `Q_DECLARE_OPERATORS_FOR_FLAGS(BindMode)` | 为 BindMode 提供按位运算。 | 可使用 `flag1 | flag2`。 |
| `Q_DECLARE_OPERATORS_FOR_FLAGS(PauseModes)` | 为 PauseModes 提供按位运算。 | 可组合暂停标志。 |
| `operator<<(QDebug, SocketError)` | 将错误枚举写入调试流。 | 仅在未禁用 debug stream 时提供。 |
| `operator<<(QDebug, SocketState)` | 将状态枚举写入调试流。 | 仅在未禁用 debug stream 时提供。 |
