# Qt QKeyValueIterator 键值对迭代器深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QKeyValueIterator>`  
> 所属模块：`Qt6::Core`  
> 模板：`template <typename Key, typename T, typename Iterator, typename Traits = QtPrivate::QDefaultKeyValues<Key, T, Iterator>> class QKeyValueIterator`  
> 典型来源：`QMap::key_value_iterator`、`QHash::key_value_iterator` 及相关容器

## 1. 它解决什么问题

`QKeyValueIterator` 是 Qt 为关联容器提供的 STL 风格键值对迭代器。它把底层关联容器 iterator 包装成一个可以同时读取 key 和 value 的迭代器：

```text
底层 iterator
    ├─ key()
    └─ value()
          │
          ▼
QKeyValueIterator
          │ operator* / operator->
          ▼
std::pair<Key, T>
```

它主要解决这些问题：

- 用统一的 `operator*()` 得到 key/value pair；
- 让 `QMap`、`QHash`、`QMultiMap` 等关联容器更容易接入 STL 风格算法；
- 通过结构化绑定直接写 `for (auto [key, value] : ...)`；
- 把“底层 iterator 如何取 key/value”的细节交给 `Traits`；
- 在不暴露底层节点类型的前提下，提供前进、后退、比较和取底层 iterator 的能力。

典型代码：

```cpp
QMap<QString, int> scores{
    {QStringLiteral("alice"), 10},
    {QStringLiteral("bob"), 20},
};

for (auto it = scores.keyValueBegin();
     it != scores.keyValueEnd();
     ++it) {
    const auto [name, score] = *it;
    qDebug() << name << score;
}
```

## 2. 它不是什么

`QKeyValueIterator` 不是：

- `QMap::iterator` 的简单别名；
- 保存 key/value 引用的节点指针；
- 可以通过 `operator*()` 修改映射值的 mutable reference；
- 可以随机跳跃的通用随机访问迭代器；
- 容器本身或容器所有权对象；
- 把 key/value 自动转换成 `QVariant` 的反射迭代器。

最重要的边界是：

> `operator*()` 返回 `std::pair<Key, T>` 的值，key 和 value 都是按值获得的；它不是映射节点的引用视图。

因此下面的 `value` 是副本：

```cpp
for (auto [key, value] : scores.asKeyValueRange()) {
    value += 100; // 只修改局部副本，不会写回 scores
}
```

如果要修改容器中的值，应使用底层容器自己的 iterator API：

```cpp
for (auto it = scores.begin(); it != scores.end(); ++it) {
    it.value() += 100;
}
```

## 3. 模板参数怎么理解

### 3.1 `Key`

`Key` 是 pair 中 key 的值类型：

```cpp
QKeyValueIterator<QString, int, NativeIterator>
```

这里的 `Key` 是 `QString`。

### 3.2 `T`

`T` 是 pair 中 value 的值类型。它不表示引用类型：

```cpp
std::pair<Key, T>
```

如果底层容器保存的是 `LargeObject`，每次解引用都可能产生一个 `LargeObject` 副本。对大对象或高频循环，应该考虑直接使用底层容器的 iterator 或 `key()` / `value()` API。

### 3.3 `Iterator`

`Iterator` 是实际被包装的底层 iterator，例如：

- `QMap<Key, T>::iterator`；
- `QMap<Key, T>::const_iterator`；
- `QHash<Key, T>::iterator`；
- 其它提供兼容 key/value 访问接口的关联容器 iterator。

`QKeyValueIterator` 通过它获取：

- `iterator_category`；
- `difference_type`；
- 基于 iterator 的比较；
- key/value 的实际来源；
- 前进和后退行为。

### 3.4 `Traits`

默认 traits 是：

```cpp
QtPrivate::QDefaultKeyValues<Key, T, Iterator>
```

它会调用：

```cpp
it.key();
it.value();
```

如果底层 iterator 没有这两个成员，但可以通过其它方式取得 key/value，可以提供自定义 traits：

```cpp
struct PairTraits
{
    static QString key(const NativeIterator &it)
    {
        return it->first;
    }

    static int value(const NativeIterator &it)
    {
        return it->second;
    }
};

using KeyValueIterator =
    QKeyValueIterator<QString, int, NativeIterator, PairTraits>;
```

自定义 traits 是适配层技术，不是普通业务代码的首选。它必须保持 key/value 类型、const 语义和 iterator 生命周期的一致性。

## 4. 为什么返回 pair 副本

头文件中的核心定义可以概括为：

```cpp
using value_type = std::pair<Key, T>;
using reference = const value_type &;

std::pair<Key, T> operator*() const;
```

虽然类里声明了 `reference` 类型别名，但 `operator*()` 的实际函数返回类型是 `std::pair<Key, T>`，也就是按值返回。阅读代码时应以具体函数签名为准。

这意味着：

```cpp
const auto pair = *it;
```

会得到当前 key/value 的快照。它不受后续 iterator 移动影响：

```cpp
const auto oldPair = *it;
++it;

// oldPair 仍然保留旧位置的 key/value 副本
```

代价也很直接：

- key 可能复制；
- value 可能复制；
- `operator->()` 指向的是临时 pair 的代理；
- 不能拿返回 pair 的地址保存成容器节点指针；
- 不能通过 pair 的 value 修改底层容器。

## 5. 与 `keyValueBegin()` 和 `asKeyValueRange()` 的关系

### 5.1 `keyValueBegin()` / `keyValueEnd()`

Qt 关联容器通常提供：

```cpp
auto begin = map.keyValueBegin();
auto end = map.keyValueEnd();
```

它们的 iterator 类型通常就是 `QKeyValueIterator` 或 const 版本的相关实例。

### 5.2 `asKeyValueRange()`

Qt 6.4 起，关联容器可以把键值迭代器包装成 range：

```cpp
for (auto [key, value] : map.asKeyValueRange()) {
    qDebug() << key << value;
}
```

这层 range 让结构化绑定和范围 `for` 更自然，但不改变 `QKeyValueIterator` 的值语义：

- `key` 是副本；
- `value` 是副本；
- 修改结构化绑定变量不会写回 map；
- 需要写回时仍使用底层可写 iterator。

### 5.3 与普通 `begin()` 的选择

| 需求 | 推荐入口 |
| --- | --- |
| 只读访问 key/value，想用结构化绑定 | `keyValueBegin()` / `asKeyValueRange()` |
| 修改 value | `begin()` 返回的可写 map iterator |
| 只访问 key | `keyBegin()` 或相关 key iterator |
| 需要保留 value 引用 | 底层 map iterator 的 `value()` 引用 |
| 接入通用 STL 风格算法 | `QKeyValueIterator` 更方便 |

## 6. 构建与包含

### 6.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 6.2 头文件

```cpp
#include <QKeyValueIterator>
```

实际使用具体容器时，还需要对应的容器头：

```cpp
#include <QHash>
#include <QMap>
#include <QMultiMap>
```

## 7. 迭代器生命周期和失效

`QKeyValueIterator` 不拥有关联容器。它的有效性遵循底层 `Iterator` 的规则：

- 容器销毁后 iterator 失效；
- 容器结构修改后，是否失效由具体容器规定；
- 递增到 end 之后继续递增是未定义行为；
- 在 begin 之前递减是未定义行为；
- 复制 iterator 不会复制容器；
- `base()` 返回的底层 iterator 仍依赖原容器。

### 7.1 隐式共享迭代器问题

Qt 的许多容器是隐式共享的。Qt 文档特别提醒：

> 在关联容器存在活动 iterator 时，应避免复制该容器。

例如：

```cpp
QMap<QString, int> map{
    {QStringLiteral("a"), 1},
    {QStringLiteral("b"), 2},
};

auto it = map.keyValueBegin();

// 不要在 it 仍然活跃时随意复制 map：
// QMap<QString, int> copy = map;
```

隐式共享容器的复制、分离和 iterator 之间不是普通 STL 容器的完全相同语义。遍历期间如果确实需要快照，应在创建 iterator 之前完成复制，或者先把需要的数据复制到独立结构中。

## 8. 逐项 API 说明

### `QKeyValueIterator()`

**作用：** 构造默认的键值对迭代器。

**关键语义：**

- 得到一个默认构造的底层 `Iterator`；
- 不指向任何已知容器元素；
- 可以作为类型的默认值或延迟初始化对象。

**边界：**

- 默认 iterator 不能解引用；
- 不要把它当作任意容器的 begin；
- 只有在赋值为有效底层 iterator 后才可遍历；
- 默认 iterator 的比较只应遵循底层 iterator 自身的有效语义。

### `explicit constexpr QKeyValueIterator(Iterator o)`

**作用：** 在底层 iterator `o` 上构造一个键值对 iterator。

**关键语义：**

- 构造函数会移动传入的 `Iterator`；
- 如果 `Iterator` 可无异常移动构造，这个构造函数也满足对应的 `noexcept` 条件；
- 包装后的 iterator 位置和 `o` 原本的位置一致；
- 适合由容器的 `keyValueBegin()`、`keyValueEnd()` 或 range 适配层调用。

**边界：**

- `o` 必须是有效的、与目标容器匹配的 iterator；
- 构造后不要继续依赖被移动的 `o` 的原位置语义；
- 不同容器的底层 iterator 不能混合；
- QKeyValueIterator 不会验证 iterator 所属容器。

### `Iterator base() const`

**作用：** 返回此键值对 iterator 包装的底层 iterator。

**关键语义：**

```cpp
const auto native = it.base();
```

- 返回的是 iterator 值，不是底层节点引用；
- 可以把位置交回底层容器 API；
- 返回的底层 iterator 和原 iterator 指向同一逻辑位置。

**边界：**

- 返回值仍受底层容器生命周期影响；
- 复制底层 iterator 不会复制容器；
- 不能从返回值推导出 key/value 一定稳定；
- 底层 iterator 失效后，`base()` 得到的副本也不能使用。

### `std::pair<Key, T> operator*() const`

**作用：** 返回当前项目的 key/value pair。

**关键语义：**

```cpp
const auto [key, value] = *it;
```

- `key` 来自 `Traits::key(i)`；
- `value` 来自 `Traits::value(i)`；
- 返回的是 `std::pair<Key, T>` 值；
- 不返回底层节点引用；
- 每次解引用都可能产生 key/value 拷贝。

**边界：**

- 不能对 end 解引用；
- 不要写 `auto &pair = *it` 并期待得到节点引用；
- 修改返回 pair 不会写回容器；
- 复杂 value 类型可能带来明显复制成本。

### `QKeyValueIterator::pointer operator->() const`

**作用：** 以指针风格访问当前 key/value pair。

**关键语义：**

```cpp
qDebug() << it->first << it->second;
```

返回的 `pointer` 实际是：

```cpp
QtPrivate::ArrowProxy<value_type>
```

它是一个临时 pair 的箭头代理，用来支持 `it->first` 和 `it->second` 的表达式语法。

**边界：**

- 它不是指向容器节点的真实裸指针；
- 不要保存 `operator->()` 的返回对象或其中地址；
- 不能通过 `it->second` 修改底层 value；
- 不能对 end 使用。

### `QKeyValueIterator<Key, T, Iterator, Traits> &operator++()`

**作用：** 前置递增，把 iterator 移动到下一个键值对。

**关键语义：**

```cpp
++it;
```

- 调用底层 `Iterator::operator++()`；
- 返回移动后的当前 iterator；
- 适合普通遍历循环；
- 不产生旧位置的额外返回值。

**边界：**

- 递增到容器 end 是允许的终点状态；
- 对 end 再次递增是未定义行为；
- 容器结构变化可能使 iterator 失效；
- 是否支持递增由底层 iterator 决定。

### `QKeyValueIterator<Key, T, Iterator, Traits> operator++(int)`

**作用：** 后置递增，返回旧位置的 iterator 副本，然后移动当前 iterator。

**关键语义：**

```cpp
const auto old = it++;
```

执行后：

```text
old -> 原键值对
it  -> 下一个键值对
```

**边界：**

- 返回的是 iterator 副本，不是 pair；
- 仍然不能对 end 继续递增；
- 需要旧位置时使用，不需要时优先 `++it`；
- 副本和当前 iterator 仍共同依赖容器。

### `QKeyValueIterator<Key, T, Iterator, Traits> &operator--()`

**作用：** 前置递减，把 iterator 移到前一个键值对。

**关键语义：**

```cpp
--it;
```

- 调用底层 `Iterator::operator--()`；
- 适用于支持双向迭代的关联容器；
- 返回移动后的 iterator。

**边界：**

- begin 之前没有合法位置；
- 对 begin 递减是未定义行为；
- 如果底层 iterator 不支持后退，调用结果未定义；
- 关联容器的具体 iterator 能力应以容器文档为准。

### `QKeyValueIterator<Key, T, Iterator, Traits> operator--(int)`

**作用：** 后置递减，返回旧位置的 iterator 副本，再把当前 iterator 后退一项。

**关键语义：**

```cpp
const auto old = it--;
```

执行后：

```text
old -> 原键值对
it  -> 前一个键值对
```

**边界：**

- begin 上调用未定义；
- 要求底层支持双向迭代；
- 返回副本可能带来 iterator 复制成本；
- 不需要旧位置时优先使用 `--it`。

### `bool operator==(QKeyValueIterator lhs, QKeyValueIterator rhs) noexcept`

**作用：** 判断两个键值对 iterator 是否指向同一个底层位置。

**关键语义：**

- 实际比较两个包装的底层 iterator；
- 参数按值传递，因此比较本身会复制 iterator 包装；
- `noexcept` 来自类声明；
- 常用于 `it == end`。

**边界：**

- 两个 iterator 必须属于同一个底层容器；
- 不同容器的相同坐标或相同 key 不表示相等；
- 已失效 iterator 不应参与比较；
- 默认 iterator 不能被当作通用 end。

### `bool operator!=(QKeyValueIterator lhs, QKeyValueIterator rhs) noexcept`

**作用：** 判断两个键值对 iterator 是否指向不同位置。

**关键语义：**

```cpp
for (auto it = map.keyValueBegin();
     it != map.keyValueEnd();
     ++it) {
    consume(*it);
}
```

- 语义上与 `operator==` 互补；
- 仍然比较底层 iterator；
- 参数按值传递。

**边界：**

- 必须使用同一个容器的 begin/end；
- 不同容器 iterator 比较没有可靠业务含义；
- 容器发生使 iterator 失效的修改后，不要依赖结果。

## 9. 典型使用场景

### 9.1 结构化绑定读取

```cpp
QHash<QString, int> frequencies;
frequencies.insert(QStringLiteral("qt"), 3);
frequencies.insert(QStringLiteral("api"), 5);

for (auto it = frequencies.keyValueBegin();
     it != frequencies.keyValueEnd();
     ++it) {
    const auto [word, count] = *it;
    qDebug() << word << count;
}
```

### 9.2 STL 算法适配

`QKeyValueIterator` 提供 `value_type`、`reference`、`iterator_category`、`difference_type` 等迭代器相关类型，可以让关联容器的 key/value 遍历更接近 STL 风格。

但具体算法是否适合使用它，仍要看：

- 算法是否需要引用语义；
- 算法是否会写入元素；
- 算法是否要求随机访问；
- pair 按值产生的成本是否可接受。

只读、按值消费的算法更适合：

```cpp
for (auto it = map.keyValueBegin();
     it != map.keyValueEnd();
     ++it) {
    consumePair(*it);
}
```

需要修改元素的算法应直接使用底层 map iterator。

### 9.3 访问 pair 字段

```cpp
auto it = map.keyValueBegin();
if (it != map.keyValueEnd()) {
    const auto pair = *it;
    qDebug() << pair.first << pair.second;
    qDebug() << it->first << it->second;
}
```

`pair` 和 `operator->()` 访问的都是当前值的读取结果，不是节点引用。

## 10. 常见误区

### 10.1 以为 `value` 是 map 中的引用

**现象：** 修改 `auto [key, value] = *it` 后，发现 map 没有变化。

**原因：** `operator*()` 返回 `std::pair<Key, T>` 值。

**处理：** 修改场景使用 `map.begin()` 返回的可写 iterator 和 `it.value()`。

### 10.2 以为 `operator->()` 指向真实节点

**现象：** 保存 `&it->second`，随后移动 iterator 或退出表达式后继续使用。

**原因：** `operator->()` 返回 `ArrowProxy<value_type>`，它代理一个临时 pair。

**处理：** 只在当前表达式中读取 `it->first` / `it->second`，需要长期保存就复制值。

### 10.3 用默认构造 iterator 当 end

**现象：** `QKeyValueIterator()` 和容器的 end 比较，得到不可靠结果。

**原因：** 默认 iterator 没有绑定到具体容器，不是该容器的 end。

**处理：** 始终使用对应容器提供的 `keyValueEnd()`。

### 10.4 以为支持随机访问

**现象：** 尝试 `it + 3` 或 `it[3]`。

**原因：** `QKeyValueIterator` 只提供 `++` 和 `--`，没有随机访问运算符。

**处理：** 按顺序递增，或换用容器支持的其它访问方式。

### 10.5 在 end 上递增

**现象：** 遍历末尾后继续 `++it`。

**原因：** 超过 end 是未定义行为。

**处理：** 循环条件必须在解引用和递增前检查 `it != end`。

### 10.6 在 begin 前递减

**现象：** 反向遍历空容器或 begin 时崩溃。

**原因：** begin 前没有合法元素位置。

**处理：** 先确认容器非空，再从 end 递减；不要对 begin 递减。

### 10.7 活动 iterator 期间复制隐式共享容器

**现象：** 复制 `QMap` / `QHash` 后，活动 iterator 的行为与预期不同。

**原因：** Qt 隐式共享容器的 detach 和 iterator 规则与 STL 容器不完全相同。

**处理：** 创建 iterator 前完成容器复制，或遍历期间避免复制容器。

### 10.8 把 key/value pair 当作稳定引用

**现象：** 把一次 `*it` 的结果保存成引用，期待它随 iterator 移动更新。

**原因：** 解引用结果是一个 pair 值，不是可变节点引用。

**处理：** 每次需要当前项时重新解引用；需要稳定数据就明确复制到业务对象。

## API 速查表
| API | 类型 | 作用 | 使用重点 |
| --- | --- | --- | --- |
| `iterator_category` | 类型别名 | 暴露底层 iterator 类别 | 只用于迭代器 traits；类自身没有随机访问运算符 |
| `difference_type` | 类型别名 | 暴露底层距离类型 | 通常来自底层 iterator |
| `value_type` | 类型别名 | 定义为 `std::pair<Key, T>` | pair 是值类型，不是节点引用 |
| `reference` | 类型别名 | 声明 pair 的引用形式 | 实际 `operator*()` 按值返回，不能据此取得 map 引用 |
| `pointer` | 类型别名 | `QtPrivate::ArrowProxy<value_type>` | 是临时 pair 的箭头代理，不是节点指针 |
| `QKeyValueIterator()` | 构造函数 | 创建默认 iterator | 不指向任何容器；不能直接解引用 |
| `QKeyValueIterator(Iterator o)` | 构造函数 | 包装底层 iterator | 移动接管 `o`；底层类型必须匹配 |
| `base()` | 查询 | 返回底层 iterator 副本 | 仍依赖原容器生命周期 |
| `operator*()` | 解引用 | 返回当前 `std::pair<Key, T>` | key/value 按值复制；不能写回容器 |
| `operator->()` | 解引用 | 以箭头语法访问 pair | 返回 `ArrowProxy`；不要保存其地址 |
| `operator++()` | 前进 | 移动到下一项 | end 上再次递增未定义 |
| `operator++(int)` | 前进 | 返回旧位置后再前进 | 需要旧 iterator 时使用 |
| `operator--()` | 后退 | 移动到上一项 | begin 前递减未定义；需双向 iterator |
| `operator--(int)` | 后退 | 返回旧位置后再后退 | 需要旧 iterator 时使用 |
| `operator==(lhs, rhs)` | 非成员比较 | 判断底层位置相同 | 只能比较同一容器的 iterator |
| `operator!=(lhs, rhs)` | 非成员比较 | 判断底层位置不同 | 常用于 `it != end` |

## 12. 一句话总结

`QKeyValueIterator` 是关联容器的键值对读取适配器：它把底层 map/hash iterator 包装成可以解引用为 `std::pair<Key, T>` 的 STL 风格 iterator，并通过 `Traits` 统一提取 key/value。它的 pair 是按值返回，`operator->()` 也是临时代理，因此适合遍历、结构化绑定和只读算法；需要修改容器时，应回到底层 map iterator 的引用式 `value()` API。
