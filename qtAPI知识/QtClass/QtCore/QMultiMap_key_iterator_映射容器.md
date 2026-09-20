# QMultiMap::key_iterator：只读遍历每条记录的键

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMultiMap>`  
> 模块：`Qt6::Core`  
> 所属类型：`QMultiMap<Key, T>::key_iterator`  
> 相关 API：`QMultiMap::keyBegin()`、`QMultiMap::keyEnd()`、`QMultiMap::const_iterator`

`QMultiMap<Key, T>::key_iterator` 是面向键的 STL 风格只读迭代器。它包装 `QMultiMap::const_iterator`，但解引用时返回 `const Key &`，而不是通常迭代器返回的 `T`。

## 它解决什么问题

遍历 `QMultiMap` 时，普通 `iterator` / `const_iterator` 的 `*it` 是值；键要通过 `it.key()` 取得。这对同时处理键和值很自然，但当算法只关心键时，传入普通迭代器就不匹配。

`key_iterator` 让键成为解引用结果，因此能直接把键区间交给 STL 或 Qt 泛型算法，而不必先调用 `keys()` 构造临时 `QList<Key>`。

适合的场景：

- 统计满足条件的键项数量；
- 检查当前记录序列是否仍按键有序；
- 将键指针范围交给只消费指针的算法；
- 对每一条记录的键做过滤、比较或输出；
- 需要避免 `keys()` 的线性复制与额外内存分配。

```cpp
#include <QMultiMap>
#include <algorithm>

QMultiMap<int, QString> jobs;
jobs.insert(10, "open");
jobs.insert(20, "render");
jobs.insert(20, "thumbnail");

const auto highPriorityCount = std::count_if(
    jobs.keyBegin(), jobs.keyEnd(),
    [](int priority) { return priority >= 20; });

// 结果为 2：相同 key 的两条记录会被分别遍历。
```

## 它不是什么

`key_iterator` 很容易被名字误解，先排除三件事：

- 它**不是**只遍历不同键的迭代器。一个键有三条记录，迭代时会得到三次这个键。
- 它**不能修改键**。解引用类型是 `const Key &`，这是为了维持 `QMultiMap` 的排序树不变式。
- 它**不提供值**。需要键和值时用 `const_iterator` 的 `key()` / `value()`，或 `asKeyValueRange()`。

`QMultiMap` 的所有条目按键升序排列；相同键的条目连续，且最近插入的值在前。因此 `keyBegin()` 到 `keyEnd()` 的键序列是非递减的，但其中会包含重复键。

```cpp
QMultiMap<int, QString> map;
map.insert(2, "old");
map.insert(1, "only");
map.insert(2, "new");

// key_iterator 解引用后的序列：1, 2, 2
// 不是：1, 2
```

## 与 `keys()`、普通迭代器的选择

| 目标 | 推荐方式 | 代价与语义 |
| --- | --- | --- |
| 只把所有键流式交给算法 | `keyBegin()` / `keyEnd()` | 不分配列表；每条记录一个键。 |
| 需要键和值 | `cbegin()` / `cend()`，再用 `it.key()`、`it.value()` | 一次遍历拿到完整条目。 |
| 需要可修改值 | `begin()` / `end()` | 仍不能修改 key；非 const 访问可能触发 detach。 |
| 需要唯一键列表 | `uniqueKeys()` | 创建新列表，重复键被折叠。 |
| 需要可长期保存、独立修改的键快照 | `keys()` | 创建新 `QList<Key>`，重复键保留。 |

```cpp
// 只关心键：无额外 QList 分配
const bool hasNegativeKey = std::any_of(
    map.keyBegin(), map.keyEnd(),
    [](int key) { return key < 0; });

// 同时关心键和值：普通 const_iterator 更清楚
for (auto it = map.cbegin(), end = map.cend(); it != end; ++it)
    qDebug() << it.key() << it.value();
```

不要为了只访问键而写 `for (const auto &key : map.keys())`，除非确实需要一个独立的 `QList`。`keys()` 需要完整遍历并分配内存，`key_iterator` 则直接引用容器内部的键。

## 创建、范围与默认构造

通常不直接构造 `key_iterator`，而是从同一 `QMultiMap` 取得成对边界：

```cpp
const QMultiMap<int, QString> map = {
    {1, "one"},
    {2, "two"},
    {2, "second two"}
};

for (auto it = map.keyBegin(), end = map.keyEnd(); it != end; ++it)
    qDebug() << *it;
```

默认构造的 `key_iterator` 是未初始化迭代器。它不能解引用、递增、递减，也不能当成某个容器的 `end()` 使用；应只把 `keyBegin()` / `keyEnd()` 或从有效 `const_iterator` 得到的迭代器用于遍历。

开始和结束迭代器必须来自同一容器、同一有效数据版本。将 A 容器的 `keyBegin()` 与 B 容器的 `keyEnd()` 进行比较或作为一个算法区间，属于错误用法。

## 解引用与 `base()`

```cpp
auto keyIt = map.keyBegin();
const int &key = *keyIt;       // 当前条目的键
const int *keyAddress = keyIt.operator->();

QMultiMap<int, QString>::const_iterator entryIt = keyIt.base();
qDebug() << entryIt.key() << entryIt.value();
```

`operator*()` 和 `operator->()` 返回的是容器内部键的 const 引用/指针。它们没有延长容器寿命；后续任何使迭代器失效的操作都可能让这些引用和指针悬空。

`base()` 返回底层 `QMultiMap::const_iterator` 的副本，用于在“只遍历键”和“需要恢复访问值”之间切换。`base()` 不会解除迭代器的只读性，也不会让它免于失效规则。

## 递增、递减与边界

`key_iterator` 是双向迭代器：

- `++it`：移到下一条记录的键并返回自身；
- `it++`：返回移动前的副本，再移到下一条；
- `--it`：移到前一条记录的键并返回自身；
- `it--`：返回移动前的副本，再移到前一条。

优先使用前缀 `++it` / `--it`，因为不需要额外保存移动前副本。

```cpp
for (auto it = map.keyBegin(), end = map.keyEnd(); it != end; ++it)
    useKey(*it);

if (!map.isEmpty()) {
    auto last = map.keyEnd();
    --last;                    // 合法：从 end() 退到最后一项
    qDebug() << *last;
}
```

这些操作的硬边界：

- 解引用 `keyEnd()` 是未定义行为；
- 在 `keyEnd()` 上递增是未定义行为；
- 在 `keyBegin()` 上递减是未定义行为；
- 空容器中 `keyBegin() == keyEnd()`，不能对该位置解引用或递减。

它不是随机访问迭代器，不能用 `it + n`、`it[n]` 或常数时间距离假设。移动多个位置时使用 `std::advance()` / `std::next()` / `std::prev()`，其代价与移动距离有关。

## 隐式共享、失效与线程

`QMultiMap` 是隐式共享容器，`key_iterator` 基于 const 迭代器，因此从 `keyBegin()` / `keyEnd()` 创建它不会为了写访问而主动 detach。但只要容器被修改，或因某次非 const 成员调用而从共享副本分离，就应认为全部现有迭代器及其引用失效。

```cpp
QMultiMap<int, QString> a;
a.insert(1, "one");

QMultiMap<int, QString> b = a; // 共享数据
auto keys = a.keyBegin();

b.insert(2, "two");            // b 分离；通常不影响 a 的迭代器
a.insert(3, "three");          // a 被修改；keys 不应再使用
```

避免在一个容器仍有活动迭代器时随意复制并修改它或其共享副本，这正是 Qt 容器文档所说的 implicit-sharing iterator problem。跨线程时，多个线程只读同一个 `QMultiMap` 可以共享；只要任一线程修改，必须由调用方同步，并使其他线程停止使用旧迭代器。

## 与泛型算法配合的边界

由于它解引用为 `const Key &`，适合只读、单遍或双向算法，例如：

```cpp
const bool sorted = std::is_sorted(map.keyBegin(), map.keyEnd());
const auto twoCount = std::count(map.keyBegin(), map.keyEnd(), 2);
```

不适合需要可写引用的算法，也不适合要求随机访问迭代器的算法，例如 `std::sort()`。`QMultiMap` 已按键排序，额外排序键区间既不需要也不能通过这个迭代器原地完成。

若 `Key` 是原始指针，`key_iterator` 只遍历指针值，不管理被指向对象。把它交给 `qDeleteAll(first, last)` 会删除对象但不会从 `QMultiMap` 移除条目，随后容器会保留悬空指针；应当在明确的所有权设计下删除并清理容器，而不是把迭代器当作所有权工具。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QMultiMap::keyBegin() const` | 取得指向第一条记录键的 `key_iterator`。 | 只读，不去重；空容器时等于 `keyEnd()`。 |
| `QMultiMap::keyEnd() const` | 取得尾后 `key_iterator`。 | 只用于边界比较，不能解引用或递增。 |
| `const Key &operator*() const` | 返回当前条目的键。 | 返回内部 const 引用；不能修改 key，迭代器失效后引用也失效。 |
| `const Key *operator->() const` | 返回当前条目键的地址。 | 指针不拥有对象；不能在 end 或失效迭代器上使用。 |
| `key_iterator &operator++()` | 前缀递增，移到下一条记录。 | 在 `keyEnd()` 上调用未定义；优先于后缀递增。 |
| `key_iterator operator++(int)` | 后缀递增，返回移动前副本。 | 在 `keyEnd()` 上调用未定义；会产生一个临时副本。 |
| `key_iterator &operator--()` | 前缀递减，移到前一条记录。 | 在 `keyBegin()` 上调用未定义；非空时可先对 `keyEnd()` 递减。 |
| `key_iterator operator--(int)` | 后缀递减，返回移动前副本。 | 在 `keyBegin()` 上调用未定义；会产生一个临时副本。 |
| `bool operator==(other) const` | 判断是否指向同一条记录。 | 只比较来自同一容器、同一有效版本的迭代器。 |
| `bool operator!=(other) const` | 判断是否指向不同记录。 | 常用于 `it != keyEnd()` 循环条件。 |
| `const_iterator base() const` | 取得底层条目的 const 迭代器。 | 可继续用 `.key()` / `.value()`；仍遵守原迭代器的生命周期和失效规则。 |

## 一句话总结

`QMultiMap::key_iterator` 是零额外列表分配的“逐条记录键视图”：它保留排序和重复键、只读且双向，适合直接喂给只关心键的算法，但不能替代唯一键集合，也不能跨容器版本长期保存。
