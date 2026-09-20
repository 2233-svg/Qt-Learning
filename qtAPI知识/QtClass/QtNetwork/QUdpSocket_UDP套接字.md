# QUdpSocket：无连接 UDP 报文

> Qt 6.11.1  
> 头文件：`#include <QUdpSocket>`  
> 模块：`Qt6::Network`  
> 继承：`QAbstractSocket -> QUdpSocket`  
> 相关类型：`QNetworkDatagram`、`QNetworkInterface`

## 它解决什么问题

`QUdpSocket` 用于发送和接收 UDP datagram。UDP 是无连接、面向报文的协议：每次发送保留一个报文边界，但不保证送达、顺序、唯一性或不重复。它适合发现、广播、组播、实时状态和对丢包可容忍的短消息。

Qt 提供两种主要使用方式：

- 未连接 socket：用 `writeDatagram()` 指定每个报文的目标，用 `readDatagram()` 或 `receiveDatagram()` 读取来源信息。
- 调用 `connectToHost()` 建立 UDP 的虚拟连接：Qt 记住一个对端，之后可以用 QIODevice 的 `write()` 和 `read()`；这只是固定默认对端，不会让 UDP 变成可靠协议。

接收端通常先 `bind()`，再监听继承自 `QIODevice` 的 `readyRead()`，并在槽中循环消费所有待处理报文：

```text
bind(address, port)
    -> readyRead()
    -> hasPendingDatagrams()
    -> receiveDatagram() / readDatagram()
```

## 实际使用场景

### 1. 普通 UDP 接收器

```cpp
auto *socket = new QUdpSocket(this);
if (!socket->bind(QHostAddress::AnyIPv4, 45454)) {
    qWarning() << socket->errorString();
    return;
}

connect(socket, &QIODevice::readyRead, this, [socket] {
    while (socket->hasPendingDatagrams()) {
        QNetworkDatagram datagram = socket->receiveDatagram();
        if (!datagram.isValid())
            continue;
        processDatagram(datagram.data(),
                        datagram.senderAddress(),
                        datagram.senderPort());
    }
});
```

收到 `readyRead()` 后应尽快读走报文。Qt 文档特别提醒：如果不读取当前报文，下一份报文到达时不一定再次发出 `readyRead()`，因为读就绪状态一直没有被清空。

### 2. 发送短报文

```cpp
const QByteArray payload = encodeState();
const qint64 sent = socket->writeDatagram(
    payload, QHostAddress("192.0.2.10"), 45454);
if (sent < 0)
    qWarning() << socket->errorString();
```

返回值是发送的字节数，失败返回 -1。UDP 报文作为一个整体提交；过大的报文可能返回 -1，并将错误设置为 `DatagramTooLargeError`。即使平台允许发送较大的报文，IP 分片也会增加丢包风险，短消息通常更可靠。

### 3. 广播

发送广播前通常需要绑定或设置适合的 socket 选项，目标地址可以是 `QHostAddress::Broadcast` 或网段广播地址。广播受操作系统权限、网卡配置、防火墙和路由器策略影响，不应假设所有网络都转发广播。

### 4. IPv4/IPv6 组播

组播接收端先绑定端口，再调用 `joinMulticastGroup()`；退出时用完全相同的组地址和接口参数调用 `leaveMulticastGroup()`。IPv6 在没有显式指定接口时并非所有操作系统都支持，因此多网卡或 IPv6 场景应优先使用带 `QNetworkInterface` 的重载。

`setMulticastInterface()` 设置发出组播使用的网卡，必须在 `BoundState` 下调用；未绑定时调用不会产生效果。TTL 和本机回环则通过 `QAbstractSocket::MulticastTtlOption`、`MulticastLoopbackOption` 设置。

### 5. 需要来源、目的地址或 hop limit 的报文

`receiveDatagram()` 返回 `QNetworkDatagram`，除数据和发送方端点外，在平台支持时还可以携带目的地址、目的端口、接收接口索引和 hop limit。需要保留这些元数据时，优先使用它而不是只写入原始缓冲区的 `readDatagram()`。

## 关键 API 语义与边界

### UDP 报文有边界，但读取缓冲太小会丢尾部

`pendingDatagramSize()` 返回第一个待处理报文的大小；没有报文时返回 -1。使用 `readDatagram()` 时，如果 `maxSize` 小于完整报文大小，超出的部分会丢失；`maxSize == 0` 会直接丢弃整个报文。

`receiveDatagram(-1)` 默认尝试读取完整报文；传入较小的正数仍会截断，传入 0 会丢弃。若使用原始缓冲区接口，先查询 `pendingDatagramSize()`，分配足够空间，再调用 `readDatagram()`。

### `readyRead()` 不是“只来一个报文”

一次 `readyRead()` 可能对应多个报文，所以槽函数应该循环 `hasPendingDatagrams()`。也不要在槽函数中只读取一份，然后等待下一次信号；未清空的读就绪状态可能使后续通知行为不符合直觉。

### 绑定和连接模式

只发送报文时不需要先 `bind()`，操作系统会选择临时本地端口。接收报文必须绑定本地地址和端口。绑定 `QHostAddress::AnyIPv4` 与 `AnyIPv6` 的行为不同，跨地址族通信时应明确选择。

对 UDP 调用 `connectToHost()` 后，QIODevice 的 `read()` 和 `write()` 使用记住的对端。未连接 socket 调用普通 `write()` 没有目标，应该使用 `writeDatagram()`。在已连接 UDP socket 上再调用带目标地址的 `writeDatagram()` 可能失败，连接模式下使用 `write()`。

### 报文大小和可靠性

UDP 的最大可发送大小取决于平台和路径，Qt 文档指出可能低至 8192 字节。大于 512 字节的报文一般不建议发送，因为很可能被 IP 层分片。应用若需要可靠性，应在应用层增加序号、确认、重传、超时和去重，或改用 TCP/QUIC 等更合适的协议。

### 组播接口必须和加入参数一致

默认重载会让操作系统选择接口；显式重载则使用指定的 `QNetworkInterface`。离开组播时应使用与加入时相同的 group address 和 interface。`multicastInterface()` 在未绑定、未设置或平台无法提供时可能返回无效接口。

### 缓冲和线程

`QAbstractSocket::setReadBufferSize()` 对 `QUdpSocket` 没有作用，UDP 依赖操作系统的 socket 缓冲。若接收处理不及时，报文可能在 OS 缓冲满后丢失；应尽量在 `readyRead()` 中快速搬运数据，再交给工作队列处理。

socket 是 QObject，只能在所属线程使用。若接收压力较大，把 socket 放入专用线程并让线程运行事件循环，或在 socket 线程快速读取后把值对象 `QNetworkDatagram` 交给其他线程。

## API 速查表

### 构造和继承行为

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `explicit QUdpSocket(QObject *parent = nullptr)` | 创建 UDP socket。 | 初始状态为 `UnconnectedState`；parent 决定对象所有权和线程归属。 |
| `virtual ~QUdpSocket()` | 销毁 UDP socket。 | 释放底层 socket；信号槽中销毁应使用 `deleteLater()`。 |
| `bind(const QHostAddress &address, quint16 port = 0, BindMode mode = DefaultForPlatform)` | 绑定本地地址和端口。 | 接收前必须绑定；port 为 0 时由系统选择。 |
| `bind(quint16 port = 0, BindMode mode = DefaultForPlatform)` | 绑定任意本地地址。 | IPv4/IPv6 族由平台和默认地址决定；需要明确地址族时使用地址重载。 |
| `connectToHost(hostName, port, openMode, protocol)` | 建立 UDP 虚拟连接。 | 之后可用 `read()`/`write()`；不提供可靠性或消息确认。 |
| `setReadBufferSize(qint64)` | 设置 QAbstractSocket 内部读缓冲。 | 对 QUdpSocket 无效果，实际依赖 OS UDP 缓冲。 |

### 报文接收

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `bool hasPendingDatagrams() const` | 判断是否至少有一个报文等待读取。 | `readyRead()` 槽中通常循环调用。 |
| `qint64 pendingDatagramSize() const` | 返回第一个待处理报文大小。 | 没有报文返回 -1；适合为 `readDatagram()` 分配精确缓冲。 |
| `qint64 readDatagram(char *data, qint64 maxSize, QHostAddress *address = nullptr, quint16 *port = nullptr)` | 读取一个报文和可选来源地址、端口。 | 成功返回报文实际大小；缓冲不足会截断并丢弃尾部；maxSize 为 0 会丢弃报文。 |
| `QNetworkDatagram receiveDatagram(qint64 maxSize = -1)` | 读取一个报文并返回来源及可用的目的地址、接口、hop limit 等元数据。 | 失败返回 invalid datagram；-1 尝试读取完整报文，0 丢弃。 |
| `readyRead()` | 继承自 QIODevice，表示有数据可读。 | 必须在槽中真正读取报文，否则后续通知可能不再出现。 |

### 报文发送

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `qint64 writeDatagram(const char *data, qint64 size, const QHostAddress &address, quint16 port)` | 向指定地址和端口发送一个 UDP 报文。 | 成功返回发送字节数，失败 -1；过大报文可能得到 `DatagramTooLargeError`。 |
| `qint64 writeDatagram(const QByteArray &datagram, const QHostAddress &host, quint16 port)` | QByteArray 便捷重载。 | 仍然是一整个 UDP 报文，不会自动拆分。 |
| `qint64 writeDatagram(const QNetworkDatagram &datagram)` | 按 datagram 中的目标、接口和 hop limit 发送。 | 未设置目标时使用 `connectToHost()` 的对端；已连接 socket 使用带目标重载可能失败。 |
| `bytesWritten(qint64)` | 继承自 QIODevice，表示报文已经写向网络。 | 不表示接收端已收到或处理。 |

### 组播

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `bool joinMulticastGroup(const QHostAddress &groupAddress)` | 在系统选择的默认接口加入组播组。 | socket 必须处于 `BoundState`；IPv6 默认接口选择并非所有系统都支持。 |
| `bool joinMulticastGroup(const QHostAddress &groupAddress, const QNetworkInterface &iface)` | 在指定网卡加入组播组。 | 多网卡和 IPv6 场景更明确。 |
| `bool leaveMulticastGroup(const QHostAddress &groupAddress)` | 在默认接口退出组播组。 | 参数应与加入时相同；必须处于 `BoundState`。 |
| `bool leaveMulticastGroup(const QHostAddress &groupAddress, const QNetworkInterface &iface)` | 在指定网卡退出组播组。 | 必须和加入时使用同一接口语义。 |
| `QNetworkInterface multicastInterface() const` | 查询外发组播使用的接口。 | 未绑定或未设置时可能返回无效接口。 |
| `void setMulticastInterface(const QNetworkInterface &iface)` | 设置外发组播接口。 | 必须在 `BoundState` 下调用；未绑定时无效果。 |
| `setSocketOption(MulticastTtlOption, value)` | 设置组播 TTL。 | 具体范围受 IP 版本和平台影响。 |
| `setSocketOption(MulticastLoopbackOption, value)` | 设置是否回环接收本机发出的组播。 | 平台网络栈可能有差异。 |

### 扩展构造和相关状态 API

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `using QAbstractSocket::bind` | 将基类 bind 重载引入 QUdpSocket。 | Qt 6 兼容声明。 |
| `bind(QHostAddress::SpecialAddress, quint16, BindMode)` | 使用特殊地址便捷绑定。 | 地址族和特殊地址语义由 QHostAddress 决定。 |
| `state()`、`error()`、`errorString()` | 查询 UDP socket 状态、错误码和文本。 | 错误码用于分类，文本用于诊断。 |
| `localAddress()`、`localPort()` | 查询绑定后的本地端点。 | 未绑定或不可用时地址可能为 Null、端口为 0。 |
| `socketDescriptor()`、`setSocketDescriptor()` | 读取或接管原生描述符。 | 同一描述符不能被多个 Qt socket 接管；代理时描述符不保证可直接用于原生 API。 |
