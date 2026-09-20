# QStringDecoder：把外部编码安全地解码为 QString

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStringDecoder>`  
> CMake：`Qt6::Core`  
> 基类：`QStringConverter`

`QStringDecoder` 把某种字节编码转换为 Qt 使用的 UTF-16 文本。它与
`QString::fromUtf8()` 这类一次性函数的主要区别是：decoder 会保留跨调用状态，因此能够正确
处理被文件块、网络包或设备读取边界拆开的字符。

它适合流式读取文本文件、分段解析 HTTP/HTML、串口文本协议、持续接收日志，以及需要知道输入
是否包含损坏字节的导入流程。

## 核心使用方式

已知输入编码时，创建一个 decoder，并让同一实例服务于同一条输入流：

```cpp
#include <QStringDecoder>

QString decodeUtf8Chunks(const QList<QByteArray> &chunks)
{
    QStringDecoder decoder(QStringConverter::Utf8);
    QString text;

    for (const QByteArray &chunk : chunks)
        text += QString(decoder(chunk));

    QString tail(8, Qt::Uninitialized);
    auto final = decoder.finalize(tail.data(), tail.size());
    if (final.error == QStringConverter::FinalizeResultError::NotEnoughSpace) {
        // 实际代码应扩大缓冲区，并对同一个 decoder 再次调用 finalize()。
        return {};
    }

    tail.truncate(final.next - tail.data());
    text += tail;

    if (final.error == QStringConverter::FinalizeResultError::InvalidCharacters)
        qWarning("The byte stream contained invalid input");

    return text;
}
```

例如一个 UTF-8 字符的前三个字节位于块 A，最后一个字节位于块 B。默认状态模式会在 A 后保存
残片，在 B 到达后输出完整字符。若每块都新建 decoder，或设置了 `Stateless`，该字符会被当作
无效输入。

## 构造与有效性

### 按枚举构造

```cpp
QStringDecoder utf8(QStringConverter::Utf8);
QStringDecoder utf16be(QStringConverter::Utf16BE);
```

枚举构造适合 Qt 内置的 UTF、Latin-1 和系统编码，类型明确且不会受名称拼写影响。

### 按名称构造

```cpp
QStringDecoder decoder(codecName);
if (!decoder.isValid())
    return reportUnsupportedCodec(codecName);
```

名称构造可使用当前 Qt 构建支持的 codec；启用 ICU 的构建可能支持更多名称。未知或不可用名称
不会抛异常，而是生成无效 decoder。

### 默认构造

默认构造得到无效对象，它主要用于稍后移动赋值：

```cpp
QStringDecoder decoder;
Q_ASSERT(!decoder.isValid());

decoder = QStringDecoder(QStringConverter::Utf8);
```

对无效对象调用转换会得到空结果并把错误状态置为真。默认构造不表示“自动检测编码”。

## `decode()` 与 `operator()` 的延迟代理

这两组重载不立刻返回 `QString`，而是返回 `EncodedData<...>` 代理。代理在转换为 `QString`
时才真正调用 decoder：

```cpp
QByteArray bytes = readChunk();

QString text1 = decoder.decode(bytes);
QString text2 = decoder(bytes);
```

直接写成具体的 `QString` 最清楚。下面的 `auto` 容易埋下生命周期和执行顺序问题：

```cpp
auto pending = decoder(bytes); // 此时 pending 不是 QString
```

对于 `const QByteArray &` 重载，代理保存对原数组的引用；对于 view 重载，代理保存非拥有视图。
如果输入先被销毁、修改或重分配，稍后再把代理转成 `QString` 就会读取失效或变化的数据。代理还
保存 decoder 指针，在具体化前继续使用或销毁 decoder 同样会改变语义。

因此除非正用于 QStringBuilder 表达式，应立即具体化：

```cpp
QString decoded = decoder(chunk);
```

## 错误替代与 BOM

默认情况下：

- 无效字节序列会输出 U+FFFD replacement character。
- `hasError()` 变为 `true`，并保持到 `resetState()` 或成功结束重置。
- 输入开头的 BOM 被当作编码签名跳过。

可用 `ConvertInvalidToNull` 把无效序列替换为 U+0000；这不会让输入变得“无错误”，
`hasError()` 仍会记录问题。设置 `ConvertInitialBom` 后，初始 BOM 会保留为字符串中的 U+FEFF。

`Stateless` 适用于每次调用都是完整独立记录的场景。它会禁止跨块等待，因此数据块末尾的不完整
序列立即产生错误。不要仅为了“线程安全”设置它；并发任务仍应使用不同实例。

## `finalize()`：明确输入流已经结束

Qt 6.11 新增 `finalize()`。当调用方确认不会再有字节时，必须让 decoder 处理待定残片：

- 完整结束且从未遇到无效字符：`NoError`。
- 已完成，但此前或末尾有无效序列：`InvalidCharacters`。
- 提供的输出缓冲区放不下尾部替代输出：`NotEnoughSpace`，扩大缓冲区后对同一实例重试。

有三个重载：

- `finalize(char16_t *out, qsizetype maxlen)`
- `finalize(QChar *out, qsizetype maxlen)`
- `finalize()`

无参数形式会完成检查并重置状态，但没有地方保存可能产生的尾部替代字符。若最终文本必须完整，
应使用带缓冲区的重载。

`FinalizeResult` 是 `FinalizeResultChar<char16_t>` 的别名，
`FinalizeResultQChar` 是 `FinalizeResultChar<QChar>` 的别名。返回值的 `next` 是输出尾后指针，
`invalidChars` 是整条流累计的无效字符数。

## 直接写入调用方缓冲区

高层代理最终会创建 `QString`。如果调用方已经管理目标缓冲区，可以使用
`requiredSpace()` 和 `appendToBuffer()`：

```cpp
QString decodeOneChunk(QStringDecoder &decoder, QByteArrayView input)
{
    QString output(decoder.requiredSpace(input.size()), Qt::Uninitialized);
    QChar *end = decoder.appendToBuffer(output.data(), input);
    output.truncate(end - output.data());
    return output;
}
```

`requiredSpace(inputLength)` 返回最坏情况下需要保留的 UTF-16 code unit 数，不是精确输出长度。
实际结尾由 `appendToBuffer()` 的返回指针决定。

必须分配完整的 `requiredSpace()` 范围。Qt 文档明确允许转换实现写入返回 `end` 指针之后、但仍在
该最大范围内的临时内容；只按“预计实际字符数”分配可能造成越界。调用结束后再按返回指针截断。

`char16_t *` 重载与 `QChar *` 重载语义相同。`out` 必须指向可写且足够大的连续内存，函数不会替
调用方检查缓冲区容量。

## HTML 编码选择

`decoderForHtml(data)` 根据 BOM 和 HTML 字符集声明创建 decoder：

```cpp
QStringDecoder decoder = QStringDecoder::decoderForHtml(prefix);
if (!decoder.isValid())
    return rejectUnsupportedHtmlEncoding();

QString html = decoder(allBytes);
```

未发现编码声明时，它返回 UTF-8 decoder；发现了 Qt 不支持的声明时返回无效 decoder。通常应把
文档开头足够多的字节传给工厂进行识别，然后让返回的同一 decoder 解码完整文档。

它不是任意文本的语言统计检测器，也不能可靠猜测没有声明的传统本地编码。

## 生命周期与线程

- decoder 不可复制，但可移动。
- 代理对象借用 decoder，并可能借用输入；代理的安全生命周期比 decoder 和输入都短。
- 同一 decoder 维护残片和累计错误，不能跨线程并发调用。
- 不同线程各自构造 decoder 可以并行工作。
- decoder 不是 `QObject`，不需要事件循环，也没有父对象所有权。
- `resetState()` 会清除无效字符计数和块尾残片，应只在放弃当前流或开始新流时调用。

## 常见错误

### 用默认构造对象直接解码

默认对象无效。按枚举或名称赋值后检查 `isValid()`。

### 用 `auto` 长期保存转换结果

保存的是借用数据的延迟代理，不是字符串。立即写成 `QString text = decoder(bytes);`。

### 一块数据一个 decoder

这会破坏跨块字符。一个连续输入流复用一个实例。

### 未调用 `finalize()`

最后一段的不完整序列可能仍在等待后续字节，错误和替代输出尚未完成。

### 只按实际预估输出分配缓冲区

`appendToBuffer()` 的低层契约要求整个 `requiredSpace()` 范围均可写。

### 看到替代字符却认为 `hasError()` 已自动清零

错误状态是累计的。读取 `finalize()` 结果，或在明确的流边界重置。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QStringDecoder()` | 创建无效占位对象 | 不会自动检测编码；转换前必须赋予有效 decoder。 |
| `QStringDecoder(Encoding, Flags)` | 使用内置编码构造 | 适合 UTF、Latin-1、System 等枚举编码。 |
| `QStringDecoder(QAnyStringView, Flags)` | 按 codec 名称构造 | 名称可能不可用；构造后检查 `isValid()`。 |
| `decode(const QByteArray &)` | 创建借用数组的延迟解码代理 | 立即具体化为 `QString`，避免原数组或 decoder 先失效。 |
| `decode(QByteArrayView)` | 创建借用视图的延迟解码代理 | view 不拥有字节；底层内存必须保持有效。 |
| `operator()(const QByteArray &)` | `decode()` 的调用运算符形式 | 返回代理，不是直接返回 `QString`。 |
| `operator()(QByteArrayView)` | 解码字节视图 | 同样延迟执行并借用 decoder。 |
| `requiredSpace(inputLength)` | 计算低层解码的最大 UTF-16 空间 | 是容量上界，不是精确输出长度；无效 decoder 返回 0。 |
| `appendToBuffer(QChar *, input)` | 把一块字节追加解码到 QChar 缓冲区 | 缓冲区必须覆盖完整 `requiredSpace()` 范围，返回实际尾后指针。 |
| `appendToBuffer(char16_t *, input)` | 写入 `char16_t` 缓冲区 | Qt 6.6 起；容量和状态规则与 QChar 重载相同。 |
| `finalize(QChar *, maxlen)` | 输出并结束待定解码状态 | Qt 6.11 起；空间不足可对同一实例重试。 |
| `finalize(char16_t *, maxlen)` | `char16_t` 版本的结束处理 | 检查 `error`、`next` 和累计 `invalidChars`。 |
| `finalize()` | 不保存尾部输出地结束并重置 | 适合只关心状态的场景；可能丢弃替代输出。 |
| `decoderForHtml(data)` | 按 HTML BOM/charset 创建 decoder | 未声明时 UTF-8；声明不支持时返回无效对象。 |
| `isValid()` | 判断 codec 是否可用 | 默认构造和未知名称可能为假。 |
| `hasError()` | 查询累计解码错误 | 不是“最后一次调用”的状态。 |
| `resetState()` | 清除错误与跨块残片 | 在流中调用会丢失未完成字符。 |

选择 `QStringDecoder` 的关键标准是：输入是外部字节，而且字符可能跨调用边界。若只处理一个已知
完整的 UTF-8 数组，`QString::fromUtf8()` 往往更简洁。
