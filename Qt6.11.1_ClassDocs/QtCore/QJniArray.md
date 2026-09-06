# QJniArray

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Jni数组”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QJniArray` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QJniArray>`
- 继承自：QJniArrayBase
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
- `const_reverse_iterator`
- `iterator`
- `reverse_iterator`

### 公有函数

- `QJniArray()`
- `QJniArray(Container &&container)`
- `QJniArray(QJniArray<Other> &&other)`
- `(since 6.9) QJniArray(QJniArrayBase::size_type size)`
- `QJniArray(QJniObject &&object)`
- `QJniArray(const QJniArray<Other> &other)`
- `QJniArray(const QJniObject &object)`
- `QJniArray(jarray array)`
- `QJniArray(std::initializer_list<T> &list)`
- `~QJniArray()`
- `auto arrayObject() const`
- `QJniArray<T>::const_reference at(QJniArrayBase::size_type i) const`
- `QJniArray<T>::iterator begin()`
- `QJniArray<T>::const_iterator begin() const`
- `QJniArray<T>::const_iterator cbegin() const`
- `QJniArray<T>::const_iterator cend() const`
- `QJniArray<T>::const_iterator constBegin() const`
- `QJniArray<T>::const_iterator constEnd() const`
- `QJniArray<T>::const_reverse_iterator crbegin() const`
- `QJniArray<T>::const_reverse_iterator crend() const`
- `QJniArray<T>::iterator end()`
- `QJniArray<T>::const_iterator end() const`
- `QJniArray<T>::reverse_iterator rbegin()`
- `QJniArray<T>::const_reverse_iterator rbegin() const`
- `QJniArray<T>::reverse_iterator rend()`
- `QJniArray<T>::const_reverse_iterator rend() const`
- `Container toContainer(Container &&container = {}) const`
- `QJniArray<T> & operator=(QJniArray<Other> &&other)`
- `QJniArray<T> & operator=(const QJniArray<Other> &other)`
- `(since 6.9) QJniArray<T>::reference operator[](QJniArrayBase::size_type i)`
- `QJniArray<T>::const_reference operator[](QJniArrayBase::size_type i) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QJniArray::iterator`

**作用与语义：**

一个随机访问迭代器用于`QJniArray`。/*。
/*!
一个随机存取、连续迭代器用于`QJniArray`。

### `[alias] QJniArray::reverse_iterator`

**作用与语义：**

`QJniArray`的反迭代器，`std::reverse_iterator<iterator>`的同义词。
注意：使用`operator->()`访问反迭代子元素需要C 20，因为C 17 `reverse_iterator`不支持返回代理对象的迭代器。/*。
/*!
`QJniArray`的反迭代器，`std::reverse_iterator<const_iterator>`的同义词。
注意：使用`operator->()`访问反迭代器元素需要C 20，因为C 17 `reverse_iterator`不支持返回代理对象的迭代器。

### `QJniArray::QJniArray()`

**作用与语义：**

QJniArray 的默认构造函数。这不会创建 Java 端数组，实例将无效。

### `[explicit] template <typename Container, QJniArrayBase::if_compatible_source_container<Container> = true> QJniArray::QJniArray(Container &&container)`

**作用与语义：**

构建一个QJniArray，将新创建的Java数组包裹为类型`Container::value_type`的元素，并将`container`的数据填充到Java数组中。
只有当`Container`是存储JNI类型或等效C类型元素的容器，并提供前向迭代器时，才参与超载解析。
构造的QJni数组的专用取决于`container`的值类型。对于`Container<T>`（如`QList<T>`），通常为`QJniArray<T>`，但有以下例外：
- `Container`：专业化
- `QByteArray`：QJniArray<jbyte>
- `QStringList`：QJniArray<jstring>
- `Container::value_type`：专业化
- `QJniObject`：QJniArray<jobject>

### `[noexcept] template <typename Other, QJniArrayBase::if_convertible<Other, T> = true> QJniArray::QJniArray(QJniArray<Other> &&other)`

**作用与语义：**

通过从`other`移动构建QJniArray。`other`数组变为`invalid`。
只有当`other`的元素类型`Other`可转换为正在构建的QJniArray的元素类型`T`时，才参与重载决议。但实际不进行转换。

### `[explicit, since 6.9] QJniArray::QJniArray(QJniArrayBase::size_type size)`

**作用与语义：**

构造一个大小为 `size` 的空 QJniArray。数组中的元素不会被初始化。

### `[explicit noexcept] QJniArray::QJniArray(QJniObject &&object)`

**作用与语义：**

通过从`object`移动构建QJni数组。`QJniObject`变为`invalid`。
注意：该构造函数不会验证 Java 端对象是否为正确类型的数组。访问不匹配的 QJniArray 会导致行为未定义。

### `template <typename Other, QJniArrayBase::if_convertible<Other, T> = true> QJniArray::QJniArray(const QJniArray<Other> &other)`

**作用与语义：**

通过复制`other`构建 QJniArray。两个 QJniArray 对象将引用同一个 Java 数组对象。
只有当`other`的元素类型`Other`可转换为正在构建的QJniArray的元素类型`T`时，才参与重载决议。但实际上不会发生转换。

### `[explicit] QJniArray::QJniArray(const QJniObject &object)`

**作用与语义：**

构造一个 QJniArray，包裹与 `object` 相同的 Java 数组，创建新的全局引用。要从现有的本地引用构造 QJniArray，可以使用通过 `fromLocalRef()` 构建的`QJniObject`。
注意：该构造函数不会验证 Java 端对象是否为正确类型的数组。访问不匹配的 QJniArray 会导致行为未定义。

### `[explicit] QJniArray::QJniArray(jarray array)`

**作用与语义：**

构建一个 QJniArray，包裹 Java 端数组`array`，创建新的全局引用`array`。
注意：该构造函数不会验证 Java 端对象是否为正确类型的数组。访问不匹配的 QJniArray 会导致行为未定义。

### `[default] QJniArray::QJniArray(std::initializer_list<T> &list)`

**作用与语义：**

构建一个QJniArray，将新创建的Java数组包裹类型为`T`的元素，并将`list`的数据填充到Java数组中。

### `QJniArray::~QJniArray()`

**作用与语义：**

销毁`QJniArray`对象，并释放所有对包裹后的 Java 数组的引用。

### `auto QJniArray::arrayObject() const`

**作用与语义：**

返回包裹后的 Java 对象，作为与该`QJniArray`对象的元素类型`jarray` `T`匹配的合适类型返回。
- `T`：jarray型
- `jbyte`：jbyteArray
- `jchar`：jcharArray
- `...`：...
- `jobject`：jobjectArray
- `QJniObject`：jobjectArray
- `Q_DECLARE_JNI_CLASS`：jobjectArray

### `[noexcept] QJniArray<T>::const_iterator QJniArray::cbegin() const`

**作用与语义：**

返回一个STL风格的const迭代子，指向数组中的第一个项。
如果数组被`invalid`，则返回与对应`end()`函数相同的迭代器。

### `[noexcept] QJniArray<T>::const_iterator QJniArray::cend() const`

**作用与语义：**

返回一个STL风格的迭代器，指向列表中最后一项之后。

### `[noexcept] QJniArray<T>::const_reverse_iterator QJniArray::crbegin() const`

**作用与语义：**

返回一个STL风格的反向迭代器，指向数组中的第一个项，顺序相反。
如果数组`invalid`，则返回与对应`rend()`函数相同的迭代器。
注意：使用 `operator->()` 访问反迭代器元素需要 C 20，因为 C 17 `reverse_iterator` 不支持返回代理对象的迭代器。

### `[noexcept] QJniArray<T>::const_reverse_iterator QJniArray::crend() const`

**作用与语义：**

返回一个STL风格的反向迭代器，指向列表中最后一个项之后，顺序相反。
注意：使用`operator->()`访问反迭代子元素需要C 20，因为C 17 `reverse_iterator`不支持返回代理对象的迭代器。

### `template <typename Container = QJniArrayBase::ToContainerType<T>, QJniArrayBase::if_compatible_target_container<T, Container> = true> Container QJniArray::toContainer(Container &&container = {}) const`

**作用与语义：**

返回一个容器，填充了包裹后的 Java 数组中的数据。
如果没有提供`container`，则返回的容器类型取决于该`QJniArray`的元素类型。对于`QJniArray<T>`，通常会是`QList<T>`，但有以下例外：
- `Specialization`：C型
- `QJniArray`<jbyte>`: `QByteArray'
- `QJniArray`<char>`: `QByteArray'
- `QJniArray`<jstring>`: `QStringList'
- `QJniArray`<`QString`>`: `QStringList'
如果你输入一个命名容器（lvalue）作为`container`，那么该容器被填充，并返回对它的引用。如果你传递一个临时容器（r值，包含默认参数），那么该容器被填充，并返回值。
如果数组`invalid`，该函数会立即返回。

### `[noexcept] template <typename Other, QJniArrayBase::if_convertible<Other, T> = true> QJniArray<T> &QJniArray::operator=(QJniArray<Other> &&other)`

**作用与语义：**

`other`移动到该`QJniArray`，并返回对此的引用。`other`数组变为`invalid`。
只有当`other`的元素类型`Other`可转换为本`QJniArray`的元素类型`T`时，才参与重载决议。但实际不会发生转换。

### `template <typename Other, QJniArrayBase::if_convertible<Other, T> = true> QJniArray<T> &QJniArray::operator=(const QJniArray<Other> &other)`

**作用与语义：**

将`other`分配到该`QJniArray`，并返回引用。两个`QJniArray`对象将引用同一个Java数组对象。
只有当`other`的元素类型`Other`可转换为该`QJniArray`的元素类型`T`时，才参与重载决议。但实际不会发生转换。

### `[since 6.9] QJniArray<T>::reference QJniArray::operator[](QJniArrayBase::size_type i)`

**作用与语义：**

返回一个引用对象，位于包裹后的 Java 数组中位置 `i`。
`i`必须是列表中有效的索引位置（即0 <= `i` < `size()`）。
返回的引用对象保持位置`i`的值，在大多数情况下会隐式转换为该值。赋值到返回的引用会覆盖 Java 数组中的该项。然而，调用对象上的变异成员函数不会修改数组中的条目。要调用该操作符的结果的成员函数，请取消引用对象：
然而，如果不打算修改数组中的值，请将数组设为const，或者改用`at()`。

**官方示例：**

```cpp
 QJniArray<QString> strings = object.callMethod<QString[]>("getStrings");
 if (!strings.isEmpty()) {
     if (!(*array[0]).isEmpty()) {
         // ...
     }
 }
```

### `QJniArray<T>::const_reference QJniArray::at(QJniArrayBase::size_type i) const`

**作用与语义：**

返回包裹后的 Java 数组中位置 `i` 的值。
`i` 必须是列表中有效的索引位置（即 0 <= `i` < `size()`）。

### `const_iterator`

**作用与语义：**

一个随机访问迭代器用于`QJniArray`。/*。
/*!
一个随机存取、连续迭代器用于`QJniArray`。

### `const_reverse_iterator`

**作用与语义：**

`QJniArray`的反迭代器，`std::reverse_iterator<iterator>`的同义词。
注意：使用`operator->()`访问反迭代子元素需要C 20，因为C 17 `reverse_iterator`不支持返回代理对象的迭代器。/*。
/*!
`QJniArray`的反迭代器，`std::reverse_iterator<const_iterator>`的同义词。
注意：使用`operator->()`访问反迭代器元素需要C 20，因为C 17 `reverse_iterator`不支持返回代理对象的迭代器。

### `iterator`

**作用与语义：**

一个随机访问迭代器用于`QJniArray`。/*。
/*!
一个随机存取、连续迭代器用于`QJniArray`。

### `reverse_iterator`

**作用与语义：**

`QJniArray`的反迭代器，`std::reverse_iterator<iterator>`的同义词。
注意：使用`operator->()`访问反迭代子元素需要C 20，因为C 17 `reverse_iterator`不支持返回代理对象的迭代器。/*。
/*!
`QJniArray`的反迭代器，`std::reverse_iterator<const_iterator>`的同义词。
注意：使用`operator->()`访问反迭代器元素需要C 20，因为C 17 `reverse_iterator`不支持返回代理对象的迭代器。

### `QJniArray<T>::iterator begin()`

**作用与语义：**

返回一个STL风格的const迭代子，指向数组中的第一个项。
如果数组被`invalid`，则返回与对应`end()`函数相同的迭代器。

### `QJniArray<T>::const_iterator begin() const`

**作用与语义：**

返回一个STL风格的const迭代子，指向数组中的第一个项。
如果数组被`invalid`，则返回与对应`end()`函数相同的迭代器。

### `QJniArray<T>::const_iterator constBegin() const`

**作用与语义：**

返回一个STL风格的const迭代子，指向数组中的第一个项。
如果数组被`invalid`，则返回与对应`end()`函数相同的迭代器。

### `QJniArray<T>::const_iterator constEnd() const`

**作用与语义：**

返回一个STL风格的迭代器，指向列表中最后一项之后。

### `QJniArray<T>::iterator end()`

**作用与语义：**

返回一个STL风格的迭代器，指向列表中最后一项之后。

### `QJniArray<T>::const_iterator end() const`

**作用与语义：**

返回一个STL风格的迭代器，指向列表中最后一项之后。

### `QJniArray<T>::reverse_iterator rbegin()`

**作用与语义：**

返回一个STL风格的反向迭代器，指向数组中的第一个项，顺序相反。
如果数组`invalid`，则返回与对应`rend()`函数相同的迭代器。
注意：使用 `operator->()` 访问反迭代器元素需要 C 20，因为 C 17 `reverse_iterator` 不支持返回代理对象的迭代器。

### `QJniArray<T>::const_reverse_iterator rbegin() const`

**作用与语义：**

返回一个STL风格的反向迭代器，指向数组中的第一个项，顺序相反。
如果数组`invalid`，则返回与对应`rend()`函数相同的迭代器。
注意：使用 `operator->()` 访问反迭代器元素需要 C 20，因为 C 17 `reverse_iterator` 不支持返回代理对象的迭代器。

### `QJniArray<T>::reverse_iterator rend()`

**作用与语义：**

返回一个STL风格的反向迭代器，指向列表中最后一个项之后，顺序相反。
注意：使用`operator->()`访问反迭代子元素需要C 20，因为C 17 `reverse_iterator`不支持返回代理对象的迭代器。

### `QJniArray<T>::const_reverse_iterator rend() const`

**作用与语义：**

返回一个STL风格的反向迭代器，指向列表中最后一个项之后，顺序相反。
注意：使用`operator->()`访问反迭代子元素需要C 20，因为C 17 `reverse_iterator`不支持返回代理对象的迭代器。

### `QJniArray<T>::const_reference operator[](QJniArrayBase::size_type i) const`

**作用与语义：**

返回包裹后的 Java 数组中位置 `i` 的值。
`i` 必须是列表中有效的索引位置（即 0 <= `i` < `size()`）。

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

`QJniArray` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
