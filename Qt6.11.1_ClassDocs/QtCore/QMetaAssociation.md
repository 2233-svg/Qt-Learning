# QMetaAssociation

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“MetaAssociation”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMetaAssociation` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QMetaAssociation>`
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

- `bool canContainsKey() const`
- `bool canCreateConstIteratorAtKey() const`
- `bool canCreateIteratorAtKey() const`
- `bool canGetKeyAtConstIterator() const`
- `bool canGetKeyAtIterator() const`
- `bool canGetMappedAtConstIterator() const`
- `bool canGetMappedAtIterator() const`
- `bool canGetMappedAtKey() const`
- `bool canInsertKey() const`
- `bool canRemoveKey() const`
- `bool canSetMappedAtIterator() const`
- `bool canSetMappedAtKey() const`
- `bool containsKey(const void *container, const void *key) const`
- `void * createConstIteratorAtKey(const void *container, const void *key) const`
- `void * createIteratorAtKey(void *container, const void *key) const`
- `void insertKey(void *container, const void *key) const`
- `void keyAtConstIterator(const void *iterator, void *key) const`
- `void keyAtIterator(const void *iterator, void *key) const`
- `QMetaType keyMetaType() const`
- `void mappedAtConstIterator(const void *iterator, void *mapped) const`
- `void mappedAtIterator(const void *iterator, void *mapped) const`
- `void mappedAtKey(const void *container, const void *key, void *mapped) const`
- `QMetaType mappedMetaType() const`
- `void removeKey(void *container, const void *key) const`
- `void setMappedAtIterator(const void *iterator, const void *mapped) const`
- `void setMappedAtKey(void *container, const void *key, const void *mapped) const`

### 静态公有成员

- `(since 6.0) QMetaAssociation fromContainer()`

### 相关非成员函数

- `bool operator!=(const QMetaAssociation &lhs, const QMetaAssociation &rhs)`
- `bool operator==(const QMetaAssociation &lhs, const QMetaAssociation &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `bool QMetaAssociation::canContainsKey() const`

**作用与语义：**

如果容器可以用`containsKey()`查询密钥，返回`true`;否则返回`false`。

### `bool QMetaAssociation::canCreateConstIteratorAtKey() const`

**作用与语义：**

如果可以用`createConstIteratorAtKey()`创建指向容器中条目的const迭代器，则返回`true`，否则返回false。

### `bool QMetaAssociation::canCreateIteratorAtKey() const`

**作用与语义：**

如果可以用`createIteratorAtKey()`创建指向容器中条目的迭代器，返回`true`;否则返回false。

### `bool QMetaAssociation::canGetKeyAtConstIterator() const`

**作用与语义：**

如果能用`keyAtConstIterator()`从const迭代器中检索密钥，则返回`true`，否则返回`false`。

### `bool QMetaAssociation::canGetKeyAtIterator() const`

**作用与语义：**

如果能用 `keyAtIterator()` 从非一致性迭代器检索密钥，返回`true`，否则返回 `false`。

### `bool QMetaAssociation::canGetMappedAtConstIterator() const`

**作用与语义：**

如果可以用`mappedAtConstIterator()`从cont迭代器中检索映射值，返回`true`，否则返回`false`。

### `bool QMetaAssociation::canGetMappedAtIterator() const`

**作用与语义：**

如果可以用 `mappedAtIterator()` 从非一致性迭代器中检索映射值，返回`true`，否则返回 `false`。

### `bool QMetaAssociation::canGetMappedAtKey() const`

**作用与语义：**

如果容器可以用`mappedAtKey()`查询值，返回`true`，否则返回`false`。

### `bool QMetaAssociation::canInsertKey() const`

**作用与语义：**

如果可以用`insertKey()`添加密钥到容器，返回`true`，否则返回`false`。

### `bool QMetaAssociation::canRemoveKey() const`

**作用与语义：**

如果可以用`removeKey()`从容器中移除密钥，返回`true`，否则返回`false`。

### `bool QMetaAssociation::canSetMappedAtIterator() const`

**作用与语义：**

如果映射值可以通过非const迭代器设置，则返回`setMappedAtIterator()` `true`，否则返回`false`。

### `bool QMetaAssociation::canSetMappedAtKey() const`

**作用与语义：**

如果映射值可以用`setMappedAtKey()`在容器中修改，返回`true`，否则返回`false`。

### `bool QMetaAssociation::containsKey(const void *container, const void *key) const`

**作用与语义：**

如果 `container` 可以查询键并且包含 `key`，则返回 `true`，否则返回 `false`。

### `void *QMetaAssociation::createConstIteratorAtKey(const void *container, const void *key) const`

**作用与语义：**

如果可能，返回指向`container`中 `key` 条目的 cont 迭代器。如果不存在该条目，则创建一个指向`container`末尾的 cont 迭代器。如果无法创建 cont 迭代器，返回 `nullptr`。
必须用 `destroyConstIterator()` 来销毁 const 迭代子。

### `void *QMetaAssociation::createIteratorAtKey(void *container, const void *key) const`

**作用与语义：**

如果可能的话，返回指向`container`中`key`的非const迭代子。如果该条目不存在，则创建一个指向`container`末尾的非const迭代子。如果无法创建非const迭代子，则返回`nullptr`。
非const迭代子必须用 `destroyIterator()` 来销毁。

### `[static constexpr, since 6.0] template <typename T> QMetaAssociation QMetaAssociation::fromContainer()`

**作用与语义：**

返回与模板参数类型对应的`QMetaAssociation`。

### `void QMetaAssociation::insertKey(void *container, const void *key) const`

**作用与语义：**

如果可能，将`key`插入`container`中。如果容器有映射值，`key`会关联一个默认创建的映射值。

### `void QMetaAssociation::keyAtConstIterator(const void *iterator, void *key) const`

**作用与语义：**

检索cont `iterator`指向的密钥，并尽可能将其存储在`key`指向的内存位置中。

### `void QMetaAssociation::keyAtIterator(const void *iterator, void *key) const`

**作用与语义：**

检索非const `iterator`指向的密钥，并尽可能将其存储在`key`指向的内存位置。

### `QMetaType QMetaAssociation::keyMetaType() const`

**作用与语义：**

返回容器中密钥的元类型。

### `void QMetaAssociation::mappedAtConstIterator(const void *iterator, void *mapped) const`

**作用与语义：**

检索const `iterator`指向的映射值，并尽可能将其存储在`mapped`指向的内存位置。

### `void QMetaAssociation::mappedAtIterator(const void *iterator, void *mapped) const`

**作用与语义：**

检索非const节点`iterator`指向的映射值，并尽可能将其存储在`mapped`指向的内存位置。

### `void QMetaAssociation::mappedAtKey(const void *container, const void *key, void *mapped) const`

**作用与语义：**

检索`container`中与`key`关联的映射值，并将其放置在`mapped`指向的内存位置（如果可能的话）。

### `QMetaType QMetaAssociation::mappedMetaType() const`

**作用与语义：**

返回容器中映射值的元类型。

### `void QMetaAssociation::removeKey(void *container, const void *key) const`

**作用与语义：**

如果可能的话，移除`key`及其映射值，从`container`中移除。

### `void QMetaAssociation::setMappedAtIterator(const void *iterator, const void *mapped) const`

**作用与语义：**

如果可能的话，将`mapped`值写入非const型`iterator`指向的容器位置。

### `void QMetaAssociation::setMappedAtKey(void *container, const void *key, const void *mapped) const`

**作用与语义：**

如果可能的话，会用作为参数传递的`mapped`值覆盖`container`中与`key`关联的值。

### `[noexcept] bool operator!=(const QMetaAssociation &lhs, const QMetaAssociation &rhs)`

**作用与语义：**

如果`QMetaAssociation` `lhs`代表与`QMetaAssociation` `rhs`不同的容器类型，返回`true`，否则返回`false`。

### `[noexcept] bool operator==(const QMetaAssociation &lhs, const QMetaAssociation &rhs)`

**作用与语义：**

返回`true`如果`QMetaAssociation` `lhs`表示与…相同的容器类型`QMetaAssociation` `rhs`，否则返回`false`.

### `(since 6.11) class Iterable`

**作用与语义：**

QMetaAssociation：：Iterable 是 QVariant 中关联容器的可迭代接口。
该类允许多种方法访问包含在`QVariant`中的关联容器元素。如果`QMetaAssociation::Iterable`实例可以转换为`QVariantHash`或`QVariantMap`，或者注册了自定义可变视图，则可以从`QVariant`中提取。
容器本身在迭代之前不会被复制。

**官方示例：**

```cpp
 QHash<int, QString> mapping;
 mapping.insert(7, "Seven");
 mapping.insert(11, "Eleven");
 mapping.insert(42, "Forty-two");

 QVariant variant = QVariant::fromValue(mapping);
 if (variant.canConvert<QVariantHash>()) {
     QMetaAssociation::Iterable iterable = variant.value<QMetaAssociation::Iterable>();
     // Can use C++11 range-for over the values:
     for (const QVariant &v : iterable) {
         qDebug() << v;
     }
     // Can use iterators:
     QMetaAssociation::Iterable::const_iterator it = iterable.begin();
     const QMetaAssociation::Iterable::const_iterator end = iterable.end();
     for ( ; it != end; ++it) {
         qDebug() << *it; // The current value
         qDebug() << it.key();
         qDebug() << it.value();
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

`QMetaAssociation` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
