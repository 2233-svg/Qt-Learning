# QCborMap::ConstIterator 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCborMap>`  
> 模块：`Qt6::Core`  
> 定位：只读遍历 `QCborMap` 的随机访问迭代器

## 它解决什么问题

`QCborMap::ConstIterator` 用于遍历 CBOR map 而不允许通过迭代器修改成员。它可来自 `constBegin()`、`constEnd()`、const `find()`，也可以在非 const map 上使用；当代码只需要检查、导出、日志记录或校验数据时，它是比 `Iterator` 更合适的默认选择。

只读语义不只是风格问题。它避免把“这段循环可能修改容器”的错误信号传给读者，也避免可写迭代器路径产生不必要的数据分离。需要原地修改值时，才选择 `QCborMap::Iterator`。

```cpp
for (auto it = map.constBegin(); it != map.constEnd(); ++it) {
    qDebug() << it.key() << it.value().toDiagnosticNotation();
}
```

## 键和值都是只读代理

`key()` 返回当前键的 `QCborValue`。`value()` 返回 `QCborValueConstRef`，可转换为 `QCborValue`、可调用类型查询和转换函数，但不能在左侧赋值。

```cpp
for (auto [key, value] : std::as_const(map)) {
    if (key.isString() && key.toString() == "mode")
        qDebug() << value.toString();
}
```

解引用结果是“键只读引用和值只读引用”的 pair，因此结构化绑定的两项都不能修改 map。若需要改值，改用 `Iterator::value()` 获取 `QCborValueRef`。

## 有效期与边界

默认构造的迭代器未初始化，调用 `key()`、`value()`、`++` 或 `--` 都是不合法的。先从 map 的迭代接口取得有效位置。

map 内容一旦被修改，所有既有迭代器都可能悬垂，即使迭代器本身是 const。读取过程中不要让其他代码同时对该 map 做结构或值修改。`++end()` 和 `--begin()` 也会导致未定义结果。

它是随机访问迭代器，支持位置偏移和比较；这些位置反映内部项顺序，不应被用作业务上的键排序或稳定协议顺序。

## 常见误区

- 认为 const iterator 能抵抗容器修改导致的失效。
- 对 `value()` 返回的 `QCborValueConstRef` 赋值。
- 使用默认构造迭代器后忘记初始化。
- 将随机访问的索引位置误当成 map 键的排序结果。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `iterator_category` | 表明它是随机访问迭代器。 | 支持偏移和距离计算，不代表业务顺序。 |
| 构造 | `ConstIterator()` | 创建未初始化迭代器。 | 赋值为有效 map 迭代器前不可使用。 |
| 构造与赋值 | 拷贝构造和 `operator=` | 复制迭代器位置。 | map 修改后副本同样可能失效。 |
| 读取键 | `key() const` | 返回当前项键。 | 只能读取，不能通过返回值改键。 |
| 读取值 | `value() const` | 返回当前项的 `QCborValueConstRef`。 | 是只读代理，长期保存时转为 `QCborValue`。 |
| 解引用 | `operator*() const` | 返回当前键和值的只读 pair。 | 结构化绑定中两个成员均不可写。 |
| 箭头访问 | `operator->() const` | 访问当前只读值代理。 | 通常 `value()` 的意图更清楚。 |
| 前进 | 前置和后置 `operator++` | 移到下一项。 | 不能对 `constEnd()` 递增。 |
| 后退 | 前置和后置 `operator--` | 移到上一项。 | 不能对 `constBegin()` 递减。 |
| 偏移 | `operator+`、`operator+=` | 向前或向后移动指定项数。 | 结果必须仍位于有效范围。 |
| 偏移 | `operator-`、`operator-=` | 后退或计算两个迭代器的距离。 | 仅对同一 map 的有效迭代器有意义。 |
| 比较 | `==`、`!=`、`<`、`<=`、`>`、`>=` | 比较两个 const 迭代器的位置。 | 只比较同一容器内的有效迭代器。 |
| 来源 API | `constBegin()`、`constEnd()`、const `find()` | 获取只读迭代器。 | 非 const map 只读遍历时也优先使用。 |
| 可写替代 | `QCborMap::Iterator` | 遍历并原地修改值。 | 只有确实需要赋值时才改用它。 |

## 一句话总结

`QCborMap::ConstIterator` 是 map 遍历的默认选择：键和值都只读，语义明确且更轻。它不能防止容器修改造成失效，所以遍历期间仍要保持 map 稳定。
