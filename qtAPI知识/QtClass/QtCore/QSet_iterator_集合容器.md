# QSet::iterator：可在遍历中删除元素的前向游标

> 适用版本：Qt 6.11.1  
> 所属头文件：`#include <QSet>`  
> 所属模块：Qt Core

`QSet<T>::iterator` 是 `QSet` 的非 const STL 风格 iterator。它的“可写”不表示可修改元素：解引用仍是 `const T &`。它存在的主要用途是让调用者在遍历中安全调用 `QSet::erase()` 删除当前位置。

原因在于 QSet 的元素同时是哈希 key。直接把一个元素改成不同值可能改变其 `qHash()` 结果，元素必须迁移到另一哈希桶；Qt 因而禁止通过 iterator 原地改值。

## 实际使用场景

筛掉满足条件的 ID、过期项或失效指针时，用 `erase()` 返回的后继 iterator 继续循环：

```cpp
auto it = sessions.begin();
while (it != sessions.end()) {
    if (isExpired(*it))
        it = sessions.erase(it);
    else
        ++it;
}
```

这比在范围 for 中调用 `remove(*it)` 更可靠。`remove()` 可能触发哈希表结构变化，而范围 for 内部的 iterator 并不会自动更新；`erase(it)` 明确把后继有效位置返回给调用方。

如果只是读取，使用 `const_iterator` 更合适。它同样访问 const 元素，且更清楚表达不会改变集合结构。

## 不是“可修改元素”的 iterator

下面的写法不成立：

```cpp
auto it = set.begin();
*it = replacement; // 错误：operator*() 返回 const T &
```

要“替换”集合中的某值，先删除旧值再插入新值：

```cpp
if (set.remove(oldValue))
    set.insert(newValue);
```

这一过程可能使其他 iterator 失效；不要在保留多个 iterator 的情况下执行它。若替换后新旧值根据 `operator==` 视为相同，插入不会增加元素。

## 前向而非双向或随机访问

Qt 6.11.1 的公开头文件把 `iterator_category` 定义为 `std::forward_iterator_tag`。支持：

- 解引用 `*it`、`it->member`；
- `++it`、`it++`；
- 和同一集合的 `end()` / `const_iterator` 比较。

不支持：

- `--it`；
- `it + n`、`it[n]`；
- 根据迭代位置推导插入顺序；
- 按 iterator 距离计算集合大小。

集合迭代顺序未指定；即使同一进程中目前看起来稳定，也不能用它建立业务排序。

## 与 const iterator 的互操作

`iterator` 可与 `const_iterator` 做相等和不等比较，方便把可写游标与 `cend()` 之类只读哨兵比较；但通常应使用同一组 `begin()` / `end()` 取得的 iterator，避免让代码依赖隐式转换细节。

默认构造 iterator 未初始化。不能解引用、前进、比较或当作“空 iterator”；未找到元素应使用 `set.end()`，不是默认构造值。

## 隐式共享和失效边界

QSet 是隐式共享容器。持有 `iterator` 时对 set 做复制、赋值、插入、删除、clear、reserve、squeeze 或 swap，可能 detach 或重建哈希表。除 `erase(pos)` 返回值外，保守地把所有旧 iterator、元素引用和指针都视为不可继续使用。

尤其不要这样写：

```cpp
auto it = set.begin();
QSet<T> snapshot = set; // 共享数据
set.insert(value);       // detach，it 的语义不再应被依赖
```

需要快照迭代而源 set 又会被修改时，用 `QSetIterator`；它持有隐式共享副本并继续遍历创建时的数据。需要在当前 set 上修改时，用这里的 `erase()` 模式，且把修改限制在单一线程和单一遍历流程。

## 常见错误

1. **把 `iterator` 当 `T &`。** 它仍返回 const 元素。
2. **删除后 `++it`。** 被删 iterator 已失效；应接住 `erase()` 的返回值。
3. **使用 `--` 或随机访问。** 它只是前向 iterator。
4. **用默认构造 iterator 表示未找到。** 用 `end()`。
5. **修改 set 后继续使用其他 iterator。** 重新获取。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `iterator_category` | `std::forward_iterator_tag`。 | 只能向前 `++`，没有 `--` 或随机访问。 |
| `value_type` / `pointer` / `reference` | 分别为 `T`、`const T *`、`const T &`。 | 非 const iterator 仍禁止修改元素。 |
| `difference_type` | STL 兼容差值类型。 | 没有 iterator 相减操作。 |
| `iterator()` | 构造未初始化 iterator。 | 只能先被赋成有效 set iterator。 |
| 拷贝构造 / 赋值 | 复制当前位置。 | 不延长容器或底层共享数据的逻辑有效期。 |
| `operator*()` | 返回当前元素的 `const T &`。 | 不可修改，不可解引用 end。 |
| `operator->()` | 返回当前元素的 `const T *`。 | 仅能访问 const 成员。 |
| `operator++()` | 前置前进。 | 遍历中优先使用，不能递增 end。 |
| `operator++(int)` | 后置前进。 | 返回旧位置副本，通常比前置多一次复制。 |
| `operator==` / `operator!=`（iterator） | 比较两个可写 iterator。 | 仅对同一 set、同一版本的 iterator 有意义。 |
| `operator==` / `operator!=`（const_iterator） | 与只读 iterator 比较位置。 | 仍应避免跨容器或跨 detach 比较。 |
| `QSet::erase(const_iterator pos)` | 删除当前位置并返回后继 `iterator`。 | 遍历删除的唯一推荐路径；pos 不能是 end。 |

## 一句话总结

`QSet::iterator` 的可写权限只用于改变集合结构而不是改 key：它是前向游标，遍历删除时写成 `it = set.erase(it)`，其余任何结构变化后都重新取 iterator。
