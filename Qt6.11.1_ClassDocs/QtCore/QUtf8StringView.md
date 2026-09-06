# QUtf8StringView

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QUtf8StringView` 是 Qt 的值类型，围绕“Utf8String视图”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QUtf8StringView` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QUtf8StringView>`
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

- `QUtf8StringView()`
- `QUtf8StringView(const Char (&)[N] string)`
- `QUtf8StringView(const Char *str)`
- `QUtf8StringView(const Container &str)`
- `QUtf8StringView(std::nullptr_t)`
- `QUtf8StringView(const Char *first, const Char *last)`
- `QUtf8StringView(const Char *str, qsizetype len)`
- `(since 6.9) QString arg(Args &&... args) const`
- `QUtf8StringView::storage_type at(qsizetype n) const`
- `QUtf8StringView::storage_type back() const`
- `QUtf8StringView::const_iterator begin() const`
- `QUtf8StringView::const_iterator cbegin() const`
- `QUtf8StringView::const_iterator cend() const`
- `void chop(qsizetype n)`
- `QUtf8StringView chopped(qsizetype n) const`
- `(since 6.5) int compare(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.5) int compare(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.5) int compare(QUtf8StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QUtf8StringView::const_reverse_iterator crbegin() const`
- `QUtf8StringView::const_reverse_iterator crend() const`
- `QUtf8StringView::const_pointer data() const`
- `bool empty() const`
- `QUtf8StringView::const_iterator end() const`
- `QUtf8StringView first(qsizetype n) const`
- `QUtf8StringView::storage_type front() const`
- `bool isEmpty() const`
- `bool isNull() const`
- `(since 6.3) bool isValidUtf8() const`
- `QUtf8StringView last(qsizetype n) const`
- `qsizetype length() const`
- `(since 6.8) qsizetype max_size() const`
- `QUtf8StringView::const_reverse_iterator rbegin() const`
- `QUtf8StringView::const_reverse_iterator rend() const`
- `qsizetype size() const`
- `(since 6.8) QUtf8StringView & slice(qsizetype pos, qsizetype n)`
- `(since 6.8) QUtf8StringView & slice(qsizetype pos)`
- `QUtf8StringView sliced(qsizetype pos) const`
- `QUtf8StringView sliced(qsizetype pos, qsizetype n) const`
- `QString toString() const`
- `void truncate(qsizetype n)`
- `const char8_t * utf8() const`
- `(since 6.7) operator std::string_view() const`
- `(since 6.10) operator std::u8string_view() const`
- `QUtf8StringView::storage_type operator[](qsizetype n) const`

### 静态公有成员

- `QUtf8StringView fromArray(const Char (&)[Size] string)`
- `(since 6.8) qsizetype maxSize()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QUtf8StringView::const_iterator`

**作用与语义：**

该typedef为`QUtf8StringView`提供了一个STL风格的const迭代器。

### `QUtf8StringView::const_pointer`

**作用与语义：**

`value_type *`的别名。为兼容STL提供。

### `QUtf8StringView::const_reference`

**作用与语义：**

`value_type &`的别名。为兼容STL提供。

### `QUtf8StringView::const_reverse_iterator`

**作用与语义：**

该typedef为`QUtf8StringView`提供了一个STL风格的const反迭代器。

### `QUtf8StringView::difference_type`

**作用与语义：**

`std::ptrdiff_t`的别名。为兼容STL而提供。

### `QUtf8StringView::iterator`

**作用与语义：**

该typedef为`QUtf8StringView`提供了一个STL风格的const迭代器。
`QUtf8StringView`不支持可变迭代器，所以这和`const_iterator`是一样的。

### `QUtf8StringView::pointer`

**作用与语义：**

`value_type *`的别名。为兼容STL提供。
`QUtf8StringView`不支持可变指针，所以这和`const_pointer`一样。

### `QUtf8StringView::reference`

**作用与语义：**

`value_type &`的别名。为兼容STL提供。
`QUtf8StringView`不支持可变引用，所以这和`const_reference`一样。

### `QUtf8StringView::reverse_iterator`

**作用与语义：**

该typedef为`QUtf8StringView`提供了一个STL风格的const反迭代器。
`QUtf8StringView`不支持可变的反迭代器，所以这和`const_reverse_iterator`是一样的。

### `QUtf8StringView::size_type`

**作用与语义：**

qsizetype 的别名。为兼容 STL 提供。

### `[alias] QUtf8StringView::storage_type`

**作用与语义：**

`char`的别名。

### `QUtf8StringView::value_type`

**作用与语义：**

`const char`的别名。为兼容STL而提供。

### `[constexpr noexcept] QUtf8StringView::QUtf8StringView()`

**作用与语义：**

构造一个空字符串视图。

### `[constexpr noexcept] template <typename Char, size_t N> QUtf8StringView::QUtf8StringView(const Char (&)[N] string)`

**作用与语义：**

在字符字符串的字面量`string`上构造字符串视图。视图覆盖数组，直到遇到第一个`Char(0)`，或`N`，以先到者为准。如果需要完整数组，可以用`fromArray()`。
`string`必须在该字符串视图对象的生命周期内保持有效。
仅当 `string` 是实际数组且 `Char` 是兼容的字符类型时，才参与重载决议。兼容的字符类型包括：`char8_t`、`char`、`signed char` 和 `unsigned char`。

### `[constexpr noexcept] template <typename Char> QUtf8StringView::QUtf8StringView(const Char *str)`

**作用与语义：**

在`str`上构造字符串视图。长度通过扫描第一个`Char(0)`确定。
`str`必须在该字符串视图对象的生命周期内保持有效。
将`nullptr`传递为`str`是安全的，且会得到空字符串视图。
只有当 `str` 不是数组且 `Char` 是兼容的字符类型时，才参与重载决议。兼容的字符类型有：`char8_t`、`char`、`signed char` 和 `unsigned char`。

### `[constexpr noexcept] template <typename Container, QUtf8StringView::if_compatible_container<Container> = true> QUtf8StringView::QUtf8StringView(const Container &str)`

**作用与语义：**

在`str`上构造字符串视图。长度取自`std::size(str)`。
`std::data(str)`必须在该字符串视图对象的生命周期内保持有效。
字符串视图当且仅当 `std::size(str) == 0`。尚不确定该构造函数是否能生成空字符串视图（`std::data(str)`需返回`nullptr`）。
仅当`Container`容器具有兼容的字符类型时，才参与超载解析`value_type`。兼容的字符类型包括：`char8_t`、`char`、`signed char`和`unsigned char`。

### `[constexpr noexcept] QUtf8StringView::QUtf8StringView(std::nullptr_t)`

**作用与语义：**

构造一个空字符串视图。

### `[constexpr] template <typename Char, QUtf8StringView::if_compatible_char<Char> = true> QUtf8StringView::QUtf8StringView(const Char *first, const Char *last)`

**作用与语义：**

在 `first` 上构造一个字符串视图，长度为 (`last` - `first`)。
`[first,last)` 的范围在此字符串视图对象的生命周期内必须保持有效。
如果 `last` 也是 `nullptr`，那么将 `\nullptr` 作为 `first` 传入是安全的，并且会得到一个空字符串视图。
如果 `last` 在 `first` 之前，或者 `first` 是 `nullptr` 而 `last` 不是，则行为未定义。
仅当 `Char` 是兼容字符类型时参与重载决议。兼容的字符类型有：`char8_t`、`char`、`signed char` 和 `unsigned char`。

### `[constexpr] template <typename Char, QUtf8StringView::if_compatible_char<Char> = true> QUtf8StringView::QUtf8StringView(const Char *str, qsizetype len)`

**作用与语义：**

在长度为`len`的 `str`上构造字符串视图。
该`[str,len)`范围必须在该字符串视图对象的整个生命周期内保持有效。
如果 `len` 也是 0，将 `nullptr` 传递为 `str` 也是安全的，并且会导致字符串视角为空。
如果`len`为负，行为未定义;当为正时，`str`为`nullptr`时。
只有当`Char`是兼容的字符类型时，才参与超载解析。兼容的字符类型有：`char8_t`、`char`、`signed char`和`unsigned char`。

### `[since 6.9] template <typename... Args> QString QUtf8StringView::arg(Args &&... args) const`

**作用与语义：**

用对应的`args`参数替换该字符串中`%N`的出现。这些参数不是位置论元：`args`中的第一个用最低的`N`替换`%N`（全部），第二个用`args`的`%N`替换下一个最低的`N`，依此类推。
`Args`可以包含任何隐含地转化为`QAnyStringView`的内容。

### `[constexpr] QUtf8StringView::storage_type QUtf8StringView::at(qsizetype n) const`

**作用与语义：**

返回此字符串视图中位置 `n` 的码点。
如果 `n` 为负数或不小于 `size()`，行为未定义。

### `[constexpr] QUtf8StringView::storage_type QUtf8StringView::back() const`

**作用与语义：**

返回字符串视图中的最后一个码点。和`last()`一样。
此功能是为了STL兼容性而提供。
警告：在空字符串视图上调用该函数构成未定义行为。

### `[noexcept] QUtf8StringView::const_iterator QUtf8StringView::begin() const`

**作用与语义：**

返回一个const-STL风格的迭代器，指向字符串视图中的第一个代码点。
此功能是为了STL兼容性而提供。

### `[noexcept] QUtf8StringView::const_iterator QUtf8StringView::cbegin() const`

**作用与语义：**

和`begin()`一样。
此功能是为了STL兼容性而提供。

### `[noexcept] QUtf8StringView::const_iterator QUtf8StringView::cend() const`

**作用与语义：**

和`end()`一样。
此功能是为了STL兼容性而提供。

### `[constexpr] void QUtf8StringView::chop(qsizetype n)`

**作用与语义：**

将字符串视图截断为`n`码点。
和`*this = first(size() - n)`一样。
注意：当`n` <0或`n` > `size()`时，行为未定义。

### `[constexpr] QUtf8StringView QUtf8StringView::chopped(qsizetype n) const`

**作用与语义：**

返回长度为`size()` - `n`的子串，从该对象的开头开始。
和`first(size() - n)`一样。
注意：当`n` <0或`n` > `size()`时，行为未定义。

### `[noexcept, since 6.5] int QUtf8StringView::compare(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

将该字符串视图与 `str` 比较，若字符串视图小于 `str` 则返回负整数;大于 `str` 则返回正整数;相等时返回零。
如果`cs`是`Qt::CaseSensitive`（默认），则比较区分大小写;否则比较不区分大小写。

### `[noexcept] QUtf8StringView::const_reverse_iterator QUtf8StringView::crbegin() const`

**作用与语义：**

和`rbegin()`一样。
此功能是为了STL兼容性而提供。

### `[noexcept] QUtf8StringView::const_reverse_iterator QUtf8StringView::crend() const`

**作用与语义：**

和`rend()`一样。
此功能是为了STL兼容性而提供。

### `[constexpr noexcept] QUtf8StringView::const_pointer QUtf8StringView::data() const`

**作用与语义：**

返回字符串视图中第一个代码点的const指针。
注意：返回值所表示的字符数组并非空终止。

### `[constexpr noexcept] bool QUtf8StringView::empty() const`

**作用与语义：**

返回该字符串视图是否为空——即是否`size() == 0`。
此功能是为了STL兼容性而提供。

### `[noexcept] QUtf8StringView::const_iterator QUtf8StringView::end() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向列表中最后一个码点之后的虚码点。
此功能是为了STL兼容性而提供。

### `[constexpr] QUtf8StringView QUtf8StringView::first(qsizetype n) const`

**作用与语义：**

返回一个字符串视图，该视图包含此字符串视图的前 `n` 个代码点。
注意：当 `n` < 0 或 `n` > `size()` 时，行为未定义。

### `[static constexpr noexcept] template < typename Char, size_t Size, QUtf8StringView::if_compatible_char<Char> = true > QUtf8StringView QUtf8StringView::fromArray(const Char (&)[Size] string)`

**作用与语义：**

在完整的字符字符串字面量`string`上构造字符串视图，包括任何后`Char(0)`。如果你不想在视图中包含空终止符，那么确定它在最后时可以`chop()`。或者你也可以使用构造函数重载，取一个数组文字，创建一个视图直到数据中第一个空终止符，但不包括它。
`string`必须在该字符串视图对象的生命周期内保持有效。
如果 数组是兼容的字符类型，该函数可对任意数组字面量工作`Char`。兼容的字符类型有：`char8_t`、`char`、`signed char` 和 `unsigned char`。

### `[constexpr] QUtf8StringView::storage_type QUtf8StringView::front() const`

**作用与语义：**

返回字符串视图中的第一个码点。和`first()`一样。
此功能是为了STL兼容性而提供。
警告：在空字符串视图上调用该函数构成未定义行为。

### `[constexpr noexcept] bool QUtf8StringView::isEmpty() const`

**作用与语义：**

返回该字符串视图是否为空——即是否`size() == 0`。
此功能是为了与其他 Qt 容器的兼容性而提供。

### `[constexpr noexcept] bool QUtf8StringView::isNull() const`

**作用与语义：**

返回该字符串视图是否为空——即是否`data() == nullptr`。
这些功能是为了与其他 Qt 容器的兼容性而提供。

### `[noexcept, since 6.3] bool QUtf8StringView::isValidUtf8() const`

**作用与语义：**

如果该字符串包含有效的 UTF-8 编码数据，则返回 `true`，否则返回 `false`。

### `[constexpr] QUtf8StringView QUtf8StringView::last(qsizetype n) const`

**作用与语义：**

返回一个字符串视图，该视图包含此字符串视图的最后 `n` 个代码点。
注意：当 `n` < 0 或 `n` > `size()` 时，行为未定义。

### `[constexpr noexcept] qsizetype QUtf8StringView::length() const`

**作用与语义：**

和`size()`一样。
此功能是为了与其他 Qt 容器的兼容性而提供。

### `[static constexpr noexcept, since 6.8] qsizetype QUtf8StringView::maxSize()`

**作用与语义：**

它返回视图理论上能表示的最大元素数。实际上，这个数量可以更小，受限于系统可用的内存。

### `[constexpr noexcept, since 6.8] qsizetype QUtf8StringView::max_size() const`

**作用与语义：**

此功能是为了STL兼容性而提供。
退货 `maxSize()`。

### `[noexcept] QUtf8StringView::const_reverse_iterator QUtf8StringView::rbegin() const`

**作用与语义：**

返回一个const STL风格的反向迭代器，指向字符串视图中的第一个码点，顺序相反。
此功能是为了STL兼容性而提供。

### `[noexcept] QUtf8StringView::const_reverse_iterator QUtf8StringView::rend() const`

**作用与语义：**

返回一个STL风格的反向迭代器，指向字符串视图中最后一个代码点之后的迭代器，顺序相反。
此功能是为了STL兼容性而提供。

### `[constexpr noexcept] qsizetype QUtf8StringView::size() const`

**作用与语义：**

返回该字符串视图的大小，以UTF-8码点表示（即多字节序列在本函数中被视为多个，与`QString`和`QStringView`中的代理对相同）。

### `[constexpr, since 6.8] QUtf8StringView &QUtf8StringView::slice(qsizetype pos, qsizetype n)`

**作用与语义：**

修改字符串视图，从位置`pos`开始，扩展到`n`码点。
注意：当`pos` <0、`n` <0或`pos` `n` > `size()`时，行为未定义。

### `[constexpr, since 6.8] QUtf8StringView &QUtf8StringView::slice(qsizetype pos)`

**作用与语义：**

修改该字符串视图，从位置`pos`开始，延伸至末端。
注意：当`pos` <0或`pos` > `size()`时，行为未定义。

### `[constexpr] QUtf8StringView QUtf8StringView::sliced(qsizetype pos) const`

**作用与语义：**

返回一个从本对象中位置 `pos` 开始并延伸到其末尾的字符串视图。
注意：当 `pos` < 0 或 `pos` > `size()` 时，行为未定义。

### `[constexpr] QUtf8StringView QUtf8StringView::sliced(qsizetype pos, qsizetype n) const`

**作用与语义：**

返回一个字符串视图，该视图包含此字符串视图的 `n` 码点，从位置 `pos` 开始。
注意：当 `pos` < 0、`n` < 0 或 `pos`   `n` > `size()` 时，行为未定义。

### `QString QUtf8StringView::toString() const`

**作用与语义：**

返回该字符串视图数据的深度副本作为`QString`。
返回值为空值`QString`当且仅当该字符串视图为空。

### `[constexpr] void QUtf8StringView::truncate(qsizetype n)`

**作用与语义：**

将字符串视图截断为`n`码点。
和`*this = first(n)`一样。
注意：当`n` <0或`n` > `size()`时，行为未定义。

### `[noexcept] const char8_t *QUtf8StringView::utf8() const`

**作用与语义：**

返回字符串视图中第一个代码点的const指针。
结果以`const char8_t*`返回，因此该函数仅在 C 20 模式下编译时可用。
注意：返回值所表示的字符数组并非空终止。

### `[noexcept, since 6.7] QUtf8StringView::operator std::string_view() const`

**作用与语义：**

将该`QUtf8StringView`对象转换为`std::string_view`对象。返回的视图将拥有与该视图相同的数据指针和长度。

### `[noexcept, since 6.10] QUtf8StringView::operator std::u8string_view() const`

**作用与语义：**

将该`QUtf8StringView`对象转换为`std::u8string_view`对象。返回的视图将拥有与该视图相同的数据指针和长度。
该功能仅在 C 20 编译时可用。

### `[constexpr] QUtf8StringView::storage_type QUtf8StringView::operator[](qsizetype n) const`

**作用与语义：**

返回此字符串视图中位置 `n` 的码点。
如果 `n` 为负数或不小于 `size()`，行为未定义。

### `const_iterator`

**作用与语义：**

该typedef为`QUtf8StringView`提供了一个STL风格的const迭代器。

### `const_pointer`

**作用与语义：**

`value_type *`的别名。为兼容STL提供。

### `const_reference`

**作用与语义：**

`value_type &`的别名。为兼容STL提供。

### `const_reverse_iterator`

**作用与语义：**

该typedef为`QUtf8StringView`提供了一个STL风格的const反迭代器。

### `difference_type`

**作用与语义：**

`std::ptrdiff_t`的别名。为兼容STL而提供。

### `iterator`

**作用与语义：**

该typedef为`QUtf8StringView`提供了一个STL风格的const迭代器。
`QUtf8StringView`不支持可变迭代器，所以这和`const_iterator`是一样的。

### `pointer`

**作用与语义：**

`value_type *`的别名。为兼容STL提供。
`QUtf8StringView`不支持可变指针，所以这和`const_pointer`一样。

### `reference`

**作用与语义：**

`value_type &`的别名。为兼容STL提供。
`QUtf8StringView`不支持可变引用，所以这和`const_reference`一样。

### `reverse_iterator`

**作用与语义：**

该typedef为`QUtf8StringView`提供了一个STL风格的const反迭代器。
`QUtf8StringView`不支持可变的反迭代器，所以这和`const_reverse_iterator`是一样的。

### `size_type`

**作用与语义：**

qsizetype 的别名。为兼容 STL 提供。

### `storage_type`

**作用与语义：**

`char`的别名。

### `value_type`

**作用与语义：**

`const char`的别名。为兼容STL而提供。

### `(since 6.5) int compare(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

将该字符串视图与 `str` 比较，若字符串视图小于 `str` 则返回负整数;大于 `str` 则返回正整数;相等时返回零。
如果`cs`是`Qt::CaseSensitive`（默认），则比较区分大小写;否则比较不区分大小写。

### `(since 6.5) int compare(QUtf8StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

将该字符串视图与 `str` 比较，若字符串视图小于 `str` 则返回负整数;大于 `str` 则返回正整数;相等时返回零。
如果`cs`是`Qt::CaseSensitive`（默认），则比较区分大小写;否则比较不区分大小写。

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

`QUtf8StringView` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
