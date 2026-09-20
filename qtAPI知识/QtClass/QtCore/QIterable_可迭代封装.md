# Qt QIterable 类型擦除迭代底座深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QIterable>`  
> 所属模块：`Qt6::Core`  
> 模板：`template <typename Container> class QIterable`  
> 主要派生接口：`QMetaSequence::Iterable`、`QMetaAssociation::Iterable`  
> 旧派生接口：`QSequentialIterable`、`QAssociativeIterable`

## 1. 它解决什么问题

`QIterable<Container>` 是 Qt 运行时容器反射体系里的一个类型擦除底座。它让上层代码可以在不知道底层容器完整 C++ 类型的情况下，通过统一入口：

- 获得只读或可写迭代器；
- 逐个访问容器元素；
- 查询底层迭代器能力；
- 查询容器大小；
- 清空底层容器；
- 把具体容器的 native iterator 包装成 Qt 的 `QIterator` 或 `QConstIterator`。

它解决的是“容器类型在编译期未知，但运行时仍要访问”的问题：

```text
具体容器
QList<int> / QVector<QString> / QMap<QString, int> / 自定义注册容器
        │
        ▼
QMetaSequence 或 QMetaAssociation
        │ 运行时容器描述
        ▼
QIterable<Container>
        │ 类型擦除的迭代入口
        ▼
QMetaSequence::Iterable / QMetaAssociation::Iterable
```

这里的 `Container` 模板参数通常不是 `QList<int>` 这样的业务容器类型，而是 `QMetaSequence` 或 `QMetaAssociation` 这种“如何操作容器”的元容器描述器。

## 2. 它不是什么

`QIterable` 很容易被误读成“Qt 版 `QList`”。实际上它不是：

- 不是一个真正拥有元素的容器；
- 不是 `QList<T>`、`QVector<T>` 或 `std::vector<T>` 的替代品；
- 不是把底层容器复制出来的快照；
- 不是一个可以独立完成元素解引用的完整具体迭代器；
- 不是自动延长底层容器生命周期的智能指针；
- 不是保证随机访问的容器适配器。

它保存的是两样东西：

```text
元容器描述器 metaContainer
        +
指向真实容器对象的借用指针
```

真正的元素类型和 `operator*()` 语义由派生的具体 iterable 和 iterator 提供。普通应用代码更常见的入口是：

- `QMetaSequence::Iterable`：顺序容器；
- `QMetaAssociation::Iterable`：关联容器；
- 维护旧 `QVariant` 反射代码时的 `QSequentialIterable`；
- 维护旧 `QVariant` 反射代码时的 `QAssociativeIterable`。

## 3. Qt 6.11 中的 API 方向

Qt 6.11 的文档已经把 `QMetaSequence::Iterable` 和 `QMetaAssociation::Iterable` 作为现代元容器访问入口。旧的 `QSequentialIterable` 和 `QAssociativeIterable` 计划在 Qt 6.15 弃用，并建议迁移到新的 `QMetaSequence` / `QMetaAssociation` iterable。

因此：

- `QIterable` 本身是底层共用基础，不是业务层首选类型；
- 新代码优先使用具体的 `QMetaSequence::Iterable` 或 `QMetaAssociation::Iterable`；
- 旧代码中看到 `QIterable<QMetaSequence>` 或 `QIterable<QMetaAssociation>` 时，要把它理解成具体 iterable 的基类；
- 不要把 `QIterable` 类型直接暴露成稳定业务 API，除非你正在实现 Qt 元容器适配层。

## 4. 一个能工作的使用形状

下面展示现代 `QMetaSequence::Iterable` 如何使用 `QIterable` 提供的能力：

```cpp
#include <QList>
#include <QMetaSequence>
#include <QVariant>

QList<int> values{10, 20, 30};

QMetaSequence meta = QMetaSequence::fromContainer<QList<int>>();
QMetaSequence::Iterable iterable(meta, &values);

for (auto it = iterable.constBegin();
     it != iterable.constEnd();
     ++it) {
    const QVariant value = *it;
    qDebug() << value;
}
```

这里没有复制 `values`。`iterable` 只是指向 `values` 的视图，迭代期间必须保证 `values` 仍然存在，并且不能让会使迭代器失效的容器修改发生在迭代过程中。

如果需要修改底层容器，必须从可写对象构造 iterable，并使用可写入口：

```cpp
QMetaSequence::Iterable writable(meta, &values);

for (auto it = writable.mutableBegin();
     it != writable.mutableEnd();
     ++it) {
    *it = QVariant(42);
}
```

具体 `operator*()` 是否支持赋值，取决于 `QMetaSequence::Iterable` 的 iterator 和底层元容器能力；`QIterable` 只提供创建可写迭代器的基础设施。

## 5. 运行时对象关系

### 5.1 `metaContainer` 是操作协议

`QMetaSequence` 或 `QMetaAssociation` 中保存的是函数表和类型信息，例如：

- 如何创建 begin/end 迭代器；
- 如何复制、比较、前进和销毁迭代器；
- 是否支持 input、forward、bidirectional、random access；
- 如何读取或写入元素；
- 是否能查询 size；
- 是否支持 clear。

`QIterable` 的方法不会猜测底层容器类型，而是把操作转发给这个描述器：

```text
QIterable::constBegin()
        ↓
metaContainer.constBegin(realContainer)
        ↓
被擦除的底层 const iterator
        ↓
QConstIterator<Container>
```

### 5.2 iterable 指向真实对象

构造 `QIterable` 时传入的指针是借用关系：

```cpp
QMetaSequence::Iterable iterable(meta, &values);
```

`iterable` 不拥有 `values`，也不会在析构时删除它。下面这种返回方式是错误的：

```cpp
QMetaSequence::Iterable makeBadIterable()
{
    QList<int> local{1, 2, 3};
    return QMetaSequence::Iterable(
        QMetaSequence::fromContainer<QList<int>>(),
        &local);
}
```

返回后 `local` 已经销毁，得到的 iterable 只剩一个悬空指针。

### 5.3 iterator 还依赖 iterable 对象

`QBaseIterator` 内部保存了指向 `QIterable` 的指针，用来访问元容器描述器和释放底层迭代器。因此不仅真实容器要活着，创建 iterator 的 iterable 对象也要活着：

```cpp
QMetaSequence::Iterable makeBadIterator(QList<int> &values)
{
    QMetaSequence::Iterable iterable(
        QMetaSequence::fromContainer<QList<int>>(),
        &values);

    return iterable;
}

// 不要从一个即将销毁的临时 iterable 保存 iterator。
```

安全的结构是让两者有明确的外层生命周期：

```cpp
QMetaSequence::Iterable iterable(meta, &values);
auto it = iterable.constBegin();
```

## 6. 只读和可写是构造时保留下来的属性

`QIterable` 使用一个带 const 标记的擦除指针保存底层对象：

```text
从 T * 构造       -> 可以取得 mutableIterable()
从 const T * 构造 -> 只能取得 constIterable()
```

即使 iterable 自身变量不是 const，从 `const T *` 构造也不能凭空获得可写访问：

```cpp
const QList<int> values{1, 2, 3};
QMetaSequence::Iterable iterable(
    QMetaSequence::fromContainer<QList<int>>(),
    &values);

// 这个视图没有合法的可写底层对象。
```

因此：

- 只读遍历使用 `constBegin()` / `constEnd()`；
- 可写遍历使用 `mutableBegin()` / `mutableEnd()`；
- `clear()` 需要可写底层容器；
- 不能用 `const_cast` 绕过 iterable 保存的 const 信息；
- 是否能真正修改元素还取决于 `QMetaSequence` / `QMetaAssociation` 的元操作能力。

## 7. 迭代能力不是容器类型猜测

`QIterable` 提供四个能力查询：

| 查询 | 对应 C++ 迭代器能力 | 说明 |
| --- | --- | --- |
| `canInputIterate()` | `std::input_iterator_tag` | 能否进行输入方向的基本遍历 |
| `canForwardIterate()` | `std::forward_iterator_tag` | 能否向前遍历并满足 forward iterator 能力 |
| `canReverseIterate()` | `std::bidirectional_iterator_tag` | 能否向后移动；名字中的 reverse 指双向能力 |
| `canRandomAccessIterate()` | `std::random_access_iterator_tag` | 能否高效跳过多个位置并计算距离 |

能力具有层级关系：

```text
random access
    ⟹ bidirectional
        ⟹ forward
            ⟹ input
```

但“能够调用某个运算符”和“该运算符高效”要分开看。业务代码应先根据能力选择算法：

```cpp
if (iterable.canRandomAccessIterate()) {
    // 可以考虑 it += n、it + n、end - begin
} else if (iterable.canForwardIterate()) {
    // 使用 ++it 顺序前进
}
```

反向移动前确认 `canReverseIterate()`：

```cpp
if (iterable.canReverseIterate()) {
    auto it = iterable.constEnd();
    --it;
}
```

不要因为某个类型的接口上出现了 `operator-` 或 `operator+=`，就假设底层容器一定支持对应能力。

## 8. `QIterable` 与具体迭代器

### 8.1 基类迭代器只负责位置

`QIterator<Container>` 和 `QConstIterator<Container>` 主要负责：

- 保存底层擦除 iterator；
- 比较两个位置；
- 前进、后退和跳跃；
- 计算位置差；
- 复制和销毁底层 iterator。

它们本身不是完整的元素访问接口。具体派生类型补上解引用语义：

```text
QIterable<QMetaSequence>
        └─ QMetaSequence::Iterable::Iterator
             └─ operator*() -> QVariant 引用代理

QIterable<QMetaAssociation>
        └─ QMetaAssociation::Iterable::Iterator
             ├─ key()
             └─ operator*() -> mapped value 引用代理
```

因此 `QIterable::mutableBegin()` 的返回类型可以移动位置，但元素访问的具体类型由派生 iterable 决定。

### 8.2 const iterator 和 mutable iterator

```cpp
auto readIt = iterable.constBegin();
auto writeIt = iterable.mutableBegin();
```

- `constBegin()` 返回 `QConstIterator<Container>` 基类对象；
- `mutableBegin()` 返回 `QIterator<Container>` 基类对象；
- 在 `QMetaSequence::Iterable` 等具体类中，它们被包装成带 `operator*()` 的派生 iterator；
- const iterator 不应修改元素；
- mutable iterator 依赖可写底层容器和对应元操作。

### 8.3 迭代器失效

`QIterable` 不改变底层容器的迭代器失效规则：

- `QVector` 扩容可能使已有 iterator 失效；
- `QList`、`QMap`、`QHash` 的失效规则由具体容器决定；
- `clear()` 会使原有位置通常全部失效；
- 通过 mutable iterator 修改容器结构时，不要继续使用受影响的旧 iterator；
- 替换或销毁被包装的容器后，iterable 和 iterator 都不能继续使用。

## 9. `size()` 的 Qt 6.11 边界

`size()` 直接回答“底层容器有多少个值”，返回 `qsizetype`：

```cpp
const qsizetype count = iterable.size();
```

### 9.1 有原生 size 时

如果元容器有原生 size 操作，`size()` 直接转发到它，通常是最可靠且最高效的路径。

### 9.2 没有原生 size 时

Qt 6.11 仍可能通过 const iterator 合成 size：

```text
constBegin()
        +
constEnd()
        +
迭代器距离
        =
size()
```

官方文档已经把这条兼容路径标记为 deprecated。它可能：

- 需要遍历或计算迭代器距离；
- 比原生 `size()` 慢；
- 依赖底层 iterator 能力；
- 发出 Qt 关于合成访问的警告。

在 Qt 7 中，如果底层没有原生 size，文档计划直接返回 `-1`，而不再替调用方猜测容器大小。

因此，不要把 `size()` 无条件当作低成本操作：

```cpp
const qsizetype count = iterable.size();
if (count < 0) {
    // 元容器没有可用的原生 size
}
```

如果算法只需要遍历，直接遍历可能比先调用 `size()` 再遍历更自然。

## 10. `clear()` 的修改边界

`clear()` 会把清空操作转发给元容器：

```cpp
iterable.clear();
```

它有三个前提：

1. iterable 必须持有可写底层对象；
2. 元容器描述器必须提供 clear 能力；
3. 真实容器在调用期间必须仍然存活。

可以通过 `metaContainer().canClear()` 检查描述器能力：

```cpp
if (iterable.metaContainer().canClear()) {
    iterable.clear();
}
```

`clear()`：

- 修改真实容器，而不是清空一个内部副本；
- 不会返回被删除的元素；
- 不会自动让外部保存的 iterator 失效通知；
- 不适合对 const view 调用；
- 不解决底层容器并发访问问题。

## 11. 逐项 API 说明

### `QIterable(const Container &metaContainer, const T *p)`

**作用：** 用元容器描述器和 const 对象指针构造只读 iterable 视图。

**关键语义：**

- `metaContainer` 描述如何操作真实容器；
- `p` 指向真实容器对象；
- const 属性会被保留；
- 不复制 `*p`。

**边界：**

- `p` 必须在整个 iterable 和其 iterator 生命周期内有效；
- `Container` 描述器必须与 `T` 的实际容器布局和操作协议匹配；
- 不能通过这个视图取得合法 mutable iterator；
- 不要传入临时对象地址。

### `QIterable(const Container &metaContainer, T *p)`

**作用：** 用元容器描述器和可写对象指针构造可写 iterable 视图。

**关键语义：**

- 允许 `mutableBegin()`、`mutableEnd()` 和 `clear()` 尝试使用可写对象；
- 具体元素是否可写仍由元容器接口决定；
- iterable 只借用 `p`，不负责释放。

**边界：**

- 可写指针不代表所有元操作都存在；
- 需要先确认相应的 iterator 或 clear 能力；
- 底层容器重分配可能使已有 iterator 失效；
- 不要把指针指向生命周期即将结束的局部对象。

### `QIterable(const Container &metaContainer, Pointer iterable)`

**作用：** 用一个可被 `QConstPreservingPointer` 接受的指针类型构造视图。

**关键语义：**

- 这是类型擦除层使用的通用构造入口；
- 可以让具体派生 iterable 接受不同形式的底层指针；
- const 和 mutable 访问属性会通过指针类型保留。

**边界：**

- `Pointer` 必须真正指向与 `metaContainer` 匹配的容器；
- 这是框架适配接口，不是把任意地址转换成容器的安全机制；
- 类型不匹配可能导致未定义行为；
- 不要把内部擦除指针当成所有权指针。

### `QIterable(const Container &metaContainer, qsizetype alignment, const void *p)`

**作用：** 用带对齐信息的 const 擦除指针构造 iterable。

**关键语义：**

- 主要服务于元类型存储和类型擦除路径；
- `alignment` 帮助 Qt 保存擦除对象的对齐信息；
- const 属性被保留。

**边界：**

- 普通业务代码通常不需要直接调用；
- `p` 必须来自 Qt 能正确解释的元类型存储；
- 错误的地址、类型或对齐信息不能靠编译器检查；
- 只能使用 const 访问路径。

### `QIterable(const Container &metaContainer, qsizetype alignment, void *p)`

**作用：** 用带对齐信息的可写擦除指针构造 iterable。

**关键语义：**

- 主要供 Qt 元容器和元类型实现；
- 允许底层元操作使用可写地址；
- 仍然不拥有这块存储。

**边界：**

- 只有在确实掌握 Qt 元类型存储协议时才应使用；
- `alignment`、对象类型和生命周期必须完全匹配；
- 错误的擦除地址可能在迭代、clear 或析构 iterator 时崩溃；
- 普通代码优先使用 `QMetaSequence::Iterable(meta, &container)` 这类具体构造。

### `bool canInputIterate() const`

**作用：** 判断底层是否具有 input iterator 能力。

**关键语义：**

- 对应 `std::input_iterator_tag`；
- 只说明可以进行基本输入方向遍历；
- 更强的 forward、bidirectional、random access 能力也会满足 input 层级。

**边界：**

- 不保证底层指针有效；
- 不保证随机访问；
- 不保证 `size()` 一定能低成本获得；
- 不能用它判断元素是否可写。

### `bool canForwardIterate() const`

**作用：** 判断底层是否可以按 forward iterator 语义向前遍历。

**关键语义：**

- 对应 `std::forward_iterator_tag`；
- 可用于选择允许重复遍历或需要更强迭代保证的算法；
- random access 和 bidirectional iterator 通常也满足它。

**边界：**

- 不表示可以 `--`；
- 不表示可以 `it + n`；
- 不表示移动一定是常数时间；
- 仍需使用具体 iterable 的正确 iterator 类型。

### `bool canReverseIterate() const`

**作用：** 判断底层是否具有 bidirectional iterator 能力，可以向后移动。

**关键语义：**

- Qt 名称使用 `canReverseIterate()`；
- 实际对应 `std::bidirectional_iterator_tag`；
- 适合判断是否能安全使用 `--it`、`it--`。

**边界：**

- 不表示容器已经反向排列；
- 不表示有独立的 reverse iterator；
- 不表示随机跳跃；
- random access 之前也会具备 bidirectional 能力。

### `bool canRandomAccessIterate() const`

**作用：** 判断底层是否具有 random access iterator 能力。

**关键语义：**

- 对应 `std::random_access_iterator_tag`；
- 表示可以高效跳过多个位置和计算 iterator 距离；
- 适合选择 `it += n`、`it + n`、`end - begin` 一类算法。

**边界：**

- 不表示 iterable 提供 `at()`；
- 不表示 `size()` 一定使用原生 size；
- 不能替代对具体 iterator 操作前置条件的检查；
- 关联容器通常不应假设随机访问。

### `QConstIterator<Container> constBegin() const`

**作用：** 返回底层容器开头的只读擦除迭代器。

**关键语义：**

- 通过 `metaContainer.constBegin()` 创建底层 iterator；
- 返回的基类 iterator 负责位置操作；
- 具体 iterable 的派生 const iterator 会补上元素读取接口；
- 适合 STL 风格的 `begin != end` 遍历。

**边界：**

- 真实容器和 iterable 必须在 iterator 生命周期内存活；
- 底层必须支持 const iterator；
- 只读 iterator 不应修改元素；
- 容器结构变化可能使它失效。

### `QConstIterator<Container> constEnd() const`

**作用：** 返回底层容器末尾位置的只读擦除迭代器。

**关键语义：**

- 通过 `metaContainer.constEnd()` 创建；
- 只能用于与同一 iterable 的 const iterator 比较；
- end 位置本身不能解引用。

**边界：**

- 不要解引用 end；
- 不要拿不同 iterable 或不同底层容器的 end 比较；
- 底层容器变化后 end 也可能失效；
- 没有 const iterator 能力时不能假设调用安全。

### `QIterator<Container> mutableBegin()`

**作用：** 返回底层容器开头的可写擦除迭代器。

**关键语义：**

- 通过 `metaContainer.begin()` 创建可写 iterator；
- 具体 iterable 的派生 iterator 提供元素读写代理；
- 只对从可写底层对象构造的视图有意义。

**边界：**

- const 指针构造的 iterable 没有合法可写对象；
- 底层必须提供 mutable iterator；
- 具体元素是否可赋值取决于元容器接口；
- 不要在容器结构变化后继续使用旧 iterator。

### `QIterator<Container> mutableEnd()`

**作用：** 返回底层容器末尾位置的可写擦除迭代器。

**关键语义：**

- 用于和 `mutableBegin()` 返回的同一 iterable iterator 比较；
- end 位置本身不能解引用；
- 可作为需要范围终点的可写遍历边界。

**边界：**

- const 底层对象不能提供合法 mutable end；
- 不要跨 iterable 比较；
- 底层容器改变后 end 可能失效；
- end 位置不能用于写入元素。

### `qsizetype size() const`

**作用：** 返回底层容器元素数量。

**关键语义：**

- 优先调用元容器提供的原生 size；
- Qt 6.11 中没有原生 size 时可能用迭代器合成；
- 合成路径可能发出警告；
- 未来 Qt 7 对无原生 size 的情况计划返回 `-1`。

**边界：**

- 不要无条件假设是 O(1)；
- 返回负值时不能当作正常元素数量；
- 空 iterable 和真实的空容器都可能需要结合元容器状态判断；
- 底层容器必须在调用期间有效。

### `void clear()`

**作用：** 清空底层容器。

**关键语义：**

- 通过 `metaContainer.clear(mutableIterable())` 转发；
- 修改真实容器，不创建新容器；
- 没有返回值；
- 适合元容器描述器已知支持 clear 的可写视图。

**边界：**

- const 视图不能合法清空；
- 先用 `metaContainer().canClear()` 检查能力；
- 调用后已有 iterator 通常失效；
- 不会通知其它持有同一底层容器的 view；
- 线程安全由真实容器和调用方负责。

### `Container metaContainer() const`

**作用：** 返回当前 iterable 使用的元容器描述器。

**关键语义：**

- 返回的是描述器值，不是底层真实容器；
- 可用于查询 `hasSize()`、`canClear()`、`hasConstIterator()` 等能力；
- 对 `QMetaSequence::Iterable` 返回 `QMetaSequence`；
- 对 `QMetaAssociation::Iterable` 返回 `QMetaAssociation`。

示例：

```cpp
const auto metaContainer = iterable.metaContainer();

if (metaContainer.hasConstIterator()) {
    // 可以创建 constBegin/constEnd
}

if (metaContainer.canClear()) {
    // 可进一步考虑 clear，但仍需确认 view 可写
}
```

**边界：**

- 它不返回真实容器地址；
- 不能从描述器推断底层对象仍然存活；
- 描述器能力存在不代表当前视图一定可写；
- 不要把它当成业务容器本身。

## 12. 典型使用模式

### 12.1 只读访问未知顺序容器

```cpp
template <typename Iterable>
void printValues(const Iterable &iterable)
{
    for (auto it = iterable.constBegin();
         it != iterable.constEnd();
         ++it) {
        qDebug() << *it;
    }
}
```

这个模板不需要知道底层是 `QList<int>`、`QVector<QString>` 还是其它已注册顺序容器，但要求具体 iterable 的 const iterator 提供相应解引用语义。

### 12.2 根据能力选择算法

```cpp
template <typename Iterable>
qsizetype countValues(const Iterable &iterable)
{
    if (iterable.canRandomAccessIterate()) {
        return iterable.size();
    }

    qsizetype count = 0;
    for (auto it = iterable.constBegin();
         it != iterable.constEnd();
         ++it) {
        ++count;
    }
    return count;
}
```

在 Qt 6.11 中，若底层没有原生 size，这个例子仍可能触发 `size()` 的兼容性回退；真正追求稳定性能时，还应先检查元容器是否有 `hasSize()`。

### 12.3 只在可写视图上修改

```cpp
QMetaSequence::Iterable iterable(meta, &values);

if (iterable.metaContainer().canClear()) {
    iterable.clear();
}
```

如果 `iterable` 是用 `const QList<int> *` 构造的，即使 `metaContainer().canClear()` 为 true，也不能把它当成可写视图。

## 13. 常见误区

### 13.1 以为 `QIterable` 自己就是完整容器

**现象：** 直接把 `QIterable<QMetaSequence>` 当成能 `operator*()` 的普通 range。

**原因：** `QIterable` 是迭代基础，元素解引用通常由 `QMetaSequence::Iterable` 等派生类提供。

**处理：** 使用具体 iterable 和具体 iterator，或使用 Qt 元容器提供的现代接口。

### 13.2 以为它复制了底层容器

**现象：** 原容器销毁或替换后，仍继续使用 iterable。

**原因：** iterable 保存的是借用指针，不是容器副本。

**处理：** 让真实容器、iterable 和 iterator 的生命周期明确重叠。

### 13.3 从临时对象创建 iterable

**现象：** 函数返回一个 iterable，调用方遍历时崩溃。

**原因：** iterable 指向局部容器或临时对象。

**处理：** 让容器由调用方持有，或者返回拥有实际数据的对象而不是借用 view。

### 13.4 只看 `canRandomAccessIterate()` 就认为 `size()` O(1)

**现象：** 性能测试发现 `size()` 触发迭代器路径。

**原因：** 随机访问能力和原生 size 能力是两个不同的元信息。

**处理：** 使用 `iterable.metaContainer().hasSize()` 检查原生 size 支持。

### 13.5 用 const 指针构造后调用可写 API

**现象：** `mutableBegin()` 或 `clear()` 没有有效底层对象。

**原因：** `QIterable` 保留了构造时的 const 属性。

**处理：** 需要修改时从可写对象构造，并确认元容器提供对应操作。

### 13.6 迭代期间改变底层容器

**现象：** iterator 比较、递增或解引用时崩溃或读取错误。

**原因：** 底层容器的结构修改使 native iterator 失效。

**处理：** 迭代期间不要做可能重分配、删除节点或清空容器的操作；必要时先复制需要的数据。

### 13.7 用不同 iterable 的 iterator 互相比较

**现象：** `it != other.end()` 得到不可靠结果。

**原因：** iterator 只能与同一底层容器、同一 iterable 坐标体系中的端点比较。

**处理：** 总是用同一个 iterable 创建 begin 和 end。

### 13.8 把 `canReverseIterate()` 理解成有 reverse container

**现象：** 直接寻找 `rbegin()` 或以为遍历顺序已经反转。

**原因：** 该函数只报告 bidirectional iterator 能力。

**处理：** 使用 `constEnd()` 后递减，或由具体 iterable/算法自行构造反向遍历。

## API 速查表
| API | 类型 | 作用 | 使用重点 |
| --- | --- | --- | --- |
| `QIterable(metaContainer, const T *)` | 构造函数 | 创建只读类型擦除视图 | 不复制对象；const 属性被保留 |
| `QIterable(metaContainer, T *)` | 构造函数 | 创建可写类型擦除视图 | 是否能写还取决于元容器能力 |
| `QIterable(metaContainer, Pointer)` | 构造函数 | 用通用指针构造视图 | 指针类型必须与描述器匹配 |
| `QIterable(metaContainer, alignment, const void *)` | 构造函数 | 用带对齐信息的 const 擦除地址构造 | 主要面向元类型内部；普通代码少用 |
| `QIterable(metaContainer, alignment, void *)` | 构造函数 | 用带对齐信息的可写擦除地址构造 | 地址、对齐、生命周期必须准确 |
| `canInputIterate()` | 能力查询 | 是否有 input iterator 能力 | 只保证基本输入方向遍历 |
| `canForwardIterate()` | 能力查询 | 是否有 forward iterator 能力 | 不代表可后退或随机访问 |
| `canReverseIterate()` | 能力查询 | 是否有 bidirectional 能力 | 可后退，不等于有 reverse iterator |
| `canRandomAccessIterate()` | 能力查询 | 是否有随机访问能力 | 不等于原生 `size()` 或 `at()` |
| `constBegin()` | 迭代器 | 创建只读 begin | 真实容器和 iterable 必须存活 |
| `constEnd()` | 迭代器 | 创建只读 end | end 不能解引用；只能比较同源 iterator |
| `mutableBegin()` | 迭代器 | 创建可写 begin | 需要可写 view 和 mutable iterator |
| `mutableEnd()` | 迭代器 | 创建可写 end | const view 不能提供合法可写端点 |
| `size()` | 查询 | 返回元素数量 | Qt 6.11 可能合成；未来无原生 size 可为 `-1` |
| `clear()` | 修改 | 清空真实底层容器 | 检查 `canClear()`；已有 iterator 通常失效 |
| `metaContainer()` | 查询 | 返回元容器描述器 | 不是实际容器；可查询底层能力 |

## 15. 一句话总结

`QIterable<Container>` 是 Qt 运行时容器反射的类型擦除底座：它保存元容器操作协议和一个借用的真实容器指针，把底层 native iterator 包装成统一的只读/可写迭代入口。实际使用时优先从 `QMetaSequence::Iterable` 或 `QMetaAssociation::Iterable` 获取它，始终让真实容器和 iterable 活得比 iterator 久，并在使用跳跃、后退、`size()` 或 `clear()` 前检查对应能力。
