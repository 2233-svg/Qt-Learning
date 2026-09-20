# QSet::const_iterator：只读前向遍历无序集合

> 适用版本：Qt 6.11.1  
> 所属头文件：`#include <QSet>`  
> 所属模块：Qt Core

`QSet<T>::const_iterator` 是遍历 `QSet<T>` 元素的只读 STL 风格 iterator。它适用于查看、导出、筛选和传入标准算法，但不能修改元素或删除元素。

`QSet` 是哈希集合，因此这个 iterator 不是列表下标，也不是排序游标。Qt 6.11.1 头文件将其类别定义为 `std::forward_iterator_tag`：只能前进，不支持 `--`、`+n`、`[]` 或稳定顺序。

## 为什么要优先使用它

即使 set 本身不是 const，只读遍历也应优先取 `cbegin()` / `cend()`：

```cpp
for (auto it = set.cbegin(), end = set.cend(); it != end; ++it) {
    qDebug() << *it;
}
```

这样把“本循环不会改集合”写进类型，并避免为了调用非 const `begin()` 而触发隐式共享 detach。`QSet::iterator` 也不能改元素值，因此只有需要 `erase()` 当前元素时才需要非 const iterator。

无序性意味着上面循环的输出顺序不能用于 UI 排序、测试快照或持久化格式。要得到稳定顺序，复制到 `QList` 后显式排序。

## 解引用、比较和有效性

`*it` 返回 `const T &`，`it->member` 返回 `const T *`。不能通过它修改 key：

```cpp
const auto it = set.constFind(id);
if (it != set.cend()) {
    inspect(*it);
}
```

默认构造的 `const_iterator` 是未初始化 iterator，只能作为之后马上被赋值的变量；不能解引用、递增、比较或拿它与 `end()` 比较。可靠来源是 `begin()`、`cbegin()`、`end()`、`cend()`、`find()`、`constFind()` 或从现有 iterator 拷贝构造。

比较仅对同一个集合、同一底层版本中获得的 iterator 有意义。`end()` 只是尾后哨兵，绝不能解引用。

## 隐式共享和失效规则

QSet 是隐式共享容器。持有 iterator 时复制 set，随后修改任一份，可能发生 detach；Qt 明确提醒这不完全遵循开发者对 STL iterator 的直觉。

最稳妥规则是：

- iterator 存活期间不复制、赋值、swap 或结构修改同一 set；
- `insert()`、`remove()`、`erase()`、`clear()`、`reserve()`、`squeeze()` 后，重新获取全部 iterator；
- 若要删除筛选结果，先收集值，或改用非 const iterator 的 `erase()` 循环；
- 不从一个线程遍历 set，同时让另一个线程修改同一个实例。

`const_iterator` 只限制当前访问路径，不能令另一个别名或其他线程的写入变安全。

## 常见错误

1. **按顺序解释遍历结果。** QSet 无序。
2. **对 `*it` 赋值。** 元素是哈希 key，只读访问。
3. **写 `--it` 或 `it + 3`。** Qt 6.11.1 的类型是前向 iterator。
4. **使用默认构造 iterator。** 它未初始化。
5. **复制/修改 set 后继续使用旧 iterator。** 可能已 detach 或失效。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `iterator_category` | `std::forward_iterator_tag`。 | 只支持向前 `++`，没有反向或随机访问。 |
| `value_type` / `pointer` / `reference` | 分别对应 `T`、`const T *`、`const T &`。 | 元素只读，不能改 key。 |
| `difference_type` | STL 兼容差值类型。 | 不代表支持 iterator 相减。 |
| `const_iterator()` | 构造未初始化 iterator。 | 必须先赋予来自 set 的有效位置。 |
| `const_iterator(iterator)` | 从可写 iterator 构造只读 iterator。 | 允许只读降级，不可反向转换。 |
| 拷贝构造 / 赋值 | 复制当前位置。 | 两个 iterator 仍依赖同一容器版本。 |
| `operator*()` | 返回当前元素的 `const T &`。 | 不可用于 end 或未初始化 iterator。 |
| `operator->()` | 返回当前元素的 `const T *`。 | 不可调用非 const 成员函数。 |
| `operator++()` | 前置前进到下一元素。 | 不可递增 end。 |
| `operator++(int)` | 后置前进并返回旧位置副本。 | 热路径优先前置 `++it`。 |
| `operator==` / `operator!=` | 比较两个 const iterator 是否同位。 | 只比较同一 set、同一有效版本的 iterator。 |

## 一句话总结

`QSet::const_iterator` 是无序哈希集合的只读前向游标：从 `cbegin()` 获取、只做 `++`、不改元素、不跨 detach 或结构变化保存。
