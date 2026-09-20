# Qt QTaggedIterator 迭代器特征包装器

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTaggedIterator>`  
> 所属模块：`Qt6::Core`  
> 首次引入：Qt 6.0  
> 定位：给 Qt 元对象容器迭代器显式标注标准库 iterator category 的轻量适配器

## 它解决什么问题

`QTaggedIterator<Iterator, IteratorCategory>` 不是普通业务代码里手写循环时最常见的迭代器，而是 Qt 元对象容器体系里的适配层。`QMetaSequence::Iterable`、`QMetaAssociation::Iterable` 可以在运行期包装很多不同容器：有的只能单向读，有的支持双向移动，有的支持随机访问。标准库算法却需要在编译期通过 `std::iterator_traits` 看到 `iterator_category`。`QTaggedIterator` 的作用就是把“这一个具体迭代器实例能当作 input / forward / bidirectional / random access 迭代器使用”这件事显式贴到类型上。

它本身继承底层 `Iterator`，并暴露：

```cpp
using iterator_category = IteratorCategory;
```

因此标准库算法可以按相应能力选择实现路径；同时构造时会检查 `IteratorCategory` 与底层 `QMetaContainer` 的运行期能力是否匹配。能力不匹配不是返回一个无效对象，而是触发 Qt 的 fatal 错误；所以这类迭代器应当由 Qt 提供的别名和工厂路径取得，而不是随意给未知迭代器“强行贴标签”。

## 实际使用场景

最典型的场景是从 `QVariant` 或元类型系统里拿到一个容器视图，然后希望像 STL 迭代器一样交给通用算法。Qt 已经在相关类型里预置了别名，例如 `QMetaSequence::Iterable::InputIterator`、`ForwardIterator`、`BidirectionalIterator`、`RandomAccessIterator` 以及对应的 const 版本；这些别名底层就是 `QTaggedIterator`。

它适合：

- 元对象层代码需要遍历未知容器，但仍希望使用 `std::find`、`std::distance`、基于迭代器区间的工具函数。
- 框架、序列化、调试器、属性编辑器等代码拿到的是 `QVariant` 中的容器，而不是编译期已知的 `QList<T>` 或 `std::vector<T>`。
- 需要把 `QMetaSequence` / `QMetaAssociation` 的运行期迭代能力映射成标准 C++ 迭代器类别。

它不适合：

- 普通 `QList`、`QVector`、`std::vector` 的日常遍历；直接使用原容器迭代器更简单。
- 绕过能力检查，把不支持反向或随机访问的容器当成更强类别使用。
- 跨越容器生命周期保存迭代器。它不拥有容器，底层视图和容器失效后，迭代器也失效。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QTaggedIterator>
```

qmake 工程使用：

```qmake
QT += core
```

## 使用模型

把 `QTaggedIterator` 理解成三层关系最清楚：

1. 底层 `Iterator` 保存“当前指向哪里”和“如何前进、后退、取值”。
2. `IteratorCategory` 告诉标准库“这个迭代器承诺具备哪一级能力”。
3. 构造函数把两者对齐：如果运行期容器不支持该类别，程序会 fatal，而不是静默降级。

简化示意：

```cpp
using RawIterator = QMetaSequence::Iterable::Iterator;
using Tagged = QTaggedIterator<RawIterator, std::forward_iterator_tag>;

// 实际项目里通常使用 QMetaSequence::Iterable 提供的别名，
// 不必直接拼出 QTaggedIterator 的模板参数。
```

标准库算法的能力要求要和迭代器类别匹配。只需要单向扫描时使用 input/forward 类别；需要 `--it` 时确认容器支持双向迭代；需要 `it + n`、`it2 - it1` 或排序类算法时，必须确认底层有随机访问能力。

## 关键语义与边界

### 类别检查是运行期硬边界

构造函数会读取底层迭代器的 `metaContainer()`，并检查 `hasInputIterator()`、`hasForwardIterator()`、`hasBidirectionalIterator()`、`hasRandomAccessIterator()`。如果请求的 `IteratorCategory` 高于底层容器能力，Qt 会调用 `qFatal()`。这通常意味着程序终止；不要把它当作可以捕获或恢复的失败状态。

### 反向与随机访问不是所有容器都有

`operator--()`、`operator-=(qsizetype)`、`operator-(qsizetype)` 依赖反向迭代能力。文档明确说明：对不支持双向迭代的 `QVariant` 容器调用这些操作会产生未定义结果。`operator+(qsizetype)`、`operator-(const QTaggedIterator &)` 这类距离和偏移操作也只应在语义上支持相应能力的迭代器上使用。

### begin/end 边界遵守 STL 规则

对 end 迭代器做 `++`，或对 begin 迭代器做 `--`，都是未定义行为。`QTaggedIterator` 不会替你做边界保护，它的定位是“像标准迭代器一样工作”，不是安全游标。

### 迭代器不拥有容器

它只是包装底层迭代器。底层 `QVariant`、`QMetaSequence::Iterable`、`QMetaAssociation::Iterable` 或真实容器被销毁、被重置，或发生会使迭代器失效的结构性修改后，已有迭代器不能继续使用。

### 只比较同一序列中的迭代器

`operator==`、`operator!=` 和距离运算只应在同一容器、同一视图产生的迭代器之间使用。把两个无关容器的迭代器拿来比较，即使类型相同，也没有可靠语义。

## 常见误区

- 误以为 `QTaggedIterator` 能“提升”容器能力。它只是标注和校验能力，不能把单向容器变成随机访问容器。
- 误把构造失败当成普通错误处理。类别不匹配会 fatal，正确做法是在取得对应别名前先看容器能力，或使用 Qt 提供的合适迭代器类型。
- 在循环中修改底层容器结构后继续使用旧迭代器。是否失效取决于底层容器规则；元对象包装不会消除这个风险。
- 对 end 做自增、对 begin 做自减。这里遵循标准迭代器边界，不提供额外保护。
- 直接在业务层大量显式实例化 `QTaggedIterator`。多数时候应该使用 `QMetaSequence::Iterable`、`QSequentialIterable`、`QMetaAssociation::Iterable`、`QAssociativeIterable` 暴露的类型别名。

## 逐项 API 说明

### `QTaggedIterator(Iterator &&it)`

从一个底层迭代器或 const 迭代器移动构造带标签的迭代器。构造时会检查模板参数中的 `IteratorCategory` 是否匹配底层容器的运行期能力；如果不匹配，会触发 fatal 错误。`it` 被移动后不应再按原状态使用。

### `bool operator==(const QTaggedIterator &other) const`

判断两个迭代器是否指向同一项。只应比较来自同一容器视图的迭代器；不同容器之间没有可靠语义。

### `bool operator!=(const QTaggedIterator &other) const`

判断两个迭代器是否指向不同项，通常用于 STL 风格循环的结束条件。语义与 `operator==` 互补。

### `QTaggedIterator &operator++()`

前置自增，移动到下一项并返回移动后的自身。不能对 end 迭代器调用。

### `QTaggedIterator operator++(int)`

后置自增，移动到下一项，但返回移动前的迭代器副本。需要保留旧位置时才使用；普通循环优先用前置 `++it`。

### `QTaggedIterator &operator--()`

前置自减，移动到上一项并返回移动后的自身。底层容器必须支持双向迭代；不能对 begin 迭代器调用。

### `QTaggedIterator operator--(int)`

后置自减，移动到上一项，但返回移动前的迭代器副本。底层容器必须支持双向迭代。

### `QTaggedIterator &operator+=(qsizetype j)`

让迭代器前进 `j` 个位置并返回自身。调用前要确保偏移不会越过合法区间，并确认底层迭代器支持这种位移语义。

### `QTaggedIterator &operator-=(qsizetype j)`

让迭代器后退 `j` 个位置并返回自身。底层容器必须支持反向移动；越过 begin 属于未定义行为。

### `QTaggedIterator operator+(qsizetype j) const`

返回当前位置之后 `j` 个位置的新迭代器，不修改当前迭代器。适合随机访问或明确支持位移的场景。

### `QTaggedIterator operator-(qsizetype j) const`

返回当前位置之前 `j` 个位置的新迭代器。底层容器必须支持双向迭代；不支持时调用会产生未定义结果。

### `qsizetype operator-(const QTaggedIterator &j) const`

返回当前迭代器与 `j` 的距离。两个迭代器必须来自同一序列，并且底层迭代器要支持距离计算语义。

### `bool operator<(const QTaggedIterator &j)`

头文件中公开的比较运算符，通过距离结果判断当前迭代器是否位于 `j` 之前。只应在同一序列并且距离运算有意义时使用。

### `bool operator<=(const QTaggedIterator &j)`

判断当前迭代器是否不晚于 `j`。语义依赖 `operator>`，同样只适合有序、可比较的同一迭代区间。

### `bool operator>(const QTaggedIterator &j)`

通过距离结果判断当前迭代器是否位于 `j` 之后。不要用于无关容器或不支持距离计算的迭代器。

### `bool operator>=(const QTaggedIterator &j)`

判断当前迭代器是否不早于 `j`。适用边界与 `<`、`>` 相同。

### `operator+(qsizetype j, const QTaggedIterator &k)`

相关非成员函数，支持 `j + k` 写法，语义等同于 `k + j`：返回从 `k` 前进 `j` 个位置后的迭代器。

## API 速查表

| API | 作用 | 重点边界 |
| --- | --- | --- |
| `QTaggedIterator(Iterator &&it)` | 从底层迭代器构造带 category 的适配器 | 类别必须匹配运行期能力；不匹配会 fatal |
| `operator==` | 判断是否指向同一项 | 只比较同一容器视图的迭代器 |
| `operator!=` | 判断是否指向不同项 | 常用于 `it != end` |
| `operator++()` | 前置前进一项 | 不能对 end 调用 |
| `operator++(int)` | 后置前进一项并返回旧位置 | 有额外副本语义，普通循环优先前置形式 |
| `operator--()` | 前置后退一项 | 需要双向迭代；不能对 begin 调用 |
| `operator--(int)` | 后置后退一项并返回旧位置 | 需要双向迭代 |
| `operator+=` | 原地前进 `j` 项 | 偏移不得越过合法区间 |
| `operator-=` | 原地后退 `j` 项 | 需要反向迭代能力 |
| `operator+(qsizetype)` | 返回前进后的新迭代器 | 当前迭代器不变 |
| `operator-(qsizetype)` | 返回后退后的新迭代器 | 不支持双向迭代时是未定义结果 |
| `operator-(const QTaggedIterator &)` | 计算两个迭代器距离 | 两者必须属于同一序列 |
| `operator<` / `<=` / `>` / `>=` | 按距离比较位置 | 仅在距离运算有意义时使用 |
| `operator+(qsizetype, const QTaggedIterator &)` | 支持 `n + it` 写法 | 等同于 `it + n` |

## 一句话总结

`QTaggedIterator` 是 Qt 元对象容器迭代器和标准库算法之间的“能力标签”：它让算法看见 iterator category，但不会提升底层容器能力；反向、随机访问和距离计算都必须先满足真实容器的能力边界。
