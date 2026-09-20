# QSslPreSharedKeyAuthenticator

> Qt 6.11.1 | Qt6::Network | `#include <QSslPreSharedKeyAuthenticator>`

## 类解决的问题

PSK（Pre-Shared Key，预共享密钥）TLS 握手不依赖传统证书私钥，而是要求通信双方使用约定的 identity 和 PSK。`QSslPreSharedKeyAuthenticator` 是 Qt 在握手回调中提供的可写认证参数对象，用来：

- 读取服务端给客户端的 `identityHint`；
- 设置客户端要发送的 identity；
- 设置用于握手的预共享密钥；
- 读取 backend 允许的最大长度。

它不是长期保存凭据的账户对象，也不是 socket 的所有权对象。它只是在 `QSslSocket::preSharedKeyAuthenticationRequired` 或 `QSslServer::preSharedKeyAuthenticationRequired` 回调期间，承载本次握手需要的认证材料。

## 实际使用场景

### 1. 客户端响应 PSK 握手

```cpp
connect(socket, &QSslSocket::preSharedKeyAuthenticationRequired,
        this, [](QSslPreSharedKeyAuthenticator *authenticator) {
    const QByteArray hint = authenticator->identityHint();
    Q_UNUSED(hint);

    authenticator->setIdentity(QByteArrayLiteral("device-42"));
    authenticator->setPreSharedKey(loadPskForDevice());
});
```

回调返回前必须设置正确的 identity 和 PSK，否则对端无法根据相同凭据完成握手。

### 2. 服务端接收客户端 PSK

```cpp
connect(server, &QSslServer::preSharedKeyAuthenticationRequired,
        this, [](QSslSocket *socket,
                 QSslPreSharedKeyAuthenticator *authenticator) {
    Q_UNUSED(socket);
    authenticator->setPreSharedKey(findPsk(authenticator->identity()));
});
```

服务端通常根据客户端提供的 identity 查找对应的 PSK。具体的 identity 解析、账户映射和撤销策略由应用负责。

### 3. 按 backend 限制裁剪凭据

```cpp
const int maxLength = authenticator->maximumPreSharedKeyLength();
QByteArray psk = loadPsk();
psk.truncate(maxLength);
authenticator->setPreSharedKey(psk);
```

更稳妥的做法是发现凭据超过限制时拒绝本次认证或更换配置，而不是静默截断后继续使用。Qt 的 setter 会按允许长度限制发送的数据，但被截断的 PSK 很可能无法匹配服务端。

## 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(app PRIVATE Qt6::Network)
```

```cpp
#include <QSslPreSharedKeyAuthenticator>

QSslPreSharedKeyAuthenticator authenticator;
authenticator.setIdentity(QByteArrayLiteral("client"));
authenticator.setPreSharedKey(QByteArrayLiteral("secret"));
```

实际 TLS 使用中，通常不由应用自行创建并传给 socket；而是由 Qt 在 PSK 信号中提供指针。

## 关键语义与边界

### 回调内必须写入 identity 和 PSK

Qt 发出 `preSharedKeyAuthenticationRequired` 是为了让应用补齐握手凭据。只读取 `identityHint()` 而不调用 `setIdentity()` 或 `setPreSharedKey()`，通常会导致 PSK 握手失败。客户端和服务端的回调都应根据自己的角色设置必要字段。

### `identityHint` 是提示，不是密码

identity hint 通常由服务端提供，用来提示客户端选择哪个账户、租户或密钥槽位。它不应被当作 PSK，也不一定是唯一身份标识；其格式和解释完全由应用协议定义。

### 最大长度由 TLS backend 决定

`maximumIdentityLength()` 和 `maximumPreSharedKeyLength()` 报告当前握手路径允许的最大字节数。它们可能因 backend、协议版本和角色而变化。不要用固定常量代替查询结果。

### 超长输入会被 Qt 截断

Qt 文档约定：identity 或 PSK 超过最大长度时，发送内容只包含前 `maximum...Length()` 个字节。这个行为不会自动把错误变成成功；截断后的值通常不再等于双方预先约定的完整凭据。应用应在设置前验证长度，必要时明确拒绝。

### 默认对象的字段为空，长度上限为 0

默认构造对象的 hint、identity 和 preSharedKey 都为空，两个最大长度为 0。这个对象不代表一个可用的认证会话；真正回调中的对象由 Qt backend 填充上下文。

### 指针由 socket/server 所有

信号参数是 Qt 管理的指针。应用可以在同步回调中读取和修改它，但不能 `delete`，也不应在回调返回后保存并异步使用该指针。若需要延迟查找凭据，应先复制必要的 identity hint 或 identity，并在回调返回前完成 setter。

### PSK 是敏感数据

不要把 `preSharedKey()`、从凭据库读取的 PSK 或完整认证对象写进日志。使用完后尽量缩短敏感数据在内存中的生命周期，并避免在普通信号、异常文本或调试输出中泄露。

### 值语义与比较

类支持拷贝、移动和比较，适合临时保存值。但在 Qt 发出的回调里，复制 authenticator 不会复制 socket 的握手控制权；真正影响握手的是 Qt 交给回调的那个对象，应直接修改它。

## 常见误区

- 只设置 identity，不设置 PSK，或反过来：两者都要按握手角色正确设置。
- 把 `identityHint()` 当作服务端已经认可的 identity：它只是提示。
- 超过最大长度后依赖 Qt 截断：截断值通常无法完成匹配，应在应用层拒绝或修正。
- 把 authenticator 指针保存到 lambda、队列或成员变量中异步使用：它由 socket/server 临时拥有，回调后不保证有效。
- 手工 `delete` 信号提供的 authenticator：这是 Qt 管理的对象，应用不能删除。
- 把 PSK 写到日志以排查认证问题：应记录 identity、长度和错误类型，不能记录密钥本身。

## 逐项 API 说明

### 构造、赋值和交换

#### `QSslPreSharedKeyAuthenticator()`

构造空认证参数对象。默认 identity hint、identity 和 PSK 为空，最大长度均为 0；实际握手对象由 Qt backend 提供。

#### `QSslPreSharedKeyAuthenticator(const QSslPreSharedKeyAuthenticator &authenticator)`

复制认证参数值。复制的是字段状态，不是 socket 的回调上下文或握手所有权。

#### `QSslPreSharedKeyAuthenticator &operator=(const QSslPreSharedKeyAuthenticator &authenticator)`

复制赋值，替换当前字段状态。

#### `QSslPreSharedKeyAuthenticator &operator=(QSslPreSharedKeyAuthenticator &&other) noexcept`

移动赋值，转移字段状态。

#### `~QSslPreSharedKeyAuthenticator()`

销毁值对象。不要用它销毁信号中的指针；该指针由 Qt 所属 socket/server 管理。

#### `void swap(QSslPreSharedKeyAuthenticator &other) noexcept`

交换两个认证参数对象，操作快速且不抛异常。

### 服务端提示和客户端身份

#### `QByteArray identityHint() const`

返回对端提供的 identity hint。它是应用协议层的提示，可能为空，也不一定等于最终要发送的 identity。

#### `void setIdentity(const QByteArray &identity)`

设置本次握手要使用的 identity。超过 `maximumIdentityLength()` 时，Qt 只发送允许长度内的前缀；调用前应由应用验证长度和编码。

#### `QByteArray identity() const`

返回当前设置的 identity。服务端通常使用它查找 PSK，客户端通常在回调中设置它。

#### `int maximumIdentityLength() const`

返回 identity 的最大允许长度，单位为字节。默认构造对象返回 0；实际值由 backend/握手上下文提供。

### 预共享密钥

#### `void setPreSharedKey(const QByteArray &preSharedKey)`

设置本次握手使用的 PSK。超过最大长度时，Qt 会限制发送长度；应用应避免依赖这种截断行为。

#### `QByteArray preSharedKey() const`

返回当前 PSK。它是敏感数据，除非确有必要，不要复制、打印或长期保存。

#### `int maximumPreSharedKeyLength() const`

返回 PSK 的最大允许长度，单位为字节。应在设置凭据前查询并验证。

### 比较

#### `bool operator==(const QSslPreSharedKeyAuthenticator &lhs, const QSslPreSharedKeyAuthenticator &rhs)`

比较两个认证参数对象的字段值是否相等。它不比较或代表任何 socket 握手上下文。

#### `bool operator!=(const QSslPreSharedKeyAuthenticator &lhs, const QSslPreSharedKeyAuthenticator &rhs)`

返回字段值比较的反结果。

## API 速查表

| 类别 | API | 语义 | 边界与注意事项 |
| --- | --- | --- | --- |
| 构造 | `QSslPreSharedKeyAuthenticator()` | 构造空认证参数。 | 默认 hint、identity、PSK 为空，最大长度为 0。 |
| 构造 | `QSslPreSharedKeyAuthenticator(const QSslPreSharedKeyAuthenticator &authenticator)` | 复制字段值。 | 不复制 socket 的握手控制权。 |
| 赋值 | `QSslPreSharedKeyAuthenticator &operator=(const QSslPreSharedKeyAuthenticator &authenticator)` | 复制赋值。 | 覆盖当前字段。 |
| 赋值 | `QSslPreSharedKeyAuthenticator &operator=(QSslPreSharedKeyAuthenticator &&other) noexcept` | 移动赋值。 | 转移字段状态。 |
| 析构 | `~QSslPreSharedKeyAuthenticator()` | 销毁值对象。 | 不要用它删除信号中的指针。 |
| 交换 | `void swap(QSslPreSharedKeyAuthenticator &other) noexcept` | 交换两个对象。 | 快速且不抛异常。 |
| 提示 | `QByteArray identityHint() const` | 读取对端提供的 identity hint。 | 只是提示，不是密码，也不一定是最终 identity。 |
| 身份 | `void setIdentity(const QByteArray &identity)` | 设置本次握手的 identity。 | 超长时 Qt 只发送前缀，应用应先验证。 |
| 身份 | `QByteArray identity() const` | 读取当前 identity。 | 服务端可据此查找 PSK。 |
| 限制 | `int maximumIdentityLength() const` | 返回 identity 最大字节数。 | 由 backend/握手上下文决定。 |
| 密钥 | `void setPreSharedKey(const QByteArray &preSharedKey)` | 设置本次握手的 PSK。 | 超长时会被限制发送，可能导致匹配失败。 |
| 密钥 | `QByteArray preSharedKey() const` | 读取当前 PSK。 | 敏感数据，不要日志输出。 |
| 限制 | `int maximumPreSharedKeyLength() const` | 返回 PSK 最大字节数。 | 不要用固定常量替代查询。 |
| 比较 | `operator==(lhs, rhs)` | 比较字段值是否相等。 | 不代表握手上下文相同。 |
| 比较 | `operator!=(lhs, rhs)` | 判断字段值不同。 | 与相等比较相反。 |

## 一句话总结

`QSslPreSharedKeyAuthenticator` 是 PSK 握手回调里的临时可写参数：回调返回前设置正确的 identity 和 PSK，先检查 backend 给出的长度上限，并始终把 authenticator 指针和 PSK 当作临时敏感数据处理。
