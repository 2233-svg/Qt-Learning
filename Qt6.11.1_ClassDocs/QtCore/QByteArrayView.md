# QByteArrayView

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QByteArrayView` 是 Qt 的值类型，围绕“Byte数组视图”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QByteArrayView` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QByteArrayView>`
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

- `QByteArrayView()`
- `(since 6.9) QByteArrayView(const Byte (&)[] data)`
- `QByteArrayView(const Byte *data)`
- `QByteArrayView(const Container &c)`
- `QByteArrayView(const QByteArray &byteArray)`
- `QByteArrayView(const char (&)[Size] data)`
- `QByteArrayView(std::nullptr_t)`
- `QByteArrayView(const Byte *first, const Byte *last)`
- `QByteArrayView(const Byte *data, qsizetype len)`
- `char at(qsizetype n) const`
- `char back() const`
- `QByteArrayView::const_iterator begin() const`
- `QByteArrayView::const_iterator cbegin() const`
- `QByteArrayView::const_iterator cend() const`
- `void chop(qsizetype length)`
- `QByteArrayView chopped(qsizetype length) const`
- `(since 6.2) int compare(QByteArrayView bv, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QByteArrayView::const_pointer constData() const`
- `bool contains(QByteArrayView bv) const`
- `bool contains(char ch) const`
- `qsizetype count(QByteArrayView bv) const`
- `qsizetype count(char ch) const`
- `QByteArrayView::const_reverse_iterator crbegin() const`
- `QByteArrayView::const_reverse_iterator crend() const`
- `QByteArrayView::const_pointer data() const`
- `bool empty() const`
- `QByteArrayView::const_iterator end() const`
- `bool endsWith(QByteArrayView bv) const`
- `bool endsWith(char ch) const`
- `QByteArrayView first(qsizetype n) const`
- `char front() const`
- `qsizetype indexOf(QByteArrayView bv, qsizetype from = 0) const`
- `qsizetype indexOf(char ch, qsizetype from = 0) const`
- `bool isEmpty() const`
- `bool isNull() const`
- `(since 6.3) bool isValidUtf8() const`
- `QByteArrayView last(qsizetype n) const`
- `qsizetype lastIndexOf(QByteArrayView bv, qsizetype from) const`
- `qsizetype lastIndexOf(char ch, qsizetype from = -1) const`
- `(since 6.2) qsizetype lastIndexOf(QByteArrayView bv) const`
- `qsizetype length() const`
- `(since 6.8) qsizetype max_size() const`
- `QByteArrayView::const_reverse_iterator rbegin() const`
- `QByteArrayView::const_reverse_iterator rend() const`
- `qsizetype size() const`
- `(since 6.8) QByteArrayView & slice(qsizetype pos, qsizetype n)`
- `(since 6.8) QByteArrayView & slice(qsizetype pos)`
- `QByteArrayView sliced(qsizetype pos) const`
- `QByteArrayView sliced(qsizetype pos, qsizetype n) const`
- `bool startsWith(QByteArrayView bv) const`
- `bool startsWith(char ch) const`
- `QByteArray toByteArray() const`
- `(since 6.3) double toDouble(bool *ok = nullptr) const`
- `(since 6.3) float toFloat(bool *ok = nullptr) const`
- `(since 6.3) int toInt(bool *ok = nullptr, int base = 10) const`
- `(since 6.3) long toLong(bool *ok = nullptr, int base = 10) const`
- `(since 6.3) qlonglong toLongLong(bool *ok = nullptr, int base = 10) const`
- `(since 6.3) short toShort(bool *ok = nullptr, int base = 10) const`
- `(since 6.3) uint toUInt(bool *ok = nullptr, int base = 10) const`
- `(since 6.3) ulong toULong(bool *ok = nullptr, int base = 10) const`
- `(since 6.3) qulonglong toULongLong(bool *ok = nullptr, int base = 10) const`
- `(since 6.3) ushort toUShort(bool *ok = nullptr, int base = 10) const`
- `(since 6.3) QByteArrayView trimmed() const`
- `void truncate(qsizetype length)`
- `(since 6.7) operator std::string_view() const`
- `char operator[](qsizetype n) const`

### 静态公有成员

- `QByteArrayView fromArray(const Byte (&)[Size] data)`
- `(since 6.8) qsizetype maxSize()`

### 相关非成员函数

- `bool operator!=(const QByteArrayView &lhs, const QByteArrayView &rhs)`
- `bool operator<(const QByteArrayView &lhs, const QByteArrayView &rhs)`
- `bool operator<=(const QByteArrayView &lhs, const QByteArrayView &rhs)`
- `bool operator==(const QByteArrayView &lhs, const QByteArrayView &rhs)`
- `bool operator>(const QByteArrayView &lhs, const QByteArrayView &rhs)`
- `bool operator>=(const QByteArrayView &lhs, const QByteArrayView &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QByteArrayView::const_iterator`

**作用与语义：**

该typedef为`QByteArrayView`提供了STL风格的const迭代器。

### `QByteArrayView::const_pointer`

**作用与语义：**

`value_type *`的别名。为兼容STL提供。

### `QByteArrayView::const_reference`

**作用与语义：**

`value_type &`的别名。为兼容STL提供。

### `QByteArrayView::const_reverse_iterator`

**作用与语义：**

该typedef为`QByteArrayView`提供了一个STL风格的const反迭代器。

### `QByteArrayView::difference_type`

**作用与语义：**

`std::ptrdiff_t`的别名。为兼容STL而提供。

### `QByteArrayView::iterator`

**作用与语义：**

该typedef为`QByteArrayView`提供了一个STL风格的const迭代器。
`QByteArrayView`不支持可变迭代器，所以这和`const_iterator`一样。

### `QByteArrayView::pointer`

**作用与语义：**

`value_type *`的别名。为与STL兼容提供。
`QByteArrayView`不支持可变指针，所以这和`const_pointer`是一样的。

### `QByteArrayView::reference`

**作用与语义：**

`value_type &`的别名。为兼容STL提供。
`QByteArrayView`不支持可变引用，所以这和`const_reference`一样。

### `QByteArrayView::reverse_iterator`

**作用与语义：**

该类型定义为`QByteArrayView`提供了一个STL风格的const反迭代器。
`QByteArrayView`不支持可变的反迭代器，所以这和`const_reverse_iterator`一样。

### `QByteArrayView::size_type`

**作用与语义：**

qsizetype 的别名。为兼容 STL 提供。

### `QByteArrayView::storage_type`

**作用与语义：**

`char`的别名。

### `QByteArrayView::value_type`

**作用与语义：**

`const char`的别名。为兼容STL而提供。

### `[constexpr noexcept] QByteArrayView::QByteArrayView()`

**作用与语义：**

构建一个空字节数组视图。

### `[constexpr noexcept, since 6.9] template <typename Byte, QByteArrayView::if_compatible_byte<Byte> = true> QByteArrayView::QByteArrayView(const Byte (&)[] data)`

**作用与语义：**

在 `data` 上构造字节数组视图，该数组大小未知。长度通过扫描第一个`Byte(0)`确定。
`data`必须在这个字节数组视图对象的生命周期内保持有效。
仅当 `Byte` 是兼容的字节类型时，才参与重载决议。

### `[constexpr noexcept] template <typename Byte> QByteArrayView::QByteArrayView(const Byte *data)`

**作用与语义：**

在`data`上构建字节数组视图。长度通过扫描第一个`Byte(0)`确定。
`data`必须在该字节数组视图对象的生命周期内保持有效。
将`nullptr`传递为`data`是安全的，并且会得到空字节数组视图。
只有当 `data` 不是数组且 `Byte` 是兼容的字节类型时，才参与超载解析。

### `[constexpr noexcept] template <typename Container, QByteArrayView::if_compatible_container<Container> = true> QByteArrayView::QByteArrayView(const Container &c)`

**作用与语义：**

在数组类容器上构建字节数组视图`c`。长度和数据分别通过 `std::size(c)` 和 `std::data(c)` 设定。
容器的数据必须在该字节数组视图对象的生命周期内保持有效。
只有当 `c` 是具有兼容字节类型元素的连续容器时，才参与超载解析。

### `[noexcept] QByteArrayView::QByteArrayView(const QByteArray &byteArray)`

**作用与语义：**

在`byteArray`上构造字节数组视图。
`byteArray.data()`必须在这个字节数组视图对象的生命周期内保持有效。
字节数组视图当且仅当 `byteArray.isNull()` 时才为空。

### `[constexpr noexcept] template <size_t Size> QByteArrayView::QByteArrayView(const char (&)[Size] data)`

**作用与语义：**

在字符数组`data`上构造字节数组视图。视图覆盖数组直到遇到第一个`'\0'`，或`Size`，以先到者为准。如果需要完整数组，可以用`fromArray()`。
`data`必须在该字节数组视图对象的生命周期内保持有效。
注意：该构造器仅适用于char数组文字。这样做的原因是兼容预定义“足够大”数组但只使用部分预分配空间的C库。为了在隐式构造器重载中直观地支持这一点，我们需要在第一个`char(0)`停止。这对char数组来说合乎逻辑，但对`std::byte`数组则不然。然而，它与对应的指针（`Byte*`）和未知长度数组（`Byte[]`）构造函数不一致，因此未来Qt版本可能会有所变化。

### `[constexpr noexcept] QByteArrayView::QByteArrayView(std::nullptr_t)`

**作用与语义：**

构建一个空字节数组视图。

### `[constexpr] template <typename Byte, QByteArrayView::if_compatible_byte<Byte> = true> QByteArrayView::QByteArrayView(const Byte *first, const Byte *last)`

**作用与语义：**

在`first`上构造长度为 （`last` - `first`） 的字节数组视图。
该`[first,last)`范围必须在整个QByteArrayView的生命周期内保持有效。
如果`nullptr`也被`last`，将`\nullptr`传递为`first`是安全的，且会导致空字节数组视图。
如果`last`先于`first`，或者`first`是`nullptr`而`last`不是，行为则未定义。
仅当 `Byte` 是兼容的字节类型时，才参与重载决议。

### `[constexpr] template <typename Byte, QByteArrayView::if_compatible_byte<Byte> = true> QByteArrayView::QByteArrayView(const Byte *data, qsizetype len)`

**作用与语义：**

构造长度为`len`的字节数组视图`data`。
该`[data,len)`范围必须在整个QByteArrayView的生命周期内保持有效。
如果 `len` 也是 0，`nullptr` 作为 `data` 传递是安全的，并且会看到空字节数组视图。
如果`len`为负，行为未定义;当为正时，`data`为`nullptr`时。
仅当 `Byte` 是兼容的字节类型时，才参与重载决议。

### `[constexpr] char QByteArrayView::at(qsizetype n) const`

**作用与语义：**

返回该字节数组视图中位置`n`的字符。
行为是负面还是不小于`size()`，行为未`n`定义。

### `[constexpr] char QByteArrayView::back() const`

**作用与语义：**

返回字节数组视图中的最后一个字节。
此功能是为了STL兼容性而提供。
警告：在空字节数组视图中调用该函数构成未定义行为。

### `[constexpr noexcept] QByteArrayView::const_iterator QByteArrayView::begin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向字节数组视图中的第一个字节。
此功能是为了STL兼容性而提供。

### `[constexpr noexcept] QByteArrayView::const_iterator QByteArrayView::cbegin() const`

**作用与语义：**

和`begin()`一样。
此功能是为了STL兼容性而提供。

### `[constexpr noexcept] QByteArrayView::const_iterator QByteArrayView::cend() const`

**作用与语义：**

和`end()`一样。
此功能是为了STL兼容性而提供。

### `[constexpr] void QByteArrayView::chop(qsizetype length)`

**作用与语义：**

将该字节数组视图截断为`length`字符。
和`*this = first(size() - length)`一样。
注意：当`length` <0或`length` > `size()`时，行为未定义。

### `[constexpr] QByteArrayView QByteArrayView::chopped(qsizetype length) const`

**作用与语义：**

返回该字节数组视图的副本，省略了最后一个`length`字节。换句话说，返回长度为`size()` - `length`的字节数组视图，从该对象的开头开始。
和`first(size() - length)`一样。
注意：当`length` <0或`length` > `size()`时，行为未定义。

### `[noexcept, since 6.2] int QByteArrayView::compare(QByteArrayView bv, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回一个整数，大小于、等于或大于零，具体取决于`QByteArrayView`排序在`QByteArrayView` `bv`之前、相同位置还是之后。比较根据大小写敏感`cs`进行。

### `[constexpr noexcept] QByteArrayView::const_pointer QByteArrayView::constData() const`

**作用与语义：**

返回一个指向字节数组视图中第一个字节的const `char`指针。
注意：返回值表示的字符数组不保证为空终止。返回指针仅安全用于访问小于该字节数组视图`size()`的索引的字节。

### `[noexcept] bool QByteArrayView::contains(char ch) const`

**作用与语义：**

如果该字节数组视图包含`bv`或字符`ch`所显示的字节序列的出现，返回`true`;否则返回`false`。

### `[noexcept] qsizetype QByteArrayView::count(QByteArrayView bv) const`

**作用与语义：**

返回`bv`在该字节数组视图中看到的字节序列的（可能重叠）次数。

### `[noexcept] qsizetype QByteArrayView::count(char ch) const`

**作用与语义：**

返回该字节数组视图中字节`ch`的出现次数。

### `[constexpr noexcept] QByteArrayView::const_reverse_iterator QByteArrayView::crbegin() const`

**作用与语义：**

和`rbegin()`一样。
此功能是为了STL兼容性而提供。

### `[constexpr noexcept] QByteArrayView::const_reverse_iterator QByteArrayView::crend() const`

**作用与语义：**

和`rend()`一样。
此功能是为了STL兼容性而提供。

### `[constexpr noexcept] QByteArrayView::const_pointer QByteArrayView::data() const`

**作用与语义：**

返回一个指向字节数组视图中第一个字节的const `char`指针。
注意：返回值表示的字符数组不保证为空终止。返回指针仅安全用于访问小于该字节数组视图`size()`的索引的字节。

### `[constexpr noexcept] bool QByteArrayView::empty() const`

**作用与语义：**

如果该字节数组视图为空，也就是返回`size() == 0`，返回`true`。
此功能是为了STL兼容性而提供。

### `[constexpr noexcept] QByteArrayView::const_iterator QByteArrayView::end() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向字节数组视图中最后一个字节之后。
此功能是为了STL兼容性而提供。

### `[constexpr noexcept] bool QByteArrayView::endsWith(char ch) const`

**作用与语义：**

如果该字节数组视图以字节数组视图`bv`结尾或字符 `ch`，返回`true`;否则返回`false`。

### `[constexpr] QByteArrayView QByteArrayView::first(qsizetype n) const`

**作用与语义：**

返回一个指向该字节数组视图前`n`字节的字节数组视图。等价于`sliced(0, n)`。
注意：当`n` <0或`n` > `size()`时，行为未定义。

### `[static constexpr noexcept] template <typename Byte, size_t Size> QByteArrayView QByteArrayView::fromArray(const Byte (&)[Size] data)`

**作用与语义：**

在数组文字 `data` 上构造一个字节数组视图。视图覆盖整个数组。这包括数组文字的尾随 null-terminator `char`。如果你不想在视图中包含空终端，确定它在结尾时可以`chop()`。或者你也可以使用构造函数重载，取一个字符数组文字，创建一个视图直到数据中第一个空终止符，但不包括它。
该函数可对任何兼容字节类型的数组文字工作。

### `[constexpr] char QByteArrayView::front() const`

**作用与语义：**

返回字节数组视图中的第一个字节。
此功能是为了STL兼容性而提供。
警告：在空字节数组视图中调用该函数构成未定义行为。

### `[noexcept] qsizetype QByteArrayView::indexOf(char ch, qsizetype from = 0) const`

**作用与语义：**

返回该字节数组视图中，从索引位置`from.Returns`-1向前搜索，返回`bv`查看的字节序列首次出现的索引位置或字节`ch`的首次出现位置。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。

### `[constexpr noexcept] bool QByteArrayView::isEmpty() const`

**作用与语义：**

如果该字节数组视图为空，也就是返回`size() == 0`，返回`true`。

### `[constexpr noexcept] bool QByteArrayView::isNull() const`

**作用与语义：**

如果该字节数组视图为空，也就是返回`data() == nullptr`，返回`true`。

### `[noexcept, since 6.3] bool QByteArrayView::isValidUtf8() const`

**作用与语义：**

返回`true`该字节数组视图是否包含有效的UTF-8编码数据，否则`false`返回。

### `[constexpr] QByteArrayView QByteArrayView::last(qsizetype n) const`

**作用与语义：**

返回一个指向该字节数组视图最后`n`字节的字节数组视图。
注意：当`n` <0或`n` > `size()`时，行为是未定义的。

### `[noexcept] qsizetype QByteArrayView::lastIndexOf(char ch, qsizetype from = -1) const`

**作用与语义：**

返回该字节数组视图中，`bv` 查看的字节序列最后一次出现的起点或字节`ch`的最后一次出现的索引位置，从索引位置`from`向后搜索。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。
如果没有匹配，则返回-1。
注意：在搜索长度为0的`bv`时，数据末尾的匹配被负`from`排除，尽管`-1`通常被认为是从视图末尾搜索：最后匹配位于最后一个字符之后，因此被排除。要包含这样的最终空匹配，要么给出`from`的正值，要么完全省略`from`参数。

### `[noexcept, since 6.2] qsizetype QByteArrayView::lastIndexOf(QByteArrayView bv) const`

**作用与语义：**

返回该字节数组视图中，`bv` 查看的字节序列最后一次出现的起点或字节`ch`的最后一次出现的索引位置，从索引位置`from`向后搜索。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。
如果没有匹配，则返回-1。
注意：在搜索长度为0的`bv`时，数据末尾的匹配被负`from`排除，尽管`-1`通常被认为是从视图末尾搜索：最后匹配位于最后一个字符之后，因此被排除。要包含这样的最终空匹配，要么给出`from`的正值，要么完全省略`from`参数。

### `[constexpr noexcept] qsizetype QByteArrayView::length() const`

**作用与语义：**

和`size()`一样。

### `[static constexpr noexcept, since 6.8] qsizetype QByteArrayView::maxSize()`

**作用与语义：**

它返回视图理论上能表示的最大元素数。实际上，这个数量可以更小，受限于系统可用的内存。

### `[constexpr noexcept, since 6.8] qsizetype QByteArrayView::max_size() const`

**作用与语义：**

此功能是为了STL兼容性而提供。
退货 `maxSize()`。

### `[constexpr noexcept] QByteArrayView::const_reverse_iterator QByteArrayView::rbegin() const`

**作用与语义：**

返回一个const STL风格的反向迭代器，指向字节数组视图中的第一个字节，顺序相反。
此功能是为了STL兼容性而提供。

### `[constexpr noexcept] QByteArrayView::const_reverse_iterator QByteArrayView::rend() const`

**作用与语义：**

返回一个STL风格的反向迭代器，指向字节数组视图中最后一个字节之后的迭代器，顺序相反。
此功能是为了STL兼容性而提供。

### `[constexpr noexcept] qsizetype QByteArrayView::size() const`

**作用与语义：**

返回该字节数组视图中的字节数。

### `[constexpr, since 6.8] QByteArrayView &QByteArrayView::slice(qsizetype pos, qsizetype n)`

**作用与语义：**

修改该字节数组视图，从位置`pos`开始，扩展`n`字节。
注意：当`pos` <0、`n` <0或`pos` `n` > `size()`时，行为未定义。

### `[constexpr, since 6.8] QByteArrayView &QByteArrayView::slice(qsizetype pos)`

**作用与语义：**

修改该字节数组视图，从位置`pos`开始，延伸至末尾。
注意：当`pos` <0或`pos` > `size()`时，行为未定义。

### `[constexpr] QByteArrayView QByteArrayView::sliced(qsizetype pos) const`

**作用与语义：**

返回一个从该对象位置`pos`开始，延伸至末端的字节数组视图。
注意：当`pos` <0或`pos` > `size()`时，行为未定义。

### `[constexpr] QByteArrayView QByteArrayView::sliced(qsizetype pos, qsizetype n) const`

**作用与语义：**

返回一个字节数组视图，指向该字节数组视图的`n`字节，从位置`pos`开始。
注意：当`pos` <0、`n` <0或`pos` `n` > `size()`时，行为未定义。

### `[constexpr noexcept] bool QByteArrayView::startsWith(char ch) const`

**作用与语义：**

如果该字节数组视图以字节数组视图`bv`或字符`ch`开头，返回`true`;否则返回`false`。

### `QByteArray QByteArrayView::toByteArray() const`

**作用与语义：**

返回该字节数组视图数据的深度副本，作为`QByteArray`。
返回值为空`QByteArray`当且仅当该字节数组视图为空。

### `[since 6.3] double QByteArrayView::toDouble(bool *ok = nullptr) const`

**作用与语义：**

返回该字节数组视图，转换为`double`值。
如果转换溢出，返回无穷大;如果因其他原因（如溢出），则返回0.0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
警告：`QByteArrayView`内容可能仅包含有效的数字字符，包括加号/减号、科学记号中使用的字符e和小数点。添加单位或额外字符会导致换算错误。
注意：数字转换在默认的 C 区域执行，无论用户所在位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。
该函数忽略前置和后置间距字符。

### `[since 6.3] float QByteArrayView::toFloat(bool *ok = nullptr) const`

**作用与语义：**

返回该字节数组视图，转换为`float`值。
如果转换溢出，返回无穷大;如果因其他原因（如溢出），则返回0.0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
警告：`QByteArrayView`内容可能仅包含有效的数字字符，包括加号/减号、科学记号中使用的字符e和小数点。添加单位或额外字符会导致转换错误。
注意：数字转换在默认的 C 区域执行，无论用户所在位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。
该函数忽略前置和后置的空白。

**官方示例：**

```cpp
 QByteArrayView string("1234.56 Volt");
 bool ok;
 float a = string.toFloat(&ok);       // a == 0, ok == false
 a = string.first(7).toFloat(&ok); // a == 1234.56, ok == true
```

### `[since 6.3] int QByteArrayView::toInt(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回此字节数组视图，并转换为`int`，默认为十`base`。支持0、2至36的底部，使用字母表示9以上的数字;A为十，B为十一，依此类推。
如果 `base` 为 0，则根据以下规则自动确定基数：如果字节数组视图以“0x”开头，其余部分被读取为十六进制（以 16 进制为基）;否则，如果以 “0” 开头，其余部分被读取为八进制（以 8 进制为基）;否则则以十进制读出。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在的位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 QByteArrayView str("FF");
 bool ok;
 int hex = str.toInt(&ok, 16);     // hex == 255, ok == true
 int dec = str.toInt(&ok, 10);     // dec == 0, ok == false
```

### `[since 6.3] long QByteArrayView::toLong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回此字节数组视图，转换为`long`整数，底数为`base`，默认为十。支持底数0和2至36，数字9以上使用字母表示;A为十，B为十一，依此类推。
如果 `base` 为 0，则根据以下规则自动确定基位：如果字节数组视图以“0x”开头，其余部分被读取为十六进制（以 16 进制为基）;否则，如果以“0” 开头，其余部分被读取为八进制（以 8 进制为基）;否则则以十进制读出。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 QByteArrayView str("FF");
 bool ok;
 long hex = str.toLong(&ok, 16);   // hex == 255, ok == true
 long dec = str.toLong(&ok, 10);   // dec == 0, ok == false
```

### `[since 6.3] qlonglong QByteArrayView::toLongLong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回该字节数组视图，转换为`long long`，使用`base`为底，默认为十。支持第0和第2到第36进位，使用字母表示9以上的数字;A为十，B为十一，依此类推。
如果 `base` 为 0，则根据以下规则自动确定基位：如果字节数组视图以“0x”开头，其余部分被读取为十六进制（以 16 进制为底）;否则，如果以 “0” 开头，其余部分被读取为八进制（以 8 进制为本）;否则则以十进制读出。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。

### `[since 6.3] short QByteArrayView::toShort(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回该字节数组视图，并转换为`short`，使用默认为十的`base`。支持0、2到36的进制，使用字母表示9以上的数字;A为十，B为十一，依此类推。
如果 `base` 为 0，则根据以下规则自动确定基数：如果字节数组视图以“0x”开头，其余部分被读取为十六进制（以 16 进制为基）;否则，如果以 “0” 开头，其余部分被读取为八进制（以 8 为底）;否则则以十进制读出。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在的位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

### `[since 6.3] uint QByteArrayView::toUInt(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回此字节数组视图，并使用`base`为底转换为`unsigned int`，默认为十。支持底数0和2至36，使用字母表示9以上的数字;A为十，B为十一，依此类推。
如果`base`为0，则根据以下规则自动确定基位：如果字节数组视图以“0x”开头，其余部分被读取为十六进制（以16为底）;否则，如果以“0”开头，其余部分被读取为八进制（以8为底）;否则则读作十进制。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。

### `[since 6.3] ulong QByteArrayView::toULong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回此字节数组视图，转换为`unsigned long int`，默认为十`base`。支持0、2至36的数字，9以上数字使用字母;A为十，B为十一，依此类推。
如果 `base` 为 0，则根据以下规则自动确定基位：如果字节数组视图以“0x”开头，其余部分被读取为十六进制（以 16 进制为基）;否则，如果以“0” 开头，其余部分被读取为八进制（以 8 进制为基）;否则则以十进制读出。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。

### `[since 6.3] qulonglong QByteArrayView::toULongLong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回该字节数组视图，转换为`unsigned long long`，使用`base`为底，默认为十。支持第0、2到36的进制，数字9以上使用字母;A为十，B为十一，依此类推。
如果 `base` 为 0，则根据以下规则自动确定基数：如果字节数组视图以“0x”开头，其余部分被读取为十六进制（以 16 进制为基）;否则，如果以 “0” 开头，其余部分被读取为八进制（以 8 为底）;否则则以十进制读出。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在的位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

### `[since 6.3] ushort QByteArrayView::toUShort(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回此字节数组视图，并转换为`unsigned short`，默认为十`base`。支持0、2至36的底部，使用字母表示9以上的数字;A为十，B为十一，依此类推。
如果 `base` 为 0，则根据以下规则自动确定基数：如果字节数组视图以“0x”开头，其余部分被读取为十六进制（以 16 进制为基）;否则，如果以 “0” 开头，其余部分被读取为八进制（以 8 进制为基）;否则则以十进制读出。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在的位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。

### `[noexcept, since 6.3] QByteArrayView QByteArrayView::trimmed() const`

**作用与语义：**

返回该字节数组视图的副本，且从起始和结尾去除了空格字符。
间距字符是标准 C 语言 `isspace()` 函数在 C 语言区域返回 `true` 的字符;这些字符包括 ASCII 字符的表格 '\t'、换行 '\n'、回车 '\r'、垂直表格 '\v'、表单输入 '\f' 和空格 ' '。

### `[constexpr] void QByteArrayView::truncate(qsizetype length)`

**作用与语义：**

将该字节数组视图截断为长度`length`。
和`*this = first(length)`一样。
注意：当`length` <0或`length` > `size()`时，行为未定义。

### `[constexpr noexcept, since 6.7] QByteArrayView::operator std::string_view() const`

**作用与语义：**

将该`QByteArrayView`对象转换为`std::string_view`对象。返回的视图将拥有相同的数据指针和长度。

### `[constexpr] char QByteArrayView::operator[](qsizetype n) const`

**作用与语义：**

返回该字节数组视图中位置`n`的字符。
行为是负面还是不小于`size()`，行为未`n`定义。

### `[noexcept] bool operator>=(const QByteArrayView &lhs, const QByteArrayView &rhs)`

**作用与语义：**

比较算子的`QByteArrayView`。

### `const_iterator`

**作用与语义：**

该typedef为`QByteArrayView`提供了STL风格的const迭代器。

### `const_pointer`

**作用与语义：**

`value_type *`的别名。为兼容STL提供。

### `const_reference`

**作用与语义：**

`value_type &`的别名。为兼容STL提供。

### `const_reverse_iterator`

**作用与语义：**

该typedef为`QByteArrayView`提供了一个STL风格的const反迭代器。

### `difference_type`

**作用与语义：**

`std::ptrdiff_t`的别名。为兼容STL而提供。

### `iterator`

**作用与语义：**

该typedef为`QByteArrayView`提供了一个STL风格的const迭代器。
`QByteArrayView`不支持可变迭代器，所以这和`const_iterator`一样。

### `pointer`

**作用与语义：**

`value_type *`的别名。为与STL兼容提供。
`QByteArrayView`不支持可变指针，所以这和`const_pointer`是一样的。

### `reference`

**作用与语义：**

`value_type &`的别名。为兼容STL提供。
`QByteArrayView`不支持可变引用，所以这和`const_reference`一样。

### `reverse_iterator`

**作用与语义：**

该类型定义为`QByteArrayView`提供了一个STL风格的const反迭代器。
`QByteArrayView`不支持可变的反迭代器，所以这和`const_reverse_iterator`一样。

### `size_type`

**作用与语义：**

qsizetype 的别名。为兼容 STL 提供。

### `storage_type`

**作用与语义：**

`char`的别名。

### `value_type`

**作用与语义：**

`const char`的别名。为兼容STL而提供。

### `bool contains(QByteArrayView bv) const`

**作用与语义：**

如果该字节数组视图包含`bv`或字符`ch`所显示的字节序列的出现，返回`true`;否则返回`false`。

### `bool endsWith(QByteArrayView bv) const`

**作用与语义：**

如果该字节数组视图以字节数组视图`bv`结尾或字符 `ch`，返回`true`;否则返回`false`。

### `qsizetype indexOf(QByteArrayView bv, qsizetype from = 0) const`

**作用与语义：**

返回该字节数组视图中，从索引位置`from.Returns`-1向前搜索，返回`bv`查看的字节序列首次出现的索引位置或字节`ch`的首次出现位置。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。

### `qsizetype lastIndexOf(QByteArrayView bv, qsizetype from) const`

**作用与语义：**

返回`bv`在该字节数组视图中，从该字节数组视图末端往回搜索时，最后一次出现字节序列的起始位置。如果未找到匹配，返回-1。

### `bool startsWith(QByteArrayView bv) const`

**作用与语义：**

如果该字节数组视图以字节数组视图`bv`或字符`ch`开头，返回`true`;否则返回`false`。

### `bool operator!=(const QByteArrayView &lhs, const QByteArrayView &rhs)`

**作用与语义：**

比较算子的`QByteArrayView`。

### `bool operator<(const QByteArrayView &lhs, const QByteArrayView &rhs)`

**作用与语义：**

比较算子的`QByteArrayView`。

### `bool operator<=(const QByteArrayView &lhs, const QByteArrayView &rhs)`

**作用与语义：**

比较算子的`QByteArrayView`。

### `bool operator==(const QByteArrayView &lhs, const QByteArrayView &rhs)`

**作用与语义：**

比较算子的`QByteArrayView`。

### `bool operator>(const QByteArrayView &lhs, const QByteArrayView &rhs)`

**作用与语义：**

比较算子的`QByteArrayView`。

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

`QByteArrayView` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
