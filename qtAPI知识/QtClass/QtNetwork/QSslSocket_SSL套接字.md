# QSslSocket

> Qt 6.11.1 | Qt6::Network | `#include <QSslSocket>`

## 类解决的问题

`QSslSocket` 是在 `QTcpSocket` 之上提供 TLS/SSL 的网络套接字。它把 TCP 字节流和证书、密钥、握手、加密读写、对端验证、会话恢复及协议协商连接起来，解决：

- 作为 TLS 客户端连接 HTTPS、数据库、消息服务或自定义安全协议；
- 作为 TLS 服务端承载已经接受的 TCP descriptor；
- 在 STARTTLS 等协议中把已连接的明文 TCP 升级为 TLS；
- 配置证书验证、CA、密码套件、协议、私钥和 ALPN；
- 接收证书错误、PSK 请求、TLS alert 和握手中断通知；
- 在握手后以普通 `QIODevice` 读写解密后的应用数据。

它不是 HTTP 客户端，也不负责业务层身份授权。TLS 握手成功只说明 TLS 层建立；应用仍需验证业务身份、权限和协议内容。

## 实际使用场景

### 1. HTTPS 风格的客户端连接

```cpp
auto *socket = new QSslSocket(this);

QSslConfiguration configuration =
    QSslConfiguration::defaultConfiguration();
configuration.setPeerVerifyMode(QSslSocket::VerifyPeer);
socket->setSslConfiguration(configuration);

connect(socket, &QSslSocket::encrypted, this, [socket] {
    socket->write("GET / HTTP/1.1\r\nHost: example.com\r\n"
                  "Connection: close\r\n\r\n");
});

connect(socket, &QSslSocket::readyRead, this, [socket] {
    qInfo().noquote() << socket->readAll();
});

socket->connectToHostEncrypted(QStringLiteral("example.com"), 443);
```

`connectToHostEncrypted()` 会先建立 TCP，再自动启动客户端 TLS 握手。应用数据可以在握手前写入并排队，但更清晰、也更容易处理错误的方式是在 `encrypted()` 后开始业务写入。

### 2. STARTTLS

```cpp
socket->connectToHost(QStringLiteral("mail.example.com"), 587);

connect(socket, &QSslSocket::readyRead, this, [socket] {
    if (serverSaidStartTls()) {
        socket->startClientEncryption();
    }
});
```

STARTTLS 必须先完成明文协议规定的升级步骤，并且 socket 处于 `ConnectedState` 且尚未加密。调用 `startClientEncryption()` 后，后续读写进入 TLS 层；应用协议必须正确区分升级前后的字节。

### 3. 服务端接管已接受 descriptor

```cpp
auto *socket = new QSslSocket;
if (!socket->setSocketDescriptor(descriptor)) {
    socket->deleteLater();
    return;
}

socket->setSslConfiguration(serverConfiguration);
socket->startServerEncryption();
```

服务端通常在 `setSocketDescriptor()` 成功后启动 `startServerEncryption()`。descriptor 的所有权由 socket 接管；不能再让另一个 `QAbstractSocket` 使用同一个 native descriptor。

### 4. 处理证书错误和 PSK

```cpp
connect(socket, &QSslSocket::sslErrors, socket,
        [socket](const QList<QSslError> &errors) {
    if (isExplicitTestException(errors)) {
        socket->ignoreSslErrors(errors);
    }
});

connect(socket, &QSslSocket::preSharedKeyAuthenticationRequired,
        socket, [](QSslPreSharedKeyAuthenticator *authenticator) {
    authenticator->setIdentity(QByteArrayLiteral("device-42"));
    authenticator->setPreSharedKey(loadPsk());
});
```

证书错误只能按明确的信任策略处理；PSK authenticator 只能在同步回调期间使用，不能保存指针异步完成认证。

## 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(app PRIVATE Qt6::Network)
```

```cpp
#include <QSslSocket>

auto *socket = new QSslSocket;
connect(socket, &QSslSocket::encrypted, socket, [socket] {
    qInfo() << socket->sessionCipher().name()
            << socket->sessionProtocol();
});
socket->connectToHostEncrypted(QStringLiteral("example.com"), 443);
```

运行时还要确认当前 Qt 构建包含 SSL backend。`supportsSsl()` 为 false 时，不能靠配置对象或代码调用强行获得 TLS 能力。

## 关键语义与边界

### 三种 `SslMode`

- `UnencryptedMode`：普通 TCP，尚未进入 TLS；
- `SslClientMode`：客户端 TLS 模式；
- `SslServerMode`：服务端 TLS 模式。

`mode()` 描述当前 TLS 角色/状态，不等于连接状态。`isEncrypted()` 只有握手完成并进入可用加密会话后才为 true；处于 `SslClientMode` 或 `SslServerMode` 并不意味着验证已经成功。

### `connectToHostEncrypted()` 会自动开始握手

它等价于普通 TCP `connectToHost()` 成功后自动调用 `startClientEncryption()`。函数返回时通常只是启动了异步连接流程；应用应等待 `encrypted()`，并处理 `sslErrors()`、`errorOccurred()`、`disconnected()` 等信号。

在 TCP 连接建立但 TLS 尚未完成期间写入的数据会进入 Qt 的写入队列，握手成功后发送。应用不应把“`write()` 返回接受了字节”解释成“对端已经收到明文业务数据”。

第二个重载允许把 TCP 连接目标和证书验证名称分开，适合连接 IP、代理地址或别名但按真实主机名验证证书的场景。

### STARTTLS 的状态前提

`startClientEncryption()` 应在 `ConnectedState + UnencryptedMode` 调用。未连接、已经加密或状态不允许升级时，调用不会完成预期握手。服务端对应 `startServerEncryption()`。

STARTTLS 协议升级必须由应用层确认服务端已经同意。不能仅因为 socket 已连接，就立即把剩余明文当成 TLS 握手数据。

### `setSocketDescriptor()` 会接管 descriptor

成功调用后，socket 使用并管理该 native descriptor。descriptor 必须有效，不能同时交给另一个 socket；socket 析构或关闭时会按 `QAbstractSocket` 所有权规则处理它。

它不会自动完成服务端 TLS 握手。服务端需要随后调用 `startServerEncryption()`；客户端若接管一个已连接 descriptor，则按场景调用 `startClientEncryption()`。

### 配置的生效时间和不可覆盖字段

协议、验证模式、验证深度、证书、私钥、CA、密码套件、曲线、OCSP、PSK hint 和 ALPN 等应在握手前设置。`setSslConfiguration()` 不能覆盖会话状态字段，如已经协商的 cipher、protocol、对端证书或会话 ticket。

更换配置不会把当前连接重置为新 TLS 会话。要使用新策略，通常应断开、创建新 socket 或在下一次连接前重新配置。

### 对端验证名称可以和 TCP 主机名不同

`setPeerVerifyName()` 设置证书主机名校验使用的名称。它解决“连接地址不是证书名称”的问题，但不会关闭证书链验证，也不会把任意字符串变成可信名称。若不显式设置，Qt 通常使用连接时的主机名。

IP 地址、DNS 名称、通配符和国际化域名有不同匹配规则，应让 Qt/backend 执行标准校验，应用层读取 SAN 主要用于诊断。

### 证书、私钥和会话结果

`setLocalCertificateChain()`、`setLocalCertificate()` 和 `setPrivateKey()` 配置本地身份；服务端私钥必须与叶子证书匹配。`peerCertificate()` 与 `peerCertificateChain()` 要等握手后才有意义。`sessionCipher()` 和 `sessionProtocol()` 也是握手结果，不是预设值。

`setPrivateKey(QString, ...)` 从文件加载私钥，默认算法是 RSA、默认格式是 PEM。加密私钥要提供口令；文件读取失败、算法不匹配或口令错误时应检查 `privateKey().isNull()`。

### 加密前后的字节计数不是同一个层

- `bytesAvailable()`、`read()`、`readyRead()` 面向已经解密的应用数据；
- `bytesToWrite()` 面向 Qt SSL 层尚未处理完的应用写入；
- `encryptedBytesAvailable()` 表示底层加密输入中尚未解密的字节，通常因为 Qt 会尽快解密而接近 0；
- `encryptedBytesToWrite()` 表示已经加密但还未写入底层 TCP 的数据；
- `encryptedBytesWritten()` 报告加密数据写入网络层；
- `bytesWritten()` 报告应用数据写入 SSL 层，不等价于网络发送完成。

不要用 `bytesWritten()` 推断对端收到，也不要用 `encryptedBytesWritten()` 推断对端已经处理应用协议。

### 阻塞等待会阻塞线程

`waitForEncrypted()`、`waitForReadyRead()`、`waitForBytesWritten()` 等会阻塞调用线程并依赖网络事件处理。GUI 线程一般应使用异步信号；阻塞等待更适合专门的工作线程。超时返回 false 时还要检查 `error()`、SSL 错误列表和 socket 状态。

### SSL 错误的同步窗口

`sslErrors()` 只报告问题，不自动决定是否继续。若应用明确允许一组错误，应在信号处理期间直接调用 `ignoreSslErrors(errors)`；使用 queued connection 或延迟调用可能已经错过握手窗口。

无参 `ignoreSslErrors()` 会忽略全部 SSL 错误，风险很高。列表重载只允许忽略指定错误，但仍要确认错误对象包含的证书和连接目标符合预期。

### 握手中断和 PSK 回调是临时同步上下文

启用 `QSslConfiguration::setHandshakeMustInterruptOnError(true)` 后，`handshakeInterruptedOnError` 需要 direct 处理，并在槽内调用 `continueInterruptedHandshake()`。否则握手会保持中断或失败。

`preSharedKeyAuthenticationRequired` 的 authenticator 指针由 socket/backend 临时管理。必须在回调返回前设置 identity 和 PSK，不能保存、删除或异步使用。

### Session ticket、OCSP 和 ALPN

`newSessionTicketReceived()` 主要适用于 TLS 1.3 和支持该能力的 OpenSSL 路径；它不是每个 backend 都保证发出。配置/读取 ticket 时要把它当作敏感材料。

OCSP stapling 需要在握手前通过配置启用；`ocspResponses()` 只有收到并解析响应后才有内容，启用开关不等于服务端提供了有效响应。

ALPN/NPN 通过 `QSslConfiguration::setAllowedNextProtocols()` 配置。握手完成后看 `nextNegotiatedProtocol()` 和 `nextProtocolNegotiationStatus()`；`None`、`Negotiated`、`Unsupported` 的含义必须结合是否设置列表和 backend 能力判断。

### backend 必须在首次使用 SSL 类前选择

Qt 6 支持多个 SSL backend。`setActiveBackend()` 应在首次创建/使用 SSL 类前完成；一旦应用已经使用 SSL 类，切换 backend 可能失败，也不应在同一进程中混用不同 backend 的对象和假设。

支持的协议、功能和实现类都可能因 backend、平台、动态库版本而不同。`supportsSsl()` 只说明当前环境是否有可用 SSL 能力，不能保证每个功能都支持。

## 常见误区

- `connectToHostEncrypted()` 返回就开始发业务协议：应等 `encrypted()`。
- `isEncrypted()` 为 false 就继续当普通 TCP 使用：TLS 握手期间的数据边界不能按业务明文解释。
- 在未连接或已经加密的状态调用 `startClientEncryption()`：不会完成预期升级。
- 用 TCP 连接地址代替证书校验名：需要时使用 `setPeerVerifyName()`。
- `setSslConfiguration()` 后期待当前会话立即重配：配置主要作用于下一次握手，不能覆盖会话状态。
- 把 `bytesWritten()` 当作对端已收到：它只表示写入 SSL 层。
- 在 `sslErrors()` 中无条件调用无参 `ignoreSslErrors()`：等于放弃证书错误防线。
- 用 queued 槽处理 SSL 错误或握手中断：可能错过同步恢复窗口。
- 保存或删除 PSK authenticator 指针：指针只在回调期间有效。
- 把 `sessionCipher()`、`sessionProtocol()` 在握手前当成真实结果读取。
- 把 `supportsSsl()` 当成所有 TLS 功能都可用：能力还需按 backend/feature 查询。
- 两个 socket 共用一个 native descriptor：会导致未定义资源管理和连接行为。

## 逐项 API 说明

### 枚举、构造和生命周期

#### `enum SslMode`

包含 `UnencryptedMode`、`SslClientMode` 和 `SslServerMode`，描述当前 socket 的 TLS 模式。它不是 `QAbstractSocket::SocketState`，不能单独说明 TCP 是否已连接。

#### `enum PeerVerifyMode`

包含 `VerifyNone`、`QueryPeer`、`VerifyPeer` 和 `AutoVerifyPeer`，控制是否及如何验证对端证书。`AutoVerifyPeer` 会根据客户端/服务端角色采用不同默认行为。

#### `explicit QSslSocket(QObject *parent = nullptr)`

构造 SSL socket。它开始时未连接、未加密，parent 决定 QObject 所有权和线程归属。

#### `~QSslSocket()`

销毁 socket，关闭并释放其网络资源和 SSL backend 状态。不要在仍有异步回调需要使用时提前删除；常见做法是连接 `disconnected()` 到 `deleteLater()`。

#### `void resume() override`

继续被代理认证、SSL 错误等流程暂停的 socket 操作。普通 TLS 错误处理优先使用专用 API；不要把它当成任意握手恢复函数。

### 连接、握手和 descriptor

#### `void connectToHostEncrypted(const QString &hostName, quint16 port, OpenMode mode = ReadWrite, NetworkLayerProtocol protocol = AnyIPProtocol)`

建立 TCP 连接并自动启动客户端 TLS。函数返回不代表加密完成；等待 `encrypted()`。

#### `void connectToHostEncrypted(const QString &hostName, quint16 port, const QString &sslPeerName, OpenMode mode = ReadWrite, NetworkLayerProtocol protocol = AnyIPProtocol)`

建立 TCP 连接并以 `sslPeerName` 作为证书验证名称。适合连接名和证书名不同的场景；不关闭链验证。

#### `bool setSocketDescriptor(qintptr socketDescriptor, SocketState state = ConnectedState, OpenMode openMode = ReadWrite)`

让 socket 接管已有 native descriptor。成功后 descriptor 不能再交给其他 socket；服务端通常随后调用 `startServerEncryption()`。

#### `void connectToHost(const QString &hostName, quint16 port, OpenMode openMode = ReadWrite, NetworkLayerProtocol protocol = AnyIPProtocol)`

建立普通 TCP 连接，不自动开始 TLS。适合 STARTTLS；升级时在正确协议状态调用 `startClientEncryption()`。

#### `void disconnectFromHost()`

请求断开连接。TLS close_notify、TCP 关闭和信号到达是异步过程；需要立即放弃时可按 `QAbstractSocket` 规则使用 `abort()`。

#### `void setSocketOption(QAbstractSocket::SocketOption option, const QVariant &value)`

设置继承的 socket 选项。具体选项是否在当前状态/backend 生效依赖 `QAbstractSocket` 和平台。

#### `QVariant socketOption(QAbstractSocket::SocketOption option)`

读取 socket 选项。返回值类型和支持情况依赖选项及平台。

#### `SslMode mode() const`

返回当前 TLS 模式。

#### `bool isEncrypted() const`

返回 TLS 握手是否完成并已建立加密会话。`SslClientMode`/`SslServerMode` 本身不保证 true。

#### `void startClientEncryption()`

在已连接且未加密的 TCP socket 上启动客户端 TLS 握手。错误状态、未连接或已经加密时不会完成预期操作。

#### `void startServerEncryption()`

在已接管连接 descriptor 或已连接的 socket 上启动服务端 TLS 握手。应先配置本地证书链、私钥和验证策略。

#### `bool waitForConnected(int msecs = 30000)`

阻塞等待 TCP 连接建立。只代表 TCP 层，不代表 TLS 加密完成；随后还要等待 `waitForEncrypted()`。

#### `bool waitForEncrypted(int msecs = 30000)`

阻塞等待 TLS 握手完成。返回 false 时检查 `error()`、`sslHandshakeErrors()` 和连接状态。

#### `bool waitForReadyRead(int msecs = 30000)`

阻塞等待解密后的应用数据可读。它不是等待底层密文到达的 API。

#### `bool waitForBytesWritten(int msecs = 30000)`

阻塞等待应用写入数据被处理到 SSL 层。它不保证密文已经到达对端。

#### `bool waitForDisconnected(int msecs = 30000)`

阻塞等待 socket 断开。GUI 线程应优先使用异步信号。

#### `void continueInterruptedHandshake()`

继续由 `handshakeInterruptedOnError` 暂停的握手。必须在同步错误处理槽中调用；没有处于中断状态时调用没有有用效果。

### 协议、验证和配置

#### `QSsl::SslProtocol protocol() const`

返回当前 socket 配置的协议策略。实际版本看 `sessionProtocol()`。

#### `void setProtocol(QSsl::SslProtocol protocol)`

设置协议策略。应在连接/握手前调用。

#### `PeerVerifyMode peerVerifyMode() const`

返回对端验证模式。

#### `void setPeerVerifyMode(PeerVerifyMode mode)`

设置对端验证模式。`VerifyNone` 会显著降低 TLS 身份验证能力。

#### `int peerVerifyDepth() const`

返回证书链深度限制，0 表示不限制。

#### `void setPeerVerifyDepth(int depth)`

设置验证深度限制。应在握手前设置。

#### `QString peerVerifyName() const`

返回用于证书主机名验证的名称。

#### `void setPeerVerifyName(const QString &hostName)`

设置证书验证名称，使其与 TCP 连接的 hostName 分离。

#### `QSslConfiguration sslConfiguration() const`

返回当前 TLS 配置的值副本。读取会话结果应在握手后进行。

#### `void setSslConfiguration(const QSslConfiguration &config)`

设置 TLS 配置。主要对下一次握手生效，不能覆盖当前会话状态字段。

### 证书、密钥和会话结果

#### `void setLocalCertificateChain(const QList<QSslCertificate> &localChain)`

设置本地证书链。通常叶子证书在第一项，中间 CA 随后。

#### `QList<QSslCertificate> localCertificateChain() const`

返回本地证书链值副本。

#### `void setLocalCertificate(const QSslCertificate &certificate)`

设置本地单张证书。需要中间链时使用 chain setter。

#### `void setLocalCertificate(const QString &fileName, QSsl::EncodingFormat format = QSsl::Pem)`

从文件加载本地证书。文件读取或解析失败时检查 `localCertificate().isNull()`。

#### `QSslCertificate localCertificate() const`

返回本地链首证书；没有可用本地证书时可能为 null。

#### `QSslCertificate peerCertificate() const`

返回握手后对端叶子证书；握手前通常为空。

#### `QList<QSslCertificate> peerCertificateChain() const`

返回握手后对端证书链。

#### `QSslCipher sessionCipher() const`

返回实际协商密码套件；握手前可能为空。

#### `QSsl::SslProtocol sessionProtocol() const`

返回实际协商协议；握手前可能未知。

#### `QList<QOcspResponse> ocspResponses() const`

返回收到并解析的 OCSP stapling 响应列表。启用 OCSP 不保证列表非空；能力和响应取决于 backend/服务端。

#### `void setPrivateKey(const QSslKey &key)`

设置本地私钥。应与本地叶子证书匹配，并在握手前设置。

#### `void setPrivateKey(const QString &fileName, QSsl::KeyAlgorithm algorithm = QSsl::Rsa, QSsl::EncodingFormat format = QSsl::Pem, const QByteArray &passPhrase = QByteArray())`

从文件加载私钥。默认按 RSA/PEM 解析；加密私钥需提供口令，失败时检查 `privateKey().isNull()`。

#### `QSslKey privateKey() const`

返回当前本地私钥值。私钥属于敏感材料，不要记录或无必要复制。

### I/O 和缓冲

#### `qint64 bytesAvailable() const`

返回应用层可读取的解密字节数，并包含继承层可用数据语义。

#### `qint64 bytesToWrite() const`

返回应用数据已写入 SSL 层但尚未处理完的字节数。

#### `bool canReadLine() const`

判断解密后的应用数据中是否可读取完整行。

#### `void close()`

关闭 socket/设备。TLS 关闭过程与 TCP 断开可能异步完成；不要用它替代业务层清理。

#### `bool atEnd() const`

判断是否没有更多可读取的应用数据且底层已到末尾。TLS 缓冲和断开状态会影响结果。

#### `void setReadBufferSize(qint64 size)`

设置读取缓冲区大小。0 通常表示不限制；实际行为还受 SSL 解密缓冲和平台影响。

#### `qint64 encryptedBytesAvailable() const`

返回尚未解密的底层加密数据字节数。Qt 通常尽快解密，因此该值常为 0；不能用它判断应用数据量。

#### `qint64 encryptedBytesToWrite() const`

返回已加密但尚未写入底层 TCP 的字节数。

### 错误处理

#### `QList<QSslError> sslHandshakeErrors() const`

返回握手期间记录的 SSL 错误列表。它是诊断快照，不会自动继续或忽略错误。

#### `void ignoreSslErrors()`

忽略全部 SSL 握手错误。安全风险高，只适合极明确、受控的测试或专用信任场景。

#### `void ignoreSslErrors(const QList<QSslError> &errors)`

只忽略指定错误列表中的错误。仍需确认错误与预期证书/主机完全匹配，并在同步握手回调中调用。

### 静态 backend 和能力查询

#### `static bool supportsSsl()`

返回当前环境是否有可用 SSL 支持。false 时不能建立正常 TLS 会话。

#### `static long sslLibraryVersionNumber()`

返回运行时 SSL 库版本号的数值表示，具体格式依赖 backend。

#### `static QString sslLibraryVersionString()`

返回运行时 SSL 库版本字符串。

#### `static long sslLibraryBuildVersionNumber()`

返回 Qt 构建时使用的 SSL 库版本号。

#### `static QString sslLibraryBuildVersionString()`

返回 Qt 构建时使用的 SSL 库版本字符串。

#### `static QList<QString> availableBackends()`

返回当前可用 SSL backend 名称列表。

#### `static QString activeBackend()`

返回当前 active backend 名称。

#### `static bool setActiveBackend(const QString &backendName)`

选择 active backend。应在首次使用 SSL 类前完成；运行中切换可能失败，不能把它当作每个 socket 的独立选项。

#### `static QList<QSsl::SslProtocol> supportedProtocols(const QString &backendName = {})`

返回指定或当前 backend 支持的协议列表。

#### `static bool isProtocolSupported(QSsl::SslProtocol protocol, const QString &backendName = {})`

判断指定协议是否由指定或当前 backend 支持。

#### `static QList<QSsl::ImplementedClass> implementedClasses(const QString &backendName = {})`

返回 backend 实现的 Qt SSL 类能力集合。

#### `static bool isClassImplemented(QSsl::ImplementedClass cl, const QString &backendName = {})`

判断指定 SSL 类是否由 backend 实现。

#### `static QList<QSsl::SupportedFeature> supportedFeatures(const QString &backendName = {})`

返回 backend 支持的扩展特性集合。

#### `static bool isFeatureSupported(QSsl::SupportedFeature feat, const QString &backendName = {})`

判断指定 backend 是否支持某项 SSL 特性。

### 信号

#### `void encrypted()`

TLS 握手成功、socket 可进行加密通信时发出。客户端通常从此信号开始发送业务数据。

#### `void peerVerifyError(const QSslError &error)`

报告单个对端证书验证错误。它不自动决定继续或停止。

#### `void sslErrors(const QList<QSslError> &errors)`

报告握手 SSL 错误列表。允许特定错误时，应在同步槽中调用匹配的 `ignoreSslErrors()`。

#### `void modeChanged(QSslSocket::SslMode newMode)`

报告 TLS 模式发生变化。

#### `void encryptedBytesWritten(qint64 totalBytes)`

报告加密数据写入底层网络的字节数。它不表示对端已经收到或处理数据。

#### `void preSharedKeyAuthenticationRequired(QSslPreSharedKeyAuthenticator *authenticator)`

请求应用设置 PSK identity 和密钥。authenticator 指针只在同步回调期间有效。

#### `void newSessionTicketReceived()`

报告收到新的 TLS session ticket，主要适用于支持该能力的 TLS 1.3/OpenSSL 路径。不能假设所有 backend 都发出。

#### `void alertSent(QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`

报告发送的 TLS alert。适合诊断，支持细节依赖 backend。

#### `void alertReceived(QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`

报告接收的 TLS alert。它不等价于连接已经断开。

#### `void handshakeInterruptedOnError(const QSslError &error)`

报告因配置要求而中断的可恢复握手错误。同步处理时调用 `continueInterruptedHandshake()` 才能继续。

### 受保护 I/O 重写点

#### `qint64 readData(char *data, qint64 maxlen) override`

从 SSL 层读取并解密应用数据的 QIODevice 内部重写点。普通应用应调用 `read()`/`readAll()`，不应直接依赖内部实现。

#### `qint64 skipData(qint64 maxSize) override`

跳过解密后的应用数据。普通应用优先使用公开 QIODevice API。

#### `qint64 writeData(const char *data, qint64 len) override`

把应用数据写入 SSL 层并安排加密发送。普通应用使用 `write()`，不要直接调用受保护函数。

## API 速查表

| 类别 | API | 语义 | 边界与注意事项 |
| --- | --- | --- | --- |
| 模式 | `SslMode` | 区分未加密、客户端 TLS、服务端 TLS。 | 不等于 TCP 连接状态。 |
| 验证 | `PeerVerifyMode` | 配置对端证书验证策略。 | `AutoVerifyPeer` 受连接角色影响。 |
| 构造 | `QSslSocket(QObject *)` | 创建 SSL socket。 | 不自动连接或握手。 |
| 生命周期 | `~QSslSocket()` | 销毁 socket 和 SSL 状态。 | 异步流程中常用 `deleteLater()`。 |
| 连接 | `connectToHostEncrypted(...)` | TCP 连接后自动客户端握手。 | 等 `encrypted()`，返回不代表成功。 |
| 连接 | `connectToHost(...)` | 建立普通 TCP。 | 适合 STARTTLS。 |
| 连接 | `disconnectFromHost()` | 异步断开。 | TLS close 和 TCP 断开可能分开完成。 |
| Descriptor | `setSocketDescriptor(...)` | 接管已有 native descriptor。 | 不能与另一个 socket 共用。 |
| 握手 | `startClientEncryption()` | 启动客户端 TLS。 | 需已连接且未加密。 |
| 握手 | `startServerEncryption()` | 启动服务端 TLS。 | 先配置证书/私钥。 |
| 状态 | `mode()` | 查询 TLS 模式。 | 不代表握手成功。 |
| 状态 | `isEncrypted()` | 查询握手是否成功。 | 只有完成加密会话才为 true。 |
| 阻塞 | `waitForConnected()` | 等 TCP 连接。 | 不等于 TLS 已建立。 |
| 阻塞 | `waitForEncrypted()` | 等 TLS 握手。 | GUI 线程慎用。 |
| 阻塞 | `waitForReadyRead()` | 等解密应用数据。 | 阻塞调用线程。 |
| 阻塞 | `waitForBytesWritten()` | 等写入 SSL 层。 | 不等于对端收到。 |
| 阻塞 | `waitForDisconnected()` | 等断开。 | 异步程序优先用信号。 |
| 恢复 | `resume()` | 继续暂停的 socket 操作。 | 不替代专用握手恢复 API。 |
| 恢复 | `continueInterruptedHandshake()` | 继续被错误中断的握手。 | 必须同步调用。 |
| 协议 | `protocol()` / `setProtocol()` | 配置协议策略。 | 实际版本看 `sessionProtocol()`。 |
| 验证 | `peerVerifyMode()` / `setPeerVerifyMode()` | 配置对端验证。 | `VerifyNone` 风险高。 |
| 验证 | `peerVerifyDepth()` / `setPeerVerifyDepth()` | 配置链深度限制。 | 0 表示不限制。 |
| 验证 | `peerVerifyName()` / `setPeerVerifyName()` | 配置证书主机名。 | 可与 TCP host 分离。 |
| 配置 | `sslConfiguration()` / `setSslConfiguration()` | 读取/设置 TLS 配置。 | 主要对下一次握手生效。 |
| 本地证书 | `setLocalCertificateChain()` / `localCertificateChain()` | 配置/读取本地证书链。 | 叶子通常在首位。 |
| 本地证书 | `setLocalCertificate()` / `localCertificate()` | 配置/读取本地叶子证书。 | 中间链用 chain API。 |
| 对端证书 | `peerCertificate()` | 获取对端叶子证书。 | 握手前可能为空。 |
| 对端链 | `peerCertificateChain()` | 获取对端证书链。 | 握手后读取。 |
| 会话 | `sessionCipher()` | 获取实际密码套件。 | 不是允许列表。 |
| 会话 | `sessionProtocol()` | 获取实际协议版本。 | 握手前可能未知。 |
| OCSP | `ocspResponses()` | 获取收到的 OCSP 响应。 | 启用 stapling 不保证有响应。 |
| 私钥 | `setPrivateKey(QSslKey)` / `privateKey()` | 配置/读取私钥。 | 必须与本地证书匹配。 |
| 私钥 | `setPrivateKey(fileName, ...)` | 从文件加载私钥。 | 默认 RSA/PEM；加密 key 需口令。 |
| I/O | `bytesAvailable()` / `bytesToWrite()` | 查询解密读和 SSL 层写缓冲。 | 不等同于密文网络计数。 |
| I/O | `canReadLine()` / `atEnd()` | 查询解密应用流状态。 | 按 QIODevice 语义使用。 |
| I/O | `close()` | 关闭 socket。 | 关闭/断开可能异步。 |
| I/O | `setReadBufferSize()` | 设置读取缓冲上限。 | 0 通常表示不限制。 |
| 加密 I/O | `encryptedBytesAvailable()` | 查询待解密密文字节。 | 通常接近 0。 |
| 加密 I/O | `encryptedBytesToWrite()` | 查询待写入 TCP 的密文。 | 不等于对端已收。 |
| 错误 | `sslHandshakeErrors()` | 获取握手错误快照。 | 不自动恢复。 |
| 错误 | `ignoreSslErrors()` | 忽略全部 SSL 错误。 | 高风险，只限明确场景。 |
| 错误 | `ignoreSslErrors(errors)` | 忽略指定 SSL 错误。 | 要按证书/主机策略白名单。 |
| Backend | `supportsSsl()` | 查询当前环境 SSL 能力。 | 不代表所有 feature 支持。 |
| Backend | SSL library version APIs | 查询运行时/构建时库版本。 | 数值格式依 backend。 |
| Backend | `availableBackends()` / `activeBackend()` | 查询 backend。 | 能力和结果因 backend 变化。 |
| Backend | `setActiveBackend()` | 设置 active backend。 | 应在首次使用 SSL 类前。 |
| 能力 | `supportedProtocols()` / `isProtocolSupported()` | 查询协议支持。 | 可指定 backend。 |
| 能力 | `implementedClasses()` / `isClassImplemented()` | 查询实现类。 | 受 backend 影响。 |
| 能力 | `supportedFeatures()` / `isFeatureSupported()` | 查询功能支持。 | 不要跨 backend 假设。 |
| 信号 | `encrypted()` | TLS 握手成功。 | 客户端常在此开始业务写入。 |
| 信号 | `peerVerifyError()` | 报告单个验证错误。 | 不自动决定继续。 |
| 信号 | `sslErrors()` | 报告 SSL 错误列表。 | 继续时同步调用 ignore API。 |
| 信号 | `modeChanged()` | TLS 模式变化。 | 不等于 encrypted。 |
| 信号 | `encryptedBytesWritten()` | 密文写入网络层。 | 不等于对端收到。 |
| 信号 | `preSharedKeyAuthenticationRequired()` | 请求 PSK 凭据。 | authenticator 只在回调内有效。 |
| 信号 | `newSessionTicketReceived()` | 收到 TLS session ticket。 | 主要 TLS 1.3/OpenSSL。 |
| 信号 | `alertSent()` / `alertReceived()` | TLS alert 诊断。 | backend 支持有差异。 |
| 信号 | `handshakeInterruptedOnError()` | 报告握手中断。 | 同步调用 continue。 |
| 受保护 | `readData()` / `skipData()` / `writeData()` | SSL QIODevice 内部 I/O 钩子。 | 普通应用使用公开 QIODevice API。 |

## 一句话总结

`QSslSocket` 把 TCP 字节流升级为 TLS：连接成功不等于加密成功，等 `encrypted()` 才进入业务层；配置和错误处理要在握手窗口内完成，应用读写面向解密数据，而实际协议、密码套件和发送状态必须在正确的层级读取。
