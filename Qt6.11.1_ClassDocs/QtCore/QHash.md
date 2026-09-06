# QHash

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QHash` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QHash` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QHash>`
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

- `(since 6.9) struct TryEmplaceResult`
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

- `QHash()`
- `QHash(std::initializer_list<std::pair<Key, T>> list)`
- `QHash(InputIterator begin, InputIterator end)`
- `QHash(const QHash<Key, T> &other)`
- `QHash(QHash<Key, T> &&other)`
- `~QHash()`
- `(since 6.4) auto asKeyValueRange() &&`
- `(since 6.4) auto asKeyValueRange() &`
- `(since 6.4) auto asKeyValueRange() const &&`
- `(since 6.4) auto asKeyValueRange() const &`
- `QHash<Key, T>::iterator begin()`
- `QHash<Key, T>::const_iterator begin() const`
- `qsizetype capacity() const`
- `QHash<Key, T>::const_iterator cbegin() const`
- `QHash<Key, T>::const_iterator cend() const`
- `void clear()`
- `QHash<Key, T>::const_iterator constBegin() const`
- `QHash<Key, T>::const_iterator constEnd() const`
- `QHash<Key, T>::const_iterator constFind(const Key &key) const`
- `QHash<Key, T>::const_key_value_iterator constKeyValueBegin() const`
- `QHash<Key, T>::const_key_value_iterator constKeyValueEnd() const`
- `bool contains(const Key &key) const`
- `qsizetype count(const Key &key) const`
- `qsizetype count() const`
- `QHash<Key, T>::iterator emplace(Key &&key, Args &&... args)`
- `QHash<Key, T>::iterator emplace(const Key &key, Args &&... args)`
- `bool empty() const`
- `QHash<Key, T>::iterator end()`
- `QHash<Key, T>::const_iterator end() const`
- `QHash<Key, T>::iterator erase(QHash<Key, T>::const_iterator pos)`
- `QHash<Key, T>::iterator find(const Key &key)`
- `QHash<Key, T>::const_iterator find(const Key &key) const`
- `void insert(const QHash<Key, T> &other)`
- `QHash<Key, T>::iterator insert(const Key &key, const T &value)`
- `(since 6.11) QHash<Key, T>::iterator insert(Key &&key, T &&value)`
- `(since 6.11) QHash<Key, T>::iterator insert(Key &&key, const T &value)`
- `(since 6.11) QHash<Key, T>::iterator insert(const Key &key, T &&value)`
- `(since 6.9) QHash<Key, T>::TryEmplaceResult insertOrAssign(K &&key, Value &&value)`
- `(since 6.9) QHash<Key, T>::TryEmplaceResult insertOrAssign(Key &&key, Value &&value)`
- `(since 6.9) QHash<Key, T>::TryEmplaceResult insertOrAssign(const Key &key, Value &&value)`
- `(since 6.9) std::pair<QHash<Key, T>::key_value_iterator, bool> insert_or_assign(K &&key, Value &&value)`
- `(since 6.9) std::pair<QHash<Key, T>::key_value_iterator, bool> insert_or_assign(Key &&key, Value &&value)`
- `(since 6.9) std::pair<QHash<Key, T>::key_value_iterator, bool> insert_or_assign(const Key &key, Value &&value)`
- `(since 6.9) QHash<Key, T>::key_value_iterator insert_or_assign(QHash<Key, T>::const_iterator hint, K &&key, Value &&value)`
- `(since 6.9) QHash<Key, T>::key_value_iterator insert_or_assign(QHash<Key, T>::const_iterator hint, Key &&key, Value &&value)`
- `(since 6.9) QHash<Key, T>::key_value_iterator insert_or_assign(QHash<Key, T>::const_iterator hint, const Key &key, Value &&value)`
- `bool isEmpty() const`
- `Key key(const T &value) const`
- `Key key(const T &value, const Key &defaultKey) const`
- `QHash<Key, T>::key_iterator keyBegin() const`
- `QHash<Key, T>::key_iterator keyEnd() const`
- `QHash<Key, T>::key_value_iterator keyValueBegin()`
- `QHash<Key, T>::const_key_value_iterator keyValueBegin() const`
- `QHash<Key, T>::key_value_iterator keyValueEnd()`
- `QHash<Key, T>::const_key_value_iterator keyValueEnd() const`
- `QList<Key> keys() const`
- `QList<Key> keys(const T &value) const`
- `float load_factor() const`
- `bool remove(const Key &key)`
- `(since 6.1) qsizetype removeIf(Predicate pred)`
- `void reserve(qsizetype size)`
- `qsizetype size() const`
- `void squeeze()`
- `void swap(QHash<Key, T> &other)`
- `T take(const Key &key)`
- `(since 6.9) QHash<Key, T>::TryEmplaceResult tryEmplace(K &&key, Args &&... args)`
- `(since 6.9) QHash<Key, T>::TryEmplaceResult tryEmplace(Key &&key, Args &&... args)`
- `(since 6.9) QHash<Key, T>::TryEmplaceResult tryEmplace(const Key &key, Args &&... args)`
- `(since 6.9) QHash<Key, T>::TryEmplaceResult tryInsert(K &&key, const T &value)`
- `(since 6.9) QHash<Key, T>::TryEmplaceResult tryInsert(const Key &key, const T &value)`
- `(since 6.9) std::pair<QHash<Key, T>::key_value_iterator, bool> try_emplace(K &&key, Args &&... args)`
- `(since 6.9) std::pair<QHash<Key, T>::key_value_iterator, bool> try_emplace(Key &&key, Args &&... args)`
- `(since 6.9) std::pair<QHash<Key, T>::key_value_iterator, bool> try_emplace(const Key &key, Args &&... args)`
- `(since 6.9) QHash<Key, T>::key_value_iterator try_emplace(QHash<Key, T>::const_iterator hint, K &&key, Args &&... args)`
- `(since 6.9) QHash<Key, T>::key_value_iterator try_emplace(QHash<Key, T>::const_iterator hint, Key &&key, Args &&... args)`
- `(since 6.9) QHash<Key, T>::key_value_iterator try_emplace(QHash<Key, T>::const_iterator hint, const Key &key, Args &&... args)`
- `T value(const Key &key) const`
- `T value(const Key &key, const T &defaultValue) const`
- `QList<T> values() const`
- `QHash<Key, T> & operator=(QHash<Key, T> &&other)`
- `QHash<Key, T> & operator=(const QHash<Key, T> &other)`
- `T & operator[](const Key &key)`
- `const T operator[](const Key &key) const`

### 相关非成员函数

- `(since 6.1) qsizetype erase_if(QHash<Key, T> &hash, Predicate pred)`
- `(since 6.5) size_t qHash(Enum key, size_t seed = 0)`
- `size_t qHash(const QStringRef &key, size_t seed = 0)`
- `size_t qHash(const QMqttTopicFilter &filter, size_t seed = 0)`
- `size_t qHash(QSslEllipticCurve key, size_t seed = 0)`
- `size_t qHash(const QGeoCoordinate &coordinate, size_t seed = 0)`
- `(since 6.0) size_t qHash(QByteArrayView key, size_t seed = 0)`
- `size_t qHash(const QMqttTopicName &name, size_t seed = 0)`
- `size_t qHash(const QOcspResponse &key, size_t seed = 0)`
- `size_t qHash(uint key, size_t seed = 0)`
- `size_t qHash(ulong key, size_t seed = 0)`
- `size_t qHash(ushort key, size_t seed = 0)`
- `(since 6.0) size_t qHash(wchar_t key, size_t seed = 0)`
- `size_t qHash(QDate key, size_t seed = 0)`
- `size_t qHash(const QSslCertificate &key, size_t seed = 0)`
- `size_t qHash(QLatin1StringView key, size_t seed = 0)`
- `size_t qHash(const QSslError &key, size_t seed = 0)`
- `(since 6.0) size_t qHash(QPoint key, size_t seed = 0)`
- `size_t qHash(QTime key, size_t seed = 0)`
- `(since 6.9) size_t qHash(T key, size_t seed)`
- `size_t qHash(char key, size_t seed = 0)`
- `(since 6.0) size_t qHash(char16_t key, size_t seed = 0)`
- `(since 6.0) size_t qHash(char32_t key, size_t seed = 0)`
- `(since 6.0) size_t qHash(char8_t key, size_t seed = 0)`
- `size_t qHash(const QBitArray &key, size_t seed = 0)`
- `size_t qHash(const QByteArray &key, size_t seed = 0)`
- `size_t qHash(const QChar key, size_t seed = 0)`
- `size_t qHash(const QDateTime &key, size_t seed = 0)`
- `size_t qHash(const QHash<Key, T> &key, size_t seed = 0)`
- `size_t qHash(const QSet<T> &key, size_t seed = 0)`
- `size_t qHash(const QString &key, size_t seed = 0)`
- `(since 6.0) size_t qHash(const QTypeRevision &key, size_t seed = 0)`
- `size_t qHash(const QUrl &key, size_t seed = 0)`
- `size_t qHash(const QVersionNumber &key, size_t seed = 0)`
- `size_t qHash(const T *key, size_t seed = 0)`
- `size_t qHash(const std::pair<T1, T2> &key, size_t seed = 0)`
- `size_t qHash(double key, size_t seed = 0)`
- `size_t qHash(float key, size_t seed = 0)`
- `size_t qHash(int key, size_t seed = 0)`
- `size_t qHash(long key, size_t seed = 0)`
- `size_t qHash(long double key, size_t seed = 0)`
- `(since 6.8) size_t qHash(qint128 key, size_t seed = 0)`
- `size_t qHash(qint64 key, size_t seed = 0)`
- `(since 6.8) size_t qHash(quint128 key, size_t seed = 0)`
- `size_t qHash(quint64 key, size_t seed = 0)`
- `size_t qHash(short key, size_t seed = 0)`
- `size_t qHash(signed char key, size_t seed = 0)`
- `(since 6.0) size_t qHash(std::nullptr_t key, size_t seed = 0)`
- `size_t qHash(uchar key, size_t seed = 0)`
- `size_t qHashBits(const void *p, size_t len, size_t seed = 0)`
- `(since 6.0) size_t qHashMulti(size_t seed, const T &... args)`
- `(since 6.0) size_t qHashMultiCommutative(size_t seed, const T &... args)`
- `size_t qHashRange(InputIterator first, InputIterator last, size_t seed = 0)`
- `size_t qHashRangeCommutative(InputIterator first, InputIterator last, size_t seed = 0)`
- `bool operator!=(const QHash<Key, T> &lhs, const QHash<Key, T> &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QHash<Key, T> &hash)`
- `bool operator==(const QHash<Key, T> &lhs, const QHash<Key, T> &rhs)`
- `QDataStream & operator>>(QDataStream &in, QHash<Key, T> &hash)`

### 公开宏

- `(since 6.11) QT_NO_SINGLE_ARGUMENT_QHASH_OVERLOAD`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QHash::ConstIterator`

**作用与语义：**

Qt风格的同义词，代表`QHash::const_iterator`。

### `QHash::Iterator`

**作用与语义：**

Qt风格的`QHash::iterator`同义词。

### `QHash::const_key_value_iterator`

**作用与语义：**

QHash::const_key_value_iterator typedef 为 `QHash` 提供了 STL 风格的常量迭代器。QHash::const_key_value_iterator 本质上与 `QHash::const_iterator` 相同，不同之处在于 operator*() 返回的是键/值对而不是值。

### `[alias] QHash::difference_type`

**作用与语义：**

Typedef 用于ptrdiff_t。提供 STL 兼容性。

### `[alias] QHash::key_type`

**作用与语义：**

Typedef 用于键。提供 STL 兼容性。

### `QHash::key_value_iterator`

**作用与语义：**

QHash：：key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QHash`。
QHash：：key_value_iterator 本质上与 `QHash::iterator` 相同，区别在于运算符*() 返回的是键值对而非值。

### `[alias] QHash::mapped_type`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `[alias] QHash::size_type`

**作用与语义：**

类型定义用于国际语言。提供支持STL兼容性。

### `[noexcept] QHash::QHash()`

**作用与语义：**

构造一个空哈希。

### `QHash::QHash(std::initializer_list<std::pair<Key, T>> list)`

**作用与语义：**

构造一个包含初始化器列表中每个元素的哈希`list`。

### `template <typename InputIterator> QHash::QHash(InputIterator begin, InputIterator end)`

**作用与语义：**

构造一个哈希，包含迭代子范围内每个元素的副本 [`begin`， `end`）。被迭代的元素必须是具有`first`和`second`数据成员的对象（如 `std::pair`），分别可转换为`Key`和可转换为`T`;或者迭代器必须有`key()`和 `value()`成员函数，分别返回键可转换为 `Key` 和返回可转换值`T`。

### `[noexcept] QHash::QHash(const QHash<Key, T> &other)`

**作用与语义：**

构建了一份`other`的复制品。
该操作发生在常数时间内，因为QHash是隐式共享的。这使得从函数返回QHash的速度非常快。如果共享实例被修改，它将被复制（写时复制），这需要线性时间。

### `[noexcept] QHash::QHash(QHash<Key, T> &&other)`

**作用与语义：**

Move-构造一个QHash实例，使其指向`other`指向的同一个对象。

### `QHash::~QHash()`

**作用与语义：**

销毁哈希值。对哈希值和所有迭代子的引用均无效。

### `[since 6.4] auto QHash::asKeyValueRange() const &&`

**作用与语义：**

返回一个范围对象，允许对该哈希值进行迭代，作为键值对。例如，该范围对象可以用于基于范围的for循环，结合结构化绑定声明：
注意，通过这种方式获得的密钥和值都是对哈希中密钥的引用。具体来说，变异值会修改哈希本身。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

**官方示例：**

```cpp
 QHash<QString, int> hash;
 hash.insert("January", 1);
 hash.insert("February", 2);
 // ...
 hash.insert("December", 12);

 for (auto [key, value] : hash.asKeyValueRange()) {
     cout << qPrintable(key) << ": " << value << endl;
     --value; // convert to JS month indexing
 }
```

### `QHash<Key, T>::iterator QHash::begin()`

**作用与语义：**

返回一个指向哈希中第一个项的STL式迭代器。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QHash<Key, T>::const_iterator QHash::begin() const`

**作用与语义：**

警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] qsizetype QHash::capacity() const`

**作用与语义：**

返回`QHash`内部哈希表中的桶数。
该函数的唯一目的是提供一种微调`QHash`内存使用的方法。一般来说，你很少需要调用这个函数。如果你想知道哈希中有多少项，可以调用`size()`。

### `[noexcept] QHash<Key, T>::const_iterator QHash::cbegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向哈希中的第一个项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QHash<Key, T>::const_iterator QHash::cend() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向哈希中最后一个项之后的虚数项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept(...)] void QHash::clear()`

**作用与语义：**

移除哈希中的所有项目，释放所有内存。
注意：该功能仅在`std::is_nothrow_destructible<Node>::value` `true`时才适用。

### `[noexcept] QHash<Key, T>::const_iterator QHash::constBegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向哈希中的第一个项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QHash<Key, T>::const_iterator QHash::constEnd() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向哈希中最后一个项之后的虚数项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QHash<Key, T>::const_iterator QHash::constFind(const Key &key) const`

**作用与语义：**

返回一个迭代器，指向哈希中`key`的项目。
如果哈希中没有`key`项，函数返回`constEnd()`。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QHash<Key, T>::const_key_value_iterator QHash::constKeyValueBegin() const`

**作用与语义：**

返回一个const型STL风格的迭代器，指向哈希中的第一个条目。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QHash<Key, T>::const_key_value_iterator QHash::constKeyValueEnd() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向哈希最后一个条目之后的虚数条目。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] bool QHash::contains(const Key &key) const`

**作用与语义：**

如果哈希包含带有`key`的项，返回 `true`;否则返回 `false`。

### `[noexcept] qsizetype QHash::count(const Key &key) const`

**作用与语义：**

返回与`key`关联的项目数量。

### `[noexcept] qsizetype QHash::count() const`

**作用与语义：**

和`size()`一样。

### `template <typename... Args> QHash<Key, T>::iterator QHash::emplace(Key &&key, Args &&... args)`

**作用与语义：**

在容器中插入一个新元素。该新元素在原地构造，使用 `args` 作为其构造的参数。
返回一个迭代子，指向新元素。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] bool QHash::empty() const`

**作用与语义：**

该函数是为了STL兼容性而提供。它等价于`isEmpty()`，如果哈希为空，返回为真;否则返回`false`。

### `[noexcept] QHash<Key, T>::iterator QHash::end()`

**作用与语义：**

返回一个STL风格的迭代器，指向哈希中最后一个项之后的虚数项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QHash<Key, T>::const_iterator QHash::end() const`

**作用与语义：**

警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `QHash<Key, T>::iterator QHash::erase(QHash<Key, T>::const_iterator pos)`

**作用与语义：**

从哈希中移除与迭代器`pos`关联的（键、值）对，并返回哈希中下一项的迭代器。
该函数从不导致`QHash`重排其内部数据结构。这意味着在迭代过程中可以安全地调用它，不会影响哈希中项的顺序。例如：
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

**官方示例：**

```cpp
 QHash<QObject *, int> objectHash;
 //...
 QHash<QObject *, int>::iterator i = objectHash.find(obj);
 while (i != objectHash.end() && i.key() == obj) {
     if (i.value() == 0) {
         i = objectHash.erase(i);
     } else {
         ++i;
     }
 }
```

### `QHash<Key, T>::iterator QHash::find(const Key &key)`

**作用与语义：**

返回一个迭代器，指向哈希中`key`的项目。
如果哈希中没有`key`项，函数返回`end()`。
如果哈希包含多个带有`key`的项，该函数返回一个迭代器，指向最近插入的值。其他值可以通过递增迭代器访问。例如，这里有一段代码对所有具有相同键的项进行迭代：
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

**官方示例：**

```cpp
 QHash<QString, int> hash;
 //...
 QHash<QString, int>::const_iterator i = hash.find("HDR");
 while (i != hash.end() && i.key() == "HDR") {
     cout << i.value() << endl;
     ++i;
 }
```

### `[noexcept] QHash<Key, T>::const_iterator QHash::find(const Key &key) const`

**作用与语义：**

警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `void QHash::insert(const QHash<Key, T> &other)`

**作用与语义：**

将`other`哈希中的所有项插入到该哈希中。
如果某个键在两个哈希中都存在，则其值将被存储在`other`中的值替换。

### `QHash<Key, T>::iterator QHash::insert(const Key &key, const T &value)`

**作用与语义：**

插入一个新项，`key`值为`value`。
如果已有`key`的物品，该物品的价值将被替换为`value`。
返回一个迭代器，指向新元素/更新元素。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[since 6.11] QHash<Key, T>::iterator QHash::insert(Key &&key, T &&value)`

**作用与语义：**

将`other`哈希中的所有项插入到该哈希中。
如果某个键在两个哈希中都存在，则其值将被存储在`other`中的值替换。

### `[since 6.9] template < typename K, typename Value, QHash<Key, T>::if_heterogeneously_searchable<K> = true, QHash<Key, T>::if_key_constructible_from<K> = true > QHash<Key, T>::TryEmplaceResult QHash::insertOrAssign(K &&key, Value &&value)`

**作用与语义：**

尝试插入带有 `key` 和 `value` 的项。如果已有 `key` 的项，其值会被覆盖为 `value`。
返回一个包含该项的`iterator`结构`TryEmplaceResult`实例，以及一个布尔值`inserted`，表示该项是新创建（`true`）还是之前存在（`false`）。

### `[since 6.9] template < typename K, typename Value, QHash<Key, T>::if_heterogeneously_searchable<K> = true, QHash<Key, T>::if_key_constructible_from<K> = true > std::pair<QHash<Key, T>::key_value_iterator, bool> QHash::insert_or_assign(K &&key, Value &&value)`

**作用与语义：**

尝试插入带有 `key` 和 `value` 的项。如果已有 具有 `key` 的项，其值会被覆盖为 `value`。
返回一对，由指向该项的迭代器和一个布尔值组成，表示该项是新创建（`true`）还是之前存在（`false`）。
这些功能是为了与标准库的兼容性而提供。

### `[since 6.9] template < typename K, typename Value, QHash<Key, T>::if_heterogeneously_searchable<K> = true, QHash<Key, T>::if_key_constructible_from<K> = true > QHash<Key, T>::key_value_iterator QHash::insert_or_assign(QHash<Key, T>::const_iterator hint, K &&key, Value &&value)`

**作用与语义：**

尝试插入带有 `key` 和 `value` 的项。如果已有 具有 `key` 的项，其值会被覆盖为 `value`。
返回一对，由指向该项的迭代器和一个布尔值组成，表示该项是新创建（`true`）还是之前存在（`false`）。
这些功能是为了与标准库的兼容性而提供。

### `[noexcept] bool QHash::isEmpty() const`

**作用与语义：**

如果哈希中没有任何项，则返回`true`;否则返回 false。

### `[noexcept] Key QHash::key(const T &value, const Key &defaultKey) const`

**作用与语义：**

返回映射到`value`的第一个键。如果哈希中没有映射到`value`的项，返回`defaultKey`;如果未提供该参数，则返回默认构造的键。
该函数可能较慢（线性时间），因为`QHash`的内部数据结构是通过键快速查找而优化的，而非按值。

### `[noexcept] QHash<Key, T>::key_iterator QHash::keyBegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向哈希中的第一个键。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QHash<Key, T>::key_iterator QHash::keyEnd() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向哈希中最后一个键之后的虚数项。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `QHash<Key, T>::key_value_iterator QHash::keyValueBegin()`

**作用与语义：**

返回一个指向哈希第一个条目的STL式迭代器。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QHash<Key, T>::const_key_value_iterator QHash::keyValueBegin() const`

**作用与语义：**

返回一个const型STL风格的迭代器，指向哈希中的第一个条目。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `QHash<Key, T>::key_value_iterator QHash::keyValueEnd()`

**作用与语义：**

返回一个STL风格的迭代子，指向哈希中最后一个条目之后的虚数条目。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] QHash<Key, T>::const_key_value_iterator QHash::keyValueEnd() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向哈希最后一个条目之后的虚数条目。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `QList<Key> QHash::keys() const`

**作用与语义：**

返回包含哈希中所有键的列表，顺序任意。
顺序保证与`values()`使用相同。
该函数会以线性时间创建一个新的列表。通过从`keyBegin()`迭代到`keyEnd()`可以避免所需的时间和内存消耗。

### `QList<Key> QHash::keys(const T &value) const`

**作用与语义：**

返回包含所有与值`value`相关的键的列表，顺序任意。
该函数可能较慢（线性时间），因为`QHash`的内部数据结构是通过键而非值快速查找而优化的。

### `[noexcept] float QHash::load_factor() const`

**作用与语义：**

返回`QHash`内部哈希表的当前负载因子。这与`capacity()`/`size()`相同。所采用的实现目标是将负载因子保持在0.25到0.5之间。这样可以避免过多的哈希表碰撞，从而降低性能。
即使负载因子较低，哈希表的实现内存开销也非常低。
这种方法纯粹用于诊断，你很少需要自己打电话。

### `bool QHash::remove(const Key &key)`

**作用与语义：**

从哈希中移除包含该`key`的项。如果密钥存在且该项已被移除，则返回真，否则返回false。

### `[since 6.1] template <typename Predicate> qsizetype QHash::removeIf(Predicate pred)`

**作用与语义：**

从哈希中移除所有谓词返回为真的元素`pred`。
该函数支持参数类型为`QHash<Key, T>::iterator`或类型为`std::pair<const Key &, T &>`的参数。
返回被移除的元素数量（如果有的话）。

### `void QHash::reserve(qsizetype size)`

**作用与语义：**

确保`QHash`内部哈希表有空间存储至少`size`项，而无需扩展哈希表。
这意味着哈希表至少包含2个* `size`桶，以确保良好的性能。
该函数适用于需要构建大哈希并希望避免重复重分配的代码。例如：
理想情况下，`size`应是哈希中预期的最大项数。`QHash`会选择最小的桶数，允许在不扩大内部哈希表的情况下存储`size`项。如果`size`低估，最坏的情况也不过是`QHash`会稍微变慢。
一般来说，你很少需要调用这个函数。`QHash` 的内部哈希表会自动增长，以提供良好的性能，同时不浪费太多内存。

**官方示例：**

```cpp
 QHash<QString, int> hash;
 hash.reserve(20000);
 for (int i = 0; i < 20000; ++i)
     hash.insert(keys[i], values[i]);
```

### `[noexcept] qsizetype QHash::size() const`

**作用与语义：**

返回哈希中的项目数量。

### `void QHash::squeeze()`

**作用与语义：**

减少`QHash`内部哈希表的大小以节省内存。
该函数的唯一目的是提供一种微调`QHash`内存使用的方法。一般来说，你很少需要调用这个函数。

### `[noexcept] void QHash::swap(QHash<Key, T> &other)`

**作用与语义：**

将该哈希值与`other`交换。该操作非常快且从未失败。

### `T QHash::take(const Key &key)`

**作用与语义：**

从哈希中移除带有`key`的项目，返回与之相关的值。
如果该项不存在于哈希中，函数仅返回一个默认构造的值。
如果不使用返回值，`remove()`效率更高。

### `[since 6.9] template < typename K, typename... Args, QHash<Key, T>::if_heterogeneously_searchable<K> = true, QHash<Key, T>::if_key_constructible_from<K> = true > QHash<Key, T>::TryEmplaceResult QHash::tryEmplace(K &&key, Args &&... args)`

**作用与语义：**

插入一个带有`key`和由`args`构造的值的新项。如果已有`key`的项存在，则不进行插入。
返回一个`TryEmplaceResult`实例，一个包含新创建项目或阻止插入的既有项目的`iterator`结构，以及一个布尔值的 `inserted`，表示插入是否发生。
例如，这可以用来避免比较新旧大小或重复查找的模式。你之前可能写过类似这样的代码：
你可以写：

**官方示例：**

```cpp
 QHash<int, MyType> hash;
 // [...]
 int myKey = getKey();
 qsizetype oldSize = hash.size();
 MyType &elem = hash[myKey];
 if (oldSize != hash.size()) // Size changed: new element!
     initialize(elem);
 // [use elem...]
```

### `[since 6.9] template < typename K, QHash<Key, T>::if_heterogeneously_searchable<K> = true, QHash<Key, T>::if_key_constructible_from<K> = true > QHash<Key, T>::TryEmplaceResult QHash::tryInsert(K &&key, const T &value)`

**作用与语义：**

插入一个`key`和值为`value`的新项。如果已有`key`的项存在，则不进行插入。
返回一个 T实例 `TryEmplaceResult`，一个包含新创建项目或阻止插入的既有项目`iterator`的结构，以及一个布尔值 `inserted`，表示插入是否发生。

### `[since 6.9] template < typename K, typename... Args, QHash<Key, T>::if_heterogeneously_searchable<K> = true, QHash<Key, T>::if_key_constructible_from<K> = true > std::pair<QHash<Key, T>::key_value_iterator, bool> QHash::try_emplace(K &&key, Args &&... args)`

**作用与语义：**

插入一个带有`key`和由`args`构造值的新项。如果已有`key`项，则不进行插入。
返回一对由迭代器（迭代器）到插入的项目（或阻止插入的项目）和一个布ol组成，表示插入是否发生。
这些功能是为了与标准库的兼容性而提供。

### `[since 6.9] template <typename... Args> QHash<Key, T>::key_value_iterator QHash::try_emplace(QHash<Key, T>::const_iterator hint, Key &&key, Args &&... args)`

**作用与语义：**

插入一个带有`key`和由`args`构造值的新项。如果已有`key`项，则不进行插入。
返回一对由迭代器（迭代器）到插入的项目（或阻止插入的项目）和一个布ol组成，表示插入是否发生。
这些功能是为了与标准库的兼容性而提供。

### `[noexcept] T QHash::value(const Key &key, const T &defaultValue) const`

**作用与语义：**

返回与`key`关联的值。
如果哈希中没有包含`key`项，函数返回`defaultValue`;如果未提供该参数，则返回默认构造值。

### `QList<T> QHash::values() const`

**作用与语义：**

返回包含哈希中所有值的列表，顺序任意。
顺序保证与`keys()`使用的顺序相同。
该函数会在线性时间内创建一个新的列表。通过从`keyValueBegin()`迭代到`keyValueEnd()`，可以避免所需的时间和内存消耗。

### `[noexcept] QHash<Key, T> &QHash::operator=(QHash<Key, T> &&other)`

**作用与语义：**

移动分配`other`到该`QHash`实例。

### `[noexcept(...)] QHash<Key, T> &QHash::operator=(const QHash<Key, T> &other)`

**作用与语义：**

将`other`赋值到该哈希值，并返回对该哈希的引用。
注意：该函数仅在`std::is_nothrow_destructible<Node>::value` `true`时才适用。

### `T &QHash::operator[](const Key &key)`

**作用与语义：**

返回与`key`关联的值作为可修改的引用。
如果哈希中没有包含`key`项，函数会在哈希中插入`key`一个默认构造的值，并返回该值的引用。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `[noexcept] const T QHash::operator[](const Key &key) const`

**作用与语义：**

和`value()`一样。

### `[since 6.1] template < typename Key, typename T, typename Predicate > qsizetype erase_if(QHash<Key, T> &hash, Predicate pred)`

**作用与语义：**

从哈希`hash`中移除所有谓词返回为真`pred`的元素。
该函数支持参数类型为`QHash<Key, T>::iterator`或类型为`std::pair<const Key &, T &>`的参数。
返回被移除的元素数量（如果有的话）。

### `[constexpr noexcept, since 6.5] template <typename Enum, std::enable_if_t<std::is_enum_v<Enum>, bool> = true> size_t qHash(Enum key, size_t seed = 0)`

**作用与语义：**

返回 `key` 的哈希值，使用 `seed` 来做种计算。
注意：在 Qt 6.5 之前，无作用域枚举依赖该函数的整数重载，因为隐式转换为其底层整数类型。对于有作用域枚举，你必须自己实现重载。这仍然是向下兼容的修复方法，以保持与较旧的 Qt 版本兼容。

### `[noexcept, since 6.0] size_t qHash(QByteArrayView key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept] size_t qHash(uint key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept] size_t qHash(ulong key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept] size_t qHash(ushort key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept, since 6.0] size_t qHash(wchar_t key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] size_t qHash(QDate key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] size_t qHash(QLatin1StringView key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept, since 6.0] size_t qHash(QPoint key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] size_t qHash(QTime key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept, since 6.9] template <typename T, std::enable_if_t<std::is_same_v<T, bool>, bool>> size_t qHash(T key, size_t seed)`

**作用与语义：**

返回 `key` 的哈希值，使用 `seed` 来做种计算。
注意：这是qHash（bool），仅接受类型为bool的参数，不接受仅转换为bool的类型参数。
注意：在 6.9 之前的 Qt 版本中，这种重载是由一个未公开的 1-to-arg qHash 适配器模板函数无意中产生的，且行为完全相同。

### `[constexpr noexcept] size_t qHash(char key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept, since 6.0] size_t qHash(char16_t key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept, since 6.0] size_t qHash(char32_t key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept, since 6.0] size_t qHash(char8_t key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] size_t qHash(const QBitArray &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] size_t qHash(const QByteArray &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept] size_t qHash(const QChar key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `size_t qHash(const QDateTime &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept(...)] template <typename Key, typename T> size_t qHash(const QHash<Key, T> &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，并用`seed`来做种子计算。
qHash()必须支持 类型 `Key` 和 `T`。
注意：该功能仅在`noexcept(qHash(std::declval<Key&>())) && noexcept(qHash(std::declval<T&>()))` `true`时使用。

### `[noexcept(...)] template <typename T> size_t qHash(const QSet<T> &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种子计算。
类型`T`必须由qHash()支持。
哈希值与`key`中元素的顺序无关，即包含相同元素的集合，哈希值为相同值。
注意：该函数只有在`noexcept(qHashRangeCommutative(key.begin(), key.end(), seed))` `true`时才会生效。

### `[noexcept] size_t qHash(const QString &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[since 6.0] size_t qHash(const QTypeRevision &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] size_t qHash(const QUrl &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `size_t qHash(const QVersionNumber &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] template <typename T> size_t qHash(const T *key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept(...)] template <typename T1, typename T2> size_t qHash(const std::pair<T1, T2> &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种子计算。
qHash()必须支持类型`T1`和`T2`类型。
注意：该函数仅在`QHashPrivate::noexceptPairHash<T1, T2>()`为`true`时使用。

### `[noexcept] size_t qHash(double key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] size_t qHash(float key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept] size_t qHash(int key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept] size_t qHash(long key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] size_t qHash(long double key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept, since 6.8] size_t qHash(qint128 key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种计算。
注意：该功能仅支持原生128位整数类型的平台。

### `[constexpr noexcept] size_t qHash(qint64 key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept, since 6.8] size_t qHash(quint128 key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种计算。
注意：该功能仅支持原生128位整数类型的平台。

### `[constexpr noexcept] size_t qHash(quint64 key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept] size_t qHash(short key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept] size_t qHash(signed char key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept, since 6.0] size_t qHash(std::nullptr_t key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept] size_t qHash(uchar key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] size_t qHashBits(const void *p, size_t len, size_t seed = 0)`

**作用与语义：**

返回`p`指向的大小为`len`的内存块的哈希值，并使用`seed`来做种计算。
只需用这个函数来实现你自己的自定义类型`qHash()`。例如，以下是你如何实现 std：：vector 的 `qHash()` overload<int>：
这利用了 std：：vector 连续布局数据的特性。如果不是这样，或者包含类型有填充，你应该用 `qHashRange()`。
值得重申的是，qHashBits() 的实现——就像 Qt 提供的`qHash()`超载一样——随时可能发生变化。你不能依赖于 qHashBits() 在不同 Qt 版本下（对相同输入）会给出相同结果。

**官方示例：**

```cpp
 inline size_t qHash(const std::vector<int> &key, size_t seed = 0)
 {
     if (key.empty())
         return seed;
     else
         return qHashBits(&key.front(), key.size() * sizeof(int), seed);
 }
```

### `[constexpr noexcept(...), since 6.0] template <typename... T> size_t qHashMulti(size_t seed, const T &... args)`

**作用与语义：**

通过对每个元素应用`qHash()`并将哈希值合并为一个，返回`args`的哈希值，使用`seed`来做种。
注意参数的顺序很重要。如果顺序不重要，请使用`qHashMultiCommutative()`。如果你是对原始内存进行哈希，使用`qHashBits()`;如果是对某个区间进行哈希，使用`qHashRange()`。
这个函数是为了方便你为自定义类型实现`qHash()`。例如，以下是你如何为类 `Employee`实现`qHash()`重载的方法：
注意：该功能只有在`std::conjunction_v<QtPrivate::QNothrowHashable<T>...>` `true`时才使用。

**官方示例：**

```cpp
 #ifndef EMPLOYEE_H
 #define EMPLOYEE_H

 class Employee
 {
 public:
     Employee() {}
     Employee(const QString &name, QDate dateOfBirth);
     QString name() const { return myName; }
     QDate dateOfBirth() const { return myDateOfBirth; }
     //...

 private:
     QString myName;
     QDate myDateOfBirth;
 };

 inline bool operator==(const Employee &e1, const Employee &e2)
 {
     return e1.name() == e2.name()
            && e1.dateOfBirth() == e2.dateOfBirth();
 }

 inline size_t qHash(const Employee &key, size_t seed)
 {
     return qHashMulti(seed, key.name(), key.dateOfBirth());
 }

 #endif // EMPLOYEE_H
```

### `[constexpr noexcept(...), since 6.0] template <typename... T> size_t qHashMultiCommutative(size_t seed, const T &... args)`

**作用与语义：**

通过对每个元素应用`qHash()`并将哈希值合并为一个，返回`args`的哈希值，使用`seed`来做种。
参数的顺序无关紧要。如果顺序重要，建议使用`qHashMulti()`，因为这样可能产生更好的哈希质量。如果你在哈希原始内存，使用`qHashBits()`;如果对某个区间进行哈希，使用`qHashRange()`。
这个功能是为了方便你为自定义类型实现`qHash()`。
注意：该函数仅在`std::conjunction_v<QtPrivate::QNothrowHashable<T>...>` `true`时才适用。

### `[noexcept(...)] template <typename InputIterator> size_t qHashRange(InputIterator first, InputIterator last, size_t seed = 0)`

**作用与语义：**

返回区间[`first`，`last`的哈希值，使用`seed`对每个元素`qHash()`施加种子，并将哈希值合并为单一。
该函数的返回值取决于该区间元素的顺序。这意味着。
以及。
哈希值变为不同值。如果顺序不重要，比如哈希表，可以用`qHashRangeCommutative()`。如果你是对原始内存进行哈希，则使用`qHashBits()`。
只用这个函数来实现你自己的自定义类型`qHash()`。例如，以下是你如何实现 std：：vector 的 `qHash()` overload<int>：
值得重申的是，qHashRange() 的实现——就像 Qt 提供的`qHash()`超载一样——随时可能发生变化。你不能依赖于 qHashRange() 在不同 Qt 版本中会给出相同结果（针对相同输入），即使元素类型的`qHash()`会。
注意：该功能仅在`noexcept(qHash(*first, 0))`为`true`时使用。

**官方示例：**

```cpp
 {0, 1, 2}
```

### `[noexcept(...)] template <typename InputIterator> size_t qHashRangeCommutative(InputIterator first, InputIterator last, size_t seed = 0)`

**作用与语义：**

通过对每个元素应用`qHash()`，并将哈希值合并为单一，返回区间[`first`，`last`的哈希值，`seed`进行种子化计算。
该函数的返回值不依赖于该值域中元素的顺序。这意味着。
以及。
哈希值也相同。如果顺序很重要，比如向量和数组，可以用`qHashRange()`。如果你是对原始内存进行哈希，可以用`qHashBits()`。
这个函数只用来实现你自己的自定义类型`qHash()`。例如，这里可以为 std 实现一个`qHash()`重载 ：：unordered_set<int>：
值得一再强调的是，qHashRangeCommutative() 的实现——就像 Qt 提供的`qHash()`超载一样——随时可能发生变化。你不能依赖于 qHashRangeCommutative() 在不同 Qt 版本下会给出相同结果（针对相同输入），即使元素类型的`qHash()`会。
注意：该功能只有在`noexcept(qHash(*first, 0))` 被`true`时才会使用。

**官方示例：**

```cpp
 {0, 1, 2}
```

### `[noexcept] bool operator!=(const QHash<Key, T> &lhs, const QHash<Key, T> &rhs)`

**作用与语义：**

返回`true`如果`lhs`哈希不等于`rhs`哈希；否则返回`false`如果两个哈希包含相同的（键，值）对，则认为它们相等。此函数要求值类型实现`operator==()`.

### `template <typename Key, typename T> QDataStream &operator<<(QDataStream &out, const QHash<Key, T> &hash)`

**作用与语义：**

写入哈希`hash`流`out`。
该函数需要键型和值类型来实现`operator<<()`。

### `[noexcept] bool operator==(const QHash<Key, T> &lhs, const QHash<Key, T> &rhs)`

**作用与语义：**

如果 `lhs` 的哈希值等于 `rhs` 的哈希值，则返回 `true`；否则返回 `false`。两个哈希值被认为相等，如果它们包含相同的（键，值）对。此函数要求值类型实现 `operator==()`。

### `template <typename Key, typename T> QDataStream &operator>>(QDataStream &in, QHash<Key, T> &hash)`

**作用与语义：**

将流`in`的哈希值读取到`hash`。
该函数需要键型和值类型来实现`operator>>()`。

### `[since 6.11] QT_NO_SINGLE_ARGUMENT_QHASH_OVERLOAD`

**作用与语义：**

定义该宏会禁用只接受一个参数的`qHash`超载;换句话说，就是不支持不接受种子的`qHash`超载。对`qHash`单参数超载的支持已不再支持，将在Qt 7中移除。
该宏是在Qt 6.11中引入的。

### `(since 6.9) struct TryEmplaceResult`

**作用与语义：**

TryEmplaceResult 类用于表示 tryEmplace() 操作的结果。
`TryEmplaceResult`类在`QHash`中用于表示`tryEmplace()`操作的结果。它包含新创建项或阻止插入的既有项的 `iterator`，以及一个布尔值 `inserted`，表示插入是否发生。

### `class const_iterator`

**作用与语义：**

QHash::const_iterator 类为 QHash 提供了 STL 风格的常量迭代器。`QHash`<Key, T>::const_iterator 允许你遍历 `QHash`。如果你希望在遍历过程中修改 `QHash`，你必须使用 `QHash::iterator`。通常情况下，在非 const `QHash` 上使用 `QHash::const_iterator` 是个好习惯，除非你需要通过迭代器更改 `QHash`。常量迭代器稍微快一些，并且可以提高代码可读性。默认的 `QHash::const_iterator` 构造函数创建一个未初始化的迭代器。你必须使用像 `QHash::cbegin()`、`QHash::cend()` 或 `QHash::constFind()` 这样的 `QHash` 函数来初始化它，才能开始迭代。下面是一个典型的循环，用于打印存储在哈希中的所有 (key, value) 对：与按键排序其项的 `QMap` 不同，`QHash` 以任意顺序存储其项。唯一保证的是共享相同键的项（因为它们是使用 `QMultiHash` 插入的）将连续出现，从最近插入的值到最早插入的值。可以在同一个哈希上使用多个迭代器。然而，要注意直接对 `QHash` 进行的任何修改（插入或删除项）可能导致迭代器失效。向哈希中插入项或调用如 `QHash::reserve()` 或 `QHash::squeeze()` 之类的方法可能会使指向该哈希的所有迭代器失效。迭代器只在 `QHash` 不需要扩展/缩小其内部哈希表时保证有效。在重新哈希操作发生后继续使用任何迭代器将导致未定义行为。然而，你可以安全地使用迭代器通过 `QHash::erase()` 方法从哈希中移除条目。该函数可以在迭代时安全调用，并且不会影响哈希中项目的顺序。警告：隐式共享容器上的迭代器工作方式与 STL 迭代器不完全相同。你应该避免在容器上迭代器处于活动状态时复制容器。更多信息，请阅读《隐式共享迭代器问题》。

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

QHash：：iterator 类为 QHash 提供了一个类似 STL 的非const迭代器。
`QHash`<密钥，T，T>：：迭代器允许你对某个`QHash`进行迭代，并修改与某个密钥相关的值（但不能修改密钥）。如果你想对const的某个`QHash`进行迭代，应该使用`QHash::const_iterator`。通常在非const的代`QHash`上也使用`QHash::const_iterator`是个好习惯，除非你需要通过迭代器更改`QHash`。const迭代器速度稍快，并且可以提高代码的可读性。
默认的`QHash::iterator`构造函数会创建一个未初始化的迭代器。你必须用像`QHash::begin()`、`QHash::end()`或`QHash::find()`这样的`QHash`函数初始化它，才能开始迭代。这里有一个典型的循环，它打印了哈希中存储的所有（键、值）对：
与按键排序的 `QMap` 不同，`QHash` 以任意顺序存储物品。
这里有一个例子，将`QHash`中存储的每个值递增2：
要从`QHash`中移除元素，可以使用 `erase_if`（`QHash`<Key， T> &map， Predicate pred）：
多个迭代器可以用于同一个哈希值。但需要注意，任何直接对`QHash`进行的修改（插入和删除项）都可能导致迭代器失效。
插入项或调用方法如`QHash::reserve()`或`QHash::squeeze()`都可能导致所有指向哈希的迭代子失效。迭代子只有在`QHash`不需要增长或缩小内部哈希表时才保证有效。在重算操作完成后使用任何迭代器会导致行为未定义。
如果你需要长时间保持迭代器，我们建议你使用`QMap`而非`QHash`。
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

QHash：：key_iterator 类为 QHash 键提供了一个 STL 风格的 const 迭代器。
`QHash::key_iterator` 本质上与 `QHash::const_iterator` 相同，区别在于运算符*() 和运算符->() 返回键而非值。
对于大多数用途，`QHash::iterator`和`QHash::const_iterator`应使用，您可以通过调用`QHash::iterator::key()`轻松访问密钥：
然而，为了实现`QHash`键与STL风格算法之间的互操作性，我们需要一个迭代器，它会去引用键而不是值。有了 `QHash::key_iterator`，我们可以对一系列键应用算法而无需调用`QHash::keys()`，但这效率较低，因为创建一个临时`QList` `QHash`需要一次迭代和内存分配。
`QHash::key_iterator`是const，密钥是无法修改的。
默认的`QHash::key_iterator`构造器会创建一个未初始化的迭代器。你必须用像`QHash::keyBegin()`或`QHash::keyEnd()`这样的`QHash`函数来初始化它。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。

**官方示例：**

```cpp
 for (auto it = hash.cbegin(), end = hash.cend(); it != end; ++it) {
     cout << "The key: " << it.key() << endl;
     cout << "The value: " << qPrintable(it.value()) << endl;
     cout << "Also the value: " << qPrintable(*it) << endl;
 }
```

### `ConstIterator`

**作用与语义：**

Qt风格的同义词，代表`QHash::const_iterator`。

### `Iterator`

**作用与语义：**

Qt风格的`QHash::iterator`同义词。

### `const_key_value_iterator`

**作用与语义：**

QHash::const_key_value_iterator typedef 为 `QHash` 提供了 STL 风格的常量迭代器。QHash::const_key_value_iterator 本质上与 `QHash::const_iterator` 相同，不同之处在于 operator*() 返回的是键/值对而不是值。

### `difference_type`

**作用与语义：**

Typedef 用于ptrdiff_t。提供 STL 兼容性。

### `key_type`

**作用与语义：**

Typedef 用于键。提供 STL 兼容性。

### `key_value_iterator`

**作用与语义：**

QHash：：key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QHash`。
QHash：：key_value_iterator 本质上与 `QHash::iterator` 相同，区别在于运算符*() 返回的是键值对而非值。

### `mapped_type`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `size_type`

**作用与语义：**

类型定义用于国际语言。提供支持STL兼容性。

### `(since 6.4) auto asKeyValueRange() &&`

**作用与语义：**

返回一个范围对象，允许对该哈希值进行迭代，作为键值对。例如，该范围对象可以用于基于范围的for循环，结合结构化绑定声明：
注意，通过这种方式获得的密钥和值都是对哈希中密钥的引用。具体来说，变异值会修改哈希本身。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

**官方示例：**

```cpp
 QHash<QString, int> hash;
 hash.insert("January", 1);
 hash.insert("February", 2);
 // ...
 hash.insert("December", 12);

 for (auto [key, value] : hash.asKeyValueRange()) {
     cout << qPrintable(key) << ": " << value << endl;
     --value; // convert to JS month indexing
 }
```

### `QHash<Key, T>::iterator emplace(const Key &key, Args &&... args)`

**作用与语义：**

在容器中插入一个新元素。该新元素在原地构造，使用 `args` 作为其构造的参数。
返回一个迭代子，指向新元素。
警告：下次调用哈希的非const函数或哈希被销毁时，返回的迭代子/引用应被视为无效。

### `(since 6.11) QHash<Key, T>::iterator insert(Key &&key, const T &value)`

**作用与语义：**

将`other`哈希中的所有项插入到该哈希中。
如果某个键在两个哈希中都存在，则其值将被存储在`other`中的值替换。

### `(since 6.11) QHash<Key, T>::iterator insert(const Key &key, T &&value)`

**作用与语义：**

将`other`哈希中的所有项插入到该哈希中。
如果某个键在两个哈希中都存在，则其值将被存储在`other`中的值替换。

### `(since 6.9) QHash<Key, T>::TryEmplaceResult insertOrAssign(Key &&key, Value &&value)`

**作用与语义：**

尝试插入带有 `key` 和 `value` 的项。如果已有 `key` 的项，其值会被覆盖为 `value`。
返回一个包含该项的`iterator`结构`TryEmplaceResult`实例，以及一个布尔值`inserted`，表示该项是新创建（`true`）还是之前存在（`false`）。

### `(since 6.9) QHash<Key, T>::TryEmplaceResult insertOrAssign(const Key &key, Value &&value)`

**作用与语义：**

尝试插入带有 `key` 和 `value` 的项。如果已有 `key` 的项，其值会被覆盖为 `value`。
返回一个包含该项的`iterator`结构`TryEmplaceResult`实例，以及一个布尔值`inserted`，表示该项是新创建（`true`）还是之前存在（`false`）。

### `(since 6.9) std::pair<QHash<Key, T>::key_value_iterator, bool> insert_or_assign(Key &&key, Value &&value)`

**作用与语义：**

尝试插入带有 `key` 和 `value` 的项。如果已有 具有 `key` 的项，其值会被覆盖为 `value`。
返回一对，由指向该项的迭代器和一个布尔值组成，表示该项是新创建（`true`）还是之前存在（`false`）。
这些功能是为了与标准库的兼容性而提供。

### `(since 6.9) std::pair<QHash<Key, T>::key_value_iterator, bool> insert_or_assign(const Key &key, Value &&value)`

**作用与语义：**

尝试插入带有`key`和`value`的项。如果已有`key`的项，其值会被覆盖为`value`。
返回一对，由指向该项的迭代器和一个布尔值组成，表示该项是新创建（`true`）还是之前存在（`false`）。
`hint`被忽视了。
这些功能是为了与标准库的兼容性而提供。

### `(since 6.9) QHash<Key, T>::key_value_iterator insert_or_assign(QHash<Key, T>::const_iterator hint, Key &&key, Value &&value)`

**作用与语义：**

尝试插入带有`key`和`value`的项。如果已有`key`的项，其值会被覆盖为`value`。
返回一对，由指向该项的迭代器和一个布尔值组成，表示该项是新创建（`true`）还是之前存在（`false`）。
`hint`被忽视了。
这些功能是为了与标准库的兼容性而提供。

### `(since 6.9) QHash<Key, T>::key_value_iterator insert_or_assign(QHash<Key, T>::const_iterator hint, const Key &key, Value &&value)`

**作用与语义：**

尝试插入带有`key`和`value`的项。如果已有`key`的项，其值会被覆盖为`value`。
返回一对，由指向该项的迭代器和一个布尔值组成，表示该项是新创建（`true`）还是之前存在（`false`）。
`hint`被忽视了。
这些功能是为了与标准库的兼容性而提供。

### `Key key(const T &value) const`

**作用与语义：**

返回映射到`value`的第一个键。如果哈希中没有映射到`value`的项，返回`defaultKey`;如果未提供该参数，则返回默认构造的键。
该函数可能较慢（线性时间），因为`QHash`的内部数据结构是通过键快速查找而优化的，而非按值。

### `(since 6.9) QHash<Key, T>::TryEmplaceResult tryEmplace(Key &&key, Args &&... args)`

**作用与语义：**

插入一个带有`key`和由`args`构造的值的新项。如果已有`key`的项存在，则不进行插入。
返回一个`TryEmplaceResult`实例，一个包含新创建项目或阻止插入的既有项目的`iterator`结构，以及一个布尔值的 `inserted`，表示插入是否发生。
例如，这可以用来避免比较新旧大小或重复查找的模式。你之前可能写过类似这样的代码：
你可以写：

**官方示例：**

```cpp
 QHash<int, MyType> hash;
 // [...]
 int myKey = getKey();
 qsizetype oldSize = hash.size();
 MyType &elem = hash[myKey];
 if (oldSize != hash.size()) // Size changed: new element!
     initialize(elem);
 // [use elem...]
```

### `(since 6.9) QHash<Key, T>::TryEmplaceResult tryEmplace(const Key &key, Args &&... args)`

**作用与语义：**

插入一个带有`key`和由`args`构造的值的新项。如果已有`key`的项存在，则不进行插入。
返回一个`TryEmplaceResult`实例，一个包含新创建项目或阻止插入的既有项目的`iterator`结构，以及一个布尔值的 `inserted`，表示插入是否发生。
例如，这可以用来避免比较新旧大小或重复查找的模式。你之前可能写过类似这样的代码：
你可以写：

**官方示例：**

```cpp
 QHash<int, MyType> hash;
 // [...]
 int myKey = getKey();
 qsizetype oldSize = hash.size();
 MyType &elem = hash[myKey];
 if (oldSize != hash.size()) // Size changed: new element!
     initialize(elem);
 // [use elem...]
```

### `(since 6.9) QHash<Key, T>::TryEmplaceResult tryInsert(const Key &key, const T &value)`

**作用与语义：**

插入一个`key`和值为`value`的新项。如果已有`key`的项存在，则不进行插入。
返回一个 T实例 `TryEmplaceResult`，一个包含新创建项目或阻止插入的既有项目`iterator`的结构，以及一个布尔值 `inserted`，表示插入是否发生。

### `(since 6.9) std::pair<QHash<Key, T>::key_value_iterator, bool> try_emplace(Key &&key, Args &&... args)`

**作用与语义：**

插入一个带有`key`和由`args`构造值的新项。如果已有`key`项，则不进行插入。
返回一对由迭代器（迭代器）到插入的项目（或阻止插入的项目）和一个布ol组成，表示插入是否发生。
这些功能是为了与标准库的兼容性而提供。

### `(since 6.9) std::pair<QHash<Key, T>::key_value_iterator, bool> try_emplace(const Key &key, Args &&... args)`

**作用与语义：**

插入一个带有`key`和由`args`构造的值的新项。如果已有`key`的项，则不进行插入。
返回插入项的迭代器，或返回阻止插入的项。
`hint`被忽视了。
这些功能是为了与标准库的兼容性而提供。

### `(since 6.9) QHash<Key, T>::key_value_iterator try_emplace(QHash<Key, T>::const_iterator hint, K &&key, Args &&... args)`

**作用与语义：**

插入一个带有`key`和由`args`构造的值的新项。如果已有`key`的项，则不进行插入。
返回插入项的迭代器，或返回阻止插入的项。
`hint`被忽视了。
这些功能是为了与标准库的兼容性而提供。

### `(since 6.9) QHash<Key, T>::key_value_iterator try_emplace(QHash<Key, T>::const_iterator hint, const Key &key, Args &&... args)`

**作用与语义：**

插入一个带有`key`和由`args`构造的值的新项。如果已有`key`的项，则不进行插入。
返回插入项的迭代器，或返回阻止插入的项。
`hint`被忽视了。
这些功能是为了与标准库的兼容性而提供。

### `T value(const Key &key) const`

**作用与语义：**

返回与`key`关联的值。
如果哈希中没有包含`key`项，函数返回`defaultValue`;如果未提供该参数，则返回默认构造值。

### `size_t qHash(const QStringRef &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `size_t qHash(const QMqttTopicFilter &filter, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `size_t qHash(QSslEllipticCurve key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `size_t qHash(const QGeoCoordinate &coordinate, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `size_t qHash(const QMqttTopicName &name, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `size_t qHash(const QOcspResponse &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `size_t qHash(const QSslCertificate &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `size_t qHash(const QSslError &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

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

`QHash` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
