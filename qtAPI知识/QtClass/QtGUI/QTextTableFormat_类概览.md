# QTextTableFormat 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextTableFormat>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QTextFrameFormat`

## 1. 它解决什么问题

`QTextTableFormat` 描述整张 `QTextTable` 的布局和外观：列数与列宽约束、单元格间距和内边距、表格对齐、表头行数、边框折叠，以及从 `QTextFrameFormat` 继承的宽高、边框和外边距。

它不保存单元格内容，也不执行插入、删除或合并。结构编辑使用 `QTextTable`；单元格自身的填充和四边框使用 `QTextTableCellFormat`。

## 2. 列宽、间距与边框折叠

`setColumnWidthConstraints()` 接受 `QList<QTextLength>`，可混合固定、百分比与可变列宽：

```cpp
format.setColumnWidthConstraints({
    QTextLength(QTextLength::FixedLength, 80),
    QTextLength(QTextLength::PercentageLength, 50),
    QTextLength(QTextLength::VariableLength, 0)
});
```

约束列表应与表格列数保持一致；不一致时不要假定 Qt 会按业务意图自动补齐。`clearColumnWidthConstraints()` 删除该属性，让布局重新按默认规则计算。

`cellSpacing` 是相邻单元格之间的距离，`cellPadding` 是单元格边框到内部内容的通用距离。不要把两者混为一谈。`borderCollapse` 表示相邻边框采用折叠模型；它会影响边框可见宽度和颜色的合成，单元格四边分别设置边框时尤其需要做实际渲染验证。

`headerRowCount` 是语义性表头行数，主要服务于表格布局与分页场景；它不自动加粗、填色或阻止编辑。

## 3. 格式写回和线程

本类是值类型。通过 `table->format()` 取得副本，修改后用 `table->setFormat()` 写回，或在 `cursor.insertTable()` 前传入。写回已有文档的操作必须在文档所属线程。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextTableFormat()` | 创建表格格式值。 | 未设置属性由文档布局默认策略解释。 |
| `isValid()` | 判断是否为表格格式类别。 | 不表示列宽或边框已配置。 |
| `setColumns(int)` / `columns()` | 设置或读取格式中的列数。 | `columns()` 缺省语义为至少 1；实际结构仍以 `QTextTable` 为准。 |
| `setColumnWidthConstraints()` / `columnWidthConstraints()` | 设置或读取列宽 `QTextLength` 列表。 | 列表应与列数匹配；百分比基于可用表宽。 |
| `clearColumnWidthConstraints()` | 删除列宽约束。 | 之后由布局按默认规则分配列宽。 |
| `setCellSpacing()` / `cellSpacing()` | 设置或读取单元格间距。 | 是格与格之间的距离，不是单元格内部边距。 |
| `setCellPadding()` / `cellPadding()` | 设置或读取统一单元格内边距。 | 不等于 `QTextTableCellFormat` 的四边细粒度 padding。 |
| `setAlignment()` / `alignment()` | 设置或读取表格在可用区域中的对齐。 | 不设置单元格内部段落对齐。 |
| `setHeaderRowCount()` / `headerRowCount()` | 设置或读取表头行数。 | 是语义/布局信息，不会自动设置样式。 |
| `setBorderCollapse()` / `borderCollapse()` | 开关相邻单元格边框折叠。 | 会影响相邻边框如何合成；复杂样式要验证渲染。 |
| 继承的 `setWidth()` / `setHeight()` | 设置表格框架尺寸约束。 | 使用 `QTextLength` 时可表达固定、百分比或可变长度。 |
| 继承的 `setBorder()` / `setMargin()` / `setPadding()` | 设置表格外框边框、外边距、内部框架边距。 | 与 cell spacing/padding 是不同层级。 |

## 4. 记忆重点

`QTextTableFormat` 描述整表，不描述单元格内容。列宽约束、cell spacing、cell padding 和 border collapse 各有不同层次；取得格式是副本，修改后必须写回表格。
