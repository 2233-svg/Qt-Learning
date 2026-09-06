# QList

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QList` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QList` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QList>`
- 继承自：未在类页中列出
- 直接派生类：QBluetoothServiceInfo::Alternative、QBluetoothServiceInfo::Sequence、QByteArrayList、QItemSelection、QMqttUserProperties、QNdefMessage、QPolygon、QPolygonF、QQueue、QSignalSpy、QStack、QStringList、QTestEventList、QVector、QVulkanInfoVector,、QXmlStreamAttributes

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
- `const_reverse_iterator`
- `difference_type`
- `parameter_type`
- `pointer`
- `reference`
- `reverse_iterator`
- `rvalue_ref`
- `size_type`
- `value_type`

### 公有函数

- `QList()`
- `QList(qsizetype size)`
- `QList(std::initializer_list<T> args)`
- `QList(InputIterator first, InputIterator last)`
- `QList(qsizetype size, QList<T>::parameter_type value)`
- `(since 6.8) QList(qsizetype size, Qt::Initialization)`
- `QList(const QList<T> &other)`
- `QList(QList<T> &&other)`
- `~QList()`
- `void append(QList<T>::parameter_type value)`
- `(since 6.0) void append(QList<T> &&value)`
- `void append(QList<T>::rvalue_ref value)`
- `void append(const QList<T> &value)`
- `(since 6.6) QList<T> & assign(std::initializer_list<T> l)`
- `(since 6.6) QList<T> & assign(InputIterator first, InputIterator last)`
- `(since 6.6) QList<T> & assign(qsizetype n, QList<T>::parameter_type t)`
- `QList<T>::const_reference at(qsizetype i) const`
- `QList<T>::reference back()`
- `QList<T>::const_reference back() const`
- `QList<T>::iterator begin()`
- `QList<T>::const_iterator begin() const`
- `qsizetype capacity() const`
- `QList<T>::const_iterator cbegin() const`
- `QList<T>::const_iterator cend() const`
- `void clear()`
- `QList<T>::const_iterator constBegin() const`
- `QList<T>::const_pointer constData() const`
- `QList<T>::const_iterator constEnd() const`
- `const T & constFirst() const`
- `const T & constLast() const`
- `bool contains(const AT &value) const`
- `qsizetype count(const AT &value) const`
- `qsizetype count() const`
- `QList<T>::const_reverse_iterator crbegin() const`
- `QList<T>::const_reverse_iterator crend() const`
- `QList<T>::pointer data()`
- `QList<T>::const_pointer data() const`
- `QList<T>::iterator emplace(qsizetype i, Args &&... args)`
- `QList<T>::iterator emplace(QList<T>::const_iterator before, Args &&... args)`
- `QList<T>::reference emplaceBack(Args &&... args)`
- `QList<T>::reference emplace_back(Args &&... args)`
- `bool empty() const`
- `QList<T>::iterator end()`
- `QList<T>::const_iterator end() const`
- `bool endsWith(QList<T>::parameter_type value) const`
- `QList<T>::iterator erase(QList<T>::const_iterator pos)`
- `QList<T>::iterator erase(QList<T>::const_iterator begin, QList<T>::const_iterator end)`
- `QList<T> & fill(QList<T>::parameter_type value, qsizetype size = -1)`
- `T & first()`
- `(since 6.0) QList<T> first(qsizetype n) const`
- `const T & first() const`
- `QList<T>::reference front()`
- `QList<T>::const_reference front() const`
- `qsizetype indexOf(const AT &value, qsizetype from = 0) const`
- `QList<T>::iterator insert(qsizetype i, QList<T>::parameter_type value)`
- `QList<T>::iterator insert(qsizetype i, QList<T>::rvalue_ref value)`
- `QList<T>::iterator insert(QList<T>::const_iterator before, qsizetype count, QList<T>::parameter_type value)`
- `QList<T>::iterator insert(QList<T>::const_iterator before, QList<T>::parameter_type value)`
- `QList<T>::iterator insert(QList<T>::const_iterator before, QList<T>::rvalue_ref value)`
- `QList<T>::iterator insert(qsizetype i, qsizetype count, QList<T>::parameter_type value)`
- `bool isEmpty() const`
- `T & last()`
- `(since 6.0) QList<T> last(qsizetype n) const`
- `const T & last() const`
- `qsizetype lastIndexOf(const AT &value, qsizetype from = -1) const`
- `qsizetype length() const`
- `(since 6.8) qsizetype max_size() const`
- `QList<T> mid(qsizetype pos, qsizetype length = -1) const`
- `void move(qsizetype from, qsizetype to)`
- `void pop_back()`
- `void pop_front()`
- `void prepend(QList<T>::parameter_type value)`
- `void prepend(QList<T>::rvalue_ref value)`
- `void push_back(QList<T>::parameter_type value)`
- `void push_back(QList<T>::rvalue_ref value)`
- `void push_front(QList<T>::parameter_type value)`
- `void push_front(QList<T>::rvalue_ref value)`
- `QList<T>::reverse_iterator rbegin()`
- `QList<T>::const_reverse_iterator rbegin() const`
- `void remove(qsizetype i, qsizetype n = 1)`
- `qsizetype removeAll(const AT &t)`
- `void removeAt(qsizetype i)`
- `void removeFirst()`
- `(since 6.1) qsizetype removeIf(Predicate pred)`
- `void removeLast()`
- `bool removeOne(const AT &t)`
- `QList<T>::reverse_iterator rend()`
- `QList<T>::const_reverse_iterator rend() const`
- `void replace(qsizetype i, QList<T>::parameter_type value)`
- `void replace(qsizetype i, QList<T>::rvalue_ref value)`
- `void reserve(qsizetype size)`
- `(since 6.0) void resize(qsizetype size)`
- `(since 6.0) void resize(qsizetype size, QList<T>::parameter_type c)`
- `(since 6.8) void resizeForOverwrite(qsizetype size)`
- `void shrink_to_fit()`
- `qsizetype size() const`
- `(since 6.0) QList<T> sliced(qsizetype pos, qsizetype n) const`
- `(since 6.0) QList<T> sliced(qsizetype pos) const`
- `void squeeze()`
- `bool startsWith(QList<T>::parameter_type value) const`
- `void swap(QList<T> &other)`
- `void swapItemsAt(qsizetype i, qsizetype j)`
- `T takeAt(qsizetype i)`
- `QList<T>::value_type takeFirst()`
- `QList<T>::value_type takeLast()`
- `T value(qsizetype i) const`
- `T value(qsizetype i, QList<T>::parameter_type defaultValue) const`
- `bool operator!=(const QList<T> &other) const`
- `QList<T> operator+(QList<T> &&other) &&`
- `QList<T> operator+(const QList<T> &other) &&`
- `QList<T> operator+(QList<T> &&other) const &`
- `QList<T> operator+(const QList<T> &other) const &`
- `QList<T> & operator+=(const QList<T> &other)`
- `(since 6.0) QList<T> & operator+=(QList<T> &&other)`
- `QList<T> & operator+=(QList<T>::parameter_type value)`
- `QList<T> & operator+=(QList<T>::rvalue_ref value)`
- `bool operator<(const QList<T> &other) const`
- `QList<T> & operator<<(QList<T>::parameter_type value)`
- `QList<T> & operator<<(const QList<T> &other)`
- `(since 6.0) QList<T> & operator<<(QList<T> &&other)`
- `QList<T> & operator<<(QList<T>::rvalue_ref value)`
- `bool operator<=(const QList<T> &other) const`
- `QList<T> & operator=(QList<T> &&other)`
- `QList<T> & operator=(const QList<T> &other)`
- `QList<T> & operator=(std::initializer_list<T> args)`
- `bool operator==(const QList<T> &other) const`
- `bool operator>(const QList<T> &other) const`
- `bool operator>=(const QList<T> &other) const`
- `QList<T>::reference operator[](qsizetype i)`
- `QList<T>::const_reference operator[](qsizetype i) const`

### 静态公有成员

- `(since 6.8) qsizetype maxSize()`

### 相关非成员函数

- `(since 6.1) qsizetype erase(QList<T> &list, const AT &t)`
- `(since 6.1) qsizetype erase_if(QList<T> &list, Predicate pred)`
- `size_t qHash(const QList<T> &key, size_t seed = 0)`
- `QDataStream & operator<<(QDataStream &out, const QList<T> &list)`
- `(since 6.9) auto operator<=>(const QList<T> &lhs, const QList<T> &rhs)`
- `QDataStream & operator>>(QDataStream &in, QList<T> &list)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QList::ConstIterator`

**作用与语义：**

Qt风格的`QList::const_iterator`同义词。

### `[alias] QList::Iterator`

**作用与语义：**

Qt风格的同义词`QList::iterator`。

### `[alias] QList::const_pointer`

**作用与语义：**

提供STL兼容性。

### `[alias] QList::const_reference`

**作用与语义：**

提供STL兼容性。

### `[alias] QList::const_reverse_iterator`

**作用与语义：**

QList：：const_reverse_iterator typedef 提供了一个 STL 风格的 cont 反迭代器用于 `QList`。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。
警告：当`QList`被修改时，迭代器将被无效。请考虑所有迭代器默认无效。该规则的例外情况有明确文档。

### `[alias] QList::difference_type`

**作用与语义：**

提供STL兼容性。

### `[alias] QList::pointer`

**作用与语义：**

提供STL兼容性。

### `[alias] QList::reference`

**作用与语义：**

提供STL兼容性。

### `[alias] QList::reverse_iterator`

**作用与语义：**

QList：：reverse_iterator typedef 提供了一个 STL 风格的非一致性反迭代器用于 `QList`。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。
警告：当`QList`被修改时，迭代器将被无效。请考虑所有迭代器默认无效。本规则的例外情况有明确文档。

### `[alias] QList::size_type`

**作用与语义：**

提供STL兼容性。

### `[alias] QList::value_type`

**作用与语义：**

提供STL兼容性。

### `[constexpr noexcept] QList::QList()`

**作用与语义：**

构建一个空列表。

### `[explicit] QList::QList(qsizetype size)`

**作用与语义：**

构建初始大小为`size`元素的列表。
这些元素以默认构造值初始化。

### `QList::QList(std::initializer_list<T> args)`

**作用与语义：**

根据 `args` 给出的 std：：initializer_list 构建列表。

### `template <typename InputIterator, QList<T>::if_input_iterator<InputIterator> = true> QList::QList(InputIterator first, InputIterator last)`

**作用与语义：**

构建一个包含迭代子范围内容的列表 [`first`， `last`）。
`InputIterator`的价值类型必须可转换为`T`。
只有当`InputIterator`满足LegacyInputIterator的要求时，才参与重载决议。

### `QList::QList(qsizetype size, QList<T>::parameter_type value)`

**作用与语义：**

构建初始大小为`size`元素的列表。每个元素初始化为`value`。

### `[since 6.8] QList::QList(qsizetype size, Qt::Initialization)`

**作用与语义：**

构建初始大小为`size`元素的列表。
QList 会尝试不初始化这些元素。
具体来说：
- 如果`T`有一个接受`Qt::Uninitialized`的构造函数，则该构造器将用于初始化元素;
- 否则，每个元素都是默认构造的。对于平凡可构造类型（如`int`、`float`等），这等同于不初始化它们。

### `[default] QList::QList(const QList<T> &other)`

**作用与语义：**

构建了`other`的副本。
该操作耗时为常数，因为QList是隐式共享的。这使得从函数返回QList非常快速。如果共享实例被修改，它会被复制（写时复制），这需要线性时间。

### `[default] QList::QList(QList<T> &&other)`

**作用与语义：**

Move-构造一个QList实例，使其指向`other`指向的同一个对象。

### `[default] QList::~QList()`

**作用与语义：**

摧毁了名单。

### `void QList::append(QList<T>::parameter_type value)`

**作用与语义：**

在列表末尾插入`value`。
这与调用 resize（`size()` 1） 并将 `value` 分配给列表中的新最后一个元素是一样的。
该操作相对快速，因为`QList`通常分配的内存超过必要，因此可以不每次重新分配整个列表即可增长。

**官方示例：**

```cpp
 QList<QString> list;
 list.append("one");
 list.append("two");
 QString three = "three";
 list.append(three);
 // list: ["one", "two", "three"]
 // three: "three"
```

### `[since 6.0] void QList::append(QList<T> &&value)`

**作用与语义：**

将`value`列表中的项目移动到该列表的末尾。

### `void QList::append(QList<T>::rvalue_ref value)`

**作用与语义：**

在列表末尾插入`value`。
这与调用 resize（`size()` 1） 并将 `value` 分配给列表中的新最后一个元素是一样的。
该操作相对快速，因为`QList`通常分配的内存超过必要，因此可以不每次重新分配整个列表即可增长。

**官方示例：**

```cpp
 QList<QString> list;
 list.append("one");
 list.append("two");
 QString three = "three";
 list.append(three);
 // list: ["one", "two", "three"]
 // three: "three"
```

### `void QList::append(const QList<T> &value)`

**作用与语义：**

将`value`列表中的项目附加到该列表中。

### `[since 6.6] QList<T> &QList::assign(std::initializer_list<T> l)`

**作用与语义：**

用 `l` 元素的副本替换本列表内容。
该列表的大小将等于`l`中的元素数量。
该函数仅在`l`中的元素数量超过该列表容量或该列表被共享时分配内存。

### `[since 6.6] template <typename InputIterator, QList<T>::if_input_iterator<InputIterator> = true> QList<T> &QList::assign(InputIterator first, InputIterator last)`

**作用与语义：**

用迭代符范围内元素的副本替换该列表的内容 [`first`， `last`）。
该列表的大小将等于该区间 [`first`， `last`） 中的元素数量。
该函数仅在该区间的元素数量超过该列表的容量或该列表被共享时分配内存。
注意：如果任一参数是*这个的迭代子，行为是未定义的。
只有当`InputIterator`满足LegacyInputIterator的要求时，才参与重载决议。

### `[since 6.6] QList<T> &QList::assign(qsizetype n, QList<T>::parameter_type t)`

**作用与语义：**

将本列表内容替换为`n`份`t`副本。
这个列表的大小将等于`n`。
该函数仅在内存超过列表容量或该列表被共享时分配`n`。

### `[noexcept] QList<T>::const_reference QList::at(qsizetype i) const`

**作用与语义：**

返回列表中索引位置`i`的项目。
`i`必须是列表中有效的索引位置（即0 <= `i` < `size()`）。

### `QList<T>::reference QList::back()`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于`last()`。

### `[noexcept] QList<T>::const_reference QList::back() const`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于`last()`。

### `QList<T>::iterator QList::begin()`

**作用与语义：**

返回一个STL风格的迭代器，指向列表中的第一个项目。
警告：返回的迭代器在脱离或`QList`修改时将失效。

### `[noexcept] QList<T>::const_iterator QList::begin() const`

**作用与语义：**

返回一个STL风格的迭代器，指向列表中的第一个项目。
警告：返回的迭代器在脱离或`QList`修改时将失效。

### `qsizetype QList::capacity() const`

**作用与语义：**

返回可在不强制重新分配的情况下存储列表中的最大数量的项目。
该函数的唯一目的是提供一种微调`QList`内存使用的方法。一般来说，你很少需要调用这个函数。如果你想知道列表中有多少项，可以调用`size()`。
注意：静态分配的列表会报告容量为0，即使它不是空的。
警告：分配内存块中的空闲空间位置未定义。换句话说，你不应假设空闲内存总是位于列表末尾。你可以调用`reserve()`以确保末尾有足够的空间。

### `[noexcept] QList<T>::const_iterator QList::cbegin() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向列表中的第一个项。
警告：返回的迭代器在脱离或`QList`修改时将失效。

### `[noexcept] QList<T>::const_iterator QList::cend() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向列表中最后一项之后。
警告：返回的迭代器在分离或`QList`修改时将失效。

### `void QList::clear()`

**作用与语义：**

移除列表中的所有元素。
如果该列表未被共享，`capacity()`将被保留。利用`squeeze()`来减少多余容量。
注意：在 5.7（`QVector`）和 6.0（`QList`）之前的 Qt 版本中，该函数释放了列表使用的内存，而非保留容量。

### `[noexcept] QList<T>::const_iterator QList::constBegin() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向列表中的第一个项。
警告：返回的迭代器在脱离或`QList`修改时将失效。

### `[noexcept] QList<T>::const_pointer QList::constData() const`

**作用与语义：**

返回一个指向列表中存储数据的const指针。该指针可用于访问列表中的项目。
警告：指针在分离或修改`QList`时将失效。
该函数主要用于将列表传递给接受普通 C 数组的函数。

### `[noexcept] QList<T>::const_iterator QList::constEnd() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向列表中最后一项之后。
警告：返回的迭代器在分离或`QList`修改时将失效。

### `[noexcept] const T &QList::constFirst() const`

**作用与语义：**

返回列表中第一个项的const引用。该函数假设列表不是空的。

### `[noexcept] const T &QList::constLast() const`

**作用与语义：**

返回列表中最后一项的const引用。该函数假设列表不是空的。

### `[noexcept] template <typename AT> bool QList::contains(const AT &value) const`

**作用与语义：**

如果列表中出现`value`，返回`true`;否则返回`false`。
该函数要求值类型实现 `operator==()`。

### `[noexcept] template <typename AT = T> qsizetype QList::count(const AT &value) const`

**作用与语义：**

返回列表中`value`的出现次数。
该函数要求值类型实现 `operator==()`。

### `[constexpr noexcept] qsizetype QList::count() const`

**作用与语义：**

和`size()`一样。

### `[noexcept] QList<T>::const_reverse_iterator QList::crbegin() const`

**作用与语义：**

返回一个const STL风格的反向迭代器，指向列表中的第一个项，顺序相反。
警告：返回的迭代器在分离或`QList`修改时将失效。

### `[noexcept] QList<T>::const_reverse_iterator QList::crend() const`

**作用与语义：**

返回一个const STL风格的反迭代器，指向列表中最后一个项之后，顺序相反。
警告：返回的迭代器在脱离或修改`QList`时将失效。

### `QList<T>::pointer QList::data()`

**作用与语义：**

返回一个指向列表中存储数据的指针。该指针可用于访问和修改列表中的项目。
警告：指针在分离或`QList`修改时失效。
该函数主要用于将列表传递给接受普通 C 数组的函数。

**官方示例：**

```cpp
 QList<int> list(10);
 int *data = list.data();
 for (qsizetype i = 0; i < 10; ++i)
     data[i] = 2 * i;
```

### `[noexcept] QList<T>::const_pointer QList::data() const`

**作用与语义：**

返回一个指向列表中存储数据的指针。该指针可用于访问和修改列表中的项目。
警告：指针在分离或`QList`修改时失效。
该函数主要用于将列表传递给接受普通 C 数组的函数。

**官方示例：**

```cpp
 QList<int> list(10);
 int *data = list.data();
 for (qsizetype i = 0; i < 10; ++i)
     data[i] = 2 * i;
```

### `template <typename... Args> QList<T>::iterator QList::emplace(qsizetype i, Args &&... args)`

**作用与语义：**

通过在位置`i`插入一个新元素来扩展容器。该新元素在原地构造，使用`args`作为构造的参数。
将迭代器返回新元素。
注意：可以保证元素会在起始处创建，但之后可能会被复制或移动到正确的位置。

**官方示例：**

```cpp
 QList<QString> list{"a", "ccc"};
 list.emplace(1, 2, 'b');
 // list: ["a", "bb", "ccc"]
```

### `template <typename... Args> QList<T>::iterator QList::emplace(QList<T>::const_iterator before, Args &&... args)`

**作用与语义：**

在迭代器指向的项前创建一个新元素`before`。该新元素在原位构造，使用`args`作为构造参数。
将迭代器返回新元素。

### `template <typename... Args> QList<T>::reference QList::emplace_back(Args &&... args)`

**作用与语义：**

在容器末尾添加一个新元素。该新元素原位构造，使用`args`作为其构造的参数。
返回新元素的引用。
也可以通过返回的引用访问新创建的对象：
这和 list.emplace（list.`size()`，`args`）。

**官方示例：**

```cpp
 QList<QString> list{"one", "two"};
 list.emplaceBack(3, 'a');
 qDebug() << list;
 // list: ["one", "two", "aaa"]
```

### `[noexcept] bool QList::empty() const`

**作用与语义：**

该函数是为了STL兼容性而提供。它等价于`isEmpty()`，如果列表为空，返回`true`;否则返回`false`。

### `QList<T>::iterator QList::end()`

**作用与语义：**

返回一个STL风格的迭代器，指向列表中最后一项之后。
警告：返回的迭代器在分离或`QList`修改时将失效。

### `[noexcept] QList<T>::const_iterator QList::end() const`

**作用与语义：**

返回一个STL风格的迭代器，指向列表中最后一项之后。
警告：返回的迭代器在分离或`QList`修改时将失效。

### `bool QList::endsWith(QList<T>::parameter_type value) const`

**作用与语义：**

如果该列表不是空的且其最后一项等于`value`，返回 `true`;否则返回 `false`。

### `QList<T>::iterator QList::erase(QList<T>::const_iterator pos)`

**作用与语义：**

从列表中移除迭代器`pos`指向的项，并返回迭代器到列表中的下一个项（可能是`end()`项）。
元素移除可以保留列表的容量，同时不会减少分配的内存。为了减少多余容量并释放尽可能多的内存，请调用`squeeze()`。
注意：当`QList`未被隐式共享时，该函数仅使位于指定位置或之后的迭代器失效。

### `QList<T>::iterator QList::erase(QList<T>::const_iterator begin, QList<T>::const_iterator end)`

**作用与语义：**

移除`begin`中（但不包括）`end`的所有项目。返回调用前`end`提及的同一项目的迭代器。
元素移除将保留列表容量，同时不会减少分配内存。要减少多余容量并释放尽可能多的内存，请调用`squeeze()`。
注意：当`QList`未被隐式共享时，该函数仅使处于或之后的迭代器失效。

### `QList<T> &QList::fill(QList<T>::parameter_type value, qsizetype size = -1)`

**作用与语义：**

为列表中的所有项分配`value`。如果`size`与默认值-1不同，列表会提前调整为`size`。

**官方示例：**

```cpp
 QList<QString> list(3);
 list.fill("Yes");
 // list: ["Yes", "Yes", "Yes"]

 list.fill("oh", 5);
 // list: ["oh", "oh", "oh", "oh", "oh"]
```

### `T &QList::first()`

**作用与语义：**

返回列表中第一个项目的引用。该函数假设列表不是空的。

### `[since 6.0] QList<T> QList::first(qsizetype n) const`

**作用与语义：**

返回包含该列表前`n`元素的子列表。
注意：当`n` <0或`n` > `size()`时，行为未定义。

### `[noexcept] const T &QList::first() const`

**作用与语义：**

返回列表中第一个项目的引用。该函数假设列表不是空的。

### `QList<T>::reference QList::front()`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于`first()`。

### `[noexcept] QList<T>::const_reference QList::front() const`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于`first()`。

### `[noexcept] template <typename AT> qsizetype QList::indexOf(const AT &value, qsizetype from = 0) const`

**作用与语义：**

返回列表中首次出现`value`的索引位置，从索引位置`from`向前搜索。如果没有匹配的项目，返回-1。
该函数要求值类型实现 `operator==()`。

**官方示例：**

```cpp
 QList<QString> list{"A", "B", "C", "B", "A"};
 list.indexOf("B");            // returns 1
 list.indexOf("B", 1);         // returns 1
 list.indexOf("B", 2);         // returns 3
 list.indexOf("X");            // returns -1
```

### `QList<T>::iterator QList::insert(qsizetype i, QList<T>::rvalue_ref value)`

**作用与语义：**

在列表中索引位置`i`插入`value`。如果`i`为0，则该值会被附加到列表中。如果`i` `size()`，则将该值附加到列表中。
对于大型列表，这个操作可能很慢（线性时间），因为它需要将索引`i`及以上的所有项在内存中移动一个位置。如果你想要一个提供快速 `insert()` 函数的容器类，可以使用 std：：list。

**官方示例：**

```cpp
 QList<QString> list = {"alpha", "beta", "delta"};
 list.insert(2, "gamma");
 // list: ["alpha", "beta", "gamma", "delta"]
```

### `QList<T>::iterator QList::insert(QList<T>::const_iterator before, qsizetype count, QList<T>::parameter_type value)`

**作用与语义：**

在列表中索引位置`i`插入`value`。如果`i`为0，则该值会被附加到列表中。如果`i` `size()`，则将该值附加到列表中。
对于大型列表，这个操作可能很慢（线性时间），因为它需要将索引`i`及以上的所有项在内存中移动一个位置。如果你想要一个提供快速 `insert()` 函数的容器类，可以使用 std：：list。

**官方示例：**

```cpp
 QList<QString> list = {"alpha", "beta", "delta"};
 list.insert(2, "gamma");
 // list: ["alpha", "beta", "gamma", "delta"]
```

### `QList<T>::iterator QList::insert(QList<T>::const_iterator before, QList<T>::rvalue_ref value)`

**作用与语义：**

在迭代器指向的项目前插入`count` `value`副本`before`。返回指向插入项中第一个的迭代器。

### `QList<T>::iterator QList::insert(qsizetype i, qsizetype count, QList<T>::parameter_type value)`

**作用与语义：**

插入迭代器指向的项目前方`value` `before`。返回指向插入项的迭代器。

### `[constexpr noexcept] bool QList::isEmpty() const`

**作用与语义：**

如果列表大小为0，返回`true`;否则返回`false`。

### `T &QList::last()`

**作用与语义：**

返回列表中最后一项的引用。该函数假设列表不是空的。

### `[since 6.0] QList<T> QList::last(qsizetype n) const`

**作用与语义：**

返回包含该列表最后`n`元素的子列表。
注意：当`n` <0或`n` > `size()`时，行为未定义。

### `[noexcept] const T &QList::last() const`

**作用与语义：**

返回列表中最后一项的引用。该函数假设列表不是空的。

### `[noexcept] template <typename AT> qsizetype QList::lastIndexOf(const AT &value, qsizetype from = -1) const`

**作用与语义：**

返回列表中该`value`值最后一次出现的索引位置，从索引位置`from`向后搜索。如果`from`为-1（默认值），搜索从最后一项开始。如果没有匹配的项，返回-1。
该函数要求值类型实现 `operator==()`。

**官方示例：**

```cpp
 QList<QString> list = {"A", "B", "C", "B", "A"};
 list.lastIndexOf("B");        // returns 3
 list.lastIndexOf("B", 3);     // returns 3
 list.lastIndexOf("B", 2);     // returns 1
 list.lastIndexOf("X");        // returns -1
```

### `[constexpr noexcept] qsizetype QList::length() const`

**作用与语义：**

和`size()`、`count()`一样。

### `[static constexpr, since 6.8] qsizetype QList::maxSize()`

**作用与语义：**

它返回列表理论上能容纳的最大元素数量。实际上，这个数量可以更小，受限于系统可用的内存容量。

### `QList<T> QList::mid(qsizetype pos, qsizetype length = -1) const`

**作用与语义：**

返回包含该列表中元素的子列表，从位置`pos`开始。如果`length`为-1（默认），则包含`pos`之后的所有元素;否则包含`length`元素（若元素少于`length`则包含所有剩余元素）。

### `void QList::move(qsizetype from, qsizetype to)`

**作用与语义：**

将索引位置`from`的项目移动到索引位置`to`。
`from`和`to`必须在界限内。
例如，要将第一个项目移动到列表末尾：

**官方示例：**

```cpp
 QList<int> list = {1, 2, 3};
 list.move(0, list.size() - 1);
 qDebug() << list; // Prints "QList(2, 3, 1)"
```

### `[noexcept] void QList::pop_back()`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于`removeLast()`。

### `[noexcept] void QList::pop_front()`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于`removeFirst()`。

### `void QList::prepend(QList<T>::rvalue_ref value)`

**作用与语义：**

插入`value`在列表开头。
这与 list.insert（0， `value`）相同。
通常该操作相对较快（摊销常数时间）。`QList` 可以在列表数据开头分配额外内存，并沿该方向增长，而无需每次操作重新分配或移动数据。不过，如果你想要一个保证常数时间前置的容器类，可以使用 std：：list，但更倾向于`QList`其他方式。

**官方示例：**

```cpp
 QList<QString> list;
 list.prepend("one");
 list.prepend("two");
 list.prepend("three");
 // list: ["three", "two", "one"]
```

### `void QList::push_back(QList<T>::parameter_type value)`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于append（`value`）。

### `void QList::push_back(QList<T>::rvalue_ref value)`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于append（`value`）。

### `void QList::push_front(QList<T>::rvalue_ref value)`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于prepend（`value`）。

### `QList<T>::reverse_iterator QList::rbegin()`

**作用与语义：**

返回一个STL风格的反向迭代器，指向列表中的第一个项目，顺序相反。
警告：返回的迭代器在分离或`QList`修改时将失效。

### `[noexcept] QList<T>::const_reverse_iterator QList::rbegin() const`

**作用与语义：**

返回一个STL风格的反向迭代器，指向列表中的第一个项目，顺序相反。
警告：返回的迭代器在分离或`QList`修改时将失效。

### `void QList::remove(qsizetype i, qsizetype n = 1)`

**作用与语义：**

从索引位置`i`开始移除列表中的`n`元素。
元素移除将保留列表容量，同时不会减少分配内存。要减少多余容量并释放尽可能多的内存，请调用`squeeze()`。
注意：当`QList`未被隐式共享时，该函数仅使位于指定位置或之后的迭代器失效。

### `template <typename AT = T> qsizetype QList::removeAll(const AT &t)`

**作用与语义：**

从列表中移除所有比较为`t`的元素。返回被移除的元素数量（如有）。
元素移除将保留列表容量，同时不会减少分配内存。为了减少多余容量并释放尽可能多的内存，请调用`squeeze()`。

### `void QList::removeAt(qsizetype i)`

**作用与语义：**

去除指标位置`i`的元素。等价于。
元素移除可以保留列表的容量，同时不会减少分配的内存。为了减少多余容量并释放尽可能多的内存，请调用`squeeze()`。
注意：当`QList`未被隐式共享时，该函数仅使位于指定位置或之后的迭代器失效。

**官方示例：**

```cpp
 remove(i);
```

### `[noexcept] void QList::removeFirst()`

**作用与语义：**

移除列表中的第一个项。调用该函数等同于调用 remove（0）。列表不能为空。如果列表可以为空，请在调用该函数前调用 `isEmpty()`。
元素移除可以保留列表的容量，同时不会减少分配的内存。为了减少多余容量并释放尽可能多的内存，请调用`squeeze()`。

### `[since 6.1] template <typename Predicate> qsizetype QList::removeIf(Predicate pred)`

**作用与语义：**

从列表中移除所有谓词`pred`返回为真元素的元素。返回被移除的元素数量（如有）。

### `[noexcept] void QList::removeLast()`

**作用与语义：**

移除列表中的最后一项。调用该函数等同于调用 remove（`size()` - 1）。列表不能为空。如果列表可以为空，请在调用该函数前调用 `isEmpty()`。
元素移除将保留列表容量，而不会减少分配内存。为了减少多余容量并释放尽可能多的内存，请调用`squeeze()`。

### `template <typename AT = T> bool QList::removeOne(const AT &t)`

**作用与语义：**

从列表中移除第一个与 `t` 比较的元素。返回是否确实移除了某个元素。
元素移除可以保留列表的容量，而不会减少分配的内存。要减少多余容量并释放尽可能多的内存，请调用`squeeze()`。

### `QList<T>::reverse_iterator QList::rend()`

**作用与语义：**

返回一个STL风格的反迭代器，指向列表中最后一个项目之后，顺序倒序。
警告：返回的迭代器在脱离或`QList`修改时会失效。

### `[noexcept] QList<T>::const_reverse_iterator QList::rend() const`

**作用与语义：**

返回一个STL风格的反迭代器，指向列表中最后一个项目之后，顺序倒序。
警告：返回的迭代器在脱离或`QList`修改时会失效。

### `void QList::replace(qsizetype i, QList<T>::rvalue_ref value)`

**作用与语义：**

将索引位置`i`的项目替换为`value`。
`i`必须是列表中有效的索引位置（即0 <= `i` < `size()`）。

### `void QList::reserve(qsizetype size)`

**作用与语义：**

尝试为至少`size`个元素分配内存。
如果你提前知道列表有多大，应该调用这个函数以防止重分配和内存碎片化。如果你经常调整列表大小，性能也会更好。
如果不确定需要多少空间，通常最好用上界作为 `size`，或者如果严格的上限远大于这个，则使用最可能规模的较高估计值。如果`size`是低估，一旦超过预留容量，列表会根据需要增长，这可能导致分配比最佳高估更大，并减缓触发该情况的操作。
警告：reserve() 保留内存，但不改变列表大小。访问列表当前端以外的数据属于未定义行为。如果你需要访问列表当前端以外的内存，请使用 `resize()`。

### `[since 6.0] void QList::resize(qsizetype size, QList<T>::parameter_type c)`

**作用与语义：**

将列表大小设置为`size`。如果`size`大于当前大小，则将元素添加到末尾;新元素以默认构造值或`c`初始化。如果`size`小于当前大小，则从末尾移除元素。
如果该列表未被共享，`capacity()`将被保留。利用`squeeze()`来减少多余容量。
注意：在 5.7 之前的 Qt 版本中（针对 `QVector`;`QList` 直到 6.0 才有`resize()`），该功能释放了列表所使用的内存，而不是保留容量。

### `[since 6.8] void QList::resizeForOverwrite(qsizetype size)`

**作用与语义：**

将列表大小设置为`size`。如果`size`小于当前大小，则从末尾移除元素。如果`size`大于当前大小，则在末尾添加元素;`QList`会尝试不初始化这些新元素。
具体来说：
- 如果`T`有一个接受`Qt::Uninitialized`的构造函数，则该构造函数将用于初始化元素;
- 否则，每个元素都是默认构造的。对于平凡可构造类型（如`int`、`float`等），这等同于不初始化它们。

### `void QList::shrink_to_fit()`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于`squeeze()`。

### `[constexpr noexcept] qsizetype QList::size() const`

**作用与语义：**

返回列表中的项目数量。

### `[since 6.0] QList<T> QList::sliced(qsizetype pos, qsizetype n) const`

**作用与语义：**

返回包含该列表的`n`元素的子列表，从位置`pos`开始。
注意：当`pos` <0、`n` <0或`pos` `n` > `size()`时，行为未定义。

### `[since 6.0] QList<T> QList::sliced(qsizetype pos) const`

**作用与语义：**

返回一个子列表，包含该列表从位置`pos`开始一直延伸到末尾的元素。
注意：当`pos` <0或`pos` > `size()`时，行为未定义。

### `void QList::squeeze()`

**作用与语义：**

释放存储物品所需的存储。
该函数的唯一目的是提供一种微调`QList`内存使用的方法。一般来说，你很少需要调用这个函数。

### `bool QList::startsWith(QList<T>::parameter_type value) const`

**作用与语义：**

如果该列表不是空的，且其第一个项等于`value`，返回 `true`;否则返回 `false`。

### `[noexcept] void QList::swap(QList<T> &other)`

**作用与语义：**

将这个列表与`other`交换。这个操作非常快，而且从未失败过。

### `void QList::swapItemsAt(qsizetype i, qsizetype j)`

**作用与语义：**

将索引位置`i`的项与索引位置`j`的项交换。该函数假设`i`和`j`都至少为0但小于`size()`。为避免失败，测试`i`和`j`都至少为0且小于`size()`。

### `T QList::takeAt(qsizetype i)`

**作用与语义：**

移除索引位置的元素`i`并返回。
等价于。
注意：当`QList`未隐式共享时，该函数仅使在指定位置或之后的迭代器失效。

**官方示例：**

```cpp
 T t = at(i);
 remove(i);
 return t;
```

### `QList<T>::value_type QList::takeFirst()`

**作用与语义：**

移除列表中的第一个项并返回它。该函数假设列表不是空的。为避免失败，先调用 `isEmpty()` 再调用该函数。

### `QList<T>::value_type QList::takeLast()`

**作用与语义：**

移除列表中的最后一项并返回。该函数假设列表不是空的。为避免失败，调用 `isEmpty()` 再调用该函数。
如果不使用返回值，`removeLast()`更高效。

### `T QList::value(qsizetype i) const`

**作用与语义：**

返回列表中索引位置`i`的值。
如果索引`i`超出边界，函数返回默认构造值。如果你确定`i`在边界内，可以用`at()`，速度稍快。

### `T QList::value(qsizetype i, QList<T>::parameter_type defaultValue) const`

**作用与语义：**

如果索引`i`超出边界，函数返回`defaultValue`。

### `bool QList::operator!=(const QList<T> &other) const`

**作用与语义：**

如果`other`不等于该列表，返回`true`;否则返回`false`。
如果两个列表包含相同值且顺序相同，则视为相等。
该函数要求值类型实现 `operator==()`。

### `QList<T> QList::operator+(QList<T> &&other) &&`

**作用与语义：**

返回包含该列表中所有项目的列表，后面是`other`列表中的所有项目。

### `QList<T> &QList::operator+=(const QList<T> &other)`

**作用与语义：**

将`other`列表的项目附加到该列表，并返回该列表的引用。

### `[since 6.0] QList<T> &QList::operator+=(QList<T> &&other)`

**作用与语义：**

将`other`列表的项目附加到该列表，并返回该列表的引用。

### `QList<T> &QList::operator+=(QList<T>::parameter_type value)`

**作用与语义：**

附`value`到列表中。

### `QList<T> &QList::operator+=(QList<T>::rvalue_ref value)`

**作用与语义：**

将`other`列表的项目附加到该列表，并返回该列表的引用。

### `bool QList::operator<(const QList<T> &other) const`

**作用与语义：**

如果该列表词汇小于`other`，返回`true`;否则返回`false`。
该函数要求值类型实现 `operator<()`。

### `QList<T> &QList::operator<<(QList<T>::parameter_type value)`

**作用与语义：**

将`value`附加到列表中并返回该列表的引用。

### `QList<T> &QList::operator<<(const QList<T> &other)`

**作用与语义：**

在列表中附加`other`并返回对列表的引用。

### `[since 6.0] QList<T> &QList::operator<<(QList<T> &&other)`

**作用与语义：**

将`value`附加到列表中并返回该列表的引用。

### `QList<T> &QList::operator<<(QList<T>::rvalue_ref value)`

**作用与语义：**

将`value`附加到列表中并返回该列表的引用。

### `bool QList::operator<=(const QList<T> &other) const`

**作用与语义：**

如果该列表词汇大小于或等于`other`，则返回`true`;否则返回`false`。
该函数要求值类型实现 `operator<()`。

### `[default] QList<T> &QList::operator=(QList<T> &&other)`

**作用与语义：**

Move-assign `other`到该`QList`实例。

### `[default] QList<T> &QList::operator=(const QList<T> &other)`

**作用与语义：**

将`other`分配到该列表并返回该列表的引用。

### `QList<T> &QList::operator=(std::initializer_list<T> args)`

**作用与语义：**

将`args`值集合分配给该`QList`实例。

### `bool QList::operator==(const QList<T> &other) const`

**作用与语义：**

如果`other`等于该列表，返回`true`;否则返回`false`。
如果两个列表包含相同值且顺序相同，则视为相等。
该函数要求值类型具有 `operator==()` 的实现。

### `bool QList::operator>(const QList<T> &other) const`

**作用与语义：**

如果该列表词汇大于`other`，则返回`true`;否则返回`false`。
该函数要求值类型实现 `operator<()`。

### `bool QList::operator>=(const QList<T> &other) const`

**作用与语义：**

如果该列表词汇大于或等于`other`，则返回`true`;否则返回`false`。
该函数要求值类型实现 `operator<()`。

### `QList<T>::reference QList::operator[](qsizetype i)`

**作用与语义：**

返回索引位置`i`的项目作为可修改的引用。
`i` 必须是列表中有效的索引位置（即 0 <= `i` < `size()`）。
注意，使用非const操作符可能会导致`QList`进行深度复制。

### `[noexcept] QList<T>::const_reference QList::operator[](qsizetype i) const`

**作用与语义：**

和at（`i`）一样。

### `[since 6.1] template <typename T, typename AT> qsizetype erase(QList<T> &list, const AT &t)`

**作用与语义：**

从列表中移除所有与`t`相等的元素`list`。返回被移除的元素数量（如有）。
注意：与`QList::removeAll`不同，`t`不能作为`list`内部元素的引用。如果无法确定是否如此，可以复制一份`t`并调用该函数。

### `[since 6.1] template <typename T, typename Predicate> qsizetype erase_if(QList<T> &list, Predicate pred)`

**作用与语义：**

从列表中移除所有谓词 `pred` 返回为真元素`list`。返回移除的元素数量（如有）。

### `[noexcept(...)] template <typename T> size_t qHash(const QList<T> &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。
类型`T`必须由qHash()支持。
注意：该函数只有在`noexcept(qHashRange(key.cbegin(), key.cend(), seed))` `true`时才适用。

### `template <typename T> QDataStream &operator<<(QDataStream &out, const QList<T> &list)`

**作用与语义：**

写入列表`list`流`out`。
该函数需要值类型来实现`operator<<()`。

### `[since 6.9] auto operator<=>(const QList<T> &lhs, const QList<T> &rhs)`

**作用与语义：**

通过字典序比较`lhs`和`rhs`的内容。返回最强适用类别类型的结果，即如果`T`类型可用`operator<=>()`则`decltype(lhs[0] <=> rhs[0])`;否则`std::weak_ordering`。
注意：该操作符仅支持C 20模式，当底层类型`T`建模`std::three_way_comparable`概念或提供`operator<()`时。

### `template <typename T> QDataStream &operator>>(QDataStream &in, QList<T> &list)`

**作用与语义：**

从stream `in`的列表读到`list`。
该函数需要值类型来实现`operator>>()`。

### `class const_iterator`

**作用与语义：**

为QList和QStack提供STL风格的const迭代器。
`QList` 既提供了 STL 风格的迭代器，也提供 Java 风格的叠代器。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。
警告：当`QList`被修改时，迭代器将被无效。请考虑所有迭代器默认无效。该规则的例外情况有明确文档。

### `class iterator`

**作用与语义：**

为QList和QStack提供STL风格的非const迭代器。
`QList` 既提供 STL 风格的迭代器，也提供 Java 风格的叠代器。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。
警告：当`QList`被修改时，迭代器将被废止。请注意，所有迭代器默认都会被废止。该规则的例外情况有明确文档。

### `ConstIterator`

**作用与语义：**

Qt风格的`QList::const_iterator`同义词。

### `Iterator`

**作用与语义：**

Qt风格的同义词`QList::iterator`。

### `const_pointer`

**作用与语义：**

提供STL兼容性。

### `const_reference`

**作用与语义：**

提供STL兼容性。

### `const_reverse_iterator`

**作用与语义：**

QList：：const_reverse_iterator typedef 提供了一个 STL 风格的 cont 反迭代器用于 `QList`。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。
警告：当`QList`被修改时，迭代器将被无效。请考虑所有迭代器默认无效。该规则的例外情况有明确文档。

### `difference_type`

**作用与语义：**

提供STL兼容性。

### `parameter_type`

**作用与语义：**

`QList<T>` 为高效传入单个 `T` 而选择的参数类型：按元素特征可能按值传递，也可能使用 `const T &`。它主要用于泛型实现。

### `pointer`

**作用与语义：**

提供STL兼容性。

### `reference`

**作用与语义：**

提供STL兼容性。

### `reverse_iterator`

**作用与语义：**

QList：：reverse_iterator typedef 提供了一个 STL 风格的非一致性反迭代器用于 `QList`。
警告：隐式共享容器上的迭代器工作方式与STL迭代器不完全相同。当迭代器在该容器上活跃时，应避免复制该容器。欲了解更多信息，请阅读隐式共享迭代器问题。
警告：当`QList`被修改时，迭代器将被无效。请考虑所有迭代器默认无效。本规则的例外情况有明确文档。

### `rvalue_ref`

**作用与语义：**

`QList<T>` 接收可移动元素时使用的参数类型，通常对应 `T &&`；传入临时值或 `std::move(value)` 可避免不必要的复制。

### `size_type`

**作用与语义：**

提供STL兼容性。

### `value_type`

**作用与语义：**

提供STL兼容性。

### `QList<T>::reference emplaceBack(Args &&... args)`

**作用与语义：**

在容器末尾添加一个新元素。该新元素原位构造，使用`args`作为其构造的参数。
返回新元素的引用。
也可以通过返回的引用访问新创建的对象：
这和 list.emplace（list.`size()`，`args`）。

**官方示例：**

```cpp
 QList<QString> list{"one", "two"};
 list.emplaceBack(3, 'a');
 qDebug() << list;
 // list: ["one", "two", "aaa"]
```

### `QList<T>::iterator insert(qsizetype i, QList<T>::parameter_type value)`

**作用与语义：**

插入迭代器指向的项目前方`value` `before`。返回指向插入项的迭代器。

### `QList<T>::iterator insert(QList<T>::const_iterator before, QList<T>::parameter_type value)`

**作用与语义：**

在列表中索引位置`i`插入`count` `value`副本。

**官方示例：**

```cpp
 QList<double> list = {2.718, 1.442, 0.4342};
 list.insert(1, 3, 9.9);
 // list: [2.718, 9.9, 9.9, 9.9, 1.442, 0.4342]
```

### `(since 6.8) qsizetype max_size() const`

**作用与语义：**

它返回列表理论上能容纳的最大元素数量。实际上，这个数量可以更小，受限于系统可用的内存容量。

### `void prepend(QList<T>::parameter_type value)`

**作用与语义：**

插入`value`在列表开头。
这与 list.insert（0， `value`）相同。
通常该操作相对较快（摊销常数时间）。`QList` 可以在列表数据开头分配额外内存，并沿该方向增长，而无需每次操作重新分配或移动数据。不过，如果你想要一个保证常数时间前置的容器类，可以使用 std：：list，但更倾向于`QList`其他方式。

**官方示例：**

```cpp
 QList<QString> list;
 list.prepend("one");
 list.prepend("two");
 list.prepend("three");
 // list: ["three", "two", "one"]
```

### `void push_front(QList<T>::parameter_type value)`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于prepend（`value`）。

### `void replace(qsizetype i, QList<T>::parameter_type value)`

**作用与语义：**

将索引位置`i`的项目替换为`value`。
`i`必须是列表中有效的索引位置（即0 <= `i` < `size()`）。

### `(since 6.0) void resize(qsizetype size)`

**作用与语义：**

将列表大小设置为`size`。如果`size`大于当前大小，则将元素添加到末尾;新元素以默认构造值或`c`初始化。如果`size`小于当前大小，则从末尾移除元素。
如果该列表未被共享，`capacity()`将被保留。利用`squeeze()`来减少多余容量。
注意：在 5.7 之前的 Qt 版本中（针对 `QVector`;`QList` 直到 6.0 才有`resize()`），该功能释放了列表所使用的内存，而不是保留容量。

### `QList<T> operator+(const QList<T> &other) &&`

**作用与语义：**

返回包含该列表中所有项目的列表，后面是`other`列表中的所有项目。

### `QList<T> operator+(QList<T> &&other) const &`

**作用与语义：**

返回包含该列表中所有项目的列表，后面是`other`列表中的所有项目。

### `QList<T> operator+(const QList<T> &other) const &`

**作用与语义：**

返回包含该列表中所有项目的列表，后面是`other`列表中的所有项目。

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

`QList` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
