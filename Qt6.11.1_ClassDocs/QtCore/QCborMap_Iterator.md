# QCborMap::Iterator

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QCborMap::Iterator` 是容器或范围的迭代器类型，用于按约定遍历元素；重点是有效期、可写性和失效规则。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCborMap::Iterator` 是 迭代器与范围机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 迭代器表示容器或目录遍历中的当前位置，通常通过 begin/end 或 range-for 使用。迭代器是否可写、是否支持随机跳转、end/sentinel 如何表示结束，取决于具体类型。

**适用场景：** 优先使用类支持的 range-for 或 STL/ranges 算法，明确 const 与可写迭代器的区别；目录 sentinel 类型使用 C++20 ranges 或 Qt 推荐的范围写法。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要解引用 end/sentinel；不要在活跃迭代器存在时复制或修改隐式共享容器；不要缓存容器元素引用跨越可能重分配的操作。

## 2. 依赖与对象关系

- 头文件：`#include <QCborMap>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

迭代器表示容器或目录遍历中的当前位置，通常通过 begin/end 或 range-for 使用。迭代器是否可写、是否支持随机跳转、end/sentinel 如何表示结束，取决于具体类型。

### 状态、生命周期和线程

**生命周期：** 迭代器依赖底层容器、目录枚举或视图对象存活；容器修改、隐式共享 detach 或目录资源关闭可能使迭代器失效。sentinel 只用于比较结束，不能解引用。

**状态与结果：** 有效迭代器、尾后迭代器和失效迭代器是不同状态。每次递增前要保证尚未到 end；删除当前元素时使用类提供的 erase/remove 规则，不要继续使用被删除位置。

**线程与事件循环：** 迭代器不提供跨线程同步；后台遍历应拥有稳定的数据快照或独占容器，结果再通过消息传回。

## 3. 直接使用

优先使用类支持的 range-for 或 STL/ranges 算法，明确 const 与可写迭代器的区别；目录 sentinel 类型使用 C++20 ranges 或 Qt 推荐的范围写法。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
for (auto it = container.cbegin(); it != container.cend(); ++it) {
    // 读取 *it，不要在遍历期间让 container 发生会使迭代器失效的修改
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `iterator_category`

### 公有函数

- `Iterator()`
- `Iterator(const QCborMap::Iterator &other)`
- `QCborValue key() const`
- `QCborValueRef value() const`
- `QCborMap::Iterator::value_type operator*() const`
- `QCborMap::Iterator operator+(qsizetype j) const`
- `QCborMap::Iterator & operator++()`
- `QCborMap::Iterator operator++(int)`
- `QCborMap::Iterator & operator+=(qsizetype j)`
- `qsizetype operator-(QCborMap::Iterator j) const`
- `QCborMap::Iterator operator-(qsizetype j) const`
- `QCborMap::Iterator & operator--()`
- `QCborMap::Iterator operator--(int)`
- `QCborMap::Iterator & operator-=(qsizetype j)`
- `const QCborValueConstRef * operator->() const`
- `QCborMap::Iterator & operator=(const QCborMap::Iterator &other)`

### 相关非成员函数

- `bool operator!=(const QCborMap::Iterator &lhs, const QCborMap::ConstIterator &rhs)`
- `bool operator!=(const QCborMap::Iterator &lhs, const QCborMap::Iterator &rhs)`
- `bool operator<(const QCborMap::Iterator &lhs, const QCborMap::ConstIterator &rhs)`
- `bool operator<(const QCborMap::Iterator &lhs, const QCborMap::Iterator &rhs)`
- `bool operator<=(const QCborMap::Iterator &lhs, const QCborMap::ConstIterator &rhs)`
- `bool operator<=(const QCborMap::Iterator &lhs, const QCborMap::Iterator &rhs)`
- `bool operator==(const QCborMap::Iterator &lhs, const QCborMap::ConstIterator &rhs)`
- `bool operator==(const QCborMap::Iterator &lhs, const QCborMap::Iterator &rhs)`
- `bool operator>(const QCborMap::Iterator &lhs, const QCborMap::ConstIterator &rhs)`
- `bool operator>(const QCborMap::Iterator &lhs, const QCborMap::Iterator &rhs)`
- `bool operator>=(const QCborMap::Iterator &lhs, const QCborMap::ConstIterator &rhs)`
- `bool operator>=(const QCborMap::Iterator &lhs, const QCborMap::Iterator &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `Iterator::iterator_category`

**作用与语义：**

std：：random_access_iterator_tag 的同义词表示该迭代器是随机访问迭代器。

### `[constexpr noexcept] Iterator::Iterator()`

**作用与语义：**

构造一个未初始化的迭代器。
像 `key()`、`value()` 和运算符()这样的函数，在未初始化的迭代器上不得调用。在使用之前，使用 operator=() 赋值。

### `[constexpr noexcept] Iterator::Iterator(const QCborMap::Iterator &other)`

**作用与语义：**

构建一个迭代器作为`other`的副本。

### `QCborValue Iterator::key() const`

**作用与语义：**

返回当前项目的密钥。
通过迭代器没有直接方法更改项目的密钥，尽管可以通过调用`QCborMap::erase()`接`QCborMap::insert()`来实现。

### `QCborValueRef Iterator::value() const`

**作用与语义：**

返回当前项目值的可修改引用。
你可以通过在赋值左侧使用value()来更改键的值。
返回值类型为 QCborValueRef，是 `QCborArray` 和 `QCborMap` 的辅助类。当你获得类型为 QCborValueRef 的对象时，可以将其当作引用`QCborValue`使用。如果你赋值，赋值将应用到你获得引用的`QCborArray`或`QCborMap`元素上。

### `QCborMap::Iterator::value_type Iterator::operator*() const`

**作用与语义：**

返回包含当前项项键和可修改当前项值的对。
这对的第二个元素类型为 QCborValueRef，是 `QCborArray` 和 `QCborMap` 的辅助类。当你获得类型为 QCborValueRef 的对象时，可以将其当作对`QCborValue`的引用使用。如果你赋值到它，赋值将应用到你获得引用的 `QCborArray` 或 `QCborMap` 中的元素。

### `QCborMap::Iterator Iterator::operator+(qsizetype j) const`

**作用与语义：**

返回一个迭代器，返回位于`j`位置的项目，从该迭代器向前。如果`j`为负，迭代器向后移动。

### `QCborMap::Iterator &Iterator::operator++()`

**作用与语义：**

前缀`++`算符`++i`，将迭代器推进到映射中的下一个项目并返回该迭代器。
调用该函数`QCborMap::end()`会导致结果未定义。

### `QCborMap::Iterator Iterator::operator++(int)`

**作用与语义：**

后缀`++`操作符`i++`将迭代器推进到映射中的下一个项目，并将迭代器返回到之前当前的项目。

### `QCborMap::Iterator &Iterator::operator+=(qsizetype j)`

**作用与语义：**

将迭代器推进`j`项。如果`j`为负，迭代器倒退。返回对该迭代器的引用。

### `qsizetype Iterator::operator-(QCborMap::Iterator j) const`

**作用与语义：**

返回迭代器中该项相对于该迭代器`j`项的位置。如果 `j` 处的项在此时间前，返回值为负。

### `QCborMap::Iterator Iterator::operator-(qsizetype j) const`

**作用与语义：**

返回一个迭代器，返回该迭代器后退`j`位置的对象。如果`j`为负，迭代器向前。

### `QCborMap::Iterator &Iterator::operator--()`

**作用与语义：**

操作符`--`前缀`--i`使前一项为当前，并返回该迭代器。
调用该函数在`QCborMap::begin()`上会导致结果未定义。

### `QCborMap::Iterator Iterator::operator--(int)`

**作用与语义：**

后缀`--`操作符 `i--` 使前一个项目为当前，并返回指向之前当前项目的迭代器。

### `QCborMap::Iterator &Iterator::operator-=(qsizetype j)`

**作用与语义：**

使迭代器倒退 `j` 项。如果 `j` 为负，迭代器继续前进。返回对该迭代器的引用。

### `const QCborValueConstRef *Iterator::operator->() const`

**作用与语义：**

返回指向当前对值的可修改引用的指针。

### `QCborMap::Iterator &Iterator::operator=(const QCborMap::Iterator &other)`

**作用与语义：**

将该迭代器设为`other`的副本，并返回对该迭代器的引用。

### `[noexcept] bool operator!=(const QCborMap::Iterator &lhs, const QCborMap::ConstIterator &rhs)`

**作用与语义：**

如果 `lhs` 指向的映射条目与 `rhs` 迭代器不同，则返回 `true`；否则返回 `false`。

### `[noexcept] bool operator<(const QCborMap::Iterator &lhs, const QCborMap::ConstIterator &rhs)`

**作用与语义：**

如果迭代器指向的映射中的元素出现在`rhs`次代子指向的入口之前，则返回`lhs` `true`。

### `[noexcept] bool operator<=(const QCborMap::Iterator &lhs, const QCborMap::ConstIterator &rhs)`

**作用与语义：**

如果迭代器`lhs`指向的映射中元素出现在或与`rhs`迭代器指向的元素之前或相同，则返回`true`。

### `[noexcept] bool operator==(const QCborMap::Iterator &lhs, const QCborMap::ConstIterator &rhs)`

**作用与语义：**

如果`lhs`指向与迭代子相同的映射元素，则返回`true` `rhs`;否则返回`false`。

### `[noexcept] bool operator>(const QCborMap::Iterator &lhs, const QCborMap::ConstIterator &rhs)`

**作用与语义：**

如果迭代器`lhs`指向的映射中的元素位于`rhs`迭代器指向的元素之后，则返回`true`。

### `[noexcept] bool operator>=(const QCborMap::Iterator &lhs, const QCborMap::ConstIterator &rhs)`

**作用与语义：**

如果迭代器指向的映射中元素落后或与`rhs`迭代器指向的元素相同，则返回`lhs` `true`。

### `iterator_category`

**作用与语义：**

std：：random_access_iterator_tag 的同义词表示该迭代器是随机访问迭代器。

### `bool operator!=(const QCborMap::Iterator &lhs, const QCborMap::Iterator &rhs)`

**作用与语义：**

如果 `lhs` 指向的映射条目与 `rhs` 迭代器不同，则返回 `true`；否则返回 `false`。

### `bool operator<(const QCborMap::Iterator &lhs, const QCborMap::Iterator &rhs)`

**作用与语义：**

如果迭代器指向的映射中的元素出现在`rhs`次代子指向的入口之前，则返回`lhs` `true`。

### `bool operator<=(const QCborMap::Iterator &lhs, const QCborMap::Iterator &rhs)`

**作用与语义：**

如果迭代器`lhs`指向的映射中元素出现在或与`rhs`迭代器指向的元素之前或相同，则返回`true`。

### `bool operator==(const QCborMap::Iterator &lhs, const QCborMap::Iterator &rhs)`

**作用与语义：**

如果`lhs`指向与迭代子相同的映射元素，则返回`true` `rhs`;否则返回`false`。

### `bool operator>(const QCborMap::Iterator &lhs, const QCborMap::Iterator &rhs)`

**作用与语义：**

如果迭代器`lhs`指向的映射中的元素位于`rhs`迭代器指向的元素之后，则返回`true`。

### `bool operator>=(const QCborMap::Iterator &lhs, const QCborMap::Iterator &rhs)`

**作用与语义：**

如果迭代器指向的映射中元素落后或与`rhs`迭代器指向的元素相同，则返回`lhs` `true`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

迭代器依赖底层容器、目录枚举或视图对象存活；容器修改、隐式共享 detach 或目录资源关闭可能使迭代器失效。sentinel 只用于比较结束，不能解引用。

### 状态和错误边界

有效迭代器、尾后迭代器和失效迭代器是不同状态。每次递增前要保证尚未到 end；删除当前元素时使用类提供的 erase/remove 规则，不要继续使用被删除位置。

### 线程边界

迭代器不提供跨线程同步；后台遍历应拥有稳定的数据快照或独占容器，结果再通过消息传回。

### 最容易出现的错误

不要解引用 end/sentinel；不要在活跃迭代器存在时复制或修改隐式共享容器；不要缓存容器元素引用跨越可能重分配的操作。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QCborMap::Iterator` 所属机制类型：迭代器与范围机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
