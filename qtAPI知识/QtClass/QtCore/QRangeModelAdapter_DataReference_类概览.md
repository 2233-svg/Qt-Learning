# QRangeModelAdapter::DataReference：可赋值，但不会绕过模型通知的单元格代理

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.11  
> 状态：Preliminary  
> 所属头文件：`#include <QRangeModelAdapter>`

`QRangeModelAdapter::DataReference` 是一个指向模型单元格的写入代理。它不是 `T &`，也不是 `std::reference_wrapper<T>`。它解决的核心问题是：让下面这种自然的 C++ 写法仍然经过 `QAbstractItemModel`：

```cpp
adapter[0] = newValue;
```

赋值时，代理调用模型 API 写入对应单元格，从而让视图收到 `dataChanged()`。如果 adapter 直接交出可修改引用，调用者可以修改容器而模型毫不知情，Qt Quick 绑定、Widgets 视图缓存和持久索引都会落后于真实数据。

## 从哪里得到它

`DataReference` 通常由 adapter 自动生成：

- 列表 adapter 的可写 `at(row)`、`operator[](row)`；
- 表格或树的可写 `at(row, column)`、`at(path, column)`；
- 可写 `RowIterator` 解引用列表项；
- 可写 `ColumnIterator` 解引用单元格；
- 可写 `RowReference::at(column)`。

```cpp
QRangeModelAdapter numbers(std::vector<int>{1, 2, 3});

auto second = numbers.at(1);
second = 99;
```

虽然可从 `QModelIndex` 显式构造，实际业务代码应从上述 adapter API 取得。手工包装一个来自错误 model、已销毁 model 或过期结构的索引，无法获得安全的引用语义。

## 读取：只有 const 视图

`get()`、隐式转换与 `operator->()` 都以 const 形式访问值：

```cpp
auto item = adapter[0];

const Book book = item.get();
qDebug() << item->title(); // 只允许 const 成员
```

复杂类型要修改时采用“读副本、改副本、赋回”：

```cpp
auto item = books[0];
Book updated = item;
updated.setRating(5);
item = updated;
```

这样模型能统一发出变化通知。`operator->()` 返回的可能是指针式包装，不应保存它跨越代理、adapter 或模型生命周期。

## 赋值：是写值，不是重新绑定

这点与 `std::reference_wrapper` 明显不同：

```cpp
auto first = adapter[0];
auto second = adapter[1];

first = second;
```

这里不会让 `first` 改为“指向第二个单元格”。它把第二个单元格当前的值复制或移动到第一个单元格，两个代理仍各自指向原来的索引。

支持从 `value_type` 复制或移动赋值，也支持从另一个 `DataReference` 复制或移动赋值。对异质表格列，`value_type` / `const_value_type` 会是 `QVariant` / `const QVariant`，需要按真实类型转换。

## 失败与有效性

`isValid()` 只回答内部 `QModelIndex` 当前是否有效。调用 `get()` 前应先检查它，尤其是代理可能来自可选索引、查找失败或结构变更之前的缓存。

代理赋值没有 `bool` 返回值。源码在调试构建中会对无法写入发出警告，发布构建不应依赖该诊断作为控制流。若业务必须得知转换失败、只读拒绝或角色不支持，使用 `QRangeModelAdapter::setData()`，检查它返回的 `bool`。

插入、删除、移动行列、`assign()`、model reset 或销毁 adapter 后，旧代理不应继续使用。它保存的是普通 `QModelIndex`，不是自动跨结构追踪的 `QPersistentModelIndex`。

## 相等性与交换

两个 `DataReference` 的相等性是值式的：它们指向同一个模型索引时相等；即使索引不同，只要当前底层值相等，比较也可能为真。因此不要用它做“单元格身份”的唯一键；需要身份时保存 `QModelIndex` 或自己的领域 ID。

`swap(lhs, rhs)` 会交换底层单元格值，而不是交换两个代理的绑定位置。它同样依赖两次模型写入，不适合作为需要强异常保证或严格原子性的事务工具。

## 常见错误

1. 把 `DataReference` 当成 `T &`，通过 `->` 调用非 const setter。
2. 认为 `left = right` 会改变 left 的引用目标。它复制 right 的值。
3. 在结构修改后继续使用旧代理。
4. 依赖 `operator=` 的隐式诊断判断写入成功。需要成功状态时改用 `setData()`。
5. 在异质列中把代理直接当成某一固定 C++ 类型，忽略它可能是 `QVariant`。
6. 用 `DataReference` 相等比较判断两个位置是否相同。值相等的不同单元格也可能比较为相等。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `DataReference(const QModelIndex &index)` | 为指定模型索引创建代理。 | 主要供 adapter 内部使用；索引必须属于存活且匹配的 model。 |
| 拷贝/移动构造 | 复制或移动代理的索引状态。 | 不复制单元格值，也不延长 model 生命周期。 |
| `value_type` | 底层项目的写入值类型。 | 异质列时为 `QVariant`。 |
| `const_value_type` | 底层项目的 const 读取类型。 | 异质列时为 `const QVariant`。 |
| `pointer` | `operator->()` 返回的指针式类型。 | 只用于短时 const 成员访问。 |
| `get()` | 读取代理当前指向的 const 值。 | 先保证 `isValid()`；不提供可写裸引用。 |
| `operator const_value_type()` | `get()` 的隐式读取形式。 | 可能发生值复制，避免在热路径反复隐式转换大对象。 |
| `operator->()` | 访问值的 const 成员。 | 不可调用非 const setter，也不要长期保存返回指针。 |
| `isValid()` | 判断内部模型索引是否有效。 | 结构变更后旧代理仍应视为不可继续使用。 |
| `operator=(const value_type &)` | 将值复制写入模型单元格。 | 经模型发通知；需要明确成功与否时用 `setData()`。 |
| `operator=(value_type &&)` | 将值移动写入模型单元格。 | 底层模型仍可能因类型/只读约束拒绝写入。 |
| `operator=(const DataReference &)` | 把另一个代理当前值复制到此单元格。 | 是值复制，不是代理重新绑定。 |
| `operator=(DataReference &&)` | 把另一个代理当前值移动到此单元格。 | 源代理仍指向原索引。 |
| `swap(lhs, rhs)` | 交换两个单元格的值。 | 不是交换引用位置，且不是原子事务。 |
| `==` / `!=` | 比较同一索引或当前底层值。 | 不可用作严格的位置身份比较。 |

## 一句话总结

`DataReference` 是 `QRangeModelAdapter` 防止“静默改容器”的关键：读取只给 const 视图，赋值一定经模型写回；把它当作短寿命的写值代理，而不是可重绑定、可长期保存的普通引用。
