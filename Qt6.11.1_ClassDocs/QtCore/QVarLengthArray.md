# QVarLengthArray

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QVarLengthArray` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QVarLengthArray` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QVarLengthArray>`
- 继承自：QVLABase、QVLAStorage
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

- `const_iterator`
- `const_pointer`
- `const_reference`
- `const_reverse_iterator`
- `difference_type`
- `iterator`
- `pointer`
- `reference`
- `reverse_iterator`
- `size_type`
- `value_type`

### 公有函数

- `QVarLengthArray()`
- `QVarLengthArray(qsizetype size)`
- `QVarLengthArray(std::initializer_list<T> args)`
- `QVarLengthArray(InputIterator first, InputIterator last)`
- `(since 6.4) QVarLengthArray(qsizetype size, const T &v)`
- `QVarLengthArray(const QVarLengthArray<T, Prealloc> &other)`
- `(since 6.0) QVarLengthArray(QVarLengthArray<T, Prealloc> &&other)`
- `~QVarLengthArray()`
- `void append(const T &t)`
- `void append(const T *buf, qsizetype size)`
- `void append(T &&t)`
- `(since 6.6) QVarLengthArray<T, Prealloc> & assign(std::initializer_list<T> list)`
- `(since 6.6) QVarLengthArray<T, Prealloc> & assign(InputIterator first, InputIterator last)`
- `(since 6.6) QVarLengthArray<T, Prealloc> & assign(qsizetype n, const T &t)`
- `const T & at(qsizetype i) const`
- `T & back()`
- `const T & back() const`
- `QVarLengthArray<T, Prealloc>::iterator begin()`
- `QVarLengthArray<T, Prealloc>::const_iterator begin() const`
- `qsizetype capacity() const`
- `QVarLengthArray<T, Prealloc>::const_iterator cbegin() const`
- `QVarLengthArray<T, Prealloc>::const_iterator cend() const`
- `void clear()`
- `QVarLengthArray<T, Prealloc>::const_iterator constBegin() const`
- `const T * constData() const`
- `QVarLengthArray<T, Prealloc>::const_iterator constEnd() const`
- `bool contains(const AT &value) const`
- `qsizetype count() const`
- `QVarLengthArray<T, Prealloc>::const_reverse_iterator crbegin() const`
- `QVarLengthArray<T, Prealloc>::const_reverse_iterator crend() const`
- `T * data()`
- `const T * data() const`
- `(since 6.3) QVarLengthArray<T, Prealloc>::iterator emplace(QVarLengthArray<T, Prealloc>::const_iterator pos, Args &&... args)`
- `(since 6.3) T & emplace_back(Args &&... args)`
- `bool empty() const`
- `QVarLengthArray<T, Prealloc>::iterator end()`
- `QVarLengthArray<T, Prealloc>::const_iterator end() const`
- `QVarLengthArray<T, Prealloc>::iterator erase(QVarLengthArray<T, Prealloc>::const_iterator pos)`
- `QVarLengthArray<T, Prealloc>::iterator erase(QVarLengthArray<T, Prealloc>::const_iterator begin, QVarLengthArray<T, Prealloc>::const_iterator end)`
- `T & first()`
- `const T & first() const`
- `T & front()`
- `const T & front() const`
- `qsizetype indexOf(const AT &value, qsizetype from = 0) const`
- `void insert(qsizetype i, T &&value)`
- `void insert(qsizetype i, const T &value)`
- `QVarLengthArray<T, Prealloc>::iterator insert(QVarLengthArray<T, Prealloc>::const_iterator before, qsizetype count, const T &value)`
- `QVarLengthArray<T, Prealloc>::iterator insert(QVarLengthArray<T, Prealloc>::const_iterator before, T &&value)`
- `QVarLengthArray<T, Prealloc>::iterator insert(QVarLengthArray<T, Prealloc>::const_iterator before, const T &value)`
- `void insert(qsizetype i, qsizetype count, const T &value)`
- `bool isEmpty() const`
- `T & last()`
- `const T & last() const`
- `qsizetype lastIndexOf(const AT &value, qsizetype from = -1) const`
- `qsizetype length() const`
- `(since 6.8) qsizetype max_size() const`
- `void pop_back()`
- `void push_back(const T &t)`
- `void push_back(T &&t)`
- `QVarLengthArray<T, Prealloc>::reverse_iterator rbegin()`
- `QVarLengthArray<T, Prealloc>::const_reverse_iterator rbegin() const`
- `void remove(qsizetype i, qsizetype count = 1)`
- `(since 6.1) qsizetype removeAll(const AT &t)`
- `(since 6.1) qsizetype removeIf(Predicate pred)`
- `void removeLast()`
- `(since 6.1) bool removeOne(const AT &t)`
- `QVarLengthArray<T, Prealloc>::reverse_iterator rend()`
- `QVarLengthArray<T, Prealloc>::const_reverse_iterator rend() const`
- `void replace(qsizetype i, const T &value)`
- `void reserve(qsizetype size)`
- `void resize(qsizetype size)`
- `(since 6.4) void resize(qsizetype size, const T &v)`
- `void shrink_to_fit()`
- `qsizetype size() const`
- `void squeeze()`
- `T value(qsizetype i) const`
- `T value(qsizetype i, const T &defaultValue) const`
- `QVarLengthArray<T, Prealloc> & operator+=(const T &value)`
- `QVarLengthArray<T, Prealloc> & operator+=(T &&value)`
- `QVarLengthArray<T, Prealloc> & operator<<(const T &value)`
- `QVarLengthArray<T, Prealloc> & operator<<(T &&value)`
- `(since 6.0) QVarLengthArray<T, Prealloc> & operator=(QVarLengthArray<T, Prealloc> &&other)`
- `QVarLengthArray<T, Prealloc> & operator=(const QVarLengthArray<T, Prealloc> &other)`
- `QVarLengthArray<T, Prealloc> & operator=(std::initializer_list<T> list)`
- `T & operator[](qsizetype i)`
- `const T & operator[](qsizetype i) const`

### 静态公有成员

- `(since 6.8) qsizetype maxSize()`

### 相关非成员函数

- `(since 6.1) qsizetype erase(QVarLengthArray<T, Prealloc> &array, const AT &t)`
- `(since 6.1) qsizetype erase_if(QVarLengthArray<T, Prealloc> &array, Predicate pred)`
- `size_t qHash(const QVarLengthArray<T, Prealloc> &key, size_t seed = 0)`
- `bool operator!=(const QVarLengthArray<T, Prealloc1> &left, const QVarLengthArray<T, Prealloc2> &right)`
- `bool operator<(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`
- `bool operator<=(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`
- `bool operator==(const QVarLengthArray<T, Prealloc1> &left, const QVarLengthArray<T, Prealloc2> &right)`
- `bool operator>(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`
- `bool operator>=(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QVarLengthArray::const_iterator`

**作用与语义：**

Typedef 表示 const T *。提供以兼容 STL 的。

### `[alias] QVarLengthArray::const_pointer`

**作用与语义：**

Typedef 表示 const T *。提供以兼容 STL 的。

### `[alias] QVarLengthArray::const_reference`

**作用与语义：**

Typedef 用于 const T 和。为 STL 兼容性提供。

### `[alias] QVarLengthArray::const_reverse_iterator`

**作用与语义：**

Typedef 用于`std::reverse_iterator<const T*>`。提供 STL 兼容性。

### `[alias] QVarLengthArray::difference_type`

**作用与语义：**

Typedef 用于ptrdiff_t。提供 STL 兼容性。

### `[alias] QVarLengthArray::iterator`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `[alias] QVarLengthArray::pointer`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `[alias] QVarLengthArray::reference`

**作用与语义：**

T和的Typedef。提供STL兼容性。

### `[alias] QVarLengthArray::reverse_iterator`

**作用与语义：**

Typedef 用于`std::reverse_iterator<T*>`。提供支持 STL 兼容性。

### `[alias] QVarLengthArray::size_type`

**作用与语义：**

类型定义用于国际语言。提供支持STL兼容性。

### `[alias] QVarLengthArray::value_type`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `[noexcept] QVarLengthArray::QVarLengthArray()`

**作用与语义：**

构造一个初始大小为零的数组。

### `[explicit] QVarLengthArray::QVarLengthArray(qsizetype size)`

**作用与语义：**

构造初始大小为`size`元素的数组。
如果值类型是原始类型（例如 char、int、float）或指针类型（例如 `QWidget` *），则元素不会被初始化。对于其他类型，元素会以默认构造值初始化。

### `QVarLengthArray::QVarLengthArray(std::initializer_list<T> args)`

**作用与语义：**

从 std：：initializer_list 由 `args` 给出的数组构造。

### `template <typename InputIterator, QVarLengthArray<T, Prealloc>::if_input_iterator<InputIterator> = true> QVarLengthArray::QVarLengthArray(InputIterator first, InputIterator last)`

**作用与语义：**

构造一个包含迭代子范围内容的数组 [`first`， `last`）。
`InputIterator`的价值类型必须可转换为`T`。
只有当`InputIterator`满足LegacyInputIterator的要求时，才参与超载解析。

### `[explicit, since 6.4] QVarLengthArray::QVarLengthArray(qsizetype size, const T &v)`

**作用与语义：**

构造一个初始大小为`size`元素的数组，填充包含`v`的副本。
注意：该构造器仅在`T`可复制构造时可用。

### `QVarLengthArray::QVarLengthArray(const QVarLengthArray<T, Prealloc> &other)`

**作用与语义：**

复制了`other`。

### `[noexcept(...), since 6.0] QVarLengthArray::QVarLengthArray(QVarLengthArray<T, Prealloc> &&other)`

**作用与语义：**

移动从`other`构造出这个可变长度数组。移动后，`other`为空。
注意：该功能仅在`std::is_nothrow_move_constructible_v<T>` `true`时才适用。

### `QVarLengthArray::~QVarLengthArray()`

**作用与语义：**

摧毁阵列。

### `void QVarLengthArray::append(const T &t)`

**作用与语义：**

将项`t`附加到数组中，必要时扩展数组。

### `void QVarLengthArray::append(const T *buf, qsizetype size)`

**作用与语义：**

`size` `buf` 引用的项目数量附加到该数组中。

### `void QVarLengthArray::append(T &&t)`

**作用与语义：**

注意：与 append（ 的 lvalue 超载不同），传递已是 `*this` 元素的对象的引用会导致行为未定义：
注意：该功能会让`QVarLengthArray::append`重载。

**官方示例：**

```cpp
 vla.append(std::move(vla[0])); // BUG: passing an object that is already in the container
```

### `[since 6.6] QVarLengthArray<T, Prealloc> &QVarLengthArray::assign(std::initializer_list<T> list)`

**作用与语义：**

用 `list` 元素的副本替换了这个容器里的内容。
该容器的大小将等于`list`中元素的数量。
该函数仅在`list`中的元素数量超过容器容量时分配内存。

### `[since 6.6] template <typename InputIterator, QVarLengthArray<T, Prealloc>::if_input_iterator<InputIterator> = true> QVarLengthArray<T, Prealloc> &QVarLengthArray::assign(InputIterator first, InputIterator last)`

**作用与语义：**

用迭代范围内元素的副本替换该容器的内容 [`first`， `last`）。
该容器的大小将等于该区间的元素数 [`first`， `last`）。该函数仅在该区间的元素数量超过容器容量时分配内存。
如果任一参数是对*这个的迭代子，则该行为是未定义的。
只有当`InputIterator`满足LegacyInputIterator的要求时，才参与重载决议。

### `[since 6.6] QVarLengthArray<T, Prealloc> &QVarLengthArray::assign(qsizetype n, const T &t)`

**作用与语义：**

用`n`份`t`的副本替换了该容器的内容。
该容器的大小将等于`n`。该函数仅在内存`n`超过容器容量时分配内存。

### `const T &QVarLengthArray::at(qsizetype i) const`

**作用与语义：**

返回索引位置`i`的项目引用。
`i` 必须是数组中的有效索引位置（即 0 <= `i` < `size()`）。

### `T &QVarLengthArray::back()`

**作用与语义：**

和`last()`一样。提供STL兼容性。

### `const T &QVarLengthArray::back() const`

**作用与语义：**

和`last()`一样。提供STL兼容性。

### `QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::begin()`

**作用与语义：**

返回一个STL风格的迭代器，指向数组中的第一个项。

### `QVarLengthArray<T, Prealloc>::const_iterator QVarLengthArray::begin() const`

**作用与语义：**

返回一个STL风格的迭代器，指向数组中的第一个项。

### `qsizetype QVarLengthArray::capacity() const`

**作用与语义：**

返回数组中可在不强制重分配的情况下存储的最大元素数量。
该函数的唯一目的是提供一种微调`QVarLengthArray`内存使用的方法。一般来说，你很少需要调用这个函数。如果你想知道数组中有多少项，可以调用`size()`。

### `QVarLengthArray<T, Prealloc>::const_iterator QVarLengthArray::cbegin() const`

**作用与语义：**

返回一个const型STL风格的迭代器，指向数组中的第一个项。

### `QVarLengthArray<T, Prealloc>::const_iterator QVarLengthArray::cend() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向数组最后一个项之后的虚数项。

### `void QVarLengthArray::clear()`

**作用与语义：**

从数组中移除所有元素。
和resize（0）一样。

### `QVarLengthArray<T, Prealloc>::const_iterator QVarLengthArray::constBegin() const`

**作用与语义：**

返回一个const型STL风格的迭代器，指向数组中的第一个项。

### `const T *QVarLengthArray::constData() const`

**作用与语义：**

返回一个指向数组中存储数据的const指针。该指针可用于访问数组中的项目。只要数组未被重新分配，指针依然有效。
该函数主要用于将数组传递给接受普通 C 数组的函数。

### `QVarLengthArray<T, Prealloc>::const_iterator QVarLengthArray::constEnd() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向数组最后一个项之后的虚数项。

### `template <typename AT = T> bool QVarLengthArray::contains(const AT &value) const`

**作用与语义：**

如果数组中包含 `value` 的出现，返回 `true`;否则返回 `false`。
该函数要求值类型实现 `operator==()`。

### `qsizetype QVarLengthArray::count() const`

**作用与语义：**

和`size()`一样。

### `QVarLengthArray<T, Prealloc>::const_reverse_iterator QVarLengthArray::crbegin() const`

**作用与语义：**

返回一个const STL风格的反迭代器，指向可变长度数组中的第一个项，顺序相反。

### `QVarLengthArray<T, Prealloc>::const_reverse_iterator QVarLengthArray::crend() const`

**作用与语义：**

返回一个const型STL风格的反迭代器，指向变量长度数组中最后一个项之后的迭代器，顺序相反。

### `T *QVarLengthArray::data()`

**作用与语义：**

返回数组中存储的数据指针。该指针可用于访问和修改数组中的项。
只要数组没有被重新分配，指针依然有效。
该函数主要用于将数组传递给接受普通 C 数组的函数。

**官方示例：**

```cpp
 QVarLengthArray<int> array(10);
 int *data = array.data();
 for (int i = 0; i < 10; ++i)
     data[i] = 2 * i;
```

### `const T *QVarLengthArray::data() const`

**作用与语义：**

返回数组中存储的数据指针。该指针可用于访问和修改数组中的项。
只要数组没有被重新分配，指针依然有效。
该函数主要用于将数组传递给接受普通 C 数组的函数。

**官方示例：**

```cpp
 QVarLengthArray<int> array(10);
 int *data = array.data();
 for (int i = 0; i < 10; ++i)
     data[i] = 2 * i;
```

### `[since 6.3] template <typename... Args> QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::emplace(QVarLengthArray<T, Prealloc>::const_iterator pos, Args &&... args)`

**作用与语义：**

在迭代器指向的对象前插入一个项，`pos`，`args`传递给其构造器。
返回一个迭代器，指向已放置的物品。

### `[since 6.3] template <typename... Args> T &QVarLengthArray::emplace_back(Args &&... args)`

**作用与语义：**

在该`QVarLengthArray`的后部插入一个项，`args`传递给其构造函数。
返回对已放置物品的引用。

### `bool QVarLengthArray::empty() const`

**作用与语义：**

如果数组大小为0，返回`true`;否则返回`false`。
和`isEmpty()`一样。提供STL兼容性。

### `QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::end()`

**作用与语义：**

返回一个STL风格的迭代器，指向数组最后一个项之后的虚数项。

### `QVarLengthArray<T, Prealloc>::const_iterator QVarLengthArray::end() const`

**作用与语义：**

返回一个STL风格的迭代器，指向数组最后一个项之后的虚数项。

### `QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::erase(QVarLengthArray<T, Prealloc>::const_iterator pos)`

**作用与语义：**

从向量中移除迭代器`pos`指向的项，返回向量中下一个项（可能是`end()`）的迭代器。

### `QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::erase(QVarLengthArray<T, Prealloc>::const_iterator begin, QVarLengthArray<T, Prealloc>::const_iterator end)`

**作用与语义：**

移除`begin`中所有至（但不包括）`end`项。返回调用前`end`提及的同一项的迭代器。

### `T &QVarLengthArray::first()`

**作用与语义：**

返回数组中第一个项的引用。数组不得为空。如果数组可以为空，调用该函数前请检查`isEmpty()`。

### `const T &QVarLengthArray::first() const`

**作用与语义：**

返回数组中第一个项的引用。数组不得为空。如果数组可以为空，调用该函数前请检查`isEmpty()`。

### `T &QVarLengthArray::front()`

**作用与语义：**

和`first()`一样。提供STL兼容性。

### `const T &QVarLengthArray::front() const`

**作用与语义：**

和`first()`一样。提供STL兼容性。

### `template <typename AT = T> qsizetype QVarLengthArray::indexOf(const AT &value, qsizetype from = 0) const`

**作用与语义：**

返回数组中首次出现`value`的索引位置，从索引位置`from`向前搜索。如果没有匹配的项，返回-1。
该函数要求值类型实现 `operator==()`。

### `void QVarLengthArray::insert(qsizetype i, T &&value)`

**作用与语义：**

在数组中索引位置`i`插入`value`。如果`i`为0，则在向量前加上该值。如果`i`为`size()`，则将该值附加到向量后。
对于大型数组，这个操作可能很慢（线性时间），因为它需要将索引`i`及以上的所有项在内存中移动一个位置。如果你想要一个能快速实现`insert()`函数的容器类，可以用 std：：list 代替。

### `QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::insert(QVarLengthArray<T, Prealloc>::const_iterator before, qsizetype count, const T &value)`

**作用与语义：**

在数组中索引位置`i`插入`value`。如果`i`为0，则在向量前加上该值。如果`i`为`size()`，则将该值附加到向量后。
对于大型数组，这个操作可能很慢（线性时间），因为它需要将索引`i`及以上的所有项在内存中移动一个位置。如果你想要一个能快速实现`insert()`函数的容器类，可以用 std：：list 代替。

### `QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::insert(QVarLengthArray<T, Prealloc>::const_iterator before, T &&value)`

**作用与语义：**

在迭代器指向的项目前插入`count` `value`副本`before`。返回指向插入项中第一个的迭代器。

### `void QVarLengthArray::insert(qsizetype i, qsizetype count, const T &value)`

**作用与语义：**

插入迭代器指向的项目前方`value` `before`。返回指向插入项的迭代器。

### `bool QVarLengthArray::isEmpty() const`

**作用与语义：**

如果数组大小为0，返回`true`;否则返回`false`。

### `T &QVarLengthArray::last()`

**作用与语义：**

返回数组中最后一个项的引用。数组不得为空。如果数组可以为空，调用该函数前请检查`isEmpty()`。

### `const T &QVarLengthArray::last() const`

**作用与语义：**

返回数组中最后一个项的引用。数组不得为空。如果数组可以为空，调用该函数前请检查`isEmpty()`。

### `template <typename AT = T> qsizetype QVarLengthArray::lastIndexOf(const AT &value, qsizetype from = -1) const`

**作用与语义：**

返回数组中值`value`最后一次出现的索引位置，从索引位置`from`回溯搜索。如果`from`为-1（默认值），搜索从最后一项开始。如果没有匹配的项，返回-1。
该函数要求值类型实现 `operator==()`。

### `qsizetype QVarLengthArray::length() const`

**作用与语义：**

和`size()`一样。

### `[static constexpr noexcept, since 6.8] qsizetype QVarLengthArray::maxSize()`

**作用与语义：**

它返回数组理论上能容纳的最大元素数。实际上，这个数量可以更小，受限于系统可用的内存容量。

### `void QVarLengthArray::pop_back()`

**作用与语义：**

和`removeLast()`一样。提供STL兼容性。

### `void QVarLengthArray::push_back(const T &t)`

**作用与语义：**

将项`t`附加到数组中，必要时扩展数组。提供STL兼容性。

### `void QVarLengthArray::push_back(T &&t)`

**作用与语义：**

注意：与 push_back() 的 lvalue 超载不同，传递对已是 `*this` 元素的对象的引用会导致行为未定义：
注意：该功能会让`QVarLengthArray::push_back`重载。

**官方示例：**

```cpp
 vla.push_back(std::move(vla[0])); // BUG: passing an object that is already in the container
```

### `QVarLengthArray<T, Prealloc>::reverse_iterator QVarLengthArray::rbegin()`

**作用与语义：**

返回一个STL风格的反向迭代器，指向可变长度数组中的第一个项，顺序相反。

### `QVarLengthArray<T, Prealloc>::const_reverse_iterator QVarLengthArray::rbegin() const`

**作用与语义：**

返回一个STL风格的反向迭代器，指向可变长度数组中的第一个项，顺序相反。

### `void QVarLengthArray::remove(qsizetype i, qsizetype count = 1)`

**作用与语义：**

从索引位置`i`开始移除数组中的`count`元素。
`i` 必须是数组中的有效索引位置（即 0 <= `i` < `size()`）。`count` 必须是 <= `size()` - `i`。`i` == 如果 `count` == 0，则允许 `size()`。

### `[since 6.1] template <typename AT = T> qsizetype QVarLengthArray::removeAll(const AT &t)`

**作用与语义：**

从数组中移除所有与`t`相等的元素。返回移除的元素数量（如有）。

### `[since 6.1] template <typename Predicate> qsizetype QVarLengthArray::removeIf(Predicate pred)`

**作用与语义：**

从数组中移除所有谓词 `pred` 返回为真元素。返回被移除的元素数量（如有）。

### `void QVarLengthArray::removeLast()`

**作用与语义：**

将数组大小减少一。分配的大小不变。

### `[since 6.1] template <typename AT = T> bool QVarLengthArray::removeOne(const AT &t)`

**作用与语义：**

从数组中移除第一个与 `t` 比较的元素。返回是否确实移除了某个元素。

### `QVarLengthArray<T, Prealloc>::reverse_iterator QVarLengthArray::rend()`

**作用与语义：**

返回一个STL风格的反向迭代器，指向变长数组中最后一个项之后的迭代器，顺序相反。

### `QVarLengthArray<T, Prealloc>::const_reverse_iterator QVarLengthArray::rend() const`

**作用与语义：**

返回一个STL风格的反向迭代器，指向变长数组中最后一个项之后的迭代器，顺序相反。

### `void QVarLengthArray::replace(qsizetype i, const T &value)`

**作用与语义：**

将指数位置`i`的项目替换为`value`。
`i` 必须是数组中的有效索引位置（即 0 <= `i` < `size()`）。

### `void QVarLengthArray::reserve(qsizetype size)`

**作用与语义：**

尝试为至少`size`个元素分配内存。如果你提前知道数组能扩展到多大，就可以调用这个函数，频繁调用`resize()`，性能可能会更好。如果`size`低估，最坏的情况也不过是`QVarLengthArray`会稍微慢一点。
该函数的唯一目的是提供一种微调`QVarLengthArray`内存使用的方法。一般来说，你很少需要调用这个函数。如果你想更改数组大小，可以调用`resize()`。

### `void QVarLengthArray::resize(qsizetype size)`

**作用与语义：**

将数组大小设置为`size`。如果`size`大于当前大小，则在末尾添加元素。如果`size`小于当前大小，则从末尾移除元素。
如果值类型是原始类型（例如 char， int， float）或指针类型（例如 `QWidget` *），则新元素不会被初始化。对于其他类型，元素会以默认构造的值初始化。

### `[since 6.4] void QVarLengthArray::resize(qsizetype size, const T &v)`

**作用与语义：**

将数组大小设置为`size`。如果`size`大于当前大小，则在末尾添加`v`的副本。如果`size`小于当前大小，则从末端移除元素。
注意：该函数仅在`T`可复制构造时可用。

### `void QVarLengthArray::shrink_to_fit()`

**作用与语义：**

和`squeeze()`一样。提供支持STL兼容性。

### `qsizetype QVarLengthArray::size() const`

**作用与语义：**

返回数组中的元素数量。

### `void QVarLengthArray::squeeze()`

**作用与语义：**

释放所有不需要存储这些物品的内存。如果容器能将其存储空间放入栈分配，它会释放堆分配并将元素复制回栈。
该函数的唯一目的是提供一种微调`QVarLengthArray`内存使用的方法。一般来说，你很少需要调用这个函数。

### `T QVarLengthArray::value(qsizetype i) const`

**作用与语义：**

返回指数位置`i`的值。
如果索引`i`超出边界，函数返回默认构造值。如果你确定`i`在边界内，可以用`at()`，速度稍快。

### `T QVarLengthArray::value(qsizetype i, const T &defaultValue) const`

**作用与语义：**

如果索引`i`超出边界，函数返回`defaultValue`。

### `QVarLengthArray<T, Prealloc> &QVarLengthArray::operator+=(const T &value)`

**作用与语义：**

将`value`附加到数组中，返回对该向量的引用。

### `QVarLengthArray<T, Prealloc> &QVarLengthArray::operator+=(T &&value)`

**作用与语义：**

将`value`附加到数组中，返回对该向量的引用。

### `QVarLengthArray<T, Prealloc> &QVarLengthArray::operator<<(const T &value)`

**作用与语义：**

将`value`附加到数组中，返回对该向量的引用。

### `QVarLengthArray<T, Prealloc> &QVarLengthArray::operator<<(T &&value)`

**作用与语义：**

将`value`附加到数组中，返回对该向量的引用。

### `[noexcept(...), since 6.0] QVarLengthArray<T, Prealloc> &QVarLengthArray::operator=(QVarLengthArray<T, Prealloc> &&other)`

**作用与语义：**

移动将`other`分配到该数组，并返回对该数组的引用。移动后，`other`为空。
注意：该函数仅在`std::is_nothrow_move_constructible_v<T>` `true`时才适用。

### `QVarLengthArray<T, Prealloc> &QVarLengthArray::operator=(const QVarLengthArray<T, Prealloc> &other)`

**作用与语义：**

将`other`分配到该数组，并返回对该数组的引用。

### `QVarLengthArray<T, Prealloc> &QVarLengthArray::operator=(std::initializer_list<T> list)`

**作用与语义：**

将 `list` 的值分配到该数组，并返回对该数组的引用。

### `T &QVarLengthArray::operator[](qsizetype i)`

**作用与语义：**

返回索引位置`i`的项目引用。
`i` 必须是数组中的有效索引位置（即 0 <= `i` < `size()`）。

### `const T &QVarLengthArray::operator[](qsizetype i) const`

**作用与语义：**

返回索引位置`i`的项目引用。
`i` 必须是数组中的有效索引位置（即 0 <= `i` < `size()`）。

### `[since 6.1] template < typename T, qsizetype Prealloc, typename AT > qsizetype erase(QVarLengthArray<T, Prealloc> &array, const AT &t)`

**作用与语义：**

从数组中移除所有与`t`相等的元素`array`。返回移除的元素数量（如有）。
注意：`t` 不允许作为 `array` 内部元素的引用。如果无法确定不是这样，可以复制一份 `t`，并用该副本调用该函数。

### `[since 6.1] template < typename T, qsizetype Prealloc, typename Predicate > qsizetype erase_if(QVarLengthArray<T, Prealloc> &array, Predicate pred)`

**作用与语义：**

从列表中移除所有谓词 `pred` 返回为真元素`array`。返回移除的元素数量（如有）。

### `[noexcept(...)] template <typename T, qsizetype Prealloc> size_t qHash(const QVarLengthArray<T, Prealloc> &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。
类型`T`必须由qHash()支持。
注意：该函数仅在`QtPrivate::QNothrowHashable_v<T>` `true`时才使用。

### `template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool operator!=(const QVarLengthArray<T, Prealloc1> &left, const QVarLengthArray<T, Prealloc2> &right)`

**作用与语义：**

如果两个数组（由`left`和`right`指定）不相等，返回 `true`。
如果两个数组包含相同且顺序相同的数值，则它们被视为相等。
该函数要求值类型实现 `operator==()`。

### `template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool operator<(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`

**作用与语义：**

如果可变长度数组`lhs`字典序小于`rhs`，返回`true`;否则返回`false`。
该函数要求值类型实现 `operator<()`。

### `template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool operator<=(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`

**作用与语义：**

如果可变长度数组`lhs`字典序上小于或等于`rhs`，返回`true`;否则返回`false`。
该函数要求值类型实现 `operator<()`。

### `template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool operator==(const QVarLengthArray<T, Prealloc1> &left, const QVarLengthArray<T, Prealloc2> &right)`

**作用与语义：**

如果两个数组相等，返回`true`，分别由`left`和`right`指定。
如果两个数组包含相同且顺序相同的数值，则它们被视为相等。
该函数要求值类型实现 `operator==()`。

### `template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool operator>(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`

**作用与语义：**

如果变长数组`lhs`字典序大于`rhs`，返回`true`;否则返回`false`。
该函数要求值类型实现 `operator<()`。

### `template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool operator>=(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`

**作用与语义：**

如果可变长度数组 `lhs` 在字典序上大于或等于 `rhs`，返回 `true`;否则返回 `false`。
该函数要求值类型实现 `operator<()`。

### `const_iterator`

**作用与语义：**

Typedef 表示 const T *。提供以兼容 STL 的。

### `const_pointer`

**作用与语义：**

Typedef 表示 const T *。提供以兼容 STL 的。

### `const_reference`

**作用与语义：**

Typedef 用于 const T 和。为 STL 兼容性提供。

### `const_reverse_iterator`

**作用与语义：**

Typedef 用于`std::reverse_iterator<const T*>`。提供 STL 兼容性。

### `difference_type`

**作用与语义：**

Typedef 用于ptrdiff_t。提供 STL 兼容性。

### `iterator`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `pointer`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `reference`

**作用与语义：**

T和的Typedef。提供STL兼容性。

### `reverse_iterator`

**作用与语义：**

Typedef 用于`std::reverse_iterator<T*>`。提供支持 STL 兼容性。

### `size_type`

**作用与语义：**

类型定义用于国际语言。提供支持STL兼容性。

### `value_type`

**作用与语义：**

T的Typedef。提供STL兼容性。

### `void insert(qsizetype i, const T &value)`

**作用与语义：**

插入迭代器指向的项目前方`value` `before`。返回指向插入项的迭代器。

### `QVarLengthArray<T, Prealloc>::iterator insert(QVarLengthArray<T, Prealloc>::const_iterator before, const T &value)`

**作用与语义：**

在向量中索引位置`i`插入`count` `value`副本。

### `(since 6.8) qsizetype max_size() const`

**作用与语义：**

它返回数组理论上能容纳的最大元素数。实际上，这个数量可以更小，受限于系统可用的内存容量。

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

`QVarLengthArray` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
