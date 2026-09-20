# Qt QList 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QList>`  
> 所属模块：`Qt6::Core`  
> 类型性质：连续内存、可动态扩容、隐式共享的值容器  
> 相关类型：`QVector`、`QVarLengthArray`、`std::vector`、`std::list`

## 1. 它解决什么问题

`QList<T>` 用一段连续内存保存一组同类型元素，并提供 Qt 风格和 STL 风格两套容器接口。它解决的是：

- 需要按索引快速访问元素；
- 需要在运行时增加或删除元素；
- 需要把容器作为值返回、复制或放进其他 Qt API；
- 需要把数据交给要求连续 C++ 数组的函数；
- 需要和 Qt 的隐式共享、`QDataStream`、`qHash()` 等基础设施协作。

Qt 6 中的 `QList<T>` 是默认的通用顺序容器。`QVector<T>` 已经是它的别名，因此 Qt 5 中“`QList` 适合小对象、`QVector` 适合连续数组”的旧判断不能直接搬到 Qt 6。

它不是链表：

- 元素存放在相邻内存位置；
- `at()`、`operator[]` 和指针访问是常量时间；
- 中间插入、删除通常需要移动后续元素，是线性时间；
- 如果真正需要中间插入稳定为常量时间、并且主要依赖迭代器而不是索引，应考虑 `std::list`。

## 2. 实际使用场景

### 2.1 保存 Qt 值对象

```cpp
QList<QString> names{"Ada", "Grace", "Linus"};
QList<QPoint> points;
points.append(QPoint(10, 20));
points.append(QPoint(30, 40));
```

适合保存 `QString`、`QPoint`、业务结构体、指针和其他可赋值类型。不能把 `QWidget` 这类不可复制或不可赋值的对象直接作为元素；通常保存 `QWidget *`、智能指针或业务值类型。

### 2.2 函数返回和跨层传递

```cpp
QList<QString> loadRecentFiles()
{
    return {QStringLiteral("a.txt"), QStringLiteral("b.txt")};
}
```

复制一个 `QList` 通常只复制共享数据块的引用，复杂度接近常量时间。真正修改其中一个副本时，Qt 才执行写时复制。

### 2.3 和连续数组 API 对接

```cpp
void consumeInts(const int *values, qsizetype count);

QList<int> values{1, 2, 3, 4};
consumeInts(values.constData(), values.size());
```

`constData()` 返回连续元素的只读指针。需要修改时使用非 const `data()`，但它可能先触发分离。

### 2.4 用于队列式操作

`append()`/`push_back()` 和 `removeLast()`/`pop_back()` 适合尾部操作。头部的 `prepend()`、`removeFirst()`、`pop_front()` 也可用，但它们会移动大量元素，不适合高吞吐队列；大量头尾进出应考虑 `QQueue`、`QVarLengthArray` 或其他专用结构。

## 3. 构建与最小代码

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QList>
```

使用流运算符时通常还需要：

```cpp
#include <QDataStream>
```

### 3.3 最小可用示例

```cpp
#include <QList>
#include <QString>

QList<QString> makeNames()
{
    QList<QString> names;
    names.reserve(3);
    names.append(QStringLiteral("Ada"));
    names.append(QStringLiteral("Grace"));
    names.append(QStringLiteral("Katherine"));
    return names;
}
```

## 4. 先掌握五条核心语义

### 4.1 Qt 6 是连续数组，不是链表

`QList<T>` 保证元素位于相邻内存位置，并提供 C-compatible array layout。可以用索引或 `data()` 访问：

```cpp
QList<int> values(3);
values[0] = 10;
values[1] = 20;
values[2] = 30;
```

因此：

- 随机访问是常量时间；
- 尾部追加通常是摊销常量时间；
- 中间插入、删除、头部插入和删除通常是线性时间；
- 扩容或分离会搬移整个元素序列。

### 4.2 复制是隐式共享，修改是写时复制

```cpp
QList<QString> original{"a", "b"};
QList<QString> copy = original; // 通常只共享数据

copy[0] = "changed";             // copy 分离并复制元素
```

复制构造和复制赋值通常是常量时间。修改共享实例时，复制成本与元素数量相关，通常是线性时间。

需要特别注意：**非 const 访问本身就可能触发分离**。例如：

```cpp
QList<int> copy = original;
int *p = copy.data();   // 为获得可写指针，可能触发深拷贝
auto it = copy.begin(); // 可写迭代器同样可能触发分离
```

只读遍历优先使用 const 容器、`cbegin()`/`cend()` 或 `constData()`。

### 4.3 `at()`、`operator[]`、`value()` 不是同一套越界策略

| 需求 | API | 越界行为 |
| --- | --- | --- |
| 只读且索引一定有效 | `at(i)` | 越界会触发 Qt 断言 |
| 读写且索引一定有效 | 非 const `operator[](i)` | 越界会触发 Qt 断言；可因写访问而分离 |
| 只读索引访问 | const `operator[](i)` | 等价于 `at(i)` |
| 不希望越界中止 | `value(i)` | 返回默认构造值 |
| 不希望越界中止并指定回退 | `value(i, fallback)` | 返回 `fallback` |

```cpp
const QList<int> values{10, 20};
Q_ASSERT(values.at(1) == 20);
Q_ASSERT(values.value(99, -1) == -1);
```

`value()` 返回元素副本，不返回引用；它适合不确定索引的查询，不适合通过返回值修改容器。

### 4.4 迭代器和裸指针的生命周期很严格

文档对 `QList` 的一般规则是：容器修改或发生分离时，迭代器通常失效。`data()`、`constData()` 返回的指针也会在分离或修改后失效。

```cpp
auto it = list.cbegin();
list.append(value); // 不要再使用旧 it
```

隐式共享容器的迭代器还存在一个额外陷阱：不要在迭代器活跃时复制容器并交替修改其中一个副本。它和 STL 容器的迭代器模型并不完全相同。

### 4.5 元素类型必须满足容器要求

`T` 至少应是可赋值的数据类型，并满足所调用 API 的额外要求：

- `append()`、`replace()`、移动和删除需要适当的构造、赋值或析构能力；
- `contains()`、`count()`、`removeAll()`、`removeOne()`、`indexOf()` 等比较 API 需要可用的 `operator==()`；
- `qHash(QList<T>)` 要求 `T` 支持 `qHash()`；
- `QDataStream` 运算符要求 `T` 支持对应的流运算符；
- 三路比较要求 `T` 支持 `operator<=>`，或至少支持可合成的 `<`。

## 5. 初始化、容量和性能边界

### 5.1 构造指定数量的元素

```cpp
QList<QString> strings(200);          // 200 个默认构造的 QString
QList<QString> filled(200, "Pass");   // 200 个相同值
```

`QList(qsizetype size)` 会创建指定数量的默认构造元素。`size` 必须非负，内存不足时可能抛出 `std::bad_alloc`；禁用异常时，内存耗尽行为不应依赖。

Qt 6.8 起可以请求不初始化新增元素：

```cpp
QList<int> buffer(1024, Qt::Uninitialized);
buffer.resizeForOverwrite(2048);
```

这只适合随后立即写满新增区域的场景。对有构造函数的 `T`，Qt 可能使用接受 `Qt::Uninitialized` 的构造函数；否则会默认构造。对 `int`、`float` 等平凡类型，新增值可能是不确定的，读取前必须先写入。

### 5.2 `size()`、`capacity()` 和 `maxSize()`

- `size()` 是实际元素数量；
- `capacity()` 是不强制重新分配时最多可容纳的元素数量；
- `maxSize()` 是类型和平台允许的理论上限；
- `capacity()` 不等于当前内存块尾部一定有同样数量的空位，内部空闲位置不应自行推断；
- `reserve(n)` 可确保至少有足够的尾部空间用于追加；
- 实际可用容量还受连续大块内存、进程地址空间和操作系统限制。

Qt 通常会为了减少扩容次数预留比当前 `size()` 更多的空间，但不要依赖具体增长倍数。

### 5.3 删除元素通常不自动释放容量

```cpp
list.clear();   // 清空元素，未共享时通常保留容量
list.squeeze(); // 需要释放多余容量时调用
```

`clear()` 在当前实例不共享时通常保留容量，适合“清空后重新填充”。如果需要尽量释放多余空间，调用 `squeeze()`；STL 风格的 `shrink_to_fit()` 是同义接口。

### 5.4 复杂度速记

| 操作 | 典型复杂度 | 说明 |
| --- | --- | --- |
| 复制构造、复制赋值 | 常量时间 | 共享数据块 |
| `at()`、索引访问 | 常量时间 | 连续内存 |
| `append()`、尾部 `emplaceBack()` | 摊销常量时间 | 扩容时为线性 |
| `prepend()`、头部插入 | 线性时间 | 需要移动已有元素 |
| 中间 `insert()` | 线性时间 | 需要移动后续元素 |
| 中间 `remove()` | 线性时间 | 需要移动后续元素 |
| `contains()`、`indexOf()` | 线性时间 | 顺序搜索 |
| `sliced()`、`mid()` | 通常线性时间 | 返回独立的结果容器；完整 `mid()` 可共享 |
| 写时复制分离 | 线性时间 | 复制元素到新数据块 |

## 6. 关键使用方式

### 6.1 追加和原地构造

```cpp
QList<QString> names;
names.append(QStringLiteral("Ada"));
names.push_back(QStringLiteral("Grace"));
names.emplaceBack(5, QChar('x')); // 直接构造 QString("xxxxx")
```

`emplaceBack()` 返回新元素的引用；如果后续操作可能扩容，不要长期保存这条引用。

`append(const QList<T> &)` 追加另一个列表的元素；`append(QList<T> &&)` 可以移动右值列表中的元素，通常减少复制。不要把自身作为右值参数传给自己：

```cpp
// 不要这样做：list.append(std::move(list));
```

### 6.2 插入、替换、移动

```cpp
QList<int> values{1, 3};
values.insert(1, 2);       // 1, 2, 3
values.replace(2, 30);      // 1, 2, 30
values.move(2, 0);          // 30, 1, 2
values.swapItemsAt(0, 2);   // 2, 1, 30
```

索引插入允许 `i == size()`，表示尾部插入；替换和交换要求索引已经存在。`move(from, to)` 的两个位置都必须在现有范围内，不能把元素移动到 `size()` 之后。

### 6.3 删除和取出

```cpp
QList<int> values{10, 20, 30};
values.removeAt(1);        // 删除 20
int last = values.takeLast();
int first = values.takeFirst();
```

使用选择：

- 只删除：`removeAt()`、`remove()`、`removeFirst()`、`removeLast()`；
- 删除并返回元素：`takeAt()`、`takeFirst()`、`takeLast()`；
- 按值删除全部或一个：`removeAll()`、`removeOne()`；
- 按谓词删除：`removeIf()` 或非成员 `erase_if()`；
- STL 风格迭代器删除：`erase(pos)`、`erase(begin, end)`。

空列表上调用 `first()`、`last()`、`takeFirst()`、`takeLast()`、`removeFirst()` 或 `removeLast()` 属于前置条件错误，通常会触发断言。

### 6.4 复制切片和范围边界

```cpp
const QList<int> values{0, 1, 2, 3, 4};
const QList<int> a = values.mid(1, 3);    // 1, 2, 3
const QList<int> b = values.sliced(1, 3); // 1, 2, 3
const QList<int> c = values.first(2);     // 0, 1
const QList<int> d = values.last(2);      // 3, 4
```

`mid()` 遵循 Qt 容器的宽松切片规则，会对位置和长度进行规范化；空范围返回空列表，完整范围可以直接共享当前数据。

`sliced()`、`first(n)`、`last(n)` 是更严格的范围 API：参数必须落在合法范围内，错误参数会触发断言。它们适合已经完成边界验证的代码。

### 6.5 `assign()` 与整体替换

```cpp
QList<int> values{1, 2, 3};
values.assign(4, 7);              // 7, 7, 7, 7
values.assign({10, 20});
```

`assign()` 从 Qt 6.6 起提供，会替换整个容器内容，并尽量复用已有容量。迭代器范围版本不能把范围指向当前 `*this`，否则行为未定义。

## 7. 公开类型和隐藏在头文件中的辅助 API

### 7.1 类型别名

- `value_type`：元素类型 `T`；
- `size_type`、`difference_type`：STL 兼容的大小和差值类型；
- `reference`、`const_reference`：元素引用类型；
- `pointer`、`const_pointer`：元素指针类型；
- `iterator`、`const_iterator`：正向可写和只读迭代器；
- `reverse_iterator`、`const_reverse_iterator`：反向可写和只读迭代器；
- `Iterator`、`ConstIterator`：Qt 风格别名；
- `parameter_type`：Qt 根据 `T` 特征选择的参数传递类型；
- `rvalue_ref`：元素右值引用相关的兼容别名。

`iterator` 和 `const_iterator` 的具体运算符、转换规则、失效警告分别见 `QList_iterator` 和 `QList_const_iterator` 笔记；使用时仍要遵守“修改或分离后不要继续使用旧迭代器”的总规则。

### 7.2 `detach()`、`isDetached()`、`isSharedWith()`

这些函数在 Qt 6.11.1 头文件中是公开成员，但不在类页的常规成员列表中：

```cpp
QList<int> a{1, 2};
QList<int> b = a;

Q_ASSERT(a.isSharedWith(b));
b.detach();                 // b 主动分离
Q_ASSERT(!a.isSharedWith(b));
Q_ASSERT(b.isDetached());
```

- `detach()`：如果共享，立即建立当前对象的独立副本；
- `isDetached()`：判断当前数据是否没有与其他 `QList` 实例共享；
- `isSharedWith(other)`：判断两个列表是否共享同一个数据块。

它们适合诊断隐式共享或在明确知道数据即将被修改时主动分离，不应作为普通业务逻辑的常规依赖。

### 7.3 `fromReadOnlyData()`

头文件还提供：

```cpp
template <qsizetype N>
static QList<T> fromReadOnlyData(const T (&data)[N]) noexcept;
```

它从固定大小的数组创建一个只读数据视图，避免立即复制数组内容。之后任何需要可写数据的操作都可能分离并复制；数组本身必须在列表仍可能引用它的整个生命周期内保持有效。由于这是头文件层面的低层辅助接口，跨模块公共接口不应轻易把它当作普通拥有型容器来使用。

## 8. 常见误区

### 8.1 把 Qt 5 的 `QList`/`QVector` 性能印象带到 Qt 6

Qt 6 中 `QVector<T>` 是 `QList<T>` 的别名。需要连续数组时直接使用 `QList` 即可，不要为了“连续内存”在 Qt 6 中机械改成 `QVector`。

### 8.2 只读访问却调用了非 const API

下面的代码可能为了返回可写引用而分离：

```cpp
QList<int> copy = values;
const int first = copy[0]; // copy 是非 const 对象，可能触发分离
```

读取时可以把对象绑定到 const 引用，或直接使用 `at()`：

```cpp
const QList<int> &view = copy;
const int first = view.at(0);
```

### 8.3 以为 `capacity()` 就能保证 `data() + size()` 后面一定有空间

Qt 文档明确指出，容量对应的空闲位置在内部布局中的具体位置不保证总在末尾。需要可靠的尾部追加空间时调用 `reserve()`，不要自行在 `data()` 后写入未构造元素。

### 8.4 删除后以为内存已经释放

`remove()`、`clear()` 和缩小 `resize()` 通常保留一部分容量。需要把容器缩到当前大小时才调用 `squeeze()`，但频繁 `squeeze()` 会带来重新分配和复制成本。

### 8.5 用 `first(n)`、`last(n)`、`sliced()` 期待自动截断

这些 API 要求范围合法。若输入来自用户、文件或网络，应先检查：

```cpp
if (pos >= 0 && n >= 0 && pos <= values.size() - n)
    result = values.sliced(pos, n);
```

不确定索引只想得到默认值时，用 `value()`；不要用 `at()` 代替宽松查询。

### 8.6 保存元素引用、迭代器或指针跨越修改

追加、插入、删除、替换、分离、扩容和某些非 const 访问都可能使旧引用、迭代器和指针失效。需要长期保存元素时保存副本、索引或稳定的业务 ID。

### 8.7 用 `QList` 做高性能头部队列

`prepend()` 和 `removeFirst()` 需要移动元素。它们适合少量操作，不适合作为大量生产者/消费者事件的核心队列。

### 8.8 误读 `resizeForOverwrite()` 的新增值

```cpp
QList<int> values;
values.resizeForOverwrite(100);
// values.at(0) 的值不能在写入前读取
```

`resizeForOverwrite()` 的优化前提是调用方会覆盖新增区域。需要可靠默认值时使用普通 `resize()`。

## 9. 逐项 API 说明

下面按用途列出 Qt 6.11.1 类页和头文件中可用的 API。重载在速查表中逐项展开。

### 9.1 构造、赋值和类型

- `QList()`：构造空列表。
- `QList(qsizetype size)`：构造 `size` 个默认构造元素；`size` 必须非负。
- `QList(std::initializer_list<T>)`：从初始化列表复制元素。
- `QList(InputIterator first, InputIterator last)`：复制半开区间 `[first, last)`；要求输入迭代器。
- `QList(qsizetype size, parameter_type value)`：构造 `size` 个相同值。
- `QList(qsizetype size, Qt::Initialization)`：Qt 6.8 起提供，使用 `Qt::Uninitialized` 请求不初始化新增元素。
- `QList(const QList &other)`：隐式共享复制，通常为常量时间。
- `QList(QList &&other)`：移动构造。
- `~QList()`：释放当前实例对数据块的引用；最后一个引用销毁时释放存储。
- `operator=(const QList &other)`：复制赋值并共享数据。
- `operator=(QList &&other)`：移动赋值。
- `operator=(std::initializer_list<T>)`：用初始化列表替换内容。
- `assign(std::initializer_list<T>)`：Qt 6.6 起，用初始化列表替换内容并返回 `*this`。
- `assign(InputIterator first, InputIterator last)`：Qt 6.6 起，用迭代器范围替换内容；范围不能来自当前容器。
- `assign(qsizetype n, parameter_type value)`：Qt 6.6 起，用 `n` 个相同值替换内容。
- `swap(QList &other)`：交换两个列表的数据块，`noexcept`，通常为常量时间。

### 9.2 大小、容量和共享状态

- `size()`：返回元素数量。
- `count()`：无参数重载，等价于 `size()`。
- `length()`：等价于 `size()`。
- `isEmpty()`：判断是否为空。
- `empty()`：STL 兼容接口，等价于 `isEmpty()`。
- `capacity()`：返回无需重新分配即可容纳的容量。
- `reserve(qsizetype size)`：至少为指定数量预留容量，并确保追加所需的尾部空间。
- `squeeze()`：尽量释放多余容量，使容量接近当前大小。
- `shrink_to_fit()`：STL 兼容接口，等价于 `squeeze()`。
- `maxSize()`：Qt 6.8 起的静态上限查询。
- `max_size()`：Qt 6.8 起的 STL 兼容上限查询，等价于 `maxSize()`。
- `detach()`：主动分离共享数据。
- `isDetached()`：判断当前实例是否独占数据。
- `isSharedWith(const QList &other)`：判断两个实例是否共享数据。

### 9.3 访问、指针和迭代

- `at(qsizetype i) const`：只读访问有效索引；越界断言；不因写访问而分离。
- `operator[](qsizetype i)`：可写访问有效索引；越界断言；非 const 对象可能分离。
- `operator[](qsizetype i) const`：只读重载，等价于 `at(i)`。
- `value(qsizetype i) const`：越界返回 `T()`。
- `value(qsizetype i, parameter_type defaultValue) const`：越界返回指定默认值。
- `data()`：返回可写连续数组指针；可能分离；指针会因修改或分离失效。
- `data() const`：返回只读连续数组指针。
- `constData()`：返回只读连续数组指针，不主动分离。
- `begin()`：返回可写迭代器；可能分离。
- `begin() const`：返回只读迭代器。
- `end()`：返回可写尾后迭代器；可能分离。
- `end() const`：返回只读尾后迭代器。
- `cbegin()`：返回只读起始迭代器。
- `cend()`：返回只读尾后迭代器。
- `constBegin()`：Qt 风格只读起始迭代器。
- `constEnd()`：Qt 风格只读尾后迭代器。
- `rbegin()`：返回可写反向起始迭代器；可能分离。
- `rbegin() const`：返回只读反向起始迭代器。
- `rend()`：返回可写反向尾后迭代器；可能分离。
- `rend() const`：返回只读反向尾后迭代器。
- `crbegin()`：返回只读反向起始迭代器。
- `crend()`：返回只读反向尾后迭代器。

### 9.4 追加、原地构造、插入和替换

- `append(parameter_type value)`：复制或按参数策略追加一个元素。
- `append(rvalue_ref value)`：移动追加一个元素；对某些可按值传递的 `T`，移动重载可能退化为按值语义。
- `append(const QList &value)`：追加另一个列表的所有元素。
- `append(QList &&value)`：Qt 6.0 起移动追加另一个列表。
- `append(const_iterator first, const_iterator last)`：追加当前或其他列表的半开迭代器范围；范围必须在调用期间保持有效。
- `emplaceBack(Args &&... args)`：在尾部原地构造元素并返回其引用。
- `emplace_back(Args &&... args)`：STL 风格别名，等价于 `emplaceBack()`。
- `emplace(qsizetype i, Args &&... args)`：在索引 `i` 处原地构造；允许 `i == size()`。
- `emplace(const_iterator before, Args &&... args)`：在迭代器指向位置前原地构造；迭代器必须属于当前列表且有效。
- `prepend(parameter_type value)`：在头部追加一个元素，线性移动已有元素。
- `prepend(rvalue_ref value)`：在头部移动追加一个元素。
- `push_back(parameter_type value)`：STL 风格接口，等价于 `append(value)`。
- `push_back(rvalue_ref value)`：STL 风格移动追加接口。
- `push_front(parameter_type value)`：STL 风格接口，等价于 `prepend(value)`。
- `push_front(rvalue_ref value)`：STL 风格移动头部插入接口。
- `insert(qsizetype i, parameter_type value)`：在索引 `i` 前插入一个元素。
- `insert(qsizetype i, rvalue_ref value)`：在索引 `i` 前移动插入一个元素。
- `insert(qsizetype i, qsizetype count, parameter_type value)`：在索引 `i` 前插入 `count` 个副本。
- `insert(const_iterator before, parameter_type value)`：在迭代器位置前插入一个副本。
- `insert(const_iterator before, rvalue_ref value)`：在迭代器位置前移动插入一个元素。
- `insert(const_iterator before, qsizetype count, parameter_type value)`：在迭代器位置前插入多个副本。
- `replace(qsizetype i, parameter_type value)`：替换已有索引处的元素。
- `replace(qsizetype i, rvalue_ref value)`：移动替换已有索引处的元素。

### 9.5 删除、取出和重排

- `remove(qsizetype i, qsizetype n = 1)`：从索引 `i` 删除 `n` 个元素；范围必须合法。
- `removeAt(qsizetype i)`：删除单个索引元素，等价于 `remove(i)`。
- `removeFirst()`：删除首元素；空列表是前置条件错误。
- `removeLast()`：删除尾元素；空列表是前置条件错误。
- `pop_back()`：STL 风格接口，等价于 `removeLast()`。
- `pop_front()`：STL 风格接口，等价于 `removeFirst()`。
- `takeAt(qsizetype i)`：移动取出并删除指定元素。
- `takeFirst()`：移动取出并删除首元素。
- `takeLast()`：移动取出并删除尾元素。
- `removeAll(const AT &value)`：删除所有相等元素并返回删除数量。
- `removeOne(const AT &value)`：删除第一个相等元素并返回是否删除。
- `removeIf(Predicate pred)`：Qt 6.1 起，删除谓词返回 `true` 的元素并返回删除数量。
- `erase(const_iterator pos)`：删除迭代器位置元素并返回后继迭代器。
- `erase(const_iterator begin, const_iterator end)`：删除半开区间并返回后继迭代器。
- `move(qsizetype from, qsizetype to)`：把已有元素移动到另一个已有位置。
- `swapItemsAt(qsizetype i, qsizetype j)`：交换两个已有索引处的元素。
- `clear()`：删除全部元素；未共享时通常保留容量。
- `fill(parameter_type value, qsizetype size = -1)`：用同一值填充；`size == -1` 时保持现有大小，否则调整为指定大小。
- `resize(qsizetype size)`：调整大小，新元素默认构造。
- `resize(qsizetype size, parameter_type value)`：调整大小，新元素用指定值构造。
- `resizeForOverwrite(qsizetype size)`：Qt 6.8 起调整大小并尽量不初始化新增元素。

### 9.6 查找、端点和切片

- `contains(const AT &value) const`：判断是否包含相等元素。
- `count(const AT &value) const`：统计相等元素数量。
- `indexOf(const AT &value, qsizetype from = 0) const`：从前向后查找，找不到返回 `-1`；负 `from` 按相对位置规范化。
- `lastIndexOf(const AT &value, qsizetype from = -1) const`：从后向前查找，找不到返回 `-1`；默认从最后元素开始。
- `first()`：返回可写首元素引用；不能为空。
- `first() const`：返回只读首元素引用；不能为空。
- `constFirst() const`：返回只读首元素引用；不能为空。
- `last()`：返回可写尾元素引用；不能为空。
- `last() const`：返回只读尾元素引用；不能为空。
- `constLast() const`：返回只读尾元素引用；不能为空。
- `front()`：STL 兼容接口，等价于 `first()`。
- `front() const`：const 重载，等价于 `first() const`。
- `back()`：STL 兼容接口，等价于 `last()`。
- `back() const`：const 重载，等价于 `last() const`。
- `startsWith(parameter_type value) const`：非空且首元素相等时返回 `true`。
- `endsWith(parameter_type value) const`：非空且尾元素相等时返回 `true`。
- `mid(qsizetype pos, qsizetype length = -1) const`：按 Qt 的宽松规则返回子列表。
- `first(qsizetype n) const`：返回前 `n` 个元素；`n` 必须合法。
- `last(qsizetype n) const`：返回后 `n` 个元素；`n` 必须合法。
- `sliced(qsizetype pos) const`：从 `pos` 到末尾；范围必须合法。
- `sliced(qsizetype pos, qsizetype n) const`：返回 `[pos, pos + n)`；范围必须合法。

### 9.7 拼接、比较和非成员 API

- `operator+=(const QList &other)`：追加列表副本。
- `operator+=(QList &&other)`：Qt 6.0 起移动追加列表。
- `operator+=(parameter_type value)`：追加一个元素。
- `operator+=(rvalue_ref value)`：移动追加一个元素。
- `operator+(const QList &other) const &`：以当前列表副本和 `other` 拼接，返回新列表。
- `operator+(const QList &other) &&`：消费当前右值列表后拼接。
- `operator+(QList &&other) const &`：保留当前列表并移动拼接右值列表。
- `operator+(QList &&other) &&`：消费两个右值列表并拼接。
- `operator<<(parameter_type value)`：Qt 风格追加一个元素。
- `operator<<(rvalue_ref value)`：Qt 风格移动追加一个元素。
- `operator<<(const QList &other)`：Qt 风格追加另一个列表。
- `operator<<(QList &&other)`：Qt 6.0 起 Qt 风格移动追加另一个列表。
- `operator==(const QList &other) const`：按长度和元素顺序比较相等。
- `operator!=(const QList &other) const`：相等判断取反。
- `operator<(const QList &other) const`：按字典序比较；在非三路比较环境中提供。
- `operator<=(const QList &other) const`：字典序小于等于。
- `operator>(const QList &other) const`：字典序大于。
- `operator>=(const QList &other) const`：字典序大于等于。
- `operator<=>(const QList &lhs, const QList &rhs)`：Qt 6.9 起，在 C++20 且 `T` 满足三路比较要求时提供。
- `erase(QList<T> &list, const AT &value)`：Qt 6.1 起，非成员按值删除并返回数量；`value` 不应是 `list` 内元素的引用。
- `erase_if(QList<T> &list, Predicate pred)`：Qt 6.1 起，非成员按谓词删除并返回数量。
- `qHash(const QList<T> &key, size_t seed = 0)`：按元素范围计算哈希；`T` 必须支持 `qHash()`。
- `operator<<(QDataStream &out, const QList<T> &list)`：把列表写入数据流；`T` 必须支持输出流运算符。
- `operator>>(QDataStream &in, QList<T> &list)`：从数据流读取列表；`T` 必须支持输入流运算符。

## API 速查表
### 10.1 成员类型

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `QList::const_iterator` | STL 风格只读正向迭代器。 | 修改或分离后失效。 |
| `QList::iterator` | STL 风格可写正向迭代器。 | `begin()` 可能先分离；修改或分离后失效。 |
| `QList::ConstIterator` | `const_iterator` 的 Qt 风格别名。 | 仅是别名。 |
| `QList::Iterator` | `iterator` 的 Qt 风格别名。 | 仅是别名。 |
| `const_pointer` | `const T *` 兼容别名。 | 指针生命周期受修改和分离影响。 |
| `const_reference` | `const T &` 兼容别名。 | 引用生命周期受修改和分离影响。 |
| `const_reverse_iterator` | STL 风格只读反向迭代器。 | 修改或分离后失效。 |
| `difference_type` | 迭代器差值类型。 | STL 兼容。 |
| `parameter_type` | Qt 的元素参数传递类型。 | 具体形式由 `T` 的类型特征决定。 |
| `pointer` | `T *` 兼容别名。 | 指针生命周期受修改和分离影响。 |
| `reference` | `T &` 兼容别名。 | 引用生命周期受修改和分离影响。 |
| `reverse_iterator` | STL 风格可写反向迭代器。 | 修改或分离后失效。 |
| `rvalue_ref` | 元素右值引用兼容别名。 | 用于移动重载。 |
| `size_type` | 容器大小类型。 | Qt 索引通常使用 `qsizetype`。 |
| `value_type` | 元素类型 `T`。 | 必须满足所调用 API 的类型要求。 |

### 10.2 构造、赋值和容量

| API | 作用 | 关键注意 |
| --- | --- | --- |
| `QList()` | 构造空列表。 | `size() == 0`。 |
| `explicit QList(qsizetype size)` | 构造指定数量的默认元素。 | `size` 必须非负；不是只预留容量。 |
| `QList(std::initializer_list<T>)` | 从 `{...}` 构造列表。 | 元素会被复制或移动到容器。 |
| `QList(InputIterator first, InputIterator last)` | 复制半开范围。 | 要求输入迭代器；范围必须有效。 |
| `QList(qsizetype size, parameter_type value)` | 构造多个相同值。 | `size` 必须非负。 |
| `QList(qsizetype size, Qt::Initialization)` | Qt 6.8 起请求不初始化。 | 使用 `Qt::Uninitialized`；新增元素写入前不可读。 |
| `QList(const QList &other)` | 复制构造。 | 隐式共享，通常常量时间。 |
| `QList(QList &&other)` | 移动构造。 | `other` 进入有效但未指定内容状态。 |
| `~QList()` | 销毁列表实例。 | 只在最后一个共享者销毁时释放共享数据。 |
| `operator=(const QList &other)` | 复制赋值。 | 通常共享数据。 |
| `operator=(QList &&other)` | 移动赋值。 | `other` 仍可析构和重新赋值。 |
| `operator=(std::initializer_list<T>)` | 用初始化列表替换内容。 | 返回 `*this`。 |
| `assign(std::initializer_list<T>)` | Qt 6.6 起整体替换。 | 尽量复用容量。 |
| `assign(InputIterator, InputIterator)` | Qt 6.6 起按范围整体替换。 | 不能使用当前容器自身的迭代器。 |
| `assign(qsizetype n, parameter_type t)` | Qt 6.6 起填充 `n` 个值。 | `n` 必须非负。 |
| `swap(QList &other)` | 交换两个列表。 | `noexcept`，通常常量时间。 |
| `size() const` | 返回元素数量。 | 返回 `qsizetype`。 |
| `count() const` | 返回元素数量。 | 等价于 `size()`。 |
| `length() const` | 返回元素数量。 | 等价于 `size()`。 |
| `isEmpty() const` | 判断空容器。 | `size() == 0`。 |
| `empty() const` | STL 风格判断空容器。 | 等价于 `isEmpty()`。 |
| `capacity() const` | 返回当前容量。 | 不表示空闲位置必在数组尾部。 |
| `reserve(qsizetype size)` | 预留容量和尾部追加空间。 | 可能分离；不会按请求缩小。 |
| `squeeze()` | 释放多余容量。 | 可能重新分配；不要频繁调用。 |
| `shrink_to_fit()` | STL 风格释放多余容量。 | 等价于 `squeeze()`。 |
| `static maxSize()` | Qt 6.8 起返回理论最大元素数。 | 受平台、元素大小和管理开销限制。 |
| `max_size() const` | Qt 6.8 起 STL 风格上限查询。 | 等价于 `maxSize()`。 |
| `detach()` | 主动断开共享。 | 可能进行线性复制。 |
| `isDetached() const` | 判断是否独占数据。 | 只用于诊断或明确的性能控制。 |
| `isSharedWith(const QList &) const` | 判断是否共享数据。 | 共享关系可能随修改改变。 |

### 10.3 访问和迭代

| API | 作用 | 关键注意 |
| --- | --- | --- |
| `at(qsizetype i) const` | 只读访问元素。 | `0 <= i < size()`，否则断言。 |
| `operator[](qsizetype i)` | 可写访问元素。 | 可能分离；索引必须有效。 |
| `operator[](qsizetype i) const` | 只读访问元素。 | 等价于 `at(i)`。 |
| `value(qsizetype i) const` | 安全读取元素副本。 | 越界返回 `T()`，包括负索引。 |
| `value(qsizetype i, parameter_type defaultValue) const` | 安全读取并指定回退值。 | 越界返回 `defaultValue`。 |
| `data()` | 返回可写连续数组指针。 | 可能分离；指针会失效。 |
| `data() const` | 返回只读连续数组指针。 | 修改或分离后失效。 |
| `constData() const` | 返回只读连续数组指针。 | 不主动分离；指针会失效。 |
| `begin()` | 返回可写起始迭代器。 | 可能分离。 |
| `begin() const` | 返回只读起始迭代器。 | 修改或分离后失效。 |
| `end()` | 返回可写尾后迭代器。 | 可能分离。 |
| `end() const` | 返回只读尾后迭代器。 | 修改或分离后失效。 |
| `cbegin() const` | 返回只读起始迭代器。 | 修改或分离后失效。 |
| `cend() const` | 返回只读尾后迭代器。 | 修改或分离后失效。 |
| `constBegin() const` | Qt 风格只读起始迭代器。 | 修改或分离后失效。 |
| `constEnd() const` | Qt 风格只读尾后迭代器。 | 修改或分离后失效。 |
| `rbegin()` | 返回可写反向起始迭代器。 | 可能分离。 |
| `rbegin() const` | 返回只读反向起始迭代器。 | 修改或分离后失效。 |
| `rend()` | 返回可写反向尾后迭代器。 | 可能分离。 |
| `rend() const` | 返回只读反向尾后迭代器。 | 修改或分离后失效。 |
| `crbegin() const` | 返回只读反向起始迭代器。 | 修改或分离后失效。 |
| `crend() const` | 返回只读反向尾后迭代器。 | 修改或分离后失效。 |

### 10.4 追加、插入和替换

| API | 作用 | 关键注意 |
| --- | --- | --- |
| `append(parameter_type value)` | 复制追加一个元素。 | 尾部追加通常摊销常量时间。 |
| `append(rvalue_ref value)` | 移动追加一个元素。 | `value` 之后处于有效但未指定状态。 |
| `append(const QList &value)` | 追加另一个列表。 | 追加元素副本。 |
| `append(QList &&value)` | 移动追加另一个列表。 | Qt 6.0 起；不要传自身。 |
| `append(const_iterator first, const_iterator last)` | 追加半开迭代器范围。 | 范围必须有效；修改后旧迭代器可能失效。 |
| `emplaceBack(Args&&...)` | 尾部原地构造并返回引用。 | 扩容会使返回引用失效。 |
| `emplace_back(Args&&...)` | STL 风格尾部原地构造。 | 等价于 `emplaceBack()`。 |
| `emplace(qsizetype i, Args&&...)` | 在索引处原地构造。 | `0 <= i <= size()`。 |
| `emplace(const_iterator before, Args&&...)` | 在迭代器前原地构造。 | 迭代器必须属于当前列表。 |
| `prepend(parameter_type value)` | 头部复制插入。 | 线性移动已有元素。 |
| `prepend(rvalue_ref value)` | 头部移动插入。 | 线性移动已有元素。 |
| `push_back(parameter_type value)` | STL 风格复制追加。 | 等价于 `append(value)`。 |
| `push_back(rvalue_ref value)` | STL 风格移动追加。 | 可能使实参进入有效但未指定状态。 |
| `push_front(parameter_type value)` | STL 风格复制头插。 | 等价于 `prepend(value)`，线性移动。 |
| `push_front(rvalue_ref value)` | STL 风格移动头插。 | 线性移动已有元素。 |
| `insert(qsizetype i, parameter_type value)` | 索引前插入副本。 | `i == size()` 表示尾部。 |
| `insert(qsizetype i, rvalue_ref value)` | 索引前移动插入。 | 索引必须在 `[0, size()]`。 |
| `insert(qsizetype i, qsizetype count, parameter_type value)` | 插入多个相同副本。 | `count >= 0`。 |
| `insert(const_iterator before, parameter_type value)` | 迭代器前插入副本。 | 迭代器必须有效。 |
| `insert(const_iterator before, rvalue_ref value)` | 迭代器前移动插入。 | 迭代器必须有效。 |
| `insert(const_iterator before, qsizetype count, parameter_type value)` | 迭代器前插入多个副本。 | 迭代器必须有效，`count >= 0`。 |
| `replace(qsizetype i, parameter_type value)` | 复制替换元素。 | `i` 必须已存在；可能分离。 |
| `replace(qsizetype i, rvalue_ref value)` | 移动替换元素。 | `i` 必须已存在。 |

### 10.5 删除、取出和容量变化

| API | 作用 | 关键注意 |
| --- | --- | --- |
| `remove(qsizetype i, qsizetype n = 1)` | 删除连续范围。 | `i` 与 `n` 必须组成合法范围。 |
| `removeAt(qsizetype i)` | 删除一个元素。 | 等价于 `remove(i)`。 |
| `removeFirst()` | 删除首元素。 | 空列表断言。 |
| `removeLast()` | 删除尾元素。 | 空列表断言。 |
| `pop_back()` | STL 风格删除尾元素。 | 等价于 `removeLast()`；空列表断言。 |
| `pop_front()` | STL 风格删除首元素。 | 等价于 `removeFirst()`；空列表断言。 |
| `takeAt(qsizetype i)` | 移动取出并删除。 | 索引必须有效。 |
| `takeFirst()` | 移动取出首元素。 | 空列表断言。 |
| `takeLast()` | 移动取出尾元素。 | 空列表断言。 |
| `removeAll(const AT &value)` | 删除全部相等项。 | 需要元素比较；返回删除数。 |
| `removeOne(const AT &value)` | 删除第一个相等项。 | 需要元素比较；返回是否删除。 |
| `removeIf(Predicate pred)` | Qt 6.1 起按谓词删除。 | 返回删除数；修改会使迭代器失效。 |
| `erase(const_iterator pos)` | 删除单个迭代器位置。 | 返回后继迭代器。 |
| `erase(const_iterator begin, const_iterator end)` | 删除半开迭代器范围。 | 两个迭代器必须属于当前列表。 |
| `clear()` | 删除全部元素。 | 未共享时通常保留容量。 |
| `fill(parameter_type value, qsizetype size = -1)` | 填充并可调整大小。 | `-1` 表示保持当前大小。 |
| `resize(qsizetype size)` | 调整大小并默认构造新增项。 | 缩小时销毁尾部项。 |
| `resize(qsizetype size, parameter_type value)` | 调整大小并用值构造新增项。 | 缩小时忽略填充值。 |
| `resizeForOverwrite(qsizetype size)` | Qt 6.8 起尽量不初始化新增项。 | 写入前不可读取新增项。 |
| `move(qsizetype from, qsizetype to)` | 移动元素位置。 | 两个索引都必须在 `[0, size())`。 |
| `swapItemsAt(qsizetype i, qsizetype j)` | 交换两个元素。 | 两个索引都必须有效。 |

### 10.6 查找、端点和切片

| API | 作用 | 关键注意 |
| --- | --- | --- |
| `contains(const AT &value) const` | 判断是否包含值。 | 要求 `operator==()`。 |
| `count(const AT &value) const` | 统计值出现次数。 | 要求 `operator==()`。 |
| `indexOf(const AT &value, qsizetype from = 0) const` | 从指定位置向后查找。 | 找不到返回 `-1`；负起点按相对位置处理。 |
| `lastIndexOf(const AT &value, qsizetype from = -1) const` | 从指定位置向前查找。 | 找不到返回 `-1`；默认从末尾开始。 |
| `first()` | 返回可写首元素。 | 空列表断言。 |
| `first() const` | 返回只读首元素。 | 空列表断言。 |
| `constFirst() const` | 返回只读首元素。 | 空列表断言。 |
| `last()` | 返回可写尾元素。 | 空列表断言。 |
| `last() const` | 返回只读尾元素。 | 空列表断言。 |
| `constLast() const` | 返回只读尾元素。 | 空列表断言。 |
| `front()` | STL 风格首元素访问。 | 等价于 `first()`。 |
| `front() const` | STL 风格只读首元素访问。 | 空列表断言。 |
| `back()` | STL 风格尾元素访问。 | 等价于 `last()`。 |
| `back() const` | STL 风格只读尾元素访问。 | 空列表断言。 |
| `startsWith(parameter_type value) const` | 判断首元素是否相等。 | 空列表返回 `false`。 |
| `endsWith(parameter_type value) const` | 判断尾元素是否相等。 | 空列表返回 `false`。 |
| `mid(qsizetype pos, qsizetype length = -1) const` | 返回宽松规则的子列表。 | 位置和长度会规范化。 |
| `first(qsizetype n) const` | 返回前 `n` 项副本。 | `n` 必须在合法范围内。 |
| `last(qsizetype n) const` | 返回后 `n` 项副本。 | `n` 必须在合法范围内。 |
| `sliced(qsizetype pos) const` | 返回从 `pos` 到末尾。 | `pos` 必须合法。 |
| `sliced(qsizetype pos, qsizetype n) const` | 返回半开范围副本。 | `pos`、`n` 必须合法。 |

### 10.7 拼接、比较和非成员

| API | 作用 | 关键注意 |
| --- | --- | --- |
| `operator+=(const QList &other)` | 追加列表。 | 返回 `*this`。 |
| `operator+=(QList &&other)` | 移动追加列表。 | Qt 6.0 起；不要传自身。 |
| `operator+=(parameter_type value)` | 追加一个值。 | 返回 `*this`。 |
| `operator+=(rvalue_ref value)` | 移动追加一个值。 | 返回 `*this`。 |
| `operator+(const QList &other) const &` | 保留左值并返回拼接副本。 | 可能分配新容器。 |
| `operator+(const QList &other) &&` | 消费左值对象并拼接。 | 适合临时列表。 |
| `operator+(QList &&other) const &` | 保留左值并移动右值列表。 | 返回新列表。 |
| `operator+(QList &&other) &&` | 消费两个右值列表并拼接。 | 适合连续表达式。 |
| `operator<<(parameter_type value)` | Qt 风格追加值。 | 返回 `*this`。 |
| `operator<<(rvalue_ref value)` | Qt 风格移动追加值。 | 返回 `*this`。 |
| `operator<<(const QList &other)` | Qt 风格追加列表。 | 返回 `*this`。 |
| `operator<<(QList &&other)` | Qt 风格移动追加列表。 | Qt 6.0 起。 |
| `operator==(const QList &other) const` | 比较长度和元素顺序。 | 需要元素可比较相等。 |
| `operator!=(const QList &other) const` | 不等比较。 | 是相等比较的否定。 |
| `operator<(const QList &other) const` | 字典序小于。 | 元素需支持 `<`；C++20 环境可能由 `<=>` 替代。 |
| `operator<=(const QList &other) const` | 字典序不大于。 | 元素需支持有序比较。 |
| `operator>(const QList &other) const` | 字典序大于。 | 元素需支持有序比较。 |
| `operator>=(const QList &other) const` | 字典序不小于。 | 元素需支持有序比较。 |
| `operator<=>(lhs, rhs)` | Qt 6.9 起三路字典序比较。 | 仅 C++20 且满足概念时可用。 |
| `erase(QList<T> &, const AT &)` | Qt 6.1 起按值删除。 | 返回删除数；值不可引用列表内部元素。 |
| `erase_if(QList<T> &, Predicate)` | Qt 6.1 起按谓词删除。 | 返回删除数。 |
| `qHash(const QList<T> &, size_t seed)` | 计算列表哈希。 | `T` 必须支持 `qHash()`。 |
| `operator<<(QDataStream &, const QList<T> &)` | 写入列表。 | `T` 必须支持流输出。 |
| `operator>>(QDataStream &, QList<T> &)` | 读取列表。 | `T` 必须支持流输入；检查流状态。 |

### 10.8 兼容性和低层辅助

| API | 作用 | 版本和注意 |
| --- | --- | --- |
| `QList::fromList(const QList &)` | 返回传入列表。 | 已弃用；Qt 6 中是兼容性 no-op。 |
| `toList() const` | 返回当前列表副本。 | 已弃用；Qt 6 中是兼容性 no-op。 |
| `QList::fromVector(const QList &)` | 返回传入列表。 | 已弃用；Qt 6 中 `QVector` 已是别名。 |
| `toVector() const` | 返回当前列表副本。 | 已弃用；Qt 6 中是兼容性 no-op。 |
| `fromReadOnlyData(const T (&)[N])` | 从固定数组构造只读数据视图。 | 头文件低层 API；数组生命周期必须覆盖视图使用期。 |

## 11. 完整示例：收集、过滤和交给 C API

```cpp
#include <QList>
#include <QString>

void consumeNames(const QString *names, qsizetype count);

QList<QString> normalizedNames(const QList<QString> &input)
{
    QList<QString> result;
    result.reserve(input.size());

    for (const QString &name : input) {
        const QString normalized = name.trimmed();
        if (!normalized.isEmpty())
            result.append(normalized);
    }

    return result;
}

void process()
{
    const QList<QString> input{
        QStringLiteral(" Ada "),
        QStringLiteral(""),
        QStringLiteral(" Grace ")
    };

    const QList<QString> names = normalizedNames(input);
    consumeNames(names.constData(), names.size());
}
```

这里使用 const 范围遍历和 `constData()`，不会为了只读访问主动获取可写数据。`normalizedNames()` 返回 `QList` 时也可以利用隐式共享和移动返回。

## 12. 选型结论

1. Qt 6 中需要通用连续数组容器时，优先考虑 `QList<T>`。
2. `QVector<T>` 在 Qt 6 中是 `QList<T>` 的别名，不是另一种性能模型。
3. 复制便宜不代表修改便宜；共享副本第一次写入可能触发线性深拷贝。
4. 只读查询优先用 `at()`、const `operator[]`、`constData()` 和 const 迭代器。
5. 可能越界但希望返回回退值时用 `value()`；范围必须合法时用 `at()`、`sliced()`、`first(n)` 或 `last(n)`。
6. 尾部追加适合 `append()`/`emplaceBack()`；中间和头部修改是线性操作。
7. `reserve()` 用于减少扩容，`squeeze()`/`shrink_to_fit()` 用于释放多余容量。
8. `resizeForOverwrite()` 只适合新增区域会被立即覆盖的性能敏感代码。
9. 任何修改、分离或可能扩容的操作都应视为会使旧迭代器、指针和引用失效。
10. 真正需要链表性质时选择 `std::list`，需要小型栈优先数组时考虑 `QVarLengthArray`。
