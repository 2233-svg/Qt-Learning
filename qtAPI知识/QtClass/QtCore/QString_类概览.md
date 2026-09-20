# QString：Qt 的 Unicode 文本值类型

> Qt 6.11.1 | `#include <QString>` | 模块：`Qt6::Core`

`QString` 是 Qt 应用中保存和处理文本的默认类型。它存储 `QChar` 序列，每个 `QChar` 是一个 UTF-16 代码单元；绝大多数 UI 文本、路径、翻译结果、JSON 字符串和 Qt API 的文本参数都应使用它，而不是把 `QByteArray` 当文本容器。

`QString` 解决的不是“存几个 char”，而是把 Unicode、编码转换、共享复制和常见文本操作放进一致的值类型接口。它是可重入的，并采用隐式共享（copy-on-write）。

## 先分清三个层次

```text
QString            已解码的 Unicode 文本，按 UTF-16 代码单元存储
QByteArray         字节；可以是 UTF-8，也可以是任意二进制
QStringView        不拥有 UTF-16 数据的视图，调用者负责生命周期
```

不要根据变量类型为 `char *` 或 `QByteArray` 就猜编码。编码必须来自协议、文件格式或 API 契约，然后显式选择 `fromUtf8()`、`fromLatin1()`、`fromLocal8Bit()` 或 `QStringDecoder`。

## 基本用法

```cpp
const QString user = QString::fromUtf8(userNameBytes);
const QString message = QStringLiteral(u"Hello, %1").arg(user);

if (message.contains(u"hello", Qt::CaseInsensitive))
    showMessage(message);
```

已知的编译期文字优先使用 `QStringLiteral(u"...")`，或在合适的命名空间中使用 `u"..."_s`。这避免了运行时从 UTF-8 字面量转换并分配字符串数据。

## UTF-16 不是“字符数”

`size()`、下标、`mid()`、`left()`、`right()`、`indexOf()` 的位置都以 UTF-16 **代码单元**为单位。BMP 以外的字符由一个代理对（两个 `QChar`）表示；用户眼里的一个字符还可能由多个 code point 和组合符构成。

```cpp
const QString text = QString::fromUtf8(u8"A😀");
// text.size() == 3：'A' 一个 QChar，😀 一个代理对
```

因此，光标移动、按“用户可见字符”截断、表情符号处理和自然语言分词不应简单 `++index` 或按 `size()` 计数。需要时使用 `QTextBoundaryFinder` 或与界面组件的文本边界规则配合。

`QString` 可以包含嵌入的 `QChar::Null`；`size()` 会计入它。只有接受 `const char *` 的传统 C API 才会在 `'\0'` 处结束，不能用来传含 NUL 的文本。

## 编码转换的边界

### 输入字节

- `fromUtf8()`：网络协议、JSON、现代文件格式和大多数跨平台数据的默认选择。
- `fromLatin1()`：协议明确规定 Latin-1 或仅 ASCII 时使用。
- `fromLocal8Bit()`：仅用于明确依赖操作系统本地编码的边界；它不适合可移植文件格式。
- 其他编码：使用 `QStringDecoder`，并保留 decoder 状态以处理分块输入。

未注明其他编码时，`QString` 接受的 `const char *` 和 `QByteArray` 转换按 UTF-8 理解。`const char *` 是以 NUL 结束的 C 字符串；需要保留嵌入 NUL 时传 `QByteArrayView` / `QByteArray` 或显式长度。

### 输出字节

- `toUtf8()`：可无损表示 Unicode，优先用于跨平台传输和存储。
- `toLatin1()`：无法表示的字符会丢失信息，不应用于任意用户文本。
- `toLocal8Bit()`：结果依赖平台本地编码；不能把它当稳定交换格式。

`qPrintable()`、`qUtf8Printable()`、`qUtf16Printable()` 返回的指针只在**当前完整语句**中有效。若要跨语句传递，先把 `toUtf8()` / `toLocal8Bit()` 的结果保存为 `QByteArray`。

## 值语义、引用与迭代器

复制 `QString` 通常只增加共享数据的引用计数；第一次非 const 操作可能 detach 并深拷贝数据。这让按值传递和返回很自然，却带来一个关键边界：

> 对一个 QString 调用任何非 const 成员后，之前取得的迭代器、`QChar &`、`data()`、`constData()`、`unicode()` 或 `utf16()` 指针都不应继续使用。

`at()` 只读访问不会触发深拷贝；非 const `operator[]`、`begin()`、`data()` 等可能触发 detach。遍历时不要持有迭代器又修改同一个字符串。

```cpp
QString value = QStringLiteral(u"draft");
const QChar *chars = value.constData();

value.append(u'!'); // chars 可能已失效
```

## 常见文本任务

### 格式化

`arg()` 替换 `%1` 到 `%99` 占位符，适合翻译文本和简单展示：

```cpp
const QString status = tr("Processed %1 of %2 files").arg(done).arg(total);
```

占位符带 `L`（如 `%L1`）且十进制时使用默认 locale。需要货币、日期、复数和严格地区格式时，使用 `QLocale` 和 Qt 的翻译系统，不要把格式规则硬编码在字符串中。

### 搜索、比较和切分

`contains()`、`indexOf()`、`startsWith()`、`endsWith()`、`count()` 支持 `QChar`、字符串视图和正则等常用匹配对象。`compare()` 与比较运算符按 UTF-16 代码单元的词典序比较，快但不一定符合用户语言习惯；UI 排序使用 `localeAwareCompare()` 或 `QCollator`。

`split()` 会创建 `QStringList`；只想懒惰遍历字段时用 `tokenize()`。`section()` 根据分隔符选段，`SectionSkipEmpty`、`SectionIncludeLeadingSep` 等标志决定空字段和分隔符是否保留。

### 修改与分配

`append()`、`prepend()`、`insert()`、`replace()`、`remove()` 是原地修改入口。已知最终长度时先 `reserve()`，重复构建长字符串时可减少重分配；多段拼接可使用 `QStringBuilder` 的 `%` 运算符，或合理地连续 `append()`。

`sliced()`、`first()`、`last()`、`chopped()` 返回新 `QString`；`slice()`、`chop()`、`truncate()` 原地改变对象。它们的索引仍是代码单元索引。

## 原始 UTF-16 数据：只在确有必要时使用

`fromRawData()` 和 `setRawData()` 让 `QString` 借用外部 `QChar` / `char16_t` 缓冲区，不复制数据。它们主要用于非常底层的互操作：

- 外部缓冲区必须至少存活到 QString 不再引用它为止。
- 得到的字符串可能没有 NUL 终止。
- 修改字符串时通常会触发分离并复制；不要依赖这种副作用管理生命周期。
- 需要保证终止符时，Qt 6.10 起使用 `nullTerminate()` 或 `nullTerminated()`，它们可能导致分配或复制。

普通代码应优先用深拷贝构造、`QStringView` 或 `QSpan<const QChar>` 风格的明确借用接口，避免把所有权藏在 `QString` 的特殊状态里。

## 常见错误

1. **把 UTF-16 索引当 Unicode 字符或用户可见字素。** 表情、组合字符和复杂文字会出错。
2. **对未知字节默认 `fromLocal8Bit()`。** 协议没有本地编码；优先从格式规范取得编码。
3. **保留 `qUtf8Printable()` 指针。** 它指向临时 `QByteArray`，语句结束即失效。
4. **在迭代时修改同一个 QString。** detach 会使迭代器和字符引用失效。
5. **用 `isNull()` 表示“没有内容”。** 除 `isNull()` 外，Qt 几乎所有 API 都把 null 与 empty 同等对待；业务判断通常应使用 `isEmpty()`。
6. **用 `toLatin1()` 保存任意文本。** 不可表示字符会失真，跨平台数据使用 UTF-8。
7. **反复使用 `+` 拼接长文本。** 已知规模时 `reserve()` + `append()`，或使用 QStringBuilder。

## API 速查表

| 类别 | API | 语义 | 使用边界 |
| --- | --- | --- | --- |
| 构造 | `QString()` / `QString(QChar)` / `QString(size, QChar)` | 创建空串、单字符或重复字符文本。 | 默认构造为 null 且 empty；一般只关心 `isEmpty()`。 |
| UTF-16 构造 | `QString(const QChar *, size)` / `QString(QStringView)` | 从 UTF-16 数据复制构造。 | 传入长度时可以包含 NUL；代码单元不等于字符数。 |
| UTF-8 便利构造 | `QString(const char *)` / `QString(QByteArray)` | 按 UTF-8 转换。 | `const char *` 以 NUL 结束；工程可用宏禁用隐式 ASCII 转换。 |
| 字面量 | `QStringLiteral()` / `u"..."_s` | 编译期生成 QString 数据。 | 静态文本优先使用；若 API 接受 `QLatin1StringView`，`_L1` 可能更轻。 |
| 字节解码 | `fromUtf8()` / `fromLatin1()` / `fromLocal8Bit()` | 明确从三种常用 8 位编码创建字符串。 | 编码由数据协议决定；本地编码不适合稳定格式。 |
| 宽字符解码 | `fromUtf16()` / `fromUcs4()` / `fromWCharArray()` | 从 UTF-16、UTF-32 或平台 `wchar_t` 创建。 | `wchar_t` 在 Windows 常为 UTF-16，Unix 常为 UTF-32。 |
| 字节编码 | `toUtf8()` / `toLatin1()` / `toLocal8Bit()` | 编码为 `QByteArray`。 | 跨平台交换用 UTF-8；Latin-1 和本地编码可能丢失或依赖平台。 |
| 标准库互操作 | `fromStdString()`、`toStdString()`、`toStdU16String()`、`toStdU32String()`、`toStdWString()` | 与标准字符串类型转换。 | `std::string` 使用 UTF-8；`wstring` 宽度依平台不同。 |
| 状态 | `isEmpty()` / `isNull()` / `size()` / `length()` | 查询空、null、代码单元数。 | 大部分业务只使用 `isEmpty()`；大小不是字素数量。 |
| 元素 | `at()` / `operator[]` / `front()` / `back()` | 读取或修改单个 `QChar`。 | 索引是 UTF-16 代码单元；非 const 访问可能 detach。 |
| 数据指针 | `data()` / `constData()` / `unicode()` / `utf16()` | 取得 UTF-16 数据指针。 | 非 const 调用后指针失效；`unicode()` 结果不保证 NUL 终止。 |
| NUL 终止 | `nullTerminate()` / `nullTerminated()` | 确保 UTF-16 数据有终止符。 | Qt 6.10 起；可能复制或分配。 |
| 原始借用 | `fromRawData()` / `setRawData()` | 不复制外部 UTF-16 缓冲区。 | 调用方承担缓冲区寿命；默认不保证 NUL 终止。 |
| 容量 | `reserve()` / `capacity()` / `squeeze()` | 预留、查询或压缩容量。 | 预知拼接规模时 reserve；squeeze 可能产生额外代价。 |
| 拼接 | `append()` / `prepend()` / `operator+=` / `operator+` | 组合字符串。 | 长链 `+` 可能多次分配；注意字节参数按 UTF-8 解码。 |
| 编辑 | `insert()` / `remove()` / `replace()` / `fill()` / `clear()` | 原地修改内容。 | 修改会使迭代器、引用和数据指针失效。 |
| 子串 | `first()` / `last()` / `left()` / `right()` / `mid()` / `sliced()` / `chopped()` | 返回部分文本。 | 按代码单元切分，可能切开代理对或组合序列。 |
| 原地裁剪 | `slice()` / `chop()` / `truncate()` | 原地保留一段或删除尾部。 | 参数要在范围内；按代码单元处理。 |
| 搜索 | `contains()` / `indexOf()` / `lastIndexOf()` / `count()` | 查找字符、字符串或正则。 | 明确大小写与正则代价；返回位置是代码单元索引。 |
| 前后缀 | `startsWith()` / `endsWith()` | 判断前缀或后缀。 | 默认大小写敏感，可指定 `Qt::CaseSensitivity`。 |
| 比较 | `compare()` / 关系运算符 | 按 UTF-16 代码单元词典序比较。 | 不等于自然语言排序；UI 使用 `localeAwareCompare()` 或 `QCollator`。 |
| 分割 | `split()` / `tokenize()` / `section()` | 拆分、惰性 token 化或取分段。 | `split()` 分配列表；`tokenize()` 返回对象应使用 `auto` 保存。 |
| 大小写 | `toLower()` / `toUpper()` / `toCaseFolded()` | Unicode 大小写或 case fold 转换。 | 不是 locale 专用规则；特殊语言规则可能需要额外处理。 |
| 规范化 | `normalized(NormalizationForm)` | 生成 D/C/KD/KC Unicode 规范化结果。 | 比较、查重和协议要求规范化时显式调用，不要默认猜测。 |
| 数字 | `number()` / `setNum()` / `toInt()` 等 | 数值格式化与解析。 | 解析时检查 `ok`；本地化展示优先 `QLocale`。 |
| 占位格式 | `arg()` | 替换 `%1` 到 `%99`。 | `%L1` 十进制使用默认 locale；适合翻译文本。 |
| HTML | `toHtmlEscaped()` | 转义 HTML 特殊字符。 | 只做转义，不等价于完整 HTML 安全策略或富文本净化。 |
| 正则 | `indexOf(QRegularExpression)`、`replace(QRegularExpression)`、`split(QRegularExpression)` | 使用正则查找、替换、切分。 | 检查正则有效性，避免把不可信复杂模式放进热点路径。 |
| 宏 | `QT_NO_CAST_FROM_ASCII` / `QT_RESTRICTED_CAST_FROM_ASCII` / `QT_NO_CAST_TO_ASCII` | 收紧 8 位字符串的隐式转换。 | 大型项目建议用它们迫使编码在边界处显式表达。 |
| 临时 C 指针 | `qPrintable()` / `qUtf8Printable()` / `qUtf16Printable()` | 获取临时本地编码、UTF-8、UTF-16 C 指针。 | 只在同一完整语句调用 C API；不能保存指针。 |

`QString` 的日常用法可以很简单：文本留在 QString 中，跨字节边界时显式编码，涉及索引时记住 UTF-16，涉及引用时记住 copy-on-write。这样大多数国际化与生命周期问题会自然消失。
