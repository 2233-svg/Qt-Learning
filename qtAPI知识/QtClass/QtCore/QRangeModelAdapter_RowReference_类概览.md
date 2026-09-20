# QRangeModelAdapter::RowReference：可写的一整行模型代理

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.11  
> 状态：Preliminary，接口仍可能调整  
> 所属头文件：`#include <QRangeModelAdapter>`

`QRangeModelAdapter::RowReference` 是表格或树 adapter 中“一行数据”的可写代理。通过可写的 `QRangeModelAdapter::at(row)`、`operator[](row)`，或者解引用 `RowIterator` 获得它。

它不是底层 `row_type &`。它保存模型索引和 adapter 上下文，让单元格写入、整行替换以及树的父子结构维护都在 Qt 模型通知规则中进行。这是它和普通 STL 行引用的根本差异。

## 它解决的问题

表格的一行常是数组、tuple 或自定义记录；树的一行还可能携带子行。若直接把底层行交给调用方修改，model 无从判断该发 `dataChanged()`、`rowsRemoved()` 还是 `rowsInserted()`，视图和 QML 绑定就会得到不一致状态。

`RowReference` 把两个层次的改动封装起来：

- 修改某一列，使用 `row.at(column)` 或 `row[column]`，返回 `DataReference`；
- 替换整行，使用 `row = replacement`，由 adapter 更新行并发出完整通知。

它适用于编辑表单回写一行、批量更新表格记录、替换树节点内容，以及把通用算法限制在 model 可观察的写路径中。

## 如何取得和使用

```cpp
auto row = tableAdapter.at(3);   // 非 const 表格或树 adapter

row[0] = QString("Ada");         // 写入第一列
row.at(1) = 36;                  // 写入第二列

for (auto cell : row) {
    // cell 是 DataReference，可读取，也可按单元格写回
}
```

`RowReference` 不可默认构造，通常不应由业务代码手动构造；应从 adapter 或 `RowIterator` 获取，确保其 `QModelIndex`、adapter 和实际 range 相匹配。

读取整行时可以转为 `ConstRowReference` 或使用其继承的只读行视图。写引用转 const 引用仍指向同一行，不复制行数据：

```cpp
QRangeModelAdapter<Range>::ConstRowReference readOnlyRow = row;
```

## 单元格访问和列遍历

非 const 的 `at(int)` 与 `operator[](int)` 返回当前列的写代理：

```cpp
auto age = row.at(1);
age = 37;
```

`column` 必须满足 `0 <= column < size()`。实现仅以 `Q_ASSERT` 检查此条件，发布构建不应把越界调用当作有定义的失败路径。调用前先检查列数，或在业务层保证表结构。

`begin()` / `end()` 返回 `ColumnIterator`，遍历当前行的列；它的解引用同样是 `DataReference`。基类仍保留 const 的 `cbegin()` / `cend()` 以及 const `begin()` / `end()`，所以对 const `RowReference` 的遍历会退化为只读列迭代。

## 整行赋值的真实语义

下列赋值都表示“把右侧行的值写到左侧引用的位置”，不表示重新绑定引用：

```cpp
row = otherRow;                  // 读取 otherRow 的底层行，再替换当前行
row = constRow;
row = replacementRow;            // const row_type &
row = std::move(replacementRow); // row_type &&
```

每次整行赋值都会对当前行从第一列到最后一列发出 `dataChanged()`。因此即使右侧和左侧只有一列不同，观察者也会看到整行需要刷新；只想改一个字段时，应改用 `row[column] = value`。

表格行的替换还受形状约束：若底层行可以报告大小，Qt 会在调试构建检查新旧行的列数一致。把不同列数的行赋给表格会破坏矩形模型契约，不能依赖发布构建“碰巧能运行”。

## 树行替换会处理子节点

树的 `RowReference::operator=` 不只是赋值：

1. 若旧行有子行，model 先以 `beginRemoveRows()` / `endRemoveRows()` 通知并删除旧子行；
2. 写入新行；
3. 若协议能设置父行，Qt 为新行建立父关系；
4. 若新行带有子行，model 再以插入通知把这些子行放入树；
5. 最后对当前行的所有列发出 `dataChanged()`。

这意味着替换树行会使旧子节点的索引、引用和 iterator 失效。也意味着新行必须是对该 tree protocol 有效的行；源码在调试构建会断言拒绝无效树行。

如果只需要改节点标题、状态或其他单列数据，不要替换整行，直接对 `row[column]` 赋值可避免不必要的子树拆装。

## 生命周期、比较和线程

`RowReference` 依赖其 `QModelIndex`、adapter、model 和当前行结构。任何插入、删除、移动行列、`assign()`、model reset、adapter/model 销毁，以及树行整体替换之后，都应丢弃旧引用并重新取得。

同类 `RowReference` 的比较假定二者属于同一 adapter；源码以断言约束该前置条件。不要用来自不同 adapter 的行引用进行排序、关系比较或作为可互换位置处理。

它可以和 `row_type` 进行相等比较，比较的是当前行值而非稳定的行身份。需要追踪领域对象身份时，用业务主键或在适当时机保存 `QModelIndex`，而不是依赖“行值相等”。

model API 没有因为使用 `RowReference` 就变成线程安全。读写和由其触发的模型通知仍应在 model 所属线程执行。

## 常见错误

1. **把 `RowReference` 当作可重绑定引用。** `row = other` 复制或移动行值，不改变 `row` 指向的位置。
2. **用整行赋值更新一个字段。** 这会刷新整行，树中还会替换子行；单字段改用 `row[column]`。
3. **给表格塞不同列数的行。** 行形状必须与已有表结构兼容。
4. **替换树行后继续访问旧子行。** 子行已被移除或替换，旧代理和 iterator 不再可靠。
5. **把 `children()` 当作复制子树。** 它返回同一 model/range 上、根索引变为该行的 adapter 视图。
6. **跨 adapter 比较行引用。** 该比较不满足可移植的使用前置条件。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `row_type` | 底层 range 中一行的类型别名。 | 用于整行赋值；必须与 adapter 的行形状兼容。 |
| `at(int column)` | 返回该列的 `DataReference`。 | `column` 必须在 `[0, size())` 内；返回的是写代理。 |
| `operator[](int column)` | `at(column)` 的下标形式。 | 不提供越界检查后的可恢复错误。 |
| `begin()` / `end()` | 返回 `ColumnIterator`，遍历当前行的写代理。 | 结构变更后重新取得迭代器。 |
| `cbegin()` / `cend()` | 从基类继承的只读列迭代入口。 | 适合只读算法，解引用不可写。 |
| `children()` | 仅树 adapter 可用；返回以当前行为根的子 adapter。 | 只遍历直接子行，不会拷贝子树。 |
| `hasChildren()` | 从基类继承；仅树 adapter 可用。 | 反映当前 model 状态，结构更新后不要缓存结论。 |
| `size()` | 返回模型列数。 | 是行的列数量，不是树的子行数量。 |
| `operator ConstRowReference()` | 创建指向同一行的只读行代理。 | 不复制行值；原 model 生命周期仍是前置条件。 |
| `operator=(const RowReference &)` | 将另一写行引用的当前行值写入本行。 | 值赋值，不是重新绑定；发出整行 `dataChanged()`。 |
| `operator=(const ConstRowReference &)` | 将只读行引用的当前值写入本行。 | 树中会处理旧子行和新子行。 |
| `operator=(const row_type &)` | 复制一行到当前位置。 | 表格须保持列数兼容。 |
| `operator=(row_type &&)` | 移动一行到当前位置。 | 移动后仍会通过 model 进行通知和树关系维护。 |
| `==`, `!=`, `<=>` | 比较行索引或与 `row_type` 比较当前行值。 | 同类行引用比较要求属于同一 adapter；值相等不是同一位置。 |

## 一句话总结

`RowReference` 是表格和树的一行可写门面：列级修改返回 `DataReference`，整行赋值会通知整行，树中还会替换子行；把它当作短寿命的模型代理，不要当作普通 `row_type &`。
