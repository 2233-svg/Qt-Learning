# QDtlsClientVerifier：DTLS 服务端 cookie 验证

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDtlsClientVerifier>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 继承：`QObject`

## 它解决什么问题

`QDtlsClientVerifier` 在 DTLS 服务端真正创建会话、分配大量状态或进行昂贵的密码学握手之前，验证发来 ClientHello 的客户端确实能接收该源地址和端口上的 UDP 响应。

它实现 DTLS cookie 机制：首次 ClientHello 没有匹配 cookie 时，服务端回发携带 cookie 的 `HelloVerifyRequest`；真正可达的客户端会携带该 cookie 再次发送 ClientHello。只有第二次报文验证成功，服务端才应为这个对端创建 `QDtls` 会话并开始握手。

这个过程能显著降低伪造源地址造成的状态耗尽和反射放大风险，但它不认证用户身份、不替代客户端证书或 PSK，也不替代应用自己的会话限流策略。

## 实际使用场景

- 对公网暴露的 DTLS 服务端，在收到陌生 UDP 来源的第一个 datagram 时先验证。
- 一个 `QUdpSocket` 同时服务多个客户端，服务器只为通过 cookie 验证的 `(address, port)` 建立 `QDtls` 对象。
- 设备网关轮换 DTLS cookie secret，限制旧 cookie 的有效时间窗口。

如果服务器明确选择不使用 cookie，需在 `QDtls` 的 `QSslConfiguration` 中关闭 DTLS cookie 验证；不能一边跳过 `QDtlsClientVerifier`，一边保留默认的 cookie 验证期望。

## 工作流

`QDtlsClientVerifier` 不会从 socket 读数据，也不拥有 `QUdpSocket`。应用应自行读出 datagram 及其来源地址、端口，再调用 `verifyClient()`：

```cpp
void Server::processDatagram(const QByteArray &datagram,
                             const QHostAddress &address,
                             quint16 port)
{
    if (!verifier.verifyClient(&socket, datagram, address, port)) {
        if (verifier.dtlsError() != QDtlsError::NoError)
            qWarning() << verifier.dtlsErrorString();

        // NoError 时通常是已发出 HelloVerifyRequest；
        // 等客户端带 cookie 的下一次 ClientHello。
        return;
    }

    auto &dtls = createSession(address, port);
    dtls.setPeer(address, port);
    dtls.doHandshake(&socket, verifier.verifiedHello());
}
```

在真实服务器中，先检查来源是否已经有会话：已有 `QDtls` 会话的 datagram 应直接送给那个会话的 `doHandshake()` 或 `decryptDatagram()`，不能对每个包反复调用 verifier。

`verifiedHello()` 返回最近一次成功验证的 ClientHello。它只应在 `verifyClient()` 返回 `true` 后立即用于创建/启动相应会话；不要把它当作按来源保存的缓存，多个客户端交错到达时应以当前调用的成功结果和当前 `(address, port)` 关联。

## `false` 的两种含义

`verifyClient()` 只有在报文中含有有效 cookie 时才返回 `true`。返回 `false` 有两种完全不同的情况：

| 情况 | `dtlsError()` | 应对 |
| --- | --- | --- |
| 正常首轮验证 | `NoError` | verifier 已向该地址/端口发出 `HelloVerifyRequest`；不创建会话，等待重试。 |
| 输入或底层操作失败 | 非 `NoError` | 记录/处理具体错误；不要把报文当作可进入握手的 ClientHello。 |

传入的 `socket` 必须有效、`dgram` 必须非空；来源地址不能是 null、广播或组播地址，端口必须是接收到报文的远端端口。否则调用本身无效。

## Cookie 密钥与参数

cookie 由客户端地址、端口和服务器 secret 等信息派生。默认 secret 来自底层密码学安全随机源；默认 secret 会被 `QDtlsClientVerifier` 与 `QDtls` 的对象共享。长期使用同一 secret 会扩大泄露和重放窗口，因此服务端应遵循自己的轮换策略，定期设置新参数。

通过 `setCookieGeneratorParameters()` 设置 hash 算法与 secret。空 secret 会使函数返回 `false` 且保留旧参数；secret 必须来自密码学安全随机源，不应由时间戳、固定字符串或普通伪随机数构造。

如果 verifier 使用非默认参数，随后为同一客户端创建的服务端 `QDtls` 必须在握手前设置同样的 `GeneratorParameters`。否则 verifier 认可的 ClientHello 与 `QDtls` 自己验证的 cookie 不一致，握手无法正确衔接。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 构造 | `QDtlsClientVerifier(QObject *parent = nullptr)` | 创建服务端 cookie 验证器；可由父对象管理生命周期。 |
| 生命周期 | `~QDtlsClientVerifier()` | 不拥有传入的 `QUdpSocket`。 |
| 核心操作 | `verifyClient(QUdpSocket *, const QByteArray &, const QHostAddress &, quint16)` | 验证 ClientHello 中的 cookie。真表示已验证；假且 `NoError` 通常表示已发送挑战，等待客户端重试。 |
| 结果 | `verifiedHello()` | 返回最近一次验证成功的 ClientHello；仅在刚刚得到 `true` 后用于对应 peer 的 `QDtls::doHandshake()`。 |
| cookie 配置 | `setCookieGeneratorParameters(const GeneratorParameters &)` | 设置 hash 与 secret；空 secret 失败。参数应在新验证流程开始前设置，并与服务端 `QDtls` 保持一致。 |
| cookie 配置 | `cookieGeneratorParameters()` | 返回当前的 cookie hash 算法和 secret。 |
| 诊断 | `dtlsError()` | 返回最近错误的 `QDtlsError`；`NoError` 可表示“挑战已发送，尚未验证”，不是只能表示成功完成。 |
| 诊断 | `dtlsErrorString()` | 返回最近错误的文本描述；适合日志，不作为逻辑分支依据。 |
| 协作类型 | `GeneratorParameters` | cookie 生成参数结构，包含 `QCryptographicHash::Algorithm` 与 secret 字节串。 |
| 协作类型 | `QDtlsError` | 与 `QDtls` 共享的错误枚举；重点区分正常挑战的 `NoError`、调用问题和 `UnderlyingSocketError`。 |

## 一句话总结

`QDtlsClientVerifier` 是 DTLS 服务端的前置防线：先确认 UDP 来源能收到挑战，再创建 `QDtls` 并投入证书、密钥和会话资源。
