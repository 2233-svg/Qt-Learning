# QRangeModelAdapter::ConstColumnIterator：只读行视图中的随机访问列迭代器

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.11  
> 状态：Preliminary  
> 所属头文件：`#include <QRangeModelAdapter>`

`QRangeModelAdapter::ConstColumnIterator` 用于按列遍历一行模型数据，但不允许经由迭代器修改数据。它是 `ColumnIterator` 的只读对应物，适合检查表格行、导出数据、比较内容，或在 `const QRangeModelAdapter` 上进行算法遍历。

该类型建模 `std::random_access_iterator`。与可写版本最关键的区别不是“const 关键字更严格”这么简单，而是解引用直接得到底层数据的 const 视图，而不是 `DataReference` 写代理，因此不会提供回写 `QAbstractItemModel` 的路径。

## 典型使用

```cpp
const auto &readOnlyTable = table;
const auto row = readOnlyTable.at(0);

for (auto it = row.cbegin(); it != row.cend(); ++it) {
    qDebug() << *it;
}
```

更常用的是范围 for：

```cpp
for (const auto &cell : row) {
    qDebug() << cell;
}
```

`ConstRowReference::begin()`、`cbegin()` 和可写行代理的 const 接口会产生该类型。不要手工构造它，直接从行代理取得 begin/end 配对。

## 解引用语义

- `*it` 返回当前位置的 const 数据类型；
- `it[n]` 返回偏移位置的 const 数据；
- `it->` 提供 const 指针或指针式包装，以便调用 const 成员；
- 不能对 `*it`、`it[n]` 或 `it->` 赋值，也不能调用非 const 成员。

这和 `QRangeModelAdapter` 的设计目标一致：若需要更改模型，必须回到可写 adapter，使用 `DataReference`、`RowReference` 或 `setData()`，从而生成正确的 `dataChanged()` 通知。

```cpp
const auto row = std::as_const(table).at(0);
auto first = row.begin();

int value = *first;
// *first = 42;             // 不可写
// first->setValue(42);     // 不可调用非 const 成员
```

## 随机访问的范围

支持 `++`、`--`、`+`、`-`、`+=`、`-=`、`[]`、距离计算和强排序，但比较域是**同一行**：

```cpp
auto begin = row.cbegin();
auto end = row.cend();
int count = end - begin;
```

比较、排序和相减来自不同行的列迭代器违反前置条件。它们即便恰好有相同列号，也没有共同的序列位置可比较。

随机访问不替代边界校验。不能解引用 `end()`，不能把偏移移动到 `begin()` 前，也不能越过 `end()` 再读取。

## 生命周期与失效

该类型内部依赖模型索引、列号和 adapter。发生以下任一情况后，不再使用已有 const 迭代器：

- 行或列插入、删除、移动；
- adapter `assign()` 或模型 reset；
- 它所依赖的 adapter 与 model 被销毁；
- 相关行的结构被整体替换。

读取值本身通常不会改变结构，但不要把“本轮没有改动”扩展为跨越其他代码、信号回调或线程任务后仍安全。模型对象应在其所属线程使用，后台线程只准备数据，再把修改排队回模型线程。

## 与 ColumnIterator 的转换关系

`ColumnIterator` 可以隐式转换为 `ConstColumnIterator`，用于把可写遍历降级为只读遍历。`ConstColumnIterator` 不可转换回可写版本，因为它可能来自 const adapter 或 const 行代理。

## 常见错误

1. 把 const 列迭代器当作不可见的 `DataReference`，期待可以赋值。
2. 计算来自两行的 `end - begin`，或用 `<` 比较它们。
3. 解引用 `cend()`，或用下标访问超出列数的位置。
4. 在结构变更后继续使用旧 iterator。
5. 以为 const adapter 让底层数据天然线程安全。const 只限制此 API 的写路径，不提供并发同步。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `iterator_category` | 标记为 `std::random_access_iterator_tag`。 | 随机访问仅在同一行内成立。 |
| `difference_type` | 列偏移与距离类型，为 `int`。 | 两端必须来自同一行。 |
| `value_type` | 单元格的数据值类型。 | 对异质行，实际值可能经 `QVariant` 表示。 |
| `reference` | 单元格的 const 访问类型。 | 无法通过它写回模型。 |
| `pointer` | 指向或包装 const 数据的指针类型。 | `operator->()` 只允许 const 成员访问。 |
| `operator*()` | 读取当前列的 const 值。 | 不可解引用 end 或失效迭代器。 |
| `operator->()` | 提供 const 指针式访问。 | 不用于修改底层对象。 |
| `operator[](n)` | 读取偏移 `n` 的 const 值。 | 目标必须仍位于该行的有效范围。 |
| `++` / `--` | 前后移动一列。 | 不可越过 begin/end 边界。 |
| `+`, `-`, `+=`, `-=` | 按列偏移。 | 结果只能在同一行有效区间内。 |
| `lhs - rhs` | 计算列位置距离。 | 必须同一行且同一 adapter。 |
| `==`, `!=`, `<=>` | 比较列位置。 | 只比较同一行的迭代器。 |
| `swap()` | 交换两个游标状态。 | 不交换模型单元格数据。 |

## 一句话总结

`ConstColumnIterator` 提供一行数据的只读随机访问视图：它适合遍历和检查，但不提供任何绕过模型通知的写入口，且只能在同一行、未发生结构变化的短生命周期内使用。
