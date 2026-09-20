# QJsonParseError 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QJsonParseError>`  
> 模块：`Qt6::Core`  
> 定位：描述 JSON 文本解析失败的类别和位置

## 它解决什么问题

`QJsonParseError` 是一个轻量结构体，不负责解析，也不是 C++ 异常。将它传给 `QJsonDocument::fromJson()` 或 Qt 6.9 起的 `QJsonValue::fromJson()`，解析器会写入错误类别 `error` 和错误位置 `offset`。

它回答的是“JSON 语法为何失败、在哪里失败”。语法成功仍不代表接口数据合格：对象可能少必填字段，字段也可能类型错误或超出范围，因此它是 JSON 校验的第一关。

```cpp
#include <QJsonDocument>
#include <QJsonParseError>

const QByteArray payload = R"({"name":"Lin", "enabled":true,})";
QJsonParseError parseError;
const QJsonDocument document = QJsonDocument::fromJson(payload, &parseError);

if (parseError.error != QJsonParseError::NoError) {
    qWarning() << "parse failed at byte" << parseError.offset
               << parseError.errorString();
    return;
}
```

程序逻辑比较 `parseError.error` 和 `NoError`。`errorString()` 是面向人阅读的文本，只用于日志或 UI，不能作为稳定的控制流条件。

## `offset` 的含义

`offset` 是解析器发现问题的原始输入偏移。对于 `QByteArray` 中的 UTF-8 JSON，它应视为字节位置，不是用户看到的“第几个 Unicode 字符”或“第几列”。

若编辑器要显示行列号，需要按原始字节扫描到该偏移，并自行处理 `\r\n`、制表符和 UTF-8 多字节字符。Qt 6.11 在无错误时默认 `offset` 为 `-1`，此时不应把它显示为有效位置。

## 各错误类别的实际含义

多数应用只分 `NoError` 和其他错误。只有 JSON 编辑器、导入工具、遥测与排障平台，才有必要按以下类别细分。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 结果 | `NoError` | JSON 语法解析成功。 | 仍需校验根类型、字段和业务规则。 |
| 对象语法 | `UnterminatedObject` | 对象缺少结束的 `}`。 | 常见于输入截断或漏写右花括号。 |
| 对象语法 | `MissingNameSeparator` | 键名和值之间缺少 `:`。 | JSON 键必须为双引号字符串。 |
| 数组语法 | `UnterminatedArray` | 数组缺少结束的 `]`。 | 常见于截断或漏写右中括号。 |
| 分隔符 | `MissingValueSeparator` | 相邻元素或成员之间缺少 `,`。 | JSON 不支持省略逗号。 |
| 值语法 | `IllegalValue` | 遇到不合法的值标记。 | 检查单引号、`True`、`None` 等非 JSON 写法。 |
| 数字语法 | `TerminationByNumber` | 数字后紧跟不允许的内容。 | 检查数字与后续标记间是否缺少分隔。 |
| 数字语法 | `IllegalNumber` | 数字格式不合法。 | JSON 不接受十六进制或前导加号。 |
| 字符串语法 | `IllegalEscapeSequence` | 字符串内转义序列不合法。 | 只能使用 JSON 规定的反斜杠转义。 |
| 字符串编码 | `IllegalUTF8String` | 字符串不是合法 UTF-8。 | 检查网络、文件的编码和字节完整性。 |
| 字符串语法 | `UnterminatedString` | 字符串缺少结束双引号。 | 常由截断或未转义引号造成。 |
| 根值限制 | `MissingObject` | document 解析路径期望对象但未得到对象。 | 任意根值可在 Qt 6.9 起使用 `QJsonValue::fromJson()`。 |
| 资源限制 | `DeepNesting` | 嵌套层级过深。 | 将其视为不可信输入的资源保护信号。 |
| 资源限制 | `DocumentTooLarge` | 文档过大而不能解析。 | 读取层也应限制输入尺寸。 |
| 尾部数据 | `GarbageAtEnd` | 一个完整 JSON 值后还有非空白数据。 | 检查两个 JSON 文档是否被错误拼接。 |

## 语法成功后的第二道校验

`{"port":"not-a-number"}` 是完全合法的 JSON，却可能不是合法配置。实际流程应分两步：

1. 用 `QJsonParseError` 判断原始文本是否符合 JSON 语法。
2. 用 `isObject()`、`contains()`、`isDouble()` 等检查结构、字段类型与范围。

将两者分开，日志才能明确指出是“文本损坏”还是“协议字段不符合约定”。

## 常见误区

- 只看 `QJsonDocument::isNull()`，不记录 `error`、`offset`。
- 用 `errorString()` 的文字内容做分支。
- 把 UTF-8 输入的 `offset` 当字符下标。
- 解析成功后跳过字段校验。
- 等到 `DocumentTooLarge` 才考虑输入大小限制。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 数据成员 | `error` | 保存 `ParseError` 错误类别。 | 成功判断为 `error == NoError`。 |
| 数据成员 | `offset` | 保存发现错误的原始输入偏移。 | UTF-8 输入按字节解释；无错误时通常是 `-1`。 |
| 错误文本 | `errorString() const` | 返回当前错误的可读说明。 | 仅用于日志和 UI，不用于程序分支。 |
| 错误枚举 | `ParseError` | 列出所有解析错误类别。 | 常规业务只区分成功与失败，诊断工具再细分。 |
| 解析协作 | `QJsonDocument::fromJson(..., QJsonParseError *)` | 解析对象或数组文档并填充错误信息。 | 解析后继续验证根类型与字段。 |
| 解析协作，Qt 6.9 起 | `QJsonValue::fromJson(..., QJsonParseError *)` | 解析任意 JSON 根值并填充错误信息。 | 兼容旧 Qt 时保留 `QJsonDocument` 路径。 |

## 一句话总结

`QJsonParseError` 用错误枚举和字节偏移解释 JSON 文本为什么失败。枚举用于判断，文本用于诊断；通过语法关之后，结构和业务校验仍不可省略。
