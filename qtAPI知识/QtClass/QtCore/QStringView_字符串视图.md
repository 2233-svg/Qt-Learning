# QStringView：不拥有字符数据的 UTF-16 视图

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStringView>`  
> CMake：`Qt6::Core`

`QStringView` 是一个轻量的、非拥有型 UTF-16 字符串视图。它只保存“首地址 + 长度”，不会
分配、复制或释放字符数据，适合把函数参数从 `const QString &` 扩展为既能接收 QString、
字符串字面量、`char16_t` 数组又不产生临时 QString 的接口。

它解决的是接口层的拷贝和所有权问题，不是替代 `QString`。需要拥有文本、跨越源对象生命周期
保存，或修改字符时，应使用 `QString`。

## 最小使用方式

```cpp
#include <QStringView>

qsizetype findHeader(QStringView line)
{
    return line.indexOf(u":");
}

QStringView line = u"Content-Type: text/plain";
QStringView name = line.left(line.indexOf(u':'));
QString owned = name.toString();
```

视图可以读取和切片，但不拥有 `line` 的数据。`name` 只有在 `line` 的字符存储仍然有效时才
有效。

## 构造来源与生命周期

常见构造方式：

```cpp
QString text = QStringLiteral("hello");
QStringView a{text};
QStringView b{u"literal"};
QStringView c{u"abc", 3};
QStringView d{buffer, bufferLength};
```

兼容字符类型包括 `QChar`、`ushort`、`char16_t`，以及在平台上大小为 2 字节的 `wchar_t`。
从指针构造且不传长度时，QStringView 会扫描到第一个零字符；从数组字面量构造同样在第一个
`Char(0)` 处停止，除非使用 `fromArray()` 保留整个数组。

`nullptr` 可以构造 null view。带长度的构造要求长度非负；`str == nullptr` 只有在长度为 0
时才是安全的。指针范围构造的 `[first, last)` 必须有效且 `last` 不得早于 `first`。

视图不会延长任何对象的生命周期：

```cpp
QStringView bad = QStringLiteral("temporary"); // 错误：临时 QString 很快销毁
```

不要从临时 QString、局部容器、会重新分配的 `QByteArray` 或可变 `QString` 中取得 view 后
长期保存。函数若返回 `QStringView`，必须在接口契约中明确承诺源数据的存活时间；不确定时
返回 `QString` 或在调用处 `toString()`。

## null、empty 和 NUL 终止

`isNull()` 检查 `data() == nullptr`，`isEmpty()`/`empty()` 检查长度是否为 0。null view 和
empty-but-non-null view 都没有字符，但状态不同：

```cpp
QStringView nullView;
QStringView emptyView(u"", 0);
Q_ASSERT(nullView.isNull());
Q_ASSERT(emptyView.isEmpty());
```

`data()`、`constData()` 和 `utf16()` 返回的数组不保证 NUL 终止。传给需要 C 风格终止字符串的
API 前，应先调用 `toString()`，或使用同时传递指针和长度的接口。`size()`/`length()` 返回
UTF-16 code unit 数，代理对计为两个。

## 读取、切片和修改视图边界

`at()` 和 `operator[]` 读取单个 `QChar`，下标按 code unit 计数。`left()`、`right()`、
`mid()`、`first()`、`last()`、`sliced()`、`chopped()` 返回子视图，不复制字符。

```cpp
QStringView value = u"abcdef";
QStringView middle = value.sliced(2, 3); // "cde"
value.slice(1, 4);                       // value 变为 "bcde"
```

`sliced()` 返回新 view；`slice()` 改变当前 view 的首地址和长度，但不会改变源字符串。
`truncate(n)` 保留前 n 个 code unit，`chop(n)` 从末尾移除 n 个 code unit。
这些显式范围 API 要求参数处于合法范围；不能用负值表达“从末尾数”。

如果需要越界时按 Qt 容器风格进行裁剪，`mid()`、`left()`、`right()` 更适合；如果使用
`sliced()`、`first()`、`last()`、`truncate()` 等严格 API，应先验证 `pos` 和 `n`。

`trimmed()` 返回去除两端空白的子视图，仍然不拥有数据。它不是 Unicode 规范化，也不会修改
中间空白。

## 搜索、比较与 Unicode 边界

`indexOf()`、`lastIndexOf()`、`contains()`、`count()` 支持 `QChar`、`QStringView`、
`QLatin1StringView`，以及在启用正则表达式时的 `QRegularExpression`。普通字符串比较受
`Qt::CaseSensitivity` 控制；正则重载的匹配位置仍按 UTF-16 code unit 计数。

`compare()` 返回小于、等于或大于零的整数，适合排序或三路判断。`localeAwareCompare()` 使用
locale 和平台相关规则，适合面向用户的显示排序，不适合跨机器持久化排序结果。

`isValidUtf16()` 只检查 code unit 能否组成有效 UTF-16。它假定主机字节序；BOM 在这里没有
特殊意义。`isUpper()` 和 `isLower()` 是 Unicode folding 判断，不应简单理解为“字符串里
是否存在大小写字母”。

`isRightToLeft()` 提供方向判断，但它不是完整排版引擎。双向文本显示仍应交给 Qt 文本布局或
平台文本系统。

## 数值转换和编码转换

`toInt()`、`toLongLong()` 等整数函数使用 C locale；`base` 必须为 2 到 36，或为 0。base 为
0 时遵循 C 约定：`0x` 走十六进制，前导 `0` 走八进制，其余走十进制。失败时返回 0，并在
提供 `ok` 指针时写入 `false`。需要 locale 感知转换时使用 `QLocale`。

浮点转换通过 `toFloat()` / `toDouble()` 完成，同样应检查 `ok`，不能把返回 0 作为唯一的失败
判断，因为合法输入 `"0"` 也返回 0。

`toUtf8()` 能无损表示 Unicode；`toLatin1()` 和 `toLocal8Bit()` 受目标编码限制，遇到无法表示
的字符会按相应 Qt 转换规则替代。`toUcs4()` 返回 `QList<uint>`，孤立无效 UTF-16 会替换为
U+FFFD，且返回列表不以零终止。

`toWCharArray()` 不写 NUL 终止符。Windows 上 `wchar_t` 通常为 2 字节，按 UTF-16 写出；Unix
上通常为 4 字节，按 UCS-4 写出。调用方至少按 `size()` 准备足够空间，但在 Unix 上补充平面
字符会占一个 `wchar_t`，输出数量可能与 UTF-16 code unit 数不同。

## split、tokenize 与返回结果的生命周期

`split()` 返回 `QList<QStringView>`，列表本身拥有 view 对象，但不拥有字符数据。源文本销毁或
重新分配后，列表中的每个 view 都失效。

```cpp
QString line = QStringLiteral("a,b,c");
const auto fields = QStringView{line}.split(u',');
```

如果只需顺序消费，用 `tokenize()` 返回 `QStringTokenizer`，避免一次性创建列表：

```cpp
for (QStringView field : QStringView{line}.tokenize(u',',
                                                    Qt::SkipEmptyParts)) {
    process(field);
}
```

`tokenize()` 的返回类型依赖模板推导，通常用 `auto` 接收，不要显式猜写复杂模板参数。

## 与 QString、QLatin1StringView 的取舍

- `QString`：拥有数据、隐式共享、可修改、可长期保存。
- `QStringView`：不拥有数据、只读、适合参数和短期切片。
- `QLatin1StringView`：专门表示 Latin-1 字符串视图，能避免先转换成 UTF-16。
- `QByteArrayView`：字节序列视图，不应与 UTF-16 字符串视图混用。

公共函数参数若只读取文本，`QStringView` 通常比 `const QString &` 更灵活；若函数要保存参数，
不要使用 view 作为内部成员，除非同时设计清晰的所有权或生命周期契约。

## 平台与线程边界

`QStringView` 是字面量类型、原始值对象，不依赖事件循环，函数可重入。它本身没有线程归属；
安全性完全取决于底层字符存储。只读共享稳定的字符串数据可以被多个线程观察，但一个线程
修改或重新分配源 QString，另一个线程读取 view 时仍需同步。

`toCFString()` 和 `toNSString()` 仅在 macOS/iOS 可用。前者返回调用方负责释放的 Core Foundation
对象；后者返回 autoreleased Objective-C 对象。不能把这些平台 API 当作跨平台转换接口。

## 常见错误

### 把 QStringView 当成拥有型字符串

它只保存指针和长度。要跨越源对象生命周期保存，调用 `toString()`。

### 把 `data()` 当 NUL 终止数组

视图的字符数组不保证末尾有零。传给 C API 前先复制或显式传长度。

### 混淆 null 和 empty

两者长度都可能为 0，但 `isNull()` 只反映数据指针是否为空。接口语义需要区分时不要只检查
`isEmpty()`。

### 用 code point 逻辑处理 size 和索引

Qt API 的位置和长度按 UTF-16 code unit 计数，代理对占两个。

### 保存 split() 的结果却销毁源 QString

`QList<QStringView>` 不拥有每个字段。源字符串失效后所有字段都悬垂。

### 忽略数字转换的 ok

返回 0 既可能是合法值，也可能是失败。始终检查 `ok`。

### 把 `localeAwareCompare()` 用作持久化排序

它依赖 locale 和平台，适合显示排序，不保证跨机器一致。

### 对严格切片 API 传越界参数

`sliced()`、`first()`、`last()`、`truncate()`、`chop()` 等要求合法范围；先检查边界。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QStringView()` | 创建 null view | `data() == nullptr`，长度为 0。 |
| `QStringView(nullptr)` | 创建 null view | 与默认构造等价。 |
| `QStringView(const Char *, qsizetype)` | 从指针和长度创建 view | 长度非负；范围必须有效；不拥有数据。 |
| `QStringView(const Char *, const Char *)` | 从半开区间创建 view | `[first,last)` 必须有效，`last` 不得早于 `first`。 |
| `QStringView(const Char *)` | 从零终止 UTF-16 字符串创建 view | 扫描第一个零字符；指针必须有效，nullptr 安全地产生 null view。 |
| `QStringView(const Char (&)[N])` | 从字符数组/字面量创建 view | 默认遇到首个零字符停止；需要完整数组使用 `fromArray()`。 |
| `QStringView(const QString &)` | 查看 QString 数据 | QString 必须在 view 使用期间保持数据有效。 |
| `QStringView(const Container &)` | 查看兼容容器 | 使用 `std::data/std::size`；容器存储不能失效。 |
| `fromArray(const Char (&)[Size])` | 查看完整字符数组 | 不因中间 NUL 截断；数组必须保持有效。 |
| `maxSize()` | 返回理论最大 code unit 数 | Qt 6.8 起；实际受内存和平台限制。 |
| `size()` | 返回长度 | 单位是 UTF-16 code unit，代理对计两个。 |
| `length()` | `size()` 的兼容别名 | 不返回 Unicode code point 数。 |
| `data()` / `constData()` | 返回 QChar 视图指针 | 非拥有且不保证 NUL 终止。 |
| `utf16()` | 返回底层 `char16_t` 指针 | 非 NUL 终止；只在存储有效期间使用。 |
| `operator[](n)` / `at(n)` | 读取第 n 个 code unit | 下标必须合法；返回 `QChar`。 |
| `begin()` / `cbegin()` | 获取正向只读迭代器 | 指向底层数组；源数据变化会使迭代器失效。 |
| `end()` / `cend()` | 获取尾后迭代器 | 不拥有数据。 |
| `rbegin()` / `crbegin()` | 获取反向只读迭代器 | 仍按 code unit 遍历。 |
| `rend()` / `crend()` | 获取反向尾迭代器 | 与源数据生命周期绑定。 |
| `empty()` / `isEmpty()` | 判断长度是否为 0 | null 和非 null 空 view 都为 true。 |
| `isNull()` | 判断数据指针是否为空 | 与 `isEmpty()` 不同。 |
| `front()` / `first()` | 读取首个 code unit | 空 view 上调用不合法。 |
| `back()` / `last()` | 读取末个 code unit | 空 view 上调用不合法。 |
| `mid(pos, n)` | 返回容错式中间子视图 | 适合 Qt 风格的裁剪语义；仍不复制数据。 |
| `left(n)` | 返回前 n 个 code unit | n 大于长度时取整个 view。 |
| `right(n)` | 返回后 n 个 code unit | n 大于长度时取整个 view。 |
| `first(n)` | 返回前 n 个严格子视图 | n 必须在合法范围内。 |
| `last(n)` | 返回后 n 个严格子视图 | n 必须在合法范围内。 |
| `sliced(pos)` | 从 pos 到末尾返回子视图 | pos 必须合法。 |
| `sliced(pos, n)` | 返回指定范围子视图 | pos/n 必须覆盖合法范围。 |
| `chopped(n)` | 删除末尾 n 个 code unit 后返回视图 | n 必须合法。 |
| `slice(pos)` | 原地改变当前 view 的范围 | 不改变源字符，只改首地址/长度。 |
| `slice(pos, n)` | 原地设置当前 view 范围 | 参数必须合法；会影响当前 view 变量。 |
| `truncate(length)` | 原地保留前 length 个 code unit | length 越界属于错误；不修改源字符串。 |
| `chop(n)` | 原地从末尾移除 n 个 code unit | n 必须合法。 |
| `trimmed()` | 返回去两端空白的子视图 | 不复制、不修改中间内容。 |
| `compare(QStringView, cs)` | 比较两个 UTF-16 视图 | 返回负/零/正；默认大小写敏感。 |
| `compare(QLatin1StringView, cs)` | 与 Latin-1 视图比较 | 避免不必要的 QString 转换。 |
| `compare(QUtf8StringView, cs)` | 与 UTF-8 视图比较 | 按字符串语义比较，不返回字节位置。 |
| `compare(QChar)` / `compare(QChar, cs)` | 与单字符比较 | 空 view 小于单字符；返回三态比较结果。 |
| `localeAwareCompare(QStringView)` | 按 locale/平台规则比较 | Qt 6.4 起；适合界面排序，不适合持久化顺序。 |
| `startsWith(QStringView/QLatin1StringView/QChar, cs)` | 判断前缀 | 默认大小写敏感；不创建子字符串。 |
| `endsWith(QStringView/QLatin1StringView/QChar, cs)` | 判断后缀 | 默认大小写敏感。 |
| `indexOf(QChar/StringView/QLatin1StringView, from, cs)` | 查找首个匹配位置 | 返回 UTF-16 code unit 索引，失败为 `-1`。 |
| `lastIndexOf(QChar/StringView/QLatin1StringView, from, cs)` | 从后查找匹配 | `from` 是 code unit 位置；重载默认从末尾。 |
| `indexOf(const QRegularExpression &, from, match)` | 查找首个正则匹配 | Qt 6.1 起；可写回匹配对象。 |
| `lastIndexOf(const QRegularExpression &, from, match)` | 查找最后正则匹配 | Qt 6.2 起；位置按 UTF-16 code unit。 |
| `contains(QChar/StringView/QLatin1StringView, cs)` | 判断是否包含文本 | 找到即 true；不返回位置。 |
| `contains(const QRegularExpression &, match)` | 判断是否有正则匹配 | 需要启用正则表达式配置。 |
| `count(QChar/StringView/QLatin1StringView, cs)` | 统计子串/字符出现次数 | 计数按 Qt 字符串规则；不返回匹配范围。 |
| `count(const QRegularExpression &)` | 统计正则匹配数量 | 需要启用正则表达式配置。 |
| `isValidUtf16()` | 检查 UTF-16 code unit 序列 | 假定主机字节序；BOM 没有特殊含义。 |
| `isRightToLeft()` | 判断文本方向倾向 | 不是完整的双向排版结果。 |
| `isUpper()` | 判断 Unicode uppercase folding | Qt 6.7 起；不是简单的“含大写字母”测试。 |
| `isLower()` | 判断 Unicode lowercase folding | Qt 6.7 起；遵循 Unicode folding 语义。 |
| `toShort()` / `toUShort()` | 转换为 short/ushort | base 为 2..36 或 0；失败通过 `ok` 报告。 |
| `toInt()` / `toUInt()` | 转换为 int/uint | 默认 base 10；base 0 遵循 C 前缀规则。 |
| `toLong()` / `toULong()` | 转换为 long/ulong | 使用 C locale；locale 感知转换使用 QLocale。 |
| `toLongLong()` / `toULongLong()` | 转换为 64 位整数 | 失败返回 0，必须检查 `ok`。 |
| `toFloat()` / `toDouble()` | 转换为浮点数 | 合法 0 与失败都可能返回 0，检查 `ok`。 |
| `toString()` | 深拷贝为 QString | null view 返回 null QString；获得独立生命周期。 |
| `toLatin1()` | 转换为 Latin-1 QByteArray | 目标编码受限，不能假定 Unicode 全部无损。 |
| `toUtf8()` | 转换为 UTF-8 QByteArray | UTF-8 可表示全部 Unicode；返回拥有型数组。 |
| `toLocal8Bit()` | 转换为本地 8-bit QByteArray | 结果受平台本地编码影响，不适合跨平台持久化。 |
| `toUcs4()` | 转换为 `QList<uint>` | 无效 UTF-16 替换为 U+FFFD；返回列表不 NUL 终止。 |
| `toWCharArray(wchar_t *)` | 写入 wchar_t 数组 | 不写 NUL；Windows 按 UTF-16，Unix 通常按 UCS-4。 |
| `split(QChar, behavior, cs)` | 按单字符返回 view 列表 | Qt 6.0 起；结果 view 借用源数据。 |
| `split(QStringView, behavior, cs)` | 按字符串返回 view 列表 | 空字段默认保留；列表不拥有字符。 |
| `split(QRegularExpression, behavior)` | 按正则返回 view 列表 | Qt 6.0 起；正则匹配结果仍借用源数据。 |
| `tokenize(needle, flags...)` | 返回惰性 QStringTokenizer | Qt 6.0 起；通常用 `auto` 接收，注意源文本生命周期。 |
| `operator std::u16string_view()` | 转换为 STL UTF-16 view | 不复制、不拥有，生命周期规则不变。 |
| `toCFString()` | 在 Apple 平台创建 CFString | Qt 6.0 起；调用方负责释放返回对象。 |
| `toNSString()` | 在 Apple 平台创建 NSString | Qt 6.0 起；返回 autoreleased 对象。 |

一句话总结：`QStringView` 是“借用一段 UTF-16 数据并高效观察它”的接口类型；它带来的性能收益
建立在严格的生命周期、长度单位和非 NUL 终止约束之上。
