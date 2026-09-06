# QMetaSequence

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“MetaSequence”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMetaSequence` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QMetaSequence>`
- 继承自：QMetaContainer
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

- `(since 6.11) class Iterable`

### 公有函数

- `void addValue(void *container, const void *value) const`
- `void addValueAtBegin(void *container, const void *value) const`
- `void addValueAtEnd(void *container, const void *value) const`
- `bool canAddValue() const`
- `bool canAddValueAtBegin() const`
- `bool canAddValueAtEnd() const`
- `bool canEraseRangeAtIterator() const`
- `bool canEraseValueAtIterator() const`
- `bool canGetValueAtConstIterator() const`
- `bool canGetValueAtIndex() const`
- `bool canGetValueAtIterator() const`
- `bool canInsertValueAtIterator() const`
- `bool canRemoveValue() const`
- `bool canRemoveValueAtBegin() const`
- `bool canRemoveValueAtEnd() const`
- `bool canSetValueAtIndex() const`
- `bool canSetValueAtIterator() const`
- `void eraseRangeAtIterator(void *container, const void *iterator1, const void *iterator2) const`
- `void eraseValueAtIterator(void *container, const void *iterator) const`
- `void insertValueAtIterator(void *container, const void *iterator, const void *value) const`
- `bool isSortable() const`
- `void removeValue(void *container) const`
- `void removeValueAtBegin(void *container) const`
- `void removeValueAtEnd(void *container) const`
- `void setValueAtIndex(void *container, qsizetype index, const void *value) const`
- `void setValueAtIterator(const void *iterator, const void *value) const`
- `void valueAtConstIterator(const void *iterator, void *result) const`
- `void valueAtIndex(const void *container, qsizetype index, void *result) const`
- `void valueAtIterator(const void *iterator, void *result) const`
- `QMetaType valueMetaType() const`

### 静态公有成员

- `(since 6.0) QMetaSequence fromContainer()`

### 相关非成员函数

- `(since 6.0) bool operator!=(const QMetaSequence &lhs, const QMetaSequence &rhs)`
- `(since 6.0) bool operator==(const QMetaSequence &lhs, const QMetaSequence &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `void QMetaSequence::addValue(void *container, const void *value) const`

**作用与语义：**

如果可能，将`value`加到`container`上。如果`canAddValue()`返回`false`，则不加`value`。否则，如果`canAddValueAtEnd()`返回`true`，则`value`会加到`container`末尾。否则，如果`canAddValueAtBegin()`返回`true`，`value`会被添加到容器的开头。否则，值会被添加到未指定的位置，或者根本不添加。后者适用于向无序容器添加值的情况，例如，`QSet`。

### `void QMetaSequence::addValueAtBegin(void *container, const void *value) const`

**作用与语义：**

如果可能，`container`开头加`value`。如果`canAddValueAtBegin()`返回`false`，则不添加`value`。

### `void QMetaSequence::addValueAtEnd(void *container, const void *value) const`

**作用与语义：**

如果可能，会在`container`末加`value`。如果`canAddValueAtEnd()`返回`false`，则不加`value`。

### `bool QMetaSequence::canAddValue() const`

**作用与语义：**

返回`true`是否可以向容器添加值，否则`false`返回。

### `bool QMetaSequence::canAddValueAtBegin() const`

**作用与语义：**

如果用 `addValue()` 添加的值可以放在容器开头，返回`true`，否则返回`false`。

### `bool QMetaSequence::canAddValueAtEnd() const`

**作用与语义：**

如果用 `addValue()` 添加的值可以放在容器末端，返回`true`，否则返回`false`。

### `bool QMetaSequence::canEraseRangeAtIterator() const`

**作用与语义：**

如果两个迭代器之间的区间可以从容器中抹除，返回`true`，否则`false`。

### `bool QMetaSequence::canEraseValueAtIterator() const`

**作用与语义：**

如果非const迭代子指向的值可以被擦除，返回`true`，否则`false`。

### `bool QMetaSequence::canGetValueAtConstIterator() const`

**作用与语义：**

如果底层容器能够检索到const迭代器指向的值，返回`true`，否则`false`返回。

### `bool QMetaSequence::canGetValueAtIndex() const`

**作用与语义：**

如果可以通过索引从容器中检索值，否则返回`true`，否则`false`。

### `bool QMetaSequence::canGetValueAtIterator() const`

**作用与语义：**

如果底层容器能够检索非const迭代器指向的值，返回则`true`，否则`false`返回。

### `bool QMetaSequence::canInsertValueAtIterator() const`

**作用与语义：**

返回`true`底层容器是否能插入一个新值，并考虑非const迭代器指向的位置。

### `bool QMetaSequence::canRemoveValue() const`

**作用与语义：**

返回`true`是否可以从容器中移除值，否则`false`。

### `bool QMetaSequence::canRemoveValueAtBegin() const`

**作用与语义：**

如果可以用`removeValue()`从容器开头移除值，返回`true`，否则返回`false`。

### `bool QMetaSequence::canRemoveValueAtEnd() const`

**作用与语义：**

如果可以用`removeValue()`从容器末端移除值，返回`true`，否则返回`false`。

### `bool QMetaSequence::canSetValueAtIndex() const`

**作用与语义：**

如果能通过索引写入容器，返回`true`，否则`false`。

### `bool QMetaSequence::canSetValueAtIterator() const`

**作用与语义：**

如果底层容器能够写入非const迭代器指向的值，返回`true`，否则`false`。

### `void QMetaSequence::eraseRangeAtIterator(void *container, const void *iterator1, const void *iterator2) const`

**作用与语义：**

如果可能的话，消除迭代器`iterator1`和`iterator2`之间的值范围，从`container`中消失。

### `void QMetaSequence::eraseValueAtIterator(void *container, const void *iterator) const`

**作用与语义：**

如果可能的话，从`container`中抹去非连续`iterator`所指向的值。

### `[static constexpr, since 6.0] template <typename T> QMetaSequence QMetaSequence::fromContainer()`

**作用与语义：**

返回与模板参数类型对应的`QMetaSequence`。

### `void QMetaSequence::insertValueAtIterator(void *container, const void *iterator, const void *value) const`

**作用与语义：**

如果可能，将`value`插入到`container`中，考虑非恒定的`iterator`。如果`canInsertValueAtIterator()`返回`false`，则该`value`未入。否则，如果`isSortable()`返回`true`，则将该值插入于`iterator`指向的值之前。否则，`value`将入在未指定位置或根本不插入。在后一种情况下，`iterator`被视为提示。如果它指向`value`的正确位置，操作可能比没有迭代器的`addValue()`更快。

### `bool QMetaSequence::isSortable() const`

**作用与语义：**

如果底层容器可排序，返回`true`，否则返回`false`。如果添加的值被放置在定义位置，则该容器被视为可排序。插入或添加可排序容器总是成功。插入或添加不可排序容器可能不成功，例如当容器是已包含入值的`QSet`时。

### `void QMetaSequence::removeValue(void *container) const`

**作用与语义：**

如果可能，从`container`中移除一个值。如果`canRemoveValue()`返回`false`，则不移除任何值。否则，如果`canRemoveValueAtEnd()`返回`true`，则移除`container`中的最后一个值。否则，如果`canRemoveValueAtBegin()`返回`true`，则移除`container`中的第一个值。否则，移除未指定值或无值。

### `void QMetaSequence::removeValueAtBegin(void *container) const`

**作用与语义：**

如果可能，移除`container`开头的一个值。如果`canRemoveValueAtBegin()`返回`false`，则该值不会被移除。

### `void QMetaSequence::removeValueAtEnd(void *container) const`

**作用与语义：**

如果可能，移除`container`末尾的一个值。如果`canRemoveValueAtEnd()`返回`false`，则该值不会被移除。

### `void QMetaSequence::setValueAtIndex(void *container, qsizetype index, const void *value) const`

**作用与语义：**

如果可能的话，使用作为参数传递的`value`覆盖`container`中`index`处的值。

### `void QMetaSequence::setValueAtIterator(const void *iterator, const void *value) const`

**作用与语义：**

如果可能的话，写入`value`到非条件的`iterator`所指向的值。

### `void QMetaSequence::valueAtConstIterator(const void *iterator, void *result) const`

**作用与语义：**

检索const `iterator`指向的值，并尽可能将其存储在`result`指向的内存位置中。

### `void QMetaSequence::valueAtIndex(const void *container, qsizetype index, void *result) const`

**作用与语义：**

在`container`中检索到`index`的值，并将其放置在`result`指向的内存位置（如果可能的话）。

### `void QMetaSequence::valueAtIterator(const void *iterator, void *result) const`

**作用与语义：**

检索非条件 `iterator` 指向的值，并尽可能将其存储在 `result` 指向的内存位置。

### `QMetaType QMetaSequence::valueMetaType() const`

**作用与语义：**

返回存储在容器中的值的元类型。

### `[noexcept, since 6.0] bool operator!=(const QMetaSequence &lhs, const QMetaSequence &rhs)`

**作用与语义：**

返回`true`如果`QMetaSequence` `lhs`表示与 {} 不同的容器类型`QMetaSequence` `rhs`，否则返回`false`.

### `[noexcept, since 6.0] bool operator==(const QMetaSequence &lhs, const QMetaSequence &rhs)`

**作用与语义：**

返回`true`如果`QMetaSequence` `lhs`表示与…相同的容器类型`QMetaSequence` `rhs`，否则返回`false`.

### `(since 6.11) class Iterable`

**作用与语义：**

QMetaSequence：：Iterable 类是 QVariant 中容器的可循环接口。
该类允许多种方法访问`QVariant`中容器的值。如果`QMetaSequence::Iterable`实例可以转换为`QVariantList`，或者其容器通过`Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE`注册，就可以从`QVariant`中提取。Qt中大多数顺序容器和部分C标准库中的容器都会自动注册。
容器本身在迭代之前不会被复制。

**官方示例：**

```cpp
 QList<int> intList = {7, 11, 42};

 QVariant variant = QVariant::fromValue(intList);
 if (variant.canConvert<QVariantList>()) {
     QMetaSequence::Iterable iterable = variant.value<QMetaSequence::Iterable>();
     // Can use C++11 range-for:
     for (const QVariant &v : iterable) {
         qDebug() << v;
     }
     // Can use iterators:
     QMetaSequence::Iterable::const_iterator it = iterable.begin();
     const QMetaSequence::Iterable::const_iterator end = iterable.end();
     for ( ; it != end; ++it) {
         qDebug() << *it;
     }
 }
```

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

`QMetaSequence` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
