# QMultiHash

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QMultiHash` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMultiHash` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QMultiHash>`
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
- `const_key_value_iterator`
- `key_value_iterator`

### 公有函数

- `QMultiHash()`
- `QMultiHash(const QHash<Key, T> &other)`
- `QMultiHash(std::initializer_list<std::pair<Key, T>> list)`
- `QMultiHash(InputIterator begin, InputIterator end)`
- `(since 6.4) auto asKeyValueRange() &&`
- `(since 6.4) auto asKeyValueRange() &`
- `(since 6.4) auto asKeyValueRange() const &&`
- `(since 6.4) auto asKeyValueRange() const &`
- `QMultiHash<Key, T>::iterator begin()`
- `QMultiHash<Key, T>::const_iterator begin() const`
- `QMultiHash<Key, T>::const_iterator cbegin() const`
- `QMultiHash<Key, T>::const_iterator cend() const`
- `void clear()`
- `QMultiHash<Key, T>::const_iterator constBegin() const`
- `QMultiHash<Key, T>::const_iterator constEnd() const`
- `QMultiHash<Key, T>::const_iterator constFind(const Key &key, const T &value) const`
- `QMultiHash<Key, T>::const_key_value_iterator constKeyValueBegin() const`
- `QMultiHash<Key, T>::const_key_value_iterator constKeyValueEnd() const`
- `bool contains(const Key &key, const T &value) const`
- `qsizetype count(const Key &key, const T &value) const`
- `QMultiHash<Key, T>::iterator emplace(Key &&key, Args &&... args)`
- `QMultiHash<Key, T>::iterator emplace(const Key &key, Args &&... args)`
- `QMultiHash<Key, T>::iterator emplaceReplace(Key &&key, Args &&... args)`
- `QMultiHash<Key, T>::iterator emplaceReplace(const Key &key, Args &&... args)`
- `QMultiHash<Key, T>::iterator end()`
- `QMultiHash<Key, T>::const_iterator end() const`
- `std::pair<QMultiHash<Key, T>::iterator, QMultiHash<Key, T>::iterator> equal_range(const Key &key)`
- `std::pair<QMultiHash<Key, T>::const_iterator, QMultiHash<Key, T>::const_iterator> equal_range(const Key &key) const`
- `QMultiHash<Key, T>::iterator erase(QMultiHash<Key, T>::const_iterator pos)`
- `QMultiHash<Key, T>::iterator find(const Key &key, const T &value)`
- `QMultiHash<Key, T>::const_iterator find(const Key &key, const T &value) const`
- `QMultiHash<Key, T>::iterator insert(const Key &key, const T &value)`
- `(since 6.11) QMultiHash<Key, T>::iterator insert(Key &&key, T &&value)`
- `(since 6.11) QMultiHash<Key, T>::iterator insert(Key &&key, const T &value)`
- `(since 6.11) QMultiHash<Key, T>::iterator insert(const Key &key, T &&value)`
- `Key key(const T &value) const`
- `Key key(const T &value, const Key &defaultKey) const`
- `QMultiHash<Key, T>::key_iterator keyBegin() const`
- `QMultiHash<Key, T>::key_iterator keyEnd() const`
- `QMultiHash<Key, T>::key_value_iterator keyValueBegin()`
- `QMultiHash<Key, T>::const_key_value_iterator keyValueBegin() const`
- `QMultiHash<Key, T>::key_value_iterator keyValueEnd()`
- `QMultiHash<Key, T>::const_key_value_iterator keyValueEnd() const`
- `QList<Key> keys() const`
- `qsizetype remove(const Key &key)`
- `qsizetype remove(const Key &key, const T &value)`
- `(since 6.1) qsizetype removeIf(Predicate pred)`
- `QMultiHash<Key, T>::iterator replace(const Key &key, const T &value)`
- `void swap(QMultiHash<Key, T> &other)`
- `T take(const Key &key)`
- `QList<Key> uniqueKeys() const`
- `(since 6.0) QMultiHash<Key, T> & unite(const QHash<Key, T> &other)`
- `QMultiHash<Key, T> & unite(const QMultiHash<Key, T> &other)`
- `T value(const Key &key) const`
- `T value(const Key &key, const T &defaultValue) const`
- `QList<T> values() const`
- `QList<T> values(const Key &key) const`
- `QMultiHash<Key, T> operator+(const QMultiHash<Key, T> &other) const`
- `QMultiHash<Key, T> & operator+=(const QMultiHash<Key, T> &other)`
- `T & operator[](const Key &key)`

### 相关非成员函数

- `(since 6.1) qsizetype erase_if(QMultiHash<Key, T> &hash, Predicate pred)`
- `size_t qHash(const QMultiHash<Key, T> &key, size_t seed = 0)`
- `bool operator!=(const QMultiHash<Key, T> &lhs, const QMultiHash<Key, T> &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QMultiHash<Key, T> &hash)`
- `bool operator==(const QMultiHash<Key, T> &lhs, const QMultiHash<Key, T> &rhs)`
- `QDataStream & operator>>(QDataStream &in, QMultiHash<Key, T> &hash)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QMultiHash::const_key_value_iterator`

**作用与语义：**

QMultiHash：：const_key_value_iterator typedef 提供了一个 STL 风格的 cont 迭代器用于 `QMultiHash`。
QMultiHash：：const_key_value_iterator 本质上与 `QMultiHash::const_iterator` 相同，区别在于运算符*() 返回的是键值对而非值。

### `QMultiHash::key_value_iterator`

**作用与语义：**

QMultiHash：：key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QMultiHash`。
QMultiHash：：key_value_iterator 本质上与 `QMultiHash::iterator` 相同，区别在于运算符*() 返回的是键值对而非值。

### `[noexcept] QMultiHash::QMultiHash()`

**作用与语义：**

构造一个空哈希。

### `[explicit] QMultiHash::QMultiHash(const QHash<Key, T> &other)`

**作用与语义：**

构建`other`的副本（可以是`QHash`或QMultiHash）。

### `QMultiHash::QMultiHash(std::initializer_list<std::pair<Key, T>> list)`

**作用与语义：**

构建一个多哈希，初始化器列表中的每个元素都副本 `list`。

### `template <typename InputIterator> QMultiHash::QMultiHash(InputIterator begin, InputIterator end)`

**作用与语义：**

构造一个多重哈希，每个迭代范围中的元素都有一个副本 [`begin`， `end`）。由该范围复制的元素必须是具有`first`和`second`数据成员的对象（如`std::pair`），分别可转换为`Key`和可转换为`T`;或者迭代器必须有`key()`和 `value()`成员函数，分别返回键可转换为`Key`和返回可转换值为 `T`。

### `[since 6.4] auto QMultiHash::asKeyValueRange() const &&`

**作用与语义：**

返回一个范围对象，允许对该哈希值进行迭代，作为键值对。例如，该范围对象可以用于基于范围的for循环，结合结构化绑定声明：
注意，通过这种方式获得的密钥和值都是对哈希中密钥的引用。具体来说，变异值会修改哈希本身。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

**官方示例：**

```cpp
 QMultiHash<QString, int> hash;
 hash.insert("January", 1);
 hash.insert("February", 2);
 // ...
 hash.insert("December", 12);

 for (auto [key, value] : hash.asKeyValueRange()) {
     cout << qPrintable(key) << ": " << value << endl;
     --value; // convert to JS month indexing
 }
```

### `QMultiHash<Key, T>::iterator QMultiHash::begin()`

**作用与语义：**

返回一个指向哈希中第一个项的STL式迭代器。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::begin() const`

**作用与语义：**

警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::cbegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向哈希中的第一个项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::cend() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向哈希中最后一个项之后的虚数项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept(...)] void QMultiHash::clear()`

**作用与语义：**

移除哈希中的所有项目，释放所有内存。
注意：该功能仅在`std::is_nothrow_destructible<Node>::value` `true`时才适用。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::constBegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向哈希中的第一个项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::constEnd() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向哈希中最后一个项之后的虚数项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::constFind(const Key &key, const T &value) const`

**作用与语义：**

返回一个迭代器，指向哈希中`key`和`value`的项目。
如果哈希中没有此类项，函数返回`constEnd()`。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::const_key_value_iterator QMultiHash::constKeyValueBegin() const`

**作用与语义：**

返回一个const型STL风格的迭代器，指向哈希中的第一个条目。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::const_key_value_iterator QMultiHash::constKeyValueEnd() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向哈希最后一个条目之后的虚数条目。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] bool QMultiHash::contains(const Key &key, const T &value) const`

**作用与语义：**

如果哈希包含`key` 和 `value` 的项，返回 返回 `true`;否则返回 `false`。

### `[noexcept] qsizetype QMultiHash::count(const Key &key, const T &value) const`

**作用与语义：**

返回带有`key`和`value`的物品数量。

### `template <typename... Args> QMultiHash<Key, T>::iterator QMultiHash::emplace(Key &&key, Args &&... args)`

**作用与语义：**

在容器中插入一个新元素。该新元素在原地构造，使用`args`作为其构造的参数。
如果哈希中已有具有相同键的项，该函数会直接创建一个新的。（这种行为不同于`replace()`，后者会覆盖已有项的值。）。
返回一个迭代子，指向新元素。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `template <typename... Args> QMultiHash<Key, T>::iterator QMultiHash::emplaceReplace(Key &&key, Args &&... args)`

**作用与语义：**

将一个新元素插入容器。该新元素在原地构造，使用`args`作为其构造的参数。
如果哈希中已有具有相同键的项，该项的值会被由`args`构造的值替换。
返回一个迭代子，指向新元素。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::iterator QMultiHash::end()`

**作用与语义：**

返回一个STL风格的迭代器，指向哈希中最后一个项之后的虚数项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::end() const`

**作用与语义：**

返回一个STL风格的迭代器，指向哈希中最后一个项之后的虚数项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `std::pair<QMultiHash<Key, T>::iterator, QMultiHash<Key, T>::iterator> QMultiHash::equal_range(const Key &key)`

**作用与语义：**

返回一对迭代器，界定`[first, second)`值的范围，这些值存储在`key`下。如果范围为空，则两个迭代器均为`end()`。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] std::pair<QMultiHash<Key, T>::const_iterator, QMultiHash<Key, T>::const_iterator> QMultiHash::equal_range(const Key &key) const`

**作用与语义：**

警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `QMultiHash<Key, T>::iterator QMultiHash::erase(QMultiHash<Key, T>::const_iterator pos)`

**作用与语义：**

从哈希中移除与迭代器`pos`关联的（键、值）对，并返回哈希中下一个项的迭代器。
该函数从不导致`QMultiHash`对其内部数据结构进行重写。这意味着在迭代过程中可以安全地调用它，且不会影响哈希中项的顺序。例如：
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

**官方示例：**

```cpp
 QMultiHash<QObject *, int> objectHash;
 //...
 QMultiHash<QObject *, int>::iterator i = objectHash.find(obj);
 while (i != objectHash.end() && i.key() == obj) {
     if (i.value() == 0) {
         i = objectHash.erase(i);
     } else {
         ++i;
     }
 }
```

### `QMultiHash<Key, T>::iterator QMultiHash::find(const Key &key, const T &value)`

**作用与语义：**

返回一个迭代器，指向`key`和`value`的项。如果哈希中没有此类项，函数返回`end()`。
如果哈希包含多个`key`和`value`的项，迭代器返回指向最近插入的项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::find(const Key &key, const T &value) const`

**作用与语义：**

警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `QMultiHash<Key, T>::iterator QMultiHash::insert(const Key &key, const T &value)`

**作用与语义：**

插入一个新项，带有`key`和值为`value`。
如果哈希中已有具有相同键的项，该函数会直接创建一个新的。（这种行为不同于`replace()`，后者会覆盖已有项的值。）。
返回一个迭代子，指向新元素。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[since 6.11] QMultiHash<Key, T>::iterator QMultiHash::insert(Key &&key, T &&value)`

**作用与语义：**

插入一个新项，带有`key`和值为`value`。
如果哈希中已有具有相同键的项，该函数会直接创建一个新的。（这种行为不同于`replace()`，后者会覆盖已有项的值。）。
返回一个迭代子，指向新元素。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] Key QMultiHash::key(const T &value, const Key &defaultKey) const`

**作用与语义：**

返回映射到`value`的第一个键。如果哈希中没有映射到`value`的项，返回`defaultKey`;如果未提供该参数，则返回默认构造的键。
该函数可能较慢（线性时间），因为`QMultiHash`的内部数据结构是通过键快速查找而优化的，而不是按值。

### `[noexcept] QMultiHash<Key, T>::key_iterator QMultiHash::keyBegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向哈希中的第一个键。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::key_iterator QMultiHash::keyEnd() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向哈希中最后一个键之后的虚数项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::key_value_iterator QMultiHash::keyValueBegin()`

**作用与语义：**

返回一个指向哈希第一个条目的STL式迭代器。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::const_key_value_iterator QMultiHash::keyValueBegin() const`

**作用与语义：**

返回一个const型STL风格的迭代器，指向哈希中的第一个条目。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::key_value_iterator QMultiHash::keyValueEnd()`

**作用与语义：**

返回一个STL风格的迭代子，指向哈希中最后一个条目之后的虚数条目。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QMultiHash<Key, T>::const_key_value_iterator QMultiHash::keyValueEnd() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向哈希最后一个条目之后的虚数条目。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `QList<Key> QMultiHash::keys() const`

**作用与语义：**

返回包含哈希中所有键的列表，顺序任意。哈希中多次出现的键也会在列表中多次出现。
顺序保证与`values()`使用的顺序相同。
该函数会以线性时间创建一个新的列表。通过从`keyBegin()`迭代到`keyEnd()`可以避免所需的时间和内存消耗。

### `qsizetype QMultiHash::remove(const Key &key)`

**作用与语义：**

从哈希中移除所有带有`key`的项目。返回被移除的物品数量。

### `qsizetype QMultiHash::remove(const Key &key, const T &value)`

**作用与语义：**

从哈希中移除所有具有`key`和值`value`的项目。返回移除的物品数量。

### `[since 6.1] template <typename Predicate> qsizetype QMultiHash::removeIf(Predicate pred)`

**作用与语义：**

从多哈希中移除所有谓词 `pred` 返回为真元素。
该函数支持的谓词要么是类型为`QMultiHash<Key, T>::iterator`，要么是类型为`std::pair<const Key &, T &>`的参数。
返回被移除的元素数量（如果有的话）。

### `QMultiHash<Key, T>::iterator QMultiHash::replace(const Key &key, const T &value)`

**作用与语义：**

插入一个新项，带有`key`和值为`value`。
如果已有`key`的物品，该物品的价值会被替换为`value`。
如果有多个`key`项，最近插入的项值会被替换为`value`。
返回一个迭代器，指向新元素/更新元素。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] void QMultiHash::swap(QMultiHash<Key, T> &other)`

**作用与语义：**

将多哈希与`other`交换。该操作非常快且从未失败。

### `T QMultiHash::take(const Key &key)`

**作用与语义：**

从哈希中移除带有`key`的项，并返回与之相关的值。
如果该项不存在于哈希中，函数仅返回默认构造的值。如果哈希中有多个`key`项，则仅移除最近插入的项。
如果不使用返回值，`remove()`效率更高。

### `QList<Key> QMultiHash::uniqueKeys() const`

**作用与语义：**

返回包含映射中所有键的列表。映射中出现多次的键在返回列表中只出现一次。

### `[since 6.0] QMultiHash<Key, T> &QMultiHash::unite(const QHash<Key, T> &other)`

**作用与语义：**

将`other`哈希中的所有项插入到该哈希中，并返回对该哈希的引用。

### `QMultiHash<Key, T> &QMultiHash::unite(const QMultiHash<Key, T> &other)`

**作用与语义：**

将`other`哈希中的所有项插入到该哈希中，并返回对该哈希的引用。

### `[noexcept] T QMultiHash::value(const Key &key, const T &defaultValue) const`

**作用与语义：**

返回与`key`关联的值。
如果哈希中没有包含`key`项，函数返回`defaultValue`，或者如果未提供该参数，则返回默认构造值。
如果哈希中有多个`key`项，则返回最近插入的项值。

### `QList<T> QMultiHash::values() const`

**作用与语义：**

返回包含哈希中所有值的列表，顺序任意。如果一个键关联多个值，则该列表中包含所有值，而不仅仅是最近插入的值。
顺序保证与`keys()`使用的顺序相同。
该函数会以线性时间创建一个新的列表。通过从`keyValueBegin()`迭代到`keyValueEnd()`可以避免这所涉及的时间和内存消耗。

### `QList<T> QMultiHash::values(const Key &key) const`

**作用与语义：**

返回与`key`相关的所有值列表，从最近插入到最近插入的。

### `QMultiHash<Key, T> QMultiHash::operator+(const QMultiHash<Key, T> &other) const`

**作用与语义：**

返回一个包含该哈希中所有项以及`other`中所有项的哈希值。如果一个键在两个哈希中都具有，则该哈希会多次包含该键。

### `QMultiHash<Key, T> &QMultiHash::operator+=(const QMultiHash<Key, T> &other)`

**作用与语义：**

将`other`哈希中的所有项插入到该哈希中，并返回对该哈希的引用。

### `T &QMultiHash::operator[](const Key &key)`

**作用与语义：**

返回与`key`关联的值作为可修改的引用。
如果哈希中没有`key`项，函数会在哈希中插入一个默认构造的值，并返回`key`的引用。
如果哈希包含多个带有`key`的项，该函数返回最近插入的值的引用。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[since 6.1] template < typename Key, typename T, typename Predicate > qsizetype erase_if(QMultiHash<Key, T> &hash, Predicate pred)`

**作用与语义：**

从多哈希`hash`中移除所有谓词返回为真的元素`pred`。
该函数支持的谓词要么取类型为`QMultiHash<Key, T>::iterator`，要么使用类型为`std::pair<const Key &, T &>`的参数。
返回被移除的元素数量（如果有的话）。

### `[noexcept(...)] template <typename Key, typename T> size_t qHash(const QMultiHash<Key, T> &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，并用`seed`来做种子计算。
qHash()必须支持 类型 `Key` 和 `T`。
注意：该功能仅在`noexcept(qHash(std::declval<Key&>())) && noexcept(qHash(std::declval<T&>()))` `true`时使用。

### `[noexcept] bool operator!=(const QMultiHash<Key, T> &lhs, const QMultiHash<Key, T> &rhs)`

**作用与语义：**

返回`true`如果`lhs`multihash 不等于`rhs`multihash；否则返回`false`如果两个多哈希包含相同的（键，值）对，它们被认为是相等的。该函数要求值类型实现`operator==()`.

### `template <typename Key, typename T> QDataStream &operator<<(QDataStream &out, const QMultiHash<Key, T> &hash)`

**作用与语义：**

写入哈希`hash`流`out`。
该函数需要键型和值类型来实现`operator<<()`。

### `[noexcept] bool operator==(const QMultiHash<Key, T> &lhs, const QMultiHash<Key, T> &rhs)`

**作用与语义：**

如果 `lhs` 多重哈希等于 `rhs` 多重哈希，则返回 `true`；否则返回 `false`。
当两个多重哈希包含相同的（键，值）对时，认为它们是相等的。
此函数要求值类型实现 `operator==()`。

### `template <typename Key, typename T> QDataStream &operator>>(QDataStream &in, QMultiHash<Key, T> &hash)`

**作用与语义：**

将流`in`的哈希值读取到`hash`。
该函数需要键型和值类型来实现`operator>>()`。

### `class const_iterator`

**作用与语义：**

QMultiHash：：const_iterator 类为 QMultiHash 提供了一个 STL 风格的 const 迭代器。
`QMultiHash`<密钥，T>：：const_iterator 允许你对一个`QMultiHash`进行迭代。如果你想在迭代过程中修改`QMultiHash`，必须用 `QMultiHash::iterator`。通常在非const的`QMultiHash`上使用Const `QMultiHash::const_iterator`是个好习惯，除非你需要通过迭代器更改`QMultiHash`。Const迭代器速度稍快，可以提高代码的可读性。
默认的`QMultiHash::const_iterator`构造器会创建一个未初始化的迭代器。你必须用`QMultiHash`函数如`QMultiHash::cbegin()`、`QMultiHash::cend()`或`QMultiHash::constFind()`初始化它，才能开始迭代。这里有一个典型的循环，打印了哈希中存储的所有（键、值）对：
与按键排序的 `QMap` 不同，`QMultiHash` 以任意顺序存储物品。唯一的保证是，共享相同键的项（因为它们是用`QMultiHash`插入的）会依次出现，从最近插入到最近插入的值。
多个迭代器可以在同一哈希上使用。但请注意，任何直接对`QMultiHash`进行的修改（插入和删除项）都可能导致迭代器失效。
插入项或调用 QMultiHash：：reserve() 或 QMultiHash：：squeeze() 等方法，可以使所有指向哈希的迭代器失效。迭代器只有在`QMultiHash`不需要增长/缩小内部哈希表时才保证有效。在重排操作 ahs 发生后使用任何迭代器会导致行为未定义。
如果你需要长时间保持迭代器，我们建议你使用`QMultiMap`而非`QMultiHash`。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。

**官方示例：**

```cpp
     QHash<QString, int> hash;
     hash.insert("January", 1);
     hash.insert("February", 2);
     //...
     hash.insert("December", 12);

     for (auto i = hash.cbegin(), end = hash.cend(); i != end; ++i)
         cout << qPrintable(i.key()) << ": " << i.value() << endl;
```

### `class iterator`

**作用与语义：**

QMultiHash：：iterator 类为 QMultiHash 提供了一个 STL 风格的非const迭代器。
`QMultiHash`<密钥，T，T>：：迭代器允许你对某个`QMultiHash`进行迭代，并修改与某个密钥相关的值（但不能修改密钥）。如果你想对const的某个`QMultiHash`进行迭代，应该使用`QMultiHash::const_iterator`。通常在非const的代`QMultiHash`上也使用`QMultiHash::const_iterator`是个好习惯，除非你需要通过迭代器更改`QMultiHash`。const迭代器速度稍快，并且可以提高代码的可读性。
默认的`QMultiHash::iterator`构造函数会创建一个未初始化的迭代器。你必须用像`QMultiHash::begin()`、`QMultiHash::end()`或`QMultiHash::find()`这样的`QMultiHash`函数初始化它，才能开始迭代。这里有一个典型的循环，它打印了哈希中存储的所有（键、值）对：
与按键排序的 `QMap` 不同，`QMultiHash` 以任意顺序存储物品。
这里有一个例子，将`QMultiHash`中存储的每个值递增2：
要从`QMultiHash`中移除元素，可以使用 `erase_if`（`QMultiHash`<Key， T> &map， Predicate pred）：
多个迭代器可以用于同一个哈希值。但需要注意，任何直接对`QHash`进行的修改（插入和删除项）都可能导致迭代器失效。
插入项或调用方法如`QHash::reserve()`或`QHash::squeeze()`都可能导致所有指向哈希的迭代子失效。迭代子只有在`QHash`不需要增长或缩小内部哈希表时才保证有效。在重算操作完成后使用任何迭代器会导致行为未定义。
如果你需要长时间保持迭代器，我们建议你使用`QMultiMap`而非`QHash`。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。

**官方示例：**

```cpp
 QHash<QString, int> hash;
 hash.insert("January", 1);
 hash.insert("February", 2);
 //...
 hash.insert("December", 12);

 for (auto i = hash.cbegin(), end = hash.cend(); i != end; ++i)
     cout << qPrintable(i.key()) << ": " << i.value() << endl;
```

### `class key_iterator`

**作用与语义：**

QMultiHash：：key_iterator 类为 QMultiHash 键提供了一个类似 STL 风格的 const 迭代器。
`QMultiHash::key_iterator` 本质上与 `QMultiHash::const_iterator` 相同，区别在于运算符*() 和运算符->() 返回键而非值。
对于大多数用途，`QMultiHash::iterator`和`QMultiHash::const_iterator`应使用，您可以通过调用`QMultiHash::iterator::key()`轻松访问密钥：
然而，为了实现`QMultiHash`键与STL风格算法之间的互操作性，我们需要一个迭代器，它会去引用键而不是值。有了 `QMultiHash::key_iterator`，我们可以对一系列键应用算法而无需调用`QMultiHash::keys()`，但这效率较低，因为创建一个临时`QList` `QMultiHash`需要一次迭代和内存分配。
`QMultiHash::key_iterator`是const，密钥是无法修改的。
默认的`QMultiHash::key_iterator`构造器会创建一个未初始化的迭代器。你必须用像`QMultiHash::keyBegin()`或`QMultiHash::keyEnd()`这样的`QMultiHash`函数来初始化它。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。

**官方示例：**

```cpp
 for (auto it = hash.cbegin(), end = hash.cend(); it != end; ++it) {
     cout << "The key: " << it.key() << endl;
     cout << "The value: " << qPrintable(it.value()) << endl;
     cout << "Also the value: " << qPrintable(*it) << endl;
 }
```

### `const_key_value_iterator`

**作用与语义：**

QMultiHash：：const_key_value_iterator typedef 提供了一个 STL 风格的 cont 迭代器用于 `QMultiHash`。
QMultiHash：：const_key_value_iterator 本质上与 `QMultiHash::const_iterator` 相同，区别在于运算符*() 返回的是键值对而非值。

### `key_value_iterator`

**作用与语义：**

QMultiHash：：key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QMultiHash`。
QMultiHash：：key_value_iterator 本质上与 `QMultiHash::iterator` 相同，区别在于运算符*() 返回的是键值对而非值。

### `(since 6.4) auto asKeyValueRange() &&`

**作用与语义：**

返回一个范围对象，允许对该哈希值进行迭代，作为键值对。例如，该范围对象可以用于基于范围的for循环，结合结构化绑定声明：
注意，通过这种方式获得的密钥和值都是对哈希中密钥的引用。具体来说，变异值会修改哈希本身。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

**官方示例：**

```cpp
 QMultiHash<QString, int> hash;
 hash.insert("January", 1);
 hash.insert("February", 2);
 // ...
 hash.insert("December", 12);

 for (auto [key, value] : hash.asKeyValueRange()) {
     cout << qPrintable(key) << ": " << value << endl;
     --value; // convert to JS month indexing
 }
```

### `QMultiHash<Key, T>::iterator emplace(const Key &key, Args &&... args)`

**作用与语义：**

在容器中插入一个新元素。该新元素在原地构造，使用`args`作为其构造的参数。
如果哈希中已有具有相同键的项，该函数会直接创建一个新的。（这种行为不同于`replace()`，后者会覆盖已有项的值。）。
返回一个迭代子，指向新元素。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `QMultiHash<Key, T>::iterator emplaceReplace(const Key &key, Args &&... args)`

**作用与语义：**

将一个新元素插入容器。该新元素在原地构造，使用`args`作为其构造的参数。
如果哈希中已有具有相同键的项，该项的值会被由`args`构造的值替换。
返回一个迭代子，指向新元素。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `(since 6.11) QMultiHash<Key, T>::iterator insert(Key &&key, const T &value)`

**作用与语义：**

插入一个新项，带有`key`和值为`value`。
如果哈希中已有具有相同键的项，该函数会直接创建一个新的。（这种行为不同于`replace()`，后者会覆盖已有项的值。）。
返回一个迭代子，指向新元素。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `(since 6.11) QMultiHash<Key, T>::iterator insert(const Key &key, T &&value)`

**作用与语义：**

插入一个新项，带有`key`和值为`value`。
如果哈希中已有具有相同键的项，该函数会直接创建一个新的。（这种行为不同于`replace()`，后者会覆盖已有项的值。）。
返回一个迭代子，指向新元素。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `Key key(const T &value) const`

**作用与语义：**

返回映射到`value`的第一个键。如果哈希中没有映射到`value`的项，返回`defaultKey`;如果未提供该参数，则返回默认构造的键。
该函数可能较慢（线性时间），因为`QMultiHash`的内部数据结构是通过键快速查找而优化的，而不是按值。

### `T value(const Key &key) const`

**作用与语义：**

返回与`key`关联的值。
如果哈希中没有包含`key`项，函数返回`defaultValue`，或者如果未提供该参数，则返回默认构造值。
如果哈希中有多个`key`项，则返回最近插入的项值。

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

`QMultiHash` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
