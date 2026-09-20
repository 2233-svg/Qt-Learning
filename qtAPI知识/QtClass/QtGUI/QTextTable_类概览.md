# QTextTable 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextTable>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QTextFrame`

## 1. 它解决什么问题

`QTextTable` 是 `QTextDocument` 内嵌表格的结构对象。它管理行列数量、插入和删除、单元格合并与拆分，并通过 `QTextTableFormat` 描述整张表的宽度、间距和边框策略。

它不是数据模型表格或 `QTableView`。每个单元格中保存的是富文本块和框架，编辑仍通过 `QTextCursor`、`QTextTableCell` 与文档坐标完成。

实际场景：

- 富文本编辑器插入和编辑报告表格；
- 生成带表头、合并标题单元格的打印文档；
- 根据 cursor 所在位置查找当前单元格或整行范围；
- 通过行列操作批量扩展或裁剪文档表格。

## 2. 创建和结构编辑

```cpp
QTextTableFormat format;
format.setCellPadding(4);
format.setCellSpacing(1);

QTextTable *table = cursor.insertTable(3, 4, format);
table->mergeCells(0, 0, 1, 4);
```

行列索引从零开始。`appendRows()` / `appendColumns()` 在末尾增加结构；`insertRows()` / `insertColumns()` 在指定索引前插入；`removeRows()` / `removeColumns()` 删除对应结构；`resize()` 同时调整总行列数。所有索引、数量和合并矩形必须在当前表格范围内并形成合法区域，调用前应由业务代码校验。

结构修改会改变单元格的位置、跨度和文档内容的归属。不要在持有旧 `QTextTableCell`、块迭代器或位置缓存时大规模修改表格，再继续假定它们代表原来的单元格。

## 3. 单元格、合并和行范围

`cellAt(row, column)`、`cellAt(position)` 和 `cellAt(cursor)` 返回值类型 `QTextTableCell`。位置重载使用文档文本位置；cursor 重载只有当 cursor 属于当前表格时才有意义。

合并后的区域由左上角主单元格代表；`rowSpan()`、`columnSpan()` 返回其覆盖范围。`mergeCells(cursor)` 依赖 cursor 选区确定矩形，适合 UI 命令；自动化代码更适合显式传入行列与跨度。`splitCell()` 只能用于现有合并单元格，并且传入的范围应与要拆分的合并区域相匹配。

`rowStart(cursor)` / `rowEnd(cursor)` 返回当前表格行首、行尾的光标范围端点，便于选中或对整行执行格式化。它们不是第一个/最后一个字符的普通字符串索引。

## 4. 格式、所有权和线程

`format()` 返回 `QTextTableFormat` 副本，修改后用 `setFormat()` 写回。表格由 `QTextDocument` 管理；从 `insertTable()`、`frameAt()` 或 `QTextCursor::currentTable()` 获得的 `QTextTable *` 不应手动删除。

表格、单元格和相关 cursor 必须在文档所属线程访问。后台任务应准备表格数据或格式副本，并在文档线程创建和填充表格。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextTable(QTextDocument *)` | 为文档构造表格对象。 | 通常由 `QTextCursor::insertTable()` 创建，文档拥有其生命周期。 |
| `~QTextTable()` | 销毁表格对象。 | 文档管理的表格不可手动删除。 |
| `rows()` / `columns()` | 返回当前行数和列数。 | 不等同于视觉行数，合并单元格不改变总格网维度。 |
| `resize(int rows, int columns)` | 调整表格总行列数。 | 会增删结构；先校验非负业务尺寸并考虑内容丢失。 |
| `appendRows(int)` / `appendColumns(int)` | 在表尾添加行或列。 | 数量应为合理正数；旧单元格坐标可能受影响。 |
| `insertRows(int, int)` / `insertColumns(int, int)` | 在指定索引前插入行或列。 | 索引按零起始；结构修改后重新取得单元格视图。 |
| `removeRows(int, int)` / `removeColumns(int, int)` | 删除指定范围行或列。 | 会删除相应单元格内容；先确认范围和合并区域影响。 |
| `cellAt(int row, int column)` | 按格网坐标取得单元格。 | 越界返回无效 cell；合并区域内可能返回同一主单元格。 |
| `cellAt(int position)` | 按文档位置取得单元格。 | position 必须属于当前表格的文档坐标。 |
| `cellAt(const QTextCursor &)` | 按光标取得单元格。 | cursor 应属于当前表格；无关 cursor 得到无效结果。 |
| `mergeCells(int, int, int, int)` | 合并一个矩形区域。 | 范围必须合法且不冲突；左上角成为主单元格。 |
| `mergeCells(const QTextCursor &)` | 按光标选区合并单元格。 | 选区必须对应可合并矩形。 |
| `splitCell(int, int, int, int)` | 拆分已合并区域。 | 要指向现有合并单元格及匹配范围。 |
| `rowStart()` / `rowEnd()` | 取得 cursor 所在表格行的范围端点。 | 结果是文档光标，不是单元格数组索引。 |
| `format()` / `setFormat()` | 读取或更新表格格式。 | `format()` 返回副本；写回会触发重布局。 |

## 5. 记忆重点

`QTextTable` 管的是富文档结构，不是数据表控件。行列操作会改变内容归属，合并按矩形和主单元格理解，`QTextTableCell` 是要随结构变化重新取得的值视图。
