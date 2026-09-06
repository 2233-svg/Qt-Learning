# QCborArray

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Cbor数组”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCborArray` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCborArray>`
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

- `class ConstIterator`
- `class Iterator`
- `const_iterator`
- `const_pointer`
- `const_reference`
- `difference_type`
- `iterator`
- `pointer`
- `reference`
- `size_type`
- `value_type`

### 公有函数

- `QCborArray()`
- `QCborArray(std::initializer_list<QCborValue> args)`
- `QCborArray(const QCborArray &other)`
- `(since 6.10) QCborArray(QCborArray &&other)`
- `~QCborArray()`
- `void append(QCborValue &&value)`
- `void append(const QCborValue &value)`
- `QCborValue at(qsizetype i) const`
- `QCborArray::iterator begin()`
- `QCborArray::const_iterator begin() const`
- `QCborArray::const_iterator cbegin() const`
- `QCborArray::const_iterator cend() const`
- `void clear()`
- `int compare(const QCborArray &other) const`
- `QCborArray::const_iterator constBegin() const`
- `QCborArray::const_iterator constEnd() const`
- `bool contains(const QCborValue &value) const`
- `bool empty() const`
- `QCborArray::iterator end()`
- `QCborArray::const_iterator end() const`
- `QCborArray::iterator erase(QCborArray::const_iterator it)`
- `QCborArray::iterator erase(QCborArray::iterator it)`
- `QCborValue extract(QCborArray::ConstIterator it)`
- `QCborValue extract(QCborArray::Iterator it)`
- `QCborValueRef first()`
- `QCborValue first() const`
- `void insert(qsizetype i, QCborValue &&value)`
- `void insert(qsizetype i, const QCborValue &value)`
- `QCborArray::iterator insert(QCborArray::const_iterator before, const QCborValue &value)`
- `QCborArray::iterator insert(QCborArray::iterator before, const QCborValue &value)`
- `bool isEmpty() const`
- `QCborValueRef last()`
- `QCborValue last() const`
- `void pop_back()`
- `void pop_front()`
- `void prepend(QCborValue &&value)`
- `void prepend(const QCborValue &value)`
- `void push_back(const QCborValue &t)`
- `void push_front(const QCborValue &t)`
- `void removeAt(qsizetype i)`
- `void removeFirst()`
- `void removeLast()`
- `qsizetype size() const`
- `void swap(QCborArray &other)`
- `QCborValue takeAt(qsizetype i)`
- `QCborValue takeFirst()`
- `QCborValue takeLast()`
- `QCborValue toCborValue() const`
- `QJsonArray toJsonArray() const`
- `QVariantList toVariantList() const`
- `QCborArray operator+(const QCborValue &v) const`
- `QCborArray & operator+=(const QCborValue &v)`
- `QCborArray & operator<<(const QCborValue &v)`
- `(since 6.10) QCborArray & operator=(QCborArray &&other)`
- `QCborArray & operator=(const QCborArray &other)`
- `QCborValueRef operator[](qsizetype i)`
- `const QCborValue operator[](qsizetype i) const`

### 静态公有成员

- `QCborArray fromJsonArray(const QJsonArray &array)`
- `(since 6.3) QCborArray fromJsonArray(QJsonArray &&array)`
- `QCborArray fromStringList(const QStringList &list)`
- `QCborArray fromVariantList(const QVariantList &list)`

### 相关非成员函数

- `bool operator!=(const QCborArray &lhs, const QCborArray &rhs)`
- `bool operator<(const QCborArray &lhs, const QCborArray &rhs)`
- `bool operator<=(const QCborArray &lhs, const QCborArray &rhs)`
- `bool operator==(const QCborArray &lhs, const QCborArray &rhs)`
- `bool operator>(const QCborArray &lhs, const QCborArray &rhs)`
- `bool operator>=(const QCborArray &lhs, const QCborArray &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QCborArray::const_iterator`

**作用与语义：**

`QCborArray::ConstIterator`的同义词。

### `QCborArray::const_pointer`

**作用与语义：**

一个类型def到`const QCborValue *`，以兼容通用算法。

### `QCborArray::const_reference`

**作用与语义：**

对`const QCborValue &`的类型定义，以保证与通用算法的兼容性。

### `QCborArray::difference_type`

**作用与语义：**

Typedef 到 qsizetype。

### `QCborArray::iterator`

**作用与语义：**

`QCborArray::Iterator`的同义词。

### `QCborArray::pointer`

**作用与语义：**

一个类型定义到`QCborValue *`，以保证与通用算法的兼容性。

### `QCborArray::reference`

**作用与语义：**

一个类型定义（typedef）到`QCborValue &`，以保证与通用算法的兼容性。

### `QCborArray::size_type`

**作用与语义：**

Typedef 到 qsizetype。

### `QCborArray::value_type`

**作用与语义：**

`QCborArray`中可以保持的值类型：即`QCborValue`。

### `[noexcept] QCborArray::QCborArray()`

**作用与语义：**

构造一个空的QCborArray。

### `QCborArray::QCborArray(std::initializer_list<QCborValue> args)`

**作用与语义：**

从`args`中发现的C大括号封闭列表初始化该QCbor数组，如下示例所示：

**官方示例：**

```cpp
 QCborArray a = { null, 0, 1, 1.5, 2, "Hello", QByteArray("World") };
```

### `[noexcept] QCborArray::QCborArray(const QCborArray &other)`

**作用与语义：**

将`other`的内容复制到该对象中。

### `[constexpr noexcept, since 6.10] QCborArray::QCborArray(QCborArray &&other)`

**作用与语义：**

移动构造者。
移除对象`other`置于默认构造状态。

### `[noexcept] QCborArray::~QCborArray()`

**作用与语义：**

摧毁`QCborArray`并释放所有相关资源。

### `void QCborArray::append(QCborValue &&value)`

**作用与语义：**

在数组可能包含的所有其他元素之后附加`value`。

### `QCborValue QCborArray::at(qsizetype i) const`

**作用与语义：**

返回数组中位置`i`的`QCborValue`元素。
如果数组小于`i`个元素，该函数返回一个包含未定义值的`QCborValue`。因此，使用该函数无法区分数组不够大的情况和数组起始于未定义值的情况。

### `QCborArray::iterator QCborArray::begin()`

**作用与语义：**

返回指向该数组中第一个项的数组迭代器。如果数组为空，则返回与 `end()` 相同的结果。

### `QCborArray::const_iterator QCborArray::begin() const`

**作用与语义：**

返回指向该数组中第一个项的数组迭代器。如果数组为空，则返回与 `end()` 相同的结果。

### `QCborArray::const_iterator QCborArray::cbegin() const`

**作用与语义：**

返回指向该数组中第一个项的数组迭代器。如果数组为空，则返回与 `end()` 相同的结果。

### `QCborArray::const_iterator QCborArray::cend() const`

**作用与语义：**

返回一个数组迭代器，指向该数组最后一个元素之后。

### `void QCborArray::clear()`

**作用与语义：**

清空这个阵列。

### `[noexcept] int QCborArray::compare(const QCborArray &other) const`

**作用与语义：**

比较该数组与`other`，按顺序比较每个元素，返回一个整数，表示该数组应在结果为负时应在`other`之后排序（如果结果为正）。如果该函数返回0，则两个数组相等且包含相同元素。
有关CBOR排序顺序的更多信息，请参见`QCborValue::compare()`。

### `QCborArray::const_iterator QCborArray::constBegin() const`

**作用与语义：**

返回指向该数组中第一个项的数组迭代器。如果数组为空，则返回与 `end()` 相同的结果。

### `QCborArray::const_iterator QCborArray::constEnd() const`

**作用与语义：**

返回一个数组迭代器，指向该数组最后一个元素之后。

### `bool QCborArray::contains(const QCborValue &value) const`

**作用与语义：**

如果该数组包含等于 `value` 的元素，则返回为真。

### `bool QCborArray::empty() const`

**作用与语义：**

`isEmpty()`的同义词。该功能是为了兼容使用标准库 API 的通用代码而提供。
如果该数组为空，则返回为真（`size()` == 0）。

### `QCborArray::iterator QCborArray::end()`

**作用与语义：**

返回一个数组迭代器，指向该数组最后一个元素之后。

### `QCborArray::const_iterator QCborArray::end() const`

**作用与语义：**

返回一个数组迭代器，指向该数组最后一个元素之后。

### `QCborArray::iterator QCborArray::erase(QCborArray::const_iterator it)`

**作用与语义：**

从该数组中移除数组迭代器指向的元素，`it`返回下一个元素（即`it`曾占据的数组中相同位置的元素）。

### `QCborValue QCborArray::extract(QCborArray::ConstIterator it)`

**作用与语义：**

从迭代子`it`指示的位置从数组中提取一个值，并返回该值。

### `QCborValueRef QCborArray::first()`

**作用与语义：**

返回该数组的第一个`QCborValue`的引用。该数组不得为空。
QCborValueRef 的 API 与 `QCborValue` 完全相同，但有一个重要区别：如果你给它赋值，这个数组会更新为该新值。

### `QCborValue QCborArray::first() const`

**作用与语义：**

返回该数组的第一个`QCborValue`。
如果数组为空，该函数返回一个包含未定义值的`QCborValue`。因此，使用该函数无法区分数组不够大的情况和数组末尾未定义值的情况。

### `[static] QCborArray QCborArray::fromJsonArray(const QJsonArray &array)`

**作用与语义：**

使用 QCborValue：：fromJson() 将 `array` 数组中的所有 JSON 项转换为 CBOR，并返回由这些元素组成的 CBOR 数组。
该转换是无损的，因为 CBOR 类型系统是 JSON 的超集。此外，该函数返回的数组可以通过 `toJsonArray()` 转换回原始 `array`。

### `[static noexcept, since 6.3] QCborArray QCborArray::fromJsonArray(QJsonArray &&array)`

**作用与语义：**

使用 QCborValue：：fromJson() 将 `array` 数组中的所有 JSON 项转换为 CBOR，并返回由这些元素组成的 CBOR 数组。
该转换是无损的，因为 CBOR 类型系统是 JSON 的超集。此外，该函数返回的数组可以通过 `toJsonArray()` 转换回原始 `array`。

### `[static] QCborArray QCborArray::fromStringList(const QStringList &list)`

**作用与语义：**

返回包含`list`列表中所有字符串的`QCborArray`。

### `[static] QCborArray QCborArray::fromVariantList(const QVariantList &list)`

**作用与语义：**

利用 `QCborValue::fromVariant()` 将`list`中的所有项目转换为 CBOR，并返回由这些元素组成的数组。
从`QVariant`转换并非完全无损。更多信息请参见`QCborValue::fromVariant()`文档。

### `void QCborArray::insert(qsizetype i, QCborValue &&value)`

**作用与语义：**

将`value`插入到该数组中位置`i`的数组。如果`i`为-1，则该项被附加到数组中。如果`i`大于数组的前置大小，则用无效的条目填充数组。

### `QCborArray::iterator QCborArray::insert(QCborArray::const_iterator before, const QCborValue &value)`

**作用与语义：**

将`value`插入到该数组中位置`i`的数组。如果`i`为-1，则该项被附加到数组中。如果`i`大于数组的前置大小，则用无效的条目填充数组。

### `bool QCborArray::isEmpty() const`

**作用与语义：**

如果该`QCborArray`为空（即 `size()` 为 0），则返回 true。

### `QCborValueRef QCborArray::last()`

**作用与语义：**

返回该数组的最后一个`QCborValue`引用。该数组不得为空。
QCborValueRef 的 API 与 `QCborValue` 完全相同，但有一个重要区别：如果你给它分配了新值，这个数组会更新为该新值。

### `QCborValue QCborArray::last() const`

**作用与语义：**

返回该阵列的最后一个`QCborValue`。
如果数组为空，该函数返回一个包含未定义值的`QCborValue`。因此，使用该函数无法区分数组不够大的情况和数组结尾未定义值的情况。

### `void QCborArray::pop_back()`

**作用与语义：**

`removeLast()`的同义词。该功能是为了兼容使用标准库API的通用代码而提供。
移除该数组的最后一个元素。数组在移除前不得为空。

### `void QCborArray::pop_front()`

**作用与语义：**

`removeFirst()`的同义词。此功能是为了兼容使用标准库API的通用代码而提供。
移除该数组的第一个元素。在移除前，数组不得为空。

### `void QCborArray::prepend(QCborValue &&value)`

**作用与语义：**

在数组中`value`前插入，先于其可能包含的其他元素。

### `void QCborArray::push_back(const QCborValue &t)`

**作用与语义：**

`append()`的同义词。该功能是为了兼容使用标准库 API 的通用代码而提供。
将元素 `t` 附加到该数组上。

### `void QCborArray::push_front(const QCborValue &t)`

**作用与语义：**

`prepend()`的同义词。该功能是为了兼容使用标准库API的通用代码而提供。
在该数组前加上元素 `t`。

### `void QCborArray::removeAt(qsizetype i)`

**作用与语义：**

从数组中移除位置`i`的元素。数组在移除前必须包含超过`i`个元素。

### `void QCborArray::removeFirst()`

**作用与语义：**

移除数组中的第一个元素，使第二个元素变为第一个。在调用此之前，数组不得为空。

### `void QCborArray::removeLast()`

**作用与语义：**

移除数组中的最后一项。数组在此调用前不得为空。

### `[noexcept] qsizetype QCborArray::size() const`

**作用与语义：**

返回该数组的大小。

### `[noexcept] void QCborArray::swap(QCborArray &other)`

**作用与语义：**

将该阵列与`other`交换。此操作非常快速且从未失败。

### `QCborValue QCborArray::takeAt(qsizetype i)`

**作用与语义：**

从数组中移除位置`i`的元素并返回。数组在移除前必须包含超过`i`个元素。

### `QCborValue QCborArray::takeFirst()`

**作用与语义：**

移除数组中的第一个项并返回，使第二个元素成为第一个。数组在此调用前不得为空。

### `QCborValue QCborArray::takeLast()`

**作用与语义：**

移除数组中的最后一项并返回。在调用之前，数组不得为空。

### `QCborValue QCborArray::toCborValue() const`

**作用与语义：**

显式构建一个表示该数组的`QCborValue`对象。该函数通常不必要，因为`QCborValue`有构造函数表示`QCborArray`，转换是隐式的。
将 `QCborArray` 转换为 `QCborValue` 使其能够在任何使用 QCborValue 的上下文中使用，包括作为 QCborArrays 中的项，以及作为 `QCborMap` 中的键和映射类型。将数组转换为 `QCborValue` 则允许访问 `QCborValue::toCbor()`。

### `QJsonArray QCborArray::toJsonArray() const`

**作用与语义：**

递归地将该数组中的每个`QCborValue`元素用`QCborValue::toJsonValue()`转换为JSON，并返回由这些元素组成的对应`QJsonArray`。
请注意，CBOR 的类型集比 JSON 更丰富且更宽，因此在此转换过程中可能会丢失一些信息。有关应用的转换详情，请参见 `QCborValue::toJsonValue()`。

### `QVariantList QCborArray::toVariantList() const`

**作用与语义：**

递归地使用`QCborValue::toVariant()`转换该数组中的每个`QCborValue`，并返回由转换后的项组成的`QVariantList`。
转换为`QVariant`并非完全无损。更多信息请参见`QCborValue::toVariant()`文档。

### `QCborArray QCborArray::operator+(const QCborValue &v) const`

**作用与语义：**

返回一个新`QCborArray`，包含与该数组相同的元素，加上最后一个元素`v`。

### `QCborArray &QCborArray::operator+=(const QCborValue &v)`

**作用与语义：**

将`v`附加到该数组并返回对该数组的引用。

### `QCborArray &QCborArray::operator<<(const QCborValue &v)`

**作用与语义：**

将`v`附加到该数组并返回对该数组的引用。

### `[noexcept, since 6.10] QCborArray &QCborArray::operator=(QCborArray &&other)`

**作用与语义：**

移动分配操作员。
被移出的对象`other`处于有效但未指定状态。

### `[noexcept] QCborArray &QCborArray::operator=(const QCborArray &other)`

**作用与语义：**

用`other`中的内容替换该数组的内容，然后返回对该对象的引用。

### `QCborValueRef QCborArray::operator[](qsizetype i)`

**作用与语义：**

返回数组中位置`i`的`QCborValue`元素的引用。数组末端以外的索引会不断扩大，填充未定义的条目，直到在指定索引处有条目。
QCborValueRef 的 API 与 `QCborValue` 完全相同，但有一个重要区别：如果你给它赋值，这个数组会更新为该值。

### `const QCborValue QCborArray::operator[](qsizetype i) const`

**作用与语义：**

返回数组中位置`i`的`QCborValue`元素。
如果数组小于`i`个元素，该函数返回一个包含未定义值的`QCborValue`。因此，使用该函数无法区分数组不够大的情况与数组在位置`i`存在未定义值的情况。

### `[noexcept] bool operator!=(const QCborArray &lhs, const QCborArray &rhs)`

**作用与语义：**

比较`lhs`和`rhs`数组，按顺序比较每个元素，若两组内容不同则返回真，否则返回为假。
有关量化税中CBOR等价的更多信息，请参见`QCborValue::compare()`。

### `[noexcept] bool operator<(const QCborArray &lhs, const QCborArray &rhs)`

**作用与语义：**

比较`lhs`和`rhs`数组，按顺序比较每个元素，如果数组应在`rhs`前排序`lhs`则返回为真，否则返回为假。
有关CBOR排序顺序的更多信息，请参见 `QCborValue::compare()`。

### `[noexcept] bool operator<=(const QCborArray &lhs, const QCborArray &rhs)`

**作用与语义：**

比较`lhs`和`rhs`数组，按顺序比较每个元素，如果`lhs`数组应在`rhs`前排序，或两个数组包含相同元素，则返回为真，否则返回。
有关CBOR排序顺序的更多信息，请参见 `QCborValue::compare()`。

### `[noexcept] bool operator==(const QCborArray &lhs, const QCborArray &rhs)`

**作用与语义：**

比较`lhs`和`rhs`数组，按顺序比较每个元素，若两个数组包含相同元素则返回为真，否则返回为假。
关于Qt中CBOR等价的更多信息，请参见`QCborValue::compare()`。

### `[noexcept] bool operator>(const QCborArray &lhs, const QCborArray &rhs)`

**作用与语义：**

比较`lhs`和`rhs`数组，按顺序比较每个元素，如果数组在`rhs`后应排序`lhs`则返回为真，否则返回为false。
有关CBOR排序顺序的更多信息，请参见 `QCborValue::compare()`。

### `[noexcept] bool operator>=(const QCborArray &lhs, const QCborArray &rhs)`

**作用与语义：**

比较`lhs`和`rhs`数组，按顺序比较每个元素，如果数组在`rhs`后排序，则返回`lhs`，或者两个数组包含相同元素，否则返回为真。
有关CBOR排序顺序的更多信息，请参见 `QCborValue::compare()`。

### `class ConstIterator`

**作用与语义：**

QCborArray：：ConstIterator 类为 QCborArray 提供了一个 STL 风格的 const 迭代器。
`QCborArray::ConstIterator`允许你对`QCborArray`进行迭代。如果你想在迭代时修改`QCborArray`，可以用`QCborArray::Iterator`。通常情况下，即使是在非const `QCborArray`上，当不需要通过迭代器更改`QCborArray`时，使用`QCborArray::ConstIterator`也是个好习惯。Const迭代器速度稍快，并且提高了代码的可读性。
迭代器通过使用`QCborArray`函数如`QCborArray::begin()`或`QCborArray::end()`初始化。迭代只能在此之后进行。
大多数`QCborArray`函数接受整数索引而非迭代器。因此，迭代器很少与`QCborArray`联系起来有用。STL风格的迭代器在一个有意义的地方是作为通用算法的参数。
多个迭代器可以用于同一个数组。但请注意，任何对`QCborArray`执行的非const函数调用都会使所有现有迭代器未定义。

### `class Iterator`

**作用与语义：**

QCborArray：：Iterator 类为 QCborArray 提供了一个 STL 风格的非const 迭代器。
`QCborArray::Iterator`允许你对`QCborArray`进行迭代，并修改与迭代器关联的数组项。如果你想对const的迭代`QCborArray`，可以用`QCborArray::ConstIterator`。通常在非const的`QCborArray`上使用`QCborArray::ConstIterator`是个好习惯，除非你需要通过迭代器更改`QCborArray`。const迭代器速度稍快，并且提高了代码的可读性。
迭代器通过使用`QCborArray`函数如`QCborArray::begin()`、`QCborArray::end()`或`QCborArray::insert()`初始化。迭代只能在此之后进行。
大多数`QCborArray`函数接受整数索引而非迭代器。因此，迭代器很少与`QCborArray`相关。STL式迭代器在一个合理的地方是作为通用算法的参数。
多个迭代器可以用于同一个数组。但请注意，任何对`QCborArray`执行的非const函数调用都会使所有现有迭代器未定义。

### `const_iterator`

**作用与语义：**

`QCborArray::ConstIterator`的同义词。

### `const_pointer`

**作用与语义：**

一个类型def到`const QCborValue *`，以兼容通用算法。

### `const_reference`

**作用与语义：**

对`const QCborValue &`的类型定义，以保证与通用算法的兼容性。

### `difference_type`

**作用与语义：**

Typedef 到 qsizetype。

### `iterator`

**作用与语义：**

`QCborArray::Iterator`的同义词。

### `pointer`

**作用与语义：**

一个类型定义到`QCborValue *`，以保证与通用算法的兼容性。

### `reference`

**作用与语义：**

一个类型定义（typedef）到`QCborValue &`，以保证与通用算法的兼容性。

### `size_type`

**作用与语义：**

Typedef 到 qsizetype。

### `value_type`

**作用与语义：**

`QCborArray`中可以保持的值类型：即`QCborValue`。

### `void append(const QCborValue &value)`

**作用与语义：**

在数组可能包含的所有其他元素之后附加`value`。

### `QCborArray::iterator erase(QCborArray::iterator it)`

**作用与语义：**

从该数组中移除数组迭代器指向的元素，`it`返回下一个元素（即`it`曾占据的数组中相同位置的元素）。

### `QCborValue extract(QCborArray::Iterator it)`

**作用与语义：**

从迭代子`it`指示的位置从数组中提取一个值，并返回该值。

### `void insert(qsizetype i, const QCborValue &value)`

**作用与语义：**

在元素`before`之前将`value`插入到该数组中，并返回指向刚插入的元素的数组迭代器。

### `QCborArray::iterator insert(QCborArray::iterator before, const QCborValue &value)`

**作用与语义：**

在元素`before`之前将`value`插入到该数组中，并返回指向刚插入的元素的数组迭代器。

### `void prepend(const QCborValue &value)`

**作用与语义：**

在数组中`value`前插入，先于其可能包含的其他元素。

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

`QCborArray` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
