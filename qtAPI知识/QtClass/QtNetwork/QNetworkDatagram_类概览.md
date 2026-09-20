# QNetworkDatagram：UDP 数据报与收发元数据

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkDatagram>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 类型：可复制、可移动的值类型

## 它解决什么问题

`QNetworkDatagram` 把 UDP 的 payload 与完整收发元数据放在同一个对象中：发送者和目标地址/端口、hop limit（IPv4 中常称 TTL）、以及接收或发送所关联的接口 index。

相比 `QUdpSocket::readDatagram()` 的若干输出参数，它能保留“这个包发给了哪个本机地址、从哪个接口进入”的信息。对多播、广播、多个本机地址、IPv6 链路本地地址和多网卡响应尤其重要。

## 实际使用场景

- 使用 `QUdpSocket::receiveDatagram()` 接收多播或广播，区分数据报实际目标地址和入接口。
- 收到 UDP 请求后用 `makeReply()` 向原始发送者回包，并尽可能保留正确接口/本机 IPv6 源地址。
- 向 IPv6 link-local 或多播地址发送时，显式指定接口 index。
- 设置有限 TTL/hop limit 的局域网发现包。

它不是可靠传输层：UDP 的丢包、重复、乱序和长度限制仍由应用协议承担。

## 基本工作流

```cpp
connect(&udpSocket, &QUdpSocket::readyRead, this, [&] {
    while (udpSocket.hasPendingDatagrams()) {
        QNetworkDatagram request = udpSocket.receiveDatagram();
        const QByteArray replyData = process(request.data());

        udpSocket.writeDatagram(std::move(request).makeReply(replyData));
    }
});
```

`makeReply()` 会把收到包的 sender 地址和端口变成回复包的 destination，并复制适当的接口信息。对 lvalue 调用会创建新对象；对 rvalue（如 `std::move(request)`）调用可更充分利用移动语义。

即使 `data()` 为空，datagram 也可能有效；有效性的条件是至少已设置 sender 或 destination 地址，而不是 payload 是否非空。

## 接收与发送时字段含义不同

| 字段 | 接收 datagram | 待发送 datagram |
| --- | --- | --- |
| `senderAddress()` / `senderPort()` | 远端发送者 | 希望使用的本机源地址/端口 |
| `destinationAddress()` / `destinationPort()` | 本机实际收到包的目标 | 远端目标地址/端口 |
| `interfaceIndex()` | 包到达的本机接口 | 希望从其发出的本机接口 |
| `hopLimit()` | 接收时剩余的 TTL/hop limit | 写入 IP 头的 hop limit，`-1` 交给 OS 决定 |

发送时显式设置 sender 地址，必须是本机已配置的地址；显式端口必须与 socket 绑定端口一致。两者留空/0 时让操作系统依据路由选择。向普通全局地址发送通常不必设置 interface index；向 IPv6 link-local 或多播目标时则很关键。

## 元数据支持的边界

所有平台都支持远端主机地址和端口，但 destination 地址、接口 index 和 hop limit 并非每个系统、每个协议族都能提供。`QUdpSocket` 无法设置的发送元数据会被静默丢弃；对 IPv4，额外元数据的支持通常比 IPv6 更不完整。

因此业务如果依赖“从特定接口收到”或“精确 TTL”，应在目标平台实测，不要仅依赖 setter 后 getter 的值。对需要强制源接口的协议，也应在 `writeDatagram()` 返回值和网络抓包中验证。

若 destination address 自己带有 IPv6 scope ID，而 `setInterfaceIndex()` 又设置了另一个非零 index，最终从哪个接口发送由操作系统决定，行为未定义。两者必须保持一致，或只设置其中一个。

## Hop limit 与 reply 的细节

`setHopLimit()` 的有效显式范围为 1 到 255；传 `-1` 表示让 OS 选择。不要把接收包的剩余 TTL 原样回写给回复：`makeReply()` 会将回复 hop limit 重置为 `-1`，这通常才是正确行为。

`makeReply()` 会在适当时复制本机地址作为 reply 的 sender，但对 IPv4 destination 不会照抄，因为 Qt 无法可靠区分普通 IPv4 地址与广播地址；这避免了错误地以广播地址为源发送。多地址 IPv4 主机若需要精确源地址，应自行在回复上明确设置。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 构造 | `QNetworkDatagram()` | 创建无 payload、无 destination 的对象；若 socket 已 `connectToHost()`，发送时可使用关联目标。 |
| 构造 | `QNetworkDatagram(const QByteArray &, const QHostAddress &destination = {}, quint16 port = 0)` | 以 payload 和可选目标构造待发送 datagram。 |
| 构造与赋值 | 复制/移动构造、复制/移动 `operator=`、`swap()` | 复制或转移 payload 与全部元数据。 |
| 状态 | `isValid()` / `isNull()` | 至少有 sender 或 destination 地址时有效；空 payload 仍可有效。 |
| 清空 | `clear()` | 重置 payload 与全部元数据为默认值。 |
| payload | `data()` / `setData(const QByteArray &)` | 获取/设置 payload；空 `QByteArray` 是有效 UDP 数据。 |
| 发送者 | `senderAddress()` / `senderPort()` | 收包时为远端来源；发包时为请求使用的本机源，未设置端口为 `-1`。 |
| 发送者 | `setSender(const QHostAddress &, quint16 port = 0)` | 设置待发送包的本机源；地址应属于本机，端口应与 socket 一致，0 让 OS 选择。 |
| 目标 | `destinationAddress()` / `destinationPort()` | 收包时为本机实际目标；发包时为远端目标，未设置端口为 `-1`。 |
| 目标 | `setDestination(const QHostAddress &, quint16)` | 设置待发送目标，可为单播、广播或多播地址。 |
| 接口 | `interfaceIndex()` / `setInterfaceIndex(uint)` | 获取/指定入/出接口；0 为未知或交给 OS 选择。与 `QNetworkInterface::index()` 对应。 |
| 跳数 | `hopLimit()` / `setHopLimit(int)` | 获取剩余或设置发出 hop limit；`-1` 让 OS 决定，显式范围 1-255。 |
| 回复 | `makeReply(const QByteArray &)` | 按入包元数据构造回复，自动对调 peer 目标并重置 hop limit；rvalue 调用更高效。 |
| 协作 | `QUdpSocket::receiveDatagram()` | 接收完整 payload 与可用元数据。 |
| 协作 | `QUdpSocket::writeDatagram(const QNetworkDatagram &)` | 发送该对象；平台不支持的元数据可能被静默忽略。 |

## 一句话总结

`QNetworkDatagram` 让 UDP 消息携带来源、目标、接口和 hop limit 上下文：它非常适合多播和多网卡，但额外元数据的可用性必须按平台验证。
