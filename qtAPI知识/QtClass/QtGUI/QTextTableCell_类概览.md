# QTextTableCell 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextTableCell>`  
> 所属模块：`Qt6::Gui`  
> 类型：关联文档表格的轻量值视图

## 1. 它解决什么问题

`QTextTableCell` 是对 `QTextTable` 中一个单元格的轻量访问句柄。它提供单元格坐标、行列跨度、内部文本范围、单元格格式和块遍历入口，使应用能够在不直接操作表格内部表示的情况下读写指定格。

它不是拥有内容的对象，也不是指针。通过 `table->cellAt()` 得到后可复制，但它依赖来源表格和文档；表格删行、合并/拆分或文档销毁后，旧 cell 不应当作长期缓存。

## 2. 格式与内容访问

`format()` 返回 `QTextCharFormat` 副本，单元格专有属性可转为 `QTextTableCellFormat`：

```cpp
QTextTableCell cell = table->cellAt(1, 2);
QTextTableCellFormat format = cell.format().toTableCellFormat();
format.setBackground(QColor("#fff6cf"));
format.setPadding(4);
cell.setFormat(format);
```

单元格中的正文是文档结构。`firstCursorPosition()` / `lastCursorPosition()` 返回可编辑范围端点，`begin()` / `end()` 迭代单元格内部的块/框架。要替换正文，使用从这些位置构造或取得的 `QTextCursor`；不要把 `setFormat()` 误当作写文本。

## 3. 坐标和合并

`row()`、`column()` 是零起始的格网坐标。对于合并单元格，`rowSpan()`、`columnSpan()` 返回它覆盖的行列数；区域内多个格网坐标可能映射到同一个 cell 视图。

`firstPosition()` / `lastPosition()` 是文档文本位置，不是行列索引或像素坐标。`tableCellFormatIndex()` 是内部格式表索引，仅适合调试或当前文档内部查询，不能作为持久化 ID。

## 4. 有效性、生命周期和线程

默认构造 cell 无效，应先检查 `isValid()`。它不拥有 `QTextTable`，也不延长文档生命周期；结构变化后重新通过 `cellAt()` 获取需要的单元格。

读取或修改 cell 必须在表格所属文档线程进行，通常是 GUI 线程。不要将 cell 跨线程传给后台任务。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextTableCell()` | 创建无效单元格视图。 | `isValid()` 为 `false`。 |
| 复制构造 / `operator=` | 复制单元格观察句柄。 | 不复制单元格内容，也不延长表格生命周期。 |
| `isValid()` | 判断是否关联表格单元格。 | 文档结构大改后应重新获取 cell。 |
| `row()` / `column()` | 返回零起始行列坐标。 | 合并区域内会指向同一主单元格语义。 |
| `rowSpan()` / `columnSpan()` | 返回单元格跨越的行列数。 | 普通单元格通常各为 1。 |
| `format()` | 返回单元格格式副本。 | 修改副本不会自动写回。 |
| `setFormat(const QTextCharFormat &)` | 更新单元格格式。 | 可传 `QTextTableCellFormat`；不修改单元格正文。 |
| `firstCursorPosition()` / `lastCursorPosition()` | 返回单元格内容范围的光标端点。 | 可继续编辑；位置随文档修改而变化。 |
| `firstPosition()` / `lastPosition()` | 返回单元格内容范围的文档位置。 | 不是行列索引或像素。 |
| `begin()` / `end()` | 遍历单元格内块和子框架。 | `end()` 是哨兵；结构变更后不要使用旧迭代器。 |
| `tableCellFormatIndex()` | 返回内部单元格格式索引。 | 非稳定业务 ID，仅当前文档语境有效。 |
| `operator==` / `operator!=` | 比较是否指向同一表格内部单元格。 | 不比较正文或格式是否相同。 |

## 5. 记忆重点

`QTextTableCell` 是文档表格中的短期值视图。用它拿格式、坐标和编辑范围；正文仍通过 cursor 修改，格式副本要写回，表格结构变化后要重新取得 cell。
