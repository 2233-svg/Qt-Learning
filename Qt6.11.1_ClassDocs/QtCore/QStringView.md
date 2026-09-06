# QStringView

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QStringView` 是 Qt 的值类型，围绕“String视图”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QStringView` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QStringView>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `const_iterator`
- `const_pointer`
- `const_reference`
- `const_reverse_iterator`
- `difference_type`
- `iterator`
- `pointer`
- `reference`
- `reverse_iterator`
- `size_type`
- `storage_type`
- `value_type`

### 公有函数

- `QStringView()`
- `QStringView(const Char (&)[N] string)`
- `QStringView(const Char *str)`
- `QStringView(const Container &str)`
- `QStringView(const QString &str)`
- `QStringView(std::nullptr_t)`
- `QStringView(const Char *first, const Char *last)`
- `QStringView(const Char *str, qsizetype len)`
- `QString arg(Args &&... args) const`
- `QChar at(qsizetype n) const`
- `QChar back() const`
- `QStringView::const_iterator begin() const`
- `QStringView::const_iterator cbegin() const`
- `QStringView::const_iterator cend() const`
- `void chop(qsizetype length)`
- `QStringView chopped(qsizetype length) const`
- `int compare(QChar ch) const`
- `int compare(QChar ch, Qt::CaseSensitivity cs) const`
- `int compare(QLatin1StringView l1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `int compare(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.5) int compare(QUtf8StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.1) QStringView::const_iterator constBegin() const`
- `(since 6.0) QStringView::const_pointer constData() const`
- `(since 6.1) QStringView::const_iterator constEnd() const`
- `bool contains(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool contains(QLatin1StringView l1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool contains(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.1) bool contains(const QRegularExpression &re, QRegularExpressionMatch *rmatch = nullptr) const`
- `(since 6.1) qsizetype count(const QRegularExpression &re) const`
- `(since 6.0) qsizetype count(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.4) qsizetype count(QLatin1StringView l1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.0) qsizetype count(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QStringView::const_reverse_iterator crbegin() const`
- `QStringView::const_reverse_iterator crend() const`
- `QStringView::const_pointer data() const`
- `bool empty() const`
- `QStringView::const_iterator end() const`
- `bool endsWith(QChar ch) const`
- `bool endsWith(QChar ch, Qt::CaseSensitivity cs) const`
- `bool endsWith(QLatin1StringView l1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool endsWith(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QChar first() const`
- `(since 6.0) QStringView first(qsizetype n) const`
- `QChar front() const`
- `qsizetype indexOf(QChar ch, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype indexOf(QLatin1StringView l1, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype indexOf(QStringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.1) qsizetype indexOf(const QRegularExpression &re, qsizetype from = 0, QRegularExpressionMatch *rmatch = nullptr) const`
- `bool isEmpty() const`
- `(since 6.7) bool isLower() const`
- `bool isNull() const`
- `bool isRightToLeft() const`
- `(since 6.7) bool isUpper() const`
- `bool isValidUtf16() const`
- `QChar last() const`
- `(since 6.0) QStringView last(qsizetype n) const`
- `(since 6.2) qsizetype lastIndexOf(const QRegularExpression &re, QRegularExpressionMatch *rmatch = nullptr) const`
- `qsizetype lastIndexOf(QChar ch, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype lastIndexOf(QLatin1StringView l1, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype lastIndexOf(QStringView str, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.1) qsizetype lastIndexOf(const QRegularExpression &re, qsizetype from, QRegularExpressionMatch *rmatch = nullptr) const`
- `(since 6.3) qsizetype lastIndexOf(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.2) qsizetype lastIndexOf(QLatin1StringView l1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.2) qsizetype lastIndexOf(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype length() const`
- `(since 6.4) int localeAwareCompare(QStringView other) const`
- `(since 6.8) qsizetype max_size() const`
- `QStringView::const_reverse_iterator rbegin() const`
- `QStringView::const_reverse_iterator rend() const`
- `qsizetype size() const`
- `(since 6.8) QStringView & slice(qsizetype pos, qsizetype n)`
- `(since 6.8) QStringView & slice(qsizetype pos)`
- `(since 6.0) QStringView sliced(qsizetype pos, qsizetype n) const`
- `(since 6.0) QStringView sliced(qsizetype pos) const`
- `(since 6.0) QList<QStringView> split(QChar sep, Qt::SplitBehavior behavior = Qt::KeepEmptyParts, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.0) QList<QStringView> split(QStringView sep, Qt::SplitBehavior behavior = Qt::KeepEmptyParts, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.0) QList<QStringView> split(const QRegularExpression &re, Qt::SplitBehavior behavior = Qt::KeepEmptyParts) const`
- `bool startsWith(QChar ch) const`
- `bool startsWith(QChar ch, Qt::CaseSensitivity cs) const`
- `bool startsWith(QLatin1StringView l1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool startsWith(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.0) CFStringRef toCFString() const`
- `(since 6.0) double toDouble(bool *ok = nullptr) const`
- `(since 6.0) float toFloat(bool *ok = nullptr) const`
- `(since 6.0) int toInt(bool *ok = nullptr, int base = 10) const`
- `QByteArray toLatin1() const`
- `QByteArray toLocal8Bit() const`
- `(since 6.0) long toLong(bool *ok = nullptr, int base = 10) const`
- `(since 6.0) qlonglong toLongLong(bool *ok = nullptr, int base = 10) const`
- `(since 6.0) NSString * toNSString() const`
- `(since 6.0) short toShort(bool *ok = nullptr, int base = 10) const`
- `QString toString() const`
- `(since 6.0) uint toUInt(bool *ok = nullptr, int base = 10) const`
- `(since 6.0) ulong toULong(bool *ok = nullptr, int base = 10) const`
- `(since 6.0) qulonglong toULongLong(bool *ok = nullptr, int base = 10) const`
- `(since 6.0) ushort toUShort(bool *ok = nullptr, int base = 10) const`
- `QList<uint> toUcs4() const`
- `QByteArray toUtf8() const`
- `qsizetype toWCharArray(wchar_t *array) const`
- `(since 6.0) auto tokenize(Needle &&sep, Flags... flags) const`
- `QStringView trimmed() const`
- `void truncate(qsizetype length)`
- `const QStringView::storage_type * utf16() const`
- `(since 6.7) operator std::u16string_view() const`
- `QChar operator[](qsizetype n) const`

### 静态公有成员

- `QStringView fromArray(const Char (&)[Size] string)`
- `(since 6.8) qsizetype maxSize()`

### 相关非成员函数

- `size_t qHash(QStringView key, size_t seed = 0)`
- `bool operator!=(const QStringView &lhs, const QStringView &rhs)`
- `bool operator<(const QStringView &lhs, const QStringView &rhs)`
- `bool operator<=(const QStringView &lhs, const QStringView &rhs)`
- `bool operator==(const QStringView &lhs, const QStringView &rhs)`
- `bool operator>(const QStringView &lhs, const QStringView &rhs)`
- `bool operator>=(const QStringView &lhs, const QStringView &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QStringView::const_iterator`

**作用与语义：**

该typedef为`QStringView`提供了STL风格的const迭代器。

### `QStringView::const_pointer`

**作用与语义：**

`value_type *`的别名。为兼容STL提供。

### `QStringView::const_reference`

**作用与语义：**

`value_type &`的别名。为兼容STL提供。

### `QStringView::const_reverse_iterator`

**作用与语义：**

该typedef为`QStringView`提供了一个STL风格的cont反迭代器。

### `QStringView::difference_type`

**作用与语义：**

`std::ptrdiff_t`的别名。为兼容STL而提供。

### `QStringView::iterator`

**作用与语义：**

该typedef为`QStringView`提供了一个STL风格的const迭代器。
`QStringView`不支持可变迭代器，所以这和`const_iterator`是一样的。

### `QStringView::pointer`

**作用与语义：**

`value_type *`的别名。为兼容STL提供。
`QStringView`不支持可变指针，所以这和`const_pointer`一样。

### `QStringView::reference`

**作用与语义：**

`value_type &`的别名。为兼容STL而提供。
`QStringView`不支持可变引用，所以这和`const_reference`一样。

### `QStringView::reverse_iterator`

**作用与语义：**

该类型定义为`QStringView`提供了一个STL风格的const反迭代器。
`QStringView`不支持可变的反迭代器，所以这和`const_reverse_iterator`相同。

### `QStringView::size_type`

**作用与语义：**

qsizetype 的别名。为兼容 STL 提供。

### `QStringView::storage_type`

**作用与语义：**

`char16_t`的别名。

### `QStringView::value_type`

**作用与语义：**

`const QChar`的别名。为兼容STL而提供。

### `[constexpr noexcept] QStringView::QStringView()`

**作用与语义：**

构造一个空字符串视图。

### `[constexpr noexcept] template <typename Char, size_t N> QStringView::QStringView(const Char (&)[N] string)`

**作用与语义：**

在字符字符串的字面值`string`上构建字符串视图。视图覆盖数组，直到遇到第一个`Char(0)`或`N`，以先到者为准。如果你需要完整数组，可以用`fromArray()`。
`string`必须在该字符串视图对象的生命周期内保持有效。
只有当 `Char` 是兼容的字符类型时，才参与超载解析。兼容的字符类型包括：`QChar`、`ushort`、`char16_t` 以及（在 Windows 等平台上，它是 16 位类型）`wchar_t`。

### `[constexpr noexcept] template <typename Char> QStringView::QStringView(const Char *str)`

**作用与语义：**

在`str`上构建字符串视图。长度通过扫描第一个`Char(0)`确定。
`str`必须在该字符串视图对象的生命周期内保持有效。
将`nullptr`传递为`str`是安全的，且会得到一个空字符串视图。
只有当`Char`是兼容的字符类型时，才参与超载解析。兼容的字符类型包括：`QChar`、`ushort`、`char16_t` 以及（在Windows等平台上，它是16位类型）`wchar_t`。

### `[constexpr noexcept] template <typename Container, QStringView::if_compatible_container<Container> = true> QStringView::QStringView(const Container &str)`

**作用与语义：**

在`str`上构造字符串视图。长度取自`std::size(str)`。
`std::data(str)`必须在该字符串视图对象的生命周期内保持有效。
字符串视图为空当且仅当 `std::size(str) == 0`。尚不确定该构造函数是否能生成空字符串视图（`std::data(str)`需返回`nullptr`）。
仅当`Container`是具有兼容字符类型的容器时，才参与超载解析`value_type`。兼容的字符类型包括：`QChar`、`ushort`、`char16_t` 以及（在Windows等平台上，它是16位类型）`wchar_t`。

### `[noexcept] QStringView::QStringView(const QString &str)`

**作用与语义：**

在`str`上构建字符串视图。
`str.data()`必须在该字符串视图对象的生命周期内保持有效。
字符串视图当且仅当 `str.isNull()` 时才为空。

### `[constexpr noexcept] QStringView::QStringView(std::nullptr_t)`

**作用与语义：**

构造一个空字符串视图。

### `[constexpr] template <typename Char, QStringView::if_compatible_char<Char> = true> QStringView::QStringView(const Char *first, const Char *last)`

**作用与语义：**

在 `first` 上构建一个长度为 (`last` - `first`) 的字符串视图。`[first,last)` 范围在此字符串视图对象的生命周期内必须保持有效。如果 `last` 也是 `nullptr`，那么将 `\nullptr` 作为 `first` 传递是安全的，并且会得到一个空字符串视图。如果 `last` 在 `first` 之前，或者 `first` 是 `nullptr` 而 `last` 不是，则行为未定义。仅当 `Char` 是兼容的字符类型时才参与重载决议。兼容的字符类型有：`QChar`、`ushort`、`char16_t`，以及在某些平台（如 Windows）上是 16 位类型的 `wchar_t`。

### `[constexpr] template <typename Char, QStringView::if_compatible_char<Char> = true> QStringView::QStringView(const Char *str, qsizetype len)`

**作用与语义：**

在 `str` 上构造一个长度为 `len` 的字符串视图。
`[str,len)` 的范围在此字符串视图对象的整个生命周期中必须保持有效。
如果 `len` 也为 0，将 `nullptr` 作为 `str` 传递是安全的，并且会生成一个空字符串视图。
如果 `len` 为负数，或者为正数时 `str` 为 `nullptr`，则行为未定义。
仅当 `Char` 是兼容字符类型时才参与重载决议。兼容的字符类型有：`QChar`、`ushort`、`char16_t`，以及（在如 Windows 等为 16 位类型的平台上）`wchar_t`。

### `template <typename... Args> QString QStringView::arg(Args &&... args) const`

**作用与语义：**

用 `args` 中对应的参数替换该字符串中出现的 `%N`。这些参数不是位置论元：`args`中的第一个用最低的`N`替换`%N`（全部），第二个用`args`的`%N`替换为下一个最低的`N`，依此类推。
`Args`可以包含任何隐含转换为`QAnyStringView`的内容。
注意：在6.9之前的Qt版本中，`QAnyStringView`和UTF-8字符串（`QUtf8StringView`、`QByteArray`、`QByteArrayView`、`const char8_t*`等）不支持`args`。

### `[constexpr noexcept] QChar QStringView::at(qsizetype n) const`

**作用与语义：**

返回该字符串视图中位置`n`的字符。
行为是负面还是不小于`size()`，行为不`n`明确。

### `[constexpr] QChar QStringView::back() const`

**作用与语义：**

返回字符串视图中的最后一个字符。和 `last()` 一样。
此功能是为了STL兼容性而提供。
警告：在空字符串视图上调用该函数构成未定义行为。

### `[noexcept] QStringView::const_iterator QStringView::begin() const`

**作用与语义：**

返回一个指向字符串视图第一个字符的const型STL式迭代器。
此功能是为了STL兼容性而提供。

### `[noexcept] QStringView::const_iterator QStringView::cbegin() const`

**作用与语义：**

和`begin()`一样。
此功能是为了STL兼容性而提供。

### `[noexcept] QStringView::const_iterator QStringView::cend() const`

**作用与语义：**

和`end()`一样。
此功能是为了STL兼容性而提供。

### `[constexpr noexcept] void QStringView::chop(qsizetype length)`

**作用与语义：**

将字符串视图截断为`length`字符。
和`*this = left(size() - length)`一样。
注意：当`length` <0或`length` > `size()`时，行为未定义。

### `[constexpr noexcept] QStringView QStringView::chopped(qsizetype length) const`

**作用与语义：**

返回长度为`size()` - `length`的子串，从该对象的开头开始。
和`left(size() - length)`一样。
注意：当`length` <0或`length` > `size()`时，行为未定义。

### `[noexcept] int QStringView::compare(QChar ch, Qt::CaseSensitivity cs) const`

**作用与语义：**

将该字符串视图与拉丁字母1字符串视图的 `l1` 或字符 `ch` 比较。如果字符串视图小于 `l1` 或 `ch`，返回负整数;如果大于 `l1` 或 `ch`，返回正整数;若相等，返回零。
如果`cs`是`Qt::CaseSensitive`（默认），则比较是区分大小写的;否则比较是无大小写的。

### `[noexcept] int QStringView::compare(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

将该字符串视图与拉丁字母1字符串视图的 `l1` 或字符 `ch` 比较。如果字符串视图小于 `l1` 或 `ch`，返回负整数;如果大于 `l1` 或 `ch`，返回正整数;若相等，返回零。
如果`cs`是`Qt::CaseSensitive`（默认），则比较是区分大小写的;否则比较是无大小写的。

### `[noexcept, since 6.5] int QStringView::compare(QUtf8StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

将该字符串视图与拉丁字母1字符串视图的 `l1` 或字符 `ch` 比较。如果字符串视图小于 `l1` 或 `ch`，返回负整数;如果大于 `l1` 或 `ch`，返回正整数;若相等，返回零。
如果`cs`是`Qt::CaseSensitive`（默认），则比较是区分大小写的;否则比较是无大小写的。

### `[noexcept, since 6.1] QStringView::const_iterator QStringView::constBegin() const`

**作用与语义：**

和`begin()`一样。

### `[noexcept, since 6.0] QStringView::const_pointer QStringView::constData() const`

**作用与语义：**

返回字符串视图中第一个字符的const指针。
注意：返回值所表示的字符数组并非空终止。

### `[noexcept, since 6.1] QStringView::const_iterator QStringView::constEnd() const`

**作用与语义：**

和`end()`一样。

### `[noexcept] bool QStringView::contains(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果该字符串视图包含`str`查看的UTF-16字符串、`l1`查看的拉丁1字符串或字符`ch`，则返回`true`;否则返回`false`。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索区分大小写;否则搜索不区分大小写。

### `[since 6.1] bool QStringView::contains(const QRegularExpression &re, QRegularExpressionMatch *rmatch = nullptr) const`

**作用与语义：**

如果该字符串视图包含`str`查看的UTF-16字符串、`l1`查看的拉丁1字符串或字符`ch`，则返回`true`;否则返回`false`。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索区分大小写;否则搜索不区分大小写。

### `[since 6.1] qsizetype QStringView::count(const QRegularExpression &re) const`

**作用与语义：**

返回正则表达式`re`在字符串视图中匹配的次数。
出于历史原因，该函数计数重叠匹配。这种行为不同于仅仅在字符串视图中用`QRegularExpressionMatchIterator`遍历匹配。

### `[noexcept, since 6.0] qsizetype QStringView::count(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回字符串视图中字符`ch`出现次数。
如果`cs`为`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索为不区分大小写。
注意：该功能会超载`QStringView::count()`。

### `[since 6.4] qsizetype QStringView::count(QLatin1StringView l1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回`l1`在该字符串视图中看到的拉丁-1字符串（可能重叠）次数。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：该功能会让`QStringView::count()`重载。

### `[noexcept, since 6.0] qsizetype QStringView::count(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回该字符串视图中（可能重叠的）出现次数`str`该字符串视图。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：该功能会让`QStringView::count()`重载。

### `[noexcept] QStringView::const_reverse_iterator QStringView::crbegin() const`

**作用与语义：**

和`rbegin()`一样。
此功能是为了STL兼容性而提供。

### `[noexcept] QStringView::const_reverse_iterator QStringView::crend() const`

**作用与语义：**

和`rend()`一样。
此功能是为了STL兼容性而提供。

### `[noexcept] QStringView::const_pointer QStringView::data() const`

**作用与语义：**

返回字符串视图中第一个字符的const指针。
注意：返回值所表示的字符数组并非空终止。

### `[constexpr noexcept] bool QStringView::empty() const`

**作用与语义：**

返回该字符串视图是否为空——即是否`size() == 0`。
此功能是为了STL兼容性而提供。

### `[noexcept] QStringView::const_iterator QStringView::end() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向列表中最后一个字符后的虚数字符。
此功能是为了STL兼容性而提供。

### `[noexcept] bool QStringView::endsWith(QChar ch, Qt::CaseSensitivity cs) const`

**作用与语义：**

如果此字符串视图以 `str` 所表示的 UTF-16 字符串、`l1` 所表示的 Latin-1 字符串或 `ch` 所表示的字符结尾，则返回 `true`；否则返回 `false`。如果 `cs` 为 `Qt::CaseSensitive`（默认值），则搜索区分大小写；否则搜索不区分大小写。

### `[constexpr] QChar QStringView::first() const`

**作用与语义：**

返回字符串视图中的第一个字符。和 `front()` 一样。
此功能是为了与其他 Qt 容器的兼容性而提供。
警告：在空字符串视图上调用该函数构成未定义行为。

### `[constexpr noexcept, since 6.0] QStringView QStringView::first(qsizetype n) const`

**作用与语义：**

返回一个字符串视图，该视图指向此字符串视图的前 `n` 个字符。
注意：当 `n` < 0 或 `n` > `size()` 时，行为未定义。

### `[static constexpr noexcept] template < typename Char, size_t Size, QStringView::if_compatible_char<Char> = true > QStringView QStringView::fromArray(const Char (&)[Size] string)`

**作用与语义：**

在完整的字符字符串文字 `string` 上构建字符串视图，包括任何尾`Char(0)`。如果你不想在视图中包含空终止符，那么确定它在最后时可以`chop()`它。或者你也可以使用构造函数重载，取一个数组文字，创建一个视图直到数据中第一个空终止符，但不包括它。
`string`必须在该字符串视图对象的生命周期内保持有效。
如果 `Char` 是兼容的字符类型，该函数可对任意数组文字工作。兼容的字符类型包括：`QChar`、`ushort`、`char16_t` 以及（在 Windows 等平台上，它是 16 位类型）`wchar_t`。

### `[constexpr] QChar QStringView::front() const`

**作用与语义：**

返回字符串视图中的第一个字符。和`first()`一样。
此功能是为了STL兼容性而提供。
警告：在空字符串视图上调用该函数构成未定义行为。

### `[noexcept] qsizetype QStringView::indexOf(QChar ch, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回 `str` 查看的 UTF-16 字符串首次出现的索引位置，`l1` 查看的拉丁字母 1 字符串，或字符 `ch`，分别从索引位置 `from` 向前搜索。如果未找到 `str`、`l1` 或 `ch`，分别返回 -1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。

### `[since 6.1] qsizetype QStringView::indexOf(const QRegularExpression &re, qsizetype from = 0, QRegularExpressionMatch *rmatch = nullptr) const`

**作用与语义：**

返回 `str` 查看的 UTF-16 字符串首次出现的索引位置，`l1` 查看的拉丁字母 1 字符串，或字符 `ch`，分别从索引位置 `from` 向前搜索。如果未找到 `str`、`l1` 或 `ch`，分别返回 -1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。

### `[constexpr noexcept] bool QStringView::isEmpty() const`

**作用与语义：**

返回该字符串视图是否为空——即是否`size() == 0`。
此功能是为了与其他 Qt 容器的兼容性而提供。

### `[noexcept, since 6.7] bool QStringView::isLower() const`

**作用与语义：**

如果该视角与其小写折叠相同，则返回`true`。
注意，这并不意味着字符串视图不包含大写字母（有些大写字母没有小写折叠;`toString()`.toLower()）保持不变）。更多信息请参阅Unicode标准第3.13节。

### `[constexpr noexcept] bool QStringView::isNull() const`

**作用与语义：**

返回该字符串视图是否为空——即是否`data() == nullptr`。
这些功能是为了与其他 Qt 容器的兼容性而提供。

### `[noexcept] bool QStringView::isRightToLeft() const`

**作用与语义：**

如果字符串视图是从右到左读取，返回`true`。

### `[noexcept, since 6.7] bool QStringView::isUpper() const`

**作用与语义：**

如果该观点与其大写折叠相同，返回`true`。
注意，这并不意味着字符串视图不包含小写字母（有些小写字母没有大写折叠;`toString()`.toUpper()保持不变）。更多信息请参阅Unicode标准第3.13节。

### `[noexcept] bool QStringView::isValidUtf16() const`

**作用与语义：**

如果字符串视图包含有效的 UTF-16 编码数据，则返回`true`，否则`false`返回。
注意，该函数不对数据进行任何特殊验证;它仅检查数据是否能成功从UTF-16解码。假设数据按主机字节顺序排列;BOM的存在无意义。

### `[constexpr] QChar QStringView::last() const`

**作用与语义：**

返回字符串视图中的最后一个字符。和`back()`一样。
此功能是为了与其他 Qt 容器的兼容性而提供。
警告：在空字符串视图上调用该函数构成未定义行为。

### `[constexpr noexcept, since 6.0] QStringView QStringView::last(qsizetype n) const`

**作用与语义：**

返回一个字符串视图，该视图指向此字符串视图的最后 `n` 个字符。
注意：当 `n` < 0 或 `n` > `size()` 时，行为未定义。

### `[since 6.2] qsizetype QStringView::lastIndexOf(const QRegularExpression &re, QRegularExpressionMatch *rmatch = nullptr) const`

**作用与语义：**

返回字符串视图中正则表达式`re`最后匹配的索引位置。如果没有匹配`re`返回-1。
如果匹配成功且`rmatch`未被`nullptr`，它还会将匹配结果写入`rmatch`指向的`QRegularExpressionMatch`对象中。
注意：由于正则表达式匹配算法的工作原理，该函数实际上会从字符串视图的开始到到达的结束处反复匹配。

### `[noexcept] qsizetype QStringView::lastIndexOf(QChar ch, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回`str`查看UTF-16字符串最后一次出现的索引位置，以及`l1`查看的拉丁字母1字符串，或字符`ch`，分别从索引位置`from`向后搜索。
如果`from`为-1，搜索从最后一个字符开始;如果是-2，则从倒数第二个字符开始，依此类推。
如果未找到`str`、`l1`或`ch`，则返回-1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：在搜索长度为0的`str`或`l1`时，数据末尾的匹配会被负`from`排除，尽管`-1`通常被认为是从字符串视图末尾搜索：结尾的匹配位于最后一个字符之后，因此被排除。要包含这样的最终空匹配，要么给出`from`的正值，要么完全省略`from`参数。

### `[since 6.1] qsizetype QStringView::lastIndexOf(const QRegularExpression &re, qsizetype from, QRegularExpressionMatch *rmatch = nullptr) const`

**作用与语义：**

返回`str`查看UTF-16字符串最后一次出现的索引位置，以及`l1`查看的拉丁字母1字符串，或字符`ch`，分别从索引位置`from`向后搜索。
如果`from`为-1，搜索从最后一个字符开始;如果是-2，则从倒数第二个字符开始，依此类推。
如果未找到`str`、`l1`或`ch`，则返回-1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：在搜索长度为0的`str`或`l1`时，数据末尾的匹配会被负`from`排除，尽管`-1`通常被认为是从字符串视图末尾搜索：结尾的匹配位于最后一个字符之后，因此被排除。要包含这样的最终空匹配，要么给出`from`的正值，要么完全省略`from`参数。

### `[noexcept, since 6.3] qsizetype QStringView::lastIndexOf(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回`str`查看UTF-16字符串最后一次出现的索引位置，以及`l1`查看的拉丁字母1字符串，或字符`ch`，分别从索引位置`from`向后搜索。
如果`from`为-1，搜索从最后一个字符开始;如果是-2，则从倒数第二个字符开始，依此类推。
如果未找到`str`、`l1`或`ch`，则返回-1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：在搜索长度为0的`str`或`l1`时，数据末尾的匹配会被负`from`排除，尽管`-1`通常被认为是从字符串视图末尾搜索：结尾的匹配位于最后一个字符之后，因此被排除。要包含这样的最终空匹配，要么给出`from`的正值，要么完全省略`from`参数。

### `[noexcept, since 6.2] qsizetype QStringView::lastIndexOf(QLatin1StringView l1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回字符串视图中正则表达式`re`最后匹配的索引位置，该匹配始于索引位置`from`之前。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。
如果没有匹配，回报率为-1 `re`。
如果匹配成功且`rmatch`未`nullptr`，它还会将匹配结果写入`rmatch`指向的`QRegularExpressionMatch`对象中。
注意：由于正则表达式匹配算法的工作原理，该函数实际上会从字符串视图开始反复匹配，直到达到`from`的位置。
注意：当搜索可能匹配0字符的正则表达式`re`时，数据末尾的匹配会被`from`排除在搜索中，尽管`-1`通常被视为从字符串视图末尾搜索：结尾的匹配位于最后一个字符之后，因此被排除。要包含这样的最终空匹配，要么给出`from`的正值，要么完全省略`from`参数。

### `[constexpr noexcept] qsizetype QStringView::length() const`

**作用与语义：**

和`size()`一样。
此功能是为了与其他 Qt 容器的兼容性而提供。

### `[since 6.4] int QStringView::localeAwareCompare(QStringView other) const`

**作用与语义：**

将该字符串视图与`other`字符串视图比较，如果该字符串视图小于、等于或大于`other`字符串视图，则返回小于、等于或大于零的整数。
比较以本地和平台为依据的方式进行。使用此功能向用户展示排序的字符串列表。

### `[static constexpr noexcept, since 6.8] qsizetype QStringView::maxSize()`

**作用与语义：**

它返回视图理论上能表示的最大元素数。实际上，这个数量可以更小，受限于系统可用的内存。

### `[constexpr noexcept, since 6.8] qsizetype QStringView::max_size() const`

**作用与语义：**

此功能是为了STL兼容性而提供。
退货 `maxSize()`。

### `[noexcept] QStringView::const_reverse_iterator QStringView::rbegin() const`

**作用与语义：**

返回一个const STL风格的反迭代器，指向字符串视图中的第一个字符，顺序相反。
此功能是为了STL兼容性而提供。

### `[noexcept] QStringView::const_reverse_iterator QStringView::rend() const`

**作用与语义：**

返回一个STL风格的反迭代器，指向字符串视图中最后一个字符之后的迭代器，顺序相反。
此功能是为了STL兼容性而提供。

### `[constexpr noexcept] qsizetype QStringView::size() const`

**作用与语义：**

返回该字符串视图的大小，单位为UTF-16码（即在该函数中，代理对计为两个，与`QString`相同）。

### `[constexpr, since 6.8] QStringView &QStringView::slice(qsizetype pos, qsizetype n)`

**作用与语义：**

修改字符串视图，从位置`pos`开始，延伸至`n`码点。
注意：当`pos` <0、`n` <0或`pos` `n` > `size()`时，行为未定义。

### `[constexpr, since 6.8] QStringView &QStringView::slice(qsizetype pos)`

**作用与语义：**

修改字符串视图，从位置`pos`开始，延伸到末端。
注意：当`pos` <0或`pos` > `size()`时，行为是未定义的。

### `[constexpr noexcept, since 6.0] QStringView QStringView::sliced(qsizetype pos, qsizetype n) const`

**作用与语义：**

返回一个字符串视图，该视图指向从位置 `pos` 开始的本字符串视图中的 `n` 个字符。
注意：当 `pos` < 0、`n` < 0 或 `pos` + `n` > `size()` 时，行为未定义。

### `[constexpr noexcept, since 6.0] QStringView QStringView::sliced(qsizetype pos) const`

**作用与语义：**

返回一个从本对象中位置 `pos` 开始并延伸到其末尾的字符串视图。
注意：当 `pos` < 0 或 `pos` > `size()` 时，行为未定义。

### `[since 6.0] QList<QStringView> QStringView::split(QStringView sep, Qt::SplitBehavior behavior = Qt::KeepEmptyParts, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

在出现 `sep` 的地方将视图拆分为子串视图，并返回这些字符串视图的列表。
参见`QString::split()`，了解`sep`、`behavior`和`cs`如何相互作用形成结果。
注意：只要该字符串视图引用的数据有效，所有返回的视图都是有效的。销毁数据会导致所有视图变成悬空状态。

### `[since 6.0] QList<QStringView> QStringView::split(const QRegularExpression &re, Qt::SplitBehavior behavior = Qt::KeepEmptyParts) const`

**作用与语义：**

在出现 `sep` 的地方将视图拆分为子串视图，并返回这些字符串视图的列表。
参见`QString::split()`，了解`sep`、`behavior`和`cs`如何相互作用形成结果。
注意：只要该字符串视图引用的数据有效，所有返回的视图都是有效的。销毁数据会导致所有视图变成悬空状态。

### `[noexcept] bool QStringView::startsWith(QChar ch, Qt::CaseSensitivity cs) const`

**作用与语义：**

如果此字符串视图以 `str` 所表示的 UTF-16 字符串、`l1` 所表示的 Latin-1 字符串或 `ch` 所表示的字符开头，则返回 `false`；否则返回 `false`。如果 `cs` 为 `Qt::CaseSensitive`（默认值），则搜索区分大小写；否则搜索不区分大小写。

### `[since 6.0] CFStringRef QStringView::toCFString() const`

**作用与语义：**

从这个`QStringView`创建CFStriring。
调用者拥有CFStriing，并负责释放该系统。
注意：此功能仅适用于macOS和iOS。

### `[since 6.0] double QStringView::toDouble(bool *ok = nullptr) const`

**作用与语义：**

返回字符串视图转换为`double`值。
如果转换溢出，返回无穷大;如果因其他原因（如溢出），则返回0.0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
字符串转换总是在“C”区域进行。对于区域相关转换，使用`QLocale::toDouble()`。
出于历史原因，该函数无法处理数千个组分隔符。如果你需要转换这些数字，可以使用`QLocale::toDouble()`。

### `[since 6.0] float QStringView::toFloat(bool *ok = nullptr) const`

**作用与语义：**

返回将字符串视图转换为`float`值。
如果转换溢出，返回无穷大;如果因其他原因（如溢出），则返回0.0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
字符串转换总是在“C”区域进行。对于区域相关转换，使用`QLocale::toFloat()`。

### `[since 6.0] int QStringView::toInt(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用底`base`转换为`int`的字符串视图，默认为10，必须介于2到36之间，即0。转换失败时返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
如果`base`为0，则使用C语言的约定：如果字符串视图以“0x”开头，则使用进制16;否则，如果字符串视图以“0”开头，则使用进制8;否则，使用进制10。
字符串转换总是在“C”区域进行。对于依赖区域的转换，请使用`QLocale::toInt()`。

### `QByteArray QStringView::toLatin1() const`

**作用与语义：**

返回字符串的拉丁-1表示，作为`QByteArray`。
如果字符串包含非拉丁1字符，则该行为未定义。

### `QByteArray QStringView::toLocal8Bit() const`

**作用与语义：**

返回字符串的本地8位表示，作为`QByteArray`。
在Unix系统上，这相当于`toUtf8()`，在Windows上则使用系统当前的代码页。
如果字符串包含不被该区域8位编码支持的字符，则该行为未定义。

### `[since 6.0] long QStringView::toLong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用底`base`转换为`long`的字符串视图，默认为10，且必须介于2到36之间，即0。转换失败时返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
如果`base`为0，则使用C语言惯例：如果字符串视图以“0x”开头，使用进制16;否则，如果字符串视图以“0”开头，使用进制8;否则使用进制10。
字符串转换总是在“C”区域进行。对于区域相关转换，请使用`QLocale::toLong()`。

### `[since 6.0] qlonglong QStringView::toLongLong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用底`base`转换为`long long`的字符串视图，默认为10，必须介于2到36之间，即0。如果转换失败，返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，通过将*`ok`设为`true`来报告成功。
如果`base`为0，则使用C语言的约定：如果字符串视图以“0x”开头，则使用进制16;否则，如果字符串视图以“0”开头，则使用进制8;否则使用进制10。
字符串转换总是在“C”区域进行。对于区域相关转换，请使用`QLocale::toLongLong()`。

### `[since 6.0] NSString *QStringView::toNSString() const`

**作用与语义：**

从该`QStringView`创建 NSString。
国家安全链是自动释放的。
注意：此功能仅适用于macOS和iOS。

### `[since 6.0] short QStringView::toShort(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用基数`base`转换为`short`的字符串视图，默认为10，且必须在2到36之间，即0。转换失败时返回0。
如果 `ok` 未`nullptr`，则通过将 *`ok` 设为 `false` 来报告失败，通过将 *`ok` 设为 `true` 来报告失败。
如果`base`为0，则使用C语言的约定：如果字符串视图以“0x”开头，则使用进制16;否则，如果字符串视图以“0”开头，使用进制8;否则，使用进制10。
字符串转换总是在“C”区域进行。对于区域相关转换，请使用`QLocale::toShort()`。

### `QString QStringView::toString() const`

**作用与语义：**

返回该字符串视图数据的深度副本作为`QString`。
返回值当且仅当该字符串视图为空时，返回值才是空的`QString`。

### `[since 6.0] uint QStringView::toUInt(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用底`base`转换为`unsigned int`的字符串视图，默认为10，且必须介于2到36之间，即0。转换失败时返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功通过将*`ok`设为`true`来报告。
如果`base`为0，则使用C语言的惯例：如果字符串视图以“0x”开头，则使用进制16;否则，如果字符串视图以“0”开头，则使用进制8;否则，使用进制10。
字符串转换总是在“C”区域进行。对于区域相关转换，请使用`QLocale::toUInt()`。

### `[since 6.0] ulong QStringView::toULong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用底`base`转换为`unsigned long`的字符串视图，默认为10，必须在2到36之间，即0。转换失败则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
如果`base`为0，则使用C语言的惯例：如果字符串视图以“0x”开头，使用进制16;否则，如果字符串视图以“0”开头，使用进制8;否则使用进制10。
字符串转换总是在“C”区域进行。对于区域相关转换，请使用`QLocale::toULongLong()`。

### `[since 6.0] qulonglong QStringView::toULongLong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用基数`base`转换为`unsigned long long`的字符串视图，默认为10，且必须介于2到36之间，即0。转换失败则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
如果`base`为0，则使用C语言的约定：如果字符串视图以“0x”开头，则使用进制16;否则，如果字符串视图以“0”开头，则使用进制8;否则，使用进制10。
字符串转换总是在“C”区域进行。对于区域相关转换，请使用`QLocale::toULongLong()`。

### `[since 6.0] ushort QStringView::toUShort(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用底`base`转换为`unsigned short`的字符串视图，默认为10，且必须介于2到36之间，即0。如果转换失败，返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
如果`base`为0，则使用C语言惯例：如果字符串视图以“0x”开头，使用进制16;否则，如果字符串视图以“0”开头，使用进制8;否则使用进制10。
字符串转换总是在“C”区域进行。对于区域相关转换，请使用`QLocale::toUShort()`。

### `QList<uint> QStringView::toUcs4() const`

**作用与语义：**

返回字符串视图的UCS-4/UTF-32表示，作为`QList`<uint>。
UCS-4 是 Unicode 编解码器，因此是无损的。该字符串视图中的所有字符都将编码在 UCS-4 中。该字符串视图中任何无效的编码单元序列都会被 Unicode 替换字符（`QChar::ReplacementCharacter`，对应于 `U+FFFD`）。
返回的列表并非0终止。

### `QByteArray QStringView::toUtf8() const`

**作用与语义：**

返回字符串视图的UTF-8表示，作为`QByteArray`。
UTF-8 是一种 Unicode 编解码器，可以表示 Unicode 字符串中的所有字符，比如 `QString`。

### `qsizetype QStringView::toWCharArray(wchar_t *array) const`

**作用与语义：**

将字符串视图转录到给定的 `array`。
调用者负责确保`array`足够大以容纳该字符串视图的`wchar_t`编码（分配与字符串视图长度相同的数组始终足够）。在`wchar_t`宽度为2字节的平台上（如Windows），该数组采用UTF-16编码;否则（Unix系统）则假设`wchar_t`宽为4字节，数据以UCS-4编写。
注意：该函数不会写入`array`末尾的空终止子。
返回写入`array`的条目数量`wchar_t`。

### `[constexpr noexcept(...), since 6.0] template <typename Needle, typename... Flags> auto QStringView::tokenize(Needle &&sep, Flags... flags) const`

**作用与语义：**

在出现该字符串的地方将字符串拆分为子串视图，并返回`sep`的字符串的懒散序列。
等价于。
但该功能在编译器中未启用 C 17 类模板参数推理（CTAD）时可正常工作。
参见`QStringTokenizer`，了解`sep`和`flags`如何相互作用形成结果。
注意：虽然该函数返回`QStringTokenizer`，但你绝不应明确命名其模板参数。如果你可以使用C 17类模板参数演绎（CTAD），你可以写成。
（不含模板参数）。如果你不能使用 C 17 CTAD，你必须只将返回值存储在`auto`变量中：
这是因为`QStringTokenizer`的模板参数对返回的具体`tokenize()`重载有非常微妙的依赖，且通常不对应分隔符所用的类型。
注意：该功能仅在`noexcept(qTokenize(std::declval<const QStringView&>(), std::forward<Needle>(needle), flags...))` `true`时才使用。

**官方示例：**

```cpp
 return QStringTokenizer{std::forward<Needle>(sep), flags...};
```

### `[noexcept] QStringView QStringView::trimmed() const`

**作用与语义：**

去除前后空白并返回结果。
空白空间指`QChar::isSpace()`返回`true`的字符。这包括ASCII字符“\t”、“\n”、“\v”、“\f”、“\r”和“''。

### `[constexpr noexcept] void QStringView::truncate(qsizetype length)`

**作用与语义：**

将字符串视图截断为长度`length`。
和`*this = left(length)`一样。
注意：当`length` <0或`length` > `size()`时，行为未定义。

### `[constexpr noexcept] const QStringView::storage_type *QStringView::utf16() const`

**作用与语义：**

返回字符串视图中第一个字符的const指针。
注意：返回值所表示的字符数组并非空终止。
`storage_type`是`char16_t`。

### `[constexpr noexcept, since 6.7] QStringView::operator std::u16string_view() const`

**作用与语义：**

将该`QStringView`对象转换为`std::u16string_view`对象。返回的视图将拥有相同的数据指针和长度。

### `[constexpr] QChar QStringView::operator[](qsizetype n) const`

**作用与语义：**

返回该字符串视图中位置`n`的字符。
行为是负面还是不小于`size()`，行为不`n`明确。

### `[noexcept] size_t qHash(QStringView key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] bool operator>=(const QStringView &lhs, const QStringView &rhs)`

**作用与语义：**

用于比较 `lhs` 和 `rhs` 的操作符。

### `const_iterator`

**作用与语义：**

该typedef为`QStringView`提供了STL风格的const迭代器。

### `const_pointer`

**作用与语义：**

`value_type *`的别名。为兼容STL提供。

### `const_reference`

**作用与语义：**

`value_type &`的别名。为兼容STL提供。

### `const_reverse_iterator`

**作用与语义：**

该typedef为`QStringView`提供了一个STL风格的cont反迭代器。

### `difference_type`

**作用与语义：**

`std::ptrdiff_t`的别名。为兼容STL而提供。

### `iterator`

**作用与语义：**

该typedef为`QStringView`提供了一个STL风格的const迭代器。
`QStringView`不支持可变迭代器，所以这和`const_iterator`是一样的。

### `pointer`

**作用与语义：**

`value_type *`的别名。为兼容STL提供。
`QStringView`不支持可变指针，所以这和`const_pointer`一样。

### `reference`

**作用与语义：**

`value_type &`的别名。为兼容STL而提供。
`QStringView`不支持可变引用，所以这和`const_reference`一样。

### `reverse_iterator`

**作用与语义：**

该类型定义为`QStringView`提供了一个STL风格的const反迭代器。
`QStringView`不支持可变的反迭代器，所以这和`const_reverse_iterator`相同。

### `size_type`

**作用与语义：**

qsizetype 的别名。为兼容 STL 提供。

### `storage_type`

**作用与语义：**

`char16_t`的别名。

### `value_type`

**作用与语义：**

`const QChar`的别名。为兼容STL而提供。

### `int compare(QChar ch) const`

**作用与语义：**

将该字符串视图与字符串视图`str`比较，若该字符串视图小于`str`则返回负整数;若大于`str`则返回正整数;相等则返回零。
如果`cs`为`Qt::CaseSensitive`（默认），则比较区分大小写;否则比较不区分大小写。

### `int compare(QLatin1StringView l1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

将该字符串视图与 `QUtf8StringView` `str` 比较，若字符串视图小于 `str`，返回负整数;若大于 `str`，返回正整数;相等则返回零。
如果`cs`是`Qt::CaseSensitive`（默认），则比较大小写区分;否则比较不区分大小写。

### `bool contains(QLatin1StringView l1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果该字符串视图包含`str`查看的UTF-16字符串、`l1`查看的拉丁1字符串或字符`ch`，则返回`true`;否则返回`false`。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索区分大小写;否则搜索不区分大小写。

### `bool contains(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果正则表达式`re`在字符串视图中匹配，返回`true`;否则返回`false`。
如果匹配成功且`rmatch`未`nullptr`，它还会将匹配结果写入`rmatch`指向的`QRegularExpressionMatch`对象中。

### `bool endsWith(QChar ch) const`

**作用与语义：**

如果此字符串视图以 `str` 所表示的 UTF-16 字符串、`l1` 所表示的 Latin-1 字符串或 `ch` 所表示的字符结尾，则返回 `true`；否则返回 `false`。如果 `cs` 为 `Qt::CaseSensitive`（默认值），则搜索区分大小写；否则搜索不区分大小写。

### `bool endsWith(QLatin1StringView l1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果此字符串视图以 `str` 所表示的 UTF-16 字符串、`l1` 所表示的 Latin-1 字符串或 `ch` 所表示的字符结尾，则返回 `true`；否则返回 `false`。如果 `cs` 为 `Qt::CaseSensitive`（默认值），则搜索区分大小写；否则搜索不区分大小写。

### `bool endsWith(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果此字符串视图以 `str` 所表示的 UTF-16 字符串、`l1` 所表示的 Latin-1 字符串或 `ch` 所表示的字符结尾，则返回 `true`；否则返回 `false`。如果 `cs` 为 `Qt::CaseSensitive`（默认值），则搜索区分大小写；否则搜索不区分大小写。

### `qsizetype indexOf(QLatin1StringView l1, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回 `str` 查看的 UTF-16 字符串首次出现的索引位置，`l1` 查看的拉丁字母 1 字符串，或字符 `ch`，分别从索引位置 `from` 向前搜索。如果未找到 `str`、`l1` 或 `ch`，分别返回 -1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。

### `qsizetype indexOf(QStringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回字符串视图中正则表达式`re`的第一个匹配的索引位置，从索引位置 `from` 向前搜索。如果 `re` 在任何地方都不匹配，返回 -1。
如果匹配成功且`rmatch`未被`nullptr`，它还会将匹配结果写入`rmatch`指向的`QRegularExpressionMatch`对象中。
注意：由于正则表达式匹配算法的工作原理，该函数实际上会从字符串视图开始反复匹配，直到达到`from`的位置。

### `qsizetype lastIndexOf(QLatin1StringView l1, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

注意：该功能会让`QStringView::lastIndexOf()`重载。

### `qsizetype lastIndexOf(QStringView str, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回 `str` 查看的 UTF-16 字符串最后出现位置，或 `l1` 查看的 Latin-1 字符串的索引位置，从该字符串视图的最后一个字符向后搜索。如果未找到 `str` 或 `l1`，分别返回 -1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索区分大小写;否则搜索不区分大小写。

### `(since 6.2) qsizetype lastIndexOf(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回 `str` 查看的 UTF-16 字符串最后出现位置，或 `l1` 查看的 Latin-1 字符串的索引位置，从该字符串视图的最后一个字符向后搜索。如果未找到 `str` 或 `l1`，分别返回 -1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索区分大小写;否则搜索不区分大小写。

### `(since 6.0) QList<QStringView> split(QChar sep, Qt::SplitBehavior behavior = Qt::KeepEmptyParts, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

将字符串拆分为子字符串视图，视角为正则表达式 `re` 匹配的部分，并返回这些字符串的列表。如果 `re` 在字符串中不匹配，split() 返回包含该字符串的单元素列表视图。
注意：返回列表中的视图是该视图的子视图;因此，它们引用的数据与该视图相同，且仅在该数据仍然有效期间有效。

### `bool startsWith(QChar ch) const`

**作用与语义：**

如果此字符串视图以 `str` 所表示的 UTF-16 字符串、`l1` 所表示的 Latin-1 字符串或 `ch` 所表示的字符开头，则返回 `false`；否则返回 `false`。如果 `cs` 为 `Qt::CaseSensitive`（默认值），则搜索区分大小写；否则搜索不区分大小写。

### `bool startsWith(QLatin1StringView l1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果此字符串视图以 `str` 所表示的 UTF-16 字符串、`l1` 所表示的 Latin-1 字符串或 `ch` 所表示的字符开头，则返回 `false`；否则返回 `false`。如果 `cs` 为 `Qt::CaseSensitive`（默认值），则搜索区分大小写；否则搜索不区分大小写。

### `bool startsWith(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果此字符串视图以 `str` 所表示的 UTF-16 字符串、`l1` 所表示的 Latin-1 字符串或 `ch` 所表示的字符开头，则返回 `false`；否则返回 `false`。如果 `cs` 为 `Qt::CaseSensitive`（默认值），则搜索区分大小写；否则搜索不区分大小写。

### `bool operator!=(const QStringView &lhs, const QStringView &rhs)`

**作用与语义：**

用于比较 `lhs` 和 `rhs` 的操作符。

### `bool operator<(const QStringView &lhs, const QStringView &rhs)`

**作用与语义：**

用于比较 `lhs` 和 `rhs` 的操作符。

### `bool operator<=(const QStringView &lhs, const QStringView &rhs)`

**作用与语义：**

用于比较 `lhs` 和 `rhs` 的操作符。

### `bool operator==(const QStringView &lhs, const QStringView &rhs)`

**作用与语义：**

用于比较 `lhs` 和 `rhs` 的操作符。

### `bool operator>(const QStringView &lhs, const QStringView &rhs)`

**作用与语义：**

用于比较 `lhs` 和 `rhs` 的操作符。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QStringView` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
