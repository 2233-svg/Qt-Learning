# Qt QMetaContainer 类型擦除容器能力笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMetaContainer>`  
> 所属模块：`Qt6::Core`  
> 类型性质：为元容器提供 iterator、size 和 clear 操作描述的基类  
> 派生类型：`QMetaSequence`、`QMetaAssociation`  
> 相关类型：`QIterable`、`QIterator`、`QConstIterator`、`QMetaType`

## 1. 它解决什么问题

`QMetaContainer` 是 Qt 运行时容器反射体系的共同底座。它不保存元素，而是保存一张“如何操作某种容器”的类型擦除接口表：

```text
具体容器的 native API
QList<T> / QMap<K, V> / 自定义可识别容器
        |
        v
QMetaSequence 或 QMetaAssociation
        |
        v
QMetaContainer
        |
        +-- iterator 能力
        +-- begin/end、复制、比较、移动、距离
        +-- size
        +-- clear
```

它解决的是：

- 运行时只知道“这是一个容器描述”，不知道完整 C++ 容器类型；
- 上层需要用统一的 `void *` 接口操作 native iterator；
- `QMetaSequence` 和 `QMetaAssociation` 需要共用 iterator 生命周期与能力查询；
- `QIterable` 需要把这些原始函数包装成 RAII iterator。

### 1.1 它不是什么

`QMetaContainer` 不是：

- `QList`、`QMap` 或 `std::vector` 的实例；
- 元素存储；
- 容器所有权管理器；
- 自动复制真实容器的快照；
- 保证所有操作存在的万能接口；
- 可以脱离真实容器独立遍历的 range。

它保存的是描述器和函数表。真实容器、真实 iterator 以及它们的生命周期都由调用方或更高层 `QIterable` 管理。

## 2. 实际使用场景

### 2.1 为 `QMetaSequence`/`QMetaAssociation` 提供共同能力

```cpp
QList<int> values{10, 20, 30};
const QMetaSequence sequence =
    QMetaSequence::fromContainer<QList<int>>();

const QMetaContainer &container = sequence;
if (container.hasConstIterator()) {
    // QMetaSequence::Iterable 会使用这些底层能力
}
```

应用代码通常直接使用 `QMetaSequence::Iterable` 或 `QMetaAssociation::Iterable`，而不是手工操作 `QMetaContainer` 的 `void *` iterator。

### 2.2 构建通用反射工具

通用工具可以先查询容器描述器的能力，再决定是否提供清空、计数、前进或随机跳跃：

```cpp
if (meta.hasSize())
    showSize(meta.size(container));

if (meta.canClear())
    offerClearAction();
```

能力查询必须先于原始操作。工具不能从类型名称或业务经验推断某个函数一定存在。

### 2.3 实现自定义 `QIterable` 适配

如果要实现或分析 Qt 的类型擦除迭代层，需要理解：

- `begin()`/`end()` 负责创建 native iterator；
- `copyIterator()` 负责把一个已创建 iterator 的位置复制到另一个；
- `destroyIterator()` 负责释放由描述器创建的 iterator；
- `QIterator` 和 `QConstIterator` 依赖这些函数实现 RAII。

这是元容器基础设施代码的使用场景，普通业务代码不应直接伪造这些调用。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QMetaContainer>
#include <QMetaSequence>
#include <QList>
#include <QDebug>
```

`QMetaContainer` 位于 `Qt6::Core`。实际使用时通常还要包含具体派生元容器和真实容器的头文件。

## 4. 三层对象模型

### 4.1 真实容器

```cpp
QList<int> values{1, 2, 3};
```

它拥有元素和 native iterator。

### 4.2 元描述器

```cpp
const QMetaSequence meta =
    QMetaSequence::fromContainer<QList<int>>();
```

`QMetaSequence`/`QMetaAssociation` 内部包含一个 `QMetaContainer` 风格的接口描述，并从 `QMetaContainer` 继承公共能力。

### 4.3 类型擦除视图

```cpp
QMetaSequence::Iterable iterable(meta, &values);
```

`Iterable` 保存真实容器的借用指针，并使用 `QMetaContainer` 创建、移动和销毁擦除 iterator。视图不拥有 `values`，也不自动防止 `values` 失效。

## 5. 能力层次和检查规则

### 5.1 iterator 能力是逐级的

Qt 依据底层 iterator 的 `std::iterator_traits<Iterator>::iterator_category` 构造能力：

```text
random access
    -> bidirectional
        -> forward
            -> input
```

因此一个 random access iterator 通常也报告更低级别的能力。反过来，input iterator 不保证可以后退、跳跃或计算高效距离。

| 查询 | 表示 |
| --- | --- |
| `hasInputIterator()` | 至少可以按 input 语义前进 |
| `hasForwardIterator()` | 支持 forward 迭代要求 |
| `hasBidirectionalIterator()` | 支持前进和后退 |
| `hasRandomAccessIterator()` | 支持随机访问和距离运算的更强语义 |

这些函数描述底层能力，不会验证当前传入的某个 iterator 是否仍然有效。

### 5.2 原生 size 与 iterator 能力独立

一个容器可以：

- 有 `size()` 但没有 iterator；
- 有 iterator 但没有原生 `size()`；
- 两者都支持；
- 两者都不支持。

不要用 `hasRandomAccessIterator()` 推断 `hasSize()`，也不要用 `hasSize()` 推断可以创建 iterator。

### 5.3 操作存在不等于参数有效

`hasIterator()` 或 `canClear()` 只说明函数表中存在相应函数。调用时仍要保证：

- `container` 指向正确的真实容器类型；
- const/非 const 资格匹配；
- iterator 来自同一描述器和同一真实容器；
- iterator 没有因容器修改而失效；
- step 和距离在底层 iterator 的允许范围内。

## 6. 描述器和默认状态

### 6.1 默认构造

```cpp
const QMetaContainer invalid;
```

默认构造的描述器没有函数表。能力查询返回 false；原始操作不应被调用。它不是一个“空但可操作的容器”。

### 6.2 派生描述器提供有效接口

```cpp
const QMetaSequence sequence =
    QMetaSequence::fromContainer<QList<int>>();
const QMetaContainer &meta = sequence;
```

`QMetaSequence` 和 `QMetaAssociation` 的 `fromContainer<T>()` 创建静态接口表。`QMetaContainer` 主要通过基类视角提供共用 iterator/size/clear 能力。

### 6.3 显式接口指针构造

头文件提供了接受内部 `QMetaContainerInterface *` 的显式构造函数，但这个类型位于 `QtMetaContainerPrivate` 命名空间，主要面向 Qt 自身和派生描述器实现：

```cpp
explicit QMetaContainer(
    const QtMetaContainerPrivate::QMetaContainerInterface *d);
```

普通应用不应手工构造内部函数表，也不应把自定义函数指针随意填入，否则很容易破坏 `void *` 类型和 iterator 生命周期契约。

## 7. 逐项 API：能力、大小和清空

### 7.1 `hasInputIterator() const`

```cpp
bool hasInputIterator() const;
```

报告底层是否提供至少 input 级别的 const 或可写 iterator 能力。它只说明可以按 input iterator 规则前进，不能据此调用 `--`、`+ n` 或高效 `operator-`。

### 7.2 `hasForwardIterator() const`

```cpp
bool hasForwardIterator() const;
```

报告是否支持 forward iterator 能力。forward iterator 可以多次遍历并复制，但仍不保证支持后退或随机跳跃。

### 7.3 `hasBidirectionalIterator() const`

```cpp
bool hasBidirectionalIterator() const;
```

报告是否可以前进和后退。只有在该能力存在时，才应让上层代码依赖 `--iterator` 或负 step。

### 7.4 `hasRandomAccessIterator() const`

```cpp
bool hasRandomAccessIterator() const;
```

报告底层 iterator 是否具有随机访问能力。它支持更强的跳跃和距离语义，但不意味着底层 `size()` 一定存在，也不意味着所有 `void *` 参数都自动安全。

### 7.5 `hasSize() const`

```cpp
bool hasSize() const;
```

报告描述器是否拥有原生 `size` 函数。只有返回 true 时，才应直接调用 `size(container)` 获取原生大小。

`QIterable::size()` 在 Qt 6.11 还可以在没有原生 size 时尝试通过 const iterator 合成大小，并可能发出合成访问警告；这是 `QIterable` 的上层策略，不是 `QMetaContainer::hasSize()` 的含义。

### 7.6 `size(const void *container) const`

```cpp
qsizetype size(const void *container) const;
```

调用描述器的原生 size 函数，读取真实容器大小：

```cpp
if (meta.hasSize())
    const qsizetype n = meta.size(&values);
```

使用边界：

- 先检查 `hasSize()`；
- `container` 必须指向与描述器匹配的真实类型；
- 只读指针足以查询大小；
- 返回值是 `qsizetype`，不要随意缩窄成 `int`；
- 没有原生 size 时不要把返回值当作可靠大小，应改用 `QIterable::size()` 或自己的遍历策略。

### 7.7 `canClear() const`

```cpp
bool canClear() const;
```

报告是否有可写的 clear 函数。它不表示当前容器为空，也不表示清空操作不会使 iterator 失效。

### 7.8 `clear(void *container) const`

```cpp
void clear(void *container) const;
```

调用底层容器的 `clear()`：

```cpp
if (meta.canClear())
    meta.clear(&values);
```

调用前需要：

- 真实容器是非 const；
- `container` 地址和描述器的 `T` 匹配；
- 不再使用清空前创建的 iterator；
- 已经取得的元素引用、QVariant proxy 或指针不再被使用。

如果没有 clear 能力，不能把“调用后没崩溃”当作清空成功。

## 8. 逐项 API：可写 iterator

### 8.1 `hasIterator() const`

```cpp
bool hasIterator() const;
```

报告是否可以创建可写 native iterator。通常要求真实容器类型有可写 `iterator`，而 const 容器或只提供 `const_iterator` 的描述器可能只有 `hasConstIterator()`。

### 8.2 `begin(void *container) const`

```cpp
void *begin(void *container) const;
```

为真实容器创建一个位于 begin 的擦除 iterator，并返回不透明指针：

```cpp
void *it = meta.begin(&values);
```

它不是返回第一个元素地址，而是返回 native iterator 对象的擦除地址。调用完成后必须使用同一描述器的 `destroyIterator()` 销毁。

边界：

- 先检查 `hasIterator()`；
- `container` 必须可写且类型匹配；
- 空容器的 begin 可能等于 end，不能解引用；
- 真实容器修改可能使 iterator 失效。

### 8.3 `end(void *container) const`

```cpp
void *end(void *container) const;
```

为真实可写容器创建 end iterator。end 只能比较，不能解引用或读取元素。它同样需要用 `destroyIterator()` 配对释放。

### 8.4 `destroyIterator(const void *iterator) const`

```cpp
void destroyIterator(const void *iterator) const;
```

释放由 `begin()`、`end()` 或其他同类 raw API 创建的可写 iterator。必须满足：

- iterator 是由同一 `QMetaContainer` 描述器创建；
- iterator 尚未被销毁；
- 真实容器仍满足底层 iterator 析构要求。

不要对普通 C++ iterator 直接传地址，也不要用 `delete` 替代它。

### 8.5 `compareIterator(const void *i, const void *j) const`

```cpp
bool compareIterator(const void *i,
                     const void *j) const;
```

比较两个同源可写 iterator 是否处于相同位置：

```cpp
const bool atEnd = meta.compareIterator(it, end);
```

`i` 和 `j` 必须来自同一描述器、同一真实容器和相容的 iterator 类型。比较不同容器、不同描述器或已失效 iterator 不受支持。

### 8.6 `copyIterator(void *target, const void *source) const`

```cpp
void copyIterator(void *target,
                  const void *source) const;
```

把 source 的 native iterator 位置复制到已经存在的 target iterator 中。它不是分配 target，也不是复制真实容器：

```text
先创建 target
再 copyIterator(target, source)
```

`QIterator` 的复制构造会使用这个 API。原始调用方必须保证 target 已由同一描述器创建并有可写 iterator 存储。

### 8.7 `advanceIterator(void *iterator, qsizetype step) const`

```cpp
void advanceIterator(void *iterator,
                     qsizetype step) const;
```

让可写 iterator 向前或向后移动指定步数：

```cpp
meta.advanceIterator(it, 1);
```

边界：

- 正 step 通常表示向后移动；
- 负 step 需要 bidirectional 能力；
- 超出 begin/end 合法范围的移动具有底层 iterator 的未定义或未支持风险；
- input/forward iterator 上的大 step 可能是线性复杂度；
- 不能对 null、已销毁或已失效 iterator 调用。

### 8.8 `diffIterator(const void *i, const void *j) const`

```cpp
qsizetype diffIterator(const void *i,
                       const void *j) const;
```

计算从 `j` 到 `i` 的距离，语义对应 `i - j`：

```cpp
const qsizetype distance =
    meta.diffIterator(it, begin);
```

两个 iterator 必须同源。距离的复杂度和适用范围由底层 iterator 决定；不要把它无条件当作 O(1) 随机访问操作。

## 9. 逐项 API：只读 iterator

### 9.1 `hasConstIterator() const`

```cpp
bool hasConstIterator() const;
```

报告是否能创建只读 native iterator。只读 iterator 可以来自 const 容器，也可以来自非 const 容器的 const 访问路径。

### 9.2 `constBegin(const void *container) const`

```cpp
void *constBegin(const void *container) const;
```

创建位于 begin 的只读擦除 iterator：

```cpp
const void *readBegin =
    meta.constBegin(&values);
```

返回类型是 `void *`，但使用语义是只读 iterator；完成后仍要调用 `destroyConstIterator()`，不能因为输入 container 是 const 就把返回指针直接当普通地址。

### 9.3 `constEnd(const void *container) const`

```cpp
void *constEnd(const void *container) const;
```

创建只读 end iterator。它只能比较，不能解引用。必须与 `destroyConstIterator()` 配对。

### 9.4 `destroyConstIterator(const void *iterator) const`

```cpp
void destroyConstIterator(const void *iterator) const;
```

释放 `constBegin()`、`constEnd()` 或其他 const iterator 创建 API 返回的对象。不要与 `destroyIterator()` 混用，因为两者可能对应不同的 native iterator 类型和析构函数。

### 9.5 `compareConstIterator(const void *i, const void *j) const`

```cpp
bool compareConstIterator(const void *i,
                          const void *j) const;
```

比较两个同源只读 iterator 是否相等。常见用途是判断遍历是否到达 const end：

```cpp
while (!meta.compareConstIterator(it, end)) {
    // 读取当前元素
    meta.advanceConstIterator(it, 1);
}
```

比较不同容器或不同描述器创建的 iterator 没有可靠语义。

### 9.6 `copyConstIterator(void *target, const void *source) const`

```cpp
void copyConstIterator(void *target,
                       const void *source) const;
```

把只读 iterator 位置复制到已创建的 target。它不会为 target 分配内存，也不会复制真实容器。target 必须是同一描述器通过 `constBegin()` 或 `constEnd()` 等 API 创建的 const iterator 存储。

### 9.7 `advanceConstIterator(void *iterator, qsizetype step) const`

```cpp
void advanceConstIterator(void *iterator,
                          qsizetype step) const;
```

移动只读 iterator。负 step 需要 bidirectional 能力，越界移动不受支持。只读不等于可以忽略底层 iterator 的失效规则；真实容器修改仍可能使 const iterator 失效。

### 9.8 `diffConstIterator(const void *i, const void *j) const`

```cpp
qsizetype diffConstIterator(const void *i,
                            const void *j) const;
```

计算只读 iterator 从 `j` 到 `i` 的距离。需要同源 iterator，复杂度由底层 iterator 决定。它不用于比较两个不同容器的偏移。

## 10. `QIterable` 如何使用这些 API

### 10.1 `QIterable` 负责 RAII 包装

`QIterable<Container>` 会在构造 iterator 时调用 `begin()`/`constBegin()`，在 iterator 析构时调用对应 destroy 函数，并使用 copy/compare/advance/diff 实现 C++ 迭代器接口。

因此推荐写法是：

```cpp
QMetaSequence::Iterable iterable(
    QMetaSequence::fromContainer<QList<int>>(),
    &values);

for (auto it = iterable.constBegin();
     it != iterable.constEnd(); ++it) {
    qDebug() << *it;
}
```

而不是把 `void *` 指针直接暴露到业务层。

### 10.2 `QIterable::size()` 的 Qt 6.11 行为

如果描述器有原生 `size()`，`QIterable::size()` 直接调用它。如果没有，Qt 6.11 仍可能通过 const begin/end 和距离计算合成大小，并发出合成访问警告。这个 fallback 可能：

- 需要完整 const iterator；
- 需要遍历或距离计算；
- 比原生 size 慢；
- 在 Qt 7 行为上有所变化。

因此对性能敏感的代码应优先检查 `meta.hasSize()`。

### 10.3 `QTaggedIterator` 的能力检查

`QMetaSequence::Iterable` 和 `QMetaAssociation::Iterable` 会根据底层 `QMetaContainer` 的能力构造 iterator 标签。若代码请求 random access/bidirectional 级别，但底层不支持，Qt 会进入 fatal 路径，而不是默默降级成较弱 iterator。

普通代码用 `auto` 和实际提供的 `begin()`/`find()`，不要手工把普通 iterator 强转成更强的标签类型。

## 11. 生命周期、失效和线程边界

### 11.1 描述器不拥有真实容器

```cpp
QMetaSequence meta =
    QMetaSequence::fromContainer<QList<int>>();
```

`meta` 可以复制和返回，但复制只复制描述器指针，不复制 `QList`。真实容器必须在 iterable/iterator 使用期间存活。

### 11.2 容器修改可能使所有 iterator 失效

以下操作通常应视为会使当前 iterator 失效，除非真实容器文档另有保证：

- `clear()`；
- 插入或删除；
- 可能重新分配存储的增长操作；
- 关联容器的节点删除；
- 让真实容器离开作用域或移动。

失效 iterator 不能继续比较、复制、移动、解引用或销毁以外地使用。

### 11.3 iterator 只与同源 iterator 比较

```cpp
auto first = meta.begin(&a);
auto otherEnd = meta.end(&b);
// 不要比较 first 和 otherEnd
```

即使 `a` 和 `b` 是相同类型，native iterator 也属于不同真实容器。必须使用同一个容器地址创建 begin/end。

### 11.4 多线程访问由调用方同步

`QMetaContainer` 的描述器函数表通常是静态只读数据，但它不为真实容器提供并发安全。多个线程共享真实容器时，必须自行同步读写和 iterator 生命周期。

## 12. 常见错误与排查顺序

### 12.1 把描述器当成真实容器

**症状：** 创建 `QMetaContainer` 后希望从对象中读出元素。

**原因：** 描述器只保存类型擦除操作，不保存元素。

**修复：** 同时持有真实容器，并把其地址传给 `QMetaSequence::Iterable` 或 raw API。

### 12.2 跳过能力检查

**症状：** `begin()` 返回空指针，或 `clear()` 没有作用。

**原因：** 底层容器未提供对应函数表槽位。

**修复：** 先检查 `hasIterator()`、`hasConstIterator()`、`canClear()` 和其他相关能力。

### 12.3 用错误的 destroy 函数

**症状：** 释放 iterator 时崩溃或堆损坏。

**原因：** 可写 iterator 和 const iterator 的创建/销毁函数不同。

**修复：** `begin/end` 配 `destroyIterator`，`constBegin/constEnd` 配 `destroyConstIterator`。

### 12.4 把 `copyIterator` 当成分配函数

**症状：** target 是未初始化内存就调用复制。

**原因：** `copyIterator` 只把位置写入已经构造的 native iterator，不负责 placement new 或分配。

**修复：** 先用同一描述器创建 target，再复制 source 位置；业务代码直接使用 `QIterator`。

### 12.5 对 end iterator 解引用

**症状：** 读取空容器或遍历结束位置时崩溃。

**原因：** end 只用于比较，不代表有效元素。

**修复：** 先比较 iterator 和 end，再读取元素。

### 12.6 对 forward/input iterator 使用负 step

**症状：** 后退时得到错误结果或未定义行为。

**原因：** 底层 iterator 不支持 bidirectional 语义。

**修复：** 检查 `hasBidirectionalIterator()`，或只使用 `++`。

### 12.7 假设 diff 一定是 O(1)

**症状：** 大容器上计算距离很慢。

**原因：** `std::distance` 对非随机访问 iterator 可能线性遍历。

**修复：** 对性能敏感路径检查 `hasRandomAccessIterator()`，或使用原生 size。

### 12.8 清空后继续使用旧 iterator

**症状：** 比较或解引用行为异常。

**原因：** `clear()` 会使 iterator 和元素引用失效。

**修复：** 清空后丢弃所有旧 iterator，需要遍历时重新创建。

### 12.9 把 QIterable 的 size fallback 当成原生能力

**症状：** `iterable.size()` 在某些类型上比预期慢或发出警告。

**原因：** 描述器没有 `sizeFn`，Qt 6.11 通过迭代器合成大小。

**修复：** 先看 `meta.hasSize()`，对无原生 size 的容器按实际复杂度设计。

## 13. 推荐设计模板

### 13.1 优先使用高层 iterable

```cpp
template <typename Container>
void dumpContainer(const Container &container)
{
    QMetaSequence::Iterable view(&container);
    for (auto it = view.constBegin();
         it != view.constEnd(); ++it) {
        qDebug() << *it;
    }
}
```

高层 iterable 自动管理擦除 iterator 的销毁，减少手工配对错误。

### 13.2 raw API 的最小安全循环

```cpp
void inspectRaw(const QMetaContainer &meta,
                const void *container)
{
    if (!meta.hasConstIterator())
        return;

    void *current = meta.constBegin(container);
    void *end = meta.constEnd(container);
    if (!current || !end)
        return;

    while (!meta.compareConstIterator(current, end)) {
        // 使用派生 QMetaSequence/QMetaAssociation 读取当前值
        meta.advanceConstIterator(current, 1);
    }

    meta.destroyConstIterator(current);
    meta.destroyConstIterator(end);
}
```

真实代码还应检查底层 iterator 是否支持前进、保证容器在整个循环期间不被修改，并使用派生描述器的 value/key API 读取元素。

### 13.3 原生 size 优先，fallback 明确

```cpp
qsizetype containerSize(const QIterable<QMetaSequence> &view)
{
    const QMetaSequence meta = view.metaContainer();
    if (meta.hasSize())
        return meta.size(view.constIterable());

    return view.size(); // Qt 6.11 可能合成并产生警告
}
```

如果项目不希望触发合成访问，应在 `hasSize()` 为 false 时返回“未知”或采用业务专用计数策略。

## API 速查表
### 14.1 能力和大小

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `hasInputIterator()` | 查询 input iterator 能力 | 不保证后退或随机访问 |
| `hasForwardIterator()` | 查询 forward iterator 能力 | 不保证 bidirectional |
| `hasBidirectionalIterator()` | 查询双向迭代能力 | 负 step 需要它 |
| `hasRandomAccessIterator()` | 查询随机访问能力 | 与原生 `size()` 独立 |
| `hasSize()` | 查询原生 size 函数 | false 时不要直接依赖 `size()` |
| `size(const void *)` | 调用原生 size | 传入匹配的真实容器地址；返回 `qsizetype` |
| `canClear()` | 查询是否可清空 | 不代表 iterator 不会失效 |
| `clear(void *)` | 清空真实容器 | 需要可写容器；清空后丢弃旧 iterator |

### 14.2 可写 iterator

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `hasIterator()` | 查询可写 iterator 能力 | const 容器通常不能使用 |
| `begin(void *)` | 创建可写 begin iterator | 返回擦除指针，不是元素地址 |
| `end(void *)` | 创建可写 end iterator | 只能比较，不能解引用 |
| `destroyIterator(const void *)` | 销毁可写 iterator | 必须与可写创建 API 配对 |
| `compareIterator(i, j)` | 比较同源可写 iterator | 不同容器不能比较 |
| `copyIterator(target, source)` | 复制 iterator 位置 | target 必须先创建 |
| `advanceIterator(iterator, step)` | 移动可写 iterator | 负值需要双向能力；不可越界 |
| `diffIterator(i, j)` | 计算 `i - j` 距离 | 复杂度随底层 iterator 能力变化 |

### 14.3 只读 iterator

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `hasConstIterator()` | 查询只读 iterator 能力 | 只读不等于容器生命周期自动延长 |
| `constBegin(const void *)` | 创建只读 begin iterator | 返回擦除指针；需配对销毁 |
| `constEnd(const void *)` | 创建只读 end iterator | 只能比较，不能解引用 |
| `destroyConstIterator(const void *)` | 销毁只读 iterator | 不能和 `destroyIterator()` 混用 |
| `compareConstIterator(i, j)` | 比较同源只读 iterator | 只比较同一容器坐标系 |
| `copyConstIterator(target, source)` | 复制只读 iterator 位置 | target 必须已创建 |
| `advanceConstIterator(iterator, step)` | 移动只读 iterator | 负值需要双向能力；不可越界 |
| `diffConstIterator(i, j)` | 计算只读距离 | 非随机访问可能是线性复杂度 |

### 14.4 相关高层类型

| 类型 | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMetaSequence` | 描述顺序容器并增加 value 操作 | 继承本类的 iterator/size/clear 能力 |
| `QMetaAssociation` | 描述关联容器并增加 key/mapped 操作 | 继承本类的 iterator/size/clear 能力 |
| `QIterable<Container>` | 保存元描述器和真实容器借用指针 | 不拥有容器；负责 iterator RAII |
| `QIterator` | 可写擦除 iterator 包装 | 由 iterable 创建，不要手工伪造 |
| `QConstIterator` | 只读擦除 iterator 包装 | 底层容器修改仍可能使其失效 |

## 15. 一句话总结

`QMetaContainer` 是 Qt 元容器反射的共同操作底座：它不保存元素，只按函数表报告并执行 iterator、size、clear 能力；使用 raw `void *` API 时必须先检查能力、匹配真实容器和 iterator 类型，并严格配对创建/复制/比较/移动/销毁，普通代码则应优先使用 `QMetaSequence::Iterable` 或 `QMetaAssociation::Iterable`。
