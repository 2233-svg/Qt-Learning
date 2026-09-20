# QSslKey

> Qt 6.11.1 | Qt6::Network | `#include <QSslKey>`

## 类解决的问题

TLS 连接需要使用公钥或私钥完成身份认证、密钥交换或签名。密钥可能来自 PEM/DER 字节、文件设备，也可能已经由 OpenSSL 等底层库创建。`QSslKey` 把这些密钥统一包装成 Qt 的值类型，负责：

- 从 PEM 或 DER 数据解析公钥/私钥；
- 从 `QIODevice` 读取密钥；
- 查询密钥类型、算法和位数；
- 导出为 PEM 或 DER；
- 在需要时把 Qt 对象交给 `QSslSocket`、`QSslConfiguration` 或底层 SSL backend。

它不是密码学运算器，也不是证书。应用通常把它作为“密钥材料”传给 `QSslSocket::setPrivateKey()`，而不是直接用它执行签名或加解密。

## 实际使用场景

### 1. 从 PEM 私钥配置 TLS 服务端

```cpp
QFile file(QStringLiteral("server.key"));
if (!file.open(QIODevice::ReadOnly)) {
    return;
}

const QSslKey key(&file, QSsl::Rsa, QSsl::Pem, QSsl::PrivateKey,
                  QByteArrayLiteral("secret"));
if (key.isNull()) {
    return;
}

QSslConfiguration config = QSslConfiguration::defaultConfiguration();
config.setPrivateKey(key);
```

构造成功只表示密钥数据能被当前 backend 解析；还要确认它与本地证书匹配，并在握手前完成配置。

### 2. 导出密钥并选择保护方式

```cpp
const QByteArray pem = key.toPem(QByteArrayLiteral("new-passphrase"));
const QByteArray der = key.toDer(); // DER 不提供加密语义
```

私钥导出前应明确存储权限、口令来源和内存暴露风险。DER 的 passphrase 参数没有加密效果，应省略。

### 3. 接收 native SSL key

```cpp
Qt::HANDLE nativeHandle = /* 由底层库创建的有效 key */;
QSslKey key(nativeHandle, QSsl::PrivateKey);
```

这种方式只适合明确依赖某个平台/backend 的代码。构造后所有权转给 `QSslKey`，原生库一侧不能继续释放同一个句柄。

## 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(app PRIVATE Qt6::Network)
```

```cpp
#include <QFile>
#include <QSslKey>

QFile file(QStringLiteral("client.key"));
if (file.open(QIODevice::ReadOnly)) {
    const QSslKey key(&file, QSsl::Rsa, QSsl::Pem);
    if (!key.isNull()) {
        qInfo() << key.type() << key.algorithm() << key.length();
    }
}
```

## 关键语义与边界

### 默认类型是私钥，但默认对象仍然是空的

无参构造得到 null key。带数据的构造函数默认 `type` 为 `QSsl::PrivateKey`，但“默认类型”不等于“已经包含有效私钥”。始终用 `isNull()` 判断解析是否成功。

### 算法、编码和类型必须与输入匹配

从 `QByteArray` 或 `QIODevice` 构造时，需要指定 `QSsl::KeyAlgorithm`、`QSsl::EncodingFormat` 和 `QSsl::KeyType`。指定错误的算法、把 DER 当 PEM，或把公钥当私钥解析，都可能得到 null key。加密私钥还需要提供正确的 passphrase。

### `length()` 的单位是位

`length()` 返回密钥长度的 bit 数，不是字节数。null key 返回 `-1`，所以不要直接把结果转换成无符号整数，也不要把它当作序列化数据长度。

### PEM 可以加密，DER 不可以

`toPem(passPhrase)` 在对象是私钥且口令非空时，会导出加密 PEM；公钥不会因此获得私钥式保护。`toDer()` 返回 DER 编码，Qt 文档明确说明 DER 不能加密，passphrase 参数只是兼容性遗留接口，未来版本可能移除。

### native handle 会发生所有权转移

`QSslKey(Qt::HANDLE handle, ...)` 要求传入有效 native key。Qt 接管该 key 的所有权，应用不得再调用底层库释放函数。`handle()` 返回的是指向 native key 的句柄或 `nullptr`，用于扩展信息查询；它高度平台相关，并且可能在不同平台和 Qt 小版本间变化。

### 复制是值语义，但不等于获得第二个 native key

`QSslKey` 是可拷贝的共享值类型。复制对象适合在 Qt API 之间传递；应用不应根据复制次数去管理 native handle，也不应把 `handle()` 返回值当成自己拥有的资源。

### 私钥属于敏感数据

私钥、解密口令和 `toPem()`/`toDer()` 返回的字节数组都可能暴露密钥材料。避免用 `qDebug()` 输出，不要写入普通日志或临时文件；保存到磁盘时要使用合适的访问权限和生命周期。

## 常见误区

- 只判断构造函数没有抛异常，就认为 key 有效：Qt 通常通过 `isNull()` 报告解析失败。
- 把 `length()` 当成字节数：它返回 bit 数，null key 返回 `-1`。
- 对 `toDer()` 传入口令并以为 DER 已加密：DER 不支持加密。
- 从 native handle 构造后仍由 OpenSSL/其他库释放：这会造成重复释放。
- 认为 `QSslKey` 能验证证书与私钥是否匹配：匹配检查应结合证书/backend 或实际 TLS 配置验证。
- 把 `handle()` 当作跨平台稳定 API：它只能用于受控的 backend 专用代码。

## 逐项 API 说明

### 构造、赋值和交换

#### `QSslKey()`

构造 null key。对象默认类型语义为私钥，但不包含可用密钥材料；使用前调用 `isNull()`。

#### `QSslKey(const QByteArray &encoded, QSsl::KeyAlgorithm algorithm, QSsl::EncodingFormat format = QSsl::Pem, QSsl::KeyType type = QSsl::PrivateKey, const QByteArray &passPhrase = QByteArray())`

从字节数组解析密钥。`algorithm` 指定 RSA、DSA、EC 等算法，`format` 指定 PEM 或 DER，`type` 指定公钥或私钥；加密私钥需要正确的 `passPhrase`。解析失败时得到 null key。

#### `QSslKey(QIODevice *device, QSsl::KeyAlgorithm algorithm, QSsl::EncodingFormat format = QSsl::Pem, QSsl::KeyType type = QSsl::PrivateKey, const QByteArray &passPhrase = QByteArray())`

从设备读取并解析密钥。设备应提供可读数据，设备的打开状态、当前位置和可读内容都会影响结果。构造后设备仍由调用方拥有，`QSslKey` 不负责删除它。

#### `explicit QSslKey(Qt::HANDLE handle, QSsl::KeyType type = QSsl::PrivateKey)`

用有效 native key 构造对象，并把该 key 的所有权转给 `QSslKey`。`type` 必须与句柄实际代表的公钥或私钥一致；句柄无效或 backend 不兼容时结果不可用。

#### `QSslKey(const QSslKey &other)`

复制密钥值对象。复制后可以独立传给 Qt API，但不应由应用按对象数量管理底层句柄。

#### `QSslKey(QSslKey &&other) noexcept`

移动构造。移动后的源对象只应析构或重新赋值，不应继续依赖其原内容。

#### `QSslKey &operator=(const QSslKey &other)`

复制赋值，替换当前对象中的密钥。

#### `QSslKey &operator=(QSslKey &&other) noexcept`

移动赋值，转移值对象状态。

#### `~QSslKey()`

销毁对象；如果对象持有 native key，Qt 按其所有权规则释放该 key。

#### `void swap(QSslKey &other) noexcept`

交换两个 key 对象，操作快速且不抛异常。

### 状态和属性

#### `bool isNull() const`

返回是否为 null key。解析输入、读取加密私钥或接收 native handle 后，都应以它作为有效性检查。

#### `void clear()`

清空密钥内容，使对象恢复为 null key。清空后 `length()` 返回 `-1`，`handle()` 返回 `nullptr`。

#### `int length() const`

返回密钥长度，单位为 bit；null key 返回 `-1`。

#### `QSsl::KeyType type() const`

返回公钥或私钥类型。对 null key 不应把默认类型当成“已有有效密钥”。

#### `QSsl::KeyAlgorithm algorithm() const`

返回密钥算法。它描述密钥材料的算法类别，不是密码套件或 TLS 协议版本。

#### `Qt::HANDLE handle() const`

返回 native key 句柄；不存在时返回 `nullptr`。只适合与明确匹配的底层 API 配合，返回值不跨平台稳定，也不转移所有权。

### 序列化

#### `QByteArray toPem(const QByteArray &passPhrase = QByteArray()) const`

以 PEM 格式导出。对象是私钥且 `passPhrase` 非空时，结果会使用口令加密；空 key 通常无法导出有效材料。

#### `QByteArray toDer(const QByteArray &passPhrase = QByteArray()) const`

以 DER 格式导出。DER 不能加密，调用时应省略 passphrase；该参数保留是为了兼容旧接口，未来可能删除。

### 比较

#### `bool operator==(const QSslKey &key) const`

比较两个 key 是否相同。它适合比较值对象，不应把结果理解为“适用于某个证书”或“在所有 backend 上具有相同内部表示”。

#### `bool operator!=(const QSslKey &key) const`

返回 `operator==` 的反结果。

## API 速查表

| 类别 | API | 语义 | 边界与注意事项 |
| --- | --- | --- | --- |
| 构造 | `QSslKey()` | 构造 null key。 | 默认类型语义为私钥，但没有有效密钥材料。 |
| 构造 | `QSslKey(const QByteArray &encoded, QSsl::KeyAlgorithm algorithm, QSsl::EncodingFormat format = QSsl::Pem, QSsl::KeyType type = QSsl::PrivateKey, const QByteArray &passPhrase = QByteArray())` | 从字节解析 PEM/DER 密钥。 | 算法、编码、类型必须匹配；加密私钥需口令。 |
| 构造 | `QSslKey(QIODevice *device, QSsl::KeyAlgorithm algorithm, QSsl::EncodingFormat format = QSsl::Pem, QSsl::KeyType type = QSsl::PrivateKey, const QByteArray &passPhrase = QByteArray())` | 从设备读取并解析密钥。 | 设备由调用方拥有并负责打开。 |
| 构造 | `explicit QSslKey(Qt::HANDLE handle, QSsl::KeyType type = QSsl::PrivateKey)` | 包装 native key。 | 所有权转给 `QSslKey`，原库不得再次释放。 |
| 构造 | `QSslKey(const QSslKey &other)` | 复制 key 值。 | 不按复制次数管理 native 句柄。 |
| 构造 | `QSslKey(QSslKey &&other) noexcept` | 移动构造。 | 移动源只应析构或重新赋值。 |
| 赋值 | `QSslKey &operator=(const QSslKey &other)` | 复制赋值。 | 覆盖当前密钥。 |
| 赋值 | `QSslKey &operator=(QSslKey &&other) noexcept` | 移动赋值。 | 转移值对象状态。 |
| 析构 | `~QSslKey()` | 销毁 key。 | Qt 管理其持有的 native key。 |
| 交换 | `void swap(QSslKey &other) noexcept` | 交换两个 key。 | 快速且不抛异常。 |
| 状态 | `bool isNull() const` | 判断是否有有效密钥材料。 | 解析失败、清空后为 `true`。 |
| 状态 | `void clear()` | 清空密钥。 | 清空后长度为 `-1`，句柄为空。 |
| 属性 | `int length() const` | 返回密钥位数。 | null key 返回 `-1`，不是字节数。 |
| 属性 | `QSsl::KeyType type() const` | 返回公钥/私钥类型。 | 默认类型不代表 key 有效。 |
| 属性 | `QSsl::KeyAlgorithm algorithm() const` | 返回密钥算法。 | 不等于 TLS 密码套件。 |
| 原生互操作 | `Qt::HANDLE handle() const` | 返回 native key 句柄。 | 高度平台/backend 相关，不转移所有权。 |
| 导出 | `QByteArray toPem(const QByteArray &passPhrase = QByteArray()) const` | 导出 PEM。 | 非空口令只对私钥产生加密 PEM。 |
| 导出 | `QByteArray toDer(const QByteArray &passPhrase = QByteArray()) const` | 导出 DER。 | DER 不支持加密，应省略口令参数。 |
| 比较 | `bool operator==(const QSslKey &key) const` | 比较两个 key。 | 只比较值，不验证证书匹配。 |
| 比较 | `bool operator!=(const QSslKey &key) const` | 判断两个 key 不同。 | 与 `operator==` 相反。 |

## 一句话总结

`QSslKey` 是 TLS 公钥/私钥材料的 Qt 包装：解析后先用 `isNull()` 验证，导出时区分 PEM 加密和 DER 不加密，接收 native handle 时牢记所有权已经交给 Qt。
