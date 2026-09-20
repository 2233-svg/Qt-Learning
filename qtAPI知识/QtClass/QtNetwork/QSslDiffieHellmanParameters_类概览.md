# QSslDiffieHellmanParameters

> Qt 6.11.1 | Qt6::Network | `#include <QSslDiffieHellmanParameters>`

## 类解决的问题

传统 DH 密钥交换需要服务端提供一组参数。`QSslDiffieHellmanParameters` 封装这组参数，并负责从 PEM/DER 数据加载、判断输入是否有效，以及报告“不安全”这一类不能忽略的错误。

它只解决 DH 参数的保存和校验，不负责生成参数，也不负责执行 TLS 握手。服务端通常把它放入 `QSslConfiguration`，再交给基于 `QSslSocket` 或 `QSslServer` 的 TLS 服务。

## 实际使用场景

### 1. 使用 Qt 默认参数

```cpp
QSslConfiguration config = QSslConfiguration::defaultConfiguration();
const auto dh = QSslDiffieHellmanParameters::defaultParameters();
if (dh.isValid())
    config.setDiffieHellmanParameters(dh);
```

Qt 6.11.1 文档说明，当前默认参数是 RFC 3526 的 2048-bit MODP group。

### 2. 从 PEM 文件加载服务端参数

```cpp
QFile file("dhparams.pem");
if (!file.open(QIODevice::ReadOnly))
    return;

const auto dh =
    QSslDiffieHellmanParameters::fromEncoded(&file, QSsl::Pem);
if (!dh.isValid()) {
    qWarning() << dh.error() << dh.errorString();
    return;
}

QSslConfiguration config = QSslConfiguration::defaultConfiguration();
config.setDiffieHellmanParameters(dh);
```

### 3. 明确禁用 DH

把空的 `QSslDiffieHellmanParameters` 设置到基于 `QSslSocket` 的服务端，会禁用 DH 密钥交换。这是一个有意的策略选择，不应与“加载失败”混为一谈。

## 构建与基本模型

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(app PRIVATE Qt6::Network)
```

```cpp
#include <QFile>
#include <QSslDiffieHellmanParameters>

QFile file("dhparams.der");
file.open(QIODevice::ReadOnly);
const auto params =
    QSslDiffieHellmanParameters::fromEncoded(&file, QSsl::Der);
```

## 关键语义与边界

### 空、无效、有效是三种需要区分的状态

- `isEmpty()`：没有参数内容。将其配置到服务端会禁用 DH。
- `isValid()`：参数已成功加载且可使用。
- `error()` / `errorString()`：解释无效对象的构造失败原因。

加载失败的对象不应直接传给 TLS 服务端。尤其是 `UnsafeParametersError`，意味着参数不安全，应拒绝使用，而不是仅记录日志后继续。

### `fromEncoded(QIODevice *)` 的前置条件

`device` 不能是 `nullptr`，并且必须已经以可读模式打开；否则返回无效对象。函数从设备读取编码数据，不替设备管理生命周期，也不要求设备必须是文件。

### PEM 与 DER 必须匹配

`QSsl::Pem` 和 `QSsl::Der` 说明输入格式。格式参数错了，即使字节内容本身存在，也可能得到 `InvalidInputDataError`。

### 默认参数不是“所有平台都永远相同”

默认参数的具体实现和安全策略可能随 Qt/SSL backend 变化；当前 Qt 6.11.1 文档明确的是 2048-bit RFC 3526 MODP group。需要合规或固定参数时，应显式加载并校验部署资产。

### 生命周期、线程和所有权

这是可拷贝、隐式共享、可重入的值类型。它不拥有传入的 `QIODevice`，也不需要事件循环。移动后的对象处于部分形成状态，只能析构或重新赋值。

## 常见误区

- 只检查 `isEmpty()`，不检查 `isValid()`。
- 把 `UnsafeParametersError` 当成普通解析失败并继续启动服务。
- 传入尚未打开的 `QFile`。
- 用 PEM 数据却指定 `QSsl::Der`，或反过来。
- 认为设置空参数会“恢复默认 DH 参数”；实际语义是禁用 DH。
- 把 DH 参数和证书私钥混淆：证书/私钥负责身份认证，DH 参数负责密钥交换参数。
- 在握手开始后才修改配置并期待已建立连接改变。

## 逐项 API 说明

### 错误枚举

#### `enum Error`

| 枚举值 | 含义 |
| --- | --- |
| `NoError` | 没有错误。 |
| `InvalidInputDataError` | 输入数据不能构造有效 DH 参数对象。 |
| `UnsafeParametersError` | 参数不安全，不应使用。 |

### 构造、赋值和交换

#### `QSslDiffieHellmanParameters()`

构造空参数对象。设置到服务端配置后会禁用 DH 密钥交换。

#### `QSslDiffieHellmanParameters(const QSslDiffieHellmanParameters &other)`

复制参数对象。

#### `QSslDiffieHellmanParameters(QSslDiffieHellmanParameters &&other)`

移动构造。移动源只应析构或重新赋值。

#### `operator=`

支持复制赋值和移动赋值。

#### `~QSslDiffieHellmanParameters()`

销毁值对象，不影响 `QSslConfiguration` 中其他对象。

#### `swap(QSslDiffieHellmanParameters &other)`

快速、无异常地交换两个参数对象。

### 工厂和状态

#### `static QSslDiffieHellmanParameters defaultParameters()`

返回 Qt 当前为 `QSslSocket` 服务端使用的默认 DH 参数。Qt 6.11.1 当前为 RFC 3526 的 2048-bit MODP group。

#### `static QSslDiffieHellmanParameters fromEncoded(const QByteArray &encoded, QSsl::EncodingFormat encoding = QSsl::Pem)`

从字节数组按 PEM 或 DER 格式构造参数。返回对象后必须调用 `isValid()`。

#### `static QSslDiffieHellmanParameters fromEncoded(QIODevice *device, QSsl::EncodingFormat encoding = QSsl::Pem)`

从已打开且可读的设备读取 PEM 或 DER 数据。传入空指针或不可读设备会返回无效对象。

#### `bool isEmpty() const`

判断对象是否没有 DH 参数内容。空对象用于显式禁用服务端 DH。

#### `bool isValid() const`

判断参数是否有效。加载后应优先调用它，再根据 `error()` 做诊断。

#### `Error error() const`

返回导致对象无效的错误枚举。

#### `QString errorString() const`

返回面向人的错误说明，适合日志和诊断；程序分支应使用 `error()`。

### 相关非成员

#### `qHash`

返回参数对象的哈希值，可用于 `QHash` / `QSet`。

#### `operator==` / `operator!=`

比较两组 DH 参数是否相同。

#### `operator<<(QDebug, ...)`

向调试流写出参数的 Base64 编码 DER 表示。不要把调试输出当成安全存储格式。

## API 速查表

| 类别 | API | 语义 | 边界与注意事项 |
| --- | --- | --- | --- |
| 类型 | `enum Error` | 描述加载/安全错误。 | `UnsafeParametersError` 必须拒绝使用。 |
| 构造 | `QSslDiffieHellmanParameters()` | 构造空参数。 | 配置到服务端会禁用 DH。 |
| 构造 | `QSslDiffieHellmanParameters(const QSslDiffieHellmanParameters &other)` | 复制参数。 | 值语义。 |
| 构造 | `QSslDiffieHellmanParameters(QSslDiffieHellmanParameters &&other)` | 移动构造。 | 移动源只应析构或重新赋值。 |
| 赋值 | `operator=(const QSslDiffieHellmanParameters &other)` | 复制赋值。 | 覆盖当前对象。 |
| 赋值 | `operator=(QSslDiffieHellmanParameters &&other)` | 移动赋值。 | 移动源处于部分形成状态。 |
| 析构 | `~QSslDiffieHellmanParameters()` | 销毁对象。 | 不拥有外部设备。 |
| 交换 | `swap(QSslDiffieHellmanParameters &other) noexcept` | 交换参数。 | 快速且不抛异常。 |
| 工厂 | `static defaultParameters()` | 返回 Qt 当前默认参数。 | Qt 6.11.1 当前为 RFC 3526 2048-bit MODP。 |
| 工厂 | `static fromEncoded(const QByteArray &, QSsl::EncodingFormat)` | 从字节数组加载参数。 | PEM/DER 格式必须匹配；加载后检查有效性。 |
| 工厂 | `static fromEncoded(QIODevice *, QSsl::EncodingFormat)` | 从设备读取参数。 | 设备不能为 `nullptr`，且必须可读。 |
| 状态 | `bool isEmpty() const` | 判断是否为空。 | 空值用于禁用 DH，不等于加载成功。 |
| 状态 | `bool isValid() const` | 判断参数是否可用。 | 失败后结合 `error()` 诊断。 |
| 错误 | `Error error() const` | 返回机器可判断的错误。 | 程序分支使用枚举。 |
| 错误 | `QString errorString() const` | 返回人类可读错误。 | 用于日志，不替代枚举。 |
| 哈希 | `qHash(const QSslDiffieHellmanParameters &, size_t seed = 0)` | 计算哈希值。 | 可作为 `QHash` 键。 |
| 比较 | `operator==` / `operator!=` | 比较参数对象。 | 不是比较错误字符串。 |
| 调试 | `operator<<(QDebug, ...)` | 输出 Base64 DER 调试表示。 | 不应当作安全持久化格式。 |

## 一句话总结

`QSslDiffieHellmanParameters` 管理服务端 DH 参数：加载后先判 `isValid()`，严肃处理 `UnsafeParametersError`，并明确区分“空参数导致禁用 DH”和“参数加载失败”。
