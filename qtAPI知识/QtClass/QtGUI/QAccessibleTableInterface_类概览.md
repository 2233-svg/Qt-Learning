# Qt QAccessibleTableInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleTableInterface>`  
> 所属模块：`Qt6::Gui`  
> 定位：向辅助技术公开二维表、树或列表结构及其选择操作的纯虚接口

## 1. 它解决什么问题

`QAccessibleTableInterface` 让屏幕阅读器等辅助技术按行、列、单元格和表头理解集合控件。Qt 的树、列表和表视图都可以借助这套二维语义公开数据，而不是只暴露为扁平的 child 列表。

它提供四类能力：

- 表的范围与 cell 定位；
- caption、summary、行列描述等上下文；
- 当前 cell、整行和整列的选择查询；
- 行列选择修改与模型变更处理。

它不是 `QAbstractItemModel` 的替代品。它面向已呈现给辅助技术的可访问结构；实现必须处理虚拟化、隐藏行列、代理排序、合并单元格和当前 selection model 的实际语义。

## 2. 结构一致性

实现 table interface 时，至少保证以下关系成立：

```text
0 <= row < rowCount()
0 <= column < columnCount()
cellAt(row, column) -> 对应 cell 或 nullptr
cell.table() -> 当前 table interface
cell.rowIndex()/columnIndex() -> 与 cellAt 参数同一坐标系
```

合并 cell 可在其覆盖区域的多个坐标返回同一个 cell interface，但该 cell 的 `rowExtent()`、`columnExtent()` 必须准确反映跨度。无效行列不能访问模型越界：查询应返回空、`false` 或空字符串，而不是断言或崩溃。

## 3. 实际使用场景

一个自定义数据网格对行选择做可访问适配：

```cpp
bool GridAccessible::selectRow(int row)
{
    if (row < 0 || row >= grid()->model()->rowCount())
        return false;

    const QModelIndex first = grid()->model()->index(row, 0);
    grid()->selectionModel()->select(
        QItemSelection(first, first),
        QItemSelectionModel::Rows | QItemSelectionModel::Select);
    return isRowSelected(row);
}
```

实际实现应使用真实模型列数建立完整 row selection，并在变化后发送选中或表格模型相关无障碍事件。不要只是修改 visual highlight 而不更新 selection model。

## 4. 查询 API

### `caption()` 与 `summary()`

`caption()` 返回表的标题对象，`summary()` 返回帮助理解表内容的摘要对象；不存在时返回 `nullptr`。它们是独立 accessible interface，不是直接返回字符串。

caption 适合“季度销售额”，summary 适合“按地区汇总，当前按收入降序”。不要把每个 column header 当作 caption，也不要把大段数据复制到 summary。

### `rowCount()`、`columnCount()` 与 `cellAt(row, column)`

返回可访问表的逻辑范围并定位 cell。计数应反映当前可访问数据，而不是尚未加载、永久隐藏或已被过滤掉却不能导航的项。

`cellAt()` 对无效坐标返回 `nullptr`。返回 pointer 由 Qt 管理，调用方不能删除；虚拟化表格可按需通过 cache 创建 cell interface，但必须避免重复注册与过期指针。

### `rowDescription(row)` 与 `columnDescription(column)`

返回行、列的描述文本。无描述或无效 index 可返回空字符串。它们补充 header cell，不应替代正式 header 的 accessible Name。

### 选择查询

| API | 语义 |
| --- | --- |
| `selectedCells()` / `selectedCellCount()` | 返回当前选中的 cell 及其数量。 |
| `selectedRows()` / `selectedRowCount()` | 返回被选中的完整行索引及数量。 |
| `selectedColumns()` / `selectedColumnCount()` | 返回被选中的完整列索引及数量。 |
| `isRowSelected(row)` | 该 row 是否**完全**选中。 |
| `isColumnSelected(column)` | 该 column 是否**完全**选中。 |

单个 cell 被选中不意味着所属整行/整列已选中。`selectedCells()` 中的 pointer 是借用，必须与 cell 的 `isSelected()` 和 selection model 同步。

## 5. 修改选择与模型变化

### `selectRow()` / `selectColumn()`

请求选择一整行或一整列，成功时返回 `true`。具体 selection model 可能在选择新行/列时取消之前的整行/整列选择，因此调用方不能假设是累加行为。

### `unselectRow()` / `unselectColumn()`

取消指定整行或整列选择，保留其他选择。无法取消、无效索引或对象已禁用时返回 `false`。

### `modelChange(QAccessibleTableModelChangeEvent *event)`

通知 table interface 其模型布局、范围或数据发生变化。`event` 只借用，接口不拥有也不应保存它。实现应据 `ModelChangeType` 和范围更新自身 cell/header cache、行列映射和 selection 快照。

普通应用通常向 `QAccessible::updateAccessibility()` 提交 `QAccessibleTableModelChangeEvent`；实现者要确保事件发生时 model 已经处于新状态，避免辅助技术读取到旧行列数。

## 6. 性能与线程边界

辅助技术可能连续按行、列导航，因此 `cellAt()`、description、selection 和 header 查询不应执行阻塞 IO 或全模型扫描。对巨型模型应：

- 复用模型 index 与可见/虚拟化映射；
- 在 `modelChange()` 后精确失效局部 cache；
- 避免在每次 `selectedCells()` 调用中创建全部 cell wrapper；
- 使 `rowCount()` 和 `columnCount()` 在一次查询周期内保持一致。

所有涉及模型、视图和 selection model 的调用应在它们的线程亲和线程运行，通常是 GUI 线程。

## 7. 逐项 API 说明

### `virtual ~QAccessibleTableInterface()`

虚析构函数。接口由 table accessible object 提供，获得的指针是借用。

### `virtual QAccessibleInterface *caption() const = 0`

返回 table caption interface；没有 caption 时返回 `nullptr`。返回对象不转移所有权。

### `virtual QAccessibleInterface *summary() const = 0`

返回 table summary interface；没有 summary 时返回 `nullptr`。它应总结表的用途/状态，不代替所有 cell 数据。

### `virtual int rowCount() const = 0` / `virtual int columnCount() const = 0`

返回逻辑行数、列数。必须是非负数，且与 `cellAt()` 的有效范围一致。

### `virtual QAccessibleInterface *cellAt(int row, int column) const = 0`

返回逻辑坐标上的 cell interface；无效坐标或不可用 cell 返回 `nullptr`。合并 cell 的重复映射应和 cell extent 一致。

### `virtual QString rowDescription(int row) const = 0` / `virtual QString columnDescription(int column) const = 0`

返回行、列描述。无效或没有说明时返回空字符串；不要把 description 当成以分隔符拼出的所有 cell 值。

### `virtual QList<QAccessibleInterface *> selectedCells() const = 0` / `virtual int selectedCellCount() const = 0`

返回选中 cell 列表与数量。两者必须一致；cell pointer 由 Qt 管理。

### `virtual QList<int> selectedRows() const = 0` / `virtual int selectedRowCount() const = 0`

返回完整选中的行索引与数量。部分选中的行不应出现在这里。

### `virtual QList<int> selectedColumns() const = 0` / `virtual int selectedColumnCount() const = 0`

返回完整选中的列索引与数量。部分选中的列不应出现在这里。

### `virtual bool isRowSelected(int row) const = 0` / `virtual bool isColumnSelected(int column) const = 0`

判断指定 row/column 是否完全选中。无效索引返回 `false`。

### `virtual bool selectRow(int row) = 0` / `virtual bool selectColumn(int column) = 0`

选择一整行/列。选择真的成功后返回 `true`；实现可以按真实 selection model 替换此前选择。

### `virtual bool unselectRow(int row) = 0` / `virtual bool unselectColumn(int column) = 0`

取消一整行/列选择，保留其他选择。未选中或不可取消时返回 `false`。

### `virtual void modelChange(QAccessibleTableModelChangeEvent *event) = 0`

处理表模型变更事件。参数只在调用期间有效；实现应更新 cache，不应延后保存 event 裸指针。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 生命周期 | `~QAccessibleTableInterface()` | 虚析构表接口。 | 指针由 table accessible object/Qt 管理。 |
| 上下文 | `caption()` | 返回表标题 interface。 | 无标题返回 `nullptr`。 |
| 上下文 | `summary()` | 返回表摘要 interface。 | 无摘要返回 `nullptr`。 |
| 范围 | `rowCount()` / `columnCount()` | 返回逻辑行列数。 | 非负；需与 `cellAt()` 一致。 |
| 单元格 | `cellAt(int, int)` | 返回逻辑位置的 cell。 | 无效坐标返回 `nullptr`；合并 cell 要报告 extent。 |
| 描述 | `rowDescription()` / `columnDescription()` | 返回行列说明。 | 无说明/无效索引返回空字符串。 |
| cell 选择 | `selectedCells()` / `selectedCellCount()` | 查询选中 cell。 | 指针借用；列表与计数一致。 |
| row 选择 | `selectedRows()` / `selectedRowCount()` | 查询完整选中行。 | 不包含部分选中行。 |
| column 选择 | `selectedColumns()` / `selectedColumnCount()` | 查询完整选中列。 | 不包含部分选中列。 |
| 判断 | `isRowSelected()` / `isColumnSelected()` | 判断行列是否完全选中。 | 无效索引为 false。 |
| 修改 | `selectRow()` / `selectColumn()` | 选择整行/列。 | 可能替换旧选择；成功才返回 true。 |
| 修改 | `unselectRow()` / `unselectColumn()` | 取消整行/列选择。 | 保留其他选择；未选中时可能失败。 |
| 变化 | `modelChange(QAccessibleTableModelChangeEvent *)` | 处理模型变化详情。 | event 不转移所有权，调用后不保存。 |

### 一句话总结

`QAccessibleTableInterface` 用统一的逻辑行列坐标把列表、树和表转为可导航的二维结构：cell、header、跨度、选择和模型变更必须同源于真实模型与 selection model，尤其不能把部分选择误报成整行或整列选择。
