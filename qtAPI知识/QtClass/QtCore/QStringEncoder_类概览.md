# QStringEncoder：把 QString 编码为外部字节流

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStringEncoder>`  
> CMake：`Qt6::Core`  
> 基类：`QStringConverter`

`QStringEncoder` 把 Qt 内部的 UTF-16 文本转换为 UTF-8、UTF-16/32、Latin-1、系统编码或当前
构建提供的其他 codec。它是有状态编码器，能处理跨块拆开的 UTF-16 代理对，也能维护
ISO-2022-JP 一类有状态编码的模式。

典型场景包括：分段写文本文件、向旧协议发送本地编码字节、持续转码日志、给 C API 准备编码
缓冲区，以及在导出时检测目标编码不能表示的字符。

## 基本用法

```cpp
#include <QStringEncoder>

QStringEncoder encoder(QStringConverter::Utf8);
QByteArray bytes = encoder(u"Qt 文本"_s);

if (encoder.hasError())
    qWarning("The input contained invalid UTF-16");
```

若只做一次 UTF-8 转换，`QString::toUtf8()` 更直接。`QStringEncoder` 的价值主要在于分块状态、
可选 codec、错误累计、BOM 策略和结束处理。

## 分块编码

Qt 字符串以 UTF-16 code unit 保存。补充平面字符由高、低代理项组成，而数据分块可能恰好把
代理对拆开。默认状态模式会暂存块尾的高代理项，等待下一块：

```cpp
QStringEncoder encoder(QStringConverter::Utf8);
QByteArray output;

for (QStringView chunk : chunks)
    output += QByteArray(encoder(chunk));

QByteArray tail(16, Qt::Uninitialized);
auto final = encoder.finalize(tail.data(), tail.size());

if (final.error == QStringConverter::FinalizeResultError::NotEnoughSpace) {
    // 扩大缓冲区，并对同一个 encoder 再次调用 finalize()。
    return {};
}

tail.truncate(final.next - tail.data());
output += tail;
```

一条逻辑输出流应始终使用同一个 encoder。每块重新构造对象会丢失代理对残片和有状态 codec 的
当前模式。

## 构造与 codec 选择

### 按 `Encoding` 构造

```cpp
QStringEncoder utf8(QStringConverter::Utf8);
QStringEncoder latin1(QStringConverter::Latin1);
QStringEncoder utf16le(QStringConverter::Utf16LE,
                       QStringConverter::Flag::WriteBom);
```

枚举覆盖 Qt 的内置 UTF、Latin-1 和 `System` 编码。`System` 在 Unix 上按 UTF-8，在 Windows
上使用 locale code page，不应作为跨平台文件格式。

### 按名称构造

```cpp
QStringEncoder encoder(codecName);
if (!encoder.isValid())
    return reportUnsupportedCodec(codecName);
```

按名称可访问当前 Qt 构建提供的扩展 codec，包括可能由 ICU 提供的编码。可用集合随构建选项和
平台变化，未知名称得到无效对象。

### 默认构造

默认构造只创建无效占位对象，适合稍后移动赋值。它不代表 UTF-8，也不会自动选择系统编码。
无效对象执行编码会返回空数组并把错误状态置位。

## `encode()` 与 `operator()` 返回代理

这些 API 返回 `DecodedData<...>` 延迟代理，而不是立即返回 `QByteArray`：

```cpp
QString text = obtainText();

QByteArray a = encoder.encode(text);
QByteArray b = encoder(QStringView{text});
```

上面因为目标类型明确，转换立即发生。下面的 `auto` 保存的是借用对象：

```cpp
auto pending = encoder(text); // 不是 QByteArray
```

代理保存 encoder 指针；`const QString &` 版本还保存字符串引用，`QStringView` 版本保存非拥有
视图。输入或 encoder 若先失效，稍后具体化就不安全。即使它们仍有效，在具体化之前继续使用
encoder 也会改变状态顺序。

日常代码应直接写：

```cpp
QByteArray encoded = encoder(text);
```

延迟代理主要用于 Qt 的字符串构建表达式，不能把它当作拥有结果的容器。

## 无法表示的字符与替代策略

当目标编码不能表示某个 Unicode 字符时，默认通常写入 `?`，同时累计无效字符，使
`hasError()` 为真。产生了字节不代表无损转换成功。

`ConvertInvalidToNull` 改为输出 NUL，但错误状态仍保留。使用这个标志时要特别小心 C 字符串
接口，因为中间 NUL 可能让接收方把内容提前截断。

输入本身也可能是无效 UTF-16，例如孤立高代理项或低代理项。分块模式会等待可能配对的下一块，
直到 `finalize()` 才能确定流尾高代理项无效。

## BOM 与无状态模式

`WriteBom` 要求 encoder 在输出开头写 BOM。它适合需要明确字节序或协议明确要求签名的文件。
不要在每个数据块创建新 encoder 并设置 `WriteBom`，否则每块都会被当作一条新流的开头。

`Stateless` 让每次编码调用相互独立，不保留代理项或 codec 模式。它适合每块本来就是完整独立
记录的协议，不适合任意切分的大文本。

`ConvertInitialBom` 是解码方向的策略，对普通编码输出没有对应作用。

## `finalize()` 的结束语义

Qt 6.11 起，应在输出流结束时调用 `finalize()`：

- 检查最后是否残留孤立 UTF-16 代理项。
- 让有状态 codec 写出结束或恢复初始状态所需的字节。
- 返回整条流累计的无效字符数。
- 完成后重置转换状态，以便开始下一条流。

带缓冲区的 `finalize(char *out, qsizetype maxlen)` 返回：

- `next`：实际输出的尾后指针。
- `invalidChars`：此前转换加结束阶段累计的无效字符数。
- `error`：`NoError`、`InvalidCharacters` 或 `NotEnoughSpace`。

若为 `NotEnoughSpace`，结束过程尚未全部交付。扩大缓冲区后对同一个 encoder 再次调用，不能
重置或替换实例。

无参数 `finalize()` 不保存可能产生的尾部字节。它适合只想检查并结束状态的场景；若 codec
可能需要结束序列，或要保留无效输入的替代输出，应传入缓冲区。

## 直接写入缓冲区

性能敏感或已有目标存储时，可绕过临时 `QByteArray`：

```cpp
QByteArray encodeOneChunk(QStringEncoder &encoder, QStringView input)
{
    QByteArray output(encoder.requiredSpace(input.size()), Qt::Uninitialized);
    char *end = encoder.appendToBuffer(output.data(), input);
    output.truncate(end - output.data());
    return output;
}
```

`requiredSpace(inputLength)` 给出最坏情况下的输出字节容量，不是精确长度。必须让整个范围可写，
再按 `appendToBuffer()` 返回的尾后指针截断。

Qt 允许转换实现使用该最大范围内、返回指针之后的空间作为内部写入区域，因此不能只按经验估算
“UTF-8 平均几个字节”来分配。`appendToBuffer()` 不接收容量参数，容量正确性完全由调用方负责。

若 encoder 无效，`requiredSpace()` 返回 0；`appendToBuffer()` 不前移输出指针并把错误状态置位。

## 生命周期与线程

- encoder 不可复制，但可移动。
- 延迟代理借用 encoder 和输入，不能比它们活得更久。
- 同一 encoder 的 codec 状态、待配对代理项和错误计数会变化，不能并发调用。
- 并行导出时，每条输出流使用独立 encoder。
- encoder 不是 `QObject`，不依赖事件循环，也没有父子对象所有权。
- `resetState()` 会清除错误和待输出状态；在流中途调用可能破坏编码序列。

## 常见错误

### 认为有输出就表示编码成功

无法表示的字符可能已被替换为 `?` 或 NUL。检查 `finalize()` 结果或 `hasError()`。

### 用 `auto` 保存编码结果

得到的是延迟代理，可能借用已销毁的 `QString`/`QStringView`。立即具体化为 `QByteArray`。

### 忘记结束有状态 codec

最后的恢复序列可能只由 `finalize()` 输出。缺少它会得到不完整的外部字节流。

### 为每个块重复写 BOM

BOM 属于整条流的开头。复用一个设置了 `WriteBom` 的 encoder。

### `ConvertInvalidToNull` 后传给 C 字符串 API

替代 NUL 可能被解释成字符串终止符。长度敏感接口应显式传递字节长度。

### 低估 `appendToBuffer()` 所需容量

必须使用 `requiredSpace()`，不能按平均编码长度猜测。

### 把 `System` 输出持久化为可移植格式

Windows 代码页会随环境变化。跨系统协议应使用明确的 UTF-8 或其他固定编码。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QStringEncoder()` | 创建无效占位对象 | 不默认选择 UTF-8；使用前需移动赋值有效 encoder。 |
| `QStringEncoder(Encoding, Flags)` | 使用内置编码构造 | 可配置替代策略、BOM 和状态模式。 |
| `QStringEncoder(QAnyStringView, Flags)` | 按 codec 名称构造 | 名称受当前 Qt/ICU 构建影响；检查 `isValid()`。 |
| `encode(const QString &)` | 创建借用 QString 的延迟编码代理 | 立即具体化为 `QByteArray`，不要长期保存代理。 |
| `encode(QStringView)` | 创建借用视图的延迟编码代理 | view 不拥有字符数据。 |
| `operator()(const QString &)` | `encode()` 的调用运算符形式 | 返回 `DecodedData` 代理，不是直接返回数组。 |
| `operator()(QStringView)` | 编码 UTF-16 视图 | 具体化时才执行，并修改 encoder 状态。 |
| `requiredSpace(inputLength)` | 计算低层编码的最大字节容量 | 是上界而非精确长度；无效 encoder 返回 0。 |
| `appendToBuffer(char *, input)` | 编码到调用方连续缓冲区 | 缓冲区必须至少有 `requiredSpace()`；返回实际尾后指针。 |
| `finalize(char *, maxlen)` | 输出并结束待定编码状态 | Qt 6.11 起；`NotEnoughSpace` 时扩大缓冲区后重试。 |
| `finalize()` | 丢弃潜在尾部输出并结束、重置 | 适合只检查状态，不适合必须保存结束字节的 codec。 |
| `isValid()` | 判断 codec 是否可用 | 默认构造和未知名称会无效。 |
| `hasError()` | 查询累计编码错误 | 替代输出仍算错误；不是单次调用结果。 |
| `resetState()` | 清除错误、代理项和 codec 状态 | 仅在放弃当前流或开始新流时使用。 |
| `name()` | 获取实际 codec 名称 | 指针不归调用方所有。 |

`QStringEncoder` 的核心边界是“输出结果”和“无损成功”并非同一件事。只要目标编码受限，就要把
结束处理和错误状态纳入导出协议。
