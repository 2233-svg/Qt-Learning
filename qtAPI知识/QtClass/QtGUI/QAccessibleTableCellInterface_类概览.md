# Qt QAccessibleTableCellInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleTableCellInterface>`  
> 所属模块：`Qt6::Gui`  
> 定位：为单个表格单元格公开行列位置、跨行列范围、表头和选择状态的纯虚接口

## 1. 它解决什么问题

`QAccessibleTableCellInterface` 让辅助技术把一个 accessible object 理解为表格中的单元格，而不仅是普通 child。它描述单元格位于哪一行哪一列、是否跨行/跨列、关联哪些行列标题、是否被选中以及属于哪张表。

它通常由“单元格的 `QAccessibleInterface`”同时实现，并从 cell 的 `interface_cast(QAccessible::TableCellInterface)` 暴露。表对象自身则实现 `QAccessibleTableInterface`。

它不是通用二维模型 API：

- 不负责直接选择或取消选择，选择操作由 table interface 提供；
- 不返回单元格显示文本，文本仍由 cell 的 `QAccessibleInterface::text()` 提供；
- 不拥有 table、header 或其他 cell 的 interface；
- 不能把视图局部索引、代理 index 或业务 ID 混为 row/column 索引。

## 2. 实际使用场景

一个自定义排班表的单元格可通过该接口报告合并区域：

```cpp
int ScheduleCellAccessible::rowIndex() const { return m_row; }
int ScheduleCellAccessible::columnIndex() const { return m_column; }
int ScheduleCellAccessible::rowExtent() const { return m_rowSpan; }
int ScheduleCellAccessible::columnExtent() const { return m_columnSpan; }

bool ScheduleCellAccessible::isSelected() const
{
    return schedule()->selectionModel()->isSelected(m_index);
}
```

对于未合并单元格，`rowExtent()` 和 `columnExtent()` 都应为 `1`。合并单元格要保证 `table()->cellAt(row, column)` 与 extent、标题和选中状态使用同一张逻辑表坐标系。

## 3. 行列、跨度与表头边界

### 行列索引

`rowIndex()`、`columnIndex()` 应返回单元格所在的逻辑行列。实践中按 Qt 模型常用的 0 起始索引实现，并与 `QAccessibleTableInterface::cellAt()` 的参数一致。

对于已合并 cell，索引应代表该 cell 的锚点位置，通常是合并区域左上角；只要 table 的 `cellAt()` 和所有关联实现一致，辅助技术即可正确推断占用范围。

### Extent

`rowExtent()` 和 `columnExtent()` 是单元格占据的行数、列数，不是最后一行/列索引：

- 普通 cell：返回 `1`；
- 跨 2 行、3 列：分别返回 `2`、`3`；
- 返回 `0` 或负数没有有效单元格语义，派生实现应避免。

### 表头

`rowHeaderCells()` 与 `columnHeaderCells()` 返回与此 cell 相关的 header cell interface 列表。多级表头可以返回多个对象；没有对应表头时可以返回空列表。

返回的指针由 Qt accessible cache 管理，调用方不能删除。虚拟化表格不要为一次查询创建未注册的临时 header interface。

## 4. 所有权、有效性与性能

cell、table 和 header 的 interface 指针都是借用。模型重置、行列删除、视图销毁或 virtualized item 回收后，旧 cell interface 可能失效；实现 `isValid()` 和 table/cell 查询时要防止访问失效的 `QModelIndex` 或 QObject。

这些查询可能在读屏导航时高频调用。不要在 `rowHeaderCells()` 中扫描整个模型或在 `isSelected()` 中重建完整 selection 列表。应复用稳定模型索引、选择模型和 header 映射。

## 5. 逐项 API 说明

### `virtual ~QAccessibleTableCellInterface()`

虚析构函数。接口通常由 cell 的 accessible object 同时实现；通过 `tableCellInterface()` 得到的指针是借用，不可 delete。

### `virtual int rowIndex() const = 0` / `virtual int columnIndex() const = 0`

返回单元格的逻辑行、列位置。索引要与 table 的 `rowCount()`、`columnCount()`、`cellAt()` 一致；无效/已移除 cell 应由其主 interface 的有效性机制处理，不要伪造看似合法的位置。

### `virtual int rowExtent() const = 0` / `virtual int columnExtent() const = 0`

返回 cell 占用的行数、列数。普通单元格均为 `1`；合并单元格返回真实 span。它们是数量，不是结束索引。

### `virtual QList<QAccessibleInterface *> rowHeaderCells() const = 0`

返回关联行标题 cell 列表。多级标题可返回多个 interface；没有行标题时返回空列表。

### `virtual QList<QAccessibleInterface *> columnHeaderCells() const = 0`

返回关联列标题 cell 列表。使用规则与 `rowHeaderCells()` 相同。

### `virtual bool isSelected() const = 0`

返回此 cell 当前是否被选中。它应与 table 的 `selectedCells()`、`selectedCellCount()`、整行/整列选择语义一致。

不要把 current cell、keyboard focus 或 hover 当成 selected。不同视图可以存在 current index 但没有 selection。

### `virtual QAccessibleInterface *table() const = 0`

返回包含此 cell 的 table accessible interface。返回指针不转移所有权；无有效 table 时应返回 `nullptr`。

它应能通过 `table->tableInterface()` 得到对应 table interface，并使 `cellAt(rowIndex(), columnIndex())` 能定位回此 cell 或同一合并 cell。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 生命周期 | `~QAccessibleTableCellInterface()` | 虚析构 cell 接口。 | 由 cell/table accessible object 管理。 |
| 坐标 | `rowIndex()` / `columnIndex()` | 返回逻辑行列位置。 | 与 `cellAt()` 坐标系一致；通常 0 起始。 |
| 跨度 | `rowExtent()` / `columnExtent()` | 返回占用行数、列数。 | 是数量；普通 cell 为 1。 |
| 表头 | `rowHeaderCells()` | 返回关联行标题 cell。 | 可为空；返回非拥有 interface 指针。 |
| 表头 | `columnHeaderCells()` | 返回关联列标题 cell。 | 多级表头可返回多个。 |
| 选择 | `isSelected()` | 判断该 cell 是否选中。 | 不等于 current、focus 或 hover。 |
| 归属 | `table()` | 返回所属 table interface。 | 可能为 `nullptr`；结果不转移所有权。 |

### 一句话总结

`QAccessibleTableCellInterface` 把 cell 放回表格语义中：位置与跨度描述二维结构，表头提供上下文，选择说明当前状态，所有结果都必须和 `QAccessibleTableInterface` 使用同一套逻辑坐标和缓存生命周期。
