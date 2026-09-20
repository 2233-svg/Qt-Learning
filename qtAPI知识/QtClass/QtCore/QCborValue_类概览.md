# QCborValue 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCborValue>`  
> 模块：`Qt6::Core`  
> 相关类型：`QCborArray`、`QCborMap`、`QCborStreamReader`、`QCborStreamWriter`、`QCborParserError`

## 它解决什么问题

`QCborValue` 是 Qt 对一项 CBOR 数据的通用内存表示。它相当于 CBOR 世界里的“带类型的值”：一个对象可以是整数、文本、二进制字节串、数组、映射、布尔值、`null`、标签值等。

当程序要处理二进制协议、设备上报、签名载荷、配置缓存或网络消息时，直接面对字节流很难做字段访问和类型校验；全部先转成 `QVariant` 又会丢掉一些 CBOR 语义。`QCborValue` 正好放在两者之间：既保留 CBOR 的主要类型和标签，又能方便地构造、访问、比较和编码。

它和 `QJsonValue` 很像，但能力边界更宽：

- CBOR 的映射键可以是任意 `QCborValue`，不局限于字符串。
- 可以区分 UTF-8 文本和原始 `QByteArray`。
- 有 `QCborTag`，可表达日期、URL、UUID、正则等带语义的扩展值。
- `Undefined` 是合法的 CBOR 值，而不只是“没有找到”。

## 先理解值的类型

默认构造的 `QCborValue` 是 `Undefined`。`QCborValue(nullptr)` 才是 `Null`。两者都“没有有效载荷”，但协议含义不同：

- `Null`：明确传递“空值”，类似 JSON 的 `null`。
- `Undefined`：CBOR 的一个合法 simple value；只读数组越界或 map 查无键时也会返回它。
- `Invalid`：Qt 内部或错误状态的无效类型，不应把它当成普通协议字段。

因此，仅通过 `isUndefined()` 不能判断“发送方真的编码了 undefined”还是“本地查询没找到”。需要区分这两种情况时，先用 `QCborMap::contains()`、迭代器或数组范围检查判断是否存在。

`Type` 中最常用的值是：

- `Integer`：范围为 `qint64` 的整数。
- `Double`：浮点数；CBOR 中过大的无符号整数也可能被解码为它。
- `ByteArray` 与 `String`：二进制内容与文本不能混为一谈。
- `Array` 与 `Map`：嵌套结构。
- `Tag`：未知或通用标签；`DateTime`、`Url`、`RegularExpression`、`Uuid` 是 Qt 识别出的常见带标签类型。
- `False`、`True`、`Null`、`Undefined`：CBOR simple values。

## 典型使用场景

### 1. 构造一份协议载荷

`QCborMap` 负责字段集合，`QCborValue` 负责把这个 map 包装成可编码的根值。

```cpp
#include <QCborMap>
#include <QCborValue>

QCborMap packet;
packet.insert("deviceId", "sensor-17");
packet.insert("enabled", true);
packet.insert("samples", QCborArray{21.5, 21.8});

const QByteArray bytes = QCborValue(packet).toCbor();
```

这里 `QByteArray` 若直接作为值插入，会编码为 CBOR byte string；若业务要传文字，请显式使用 `QString`，避免消费者把二进制当文本解释。

### 2. 接收不可信 CBOR 并严格检查

解码成功不等于输入可信。应同时检查解析错误、根类型、字段是否存在和每个字段的类型。

```cpp
#include <QCborMap>
#include <QCborParserError>
#include <QCborValue>

QCborParserError parseError;
const QCborValue root = QCborValue::fromCbor(payload, &parseError);

if (parseError.error != QCborError::NoError || !root.isMap())
    return;

const QCborMap map = root.toMap();
if (!map.contains("deviceId") || !map.value("deviceId").isString())
    return;

const QString deviceId = map.value("deviceId").toString();
```

`fromCbor()` 在失败时可能返回部分构造的、看起来仍然合法的值，因此不能只写 `root.isMap()`；必须检查 `parseError.error`。成功时 `parseError.offset` 是第一个未消费字节的位置，可用来连续解析粘在同一缓冲区中的多个 CBOR 项。

### 3. 解开已知标签

标签的重点不是“值是一个字符串”，而是“这个字符串在协议里是什么”。例如 URL 标签会被 Qt 表示为 `Url`。

```cpp
QCborValue value(QUrl("https://example.com/api"));

if (value.isUrl()) {
    const QUrl endpoint = value.toUrl();
    // 使用 endpoint 发起请求或保存配置
}
```

处理通用标签时，先确认 `isTag()`，再读取 tag 号与被包裹的值：

```cpp
if (value.isTag() && value.tag() == QCborKnownTags::Signature) {
    const QCborValue signedPart = value.taggedValue();
    // 根据协议验证 signedPart
}
```

## 解析和编码的关键边界

### `fromCbor()` 只读取一个顶层项

传入 `QByteArray` 的重载会从开头递归读取一个完整顶层项。若缓冲区后面还有下一项，成功后的 `offset` 指向下一项的开头；这适合按帧拼接的协议。`const char *` 与 `const quint8 *` 重载只是先按给定长度包装输入，再走同一条解析路径。

传入 `QCborStreamReader` 的重载适合流式输入，但同样要在调用后检查 `reader.lastError()`。不要因为拿到了 `QCborValue` 就假设整个嵌套内容已正确解析。

### 大整数和数值转换

`QCborValue` 的 `Integer` 只容纳 `qint64`。CBOR 里的无符号整数若超出这个范围，解码时会变成 `Double`，最多可能损失 11 位精度。存放金额、序列号、哈希片段等要求精确的超大数时，应在协议层使用 byte string 或十进制字符串，而不是期待 `Double` 保真。

`toInteger()` 会接受 `Integer`，也会把 `Double` 强制转换成整数；`toDouble()` 同理会把整数转换为浮点。因此在校验外部输入时，先用 `isInteger()` 或 `isDouble()` 确认原始类型，再转换，不能把默认值当成类型校验结果。

### `toArray()` 和 `toMap()` 返回的是值

它们会返回一个 `QCborArray` 或 `QCborMap` 副本。修改这个副本后，原 `QCborValue` 不会自动更新，必须再写回：

```cpp
QCborValue root(QCborMap{{"retries", 1}});
QCborMap object = root.toMap();
object.insert("timeoutMs", 3000);
root = object;
```

对于已知就是 map 的根值，直接保存 `QCborMap` 往往更清楚。只有需要在“标量、数组、映射之间任选其一”的接口边界，才优先用 `QCborValue`。

### 非 const `operator[]` 会改变原值

`value["name"]` 的非 const 版本返回 `QCborValueRef`，用于读写 map 成员。若 `value` 不是 map：

- 原来是数组时，字符串键访问会将数组转换为以索引为键的 map。
- 原来是其他类型时，会被覆盖成空 map。
- 用整数访问数组时，仅当索引在现有范围内保留数组；越界会把数组转换为 map。

这是一种方便的“就地建结构”语法，但对解析得到的值做只读查询时很危险。读取请让对象保持 `const`，或使用 `const QCborMap` 的 `value()`；修改时再显式使用非 const 访问。

`QCborValueRef` 是容器元素的代理，不是独立的长期值。不要把它保存到容器修改、销毁或脱离作用域之后；需要持久保存时转换成 `QCborValue`。

### 诊断文本不能当作反序列化格式

`toDiagnosticNotation()` 很适合日志和调试，能够展示 JSON 没有的 tag、byte string 等类型；Qt 不提供把这段文字再解析回 `QCborValue` 的 API。`ExtendedFormat` 的具体写法也可能随 Qt 或规范草案变化，所以它不能作为稳定存储格式或跨进程协议。

## 互转时会损失什么

`fromJsonValue()` 和 `toJsonValue()` 用于 JSON 边界，但不是无损转换。CBOR 的 byte string、tag、`Undefined`、非字符串 map 键等没有一一对应的 JSON 表示。与 `QVariant` 往返也要按实际元类型确认，尤其是跨语言或数据库接口。

`QRegularExpression` 的 CBOR 表示只保存 pattern，不保存 pattern options。若正则选项也是业务语义，应额外用 map 字段编码。

## 编码选项怎么选

`toCbor()` 默认使用 `NoTransformation`，即按当前值的类型编码。需要特殊输出时使用 `EncodingOptions`：

- `SortKeysInMaps`：按规范顺序编码 map 键；做签名、哈希或需要可重复字节序列时常用。
- `UseFloat`：可表示时用单精度 float，优先减小体积但会降低精度。
- `UseFloat16`：可表示时进一步尝试半精度；仅适合精度容忍度明确的传感器或图形数据。
- `UseIntegers`：浮点数没有小数部分且能表示为整数时，编码为整数。
- `NoTransformation`：不做上述转换，最适合作为默认的语义保留模式。

这些选项决定字节表示而非业务类型系统。需要验签的协议应把选项、键排序规则和版本约定写进协议，而不是让每个调用点自行选择。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `Type` | 表示当前值的实际 CBOR 类型及 Qt 识别的扩展类型。 | 用 `type()` 或 `isXxx()` 判断原始类型；不要靠转换函数的默认值猜类型。 |
| 枚举值 | `Integer` | 表示 `qint64` 整数。 | 大于 `qint64` 的 CBOR 无符号数不能以此类型保留。 |
| 枚举值 | `ByteArray` | 表示原始二进制字节串。 | 它不是文本；与 `String` 的协议语义不同。 |
| 枚举值 | `String` | 表示 UTF-8 文本字符串。 | 二进制标识符应使用 `QByteArray`。 |
| 枚举值 | `Array` | 表示 `QCborArray`。 | `toArray()` 取回的是值，改完须写回。 |
| 枚举值 | `Map` | 表示 `QCborMap`。 | CBOR map 键可不是字符串，遍历时不要假设键类型。 |
| 枚举值 | `Tag` | 表示普通或未知 CBOR 标签。 | 先 `isTag()`，再读 `tag()` 与 `taggedValue()`。 |
| 枚举值 | `False`、`True` | 表示两个布尔 simple value。 | 一般使用 `isBool()` 和 `toBool()`。 |
| 枚举值 | `Null` | 表示明确的空值。 | 与默认构造出的 `Undefined` 不同。 |
| 枚举值 | `Undefined` | 表示合法的 CBOR undefined simple value。 | 查找失败也返回它；需要结合 `contains()` 或迭代器判断。 |
| 枚举值 | `Double` | 表示 IEEE 浮点数。 | 不可承担精确的大整数或金额。 |
| 枚举值 | `DateTime`、`Url`、`RegularExpression`、`Uuid` | 表示 Qt 识别的带标签扩展值。 | 和 JSON、QVariant 往返前确认扩展语义是否保留。 |
| 枚举值 | `Invalid` | 表示无效类型。 | 不作为正常数据字段使用。 |
| 编码选项 | `SortKeysInMaps` | 编码时按规范顺序排序 map 键。 | 签名或哈希场景要让所有参与方使用相同规则。 |
| 编码选项 | `UseFloat` | 可行时用单精度编码浮点数。 | 会牺牲精度，不能仅因体积小就默认开启。 |
| 编码选项 | `UseFloat16` | 可行时使用半精度浮点编码。 | 精度范围更窄，适合明确可容忍误差的数据。 |
| 编码选项 | `UseIntegers` | 将可表示为整数的浮点编码成整数。 | 接收端若依赖“原本是 double”的类型信息，不要使用。 |
| 编码选项 | `NoTransformation` | 不执行额外编码变换。 | 默认值；通常最符合内存中已有的类型语义。 |
| 诊断选项 | `Compact` | 生成无换行的诊断文本。 | 适合单行日志。 |
| 诊断选项 | `LineWrapped` | 生成带换行的诊断文本。 | 适合人工查看复杂嵌套内容。 |
| 诊断选项 | `ExtendedFormat` | 使用扩展诊断表示法。 | 具体格式可能变化，不能作为稳定交换格式。 |
| 构造 | `QCborValue()` | 构造 `Undefined` 值。 | 不等于 `Null`。 |
| 构造 | `QCborValue(Type type)` | 按指定 `Type` 建立值。 | 多用于明确构造 simple 或特殊类型；普通数据优先使用对应值构造。 |
| 构造 | `QCborValue(std::nullptr_t)` | 构造 `Null` 值。 | 使用 `nullptr`，不要用默认构造代替。 |
| 构造 | `QCborValue(bool value)` | 构造 `True` 或 `False`。 | 读取时可用 `isBool()` 保证输入确实是布尔类型。 |
| 构造 | `QCborValue(qint64 value)` | 构造整数值。 | 只覆盖有符号 64 位范围。 |
| 构造 | `QCborValue(double value)` | 构造双精度值。 | 对精确数字不要以浮点作为传输载体。 |
| 构造 | `QCborValue(QCborSimpleType value)` | 构造任意 simple value。 | 未定义的 simple 值只应用于确有互操作规范的场景。 |
| 构造 | `QCborValue(const QByteArray &value)` | 构造 byte string。 | 它不会按文本处理字节。 |
| 构造 | `QCborValue(const QString &value)` | 构造文本字符串。 | 需要避免隐式 ASCII 转换歧义时使用 `QStringLiteral`。 |
| 构造 | `QCborValue(QStringView value)` | 用字符串视图构造文本值。 | 构造完成后值独立于视图的来源。 |
| 构造 | `QCborValue(QLatin1StringView value)` | 用 Latin-1 字符串视图构造文本值。 | 仅对确知为 Latin-1 的常量或数据使用。 |
| 构造 | `QCborValue(const QCborArray &value)` | 以数组副本构造值。 | 后续修改原数组不会改这个值。 |
| 构造 | `QCborValue(QCborArray &&value)` | 移动数组构造值。 | 移动后不要依赖源数组内容。 |
| 构造 | `QCborValue(const QCborMap &value)` | 以 map 副本构造值。 | 适合封装协议根对象。 |
| 构造 | `QCborValue(QCborMap &&value)` | 移动 map 构造值。 | 移动后源 map 只保持有效但内容未指定。 |
| 构造 | `QCborValue(QCborTag tag, const QCborValue &value)` | 创建自定义 tag 包裹的值。 | tag 号和内部值的约束由协议定义。 |
| 构造 | `QCborValue(QCborKnownTags tag, const QCborValue &value)` | 用 Qt 已知标签创建带标签值。 | 对日期、URL 等优先用对应 Qt 类型构造，语义更清楚。 |
| 构造 | `QCborValue(const QDateTime &value)` | 构造日期时间标签值。 | 明确时区和精度要求，避免协议双方解释不同。 |
| 构造 | `QCborValue(const QUrl &value)` | 构造 URL 标签值。 | 不替代 URL 的业务合法性校验。 |
| 构造 | `QCborValue(const QRegularExpression &value)` | 构造正则标签值。 | 只保存 pattern，不保存正则选项。 |
| 构造 | `QCborValue(const QUuid &value)` | 构造 UUID 标签值。 | 与字符串 UUID 的 wire 格式不同。 |
| 生命周期 | 拷贝、移动构造与赋值 | 复制或转移一个值。 | 容器内容采用隐式共享；修改可能触发分离。 |
| 生命周期 | `~QCborValue()` | 销毁值及其持有的容器数据。 | 普通值类型，无需手动资源管理。 |
| 查询 | `type()` | 返回当前 `Type`。 | 适合 `switch`；常规分支用可读性更强的 `isXxx()`。 |
| 查询 | `isInteger()`、`isDouble()` | 判断整数或双精度类型。 | 先判断再转换，尤其是外部输入。 |
| 查询 | `isByteArray()`、`isString()` | 判断字节串或文本类型。 | 两者不可因内容看起来相同而混用。 |
| 查询 | `isArray()`、`isMap()`、`isContainer()` | 判断容器类型。 | 解析嵌套协议时先检查，再调用 `toArray()` 或 `toMap()`。 |
| 查询 | `isFalse()`、`isTrue()`、`isBool()` | 判断布尔 simple value。 | `isBool()` 是读取布尔字段最常用的检查。 |
| 查询 | `isNull()`、`isUndefined()`、`isInvalid()` | 判断三种“无内容”状态。 | `Undefined` 既可能来自数据也可能来自查找失败。 |
| 查询 | `isSimpleType()`、`isSimpleType(QCborSimpleType)` | 判断是否为 simple value 或指定 simple 值。 | 不明 simple 值的互操作性通常较差。 |
| 查询 | `isTag()` | 判断是否为任意标签值。 | 对扩展类型也会返回真。 |
| 查询 | `isDateTime()`、`isUrl()`、`isRegularExpression()`、`isUuid()` | 判断 Qt 识别的扩展标签类型。 | 确认发送端使用的是同一标准标签。 |
| 转换 | `toInteger(qint64 defaultValue)` | 取整数，或将 double 转为整数。 | 非数值类型返回默认值；严格校验要先用 `isInteger()`。 |
| 转换 | `toDouble(double defaultValue)` | 取双精度，或将整数转为 double。 | 大整数转 double 可能失精。 |
| 转换 | `toBool(bool defaultValue)` | 取布尔值。 | 非布尔类型只返回默认值，不会解析字符串。 |
| 转换 | `toSimpleType(QCborSimpleType defaultValue)` | 取 simple type 编号。 | 用于需要兼容未知 simple 值的低层协议。 |
| 转换 | `toByteArray(const QByteArray &defaultValue)` | 取 byte string。 | 文本值不会自动转为 UTF-8 字节。 |
| 转换 | `toString(const QString &defaultValue)` | 取文本字符串。 | byte string 不会自动按 UTF-8 解码。 |
| 转换 | `toStringView(QAnyStringView defaultValue)` | 以字符串视图读取文本。 | Qt 6.10 起可用；不要让视图跨越源值生命周期。 |
| 转换 | `toDateTime(const QDateTime &defaultValue)` | 取日期时间标签值。 | 非日期标签返回默认值。 |
| 转换 | `toUrl(const QUrl &defaultValue)` | 取 URL 标签值。 | 返回后仍需做业务层 URL 校验。 |
| 转换 | `toRegularExpression(const QRegularExpression &defaultValue)` | 取正则标签值。 | 读取到的正则不恢复原 pattern options。 |
| 转换 | `toUuid(const QUuid &defaultValue)` | 取 UUID 标签值。 | 非 UUID 标签返回默认值。 |
| 转换 | `toArray()`、`toArray(defaultValue)` | 取数组或类型不符时的默认数组。 | 返回值副本，改完需重新赋给父值。 |
| 转换 | `toMap()`、`toMap(defaultValue)` | 取 map 或类型不符时的默认 map。 | 返回值副本；map 键可能是非字符串。 |
| 标签 | `tag(QCborTag defaultValue)` | 取得标签编号。 | 必须先用 `isTag()` 区分默认返回值。 |
| 标签 | `taggedValue(const QCborValue &defaultValue)` | 取得标签内部包裹的值。 | 内部值仍需按协议做类型验证。 |
| 比较 | `compare(const QCborValue &other)` | 按 Qt 的 CBOR 比较规则返回小于、等于或大于。 | map 和 array 会递归比较；不要把它等同于字节序列比较。 |
| 修改 | `swap(QCborValue &other)` | 高效交换两个值。 | 常用于异常安全的赋值或算法内部。 |
| 下标 | `operator[](const QString &key)` | 以文本键读写 map 成员，返回 `QCborValueRef`。 | 非 const 调用会把非 map 改写为 map，数组也会发生转换。 |
| 下标 | `operator[](QLatin1StringView key)` | 以 Latin-1 键读写 map 成员。 | 仅在键确知为 Latin-1 时使用。 |
| 下标 | `operator[](qint64 key)` | 用数值键读写 map 或数组元素。 | 数组越界的非 const 访问会把数组转换成 map。 |
| 下标 | `const operator[](QString, QLatin1StringView, qint64)` | 只读查找 map 键或数组索引。 | 未命中返回 `Undefined`，不能区分真实 undefined 值。 |
| 序列化 | `fromCbor(QCborStreamReader &reader)` | 从流读取器当前项解码一个值。 | 失败后检查 `reader.lastError()`；返回值可能部分完成。 |
| 序列化 | `fromCbor(const QByteArray &, QCborParserError *)` | 从字节数组解码一个顶层项。 | 始终提供错误对象；成功时 `offset` 指向第一个未消费字节。 |
| 序列化 | `fromCbor(const char *, qsizetype, QCborParserError *)` | 从字符字节区间解码。 | 长度必须准确，内部会构造 `QByteArray`。 |
| 序列化 | `fromCbor(const quint8 *, qsizetype, QCborParserError *)` | 从无符号字节区间解码。 | 同样需要检查错误对象，不能只检查返回值类型。 |
| 序列化 | `toCbor(EncodingOptions)` | 将值编码为新 `QByteArray`。 | 签名和哈希场景明确指定排序与浮点变换规则。 |
| 序列化 | `toCbor(QCborStreamWriter &, EncodingOptions)` | 直接写入流式编码器。 | 适合大输出或连续输出；注意 writer 的错误状态。 |
| 互转 | `fromVariant(const QVariant &)` | 将 Qt 变体转换为 CBOR 值。 | 不是所有元类型都有无损的 CBOR 表示。 |
| 互转 | `toVariant()` | 将值转换为 `QVariant`。 | 跨边界前验证 tag、byte string 等特殊类型是否仍满足需求。 |
| 互转 | `fromJsonValue(const QJsonValue &)` | 将 JSON 值转换为 CBOR 值。 | JSON 本来不含 byte string、tag 和任意键类型。 |
| 互转 | `toJsonValue()` | 将 CBOR 值转换为 JSON 值。 | 转换可能丢失 CBOR 独有信息，不可作为无损中间格式。 |
| 调试 | `toDiagnosticNotation(DiagnosticNotationOptions)` | 生成人类可读的 CBOR 诊断文本。 | 只用于日志和调试，Qt 不支持反向解析这段文本。 |
| 非成员 | 比较运算符 `==`、`!=`、`<`、`<=`、`>`、`>=` | 依据 `compare()` 比较两个值。 | 容器内容递归参与比较；与原始 CBOR 字节是否相同是两回事。 |
| 非成员 | `qHash(const QCborValue &, size_t)` | 为值生成哈希，供哈希容器使用。 | 用作 `QHash` 键时，保持值不被修改。 |

## 一句话总结

`QCborValue` 的价值不只是“把 CBOR 读出来”。它让程序能保留并审查 CBOR 的类型、标签和嵌套结构；真实项目中最重要的是始终检查解析错误与原始类型，避免在默认值、隐式转换和非 const 下标访问中悄悄改变协议含义。
