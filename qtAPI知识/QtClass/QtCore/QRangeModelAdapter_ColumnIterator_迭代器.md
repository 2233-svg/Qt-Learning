# QRangeModelAdapter::ColumnIterator：可写行代理中的随机访问列迭代器

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.11  
> 状态：Preliminary  
> 所属头文件：`#include <QRangeModelAdapter>`

`QRangeModelAdapter::ColumnIterator` 是 `QRangeModelAdapter` 可写行代理的列迭代器。它解决的是“遍历表格或树中某一行的每个单元格时，如何保持模型通知”这一问题。

它看起来像标准随机访问迭代器，但解引用并不返回底层容器的 `T &`，而是返回 `DataReference`。给这个代理赋值会经由 `QAbstractItemModel::setData()` 更新数据并发出模型通知，避免视图缓存与持久索引失真。

## 从行代理取得，而不是手工构造

```cpp
QRangeModelAdapter table(std::vector<std::vector<int>>{
    {1, 2, 3},
    {4, 5, 6},
});

auto row = table.at(0);
for (auto cell : row) {
    int value = cell;
    cell = value * 10;
}
```

`row.begin()` 返回 `ColumnIterator`，`row.end()` 返回同一行末尾的迭代器。不要自行拼接 `QModelIndex`、列号和 adapter 来构造它；公开构造路径是实现细节，行代理给出的 begin/end 才能保证比较和范围一致。

## 解引用后的写入语义

```cpp
auto it = row.begin();

int oldValue = *it;  // DataReference 可读为 const 值
*it = oldValue + 1;  // 经模型写回，通知 dataChanged()
```

`*it`、`it[n]` 与 `it->` 都是代理入口：

- `*it` / `it[n]` 返回 `DataReference` 值；
- `it->` 返回同一个代理，便于访问底层值的 const 成员；
- 不能借 `->` 调用非 const 成员来偷偷修改对象，因为那会绕过模型通知；
- 要修改复杂对象时，读取副本、修改副本，再赋回代理。

```cpp
auto cell = row.begin();
Book copy = *cell;
copy.setRating(5);
*cell = copy;
```

## 随机访问迭代器的前提

该类型建模 `std::random_access_iterator`，支持递增、递减、加减偏移、下标、距离比较和强排序。这里的“随机访问”仅指同一模型行内可按列号跳转，不意味着可以对任意两个 `ColumnIterator` 计算距离。

相减、相等比较和排序比较都要求迭代器来自同一行；距离计算还要求属于同一 adapter。把不同行的 `begin()` 混在一起比较或相减违反前置条件，调试构建会断言。

```cpp
auto a = table.at(0).begin();
auto b = table.at(0).end();
int columns = b - a; // 合法

auto other = table.at(1).begin();
// b - other;        // 不同一行，违反前置条件
```

## 失效规则

把它当作模型索引上的短寿命游标。插入、删除、移动行列，整体 `assign()`、model reset、adapter 销毁，都会使旧迭代器或其 `DataReference` 不能再可靠使用。即使底层容器刚好不让迭代器失效，模型索引和列位置的语义也可能已变。

遍历中修改当前单元格值是合理的；遍历中改变行的结构不是。需要插入或删除列时，先结束本轮迭代，再调用 adapter 的结构 API。

## 与 ConstColumnIterator 的关系

`ColumnIterator` 可隐式转换为 `ConstColumnIterator`。转换后保留当前位置，但只读解引用；不能反向把 const 迭代器恢复为可写迭代器。

```cpp
auto writable = table.at(0).begin();
QRangeModelAdapter<decltype(table.range())>::ConstColumnIterator readOnly = writable;
```

实际代码通常不需要写出嵌套类型，让 `auto` 或 const 行代理推导即可。由于 adapter 是模板，手写该类型往往比让编译器推导更脆弱。

## 常见错误

1. 以为 `*it` 是底层元素引用，试图通过非 const 成员原地修改对象。它是通知型代理。
2. 比较来自不同行的列迭代器，或计算它们的距离。
3. 在 `for` 循环内插入、删除、移动列后继续递增旧 iterator。
4. 保存 `it->` 或 `*it` 得到的代理，跨 model reset 或 adapter 销毁后继续写。
5. 把 Preliminary 迭代器类型放进长期稳定的公开 ABI。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `iterator_category` | 标记为 `std::random_access_iterator_tag`。 | 仅在同一行内满足随机访问语义。 |
| `difference_type` | 列偏移与距离类型，为 `int`。 | 距离和排序要求来自同一行、同一 adapter。 |
| `value_type` / `reference` / `pointer` | 都围绕 `DataReference` 代理定义。 | 不把它当作裸 `T *` 或 `T &`。 |
| `operator*()` | 返回当前位置的 `DataReference`。 | 读取为值，赋值经模型写回并通知。 |
| `operator->()` | 返回当前单元格代理。 | 仅用于 const 成员访问；不能绕过通知直接改对象。 |
| `operator[](n)` | 返回偏移 `n` 处的单元格代理。 | 范围必须仍在当前行的 `[begin, end)` 内。 |
| `++it` / `it++` | 前进一个列。 | 不可解引用 `end()`，也不可越过行边界。 |
| `--it` / `it--` | 后退一个列。 | 不可在 `begin()` 前继续后退。 |
| `it + n` / `n + it` / `it += n` | 向后跳 `n` 列。 | 目标列必须有效或恰好为 end。 |
| `it - n` / `it -= n` | 向前跳 `n` 列。 | 不能落到 begin 之前。 |
| `lhs - rhs` | 计算两个列位置的差。 | 两者必须同一行且同一 adapter。 |
| `==`, `!=`, `<=>` | 比较列位置。 | 仅比较同一行的迭代器。 |
| `swap(lhs, rhs)` | 交换迭代器位置。 | 交换的是游标状态，不交换模型数据。 |
| 转为 `ConstColumnIterator` | 放弃写能力，保留当前列位置。 | 单向转换，不能从 const 迭代器恢复写权限。 |

## 一句话总结

`ColumnIterator` 是“列位置 + 模型写入代理”：它能像随机访问迭代器一样遍历一行，但所有写入都必须通过 `DataReference` 完成，且比较、距离计算和生命周期都局限在同一行、同一个存活的 adapter 中。
