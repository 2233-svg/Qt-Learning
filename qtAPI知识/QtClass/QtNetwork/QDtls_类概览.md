# QDtls：在 UDP 上建立 DTLS 安全会话

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDtls>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 继承：`QObject`

## 它解决什么问题

`QDtls` 在无连接、可能丢包和乱序的 UDP 数据报之上执行 DTLS 握手、加密、认证与关闭通知。它让应用保留 UDP 的消息边界和低延迟，同时为每个对端建立独立的 TLS 风格安全会话。

它不是 `QUdpSocket` 的替代品，也不是“把 UDP socket 升级为加密 socket”的包装器。`QUdpSocket` 仍负责收发原始 datagram；应用从 socket 读出每个 datagram 后，将它交给正确的 `QDtls` 实例。`QDtls` 既不读取也不拥有这个 socket。

## 实际使用场景

- 实时遥测、工业控制或设备管理协议需要 UDP 消息边界，同时要求身份认证和保密性。
- 游戏或媒体控制平面使用 UDP，且服务端要为不同客户端维护独立安全会话。
- 使用自定义 UDP 协议但不希望自行实现重放防护、握手密钥协商和证书校验。

若协议需要可靠字节流、自动拥塞控制和顺序交付，通常应考虑 TCP/TLS 与 `QSslSocket`。DTLS 不会为应用数据提供可靠重传；丢失的普通业务 datagram 仍由应用协议处理。

## 使用模型：一个 UDP socket，多条 DTLS 会话

`QUdpSocket` 可以收到不同来源的包，因此服务器应以远端地址和端口为键，维护 `QDtls` 会话表：

1. 在 `QUdpSocket::readyRead` 中读出完整 datagram、来源地址和端口。
2. 对尚未验证的新客户端，先交给 `QDtlsClientVerifier` 做 cookie 验证。
3. 为已经通过验证的客户端找到或创建对应的 `QDtls`，并确保先调用 `setPeer(address, port)`。
4. 握手期把每个该客户端的包交给 `doHandshake()`；只有 `handshakeState()` 为 `HandshakeComplete` 后，才调用 `decryptDatagram()` 或 `writeDatagramEncrypted()`。

客户端发起与续接握手的最小骨架：

```cpp
QDtls dtls(QSslSocket::SslClientMode);
dtls.setPeer(serverAddress, serverPort, u"gateway.example.com"_qs);

connect(&dtls, &QDtls::handshakeTimeout, this, [&] {
    if (!dtls.handleTimeout(&udpSocket))
        qWarning() << dtls.dtlsErrorString();
});

dtls.doHandshake(&udpSocket); // 发送初始 ClientHello

// 在 udpSocket 的 readyRead 处理函数中，确认来源属于该 peer 后：
if (!dtls.doHandshake(&udpSocket, incomingDatagram)) {
    qWarning() << dtls.dtlsErrorString();
} else if (dtls.handshakeState() == QDtls::HandshakeComplete) {
    // 此时才能发送或解密业务 datagram。
}
```

服务端第一次调用 `doHandshake()` 时，第二个参数必须是刚收到的、非空的 ClientHello。之后继续把同一客户端的握手 datagram 传入该函数，直到完成或出错。

## 握手状态、重传与关闭

`doHandshake()` 返回 `true` 只表示本次处理没有发现错误，不等于握手已完成；要继续检查 `handshakeState()` 或 `isConnectionEncrypted()`。

| 状态 | 含义 |
| --- | --- |
| `HandshakeNotStarted` | 尚未开始，或 `shutdown()` 后回到此状态。 |
| `HandshakeInProgress` | 正在等待或处理后续握手 datagram。 |
| `PeerVerificationFailed` | 证书/对端身份校验失败，等待应用决定忽略或中止。 |
| `HandshakeComplete` | 握手成功，已建立加密会话。 |

DTLS 握手包可能在 UDP 中丢失。收到 `handshakeTimeout()` 后，应用必须调用 `handleTimeout(socket)`，让 `QDtls` 重传需要重发的握手消息。忽略这个信号会使握手停在中途。

会话结束时调用 `shutdown()`，它会发送加密 shutdown alert 并复位状态。客户端若希望以后复用相同本地端口重新连接同一服务端，尤其应先关闭旧会话；否则服务端可能丢弃新的 ClientHello。

## 证书校验、PSK 与 cookie

`setPeer()` 的 `verificationName` 是证书主机名校验使用的名称，不是对端 IP 的显示标签。连接 IP 地址时若证书签发给域名，仍应传入该域名；这必须在握手开始前设置。

如果 `doHandshake()` 因 `PeerVerificationError` 失败，读取 `peerVerificationErrors()` 判断具体原因。只有在业务上能够严格证明某些错误可接受时，才调用 `ignoreVerificationErrors()`，然后调用 `resumeHandshake()`；否则使用 `abortHandshake()`。盲目忽略证书错误会取消身份认证的意义。

协商到预共享密钥（PSK）套件时会发射 `pskRequired(QSslPreSharedKeyAuthenticator *)`。槽必须在该回调期间向传入的 authenticator 设置有效 identity 和 key；未提供凭据，握手会失败。

DTLS cookie 是服务端抵御伪造源地址、资源耗尽和反射放大攻击的无状态机制。生产服务端通常先用 `QDtlsClientVerifier` 验证 ClientHello，再把 `verifiedHello()` 交给对应 `QDtls` 开始握手。若服务器明确不使用 `QDtlsClientVerifier`，必须在 `QSslConfiguration` 中关闭 DTLS cookie 验证后再调用 `setDtlsConfiguration()`；否则不会按预期完成握手。

如果 verifier 使用了自定义 cookie secret/hash，服务端的 `QDtls` 必须在握手前设置完全相同的 `GeneratorParameters`。cookie secret 应来自密码学安全随机源，并按服务器的安全策略轮换。

## MTU 与数据报边界

DTLS 把路径 MTU 探测留给应用。`setMtuHint()` 可提供已发现或估计的 MTU，它只影响握手消息的分片与重组。

业务数据不会由 `QDtls` 分片：传给 `writeDatagramEncrypted()` 的每条消息连同 DTLS 开销都必须适合单个 UDP datagram。不要把 TCP 的“任意长度写入”心智模型套进来。启用 HelloVerifyRequest 的服务端还会丢弃分片的初始 ClientHello，因此客户端的首个 ClientHello 也要保持足够小。

## 错误处理边界

`dtlsError()` 返回最近一次 `QDtlsError`，`dtlsErrorString()` 供日志使用：

- `InvalidInputParameters`、`InvalidOperation`：调用时机、peer、socket 或状态不正确。
- `UnderlyingSocketError`：底层 `QUdpSocket::writeDatagram()` 失败，应同时检查 socket 的 `error()` 与 `errorString()`。
- `PeerVerificationError`：需要在“忽略指定错误后恢复”与“中止”之间明确选择。
- `TlsInitializationError`、`TlsFatalError`：TLS 后端初始化或致命握手失败。
- `TlsNonFatalError`：单次加/解密失败，但会话仍可继续；不可把它直接当作会话已断开。
- `RemoteClosedConnectionError`：收到对端 shutdown alert。

`decryptDatagram()` 可能为了协议处理而向 socket 写出数据；因此即使只是“解密”，也需要传入有效、可写的 `QUdpSocket`。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 相关枚举 | `QDtlsError` | `NoError`、参数/操作错误、底层 socket 错误、证书错误、TLS 致命或非致命错误等；失败后结合 `dtlsErrorString()` 诊断。 |
| 枚举 | `HandshakeState` | 握手状态机；`doHandshake()` 返回真仍应检查是否为 `HandshakeComplete`。 |
| 类型别名 | `GeneratorParameters` | 即 `QDtlsClientVerifier::GeneratorParameters`，包含 cookie hash 算法和 secret。 |
| 构造 | `QDtls(QSslSocket::SslMode mode, QObject *parent = nullptr)` | 以 `SslClientMode` 或 `SslServerMode` 创建；模式一经确定不能临时切换。 |
| 生命周期 | `~QDtls()` | 不拥有 `QUdpSocket`；建议客户端销毁前先 `shutdown()`。 |
| 对端配置 | `setPeer(const QHostAddress &, quint16, const QString &verificationName = {})` | 设置地址、端口与可选证书校验名；必须在握手前完成。 |
| 对端配置 | `setPeerVerificationName(const QString &)` | 只改证书校验名称；必须在握手前调用。 |
| 对端状态 | `peerAddress()` / `peerPort()` / `peerVerificationName()` | 读取当前绑定的远端地址、端口和校验主机名。 |
| 模式 | `sslMode()` | 返回客户端或服务端 DTLS 模式。 |
| MTU | `setMtuHint(quint16)` / `mtuHint()` | 设置/读取路径 MTU 提示；仅影响握手分片，业务 datagram 仍必须自行控制大小。 |
| cookie | `setCookieGeneratorParameters(const GeneratorParameters &)` | 服务端专用，握手前设置 hash 与 secret；与 `QDtlsClientVerifier` 配套使用时参数必须一致。 |
| cookie | `cookieGeneratorParameters()` | 读取当前 cookie 参数。 |
| TLS 配置 | `setDtlsConfiguration(const QSslConfiguration &)` | 握手前设置证书、私钥、协议、套件及 cookie 策略；成功返回 `true`。 |
| TLS 配置 | `dtlsConfiguration()` | 读取当前 DTLS 配置。 |
| 握手 | `doHandshake(QUdpSocket *, const QByteArray &dgram = {})` | 启动或继续握手。服务端首次调用必须传 ClientHello；返回假后读 `dtlsError()`。 |
| 握手 | `handshakeState()` | 查询当前状态；加密成立的权威状态是 `HandshakeComplete`。 |
| 握手 | `handleTimeout(QUdpSocket *)` | 在 `handshakeTimeout()` 后调用以重传；仅真正发生超时时返回真。 |
| 握手 | `resumeHandshake(QUdpSocket *)` | 忽略指定证书错误后继续握手；不能代替正常的 `doHandshake()` 流程。 |
| 握手 | `abortHandshake(QUdpSocket *)` | 中止正在进行的握手；没有进行中的握手时返回假并设置错误。 |
| 关闭 | `shutdown(QUdpSocket *)` | 发送加密关闭告警并回到 `HandshakeNotStarted`。 |
| 加密状态 | `isConnectionEncrypted()` | 仅在握手成功后为真。 |
| 协商结果 | `sessionCipher()` | 返回握手选定的套件；未加密时为空 cipher。 |
| 协商结果 | `sessionProtocol()` | 返回协商出的 DTLS 协议；未加密时为 `UnknownProtocol`。 |
| 发送 | `writeDatagramEncrypted(QUdpSocket *, const QByteArray &)` | 加密并发送一条 datagram；仅限握手完成后，成功返回写入字节数，失败为 `-1`。 |
| 接收 | `decryptDatagram(QUdpSocket *, const QByteArray &)` | 解密一条来自匹配 peer 的 datagram；仅限握手完成后，可能因协议处理写 socket。 |
| 证书错误 | `peerVerificationErrors()` | 返回握手中发生的对端校验错误，用于精确评估是否可接受。 |
| 证书错误 | `ignoreVerificationErrors(const QList<QSslError> &)` | 设置允许忽略的错误列表，后续调用会替换旧列表；只忽略经业务确认的具体错误。 |
| 诊断 | `dtlsError()` / `dtlsErrorString()` | 获取最近错误枚举与文本；文本用于记录，逻辑分支用枚举。 |
| 信号 | `handshakeTimeout()` | 握手包可能丢失；收到后调用 `handleTimeout()`。 |
| 信号 | `pskRequired(QSslPreSharedKeyAuthenticator *)` | PSK 套件协商时发射；在槽中设置 identity 和 key，否则握手失败。 |

## 一句话总结

`QDtls` 为单个 UDP 对端管理 DTLS 会话：应用负责读包、按 peer 分派和业务层可靠性，`QDtls` 负责握手、重传、认证与单个 datagram 的加解密。
