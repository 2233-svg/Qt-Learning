# QContiguousCache

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QContiguousCache` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QContiguousCache` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QContiguousCache>`
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

### 公有函数

- `QContiguousCache(qsizetype capacity = 0)`
- `QContiguousCache(const QContiguousCache<T> &other)`
- `~QContiguousCache()`
- `void append(const T &value)`
- `bool areIndexesValid() const`
- `const T & at(qsizetype i) const`
- `qsizetype available() const`
- `qsizetype capacity() const`
- `void clear()`
- `bool containsIndex(qsizetype i) const`
- `qsizetype count() const`
- `T & first()`
- `const T & first() const`
- `qsizetype firstIndex() const`
- `void insert(qsizetype i, const T &value)`
- `bool isEmpty() const`
- `bool isFull() const`
- `T & last()`
- `const T & last() const`
- `qsizetype lastIndex() const`
- `void normalizeIndexes()`
- `void prepend(const T &value)`
- `void removeFirst()`
- `void removeLast()`
- `void setCapacity(qsizetype size)`
- `qsizetype size() const`
- `void swap(QContiguousCache<T> &other)`
- `T takeFirst()`
- `T takeLast()`
- `bool operator!=(const QContiguousCache<T> &other) const`
- `QContiguousCache<T> & operator=(QContiguousCache<T> &&other)`
- `QContiguousCache<T> & operator=(const QContiguousCache<T> &other)`
- `bool operator==(const QContiguousCache<T> &other) const`
- `T & operator[](qsizetype i)`
- `const T & operator[](qsizetype i) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QContiguousCache::QContiguousCache(qsizetype capacity = 0)`

**作用与语义：**

用给定的 `capacity` 构建缓存。

### `QContiguousCache::QContiguousCache(const QContiguousCache<T> &other)`

**作用与语义：**

构建了一份`other`的副本。
该操作耗时为常数，因为 QContiguousCache 是隐式共享的。这使得从函数返回 QContiguousCache 的速度非常快。如果共享实例被修改，它将被复制（写时复制），这需要线性时间。

### `QContiguousCache::~QContiguousCache()`

**作用与语义：**

摧毁缓存。

### `void QContiguousCache::append(const T &value)`

**作用与语义：**

插入`value`在缓存末尾。如果缓存已经满了，缓存开头的项目将被移除。

### `bool QContiguousCache::areIndexesValid() const`

**作用与语义：**

返回缓存中存储的项索引是否有效。如果条目在索引位置INT_MAX之后添加或在索引位置0之前加上，索引可能失效。这种情况仅在连续缓存的非常长寿命循环缓冲区使用中发生。通过调用`normalizeIndexes()`可以使索引重新有效。

### `const T &QContiguousCache::at(qsizetype i) const`

**作用与语义：**

返回缓存中索引位置`i`的项目。`i` 必须是缓存中的有效索引位置（即 `firstIndex()` <= `i` <= `lastIndex()`）。
缓存中的索引表示该项从第一个附加到缓存的物品所处的位置数。也就是说，容量为100的缓存如果附加了150个物品，其有效索引范围为50到149。这使得可以基于理论上的无限列表将物品插入和检索到缓存中。

### `qsizetype QContiguousCache::available() const`

**作用与语义：**

返回可在缓存满之前添加的物品数量。

### `qsizetype QContiguousCache::capacity() const`

**作用与语义：**

返回缓存在满之前可存储的物品数量。当缓存包含的物品数量等于其容量时，添加新物品会导致距离新增物品最远的物品被移除。

### `void QContiguousCache::clear()`

**作用与语义：**

从缓存中移除所有物品。容量保持不变。

### `bool QContiguousCache::containsIndex(qsizetype i) const`

**作用与语义：**

如果缓存的索引范围包含给定的索引`i`，返回`true`。

### `qsizetype QContiguousCache::count() const`

**作用与语义：**

和`size()`一样。

### `T &QContiguousCache::first()`

**作用与语义：**

返回缓存中第一个项目的引用。该函数假设缓存不是空的。

### `const T &QContiguousCache::first() const`

**作用与语义：**

返回缓存中第一个项目的引用。该函数假设缓存不是空的。

### `qsizetype QContiguousCache::firstIndex() const`

**作用与语义：**

返回缓存中的第一个有效索引。如果缓存为空，索引将无效。

### `void QContiguousCache::insert(qsizetype i, const T &value)`

**作用与语义：**

在索引位置`i`插入`value`。如果缓存中`i`已有某项，则该值被替换。如果`i`多于`lastIndex()`或少于`firstIndex()`，则相当于`append()`或`prepend()`。
如果给定的索引`i`不在缓存当前范围内，也不在缓存索引范围边界内，则先清除缓存后再插入该项。此时缓存的大小为1。值得努力按照与当前索引范围相邻的顺序插入物品。
`QContiguousCache`类的有效索引范围为0到INT_MAX。插入超出该范围的行为未定义。

### `bool QContiguousCache::isEmpty() const`

**作用与语义：**

如果缓存中没有存储任何物品，返回`true`。

### `bool QContiguousCache::isFull() const`

**作用与语义：**

如果缓存中存储的项目数量等于缓存的容量，则返回 `true`。

### `T &QContiguousCache::last()`

**作用与语义：**

返回缓存中最后一项的引用。该函数假设缓存不是空的。

### `const T &QContiguousCache::last() const`

**作用与语义：**

返回缓存中最后一项的引用。该函数假设缓存不是空的。

### `qsizetype QContiguousCache::lastIndex() const`

**作用与语义：**

返回缓存中最后一个有效索引。如果缓存为空，索引将无效。

### `void QContiguousCache::normalizeIndexes()`

**作用与语义：**

移动缓存的第一个索引和最后一个索引，使其指向有效索引。该函数不修改缓存内容或缓存中元素的顺序。
其提供是为了在将缓存作为循环缓冲区时纠正索引溢出。

**官方示例：**

```cpp
 QContiguousCache<int> cache(10);
 cache.insert(INT_MAX, 1); // cache contains one value and has valid indexes, INT_MAX to INT_MAX
 cache.append(2); // cache contains two values but does not have valid indexes.
 cache.normalizeIndexes(); // cache has two values, 1 and 2.  New first index will be in the range of 0 to capacity().
```

### `void QContiguousCache::prepend(const T &value)`

**作用与语义：**

插入`value`缓存的起始位置。如果缓存已经满了，缓存末端的项目将被移除。

### `void QContiguousCache::removeFirst()`

**作用与语义：**

从缓存中移除第一个项目。该函数假设缓存不是空的。

### `void QContiguousCache::removeLast()`

**作用与语义：**

移除缓存中的最后一项。该函数假设缓存不是空的。

### `void QContiguousCache::setCapacity(qsizetype size)`

**作用与语义：**

将缓存容量设置为给定的`size`。缓存可以容纳等于其容量的数量。在插入、附加或前置物品到缓存时，如果缓存已经满，那么距离新增物品最远的物品将被移除。
如果给定`size`小于当前缓存中的物品数量，则只有缓存中最后`size`个物品会被保留。

### `qsizetype QContiguousCache::size() const`

**作用与语义：**

返回缓存中包含的物品数量。

### `[noexcept] void QContiguousCache::swap(QContiguousCache<T> &other)`

**作用与语义：**

将该缓存与`other`交换。这个操作非常快，且从未失败。

### `T QContiguousCache::takeFirst()`

**作用与语义：**

移除缓存中的第一个项目并返回。该函数假设缓存不是空的。
如果不使用返回值，`removeFirst()`效率更高。

### `T QContiguousCache::takeLast()`

**作用与语义：**

移除缓存中的最后一项并返回。该函数假设缓存不是空的。
如果不使用返回值，`removeLast()`效率更高。

### `bool QContiguousCache::operator!=(const QContiguousCache<T> &other) const`

**作用与语义：**

如果 `other` 不等于该缓存，返回 `true`;否则返回 `false`。
如果两个缓存在相同索引上包含相同的值，则它们被视为相等。该函数需要值类型来实现`operator==()`。

### `[noexcept] QContiguousCache<T> &QContiguousCache::operator=(QContiguousCache<T> &&other)`

**作用与语义：**

Move-assign `other` 到该`QContiguousCache`实例。

### `QContiguousCache<T> &QContiguousCache::operator=(const QContiguousCache<T> &other)`

**作用与语义：**

将`other`分配到该缓存并返回对该缓存的引用。

### `bool QContiguousCache::operator==(const QContiguousCache<T> &other) const`

**作用与语义：**

如果`other`等于该缓存，则返回`true`;否则返回`false`。
如果两个缓存在相同索引上包含相同的值，则它们被视为相等。该函数需要该值类型来实现`operator==()`。

### `T &QContiguousCache::operator[](qsizetype i)`

**作用与语义：**

返回索引位置`i`的项目作为可修改的引用。如果缓存在给定索引位置没有包含某个项`i`则会先在该位置插入一个空项。
大多数情况下，最好使用`at()`或`insert()`。
注意：操作符[]的非const重载需要`QContiguousCache`进行深度复制。使用`at()`进行非const `QContiguousCache`的只读访问。

### `const T &QContiguousCache::operator[](qsizetype i) const`

**作用与语义：**

和at（`i`）一样。

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

`QContiguousCache` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
