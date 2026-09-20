# QStringConverter::FinalizeResultChar：结束转换的缓冲区结果

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStringConverter>`  
> CMake：`Qt6::Core`  
> 自 Qt 6.11 起提供

`QStringConverter::FinalizeResultChar<Char>` 是 `QStringDecoder::finalize()` 和
`QStringEncoder::finalize()` 返回的轻量结果结构。它不拥有输出内存，也不执行转换；它回答三个
结束阶段最重要的问题：

1. 输出写到了哪里。
2. 整条转换流累计遇到了多少无效字符。
3. 结束处理是否完成，还是需要更大的缓冲区重试。

解码器把它实例化为 `FinalizeResultChar<char16_t>` 或 `FinalizeResultChar<QChar>`，编码器把它
实例化为 `FinalizeResultChar<char>`。

## 为什么结束时还需要结果

分块转换会保存暂时不能判断的输入。例如，最后一个网络包只包含一个 UTF-8 四字节序列的前三个
字节；在数据流没有结束前，转换器必须等待第四个字节。调用 `finalize()` 才明确告诉它：
不会再有输入了，现在应把残片判为无效并完成状态清理。

编码方向也可能在结束时产生字节。某些有状态编码需要输出恢复到初始状态的序列。因此
`finalize(out, maxlen)` 既可能只报告错误，也可能实际写入尾部内容。

## 三个字段

### `Char *next`

`next` 指向最后一个已写字符之后的位置，使用方式与 STL 的半开区间尾指针相同：

```cpp
const qsizetype written = result.next - buffer.data();
```

它指向调用方传给 `finalize()` 的缓冲区，不拥有内存。缓冲区释放或重分配后，该指针随即失效。
当调用无参数 `finalize()` 时，没有输出缓冲区可供使用，不应把 `next` 当作可解引用地址。

### `qint16 invalidChars`

该值包含先前转换调用累计的无效字符数，以及本次结束处理发现的无效字符。它不是只统计
`finalize()` 这一次。

实际业务通常先根据 `error` 判断转换是否完成，再把 `invalidChars != 0` 作为内容存在损坏或替代
输出的信号。字段类型是 `qint16`，不适合作为超长恶意输入的无限精度错误计数器。

### `Error error`

`Error` 是 `QStringConverter::FinalizeResultError` 的别名：

| 值 | 含义 | 调用方动作 |
| --- | --- | --- |
| `NoError` | 结束处理完成，且没有无效字符 | 接受输出。 |
| `InvalidCharacters` | 结束处理完成，但整条流中遇到过无效字符 | 输出可能含替代字符；按业务策略接受、记录或拒绝。 |
| `NotEnoughSpace` | 缓冲区不足，结束处理尚未完成 | 保留转换器，扩大缓冲区，再次调用 `finalize()`。 |

`InvalidCharacters` 不表示“没有任何输出”。默认策略通常会写替代字符，所以它是带质量信息的
完成状态。`NotEnoughSpace` 才表示当前结束过程尚未全部交付。

## 可重试的缓冲区协议

下面示例故意从很小的缓冲区开始，展示 `NotEnoughSpace` 的处理方式：

```cpp
#include <QStringEncoder>

QByteArray finishEncoding(QStringEncoder &encoder)
{
    QByteArray tail(8, Qt::Uninitialized);

    for (;;) {
        auto r = encoder.finalize(tail.data(), tail.size());

        if (r.error != QStringConverter::FinalizeResultError::NotEnoughSpace) {
            tail.truncate(r.next - tail.data());
            if (r.error == QStringConverter::FinalizeResultError::InvalidCharacters)
                qWarning("The input contained invalid UTF-16");
            return tail;
        }

        tail.resize(tail.size() * 2);
    }
}
```

空间不足时不要调用 `resetState()`，也不要换一个新转换器；待输出的结束状态仍保存在原实例中。
扩大缓冲区后继续对同一实例调用 `finalize()`。

当结束内容已经全部交付、没有残留内容，或者使用 `out == nullptr` 的无输出形式结束时，转换器会
回到可用于新流的重置状态。无参数 `finalize()` 等价于不提供输出空间：它会丢弃潜在尾部输出，
但仍报告无效字符状态并结束当前流。

## 使用边界

- 该结构只是瞬时返回值，复制它不会复制或冻结转换器状态。
- `next` 的元素类型由方向决定：编码是 `char *`，解码是 `char16_t *` 或 `QChar *`。
- `next` 与缓冲区起点相减前，必须确认它们属于同一块仍然有效的内存。
- `NotEnoughSpace` 后的重试依赖原转换器状态，不能移动、销毁或重置该实例。
- 同一个转换器不能被多个线程同时结束或继续转换。
- 若不关心可能产生的尾部输出，可以用无参数 `finalize()`；对有状态编码，这可能丢失协议所需的
  结束字节，不适合要完整保存结果的场景。

## 常见错误

### 只检查 `invalidChars`

即使无效字符数为零，`error` 仍可能是 `NotEnoughSpace`。先判断是否完成，再处理质量信息。

### 把 `InvalidCharacters` 当成可重试错误

它表示结束已经完成，只是转换期间出现过替代。再次 `finalize()` 不会修复原始输入。

### 缓冲区扩容后继续使用旧 `next`

`QByteArray::resize()` 或容器扩容可能搬迁内存。扩容后必须以新缓冲区地址和下一次返回的 `next`
为准。

### 无参数结束后期待取回尾部字节

无参数形式用于报告并重置，不提供保存尾部输出的位置。需要完整输出时必须传缓冲区。

### 在 `NotEnoughSpace` 后重建转换器

新实例没有原来的待交付状态。应对原实例扩大缓冲区并重试。

## API 速查表

| 成员 | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `using Error = FinalizeResultError` | 暴露结束错误枚举别名 | 使用 `NoError`、`InvalidCharacters`、`NotEnoughSpace` 判断结果。 |
| `Char *next` | 指向已写输出的尾后位置 | 不拥有内存；缓冲区失效后指针失效。 |
| `qint16 invalidChars` | 返回整条流累计的无效字符数量 | 包含此前调用和本次结束发现的错误，不只是最后一步。 |
| `Error error` | 指示结束是否完成及内容质量 | `NotEnoughSpace` 可重试；`InvalidCharacters` 是已完成但有替代。 |

`FinalizeResultChar` 的核心不是包装一个布尔值，而是给低层缓冲区转换提供明确的“写入位置、
累计质量、是否完成”三元协议。
