# QCborStreamReader 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCborStreamReader>`  
> 模块：`Qt6::Core`  
> 相关类型：`QByteArray`、`QIODevice`、`QCborError`、`QCborValue`

## 它解决什么问题

`QCborStreamReader` 是一个低层、流式的 CBOR 解码器。它不把整份输入一次性构造成 `QCborValue`，而是让程序站在当前 CBOR 项上逐个处理：

- 适合从 `QByteArray`、文件、管道、进程输出或网络设备读取。
- 遇到不需要的巨大字段时，可以直接跳过，不必先分配完整对象。
- 可以处理不定长数组、map、text string 和 byte string。
- 可以在输入尚未收全时暂停，等更多字节到达后继续解析。

它的接口风格类似 `QXmlStreamReader` 的游标式读取，但 CBOR 是二进制格式，调用顺序更严格。若业务只是“把一整段 CBOR 转成对象再访问字段”，优先使用 `QCborValue::fromCbor()`；只有需要控制内存、处理流式输入、跳过字段或保留原始数值宽度时，才直接使用这个类。

## 最重要的模型：当前项不会总是以同一种方式前进

读取器始终有一个“当前项”。不同类别的项，前进规则不同：

| 项目类别 | 典型类型 | 读取方式 | 读取后如何前进 |
| --- | --- | --- | --- |
| 定宽项 | 整数、tag、simple type、float | `toInteger()`、`toTag()`、`toSimpleType()`、`toFloat()` 等 | 调用 `next()` |
| 字符串项 | text string、byte string | `readString()`、`readByteArray()` 等 | 读取函数会消费一个 chunk；循环到 `EndOfString` 后已到下一项 |
| 容器项 | array、map | `enterContainer()`，循环读取子项 | 子项读完后调用 `leaveContainer()`，它会到容器后的下一项 |

最容易写错的是把三种规则混在一起：对整数调用 `readString()` 会触发断言或错误；对已经 `hasNext() == false` 的容器再次调用 `next()` 也是错误；对字符串读取一次就调用 `next()`，则可能跳过后续数据。

## 输入来源和所有权

### 从完整 `QByteArray` 读取

```cpp
QCborStreamReader reader(payload);

while (reader.isValid()) {
    // 根据 reader.type() 处理当前项
    if (reader.isInteger()) {
        const qint64 value = reader.toInteger();
        qDebug() << value;
        reader.next();
    } else {
        reader.next(); // 示例中跳过其他项
    }
}

if (reader.lastError() != QCborError::NoError)
    qWarning() << reader.lastError().toString();
```

`QCborStreamReader` 不复制 `QIODevice` 的所有权。使用设备构造时，设备必须在 reader 销毁前保持有效；reader 也不会替你打开或关闭设备。

### 从 `QIODevice` 读取

```cpp
QFile file("message.cbor");
if (!file.open(QIODevice::ReadOnly))
    return;

QCborStreamReader reader(&file);
// reader 读取 file 当前所在位置的数据
```

`currentOffset()` 只有在设备从解码开始时就位于 CBOR 数据起点时，才可以直接理解为输入中的字节偏移。如果设备从文件中间位置开始读，它代表的是相对于解码起点的消费位置，而不是文件绝对位置。

## 固定宽度值的读取

固定宽度值已经被 reader 预解析，访问函数本身不会推进游标：

```cpp
QCborStreamReader reader(QByteArray::fromHex("182a")); // CBOR unsigned integer 42

if (reader.isUnsignedInteger()) {
    const quint64 value = reader.toUnsignedInteger();
    qDebug() << value;
    reader.next();
}
```

### 整数必须区分三种取法

- `toUnsignedInteger()` 返回完整 `quint64` 范围，适合序列号、位掩码或协议里的无符号计数。
- `toNegativeInteger()` 返回 CBOR 负数的无符号编码部分，类型是 `QCborNegativeInteger`。它可以表达小于 `qint64` 范围的负数。
- `toInteger()` 将正数和负数都转成 `qint64`；超出范围时会溢出并得到错误的符号。

因此，不能对所有 `isInteger()` 的值无条件调用 `toInteger()`。当协议允许完整 CBOR 整数范围时，应根据 `isUnsignedInteger()` 和 `isNegativeInteger()` 选择保真 API。

### 浮点值不会自动转换

`toFloat16()`、`toFloat()`、`toDouble()` 只读取当前实际编码类型，不会把整数或另一种浮点宽度转换成目标类型。调用前分别检查 `isFloat16()`、`isFloat()`、`isDouble()`。

## 数组和 map 的遍历

容器读取必须成对调用 `enterContainer()` 和 `leaveContainer()`：

```cpp
bool skipOrRead(QCborStreamReader &reader)
{
    if (!reader.isContainer())
        return false;

    if (!reader.enterContainer())
        return false;

    while (reader.lastError() == QCborError::NoError && reader.hasNext()) {
        // 这里处理当前子项。
        // 对固定宽度项调用 next()，字符串读取函数会自行推进，
        // 嵌套容器则递归 enterContainer()/leaveContainer()。
        if (reader.isInteger()) {
            qDebug() << reader.toInteger();
            reader.next();
        } else {
            reader.next(); // 跳过当前完整子树
        }
    }

    if (reader.lastError() != QCborError::NoError)
        return false;
    return reader.leaveContainer();
}
```

`hasNext()` 的含义取决于所在层级：

- 解析根项时为 `false`，表示根项已完成。
- 在容器内部为 `false`，表示当前容器的子项已读完，此时应调用 `leaveContainer()`。

`parentContainerType()` 可以告诉你当前项位于 array 还是 map 中；在根项上返回 `Invalid`。对于 map，reader 不会帮你把“键”和“值”合并成一个字段，遍历时要按 CBOR 输入顺序分别处理 key、value。

### 不要盲目信任容器长度

当 `isLengthKnown()` 为真时，`length()` 可以取得数组元素数、map 键值对数、字符串字节数或 byte string 字节数。当长度未知时，容器会用 break 结束，字符串可能由多个 chunk 组成。

外部输入可以声称数组有十亿项。即使想根据 `length()` 预分配容器，也要先做业务上限检查，否则一个看似合法的长度字段就可能导致巨额内存分配。

## 字符串和 byte string

### `readString()` 与 `readByteArray()` 的状态循环

`readString()` 和 `readByteArray()` 每次读取一块，返回 `StringResult`：

```cpp
QString readText(QCborStreamReader &reader)
{
    QString result;
    auto chunk = reader.readString();

    while (chunk.status == QCborStreamReader::Ok) {
        result += chunk.data;
        chunk = reader.readString();
    }

    if (chunk.status == QCborStreamReader::Error) {
        result.clear();
        qWarning() << reader.lastError().toString();
    }
    return result;
}
```

即使字符串在编码中是单段且长度已知，也要循环直到 `EndOfString`。`Ok` 表示本次有数据；`EndOfString` 表示已经完整结束；`Error` 表示读取失败。`StringResult::data` 只有在 `status == Ok` 时有效。

文本和二进制没有隐式转换：

- `isString()` 后用 `readString()` 或 `readUtf8String()`。
- `isByteArray()` 后用 `readByteArray()`。
- 不要因为 byte string 内容恰好是 UTF-8，就用文本 API 读取它。

### `readUtf8String()` 和 `readStringChunk()`

Qt 6.7 起，`readUtf8String()` 返回文本的 UTF-8 字节块，适合要直接写入网络缓冲区、哈希器或文件的代码。它仍然要循环读取到 `EndOfString`。

`readStringChunk(char *, qsizetype)` 把当前 chunk 直接写入调用方缓冲区，适合超大内容和精确控制内存：

```cpp
QByteArray readRawString(QCborStreamReader &reader)
{
    QByteArray output;
    do {
        const qsizetype chunkSize = reader.currentStringChunkSize();
        const qsizetype oldSize = output.size();
        output.resize(oldSize + chunkSize);

        const auto result =
            reader.readStringChunk(output.data() + oldSize, chunkSize);
        if (result.status == QCborStreamReader::Error) {
            output.clear();
            break;
        }
        if (result.status == QCborStreamReader::EndOfString)
            break;
    } while (true);
    return output;
}
```

这个 API 不验证 text string 的 UTF-8 格式，因此它不会产生 `QCborError::InvalidUtf8String`。需要 Qt 完成 UTF-8 验证时，使用 `readString()`；需要原始字节和超大数据时，才选择 `readStringChunk()` 并在自己的边界上校验。

### `readAll...()` 什么时候能用

Qt 6.7 起的 `readAllString()`、`readAllUtf8String()`、`readAllByteArray()` 会循环读取并拼接完整值，适合输入已经全部可用的 `QByteArray` 或已读完的设备。

它们返回空的 `QString` / `QByteArray` 时，空值和失败可能无法只靠返回值区分，所以仍然检查 `lastError()`。这些函数不能在“数据可能稍后到达”的 socket、pipe 场景中暂停后恢复；不完整流应使用分块 API，等待数据后继续。

## 不完整输入和错误处理

`QCborStreamReader` 能区分普通解析错误和输入暂时不完整：

- `QCborError::NoError`：目前没有错误。
- `QCborError::EndOfFile`：当前项还缺数据，通常可以等待更多输入后恢复。
- 其他错误，如 `UnexpectedBreak`、`InvalidUtf8String`、`NestingTooDeep` 等，通常不应继续把剩余输入当成可信数据。

### QByteArray 分片输入

```cpp
QCborStreamReader reader;
reader.addData(firstPart);

if (reader.lastError() == QCborError::EndOfFile) {
    reader.addData(secondPart); // addData() 会重新解析当前项
}
```

`addData()` 会把新字节追加到内部输入，并自动重新解析因到达输入末尾而暂停的当前项。它适合协议层已经把分片按顺序交给你的场景。

### QIODevice 追加数据

对 `QIODevice`，设备本身负责后续数据到达；当 reader 因 `EndOfFile` 停止后，数据可读时调用：

```cpp
if (reader.lastError() == QCborError::EndOfFile) {
    // 在 device 已有更多数据后
    reader.reparse();
}
```

`reparse()` 只适合“之前确实因输入不完整而失败”的当前项；其他情况下调用它是空操作或不能修复错误。

### `isInvalid()` 不等于 `isNull()`

刚构造空 reader、解码失败或容器结束后，当前项可能是 `Invalid`。`Null` 则是正常、合法的 CBOR simple value。不要用 `!isNull()` 代替 `isValid()`。

## 跳过和递归深度

`next()` 不只适用于整数等定宽值。对字符串、数组或 map 调用时，它会跳过整个当前项，包括嵌套内容。这是处理协议中的未知字段、扩展字段和不需要的巨大数据时非常有用的能力。

`next(maxRecursion)` 可限制跳过或前进时允许的嵌套深度。外部输入的嵌套层数可能恶意很深，业务可以把默认的 `10000` 调低到符合协议的上限；返回 `false` 后通过 `lastError()` 查看是否是 `NestingTooDeep`。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员类型 | `Type` | 表示当前 CBOR 项的主类型、浮点宽度或无效状态。 | `ByteArray`/`ByteString` 与 `String`/`TextString` 是别名；用 `type()` 或 `isXxx()` 判断。 |
| 枚举值 | `UnsignedInteger` | 表示 0 到 `2^64 - 1` 的无符号整数。 | 超出 `qint64` 时不能调用 `toInteger()` 期待保真。 |
| 枚举值 | `NegativeInteger` | 表示 CBOR 负整数编码。 | 完整范围用 `toNegativeInteger()`；`toInteger()` 可能溢出。 |
| 枚举值 | `ByteString`、`ByteArray` | 表示原始二进制 byte string。 | 不要用文本读取函数替代。 |
| 枚举值 | `TextString`、`String` | 表示 Unicode 文本字符串。 | `readString()` 会验证 UTF-8；原始 chunk API 不验证。 |
| 枚举值 | `Array` | 表示 CBOR 数组容器。 | 用 `enterContainer()` / `leaveContainer()` 遍历。 |
| 枚举值 | `Map` | 表示 CBOR map 容器。 | key 和 value 是相邻的两个当前项，键不一定是字符串。 |
| 枚举值 | `Tag` | 表示 CBOR 标签。 | 读取编号用 `toTag()`，随后通常还要读取被标签项。 |
| 枚举值 | `SimpleType` | 表示 boolean、null、undefined 或其他 simple value。 | 用 `toSimpleType()` 进一步区分。 |
| 枚举值 | `HalfFloat`、`Float16` | 表示 IEEE 754 半精度浮点。 | 使用 `toFloat16()`，不会自动转为其他浮点类型。 |
| 枚举值 | `Float` | 表示 IEEE 754 单精度浮点。 | 使用 `toFloat()`，调用前检查 `isFloat()`。 |
| 枚举值 | `Double` | 表示 IEEE 754 双精度浮点。 | 使用 `toDouble()`，调用前检查 `isDouble()`。 |
| 枚举值 | `Invalid` | 表示没有可读取的有效当前项。 | 可能来自错误或容器结束，不等于 CBOR null。 |
| 成员类型 | `StringResult<Container>` | 封装字符串或 byte string 一次分块读取的结果。 | 只有 `status == Ok` 时 `data` 才有效。 |
| 成员类型 | `StringResultCode` | 描述当前 chunk 是有数据、结束还是错误。 | `Ok` 后继续读；`EndOfString` 停止；`Error` 检查 `lastError()`。 |
| 枚举值 | `EndOfString` | 表示字符串已经完整读取且没有错误。 | 不要把 `data` 当作最后一块数据。 |
| 枚举值 | `Ok` | 表示本次读到了一个有效 chunk。 | 消费 `data` 后再次调用读取 API。 |
| 枚举值 | `Error` | 表示字符串读取失败。 | 已追加的部分数据不应直接当成完整可信结果。 |
| 构造 | `QCborStreamReader()` | 创建没有输入源的 reader。 | 初始状态报告解析错误；之后用 `addData()` 或 `setDevice()`。 |
| 构造 | `QCborStreamReader(const QByteArray &data)` | 从一份字节数组开始解码。 | reader 管理自己的输入状态，适合完整或分片追加数据。 |
| 构造 | `QCborStreamReader(const char *data, qsizetype len)` | 从指定长度的字符缓冲区解码。 | `len` 必须准确，不能依赖 NUL 终止。 |
| 构造 | `QCborStreamReader(const quint8 *data, qsizetype len)` | 从指定长度的无符号字节缓冲区解码。 | 同样必须显式传长度。 |
| 构造 | `QCborStreamReader(QIODevice *device)` | 从设备当前读位置解码 CBOR。 | 不取得设备所有权；设备必须活得比 reader 久。 |
| 生命周期 | `~QCborStreamReader()` | 销毁 reader 的解码状态。 | 不会替你销毁传入的 `QIODevice`。 |
| 数据源 | `setDevice(QIODevice *device)` | 设置新的设备并重置解码器。 | 设备不会被接管；设置后从设备当前状态开始。 |
| 数据源 | `device()` | 返回当前设备指针。 | 从 `QByteArray` 读取时返回 `nullptr`。 |
| 数据源 | `addData(const QByteArray &data)` | 追加字节并重新解析当前不完整项。 | 主要用于分片输入；追加顺序必须与原始流一致。 |
| 数据源 | `addData(const char *data, qsizetype len)` | 追加指定长度的字符字节。 | 不把输入当 C 字符串处理。 |
| 数据源 | `addData(const quint8 *data, qsizetype len)` | 追加指定长度的无符号字节。 | 长度和指针必须覆盖有效内存。 |
| 状态 | `clear()` | 清空输入并清除解码状态。 | 清空后 reader 指向空输入并报告解析错误；要继续读需 `addData()`。 |
| 状态 | `reset()` | 将输入和解码位置重置到开头。 | 对设备会调用 `QIODevice::reset()`，设备不支持 seek 时不要依赖它。 |
| 状态 | `reparse()` | 重新解析因 `EndOfFile` 暂停的当前项。 | 设备有更多数据后调用；对其他错误没有修复作用。 |
| 错误 | `lastError()` | 返回最近一次解码错误。 | `NoError` 才表示当前解析没有记录错误；重点区分 `EndOfFile`。 |
| 位置 | `currentOffset()` | 返回当前正在解码项相对输入起点的偏移。 | 设备从文件中间开始读时不是文件绝对偏移。 |
| 位置 | `type()` | 返回当前项的 `Type`。 | 访问 `toXxx()` 前先检查类型。 |
| 位置 | `isValid()` | 判断当前项是否有效。 | 容器结束或解析错误时可能为假；`Null` 仍然有效。 |
| 位置 | `isInvalid()` | 判断当前项是否无效。 | 不要和 `isNull()` 混淆。 |
| 容器 | `hasNext()` | 判断当前根项或容器内是否还有下一个子项。 | 容器结束后调用 `leaveContainer()`，不要继续 `next()`。 |
| 容器 | `containerDepth()` | 返回已进入但尚未离开的容器层数。 | 每次 `enterContainer()` 都必须对应一次 `leaveContainer()`。 |
| 容器 | `parentContainerType()` | 返回当前项的父容器是 array 还是 map。 | 根项没有父容器，返回 `Invalid`。 |
| 容器 | `isContainer()` | 判断当前项是否为 array 或 map。 | 为真后才能调用 `enterContainer()`。 |
| 容器 | `isArray()` | 判断当前项是否为 array。 | 可结合 `isLengthKnown()` 读取显式长度。 |
| 容器 | `isMap()` | 判断当前项是否为 map。 | map 的 key 和 value 分别占一个读取位置。 |
| 容器 | `enterContainer()` | 进入当前 array 或 map 的子项序列。 | 必须在 `isContainer()` 为真时调用，并配对离开。 |
| 容器 | `leaveContainer()` | 退出当前容器并定位到其后的下一项。 | 只有 `hasNext() == false` 且深度非零时调用。 |
| 容器 | `isLengthKnown()` | 判断当前字符串、byte string、array 或 map 是否有显式长度。 | 只对这些类型调用；未知长度不能调用 `length()`。 |
| 容器 | `length()` | 返回已知字符串字节数、数组元素数或 map 键值对数。 | 必须先确认 `isLengthKnown()`，否则是错误。 |
| 前进 | `next(int maxRecursion)` | 前进一个固定宽度项，也可跳过完整字符串或容器子树。 | `hasNext()` 已为假时调用是错误；限制递归深度防止过深嵌套。 |
| 查询 | `isUnsignedInteger()` | 判断当前项是否为无符号整数。 | 为真后使用 `toUnsignedInteger()` 或在安全范围内用 `toInteger()`。 |
| 查询 | `isNegativeInteger()` | 判断当前项是否为负整数。 | 大范围负数用 `toNegativeInteger()`。 |
| 查询 | `isInteger()` | 判断当前项是否为任意整数。 | 不代表一定能安全转换为 `qint64`。 |
| 查询 | `isByteArray()` | 判断当前项是否为 byte string。 | 为真后使用 byte string 读取 API。 |
| 查询 | `isString()` | 判断当前项是否为 text string。 | 为真后使用文本读取 API。 |
| 查询 | `isTag()` | 判断当前项是否为标签。 | 用 `toTag()` 取得标签号；标签包裹的值仍需后续读取。 |
| 查询 | `isSimpleType()` | 判断当前项是否为 simple value。 | 可再用 `toSimpleType()` 或重载判断具体值。 |
| 查询 | `isSimpleType(QCborSimpleType st)` | 判断当前项是否为指定 simple value。 | 只对约定的 simple type 放行，未知值通常应拒绝。 |
| 查询 | `isFalse()`、`isTrue()`、`isBool()` | 判断 false、true 或任意布尔值。 | `toBool()` 不会把整数转换成布尔。 |
| 查询 | `isNull()` | 判断当前项是否为合法的 CBOR null。 | `Null` 不是无效状态。 |
| 查询 | `isUndefined()` | 判断输入是否显式编码了 undefined。 | reader 不会把查找失败伪装成 undefined。 |
| 查询 | `isFloat16()`、`isFloat()`、`isDouble()` | 判断浮点编码宽度。 | 各自调用对应 `toFloat16()`、`toFloat()`、`toDouble()`。 |
| 读取 | `toUnsignedInteger()` | 读取完整 `quint64` 无符号整数。 | 只对 `isUnsignedInteger()` 为真的当前项调用。 |
| 读取 | `toNegativeInteger()` | 读取负整数的 CBOR 无符号幅值编码。 | 可保留 `-2^63` 以下的值，但业务使用要谨慎。 |
| 读取 | `toInteger()` | 将当前整数转为 `qint64`。 | 超过有符号范围会溢出，不能用于完整 CBOR 整数。 |
| 读取 | `toBool()` | 读取当前布尔值。 | 只对 `isBool()` 为真时调用，不做其他类型转换。 |
| 读取 | `toSimpleType()` | 读取当前 simple value 的编号。 | 只对 `isSimpleType()` 为真时调用。 |
| 读取 | `toTag()` | 读取当前 tag 编号。 | 只对 `isTag()` 为真时调用。 |
| 读取 | `toFloat16()` | 读取当前半精度浮点。 | 不会自动转换整数、float 或 double。 |
| 读取 | `toFloat()` | 读取当前单精度浮点。 | 不会自动转换其他宽度的浮点。 |
| 读取 | `toDouble()` | 读取当前双精度浮点。 | 不会自动转换整数或其他浮点宽度。 |
| 字符串读取 | `readString()` | 读取一个 text string chunk，返回 `StringResult<QString>`。 | 循环直到 `EndOfString`；先确认 `isString()`。 |
| 字符串读取 | `readUtf8String()` | Qt 6.7 起以 UTF-8 `QByteArray` chunk 读取文本。 | 仍需循环；只适用于完整或可继续处理的流式策略。 |
| 字符串读取 | `readByteArray()` | 读取一个 byte string chunk，返回 `StringResult<QByteArray>`。 | 先确认 `isByteArray()`，循环处理 chunk。 |
| 字符串读取 | `readStringChunk(char *ptr, qsizetype maxlen)` | 把当前文本或字节 chunk 写入调用方缓冲区。 | `data` 是实际写入字节数；文本 UTF-8 不会被验证。 |
| 字符串读取 | `currentStringChunkSize()` | 返回当前文本或字节 chunk 的大小。 | 与 `readStringChunk()` 配合预留空间；先确认字符串类型。 |
| 字符串读取 | `readAllString()` | Qt 6.7 起读取并拼接完整文本。 | 失败时返回空字符串，必须结合 `lastError()`；不可恢复。 |
| 字符串读取 | `readAllUtf8String()` | Qt 6.7 起读取并拼接完整文本的 UTF-8 字节。 | 适合完整输入，不适合等待后续数据的 socket 或 pipe。 |
| 字符串读取 | `readAllByteArray()` | Qt 6.7 起读取并拼接完整 byte string。 | 失败和合法空字节串不能只靠返回值区分。 |
| 字符串读取 | `readAndAppendToString(QString &dst)` | Qt 6.7 起将完整文本追加到目标字符串。 | 错误时目标可能已追加部分数据；不可恢复。 |
| 字符串读取 | `readAndAppendToUtf8String(QByteArray &dst)` | Qt 6.7 起将文本的 UTF-8 字节追加到目标。 | 只接受 text string；错误时可能留下部分结果。 |
| 字符串读取 | `readAndAppendToByteArray(QByteArray &dst)` | Qt 6.7 起将完整 byte string 追加到目标。 | 只接受 byte string；错误时可能留下部分结果。 |

## 一句话总结

`QCborStreamReader` 是“带游标的 CBOR 解码器”：固定值读完要 `next()`，字符串要循环读到 `EndOfString`，容器要成对进入和离开；面对分片输入时只把 `EndOfFile` 当作可等待恢复的状态，其他错误应停止信任后续数据。
