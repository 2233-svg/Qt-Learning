# QStringConverter：字符串编码转换的状态与识别层

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStringConverter>`  
> CMake：`Qt6::Core`

`QStringConverter` 不是一个拿来直接执行转换的完整工具。它是 `QStringDecoder` 与
`QStringEncoder` 的公共状态基类，统一保存所选编码、转换标志、未完成的字符以及累计错误，
并提供编码名称查询和数据编码探测功能。

真正的方向性操作由两个派生类完成：

- `QStringDecoder`：外部字节序列转换为 Qt 的 UTF-16 `QString`。
- `QStringEncoder`：Qt 的 UTF-16 字符串转换为指定编码的字节序列。

## 它解决什么问题

字符编码转换不只是一次“查表”。真实输入经常来自网络包、串口、压缩流或分段读取的文件，
一个 UTF-8 字符可能被拆在两个数据块中；UTF-16 输入中的代理对也可能跨块。转换器必须记住
上一块末尾的残片，并在下一块到达后继续处理。

`QStringConverter` 把这些共同问题集中到同一套状态中：

1. 记录当前 codec 及转换策略。
2. 保存分块转换留下的不完整序列。
3. 累计无效字符计数，使 `hasError()` 能反映整段转换历史。
4. 在流结束时配合派生类的 `finalize()` 处理残留状态。
5. 根据 BOM、HTML 声明或名称选择编码。

它适合的实际场景包括：解析未知编码的文本文件、读取 HTML 响应、处理 TCP 分片、把 Qt 文本
导出给旧系统，以及在导入流程中统一记录替换字符和格式错误。

## 编码模型

### 内置 Encoding

| 枚举 | 含义 | 边界 |
| --- | --- | --- |
| `Utf8` | UTF-8 | 无 BOM 也可正常工作。 |
| `Utf16` | 本机字节序 UTF-16 | 与显式 LE/BE 不同；跨平台文件宜写明字节序或 BOM。 |
| `Utf16LE` / `Utf16BE` | 固定小端/大端 UTF-16 | 字节序由枚举决定。 |
| `Utf32` | 本机字节序 UTF-32 | 与显式 LE/BE 的可移植性不同。 |
| `Utf32LE` / `Utf32BE` | 固定小端/大端 UTF-32 | 一个码点通常占四字节。 |
| `Latin1` | ISO-8859-1/Latin-1 语义 | 只能直接表示 U+0000 到 U+00FF。 |
| `System` | 平台系统编码 | Unix 上按 UTF-8；Windows 上使用 locale code page，结果依赖机器配置。 |

这些枚举是 Qt 始终认识的基础编码。构建 Qt 时若启用了 ICU，还可能按名称使用更多 codec；
因此“能够用名称构造转换器”不等于该名称一定能映射为 `Encoding` 枚举。

### Flag 的实际语义

| 标志 | 行为 |
| --- | --- |
| `Default` | 保留跨块状态；无效输入通常输出 U+FFFD，无法编码的字符通常输出 `?`。 |
| `Stateless` | 每次调用独立处理，不保存块尾残片；不完整序列立即按错误处理。 |
| `ConvertInvalidToNull` | 用 NUL 替代无效输入，而不是默认替代字符。 |
| `WriteBom` | 编码时在输出开头写入 BOM；主要供 `QStringEncoder` 使用。 |
| `ConvertInitialBom` | 解码时把开头 BOM 转成 U+FEFF；默认会把 BOM 当作签名跳过。 |

头文件中还存在内部用途的 `UsesIcu` 位。它不是普通应用应主动设置的公开转换策略。

## 正确的分块流程

同一条逻辑流必须复用同一个 decoder 或 encoder。不要为每个数据块重新构造对象，否则块边界上
保存的半个字符会丢失。

```cpp
#include <QStringDecoder>

QString decodeChunks(const QList<QByteArray> &chunks)
{
    QStringDecoder decoder(QStringConverter::Utf8);
    QString result;

    for (const QByteArray &chunk : chunks)
        result += QString(decoder(chunk));

    const auto tail = decoder.finalize();
    if (tail.error != QStringConverter::FinalizeResultError::NoError)
        qWarning("Input contained an incomplete or invalid sequence");

    return result;
}
```

Qt 6.11 起，输入流结束后应显式调用派生类的 `finalize()`。最后一个数据块可能以不完整的 UTF-8
序列、半个 UTF-16 代理对或某种有状态编码的中间状态结束；只检查每次转换后的 `hasError()`
不能替代结束处理。

## 状态、生命周期与线程边界

- 转换器是有状态对象，不可复制，但可移动。
- `hasError()` 是累计状态：只要此前出现过无效字符，它就保持为 `true`，直到重置。
- `resetState()` 同时清除错误计数和未完成的分块状态。它不是“保留残片、只清错误”。
- `name()` 返回当前 codec 的名称指针；无效转换器没有可用 codec，应先检查 `isValid()`。
- 同一实例不能被多个线程并发转换。不同线程各自使用独立实例没有问题。
- 该类不依赖事件循环，也不是 `QObject`，没有父子所有权机制。

在一条流尚未结束时调用 `resetState()`，等同于主动丢弃块尾残片。切换到另一条独立输入流时，
则应重置或重新构造转换器，避免前一条流的状态污染后一条。

## 编码识别与名称查询

### `encodingForData()`

该函数查看 BOM，并可借助 `expectedFirstCharacter` 比较不同 UTF-16/UTF-32 字节序的开头模式。
它返回的是探测结果，而不是可靠的通用编码检测器。普通无 BOM 文本往往无法仅凭一小段字节
确定编码，此时返回空 `std::optional`。

```cpp
const auto encoding =
    QStringConverter::encodingForData(bytes, u'<');

if (encoding) {
    QStringDecoder decoder(*encoding);
    QString text = decoder(bytes);
}
```

不要把“探测不到”直接解释为 UTF-8，也不要用它区分任意传统单字节编码。

### `encodingForHtml()`

它按 HTML 文档规则检查 BOM 和字符集声明。未检测到声明时返回 UTF-8；检测到声明但 Qt 不支持
该编码时返回空值。调用方应区分这两种情况，不能用 `value_or(Utf8)` 把“不支持”静默伪装成
“未声明”。

如果目标是直接得到可用解码器，`QStringDecoder::decoderForHtml()` 更方便：未检测到时得到
UTF-8 decoder，不支持时得到无效 decoder。

### 名称与可用 codec

- `encodingForName()` 只把名称映射到 `Encoding` 枚举中的内置编码。
- ICU 提供的扩展名称可能可用于构造 `QStringDecoder`/`QStringEncoder`，但
  `encodingForName()` 仍可返回 `nullopt`。
- `availableCodecs()` 列出当前构建可用的名称，顺序没有稳定契约；不要依赖索引或显示顺序。
- `nameForEncoding()` 从内置枚举取得规范名称。

## 常见错误

### 每个数据块都新建转换器

这样会把拆在块边界上的多字节字符当作错误。一个输入流对应一个转换器实例。

### 流结束时没有 `finalize()`

末尾不完整序列可能尚未计入错误，有状态编码也可能还有结束输出。结束处理是协议的一部分。

### 把 `hasError()` 当作“上一次调用是否失败”

它反映累计错误。要开始一次新的独立检查，调用 `resetState()` 或使用新实例。

### 盲信自动探测

BOM 和 HTML 声明可以提供强证据，任意字节内容通常不能。业务协议如果规定了编码，应优先遵守
协议，不要用启发式探测覆盖它。

### 把 `System` 当作固定编码

Windows 的系统代码页可能随用户环境变化；跨机器存储或网络协议应选择明确编码，通常是 UTF-8。

### 共享一个实例并发转换

内部残留状态和错误计数都会被竞争修改。需要并行转换时，为每条任务创建独立实例。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `Encoding` | 指定内置字符编码 | `System` 有平台差异；扩展 ICU codec 不一定有对应枚举。 |
| `Flag` / `Flags` | 配置状态、替代字符和 BOM 策略 | `Stateless` 会放弃跨调用残片；`ConvertInitialBom` 与 `WriteBom` 方向不同。 |
| `FinalizeResultError` | 描述结束处理结果 | 区分无错误、存在无效字符和输出空间不足。 |
| `FinalizeResultChar<Char>` | 返回结束位置、无效字符数和错误 | `next` 指向调用方缓冲区；`NotEnoughSpace` 时可扩大缓冲区后重试。 |
| `isValid() const` | 判断是否绑定了有效 codec | 名称构造可能失败；无效对象不能正常转换。 |
| `hasError() const` | 查询累计是否遇到无效字符 | 不是单次调用状态；重置前会持续为真。 |
| `resetState()` | 清除转换状态与错误 | 同时丢弃未完成序列，只应在流边界使用。 |
| `name() const` | 取得当前 codec 名称 | 返回的指针不归调用方所有；无效对象先检查 `isValid()`。 |
| `availableCodecs()` | 列出本构建支持的 codec 名称 | 可受 ICU 构建选项影响；返回顺序不稳定。 |
| `encodingForData(data, expected)` | 根据 BOM/开头模式探测 UTF 编码 | 无法确定时返回 `nullopt`，不是通用统计检测器。 |
| `encodingForHtml(data)` | 按 HTML 声明和 BOM 选择编码 | 未声明默认 UTF-8；声明不受支持则返回 `nullopt`。 |
| `encodingForName(name)` | 将名称映射到内置 `Encoding` | 不代表全部 ICU codec；失败返回 `nullopt`。 |
| `nameForEncoding(encoding)` | 取得内置枚举的规范名称 | 参数应是有效 `Encoding` 值，返回指针不需释放。 |

## 选择建议

- 已知外部编码：直接构造 `QStringDecoder` 或 `QStringEncoder`。
- HTML 字节流：优先使用 `QStringDecoder::decoderForHtml()`。
- 只需一次 UTF-8 转换：`QString::fromUtf8()` / `QString::toUtf8()` 更直接。
- 输入会分块、需要错误累计或结束检查：使用状态化 converter。

一句话说，`QStringConverter` 管的是“这条编码转换流现在处于什么状态”；真正的数据方向由
`QStringDecoder` 和 `QStringEncoder` 决定。
