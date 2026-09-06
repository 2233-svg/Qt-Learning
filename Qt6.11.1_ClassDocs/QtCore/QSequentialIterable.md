# QSequentialIterable

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“SequentialIterable”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSequentialIterable` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QSequentialIterable>`
- 继承自：QIterable
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

- `BidirectionalConstIterator`
- `BidirectionalIterator`
- `ForwardConstIterator`
- `ForwardIterator`
- `InputConstIterator`
- `InputIterator`
- `RandomAccessConstIterator`
- `RandomAccessIterator`
- `(until 6.15) const_iterator`
- `(since 6.0, until 6.15) iterator`

### 公有函数

- `void addValue(const QVariant &value, QSequentialIterable::Position position = Unspecified)`
- `QVariant at(qsizetype idx) const`
- `void removeValue(QSequentialIterable::Position position = Unspecified)`
- `void set(qsizetype idx, const QVariant &value)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QSequentialIterable::BidirectionalConstIterator`

**作用与语义：**

用标准测试暴露`const_iterator`：：bidirectional_iterator_tag。

### `[alias] QSequentialIterable::BidirectionalIterator`

**作用与语义：**

使用标准化程序暴露迭代器：：bidirectional_iterator_tag。

### `[alias] QSequentialIterable::ForwardConstIterator`

**作用与语义：**

用 std（标准化）暴露`const_iterator` ：：forward_iterator_tag。

### `[alias] QSequentialIterable::ForwardIterator`

**作用与语义：**

用std：：forward_iterator_tag暴露迭代器。

### `[alias] QSequentialIterable::InputConstIterator`

**作用与语义：**

用STD暴露`const_iterator`：：input_iterator_tag。

### `[alias] QSequentialIterable::InputIterator`

**作用与语义：**

使用 std：：input_iterator_tag 暴露迭代器。

### `[alias] QSequentialIterable::RandomAccessConstIterator`

**作用与语义：**

用STD暴露`const_iterator`：：random_access_iterator_tag。

### `[alias] QSequentialIterable::RandomAccessIterator`

**作用与语义：**

用std：：random_access_iterator_tag暴露迭代器。

### `[alias, until 6.15] QSequentialIterable::const_iterator`

**作用与语义：**

该typedef计划在6.15版本中弃用。
用`QMetaSequence::Iterable::ConstIterator`代替。
QSequentialIterable：：const_iterator 允许在`QVariant`中的容器上进行迭代。
QSequentialIterable：：const_iterator只能由`QSequentialIterable`实例创建，且其使用方式类似于其他STL风格迭代子。

### `[alias, since 6.0, until 6.15] QSequentialIterable::iterator`

**作用与语义：**

该typedef计划在6.15版本中弃用。
用 `QMetaSequence::Iterable::Iterator` 代替。
QSequentialIterable：：iterator允许在`QVariant`中的容器上进行迭代。
QSequentialIterable：：iterator只能由`QSequentialIterable`实例创建，且其使用方式类似于其他STL风格的迭代器。
这种类型防御是在Qt 6.0中引入的。

### `void QSequentialIterable::addValue(const QVariant &value, QSequentialIterable::Position position = Unspecified)`

**作用与语义：**

如果可能的话，`position`时给容器加`value`。

### `QVariant QSequentialIterable::at(qsizetype idx) const`

**作用与语义：**

返回容器中位置`idx`的值。

### `void QSequentialIterable::removeValue(QSequentialIterable::Position position = Unspecified)`

**作用与语义：**

如果可能，`position`处从容器中移除一个值。

### `void QSequentialIterable::set(qsizetype idx, const QVariant &value)`

**作用与语义：**

将容器中位置`idx`的元素设置为`value`。

### `BidirectionalConstIterator`

**作用与语义：**

用标准测试暴露`const_iterator`：：bidirectional_iterator_tag。

### `BidirectionalIterator`

**作用与语义：**

使用标准化程序暴露迭代器：：bidirectional_iterator_tag。

### `ForwardConstIterator`

**作用与语义：**

用 std（标准化）暴露`const_iterator` ：：forward_iterator_tag。

### `ForwardIterator`

**作用与语义：**

用std：：forward_iterator_tag暴露迭代器。

### `InputConstIterator`

**作用与语义：**

用STD暴露`const_iterator`：：input_iterator_tag。

### `InputIterator`

**作用与语义：**

使用 std：：input_iterator_tag 暴露迭代器。

### `RandomAccessConstIterator`

**作用与语义：**

用STD暴露`const_iterator`：：random_access_iterator_tag。

### `RandomAccessIterator`

**作用与语义：**

用std：：random_access_iterator_tag暴露迭代器。

### `(until 6.15) const_iterator`

**作用与语义：**

该typedef计划在6.15版本中弃用。
用`QMetaSequence::Iterable::ConstIterator`代替。
QSequentialIterable：：const_iterator 允许在`QVariant`中的容器上进行迭代。
QSequentialIterable：：const_iterator只能由`QSequentialIterable`实例创建，且其使用方式类似于其他STL风格迭代子。

### `(since 6.0, until 6.15) iterator`

**作用与语义：**

该typedef计划在6.15版本中弃用。
用 `QMetaSequence::Iterable::Iterator` 代替。
QSequentialIterable：：iterator允许在`QVariant`中的容器上进行迭代。
QSequentialIterable：：iterator只能由`QSequentialIterable`实例创建，且其使用方式类似于其他STL风格的迭代器。
这种类型防御是在Qt 6.0中引入的。

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

`QSequentialIterable` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
