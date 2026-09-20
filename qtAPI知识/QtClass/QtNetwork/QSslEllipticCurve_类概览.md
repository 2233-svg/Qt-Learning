# QSslEllipticCurve

> Qt 6.11.1 | Qt6::Network | `#include <QSslEllipticCurve>`

## 类解决的问题

TLS 的椭圆曲线不是普通字符串。SSL 后端需要知道曲线的内部标识、短名称、长名称，以及它是否属于 TLS 密钥交换允许协商的 named curve。`QSslEllipticCurve` 把这些信息封装成可比较的值类型，供 `QSslConfiguration::ellipticCurves()` 和 `setEllipticCurves()` 使用。

它解决的是“在 Qt API 与 SSL 后端之间传递一个明确的曲线标识”，而不是执行椭圆曲线数学运算，也不是生成密钥。

## 实际使用场景

### 1. 查询当前后端支持的曲线

```cpp
const auto curves = QSslConfiguration::supportedEllipticCurves();
for (const QSslEllipticCurve &curve : curves)
    qDebug() << curve.shortName() << curve.longName();
```

### 2. 为 TLS 配置允许的曲线

```cpp
QSslConfiguration config = QSslConfiguration::defaultConfiguration();
const auto curve = QSslEllipticCurve::fromShortName("P-256");
if (curve.isValid() && curve.isTlsNamedCurve()) {
    config.setEllipticCurves({curve});
}
```

实际能否使用还取决于 SSL backend、Qt 构建方式和协议版本。配置前应优先与 `supportedEllipticCurves()` 的结果比较。

### 3. 诊断协商失败

记录 `shortName()`、`longName()` 和 `isTlsNamedCurve()`，可以判断问题是名称解析失败、后端不支持，还是曲线不适用于 TLS 密钥交换。

## 构建与基本模型

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(app PRIVATE Qt6::Network)
```

```cpp
#include <QSslConfiguration>
#include <QSslEllipticCurve>

QSslEllipticCurve curve =
    QSslEllipticCurve::fromShortName(QStringLiteral("secp256r1"));
if (!curve.isValid()) {
    // 名称未被当前 SSL backend 识别。
}
```

## 关键语义与边界

### 默认构造对象无效

`QSslEllipticCurve()` 构造的是 invalid curve。`shortName()` 和 `longName()` 对无效对象返回空字符串；使用前先检查 `isValid()`。

### 名称是 backend 相关的

`fromShortName()` 接受 RFC 4492 常用短名称（例如 `secp521r1`）或 NIST 风格名称（例如 `P-256`），但实际识别集合依赖 SSL 实现。`fromLongName()` 的拼写也依赖实现。

在 OpenSSL 实现中，这两个查找函数按大小写敏感处理。不要先验地把输入转小写，也不要假设不同 backend 的长名称相同。

### 有效不等于可用于 TLS

`isValid()` 只说明对象代表一个有效曲线；`isTlsNamedCurve()` 才说明该曲线属于 TLS 椭圆曲线密钥交换可使用的 named curve。两者都应检查。

### 平台约束

Qt 6.11.1 文档注明该类当前只在 OpenSSL backend 支持。项目若切换到其他 SSL backend，不应把这类对象当成跨 backend 的稳定配置接口。

### 生命周期和容器

这是轻量值类型，函数可重入。它可以比较相等，可作为 `QHash` 和 `QSet` 的键，但不能作为 `QMap` 的键，因为该类没有排序关系。`QDebug` 输出适合日志诊断，不应作为持久化格式。

## 常见误区

- 忽略 `isValid()`，直接把查找结果传给 `setEllipticCurves()`。
- 把“有效曲线”误认为“当前 backend 支持并允许 TLS 协商的曲线”。
- 认为 `P-256`、`prime256v1`、`secp256r1` 在所有 backend 中一定等价且都能被同一个函数识别。
- 用 `longName()` 作为跨平台配置文件中的唯一名称。
- 把 `QSslEllipticCurve` 当成公钥、私钥或椭圆曲线参数本身；它只描述曲线标识。

## 逐项 API 说明

### 构造和查询

#### `QSslEllipticCurve()`

构造无效曲线，适合声明变量或接收失败结果。必须通过 `isValid()` 判断是否可用。

#### `bool isValid() const`

返回当前对象是否代表有效曲线。

#### `bool isTlsNamedCurve() const`

返回当前曲线是否属于 TLS 椭圆曲线密码算法密钥交换可使用的 named curve。无效曲线自然不能当作可协商曲线使用。

#### `QString shortName() const`

返回曲线的 conventional short name。无效对象返回空字符串。

#### `QString longName() const`

返回曲线的 conventional long name。无效对象返回空字符串，具体名称拼写依赖 SSL backend。

### 从名称构造

#### `static QSslEllipticCurve fromShortName(const QString &name)`

按短名称查找曲线。名称不受支持时返回 invalid 对象。识别规则由 SSL backend 决定；OpenSSL 下大小写敏感。

#### `static QSslEllipticCurve fromLongName(const QString &name)`

按长名称查找曲线。名称不受支持时返回 invalid 对象。长名称的精确拼写由 SSL backend 决定；OpenSSL 下大小写敏感。

### 相关非成员

#### `operator==` / `operator!=`

比较两个对象是否代表同一曲线，而不是比较名称字符串的格式。

#### `operator<<(QDebug, QSslEllipticCurve)`

把曲线写入 Qt 调试流，用于日志和诊断。

## API 速查表

| 类别 | API | 语义 | 边界与注意事项 |
| --- | --- | --- | --- |
| 构造 | `constexpr QSslEllipticCurve() noexcept` | 构造无效曲线。 | `isValid()` 为 `false`，名称为空。 |
| 静态工厂 | `static QSslEllipticCurve fromShortName(const QString &name)` | 按短名称查找曲线。 | 未识别返回 invalid；OpenSSL 名称大小写敏感。 |
| 静态工厂 | `static QSslEllipticCurve fromLongName(const QString &name)` | 按长名称查找曲线。 | 长名称依 backend；未识别返回 invalid。 |
| 查询 | `bool isValid() const noexcept` | 判断对象是否代表有效曲线。 | 不等同于当前配置可用。 |
| 查询 | `bool isTlsNamedCurve() const noexcept` | 判断是否为 TLS 可协商 named curve。 | 配置 TLS 时应与 `isValid()` 一起检查。 |
| 查询 | `QString shortName() const` | 返回 conventional short name。 | 无效对象返回空字符串。 |
| 查询 | `QString longName() const` | 返回 conventional long name。 | 拼写依赖 backend；无效对象返回空字符串。 |
| 比较 | `operator==(lhs, rhs)` | 判断代表的曲线是否相同。 | 可用于相等比较。 |
| 比较 | `operator!=(lhs, rhs)` | 判断代表的曲线是否不同。 | 与 `operator==` 语义相反。 |
| 调试 | `operator<<(QDebug, curve)` | 输出曲线调试信息。 | 不是稳定序列化格式。 |

## 一句话总结

`QSslEllipticCurve` 是 TLS 曲线标识值对象：先从 supported 列表选择，再检查 `isValid()` 和 `isTlsNamedCurve()`，最后交给 `QSslConfiguration`。
