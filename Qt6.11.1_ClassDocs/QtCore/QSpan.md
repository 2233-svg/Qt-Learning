# QSpan

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Span”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSpan` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QSpan>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `const_iterator`
- `const_pointer`
- `const_reference`
- `const_reverse_iterator`
- `difference_type`
- `element_type`
- `iterator`
- `pointer`
- `reference`
- `reverse_iterator`
- `size_type`
- `value_type`

### 公有函数

- `QSpan()`
- `QSpan(QSpan<S, N> other)`
- `QSpan(Range &&r)`
- `QSpan(const std::array<S, N> &arr)`
- `QSpan(q20::type_identity_t<T> (&)[N] arr)`
- `QSpan(std::array<S, N> &arr)`
- `QSpan(std::initializer_list<QSpan<T, E>::value_type> il)`
- `QSpan(std::span<S, N> other)`
- `QSpan(It first, It last)`
- `QSpan(It first, qsizetype count)`
- `QSpan(const QSpan<T, E> &other)`
- `QSpan(QSpan<T, E> &&other)`
- `~QSpan()`
- `auto back() const`
- `auto begin() const`
- `auto cbegin() const`
- `auto cend() const`
- `(since 6.9) void chop(QSpan<T, E>::size_type n)`
- `(since 6.9) auto chopped(QSpan<T, E>::size_type n) const`
- `auto crbegin() const`
- `auto crend() const`
- `auto data() const`
- `auto empty() const`
- `auto end() const`
- `auto first() const`
- `auto first(QSpan<T, E>::size_type n) const`
- `auto front() const`
- `auto isEmpty() const`
- `auto last() const`
- `auto last(QSpan<T, E>::size_type n) const`
- `auto rbegin() const`
- `auto rend() const`
- `auto size() const`
- `auto size_bytes() const`
- `(since 6.9) void slice(QSpan<T, E>::size_type pos)`
- `(since 6.9) void slice(QSpan<T, E>::size_type pos, QSpan<T, E>::size_type n)`
- `auto sliced(QSpan<T, E>::size_type pos) const`
- `auto sliced(QSpan<T, E>::size_type pos, QSpan<T, E>::size_type n) const`
- `auto subspan() const`
- `auto subspan(QSpan<T, E>::size_type pos) const`
- `auto subspan(QSpan<T, E>::size_type pos, QSpan<T, E>::size_type n) const`
- `QSpan<T, E> & operator=(QSpan<T, E> &&other)`
- `QSpan<T, E> & operator=(const QSpan<T, E> &other)`
- `QSpan<T, E>::reference operator[](QSpan<T, E>::size_type idx) const`

### 相关非成员函数

- `(since 6.8) auto as_bytes(QSpan<T, E> s)`
- `(since 6.8) auto as_writable_bytes(QSpan<T, E> s)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QSpan::const_iterator`

**作用与语义：**

分别是`const T*`和`const_pointer`的别名。

### `[alias] QSpan::const_pointer`

**作用与语义：**

分别是`const T*`和`const element_type*`的别名。
该别名是为了与STL兼容而提供。

### `[alias] QSpan::const_reference`

**作用与语义：**

分别是`const T&`和`const element_type&`的别名。
该别名是为了与STL兼容而提供。

### `[alias] QSpan::const_reverse_iterator`

**作用与语义：**

`std::reverse_iterator<const_iterator>`的化名。

### `[alias] QSpan::difference_type`

**作用与语义：**

qptrdiff的别名。这与`std::span`不同。
该别名是为了与STL兼容而提供。

### `[alias] QSpan::element_type`

**作用与语义：**

`T`的别名。包括有的话`const`。
该别名是为了与STL兼容而提供。

### `[alias] QSpan::iterator`

**作用与语义：**

分别是`T*`和`pointer`的别名。包括`const`（如果有的话）。

### `[alias] QSpan::pointer`

**作用与语义：**

分别是`T*`和`element_type*`的别名。包括`const`（如果有的话）。
该别名是为了与STL兼容而提供。

### `[alias] QSpan::reference`

**作用与语义：**

分别是`T&`和`element_type&`的别名。包括有的话`const`。
该别名是为了与STL兼容而提供。

### `[alias] QSpan::reverse_iterator`

**作用与语义：**

`std::reverse_iterator<iterator>`的别名。包括`const`，如果有的话。

### `[alias] QSpan::size_type`

**作用与语义：**

qsizetype 的别名。这与 `std::span` 不同。
该别名是为了与STL兼容而提供。

### `[alias] QSpan::value_type`

**作用与语义：**

`T`的别名。排除`const`，如果有的话。
该别名是为了与STL兼容而提供。

### `[default] QSpan::QSpan()`

**作用与语义：**

默认构造者。
该构造器仅在`E`为零（0）或`std::dynamic_extent`时存在。换句话说：只有固定零大小或可变大小的张成是默认可构造的。

### `[constexpr noexcept] template < typename S, size_t N, QSpan<T, E>::if_qualification_conversion<S> = true > QSpan::QSpan(std::span<S, N> other)`

**作用与语义：**

构建一个引用所提供跨度数据的`QSpan` `other`。
仅当。
- `N`或`extent`为`std::dynamic_extent`或`extent` `==` `N`
- `S` 或 `const S` 与 `T` 相同。

### `[constexpr] template <typename Range, QSpan<T, E>::if_compatible_range<Range> = true> QSpan::QSpan(Range &&r)`

**作用与语义：**

构建一个引用所提供跨度数据的`QSpan` `other`。
仅当。
- `N`或`extent`为`std::dynamic_extent`或`extent` `==` `N`
- `S` 或 `const S` 与 `T` 相同。

### `[constexpr noexcept] template < typename S, size_t N, QSpan<T, E>::if_qualification_conversion<S> = true > QSpan::QSpan(const std::array<S, N> &arr)`

**作用与语义：**

构建一个QSpan，引用所提供范围`r`的数据。
仅当`Range`与该范围兼容时，才参与重载决议。

### `[constexpr] QSpan::QSpan(std::initializer_list<QSpan<T, E>::value_type> il)`

**作用与语义：**

构建一个引用所提供数组数据的`QSpan` `arr`。
注意：`q20::type_identity_t`是C 20 `std::type_identity_t`的C 17反向移植。
仅当。
- `N`或`extent`要么`std::dynamic_extent`，要么`extent` `==` `N`
- `S` 或 `const S` 与 `T` 相同。

### `[constexpr] template <typename It, QSpan<T, E>::if_compatible_iterator<It> = true> QSpan::QSpan(It first, It last)`

**作用与语义：**

构建一个引用所提供数组数据的`QSpan` `arr`。
注意：`q20::type_identity_t`是C 20 `std::type_identity_t`的C 17反向移植。
仅当。
- `N`或`extent`要么`std::dynamic_extent`，要么`extent` `==` `N`
- `S` 或 `const S` 与 `T` 相同。

### `[constexpr] template <typename It, QSpan<T, E>::if_compatible_iterator<It> = true> QSpan::QSpan(It first, qsizetype count)`

**作用与语义：**

构建一个引用所提供数组数据的`QSpan` `arr`。
注意：`q20::type_identity_t`是C 20 `std::type_identity_t`的C 17反向移植。
仅当。
- `N`或`extent`要么`std::dynamic_extent`，要么`extent` `==` `N`
- `S` 或 `const S` 与 `T` 相同。

### `[default] QSpan::~QSpan()`

**作用与语义：**

这些特殊成员函数是隐式定义的。
注意：移动等同于复制。只有 `data()` 和 `size()` 从 span 到 span 进行复制，而不是引用的数据。

### `[constexpr] auto QSpan::back() const`

**作用与语义：**

返回对该区间最后一个元素的引用。
该跨度不能为空，否则行为未定义。

### `[constexpr noexcept] auto QSpan::begin() const`

**作用与语义：**

返回指向跨间起点的中介器。
因为`QSpan`迭代器只是指针，这和调用`data()`是一样的。

### `[constexpr noexcept] auto QSpan::cbegin() const`

**作用与语义：**

返回指向跨度起点的`const_iterator`。
即使`T`未`const`，这也会返回只读的迭代器：

**官方示例：**

```cpp
 QSpan<int> span = ~~~;
 *span.begin() = 42; // OK
 *span.cbegin() = 42; // ERROR: cannot assign through a const_iterator
```

### `[constexpr noexcept] auto QSpan::cend() const`

**作用与语义：**

返回指向跨距末端之外的`const_iterator`。

### `[constexpr, since 6.9] void QSpan::chop(QSpan<T, E>::size_type n)`

**作用与语义：**

和`*this = chopped(``n``)`一样。
该函数仅适用于可变大小的跨度。

### `[constexpr, since 6.9] auto QSpan::chopped(QSpan<T, E>::size_type n) const`

**作用与语义：**

返回一个大小为`size()`的`variable-sized`跨——`n`引用了该跨度的第一个`size()`——`n`该跨度的元素。
和`first(size() - n)`一样。
`n`必须是非负的。
该张成至少包含`n`个元素（`E` >= `n` 和 `size()` >= `n`），否则行为未定义。

### `[constexpr noexcept] auto QSpan::crbegin() const`

**作用与语义：**

返回指向反转跨距起点的`const_reverse_iterator`。

### `[constexpr noexcept] auto QSpan::crend() const`

**作用与语义：**

返回指向反转跨距结束后1的`const_reverse_iterator`。

### `[constexpr noexcept] auto QSpan::data() const`

**作用与语义：**

返回指向跨度起点的指针。
就像打电话`begin()`一样。

### `[constexpr noexcept] auto QSpan::isEmpty() const`

**作用与语义：**

返回跨度是否空，即是否`size() == 0`。
这些函数的作用是一样的：`empty()`用于STL兼容性，`isEmpty()`用于Qt兼容性。

### `[constexpr noexcept] auto QSpan::end() const`

**作用与语义：**

返回一个迭代器，指向跨度末端之外的迭代器。
因为`QSpan`迭代器只是指针，这就像调用`data() + size()`一样。

### `[constexpr noexcept(...)] template <std::size_t Count> auto QSpan::first() const`

**作用与语义：**

返回一个`fixed-sized`的跨度，`Count`引用`*this`的前`Count`元素。
张成必须至少包含`Count`个元素（`E` >= `Count` 和 `size()` >= `Count`），否则行为未定义。
注意：该函数只有在`subspan_always_succeeds_v<Count>` `true`时才适用。

### `[constexpr] auto QSpan::first(QSpan<T, E>::size_type n) const`

**作用与语义：**

返回一个`variable-sized`的跨度，`n`引用`*this`的前`n`元素。
`n`必须是非负的。
张成必须至少包含`n`个元素（`E` >= `n` 和 `size()` >= `n`），否则行为未定义。

### `[constexpr] auto QSpan::front() const`

**作用与语义：**

返回对该张成中第一个元素的引用。
该跨度不能为空，否则行为未定义。

### `[constexpr noexcept(...)] template <std::size_t Count> auto QSpan::last() const`

**作用与语义：**

返回一个`fixed-sized`的跨度，大小为`Count`引用`*this`最后`Count`元素。
张成必须至少包含`Count`个元素（`E` >= `Count` 和 `size()` >= `Count`），否则行为未定义。
注意：该功能仅在`subspan_always_succeeds_v<Count>` `true`时才适用。

### `[constexpr] auto QSpan::last(QSpan<T, E>::size_type n) const`

**作用与语义：**

返回一个`variable-sized`的跨度，大小为`n`引用`*this`最后`n`元素。
`n`必须是非负的。
张成必须至少包含`n`个元素（`E` >= `n` 和 `size()` >= `n`），否则行为未定义。

### `[constexpr noexcept] auto QSpan::rbegin() const`

**作用与语义：**

返回指向反转跨距起点的`reverse_iterator`。

### `[constexpr noexcept] auto QSpan::rend() const`

**作用与语义：**

返回指向反转跨距末端之外的`reverse_iterator`。

### `[constexpr noexcept] auto QSpan::size() const`

**作用与语义：**

返回张成大小，即它引用的元素数。

### `[constexpr noexcept] auto QSpan::size_bytes() const`

**作用与语义：**

返回该区域间的大小（字节单位），即元素数乘以`sizeof(T)`。

### `[constexpr, since 6.9] void QSpan::slice(QSpan<T, E>::size_type pos)`

**作用与语义：**

和`*this = sliced(``pos``)`一样。
该函数仅适用于可变大小的跨度。

### `[constexpr, since 6.9] void QSpan::slice(QSpan<T, E>::size_type pos, QSpan<T, E>::size_type n)`

**作用与语义：**

和`*this = sliced(``pos``,``n``)`一样。
该函数仅适用于可变大小的跨度。

### `[constexpr noexcept(...)] template <std::size_t Offset, std::size_t Count> auto QSpan::subspan() const`

**作用与语义：**

返回一个大小为 的跨度`Count`引用该跨度的 从 `Offset` 开始的 `Count` 元素。
如果`*this`是一个可变大小的张成，则返回类型是可变大小的张成，否则是固定大小的张成。
该张成必须至少包含`Offset + Count`个元素（`E` >= `Offset + Count` 和 `size()` >= `Offset + Count`），否则行为未定义。
注意：该功能仅在`subspan_always_succeeds_v<Offset + Count>`为`true`时使用。

### `[constexpr noexcept(...)] template <std::size_t Offset> auto QSpan::subspan() const`

**作用与语义：**

在去除前`Offset`元素后，返回一个大小为 `E - Offset` 的跨度。
如果`*this`是可变大小的张成，则返回类型是可变大小的张成，否则是固定大小的张成。
该张成必须至少包含`Offset`个元素（`E` >= `Offset` 和 `size()` >= `Offset`），否则行为未定义。
注意：该功能仅在`subspan_always_succeeds_v<Offset>`为`true`时使用。

### `[constexpr] auto QSpan::sliced(QSpan<T, E>::size_type pos) const`

**作用与语义：**

在去除前`pos`元素后，返回一个大小为 `variable-sized` 的跨度，`size() - pos`引用该跨度的剩余部分。
`pos`必须是非负的。
该张成必须至少包含`pos`个元素（`E` >= `pos` 和 `size()` >= `pos`），否则行为未定义。
这些函数的作用相同：`subspan()`用于STL兼容性，`sliced()`用于量子态兼容性。

### `[constexpr] auto QSpan::sliced(QSpan<T, E>::size_type pos, QSpan<T, E>::size_type n) const`

**作用与语义：**

返回一个`variable-sized`的张幅，`n`引用该跨度的`n`元素，从`pos`开始。
`pos`和`n`都必须是非负的。
该张成必须至少包含`pos + n`个元素（`E` >= `pos + n` 和 `size()` >= `pos + n`），否则行为未定义。
这些函数的作用是一样的：`subspan()`用于STL兼容性，`sliced()`用于量子体兼容性。

### `[constexpr] QSpan<T, E>::reference QSpan::operator[](QSpan<T, E>::size_type idx) const`

**作用与语义：**

返回张成中索引`idx`的元素的引用。
指标必须在范围内，即 `idx` >= 0 且 `idx` < `size()`，否则行为未定义。

### `const std::size_t QSpan::extent`

**作用与语义：**

`QSpan<T, E>`的第二个模板参数，即`E`。这对可变大小的张成是`std::dynamic_extent`的。
注意：虽然`QSpan`中的所有其他大小和索引都使用qsizetype，但该变量和`E`一样，实际上属于`size_t`类型，以保证与`std::span`和`std::dynamic_extent`的兼容性。

### `[noexcept, since 6.8] auto as_bytes(QSpan<T, E> s)`

**作用与语义：**

返回`s`为`size()`等于`s.size_bytes()`的`QSpan<const std::byte, E'>`。
如果`E` `std::dynamic_extent`，那么`E'`也是。否则，`E' = E * sizeof(T)`。
注意：`q20::dynamic_extent`是C 20 `std::dynamic_extent`的C 17回移植版。

### `[noexcept, since 6.8] auto as_writable_bytes(QSpan<T, E> s)`

**作用与语义：**

返回`s`为`size()`等于`s.size_bytes()`的`QSpan<std::byte, E'>`。
如果`E` `std::dynamic_extent`，那么`E'`也是。否则，`E' = E * sizeof(T)`。
注：`q20::dynamic_extent`是C 20 `std::dynamic_extent`的C 17回移植版。
只有在`!std::is_const_v<T>`时才参与超载解决。

### `const_iterator`

**作用与语义：**

分别是`const T*`和`const_pointer`的别名。

### `const_pointer`

**作用与语义：**

分别是`const T*`和`const element_type*`的别名。
该别名是为了与STL兼容而提供。

### `const_reference`

**作用与语义：**

分别是`const T&`和`const element_type&`的别名。
该别名是为了与STL兼容而提供。

### `const_reverse_iterator`

**作用与语义：**

`std::reverse_iterator<const_iterator>`的化名。

### `difference_type`

**作用与语义：**

qptrdiff的别名。这与`std::span`不同。
该别名是为了与STL兼容而提供。

### `element_type`

**作用与语义：**

`T`的别名。包括有的话`const`。
该别名是为了与STL兼容而提供。

### `iterator`

**作用与语义：**

分别是`T*`和`pointer`的别名。包括`const`（如果有的话）。

### `pointer`

**作用与语义：**

分别是`T*`和`element_type*`的别名。包括`const`（如果有的话）。
该别名是为了与STL兼容而提供。

### `reference`

**作用与语义：**

分别是`T&`和`element_type&`的别名。包括有的话`const`。
该别名是为了与STL兼容而提供。

### `reverse_iterator`

**作用与语义：**

`std::reverse_iterator<iterator>`的别名。包括`const`，如果有的话。

### `size_type`

**作用与语义：**

qsizetype 的别名。这与 `std::span` 不同。
该别名是为了与STL兼容而提供。

### `value_type`

**作用与语义：**

`T`的别名。排除`const`，如果有的话。
该别名是为了与STL兼容而提供。

### `QSpan(QSpan<S, N> other)`

**作用与语义：**

构建一个QSpan，引用提供的初始化器列表中的数据`il`。
注意：只有当`E`为`std::dynamic_extent`时，此构造器才`noexcept`。
注意：如果`E`不`std::dynamic_extent`且`il`大小不`E`，行为未定义。
只有当`T`符合`const`资格时，才参与超载解决。

### `QSpan(q20::type_identity_t<T> (&)[N] arr)`

**作用与语义：**

构建一个QSpan，引用从`first`开始且长度为（`last` - `first`）的数据。
`[first, last)`必须是有效的范围。
只有当`It`是兼容的迭代器时，才参与重载决议。

### `QSpan(std::array<S, N> &arr)`

**作用与语义：**

构建一个QSpan，引用从`first`开始且长度为`count`的数据。
`[first, count)`必须是一个有效的范围。
只有当`It`是兼容的迭代子时，才参与重载决议。

### `QSpan(const QSpan<T, E> &other)`

**作用与语义：**

这些特殊成员函数是隐式定义的。
注意：移动等同于复制。只有 `data()` 和 `size()` 从 span 到 span 进行复制，而不是引用的数据。

### `QSpan(QSpan<T, E> &&other)`

**作用与语义：**

这些特殊成员函数是隐式定义的。
注意：移动等同于复制。只有 `data()` 和 `size()` 从 span 到 span 进行复制，而不是引用的数据。

### `auto empty() const`

**作用与语义：**

返回跨度是否空，即是否`size() == 0`。
这些函数的作用是一样的：`empty()`用于STL兼容性，`isEmpty()`用于Qt兼容性。

### `auto subspan(QSpan<T, E>::size_type pos) const`

**作用与语义：**

在去除前`pos`元素后，返回一个大小为 `variable-sized` 的跨度，`size() - pos`引用该跨度的剩余部分。
`pos`必须是非负的。
该张成必须至少包含`pos`个元素（`E` >= `pos` 和 `size()` >= `pos`），否则行为未定义。
这些函数的作用相同：`subspan()`用于STL兼容性，`sliced()`用于量子态兼容性。

### `auto subspan(QSpan<T, E>::size_type pos, QSpan<T, E>::size_type n) const`

**作用与语义：**

返回一个`variable-sized`的张幅，`n`引用该跨度的`n`元素，从`pos`开始。
`pos`和`n`都必须是非负的。
该张成必须至少包含`pos + n`个元素（`E` >= `pos + n` 和 `size()` >= `pos + n`），否则行为未定义。
这些函数的作用是一样的：`subspan()`用于STL兼容性，`sliced()`用于量子体兼容性。

### `QSpan<T, E> & operator=(QSpan<T, E> &&other)`

**作用与语义：**

这些特殊成员函数是隐式定义的。
注意：移动等同于复制。只有 `data()` 和 `size()` 从 span 到 span 进行复制，而不是引用的数据。

### `QSpan<T, E> & operator=(const QSpan<T, E> &other)`

**作用与语义：**

这些特殊成员函数是隐式定义的。
注意：移动等同于复制。只有 `data()` 和 `size()` 从 span 到 span 进行复制，而不是引用的数据。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSpan` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
