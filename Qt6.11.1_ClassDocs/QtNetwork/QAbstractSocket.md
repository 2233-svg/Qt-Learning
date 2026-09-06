# QAbstractSocket

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QAbstractSocket` 是 Qt Network 的“抽象套接字”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QAbstractSocket` 是 Qt Network 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractSocket>`
- 继承自：QIODevice
- 直接派生类：QTcpSocket、QUdpSocket

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum BindFlag { ShareAddress, DontShareAddress, ReuseAddressHint, DefaultForPlatform }`
- `flags BindMode`
- `enum NetworkLayerProtocol { IPv4Protocol, IPv6Protocol, AnyIPProtocol, UnknownNetworkLayerProtocol }`
- `enum PauseMode { PauseNever, PauseOnSslErrors }`
- `flags PauseModes`
- `enum SocketError { ConnectionRefusedError, RemoteHostClosedError, HostNotFoundError, SocketAccessError, SocketResourceError, …, UnknownSocketError }`
- `enum SocketOption { LowDelayOption, KeepAliveOption, MulticastTtlOption, MulticastLoopbackOption, TypeOfServiceOption, …, KeepAliveCountOption }`
- `enum SocketState { UnconnectedState, HostLookupState, ConnectingState, ConnectedState, BoundState, …, ListeningState }`
- `enum SocketType { TcpSocket, UdpSocket, SctpSocket, UnknownSocketType }`

### 公有函数

- `QAbstractSocket(QAbstractSocket::SocketType socketType, QObject *parent)`
- `virtual ~QAbstractSocket()`
- `void abort()`
- `virtual bool bind(const QHostAddress &address, quint16 port = 0, QAbstractSocket::BindMode mode = DefaultForPlatform)`
- `bool bind(quint16 port = 0, QAbstractSocket::BindMode mode = DefaultForPlatform)`
- `(since 6.2) bool bind(QHostAddress::SpecialAddress addr, quint16 port = 0, QAbstractSocket::BindMode mode = DefaultForPlatform)`
- `virtual void connectToHost(const QString &hostName, quint16 port, QIODeviceBase::OpenMode openMode = ReadWrite, QAbstractSocket::NetworkLayerProtocol protocol = AnyIPProtocol)`
- `void connectToHost(const QHostAddress &address, quint16 port, QIODeviceBase::OpenMode openMode = ReadWrite)`
- `virtual void disconnectFromHost()`
- `QAbstractSocket::SocketError error() const`
- `bool flush()`
- `bool isValid() const`
- `QHostAddress localAddress() const`
- `quint16 localPort() const`
- `QAbstractSocket::PauseModes pauseMode() const`
- `QHostAddress peerAddress() const`
- `QString peerName() const`
- `quint16 peerPort() const`
- `QString protocolTag() const`
- `QNetworkProxy proxy() const`
- `qint64 readBufferSize() const`
- `virtual void resume()`
- `void setPauseMode(QAbstractSocket::PauseModes pauseMode)`
- `void setProtocolTag(const QString &tag)`
- `void setProxy(const QNetworkProxy &networkProxy)`
- `virtual void setReadBufferSize(qint64 size)`
- `virtual bool setSocketDescriptor(qintptr socketDescriptor, QAbstractSocket::SocketState socketState = ConnectedState, QIODeviceBase::OpenMode openMode = ReadWrite)`
- `virtual void setSocketOption(QAbstractSocket::SocketOption option, const QVariant &value)`
- `virtual qintptr socketDescriptor() const`
- `virtual QVariant socketOption(QAbstractSocket::SocketOption option)`
- `QAbstractSocket::SocketType socketType() const`
- `QAbstractSocket::SocketState state() const`
- `virtual bool waitForConnected(int msecs = 30000)`
- `virtual bool waitForDisconnected(int msecs = 30000)`

### 重实现的公有函数

- `virtual qint64 bytesAvailable() const override`
- `virtual qint64 bytesToWrite() const override`
- `virtual void close() override`
- `virtual bool isSequential() const override`
- `virtual bool waitForBytesWritten(int msecs = 30000) override`
- `virtual bool waitForReadyRead(int msecs = 30000) override`

### 信号

- `void connected()`
- `void disconnected()`
- `void errorOccurred(QAbstractSocket::SocketError socketError)`
- `void hostFound()`
- `void proxyAuthenticationRequired(const QNetworkProxy &proxy, QAuthenticator *authenticator)`
- `void stateChanged(QAbstractSocket::SocketState socketState)`

### 保护函数

- `void setLocalAddress(const QHostAddress &address)`
- `void setLocalPort(quint16 port)`
- `void setPeerAddress(const QHostAddress &address)`
- `void setPeerName(const QString &name)`
- `void setPeerPort(quint16 port)`
- `void setSocketError(QAbstractSocket::SocketError socketError)`
- `void setSocketState(QAbstractSocket::SocketState state)`

### 重实现的保护函数

- `virtual qint64 readData(char *data, qint64 maxSize) override`
- `virtual qint64 readLineData(char *data, qint64 maxlen) override`
- `virtual qint64 skipData(qint64 maxSize) override`
- `virtual qint64 writeData(const char *data, qint64 size) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAbstractSocket::BindFlagflags QAbstractSocket::BindMode`

**作用与语义：**

这个枚举描述了你可以通过不同标志来修改`QAbstractSocket::bind()`行为的不同信号。
- `QAbstractSocket::ShareAddress`：`0x1`;允许其他服务绑定到同一地址和端口。当多个进程通过监听同一地址和端口来分担单一服务负载时（例如，拥有多个预分叉监听器的Web服务器可以大大提升响应时间），这非常有用。然而，由于任何服务都允许重新绑定，这一选项受到一定的安全考虑。注意，将此选项与ReuseAddressHint结合后，你还将允许服务重新绑定已有的共享地址。在Unix上，这相当于SO_REUSEADDR套接字选项。在Windows上，这是默认行为，因此该选项被忽略。
- `QAbstractSocket::DontShareAddress`：`0x2`;独占绑定地址和端口，确保不允许其他服务重新绑定。通过将此选项传递给`QAbstractSocket::bind()`，成功时确保只有你的服务监听地址和端口。即使服务通过ReuseAddressHint，也不能重新绑定。该选项比ShareAddress更安全，但在某些操作系统上，需要你以管理员权限运行服务器。在Unix和macOS上，绑定地址和端口的默认行为是不共享，因此忽略此选项。在Windows上，该选项使用SO_EXCLUSIVEADDRUSE套接字选项。
- `QAbstractSocket::ReuseAddressHint`：`0x4`;提示`QAbstractSocket`即使地址和端口已被其他套接字绑定，也应尝试重新绑定服务。在Windows和Unix上，这相当于SO_REUSEADDR套接字选项。
- `QAbstractSocket::DefaultForPlatform`：`0x0`;当前平台的默认选项。在Unix和macOS上，这相当于（DontShareAddress ReuseAddressHint），在Windows上，则等同于ShareAddress。
BindMode 类型是 QFlag 的 typedef<BindFlag>。它存储 BindFlag 值的 OR 组合。

### `enum QAbstractSocket::NetworkLayerProtocol`

**作用与语义：**

该枚举描述了Qt中使用的网络层协议值。
- `QAbstractSocket::IPv4Protocol`：`0`;IPv4
- `QAbstractSocket::IPv6Protocol`：`1`;IPv6
- `QAbstractSocket::AnyIPProtocol`：`2`;IPv4或IPv6
- `QAbstractSocket::UnknownNetworkLayerProtocol`：`-1`;除IPv4和IPv6外

### `enum QAbstractSocket::PauseModeflags QAbstractSocket::PauseModes`

**作用与语义：**

该枚举描述了套接字在持续数据传输时应暂停的行为。目前唯一支持的通知是`QSslSocket::sslErrors()`。
- `QAbstractSocket::PauseNever`：`0x0`;不要暂停套接字的数据传输。这是默认设置，并且与Qt 4的行为一致。
- `QAbstractSocket::PauseOnSslErrors`：`0x1`;收到SSL错误通知后暂停套接字的数据传输。即`QSslSocket::sslErrors()`。
PauseMode 类型是 QFlags 的 typedef<PauseMode>。它存储 PauseMode 值的 OR 组合。

### `enum QAbstractSocket::SocketError`

**作用与语义：**

该枚举描述了可能发生的套接字错误。
- `QAbstractSocket::ConnectionRefusedError`：`0`;连接被对等端拒绝（或超时）。
- `QAbstractSocket::RemoteHostClosedError`：`1`;远程主机关闭了连接。注意，客户端套接字（即该套接字）在发送远程关闭通知后将关闭。
- `QAbstractSocket::HostNotFoundError`：`2`;未找到主机地址。
- `QAbstractSocket::SocketAccessError`：`3`;套接字操作失败，因为应用程序缺乏所需的权限。
- `QAbstractSocket::SocketResourceError`：`4`;本地系统资源耗尽（例如套接字过多）。
- `QAbstractSocket::SocketTimeoutError`：`5`;套接字操作超时。
- `QAbstractSocket::DatagramTooLargeError`：`6`;数据报大于操作系统的限制（最低可达8192字节）。
- `QAbstractSocket::NetworkError`：`7`;网络发生错误（例如，网络电缆被意外拔除）。
- `QAbstractSocket::AddressInUseError`：`8`;指定给`QAbstractSocket::bind()`的地址已在使用中，且设置为排他。
- `QAbstractSocket::SocketAddressNotAvailableError`：`9`;指定给`QAbstractSocket::bind()`的地址不属于主机。
- `QAbstractSocket::UnsupportedSocketOperationError`：`10`;请求的套接字操作不被本地操作系统支持（例如，不支持 IPv6）。
- `QAbstractSocket::ProxyAuthenticationRequiredError`：`12`;套接字使用代理，代理需要认证。
- `QAbstractSocket::SslHandshakeFailedError`：`13`;SSL/TLS握手失败，连接被关闭（仅`QSslSocket`使用）
- `QAbstractSocket::UnfinishedSocketOperationError`：`11`;仅由QAbstractSocketEngine使用，最后尝试的操作尚未完成（仍在后台进行中）。
- `QAbstractSocket::ProxyConnectionRefusedError`：`14`;无法联系代理服务器，因为该服务器的连接被拒绝
- `QAbstractSocket::ProxyConnectionClosedError`：`15`;与代理服务器的连接意外关闭（在与最终节点连接建立之前）
- `QAbstractSocket::ProxyConnectionTimeoutError`：`16`;与代理服务器的连接超时或代理服务器在认证阶段停止响应。
- `QAbstractSocket::ProxyNotFoundError`：`17`;未找到带有`setProxy()`的代理地址（或应用代理）。
- `QAbstractSocket::ProxyProtocolError`：`18`;与代理服务器的连接协商失败，因为代理服务器的响应无法被理解。
- `QAbstractSocket::OperationError`：`19`;在套筒处于不允许操作的状态时尝试操作。
- `QAbstractSocket::SslInternalError`：`20`;所使用的SSL库报告了内部错误。这很可能是由于安装不良或库配置错误所致。
- `QAbstractSocket::SslInvalidUserDataError`：`21`;提供了无效数据（证书、密钥、密码等），其使用导致SSL库出现错误。
- `QAbstractSocket::TemporaryError`：`22`;发生了临时错误（例如，操作会阻塞，而套接字是非阻塞的）。
- `QAbstractSocket::UnknownSocketError`：`-1`;发生了未识别的错误。

### `enum QAbstractSocket::SocketOption`

**作用与语义：**

这个枚举代表套接字上可以设置的选项。如果需要，可以在收到套接字的`connected()`信号后设置，或者在从`QTcpServer`接收到新套接字后设置。
- `QAbstractSocket::LowDelayOption`：`0`;尝试优化套接字以降低延迟。对于`QTcpSocket`，这会设置TCP_NODELAY选项并禁用Nagle算法。将此设置为1以启用。
- `QAbstractSocket::KeepAliveOption`：`1`;将此设置为1以启用SO_KEEPALIVE套接字选项
- `QAbstractSocket::MulticastTtlOption`：`2`;将其设置为整数值以设置IP_MULTICAST_TTL（多播数据报的TTL）套接字选项。
- `QAbstractSocket::MulticastLoopbackOption`：`3`;将此设为1以启用IP_MULTICAST_LOOP（多播回环）套接字选项。
- `QAbstractSocket::TypeOfServiceOption`：`4`;Windows不支持此选项。该选项映射到IP_TOS套接字选项。有关可能的值，请参见下表。
- `QAbstractSocket::SendBufferSizeSocketOption`：`5`;在操作系统层面设置套接字发送缓冲区的字节大小。这映射到SO_SNDBUF套接字选项。该选项不影响`QIODevice`或`QAbstractSocket`缓冲区。该枚举值在Qt 5.3中引入。
- `QAbstractSocket::ReceiveBufferSizeSocketOption`：`6`;在操作系统层面设置套接字接收缓冲区大小（字节）。这映射到SO_RCVBUF套接字选项。该选项不影响`QIODevice`或`QAbstractSocket`缓冲区（见`setReadBufferSize()`）。该枚举值在Qt 5.3中引入。
- `QAbstractSocket::PathMtuSocketOption`：`7`;检索IP栈目前已知的路径最大传输单元（PMTU）值（如有）。部分IP协议栈还允许设置传输的MTU。该枚举值于Qt 5.11引入。
- `QAbstractSocket::KeepAliveIdleOption`：`8`;如果启用KeepAliveOption，连接需要保持空闲的时间（秒数）。该枚举值于Qt 6.11引入。
- `QAbstractSocket::KeepAliveIntervalOption`：`9`;如果启用KeepAliveOption，则指单个保持活探针之间的秒数。并非所有操作系统都支持此选项。该枚举值是在Qt 6.11中引入的。
- `QAbstractSocket::KeepAliveCountOption`：`10`;如果启用KeepAliveOption，TCP在断开连接前可发送的最大保持活探测数量。该选项并非所有操作系统都支持。该枚举值于Qt 6.11引入。
TypeOfServiceOption 可能的值有：
- `Value`：描述
- `224`：网络控制
- `192`：网络间控制
- `160`：CRITIC/ECP
- `128`：闪烁覆盖
- `96`：闪电侠
- `64`：立即
- `32`：优先级
- `0`：例行公事

### `enum QAbstractSocket::SocketState`

**作用与语义：**

该枚举描述了套筒可能处于的不同状态。
- `QAbstractSocket::UnconnectedState`：`0`;套接字未连接。
- `QAbstractSocket::HostLookupState`：`1`;套接字正在执行主机名称查询。
- `QAbstractSocket::ConnectingState`：`2`;套接字已开始建立连接。
- `QAbstractSocket::ConnectedState`：`3`;建立联系。
- `QAbstractSocket::BoundState`：`4`;套接字绑定在地址和端口。
- `QAbstractSocket::ClosingState`：`6`;套接字即将关闭（数据可能仍在等待写入）。
- `QAbstractSocket::ListeningState`：`5`;仅供内部使用。

### `enum QAbstractSocket::SocketType`

**作用与语义：**

该枚举描述了传输层协议。
- `QAbstractSocket::TcpSocket`：`0`;TCP
- `QAbstractSocket::UdpSocket`：`1`;统一民主党（UDP）
- `QAbstractSocket::SctpSocket`：`2`;SCTP
- `QAbstractSocket::UnknownSocketType`：`-1`;除TCP、UDP和SCTP外

### `QAbstractSocket::QAbstractSocket(QAbstractSocket::SocketType socketType, QObject *parent)`

**作用与语义：**

创建一个新的类型为`socketType`的抽象套接字。`parent`参数传递给`QObject`的构造函数。

### `[virtual noexcept] QAbstractSocket::~QAbstractSocket()`

**作用与语义：**

会毁坏套接字。

### `void QAbstractSocket::abort()`

**作用与语义：**

中止当前连接并重置套接字。与`disconnectFromHost()`不同，该函数立即关闭套接字，丢弃写缓冲区中未处理的数据。

### `[virtual] bool QAbstractSocket::bind(const QHostAddress &address, quint16 port = 0, QAbstractSocket::BindMode mode = DefaultForPlatform)`

**作用与语义：**

用`BindMode` `mode`绑定到`port`端口的`address`。
对于 UDP 套接字，绑定后，每当 UDP 数据报到达指定地址和端口时，信号`QUdpSocket::readyRead()`就会发出。因此，这个功能对于编写 UDP 服务器非常有用。
对于TCP套接字，该函数可用于指定输出连接的接口，这在多个网络接口的情况下非常有用。
默认情况下，套接字通过`DefaultForPlatform` `BindMode`绑定。如果未指定端口，则随机选择端口。
成功时，函数返回`true`，套接字进入`BoundState`;否则返回`false`。

### `bool QAbstractSocket::bind(quint16 port = 0, QAbstractSocket::BindMode mode = DefaultForPlatform)`

**作用与语义：**

通过`BindMode` `mode`绑定到端口`port`的 `QHostAddress`：any。
默认情况下，套接字被绑定为`DefaultForPlatform` `BindMode`。如果未指定端口，则选择随机端口。

### `[since 6.2] bool QAbstractSocket::bind(QHostAddress::SpecialAddress addr, quint16 port = 0, QAbstractSocket::BindMode mode = DefaultForPlatform)`

**作用与语义：**

通过`BindMode` `mode`绑定到端口`port`的特殊地址`addr`。
默认情况下，套接字通过`DefaultForPlatform` `BindMode`绑定。如果未指定端口，则随机选择端口。

### `[override virtual] qint64 QAbstractSocket::bytesAvailable() const`

**作用与语义：**

重实现自：`QIODevice::bytesAvailable()` const.
返回等待读取的输入字节数。

### `[override virtual] qint64 QAbstractSocket::bytesToWrite() const`

**作用与语义：**

重装：`QIODevice::bytesToWrite()` const.
返回等待写入的字节数。当控制返回事件循环或调用`flush()`时，字节会被写入。

### `[override virtual] void QAbstractSocket::close()`

**作用与语义：**

重装：`QIODevice::close()`。
关闭套接字的I/O设备，并调用`disconnectFromHost()`关闭套接字连接。
关于关闭I/O设备时发生的动作，请参见`QIODevice::close()`。

### `[virtual] void QAbstractSocket::connectToHost(const QString &hostName, quint16 port, QIODeviceBase::OpenMode openMode = ReadWrite, QAbstractSocket::NetworkLayerProtocol protocol = AnyIPProtocol)`

**作用与语义：**

尝试在给定`port`上与`hostName`建立连接。`protocol`参数可用于指定使用哪种网络协议（例如：IPv4 或 IPv6）。
套接字在给定`openMode`中打开，首先进入`HostLookupState`，然后对`hostName`进行主机名查询。如果查询成功，`hostFound()`会被发射，`QAbstractSocket`进入`ConnectingState`。然后尝试连接到查找返回的地址或多个地址。最后，如果建立连接，`QAbstractSocket`进入`ConnectedState`并发出`connected()`。
套接字随时可以发出`errorOccurred()`信号，提示发生了错误。
`hostName`可以是字符串形式的IP地址（例如，“43.195.83.32”），也可以是主机名（例如，“example.com”）。`QAbstractSocket`只有在需要时才会进行查找。`port`按本地字节顺序排列。

### `void QAbstractSocket::connectToHost(const QHostAddress &address, quint16 port, QIODeviceBase::OpenMode openMode = ReadWrite)`

**作用与语义：**

尝试连接端口`port` `address`。

### `[signal] void QAbstractSocket::connected()`

**作用与语义：**

该信号是在`connectToHost()`被调用并成功建立连接后发出的。
注意：在某些操作系统上，connected() 信号可能直接从连接本地主机的 `connectToHost()`调用发出。

### `[virtual] void QAbstractSocket::disconnectFromHost()`

**作用与语义：**

尝试关闭套接字。如果有待写入的数据，`QAbstractSocket`会进入`ClosingState`并等待所有数据写入完成。最终，它会进入`UnconnectedState`并发出`disconnected()`信号。

### `[signal] void QAbstractSocket::disconnected()`

**作用与语义：**

当套接字断开时，该信号会发出。
警告：如果你需要删除连接该信号的槽函数中的`sender()`，请使用`deleteLater()`功能。

### `QAbstractSocket::SocketError QAbstractSocket::error() const`

**作用与语义：**

返回最后一次发生的错误类型。

### `[signal] void QAbstractSocket::errorOccurred(QAbstractSocket::SocketError socketError)`

**作用与语义：**

该信号是在错误发生后发出的。`socketError`参数描述了发生的错误类型。
当该信号发出时，套接字可能还没准备好进行重连尝试。在这种情况下，重新连接的尝试应从事件循环中进行。例如，使用QChronoTimer：：singleShot()，超时为0ns。
`QAbstractSocket::SocketError`不是注册元类型，所以对于排队连接，你需要用`Q_DECLARE_METATYPE()`和`qRegisterMetaType()`注册它。

### `bool QAbstractSocket::flush()`

**作用与语义：**

该函数尽可能多地从内部写入缓冲区写入底层网络套接字，且不阻塞。如果写入了任何数据，该函数返回`true`;否则返回false。
如果你需要`QAbstractSocket`立即开始发送缓冲数据，可以调用这个函数。成功写入的字节数取决于操作系统。在大多数情况下，你不需要调用这个函数，因为一旦控制返回事件循环，系统会自动开始发送数据`QAbstractSocket`。如果没有事件循环，则调用 `waitForBytesWritten()`。

### `[signal] void QAbstractSocket::hostFound()`

**作用与语义：**

该信号是在`connectToHost()`被调用且主机查询成功后发出的。
注意：自Qt 4.6.3起，`QAbstractSocket`可能直接从`connectToHost()`调用中发送hostFound()，因为DNS结果可能被缓存。

### `[override virtual] bool QAbstractSocket::isSequential() const`

**作用与语义：**

重装：`QIODevice::isSequential()` const.

### `bool QAbstractSocket::isValid() const`

**作用与语义：**

如果套接字有效且准备好使用，返回`true`;否则返回`false`。
注意：套接字的状态必须`ConnectedState`才能进行读写。

### `QHostAddress QAbstractSocket::localAddress() const`

**作用与语义：**

如果有本地套接字的主机地址，返回;否则返回`QHostAddress::Null`。
这通常是主机的主IP地址，但也可以`QHostAddress::LocalHost`（127.0.0.1）以连接本地主机。

### `quint16 QAbstractSocket::localPort() const`

**作用与语义：**

如果有，返回本地套接字的主机端口号（按本地字节顺序）;否则返回0。

### `QAbstractSocket::PauseModes QAbstractSocket::pauseMode() const`

**作用与语义：**

返回该套筒的暂停模式。

### `QHostAddress QAbstractSocket::peerAddress() const`

**作用与语义：**

如果套接字处于`ConnectedState`，返回连接节点的地址;否则返回`QHostAddress::Null`。

### `QString QAbstractSocket::peerName() const`

**作用与语义：**

返回由 `connectToHost()` 指定的对等端名称，若未调用`connectToHost()`则返回空 `QString`。

### `quint16 QAbstractSocket::peerPort() const`

**作用与语义：**

如果套接字处于`ConnectedState`，返回连接节点的端口;否则返回0。

### `QString QAbstractSocket::protocolTag() const`

**作用与语义：**

返回该套接字的协议标签。如果协议标签被设置，则在内部创建该标签以指示将使用协议标签时，该标签会传递给`QNetworkProxyQuery`。

### `QNetworkProxy QAbstractSocket::proxy() const`

**作用与语义：**

返回该套接字的网络代理。默认情况下使用`QNetworkProxy::DefaultProxy`，这意味着该套接字会查询该应用的默认代理设置。

### `[signal] void QAbstractSocket::proxyAuthenticationRequired(const QNetworkProxy &proxy, QAuthenticator *authenticator)`

**作用与语义：**

当使用需要认证的`proxy`时，可以发出该信号。 `authenticator`随后可以填写所需信息，从而允许认证并继续连接。
注意：无法使用队列连接连接该信号，因为如果信号返回时认证器未输入新信息，连接将失败。

### `qint64 QAbstractSocket::readBufferSize() const`

**作用与语义：**

返回内部读取缓冲区的大小。这限制了客户端在调用`read()`或`readAll()`之前能接收的数据量。
读取缓冲区大小为0（默认值）意味着缓冲区没有大小限制，确保不会丢失数据。

### `[override virtual protected] qint64 QAbstractSocket::readData(char *data, qint64 maxSize)`

**作用与语义：**

从套接字接收缓冲区复制最多 `maxSize` 字节到 `data`，返回读取字节数，失败返回 -1。这是供 `QIODevice::read()` 调用的受保护实现；异步代码应先响应 `readyRead()`，不要直接调用它或阻塞轮询。

### `[override virtual protected] qint64 QAbstractSocket::readLineData(char *data, qint64 maxlen)`

**作用与语义：**

重新实现：`QIODevice::readLineData`（char *data， qint64 maxSize）.

### `[virtual] void QAbstractSocket::resume()`

**作用与语义：**

继续在套接字上传输数据。该方法应仅在套接字被设置为通知暂停且收到通知后使用。目前唯一支持的通知是`QSslSocket::sslErrors()`。如果套接字未暂停，调用此方法会导致行为未定义。

### `[protected] void QAbstractSocket::setLocalAddress(const QHostAddress &address)`

**作用与语义：**

将连接的本地地址设置为`address`。
你可以在`QAbstractSocket`的子类中调用该函数，在连接建立后更改`localAddress()`函数的返回值。此功能通常被代理连接用于虚拟连接设置。
注意，该函数不会绑定连接前套接字的本地地址（例如`QAbstractSocket::bind()`）。

### `[protected] void QAbstractSocket::setLocalPort(quint16 port)`

**作用与语义：**

将端口设置在连接的本地端`port`。
你可以在`QAbstractSocket`的子类中调用该函数，在连接建立后更改`localPort()`函数的返回值。该功能通常被代理连接用于虚拟连接设置。
注意，该函数不会在连接前绑定套接字的本地端口（例如`QAbstractSocket::bind()`）。

### `void QAbstractSocket::setPauseMode(QAbstractSocket::PauseModes pauseMode)`

**作用与语义：**

控制收到通知后是否暂停。`pauseMode`参数指定了套接字应暂停的条件。目前唯一支持的通知是`QSslSocket::sslErrors()`。如果设置为`PauseOnSslErrors`，套接字上的数据传输将暂停，需要通过调用`resume()`显式重新启用。默认情况下，该选项设置为`PauseNever`。该选项必须在连接到服务器前调用，否则会导致行为未定义。

### `[protected] void QAbstractSocket::setPeerAddress(const QHostAddress &address)`

**作用与语义：**

将连接远端地址设置为`address`。
你可以在`QAbstractSocket`的子类中调用该函数，在连接建立后更改`peerAddress()`函数的返回值。该功能通常被代理连接用于虚拟连接设置。

### `[protected] void QAbstractSocket::setPeerName(const QString &name)`

**作用与语义：**

将远程节点的主机名设置为`name`。
你可以在`QAbstractSocket`的子类中调用该函数，在连接建立后更改`peerName()`函数的返回值。该功能通常被代理连接用于虚拟连接设置。

### `[protected] void QAbstractSocket::setPeerPort(quint16 port)`

**作用与语义：**

将连接远端端口设置为`port`。
你可以在`QAbstractSocket`的子类中调用该函数，在连接建立后更改`peerPort()`函数的返回值。该功能通常被代理连接用于虚拟连接设置。

### `void QAbstractSocket::setProtocolTag(const QString &tag)`

**作用与语义：**

将该套接字的协议标签设置为`tag`。

### `void QAbstractSocket::setProxy(const QNetworkProxy &networkProxy)`

**作用与语义：**

将该套接字的显式网络代理设置为`networkProxy`。
要禁用该套接字的代理，请使用`QNetworkProxy::NoProxy`代理类型：
代理的默认值是`QNetworkProxy::DefaultProxy`，这意味着套接字会使用应用设置：如果代理设置为`QNetworkProxy::setApplicationProxy`，则使用该设置;否则，如果工厂设置为`QNetworkProxyFactory::setApplicationProxyFactory`，它会查询该工厂，类型为`QNetworkProxyQuery::TcpSocket`。

**官方示例：**

```cpp
 socket->setProxy(QNetworkProxy::NoProxy);
```

### `[virtual] void QAbstractSocket::setReadBufferSize(qint64 size)`

**作用与语义：**

将`QAbstractSocket`内部读取缓冲区的大小设置为`size`字节。
如果缓冲区大小被限制在某个特定大小，`QAbstractSocket`不会缓冲超过这个大小的数据。例外情况下，缓冲区大小为0意味着读取缓冲区是无限的，所有输入数据都被缓冲。这是默认设置。
如果你只在特定时间点读取数据（例如在实时流媒体应用中），或者想保护套接字免受过多数据接收，避免最终导致内存不足，这个选项非常有用。
只有`QTcpSocket`使用`QAbstractSocket`的内部缓冲区;`QUdpSocket` 完全不使用缓冲，而是依赖操作系统提供的隐式缓冲。因此，调用该函数在`QUdpSocket`上没有效果。

### `[virtual] bool QAbstractSocket::setSocketDescriptor(qintptr socketDescriptor, QAbstractSocket::SocketState socketState = ConnectedState, QIODeviceBase::OpenMode openMode = ReadWrite)`

**作用与语义：**

用本地套接字描述符`socketDescriptor`初始化`QAbstractSocket`。如果`socketDescriptor`被接受为有效的套接字描述符，返回`true`;否则返回`false`。套接字以`openMode`指定的模式打开，进入`socketState`指定的套接字状态。清除读写缓冲区，丢弃任何待处理的数据。
注意：无法用相同的本地套接字描述符初始化两个抽象套接字。

### `[protected] void QAbstractSocket::setSocketError(QAbstractSocket::SocketError socketError)`

**作用与语义：**

将最后一次发生的错误类型设置为`socketError`。

### `[virtual] void QAbstractSocket::setSocketOption(QAbstractSocket::SocketOption option, const QVariant &value)`

**作用与语义：**

将给定`option`设置为`value`描述的值。
注意：由于选项设置在内部套接字上，选项仅在套接字已被创建时生效。这只有在调用`bind()`后或`connected()`已发出时才会生效。

### `[protected] void QAbstractSocket::setSocketState(QAbstractSocket::SocketState state)`

**作用与语义：**

将套筒状态设置为`state`。

### `[override virtual protected] qint64 QAbstractSocket::skipData(qint64 maxSize)`

**作用与语义：**

重装：`QIODevice::skipData`（qint64 maxSize）。

### `[virtual] qintptr QAbstractSocket::socketDescriptor() const`

**作用与语义：**

如果有本地套`QAbstractSocket`描述符，返回该对象的本地套接字描述符;否则返回 -1。
如果套接字使用`QNetworkProxy`，返回的描述符可能无法与本地套接字函数一起使用。
当`QAbstractSocket`处于`UnconnectedState`时，套接字描述符不可用。

### `[virtual] QVariant QAbstractSocket::socketOption(QAbstractSocket::SocketOption option)`

**作用与语义：**

返回`option`期权的价值。

### `QAbstractSocket::SocketType QAbstractSocket::socketType() const`

**作用与语义：**

返回套接字类型（TCP、UDP或其他）。

### `QAbstractSocket::SocketState QAbstractSocket::state() const`

**作用与语义：**

返回套筒的状态。

### `[signal] void QAbstractSocket::stateChanged(QAbstractSocket::SocketState socketState)`

**作用与语义：**

每当`QAbstractSocket`的状态发生变化时，该信号就会发出。`socketState`参数即为新状态。
`QAbstractSocket::SocketState` 不是注册元类型，所以对于排队连接，你需要用 `Q_DECLARE_METATYPE()` 和 `qRegisterMetaType()` 注册。

### `[override virtual] bool QAbstractSocket::waitForBytesWritten(int msecs = 30000)`

**作用与语义：**

重装：`QIODevice::waitForBytesWritten`（int msecs）。
该函数会阻塞，直到至少一个字节写入套接字并发出`bytesWritten()`信号。该函数在`msecs`毫秒后超时;默认超时为30000毫秒。
如果`bytesWritten()`信号被发射，函数返回`true`;否则返回`false`（如果发生错误或操作超时）。
注意：该功能在Windows上可能会随机失败。如果你的软件能在Windows上运行，可以考虑使用事件循环和`bytesWritten()`信号。

### `[virtual] bool QAbstractSocket::waitForConnected(int msecs = 30000)`

**作用与语义：**

等待套接字连接，最多可达`msecs`毫秒。如果连接已建立，该函数返回`true`;否则返回`false`。如果返回`false`，你可以调用`error()`来确定错误原因。
以下示例等待最多一秒以建立连接：
如果 msecs 为 -1，该函数不会超时。
注意：该函数可能比`msecs`稍长，具体取决于完成主机查找所需的时间。
注意：多次调用这些函数不会累计时间。如果函数超时，连接进程将被中止。
注意：该功能在Windows上可能会随机失败。如果你的软件能在Windows上运行，可以考虑使用事件循环和`connected()`信号。

**官方示例：**

```cpp
 socket->connectToHost("imap", 143);
 if (socket->waitForConnected(1000))
     qDebug("Connected!");
```

### `[virtual] bool QAbstractSocket::waitForDisconnected(int msecs = 30000)`

**作用与语义：**

等待套接字断开连接，最多可达`msecs`毫秒。如果连接成功断开，该函数返回`true`;否则返回`false`（如果操作超时、发生错误或该`QAbstractSocket`已断开）。如果返回`false`，你可以调用`error()`来确定错误原因。
以下示例等待连接关闭最多一秒钟：
如果 msecs 为 -1，该函数不会超时。
注意：该功能在Windows上可能会随机失败。如果你的软件能在Windows上运行，可以考虑使用事件循环和`disconnected()`信号。

**官方示例：**

```cpp
 socket->disconnectFromHost();
 if (socket->state() == QAbstractSocket::UnconnectedState
     || socket->waitForDisconnected(1000)) {
         qDebug("Disconnected!");
 }
```

### `[override virtual] bool QAbstractSocket::waitForReadyRead(int msecs = 30000)`

**作用与语义：**

重装：`QIODevice::waitForReadyRead`（int msecs）。
该功能会阻塞，直到有新数据可供读取且`readyRead()`信号已发出。该函数在`msecs`毫秒后超时;默认超时为30000毫秒。
如果`readyRead()`信号被发射且有新数据可用，函数返回`true`;否则返回`false`（如果发生错误或操作超时）。
注意：该功能在Windows上可能会随机失效。如果你的软件能在Windows上运行，可以考虑使用事件循环和`readyRead()`信号。

### `[override virtual protected] qint64 QAbstractSocket::writeData(const char *data, qint64 size)`

**作用与语义：**

把最多 `size` 字节加入套接字发送缓冲区，返回已接受字节数，失败返回 -1。返回成功不表示数据已经到达对端；实际写出进度由 `bytesWritten()` 通知，错误用 `error()` 和 `errorString()` 检查。

### `enum BindFlag { ShareAddress, DontShareAddress, ReuseAddressHint, DefaultForPlatform }`

**作用与语义：**

这个枚举描述了你可以通过不同标志来修改`QAbstractSocket::bind()`行为的不同信号。
- `QAbstractSocket::ShareAddress`：`0x1`;允许其他服务绑定到同一地址和端口。当多个进程通过监听同一地址和端口来分担单一服务负载时（例如，拥有多个预分叉监听器的Web服务器可以大大提升响应时间），这非常有用。然而，由于任何服务都允许重新绑定，这一选项受到一定的安全考虑。注意，将此选项与ReuseAddressHint结合后，你还将允许服务重新绑定已有的共享地址。在Unix上，这相当于SO_REUSEADDR套接字选项。在Windows上，这是默认行为，因此该选项被忽略。
- `QAbstractSocket::DontShareAddress`：`0x2`;独占绑定地址和端口，确保不允许其他服务重新绑定。通过将此选项传递给`QAbstractSocket::bind()`，成功时确保只有你的服务监听地址和端口。即使服务通过ReuseAddressHint，也不能重新绑定。该选项比ShareAddress更安全，但在某些操作系统上，需要你以管理员权限运行服务器。在Unix和macOS上，绑定地址和端口的默认行为是不共享，因此忽略此选项。在Windows上，该选项使用SO_EXCLUSIVEADDRUSE套接字选项。
- `QAbstractSocket::ReuseAddressHint`：`0x4`;提示`QAbstractSocket`即使地址和端口已被其他套接字绑定，也应尝试重新绑定服务。在Windows和Unix上，这相当于SO_REUSEADDR套接字选项。
- `QAbstractSocket::DefaultForPlatform`：`0x0`;当前平台的默认选项。在Unix和macOS上，这相当于（DontShareAddress ReuseAddressHint），在Windows上，则等同于ShareAddress。
BindMode 类型是 QFlag 的 typedef<BindFlag>。它存储 BindFlag 值的 OR 组合。

### `flags BindMode`

**作用与语义：**

这个枚举描述了你可以通过不同标志来修改`QAbstractSocket::bind()`行为的不同信号。
- `QAbstractSocket::ShareAddress`：`0x1`;允许其他服务绑定到同一地址和端口。当多个进程通过监听同一地址和端口来分担单一服务负载时（例如，拥有多个预分叉监听器的Web服务器可以大大提升响应时间），这非常有用。然而，由于任何服务都允许重新绑定，这一选项受到一定的安全考虑。注意，将此选项与ReuseAddressHint结合后，你还将允许服务重新绑定已有的共享地址。在Unix上，这相当于SO_REUSEADDR套接字选项。在Windows上，这是默认行为，因此该选项被忽略。
- `QAbstractSocket::DontShareAddress`：`0x2`;独占绑定地址和端口，确保不允许其他服务重新绑定。通过将此选项传递给`QAbstractSocket::bind()`，成功时确保只有你的服务监听地址和端口。即使服务通过ReuseAddressHint，也不能重新绑定。该选项比ShareAddress更安全，但在某些操作系统上，需要你以管理员权限运行服务器。在Unix和macOS上，绑定地址和端口的默认行为是不共享，因此忽略此选项。在Windows上，该选项使用SO_EXCLUSIVEADDRUSE套接字选项。
- `QAbstractSocket::ReuseAddressHint`：`0x4`;提示`QAbstractSocket`即使地址和端口已被其他套接字绑定，也应尝试重新绑定服务。在Windows和Unix上，这相当于SO_REUSEADDR套接字选项。
- `QAbstractSocket::DefaultForPlatform`：`0x0`;当前平台的默认选项。在Unix和macOS上，这相当于（DontShareAddress ReuseAddressHint），在Windows上，则等同于ShareAddress。
BindMode 类型是 QFlag 的 typedef<BindFlag>。它存储 BindFlag 值的 OR 组合。

### `enum PauseMode { PauseNever, PauseOnSslErrors }`

**作用与语义：**

该枚举描述了套接字在持续数据传输时应暂停的行为。目前唯一支持的通知是`QSslSocket::sslErrors()`。
- `QAbstractSocket::PauseNever`：`0x0`;不要暂停套接字的数据传输。这是默认设置，并且与Qt 4的行为一致。
- `QAbstractSocket::PauseOnSslErrors`：`0x1`;收到SSL错误通知后暂停套接字的数据传输。即`QSslSocket::sslErrors()`。
PauseMode 类型是 QFlags 的 typedef<PauseMode>。它存储 PauseMode 值的 OR 组合。

### `flags PauseModes`

**作用与语义：**

该枚举描述了套接字在持续数据传输时应暂停的行为。目前唯一支持的通知是`QSslSocket::sslErrors()`。
- `QAbstractSocket::PauseNever`：`0x0`;不要暂停套接字的数据传输。这是默认设置，并且与Qt 4的行为一致。
- `QAbstractSocket::PauseOnSslErrors`：`0x1`;收到SSL错误通知后暂停套接字的数据传输。即`QSslSocket::sslErrors()`。
PauseMode 类型是 QFlags 的 typedef<PauseMode>。它存储 PauseMode 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

### 状态和错误边界

请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

### 线程边界

QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractSocket` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
