# QMap

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QMap` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMap` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QMap>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

### 状态、生命周期和线程

**生命周期：** 容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

**状态与结果：** 要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

**线程与事件循环：** 不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

## 3. 直接使用

先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
#include <QList>

QList<int> values{1, 2, 3};
values.append(4);
for (const int value : values) {
    // 使用 value
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `class const_iterator`
- `class iterator`
- `class key_iterator`
- `ConstIterator`
- `Iterator`
- `const_key_value_iterator`
- `difference_type`
- `key_type`
- `key_value_iterator`
- `mapped_type`
- `size_type`

### 公有函数

- `QMap()`
- `QMap(const std::map<Key, T> &other)`
- `QMap(std::initializer_list<std::pair<Key, T>> list)`
- `QMap(std::map<Key, T> &&other)`
- `QMap(const QMap<Key, T> &other)`
- `QMap(QMap<Key, T> &&other)`
- `~QMap()`
- `(since 6.4) auto asKeyValueRange() &&`
- `(since 6.4) auto asKeyValueRange() &`
- `(since 6.4) auto asKeyValueRange() const &&`
- `(since 6.4) auto asKeyValueRange() const &`
- `QMap<Key, T>::iterator begin()`
- `QMap<Key, T>::const_iterator begin() const`
- `QMap<Key, T>::const_iterator cbegin() const`
- `QMap<Key, T>::const_iterator cend() const`
- `void clear()`
- `QMap<Key, T>::const_iterator constBegin() const`
- `QMap<Key, T>::const_iterator constEnd() const`
- `QMap<Key, T>::const_iterator constFind(const Key &key) const`
- `QMap<Key, T>::const_key_value_iterator constKeyValueBegin() const`
- `QMap<Key, T>::const_key_value_iterator constKeyValueEnd() const`
- `bool contains(const Key &key) const`
- `QMap<Key, T>::size_type count(const Key &key) const`
- `QMap<Key, T>::size_type count() const`
- `bool empty() const`
- `QMap<Key, T>::iterator end()`
- `QMap<Key, T>::const_iterator end() const`
- `std::pair<QMap<Key, T>::iterator, QMap<Key, T>::iterator> equal_range(const Key &key)`
- `std::pair<QMap<Key, T>::const_iterator, QMap<Key, T>::const_iterator> equal_range(const Key &key) const`
- `QMap<Key, T>::iterator erase(QMap<Key, T>::const_iterator pos)`
- `(since 6.0) QMap<Key, T>::iterator erase(QMap<Key, T>::const_iterator first, QMap<Key, T>::const_iterator last)`
- `QMap<Key, T>::iterator find(const Key &key)`
- `QMap<Key, T>::const_iterator find(const Key &key) const`
- `T & first()`
- `const T & first() const`
- `const Key & firstKey() const`
- `void insert(QMap<Key, T> &&map)`
- `void insert(const QMap<Key, T> &map)`
- `QMap<Key, T>::iterator insert(const Key &key, const T &value)`
- `QMap<Key, T>::iterator insert(QMap<Key, T>::const_iterator pos, const Key &key, const T &value)`
- `bool isEmpty() const`
- `Key key(const T &value, const Key &defaultKey = Key()) const`
- `QMap<Key, T>::key_iterator keyBegin() const`
- `QMap<Key, T>::key_iterator keyEnd() const`
- `QMap<Key, T>::key_value_iterator keyValueBegin()`
- `QMap<Key, T>::const_key_value_iterator keyValueBegin() const`
- `QMap<Key, T>::key_value_iterator keyValueEnd()`
- `QMap<Key, T>::const_key_value_iterator keyValueEnd() const`
- `QList<Key> keys() const`
- `QList<Key> keys(const T &value) const`
- `T & last()`
- `const T & last() const`
- `const Key & lastKey() const`
- `QMap<Key, T>::iterator lowerBound(const Key &key)`
- `QMap<Key, T>::const_iterator lowerBound(const Key &key) const`
- `QMap<Key, T>::size_type remove(const Key &key)`
- `(since 6.1) QMap<Key, T>::size_type removeIf(Predicate pred)`
- `QMap<Key, T>::size_type size() const`
- `void swap(QMap<Key, T> &other)`
- `T take(const Key &key)`
- `std::map<Key, T> toStdMap() const &`
- `(since 6.0) std::map<Key, T> toStdMap() &&`
- `QMap<Key, T>::iterator upperBound(const Key &key)`
- `QMap<Key, T>::const_iterator upperBound(const Key &key) const`
- `T value(const Key &key, const T &defaultValue = T()) const`
- `QList<T> values() const`
- `QMap<Key, T> & operator=(QMap<Key, T> &&other)`
- `QMap<Key, T> & operator=(const QMap<Key, T> &other)`
- `T & operator[](const Key &key)`
- `T operator[](const Key &key) const`

### 相关非成员函数

- `(since 6.1) qsizetype erase_if(QMap<Key, T> &map, Predicate pred)`
- `(since 6.8) size_t qHash(const QMap<Key, T> &key, size_t seed = 0)`
- `bool operator!=(const QMap<Key, T> &lhs, const QMap<Key, T> &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QMap<Key, T> &map)`
- `bool operator==(const QMap<Key, T> &lhs, const QMap<Key, T> &rhs)`
- `QDataStream & operator>>(QDataStream &in, QMap<Key, T> &map)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QMap::ConstIterator`

**作用与语义：**

Qt风格的`QMap::const_iterator`同义词。

### `QMap::Iterator`

**作用与语义：**

Qt风格的同义词`QMap::iterator`。

### `QMap::const_key_value_iterator`

**作用与语义：**

QMap：：const_key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QMap`。
QMap：：const_key_value_iterator 本质上与 `QMap::const_iterator` 相同，区别在于运算符*() 返回的是键值对而非值。

### `[alias] QMap::difference_type`

**作用与语义：**

Typedef 用于ptrdiff_t。提供 STL 兼容性。

### `[alias] QMap::key_type`

**作用与语义：**

Typedef 用于键。提供 STL 兼容性。

### `QMap::key_value_iterator`

**作用与语义：**

QMap：：key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QMap`。
QMap：：key_value_iterator 本质上与 `QMap::iterator` 相同，区别在于运算符*() 返回的是键值对而非值。

### `[alias] QMap::mapped_type`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `[alias] QMap::size_type`

**作用与语义：**

类型定义用于国际语言。提供支持STL兼容性。

### `QMap::QMap()`

**作用与语义：**

构建一个空地图。

### `[explicit] QMap::QMap(const std::map<Key, T> &other)`

**作用与语义：**

复制了`other`。

### `QMap::QMap(std::initializer_list<std::pair<Key, T>> list)`

**作用与语义：**

构造一个映射，包含初始化器列表中每个元素的副本 `list`。

### `[explicit] QMap::QMap(std::map<Key, T> &&other)`

**作用与语义：**

通过从`other`移动来构造映射。

### `[default] QMap::QMap(const QMap<Key, T> &other)`

**作用与语义：**

构建了一份`other`的副本。
该操作发生在常数时间内，因为QMap是隐式共享的。这使得从函数返回QMap非常快速。如果共享实例被修改，它会被复制（写时复制），这需要线性时间。

### `[default] QMap::QMap(QMap<Key, T> &&other)`

**作用与语义：**

Move-构造一个QMap实例。

### `[default] QMap::~QMap()`

**作用与语义：**

会销毁该映射。对映射中值的引用以及该映射上的所有迭代子的引用都变得无效。

### `[since 6.4] auto QMap::asKeyValueRange() const &&`

**作用与语义：**

返回一个范围对象，允许以键值对形式在该映射上进行循环。例如，该范围对象可以用于基于范围的for循环，并结合结构化绑定声明：
注意，键和通过这种方式获得的值都是映射中对函数的引用。具体来说，变异值会修改映射本身。

**官方示例：**

```cpp
 QMap<QString, int> map;
 map.insert("January", 1);
 map.insert("February", 2);
 // ...
 map.insert("December", 12);

 for (auto [key, value] : map.asKeyValueRange()) {
     cout << qPrintable(key) << ": " << value << endl;
     --value; // convert to JS month indexing
 }
```

### `QMap<Key, T>::iterator QMap::begin()`

**作用与语义：**

返回一个指向地图第一个项目的STL式迭代子。

### `QMap<Key, T>::const_iterator QMap::begin() const`

**作用与语义：**

返回一个指向地图第一个项目的STL式迭代子。

### `QMap<Key, T>::const_iterator QMap::cbegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向映射中的第一个项目。

### `QMap<Key, T>::const_iterator QMap::cend() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向映射中最后一个项之后的虚数项。

### `void QMap::clear()`

**作用与语义：**

移除地图上的所有物品。

### `QMap<Key, T>::const_iterator QMap::constBegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向映射中的第一个项目。

### `QMap<Key, T>::const_iterator QMap::constEnd() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向映射中最后一个项之后的虚数项。

### `QMap<Key, T>::const_iterator QMap::constFind(const Key &key) const`

**作用与语义：**

返回一个指向映射中键为`key`的元素的const迭代器。
如果映射中没有键为`key`的项，函数返回`constEnd()`。

### `QMap<Key, T>::const_key_value_iterator QMap::constKeyValueBegin() const`

**作用与语义：**

返回一个const的STL风格迭代子，指向映射中的第一个条目。

### `QMap<Key, T>::const_key_value_iterator QMap::constKeyValueEnd() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向映射中最后一个条目之后的虚数条目。

### `bool QMap::contains(const Key &key) const`

**作用与语义：**

如果映射包含键为`key`的项，返回`true`;否则返回`false`。

### `QMap<Key, T>::size_type QMap::count(const Key &key) const`

**作用与语义：**

返回与密钥`key`相关的项目数量。

### `QMap<Key, T>::size_type QMap::count() const`

**作用与语义：**

和`size()`一样。

### `bool QMap::empty() const`

**作用与语义：**

该函数是为了STL兼容性而提供。它等价于`isEmpty()`，映射为空时返回真;否则返回假。

### `QMap<Key, T>::iterator QMap::end()`

**作用与语义：**

返回一个STL风格的迭代器，指向地图最后一个项目之后的虚构项。

### `QMap<Key, T>::const_iterator QMap::end() const`

**作用与语义：**

返回一个STL风格的迭代器，指向地图最后一个项目之后的虚构项。

### `std::pair<QMap<Key, T>::iterator, QMap<Key, T>::iterator> QMap::equal_range(const Key &key)`

**作用与语义：**

返回一对迭代子，界定`[first, second)`值的范围，这些值存储在`key`下。

### `std::pair<QMap<Key, T>::const_iterator, QMap<Key, T>::const_iterator> QMap::equal_range(const Key &key) const`

**作用与语义：**

返回一对迭代子，界定`[first, second)`值的范围，这些值存储在`key`下。

### `QMap<Key, T>::iterator QMap::erase(QMap<Key, T>::const_iterator pos)`

**作用与语义：**

从映射中移除迭代器`pos`指向的（键，值）对，并返回映射中下一个项目的迭代器。
注意：迭代器`pos`必须有效且可去参照。

### `[since 6.0] QMap<Key, T>::iterator QMap::erase(QMap<Key, T>::const_iterator first, QMap<Key, T>::const_iterator last)`

**作用与语义：**

从映射中移除迭代器范围[`first`， `last`）指向的（键，值）对。返回映射中最后移除元素后的该项的迭代器。
注意：`[first, last)`范围必须是`*this`有效的范围。

### `QMap<Key, T>::iterator QMap::find(const Key &key)`

**作用与语义：**

返回一个迭代器，指向地图中键`key`的物品。
如果映射中没有键为`key`的项，函数返回`end()`。

### `QMap<Key, T>::const_iterator QMap::find(const Key &key) const`

**作用与语义：**

返回一个迭代器，指向地图中键`key`的物品。
如果映射中没有键为`key`的项，函数返回`end()`。

### `T &QMap::first()`

**作用与语义：**

返回映射中第一个值的引用，即映射到最小键的值。该函数假设映射不是空的。
当调用非共享（或const版本）时，执行时间常数。

### `const T &QMap::first() const`

**作用与语义：**

返回映射中第一个值的引用，即映射到最小键的值。该函数假设映射不是空的。
当调用非共享（或const版本）时，执行时间常数。

### `const Key &QMap::firstKey() const`

**作用与语义：**

返回映射中最小的键的引用。该函数假设映射不是空的。
该程序执行时间为常数。

### `void QMap::insert(QMap<Key, T> &&map)`

**作用与语义：**

把`map`的所有物品都搬到这张地图上。
如果键在两个映射中都存在，则其值将被存储在`map`中的值替换。
如果`map`被共享，则会复制这些项目。

### `void QMap::insert(const QMap<Key, T> &map)`

**作用与语义：**

将`map`中的所有物品插入这张地图。
如果键在两个映射中都具有，则其值将被存储在`map`中的值替换。

### `QMap<Key, T>::iterator QMap::insert(const Key &key, const T &value)`

**作用与语义：**

插入一个键`key`且值为`value`的新项。
如果已有具有密钥`key`的物品，则该物品的值被替换为`value`。
返回一个迭代器，指向新元素/更新元素。

### `QMap<Key, T>::iterator QMap::insert(QMap<Key, T>::const_iterator pos, const Key &key, const T &value)`

**作用与语义：**

插入一个新物品，键`key`和值`value`，并附有提示`pos`建议插入位置。
如果`constBegin()`作为提示，表示`key`小于映射中的任何键，而`constEnd()`则表示`key`（严格来说）大于映射中的任何键。否则提示应满足条件 （`pos` - 1）。`key()` < `key` <= pos。`key()`。如果提示`pos`错误，则忽略，进行常规插入。
如果已有带有密钥`key`的项目，该项的值会被替换为`value`。
如果提示正确且映射未共享，插入会以摊销常数时间执行。
在从排序数据创建映射时，先插入最大密钥并`constBegin()`比按排序顺序插入`constEnd()`快，因为需要`constEnd()` - 1（用于检查提示是否有效）需要对数时间。
注意：注意提示。从旧共享实例提供迭代器可能会崩溃，但也有可能无声破坏地图和`pos`地图。
返回一个迭代器，指向新元素/更新元素。

### `bool QMap::isEmpty() const`

**作用与语义：**

如果映射中没有任何项目，则返回`true`;否则返回 false。

### `Key QMap::key(const T &value, const Key &defaultKey = Key()) const`

**作用与语义：**

返回第一个值为`value`的键;如果映射中没有值为`value`的项，则返回`defaultKey`键。如果没有提供`defaultKey`，函数返回一个默认构造的键。
该函数可能较慢（线性时间），因为`QMap`的内部数据结构是通过按键快速查找而优化的，而不是按值。

### `QMap<Key, T>::key_iterator QMap::keyBegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向映射中的第一个键。

### `QMap<Key, T>::key_iterator QMap::keyEnd() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向映射中最后一个键之后的虚数项。

### `QMap<Key, T>::key_value_iterator QMap::keyValueBegin()`

**作用与语义：**

返回一个STL风格的迭代子，指向地图中的第一个条目。

### `QMap<Key, T>::const_key_value_iterator QMap::keyValueBegin() const`

**作用与语义：**

返回一个const的STL风格迭代子，指向映射中的第一个条目。

### `QMap<Key, T>::key_value_iterator QMap::keyValueEnd()`

**作用与语义：**

返回一个STL风格的迭代子，指向地图上最后一个条目之后的虚数条目。

### `QMap<Key, T>::const_key_value_iterator QMap::keyValueEnd() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向映射中最后一个条目之后的虚数条目。

### `QList<Key> QMap::keys() const`

**作用与语义：**

返回包含映射中所有键的列表，按升序返回。
顺序保证与`values()`使用的顺序相同。
该函数会在线性时间内创建一个新的列表。通过从`keyBegin()`迭代到`keyEnd()`，可以避免所需的时间和内存消耗。

### `QList<Key> QMap::keys(const T &value) const`

**作用与语义：**

返回包含所有与`value`值相关的键的列表，按升序返回。
该函数可能较慢（线性时间），因为`QMap`的内部数据结构优化为按键快速查找，而非按值。

### `T &QMap::last()`

**作用与语义：**

返回映射中最后一个值的引用，即映射到最大键的值。该函数假设映射不是空的。
当调用非共享（或const版本）时，执行时间常数。

### `const T &QMap::last() const`

**作用与语义：**

返回映射中最后一个值的引用，即映射到最大键的值。该函数假设映射不是空的。
当调用非共享（或const版本）时，执行时间常数。

### `const Key &QMap::lastKey() const`

**作用与语义：**

返回映射中最大密钥的引用。该函数假设映射不是空的。
该程序执行时间为常数。

### `QMap<Key, T>::iterator QMap::lowerBound(const Key &key)`

**作用与语义：**

返回一个迭代器，指向映射中键为`key`的第一个项目。如果映射中没有键为`key`的项，函数返回一个迭代器到键数更大的最近项目。

### `QMap<Key, T>::const_iterator QMap::lowerBound(const Key &key) const`

**作用与语义：**

返回一个迭代器，指向映射中键为`key`的第一个项目。如果映射中没有键为`key`的项，函数返回一个迭代器到键数更大的最近项目。

### `QMap<Key, T>::size_type QMap::remove(const Key &key)`

**作用与语义：**

从地图上移除所有带有钥匙`key`的物品。返回移除的物品数量，如果钥匙存在地图，则为1，否则为0。

### `[since 6.1] template <typename Predicate> QMap<Key, T>::size_type QMap::removeIf(Predicate pred)`

**作用与语义：**

从映射中移除所有谓词返回为真的元素`pred`。
该函数支持的谓词要么取类型为`QMap<Key, T>::iterator`，要么参数为`std::pair<const Key &, T &>`。
返回被移除的元素数量（如果有的话）。

### `QMap<Key, T>::size_type QMap::size() const`

**作用与语义：**

返回映射中（键，值）对的数量。

### `[noexcept] void QMap::swap(QMap<Key, T> &other)`

**作用与语义：**

将这张地图与`other`交换。这个操作非常快，从未失败过。

### `T QMap::take(const Key &key)`

**作用与语义：**

从映射中移除带有键`key`的项目，并返回与之相关的值。
如果该项不存在于映射中，函数仅返回默认构造值。
如果你不使用返回值，`remove()`效率更高。

### `std::map<Key, T> QMap::toStdMap() const &`

**作用与语义：**

返回一个相当于该`QMap`的STL映射。

### `[since 6.0] std::map<Key, T> QMap::toStdMap() &&`

**作用与语义：**

注意：调用该函数会使该`QMap`处于部分成形状态，唯一有效的操作是销毁或赋予新值。

### `QMap<Key, T>::iterator QMap::upperBound(const Key &key)`

**作用与语义：**

返回一个迭代器，指向紧接着上一个键为`key`的项目的项目。如果映射中没有键`key`的项目，函数返回一个迭代器，指向键数更大的最近项目。

**官方示例：**

```cpp
 QMap<int, QString> map;
 map.insert(1, "one");
 map.insert(5, "five");
 map.insert(10, "ten");

 map.upperBound(0);      // returns iterator to (1, "one")
 map.upperBound(1);      // returns iterator to (5, "five")
 map.upperBound(2);      // returns iterator to (5, "five")
 map.upperBound(10);     // returns end()
 map.upperBound(999);    // returns end()
```

### `QMap<Key, T>::const_iterator QMap::upperBound(const Key &key) const`

**作用与语义：**

返回一个迭代器，指向紧接着上一个键为`key`的项目的项目。如果映射中没有键`key`的项目，函数返回一个迭代器，指向键数更大的最近项目。

**官方示例：**

```cpp
 QMap<int, QString> map;
 map.insert(1, "one");
 map.insert(5, "five");
 map.insert(10, "ten");

 map.upperBound(0);      // returns iterator to (1, "one")
 map.upperBound(1);      // returns iterator to (5, "five")
 map.upperBound(2);      // returns iterator to (5, "five")
 map.upperBound(10);     // returns end()
 map.upperBound(999);    // returns end()
```

### `T QMap::value(const Key &key, const T &defaultValue = T()) const`

**作用与语义：**

返回与密钥`key`关联的值。
如果映射中没有键为`key`的项，函数返回`defaultValue`。如果没有指定`defaultValue`，函数返回默认构造值。

### `QList<T> QMap::values() const`

**作用与语义：**

返回包含映射中所有值的列表，按键值的升序排列。
该函数会在线性时间内创建一个新的列表。通过从`keyValueBegin()`迭代到`keyValueEnd()`可以避免所需的时间和内存消耗。

### `[default] QMap<Key, T> &QMap::operator=(QMap<Key, T> &&other)`

**作用与语义：**

Move-assign `other`到该`QMap`实例。

### `[default] QMap<Key, T> &QMap::operator=(const QMap<Key, T> &other)`

**作用与语义：**

将`other`分配到该映射，并返回对该映射的引用。

### `T &QMap::operator[](const Key &key)`

**作用与语义：**

返回与密钥`key`关联的值作为可修改的引用。
如果映射中没有键为`key`的项，函数会在键`key`的映射中插入默认构造的值，并返回对该值的引用。

### `T QMap::operator[](const Key &key) const`

**作用与语义：**

和`value()`一样。

### `[since 6.1] template < typename Key, typename T, typename Predicate > qsizetype erase_if(QMap<Key, T> &map, Predicate pred)`

**作用与语义：**

从映射`map`中移除所有谓词返回为真的元素`pred`。
该函数支持的谓词要么是类型为`QMap<Key, T>::iterator`，要么是类型为`std::pair<const Key &, T &>`的参数。
返回被移除的元素数量（如果有的话）。

### `[since 6.8] size_t qHash(const QMap<Key, T> &key, size_t seed = 0)`

**作用与语义：**

返回 `key` 的哈希值，使用 `seed` 来做种式计算。
qHash() 必须支持 qHash() 支持类型 `Key` 和 `T`。

### `bool operator!=(const QMap<Key, T> &lhs, const QMap<Key, T> &rhs)`

**作用与语义：**

如果 `lhs` 不等于 `rhs`，则返回 `rhs`；否则返回 false。
如果两个映射包含相同的（键, 值）对，则认为它们相等。
此函数要求键类型和值类型实现 `operator==()`。

### `template <typename Key, typename T> QDataStream &operator<<(QDataStream &out, const QMap<Key, T> &map)`

**作用与语义：**

写入映射`map`流`out`。
该函数需要键型和值类型来实现`operator<<()`。

### `bool operator==(const QMap<Key, T> &lhs, const QMap<Key, T> &rhs)`

**作用与语义：**

如果 `lhs` 等于 `rhs`，则返回 `rhs`；否则返回 false。
当两个映射包含相同的（键，值）对时，它们被认为是相等的。
此函数要求键类型和值类型实现 `operator==()`。

### `template <typename Key, typename T> QDataStream &operator>>(QDataStream &in, QMap<Key, T> &map)`

**作用与语义：**

读取`in`溪的地图到`map`。
该函数需要键型和值类型来实现`operator>>()`。

### `class const_iterator`

**作用与语义：**

QMap：：const_iterator 类为 QMap 提供了一个 STL 风格的 const 迭代器。
`QMap`<密钥，T>：：const_iterator 允许你对`QMap`进行迭代。如果你想在迭代时修改`QMap`，必须用 `QMap::iterator`。通常在非连续性`QMap`上使用 `QMap::const_iterator` 也是个好习惯，除非你需要通过迭代器更改`QMap`。Const 迭代器速度稍快，且能提高代码的可读性。
默认的`QMap::const_iterator`构造函数会创建一个未初始化的迭代器。你必须用`QMap::cbegin()`、`QMap::cend()`或`QMap::constFind()`等`QMap`函数初始化它，才能开始迭代。这里有一个典型的循环，可以打印映射中存储的所有（键、值）对：
这里有一个例子，去除所有点数大于10的物品：
这里的行为也一样`erase_if()`。
与以任意顺序存储物品的`QHash`不同，`QMap`按键顺序存储。
同一张地图上可以使用多个迭代器。如果你向地图添加物品，现有的迭代器依然有效。如果你从地图上移除物品，指向已移除物品的迭代器将变成悬挂迭代器。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。

**官方示例：**

```cpp
 QMap<QString, int> map;
 map.insert("January", 1);
 map.insert("February", 2);
 //...
 map.insert("December", 12);

 for (auto i = map.cbegin(), end = map.cend(); i != end; ++i)
     cout << qPrintable(i.key()) << ": " << i.value() << endl;
```

### `class iterator`

**作用与语义：**

QMap：：iterator 类为 QMap 提供了一个类似 STL 的非const迭代器。
`QMap`<密钥，T>：：迭代器允许你对某个`QMap`进行迭代，并修改某个特定键下存储的值（但不能修改键）。如果你想对const的迭代`QMap`进行迭代，应该使用`QMap::const_iterator`。通常在非const的`QMap`迭代器上也使用`QMap::const_iterator`是个好习惯，除非你需要通过迭代器更改`QMap`。const迭代器速度稍快，且能提高代码的可读性。
默认的`QMap::iterator`构造器会创建一个未初始化的迭代器。你必须先用`QMap::begin()`、`QMap::end()`或`QMap::find()`等`QMap`函数初始化它，才能开始迭代。这里有一个典型的循环，可以打印映射中存储的所有（键、值）对：
与以任意顺序存储物品的 `QHash` 不同，`QMap` 按键顺序存储。
这里有一个例子，将`QMap`中存储的每个值增加2：
要从`QMap`中移除元素，可以使用`erase_if`（`QMap`<Key， T> &map， Predicate pred）：
同一张地图上可以使用多个迭代器。如果你向地图添加物品，现有的迭代器依然有效。如果你从地图上移除物品，指向已移除物品的迭代器将变成悬挂迭代器。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。

**官方示例：**

```cpp
 QMap<QString, int> map;
 map.insert("January", 1);
 map.insert("February", 2);
 //...
 map.insert("December", 12);

 for (auto i = map.cbegin(), end = map.cend(); i != end; ++i)
     cout << qPrintable(i.key()) << ": " << i.value() << endl;
```

### `class key_iterator`

**作用与语义：**

QMap：：key_iterator 类为 QMap 密钥提供了一个 STL 风格的 const 迭代器。
`QMap::key_iterator` 本质上与 `QMap::const_iterator` 相同，区别在于运算符*() 和运算符->() 返回键而非值。
对于大多数用途，`QMap::iterator`和应`QMap::const_iterator`，您可以通过调用`QMap::iterator::key()`轻松访问密钥：
然而，为了实现`QMap`键与STL风格算法之间的互操作性，我们需要一个迭代器，它不引用键而非值。有了`QMap::key_iterator`，我们可以对多个键应用算法而无需调用`QMap::keys()`，但这效率较低，因为创建一个临时`QList`需要`QMap`迭代和内存分配。
`QMap::key_iterator`是const，密钥无法修改。
默认的`QMap::key_iterator`构造函数会创建一个未初始化的迭代器。你必须用像 `QMap::keyBegin()` 或 `QMap::keyEnd()` 这样的 `QMap` 函数来初始化它。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。

**官方示例：**

```cpp
 for (QMap<int, QString>::const_iterator it = map.cbegin(), end = map.cend(); it != end; ++it) {
     cout << "The key: " << it.key() << endl;
     cout << "The value: " << qPrintable(it.value()) << endl;
     cout << "Also the value: " << qPrintable(*it) << endl;
 }
```

### `ConstIterator`

**作用与语义：**

Qt风格的`QMap::const_iterator`同义词。

### `Iterator`

**作用与语义：**

Qt风格的同义词`QMap::iterator`。

### `const_key_value_iterator`

**作用与语义：**

QMap：：const_key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QMap`。
QMap：：const_key_value_iterator 本质上与 `QMap::const_iterator` 相同，区别在于运算符*() 返回的是键值对而非值。

### `difference_type`

**作用与语义：**

Typedef 用于ptrdiff_t。提供 STL 兼容性。

### `key_type`

**作用与语义：**

Typedef 用于键。提供 STL 兼容性。

### `key_value_iterator`

**作用与语义：**

QMap：：key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QMap`。
QMap：：key_value_iterator 本质上与 `QMap::iterator` 相同，区别在于运算符*() 返回的是键值对而非值。

### `mapped_type`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `size_type`

**作用与语义：**

类型定义用于国际语言。提供支持STL兼容性。

### `(since 6.4) auto asKeyValueRange() &&`

**作用与语义：**

返回一个范围对象，允许以键值对形式在该映射上进行循环。例如，该范围对象可以用于基于范围的for循环，并结合结构化绑定声明：
注意，键和通过这种方式获得的值都是映射中对函数的引用。具体来说，变异值会修改映射本身。

**官方示例：**

```cpp
 QMap<QString, int> map;
 map.insert("January", 1);
 map.insert("February", 2);
 // ...
 map.insert("December", 12);

 for (auto [key, value] : map.asKeyValueRange()) {
     cout << qPrintable(key) << ": " << value << endl;
     --value; // convert to JS month indexing
 }
```

## 6. 深入实践与常见坑

### 生命周期和资源边界

容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

### 状态和错误边界

要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

### 线程边界

不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

### 最容易出现的错误

不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QMap` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
