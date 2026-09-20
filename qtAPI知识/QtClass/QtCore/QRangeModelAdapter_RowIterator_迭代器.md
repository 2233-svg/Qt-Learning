# QRangeModelAdapter::RowIterator：以可写代理按行遍历 QRangeModelAdapter

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.11  
> 状态：Preliminary，接口仍可能调整  
> 所属头文件：`#include <QRangeModelAdapter>`

`QRangeModelAdapter::RowIterator` 是 `QRangeModelAdapter` 的可写行迭代器，建模 `std::random_access_iterator`。它把列表、表格和树统一成“按行走”的 C++ 范围接口，同时把写入保留在 Qt 模型通知体系内。

它最容易被误解的地方是：解引用并不返回底层容器的 `T &`。列表返回 `DataReference`，表格和树返回 `RowReference`。两者都是代理，赋值会通过 model 更新数据并通知观察者，而非让调用者绕过 `QAbstractItemModel` 直接改容器。

## 它解决的问题

假设业务保存一组订单，界面同时有 `QTableView` 或 Qt Quick 视图观察同一模型。直接取得容器迭代器并修改元素，数据本身也许变了，但模型不会自动发出 `dataChanged()`，视图、绑定和代理模型就可能显示旧内容。

`RowIterator` 让自然的范围写法仍然走 adapter：

```cpp
for (auto rowOrItem : adapter) {
    // 列表：rowOrItem 是 DataReference；
    // 表格或树：rowOrItem 是 RowReference。
    // 对代理赋值会回写 model，而不是只改一块无人知晓的内存。
}
```

实际适用场景包括：

- 批量规范化列表值，例如把一批枚举或数字修正后逐项写回；
- 逐行更新二维表的一列；
- 遍历树节点的某一层并替换整行数据；
- 给已有 `QRangeModelAdapter` 写算法，避免为列表、表格、树分别维护访问代码。

它不适合把 model 当作普通 STL 容器做任意结构编辑。插入、删除、移动行应调用 adapter 或 model 的结构操作；迭代器只定位当前根范围内的既有行。

## 基本使用

```cpp
QRangeModelAdapter adapter(std::vector<int>{2, 4, 6});

for (auto item : adapter) {
    item = int(item) * 10;       // DataReference 写回对应列表项
}
```

表格或树中，先得到行代理，再按列访问：

```cpp
for (auto row : tableAdapter) {
    auto firstCell = row.at(0);  // DataReference
    firstCell = normalizedValue;
}
```

树 adapter 只遍历当前根索引的直接子行。若要遍历某行的子节点，先取得该行的 `RowReference`，再使用其 `children()` 返回的子 adapter：

```cpp
auto parent = treeAdapter.at(0);
for (auto child : parent.children()) {
    // 这里只处理 parent 的直接子行
}
```

这不是深度优先遍历。整棵树需要调用方自行递归或使用适合的遍历策略。

## 解引用语义取决于模型形状

### 列表：`DataReference`

列表的 `*it`、`it[n]` 和 `it.operator->()` 使用 `DataReference`。该代理可读取当前项目，也可赋值写回模型；它不是可以永久保存的 `T &`。

```cpp
auto it = listAdapter.begin();
auto value = *it;
value = 42;                      // 写入第 0 个项目
```

复杂对象不能通过 `value->setName()` 原地修改，因为读取接口只给 const 视图。正确做法是取副本、修改副本、再赋给代理。

### 表格和树：`RowReference`

表格和树的 `*it` 是 `RowReference`，代表一整行。它可按列访问、遍历列，或用同类型行替换当前行：

```cpp
auto row = *tableAdapter.begin();
row[1] = 18;                     // 修改第二列
```

整行赋值不是“让引用改指向别处”。`row = replacement` 会把 `replacement` 的行数据写入当前位置，并为该行所有单元格发出 `dataChanged()`。树中还可能删除旧子行、插入新行携带的子行，因此这类赋值有结构性副作用。

## 随机访问与迭代器前置条件

`RowIterator` 支持标准随机访问操作：`*`、`->`、`[]`、递增递减、加减偏移、迭代器相减、比较和 `swap()`。

```cpp
auto first = adapter.begin();
auto third = first + 2;
auto itemOrRow = third[0];
const int distance = adapter.end() - first;
```

这些语义仍受标准迭代器前置条件约束：

- 不可解引用 `end()`，不可移动到 `begin()` 之前或 `end()` 之后；
- 两个参与距离计算的 iterator 必须表示同一行序列；
- 树的不同 `children()` adapter 属于不同父节点范围，即便行号相同也不应相减或混用；
- `operator-(lhs, rhs)` 的实现按行号相减，不会替调用方验证 adapter 是否相同；
- `swap()` 交换两个迭代器的游标状态，不会交换模型中的两行数据。

可以把 `RowIterator` 隐式转换为 `ConstRowIterator`，以便把写迭代器交给只读算法；反向转换不成立。

## 生命周期、修改和线程边界

迭代器保存行号、树根索引和 adapter 指针。它依赖 adapter、其 model 及其当前结构持续有效。以下操作后，旧的 iterator、`RowReference` 或 `DataReference` 都不应继续使用：

- 插入、删除或移动行、列；
- `assign()` 替换 adapter 的整个范围；
- model reset 或重建；
- adapter 或 model 销毁；
- 树中把某行赋值为另一行，从而替换子行。

`const` 版本只表示该 API 不提供写入口，不表示模型可以跨线程无锁读取。`QAbstractItemModel`、视图和与之关联的 adapter 应在 model 所属线程使用；工作线程应生成纯数据，随后通过信号或队列把更新交回模型线程。

## 常见错误

1. **把 `*it` 当作底层项目引用。** 列表得到的是 `DataReference`，表格和树得到的是 `RowReference`。
2. **在遍历中直接改结构。** `insertRow()`、`removeRows()`、reset 等会使已有迭代器失效；先记录计划，再重新获取 iterator。
3. **误认为树迭代器会遍历全部后代。** 它只走当前根下的一层直接子行。
4. **跨树父节点做距离计算。** 不同子 adapter 不是同一个序列。
5. **缓存 `end()` 后修改模型。** 修改后必须重新取得边界 iterator。
6. **在工作线程中遍历或写 model。** iterator 没有为跨线程访问增加同步或线程迁移能力。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `iterator_category` | 标记为 `std::random_access_iterator_tag`。 | 随机访问不取消标准 iterator 的同一序列和有效性要求。 |
| `difference_type` | 行偏移和 iterator 距离类型，为 `int`。 | 仅对同一 adapter 根范围内的 iterator 求差。 |
| `value_type` / `reference` | 列表为 `DataReference`；表格和树为 `RowReference`。 | 先按模型形状决定解引用后的操作方式。 |
| `pointer` | 列表和表格/树均为对应代理类型。 | `operator->()` 不会交出底层容器的裸可写指针。 |
| `operator ConstRowIterator()` | 将可写 iterator 转为只读 iterator。 | 转换后无法通过该 iterator 写入。 |
| `operator*()` | 返回当前列表项或行的可写代理。 | 不可解引用 `end()` 或失效 iterator。 |
| `operator->()` | 为当前代理提供箭头访问。 | 只作短时访问；不要保存跨结构变更。 |
| `operator[](n)` | 返回当前偏移 `n` 的列表项或行代理。 | 目标必须位于当前根范围内。 |
| `++` / `--` | 前后移动一个行位置。 | 不可越过范围边界。 |
| `+`, `-`, `+=`, `-=` | 按行数偏移 iterator。 | 不要生成范围外 iterator。 |
| `lhs - rhs` | 计算两个游标的行号差。 | 调用方负责保证它们来自同一行序列。 |
| `==`, `!=`, `<=>` | 比较根索引与行位置。 | 跨不同根范围的比较没有用于算法位置关系的意义。 |
| `swap()` | 交换两个 iterator 的游标状态。 | 不交换底层行数据。 |

## 一句话总结

`RowIterator` 让 `QRangeModelAdapter` 能以 STL 风格按行写入，但解引用始终是模型代理：列表得到 `DataReference`，表格和树得到 `RowReference`；结构变更、跨根比较和跨线程使用都必须格外谨慎。
