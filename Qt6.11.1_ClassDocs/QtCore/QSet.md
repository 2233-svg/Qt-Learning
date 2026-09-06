# QSet

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QSet` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSet` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QSet>`
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
- `ConstIterator`
- `Iterator`
- `const_pointer`
- `const_reference`
- `difference_type`
- `key_type`
- `pointer`
- `reference`
- `size_type`
- `value_type`

### 公有函数

- `QSet()`
- `QSet(std::initializer_list<T> list)`
- `QSet(InputIterator first, InputIterator last)`
- `QSet<T>::const_iterator begin() const`
- `QSet<T>::iterator begin()`
- `qsizetype capacity() const`
- `QSet<T>::const_iterator cbegin() const`
- `QSet<T>::const_iterator cend() const`
- `void clear()`
- `QSet<T>::const_iterator constBegin() const`
- `QSet<T>::const_iterator constEnd() const`
- `QSet<T>::const_iterator constFind(const T &value) const`
- `bool contains(const QSet<T> &other) const`
- `bool contains(const T &value) const`
- `qsizetype count() const`
- `bool empty() const`
- `QSet<T>::const_iterator end() const`
- `QSet<T>::iterator end()`
- `QSet<T>::iterator erase(QSet<T>::const_iterator pos)`
- `QSet<T>::const_iterator find(const T &value) const`
- `QSet<T>::iterator find(const T &value)`
- `QSet<T>::iterator insert(const T &value)`
- `(since 6.1) QSet<T>::iterator insert(QSet<T>::const_iterator it, const T &value)`
- `QSet<T> & intersect(const QSet<T> &other)`
- `bool intersects(const QSet<T> &other) const`
- `bool isEmpty() const`
- `bool remove(const T &value)`
- `(since 6.1) qsizetype removeIf(Pred pred)`
- `void reserve(qsizetype size)`
- `qsizetype size() const`
- `void squeeze()`
- `QSet<T> & subtract(const QSet<T> &other)`
- `void swap(QSet<T> &other)`
- `QSet<T> & unite(QSet<T> &&other)`
- `QSet<T> & unite(const QSet<T> &other)`
- `QList<T> values() const`
- `QSet<T> & operator&=(const QSet<T> &other)`
- `QSet<T> & operator&=(const T &value)`
- `QSet<T> & operator+=(QSet<T> &&other)`
- `QSet<T> & operator+=(const QSet<T> &other)`
- `QSet<T> & operator+=(const T &value)`
- `QSet<T> & operator-=(const QSet<T> &other)`
- `QSet<T> & operator-=(const T &value)`
- `QSet<T> & operator<<(const T &value)`
- `QSet<T> & operator|=(QSet<T> &&other)`
- `QSet<T> & operator|=(const QSet<T> &other)`
- `QSet<T> & operator|=(const T &value)`

### 相关非成员函数

- `(since 6.1) qsizetype erase_if(QSet<T> &set, Predicate pred)`
- `bool operator!=(const QSet<T> &lhs, const QSet<T> &rhs)`
- `QSet<T> operator&(QSet<T> &&lhs, const QSet<T> &rhs)`
- `QSet<T> operator&(const QSet<T> &lhs, const QSet<T> &rhs)`
- `QSet<T> operator+(QSet<T> &&lhs, QSet<T> &&rhs)`
- `QSet<T> operator+(QSet<T> &&lhs, const QSet<T> &rhs)`
- `QSet<T> operator+(const QSet<T> &lhs, QSet<T> &&rhs)`
- `QSet<T> operator+(const QSet<T> &lhs, const QSet<T> &rhs)`
- `QSet<T> operator-(QSet<T> &&lhs, const QSet<T> &rhs)`
- `QSet<T> operator-(const QSet<T> &lhs, const QSet<T> &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QSet<T> &set)`
- `bool operator==(const QSet<T> &lhs, const QSet<T> &rhs)`
- `QDataStream & operator>>(QDataStream &in, QSet<T> &set)`
- `QSet<T> operator|(QSet<T> &&lhs, QSet<T> &&rhs)`
- `QSet<T> operator|(QSet<T> &&lhs, const QSet<T> &rhs)`
- `QSet<T> operator|(const QSet<T> &lhs, QSet<T> &&rhs)`
- `QSet<T> operator|(const QSet<T> &lhs, const QSet<T> &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QSet::ConstIterator`

**作用与语义：**

Qt风格的`QSet::const_iterator`同义词。

### `QSet::Iterator`

**作用与语义：**

Qt风格的同义词`QSet::iterator`。

### `QSet::const_pointer`

**作用与语义：**

Typedef 表示 const T *。提供以兼容 STL 的。

### `QSet::const_reference`

**作用与语义：**

Typedef 用于 const T 和。为 STL 兼容性提供。

### `QSet::difference_type`

**作用与语义：**

Typedef 用于 const ptrdiff_t。提供 STL 兼容性。

### `QSet::key_type`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `QSet::pointer`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `QSet::reference`

**作用与语义：**

T和的Typedef。提供STL兼容性。

### `QSet::size_type`

**作用与语义：**

类型定义用于国际语言。提供支持STL兼容性。

### `QSet::value_type`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `[noexcept] QSet::QSet()`

**作用与语义：**

构造一个空集合。

### `QSet::QSet(std::initializer_list<T> list)`

**作用与语义：**

构造一个集合，包含初始化器列表中每个元素的副本 ，这些元素的副本 `list`。

### `template <typename InputIterator, QtPrivate::IfIsInputIterator<InputIterator> = true> QSet::QSet(InputIterator first, InputIterator last)`

**作用与语义：**

构造一个包含迭代子范围内容的集合 [`first`， `last`）。
`InputIterator`的价值类型必须可转换为`T`。
注意：如果范围[`first`， `last`）包含重复元素，则保留第一个元素。

### `[noexcept] QSet<T>::const_iterator QSet::begin() const`

**作用与语义：**

返回一个位于集合中第一个项的const STL风格迭代器。

### `QSet<T>::iterator QSet::begin()`

**作用与语义：**

返回一个非const型STL式迭代器，位于集合的第一个项。

### `qsizetype QSet::capacity() const`

**作用与语义：**

返回集合内部哈希表中的桶数。
该函数的唯一目的是提供一种微调`QSet`内存使用的方法。一般来说，你很少需要调用这个函数。如果你想知道集合中有多少项，可以调用`size()`。

### `[noexcept] QSet<T>::const_iterator QSet::cbegin() const`

**作用与语义：**

返回一个位于集合中第一个项的const STL风格迭代器。

### `[noexcept] QSet<T>::const_iterator QSet::cend() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向集合中最后一个项之后的虚数项。

### `void QSet::clear()`

**作用与语义：**

移除套装中的所有元素。

### `[noexcept] QSet<T>::const_iterator QSet::constBegin() const`

**作用与语义：**

返回一个位于集合中第一个项的const STL风格迭代器。

### `[noexcept] QSet<T>::const_iterator QSet::constEnd() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向集合中最后一个项之后的虚数项。

### `QSet<T>::const_iterator QSet::constFind(const T &value) const`

**作用与语义：**

返回一个位于集合`value`项处的cont迭代器。如果集合中没有`value`项，函数返回`constEnd()`。

### `bool QSet::contains(const QSet<T> &other) const`

**作用与语义：**

如果集合包含`other`集合的所有项，返回`true`;否则返回`false`。

### `bool QSet::contains(const T &value) const`

**作用与语义：**

如果集合包含项`value`，则返回`true`;否则返回false。

### `qsizetype QSet::count() const`

**作用与语义：**

和`size()`一样。

### `bool QSet::empty() const`

**作用与语义：**

如果集合为空，返回`true`。该函数用于STL兼容性。它等价于`isEmpty()`。

### `[noexcept] QSet<T>::const_iterator QSet::end() const`

**作用与语义：**

返回一个const STL风格的迭代器，位于集合中最后一个项之后的虚数项。

### `QSet<T>::iterator QSet::end()`

**作用与语义：**

返回一个非const的STL风格迭代子，指向集合中最后一个项之后的虚数项。

### `QSet<T>::iterator QSet::erase(QSet<T>::const_iterator pos)`

**作用与语义：**

从集合中移除迭代器位置`pos`的项，返回位于集合中下一个项的迭代器。
与`remove()`不同，该函数从不促使`QSet`重排其内部数据结构。这意味着在迭代过程中可以安全地调用它，且不会影响集中项的顺序。
注意：迭代器`pos`必须有效且可去引用。在任何其他迭代器上调用该方法，包括其自身`end()`，都会导致行为未定义。特别地，即使是空集的`begin()`个迭代器也无法被反引用。

### `QSet<T>::const_iterator QSet::find(const T &value) const`

**作用与语义：**

返回一个位于集合`value`项处的cont迭代器。如果集合中没有`value`项，函数返回`constEnd()`。

### `QSet<T>::iterator QSet::find(const T &value)`

**作用与语义：**

返回一个位于集合`value`项处的非const迭代器。如果集合中没有`value`项，函数返回`end()`。

### `QSet<T>::iterator QSet::insert(const T &value)`

**作用与语义：**

如果`value`项尚未在集合中，则插入`value`项，并返回指向插入项的迭代器。

### `[since 6.1] QSet<T>::iterator QSet::insert(QSet<T>::const_iterator it, const T &value)`

**作用与语义：**

如果`value`项尚未在集合中，`value`项插入到集合中，并返回指向插入项的迭代器。
迭代体`it`被忽略。
此功能是为了与STL的兼容性而提供。

### `QSet<T> &QSet::intersect(const QSet<T> &other)`

**作用与语义：**

移除该集合中所有不包含在`other`集合中的项。返回对该集合的引用。

### `bool QSet::intersects(const QSet<T> &other) const`

**作用与语义：**

如果该套装与`other`至少有一项物品相同，则`true`回归。

### `bool QSet::isEmpty() const`

**作用与语义：**

如果集合不包含元素，则返回`true`;否则返回 false。

### `bool QSet::remove(const T &value)`

**作用与语义：**

移除所有元素`value`的出现。如果实际移除了，则返回真;否则返回`false`。

### `[since 6.1] template <typename Pred> qsizetype QSet::removeIf(Pred pred)`

**作用与语义：**

从该集合中移除所有谓词`pred`返回`true`的元素。返回移除的元素数量（如有）。

### `void QSet::reserve(qsizetype size)`

**作用与语义：**

确保集合的内部哈希表至少包含`size`个桶。
该函数适用于需要构建庞大集合且希望避免重复重分配的代码。例如：
理想情况下，`size`应略多于集合中预期的最大元素数。`size`不必是素数，因为`QSet`内部也会使用素数。如果`size`低估，最坏的情况也不过是 `QSet` 会稍微慢一些。
一般来说，你很少需要调用这个函数。`QSet` 的内部哈希表会自动缩小或增长，以提供良好的性能而不浪费太多内存。

**官方示例：**

```cpp
 QSet<QString> set;
 set.reserve(20000);
 for (int i = 0; i < 20000; ++i)
     set.insert(values[i]);
```

### `qsizetype QSet::size() const`

**作用与语义：**

返回集合中的物品数量。

### `void QSet::squeeze()`

**作用与语义：**

减少集合内部哈希表的大小以节省内存。
该函数的唯一目的是提供一种微调`QSet`内存使用的方法。一般来说，你很少需要调用这个函数。

### `QSet<T> &QSet::subtract(const QSet<T> &other)`

**作用与语义：**

移除该集合中包含在`other`集合中的所有项目。返回对该集合的引用。

### `[noexcept] void QSet::swap(QSet<T> &other)`

**作用与语义：**

将这套设备与`other`交换。这个操作非常快，而且从不失败。

### `QSet<T> &QSet::unite(QSet<T> &&other)`

**作用与语义：**

`other`集中未包含的每个元素都入到该集合中。返回该集合的引用。

### `QList<T> QSet::values() const`

**作用与语义：**

返回包含集合中元素的新`QList`。`QList`中元素的顺序未定义。
注意：自Qt 5.14起，Qt的通用容器类可以使用范围构造器，应替代该方法。
该函数会以线性时间创建一个新的列表。通过从`constBegin()`迭代到`constEnd()`可以避免这所涉及的时间和内存消耗。

### `QSet<T> &QSet::operator&=(const QSet<T> &other)`

**作用与语义：**

和交集（`other`）一样。

### `QSet<T> &QSet::operator&=(const T &value)`

**作用与语义：**

与 intersect（other） 相同，如果我们认为 other 是包含单元素`value`的集合。

### `QSet<T> &QSet::operator-=(const QSet<T> &other)`

**作用与语义：**

和减法（`other`）一样。

### `QSet<T> &QSet::operator-=(const T &value)`

**作用与语义：**

如果发现了`value`项，则移除该集合中的出现，并返回该集合的引用。如果`value`不包含该集合，则不移除任何内容。

### `QSet<T> &QSet::operator|=(const T &value)`

**作用与语义：**

插入一个新项`value`并返回该集合的引用。如果`value`已存在于集合中，则该集合保持不变。

### `QSet<T> &QSet::operator+=(QSet<T> &&other)`

**作用与语义：**

插入一个新项`value`并返回该集合的引用。如果`value`已存在于集合中，则该集合保持不变。

### `[since 6.1] template <typename T, typename Predicate> qsizetype erase_if(QSet<T> &set, Predicate pred)`

**作用与语义：**

从集合`set`中移除所有谓词 `pred` 返回为真元素的元素。返回被移除的元素数量（如有）。

### `[noexcept] bool operator!=(const QSet<T> &lhs, const QSet<T> &rhs)`

**作用与语义：**

如果`lhs`集不等于`rhs`集，则返回`true`;否则返回`false`。
如果两个集合包含相同的元素，则它们被视为相等。
该函数需要值类型来实现`operator==()`。

### `QSet<T> operator&(QSet<T> &&lhs, const QSet<T> &rhs)`

**作用与语义：**

返回一个新 `QSet`，即集合 `lhs` 和 `rhs` 的交集。

### `QSet<T> operator-(QSet<T> &&lhs, const QSet<T> &rhs)`

**作用与语义：**

返回一个新`QSet`，即集合`lhs`和`rhs`的集合差。

### `template <typename T> QDataStream &operator<<(QDataStream &out, const QSet<T> &set)`

**作用与语义：**

插入一个新项`value`并返回该集合的引用。如果`value`已存在于集合中，则该集合保持不变。

### `[noexcept] bool operator==(const QSet<T> &lhs, const QSet<T> &rhs)`

**作用与语义：**

如果`lhs`集合等于`rhs`集合，则返回`true`;否则返回`false`。
如果两个集合包含相同的元素，则它们被视为相等。
该函数需要值类型来实现`operator==()`。

### `template <typename T> QDataStream &operator>>(QDataStream &in, QSet<T> &set)`

**作用与语义：**

将 stream `in` 的集合读取到 `set`。
该函数需要值类型来实现`operator>>()`。

### `QSet<T> operator+(QSet<T> &&lhs, QSet<T> &&rhs)`

**作用与语义：**

返回一个新`QSet`，即集合`lhs`和`rhs`的并集。

### `class const_iterator`

**作用与语义：**

QSet：：const_iterator 类为 QSet 提供了一个 STL 风格的 const 迭代器。
`QSet` 既有 STL 风格的迭代器，也有 Java 风格的迭代器。STL 风格的迭代器更为低阶且操作更繁琐;但它们稍快一些，对于已经懂 STL 的开发者来说，它们具有熟悉度的优势。
`QSet`<Key， T>：：const_iterator 允许你对某个`QSet`进行迭代。如果你想在迭代时修改`QSet`，必须用 `QSet::iterator`。通常在非连续性`QSet`上使用 `QSet::const_iterator` 也是好习惯，除非你需要通过迭代器更改`QSet`。Const 迭代器速度稍快，且能提高代码的可读性。
默认的`QSet::const_iterator`构造器会创建一个未初始化的迭代器。你必须先用 `QSet::begin()`、`QSet::end()` 或 `QSet::insert()` 等函数初始化它，才能开始迭代。这里有一个典型的循环，打印集合中存储的所有项：
STL 风格的迭代器可以作为通用算法的参数。例如，以下是使用 qFind() 算法在集合中寻找一个项的方法：
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。

**官方示例：**

```cpp
 QSet<QString> set = {"January", "February", /*...*/ "December"};

 // i is QSet<QString>::const_iterator
 for (auto i = set.cbegin(), end = set.cend(); i != end; ++i)
     qDebug() << *i;
```

### `class iterator`

**作用与语义：**

QSet::iterator 类为 QSet 提供了一个 STL 风格的非常量迭代器。
`QSet` 同时具有 STL 风格的迭代器和 Java 风格的迭代器。STL 风格的迭代器更底层，也更复杂难用；另一方面，它们速度略快，并且对于已经熟悉 STL 的开发者来说，更具熟悉性优势。
`QSet`<T>::iterator 允许你遍历一个 `QSet` 并在遍历过程中移除项目（使用 `QSet::erase()`）。(`QSet` 不允许通过迭代器修改值，因为那可能需要在 `QSet` 使用的内部哈希表中移动值。) 如果你想遍历一个 const `QSet`，应使用 `QSet::const_iterator`。在非 const `QSet` 上使用 `QSet::const_iterator` 也是一个良好的习惯，除非你需要通过迭代器修改 `QSet`。常量迭代器速度略快，并且可以提高代码可读性。
默认的 `QSet::iterator` 构造函数创建一个未初始化的迭代器。在开始迭代之前，你必须使用 `QSet::begin()`、`QSet::end()` 或 `QSet::insert()` 等函数进行初始化。下面是一个打印集合中所有项目的典型循环：
下面是一个在遍历过程中移除集合中某些项目（所有以‘J’开头的项目）的循环：
STL 风格的迭代器可以作为通用算法的参数。例如，下面展示了如何用 qFind() 算法在集合中查找一个项目：
同一个集合上可以使用多个迭代器。
警告: 隐式共享容器上的迭代器并不完全像 STL 迭代器那样工作。在迭代器正在使用容器时，应避免复制该容器。有关更多信息，请阅读《隐式共享迭代器问题》。

**官方示例：**

```cpp
 QSet<QString> set = {"January", "February", /*...*/ "December"};

 // i is a QSet<QString>::iterator
 for (auto i = set.begin(), end = set.end(); i != end; ++i)
     qDebug() << *i;
```

### `ConstIterator`

**作用与语义：**

Qt风格的`QSet::const_iterator`同义词。

### `Iterator`

**作用与语义：**

Qt风格的同义词`QSet::iterator`。

### `const_pointer`

**作用与语义：**

Typedef 表示 const T *。提供以兼容 STL 的。

### `const_reference`

**作用与语义：**

Typedef 用于 const T 和。为 STL 兼容性提供。

### `difference_type`

**作用与语义：**

Typedef 用于 const ptrdiff_t。提供 STL 兼容性。

### `key_type`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `pointer`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `reference`

**作用与语义：**

T和的Typedef。提供STL兼容性。

### `size_type`

**作用与语义：**

类型定义用于国际语言。提供支持STL兼容性。

### `value_type`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `QSet<T> & unite(const QSet<T> &other)`

**作用与语义：**

`other`集中未包含的每个元素都入到该集合中。返回该集合的引用。

### `QSet<T> & operator+=(const QSet<T> &other)`

**作用与语义：**

和 unite（`other`）一样。

### `QSet<T> & operator+=(const T &value)`

**作用与语义：**

和 unite（`other`）一样。

### `QSet<T> & operator<<(const T &value)`

**作用与语义：**

写入流媒体`out`的`set`。
该函数需要值类型来实现`operator<<()`。

### `QSet<T> & operator|=(QSet<T> &&other)`

**作用与语义：**

和 unite（`other`）一样。

### `QSet<T> & operator|=(const QSet<T> &other)`

**作用与语义：**

和 unite（`other`）一样。

### `QSet<T> operator&(const QSet<T> &lhs, const QSet<T> &rhs)`

**作用与语义：**

返回一个新 `QSet`，即集合 `lhs` 和 `rhs` 的交集。

### `QSet<T> operator+(QSet<T> &&lhs, const QSet<T> &rhs)`

**作用与语义：**

返回一个新`QSet`，即集合`lhs`和`rhs`的并集。

### `QSet<T> operator+(const QSet<T> &lhs, QSet<T> &&rhs)`

**作用与语义：**

返回一个新`QSet`，即集合`lhs`和`rhs`的并集。

### `QSet<T> operator+(const QSet<T> &lhs, const QSet<T> &rhs)`

**作用与语义：**

返回一个新`QSet`，即集合`lhs`和`rhs`的并集。

### `QSet<T> operator-(const QSet<T> &lhs, const QSet<T> &rhs)`

**作用与语义：**

返回一个新`QSet`，即集合`lhs`和`rhs`的集合差。

### `QSet<T> operator|(QSet<T> &&lhs, QSet<T> &&rhs)`

**作用与语义：**

返回一个新`QSet`，即集合`lhs`和`rhs`的并集。

### `QSet<T> operator|(QSet<T> &&lhs, const QSet<T> &rhs)`

**作用与语义：**

返回一个新`QSet`，即集合`lhs`和`rhs`的并集。

### `QSet<T> operator|(const QSet<T> &lhs, QSet<T> &&rhs)`

**作用与语义：**

返回一个新`QSet`，即集合`lhs`和`rhs`的并集。

### `QSet<T> operator|(const QSet<T> &lhs, const QSet<T> &rhs)`

**作用与语义：**

返回一个新`QSet`，即集合`lhs`和`rhs`的并集。

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

`QSet` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
