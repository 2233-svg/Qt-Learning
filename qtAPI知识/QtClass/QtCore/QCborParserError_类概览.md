# QCborParserError 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCborParserError>`  
> 模块：`Qt6::Core`  
> 定位：`QCborValue::fromCbor()` 返回的解码错误与字节偏移

## 它解决什么问题

`QCborParserError` 把 CBOR 解码失败的原因和位置放在一起。它由 `QCborValue::fromCbor()` 的带错误参数重载填充，包含 `QCborError error` 和 `qint64 offset`。

最关键的边界是：`fromCbor()` 在失败时仍可能返回一个部分解码、且外观上像正常值的 `QCborValue`。返回值不能证明成功，必须检查 `error.error`。

```cpp
#include <QCborParserError>
#include <QCborValue>

QCborParserError parseError;
const QCborValue value = QCborValue::fromCbor(bytes, &parseError);

if (parseError.error != QCborError::NoError) {
    qWarning() << "CBOR decode failed at byte" << parseError.offset
               << parseError.errorString();
    return;
}
```

## `offset` 在成功和失败时的意义

失败时，`offset` 是发现问题的字节位置；Qt 会尽量把它指向包含错误的 CBOR 项起始处，即使问题实际发生在该项内部，例如 UTF-8 解码失败。

成功时，`offset` 不是无效值，而是已经消费的字节数，即第一个未使用字节的位置。这使得一个 `QByteArray` 中连续拼接多个 CBOR 项时，可以从 `bytes.constData() + offset` 继续解析下一项。

不要把 `offset` 当字符位置或 CBOR 容器元素下标；它始终针对原始二进制缓冲区。

## 单项解析与拼接帧

```cpp
qsizetype consumed = 0;
while (consumed < bytes.size()) {
    QCborParserError error;
    const QCborValue item = QCborValue::fromCbor(
        bytes.constData() + consumed, bytes.size() - consumed, &error);

    if (error.error != QCborError::NoError)
        break;

    consumed += error.offset;
    // 处理 item
}
```

如果调用协议规定“一帧恰好一个 CBOR 项”，则成功后的 `offset` 应等于输入长度；否则剩余字节代表额外数据。若协议允许拼接 CBOR 序列，就按成功偏移推进。特别注意不能在成功却 `offset == 0` 的情况下无限循环；正常解码一个完整项应消费字节。

## 与 `QCborError` 的分工

`QCborParserError::error` 是详细的 `QCborError`。程序分支比较枚举码，例如区分 `EndOfFile`、`InvalidUtf8String`、`DataTooLarge`；`errorString()` 与 `QCborError::toString()` 返回未翻译的描述，适合日志，不适合作为持久化错误码或条件分支。

## 常见误区

- 不检查 `error`，直接使用 `fromCbor()` 的返回值。
- 把失败时的 `offset` 当作“准确错误字符”；它是二进制数据位置，且通常指向问题项起点。
- 成功时忽略 `offset`；处理拼接 CBOR 数据时它正是消费长度。
- 只处理语法错误，不限制总数据量和嵌套深度。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 数据成员 | `error` | 保存本次解码的 `QCborError`。 | 成功判断为 `error == QCborError::NoError`。 |
| 数据成员 | `offset` | 保存错误位置，或成功时已消费的字节数。 | 以原始 CBOR 字节为单位，不是字符或元素索引。 |
| 描述 | `errorString() const` | 返回当前错误码的未翻译文本。 | 用于日志和 UI，不作为程序稳定分支。 |
| 协作 | `QCborValue::fromCbor(const QByteArray &, QCborParserError *)` | 从字节数组解码一个 CBOR 项。 | 失败时返回值可能部分有效，必须检查错误对象。 |
| 协作 | `QCborValue::fromCbor(const char *, qsizetype, QCborParserError *)` | 从字符字节指针和长度解码。 | 指针必须在调用期间有效，长度必须准确。 |
| 协作 | `QCborValue::fromCbor(const quint8 *, qsizetype, QCborParserError *)` | 从无符号字节指针和长度解码。 | 适合二进制缓冲区，规则与 `char *` 重载相同。 |
| 错误协作 | `QCborError` | 提供错误分类和文本说明。 | 用枚举码处理恢复策略，用文字辅助诊断。 |

## 一句话总结

`QCborParserError` 让单项 CBOR 解码既能报告失败，也能报告成功时消费了多少字节。检查 `error` 是正确性的前提，理解 `offset` 才能安全处理拼接二进制数据。
