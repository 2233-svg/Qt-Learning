# QStringMatcher：为重复子串搜索准备的匹配器

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStringMatcher>`  
> CMake：`Qt6::Core`

`QStringMatcher` 用来反复搜索同一个 UTF-16 子串。它在构造或设置模式时准备内部的跳表，
之后通过 `indexIn()` 在多个字符串，或同一个长字符串的多个位置上搜索。

它解决的是“同一模式被重复使用”的成本问题，而不是提供正则表达式能力。只搜索一次时，
直接使用 `QString::indexOf()` 或 `QStringView::indexOf()` 更简单；在循环、批量过滤、日志扫描、
语法高亮和 `QStringList::filter()` 中反复匹配同一个字面模式时，matcher 才有明显价值。

## 最小使用方式

```cpp
#include <QStringMatcher>

QStringMatcher matcher(u"error", Qt::CaseInsensitive);

for (const QString &line : lines) {
    const qsizetype column = matcher.indexIn(line);
    if (column >= 0)
        report(line, column);
}
```

`indexIn()` 返回模式在 haystack 中第一次出现的 UTF-16 code unit 索引；没有匹配时返回 `-1`。
`from` 是搜索起点，不是字节偏移，也不是匹配次数。

## 模式、大小写和性能边界

matcher 保存当前模式和大小写设置，并为重复搜索维护内部预处理数据。调用
`setPattern()` 或 `setCaseSensitivity()` 后，后续 `indexIn()` 使用新的设置。

```cpp
QStringMatcher matcher;
matcher.setPattern(QStringLiteral("timeout"));
matcher.setCaseSensitivity(Qt::CaseInsensitive);
```

默认是 `Qt::CaseSensitive`。大小写不敏感比较遵循 Qt 的字符串比较规则，并不等于完整的
locale-aware 或任意 Unicode 正规化匹配；例如不同规范化形式的 Unicode 文本不会因为视觉相同
就自动相等。

模式是字面字符串，不是正则表达式。若需要通配符、捕获组、断言或复杂 Unicode 规则，应使用
`QRegularExpression`。

空模式是一个需要单独确认的边界。它不是“没有 matcher”；根据底层字符串搜索的语义，空模式
可以在起始位置匹配。若业务上空过滤条件应表示“不过滤”或“拒绝”，应在调用前明确处理，不要
把它交给 matcher 后再猜结果。

## pattern 的生命周期

`pattern()` 返回一个 `QString`，是稳定的值结果，适合需要保存副本的代码。
Qt 6.7 起的 `patternView()` 返回 `QStringView`，避免复制，但它是非拥有视图：

```cpp
QStringView view = matcher.patternView();
```

视图的有效期不能超过 matcher 中对应模式数据的有效期。调用 `setPattern()` 可能替换模式并使
此前取得的 view 失效；销毁 matcher 后 view 也失效。只需长期保存文本时使用 `pattern()`。

使用指针加长度构造或搜索时，调用方必须保证 `[ptr, ptr + length)` 是有效的 UTF-16 区域；
matcher 不读取 NUL 之外的数据，也不替调用方检查长度。

## 输入类型与返回索引

`indexIn()` 有三种输入形式：

- `QStringView`：适合不产生临时拷贝的字符串视图。
- `const QString &`：适合拥有型 QString。
- `const QChar *` 加显式长度：适合已有连续 UTF-16 缓冲区。

返回值按 UTF-16 code unit 计数。补充平面字符占两个 code unit，因此返回的位置不能直接当作
Unicode code point 数或 UTF-8 字节位置。

```cpp
QString text = QStringLiteral("A😀B");
QStringMatcher matcher(QStringLiteral("B"));
Q_ASSERT(matcher.indexIn(text) == 3); // A=0, 😀=1..2, B=3
```

`from` 小于零不是这里推荐的倒序搜索接口；需要从后向前搜索时使用
`QStringView::lastIndexOf()` 或 `QString::lastIndexOf()`。

## 拷贝、修改与线程

`QStringMatcher` 是普通值对象，支持拷贝构造和拷贝赋值；复制会复制模式与匹配配置。
它不是 `QObject`，不需要事件循环或父对象。

成员函数是可重入的。不同线程各自使用 matcher 没有问题；同一个 matcher 如果一个线程正在
调用 `setPattern()`，另一个线程同时调用 `indexIn()`，仍需要外部同步。只读并发是否可接受不应
成为设计依赖，最稳妥的做法是每个工作任务持有自己的 matcher 副本。

## 与 QStringList 和 QRegularExpression 的选择

- 单次字面搜索：`QStringView::indexOf()`。
- 同一字面模式反复搜索：`QStringMatcher`。
- 对整个列表筛选同一模式：`QStringList::filter(const QStringMatcher &)`。
- 复杂模式、捕获和替换：`QRegularExpression`。
- 字节序列搜索：对应的 `QByteArrayMatcher`。

matcher 只预处理“模式”，不会缓存每个 haystack，也不会把搜索结果保存下来。修改输入字符串
不会修改 matcher，但输入视图在搜索调用期间必须有效。

## 常见错误

### 一次性搜索也创建 matcher

这会增加代码和预处理成本，直接 `indexOf()` 更清楚。

### 把模式当正则表达式

`"."`、`"a+"` 等都按普通字符匹配。正则需求应使用 `QRegularExpression`。

### 保存 `patternView()` 过久

它不拥有数据，且 `setPattern()` 可能让旧视图失效。要跨 matcher 修改或跨长期任务保存，调用
`pattern()` 得到值副本。

### 把返回索引当 Unicode 码点或字节偏移

Qt 字符串索引以 UTF-16 code unit 计数，代理对占两个位置。

### 忽略 `from` 的边界

`from` 是 haystack 中的起始 code unit 索引。它不表示“跳过多少个匹配”，也不把搜索变成反向。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QStringMatcher()` | 创建空 matcher | 初始没有有效搜索模式；调用 `setPattern()` 后再搜索。 |
| `QStringMatcher(const QString &, cs)` | 从 QString 构造字面模式 | 模式用于后续 `indexIn()`；默认大小写敏感。 |
| `QStringMatcher(QStringView, cs)` | 从字符串视图构造模式 | 视图输入必须在构造及匹配所需期间保持有效；避免把临时数据的视图长期保存。 |
| `QStringMatcher(const QChar *, length, cs)` | 从 UTF-16 缓冲区和长度构造 | 按显式长度读取，不要求 NUL 终止；指针范围必须有效。 |
| `QStringMatcher(const QStringMatcher &)` | 复制 matcher | 复制模式、大小写和预处理状态，属于值语义。 |
| `operator=(const QStringMatcher &)` | 复制赋值 matcher | 目标变为与源相同的搜索配置。 |
| `~QStringMatcher()` | 销毁 matcher | 释放内部预处理数据；不管理外部 haystack 的生命周期。 |
| `setPattern(const QString &)` | 替换搜索模式 | 后续搜索使用新模式；此前取得的 `patternView()` 不应继续使用。 |
| `setCaseSensitivity(Qt::CaseSensitivity)` | 修改大小写策略 | 改变后续搜索；默认是 `CaseSensitive`。 |
| `caseSensitivity() const` | 查询大小写策略 | 返回当前 matcher 的设置。 |
| `indexIn(QStringView, from)` | 在字符串视图中搜索 | 返回 UTF-16 code unit 索引，找不到返回 `-1`。 |
| `indexIn(const QString &, from)` | 在 QString 中搜索 | 不改变输入；适合拥有型字符串。 |
| `indexIn(const QChar *, length, from)` | 在连续 UTF-16 缓冲区中搜索 | `length` 是 code unit 数，调用方负责内存有效性。 |
| `pattern() const` | 返回模式的 QString 副本 | 需要拥有或长期保存模式时使用。 |
| `patternView() const` | 返回模式的非拥有视图 | Qt 6.7 起；matcher 改模式或销毁后，旧视图不能继续使用。 |

一句话总结：`QStringMatcher` 是“把同一个字面模式预备好再反复查找”的工具；它的性能收益来自
复用，而不是来自一次搜索本身。
