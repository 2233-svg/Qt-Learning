# QCborStreamReader::StringResult 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCborStreamReader>`  
> 模块：`Qt6::Core`  
> 定位：CBOR 字符串或字节串分块读取的一次结果

## 它解决什么问题

CBOR 的 text string 和 byte string 可以是普通单段值，也可以是由多个 chunk 组成的不定长值。`QCborStreamReader::StringResult<Container>` 是 `readString()`、`readUtf8String()`、`readByteArray()` 和 `readStringChunk()` 的返回结构，用同一个 `status` 同时表达：

- 本次是否读到一段数据。
- 整个字符串是否已经读完。
- 读取是否出错。

它不是独立创建、长期保存的业务对象，而是驱动“读一块 -> 处理一块 -> 再读”的状态载体。

## 三种状态与正确循环

`StringResultCode` 的含义如下：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 状态 | `Ok` | 本次成功读到一个 chunk。 | 此时 `data` 有效，应处理或追加它。 |
| 状态 | `EndOfString` | 字符串已经全部读取完，且没有错误。 | 此时不能把 `data` 当作最后一块数据。 |
| 状态 | `Error` | 读取或解析发生错误。 | `data` 无效，应检查 `reader.lastError()`。 |

即使当前字符串是已知长度的普通单段字符串，调用方也必须循环到 `EndOfString`，而不是假设一次 `readString()` 就结束：

```cpp
QString text;
for (;;) {
    const auto result = reader.readString();

    if (result.status == QCborStreamReader::Ok) {
        text += result.data;
        continue;
    }
    if (result.status == QCborStreamReader::EndOfString)
        break;

    text.clear();
    qWarning() << reader.lastError().toString();
    break;
}
```

## `data` 的有效期和语义

`data` 的类型由模板实参决定：

- `StringResult<QString>`：`readString()` 读出的文本 chunk。
- `StringResult<QByteArray>`：`readByteArray()` 读出的字节 chunk，或 Qt 6.7 起 `readUtf8String()` 读出的 UTF-8 文本 chunk。
- `StringResult<qsizetype>`：`readStringChunk()` 写入调用方缓冲区的字节数。

只有 `status == Ok` 时才能访问 `data`。`EndOfString` 和 `Error` 都不携带可消费的数据；尤其不要把空 `data` 误判为字符串结束，合法的空 chunk 和读取结束应由 `status` 区分。

## 选择哪种读取 API

`readString()` / `readByteArray()` 易用，自动提供每段的 `QString` 或 `QByteArray`。当完整数据已经可得时，Qt 6.7 的 `readAllString()`、`readAllUtf8String()`、`readAllByteArray()` 更省代码，但它们不能在网络套接字、管道等“数据后续还会到达”的场景中恢复读取。

`readStringChunk()` 将数据写到调用方提供的缓冲区，适合超大内容和受控内存使用；它不验证 text string 的 UTF-8 合法性，因此需要 UTF-8 严格校验时，应优先使用 `readString()` 或自行校验。

调用读取函数前先确认当前项类型：文本用 `reader.isString()`，二进制用 `reader.isByteArray()`。这些 API 不做字符串与字节串的隐式转换。

## 常见误区

- 不检查 `status` 就直接使用 `data`。
- 收到一次 `Ok` 后便认为字符串读取完成。
- 把空 `QString` 或空 `QByteArray` 当作结束信号。
- 在 `Error` 后继续拼接此前的部分数据，并当作完整可信内容。
- 对可能继续到达的数据使用不可恢复的 `readAll...()` 接口。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 模板结构 | `StringResult<Container>` | 封装一次字符串读取的内容与状态。 | 通常用 `auto` 接收，不把它当业务数据模型。 |
| 数据成员 | `data` | 保存本次读到的数据或字节数。 | 仅当 `status == Ok` 时有效。 |
| 数据成员 | `status` | 保存 `StringResultCode` 状态。 | 必须先判断它，再消费 `data`。 |
| 生产者 | `readString()` | 读取一个 CBOR text string chunk，返回 `StringResult<QString>`。 | 先确认 `isString()`，循环直到 `EndOfString`。 |
| 生产者，Qt 6.7 起 | `readUtf8String()` | 读取一个文本 chunk 的 UTF-8 字节表示。 | 返回 `QByteArray` chunk，仍需循环处理。 |
| 生产者 | `readByteArray()` | 读取一个 CBOR byte string chunk。 | 先确认 `isByteArray()`，不能用一次调用代替完整读取。 |
| 生产者 | `readStringChunk(char *, qsizetype)` | 将当前文本或字节串 chunk 写入调用方缓冲区。 | `data` 是实际写入字节数；该路径不验证 UTF-8。 |
| 配套状态 | `QCborStreamReader::EndOfString` | 指示当前字符串无错结束。 | 停止循环，不读取 `data`。 |
| 配套状态 | `QCborStreamReader::Ok` | 指示当前结果带有一段有效数据。 | 处理 `data` 后继续调用读取函数。 |
| 配套状态 | `QCborStreamReader::Error` | 指示读取失败。 | 放弃或回滚部分结果，查询 `lastError()`。 |
| 配套 API | `currentStringChunkSize()` | 获得当前 chunk 大小。 | 用于为 `readStringChunk()` 预分配缓冲区。 |
| 配套 API | `readAllString()`、`readAllUtf8String()`、`readAllByteArray()` | 一次读取并拼接整个值。 | 仅在输入完整可用时使用，失败时再检查 `lastError()`。 |
| 配套 API | `QCborStreamReader::lastError()` | 返回底层 `QCborError`。 | `status == Error` 后用于确定失败类别。 |

## 一句话总结

`StringResult` 的价值在于让 chunk 数据和读取状态不可分离：只有 `Ok` 才消费 `data`，一直读到 `EndOfString` 才成功结束，`Error` 则交给 `lastError()` 决定后续策略。
