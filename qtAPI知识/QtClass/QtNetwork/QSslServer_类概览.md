# QSslServer

> Qt 6.11.1 | Qt6::Network | `#include <QSslServer>`

## 类解决的问题

`QSslServer` 是带 TLS 握手流程的 TCP 服务器。它继承 `QTcpServer`，负责：

- 监听 TCP 地址和端口；
- 接受原生 TCP 连接并创建 `QSslSocket`；
- 使用服务端 `QSslConfiguration` 启动 TLS 握手；
- 只有握手成功后，才把 socket 放入 pending connection 队列；
- 转发证书错误、对端验证错误、PSK 回调、TLS alert 和握手中断信号。

它把“监听连接”和“把明文 TCP 升级为安全 TLS 连接”连接起来，但不负责业务协议、用户认证数据库或 HTTP 处理。应用仍需从 `nextPendingConnection()` 取出 `QSslSocket` 并处理其读写。

## 实际使用场景

### 1. 最小 TLS 服务端

```cpp
auto *server = new QSslServer(this);

QSslConfiguration configuration =
    QSslConfiguration::defaultConfiguration();
configuration.setLocalCertificateChain(serverChain);
configuration.setPrivateKey(serverKey);
configuration.setPeerVerifyMode(QSslSocket::VerifyNone);
server->setSslConfiguration(configuration);

connect(server, &QTcpServer::newConnection, this, [server] {
    while (server->hasPendingConnections()) {
        auto *socket = qobject_cast<QSslSocket *>(
            server->nextPendingConnection());
        if (!socket) {
            continue;
        }

        connect(socket, &QSslSocket::readyRead, socket, [socket] {
            socket->write(makeResponse(socket->readAll()));
        });
        connect(socket, &QAbstractSocket::disconnected,
                socket, &QObject::deleteLater);
    }
});

if (!server->listen(QHostAddress::Any, 8443)) {
    qWarning() << server->errorString();
}
```

必须先配置证书和私钥，再调用 `listen()`。`QSslServer` 会在收到 TCP 连接后启动服务端握手，业务层不应把 pending socket 当成已连接明文 socket 来提前使用。

### 2. 双向 TLS

```cpp
configuration.setCaCertificates(clientCaCertificates);
configuration.setPeerVerifyMode(QSslSocket::VerifyPeer);
configuration.setPeerVerifyDepth(3);
```

服务端要求客户端证书时，应配置用于验证客户端的 CA，并明确设置 `VerifyPeer`。握手成功的 socket 才会进入 pending queue；客户端没有证书或证书链不可信时，通常会在握手阶段失败。

### 3. 服务端 PSK

```cpp
connect(server, &QSslServer::preSharedKeyAuthenticationRequired,
        this, [](QSslSocket *socket,
                 QSslPreSharedKeyAuthenticator *authenticator) {
    Q_UNUSED(socket);
    authenticator->setPreSharedKey(
        lookupPsk(authenticator->identity()));
});
```

PSK 回调中的 authenticator 由 Qt 临时管理。应在信号处理期间完成 identity/PSK 设置，不能保存指针后异步处理。

## 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(app PRIVATE Qt6::Network)
```

```cpp
#include <QSslServer>

auto *server = new QSslServer;
server->setSslConfiguration(configuration);
server->setHandshakeTimeout(5000);
server->listen(QHostAddress::Any, 443);
```

构建必须包含 SSL 能力和 Qt Network。具体证书格式、backend 和平台支持仍要在目标运行环境验证。

## 关键语义与边界

### 必须在 `listen()` 前设置 SSL 配置

`setSslConfiguration()` 适合在服务器开始监听前调用。服务器接受连接后，会用当前配置初始化新建的 `QSslSocket`。监听后再修改配置，通常只影响之后接受的连接；已经开始握手或已经入队的 socket 不会被重新配置。

为避免连接在旧配置和新配置之间出现不确定行为，生产代码应在配置完成后再 `listen()`，修改证书或私钥时可先关闭监听、更新配置，再重新监听。

### 只有 TLS 成功的 socket 才进入 pending queue

与普通 `QTcpServer` 不同，`QSslServer` 收到 TCP 连接后先执行服务端 TLS 握手。只有加密握手成功，socket 才能通过 `nextPendingConnection()` 取出。`newConnection()` 因而表示“有可交付的加密连接”，而不是“有一个刚建立的明文 TCP 连接”。

握手失败的 socket 不应被业务层继续读写；失败原因通过 `sslErrors`、`peerVerifyError`、`errorOccurred` 或 socket 自身信号诊断。

### 默认握手超时是 5000 ms

`handshakeTimeout()` 默认值为 5000 毫秒。它只约束新接受连接的 TLS 握手阶段；修改超时不会改变已经在握手中的连接。超时过小会误伤慢客户端，过大则会让半连接长期占用资源。

超时不是 TCP accept backlog，也不是业务请求超时。TLS 成功后，应用仍需自己设置业务层读写和空闲超时。

### pending socket 的所有权

`nextPendingConnection()` 返回的 socket 是由 server 作为父对象管理的。应用取出后负责在适当时机销毁，常见做法是把 `disconnected()` 连接到 `deleteLater()`。若 socket 仍留在 pending queue 中，server 析构时会按 QObject 父子关系处理它。

不要手动删除仍由 server 内部流程使用的 socket，也不要把 socket 指针交给另一个线程直接读写。跨线程服务应在 `incomingConnection()` 层传递原生 descriptor，并在目标线程创建 socket；但要注意 `QSslServer` 的 TLS 启动流程和线程归属。

### 握手错误信号的处理必须及时

`sslErrors(QSslSocket *, ...)` 与 socket 的 `sslErrors()` 类似：若应用决定允许特定错误继续，应在对应信号处理期间对该 socket 调用 `ignoreSslErrors()`。使用 queued connection 或把决定延迟到之后，通常已经错过 backend 要求的握手窗口。

`handshakeInterruptedOnError` 需要在同步槽中调用 socket 的 `continueInterruptedHandshake()`。不要在回调返回后保存 socket 的临时握手上下文来异步恢复。

### 忽略错误是信任策略，不是恢复按钮

`sslErrors` 中调用 `ignoreSslErrors()` 会绕过某些证书验证错误。无条件忽略会使中间人、过期证书、主机名不匹配或撤销证书进入业务层。若确有内部测试例外，应按固定错误集合、预期证书指纹和明确环境限定。

### PSK authenticator 指针不归应用

`preSharedKeyAuthenticationRequired` 提供的 `QSslPreSharedKeyAuthenticator *` 由 Qt/socket 管理。应用只能在同步回调内读取和修改它，不能 `delete`、保存或异步使用。PSK 是敏感数据，日志中只记录 identity 或长度，不要记录密钥内容。

### TLS alert 主要用于诊断

`alertSent` 和 `alertReceived` 反映 TLS alert。并非所有 backend 都会产生相同的 alert 细节；信号适合诊断和统计，不应作为唯一的连接状态来源。连接是否可用仍看 socket 状态、`encrypted()`、错误信号和断开信号。

### `incomingConnection()` 的扩展边界

`QSslServer::incomingConnection(qintptr)` 会把 descriptor 交给 `QSslSocket` 并启动服务端握手。派生类如果重写此函数，必须保留：

- descriptor 的有效性和所有权转移；
- socket 的线程归属；
- TLS 配置和握手启动；
- 成功后调用 `addPendingConnection()`；
- 失败时正确清理 socket。

如果只是处理普通 TLS 服务，不需要重写它。若要自定义线程模型、连接限流或 socket 子类，必须完整理解 `QTcpServer` 的 pending queue 机制。

## 常见误区

- 先 `listen()` 再设置证书和私钥：新连接可能在错误配置下开始握手。
- 把 `newConnection()` 当成 TCP accept 完成：`QSslServer` 只有 TLS 成功后才把 socket 放入 pending queue。
- 只连接 `newConnection()` 却不循环取完 pending socket：高负载时会留下已握手连接。
- 把默认 5000 ms 当成业务请求超时：它只针对新连接的 TLS 握手。
- 从 pending queue 取出 socket 后忘记安排销毁：长期服务会积累已断开对象。
- 在 `sslErrors` 中无条件忽略所有错误：这会绕过证书信任策略。
- 用 queued 槽处理握手中断或 SSL 错误：可能错过同步恢复窗口。
- 删除或保存 PSK authenticator 指针：它由 Qt 临时管理。
- 重写 `incomingConnection()` 却遗漏 `addPendingConnection()`：`nextPendingConnection()` 将取不到自定义 socket。
- 把 TLS alert 当成完整连接状态：alert 支持和细节受 backend 影响。

## 逐项 API 说明

### 构造、析构和配置

#### `explicit QSslServer(QObject *parent = nullptr)`

构造 TLS 服务器对象。parent 决定 QObject 所有权和线程归属；构造本身不监听、不创建 TLS socket。

#### `~QSslServer() override`

销毁服务器对象并释放其监听资源和仍由 QObject 父子关系管理的子对象。已取出的 socket 若已改变 parent 或由应用接管，生命周期应由应用负责。

#### `void setSslConfiguration(const QSslConfiguration &sslConfiguration)`

设置新接受连接使用的 TLS 配置。应在 `listen()` 前完成；已开始握手的 socket 不会因修改配置而重启。

#### `QSslConfiguration sslConfiguration() const`

返回当前服务器 TLS 配置的值副本。修改返回值不会自动修改 server，必须再次调用 setter。

#### `void setHandshakeTimeout(int timeout)`

设置新连接 TLS 握手的超时毫秒数。通常应传非负值；修改不追溯已经开始握手的连接。

#### `int handshakeTimeout() const`

返回当前握手超时配置，默认是 5000 ms。

### 连接接收扩展点

#### `void incomingConnection(qintptr socket)`

新 TCP 连接到达时的保护重写点。默认实现将 descriptor 包装成 `QSslSocket`、应用服务端配置并开始 TLS 握手；只有握手成功后才把 socket 放入 pending queue。

重写时必须自行保持 socket 的所有权、配置、握手启动、错误清理和 pending queue 语义。没有定制需求时不要重写。

### 信号

#### `void sslErrors(QSslSocket *socket, const QList<QSslError> &errors)`

报告指定服务端 socket 的 SSL/TLS 错误列表。若策略允许继续，应在同步槽中对 `socket` 调用 `ignoreSslErrors()` 或按错误列表调用重载；不要把它当作无条件放行通知。

#### `void peerVerifyError(QSslSocket *socket, const QSslError &error)`

报告对端证书验证中的单个错误。它适合诊断和策略记录；是否继续仍受验证模式、`sslErrors` 及应用策略控制。

#### `void errorOccurred(QSslSocket *socket, QAbstractSocket::SocketError error)`

报告指定 socket 的网络或 TLS 相关错误。应结合 socket 的 `errorString()`、SSL 错误和连接状态排查。

#### `void preSharedKeyAuthenticationRequired(QSslSocket *socket, QSslPreSharedKeyAuthenticator *authenticator)`

要求应用提供 PSK 认证材料。回调返回前设置 identity/PSK；authenticator 指针由 Qt 管理，不能保存或删除。

#### `void alertSent(QSslSocket *socket, QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`

报告发送的 TLS alert。适合诊断；支持和文本细节依赖 backend。

#### `void alertReceived(QSslSocket *socket, QSsl::AlertLevel level, QSsl::AlertType type, const QString &description)`

报告收到的 TLS alert。它不等价于 socket 已断开，也不保证所有 backend 都提供完整信息。

#### `void handshakeInterruptedOnError(QSslSocket *socket, const QSslError &error)`

当配置要求在可恢复错误处中断握手时报告错误。若要继续，必须在同步处理期间调用 `socket->continueInterruptedHandshake()`。

#### `void startedEncryptionHandshake(QSslSocket *socket)`

报告该 socket 开始服务端加密握手。它早于握手成功；此时不能把 socket 当成已加密连接使用。

## API 速查表

| 类别 | API | 语义 | 边界与注意事项 |
| --- | --- | --- | --- |
| 构造 | `QSslServer(QObject *parent = nullptr)` | 创建 TLS 服务器。 | 不自动监听；parent 决定所有权和线程。 |
| 生命周期 | `~QSslServer()` | 销毁服务器和其管理资源。 | 已取出的 socket 生命周期由应用确认。 |
| 配置 | `setSslConfiguration(...)` | 设置新连接的 TLS 配置。 | 应在 `listen()` 前调用。 |
| 配置 | `sslConfiguration()` | 获取配置副本。 | 修改副本不会自动回写。 |
| 超时 | `setHandshakeTimeout(int)` | 设置新连接握手超时。 | 默认 5000 ms；不影响已握手连接。 |
| 超时 | `handshakeTimeout()` | 读取握手超时。 | 不是业务读写超时。 |
| 扩展 | `incomingConnection(qintptr)` | 接收 descriptor 并启动 TLS。 | 重写时要保留所有权、握手和 pending 语义。 |
| 信号 | `sslErrors(socket, errors)` | 报告 SSL 错误列表。 | 允许例外时同步调用 `ignoreSslErrors()`。 |
| 信号 | `peerVerifyError(socket, error)` | 报告对端证书验证错误。 | 不等于自动终止或自动放行。 |
| 信号 | `errorOccurred(socket, error)` | 报告 socket 错误。 | 配合 socket 的错误文本和状态排查。 |
| 信号 | `preSharedKeyAuthenticationRequired(...)` | 请求提供 PSK。 | authenticator 只在同步回调中有效。 |
| 信号 | `alertSent(...)` | 报告发送 TLS alert。 | 主要诊断用途，backend 支持有差异。 |
| 信号 | `alertReceived(...)` | 报告接收 TLS alert。 | 不等价于完整连接状态。 |
| 信号 | `handshakeInterruptedOnError(...)` | 报告可恢复握手中断。 | 继续需同步调用 `continueInterruptedHandshake()`。 |
| 信号 | `startedEncryptionHandshake(socket)` | 报告开始服务端 TLS 握手。 | 此时尚未加密成功。 |
| 继承 | `listen()` / `newConnection()` / `nextPendingConnection()` | 继承 TCP 监听和 pending 队列。 | pending 中只有 TLS 成功的连接。 |
| 继承 | `hasPendingConnections()` | 查询可交付的已握手连接。 | 槽中应循环取完。 |

## 一句话总结

`QSslServer` 把 TCP accept 和服务端 TLS 握手串起来：先配置再监听，只有握手成功的 `QSslSocket` 才进入 pending queue，错误/PSK/中断回调必须按同步窗口处理，而取出的 socket 生命周期由应用负责。
