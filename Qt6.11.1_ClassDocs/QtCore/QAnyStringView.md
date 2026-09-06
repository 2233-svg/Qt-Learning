# QAnyStringView

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QAnyStringView` 是 Qt 的值类型，围绕“AnyString视图”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QAnyStringView` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QAnyStringView>`
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

- `difference_type`
- `size_type`

### 公有函数

- `QAnyStringView()`
- `QAnyStringView(const Char &ch)`
- `QAnyStringView(const Char (&)[N] string)`
- `QAnyStringView(const Char *str)`
- `QAnyStringView(const Container &str)`
- `QAnyStringView(const QByteArray &str)`
- `QAnyStringView(const QString &str)`
- `QAnyStringView(std::nullptr_t)`
- `QAnyStringView(const Char *first, const Char *last)`
- `QAnyStringView(const Char *str, qsizetype len)`
- `(since 6.9) QString arg(Args &&... args) const`
- `QChar back() const`
- `(since 6.5) void chop(qsizetype n)`
- `(since 6.5) QAnyStringView chopped(qsizetype n) const`
- `const void * data() const`
- `bool empty() const`
- `(since 6.5) QAnyStringView first(qsizetype n) const`
- `QChar front() const`
- `bool isEmpty() const`
- `bool isNull() const`
- `(since 6.5) QAnyStringView last(qsizetype n) const`
- `qsizetype length() const`
- `(since 6.8) qsizetype max_size() const`
- `qsizetype size() const`
- `qsizetype size_bytes() const`
- `(since 6.8) QAnyStringView & slice(qsizetype pos, qsizetype n)`
- `(since 6.8) QAnyStringView & slice(qsizetype pos)`
- `(since 6.5) QAnyStringView sliced(qsizetype pos) const`
- `(since 6.5) QAnyStringView sliced(qsizetype pos, qsizetype n) const`
- `QString toString() const`
- `(since 6.5) void truncate(qsizetype n)`
- `decltype(auto) visit(Visitor &&v) const`

### 静态公有成员

- `int compare(QAnyStringView lhs, QAnyStringView rhs, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QAnyStringView fromArray(const Char (&)[Size] string)`

### 相关非成员函数

- `bool operator!=(const QAnyStringView &lhs, const QAnyStringView &rhs)`
- `bool operator<(const QAnyStringView &lhs, const QAnyStringView &rhs)`
- `(since 6.7) QDebug operator<<(QDebug d, QAnyStringView s)`
- `bool operator<=(const QAnyStringView &lhs, const QAnyStringView &rhs)`
- `bool operator==(const QAnyStringView &lhs, const QAnyStringView &rhs)`
- `bool operator>(const QAnyStringView &lhs, const QAnyStringView &rhs)`
- `bool operator>=(const QAnyStringView &lhs, const QAnyStringView &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QAnyStringView::difference_type`

**作用与语义：**

`std::ptrdiff_t`的别名。为兼容STL而提供。

### `QAnyStringView::size_type`

**作用与语义：**

qsizetype 的别名。为兼容 STL 提供。

### `[constexpr noexcept] QAnyStringView::QAnyStringView()`

**作用与语义：**

构造一个空字符串视图。

### `[constexpr noexcept] template <typename Char, QAnyStringView::if_compatible_char<Char> = true> QAnyStringView::QAnyStringView(const Char &ch)`

**作用与语义：**

在单个字符的字符串视图上构造一个字符串视图`ch`。长度通常为`1`（但见下文）。
一般来说，你必须假设这样创建的QAnyStringView会在完整表达式结束时开始引用过时数据，当临时表达式被删除时。这意味着用它传递一个字符给QAnyStringView取用函数是可以且安全的（只要函数文档不要求超过初始调用的生命周期）：
但让物体停留更久是未定义的行为：
如果你需要这个，更倾向于。
上述内容适用于所有直接支持的兼容字符类型。
如果 `ch` 不是这些类型之一，只是转换为 `QChar`，例如 `QChar::SpecialCharacter` 或 `QLatin1Char`，QAnyStringView 会绑定到一个临时对象，该对象在完整表达式结束时已被删除，就像第二个例子中一样。
如果`ch`无法用单一的UTF-16码单元表示（例如因为它是`char32_t`值），该构造器会将`ch`分解成两个UFT-16码单元。此时生成的QAnyStringView将有`2`的`size()`，且存储分解的临时缓冲区在完整表达式结束时被删除，类似于。
在这种情况下，对应的安全版本是。

**官方示例：**

```cpp
 int to_int(QAnyStringView);
 int res = to_int(u'9'); // OK, data stays around for the duration of the call
```

### `[constexpr noexcept] template <typename Char, size_t N> QAnyStringView::QAnyStringView(const Char (&)[N] string)`

**作用与语义：**

在字符字符串的字面 `string` 上构造字符串视图。视图覆盖数组，直到遇到第一个`Char(0)`，或`N`，以先到者为准。如果你需要完整数组，可以用 `fromArray()`。
`string`必须在该字符串视图对象的生命周期内保持有效。
仅当 是实际数组且 是兼容的字符类型时`string`才参与超载解析`Char`。

### `[constexpr noexcept] template <typename Char> QAnyStringView::QAnyStringView(const Char *str)`

**作用与语义：**

在`str`上构建字符串视图。长度通过扫描第一个`Char(0)`确定。
`str`必须在该字符串视图对象的生命周期内保持有效。
将`nullptr`传递为`str`是安全的，且会得到无字符串视图。
仅当 `str` 不是数组且 `Char` 是兼容的字符类型时，才参与超载解析。

### `[constexpr noexcept] template <typename Container, QAnyStringView::if_compatible_container<Container> = true> QAnyStringView::QAnyStringView(const Container &str)`

**作用与语义：**

在`str`上构造字符串视图。长度取自`std::size(str)`。
`std::data(str)`必须在这个字符串视图对象的生命周期内保持有效。
字符串视图为空，当且仅当 `std::size(str) == 0`。尚不确定该构造函数是否能生成空字符串视图（`std::data(str)`需返回`nullptr`）。
仅当`Container`容器具有兼容的字符类型时，才参与重载决议`value_type`。

### `[noexcept] QAnyStringView::QAnyStringView(const QByteArray &str)`

**作用与语义：**

在`str`上构建字符串视图。`str`中的数据被解释为UTF-8。
`str.data()`必须在该字符串视图对象的生命周期内保持有效。
字符串视图当且仅当 `str.isNull()` 时才为空。

### `[noexcept] QAnyStringView::QAnyStringView(const QString &str)`

**作用与语义：**

在`str`上构建字符串视图。
`str.data()`必须在该字符串视图对象的生命周期内保持有效。
字符串视图当且仅当 `str.isNull()` 时才为空。

### `[constexpr noexcept] QAnyStringView::QAnyStringView(std::nullptr_t)`

**作用与语义：**

构造一个空字符串视图。

### `[constexpr] template <typename Char, QAnyStringView::if_compatible_char<Char> = true> QAnyStringView::QAnyStringView(const Char *first, const Char *last)`

**作用与语义：**

在 `first` 上构造一个长度为 (`last` - `first`) 的字符串视图。
`[first,last)` 的范围在该字符串视图对象的生命周期内必须保持有效。
如果 `last` 也是 `nullptr`，则将 `nullptr` 作为 `first` 传递是安全的，并且会产生一个空的字符串视图。
如果 `last` 早于 `first`，或者 `first` 是 `nullptr` 而 `last` 不是，则行为未定义。
仅当 `Char` 是兼容的字符类型时，才参与重载决议。

### `[constexpr] template <typename Char, QAnyStringView::if_compatible_char<Char> = true> QAnyStringView::QAnyStringView(const Char *str, qsizetype len)`

**作用与语义：**

在 `str` 上构造一个长度为 `len` 的字符串视图。`[str,len)` 范围在此字符串视图对象的整个生命周期内必须保持有效。如果 `len` 也为 0，则将 `nullptr` 作为 `str` 传递是安全的，并将导致一个空字符串视图。如果 `len` 为负数，或者为正数且 `str` 为 `nullptr`，则行为未定义。仅当 `Char` 是兼容字符类型时，才参与重载决议。

### `[since 6.9] template <typename... Args> QString QAnyStringView::arg(Args &&... args) const`

**作用与语义：**

用对应的`args`参数替换该字符串中`%N`的出现。这些参数不是位置论元：`args`中的第一个用最低的`N`替换`%N`（全部），第二个用`args`的`%N`替换下一个最低的`N`，依此类推。
`Args`可以包含任何隐含地转化为`QAnyStringView`的内容。

### `[constexpr] QChar QAnyStringView::back() const`

**作用与语义：**

返回字符串视图中的最后一个字符。
此功能是为了STL兼容性而提供。
警告：在空字符串视图上调用该函数构成未定义行为。

### `[constexpr, since 6.5] void QAnyStringView::chop(qsizetype n)`

**作用与语义：**

将字符串视图截断为`n`码点。
和`*this = first(size() - n)`一样。
注意：当`n` <0或`n` > `size()`时，行为未定义。

### `[constexpr, since 6.5] QAnyStringView QAnyStringView::chopped(qsizetype n) const`

**作用与语义：**

返回长度为`size()` - `n`的子串，从该对象的开头开始。
和`first(size() - n)`一样。
注意：当`n` <0或`n` > `size()`时，行为未定义。

### `[static noexcept] int QAnyStringView::compare(QAnyStringView lhs, QAnyStringView rhs, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

比较弦视图`lhs`与弦视图`rhs`，如果`lhs`小于`rhs`，返回负整数;如果大于`rhs`，则返回正整数;相等则返回零。
如果`cs`是`Qt::CaseSensitive`（默认），则比较区分大小写;否则比较不区分大小写。

### `[constexpr noexcept] const void *QAnyStringView::data() const`

**作用与语义：**

返回字符串视图中第一个字符的const指针。
注意：返回值所表示的字符数组并非空终止。

### `[constexpr noexcept] bool QAnyStringView::empty() const`

**作用与语义：**

返回该字符串视图是否为空——即是否`size() == 0`。
此功能是为了STL兼容性而提供。

### `[constexpr, since 6.5] QAnyStringView QAnyStringView::first(qsizetype n) const`

**作用与语义：**

返回一个字符串视图，该视图包含此字符串视图的前 `n` 个代码点。
注意：当 `n` < 0 或 `n` > `size()` 时，行为未定义。

### `[static constexpr noexcept] template < typename Char, size_t Size, QAnyStringView::if_compatible_char<Char> = true > QAnyStringView QAnyStringView::fromArray(const Char (&)[Size] string)`

**作用与语义：**

在完整的字符字符串文字 `string` 上构建字符串视图，包括任何尾`Char(0)`。如果你不想在视图中包含空终止符，那么确定它在最后时可以`chop()`它。或者你也可以使用构造函数重载，取一个数组文字，创建一个视图直到数据中第一个空终止符，但不包括它。
`string`必须在该字符串视图对象的生命周期内保持有效。
如果 `Char` 是兼容的字符类型，该函数可对任意数组文字工作。兼容的字符类型包括：`QChar`、`ushort`、`char16_t` 以及（在 Windows 等平台上，它是 16 位类型）`wchar_t`。

### `[constexpr] QChar QAnyStringView::front() const`

**作用与语义：**

返回字符串视图中的第一个字符。
此功能是为了STL兼容性而提供。
警告：在空字符串视图上调用该函数构成未定义行为。

### `[constexpr noexcept] bool QAnyStringView::isEmpty() const`

**作用与语义：**

返回该字符串视图是否为空——即是否`size() == 0`。
此功能是为了与其他 Qt 容器的兼容性而提供。

### `[constexpr noexcept] bool QAnyStringView::isNull() const`

**作用与语义：**

返回该字符串视图是否为空——即是否`data() == nullptr`。
这些功能是为了与其他 Qt 容器的兼容性而提供。

### `[constexpr, since 6.5] QAnyStringView QAnyStringView::last(qsizetype n) const`

**作用与语义：**

返回一个字符串视图，该视图包含此字符串视图的最后 `n` 个代码点。
注意：当 `n` < 0 或 `n` > `size()` 时，行为未定义。

### `[constexpr noexcept] qsizetype QAnyStringView::length() const`

**作用与语义：**

和`size()`一样。
此功能是为了与其他 Qt 容器的兼容性而提供。

### `[constexpr noexcept, since 6.8] qsizetype QAnyStringView::max_size() const`

**作用与语义：**

此功能是为了STL兼容性而提供。
它返回字符串视图理论上能表示的最大元素数。实际上，这个数量可以更小，受限于系统可用的内存容量。
注意：返回的值是基于当前使用的字符类型计算的，因此在两个不同视图上调用该函数可能会返回不同的结果。

### `[constexpr noexcept] qsizetype QAnyStringView::size() const`

**作用与语义：**

返回该字符串视图的大小，包含编码的码点。

### `[constexpr noexcept] qsizetype QAnyStringView::size_bytes() const`

**作用与语义：**

返回该字符串视图的大小，但以字节为单位，而非代码点。
你可以将该函数与`data()`一起使用进行哈希或序列化。
此功能是为了STL兼容性而提供。

### `[constexpr, since 6.8] QAnyStringView &QAnyStringView::slice(qsizetype pos, qsizetype n)`

**作用与语义：**

修改字符串视图，从位置`pos`开始，扩展到`n`码点。
注意：当`pos` <0、`n` <0或`pos` `n` > `size()`时，行为未定义。

### `[constexpr, since 6.8] QAnyStringView &QAnyStringView::slice(qsizetype pos)`

**作用与语义：**

修改该字符串视图，从位置`pos`开始，延伸至末端。
注意：当`pos` <0或`pos` > `size()`时，行为未定义。

### `[constexpr, since 6.5] QAnyStringView QAnyStringView::sliced(qsizetype pos) const`

**作用与语义：**

返回一个从本对象中位置 `pos` 开始并延伸到其末尾的字符串视图。
注意：当 `pos` < 0 或 `pos` > `size()` 时，行为未定义。

### `[constexpr, since 6.5] QAnyStringView QAnyStringView::sliced(qsizetype pos, qsizetype n) const`

**作用与语义：**

返回一个字符串视图，该视图包含此字符串视图的 `n` 码点，从位置 `pos` 开始。
注意：当 `pos` < 0、`n` < 0 或 `pos`   `n` > `size()` 时，行为未定义。

### `QString QAnyStringView::toString() const`

**作用与语义：**

返回该字符串视图数据的深度副本作为`QString`。
返回值为空值`QString`当且仅当该字符串视图为空。

### `[constexpr, since 6.5] void QAnyStringView::truncate(qsizetype n)`

**作用与语义：**

将字符串视图截断为`n`码点。
和`*this = first(n)`一样。
注意：当`n` <0或`n` > `size()`时，行为未定义。

### `[constexpr] template <typename Visitor> decltype(auto) QAnyStringView::visit(Visitor &&v) const`

**作用与语义：**

调用`v`使用`QUtf8StringView`、`QLatin1String`或`QStringView`，具体取决于该字符串视图所引用的字符串数据编码方式。
大多数取`QAnyStringView`函数分叉成每个编码函数的方式如下：
这里，我们重复使用了相同的名称 `s`，既用于`QAnyStringView`对象，也用于 lambda 参数。这是一种习用法代码，通过 visit() 调用帮助追踪对象的身份，例如在更复杂的情境中。
Visit() 要求所有 lambda 实例具有相同的返回类型。如果它们不同，即使存在共同类型，编译时也会有错误。为了解决这个问题，你可以在 lambda 上使用显式返回类型，或者在返回语句中 cast ：

**官方示例：**

```cpp
 void processImpl(QLatin1String s) { ~~~ }
 void processImpl(QUtf8StringView s) { ~~~ }
 void processImpl(QStringView s) { ~~~ }

 void process(QAnyStringView s)
 {
     s.visit([](auto s) { processImpl(s); });
 }
```

### `[since 6.7] QDebug operator<<(QDebug d, QAnyStringView s)`

**作用与语义：**

输出`s`调试流`d`。
如果`d.quotedString()` `true`，表示字符串属于哪种编码方式。如果你只想要字符串数据，可以用这样的方式`visit()`：

**官方示例：**

```cpp
 s.visit([&d) (auto s) { d << s; });
```

### `[noexcept] bool operator>(const QAnyStringView &lhs, const QAnyStringView &rhs)`

**作用与语义：**

比较 `lhs` 和 `rhs` 的操作符。

### `difference_type`

**作用与语义：**

`std::ptrdiff_t`的别名。为兼容STL而提供。

### `size_type`

**作用与语义：**

qsizetype 的别名。为兼容 STL 提供。

### `bool operator!=(const QAnyStringView &lhs, const QAnyStringView &rhs)`

**作用与语义：**

比较 `lhs` 和 `rhs` 的操作符。

### `bool operator<(const QAnyStringView &lhs, const QAnyStringView &rhs)`

**作用与语义：**

比较 `lhs` 和 `rhs` 的操作符。

### `bool operator<=(const QAnyStringView &lhs, const QAnyStringView &rhs)`

**作用与语义：**

比较 `lhs` 和 `rhs` 的操作符。

### `bool operator==(const QAnyStringView &lhs, const QAnyStringView &rhs)`

**作用与语义：**

比较 `lhs` 和 `rhs` 的操作符。

### `bool operator>=(const QAnyStringView &lhs, const QAnyStringView &rhs)`

**作用与语义：**

比较 `lhs` 和 `rhs` 的操作符。

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

`QAnyStringView` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
