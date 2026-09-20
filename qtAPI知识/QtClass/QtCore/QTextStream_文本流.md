# Qt QTextStream 文本流

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextStream>`  
> 所属模块：`Qt6::Core`  
> 继承关系：`QIODeviceBase -> QTextStream`  
> 类型特征：不可复制；Qt 6 中通常为 final；所有成员函数可重入  
> 定位：在 `QIODevice`、`QString`、`QByteArray`、`FILE *` 上按文本语义读写 Unicode 字符、行、词和数字

## 它解决什么问题

`QTextStream` 是 Qt 的“文本 I/O 适配层”。底层设备读写的是字节，但业务代码通常想读写的是 `QString`、一行文本、一个词、整数、浮点数，且还要处理编码、BOM、数字格式、字段宽度、对齐、填充字符和区域设置。`QTextStream` 把这些规则包装成流式接口：

```cpp
out << "value=" << 42 << Qt::endl;
in >> name >> score;
```

它和 `QDataStream` 的定位不同：`QTextStream` 面向人类可读文本，受编码、locale 和格式化选项影响；`QDataStream` 面向二进制序列化，适合稳定的机器读写格式。

## 实际使用场景

- 逐行读取 UTF-8、UTF-16、UTF-32 或带 BOM 的文本文件。
- 写配置、日志、报表、命令行输出等人类可读文本。
- 从 `stdin` 读入词、数字或整行，向 `stdout` / `stderr` 输出。
- 在内存中的 `QString` 或 `QByteArray` 上复用同一套文本解析逻辑。
- 生成对齐表格、十六进制/八进制/二进制数字、固定精度浮点文本。

它不适合直接读写任意二进制数据。文本流会做编码转换、换行和数字解析；处理图片、压缩包、协议帧时应使用 `QIODevice` 的字节 API 或 `QDataStream`。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QTextStream>
```

qmake 工程使用：

```qmake
QT += core
```

头文件有一个实际边界：如果其他头文件已经定义了名为 `Status` 的宏，再包含 `qtextstream.h` 会报错。遇到老式平台头或第三方 C 头时，优先在它们之前包含 `<QTextStream>`，或者清理有问题的宏。

## 最小可用示例

```cpp
#include <QFile>
#include <QTextStream>

QStringList readLines(const QString &path)
{
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
        return {};

    QTextStream in(&file);
    in.setEncoding(QStringConverter::Utf8);

    QStringList lines;
    QString line;
    while (in.readLineInto(&line))
        lines.append(line);

    return lines;
}
```

`readLine()` 和 `readLineInto()` 返回的行不包含末尾的 `\n` 或 `\r\n`。不要习惯性地再调用 `trimmed()`，除非你确实想去掉行首行尾的普通空白。

## 绑定对象与生命周期

`QTextStream` 自己不是文件，也不是 socket。它要绑定到一个后端：

- `QIODevice *`：最常见，例如 `QFile`、`QBuffer`、`QTcpSocket`。
- `FILE *`：常用于 `stdin`、`stdout`、`stderr`。
- `QString *`：直接在字符串上读写，编码设置不起作用。
- `QByteArray *`：内部用 `QBuffer` 包装，可按 open mode 读写字节数组。
- `const QByteArray &`：只读包装，适合解析常量字节片段。

构造或 `setDevice()` / `setString()` 绑定后，外部对象必须在 `QTextStream` 使用期间保持有效。析构时，如果流绑定的是设备，会隐式 `flush()`；文档明确说设备本身不受影响。也就是说，流会刷新自己的文本缓冲，但不会替你设计文件关闭、socket 断开或外部对象寿命。

默认构造的流没有绑定任何设备或字符串，必须先调用 `setDevice()` 或 `setString()` 才能读写。

## 编码、BOM 与 QString 后端

`QTextStream` 内部使用基于 Unicode 的缓冲，通过 `QStringConverter` 在字节和文本之间转换。默认编码是 UTF-8，自动 Unicode 检测默认开启：读取时若看到 UTF-8、UTF-16 或 UTF-32 的 BOM，会切换到对应 UTF 编码。

写出时默认不生成 BOM。需要 BOM 时，必须在写入任何数据之前调用：

```cpp
out.setEncoding(QStringConverter::Utf8);
out.setGenerateByteOrderMark(true);
```

一旦已经写过数据，再调用 `setGenerateByteOrderMark(true)` 不会补写 BOM。

如果流直接操作 `QString`，编码被禁用：字符串已经是 Qt 的 Unicode 文本，不需要字节编码转换。`setEncoding()` 对这种后端无效。

不要在已经从顺序 socket 读取了一部分数据后随意切换编码。文档警告：内部缓冲里可能还残留按旧编码解码出的文本。

## 读取模型

`QTextStream` 支持三类读取方式：

- 块读取：`read(maxlen)`、`readAll()`。
- 行读取：`readLine()`、`readLineInto()`。
- 格式化读取：`operator>>` 读取字符、词、数字。

`atEnd()` 与 `QIODevice::atEnd()` 不完全相同，因为它还考虑了 `QTextStream` 自己的 Unicode 缓冲。文本流有缓冲，所以 `pos()` 可能为了重建设备位置而 seek 底层设备；这可能很昂贵，不要在紧密循环里频繁调用。

`readAll()` 会把剩余内容一次性读入内存，大文件应避免使用。未知大小的输入优先 `readLineInto()`；如果目标 `QString` 容量足够，它可以减少分配。

`operator>>(QString &)` 读取一个词，词由 `QChar::isSpace()` 认定的空白分隔，并跳过前导空白。`operator>>(QChar &)` 读取一个字符，不跳过空白。数字读取会跳过前导空白，并按当前 `integerBase()`、`realNumberNotation()` 和 `locale()` 解析。

## 写入与格式化

写入 `QString`、`QStringView`、`QLatin1StringView`、`QChar`、数字和指针都走文本格式化。写 `QString` 会按当前编码转成字节；写 `QByteArray` 时，内容会先按 UTF-8 转为 `QString`；写 `const char *` 时，指针必须指向以 `\0` 结束的 UTF-8 文本。

字段宽度、填充与对齐是持久设置：

```cpp
QString text;
QTextStream out(&text);
out << qSetFieldWidth(8) << Qt::left << "A" << 12;
out.setFieldWidth(0);
out << " done";
```

这一点和 C++ iostream 不同：`setFieldWidth()` 不是“只对下一个元素生效”，而是对之后写入的每个元素都生效，甚至包括 `Qt::endl`。用完后通常要设回 `0`。

浮点默认使用 `SmartNotation`，精度默认 `6`。在 `FixedNotation` 和 `ScientificNotation` 下，精度表示小数位数；在 `SmartNotation` 下，精度表示最大有效数字数。精度不能为负数。

整数基数默认是 `0`。读取时 `0` 表示自动检测前缀；写出时若未显式设置，按十进制输出。可显式设置为 `2`、`8`、`10`、`16`。

## 状态与错误

`status()` 返回文本流状态。常见状态包括：

- `Ok`：正常。
- `ReadPastEnd`：已经读过底层数据末尾。
- `ReadCorruptData`：读到损坏数据。
- `WriteFailed`：无法写入底层设备。

Qt 6.10 起，`explicit operator bool()` 等价于 `status() == Ok`。流式读取/写入后，应在关键边界检查状态；I/O 错误不会自动抛异常。

`setStatus()` 有一个容易忽略的规则：第一次设置状态后，后续 `setStatus()` 会被忽略，直到调用 `resetStatus()`。这可以保留最早的错误原因，但如果你手动复用流状态，必须明确 reset。

`reset()` 只重置格式化选项，让它回到构造时默认值；它不替换设备、不清空字符串，也不丢弃已有缓冲数据。

## 常用操纵器

`QTextStream` 支持 Qt 命名空间中的流操纵器。它们本质上是对 setter 的流式语法：

| 操纵器 | 等价操作 |
| --- | --- |
| `Qt::bin` / `Qt::oct` / `Qt::dec` / `Qt::hex` | 设置整数基数为 2 / 8 / 10 / 16 |
| `Qt::showbase` / `Qt::noshowbase` | 打开/关闭基数前缀 |
| `Qt::forcesign` / `Qt::noforcesign` | 打开/关闭正数强制显示符号 |
| `Qt::forcepoint` / `Qt::noforcepoint` | 打开/关闭强制显示小数点 |
| `Qt::uppercasebase` / `Qt::lowercasebase` | 设置 `0x`、`0b` 等前缀大小写 |
| `Qt::uppercasedigits` / `Qt::lowercasedigits` | 设置 10 到 35 的数字字母大小写 |
| `Qt::fixed` / `Qt::scientific` | 设置浮点表示法 |
| `Qt::left` / `Qt::right` / `Qt::center` | 设置字段对齐 |
| `Qt::endl` | 写入换行并 flush |
| `Qt::flush` | flush |
| `Qt::reset` | reset 格式选项 |
| `Qt::ws` | 跳过空白 |
| `Qt::bom` | 开启 BOM 生成 |

带参数的全局操纵器包括 `qSetFieldWidth(width)`、`qSetPadChar(ch)`、`qSetRealNumberPrecision(precision)`。

## 常见误区

- 用 `QTextStream` 处理二进制文件，结果被编码转换破坏。
- 构造了默认流却没有绑定设备或字符串。
- 在写入后才开启 BOM，期望它补写文件开头。
- 调用 `setFieldWidth()` 后忘记恢复为 `0`，导致后续所有元素都被填充。
- 用 `readAll()` 读大文件，造成内存峰值过高。
- 读取一行后再无差别 `trimmed()`，误删有意义的前导或尾随空格。
- 把 `const char *` 输出当作任意字节输出；它必须是以 `\0` 结束的 UTF-8 文本。
- 使用 `operator>>(char *c)`，却没有提供足够大的缓冲区。这个重载很危险，优先使用 `QByteArray` 或 `QString`。
- 在顺序 socket 上读了一部分后切换编码，忽略内部缓冲可能仍含旧编码文本。
- 频繁调用 `pos()`，忽略它可能触发底层 seek。

## 关键 API 语义

### 构造与绑定

`QTextStream()` 创建未绑定流；`QTextStream(QIODevice *)` 绑定设备；`QTextStream(FILE *, OpenMode)` 通过内部 `QFile` 适配 C `FILE *`；`QTextStream(QString *, OpenMode)` 直接读写字符串；`QTextStream(QByteArray *, OpenMode)` 通过内部 `QBuffer` 读写字节数组；`QTextStream(const QByteArray &, OpenMode)` 只读访问常量字节数组。

`setDevice()` 替换当前设备，替换前会 `flush()` 旧设备，并把 locale 重置为默认 C、编码重置为 UTF-8。`setString()` 绑定字符串；若已有设备，也会先 `flush()`。

### 编码控制

`encoding()` / `setEncoding()` 查询或设置设备字节流编码。默认 UTF-8；字符串后端无效。`autoDetectUnicode()` / `setAutoDetectUnicode()` 控制 BOM 自动检测，默认开启。`generateByteOrderMark()` / `setGenerateByteOrderMark()` 控制写出 BOM，默认关闭，且必须在第一次写入前设置。

### 位置与缓冲

`atEnd()` 检查文本流是否无更多可读数据，会考虑内部 Unicode 缓冲。`pos()` 返回与当前流位置对应的设备位置，失败返回 `-1`；可能昂贵。`seek(pos)` 跳到设备位置，成功返回 `true`。`flush()` 把待写文本推到底层设备；字符串后端调用它没有效果。析构时若绑定设备会隐式 `flush()`。

### 读取函数

`read(maxlen)` 最多读指定字符数；`readAll()` 读完剩余内容；`readLine(maxlen)` 读一行并去掉行尾；`readLineInto(line, maxlen)` 读一行到已有 `QString`，可减少分配，EOF 或错误返回 `false`。`skipWhiteSpace()` 丢弃空白直到非空白或结束。

### 格式选项

`fieldWidth()` / `setFieldWidth()` 控制字段宽度，`0` 表示按文本长度；设置后持续生效。`fieldAlignment()` / `setFieldAlignment()` 控制填充位置。`padChar()` / `setPadChar()` 控制填充字符，默认空格。`integerBase()` / `setIntegerBase()` 控制整数基数，`0` 表示读取自动检测。`numberFlags()` / `setNumberFlags()` 控制基数前缀、符号、小数点和大小写。`realNumberNotation()`、`setRealNumberNotation()`、`realNumberPrecision()`、`setRealNumberPrecision()` 控制浮点输出。`locale()` / `setLocale()` 控制数字和字符串表示之间的区域设置；默认是 C locale，且为兼容性不使用千位分隔符。

### 状态函数

`status()` 返回当前状态。`setStatus()` 可手动设置状态，但在 `resetStatus()` 前后续设置会被忽略。`resetStatus()` 清除状态。`operator bool()`（Qt 6.10）在状态为 `Ok` 时为 `true`。`reset()` 重置格式选项，不改变绑定对象和缓冲。

### 流运算符

输出重载覆盖 `QChar`、`char`、`char16_t`（Qt 6.3.1）、`QString`、`QStringView`、`QLatin1StringView`、`QByteArray`、`const char *`、`const void *`、整数类型和浮点类型。输入重载覆盖 `QChar`、`char`、`char16_t`（Qt 6.4）、`QString`、`QByteArray`、`char *`、整数类型和浮点类型。

`QString` 输入读一个以空白分隔的词；`QChar` 输入读单个字符且不跳过空白；数字输入失败时目标通常被置为零并设置状态；`char *` 输入要求调用方提供足够缓冲，优先避免。

## API 速查表

### 枚举与标志

| API | 作用 | 重点边界 |
| --- | --- | --- |
| `FieldAlignment` | 字段宽度大于内容时的对齐方式 | `AlignAccountingStyle` 会让数字符号贴左、数字贴右 |
| `NumberFlag` / `NumberFlags` | 控制数字输出前缀、符号、小数点和大小写 | 是 `QFlags`，用 OR 组合 |
| `RealNumberNotation` | 选择 `Smart`、`Fixed`、`Scientific` 浮点表示 | 精度含义随 notation 变化 |
| `Status` | 描述文本流状态 | I/O 错误靠状态表示，不抛异常 |

### 构造与绑定

| API | 作用 | 重点边界 |
| --- | --- | --- |
| `QTextStream()` | 创建未绑定流 | 读写前必须绑定设备或字符串 |
| `QTextStream(QIODevice *device)` | 在设备上读写文本 | 设备需已按合适模式打开并保持有效 |
| `QTextStream(FILE *fileHandle, OpenMode)` | 适配 C `FILE *` | 常用于 `stdin`、`stdout`、`stderr` |
| `QTextStream(QString *string, OpenMode)` | 直接读写字符串 | 编码设置不起作用 |
| `QTextStream(QByteArray *array, OpenMode)` | 通过内部 `QBuffer` 读写字节数组 | 数组必须保持有效 |
| `QTextStream(const QByteArray &array, OpenMode)` | 只读解析常量字节数组 | 无论 open mode 如何，数组只读 |
| `~QTextStream()` | 销毁流 | 绑定设备时隐式 `flush()`，不替你管理外部对象生命周期 |
| `setDevice()` / `device()` | 替换或查询当前设备 | 替换前 flush；会重置 locale 和编码 |
| `setString()` / `string()` | 替换或查询当前字符串后端 | 若已有设备会先 flush |

### 编码与 BOM

| API | 作用 | 重点边界 |
| --- | --- | --- |
| `setEncoding()` / `encoding()` | 设置/查询字节编码 | 默认 UTF-8；字符串后端无效 |
| `setAutoDetectUnicode()` / `autoDetectUnicode()` | 控制读取时 BOM 自动检测 | 默认开启；可与 UTF-8 默认编码配合 |
| `setGenerateByteOrderMark()` / `generateByteOrderMark()` | 控制写出 BOM | 默认关闭；必须在任何写入前调用 |

### 读写与位置

| API | 作用 | 重点边界 |
| --- | --- | --- |
| `atEnd()` | 判断文本流是否读完 | 与 `QIODevice::atEnd()` 不同，会看内部缓冲 |
| `read(maxlen)` | 最多读 `maxlen` 个字符 | 返回 `QString` |
| `readAll()` | 读完剩余文本 | 大文件慎用 |
| `readLine(maxlen)` | 读一行，不含行尾 | EOF 返回 null `QString` |
| `readLineInto(line, maxlen)` | 读一行到已有字符串 | EOF 或错误返回 `false`；会丢弃原内容 |
| `skipWhiteSpace()` | 跳过 `QChar::isSpace()` 空白 | 适合逐字符读取前清理空白 |
| `flush()` | 刷新待写文本到底层设备 | 字符串后端无效果 |
| `pos()` | 返回当前对应设备位置 | 失败为 `-1`；可能触发昂贵 seek |
| `seek(pos)` | 移动到底层设备位置 | 成功返回 `true` |

### 格式化

| API | 作用 | 重点边界 |
| --- | --- | --- |
| `setFieldWidth()` / `fieldWidth()` | 控制字段宽度 | 持续作用于之后所有元素，不只下一项 |
| `setFieldAlignment()` / `fieldAlignment()` | 控制字段对齐 | 与 field width 配合 |
| `setPadChar()` / `padChar()` | 控制填充字符 | 默认空格 |
| `setIntegerBase()` / `integerBase()` | 控制整数基数 | 只允许 `0`、`2`、`8`、`10`、`16` |
| `setNumberFlags()` / `numberFlags()` | 控制数字前缀、符号、大小写等 | 影响生成文本 |
| `setRealNumberNotation()` / `realNumberNotation()` | 控制浮点表示法 | 默认 `SmartNotation` |
| `setRealNumberPrecision()` / `realNumberPrecision()` | 控制浮点精度 | 默认 6，不能为负 |
| `setLocale()` / `locale()` | 控制数字文本转换 locale | 默认 C locale |
| `reset()` | 恢复格式选项默认值 | 不改变设备、字符串和缓冲 |

### 状态与判断

| API | 作用 | 重点边界 |
| --- | --- | --- |
| `status()` | 查询当前状态 | 读取/写入后用它判断错误 |
| `setStatus()` | 手动设置状态 | reset 前后续设置被忽略 |
| `resetStatus()` | 清除状态 | 允许后续重新设置 |
| `operator bool()`（Qt 6.10） | 判断状态是否为 `Ok` | 显式转换，等价于 `status() == Ok` |

### 运算符与操纵器

| API | 作用 | 重点边界 |
| --- | --- | --- |
| `operator<<` 字符串类 | 写 `QString`、`QStringView`、`QLatin1StringView`、`QByteArray`、`const char *` | `QByteArray` 和 `const char *` 按 UTF-8 文本处理；`const char *` 必须以 `\0` 结束 |
| `operator<<` 字符类 | 写 `QChar`、`char`、`char16_t` | `char16_t` 输出自 Qt 6.3.1 起提供 |
| `operator<<` 数字类 | 写整数和浮点数 | 受 base、flags、notation、precision、locale 影响 |
| `operator<< const void *` | 以带基数的十六进制写指针 | 用于文本调试输出 |
| `operator>> QString` / `QByteArray` | 读取一个以空白分隔的词 | `QByteArray` 保存 UTF-8 |
| `operator>> QChar` / `char` / `char16_t` | 读取单个字符 | `QChar` 不跳过空白；`char16_t` 输入自 Qt 6.4 起提供 |
| `operator>>` 数字类 | 读取整数和浮点数 | 前导空白会跳过；基数可自动检测 |
| `operator>> char *` | 读取一个词到 C 缓冲 | 危险，缓冲至少需 `3*n+1` 字节；优先用 `QByteArray` |
| `Qt::bin/oct/dec/hex` | 设置整数基数 | 等价于 `setIntegerBase()` |
| `Qt::showbase/forcesign/forcepoint` 等 | 设置或清除 `NumberFlags` | 修改持久格式状态 |
| `Qt::fixed/scientific` | 设置浮点表示 | 等价于 `setRealNumberNotation()` |
| `Qt::left/right/center` | 设置字段对齐 | 等价于 `setFieldAlignment()` |
| `Qt::endl` / `Qt::flush` | 写换行并刷新 / 仅刷新 | `Qt::endl` 会 flush |
| `Qt::reset` / `Qt::ws` / `Qt::bom` | 重置格式、跳过空白、开启 BOM | `Qt::bom` 仍需在写入前使用 |
| `qSetFieldWidth()` | 带参数设置字段宽度 | 等价于 `setFieldWidth()` |
| `qSetPadChar()` | 带参数设置填充字符 | 等价于 `setPadChar()` |
| `qSetRealNumberPrecision()` | 带参数设置浮点精度 | 等价于 `setRealNumberPrecision()` |

## 一句话总结

`QTextStream` 是字节设备和 Unicode 文本之间的格式化桥梁；正确使用的关键是先明确后端生命周期，再明确编码/BOM，最后把字段宽度、locale、状态和缓冲这些“会持续影响后续读写”的设置管住。
