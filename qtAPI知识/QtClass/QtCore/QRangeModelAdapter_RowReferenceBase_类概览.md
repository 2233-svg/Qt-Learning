# QRangeModelAdapter::RowReferenceBase：统一只读行视图的公共基类

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.11  
> 状态：Preliminary，接口仍可能调整  
> 所属头文件：`#include <QRangeModelAdapter>`

`QRangeModelAdapter::RowReferenceBase<Reference, Adapter>` 是 `RowReference` 与 `ConstRowReference` 共用的实现基类。业务代码通常不会直接命名它；理解它的价值在于，能正确使用两种行代理共同拥有的只读能力：取整行、按列读取、遍历列，以及在树中查看和进入子节点。

它解决的是“同一行应如何在可写和只读上下文中保持一致读取语义”的问题。`RowReference` 在此基础上额外提供写列和整行赋值；`ConstRowReference` 则只暴露这里的读取能力。

## 适用对象与真实场景

表格与树 adapter 的按行访问不是返回裸 `row_type &`，而是行代理。无论调用者拿到的是可写 `RowReference` 还是只读 `ConstRowReference`，都可以把它当作一个只读列范围：

```cpp
for (const auto &row : std::as_const(tableAdapter)) {
    for (const auto &cell : row) {
        qDebug() << cell;
    }
}
```

这很适合：

- 导出表格或树某一层的数据；
- 对记录做校验、筛选和日志记录；
- 编写同时接受可写行和只读行的只读算法；
- 在树中检查节点是否有直接子行，并取得以该节点为根的子 adapter。

这里“统一”指访问方式统一，不表示解引用类型永远相同。列的 const 值可依数据结构而异：可能是 const 引用包装、指向 const 对象的指针，或异质数据模型中的 `QVariant`。

## 读取一行和按列读取

`RowReferenceBase` 通过 `get()`、隐式转换和 `operator->()` 提供底层行的 const 读取语义。这些接口由内部 `RowGetter` 实现，具体返回形式与行类型是否为指针有关。

```cpp
auto row = std::as_const(tableAdapter).at(0);
const auto rowValue = row.get(); // 读取当前底层行的 const 视图或值
```

不要把该结果视为长期稳定的裸引用。它依赖 model 的实际 range；行被替换、删除、移动或 model reset 后，先前的行代理和从它取得的视图都不应继续使用。

`at(int column)` 与 `operator[](int column)` 读取一个列值：

```cpp
const auto cell = row.at(2);
```

列号必须满足 `0 <= column < size()`。实现使用断言，而不是返回可恢复的错误；在发布构建中越界访问不构成可依赖的失败处理。需要按动态列号读取时，应先以 `size()` 验证范围。

## 作为 const 列范围遍历

`cbegin()` / `cend()` 返回 `ConstColumnIterator`，分别指向本行的第一列和最后一列后一位置。const `begin()` / `end()` 是它们的别名，因此范围 for 在 const 行上自然得到只读列迭代。

```cpp
for (auto it = row.cbegin(); it != row.cend(); ++it) {
    const auto cell = *it;
    // 读取 cell
}
```

`size()` 返回 adapter 的模型列数，即本行可访问的列数。它不是树节点数量，也不是底层 `row_type` 某个任意容器的独立长度；表格模型要求行形状与 model 的列结构一致。

对非 const `RowReference`，派生类覆盖 `begin()` / `end()` 并提供 `ColumnIterator`，从而允许修改每个单元格。要强制只读遍历，可使用 `cbegin()` / `cend()` 或先转为 `ConstRowReference`。

## 树特有能力

`hasChildren()` 与 `children()` 仅在 adapter 的 `Range` 是树时参与重载决议；对列表和表格根本不存在这些成员，不能用运行时 `if` 代替编译期类型约束。

```cpp
auto node = std::as_const(treeAdapter).at(0);

if (node.hasChildren()) {
    const auto descendants = node.children();
    for (const auto &child : descendants) {
        // 处理该节点的直接子行
    }
}
```

`hasChildren()` 查询当前 model 中该节点是否至少有一个直接子行。`children()` 返回新的 `QRangeModelAdapter`，其底层 range/model 与原 adapter 相同，但根索引改为当前行。它是子范围视图，不会复制子树，也不会做递归遍历。

即使 `hasChildren()` 刚返回 true，其他代码仍可能在随后删除子行；若模型可能改变，应把检查与使用保持在适当的模型线程和同步边界内。

## 比较、生命周期与线程边界

同一类行代理支持相等和三路比较，比较依据是 `QModelIndex`；源码断言两者绑定同一个 adapter。不要把来自不同 adapter 的行引用混在同一个排序或位置比较中。

行代理也可与 `row_type` 做值相等比较，代表“当前行数据相等”，不是“同一模型位置”。例如两条内容相同的记录可能相等，但仍是不同的行。

`RowReferenceBase` 存储 `QModelIndex` 与 adapter 指针。插入、删除、移动行列、`assign()`、model reset、树行替换、adapter 销毁和 model 销毁之后，旧行代理及其列 iterator 均应视为失效。它并不使用 `QPersistentModelIndex` 替用户自动跨结构追踪位置。

所有访问仍必须遵循 `QAbstractItemModel` 的线程亲和性。const 行代理只限制写 API，不能让 model 在多个线程中同时无锁读取。

## 常见错误

1. **把基类当成可独立构造的业务类型。** 它是 `RowReference` / `ConstRowReference` 的共同实现，通常从 adapter 获得派生代理。
2. **假设列读取总返回 const 引用。** 它可能是包装器、const 指针或 `QVariant`，取决于 range 和协议。
3. **把 `size()` 当成树的孩子数。** 它始终表示列数；子行数量应从 `children()` 对应 adapter 查询。
4. **在表格或列表上调用树 API。** `children()` / `hasChildren()` 只对树 range 编译可用。
5. **在结构变更后保存 `row.get()` 的结果。** 该读取视图的有效性不独立于 model 与行代理。
6. **把值相等当作位置相同。** `row == rowType` 检查行内容，不提供稳定身份。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `const_iterator` | `ConstColumnIterator` 类型别名。 | 用于按列只读遍历。 |
| `size_type` / `difference_type` | 均为 `int`。 | 与模型行列计数的 `int` 接口一致。 |
| `const_row_type` | 底层行的 const 读取类型。 | 不保证是 `const row_type &`；可能是指针或值式类型。 |
| `get()` | 返回当前行的 const 读取视图。 | 结构变更后不要继续使用结果。 |
| `operator const_row_type()` | `get()` 的隐式读取形式。 | 大对象上避免在热路径反复发生隐式复制。 |
| `operator->()` | 访问行值的 const 成员。 | 不提供可写底层行指针，不应长期保存返回值。 |
| `at(int column)` | 读取指定列的 const 项目包装。 | `column` 必须位于 `[0, size())`。 |
| `operator[](int column)` | `at(column)` 的下标读取形式。 | 不把越界当作可恢复错误。 |
| `cbegin()` / `cend()` | 返回首列和尾后位置的 `ConstColumnIterator`。 | 不可解引用 `cend()`；结构改变后重新获取。 |
| `begin() const` / `end() const` | `cbegin()` / `cend()` 的别名。 | const 行的范围 for 始终只读。 |
| `size()` | 返回模型的列数。 | 不是树孩子数量。 |
| `hasChildren()` | 仅树 range 可用；查询是否存在直接子行。 | 是瞬时 model 状态，不要跨修改缓存。 |
| `children()` | 仅树 range 可用；取得以当前行为根的子 adapter。 | 共享同一 model/range，不复制数据，也不递归遍历。 |
| `==`, `!=`, `<=>` | 以模型索引比较行代理。 | 比较前置条件是两个代理属于同一 adapter。 |
| `row == row_type` | 比较当前行数据和值。 | 内容相等不代表同一模型位置。 |

## 一句话总结

`RowReferenceBase` 为可写和只读行代理定义了相同的只读行接口：按列读取、遍历列、读取整行，以及树中的子范围导航；它的结果始终依赖当前 model 结构和线程边界。
