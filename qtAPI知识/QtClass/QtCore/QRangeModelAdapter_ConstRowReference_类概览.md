# QRangeModelAdapter::ConstRowReference：把一条表格或树行包装成只读列范围

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.11  
> 状态：Preliminary  
> 所属头文件：`#include <QRangeModelAdapter>`

`QRangeModelAdapter::ConstRowReference` 是围绕 `QRangeModel` 中一条 const 行的引用包装器。它解决的是底层行类型不统一时的只读访问问题：一行可能是 `std::vector`、`std::tuple`、gadget，甚至是由指针组成的视图，但调用方仍能把它当成“可按列遍历、可按列取值”的只读范围。

它主要出现在表格和树模型的 const 遍历路径中：解引用 `ConstRowIterator` 时得到它；内部 const 行访问也依赖同一套语义。普通列表只有单个项目，通常不需要该行包装器。

## 使用方式

```cpp
const auto &readOnly = tableAdapter;

for (const auto &row : readOnly) {
    qDebug() << "columns:" << row.size();

    for (const auto &cell : row) {
        qDebug() << cell;
    }
}
```

也可按列访问：

```cpp
const auto row = *tableAdapter.cbegin();
auto first = row.at(0);
auto second = row[1];
```

`at(column)` 与 `operator[]` 得到的是 const 单元格数据，而不是可写 `DataReference`。因此它适合渲染、导出、校验和比较，不能用来回写模型。

## 为什么是包装器，而不是直接 `const Row &`

对标准范围行，直接返回 `const Row &` 看起来更简单；但 `QRangeModelAdapter` 还支持 tuple、gadget、指针行和其他不一定天然具有统一迭代器接口的类型。`ConstRowReference` 将它们收敛为：

- `size()` 返回模型列数；
- `begin()` / `end()`、`cbegin()` / `cend()` 返回 `ConstColumnIterator`；
- `at(column)` / `operator[](column)` 返回一列的 const 数据；
- 可通过继承的行获取接口读取或访问底层行的 const 视图。

这意味着“行的原始 C++ 类型”和“模型可见的列范围”不是一回事。尤其是 gadget 与 tuple，列数来自模型对行的解释，不能仅凭 `sizeof` 或成员数量猜测。

## 树的额外能力

当 adapter 表示树时，const 行引用额外提供：

```cpp
if (row.hasChildren()) {
    for (const auto &child : row.children()) {
        // child 是当前行的直接子行
    }
}
```

`children()` 返回一个 const `QRangeModelAdapter` 子视图，它与父 adapter 共享同一个 `QRangeModel`，但把当前行作为根索引。它不是深度优先遍历器，也不复制子树；它只改变后续行操作所使用的 parent。

## 边界与生命周期

- `at(column)` 断言 `0 <= column < size()`；它不是可恢复的越界查询。
- `begin()` / `end()` 中的列数来自 `adapter.columnCount()`，行类型必须保持模型承诺的列形状。
- 插入、删除、移动行列、`assign()` 或 model reset 后，不保存旧行引用或旧列迭代器继续读取。
- 指针行的 const 视图不会替你管理指向对象的寿命。对象被释放后，行包装器也无法变得安全。
- const 引用只限制当前访问路径，不能让另一个线程同时无锁修改 model 或底层范围。

## 与 RowReference、DataReference 的区别

| 类型 | 表示什么 | 能否写入 |
| --- | --- | --- |
| `ConstRowReference` | 一整条只读表格/树行 | 否 |
| `RowReference` | 一整条可写表格/树行的通知型代理 | 可通过整体行或单元格代理写入 |
| `DataReference` | 一个可写模型单元格的代理 | 可以赋值，模型会发通知 |

若只是要改一个单元格，使用可写 adapter 的 `at(row, column)` 或 `setData()`。若要替换整行，使用 `RowReference` 的赋值，不要从 `ConstRowReference` 上试图移除 const。

## 常见错误

1. 将 `ConstRowReference` 当作可修改的 `std::vector &`。
2. 在不检查列数的情况下访问 `row[column]`。
3. 用 `children()` 期待一次拿到所有后代，它只返回直接子行子视图。
4. 在表格结构变化后继续保存行引用或列 iterator。
5. 认为 const 指针行会自动延长底层 QObject 或领域对象寿命。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `get()` / 到 const 行类型的转换 | 取得底层行的 const 视图或引用。 | 具体返回形态随行类型变化，不要假定总是 `const T &`。 |
| `operator->()` | 访问底层行的 const 成员。 | 不可调用非 const 成员修改行。 |
| `size()` | 返回模型解释出的列数。 | 等于 adapter 的当前 `columnCount()`。 |
| `begin()` / `end()` | 返回 `ConstColumnIterator` 范围。 | 用于只读列遍历；结构修改后失效。 |
| `cbegin()` / `cend()` | `begin()` / `end()` 的显式 const 形式。 | 不可解引用 cend。 |
| `at(column)` | 读取指定列的 const 数据。 | 列号必须在 `[0, size())`。 |
| `operator[](column)` | `at(column)` 的下标形式。 | 同样没有容错越界语义。 |
| `hasChildren()` | 查询当前树行是否有直接子行。 | 仅树 adapter 提供。 |
| `children()` | 返回以当前行为根的 const 子 adapter。 | 与父对象共享 model，只遍历直接子行。 |
| `const_iterator` | 行内只读列迭代器类型。 | 即 `ConstColumnIterator`。 |
| `size_type` / `difference_type` | 列数与列偏移类型。 | 两者均为整型模型坐标，不能替代生命周期检查。 |

## 一句话总结

`ConstRowReference` 将任意表格或树行统一为只读列范围：可以取列、遍历列、查看直接子行，却不能修改模型；把它当作短寿命的模型视图，而不是可长期保存的底层容器引用。
