# QSslCertificateExtension

> Qt 6.11.1 | Qt6::Network | `#include <QSslCertificateExtension>`

## 类解决的问题

X.509 证书不是只有主题、颁发者和有效期，还包含一组扩展字段，例如主题备用名称、密钥用途、基本约束等。`QSslCertificateExtension` 是 Qt 对“一个证书扩展”的只读值对象封装，用来查看：

- 扩展的 ASN.1 OID；
- Qt 或 SSL 后端认识的扩展名称；
- 扩展是否是 critical；
- 扩展值被解码成的 `QVariant`；
- 当前 Qt 版本是否承诺这个 `QVariant` 的结构保持稳定。

它通常不是应用主动创建扩展的编辑器。Qt 通过 `QSslCertificate::extensions()` 返回它，应用再按 OID、名称和支持状态读取内容。

## 实际使用场景

### 1. 检查证书是否覆盖目标主机

主机名校验通常直接使用 `QSslCertificate::subjectAlternativeNames()`。只有在做证书审计、诊断工具或需要识别未知扩展时，才需要遍历 `extensions()`。

### 2. 展示证书详情

证书查看器可以把 `oid()`、`name()`、`isCritical()` 和 `value()` 展示出来。对于未知扩展，应优先展示 OID 和原始/后端解码结果，不要把 `QVariant` 强行解释成固定结构。

### 3. 兼容扩展和版本

`isSupported()` 的“支持”不是指扩展一定存在，也不是指证书一定有效，而是指 Qt 保证该扩展的 `QVariant` 值结构在版本间保持不变。未知扩展仍可读取，但其值结构可能随 Qt 或 SSL 后端变化。

## 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(app PRIVATE Qt6::Network)
```

```cpp
#include <QSslCertificate>
#include <QSslCertificateExtension>
#include <QDebug>

QSslCertificate certificate("server.crt");
for (const QSslCertificateExtension &extension : certificate.extensions()) {
    qDebug() << extension.oid()
             << extension.name()
             << extension.isCritical()
             << extension.isSupported()
             << extension.value();
}
```

## 关键语义与边界

### 它是只读视图，不是扩展构造器

公开接口只有默认构造、拷贝/赋值、查询和 `swap()`，没有设置 OID、名称、critical 标志或值的 setter。默认构造对象没有一个可供应用填充的“新扩展编辑状态”；有意义的扩展通常来自 `QSslCertificate::extensions()`。

### `value()` 的类型由扩展种类决定

返回值是 `QVariant`，其内部结构取决于具体扩展。不能仅因为 `canConvert<T>()` 成功，就把所有版本和后端都当成相同协议。跨版本保存或传输时，应同时保存 OID，并对 `isSupported()` 和实际类型做检查。

### `name()` 不一定是人类可读的固定名称

如果 Qt 不认识该扩展，`name()` 会返回 OID。因此 UI 不应假定 `name()` 非空或一定是熟悉的短名称。

### critical 不等于 Qt 已支持

`isCritical()` 说明证书发布者把该扩展标记为关键扩展；`isSupported()` 说明 Qt 对返回值结构的稳定性承诺。这两个概念互相独立。

### 生命周期、线程和所有权

这是可拷贝的值类型，函数是可重入的。对象本身不拥有 `QSslCertificate` 或外部 `QIODevice`，也不需要事件循环。复制的是 Qt 值对象状态，不是让应用获得 SSL 后端对象的所有权。

## 常见误区

- 把 `isSupported() == false` 当成“扩展无效”：它只表示 `QVariant` 结构没有跨版本稳定承诺。
- 只显示 `name()` 而不显示 `oid()`：未知扩展的名称可能就是 OID，且 OID 才是稳定识别符。
- 把 `value()` 当成统一字符串：不同扩展可能是列表、映射或其他 Qt 类型。
- 用它代替主机名验证：TLS 主机名验证应由 `QSslSocket`/`QSslCertificate::verify()` 的证书校验流程完成。
- 试图通过默认构造对象创建自定义证书扩展：该类没有公开的构造参数或写入接口。

## 逐项 API 说明

### 构造、赋值和交换

#### `QSslCertificateExtension()`

构造一个扩展值对象。它主要用于声明变量、容器元素或接收 Qt 返回值；单独默认构造并不能创建一个可写入的证书扩展。

#### `QSslCertificateExtension(const QSslCertificateExtension &other)`

复制 `other` 的扩展信息。该类是值类型，复制后可独立保存和查询。

#### `operator=(const QSslCertificateExtension &other)`

把 `other` 的内容复制到当前对象并返回当前对象引用。

#### `operator=(QSslCertificateExtension &&other)`

移动赋值，交换/转移内部值对象状态。移动后的对象只应继续析构或重新赋值，不应依赖其原有内容。

#### `~QSslCertificateExtension()`

销毁扩展值对象，不会销毁证书、socket 或其他外部资源。

#### `swap(QSslCertificateExtension &other)`

无异常地交换两个扩展对象，适合实现高效的值对象赋值或容器操作。

### 查询

#### `QString oid() const`

返回扩展的 ASN.1 对象标识符。需要稳定识别扩展时优先使用 OID，而不是依赖本地化名称。

#### `QString name() const`

返回扩展名称；Qt 不认识该扩展时返回 OID。

#### `QVariant value() const`

返回扩展的解码值。结构由扩展类型决定；未知或不稳定扩展不能假定固定的 `QVariant` 类型。

#### `bool isCritical() const`

返回证书是否将该扩展标记为 critical。

#### `bool isSupported() const`

返回 Qt 是否承诺该扩展的 `value()` 结构在版本间保持不变。返回 `false` 不代表不能读取，只代表应用需要自行承担结构兼容性。

## API 速查表

| 类别 | API | 语义 | 边界与注意事项 |
| --- | --- | --- | --- |
| 构造 | `QSslCertificateExtension()` | 构造扩展值对象。 | 没有 setter，不能靠它编辑或生成证书扩展。 |
| 构造 | `QSslCertificateExtension(const QSslCertificateExtension &other)` | 复制扩展信息。 | 值语义；不转移证书或后端资源所有权。 |
| 赋值 | `QSslCertificateExtension &operator=(const QSslCertificateExtension &other)` | 复制赋值并返回自身。 | 覆盖当前对象内容。 |
| 赋值 | `QSslCertificateExtension &operator=(QSslCertificateExtension &&other)` | 移动赋值。 | 移动源只应析构或重新赋值。 |
| 析构 | `~QSslCertificateExtension()` | 销毁值对象。 | 不影响来源证书。 |
| 交换 | `void swap(QSslCertificateExtension &other) noexcept` | 交换两个对象。 | 快速且不抛异常。 |
| 查询 | `QString oid() const` | 返回 ASN.1 OID。 | 适合作为稳定识别键。 |
| 查询 | `QString name() const` | 返回扩展名称。 | 未知扩展时返回 OID。 |
| 查询 | `QVariant value() const` | 返回依扩展类型解码的值。 | 结构不统一；先检查 OID 和 `isSupported()`。 |
| 查询 | `bool isCritical() const` | 查询 critical 标志。 | 不等同于 Qt 是否支持该扩展。 |
| 查询 | `bool isSupported() const` | 查询 Qt 是否保证值结构稳定。 | `false` 仍可读取，但不能依赖跨版本结构。 |

## 一句话总结

`QSslCertificateExtension` 是证书扩展的只读值对象：用 OID 识别，用 `isCritical()` 判断证书语义，用 `isSupported()` 判断 `QVariant` 结构能否稳定依赖。
