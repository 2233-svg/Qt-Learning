# QSslConfiguration

> Qt 6.11.1 | Qt6::Network | `#include <QSslConfiguration>`

## 类解决的问题

`QSslConfiguration` 集中保存一次 TLS/DTLS 会话需要的安全策略和材料。它把协议版本、对端验证、证书链、私钥、密码套件、CA、椭圆曲线、PSK 提示、ALPN/NPN 和 backend 专用选项组合成一个可复制的值对象，解决：

- 为多个 `QSslSocket` 复用同一套 TLS 策略；
- 在连接开始前明确证书验证、密码套件和信任库；
- 为服务端配置本地证书链和私钥；
- 读取握手完成后的协商结果；
- 在应用级别设置默认 TLS/DTLS 配置；
- 将 backend 特有选项以统一的 Qt API 传递给底层实现。

它不是 socket，也不会主动开始握手。把配置传给 socket 后，socket 才会在实际连接中使用这些设置。配置是隐式共享值类型；复制成本低，但修改采用写时复制。

## 实际使用场景

### 1. 客户端固定验证策略和 CA

```cpp
QSslConfiguration configuration =
    QSslConfiguration::defaultConfiguration();
configuration.setPeerVerifyMode(QSslSocket::VerifyPeer);

const QList<QSslCertificate> caCertificates =
    QSslCertificate::fromFile(QStringLiteral("company-ca.pem"));
configuration.setCaCertificates(caCertificates);

socket->setSslConfiguration(configuration);
socket->setPeerVerifyName(QStringLiteral("api.example.com"));
socket->connectToHostEncrypted(QStringLiteral("10.0.0.8"), 443);
```

`setPeerVerifyName()` 属于 `QSslSocket`，不是 `QSslConfiguration`。如果 TCP 连接地址是 IP、代理名或别名，而证书应按另一个 DNS 名称校验，应在 socket 上单独设置校验名。

### 2. 配置服务端证书链和私钥

```cpp
QSslConfiguration configuration =
    QSslConfiguration::defaultConfiguration();
configuration.setLocalCertificateChain(serverChain);
configuration.setPrivateKey(serverKey);
configuration.setPeerVerifyMode(QSslSocket::VerifyNone);

server->setSslConfiguration(configuration);
server->listen(QHostAddress::Any, 8443);
```

服务端私钥必须与本地叶子证书匹配，证书链顺序通常是叶子证书在前、中间 CA 在后。`QSslServer` 要求在 `listen()` 前设置配置。

### 3. 限制密码套件和协议能力

```cpp
QSslConfiguration configuration =
    QSslConfiguration::defaultConfiguration();

const QList<QSslCipher> supported =
    QSslConfiguration::supportedCiphers();
configuration.setCiphers(filterCiphers(supported));
configuration.setProtocol(QSsl::TlsV1_2OrLater);
configuration.setEllipticCurves(
    QSslConfiguration::supportedEllipticCurves());
```

自定义列表必须来自当前 backend 的支持集合。不要把某台机器上的密码套件名称、曲线名称或协议枚举硬编码成跨 backend 的保证。

### 4. 设置 ALPN 并读取协商结果

```cpp
QSslConfiguration configuration =
    QSslConfiguration::defaultConfiguration();
configuration.setAllowedNextProtocols({
    QByteArrayLiteral("h2"),
    QByteArrayLiteral("http/1.1")
});

socket->setSslConfiguration(configuration);
socket->connectToHostEncrypted(host, 443);

connect(socket, &QSslSocket::encrypted, this, [socket] {
    qInfo() << socket->sslConfiguration().nextNegotiatedProtocol();
});
```

允许列表应在握手开始前设置。握手完成后，通过 socket 的配置读取 `nextNegotiatedProtocol()` 和状态；`None` 可能表示没有启用、尚未协商或 backend 不支持，必须结合状态判断。

## 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(app PRIVATE Qt6::Network)
```

```cpp
#include <QSslConfiguration>
#include <QSslSocket>

QSslConfiguration configuration =
    QSslConfiguration::defaultConfiguration();
configuration.setPeerVerifyMode(QSslSocket::VerifyPeer);
socket->setSslConfiguration(configuration);
```

## 关键语义与边界

### `isNull()` 表示“是否改过配置”，不是“配置无效”

默认构造的 `QSslConfiguration` 是 null。一个尚未调用 setter 的对象也保持 null；调用任意配置 setter 后通常变为非 null。非 null 不表示所有设置都被 backend 接受，也不表示证书、私钥或密码套件一定有效。

`defaultConfiguration()` 返回可使用的默认配置，即使它不是 null。判断是否真正可用，应检查具体材料、backend 能力和 socket 的握手结果。

### 大多数设置必须在握手前完成

协议、验证模式、证书链、私钥、CA、密码套件、曲线、PSK hint、OCSP stapling、ALPN/NPN 和多数 SSL option 都应在连接或握手开始前设置。握手开始后修改配置对象，不会回溯改变已经建立的 SSL 会话；修改 socket 的配置也不能可靠地改变当前会话。

读取 `sessionCipher()`、`sessionProtocol()`、`peerCertificate()` 等会话状态时，应等到握手成功或相应状态已经产生。

### 默认配置只影响之后创建的会话

`setDefaultConfiguration()` 和 `setDefaultDtlsConfiguration()` 只改变之后使用默认配置的新连接。已经创建、已经复制或已经交给 socket 的配置不会被动态更新。显式 `setSslConfiguration()` 的 socket 也不会因为全局默认值改变而自动重配。

全局默认配置是进程级策略，库代码修改它会影响同一进程中的其他连接。更可控的做法是为具体 socket 或 server 构造并显式设置配置。

### 默认验证模式是 `AutoVerifyPeer`

默认模式是 `QSslSocket::AutoVerifyPeer`：

- 客户端行为等效于 `VerifyPeer`；
- 服务端行为等效于 `QueryPeer`。

这意味着同一份默认配置用于客户端和服务端时，角色会影响验证行为。若协议明确要求服务端必须验证客户端证书，应显式使用 `VerifyPeer`，并配置合适的 CA。

### 验证深度的 `0` 表示不限制

`peerVerifyDepth()` 为 0 表示不限制验证深度，检查完整的证书链。正数用于限制链深度；它不是“必须有几张证书”，也不是 TCP 跳数。设置过小可能拒绝本来合法的中间 CA 链。

### 证书链和私钥是值对象，但敏感材料仍需保护

`setLocalCertificateChain()`、`setCaCertificates()` 和 `setPrivateKey()` 复制值对象状态，配置不拥有外部 `QIODevice` 或证书文件。隐式共享减少复制成本，但私钥、session ticket 和 backend 选项中的敏感内容仍可能长期留在内存中。

本地证书链通常叶子在前；对端证书链和会话证书在握手后才有意义。`localCertificate()` 返回链首，而不是任意 CA。

### CA 设置是替换还是追加

- `setCaCertificates()` 替换当前 CA 列表；
- `addCaCertificate()` 追加一张；
- `addCaCertificates(const QList<...>&)` 追加一组；
- `addCaCertificates(path, format, syntax)` 从路径解析并追加，使用 `QSslCertificate::PatternSyntax`。

默认配置通常使用系统 CA。`setCaCertificates()` 之后，应用要明确自己是在替换系统信任库还是在构造专用信任库；不要因为某个平台没有系统 CA，就假设所有平台都一致。若要使用系统 CA，可读取 `systemCaCertificates()` 后显式合并。

### 密码套件列表必须来自当前 backend

`setCiphers(QList<QSslCipher>)` 要求列表是 `supportedCiphers()` 的子集，并按偏好顺序排列。空列表、包含不支持套件或过度收紧的列表可能导致没有共同密码套件。

字符串重载使用冒号分隔的密码套件名称。名称、支持情况和顺序由 backend 决定；Windows Schannel 等 backend 可能忽略应用提供的顺序。读取 `ciphers()` 才能确认配置对象当前保存的列表，最终协商结果看 `sessionCipher()`。

### 椭圆曲线也只能选择受支持子集

`setEllipticCurves()` 应传入 `supportedEllipticCurves()` 的子集。曲线列表为空或与对端没有交集时，握手可能失败。支持情况取决于 backend、平台和构建方式。

### `sessionCipher()` 与 `sessionProtocol()` 是结果，不是预设

`ciphers()` 是允许列表；`sessionCipher()` 是实际握手选中的密码套件。`protocol()` 是配置的协议策略；`sessionProtocol()` 是实际协商版本。握手前后者可能为空或为 `UnknownProtocol`，不能用配置策略代替真实协商结果。

### backend configuration 只表达显式应用设置

`backendConfiguration()` 返回应用通过 `setBackendConfigurationOption()` 或 `setBackendConfiguration()` 写入的键值，不保证包含 backend 内部默认值、最终生效值或所有未识别选项。键名和值的含义由具体 backend 定义，通常使用 `QByteArray` 键和 `QVariant` 值。

backend 专用设置可能覆盖通用 Qt 设置。跨平台程序应先判断 `activeBackend()`、`isFeatureSupported()` 或文档规定的 backend，再设置选项，并对不支持情况保留可用回退。

### Session ticket 是敏感材料

`sessionTicket()` 和 `sessionTicketLifeTimeHint()` 用于 TLS 会话恢复相关能力。ticket 可能包含敏感的恢复材料，不应写日志、传给不可信组件或持久化到无保护存储。生命期提示不是保证的有效期，最终仍由 backend 和服务端控制。

### `ephemeralServerKey()` 只在特定客户端会话有意义

它返回客户端连接中服务端使用的临时密钥，通常只对使用前向保密算法的会话有意义。服务端 socket 或不支持该能力的 backend 可能返回空 key。它不是服务端长期私钥，也不能用来替代 `peerCertificate().publicKey()`。

### PSK identity hint 的角色和时机

`setPreSharedKeyIdentityHint()` 只对服务端模式有意义，且主要影响下一次握手。它是给客户端的提示，不是客户端 identity 或 PSK，也不负责查找凭据。实际 identity 和 PSK 通过 `QSslPreSharedKeyAuthenticator` 回调设置。

### DTLS、握手中断和缺少证书是能力相关 API

DTLS cookie verification 只适用于 DTLS。`handshakeMustInterruptOnError()` 主要由 OpenSSL backend 支持，用于把可恢复的握手错误交给应用后再继续；启用后必须连接对应信号并同步调用 `continueInterruptedHandshake()`。

`missingCertificateIsFatal()` 主要由 OpenSSL backend 支持，控制缺少本地证书等情况能否被 backend 继续处理。应用不能把它当作跨 backend 一致的 TLS 规则。

### OCSP stapling 与 ALPN/NPN 必须在握手前启用

`setOcspStaplingEnabled(true)` 只是请求/启用 stapling 路径，不能保证服务端返回有效 OCSP 响应。`ocspStaplingEnabled()` 反映配置，不等于已经收到响应。

`setAllowedNextProtocols()` 的列表顺序表达应用偏好，但最终结果由双方和 backend 决定。`nextNegotiatedProtocol()` 只有协商完成后才有意义；`NextProtocolNegotiationUnsupported` 表示没有共同协议或能力不支持，应用应准备回退。

## 常见误区

- 把 null 配置当作“连接不可用”：`isNull()` 只表示没有显式配置状态。
- 在握手过程中修改配置，期待当前会话立刻改变：多数设置只对下一次握手生效。
- 修改默认配置后期待已有 socket 自动更新：默认配置只影响后续新会话。
- 客户端和服务端共用默认 `AutoVerifyPeer` 却忽略角色差异：服务端默认更接近 `QueryPeer`。
- 把 `peerVerifyDepth == 0` 当成“关闭验证”：它只表示不限制链深度。
- 用 `ciphers()` 推断实际协商套件：实际结果要看 `sessionCipher()`。
- 把 `sessionTicket()` 当作普通缓存：它是敏感 TLS 材料。
- 把 `ephemeralServerKey()` 当作服务器长期私钥：它只是特定会话的临时密钥。
- 在不判断 backend 的情况下写 backend-specific 配置：键名和值没有跨 backend 的通用语义。
- 启用 OCSP/ALPN 就认为一定协商成功：这些 API 只配置能力，结果仍需在握手后检查。
- 用一份全局默认配置偷偷影响整个进程：共享库更适合对具体 socket/server 显式设置。

## 逐项 API 说明

### 构造、值语义和比较

#### `QSslConfiguration()`

构造 null 配置。尚未调用 setter 时 `isNull()` 为 true；它不主动加载证书、CA 或 backend 状态。

#### `QSslConfiguration(const QSslConfiguration &other)`

复制配置值。配置采用隐式共享，复制不会复制 socket 或 SSL 会话。

#### `~QSslConfiguration()`

销毁配置值对象，不会关闭使用过它的 socket。

#### `QSslConfiguration &operator=(const QSslConfiguration &other)`

复制赋值，替换当前配置。

#### `QSslConfiguration &operator=(QSslConfiguration &&other) noexcept`

移动赋值，转移配置状态。

#### `void swap(QSslConfiguration &other) noexcept`

交换两个配置对象。

#### `bool operator==(const QSslConfiguration &other) const`

比较配置值。它适合测试和缓存键语义，不表示两个配置在所有 backend 上会产生相同的最终握手结果。

#### `bool operator!=(const QSslConfiguration &other) const`

返回不相等比较结果。

#### `bool isNull() const`

判断配置是否仍是未显式设置的 null 值。非 null 也不代表每个设置都被 backend 接受。

### 协议和对端验证

#### `QSsl::SslProtocol protocol() const`

返回协议策略，如 `SecureProtocols` 或特定 TLS 版本策略。它是允许范围，不是实际协商结果。

#### `void setProtocol(QSsl::SslProtocol protocol)`

设置协议策略。应在握手前调用；最终版本通过 `sessionProtocol()` 读取。

#### `QSslSocket::PeerVerifyMode peerVerifyMode() const`

返回对端证书验证模式。默认是 `AutoVerifyPeer`，实际客户端/服务端行为不同。

#### `void setPeerVerifyMode(QSslSocket::PeerVerifyMode mode)`

设置对端验证策略。`VerifyNone` 会关闭证书验证能力，只有在明确的受控场景才应使用。

#### `int peerVerifyDepth() const`

返回证书链验证深度限制。0 表示不限制。

#### `void setPeerVerifyDepth(int depth)`

设置验证深度限制。应使用非负值，并确保不会因中间 CA 数量导致合法链被拒绝。

### 本地和对端证书

#### `QList<QSslCertificate> localCertificateChain() const`

返回本地证书链。通常第一张是叶子证书。

#### `void setLocalCertificateChain(const QList<QSslCertificate> &localChain)`

设置本地证书链。用于服务端或需要客户端证书的场景；链顺序和证书有效性由应用负责。

#### `QSslCertificate localCertificate() const`

返回本地证书链首张证书。没有本地证书时返回 null certificate。

#### `void setLocalCertificate(const QSslCertificate &certificate)`

设置本地单张证书。若需要发送中间链，应使用 `setLocalCertificateChain()`。

#### `QSslCertificate peerCertificate() const`

返回握手后对端证书。握手前通常为空。

#### `QList<QSslCertificate> peerCertificateChain() const`

返回握手后收到的对端证书链。顺序和内容受 backend/对端发送内容影响；没有握手或无证书时可能为空。

#### `QSslCipher sessionCipher() const`

返回实际协商密码套件。握手前通常为空 cipher。

#### `QSsl::SslProtocol sessionProtocol() const`

返回实际协商协议。握手前可能是未知值。

### 私钥

#### `QSslKey privateKey() const`

返回当前配置的本地私钥。私钥是敏感材料，读取后不要输出或长期复制。

#### `void setPrivateKey(const QSslKey &key)`

设置本地私钥，通常用于服务端或双向 TLS 客户端。它必须与本地叶子证书匹配，并在握手前设置。

### 密码套件

#### `QList<QSslCipher> ciphers() const`

返回当前允许的密码套件列表，通常按偏好顺序保存。

#### `void setCiphers(const QList<QSslCipher> &ciphers)`

设置允许的密码套件列表。列表应是 `supportedCiphers()` 的子集；过度收紧可能导致握手无共同套件。

#### `void setCiphers(const QString &ciphers)`

使用冒号分隔的名称设置密码套件。名称和顺序依赖 backend，某些 backend 可能忽略顺序。

#### `static QList<QSslCipher> supportedCiphers()`

返回当前 active backend 支持的密码套件。应用应从此结果筛选，而不是假设所有平台一致。

### CA 和 SSL 选项

#### `QList<QSslCertificate> caCertificates() const`

返回当前显式配置的 CA 列表。不要把它误解成 backend 最终使用的全部信任锚。

#### `void setCaCertificates(const QList<QSslCertificate> &certificates)`

替换 CA 列表。显式设置后要确认是否仍需保留系统 CA。

#### `bool addCaCertificates(const QString &path, QSsl::EncodingFormat format = QSsl::Pem, QSslCertificate::PatternSyntax syntax = QSslCertificate::PatternSyntax::FixedString)`

从路径读取并追加 CA。路径语法交给 `QSslCertificate::fromPath()`；失败或没有可解析证书时返回 false。

#### `void addCaCertificate(const QSslCertificate &certificate)`

追加一张 CA 证书。传入 null certificate 不会变成有效信任锚。

#### `void addCaCertificates(const QList<QSslCertificate> &certificates)`

追加一组 CA 证书，不替换已有列表。

#### `static QList<QSslCertificate> systemCaCertificates()`

返回平台/backend 能发现的系统 CA。结果受操作系统、部署方式和 SSL backend 影响，可能为空。

#### `void setSslOption(QSsl::SslOption option, bool on)`

打开或关闭指定 SSL 选项。具体选项语义由 `QSsl` 文档和 backend 支持决定，应在握手前设置。

#### `bool testSslOption(QSsl::SslOption option) const`

读取指定 SSL 选项是否启用。它表示配置状态，不一定表示 backend 最终能实现该选项。

### Session ticket 和临时密钥

#### `QByteArray sessionTicket() const`

返回会话恢复 ticket。属于敏感 TLS 材料，不应写日志或交给不可信代码。

#### `void setSessionTicket(const QByteArray &sessionTicket)`

设置会话 ticket，用于支持的会话恢复场景。ticket 必须来自兼容 backend/连接上下文，不能随意跨环境复用。

#### `int sessionTicketLifeTimeHint() const`

返回 backend/服务端提供的 ticket 生命期提示。它不是绝对有效期。

#### `QSslKey ephemeralServerKey() const`

返回客户端看到的临时服务端密钥。只对支持前向保密的相关会话有意义，不是长期私钥。

### 椭圆曲线、PSK 和 DH

#### `QList<QSslEllipticCurve> ellipticCurves() const`

返回当前允许使用的椭圆曲线列表。

#### `void setEllipticCurves(const QList<QSslEllipticCurve> &curves)`

设置椭圆曲线列表。应传 `supportedEllipticCurves()` 的子集。

#### `static QList<QSslEllipticCurve> supportedEllipticCurves()`

返回当前 backend 支持的曲线列表。

#### `QByteArray preSharedKeyIdentityHint() const`

返回服务端模式下给 PSK 客户端的 identity hint。它只是提示，可能为空。

#### `void setPreSharedKeyIdentityHint(const QByteArray &hint)`

设置服务端发送的 PSK identity hint，主要对下一次握手生效。实际 PSK 通过 authenticator 回调提供。

#### `QSslDiffieHellmanParameters diffieHellmanParameters() const`

返回配置的 DH 参数。它主要服务于 backend 支持的传统 DH 场景；空参数表示没有显式设置。

#### `void setDiffieHellmanParameters(const QSslDiffieHellmanParameters &dhparams)`

设置 DH 参数。参数必须能被当前 backend 使用，并在握手前设置。

### Backend 和默认配置

#### `QMap<QByteArray, QVariant> backendConfiguration() const`

返回应用显式设置的 backend 键值。它不保证包含 backend 默认值或最终生效值。

#### `void setBackendConfigurationOption(const QByteArray &name, const QVariant &value)`

设置一个 backend 专用选项。键名和值由 active backend 定义，跨 backend 不应直接复用。

#### `void setBackendConfiguration(const QMap<QByteArray, QVariant> &backendConfiguration = QMap<QByteArray, QVariant>())`

整体替换 backend 配置映射。传空映射可清除显式 backend 选项。

#### `static QSslConfiguration defaultConfiguration()`

返回当前默认 TLS 配置的值副本。后续修改副本不会自动改全局默认值。

#### `static void setDefaultConfiguration(const QSslConfiguration &configuration)`

设置进程级默认 TLS 配置，影响之后创建或使用默认配置的新会话，不追溯已有连接。

#### `static QSslConfiguration defaultDtlsConfiguration()`

返回默认 DTLS 配置。只有启用 DTLS 支持时可用。

#### `static void setDefaultDtlsConfiguration(const QSslConfiguration &configuration)`

设置进程级默认 DTLS 配置，只影响后续 DTLS 会话。

### DTLS、握手控制、OCSP 和协议协商

#### `bool dtlsCookieVerificationEnabled() const`

返回是否启用 DTLS cookie 验证。它只适用于 DTLS，并受构建配置影响。

#### `void setDtlsCookieVerificationEnabled(bool enable)`

启用或关闭 DTLS cookie 验证。应在 DTLS 握手前设置。

#### `bool handshakeMustInterruptOnError() const`

返回是否要求在可恢复握手错误处中断并通知应用。主要由 OpenSSL backend 支持。

#### `void setHandshakeMustInterruptOnError(bool interrupt)`

设置握手错误中断策略。启用后必须通过 socket/server 的信号同步处理并继续握手。

#### `bool missingCertificateIsFatal() const`

返回缺少证书时是否视为致命错误。主要由 OpenSSL backend 支持。

#### `void setMissingCertificateIsFatal(bool cannotRecover)`

设置缺少证书的错误策略。它不是所有 backend 都能同样实现。

#### `void setOcspStaplingEnabled(bool enable)`

在握手前启用 OCSP stapling 路径。启用不保证收到有效 stapled response。

#### `bool ocspStaplingEnabled() const`

返回 OCSP stapling 配置开关状态，不代表实际已有 OCSP 响应。

#### `enum NextProtocolNegotiationStatus`

包含 `NextProtocolNegotiationNone`、`NextProtocolNegotiationNegotiated` 和 `NextProtocolNegotiationUnsupported`。它描述 ALPN/NPN 协议协商状态。

#### `void setAllowedNextProtocols(const QList<QByteArray> &protocols)`

设置 ALPN/NPN 允许协议及偏好顺序。应在握手前调用；最终选择仍由双方决定。

#### `QList<QByteArray> allowedNextProtocols() const`

返回已配置的允许协议列表。

#### `QByteArray nextNegotiatedProtocol() const`

返回实际协商出的下一协议。尚未协商或没有结果时可能为空。

#### `NextProtocolNegotiationStatus nextProtocolNegotiationStatus() const`

返回 ALPN/NPN 状态。`None` 不等于失败，需结合是否启用协议列表和握手状态理解。

#### `static const char ALPNProtocolHTTP2[]`

Qt 提供的 HTTP/2 ALPN 协议名常量，值适合放入允许协议列表。

#### `static const char NextProtocolHttp1_1[]`

Qt 提供的 HTTP/1.1 下一协议名常量，适合与 ALPN/NPN 列表配合使用。

## API 速查表

| 类别 | API | 语义 | 边界与注意事项 |
| --- | --- | --- | --- |
| 构造 | `QSslConfiguration()` | 构造 null 配置。 | `isNull()` 为 true，不代表 SSL 不可用。 |
| 值语义 | 拷贝/移动/赋值/`swap()` | 管理隐式共享配置值。 | 不拥有 socket、文件或 SSL 会话。 |
| 比较 | `operator==` / `operator!=` | 比较配置值。 | 不保证最终握手结果相同。 |
| 状态 | `isNull()` | 判断是否有显式配置状态。 | 不等于配置有效性。 |
| 协议 | `protocol()` / `setProtocol()` | 查询或设置协议策略。 | 实际版本看 `sessionProtocol()`。 |
| 验证 | `peerVerifyMode()` / `setPeerVerifyMode()` | 配置对端证书验证。 | 默认 `AutoVerifyPeer` 受角色影响。 |
| 验证 | `peerVerifyDepth()` / `setPeerVerifyDepth()` | 查询/设置验证深度。 | 0 表示不限制。 |
| 本地证书 | `localCertificateChain()` / `setLocalCertificateChain()` | 配置本地证书链。 | 叶子证书通常在首位。 |
| 本地证书 | `localCertificate()` / `setLocalCertificate()` | 读取/设置链首单证书。 | 需要中间链时用 chain API。 |
| 对端证书 | `peerCertificate()` | 获取握手后的对端叶子证书。 | 握手前可能为空。 |
| 对端链 | `peerCertificateChain()` | 获取握手后的对端证书链。 | 内容取决于对端和 backend。 |
| 会话结果 | `sessionCipher()` | 获取实际协商密码套件。 | 不是允许列表。 |
| 会话结果 | `sessionProtocol()` | 获取实际协商协议。 | 握手前可能未知。 |
| 私钥 | `privateKey()` / `setPrivateKey()` | 查询/配置本地私钥。 | 必须与叶子证书匹配，属于敏感材料。 |
| 密码套件 | `ciphers()` / `setCiphers(QList)` | 配置允许套件及顺序。 | 必须是当前 backend 支持子集。 |
| 密码套件 | `setCiphers(QString)` | 用冒号名称设置套件。 | 名称/顺序依赖 backend。 |
| 查询能力 | `supportedCiphers()` | 获取支持的密码套件。 | 不同 backend/platform 可能不同。 |
| CA | `caCertificates()` / `setCaCertificates()` | 查询或替换 CA 列表。 | 替换后要确认是否保留系统 CA。 |
| CA | `addCaCertificate()` | 追加一张 CA。 | null 证书不能成为有效信任锚。 |
| CA | `addCaCertificates(QList)` | 追加一组 CA。 | 不替换原列表。 |
| CA | `addCaCertificates(path, ...)` | 从路径解析并追加 CA。 | 返回 false 表示没有成功追加。 |
| 系统 CA | `systemCaCertificates()` | 获取系统 CA。 | 受 OS、部署和 backend 影响。 |
| SSL 选项 | `setSslOption()` / `testSslOption()` | 设置/读取 SSL option。 | 反映配置，不保证 backend 实现。 |
| Session ticket | `sessionTicket()` / `setSessionTicket()` | 读取/设置会话恢复 ticket。 | 属于敏感材料。 |
| Session ticket | `sessionTicketLifeTimeHint()` | 读取生命期提示。 | 不是绝对有效期。 |
| 临时密钥 | `ephemeralServerKey()` | 获取客户端会话临时服务端密钥。 | 非长期私钥，可能为空。 |
| 椭圆曲线 | `ellipticCurves()` / `setEllipticCurves()` | 配置允许曲线。 | 应是支持曲线的子集。 |
| 椭圆曲线 | `supportedEllipticCurves()` | 查询支持曲线。 | 受 backend/platform 影响。 |
| PSK | `preSharedKeyIdentityHint()` / `setPreSharedKeyIdentityHint()` | 查询/设置服务端 PSK 提示。 | 主要影响下一次服务端握手。 |
| DH | `diffieHellmanParameters()` / `setDiffieHellmanParameters()` | 查询/设置 DH 参数。 | 依赖 backend 和握手算法。 |
| Backend | `backendConfiguration()` | 获取显式 backend 设置。 | 不含全部 backend 默认值。 |
| Backend | `setBackendConfigurationOption()` | 设置 backend 专用键值。 | 不具备跨 backend 通用语义。 |
| Backend | `setBackendConfiguration()` | 整体替换 backend 配置。 | 空映射可清除显式设置。 |
| 默认 TLS | `defaultConfiguration()` | 获取默认配置副本。 | 修改副本不修改全局默认。 |
| 默认 TLS | `setDefaultConfiguration()` | 设置进程级默认 TLS 配置。 | 只影响后续新会话。 |
| 默认 DTLS | `defaultDtlsConfiguration()` | 获取默认 DTLS 配置。 | 需启用 DTLS。 |
| 默认 DTLS | `setDefaultDtlsConfiguration()` | 设置默认 DTLS 配置。 | 不追溯已有会话。 |
| DTLS | `dtlsCookieVerificationEnabled()` / `setDtlsCookieVerificationEnabled()` | 配置 DTLS cookie 验证。 | 只适用于 DTLS。 |
| 握手控制 | `handshakeMustInterruptOnError()` / `setHandshakeMustInterruptOnError()` | 配置错误时是否中断握手。 | 主要 OpenSSL；继续需同步调用 socket API。 |
| 证书缺失 | `missingCertificateIsFatal()` / `setMissingCertificateIsFatal()` | 配置缺少证书的致命性。 | 主要 OpenSSL 支持。 |
| OCSP | `setOcspStaplingEnabled()` / `ocspStaplingEnabled()` | 配置 OCSP stapling。 | 开启不等于已收到响应。 |
| ALPN/NPN | `NextProtocolNegotiationStatus` | 描述下一协议协商状态。 | `None` 不一定是失败。 |
| ALPN/NPN | `setAllowedNextProtocols()` / `allowedNextProtocols()` | 配置/读取允许协议列表。 | 握手前设置，顺序表达偏好。 |
| ALPN/NPN | `nextNegotiatedProtocol()` | 获取实际协商协议。 | 握手前可能为空。 |
| 常量 | `ALPNProtocolHTTP2` / `NextProtocolHttp1_1` | Qt 提供的常用协议名。 | 仍需检查 backend/对端是否支持。 |

## 一句话总结

`QSslConfiguration` 是 TLS/DTLS 策略和值材料的可复制容器：先配置再握手，验证模式要考虑客户端/服务端角色，允许列表不等于实际协商结果，真正的会话密码套件、协议和 ALPN 结果必须在握手后读取。
