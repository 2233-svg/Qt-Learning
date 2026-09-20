# QTextTableCell
> Qt 6.11.1 · Qt GUI · 来自 `QTextTableCell`

## 1. 先建立直觉

`QTextTableCell` 是 `QTextTable` 中一个单元格的句柄。它能告诉你单元格的位置、跨度、格式，以及该单元格内容的首尾 cursor。它是值类型，不拥有内容。

## 2. 类说明

- 头文件：`#include <QTextTableCell>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型
- 协作类：`QTextTable`、`QTextCursor`、`QTextTableCellFormat`

## 3. API 速查

| API | 作用 |
| --- | --- |
| `isValid()` | cell 是否有效 |
| `row()` / `column()` | 起始行列 |
| `rowSpan()` / `columnSpan()` | 跨行跨列 |
| `format()` / `setFormat()` | 读取或设置 cell 格式 |
| `firstCursorPosition()` / `lastCursorPosition()` | 内容首尾 cursor |
| `firstPosition()` / `lastPosition()` | 文档位置范围 |

## 4. 关键用法

```cpp
QTextTableCell cell = table->cellAt(1, 0);
QTextCursor c = cell.firstCursorPosition();
c.insertText("Value");
```

## 5. 使用场景

读写表格单元格内容、设置表头样式、分析合并单元格跨度、导出表格坐标。

## 6. 常见坑与经验

- 无效 cell 的行列和 cursor 不可靠，先 `isValid()`。
- cell 的文字对齐要改 cell 内 block format。
- 修改 format 后要 `cell.setFormat(format)` 写回。

## 7. 知识点覆盖

单元格位置、跨度、内容 cursor、cell 格式、合并表格读取。
