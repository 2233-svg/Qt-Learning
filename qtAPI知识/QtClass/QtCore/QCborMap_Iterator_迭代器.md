# QCborMap::Iterator 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCborMap>`  
> 模块：`Qt6::Core`  
> 定位：遍历并修改 `QCborMap` 成员值的随机访问迭代器

## 它解决什么问题

`QCborMap::Iterator` 是 `QCborMap::begin()`、`end()` 和 `find()` 返回的可写迭代器。它按“一个键和一个值”为单位遍历 CBOR map：键可读取，但不能通过迭代器直接改名；值以 `QCborValueRef` 代理形式返回，可以原地赋值。

它适用于需要根据现有键修改值的场景，例如规范化配置、删除敏感字段前筛选、批量调整嵌套 CBOR 数据。只读遍历应优先使用 `QCborMap::ConstIterator`，它更清楚地表达意图，并避免不必要的可写分离。

```cpp
for (auto it = map.begin(); it != map.end(); ++it) {
    if (it.key().isString() && it.key().toString() == "enabled")
        it.value() = true;
}
```

## 键是值，值是代理

`key()` 返回独立的 `QCborValue`，不能原地修改键。若要“改键”，应删除旧项再插入新键值对。

`value()` 返回 `QCborValueRef`。给这个代理赋值会写入原 map：

```cpp
auto it = map.find("retryCount");
if (it != map.end())
    it.value() = 3;
```

`*it` 返回 `std::pair<QCborValueConstRef, QCborValueRef>`，适合结构化绑定：

```cpp
for (auto [key, value] : map) {
    if (key.isString() && key.toString() == "name")
        value = "normalized";
}
```

键引用是只读，第二项才是可写代理。不要将 `QCborValueRef` 保存到容器修改或销毁之后；需要长期保存时转为 `QCborValue`。

## 有效期与随机访问的边界

默认构造的迭代器没有指向任何 map，不能调用 `key()`、`value()`、递增或递减。必须先用 `begin()`、`end()`、`find()` 等 map API 初始化。

`QCborMap` 被修改后，已有迭代器可能悬垂，包括 `insert()`、`remove()`、`take()`、`erase()` 等会变更容器内容的操作。遍历时如果要删除项，使用 `erase()` 返回的新迭代器继续循环；不能继续使用被删项的迭代器。

它是随机访问迭代器，因此支持加减偏移和比较位置；不过位置是 map 当前存储顺序中的位置，不是键排序含义。不要用迭代器偏移表达稳定业务顺序。

## 常见误区

- 在未初始化的默认构造迭代器上解引用或递增。
- 通过 `key()` 返回值修改键，以为能改 map。
- 修改 map 后继续使用旧迭代器或 `QCborValueRef`。
- 对 `end()` 做 `++`，或对 `begin()` 做 `--`，会产生未定义结果。
- 只读扫描时仍用 `Iterator`，使代码误导为会修改数据。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `iterator_category` | 声明为随机访问迭代器。 | 可做偏移和距离计算，不将物理位置当业务排序。 |
| 构造 | `Iterator()` | 构造未初始化迭代器。 | 赋值为 `begin()`、`end()` 或 `find()` 结果前不可使用。 |
| 构造 | `Iterator(const Iterator &)` | 复制迭代器位置。 | 副本与原迭代器同样会在 map 修改后失效。 |
| 赋值 | `operator=(const Iterator &)` | 将迭代器重新绑定到另一位置。 | 不延长来源 map 或元素的存活期。 |
| 读取键 | `key() const` | 返回当前项的键。 | 返回值不能改写 map 键；改键应删除并重新插入。 |
| 读取和修改值 | `value() const` | 返回当前项值的 `QCborValueRef`。 | 代理赋值会改原 map，不要跨容器修改保存。 |
| 解引用 | `operator*() const` | 返回键只读引用和值可写代理组成的 pair。 | 结构化绑定时只有第二项可写。 |
| 箭头访问 | `operator->() const` | 访问当前值代理。 | 少用这个低层形式，`value()` 语义更直观。 |
| 前进 | 前置和后置 `operator++` | 移到下一项。 | 不能对 `end()` 递增。 |
| 后退 | 前置和后置 `operator--` | 移到上一项。 | 不能对 `begin()` 递减。 |
| 偏移 | `operator+`、`operator+=` | 向前或向后移动若干项。 | 负偏移可后退，结果必须仍在有效范围内。 |
| 偏移 | `operator-`、`operator-=` | 向后或向前移动若干项，或计算两个迭代器距离。 | 距离与比较只对同一 map 的有效迭代器有意义。 |
| 比较 | `==`、`!=`、`<`、`<=`、`>`、`>=` | 比较两个 `Iterator`，或与 `ConstIterator` 比较位置。 | 只比较同一容器的有效迭代器。 |
| 来源 API | `QCborMap::begin()`、`end()`、`find()` | 获得有效迭代器。 | 首次使用迭代器应从这些 API 获取。 |
| 删除协作 | `QCborMap::erase(iterator)` | 删除当前项并返回后继迭代器。 | 遍历删除时接住返回值继续。 |
| 只读替代 | `QCborMap::ConstIterator` | 只读遍历 map。 | 不修改值时优先使用，表达更清晰。 |

## 一句话总结

`QCborMap::Iterator` 让你遍历键值项并原地修改值，不能修改键。它的能力来自 `QCborValueRef`，它的风险也来自该代理和迭代器在 map 修改后的失效规则。
