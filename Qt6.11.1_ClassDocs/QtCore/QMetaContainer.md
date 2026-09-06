# QMetaContainer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Meta容器”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMetaContainer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QMetaContainer>`
- 继承自：未在类页中列出
- 直接派生类：QMetaAssociation、QMetaSequence

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

### 公有函数

- `void advanceConstIterator(void *iterator, qsizetype step) const`
- `void advanceIterator(void *iterator, qsizetype step) const`
- `void * begin(void *container) const`
- `bool canClear() const`
- `void clear(void *container) const`
- `bool compareConstIterator(const void *i, const void *j) const`
- `bool compareIterator(const void *i, const void *j) const`
- `void * constBegin(const void *container) const`
- `void * constEnd(const void *container) const`
- `void copyConstIterator(void *target, const void *source) const`
- `void copyIterator(void *target, const void *source) const`
- `void destroyConstIterator(const void *iterator) const`
- `void destroyIterator(const void *iterator) const`
- `qsizetype diffConstIterator(const void *i, const void *j) const`
- `qsizetype diffIterator(const void *i, const void *j) const`
- `void * end(void *container) const`
- `bool hasBidirectionalIterator() const`
- `bool hasConstIterator() const`
- `bool hasForwardIterator() const`
- `bool hasInputIterator() const`
- `bool hasIterator() const`
- `bool hasRandomAccessIterator() const`
- `bool hasSize() const`
- `qsizetype size(const void *container) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `void QMetaContainer::advanceConstIterator(void *iterator, qsizetype step) const`

**作用与语义：**

将const的前进`iterator`步`step`步。如果`step`为负，`iterator`会向后移动，靠近容器的起始位置。如果`hasBidirectionalIterator()`返回false，则`step`负值的行为未明确说明。

### `void QMetaContainer::advanceIterator(void *iterator, qsizetype step) const`

**作用与语义：**

将非const的 `iterator` 前进`step`步。如果 `step`为负，则`iterator`会向后移动，靠近容器的起始位置。如果`hasBidirectionalIterator()`返回假，则对负值`step`行为未明确说明。

### `void *QMetaContainer::begin(void *container) const`

**作用与语义：**

创建并返回一个指向`container`起始的非const迭代器。迭代器通过new在堆上分配。最终必须用`destroyIterator`销毁它，以回收内存。
如果容器没有提供非连续迭代器，返回`nullptr`。

### `bool QMetaContainer::canClear() const`

**作用与语义：**

如果容器能被清理，`false` `true`退货。

### `void QMetaContainer::clear(void *container) const`

**作用与语义：**

如果能清除的话，`container`会清除。

### `bool QMetaContainer::compareConstIterator(const void *i, const void *j) const`

**作用与语义：**

如果const迭代器`i`和`j`指向它们正在迭代的容器中的相同值，返回`true`，否则返回`false`。

### `bool QMetaContainer::compareIterator(const void *i, const void *j) const`

**作用与语义：**

如果非常量迭代器 `i` 和 `j` 指向它们所迭代的容器中的相同值，则返回 `true`，否则返回 `false`。

### `void *QMetaContainer::constBegin(const void *container) const`

**作用与语义：**

创建并返回指向 `container` 起始的 cont 迭代器。迭代器通过 new 在堆上分配。最终必须用 `destroyConstIterator` 销毁它，以回收内存。
如果容器没有提供任何连续迭代器，返回`nullptr`。

### `void *QMetaContainer::constEnd(const void *container) const`

**作用与语义：**

创建并返回指向`container`末尾的const迭代器。该迭代器通过new在堆上分配。最终必须用`destroyConstIterator`销毁它，以回收内存。
如果容器没有提供任何连续迭代器，返回`nullptr`。

### `void QMetaContainer::copyConstIterator(void *target, const void *source) const`

**作用与语义：**

将 const 迭代器`source`复制到 const 迭代器 `target`。之后 `compareConstIterator`（目标，源）返回 `true`。

### `void QMetaContainer::copyIterator(void *target, const void *source) const`

**作用与语义：**

将非const迭代器`source`复制到非const迭代器`target`。之后`compareIterator`（target， source）返回`true`。

### `void QMetaContainer::destroyConstIterator(const void *iterator) const`

**作用与语义：**

摧毁之前用`constBegin()`或`constEnd()`创建`iterator`的函数。

### `void QMetaContainer::destroyIterator(const void *iterator) const`

**作用与语义：**

摧毁之前用`begin()`或`end()`创建的非连续`iterator`。

### `qsizetype QMetaContainer::diffConstIterator(const void *i, const void *j) const`

**作用与语义：**

返回集合迭代子`i`和`j`之间的距离，相当于 `i` `-` `j`。如果`j`比`i`更接近容器末端，则返回值为负。如果`hasBidirectionalIterator()`返回为假，则行为未明确说明。

### `qsizetype QMetaContainer::diffIterator(const void *i, const void *j) const`

**作用与语义：**

返回非const迭代子`i`和`j`之间的距离，相当于于4 `i` `-` `j`。如果`j`比`i`更接近容器末端，返回的值为负。如果`hasBidirectionalIterator()`返回false，则行为未指定。

### `void *QMetaContainer::end(void *container) const`

**作用与语义：**

创建并返回指向`container`末尾的非const迭代子。该迭代子通过new在堆上分配。最终必须用`destroyIterator`销毁它，以回收内存。
如果容器没有提供任何非连续迭代，返回`nullptr`。

### `bool QMetaContainer::hasBidirectionalIterator() const`

**作用与语义：**

如果底层容器提供双向迭代器或随机访问迭代器，分别由 std：：bidirectional_iterator_tag 和 std：：random_access_iterator_tag 定义，则返回 `true`。否则返回 `false`。
`QMetaContainer`假设同一容器的const和非const迭代器具有相同的迭代特征。

### `bool QMetaContainer::hasConstIterator() const`

**作用与语义：**

如果底层容器提供 const 迭代器，则返回`true`，否则`false`。

### `bool QMetaContainer::hasForwardIterator() const`

**作用与语义：**

如果底层容器至少提供了 std：：forward_iterator_tag 定义的前向迭代器，返回 `true`，否则返回 `false`。双向迭代器和随机访问迭代器是前向迭代器的专用化。如果容器提供此类迭代，该方法也会返回`true`。
`QMetaContainer`假设同一容器的const和非const迭代子具有相同的迭代特征。

### `bool QMetaContainer::hasInputIterator() const`

**作用与语义：**

如果底层容器至少提供 std：：input_iterator_tag 定义的输入迭代器，返回 `true`，否则返回 `false`。前向、双向和随机访问迭代器是输入迭代器的专用化。如果容器提供其中一个，该方法也会返回`true`。
`QMetaContainer`假设同一容器的const和非const迭代器具有相同的迭代特征。

### `bool QMetaContainer::hasIterator() const`

**作用与语义：**

如果底层容器提供非一致性迭代器，返回`true`，否则`false`。

### `bool QMetaContainer::hasRandomAccessIterator() const`

**作用与语义：**

如果底层容器提供了由 std：：random_access_iterator_tag 定义的随机访问迭代器，则返回`true`;否则返回 `false`。
`QMetaContainer`假设同一容器的const和非const迭代器具有相同的迭代特征。

### `bool QMetaContainer::hasSize() const`

**作用与语义：**

如果容器可以查询尺寸，`true`返回，否则`false`。

### `qsizetype QMetaContainer::size(const void *container) const`

**作用与语义：**

如果可以查询给定`container`的大小，返回该中的值数。否则返回`-1`。

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

`QMetaContainer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
