# QCborMap

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Cbor映射”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCborMap` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCborMap>`
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
- `(since 6.10) const_key_value_iterator`
- `iterator`
- `key_type`
- `(since 6.10) key_value_iterator`
- `mapped_type`
- `size_type`
- `value_type`

### 公有函数

- `QCborMap()`
- `QCborMap(std::initializer_list<QCborMap::value_type> args)`
- `QCborMap(const QCborMap &other)`
- `(since 6.10) QCborMap(QCborMap &&other)`
- `~QCborMap()`
- `(since 6.10) auto asKeyValueRange() &&`
- `(since 6.10) auto asKeyValueRange() &`
- `(since 6.10) auto asKeyValueRange() const &&`
- `(since 6.10) auto asKeyValueRange() const &`
- `QCborMap::iterator begin()`
- `QCborMap::const_iterator begin() const`
- `QCborMap::const_iterator cbegin() const`
- `QCborMap::const_iterator cend() const`
- `void clear()`
- `int compare(const QCborMap &other) const`
- `QCborMap::const_iterator constBegin() const`
- `QCborMap::const_iterator constEnd() const`
- `QCborMap::const_iterator constFind(qint64 key) const`
- `QCborMap::const_iterator constFind(QLatin1StringView key) const`
- `QCborMap::const_iterator constFind(const QCborValue &key) const`
- `QCborMap::const_iterator constFind(const QString &key) const`
- `(since 6.10) QCborMap::const_key_value_iterator constKeyValueBegin() const`
- `(since 6.10) QCborMap::const_key_value_iterator constKeyValueEnd() const`
- `bool contains(const QCborValue &key) const`
- `bool contains(qint64 key) const`
- `bool contains(QLatin1StringView key) const`
- `bool contains(const QString &key) const`
- `bool empty() const`
- `QCborMap::iterator end()`
- `QCborMap::const_iterator end() const`
- `QCborMap::iterator erase(QCborMap::const_iterator it)`
- `QCborMap::iterator erase(QCborMap::iterator it)`
- `QCborValue extract(QCborMap::const_iterator it)`
- `QCborValue extract(QCborMap::iterator it)`
- `QCborMap::iterator find(qint64 key)`
- `QCborMap::const_iterator find(qint64 key) const`
- `QCborMap::iterator find(QLatin1StringView key)`
- `QCborMap::iterator find(const QCborValue &key)`
- `QCborMap::iterator find(const QString &key)`
- `QCborMap::const_iterator find(QLatin1StringView key) const`
- `QCborMap::const_iterator find(const QCborValue &key) const`
- `QCborMap::const_iterator find(const QString &key) const`
- `QCborMap::iterator insert(QCborMap::value_type v)`
- `QCborMap::iterator insert(QLatin1StringView key, const QCborValue &value)`
- `QCborMap::iterator insert(const QCborValue &key, const QCborValue &value)`
- `QCborMap::iterator insert(const QString &key, const QCborValue &value)`
- `QCborMap::iterator insert(qint64 key, const QCborValue &value)`
- `bool isEmpty() const`
- `(since 6.10) QCborMap::key_value_iterator keyValueBegin()`
- `(since 6.10) QCborMap::const_key_value_iterator keyValueBegin() const`
- `(since 6.10) QCborMap::key_value_iterator keyValueEnd()`
- `(since 6.10) QCborMap::const_key_value_iterator keyValueEnd() const`
- `QList<QCborValue> keys() const`
- `void remove(const QCborValue &key)`
- `void remove(qint64 key)`
- `void remove(QLatin1StringView key)`
- `void remove(const QString &key)`
- `qsizetype size() const`
- `void swap(QCborMap &other)`
- `QCborValue take(QLatin1StringView key)`
- `QCborValue take(const QCborValue &key)`
- `QCborValue take(const QString &key)`
- `QCborValue take(qint64 key)`
- `QCborValue toCborValue() const`
- `QJsonObject toJsonObject() const`
- `QVariantHash toVariantHash() const`
- `QVariantMap toVariantMap() const`
- `QCborValue value(const QCborValue &key) const`
- `QCborValue value(qint64 key) const`
- `QCborValue value(QLatin1StringView key) const`
- `QCborValue value(const QString &key) const`
- `(since 6.10) QCborMap & operator=(QCborMap &&other)`
- `QCborMap & operator=(const QCborMap &other)`
- `QCborValueRef operator[](qint64 key)`
- `const QCborValue operator[](const QCborValue &key) const`
- `const QCborValue operator[](qint64 key) const`
- `QCborValueRef operator[](QLatin1StringView key)`
- `QCborValueRef operator[](const QCborValue &key)`
- `QCborValueRef operator[](const QString &key)`
- `const QCborValue operator[](QLatin1StringView key) const`
- `const QCborValue operator[](const QString &key) const`

### 静态公有成员

- `QCborMap fromJsonObject(const QJsonObject &obj)`
- `(since 6.3) QCborMap fromJsonObject(QJsonObject &&obj)`
- `QCborMap fromVariantHash(const QVariantHash &hash)`
- `QCborMap fromVariantMap(const QVariantMap &map)`

### 相关非成员函数

- `bool operator!=(const QCborMap &lhs, const QCborMap &rhs)`
- `bool operator<(const QCborMap &lhs, const QCborMap &rhs)`
- `bool operator<=(const QCborMap &lhs, const QCborMap &rhs)`
- `bool operator==(const QCborMap &lhs, const QCborMap &rhs)`
- `bool operator>(const QCborMap &lhs, const QCborMap &rhs)`
- `bool operator>=(const QCborMap &lhs, const QCborMap &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QCborMap::const_iterator`

**作用与语义：**

`QCborMap::ConstIterator`的同义词。

### `[since 6.10] QCborMap::const_key_value_iterator`

**作用与语义：**

QCborMap：：const_key_value_iterator typedef 提供了一个 STL 风格的迭代器用于 `QCborMap`。
QCborMap：：const_key_value_iterator 本质上与 `QCborMap::const_iterator` 相同，但为与其他容器如 `QJsonObject` 实现对称而提供。
这种类型防御是在Qt 6.10中引入的。

### `QCborMap::iterator`

**作用与语义：**

`QCborMap::Iterator`的同义词。

### `QCborMap::key_type`

**作用与语义：**

该映射的密钥类型。由于`QCborMap`键可以是任何CBOR类型，这就是`QCborValue`。

### `[since 6.10] QCborMap::key_value_iterator`

**作用与语义：**

QCborMap::key_value_iterator 类型定义提供了一个 STL 风格的 `QCborMap` 迭代器。
QCborMap::key_value_iterator 本质上与 `QCborMap::iterator` 相同，但为了与 `QJsonObject` 等其他容器保持对称而提供。
此类型定义在 Qt 6.10 中引入。

### `QCborMap::mapped_type`

**作用与语义：**

映射到的类型（值），也就是`QCborValue`。

### `QCborMap::size_type`

**作用与语义：**

就是`QCborMap`用来测量尺寸的那种。

### `QCborMap::value_type`

**作用与语义：**

存储在此容器中的值：一对 QCborValues。

### `[noexcept] QCborMap::QCborMap()`

**作用与语义：**

构造一个空的CBOR映射对象。

### `QCborMap::QCborMap(std::initializer_list<QCborMap::value_type> args)`

**作用与语义：**

构建一个QCborMap，包含`args`中大括号初始化列表中的项，如下示例所示：

**官方示例：**

```cpp
 QCborMap map = {
     {0, "Hello"},
     {1, "World"},
     {"foo", nullptr},
     {"bar", QCborArray{0, 1, 2, 3, 4}}
 };
```

### `[noexcept] QCborMap::QCborMap(const QCborMap &other)`

**作用与语义：**

创建一个 QCborMap 对象，它是 `other` 的副本。

### `[constexpr noexcept, since 6.10] QCborMap::QCborMap(QCborMap &&other)`

**作用与语义：**

移动构造者。
移除对象`other`置于默认构造状态。

### `[noexcept] QCborMap::~QCborMap()`

**作用与语义：**

摧毁该`QCborMap`对象并释放其拥有的所有相关资源。

### `[since 6.10] auto QCborMap::asKeyValueRange() const &&`

**作用与语义：**

返回一个范围对象，允许对该映射进行键值对的迭代。
注意，通过这种方式获得的值是映射中值的引用。具体来说，变异值会修改映射本身。

### `QCborMap::iterator QCborMap::begin()`

**作用与语义：**

返回指向该映射的第一个键值对的映射迭代器。如果该映射为空，返回的迭代子将与`end()`相同。

### `QCborMap::const_iterator QCborMap::begin() const`

**作用与语义：**

返回一个映射迭代器，指向该映射的第一个键值对。如果该映射为空，返回的迭代器将与`constEnd()`相同。

### `QCborMap::const_iterator QCborMap::cbegin() const`

**作用与语义：**

返回一个映射迭代器，指向该映射的第一个键值对。如果该映射为空，返回的迭代器将与`constEnd()`相同。

### `QCborMap::const_iterator QCborMap::cend() const`

**作用与语义：**

返回一个映射迭代器，表示映射中最后一个元素之后的元素。

### `void QCborMap::clear()`

**作用与语义：**

清空这张地图。

### `[noexcept] int QCborMap::compare(const QCborMap &other) const`

**作用与语义：**

比较该映射与`other`，按顺序比较每个元素，返回一个整数，指示该映射应在 之前排序（结果为负时）还是在 `other` 之后排序（如果结果为正）。如果该函数返回 0，则两个映射相等且包含相同元素。
注意，CBOR 映射是无序的，这意味着包含相同对但顺序不同的映射仍然会有不同的比较。为避免这种情况，建议以可预测的顺序插入元素，例如按键值递增。事实上，规范的 CBOR 表示需要键按排序的映射。
有关CBOR排序顺序的更多信息，请参见 `QCborValue::compare()`。

### `QCborMap::const_iterator QCborMap::constBegin() const`

**作用与语义：**

返回一个映射迭代器，指向该映射的第一个键值对。如果该映射为空，返回的迭代器将与`constEnd()`相同。

### `QCborMap::const_iterator QCborMap::constEnd() const`

**作用与语义：**

返回一个映射迭代器，表示映射中最后一个元素之后的元素。

### `QCborMap::const_iterator QCborMap::constFind(qint64 key) const`

**作用与语义：**

如果映射包含键为`key`的键值对，返回映射迭代器。如果没有，该函数返回`constEnd()`。
CBOR 建议使用整数密钥，因为它们占用空间更小，编码和解码更简单。
如果映射包含多个等于 `key` 的键，函数将找到哪一个则未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流来创建此类映射。通常不允许重复键，且重复键通常表明发送端存在问题。

### `QCborMap::const_iterator QCborMap::constFind(QLatin1StringView key) const`

**作用与语义：**

如果映射包含该对，返回键为`key`的键值对的映射迭代器。如果没有，该函数返回`constEnd()`。
如果映射包含多个等于 `key` 的键，函数将找到哪个键则未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流创建此类映射。通常不允许重复键，且键重复通常表明发送端存在问题。

### `QCborMap::const_iterator QCborMap::constFind(const QCborValue &key) const`

**作用与语义：**

如果映射包含该对，返回键为`key`的键值对的映射迭代器。如果没有，该函数返回`constEnd()`。
如果映射包含多个等于 `key` 的键，函数将找到哪个键则未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流创建此类映射。通常不允许重复键，且键重复通常表明发送端存在问题。

### `QCborMap::const_iterator QCborMap::constFind(const QString &key) const`

**作用与语义：**

如果映射包含该对，返回键为`key`的键值对的映射迭代器。如果没有，该函数返回`constEnd()`。
如果映射包含多个等于 `key` 的键，函数将找到哪个键则未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流创建此类映射。通常不允许重复键，且键重复通常表明发送端存在问题。

### `[since 6.10] QCborMap::const_key_value_iterator QCborMap::constKeyValueBegin() const`

**作用与语义：**

返回一个const的STL风格迭代子，指向映射中的第一个条目。

### `[since 6.10] QCborMap::const_key_value_iterator QCborMap::constKeyValueEnd() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向映射中最后一个条目之后的虚数条目。

### `bool QCborMap::contains(const QCborValue &key) const`

**作用与语义：**

如果该映射包含由键`key`识别的键值对，则返回为真。

### `bool QCborMap::contains(qint64 key) const`

**作用与语义：**

如果该映射包含由键`key`标识的键值对，则返回为真。CBOR 建议使用整数键，因为它们占用空间更小且编码和解码更简单。

### `bool QCborMap::contains(QLatin1StringView key) const`

**作用与语义：**

如果该映射包含由键`key`识别的键值对，则返回为真。

### `bool QCborMap::contains(const QString &key) const`

**作用与语义：**

如果该映射包含由键`key`识别的键值对，则返回为真。

### `bool QCborMap::empty() const`

**作用与语义：**

`isEmpty()`的同义词。该功能是为了兼容使用标准库API的通用代码而提供。
如果该映射为空，则返回真（`size()` == 0）。

### `QCborMap::iterator QCborMap::end()`

**作用与语义：**

返回一个映射迭代器，表示映射中最后一个元素之后的元素。

### `QCborMap::const_iterator QCborMap::end() const`

**作用与语义：**

返回一个映射迭代器，表示映射中最后一个元素之后的元素。

### `QCborMap::iterator QCborMap::erase(QCborMap::const_iterator it)`

**作用与语义：**

移除映射迭代器指向的键值对`it`，并在移除后返回指向下一个元素的指针。

### `QCborMap::iterator QCborMap::erase(QCborMap::iterator it)`

**作用与语义：**

移除映射迭代器指向的键值对`it`，并在移除后返回指向下一个元素的指针。

### `QCborValue QCborMap::extract(QCborMap::const_iterator it)`

**作用与语义：**

从迭代器`it`指示的位置从映射中提取一个值，并返回该值。

### `QCborMap::const_iterator QCborMap::find(qint64 key) const`

**作用与语义：**

如果映射包含键为`key`的键值对，返回映射迭代器。如果没有，该函数返回`end()`。
CBOR 建议使用整数密钥，因为它们占用空间更小，编码和解码更简单。
如果映射包含多个等于 `key` 的键，则该函数将找到哪一个键未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流来创建此类映射。通常不允许重复键，且重复键通常表明发送端存在问题。

### `QCborMap::const_iterator QCborMap::find(QLatin1StringView key) const`

**作用与语义：**

如果映射包含键为`key`的键值对，返回映射迭代器。如果没有，该函数返回`end()`。
CBOR 建议使用整数密钥，因为它们占用空间更小，编码和解码更简单。
如果映射包含多个等于 `key` 的键，则该函数将找到哪一个键未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流来创建此类映射。通常不允许重复键，且重复键通常表明发送端存在问题。

### `QCborMap::const_iterator QCborMap::find(const QCborValue &key) const`

**作用与语义：**

返回键值为`key`的映射迭代器，如果映射包含该对。如果没有，该函数返回`end()`。
如果映射包含多个等于`key`的键，则该函数将找到哪一个键未定义。`QCborMap`不允许插入重复键，但可以通过解码包含它们的CBOR流来创建此类映射。通常不允许重复键，且重复键通常表明发送方存在问题。

### `QCborMap::const_iterator QCborMap::find(const QString &key) const`

**作用与语义：**

返回键值为`key`的映射迭代器，如果映射包含该对。如果没有，该函数返回`end()`。
如果映射包含多个等于`key`的键，则该函数将找到哪一个键未定义。`QCborMap`不允许插入重复键，但可以通过解码包含它们的CBOR流来创建此类映射。通常不允许重复键，且重复键通常表明发送方存在问题。

### `[static] QCborMap QCborMap::fromJsonObject(const QJsonObject &obj)`

**作用与语义：**

使用 QCborValue：：fromJson() 将 `obj` 对象中的所有 JSON 项转换为 CBOR，并返回由这些元素组成的映射。
该转换是无损的，因为 CBOR 类型系统是 JSON 的超集。此外，该函数返回的映射还可以通过使用 `toJsonObject()` 转换回原始`obj`。

### `[static noexcept, since 6.3] QCborMap QCborMap::fromJsonObject(QJsonObject &&obj)`

**作用与语义：**

使用 QCborValue：：fromJson() 将 `obj` 对象中的所有 JSON 项转换为 CBOR，并返回由这些元素组成的映射。
该转换是无损的，因为 CBOR 类型系统是 JSON 的超集。此外，该函数返回的映射还可以通过使用 `toJsonObject()` 转换回原始`obj`。

### `[static] QCborMap QCborMap::fromVariantHash(const QVariantHash &hash)`

**作用与语义：**

用`QCborValue::fromVariant()`将`hash`中的所有物品转换为CBOR，并返回由这些元素组成的地图。
从`QVariant`转换并非完全无损。更多信息请参见`QCborValue::fromVariant()`的文档。

### `[static] QCborMap QCborMap::fromVariantMap(const QVariantMap &map)`

**作用与语义：**

利用`QCborValue::fromVariant()`将`map`中的所有物品转换为CBOR，并返回由这些元素组成的地图。
从`QVariant`转换并非完全无损。更多信息请参阅`QCborValue::fromVariant()`文档。

### `QCborMap::iterator QCborMap::insert(QCborMap::value_type v)`

**作用与语义：**

将`v`中的键值对插入该映射，并返回指向新插入对的映射迭代器。
如果映射的键已经等于 `v.first`，其值将被 `v.second` 覆盖。

### `QCborMap::iterator QCborMap::insert(QLatin1StringView key, const QCborValue &value)`

**作用与语义：**

将键`key`和值`value`插入该映射，返回指向新插入对的映射迭代器。
如果映射的键已经等于 `key`，其值将被 `value` 覆盖。

### `QCborMap::iterator QCborMap::insert(const QCborValue &key, const QCborValue &value)`

**作用与语义：**

将键`key`和值`value`插入该映射，返回指向新插入对的映射迭代器。
如果映射的键已经等于 `key`，其值将被 `value` 覆盖。

### `QCborMap::iterator QCborMap::insert(const QString &key, const QCborValue &value)`

**作用与语义：**

将键`key`和值`value`插入该映射，返回指向新插入对的映射迭代器。
如果映射的键已经等于 `key`，其值将被 `value` 覆盖。

### `QCborMap::iterator QCborMap::insert(qint64 key, const QCborValue &value)`

**作用与语义：**

将键`key`和值`value`插入该映射，返回指向新插入对的映射迭代器。
如果映射的键已经等于 `key`，其值将被 `value` 覆盖。

### `bool QCborMap::isEmpty() const`

**作用与语义：**

如果该映射为空（即 `size()` 为 0），则返回真。

### `[since 6.10] QCborMap::key_value_iterator QCborMap::keyValueBegin()`

**作用与语义：**

返回一个STL风格的迭代子，指向地图中的第一个条目。

### `[since 6.10] QCborMap::const_key_value_iterator QCborMap::keyValueBegin() const`

**作用与语义：**

返回一个const的STL风格迭代子，指向映射中的第一个条目。

### `[since 6.10] QCborMap::key_value_iterator QCborMap::keyValueEnd()`

**作用与语义：**

返回一个STL风格的迭代子，指向地图上最后一个条目之后的虚数条目。

### `[since 6.10] QCborMap::const_key_value_iterator QCborMap::keyValueEnd() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向映射中最后一个条目之后的虚数条目。

### `QList<QCborValue> QCborMap::keys() const`

**作用与语义：**

返回该映射中所有键的列表。

### `void QCborMap::remove(const QCborValue &key)`

**作用与语义：**

如果找到键`key`，则从映射中移除键和对应的值。如果映射中没有这样的键，该函数则无效。
如果映射包含多个等于 `key` 的键，则该函数将移除哪一个未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流来创建此类映射。通常不允许重复键，且存在重复键通常表明发送端存在问题。
remove（qint64）、remove（`QLatin1StringView`）、remove（const `QString` &）。

### `void QCborMap::remove(qint64 key)`

**作用与语义：**

如果找到了，则移除映射中的键`key`和相应值。如果映射中没有这样的键，该函数则不做任何操作。
如果映射包含多个等于 `key` 的键，则该函数将移除哪一个键未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流来创建此类映射。通常不允许重复键，且重复键通常表明发送端存在问题。
remove（`QLatin1StringView`）、remove（const `QString` &）、remove（const `QCborValue` &）。

### `void QCborMap::remove(QLatin1StringView key)`

**作用与语义：**

如果找到了键`key`，则从映射中移除键和相应值。如果映射中没有这样的键，该函数则不做任何事。
如果映射包含多个等于 `key` 的键，则该函数将移除哪一个未定义。`QCborMap` 不允许插入重复键，但可以通过解码 CBOR 流来创建此类映射。通常不允许重复键，且重复键通常表明发送方存在问题。

### `void QCborMap::remove(const QString &key)`

**作用与语义：**

如果找到键`key`，则从映射中移除键和相应值。如果映射中没有这样的键，该函数则不做任何事。
如果映射包含多个等于 `key` 的键，则无法确定该函数将移除哪一个。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流来创建此类映射。通常不允许重复键，且键重复通常表明发送端存在问题。
remove（qint64）、remove（`QLatin1StringView`）、remove（const `QCborValue` &）。

### `[noexcept] qsizetype QCborMap::size() const`

**作用与语义：**

返回该映射中的元素数量。

### `[noexcept] void QCborMap::swap(QCborMap &other)`

**作用与语义：**

将这张地图与`other`交换。这个操作非常快，从未失败过。

### `QCborValue QCborMap::take(QLatin1StringView key)`

**作用与语义：**

从映射中移除键`key`和对应的值，并在找到时返回该值。如果映射中没有这样的键，该函数则不做任何事。
如果映射包含多个等于 `key` 的键，则该函数将移除哪一个键未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流来创建此类映射。通常不允许重复键，且重复键通常表明发送端存在问题。

### `QCborValue QCborMap::take(const QCborValue &key)`

**作用与语义：**

从映射中移除键`key`和对应的值，并在找到时返回该值。如果映射中没有这样的键，该函数则不做任何事。
如果映射包含多个等于 `key` 的键，则该函数将移除哪一个键未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流来创建此类映射。通常不允许重复键，且重复键通常表明发送端存在问题。

### `QCborValue QCborMap::take(const QString &key)`

**作用与语义：**

从映射中移除键`key`和对应的值，并在找到时返回该值。如果映射中没有这样的键，该函数则不做任何事。
如果映射包含多个等于 `key` 的键，则该函数将移除哪一个键未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流来创建此类映射。通常不允许重复键，且重复键通常表明发送端存在问题。

### `QCborValue QCborMap::take(qint64 key)`

**作用与语义：**

从映射中移除键`key`和对应的值，并在找到时返回该值。如果映射中没有这样的键，该函数则不做任何事。
如果映射包含多个等于 `key` 的键，则该函数将移除哪一个键未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流来创建此类映射。通常不允许重复键，且重复键通常表明发送端存在问题。

### `QCborValue QCborMap::toCborValue() const`

**作用与语义：**

显式构造一个表示该映射的`QCborValue`对象。该函数通常不必要，因为`QCborValue`有构造函数表示`QCborMap`，因此转换是隐式的。
将 `QCborMap` 转换为 `QCborValue` 使其能够在任何可以使用 QCborValues 的上下文中使用，包括作为 `QCborMap` 中的键和映射类型，以及`QCborValue::toCbor()`。

### `QJsonObject QCborMap::toJsonObject() const`

**作用与语义：**

递归地将该映射中的每个`QCborValue`值转换为 JSON，并用 `QCborValue::toJsonValue()` 生成字符串键，然后返回由这些关联组成的对应 `QJsonObject`。
请注意，CBOR 的类型集比 JSON 更丰富且更宽，因此在此转换过程中可能会丢失一些信息。有关应用的转换详情，请参见 `QCborValue::toJsonValue()`。
JSON 对象被定义为具有字符串键，与 CBOR 不同，因此将 `QCborMap` 转换为 `QJsonObject` 意味着对键值进行“字符串化”步骤。转换将采用上述对标签和扩展类型的特殊处理，并对其余类型进行如下转换：
- `Type`：变换
- `Bool`：“真”与“假”
- `Null`：“无”
- `Undefined`：“未定义”
- `Integer`：数字的十进制字符串形式
- `Double`：数字的十进制字符串形式
- `Byte array`：除非标签不同（见上文），编码为Base64url
- `Array`：被其诊断符号的紧凑形式取代
- `Map`：被其诊断符号的紧凑形式取代
- `Tags and extended types`：丢弃标签编号，标记值转换为字符串

### `QVariantHash QCborMap::toVariantHash() const`

**作用与语义：**

利用`QCborValue::toVariant()`将CBOR值转换为`QVariant`，并“串联”该映射中的所有CBOR键，返回该关联列表产生的`QVariantHash`。
QVariantMaps 有字符串键，与 CBOR 不同，因此将`QCborMap`转换为 `QVariantMap` 会涉及对键值进行“串化”步骤。详情请参见`QCborMap::toJsonObject()`。
此外，转换为`QVariant`的过程并非完全无损。更多信息请参见`QCborValue::toVariant()`的文档。

### `QVariantMap QCborMap::toVariantMap() const`

**作用与语义：**

利用`QCborValue::toVariant()`将CBOR值转换为`QVariant`，并“串联”该映射中的所有CBOR键，返回该关联列表产生的`QVariantMap`。
QVariantMaps 有字符串键，与 CBOR 不同，因此将`QCborMap`转换为 `QVariantMap` 会意味着键值的“字符串化”步骤。详情请参见 `QCborMap::toJsonObject()`。
此外，转换为`QVariant`的过程并非完全无损。更多信息请参见`QCborValue::toVariant()`中的文档。

### `QCborValue QCborMap::value(const QCborValue &key) const`

**作用与语义：**

返回该映射中对应关键`key`的`QCborValue`元素（如果存在）。
如果映射中没有键`key`，该函数返回一个包含未定义值的`QCborValue`。因此，使用该函数无法区分键不存在的情况和键映射到未定义值的情况。
如果映射包含多个等于 `key` 的键，则该函数返回哪一个键未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流来创建此类映射。通常不允许重复键，且键重复通常表明发送端存在问题。
value（qint64）、value（`QLatin1StringView`）、value（const `QString` &）。

### `QCborValue QCborMap::value(qint64 key) const`

**作用与语义：**

返回此映射中对应于键 `key` 的 `QCborValue` 元素（如果存在）。CBOR 建议使用整数键，因为它们占用的空间更小，编码和解码也更简单。
如果映射不包含键 `key`，该函数将返回一个包含未定义值的 `QCborValue`。因此，使用此函数无法区分键不存在的情况与键映射到未定义值的情况。
如果映射中包含多个等同于 `key` 的键，则函数返回的值不确定。`QCborMap` 不允许插入重复键，但可以通过解码包含重复键的 CBOR 流来创建这样的映射。通常不允许重复键，并且存在重复键通常表明发送方存在问题。
value(`QLatin1StringView`), value(const `QString` &), value(const `QCborValue` &)。

### `QCborValue QCborMap::value(QLatin1StringView key) const`

**作用与语义：**

返回该映射中对应关键`key`的`QCborValue`元素（如果存在）。
如果映射中没有键`key`，该函数返回一个包含未定义值的`QCborValue`。因此，使用该函数无法区分键不存在的情况和键映射到未定义值的情况。
如果映射包含多个等于`key`的键，则该函数返回哪一个键未定义。`QCborMap`不允许插入重复键，但可以通过解码包含它们的CBOR流创建此类映射。通常不允许重复键，且有重复键通常表明发送方存在问题。
value（qint64）、value（const `QString` &）、value（const `QCborValue` &）。

### `QCborValue QCborMap::value(const QString &key) const`

**作用与语义：**

返回该映射中对应关键`key`的`QCborValue`元素（如果存在）。
如果映射中没有键`key`，该函数返回一个包含未定义值的`QCborValue`。因此，使用该函数无法区分键不存在的情况和键映射到未定义值的情况。
如果映射包含多个等于 `key` 的键，则该函数返回哪个键未定义。`QCborMap` 不允许插入重复键，但可以通过解码 CBOR 流来创建此类映射。通常不允许重复键，且键重复通常表明发送端存在问题。
value（qint64）、value（`QLatin1StringView`）、value（const `QCborValue` &）。

### `[noexcept, since 6.10] QCborMap &QCborMap::operator=(QCborMap &&other)`

**作用与语义：**

移动分配操作员。
被移出的对象`other`处于有效但未指定状态。

### `[noexcept] QCborMap &QCborMap::operator=(const QCborMap &other)`

**作用与语义：**

用`other`的副本替换该对象的内容，然后返回该对象的引用。

### `QCborValueRef QCborMap::operator[](qint64 key)`

**作用与语义：**

返回对应键`key`的映射值的QCborValueRef。CBOR 建议使用整数键，因为它们占用空间更小且编码和解码更简单。
QCborValueRef 的 API 与 `QCborValue` 完全相同，但有一个重要区别：如果你给它分配了新值，这个映射会更新为该新值。
如果映射的键不等于 `key`，插入一个函数，该函数返回对新值的引用，该值将是一个未定义值的 `QCborValue`。因此，使用该函数无法区分键不存在的情况和键映射到未定义值的情况。
如果映射包含多个等于 `key` 的键，返回将引用哪个键则未定义。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流来创建此类映射。通常不允许重复键，且有重复键通常表明发送端存在问题。

### `const QCborValue QCborMap::operator[](const QCborValue &key) const`

**作用与语义：**

返回该映射中对应关键`key`的`QCborValue`元素（如果存在）。
如果映射中没有键`key`，该函数返回一个包含未定义值的`QCborValue`。因此，使用该函数无法区分键不存在的情况和键映射到未定义值的情况。
如果映射包含多个键，且等于`key`，则该函数返回哪个键未定义。`QCborMap`不允许插入重复键，但可以通过解码包含它们的CBOR流创建此类映射。通常不允许重复键，且键重复通常表明发送端存在问题。
运算符[]（qint64）， 运算符[]（`QLatin1StringView`）， 运算符[]（const QCborOperator[] &）。

### `const QCborValue QCborMap::operator[](qint64 key) const`

**作用与语义：**

返回此映射中对应于键 `key` 的 `QCborValue` 元素（如果存在）。CBOR 建议使用整数键，因为它们占用的空间更小，编码和解码也更简单。
如果映射不包含键 `key`，该函数将返回一个包含未定义值的 `QCborValue`。因此，使用此函数无法区分键不存在的情况与键映射到未定义值的情况。
如果映射中包含多个等同于 `key` 的键，则函数返回的值不确定。`QCborMap` 不允许插入重复键，但可以通过解码包含重复键的 CBOR 流来创建这样的映射。通常不允许重复键，并且存在重复键通常表明发送方存在问题。
operator[](`QLatin1StringView`), operator[](const `QString` &), operator[](const QCborOperator[] &)。

### `QCborValueRef QCborMap::operator[](QLatin1StringView key)`

**作用与语义：**

返回对应键`key`的映射值的QCborValueRef。
QCborValueRef 的 API 与 `QCborValue` 完全相同，但有一个重要区别：如果你给它赋予新值，这个映射会更新为该值。
如果映射的键不等于 `key`，插入一个键，该函数返回对新值的引用，该值将是一个未定义值的 `QCborValue`。因此，使用该函数无法区分键不存在的情况和键映射到未定义值的情况。
如果映射包含多个等于`key`的键，返回将引用哪个键则未定义。`QCborMap`不允许插入重复键，但可以通过解码包含它们的CBOR流来创建此类映射。通常不允许重复键，且存在重复键通常表明发送方存在问题。

### `QCborValueRef QCborMap::operator[](const QCborValue &key)`

**作用与语义：**

返回对应键`key`的映射值的QCborValueRef。
QCborValueRef 的 API 与 `QCborValue` 完全相同，但有一个重要区别：如果你给它赋予新值，这个映射会更新为该值。
如果映射的键不等于 `key`，插入一个键，该函数返回对新值的引用，该值将是一个未定义值的 `QCborValue`。因此，使用该函数无法区分键不存在的情况和键映射到未定义值的情况。
如果映射包含多个等于`key`的键，返回将引用哪个键则未定义。`QCborMap`不允许插入重复键，但可以通过解码包含它们的CBOR流来创建此类映射。通常不允许重复键，且存在重复键通常表明发送方存在问题。

### `QCborValueRef QCborMap::operator[](const QString &key)`

**作用与语义：**

返回对应键`key`的映射值的QCborValueRef。
QCborValueRef 的 API 与 `QCborValue` 完全相同，但有一个重要区别：如果你给它赋予新值，这个映射会更新为该值。
如果映射的键不等于 `key`，插入一个键，该函数返回对新值的引用，该值将是一个未定义值的 `QCborValue`。因此，使用该函数无法区分键不存在的情况和键映射到未定义值的情况。
如果映射包含多个等于`key`的键，返回将引用哪个键则未定义。`QCborMap`不允许插入重复键，但可以通过解码包含它们的CBOR流来创建此类映射。通常不允许重复键，且存在重复键通常表明发送方存在问题。

### `const QCborValue QCborMap::operator[](QLatin1StringView key) const`

**作用与语义：**

返回该映射中对应关键`key`的`QCborValue`元素（如果存在）。
如果映射不包含密钥`key`，该函数返回一个包含未定义值的`QCborValue`。因此，使用该函数无法区分密钥不存在的情况和密钥映射到未定义值的情况。
如果映射包含多个键，等于 `key`，则不确定该函数返回哪一个键。`QCborMap` 不允许插入重复键，但可以通过解码包含它们的 CBOR 流来创建此类映射。通常不允许重复键，且键重复通常表明发送端存在问题。
算符[]（qint64）， 算符[]（const `QString` &）， 算符[]（const QCborOperator[] &）。

### `const QCborValue QCborMap::operator[](const QString &key) const`

**作用与语义：**

返回该映射中对应关键`key`的`QCborValue`元素（如果存在）。
如果映射中没有键`key`，该函数返回一个包含未定义值的`QCborValue`。因此，使用该函数无法区分键不存在的情况和键映射到未定义值的情况。
如果映射包含多个键，且等于`key`，则该函数返回哪个键未定义。`QCborMap`不允许插入重复键，但可以通过解码包含它们的CBOR流创建此类映射。通常不允许重复键，且键重复通常表明发送端存在问题。
运算符[]（qint64）， 运算符[]（`QLatin1StringView`）， 运算符[]（const QCborOperator[] &）。

### `[noexcept] bool operator!=(const QCborMap &lhs, const QCborMap &rhs)`

**作用与语义：**

比较`lhs`和`rhs`映射，按顺序比较每个元素，若两个映射包含不同元素或顺序不同元素则返回为真，否则为假。
注意，CBOR 映射是无序的，这意味着包含相同对但顺序不同的映射仍然会有不同的比较。为避免这种情况，建议以可预测的顺序插入元素，例如按键值递增。事实上，规范的 CBOR 表示需要键按排序的映射。
有关Qt中CBOR等价的更多信息，请参见`QCborValue::compare()`。

### `[noexcept] bool operator<(const QCborMap &lhs, const QCborMap &rhs)`

**作用与语义：**

比较`lhs`和`rhs`映射，按顺序比较每个元素，如果应在`rhs`前排序`lhs`映射，返回真;否则返回为假。
注意，CBOR 映射是无序的，这意味着包含相同对但顺序不同的映射仍然会有不同的比较。为避免这种情况，建议以可预测的顺序插入元素，例如按键值递增。事实上，规范的 CBOR 表示需要键按排序的映射。
有关CBOR排序顺序的更多信息，请参见 `QCborValue::compare()`。

### `[noexcept] bool operator<=(const QCborMap &lhs, const QCborMap &rhs)`

**作用与语义：**

比较`lhs`和`rhs`映射，按顺序比较每个元素，如果应先排序`lhs`映射在`rhs`之前排序，或两个映射包含相同元素且顺序相同，则返回为真;否则返回为false。
注意，CBOR 映射是无序的，这意味着包含相同对但顺序不同的映射仍然会有不同的比较。为避免这种情况，建议以可预测的顺序插入元素，例如按键值递增。事实上，规范的 CBOR 表示需要键按排序的映射。
有关CBOR排序顺序的更多信息，请参见`QCborValue::compare()`。

### `[noexcept] bool operator==(const QCborMap &lhs, const QCborMap &rhs)`

**作用与语义：**

比较`lhs`和`rhs`映射，按顺序比较每个元素，若两个映射包含相同元素且顺序相同，则返回为真;否则为假。
注意，CBOR 映射是无序的，这意味着包含相同对但顺序不同的映射仍然会有不同的比较。为避免这种情况，建议以可预测的顺序插入元素，例如按键值递增。事实上，规范的 CBOR 表示需要键按排序的映射。
关于Qt中CBOR等价的更多信息，请参见`QCborValue::compare()`。

### `[noexcept] bool operator>(const QCborMap &lhs, const QCborMap &rhs)`

**作用与语义：**

比较`lhs`和`rhs`映射，按顺序比较每个元素，如果`lhs`映射在`rhs`后排序，则返回为真;否则返回为假。
注意，CBOR 映射是无序的，这意味着包含相同对但顺序不同的映射仍然会有不同的比较。为避免这种情况，建议以可预测的顺序插入元素，例如按键值递增。事实上，规范的 CBOR 表示需要键按排序的映射。
有关CBOR排序顺序的更多信息，请参见`QCborValue::compare()`。

### `[noexcept] bool operator>=(const QCborMap &lhs, const QCborMap &rhs)`

**作用与语义：**

比较`lhs`和`rhs`映射，按顺序比较每个元素，如果映射应在`rhs`后排序，或者两个映射包含相同元素且顺序相同，则返回`lhs`为真;否则返回为假。
注意，CBOR 映射是无序的，这意味着包含相同对但顺序不同的映射仍然会有不同的比较。为避免这种情况，建议以可预测的顺序插入元素，例如按键值递增。事实上，规范的 CBOR 表示需要键按排序的映射。
有关CBOR排序顺序的更多信息，请参见`QCborValue::compare()`。

### `class ConstIterator`

**作用与语义：**

QCborMap：：ConstIterator 类为 QCborMap 提供了一个 STL 风格的 const 迭代器。
`QCborMap::ConstIterator`允许你对一个`QCborMap`进行迭代。如果你想在迭代过程中修改`QCborMap`，必须用`QCborMap::Iterator`。即使是在非const `QCborMap`上，通常使用Const Iterator的做法是`QCborMap::ConstIterator`，因为你不需要通过迭代器更改`QCborMap`。Const迭代器速度稍快，且提高了代码的可读性。
你必须用`QCborMap::begin()`、`QCborMap::end()`或`QCborMap::find()`等`QCborMap`函数初始化迭代器，才能开始迭代......
多个迭代器可以用于同一个对象。不过，如果对象被修改，现有的迭代器会变得悬挂。

### `class Iterator`

**作用与语义：**

QCborMap：：Iterator 类为 QCborMap 提供了一个类似 STL 的非const 迭代器。
`QCborMap::Iterator`允许你对某个 `QCborMap` 进行迭代，并修改某个特定键下存储的值（但不能修改键）。如果你想对 const `QCborMap` 进行迭代，应该使用 S 的 `QCborMap::ConstIterator`。通常在非 const 的`QCborMap`上也使用 `QCborMap::ConstIterator` 是个好习惯，除非你需要通过迭代器更改`QCborMap`。Const 迭代器速度稍快，并且提高了代码的可读性。
你必须用`QCborMap`函数如`QCborMap::begin()`、`QCborMap::end()`或`QCborMap::find()`初始化迭代器，才能开始迭代......
多个迭代器可以用于同一个对象。然而，一旦对象被修改，现有的迭代器会变得悬浮。

### `const_iterator`

**作用与语义：**

`QCborMap::ConstIterator`的同义词。

### `(since 6.10) const_key_value_iterator`

**作用与语义：**

QCborMap：：const_key_value_iterator typedef 提供了一个 STL 风格的迭代器用于 `QCborMap`。
QCborMap：：const_key_value_iterator 本质上与 `QCborMap::const_iterator` 相同，但为与其他容器如 `QJsonObject` 实现对称而提供。
这种类型防御是在Qt 6.10中引入的。

### `iterator`

**作用与语义：**

`QCborMap::Iterator`的同义词。

### `key_type`

**作用与语义：**

该映射的密钥类型。由于`QCborMap`键可以是任何CBOR类型，这就是`QCborValue`。

### `(since 6.10) key_value_iterator`

**作用与语义：**

QCborMap::key_value_iterator 类型定义提供了一个 STL 风格的 `QCborMap` 迭代器。
QCborMap::key_value_iterator 本质上与 `QCborMap::iterator` 相同，但为了与 `QJsonObject` 等其他容器保持对称而提供。
此类型定义在 Qt 6.10 中引入。

### `mapped_type`

**作用与语义：**

映射到的类型（值），也就是`QCborValue`。

### `size_type`

**作用与语义：**

就是`QCborMap`用来测量尺寸的那种。

### `value_type`

**作用与语义：**

存储在此容器中的值：一对 QCborValues。

### `(since 6.10) auto asKeyValueRange() &&`

**作用与语义：**

返回一个范围对象，允许对该映射进行键值对的迭代。
注意，通过这种方式获得的值是映射中值的引用。具体来说，变异值会修改映射本身。

### `QCborValue extract(QCborMap::iterator it)`

**作用与语义：**

从迭代器`it`指示的位置从映射中提取一个值，并返回该值。

### `QCborMap::iterator find(qint64 key)`

**作用与语义：**

返回键值为`key`的映射迭代器，如果映射包含该对。如果没有，该函数返回`end()`。
如果映射包含多个等于`key`的键，则该函数将找到哪一个键未定义。`QCborMap`不允许插入重复键，但可以通过解码包含它们的CBOR流来创建此类映射。通常不允许重复键，且重复键通常表明发送方存在问题。

### `QCborMap::iterator find(QLatin1StringView key)`

**作用与语义：**

返回键值为`key`的映射迭代器，如果映射包含该对。如果没有，该函数返回`end()`。
如果映射包含多个等于`key`的键，则该函数将找到哪一个键未定义。`QCborMap`不允许插入重复键，但可以通过解码包含它们的CBOR流来创建此类映射。通常不允许重复键，且重复键通常表明发送方存在问题。

### `QCborMap::iterator find(const QCborValue &key)`

**作用与语义：**

返回键值为`key`的映射迭代器，如果映射包含该对。如果没有，该函数返回`end()`。
如果映射包含多个等于`key`的键，则该函数将找到哪一个键未定义。`QCborMap`不允许插入重复键，但可以通过解码包含它们的CBOR流来创建此类映射。通常不允许重复键，且重复键通常表明发送方存在问题。

### `QCborMap::iterator find(const QString &key)`

**作用与语义：**

返回键值为`key`的映射迭代器，如果映射包含该对。如果没有，该函数返回`end()`。
如果映射包含多个等于`key`的键，则该函数将找到哪一个键未定义。`QCborMap`不允许插入重复键，但可以通过解码包含它们的CBOR流来创建此类映射。通常不允许重复键，且重复键通常表明发送方存在问题。

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

`QCborMap` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
