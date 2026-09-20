# QCborError 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QtCborCommon>`  
> 模块：`Qt6::Core`  
> 定位：CBOR 读取、解析与转换过程中使用的统一错误码

## 它解决什么问题

`QCborError` 是一个含 `Code` 错误码的轻量值类型。`QCborStreamReader::lastError()`、`QCborValue` 的 CBOR 解码以及 `QCborParserError` 都用它描述失败原因。

它不保存错误偏移，也不抛异常。需要“哪个字节附近坏了”时使用 `QCborParserError`；需要在流式读取后判断当前读取器是否还能继续时查询 `QCborStreamReader::lastError()`。

```cpp
QCborStreamReader reader(data);
if (!reader.next()) {
    const QCborError error = reader.lastError();
    if (error != QCborError::NoError)
        qWarning() << error.toString();
}
```

错误判断使用枚举码，`toString()` 只用于日志或诊断显示。

## 错误码的层次

前几项通常来自流读取状态：输入设备失败、越过输入末尾。`256` 起更多是 CBOR 数据的编码或结构错误，`1024` 起代表资源或 Qt 支持边界问题。应用往往只需区分“无错”“输入尚未完整”“数据非法”和“资源限制”，编辑器或分析器才需要逐项展示。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成功 | `NoError` | 没有错误。 | 任何返回值本身都不能替代对此码的检查。 |
| 内部状态 | `UnknownError` | 未能细分的错误。 | 记录原始数据和上下文以排查。 |
| 输入状态 | `AdvancePastEnd` | 读取操作越过现有输入末尾。 | 流式输入可能只是数据尚未到齐，不一定是恶意数据。 |
| 输入状态 | `InputOutputError` | 关联的 `QIODevice` 发生 I/O 错误。 | 同时检查设备的 `errorString()`。 |
| 数据尾部 | `GarbageAtEnd` | 一个完整 CBOR 项后存在多余数据。 | 对单项协议是错误；拼接帧协议可按消费偏移继续读。 |
| 数据尾部 | `EndOfFile` | CBOR 项尚未完整，输入已经结束。 | 文件截断或网络帧不完整都可能触发。 |
| 结构 | `UnexpectedBreak` | 在不允许的位置遇到 CBOR break 标记。 | 常见于不定长容器或字符串编码损坏。 |
| 类型 | `UnknownType` | 遇到无法识别的 CBOR 主类型或附加信息。 | 保留原始字节，避免盲目容错。 |
| 类型 | `IllegalType` | 当前上下文不允许该 CBOR 类型。 | 常由调用方期待的类型与实际数据不符引起。 |
| 数值 | `IllegalNumber` | 数字编码不合法。 | 不应继续把当前项当作可信数值。 |
| 简单值 | `IllegalSimpleType` | simple value 编码不合法。 | 检查生产端是否符合 CBOR 规范。 |
| 文本 | `InvalidUtf8String` | CBOR text string 含非法 UTF-8。 | byte string 与 text string 的协议含义不能混用。 |
| 资源 | `DataTooLarge` | 数据或长度超出可处理范围。 | 在读取层限制帧大小，避免内存压力。 |
| 资源 | `NestingTooDeep` | 容器嵌套超过安全深度。 | 当作不可信输入的资源保护信号。 |
| 支持边界 | `UnsupportedType` | Qt 当前转换路径不支持该 CBOR 类型。 | 不能假定 CBOR 的所有标签和扩展都可映射到目标类型。 |

## 常见误区

- 用 `toString()` 的文字作为控制流条件；应比较 `Code`。
- 把 `AdvancePastEnd` 一律视为损坏数据；追加式流输入可能需要等待更多字节。
- 忽略 `DataTooLarge` 和 `NestingTooDeep`；它们是输入资源保护边界。
- 只处理解码失败，不检查 `QIODevice` 的真实 I/O 失败。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `QCborError::Code` | 定义所有 CBOR 错误码。 | 程序逻辑比较枚举值，不比较描述文本。 |
| 数据成员 | `c` | 保存当前 `Code`。 | 普通应用可经转换运算符直接与错误码比较。 |
| 转换 | `operator Code() const` | 将错误对象作为 `Code` 使用。 | 便于 `error == QCborError::NoError`。 |
| 描述 | `toString() const` | 返回错误码的文字描述。 | 用于日志和 UI，不承诺作为稳定协议字段。 |
| 协作 | `QCborStreamReader::lastError()` | 获取流读取器最近的 `QCborError`。 | 在 `next()`、读取字符串或容器操作失败后检查。 |
| 协作 | `QCborParserError::error` | 在带偏移的解析错误中保存此错误码。 | 需要诊断位置时配合 `offset` 使用。 |

## 一句话总结

`QCborError` 是 CBOR 错误分类的共同语言。用错误码决定恢复、等待还是拒绝输入，用 `toString()` 辅助人类排查。
