# QMultiMap

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QMultiMap` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMultiMap` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QMultiMap>`
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

- `QMultiMap()`
- `(since 6.0) QMultiMap(QMap<Key, T> &&other)`
- `(since 6.0) QMultiMap(const QMap<Key, T> &other)`
- `QMultiMap(const std::multimap<Key, T> &other)`
- `QMultiMap(std::initializer_list<std::pair<Key, T>> list)`
- `QMultiMap(std::multimap<Key, T> &&other)`
- `QMultiMap(const QMultiMap<Key, T> &other)`
- `QMultiMap(QMultiMap<Key, T> &&other)`
- `~QMultiMap()`
- `(since 6.4) auto asKeyValueRange() &&`
- `(since 6.4) auto asKeyValueRange() &`
- `(since 6.4) auto asKeyValueRange() const &&`
- `(since 6.4) auto asKeyValueRange() const &`
- `QMultiMap<Key, T>::iterator begin()`
- `QMultiMap<Key, T>::const_iterator begin() const`
- `QMultiMap<Key, T>::const_iterator cbegin() const`
- `QMultiMap<Key, T>::const_iterator cend() const`
- `void clear()`
- `QMultiMap<Key, T>::const_iterator constBegin() const`
- `QMultiMap<Key, T>::const_iterator constEnd() const`
- `QMultiMap<Key, T>::const_iterator constFind(const Key &key) const`
- `QMultiMap<Key, T>::const_iterator constFind(const Key &key, const T &value) const`
- `QMultiMap<Key, T>::const_key_value_iterator constKeyValueBegin() const`
- `QMultiMap<Key, T>::const_key_value_iterator constKeyValueEnd() const`
- `bool contains(const Key &key) const`
- `bool contains(const Key &key, const T &value) const`
- `QMultiMap<Key, T>::size_type count(const Key &key) const`
- `QMultiMap<Key, T>::size_type count(const Key &key, const T &value) const`
- `QMultiMap<Key, T>::size_type count() const`
- `bool empty() const`
- `QMultiMap<Key, T>::iterator end()`
- `QMultiMap<Key, T>::const_iterator end() const`
- `std::pair<QMultiMap<Key, T>::iterator, QMultiMap<Key, T>::iterator> equal_range(const Key &key)`
- `std::pair<QMultiMap<Key, T>::const_iterator, QMultiMap<Key, T>::const_iterator> equal_range(const Key &key) const`
- `QMultiMap<Key, T>::iterator erase(QMultiMap<Key, T>::const_iterator pos)`
- `(since 6.0) QMultiMap<Key, T>::iterator erase(QMultiMap<Key, T>::const_iterator first, QMultiMap<Key, T>::const_iterator last)`
- `QMultiMap<Key, T>::iterator find(const Key &key)`
- `QMultiMap<Key, T>::const_iterator find(const Key &key) const`
- `QMultiMap<Key, T>::const_iterator find(const Key &key, const T &value) const`
- `T & first()`
- `const T & first() const`
- `const Key & firstKey() const`
- `QMultiMap<Key, T>::iterator insert(const Key &key, const T &value)`
- `QMultiMap<Key, T>::iterator insert(QMultiMap<Key, T>::const_iterator pos, const Key &key, const T &value)`
- `bool isEmpty() const`
- `Key key(const T &value, const Key &defaultKey = Key()) const`
- `QMultiMap<Key, T>::key_iterator keyBegin() const`
- `QMultiMap<Key, T>::key_iterator keyEnd() const`
- `QMultiMap<Key, T>::key_value_iterator keyValueBegin()`
- `QMultiMap<Key, T>::const_key_value_iterator keyValueBegin() const`
- `QMultiMap<Key, T>::key_value_iterator keyValueEnd()`
- `QMultiMap<Key, T>::const_key_value_iterator keyValueEnd() const`
- `QList<Key> keys() const`
- `QList<Key> keys(const T &value) const`
- `T & last()`
- `const T & last() const`
- `const Key & lastKey() const`
- `QMultiMap<Key, T>::iterator lowerBound(const Key &key)`
- `QMultiMap<Key, T>::const_iterator lowerBound(const Key &key) const`
- `QMultiMap<Key, T>::size_type remove(const Key &key)`
- `QMultiMap<Key, T>::size_type remove(const Key &key, const T &value)`
- `(since 6.1) QMultiMap<Key, T>::size_type removeIf(Predicate pred)`
- `QMultiMap<Key, T>::iterator replace(const Key &key, const T &value)`
- `QMultiMap<Key, T>::size_type size() const`
- `void swap(QMultiMap<Key, T> &other)`
- `T take(const Key &key)`
- `std::multimap<Key, T> toStdMultiMap() const &`
- `QList<Key> uniqueKeys() const`
- `QMultiMap<Key, T> & unite(QMultiMap<Key, T> &&other)`
- `QMultiMap<Key, T> & unite(const QMultiMap<Key, T> &other)`
- `QMultiMap<Key, T>::iterator upperBound(const Key &key)`
- `QMultiMap<Key, T>::const_iterator upperBound(const Key &key) const`
- `T value(const Key &key, const T &defaultValue = T()) const`
- `QList<T> values() const`
- `QList<T> values(const Key &key) const`
- `QMultiMap<Key, T> & operator=(QMultiMap<Key, T> &&other)`
- `QMultiMap<Key, T> & operator=(const QMultiMap<Key, T> &other)`

### 相关非成员函数

- `(since 6.1) qsizetype erase_if(QMultiMap<Key, T> &map, Predicate pred)`
- `bool operator!=(const QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`
- `QMultiMap<Key, T> operator+(const QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`
- `QMultiMap<Key, T> operator+=(QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QMultiMap<Key, T> &map)`
- `bool operator==(const QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`
- `QDataStream & operator>>(QDataStream &in, QMultiMap<Key, T> &map)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QMultiMap::ConstIterator`

**作用与语义：**

Qt风格的同义词`QMultiMap::const_iterator`。

### `QMultiMap::Iterator`

**作用与语义：**

Qt风格的同义词，代表`QMultiMap::iterator`。

### `QMultiMap::const_key_value_iterator`

**作用与语义：**

QMultiMap：：const_key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QMultiMap`。
QMultiMap：：const_key_value_iterator 本质上与 `QMultiMap::const_iterator` 相同，区别在于 operator*() 返回的是键值对而非值。

### `[alias] QMultiMap::difference_type`

**作用与语义：**

Typedef 用于ptrdiff_t。提供 STL 兼容性。

### `[alias] QMultiMap::key_type`

**作用与语义：**

Typedef 用于键。提供 STL 兼容性。

### `QMultiMap::key_value_iterator`

**作用与语义：**

QMultiMap：：key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QMultiMap`。
QMultiMap：：key_value_iterator 本质上与 `QMultiMap::iterator` 相同，区别在于 operator*() 返回的是键值对而非值。

### `[alias] QMultiMap::mapped_type`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `[alias] QMultiMap::size_type`

**作用与语义：**

类型定义用于国际语言。提供支持STL兼容性。

### `QMultiMap::QMultiMap()`

**作用与语义：**

构建一个空的多重映射。

### `[explicit, since 6.0] QMultiMap::QMultiMap(QMap<Key, T> &&other)`

**作用与语义：**

如果`other`共享，则构造多重映射作为`other`的复制。否则，通过移动`other`中的元素构造多映射。

### `[explicit, since 6.0] QMultiMap::QMultiMap(const QMap<Key, T> &other)`

**作用与语义：**

构建一个多映射，作为`other`的复制品。

### `[explicit] QMultiMap::QMultiMap(const std::multimap<Key, T> &other)`

**作用与语义：**

复制了`other`。

### `QMultiMap::QMultiMap(std::initializer_list<std::pair<Key, T>> list)`

**作用与语义：**

构造一个多映射，包含初始化器列表中每个元素的副本 `list`。

### `[explicit] QMultiMap::QMultiMap(std::multimap<Key, T> &&other)`

**作用与语义：**

通过从`other`移动来构造多映射。

### `[default] QMultiMap::QMultiMap(const QMultiMap<Key, T> &other)`

**作用与语义：**

他制造了一份`other`的复制品。
该操作发生在常数时间内，因为QMultiMap是隐式共享的。这使得从函数返回QMultiMap的速度非常快。如果共享实例被修改，它会被复制（写时复制），这需要线性时间。

### `[default] QMultiMap::QMultiMap(QMultiMap<Key, T> &&other)`

**作用与语义：**

Move-构造一个QMultiMap实例，使其指向`other`指向的同一对象。

### `[default] QMultiMap::~QMultiMap()`

**作用与语义：**

销毁多映射。对多映射中值的引用以及该多映射上的所有迭代符的引用均无效。

### `[since 6.4] auto QMultiMap::asKeyValueRange() const &&`

**作用与语义：**

返回一个范围对象，允许在该多映射上以键值对形式迭代。例如，该范围对象可以结合结构化绑定声明，用于基于范围的for循环：
注意，键和通过这种方式获得的值都是多映射中的引用。具体来说，变异值会修改映射本身。

**官方示例：**

```cpp
 QMultiMap<QString, int> map;
 map.insert("January", 1);
 map.insert("February", 2);
 // ...
 map.insert("December", 12);

 for (auto [key, value] : map.asKeyValueRange()) {
     cout << qPrintable(key) << ": " << value << endl;
     --value; // convert to JS month indexing
 }
```

### `QMultiMap<Key, T>::iterator QMultiMap::begin()`

**作用与语义：**

返回一个STL风格的迭代器，指向多映射中的第一个项目。

### `QMultiMap<Key, T>::const_iterator QMultiMap::begin() const`

**作用与语义：**

返回一个STL风格的迭代器，指向多映射中的第一个项目。

### `QMultiMap<Key, T>::const_iterator QMultiMap::cbegin() const`

**作用与语义：**

返回一个const型STL式迭代器，指向多映射中的第一个项目。

### `QMultiMap<Key, T>::const_iterator QMultiMap::cend() const`

**作用与语义：**

返回一个const型STL式迭代器，指向多映射中最后一个项之后的虚构项。

### `void QMultiMap::clear()`

**作用与语义：**

移除多地图上的所有物品。

### `QMultiMap<Key, T>::const_iterator QMultiMap::constBegin() const`

**作用与语义：**

返回一个const型STL式迭代器，指向多映射中的第一个项目。

### `QMultiMap<Key, T>::const_iterator QMultiMap::constEnd() const`

**作用与语义：**

返回一个const型STL式迭代器，指向多映射中最后一个项之后的虚构项。

### `QMultiMap<Key, T>::const_iterator QMultiMap::constFind(const Key &key) const`

**作用与语义：**

返回一个 cont 迭代器，指向多映射中键为 `key` 的项目。
如果多映射中没有键为`key`的项，函数返回`constEnd()`。

### `QMultiMap<Key, T>::const_iterator QMultiMap::constFind(const Key &key, const T &value) const`

**作用与语义：**

返回一个迭代器，指向键为`key`的项目，映射中`value`值。
如果映射中没有这样的项，函数返回`constEnd()`。

### `QMultiMap<Key, T>::const_key_value_iterator QMultiMap::constKeyValueBegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向多映射中的第一个条目。

### `QMultiMap<Key, T>::const_key_value_iterator QMultiMap::constKeyValueEnd() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向多映射最后一个条目之后的虚数条目。

### `bool QMultiMap::contains(const Key &key) const`

**作用与语义：**

如果多映射包含键为`key`的项，返回`true`;否则返回`false`。

### `bool QMultiMap::contains(const Key &key, const T &value) const`

**作用与语义：**

如果多映射包含键为`key`、值为`value`的项，返回`true`;否则返回`false`。

### `QMultiMap<Key, T>::size_type QMultiMap::count(const Key &key) const`

**作用与语义：**

返回与密钥`key`相关的项目数量。

### `QMultiMap<Key, T>::size_type QMultiMap::count(const Key &key, const T &value) const`

**作用与语义：**

返回带有密钥`key`和值`value`的项目数量。

### `QMultiMap<Key, T>::size_type QMultiMap::count() const`

**作用与语义：**

和`size()`一样。

### `bool QMultiMap::empty() const`

**作用与语义：**

该函数是为了STL兼容性而提供。它等价于`isEmpty()`，映射为空时返回真;否则返回假。

### `QMultiMap<Key, T>::iterator QMultiMap::end()`

**作用与语义：**

返回一个STL风格的迭代子，指向多映射中最后一个项之后的虚构项。

### `QMultiMap<Key, T>::const_iterator QMultiMap::end() const`

**作用与语义：**

返回一个STL风格的迭代子，指向多映射中最后一个项之后的虚构项。

### `std::pair<QMultiMap<Key, T>::iterator, QMultiMap<Key, T>::iterator> QMultiMap::equal_range(const Key &key)`

**作用与语义：**

返回一对迭代子，界定`[first, second)`值的范围，这些值存储在`key`下。

### `std::pair<QMultiMap<Key, T>::const_iterator, QMultiMap<Key, T>::const_iterator> QMultiMap::equal_range(const Key &key) const`

**作用与语义：**

返回一对迭代子，界定`[first, second)`值的范围，这些值存储在`key`下。

### `QMultiMap<Key, T>::iterator QMultiMap::erase(QMultiMap<Key, T>::const_iterator pos)`

**作用与语义：**

从多映射中移除迭代器`pos`指向的（键，值）对，并返回迭代器到映射中的下一个项。
注意：迭代子`pos`必须有效且可去引用。

### `[since 6.0] QMultiMap<Key, T>::iterator QMultiMap::erase(QMultiMap<Key, T>::const_iterator first, QMultiMap<Key, T>::const_iterator last)`

**作用与语义：**

从多映射中移除迭代器范围[`first`， `last`）所指向的（键、值）对。返回迭代器到多映射中最后移除元素后的项目。
注意：`[first, last)`范围必须是`*this`有效的范围。

### `QMultiMap<Key, T>::iterator QMultiMap::find(const Key &key)`

**作用与语义：**

返回一个迭代器，指向多映射中键为`key`的项目。
如果多映射中没有键为`key`的项，函数返回`end()`。
如果映射包含多个键为`key`的项，该函数返回一个指向最近插入值的迭代器。其他值可以通过递增迭代器来访问。例如，这里有一段代码可以遍历所有具有相同键的项：

**官方示例：**

```cpp
 auto i = multimap.find("plenty");
 while (i != multimap.end() && i.key() == "plenty") {
     cout << i.value() << endl;
     ++i;
 }

 // better:
 auto [i, end] = multimap.equal_range("plenty");
 while (i != end) {
     cout << i.value() << endl;
     ++i;
 }
```

### `QMultiMap<Key, T>::const_iterator QMultiMap::find(const Key &key) const`

**作用与语义：**

返回一个迭代器，指向多映射中键为`key`的项目。
如果多映射中没有键为`key`的项，函数返回`end()`。
如果映射包含多个键为`key`的项，该函数返回一个指向最近插入值的迭代器。其他值可以通过递增迭代器来访问。例如，这里有一段代码可以遍历所有具有相同键的项：

**官方示例：**

```cpp
 auto i = multimap.find("plenty");
 while (i != multimap.end() && i.key() == "plenty") {
     cout << i.value() << endl;
     ++i;
 }

 // better:
 auto [i, end] = multimap.equal_range("plenty");
 while (i != end) {
     cout << i.value() << endl;
     ++i;
 }
```

### `QMultiMap<Key, T>::const_iterator QMultiMap::find(const Key &key, const T &value) const`

**作用与语义：**

返回一个const迭代器，指向映射中`key`和`value`的对象。
如果映射中没有此类项，函数返回`end()`。
如果映射包含多个具有指定`key`的项，该函数返回一个 cont 迭代器，指向最近插入的值。

### `T &QMultiMap::first()`

**作用与语义：**

返回多映射中第一个值的引用，即映射到最小键的值。该函数假设多映射不是空的。
当调用非共享（或const版本）时，执行时间常数。

### `const T &QMultiMap::first() const`

**作用与语义：**

返回多映射中第一个值的引用，即映射到最小键的值。该函数假设多映射不是空的。
当调用非共享（或const版本）时，执行时间常数。

### `const Key &QMultiMap::firstKey() const`

**作用与语义：**

返回多映射中最小键的引用。该函数假设多映射不是空的。
该程序执行时间为常数。

### `QMultiMap<Key, T>::iterator QMultiMap::insert(const Key &key, const T &value)`

**作用与语义：**

插入一个带有密钥`key`且值为`value`的新项。
如果映射中已有具有相同键的项，该函数会直接创建一个新的键。（这种行为不同于`replace()`，后者会覆盖已有项的值。）。
返回一个迭代子，指向新元素。

### `QMultiMap<Key, T>::iterator QMultiMap::insert(QMultiMap<Key, T>::const_iterator pos, const Key &key, const T &value)`

**作用与语义：**

插入一个新物品，键`key`和值`value`，并附有提示`pos`建议插入位置。
如果用`constBegin()`作为提示，表示`key`小于多映射中的任何键，而`constEnd()`则表示`key`（严格来说）大于多映射中的任何键。否则提示应满足条件 （`pos` - 1）。`key()` < `key` <= pos。`key()`。如果提示`pos`错误，则忽略，进行常规插入。
如果提示正确且多映射未共享，插入映射在摊销常数时间内执行。
如果地图中已有带有相同键的物品，这个函数会直接创建一个新的。
从排序数据创建多映射时，先插入最大键（`constBegin()`）比按排序顺序插入`constEnd()`快，因为 `constEnd()` - 1（用于检查提示有效）需要对数时间。
返回一个迭代子，指向新元素。
注意：要小心提示。从旧共享实例提供迭代器可能会崩溃，但也有可能无声破坏多地图和`pos`多地图。

### `bool QMultiMap::isEmpty() const`

**作用与语义：**

如果多映射中没有任何项目，则返回`true`;否则返回 false。

### `Key QMultiMap::key(const T &value, const Key &defaultKey = Key()) const`

**作用与语义：**

返回第一个值为`value`的键;如果多映射中没有值为`value`的项，则返回`defaultKey`键。如果没有提供`defaultKey`，函数返回一个默认构造的键。
该函数可能较慢（线性时间），因为`QMultiMap`的内部数据结构优化为按键快速查找，而非按值。

### `QMultiMap<Key, T>::key_iterator QMultiMap::keyBegin() const`

**作用与语义：**

返回一个指向多映射第一个键的const STL风格迭代器。

### `QMultiMap<Key, T>::key_iterator QMultiMap::keyEnd() const`

**作用与语义：**

返回一个const型STL式迭代器，指向多映射最后一个键后的虚数项。

### `QMultiMap<Key, T>::key_value_iterator QMultiMap::keyValueBegin()`

**作用与语义：**

返回一个STL风格的迭代子，指向多映射中的第一个条目。

### `QMultiMap<Key, T>::const_key_value_iterator QMultiMap::keyValueBegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向多映射中的第一个条目。

### `QMultiMap<Key, T>::key_value_iterator QMultiMap::keyValueEnd()`

**作用与语义：**

返回一个STL风格的迭代子，指向多映射中最后一个条目之后的虚构条目。

### `QMultiMap<Key, T>::const_key_value_iterator QMultiMap::keyValueEnd() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向多映射最后一个条目之后的虚数条目。

### `QList<Key> QMultiMap::keys() const`

**作用与语义：**

返回一个包含多映射中所有键的列表，按升序排列。在多映射中多次出现的键也会在列表中多次出现。
顺序保证与`values()`使用相同。
该函数会以线性时间创建新的列表。通过从`keyBegin()`迭代到`keyEnd()`，可以避免所需的时间和内存消耗。

### `QList<Key> QMultiMap::keys(const T &value) const`

**作用与语义：**

返回包含所有与值`value`相关的键的列表，按升序返回。
该函数可能较慢（线性时间），因为`QMultiMap`的内部数据结构优化为按键快速查找，而非按值。

### `T &QMultiMap::last()`

**作用与语义：**

返回多映射中最后一个值的引用，即映射到最大键的值。该函数假设映射不是空的。
当调用非共享（或const版本）时，执行时间常数。

### `const T &QMultiMap::last() const`

**作用与语义：**

返回多映射中最后一个值的引用，即映射到最大键的值。该函数假设映射不是空的。
当调用非共享（或const版本）时，执行时间常数。

### `const Key &QMultiMap::lastKey() const`

**作用与语义：**

返回多映射中最大密钥的引用。该函数假设多映射不是空的。
该程序执行时间为常数。

### `QMultiMap<Key, T>::iterator QMultiMap::lowerBound(const Key &key)`

**作用与语义：**

返回一个迭代器，指向映射中键为`key`的第一个项目。如果映射中没有键为`key`的项，函数返回一个迭代器到键数较大的最近项。
如果映射包含多个键为`key`的项，该函数返回一个指向最近插入值的迭代器。其他值可以通过递增迭代器来访问。例如，这里有一段代码对所有具有相同键的项进行迭代：

**官方示例：**

```cpp
 QMultiMap<int, QString> multimap;
 multimap.insert(1, "one");
 multimap.insert(5, "five");
 multimap.insert(5, "five (2)");
 multimap.insert(10, "ten");

 multimap.lowerBound(0);      // returns iterator to (1, "one")
 multimap.lowerBound(1);      // returns iterator to (1, "one")
 multimap.lowerBound(2);      // returns iterator to (5, "five")
 multimap.lowerBound(5);      // returns iterator to (5, "five")
 multimap.lowerBound(6);      // returns iterator to (10, "ten")
 multimap.lowerBound(10);     // returns iterator to (10, "ten")
 multimap.lowerBound(999);    // returns end()
```

### `QMultiMap<Key, T>::const_iterator QMultiMap::lowerBound(const Key &key) const`

**作用与语义：**

返回一个迭代器，指向映射中键为`key`的第一个项目。如果映射中没有键为`key`的项，函数返回一个迭代器到键数较大的最近项。
如果映射包含多个键为`key`的项，该函数返回一个指向最近插入值的迭代器。其他值可以通过递增迭代器来访问。例如，这里有一段代码对所有具有相同键的项进行迭代：

**官方示例：**

```cpp
 QMultiMap<int, QString> multimap;
 multimap.insert(1, "one");
 multimap.insert(5, "five");
 multimap.insert(5, "five (2)");
 multimap.insert(10, "ten");

 multimap.lowerBound(0);      // returns iterator to (1, "one")
 multimap.lowerBound(1);      // returns iterator to (1, "one")
 multimap.lowerBound(2);      // returns iterator to (5, "five")
 multimap.lowerBound(5);      // returns iterator to (5, "five")
 multimap.lowerBound(6);      // returns iterator to (10, "ten")
 multimap.lowerBound(10);     // returns iterator to (10, "ten")
 multimap.lowerBound(999);    // returns end()
```

### `QMultiMap<Key, T>::size_type QMultiMap::remove(const Key &key)`

**作用与语义：**

移除所有带有钥匙`key`的物品从多地图中移除。返回移除物品数量。

### `QMultiMap<Key, T>::size_type QMultiMap::remove(const Key &key, const T &value)`

**作用与语义：**

移除所有具有关键 `key` 和 `value` 的物品从多地图中移除。返回移除的物品数量。

### `[since 6.1] template <typename Predicate> QMultiMap<Key, T>::size_type QMultiMap::removeIf(Predicate pred)`

**作用与语义：**

从多重映射中移除所有谓词返回为真`pred`的元素。
该函数支持的谓词要么取类型为`QMultiMap<Key, T>::iterator`，要么参数为`std::pair<const Key &, T &>`。
返回被移除的元素数量（如果有的话）。

### `QMultiMap<Key, T>::iterator QMultiMap::replace(const Key &key, const T &value)`

**作用与语义：**

插入一个带有键`key`和值为`value`的新项。
如果已有具有密钥`key`的项目，该项的值将被替换为`value`。
如果有多个具有键`key`的项目，最近插入的物品的值会被替换为`value`。
返回一个迭代器，指向新元素/更新元素。

### `QMultiMap<Key, T>::size_type QMultiMap::size() const`

**作用与语义：**

返回多映射中（键，值）对的数量。

### `[noexcept] void QMultiMap::swap(QMultiMap<Key, T> &other)`

**作用与语义：**

将多地图与`other`交换。这个操作非常快，从未失败过。

### `T QMultiMap::take(const Key &key)`

**作用与语义：**

从多映射中移除带有密钥`key`的物品，并返回与之相关的值。
如果该项不存在于多映射中，函数仅返回默认构造值。如果映射中有多个 `key` 项，则只移除并返回最近插入的项。
如果不使用返回值，`remove()`效率更高。

### `std::multimap<Key, T> QMultiMap::toStdMultiMap() const &`

**作用与语义：**

返回与此 `QMultiMap` 相当的 STL 多映射。

### `QList<Key> QMultiMap::uniqueKeys() const`

**作用与语义：**

返回包含映射中所有键的列表，按升序返回。映射中多次出现的键在返回列表中只出现一次。

### `QMultiMap<Key, T> &QMultiMap::unite(QMultiMap<Key, T> &&other)`

**作用与语义：**

将`other`映射中的所有物品移动到该映射中。如果某个键在两个映射中都存在，生成的映射将多次包含该键。
如果`other`被共享，则这些项目会被复制。

### `QMultiMap<Key, T> &QMultiMap::unite(const QMultiMap<Key, T> &other)`

**作用与语义：**

将`other`映射中的所有元素插入到该映射中。如果某个键在两个映射中都存在，生成的映射将多次包含该键。

### `QMultiMap<Key, T>::iterator QMultiMap::upperBound(const Key &key)`

**作用与语义：**

返回一个迭代器，指向紧接着上一个键为`key`的项目的项目。如果映射中没有键`key`的项目，函数返回一个迭代器，指向键数更大的最近项目。

**官方示例：**

```cpp
 QMultiMap<int, QString> multimap;
 multimap.insert(1, "one");
 multimap.insert(5, "five");
 multimap.insert(5, "five (2)");
 multimap.insert(10, "ten");

 multimap.upperBound(0);      // returns iterator to (1, "one")
 multimap.upperBound(1);      // returns iterator to (5, "five")
 multimap.upperBound(2);      // returns iterator to (5, "five")
 multimap.lowerBound(5);      // returns iterator to (5, "five (2)")
 multimap.lowerBound(6);      // returns iterator to (10, "ten")
 multimap.upperBound(10);     // returns end()
 multimap.upperBound(999);    // returns end()
```

### `QMultiMap<Key, T>::const_iterator QMultiMap::upperBound(const Key &key) const`

**作用与语义：**

返回一个迭代器，指向紧接着上一个键为`key`的项目的项目。如果映射中没有键`key`的项目，函数返回一个迭代器，指向键数更大的最近项目。

**官方示例：**

```cpp
 QMultiMap<int, QString> multimap;
 multimap.insert(1, "one");
 multimap.insert(5, "five");
 multimap.insert(5, "five (2)");
 multimap.insert(10, "ten");

 multimap.upperBound(0);      // returns iterator to (1, "one")
 multimap.upperBound(1);      // returns iterator to (5, "five")
 multimap.upperBound(2);      // returns iterator to (5, "five")
 multimap.lowerBound(5);      // returns iterator to (5, "five (2)")
 multimap.lowerBound(6);      // returns iterator to (10, "ten")
 multimap.upperBound(10);     // returns end()
 multimap.upperBound(999);    // returns end()
```

### `T QMultiMap::value(const Key &key, const T &defaultValue = T()) const`

**作用与语义：**

返回与密钥`key`关联的值。
如果多映射中没有关键字为`key`的项，函数返回`defaultValue`。如果没有指定`defaultValue`，函数返回默认构造的值。如果多映射中有多个 `key` 的项，则返回最近插入的项值。

### `QList<T> QMultiMap::values() const`

**作用与语义：**

返回包含映射中所有值的列表，按键值的升序排列。如果一个键关联多个值，则该键的所有值都会在列表中，而不仅仅是最近插入的值。

### `QList<T> QMultiMap::values(const Key &key) const`

**作用与语义：**

返回包含所有与键`key`相关的值的列表，从最近插入到最近插入的。

### `[default] QMultiMap<Key, T> &QMultiMap::operator=(QMultiMap<Key, T> &&other)`

**作用与语义：**

Move-assign `other`到该`QMultiMap`实例。

### `[default] QMultiMap<Key, T> &QMultiMap::operator=(const QMultiMap<Key, T> &other)`

**作用与语义：**

将`other`分配到该多映射，并返回该多映射的引用。

### `[since 6.1] template < typename Key, typename T, typename Predicate > qsizetype erase_if(QMultiMap<Key, T> &map, Predicate pred)`

**作用与语义：**

从多映射`map`中移除所有谓词 `pred` 返回为真的元素。
该函数支持的谓词要么取类型为`QMultiMap<Key, T>::iterator`，要么参数为类型为`std::pair<const Key &, T &>`。
返回被移除的元素数量（如果有的话）。

### `bool operator!=(const QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`

**作用与语义：**

如果 `lhs` 不等于 `rhs`，则返回 `true`；否则返回 `false`。
如果两个多重映射包含相同的（键，值）对，且顺序相同（重复键的顺序很重要），则认为它们相等。
此函数要求键类型和值类型实现 `operator==()`。

### `template <typename Key, typename T> QMultiMap<Key, T> operator+(const QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`

**作用与语义：**

返回一个映射，包含`lhs`映射中的所有元素，以及`rhs`中的所有元素。如果某个键在两个映射中都存在，生成的映射将多次包含该键。

### `template <typename Key, typename T> QMultiMap<Key, T> operator+=(QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`

**作用与语义：**

将`rhs`地图中的所有物品插入`lhs`映射，并返回生成的映射。

### `template <typename Key, typename T> QDataStream &operator<<(QDataStream &out, const QMultiMap<Key, T> &map)`

**作用与语义：**

写入多映射`map`流`out`。
该函数需要键型和值类型来实现`operator<<()`。

### `bool operator==(const QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`

**作用与语义：**

如果 `lhs` 等于 `rhs`，则返回 `operator==()`；否则返回 false。两个多重映射被认为是相等的，当且仅当它们包含相同的（键, 值）对，并且顺序相同（对于重复键顺序很重要）。此函数要求键和值类型实现 `operator==()`。

### `template <typename Key, typename T> QDataStream &operator>>(QDataStream &in, QMultiMap<Key, T> &map)`

**作用与语义：**

读取`in`溪的地图到`map`。
该函数需要键型和值类型来实现`operator>>()`。

### `class const_iterator`

**作用与语义：**

QMultiMap：：const_iterator 类为 QMultiMap 提供了一个 STL 风格的 const 迭代器。
`QMultiMap`<密钥，T>：：const_iterator 允许你对一个`QMultiMap`进行迭代。如果你想在迭代过程中修改`QMultiMap`，必须用 `QMultiMap::iterator`。通常在非连续性`QMultiMap`上使用`QMultiMap::const_iterator`是个好习惯，除非你需要通过迭代器更改`QMultiMap`。Const 迭代器速度稍快，且能提高代码的可读性。
默认的`QMultiMap::const_iterator`构造器会创建一个未初始化的迭代器。你必须用像`QMultiMap::cbegin()`、`QMultiMap::cend()`或`QMultiMap::constFind()`这样的`QMultiMap`函数初始化它，才能开始迭代。这里有一个典型的循环，它打印了映射中存储的所有（键、值）对：
这里有一个例子，去除所有点数大于10的物品：
与 `QMultiHash` 不同，`QMultiMap` 是按键顺序存储物品。共享相同键的项将依次出现，从最近到最近插入的值。
多个迭代器可以在同一多地图上使用。如果你向地图添加物品，现有的迭代器依然有效。如果你从地图上移除物品，指向已移除物品的迭代器将变成悬挂的迭代器。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。

**官方示例：**

```cpp
 QMultiMap<QString, int> multimap;
 multimap.insert("January", 1);
 multimap.insert("February", 2);
 //...
 multimap.insert("December", 12);

 for (auto i = multimap.cbegin(), end = multimap.cend(); i != end; ++i)
     cout << qPrintable(i.key()) << ": " << i.value() << endl;
```

### `class iterator`

**作用与语义：**

QMultiMap：：iterator 类为 QMultiMap 提供了一个 STL 风格的非const迭代器。
`QMultiMap`<密钥，T>：：迭代器允许你对某个`QMultiMap`进行迭代，并修改存储在特定密钥下的值（但不能修改密钥）。如果你想对const的`QMultiMap`进行迭代，应该使用`QMultiMap::const_iterator`。通常在非const的`QMultiMap`上使用`QMultiMap::const_iterator`是个好习惯，除非你需要通过迭代器更改`QMultiMap`。const迭代器速度稍快，可以提高代码的可读性。
默认的`QMultiMap::iterator`构造函数会创建一个未初始化的迭代器。你必须先用`QMultiMap`函数如`QMultiMap::begin()`、`QMultiMap::end()`或`QMultiMap::find()`初始化它，才能开始迭代。这是一个典型的循环，打印映射中存储的所有（键、值）对：
与以任意顺序存储物品的 `QMultiHash` 不同，`QMultiMap` 按键排序存储。共享相同键的物品将依次出现，从最近到最近插入的值。
这里有一个例子，将`QMultiMap`中存储的每个值增为2：
要从`QMultiMap`中移除元素，可以使用 `erase_if`（`QMultiMap`<Key， T> &map， Predicate pred）：
同一张地图上可以使用多个迭代器。如果你向地图添加物品，现有的迭代器依然有效。如果你从地图上移除物品，指向已移除物品的迭代器将变成悬挂迭代器。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。

**官方示例：**

```cpp
 for (auto i = multimap.begin(), end = multimap.end(); i != end; ++i)
     i.value() += 2;
```

### `class key_iterator`

**作用与语义：**

QMultiMap：：key_iterator 类为 QMultiMap 键提供了一个 STL 风格的 const 迭代器。
`QMultiMap::key_iterator` 本质上与 `QMultiMap::const_iterator` 相同，区别在于运算符*() 和运算符->() 返回键而非值。
对于大多数用途，`QMultiMap::iterator`和应`QMultiMap::const_iterator`，您可以通过调用`QMultiMap::iterator::key()`轻松访问密钥：
然而，为了实现`QMultiMap`键与STL风格算法之间的互操作性，我们需要一个迭代器，它不引用键而非值。有了`QMultiMap::key_iterator`，我们可以对多个键应用算法而无需调用`QMultiMap::keys()`，但这效率较低，因为创建一个临时`QList`需要`QMultiMap`迭代和内存分配。
`QMultiMap::key_iterator`是const，密钥无法修改。
默认的`QMultiMap::key_iterator`构造函数会创建一个未初始化的迭代器。你必须用像 `QMultiMap::keyBegin()` 或 `QMultiMap::keyEnd()` 这样的 `QMultiMap` 函数来初始化它。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。

**官方示例：**

```cpp
 for (auto it = multimap.cbegin(), end = multimap.cend(); it != end; ++it) {
     cout << "The key: " << it.key() << endl;
     cout << "The value: " << qPrintable(it.value()) << endl;
     cout << "Also the value: " << qPrintable(*it) << endl;
 }
```

### `ConstIterator`

**作用与语义：**

Qt风格的同义词`QMultiMap::const_iterator`。

### `Iterator`

**作用与语义：**

Qt风格的同义词，代表`QMultiMap::iterator`。

### `const_key_value_iterator`

**作用与语义：**

QMultiMap：：const_key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QMultiMap`。
QMultiMap：：const_key_value_iterator 本质上与 `QMultiMap::const_iterator` 相同，区别在于 operator*() 返回的是键值对而非值。

### `difference_type`

**作用与语义：**

Typedef 用于ptrdiff_t。提供 STL 兼容性。

### `key_type`

**作用与语义：**

Typedef 用于键。提供 STL 兼容性。

### `key_value_iterator`

**作用与语义：**

QMultiMap：：key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QMultiMap`。
QMultiMap：：key_value_iterator 本质上与 `QMultiMap::iterator` 相同，区别在于 operator*() 返回的是键值对而非值。

### `mapped_type`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `size_type`

**作用与语义：**

类型定义用于国际语言。提供支持STL兼容性。

### `(since 6.4) auto asKeyValueRange() &&`

**作用与语义：**

返回一个范围对象，允许在该多映射上以键值对形式迭代。例如，该范围对象可以结合结构化绑定声明，用于基于范围的for循环：
注意，键和通过这种方式获得的值都是多映射中的引用。具体来说，变异值会修改映射本身。

**官方示例：**

```cpp
 QMultiMap<QString, int> map;
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

`QMultiMap` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
