# Qt QIterator 类型擦除可写迭代器深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QIterator>`  
> 所属模块：`Qt6::Core`  
> 模板：`template <typename Container> struct QIterator`  
> 继承关系：`QBaseIterator<Container> -> QIterator<Container>`  
> 常见派生类型：`QMetaSequence::Iterable::Iterator`、`QMetaAssociation::Iterable::Iterator`

## 1. 它解决什么问题

`QIterator<Container>` 是 Qt 运行时容器反射体系中的类型擦除可写迭代器。它把某个具体容器的 native iterator 包装起来，让上层代码可以在不知道底层容器完整 C++ 类型的情况下：

- 比较两个迭代位置；
- 向前或向后移动；
- 按距离跳跃；
- 计算两个位置之间的距离；
- 把位置交给具体派生 iterator 读取或修改元素。

它位于这条关系链中：

```text
真实容器的 native iterator
        │ 被 void * 擦除
        ▼
QIterator<Container>
        │ 由 QMetaSequence / QMetaAssociation 解释
        ▼
QMetaSequence::Iterable::Iterator
QMetaAssociation::Iterable::Iterator
```

它主要服务于这些场景：

- `QVariant` 或 Qt 元容器反射访问未知类型的顺序容器；
- 通过 `QMetaSequence::Iterable` 遍历 `QList<T>`、`QVector<T>` 等容器；
- 通过 `QMetaAssociation::Iterable` 遍历未知键值容器；
- 在运行时只知道 `QMetaSequence` / `QMetaAssociation`，仍需要保持 iterator 语义；
- 让具体派生 iterator 复用统一的位置管理、复制、销毁和移动逻辑。

## 2. 它不是普通容器迭代器

`QIterator` 虽然提供 STL 风格的 `++`、`--`、`+`、`-`，但它不是：

- `QVector<T>::iterator` 的类型别名；
- `QMap<K, V>::iterator` 的直接替代品；
- 可以脱离 `QIterable` 独立创建的迭代器；
- 自己就带有 `operator*()` 的完整元素访问器；
- 自动延长容器生命周期的智能指针；
- 保证随机访问、负向移动或 O(1) 距离计算的通用迭代器。

Qt 官方建议一般不要直接使用 `QIterator`，而是通过它的派生类型使用：

```text
QMetaSequence::Iterable::Iterator
QMetaAssociation::Iterable::Iterator
```

派生类型会补上具体元素语义，例如：

```cpp
auto it = iterable.mutableBegin();
*it = QVariant(42);
```

上面的 `operator*()` 不是 `QIterator` 自身提供的，而是具体 sequence 或 association iterator 提供的代理引用。

## 3. 最小实际用法

顺序容器反射中的典型用法如下：

```cpp
#include <QList>
#include <QMetaSequence>
#include <QVariant>

QList<int> values{10, 20, 30};

const QMetaSequence meta =
    QMetaSequence::fromContainer<QList<int>>();
QMetaSequence::Iterable iterable(meta, &values);

for (auto it = iterable.mutableBegin();
     it != iterable.mutableEnd();
     ++it) {
    const QVariant oldValue = *it;
    *it = oldValue.toInt() + 1;
}
```

这里的 `it` 实际是 `QMetaSequence::Iterable::Iterator`，它继承 `QIterator<QMetaSequence>` 并补上了元素解引用能力。

如果只读访问，使用 const iterator：

```cpp
for (auto it = iterable.constBegin();
     it != iterable.constEnd();
     ++it) {
    qDebug() << *it;
}
```

## 4. `Container` 参数和生命周期

### 4.1 `Container` 是元容器描述器

在常见 Qt API 中：

```cpp
QIterator<QMetaSequence>
QIterator<QMetaAssociation>
```

这里的 `Container` 不是 `QList<int>` 或 `QMap<QString, int>`。它是一个能够解释擦除 iterator 的元容器对象。

`QIterator` 通过 `QBaseIterator` 保存：

```text
QIterable<Container> 指针
        +
void * native iterator
```

当调用 `operator++()` 时，它并不知道具体容器如何递增，而是把请求转发给：

```text
iterable->metaContainer().advanceIterator(nativeIterator, 1)
```

### 4.2 只能由 `QIterable` 创建

官方语义是，`QIterator` 只能由 `QIterable` 实例创建。虽然构造函数是 public，但它要求调用方提供：

- 一个匹配的 `QIterable<Container> *`；
- 一个由同一元容器创建的 native iterator 指针；
- 与 iterator 所有权相符的销毁协议。

普通业务代码不要手工传入任意 `void *`：

```cpp
// 不要伪造这种对象：
// QIterator<QMetaSequence> it(&iterable, arbitraryPointer);
```

错误的指针会在比较、递增、复制或析构时触发未定义行为。

### 4.3 iterable 必须比 iterator 活得久

`QBaseIterator` 内部保存指向 `QIterable` 的指针，用于查询元容器并销毁 native iterator。因此：

```cpp
QMetaSequence::Iterable iterable(meta, &values);
auto it = iterable.mutableBegin();
```

是安全的生命周期结构，而下面这种写法不安全：

```cpp
auto makeBadIterator(QList<int> &values)
{
    return QMetaSequence::Iterable(
        QMetaSequence::fromContainer<QList<int>>(),
        &values).mutableBegin();
}
```

临时 iterable 在完整表达式结束后销毁，返回的 iterator 仍然保存着悬空的 iterable 指针。

真实容器也必须继续存在：

```text
真实容器存活
    > iterable 存活
        > QIterator 存活
```

严格来说，容器和 iterable 至少要覆盖 iterator 使用期间的全部操作；容器结构变化还可能额外使 native iterator 失效。

## 5. QIterator 的复制和移动

`QIterator` 继承 `QBaseIterator` 的复制和移动语义。

### 5.1 复制会复制 native iterator

复制一个 `QIterator` 会通过元容器的 copy iterator 操作创建一个独立的底层位置：

```cpp
auto first = iterable.mutableBegin();
auto second = first;

++second;
```

此时 `first` 和 `second` 通常指向不同位置。推进 `second` 不应推进 `first`。

这正是后缀递增的基础：

```cpp
auto old = it++;
```

`old` 保存递增前的位置，`it` 已经移动到下一项。

### 5.2 移动转移底层 iterator 所有权

移动构造或移动赋值会把 native iterator 的管理权转移给目标对象，源对象不再负责销毁同一份底层 iterator：

```cpp
auto replacement = std::move(it);
```

移动后的源 iterator 只能被重新赋值或销毁，不要继续把它当作有效位置使用。

### 5.3 复制不是容器复制

复制 `QIterator` 只复制当前迭代位置，不复制真实容器。多个 iterator 仍然共同依赖：

- 同一个真实容器；
- 同一个 `QIterable`；
- 同一个元容器描述器。

## 6. 迭代能力和复杂度

是否能调用某个操作，首先取决于 `QIterable` 的能力查询：

| 能力 | 相关操作 | 复杂度提示 |
| --- | --- | --- |
| input | `++it` | 基本前进；通常不能后退 |
| forward | `++it`、重复遍历 | 可以按 forward 语义前进 |
| bidirectional | `--it`、`it - n`、`it -= n` | 后退合法，可能是线性 |
| random access | `it + n`、`it - n`、`it1 - it2` | 通常能高效跳跃和求距离 |

这些能力不是 `QIterator` 自己动态推断的，而是元容器描述器根据底层 iterator category 提供的。

在使用前：

```cpp
if (iterable.canReverseIterate()) {
    --it;
}
```

如果需要把算法写成随机访问形式：

```cpp
if (iterable.canRandomAccessIterate()) {
    it += offset;
}
```

非随机访问容器上，正向 `operator+=` 可能通过多次递增实现，不能默认是 O(1)。负数跳跃和后退则要求双向能力。

## 7. 位置边界规则

### 7.1 begin 可以解引用，end 不能解引用

```cpp
auto begin = iterable.mutableBegin();
auto end = iterable.mutableEnd();

if (begin != end) {
    use(*begin);
}
```

`end` 表示“最后一个元素之后”的位置，不是最后一个元素：

```cpp
// 错误：
// use(*end);
```

### 7.2 end 不能递增

Qt 文档明确说明，在 `QMetaSequence::Iterable::constEnd()` 上调用 `operator++()` 会产生未定义结果：

```cpp
// 不要：
// ++iterable.constEnd();
```

普通遍历只在 `it != end` 时递增当前有效元素。

### 7.3 begin 不能递减

在 `begin()` 上调用 `operator--()` 会试图移动到第一个元素之前的位置，结果未定义：

```cpp
// 不要：
// auto it = iterable.mutableBegin();
// --it;
```

如果需要反向遍历，应先从 end 退一步，但要先判断容器非空并具备双向能力：

```cpp
if (iterable.canReverseIterate()
        && iterable.constBegin() != iterable.constEnd()) {
    auto it = iterable.constEnd();
    --it;
    use(*it);
}
```

## 8. 逐项 API 说明

### `explicit QIterator(QIterable<Container> *iterable, void *iterator)`

**作用：** 用一个 iterable 和 native iterator 指针创建 `QIterator`。

**关键语义：**

- `iterable` 提供元容器描述器和真实容器访问路径；
- `iterator` 指向由该元容器创建的底层 native iterator；
- `QIterator` 会在生命周期结束时通过元容器销毁底层 iterator；
- 具体派生 iterator 通常调用这个构造函数。

**边界：**

- 普通业务代码不要手工传 `void *`；
- `iterable` 必须在 iterator 使用期间保持有效；
- `iterator` 必须由匹配的元容器创建；
- 不要把 const iterator 指针传给可写 `QIterator`；
- 错误的所有权会导致重复释放或泄漏。

### `bool operator==(const QIterator<Container> &other) const`

**作用：** 判断两个 iterator 是否指向同一个迭代位置。

**关键语义：**

- 比较通过元容器的 `compareIterator()` 完成；
- 常用于 `it == end` 或 `it == other`；
- 两个 iterator 应来自同一 iterable 和同一底层容器。

```cpp
if (it == iterable.mutableEnd()) {
    // 到达末尾
}
```

**边界：**

- 不要比较不同容器的 iterator；
- 不要把相同整数偏移当作跨容器相等；
- 已失效 iterator 的比较结果不能依赖；
- end 只能和同一 iterable 的 iterator 配对。

### `bool operator!=(const QIterator<Container> &other) const`

**作用：** 判断两个 iterator 是否指向不同位置。

**关键语义：**

- 通常用于遍历循环：

```cpp
for (auto it = iterable.mutableBegin();
     it != iterable.mutableEnd();
     ++it) {
    use(*it);
}
```

- 语义上与 `operator==` 互补。

**边界：**

- 仍然要求两个 iterator 来源一致；
- 不能用不同 iterable 的 end 作为终点；
- 底层容器结构变化后，不要继续依赖比较结果。

### `QIterator<Container> &operator++()`

**作用：** 前置递增，把 iterator 移到下一个位置并返回移动后的 iterator。

**关键语义：**

```cpp
++it;
```

- 通常是循环中首选的前进方式；
- 可以在 input/forward/bidirectional/random access 能力下使用；
- 对位置的实际推进由元容器 `advanceIterator(..., 1)` 完成。

**边界：**

- 不能对 end 递增；
- 底层容器结构变化可能使 iterator 失效；
- 不要假设每次递增都完全没有类型擦除开销；
- 真实容器的 iterator category 必须支持该操作。

### `QIterator<Container> operator++(int)`

**作用：** 后置递增，返回递增前的 iterator 副本，然后把当前 iterator 移到下一位置。

**关键语义：**

```cpp
const auto old = it++;
```

执行后：

```text
old -> 原位置
it  -> 下一位置
```

它需要复制底层 native iterator，因此在不需要旧位置时，通常优先使用 `++it`。

**边界：**

- 不能对 end 递增；
- 返回的旧副本仍依赖同一个 iterable 和真实容器；
- 容器结构变化可能同时使 old 和 it 失效；
- 不要把后缀递增当成“只返回引用”的廉价操作。

### `QIterator<Container> &operator--()`

**作用：** 前置递减，把 iterator 移到前一个位置并返回移动后的 iterator。

**关键语义：**

```cpp
--it;
```

- 要求底层支持 bidirectional iterator；
- 实际由元容器以负一步长推进；
- 适合从 end 向最后一个元素移动。

**边界：**

- 不支持双向迭代时，调用结果未定义；
- 不能对 begin 递减；
- 不要把 `canReverseIterate()` 理解成已有 reverse iterator；
- 先判断非空，再从 end 递减。

### `QIterator<Container> operator--(int)`

**作用：** 后置递减，返回递减前的 iterator 副本，再将当前 iterator 后退一位。

**关键语义：**

```cpp
const auto old = it--;
```

执行后：

```text
old -> 原位置
it  -> 前一位置
```

**边界：**

- 要求双向迭代能力；
- begin 上调用未定义；
- 会复制底层 native iterator；
- 不需要旧位置时优先使用 `--it`。

### `QIterator<Container> &operator+=(qsizetype j)`

**作用：** 把当前 iterator 向前移动 `j` 个位置。

**关键语义：**

```cpp
it += j;
```

- `j` 为正时向前；
- 对随机访问容器通常能高效跳跃；
- 对较弱迭代器可能通过多次递增完成；
- 返回修改后的当前 iterator。

**边界：**

- 负数 `j` 要求底层至少支持双向迭代；
- 不要跳出 `[begin, end]` 合法范围；
- 不要把一般容器上的 `+=` 当作 O(1)；
- 具体支持能力由 `QIterable` 元容器描述器决定。

### `QIterator<Container> &operator-=(qsizetype j)`

**作用：** 把当前 iterator 向后移动 `j` 个位置。

**关键语义：**

```cpp
it -= j;
```

它等价于用负方向移动：

```text
当前位置 - j
```

**边界：**

- 要求底层支持双向迭代；
- `j` 过大可能越过 begin；
- 不要在 input/forward-only 容器上使用；
- 非随机访问容器上可能是线性移动。

### `QIterator<Container> operator+(qsizetype j) const`

**作用：** 返回一个位于当前 iterator 前方 `j` 个位置的新 iterator，不改变原 iterator。

**关键语义：**

```cpp
const auto target = it + offset;
```

它相当于复制当前 iterator，再执行 `+= offset`。

**边界：**

- 结果位置必须仍在合法范围内；
- 负数偏移要求双向能力；
- 非随机访问容器上可能是线性移动；
- 原 iterator 和返回值仍共享底层容器及 iterable 生命周期。

### `QIterator<Container> operator-(qsizetype j) const`

**作用：** 返回一个位于当前 iterator 后方 `j` 个位置的新 iterator。

**关键语义：**

```cpp
const auto previous = it - offset;
```

它不会改变原 iterator。

**边界：**

- 官方文档明确要求底层支持双向迭代；
- 不支持双向迭代时调用结果未定义；
- 不能退到 begin 之前；
- 不要把它误解成“从两个 iterator 求差”的重载。

### `qsizetype operator-(const QIterator<Container> &j) const`

**作用：** 返回两个 iterator 之间的距离。

**关键语义：**

```cpp
const qsizetype distance = end - begin;
```

实现会把距离计算转发给元容器：

```text
metaContainer.diffIterator(this, j)
```

对随机访问容器通常高效；对只能顺序推进的 iterator，底层可能通过 `std::distance` 线性计算。

**边界：**

- 两个 iterator 必须来自同一底层容器和同一迭代体系；
- 不要对不同容器的 iterator 求距离；
- 位置顺序和负距离是否可用取决于底层 iterator category；
- 失效 iterator 或跨容器距离没有可靠语义。

### `QIterator<Container> operator+(qsizetype j, const QIterator<Container> &k)`

**作用：** 以非成员形式返回从 `k` 向前 `j` 个位置的新 iterator。

**关键语义：**

```cpp
const auto target = offset + it;
```

它与：

```cpp
const auto target = it + offset;
```

表达同一个位置操作。

**边界：**

- 仍受 `operator+` 的边界和能力约束；
- 不会因为是非成员函数而获得额外随机访问能力；
- 不同容器 iterator 不能混用。

## 9. 位置操作示例

### 9.1 普通可写遍历

```cpp
for (auto it = iterable.mutableBegin();
     it != iterable.mutableEnd();
     ++it) {
    update(*it);
}
```

### 9.2 保存旧位置

```cpp
auto it = iterable.mutableBegin();
const auto old = it++;

use(*old);
use(*it);
```

只在确实需要旧位置时使用后置递增。

### 9.3 从末尾向前访问

```cpp
auto begin = iterable.constBegin();
auto end = iterable.constEnd();

if (iterable.canReverseIterate() && begin != end) {
    auto it = end;
    --it;
    use(*it);
}
```

如果要完整反向遍历：

```cpp
if (iterable.canReverseIterate()) {
    auto begin = iterable.constBegin();
    auto it = iterable.constEnd();

    while (it != begin) {
        --it;
        use(*it);
    }
}
```

### 9.4 随机访问路径

```cpp
if (iterable.canRandomAccessIterate()) {
    auto it = iterable.mutableBegin();
    it += offset;

    if (it != iterable.mutableEnd()) {
        use(*it);
    }
}
```

即使支持随机访问，也要保证 `offset` 没有把 iterator 推出合法范围。

## 10. 与 `QConstIterator` 的区别

`QIterator` 和 `QConstIterator` 的位置操作形状相似，关键差异是底层可写性：

| 类型 | 底层入口 | 典型用途 | 是否修改元素 |
| --- | --- | --- | --- |
| `QConstIterator<Container>` | `QIterable::constBegin()` | 只读遍历 | 不应修改 |
| `QIterator<Container>` | `QIterable::mutableBegin()` | 可写遍历 | 取决于派生 iterator 和元容器能力 |

不要因为 `QIterator` 是“mutable iterator”就认为：

- 容器结构可以随意增删；
- 元容器一定支持元素赋值；
- const 底层对象可以被写入；
- iterator 失效规则会消失。

它只表示这条 iterator 路径允许把可写能力交给具体派生类型。

## 11. 常见误区

### 11.1 直接手工构造 `QIterator`

**现象：** 业务代码把某个 native iterator 地址强转成 `void *` 传入。

**原因：** 误以为 `QIterator` 是公开的通用 iterator 构造器。

**处理：** 让 `QIterable` 或 `QMetaSequence::Iterable` 创建 iterator；不要伪造擦除指针。

### 11.2 以为 `QIterator` 自己能解引用

**现象：** 直接对 `QIterator<QMetaSequence>` 使用 `*it`。

**原因：** `QIterator` 只实现位置操作，元素访问由派生类型提供。

**处理：** 使用 `QMetaSequence::Iterable::Iterator` 或 `QMetaAssociation::Iterable::Iterator`。

### 11.3 对不同 iterable 的 iterator 做比较

**现象：** 一个 iterable 的 iterator 和另一个 iterable 的 end 比较。

**原因：** 忽略了 native iterator 比较必须使用同一个底层容器和元容器协议。

**处理：** begin 和 end 永远从同一个 iterable 创建。

### 11.4 在 end 上递增或 begin 上递减

**现象：** 反向遍历偶发崩溃，或最后一个元素读取错误。

**原因：** end 不是元素，begin 前面也没有合法元素。

**处理：** 先判断非空和双向能力，再从 end 递减；永远不要对 end 递增。

### 11.5 只因 `operator+` 存在就认为是随机访问

**现象：** 对链式容器频繁 `it + 100000`，性能异常。

**原因：** 类型擦除接口可以统一暴露位置操作，但底层可能只能逐步推进。

**处理：** 先检查 `canRandomAccessIterate()`，性能敏感时使用适配算法。

### 11.6 修改底层容器后继续使用 iterator

**现象：** 迭代器比较或解引用得到错误数据。

**原因：** 具体容器的插入、删除、清空或重新分配使 native iterator 失效。

**处理：** 结构修改后重新从 iterable 获取 begin/end；不要依赖失效 iterator。

### 11.7 把复制 iterator 当作复制容器

**现象：** 复制 iterator 后销毁一个，另一个仍被当成独立容器视图。

**原因：** iterator 副本只拥有独立位置，不拥有底层容器。

**处理：** 管理真实容器和 iterable 的生命周期，iterator 只表示位置。

### 11.8 在容器为空时直接 `--end`

**现象：** 空容器反向读取崩溃。

**原因：** 空容器中 `begin == end`，此时 end 前面不存在有效元素。

**处理：**

```cpp
if (begin != end && iterable.canReverseIterate()) {
    --end;
}
```

## API 速查表
| API | 类型 | 作用 | 使用重点 |
| --- | --- | --- | --- |
| `QIterator(iterable, void *iterator)` | 构造函数 | 包装 native iterator | 仅由 QIterable/派生类创建；不要伪造指针 |
| `operator==(other)` | 比较 | 判断是否为同一位置 | 只比较同一 iterable 的 iterator |
| `operator!=(other)` | 比较 | 判断是否为不同位置 | 常用于 `it != end` |
| `operator++()` | 前进 | 前移一项并返回新位置 | end 上递增未定义 |
| `operator++(int)` | 前进 | 返回旧位置后再前移 | 需要旧副本时使用；有复制成本 |
| `operator--()` | 后退 | 后移一项并返回新位置 | 需要双向能力；begin 上未定义 |
| `operator--(int)` | 后退 | 返回旧位置后再后退 | 需要双向能力；有复制成本 |
| `operator+=(j)` | 跳跃 | 向前移动 `j` 项 | 复杂度取决于底层 iterator category |
| `operator-=(j)` | 跳跃 | 向后移动 `j` 项 | 需要双向能力；不能越过 begin |
| `operator+(j)` | 非修改跳跃 | 返回前方 `j` 项的新 iterator | 原 iterator 不变；负数需双向能力 |
| `operator-(j)` | 非修改跳跃 | 返回后方 `j` 项的新 iterator | 官方要求双向迭代能力 |
| `operator-(other)` | 距离 | 返回两个 iterator 的距离 | 同一容器；非随机访问可能线性 |
| `operator+(j, k)` | 非成员跳跃 | 返回 `k` 前方 `j` 项的位置 | 与 `k + j` 等价；不增加能力 |
| 继承 `QBaseIterator` | 基类能力 | 保存/访问擦除 iterator 和 iterable | 普通代码通常通过具体 iterable 间接使用 |

## 13. 一句话总结

`QIterator<Container>` 是 Qt 元容器反射中的“可写位置句柄”：它不拥有容器，也不自己定义元素解引用，而是依赖 `QIterable`、元容器描述器和具体派生 iterator 完成位置比较、前进、后退与跳跃。使用时始终从具体 iterable 获取它，保证 begin/end 同源，先检查双向或随机访问能力，并让真实容器和 iterable 活得比 iterator 久。
