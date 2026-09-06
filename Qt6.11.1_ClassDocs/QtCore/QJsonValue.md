# QJsonValue

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** JSON 基本值容器，负责在 null、布尔、数字、字符串、对象和数组之间表示值。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QJsonValue`：JSON 基本值容器，负责在 null、布尔、数字、字符串、对象和数组之间表示值。

**内部模型：** JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

**适用场景：** 接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

## 2. 依赖与对象关系

- 头文件：`#include <QJsonValue>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

### 状态、生命周期和线程

**生命周期：** 解析结果通常是值对象，可在作用域内传递；流式解析器则依赖输入设备和读取顺序。解析错误、结构合法和业务字段合法是三个不同层次，必须分别检查。

**状态与结果：** 先判断文档是否为空、根节点类型和解析错误，再访问字段；字段缺失、类型不匹配、空值和默认值要分开处理。序列化时要明确紧凑/格式化输出和编码。

**线程与事件循环：** 值形式的解析结果可以复制后跨线程处理；共享设备、流对象和可变 DOM 不应无保护地跨线程使用。大文档要评估一次性树结构的内存成本，必要时用流式 API。

## 3. 直接使用

接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(since 6.9) JsonFormat`
- `enum Type { Null, Bool, Double, String, Array, …, Undefined }`

### 公有函数

- `QJsonValue(QJsonValue::Type type = Null)`
- `QJsonValue(QLatin1StringView s)`
- `QJsonValue(bool b)`
- `QJsonValue(const QJsonArray &a)`
- `QJsonValue(const QJsonObject &o)`
- `QJsonValue(const QString &s)`
- `QJsonValue(const char *s)`
- `QJsonValue(double v)`
- `(since 6.3) QJsonValue(QJsonArray &&a)`
- `(since 6.3) QJsonValue(QJsonObject &&o)`
- `QJsonValue(int v)`
- `QJsonValue(qint64 v)`
- `QJsonValue(const QJsonValue &other)`
- `QJsonValue(QJsonValue &&other)`
- `~QJsonValue()`
- `bool isArray() const`
- `bool isBool() const`
- `bool isDouble() const`
- `bool isNull() const`
- `bool isObject() const`
- `bool isString() const`
- `bool isUndefined() const`
- `void swap(QJsonValue &other)`
- `QJsonArray toArray(const QJsonArray &defaultValue) const`
- `QJsonArray toArray() const`
- `bool toBool(bool defaultValue = false) const`
- `double toDouble(double defaultValue = 0) const`
- `int toInt(int defaultValue = 0) const`
- `(since 6.0) qint64 toInteger(qint64 defaultValue = 0) const`
- `(since 6.9) QByteArray toJson(QJsonValue::JsonFormat format = JsonFormat::Indented) const`
- `QJsonObject toObject(const QJsonObject &defaultValue) const`
- `QJsonObject toObject() const`
- `QString toString() const`
- `QString toString(const QString &defaultValue) const`
- `(since 6.10) QAnyStringView toStringView(QAnyStringView defaultValue = {}) const`
- `QVariant toVariant() const`
- `QJsonValue::Type type() const`
- `QJsonValue & operator=(QJsonValue &&other)`
- `QJsonValue & operator=(const QJsonValue &other)`
- `const QJsonValue operator[](const QString &key) const`
- `const QJsonValue operator[](qsizetype i) const`
- `const QJsonValue operator[](QLatin1StringView key) const`
- `const QJsonValue operator[](QStringView key) const`

### 静态公有成员

- `(since 6.9) QJsonValue fromJson(QByteArrayView json, QJsonParseError *error = nullptr)`
- `QJsonValue fromVariant(const QVariant &variant)`

### 相关非成员函数

- `bool operator!=(const QJsonValue &lhs, const QJsonValue &rhs)`
- `bool operator==(const QJsonValue &lhs, const QJsonValue &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias, since 6.9] QJsonValue::JsonFormat`

**作用与语义：**

和`QJsonDocument::JsonFormat`一样。
这种类型防御是在Qt 6.9引入的。

### `enum QJsonValue::Type`

**作用与语义：**

该枚举描述了 JSON 值的类型。
- `QJsonValue::Null`：`0x0`;空值
- `QJsonValue::Bool`：`0x1`;一个布尔值。使用`toBool()`转换为布尔值。
- `QJsonValue::Double`：`0x2`;一个数值。用`toDouble()`转换为双倍，或用`toInteger()`转换为qint64。
- `QJsonValue::String`：`0x3`;字符串。用`toString()`转换为`QString`。
- `QJsonValue::Array`：`0x4`;一个数组。使用`toArray()`转换为`QJsonArray`。
- `QJsonValue::Object`：`0x5`;一个对象。使用`toObject()`转换为`QJsonObject`。
- `QJsonValue::Undefined`：`0x80`;值未定义。当尝试读取数组中的超出范围值或对象中不存在的键时，通常会以错误条件返回。

### `QJsonValue::QJsonValue(QJsonValue::Type type = Null)`

**作用与语义：**

生成类型为`type`的QJsonValue。
默认情况下，是创建一个 Null 值。

### `QJsonValue::QJsonValue(QLatin1StringView s)`

**作用与语义：**

创建 String 类型的值，`s` 查看 Latin-1 字符串。

### `QJsonValue::QJsonValue(bool b)`

**作用与语义：**

生成一个类型为Bool的值，值为`b`。

### `QJsonValue::QJsonValue(const QJsonArray &a)`

**作用与语义：**

生成类型为 Array 的值，值为 `a`。

### `QJsonValue::QJsonValue(const QJsonObject &o)`

**作用与语义：**

创建一个类型为 Object 的值，值为 `o`。

### `QJsonValue::QJsonValue(const QString &s)`

**作用与语义：**

生成一个类型为 String 的值，值为 `s`。

### `QJsonValue::QJsonValue(const char *s)`

**作用与语义：**

假设输入采用UTF-8编码，生成一个类型为String的值，值为`s`。
你可以通过在编译应用时定义`QT_NO_CAST_FROM_ASCII`来禁用这个构造函数。

### `QJsonValue::QJsonValue(double v)`

**作用与语义：**

生成一个类型为 Double，值为 `v`。

### `[noexcept, since 6.3] QJsonValue::QJsonValue(QJsonArray &&a)`

**作用与语义：**

生成类型为`type`的QJsonValue。
默认情况下，是创建一个 Null 值。

### `[noexcept, since 6.3] QJsonValue::QJsonValue(QJsonObject &&o)`

**作用与语义：**

生成类型为`type`的QJsonValue。
默认情况下，是创建一个 Null 值。

### `QJsonValue::QJsonValue(int v)`

**作用与语义：**

生成一个类型为 Double，值为 `v`。

### `QJsonValue::QJsonValue(qint64 v)`

**作用与语义：**

生成一个类型为 Double 的值，值为 `v`。
该值内部存储为64位整数，只要用`toInteger()`检索，就能保持完整精度。然而，用`toDouble()`取值时，除非值介于±2^53之间，否则精度会下降。

### `[noexcept] QJsonValue::QJsonValue(const QJsonValue &other)`

**作用与语义：**

创建`other`副本。

### `[noexcept] QJsonValue::QJsonValue(QJsonValue &&other)`

**作用与语义：**

从`other`移动构造一个QJson值。

### `[noexcept] QJsonValue::~QJsonValue()`

**作用与语义：**

毁掉了价值。

### `[static, since 6.9] QJsonValue QJsonValue::fromJson(QByteArrayView json, QJsonParseError *error = nullptr)`

**作用与语义：**

解析`json`为UTF-8编码的JSON值，并由此生成`QJsonValue`。
如果解析成功，返回有效的`QJsonValue`。如果失败，返回的值将被`undefined`，可选的`error`变量将包含关于错误的更多细节。

### `[static] QJsonValue QJsonValue::fromVariant(const QVariant &variant)`

**作用与语义：**

将`variant`转换成`QJsonValue`并退回。
转换后将`QVariant`类型转换为如下：
- `Source type`：目的地类型
- `QMetaType::Nullptr`：`QJsonValue::Null`
- `QMetaType::Bool`：`QJsonValue::Bool`
- `QMetaType::Int`
`QMetaType::UInt`。
`QMetaType::LongLong`。
`QMetaType::ULongLong`。
`QMetaType::Float`。
`QMetaType::Double`：`QJsonValue::Double`。
- `QMetaType::QString`：`QJsonValue::String`
- `QMetaType::QStringList`
`QMetaType::QVariantList`：`QJsonValue::Array`。
- `QMetaType::QVariantMap`
`QMetaType::QVariantHash`：`QJsonValue::Object`。
- `QMetaType::QUrl`：`QJsonValue::String`。转换时将使用带有标志`QUrl::FullyEncoded`的`QUrl::toString()`，以确保解析URL的最大兼容性
- `QMetaType::QUuid`：`QJsonValue::String`。自Qt 5.11起，所得字符串不再包含大括号
- `QMetaType::QCborValue`：无论回归`QCborValue::toJsonValue()`类型。
- `QMetaType::QCborArray`：`QJsonValue::Array`。有关转换限制，请参见 `QCborValue::toJsonValue()`。
- `QMetaType::QCborMap`：QJsonValue：：Map。参见`QCborValue::toJsonValue()`关于转换限制和映射键的“串化”。
`QVariant` 可能携带比 JSON 可表示的信息更多。如果`QVariant`不是上述类型之一，转换不保证，未来版本的 Qt 可能会变更，就像 UUID 版本一样。代码应尽量避免使用上述以外的其他类型。
如果 `QVariant::isNull()` 返回为真，则返回或插入一个空 `QJsonValue`，无论 `QVariant` 携带的类型如何。注意 Qt 6.0 中影响 `QVariant::isNull()` 的行为变化也影响该函数。
浮点值为无穷大或 NaN 的值将被转换为空 JSON 值。自 Qt 6.0 起，`QJsonValue` 可以无损存储任意 64 位带符号整数的全部精度，但在之前版本中，超出 ±2^53 范围的值可能会损失精度。大于或等于 2^63 的无符号 64 位值将会丢失精度或别名变为负值，因此应避免`QMetaType::ULongLong`。
对于上述未列出的其他类型，会尝试转换为字符串，通常但不总是通过调用`QVariant::toString()`实现。如果转换失败，该值将被空JSON值替换。请注意，`QVariant::toString()`对大多数类型也是有损的。例如，如果传递的`QVariant`表示原始字节数组数据，建议预编码为Base64（或其他无损编码），否则将使用`QString::fromUtf8()`进行有损转换。
请注意，通过`QVariant::toString()`的转换可能随时发生变化。未来`QVariant`和`QJsonValue`都可能扩展以支持更多类型，这将导致该函数执行转换的方式发生变化。

### `bool QJsonValue::isArray() const`

**作用与语义：**

如果值包含数组，返回`true`。

### `bool QJsonValue::isBool() const`

**作用与语义：**

如果值包含布尔值，返回`true`。

### `bool QJsonValue::isDouble() const`

**作用与语义：**

如果值包含重叠，返回`true`。

### `bool QJsonValue::isNull() const`

**作用与语义：**

如果值为空，返回`true`。

### `bool QJsonValue::isObject() const`

**作用与语义：**

如果值包含对象，返回`true`。

### `bool QJsonValue::isString() const`

**作用与语义：**

如果值包含字符串，返回`true`。

### `bool QJsonValue::isUndefined() const`

**作用与语义：**

如果值未定义，返回`true`。这种情况在某些情况下可能发生，例如访问`QJsonObject`中不存在的密钥。

### `[noexcept] void QJsonValue::swap(QJsonValue &other)`

**作用与语义：**

将该值与`other`交换。该操作非常快速且从未失败。

### `QJsonArray QJsonValue::toArray(const QJsonArray &defaultValue) const`

**作用与语义：**

将值转换为数组并返回。
如果`type()`不是数组，`defaultValue`会被返回。

### `QJsonArray QJsonValue::toArray() const`

**作用与语义：**

将值转换为数组并返回。
如果`type()`不是数组，则会返回`QJsonArray()`。

### `bool QJsonValue::toBool(bool defaultValue = false) const`

**作用与语义：**

将值转换为布尔值并返回。
如果`type()`不是布尔，`defaultValue`将被返回。

### `double QJsonValue::toDouble(double defaultValue = 0) const`

**作用与语义：**

将数值转换为双重值并返回。
如果`type()`不是双倍，`defaultValue`将被退还。

### `int QJsonValue::toInt(int defaultValue = 0) const`

**作用与语义：**

将值转换为整数并返回。
如果`type()`不是双倍，或者该值不是整数，则返回`defaultValue`。

### `[since 6.0] qint64 QJsonValue::toInteger(qint64 defaultValue = 0) const`

**作用与语义：**

将数值转换为整数并返回。
如果`type()`不是 Double，或者值不是可表示为 qint64 的整数，`defaultValue`将被返回。

### `[since 6.9] QByteArray QJsonValue::toJson(QJsonValue::JsonFormat format = JsonFormat::Indented) const`

**作用与语义：**

将`QJsonValue`转换为UTF-8编码的JSON值，并附有给`format`。

### `QJsonObject QJsonValue::toObject(const QJsonObject &defaultValue) const`

**作用与语义：**

将值转换为对象并返回。
如果`type()`不是对象，`defaultValue`将被返回。

### `QJsonObject QJsonValue::toObject() const`

**作用与语义：**

将值转换为对象并返回。
如果`type()`不是对象，`QJsonObject()`将被返回。

### `QString QJsonValue::toString() const`

**作用与语义：**

将数值转换为`QString`并返回。
如果`type()`不是String，则返回空`QString`。

### `QString QJsonValue::toString(const QString &defaultValue) const`

**作用与语义：**

将数值转换为`QString`并返回。
如果`type()`不是String，`defaultValue`将被返回。

### `[since 6.10] QAnyStringView QJsonValue::toStringView(QAnyStringView defaultValue = {}) const`

**作用与语义：**

如果字符串值属于`string`类型，返回存储在该`QJsonValue`中的字符串值。否则返回`defaultValue`。由于`QJsonValue`以US-ASCII、UTF-8或UTF-16形式存储字符串，返回的`QAnyStringView`可以存在这些编码中的任意一种。
该函数不分配内存。返回值有效，直到下一次调用该对象的非const成员函数。如果该对象超出作用域，返回值有效，直到下一次调用父JSON对象或数组上的非const成员函数。

### `QVariant QJsonValue::toVariant() const`

**作用与语义：**

将价值转换为`QVariant()`。
`QJsonValue`类型将按以下方式转换：
- `Null`：`QMetaType::Nullptr`
- `Bool`：`QMetaType::Bool`
- `Double`：`QMetaType::Double`或`QMetaType::LongLong`
- `String`：`QString`
- `Array`：`QVariantList`
- `Object`：`QVariantMap`
- `Undefined`：`QVariant()`

### `QJsonValue::Type QJsonValue::type() const`

**作用与语义：**

返回值的类型。

### `[noexcept] QJsonValue &QJsonValue::operator=(QJsonValue &&other)`

**作用与语义：**

Move-assign `other` 到该值。

### `[noexcept] QJsonValue &QJsonValue::operator=(const QJsonValue &other)`

**作用与语义：**

将`other`中存储的值分配给该对象。

### `const QJsonValue QJsonValue::operator[](const QString &key) const`

**作用与语义：**

返回代表密钥`key`值的`QJsonValue`。
相当于调用 `toObject()`.value（key）。
如果密钥不存在，或者`isObject()`为假，返回的`QJsonValue`为`QJsonValue::Undefined`。

### `const QJsonValue QJsonValue::operator[](qsizetype i) const`

**作用与语义：**

返回一个`QJsonValue`，表示索引`i`的值。
相当于调用 `toArray()`.at（i）。
如果`i`出界，或者`isArray()`为假，返回的`QJsonValue`为`QJsonValue::Undefined`。

### `const QJsonValue QJsonValue::operator[](QLatin1StringView key) const`

**作用与语义：**

返回代表密钥`key`值的`QJsonValue`。
相当于调用 `toObject()`.value（key）。
如果密钥不存在，或者`isObject()`为假，返回的`QJsonValue`为`QJsonValue::Undefined`。

### `const QJsonValue QJsonValue::operator[](QStringView key) const`

**作用与语义：**

返回代表密钥`key`值的`QJsonValue`。
相当于调用 `toObject()`.value（key）。
如果密钥不存在，或者`isObject()`为假，返回的`QJsonValue`为`QJsonValue::Undefined`。

### `[noexcept] bool operator!=(const QJsonValue &lhs, const QJsonValue &rhs)`

**作用与语义：**

如果`lhs`值不等于`rhs`值，回报`true`，否则`false`。

### `[noexcept] bool operator==(const QJsonValue &lhs, const QJsonValue &rhs)`

**作用与语义：**

如果`lhs`值等于`rhs`值，则`true`，否则`false`。

### `(since 6.9) JsonFormat`

**作用与语义：**

和`QJsonDocument::JsonFormat`一样。
这种类型防御是在Qt 6.9引入的。

## 6. 深入实践与常见坑

### 生命周期和资源边界

解析结果通常是值对象，可在作用域内传递；流式解析器则依赖输入设备和读取顺序。解析错误、结构合法和业务字段合法是三个不同层次，必须分别检查。

### 状态和错误边界

先判断文档是否为空、根节点类型和解析错误，再访问字段；字段缺失、类型不匹配、空值和默认值要分开处理。序列化时要明确紧凑/格式化输出和编码。

### 线程边界

值形式的解析结果可以复制后跨线程处理；共享设备、流对象和可变 DOM 不应无保护地跨线程使用。大文档要评估一次性树结构的内存成本，必要时用流式 API。

### 最容易出现的错误

不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QJsonValue` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
