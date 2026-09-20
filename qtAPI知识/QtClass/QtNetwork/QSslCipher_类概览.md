# QSslCipher

> Qt 6.11.1 | Qt6::Network | `#include <QSslCipher>`

## 类解决的问题

TLS 连接最终会选定一个密码套件。密码套件同时描述密钥交换、身份认证、对称加密、协议版本和密钥位数。`QSslCipher` 是这个“密码套件描述”的值对象，用来：

- 从名称构造一个待配置的密码套件；
- 查询 SSL backend 支持的密码套件属性；
- 配置 `QSslConfiguration` 的密码套件优先级；
- 在握手完成后展示实际协商结果。

它不代表一个正在运行的连接，也不保存 socket 状态。连接的实际协商结果应从 `QSslSocket::sessionCipher()` 或 `QSslConfiguration::sessionCipher()` 读取。

## 实际使用场景

### 1. 查看 backend 支持的套件

```cpp
for (const QSslCipher &cipher : QSslSocket::supportedCiphers()) {
    qDebug() << cipher.name()
             << cipher.protocolString()
             << cipher.keyExchangeMethod()
             << cipher.encryptionMethod()
             << cipher.usedBits();
}
```

### 2. 配置密码套件顺序

```cpp
QSslConfiguration config = QSslConfiguration::defaultConfiguration();
QList<QSslCipher> ciphers = config.ciphers();
// 对 ciphers 做明确的筛选和排序后：
config.setCiphers(ciphers);
```

传给 `setCiphers()` 的列表应来自 `supportedCiphers()` 或当前配置的 `ciphers()`，并按希望的协商优先级排列。

### 3. 记录真实会话参数

```cpp
connect(socket, &QSslSocket::encrypted, this, [socket] {
    const QSslCipher cipher = socket->sessionCipher();
    qInfo() << cipher.name()
            << cipher.protocolString()
            << cipher.usedBits();
});
```

## 构建与基本模型

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(app PRIVATE Qt6::Network)
```

```cpp
#include <QSslCipher>
#include <QSslSocket>

QSslCipher cipher(QStringLiteral("TLS_AES_256_GCM_SHA384"));
if (!cipher.isNull()) {
    // 这个名称被当前 backend 识别为受支持密码套件。
}
```

## 关键语义与边界

### 空对象是“无效 cipher”

默认构造对象是空 cipher。用不受支持的名称，或名称与协议不匹配的构造方式，也会得到可通过 `isNull()` 识别的无效对象。无效对象的 `name()` 返回空字符串。

### 构造函数不会接受任意字符串

`QSslCipher(const QString &name)` 只接受当前 `QSslSocket::supportedCiphers()` 中的受支持套件名称。带协议的重载要求名称和 `QSsl::SslProtocol` 共同标识一个受支持套件。不要把 IANA 名称、OpenSSL 名称或配置文件中的名称混用而不做验证。

### supportedBits 与 usedBits 不同

`supportedBits()` 是套件支持的位数，`usedBits()` 是该套件实际使用的位数。两者可能不同，安全审计和展示时不要只看其中一个；同时还要关注协议、认证算法和 backend 的实际策略。

### protocol 可能是 UnknownProtocol

`protocol()` 返回枚举协议；如果对象无法确定协议，会返回 `QSsl::UnknownProtocol`。此时 `protocolString()` 可能包含更多后端提供的信息。

### 配置对象与会话对象不是一回事

`QSslConfiguration::ciphers()` 表示允许使用的候选列表；`sessionCipher()` 才是握手后实际选中的套件。握手前查询 session cipher 得到空或无效对象是正常的。

### 生命周期和线程

这是可拷贝、隐式共享、可重入的值类型，不需要事件循环，也不拥有 socket。复制不会复制一个网络会话。

## 常见误区

- 把 `QSslCipher` 当成加密器，直接用它进行数据加解密。
- 把 `supportedBits()` 当成当前连接真正使用的密钥位数。
- 配置了 `ciphers()` 后误以为服务器一定会选择列表第一项；最终选择仍取决于双方能力、协议和 backend 策略。
- 把 `sessionCipher()` 在 `encrypted()` 之前的空结果当成握手错误。
- 用不受支持的字符串构造后不检查 `isNull()`。
- 只记录套件名称，不记录 `protocolString()`、认证方式和实际位数，导致排障信息不足。

## 逐项 API 说明

### 构造、赋值和交换

#### `QSslCipher()`

构造空 cipher。

#### `explicit QSslCipher(const QString &name)`

按名称构造受支持的密码套件。名称不在当前 backend 支持列表中时，结果为空，应立即检查 `isNull()`。

#### `QSslCipher(const QString &name, QSsl::SslProtocol protocol)`

按名称和协议构造密码套件；二者必须共同匹配受支持套件。

#### `QSslCipher(const QSslCipher &other)`

复制密码套件描述。

#### `operator=(const QSslCipher &other)` / `operator=(QSslCipher &&other)`

执行复制或移动赋值。移动源只应析构或重新赋值。

#### `~QSslCipher()`

销毁值对象，不影响任何 socket 或 SSL 会话。

#### `swap(QSslCipher &other)`

快速、无异常地交换两个 cipher。

### 状态和属性

#### `bool isNull() const`

返回对象是否为空/无效。

#### `QString name() const`

返回密码套件名称；空 cipher 返回空字符串。

#### `QSsl::SslProtocol protocol() const`

返回协议枚举；无法确定时返回 `QSsl::UnknownProtocol`。

#### `QString protocolString() const`

返回 backend 提供的协议字符串，必要时可补充枚举无法表达的协议细节。

#### `QString keyExchangeMethod() const`

返回密钥交换方法名称。

#### `QString authenticationMethod() const`

返回身份认证方法名称。

#### `QString encryptionMethod() const`

返回对称加密方法名称。

#### `int supportedBits() const`

返回密码套件支持的位数。

#### `int usedBits() const`

返回密码套件实际使用的位数。

### 比较

`operator==` 和 `operator!=` 比较两个密码套件是否相同，适合检查配置列表或会话结果。

## API 速查表

| 类别 | API | 语义 | 边界与注意事项 |
| --- | --- | --- | --- |
| 构造 | `QSslCipher()` | 构造空 cipher。 | `isNull()` 为 `true`。 |
| 构造 | `explicit QSslCipher(const QString &name)` | 按名称查找受支持套件。 | 名称不支持时得到空对象。 |
| 构造 | `QSslCipher(const QString &name, QSsl::SslProtocol protocol)` | 按名称和协议查找套件。 | 两者必须共同匹配 supported 列表。 |
| 构造 | `QSslCipher(const QSslCipher &other)` | 复制套件描述。 | 不复制运行中的 SSL 会话。 |
| 赋值 | `QSslCipher &operator=(const QSslCipher &other)` | 复制赋值。 | 覆盖当前对象。 |
| 赋值 | `QSslCipher &operator=(QSslCipher &&other)` | 移动赋值。 | 移动源只应析构或重新赋值。 |
| 析构 | `~QSslCipher()` | 销毁值对象。 | 不影响 socket。 |
| 交换 | `void swap(QSslCipher &other) noexcept` | 交换两个对象。 | 快速且不抛异常。 |
| 状态 | `bool isNull() const` | 判断是否为空/无效。 | 解析名称后必须检查。 |
| 标识 | `QString name() const` | 返回套件名称。 | 空 cipher 返回空字符串。 |
| 协议 | `QSsl::SslProtocol protocol() const` | 返回协议枚举。 | 不确定时为 `UnknownProtocol`。 |
| 协议 | `QString protocolString() const` | 返回协议字符串。 | 可能比枚举提供更多信息。 |
| 密钥交换 | `QString keyExchangeMethod() const` | 返回密钥交换方法。 | 用于诊断和审计。 |
| 认证 | `QString authenticationMethod() const` | 返回身份认证方法。 | 不要只看加密算法。 |
| 加密 | `QString encryptionMethod() const` | 返回对称加密方法。 | 描述套件，不执行加解密。 |
| 强度 | `int supportedBits() const` | 返回支持位数。 | 不一定等于实际使用位数。 |
| 强度 | `int usedBits() const` | 返回实际使用位数。 | 结合会话套件读取。 |
| 比较 | `operator==(const QSslCipher &other) const` | 判断两个套件是否相同。 | 可用于列表筛选。 |
| 比较 | `operator!=(const QSslCipher &other) const` | 判断两个套件是否不同。 | 与 `operator==` 相反。 |

## 一句话总结

`QSslCipher` 只描述一个 TLS 密码套件；配置看候选列表，真实连接看 `sessionCipher()`，强度判断同时看 `supportedBits()` 和 `usedBits()`。
