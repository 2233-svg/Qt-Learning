# QSet：无序、去重、快速查找的 Qt 哈希集合

> 适用版本：Qt 6.11.1  
> 所属头文件：`#include <QSet>`  
> 所属模块：Qt Core

`QSet<T>` 是 Qt 的无序去重集合，内部基于 `QHash` 实现。它适合回答“这个值是否已经出现”“两个权限集合是否有交集”“需要从大量候选中快速去重”这类问题，而不适合依赖稳定排列、索引位置或按键排序的场景。

`QSet` 是隐式共享的值类型：复制通常很轻，但后续对某一副本的修改会 detach。这个特性配合迭代器时有一条重要规则：**不要在某个 set 上持有 STL iterator 的同时复制或修改该 set。**

## 什么时候用它

```cpp
QSet<QString> enabledFeatures;
enabledFeatures.insert("export");
enabledFeatures.insert("sync");
enabledFeatures.insert("export"); // 重复插入不会增加元素

if (enabledFeatures.contains("sync")) {
    startSynchronization();
}
```

实际场景：

- 用户权限、标签、已处理 ID、已打开文档的去重集合；
- 判断两个集合是否有共同项，例如 `intersects()`；
- 从输入序列消除重复值；
- 用集合交、并、差表达筛选规则。

若需要稳定遍历顺序，使用 `QMap`、排序后的 `QList` 或基于业务字段显式排序后的 `values()`。`QSet` 的迭代顺序未指定，不能依赖一次运行中的顺序，更不能写入持久格式或 UI 后期待该顺序稳定。

## 元素类型要求

`T` 必须是可赋值类型，能用 `operator==()` 比较，并有可见的全局 `qHash()` 重载。自定义类型通常需要：

```cpp
struct Permission {
    QString scope;
    int level = 0;

    friend bool operator==(const Permission &, const Permission &) = default;
};

size_t qHash(const Permission &permission, size_t seed = 0) noexcept
{
    return qHashMulti(seed, permission.scope, permission.level);
}
```

哈希和相等关系必须一致：若 `a == b`，则在相同 seed 下两者的哈希必须相同。不要在元素已经插入后修改参与 `operator==` 或 `qHash` 的字段，尤其是集合存指针、而指向对象的值又参与哈希时；此时元素会留在旧桶中，`contains()` 和 `remove()` 的逻辑结果将变得不可预测。

不能把不可复制的 `QWidget` 之类 QObject 子类按值放进 set；通常存 `QWidget *`、`QPointer<QWidget>` 或领域 ID。存裸 QObject 指针时，set 不拥有对象，也不会在 QObject 销毁时自动移除悬空指针。

## 插入、查找与删除

```cpp
QSet<int> ids = {3, 7, 11};

ids.insert(7);                   // 无变化
ids.insert(13);                  // 新增

if (ids.contains(11)) {
    ids.remove(11);              // 返回 true
}
```

`insert()` 无论值是否已存在都会返回指向集合中该值的 iterator。`remove(value)` 因为 set 没有重复项，所以删除成功返回 `true`，否则 `false`。

`find()` / `constFind()` 找不到时分别返回 `end()` / `constEnd()`，而不是空指针。`contains(otherSet)` 是子集判断：仅当当前集合包含 `otherSet` 的所有值时才为 true，不是“有任意交集”；判断任意共同元素用 `intersects(otherSet)`。

Qt 6.1 新增的 `insert(const_iterator hint, const T &value)` 为兼容标准容器提供 hint 形态，但 `QSet` 无序，Qt 6.11.1 实现不使用该 hint。不要为它计算或缓存“插入位置”，这不会改善哈希集合定位，也不承诺迭代顺序。

## 遍历和安全删除

`QSet` 的 iterator 以 `std::forward_iterator_tag` 暴露，只支持向前 `++`，没有 `--`、随机访问、下标或稳定位置语义。

更反直觉的是，`QSet::iterator` 解引用也返回 `const T &`，无法通过 `*it = value` 修改元素。修改元素可能改变哈希值并要求重放到另一个桶，因此 Qt 只允许用 iterator 删除元素：

```cpp
auto it = ids.begin();
while (it != ids.end()) {
    if (shouldRemove(*it))
        it = ids.erase(it);      // 返回下一个有效位置
    else
        ++it;
}
```

只读遍历优先使用 `cbegin()` / `cend()`：

```cpp
for (auto it = ids.cbegin(), end = ids.cend(); it != end; ++it) {
    consume(*it);
}
```

它既表达只读意图，也避免为了取得非 const `begin()` 而触发不必要的隐式共享 detach。不要长期保存 iterator；插入、删除、清空、reserve、squeeze、swap、赋值、detach 或其他可能重建哈希表的操作之后，重新取得 iterator。唯一适合在循环里继续使用的删除路径是 `erase(pos)` 返回的那个后继 iterator。

## 隐式共享与 Java 风格迭代器

复制 `QSet` 通常共享底层数据，直到某一份被修改：

```cpp
QSet<QString> original = loadTags();
QSet<QString> copy = original;  // 通常为廉价共享
copy.insert("draft");            // copy detach，original 不变
```

STL 风格 iterator 对这种 detach 很敏感，Qt 文档称其为“隐式共享 iterator 问题”。有活动 iterator 时复制容器，之后再修改其中一份，可能让代码看似在遍历同一对象，实际却落到旧共享数据或失效位置。范围 for 中不要对正在遍历的同一个 `QSet` 赋值、复制或做结构修改。

`QSetIterator<T>` 是只读 Java 风格迭代器，内部保存 set 的隐式共享副本，因此原 set 后续修改会 detach，iterator 继续遍历构造时的原始集合视图。它适合兼容旧代码或需要稳定快照式只读遍历，但现代新代码通常优先使用 STL 风格 const iterator 或范围 for。

## 集合运算

```cpp
QSet<QString> granted = {"read", "export"};
QSet<QString> required = {"export", "delete"};

const QSet<QString> missing = required - granted;
const QSet<QString> common = granted & required;
const QSet<QString> all = granted | required;
```

原地操作：

- `unite(other)` / `|=` / `+=`：并集；
- `intersect(other)` / `&=`：保留共同元素；
- `subtract(other)` / `-=`：移除 other 中出现的元素；
- `&= value`：只保留一个等于 `value` 的元素（若有）。

非成员 `+` 是并集的别名，返回新 set。右值 overload 可减少临时对象移动/分配，但不要为追求语法压缩而牺牲集合运算的可读性。

## 容量和性能

查找、插入、删除平均为常数时间，但 hash 质量和冲突分布会影响实际成本。`QSet` 会自行增长和收缩；只有在预先知道元素量较大时才调用 `reserve()`：

```cpp
QSet<QString> emails;
emails.reserve(importedRows.size());

for (const auto &row : importedRows)
    emails.insert(row.email);
```

`capacity()` 是内部哈希桶数量，不是元素数量；实际元素数用 `size()`。大量删除后若明确希望降低内存占用，可 `squeeze()`，但它可能重建内部表，所以不要在活跃 iterator 或性能敏感热路径中随意调用。

`values()` 会生成新的 `QList<T>`，且列表顺序未定义。若想用于 UI、测试快照或序列化，应先显式排序。

## 线程与生命周期

`QSet` 不带 QObject 线程亲和性，按值传递或移动到工作线程是正常的；前提是没有多个线程同时读写**同一个实例**。共享副本并不让并发写入自动安全，detach 也不替代同步。

对指针元素尤其要区分“容器寿命”和“对象寿命”：set 析构只销毁指针值，不销毁指向对象。跨线程传递 `QSet<QObject *>` 也不会让其中 QObject 可在接收线程直接使用。

## 常见错误

1. **依赖迭代顺序。** `QSet` 是无序哈希集合。
2. **把 `contains(other)` 当作“有交集”。** 它是“other 是我的子集”；任意交集用 `intersects()`。
3. **通过 iterator 改元素。** `*it` 是 const；删除后重新插入新值。
4. **遍历中普通 `remove()`。** 用 `it = erase(it)`，或预先收集待删元素。
5. **复制或修改 set 时继续持有 STL iterator。** 隐式共享 detach 会造成 iterator 问题。
6. **使用不一致的 `qHash` / `operator==`。** 这会破坏哈希查找契约。
7. **把 `capacity()` 当元素数。** 元素数是 `size()`。
8. **将 `values()` 结果当排序列表。** 返回顺序未定义。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `value_type` / `key_type` | 元素类型 `T` 的别名。 | `T` 必须可赋值、可相等比较且可哈希。 |
| `size_type` / `difference_type` | STL 兼容的大小/差值类型。 | 不提供基于索引的集合位置语义。 |
| `reference` / `const_reference` / `pointer` / `const_pointer` | STL 兼容别名。 | iterator 实际只暴露元素的 const 访问。 |
| `Iterator` / `ConstIterator` | Qt 风格的 `iterator` / `const_iterator` 别名。 | 新代码通常直接使用标准命名。 |
| `QSet()` | 构造空集合。 | 不分配元素。 |
| `QSet(initializer_list)` | 从初始化列表去重构造。 | 重复元素只保留一个。 |
| `QSet(first, last)` | 从输入范围构造。 | 范围是半开 `[first, last)`；元素仍会去重。 |
| `begin()` / `end()` | 获取可用于删除的前向 iterator 范围。 | 非 const iterator 也不能改元素；不要跨结构变化保存。 |
| `cbegin()` / `cend()` | 获取只读前向 iterator 范围。 | 只读遍历首选，避免不必要 detach。 |
| `constBegin()` / `constEnd()` | Qt 风格 const iterator 入口。 | 语义等同 `cbegin()` / `cend()`。 |
| `capacity()` | 返回内部哈希桶数量。 | 不是元素数。 |
| `reserve(size)` | 预留至少对应规模的桶。 | 大批量已知数量插入前使用；可能使 iterator 失效。 |
| `squeeze()` | 收缩内部哈希表以节省内存。 | 可能重建桶；活跃 iterator 全部重新获取。 |
| `size()` / `count()` | 返回元素数量。 | 两者等价。 |
| `isEmpty()` / `empty()` | 判断是否无元素。 | 两者等价，后者为 STL 兼容。 |
| `insert(value)` | 插入值并返回其 iterator。 | 已存在时不重复插入。 |
| `insert(hint, value)` | 带 hint 的插入形式。 | Qt 6.1 起；无序 set 不使用 hint 作定位优化。 |
| `contains(value)` | 判断单个值是否存在。 | 平均常数时间，依赖正确 `qHash`。 |
| `contains(otherSet)` | 判断 `otherSet` 是否为当前集合的子集。 | 不是交集检测。 |
| `find()` / `constFind()` | 查找元素并返回 iterator。 | 未找到比较 `end()` / `constEnd()`。 |
| `remove(value)` | 移除指定值。 | 返回是否实际删除。 |
| `erase(pos)` | 删除 pos 指向的元素并返回后继。 | `pos` 不能是 end；安全遍历删除用它。 |
| `removeIf(pred)` / `erase_if(set, pred)` | 删除满足谓词的全部元素，返回删除数。 | Qt 6.1 起；谓词不要修改同一 set。 |
| `clear()` | 移除所有元素。 | iterator 和元素引用不再可用。 |
| `values()` | 返回包含全部值的新 `QList`。 | 产生复制，顺序未定义。 |
| `unite()` / `|=` / `+=` / `operator|` / `operator+` | 执行并集。 | 原地与返回新集合版本要区分。 |
| `intersect()` / `&=` / `operator&` | 执行交集。 | 原地版本会删除不在 other 的元素。 |
| `subtract()` / `-=` / `operator-` | 执行差集。 | 原地版本会删除 other 中存在的元素。 |
| `intersects(other)` | 判断是否至少有一个共同元素。 | 用于“任意交集”检查。 |
| `swap(other)` | 常数级交换两个 set 的内部数据。 | 旧 iterator 不能继续按原容器解释。 |
| `==` / `!=` | 比较两个 set 的元素集合。 | 不比较迭代顺序。 |
| `QDataStream <<` / `>>` | 序列化和反序列化集合。 | 遍历顺序未定义，不应用顺序承载额外语义。 |

## 一句话总结

`QSet` 是基于哈希的无序去重集合：元素必须有一致的相等与哈希规则，不能经 iterator 改 key，遍历删除用 `erase()` 返回值，并且绝不把隐式共享容器的复制/detach 与活跃 STL iterator 混在一起。
