# QCborValue

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Cbor值”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCborValue` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCborValue>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum DiagnosticNotationOption { Compact, LineWrapped, ExtendedFormat }`
- `flags DiagnosticNotationOptions`
- `enum EncodingOption { NoTransformation, UseFloat, UseFloat16, UseIntegers }`
- `flags EncodingOptions`
- `enum Type { Integer, ByteArray, String, Array, Map, …, Uuid }`

### 公有函数

- `QCborValue()`
- `QCborValue(QCborArray &&a)`
- `QCborValue(QCborMap &&m)`
- `QCborValue(QCborSimpleType st)`
- `QCborValue(QCborValue::Type t_)`
- `QCborValue(QStringView s)`
- `QCborValue(bool b)`
- `QCborValue(const QByteArray &ba)`
- `QCborValue(const QCborArray &a)`
- `QCborValue(const QCborMap &m)`
- `QCborValue(const QDateTime &dt)`
- `QCborValue(const QRegularExpression &rx)`
- `QCborValue(const QString &s)`
- `QCborValue(const QUrl &url)`
- `QCborValue(const QUuid &uuid)`
- `QCborValue(double d)`
- `QCborValue(qint64 i)`
- `QCborValue(std::nullptr_t)`
- `QCborValue(QCborKnownTags tag, const QCborValue &tv = QCborValue())`
- `QCborValue(QCborTag tag, const QCborValue &tv = QCborValue())`
- `QCborValue(QLatin1StringView s)`
- `QCborValue(const QCborValue &other)`
- `QCborValue(QCborValue &&other)`
- `~QCborValue()`
- `int compare(const QCborValue &other) const`
- `bool isArray() const`
- `bool isBool() const`
- `bool isByteArray() const`
- `bool isContainer() const`
- `bool isDateTime() const`
- `bool isDouble() const`
- `bool isFalse() const`
- `bool isInteger() const`
- `bool isInvalid() const`
- `bool isMap() const`
- `bool isNull() const`
- `bool isRegularExpression() const`
- `bool isSimpleType() const`
- `bool isSimpleType(QCborSimpleType st) const`
- `bool isString() const`
- `bool isTag() const`
- `bool isTrue() const`
- `bool isUndefined() const`
- `bool isUrl() const`
- `bool isUuid() const`
- `void swap(QCborValue &other)`
- `QCborTag tag(QCborTag defaultValue = QCborTag(-1)) const`
- `QCborValue taggedValue(const QCborValue &defaultValue = QCborValue()) const`
- `QCborArray toArray() const`
- `QCborArray toArray(const QCborArray &defaultValue) const`
- `bool toBool(bool defaultValue = false) const`
- `QByteArray toByteArray(const QByteArray &defaultValue = {}) const`
- `QByteArray toCbor(QCborValue::EncodingOptions opt = NoTransformation) const`
- `void toCbor(QCborStreamWriter &writer, QCborValue::EncodingOptions opt = NoTransformation) const`
- `QDateTime toDateTime(const QDateTime &defaultValue = {}) const`
- `QString toDiagnosticNotation(QCborValue::DiagnosticNotationOptions opts = Compact) const`
- `double toDouble(double defaultValue = 0) const`
- `qint64 toInteger(qint64 defaultValue = 0) const`
- `QJsonValue toJsonValue() const`
- `QCborMap toMap() const`
- `QCborMap toMap(const QCborMap &defaultValue) const`
- `QRegularExpression toRegularExpression(const QRegularExpression &defaultValue = {}) const`
- `QCborSimpleType toSimpleType(QCborSimpleType defaultValue = QCborSimpleType::Undefined) const`
- `QString toString(const QString &defaultValue = {}) const`
- `(since 6.10) QAnyStringView toStringView(QAnyStringView defaultValue = {}) const`
- `QUrl toUrl(const QUrl &defaultValue = {}) const`
- `QUuid toUuid(const QUuid &defaultValue = {}) const`
- `QVariant toVariant() const`
- `QCborValue::Type type() const`
- `QCborValue & operator=(const QCborValue &other)`
- `QCborValue & operator=(QCborValue &&other)`
- `QCborValueRef operator[](const QString &key)`
- `const QCborValue operator[](const QString &key) const`
- `QCborValueRef operator[](QLatin1StringView key)`
- `QCborValueRef operator[](qint64 key)`
- `const QCborValue operator[](QLatin1StringView key) const`
- `const QCborValue operator[](qint64 key) const`

### 静态公有成员

- `QCborValue fromCbor(QCborStreamReader &reader)`
- `QCborValue fromCbor(const QByteArray &ba, QCborParserError *error = nullptr)`
- `QCborValue fromCbor(const char *data, qsizetype len, QCborParserError *error = nullptr)`
- `QCborValue fromCbor(const quint8 *data, qsizetype len, QCborParserError *error = nullptr)`
- `QCborValue fromJsonValue(const QJsonValue &v)`
- `QCborValue fromVariant(const QVariant &variant)`

### 相关非成员函数

- `bool operator!=(const QCborValue &lhs, const QCborValue &rhs)`
- `bool operator<(const QCborValue &lhs, const QCborValue &rhs)`
- `bool operator<=(const QCborValue &lhs, const QCborValue &rhs)`
- `bool operator==(const QCborValue &lhs, const QCborValue &rhs)`
- `bool operator>(const QCborValue &lhs, const QCborValue &rhs)`
- `bool operator>=(const QCborValue &lhs, const QCborValue &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QCborValue::DiagnosticNotationOptionflags QCborValue::DiagnosticNotationOptions`

**作用与语义：**

该枚举用于选项参数 to `toDiagnosticNotation()`，以修改输出格式。
- `QCborValue::Compact`：`0x00`;不使用任何换行，形成紧凑的表示。
- `QCborValue::LineWrapped`：换行`0x01`;每行一个换行`QCborValue`。
- `QCborValue::ExtendedFormat`：`0x02`;使用了一些RFC 7049中没有的选项来表示数值。这些选项可能会发生变化。
目前，`ExtendedFormat`将改变字节数组的表示方式。没有它，字节数组总是十六进制编码且没有空格。有了它，`QCborValue::toCbor()`会根据上下文使用带空格的十六进制、base64或base64url编码。
DiagnosticNotationOptions 类型是 QFlags 的 typedef<DiagnosticNotationOption>。它存储 DiagnosticNotationOption 值的 OR 组合。

### `enum QCborValue::EncodingOptionflags QCborValue::EncodingOptions`

**作用与语义：**

该枚举用于`toCbor()`的选项参数，修改编码器的行为。
- `QCborValue::NoTransformation`：`0`;（默认）不执行变换。
- `QCborValue::UseFloat`：`0x02`;告诉编码器尽可能使用 IEEE 754 单精度浮点（即 `float`）。
- `QCborValue::UseFloat16`：`UseFloat | 0x04`;告诉编码器尽可能使用IEEE 754半精度浮点（即`qfloat16`）。暗示`UseFloat`。
- `QCborValue::UseIntegers`：`0x08`;每当类型为`Double`的值包含整数时，指示编码器使用整数。
编码流为规范格式是必须使用`UseFloat16`，但并非其他必要条件。
EncodingOptions 类型是 QFlags 的 typedef<EncodingOption>。它存储 EncodingOption 值的 OR 组合。

### `enum QCborValue::Type`

**作用与语义：**

这个枚举代表`QCborValue`类型。`type()`函数返回它。
CBOR 内置类型包括：
- `QCborValue::Integer`：`0x00`;`qint64`：整数值
- `QCborValue::ByteArray`：`0x40`;`QByteArray`：字节数组（“字节串”）
- `QCborValue::String`：`0x60`;`QString`：Unicode字符串（“文本字符串”）
- `QCborValue::Array`：`0x80`;`QCborArray`：QCborValue 数组
- `QCborValue::Map`：`0xa0`;`QCborMap`：QCborValues 的关联容器
- `QCborValue::SimpleType`：`0x100`;`QCborSimpleType`：几种简单类型/值之一
- `QCborValue::False`：`SimpleType + int(QCborSimpleType::False)`;`bool`：值的简单类型`false`
- `QCborValue::True`：`SimpleType + int(QCborSimpleType::True)`;`bool`：简单类型，值`true`
- `QCborValue::Null`：`SimpleType + int(QCborSimpleType::Null)`;`std::nullptr_t`：空值的简单类型
- `QCborValue::Undefined`：`SimpleType + int(QCborSimpleType::Undefined)`;（无类型）未定义值的简单类型
- `QCborValue::Double`：`0x202`;`double`：双精度浮点
- `QCborValue::Invalid`：`-1`;这不是有效的值，通常表示CBOR解码错误
此外，`QCborValue` 也可以表示扩展类型：
- `QCborValue::Tag`：`0xc0`;未知或未识别的扩展类型，由其标签（`QCborTag`）和标记值（`QCborValue`）表示
- `QCborValue::DateTime`：`0x10000`;`QDateTime`：日期和时间戳
- `QCborValue::Url`：`0x10020`;`QUrl`：URL 或 URI
- `QCborValue::RegularExpression`：`0x10023`;`QRegularExpression`：正则表达式的模式
- `QCborValue::Uuid`：`0x10025`;`QUuid`：UUID

### `QCborValue::QCborValue()`

**作用与语义：**

创建`Undefined`类型的QCborValue。
CBOR 未定义值用于表示缺失信息，通常是由于之前操作未按预期完成的结果。`QCborArray` 和 `QCborMap` API 也用它们表示未找到搜索的项目。
未定义的值由未定义简单类型表示。因此，未定义值的QCborValues对`isSimpleType()`和 `isSimpleType(QCborSimpleType::Undefined)`也会返回true。
未定义值与零值不同。
未定义值的 QCborValue 对象也不同于无效的 QCborValue 对象。API 不会生成无效的 QCborValue，但它们可能因解析错误而存在。

### `QCborValue::QCborValue(QCborSimpleType st)`

**作用与语义：**

创建简单类型`st`的QCborValue。该类型之后可以通过`toSimpleType()`和`isSimpleType`（st）检索。
CBOR 简单类型是指没有任何关联值的类型，例如 C 的 `std::nullptr_t` 类型，其唯一可能的值是 `nullptr`。
如果`st` `QCborSimpleType::Null`，所得的QCborValue类型为`Null`，`QCborSimpleType::Undefined`亦然。如果`st`为`QCborSimpleType::False`或`QCborSimpleType::True`，则生成的QCborValue将是一个包含虚假值或真值的布尔值。
该函数可用于API中未定义的简单类型。例如，要创建具有简单类型12的QCborValue，可以写成：
简单类型应在发布规范前不使用，因为其他实现可能无法正确支持。简单类型值24至31为保留，不得使用。
`isSimpleType()`，`isNull()`，`isUndefined()`，`isTrue()`，`isFalse()`。

**官方示例：**

```cpp
 QCborValue value(QCborSimpleType(12));
```

### `QCborValue::QCborValue(QCborValue::Type t_)`

**作用与语义：**

创建类型为`t_`的QCborValue。与此类类型关联的值（如果有的话）将默认构造。

### `QCborValue::QCborValue(QStringView s)`

**作用与语义：**

创建字符串值为`s`的QCborValue。该值之后可以通过`toString()`检索。

### `QCborValue::QCborValue(bool b)`

**作用与语义：**

创建一个布尔值`b`的QCborValue。该值之后可以通过`toBool()`检索。
内部，CBOR 布尔由一对类型表示，一个表示真，一个表示假。因此，布尔 QCborValues 对 `isSimpleType()` 和 `isSimpleType(QCborSimpleType::False)` 或 `isSimpleType(QCborSimpleType::True)` 中的一个返回为真。

### `QCborValue::QCborValue(const QByteArray &ba)`

**作用与语义：**

创建带有字节数组值`ba`的QCborValue。该值之后可以通过`toByteArray()`检索。

### `QCborValue::QCborValue(QCborArray &&a)`

**作用与语义：**

创建与数组 `a` 的 数组 `QCborValue`。数组之后可以用 `toArray()` 检索。

### `QCborValue::QCborValue(QCborMap &&m)`

**作用与语义：**

创建与数组 `a` 的 数组 `QCborValue`。数组之后可以用 `toArray()` 检索。

### `[explicit] QCborValue::QCborValue(const QDateTime &dt)`

**作用与语义：**

用`m`的地图创建`QCborValue`。之后可以用`toMap()`获取该地图。

### `[explicit] QCborValue::QCborValue(const QRegularExpression &rx)`

**作用与语义：**

用`m`的地图创建`QCborValue`。之后可以用`toMap()`获取该地图。

### `QCborValue::QCborValue(const QString &s)`

**作用与语义：**

创建一个带有日期/时间扩展类型的QCborValue对象，包含`dt`所表示的值。该值之后可以通过`toDateTime()`检索。
CBOR 日期/时间类型是使用标签的扩展类型：要么是字符串（ISO 日期格式）标记为`DateTime`，要么是数字（自 1970 年初以来的秒数，UTC），标记为 `UnixTime_t`。解析 CBOR 流时，QCborValue 会将 `UnixTime_t` 转换为基于字符串的类型。

### `[explicit] QCborValue::QCborValue(const QUrl &url)`

**作用与语义：**

创建一个正则表达式模式扩展类型 QCborValue 对象，包含 `rx` 表示的值。该值之后可以通过 `toRegularExpression()` 检索。
CBOR 正则表达式类型是一种扩展类型，由标记为 `RegularExpression` 的字符串表示。注意，CBOR 正则表达式仅存储模式，因此`QRegularExpression`对象可能携带的任何标志都会丢失。

### `[explicit] QCborValue::QCborValue(const QUuid &uuid)`

**作用与语义：**

创建字符串值为`s`的QCborValue。该值之后可以通过`toString()`检索。

### `QCborValue::QCborValue(double d)`

**作用与语义：**

创建一个 URL 扩展类型 QCborValue 对象，包含 `url` 表示的值。该值之后可以通过 `toUrl()` 检索。
CBOR URL 类型是一种扩展类型，由标记为 `Url` 的字符串表示。

### `QCborValue::QCborValue(qint64 i)`

**作用与语义：**

创建UUID扩展类型的QCborValue对象，包含`uuid`所表示的值。该值之后可以通过`toUuid()`检索。
CBOR UUID 类型是一种扩展类型，由标记为 `Uuid` 的字节数组表示。

### `QCborValue::QCborValue(std::nullptr_t)`

**作用与语义：**

创建带有浮点值`d`的QCborValue。该值之后可以通过`toDouble()`检索。
CBOR 浮点值与整数值不同。因此，带有整数的 QCborValue 对象与包含浮点的 QCborValue 对象的比较效果会不同，即使两者中的值是等价的。

### `QCborValue::QCborValue(QCborKnownTags tag, const QCborValue &tv = QCborValue())`

**作用与语义：**

创建一个整数值为`i`的QCborValue。该值之后可以通过`toInteger()`检索。
CBOR 整数值与浮点值不同。因此，带有整数的 QCborValue 对象与包含浮点的 QCborValue 对象的比较效果会不同，即使两者中的值是等价的。

### `QCborValue::QCborValue(QLatin1StringView s)`

**作用与语义：**

创建`Null`类型的QCborValue。
CBOR 空值用于表示未提供的可选值。它们与未定义值不同，空值通常不是之前错误或问题的结果。

### `[noexcept] QCborValue::QCborValue(const QCborValue &other)`

**作用与语义：**

为标签值 `tag` 表示的扩展类型创建`QCborValue`，标记值 `tv`。标签可以通过 `tag()` 检索，标记值则用 `taggedValue()` 检索。

### `[noexcept] QCborValue::QCborValue(QCborValue &&other)`

**作用与语义：**

为标签值 `tag` 表示的扩展类型创建`QCborValue`，标记值 `tv`。标签可以通过 `tag()` 检索，标记值则用 `taggedValue()` 检索。

### `[noexcept] QCborValue::~QCborValue()`

**作用与语义：**

丢弃当前`QCborValue`对象并释放所有相关资源。

### `int QCborValue::compare(const QCborValue &other) const`

**作用与语义：**

比较该值与`other`，返回一个整数，表示该值应在 之前排序（结果为负）还是在 `other` 之后排序（如果结果为正）。如果该函数返回 0，则两个值相等且内容相同。
如果每个`QCborValue`包含数组或映射，比较是递归到其内元素的。
`QCborValue`比较一个包含扩展类型（如`Url`和`Url`）及其等价标记表示的`QCborValue`。例如，以下表达式为真：
请注意，像 `QUrl` 和 `QDateTime` 这样的 Qt 类型会对其参数进行规范化并进行其他修改。上述表达式之所以成立，是因为右侧的字符串是左侧`QCborValue`的归一化值。例如，如果“https”部分在两侧都是大写字母，比较将失败。有关`QCborValue`执行的规范化信息，请参阅采用该 Qt 类型的构造者的文档。
CBOR 中的排序顺序在 RFC 7049，第 3.9 节中定义，该节讨论了遵循规范编码时对映射中键的排序。根据规范，“排序是在键数据项表示的字节上进行”，并列出了以下后果：
- “如果两个键长度不同，较短的键排序得更早;”
- “如果两个键长度相同，按字节顺序排较小的键会更早排序。”
这导致了QCborValues的排序结果，该函数的结果与后来通过比较包含元素后检索的结果不同。例如，包含字符串“zzz”的`QCborValue`会在字符串“foobar”的`QCborValue`之前排序，尽管在`QStrings`或`QByteArrays`比较时，“zzz”排序是在“foobar”之后（字典顺序）。
规范并未明确说明不同类型值应执行何种排序顺序（说明排序不应“关注主要类型3/5位的拆分”）。`QCborValue`假设类型也应排序。`QCborValue::Type`枚举的数值按此顺序排列，扩展类型除外，后者与其标记对应物比较。
注意：排序顺序为初步，可能会变动。应用暂时不应依赖该函数返回的顺序。

**官方示例：**

```cpp
 QCborValue(QUrl("https://example.com")) == QCborValue(QCborKnownTags::Url, "https://example.com");
```

### `[static] QCborValue QCborValue::fromCbor(QCborStreamReader &reader)`

**作用与语义：**

从`reader`中发现的CBOR流中解码一个项，并返回等价的表示。该函数是递归的：如果该项是映射或数组，它会解码该映射或数组中的所有项，直到最外层的对象完成。
该函数不必用于`QCborStreamReader`的根元素。例如，以下代码展示了如何跳过文件开头的CBOR签名标签：
返回的值可能部分完整，且即使解码失败，也无法与有效`QCborValue`区分。为了判断是否存在错误，检查`reader.lastError()`是否表示错误条件。该函数在第一次错误后立即停止解码。

**官方示例：**

```cpp
 if (reader.isTag() && reader.toTag() == QCborKnownTags::Signature)
     reader.next();

 QCborValue contents = QCborValue::fromCbor(reader);
```

### `[static] QCborValue QCborValue::fromCbor(const QByteArray &ba, QCborParserError *error = nullptr)`

**作用与语义：**

从字节数组 `ba` 中发现的 CBOR 流中解码一个项目，并返回等价的表示。该函数是递归的：如果该项目是映射或数组，它会解码该映射或数组中的所有项目，直到最外层对象完成。
该函数会将`error`指向的对象中的错误状态（如有）存储，以及错误发生位置的偏移量。如果没有发生错误，则`NoError`存储错误状态和消耗的字节数（即存储第一个未使用的字节的偏移量）。利用这些信息可以解析可能存在于同一字节数组中的更多数据。
返回的值可能部分完整，且即使解码失败，也无法与有效`QCborValue`区分。要判断是否存在错误，检查`error`中是否存储了错误。该函数在第一次错误后立即停止解码。

### `[static] QCborValue QCborValue::fromCbor(const quint8 *data, qsizetype len, QCborParserError *error = nullptr)`

**作用与语义：**

将`len`字节的`data`转换为`QByteArray`，然后调用该函数的超载，接受`QByteArray`，如果提供，也传递`error`。

### `[static] QCborValue QCborValue::fromJsonValue(const QJsonValue &v)`

**作用与语义：**

将`v`中包含的 JSON 值转换为对应的 CBOR 值并返回。从 JSON 转换为 CBOR 时不会丢失数据，因为 CBOR 类型集比 JSON 更丰富。此外，使用该函数转换为 CBOR 的值可以通过 `toJsonValue()` 转换为 JSON，且不会丢失数据。
下表列出了 JSON 类型映射到 CBOR 类型的情况：
- `JSON Type`：CBOR 类型
- `Bool`：布尔
- `Number`：整数（如果数字无分数且处于`qint64`范围内）或双倍
- `String`：弦
- `Array`：阵列
- `Object`：地图
- `Null`：无效
`QJsonValue`也可以是未定义的，表示之前的操作未完成（例如，寻找对象中不存在的键）。未定义的值不是JSON类型，可能不会出现在JSON数组和对象中，但如果对应的`QJsonValue`未定义，该函数会返回`QCborValue`未定义值。

### `[static] QCborValue QCborValue::fromVariant(const QVariant &variant)`

**作用与语义：**

将`QVariant` `variant`转换成`QCborValue`并退回。
QVariant可能包含大量不同的元类型列表，其中许多在CBOR中没有对应的表示。这包括所有用户自定义的元类型。在准备使用CBOR传输时，建议仔细编码每个值，以防止表示丢失。
下表列出了该函数将应用的转换：
- `Qt (C++) type`：CBOR 类型
- `invalid (QVariant())`：未定义
- `bool`：布尔
- `std::nullptr_t`：无效
- `short`、`ushort`、`int`、`uint`、`qint64`：整数
- `quint64`：整数，或在qint64范围之外时为双倍
- `float`，`double`：双倍
- `QByteArray`：`ByteArray`
- `QDateTime`：`DateTime`
- `QCborSimpleType`：简单型
- `QJsonArray`：数组，使用 QCborArray：：formJsonArray() 进行转换
- `QJsonDocument`：数组或映射
- `QJsonObject`：地图，使用`QCborMap::fromJsonObject()`转换
- `QJsonValue`：使用`fromJsonValue()`转换
- `QRegularExpression`：`RegularExpression`
- `QString`：弦
- `QStringList`：阵列
- `QVariantHash`：地图
- `QVariantList`：数组
- `QVariantMap`：地图
- `QUrl`：网址
- `QUuid`：乌伊德
如果 返回 `QVariant::isNull()`，则返回或插入一个空 `QCborValue`，无论 `QVariant` 携带的类型如何，都会返回或插入该列表或对象。注意 Qt 6.0 中影响 `QVariant::isNull()` 的行为变化也影响该函数。
对于上述未列出的其他类型，通常会尝试转换为字符串，但不总是通过调用`QVariant::toString()`。如果转换失败，该值将被未定义的CBOR值替代。注意，大多数类型`QVariant::toString()`也是有损的。
请注意，通过`QVariant::toString()`的转换可能随时发生变化。未来`QVariant`和`QCborValue`都可能扩展以支持更多类型，这将导致该函数执行转换的方式发生变化。

### `bool QCborValue::isArray() const`

**作用与语义：**

如果该`QCborValue`属于数组类型，则返回真。数组值可以通过`toArray()`检索。

### `bool QCborValue::isBool() const`

**作用与语义：**

如果该`QCborValue`是布尔值，则返回真值。该值可用`toBool()`检索。

### `bool QCborValue::isByteArray() const`

**作用与语义：**

如果该`QCborValue`属于字节数组类型，则返回真。字节数组值可用`toByteArray()`检索。

### `bool QCborValue::isContainer() const`

**作用与语义：**

如果`QCborValue`是数组或映射，则此便利函数返回true。

### `bool QCborValue::isDateTime() const`

**作用与语义：**

如果该`QCborValue`属于日期/时间类型，则返回真值。该值可以通过`toDateTime()`检索。日期/时间是使用标签`DateTime`的扩展类型。
此外，在从CBOR流解码时，`QCborValue`会解释`UnixTime_t`值标签并将其转换为对应的日期/时间。

### `bool QCborValue::isDouble() const`

**作用与语义：**

如果该`QCborValue`为浮点类型，则返回真值。该值可用`toDouble()`检索。

### `bool QCborValue::isFalse() const`

**作用与语义：**

如果该`QCborValue`是带有假值的布尔，则返回真。该函数存在是因为内部CBOR布尔作为两个独立类型存储，一个为真，一个为假。

### `bool QCborValue::isInteger() const`

**作用与语义：**

如果该`QCborValue`为整数类型，则返回真值。整数值可用`toInteger()`检索。

### `bool QCborValue::isInvalid() const`

**作用与语义：**

如果该`QCborValue`没有任何有效类型，则返回为真。无效的QCbor值与未定义值的值不同，通常代表译码错误。

### `bool QCborValue::isMap() const`

**作用与语义：**

如果该 `QCborValue` 是映射类型，则返回 true。映射值可用 `toMap()` 检索。

### `bool QCborValue::isNull() const`

**作用与语义：**

如果该`QCborValue`为空类型，则返回为真。
CBOR 空值用于表示未提供的可选值。它们与未定义值不同，空值通常不是之前错误或问题的结果。
空值与未定义值和无效`QCborValue`对象不同。API不会生成无效的QCborValue，但它们可能因解析错误而存在。

### `bool QCborValue::isRegularExpression() const`

**作用与语义：**

如果该`QCborValue`包含正则表达式的模式，则返回为真。该模式可用 `toRegularExpression()` 检索。

### `bool QCborValue::isSimpleType() const`

**作用与语义：**

如果该`QCborValue`属于 CBOR 简单类型之一，则返回为真。该类型本身后来可以通过 `type()` 检索，即使是 API 中没有枚举的类型。它们也可以通过 `isSimpleType`（QCborSimpleType） 重载检查。

### `bool QCborValue::isSimpleType(QCborSimpleType st) const`

**作用与语义：**

如果该`QCborValue`为简单类型，返回真;`toSimpleType()`返回`st`，否则返回假。该函数可用于检查任何CBOR简单类型，即使是API中没有枚举的类型。例如，对于值12的简单类型，你可以写成：

**官方示例：**

```cpp
 value.isSimpleType(QCborSimpleType(12));
```

### `bool QCborValue::isString() const`

**作用与语义：**

如果该`QCborValue`属于字符串类型，则返回真。字符串值可用`toString()`检索。

### `bool QCborValue::isTag() const`

**作用与语义：**

如果该`QCborValue`属于标签类型，则返回真值。标签值可以用`tag()`检索，标记值可以用`taggedValue()`检索。
该函数对于 API 识别的扩展类型也返回为真。对于在 Qt API 更新支持扩展类型之前直接处理的代码，可以通过使用 `taggedValue()` 重建标签标签值对。

### `bool QCborValue::isTrue() const`

**作用与语义：**

如果该`QCborValue`是具有真值的布尔值，则返回真。该函数存在是因为内部CBOR布尔值分为两个独立类型，一个用于假，一个用于真。

### `bool QCborValue::isUndefined() const`

**作用与语义：**

如果该`QCborValue`属于未定义类型，则返回为真。
CBOR 未定义值用于表示缺失信息，通常是由于之前的操作未按预期完成所致。`QCborArray` 和 `QCborMap` API 也使用它们来表示未找到搜索的项目。
未定义值与空值不同。
`QCborValue`未定义值的对象也不同于无效`QCborValue`对象。API不会生成无效的QCborValues，但它们可能因解析错误而存在。

### `bool QCborValue::isUrl() const`

**作用与语义：**

如果该`QCborValue`属于 URL 类型，则返回为真。可以通过 `toUrl()` 检索 URL 值。

### `bool QCborValue::isUuid() const`

**作用与语义：**

如果该`QCborValue`包含UUID，则返回为真。该值可以用`toUuid()`检索。

### `[noexcept] void QCborValue::swap(QCborValue &other)`

**作用与语义：**

将该值与`other`交换。该操作非常快速且从未失败。

### `QCborTag QCborValue::tag(QCborTag defaultValue = QCborTag(-1)) const`

**作用与语义：**

如果该扩展`QCborValue`对象属于标签类型，返回其标签，`defaultValue`否则返回。
CBOR 通过将数字（标签）与存储表示关联来表示扩展类型。该函数返回该数字。要检索表示，请使用 `taggedValue()`。

### `QCborValue QCborValue::taggedValue(const QCborValue &defaultValue = QCborValue()) const`

**作用与语义：**

如果该扩展`QCborValue`对象属于标签类型，返回其标记值，`defaultValue`否则返回。
CBOR 通过将数字（标签）与存储的表示关联来表示扩展类型。该函数返回该表示。要检索标签，请使用 `tag()`。

### `QCborArray QCborValue::toArray(const QCborArray &defaultValue) const`

**作用与语义：**

如果数组类型是，返回存储在本`QCborValue`中的数组值。否则返回`defaultValue`。
注意，该函数不会将其他类型转换为`QCborArray`。

### `bool QCborValue::toBool(bool defaultValue = false) const`

**作用与语义：**

如果该`QCborValue`是布尔类型，则返回存储在该中的布尔值。否则返回`defaultValue`。

### `QByteArray QCborValue::toByteArray(const QByteArray &defaultValue = {}) const`

**作用与语义：**

如果`QCborValue`中字节数组是字节数组类型，则返回该中存储的字节数组值。否则返回`defaultValue`。
注意，该函数不会将其他类型转换为`QByteArray`。

### `QByteArray QCborValue::toCbor(QCborValue::EncodingOptions opt = NoTransformation) const`

**作用与语义：**

将该`QCborValue`对象编码为其 CBOR 表示，使用 `opt` 中指定的选项，返回包含该表示的字节数组。
该函数不会失败，除非该`QCborValue`或包含的任意项（如映射或数组）无效。API通常不会生成无效类型，但可能因解码错误。
默认情况下，该函数不对`QCborValue`中的值进行变换，直接将所有浮点写入双精度（`double`）类型。如果指定了`UseFloat`选项，则对任何在使用该表示时不会损失精度的浮点值使用单精度（`float`）。这包括无穷远和NaN值。
同样，如果指定了`UseFloat16`，如果转换为该函数并未导致精度损失，该函数会尝试使用半精度（`qfloat16`）浮点。对于无穷大和NaN，这总是成立的。
如果指定`UseIntegers`，则对任何包含实际整数的浮点值都使用整数。

### `void QCborValue::toCbor(QCborStreamWriter &writer, QCborValue::EncodingOptions opt = NoTransformation) const`

**作用与语义：**

将该`QCborValue`对象编码为其CBOR表示，使用`opt`中指定的选项，编码给`writer`指定的写入者。例如，同一个写入器可以被多个QCborValues使用，以便在更大数组中编码不同元素。
该函数不会失败，除非该`QCborValue`或包含的任意项（如映射或数组）无效。API通常不会生成无效类型，但可能因译码错误而产生。
默认情况下，该函数不对`QCborValue`中的值进行变换，直接将所有浮点写入双精度（binary64）类型。如果指定了`UseFloat`选项，则对任何在使用该表示法时不会损失精度的浮点值使用单精度（binary32）。这包括无穷大和NaN值。
同样，如果指定`UseFloat16`，该函数会尝试使用半精度（二进制16）浮点，前提是转换为该浮点数不会损失精度。这对无穷大和NaN总是成立。
如果指定了`UseIntegers`，则会对任何包含实际整数的浮点值使用整数。

### `QDateTime QCborValue::toDateTime(const QDateTime &defaultValue = {}) const`

**作用与语义：**

如果该`QCborValue`中存储的日期/时间值是日期/时间扩展类型，则返回该值。否则返回`defaultValue`。
注意，该函数不会将其他类型转换为`QDateTime`。

### `QString QCborValue::toDiagnosticNotation(QCborValue::DiagnosticNotationOptions opts = Compact) const`

**作用与语义：**

创建该 CBOR 对象的诊断符号对应物并返回。`opts` 参数控制符号的方言。诊断符号在调试中非常有用，帮助开发者理解存储在`QCborValue`或 CBOR 流中的值。因此，Qt API 不支持将诊断解析回内存格式或 CBOR 流，尽管表示方式是唯一且可行的。
CBOR 诊断符号由 RFC 7049 第 6 节规定。它是 CBOR 流的文本表示，与 JSON 非常相似，但支持 JSON 中没有的 CBOR 类型。`ExtendedFormat` 标志支持的扩展格式目前存在于一些 IETF 草案中，其格式可能会发生变化。
该函数生成的流的等价表示与`toCbor()`生成的相同，且不提供任何转换选项。这也意味着如果该函数是用`fromCbor()`创建的，该函数可能无法生成用于创建该对象的流的表示，因为该函数可能应用了变换。关于无变换的高保真度流符号，请参见`cbordump`例。

### `double QCborValue::toDouble(double defaultValue = 0) const`

**作用与语义：**

如果浮点值是 Double 类型，则返回该`QCborValue`中存储的浮点值。如果是整数类型，该函数返回将整数值转换为 double。在其他情况下，返回 `defaultValue`。

### `qint64 QCborValue::toInteger(qint64 defaultValue = 0) const`

**作用与语义：**

如果该值是整数类型，返回该`QCborValue`中存储的整数值。如果是 Double 类型，该函数返回将浮点数转换为整数的值。其他情况下，返回 `defaultValue`。

### `QJsonValue QCborValue::toJsonValue() const`

**作用与语义：**

将该`QCborValue`对象转换为等效的 JSON 表示，并返回为 `QJsonValue`。
请注意，CBOR 包含比 JSON 更丰富且更宽的类型集，因此在此转换过程中可能会丢失一些信息。下表比较了 CBOR 类型与 JSON 类型，并指出信息是否可能丢失。
- `CBOR Type`：JSON 类型;注释
- `Bool`：布尔值;不可能导致数据丢失
- `Double`：数字;无穷大和NaN将转换为空值;其他值不丢失数据
- `Integer`：数字;如果整数大于253或小于-253，转换过程中可能发生数据丢失。
- `Null`：无;不可能导致数据丢失
- `Undefined`：空;类型信息丢失
- `String`：字符串;不可能导致数据丢失
- `Byte Array`：字符串;转换为无损编码，如Base64url，但字符串与字节数组的区别已丧失
- `Other simple types`：字符串;类型信息丢失
- `Array`：数组;转换适用于每个包含的值
- `Map`：对象;键转换为字符串;值根据该表进行转换
- `Tags and extended types`：特殊;标签编号本身丢失，标记值转换为 JSON
有关将 CBOR 映射密钥转换为字符串的信息，请参见 `QCborMap::toJsonObject()`。
如果该`QCborValue`包含未定义值，该函数也会返回未定义的`QJsonValue`。注意，JSON 不支持未定义值，未定义的 QJsonValue 是规范的扩展。它们不能被保留在`QJsonArray`或`QJsonObject`中，但可以通过函数返回以表示失败。在其他所有意图和目的上，它们与空值相同。
有些标签会被特殊处理，将被标记值从 CBOR 转换为 JSON。下表列出了这些特殊情况：
- `Tag`：CBOR 类型;变换
- `ExpectedBase64url`：字节数组;将字节数组编码为 Base64url
- `ExpectedBase64`：字节数组;将字节数组编码为 Base64
- `ExpectedBase16`：字节数组;将字节数组编码为十六进制
- `Url`：URL 和字符串;使用 `QUrl::toEncoded()` 将编码规范化为 URL 的完整编码格式
- `Uuid`：Uuid 和字节数组;使用 `QUuid::toString()` 来创建字符串表示

### `QCborMap QCborValue::toMap(const QCborMap &defaultValue) const`

**作用与语义：**

如果映射类型为该映射类型，返回存储在该`QCborValue`中的映射值。否则返回`defaultValue`。
注意，该函数不进行其他类型到`QCborMap`的转换。

### `QRegularExpression QCborValue::toRegularExpression(const QRegularExpression &defaultValue = {}) const`

**作用与语义：**

如果正则表达式模式扩展类型，返回该`QCborValue`中存储的正则表达式值。否则返回`defaultValue`。
注意，该函数不会将其他类型转换为`QRegularExpression`。

### `QCborSimpleType QCborValue::toSimpleType(QCborSimpleType defaultValue = QCborSimpleType::Undefined) const`

**作用与语义：**

如果该类型是简单类型，则返回该`QCborValue`的简单类型。如果不是简单类型，返回`defaultValue`。
以下类型为简单类型，该函数将返回列出的值：
- `QCborValue::False`：`QCborSimpleType::False`
- `QCborValue::True`：`QCborSimpleType::True`
- `QCborValue::Null`：`QCborSimpleType::Null`
- `QCborValue::Undefined`：`QCborSimpleType::Undefined`

### `QString QCborValue::toString(const QString &defaultValue = {}) const`

**作用与语义：**

如果字符串类型为 ，返回该`QCborValue`中存储的字符串值。否则返回  `defaultValue`。
注意，该函数不进行其他类型转换为`QString`。

### `[since 6.10] QAnyStringView QCborValue::toStringView(QAnyStringView defaultValue = {}) const`

**作用与语义：**

如果字符串类型为该字符串类型，返回存储在该`QCborValue`中的字符串值。否则返回`defaultValue`。由于`QCborValue`以US-ASCII、UTF-8或UTF-16格式存储字符串，返回的`QAnyStringView`可能属于这些编码中的任意一种。
该函数不分配内存。返回值有效，直到下一次调用该对象的非const成员函数。如果该对象超出作用域，返回值在下一次调用父CBOR对象（映射或数组）非const成员函数之前有效。
注意，该函数不会将其他类型转换为`QString`。

### `QUrl QCborValue::toUrl(const QUrl &defaultValue = {}) const`

**作用与语义：**

如果该 URL 是 URL 扩展类型，则返回存储在本`QCborValue`中的 URL 值。否则返回 `defaultValue`。
注意，该函数不会将其他类型转换为`QUrl`。

### `QUuid QCborValue::toUuid(const QUuid &defaultValue = {}) const`

**作用与语义：**

如果 UUID 是扩展类型，返回存储在本`QCborValue`中的 UUID 值。否则返回 `defaultValue`。
注意，该函数不会将其他类型转换为`QUuid`。

### `QVariant QCborValue::toVariant() const`

**作用与语义：**

将该值转换为本地 Qt 类型并返回相应的 `QVariant`。
下表列出了QCborValue类型与Qt元类型之间的映射。
- `CBOR Type`：Qt或C类型;注释
- `Integer`：`qint64`
- `Double`：`double`
- `Bool`：`bool`
- `Null`：`std::nullptr_t`
- `Undefined`：无类型（QVariant()）
- `Byte array`：`QByteArray`
- `String`：`QString`
- `Array`：`QVariantList`;递归转换所有值
- `Map`：`QVariantMap`;密钥类型是“串化”
- `Other simple types`：`QCborSimpleType`
- `DateTime`：`QDateTime`
- `Url`：`QUrl`
- `RegularExpression`：`QRegularExpression`
- `Uuid`：`QUuid`
- `Other tags`：特殊;忽略标签，使用该函数转换标记值
注意，CBOR 映射和数组中的值也是通过该函数递归转换的，并被放在 `QVariantMap` 和 `QVariantList` 中。你不会在 QVariants 中找到存储`QCborMap`和`QCborArray`。
QVariantMaps 有字符串键，与 CBOR 不同，因此将`QCborMap`转换为 `QVariantMap` 会意味着对键值进行“串化”步骤。详情请参见 `QCborMap::toJsonObject()`。

### `QCborValue::Type QCborValue::type() const`

**作用与语义：**

返回该`QCborValue`的类型。该类型也可以通过“isXxx”函数之一稍后检索。

### `[noexcept] QCborValue &QCborValue::operator=(const QCborValue &other)`

**作用与语义：**

用`other`的副本替换了这个QCborObject的内容。

### `[noexcept] QCborValue &QCborValue::operator=(QCborValue &&other)`

**作用与语义：**

将`other` `QCborValue`对象的内容移入该对象，并释放该对象的资源。返回对该对象的引用。

### `QCborValueRef QCborValue::operator[](const QString &key)`

**作用与语义：**

返回一个QCborValueRef，可用于读取或修改该映射中的条目，作为映射，并带有给定`key`。当该`QCborValue`为`QCborMap`时，该函数等价于该映射上的匹配算符[]。
返回引用前：如果该`QCborValue`是数组，首先将其转换为映射（使每个索引 `i` `map[i]` `array[i]`，且有效 `array[i]`）;否则，如果不是映射，则将被覆盖为空映射。

### `const QCborValue QCborValue::operator[](const QString &key) const`

**作用与语义：**

如果该`QCborValue`是`QCborMap`，则搜索键匹配`key`的元素。如果映射中没有键匹配的 `key`，或者该`QCborValue`对象不是映射，则返回未定义的值。
该函数等价于：

**官方示例：**

```cpp
 value.toMap().value(key);
```

### `QCborValueRef QCborValue::operator[](QLatin1StringView key)`

**作用与语义：**

返回一个QCborValueRef，可用于读取或修改该映射中的条目，作为映射，并带有给定`key`。当该`QCborValue`为`QCborMap`时，该函数等价于该映射上的匹配算符[]。
返回引用前：如果该`QCborValue`是数组，首先将其转换为映射（使每个索引 `i` `map[i]` `array[i]`，且有效 `array[i]`）;否则，如果不是映射，则将被覆盖为空映射。

### `QCborValueRef QCborValue::operator[](qint64 key)`

**作用与语义：**

返回一个QCborValueRef，可用于读取或修改该项中的元素，作为映射或数组，且给定`key`。当该`QCborValue`是`QCborMap`，或对于0 <= 键 < 0x10000，是`QCborArray`时，该函数等价于该映射或数组上的匹配算子[]。
返回引用前：如果该`QCborValue`是数组但键超出范围，先将数组转换为映射（使每个索引`i` `map[i]` `array[i]`，且有效`array[i]`）;否则，如果不是映射，则会被覆盖为空映射。

### `const QCborValue QCborValue::operator[](QLatin1StringView key) const`

**作用与语义：**

如果该`QCborValue`是`QCborMap`，则搜索键匹配`key`的元素。如果映射中没有键匹配的 `key`，或者该`QCborValue`对象不是映射，则返回未定义的值。
该函数等价于：

**官方示例：**

```cpp
 value.toMap().value(key);
```

### `const QCborValue QCborValue::operator[](qint64 key) const`

**作用与语义：**

如果`QCborValue`是`QCborMap`，则搜索键匹配`key`的元素。如果是`QCborArray`，返回索引为`key`的元素。如果数组或映射中没有匹配值，或者该`QCborValue`对象不是数组或映射，返回未定义的值。

### `[noexcept] bool operator!=(const QCborValue &lhs, const QCborValue &rhs)`

**作用与语义：**

比较 `lhs` 和 `rhs`，如果内容不同则返回 true，否则返回 false。如果每个 `QCborValue` 包含数组或映射，则比较会递归到其中包含的元素。有关 Qt 中 CBOR 相等性的更多信息，请参见 `QCborValue::compare()`。

### `[noexcept] bool operator<(const QCborValue &lhs, const QCborValue &rhs)`

**作用与语义：**

比较 `rhs` 和 `rhs`，如果 `lhs` 应该排在 `rhs` 之前则返回 true，否则返回 false。如果每个 `QCborValue` 包含数组或映射，则比较将递归到其中包含的元素。有关 CBOR 排序顺序的更多信息，请参见 `QCborValue::compare()`。

### `[noexcept] bool operator<=(const QCborValue &lhs, const QCborValue &rhs)`

**作用与语义：**

比较 `lhs` 和 `rhs`，如果 `lhs` 应该排在 `rhs` 之前或等于 `rhs`，则返回 true，否则返回 false。如果每个 `QCborValue` 包含数组或映射，则比较会递归到其中的元素。
有关 CBOR 排序顺序的更多信息，请参见 `QCborValue::compare()`。

### `[noexcept] bool operator==(const QCborValue &lhs, const QCborValue &rhs)`

**作用与语义：**

比较 `lhs` 和 `rhs`，如果它们内容相同则返回 true，否则返回 false。如果每个 `QCborValue` 包含数组或映射，则比较会递归到其中的元素。有关 Qt 中 CBOR 相等性的更多信息，请参见 `compare()`。

### `[noexcept] bool operator>(const QCborValue &lhs, const QCborValue &rhs)`

**作用与语义：**

比较 `lhs` 和 `rhs`，如果 `lhs` 应该排在 `rhs` 之后则返回 true，否则返回 false。如果每个 `QCborValue` 包含数组或映射，则比较将递归到其中包含的元素。有关 CBOR 排序顺序的更多信息，请参见 `QCborValue::compare()`。

### `[noexcept] bool operator>=(const QCborValue &lhs, const QCborValue &rhs)`

**作用与语义：**

比较 `lhs` 和 `rhs`，如果 `lhs` 应该排在 `rhs` 之后或等于 `rhs`，则返回 true，否则返回 false。如果每个 `QCborValue` 包含数组或映射，则比较会递归到其中的元素。
有关 CBOR 排序顺序的更多信息，请参见 `QCborValue::compare()`。

### `enum DiagnosticNotationOption { Compact, LineWrapped, ExtendedFormat }`

**作用与语义：**

该枚举用于选项参数 to `toDiagnosticNotation()`，以修改输出格式。
- `QCborValue::Compact`：`0x00`;不使用任何换行，形成紧凑的表示。
- `QCborValue::LineWrapped`：换行`0x01`;每行一个换行`QCborValue`。
- `QCborValue::ExtendedFormat`：`0x02`;使用了一些RFC 7049中没有的选项来表示数值。这些选项可能会发生变化。
目前，`ExtendedFormat`将改变字节数组的表示方式。没有它，字节数组总是十六进制编码且没有空格。有了它，`QCborValue::toCbor()`会根据上下文使用带空格的十六进制、base64或base64url编码。
DiagnosticNotationOptions 类型是 QFlags 的 typedef<DiagnosticNotationOption>。它存储 DiagnosticNotationOption 值的 OR 组合。

### `flags DiagnosticNotationOptions`

**作用与语义：**

该枚举用于选项参数 to `toDiagnosticNotation()`，以修改输出格式。
- `QCborValue::Compact`：`0x00`;不使用任何换行，形成紧凑的表示。
- `QCborValue::LineWrapped`：换行`0x01`;每行一个换行`QCborValue`。
- `QCborValue::ExtendedFormat`：`0x02`;使用了一些RFC 7049中没有的选项来表示数值。这些选项可能会发生变化。
目前，`ExtendedFormat`将改变字节数组的表示方式。没有它，字节数组总是十六进制编码且没有空格。有了它，`QCborValue::toCbor()`会根据上下文使用带空格的十六进制、base64或base64url编码。
DiagnosticNotationOptions 类型是 QFlags 的 typedef<DiagnosticNotationOption>。它存储 DiagnosticNotationOption 值的 OR 组合。

### `enum EncodingOption { NoTransformation, UseFloat, UseFloat16, UseIntegers }`

**作用与语义：**

该枚举用于`toCbor()`的选项参数，修改编码器的行为。
- `QCborValue::NoTransformation`：`0`;（默认）不执行变换。
- `QCborValue::UseFloat`：`0x02`;告诉编码器尽可能使用 IEEE 754 单精度浮点（即 `float`）。
- `QCborValue::UseFloat16`：`UseFloat | 0x04`;告诉编码器尽可能使用IEEE 754半精度浮点（即`qfloat16`）。暗示`UseFloat`。
- `QCborValue::UseIntegers`：`0x08`;每当类型为`Double`的值包含整数时，指示编码器使用整数。
编码流为规范格式是必须使用`UseFloat16`，但并非其他必要条件。
EncodingOptions 类型是 QFlags 的 typedef<EncodingOption>。它存储 EncodingOption 值的 OR 组合。

### `flags EncodingOptions`

**作用与语义：**

该枚举用于`toCbor()`的选项参数，修改编码器的行为。
- `QCborValue::NoTransformation`：`0`;（默认）不执行变换。
- `QCborValue::UseFloat`：`0x02`;告诉编码器尽可能使用 IEEE 754 单精度浮点（即 `float`）。
- `QCborValue::UseFloat16`：`UseFloat | 0x04`;告诉编码器尽可能使用IEEE 754半精度浮点（即`qfloat16`）。暗示`UseFloat`。
- `QCborValue::UseIntegers`：`0x08`;每当类型为`Double`的值包含整数时，指示编码器使用整数。
编码流为规范格式是必须使用`UseFloat16`，但并非其他必要条件。
EncodingOptions 类型是 QFlags 的 typedef<EncodingOption>。它存储 EncodingOption 值的 OR 组合。

### `QCborValue(const QCborArray &a)`

**作用与语义：**

创建包含 `s` 查看的 Latin-1 字符串的 QCborValue。该值之后可以通过 `toString()` 检索。

### `QCborValue(const QCborMap &m)`

**作用与语义：**

将`other`的内容复制到该对象中。

### `QCborValue(QCborTag tag, const QCborValue &tv = QCborValue())`

**作用与语义：**

将`other` QCborValue 对象的内容移入该对象，释放该对象的资源。

### `QCborArray toArray() const`

**作用与语义：**

如果数组类型是，返回存储在本`QCborValue`中的数组值。否则返回`defaultValue`。
注意，该函数不会将其他类型转换为`QCborArray`。

### `QCborMap toMap() const`

**作用与语义：**

如果映射类型为该映射类型，返回存储在该`QCborValue`中的映射值。否则返回`defaultValue`。
注意，该函数不进行其他类型到`QCborMap`的转换。

### `QCborValue fromCbor(const char *data, qsizetype len, QCborParserError *error = nullptr)`

**作用与语义：**

将`len`字节的`data`转换为`QByteArray`，然后调用该函数的超载，接受`QByteArray`，如果提供，也传递`error`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QCborValue` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
