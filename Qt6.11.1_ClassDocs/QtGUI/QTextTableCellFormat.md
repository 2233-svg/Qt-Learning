# QTextTableCellFormat
> Qt 6.11.1 · Qt GUI · 来自 `QTextTableCellFormat`

## 1. 先建立直觉

`QTextTableCellFormat` 描述单个表格单元格的外观，主要是 padding、边框和背景等属性。它用于精细控制某个 cell，而不是整个表格。

## 2. 类说明

- 头文件：`#include <QTextTableCellFormat>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QTextCharFormat`
- 协作类：`QTextTableCell`、`QTextTable`

表格 cell 里可以包含多个 block。cell format 影响 cell 容器外观，cell 内文字仍可有自己的字符和块格式。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setTopPadding()` / `topPadding()` | 上内边距 |
| `setBottomPadding()` / `bottomPadding()` | 下内边距 |
| `setLeftPadding()` / `leftPadding()` | 左内边距 |
| `setRightPadding()` / `rightPadding()` | 右内边距 |
| `setPadding()` | 一次设置四边内边距 |
| `setTopBorder()` 等 | 单边边框宽度 |
| `setTopBorderStyle()` 等 | 单边边框样式 |
| `setTopBorderBrush()` 等 | 单边边框画刷 |

## 4. 关键用法

```cpp
QTextTableCell cell = table->cellAt(0, 0);
QTextTableCellFormat cf = cell.format().toTableCellFormat();
cf.setBackground(Qt::lightGray);
cf.setPadding(6);
cell.setFormat(cf);
```

单独设置表头行 cell，通常比改整个 table format 更灵活。

## 5. 使用场景

- 表头背景色、加粗边框。
- 某些单元格高亮。
- 报表中不同区域边框样式。
- HTML table cell 样式映射。

## 6. 常见坑与经验

- cell 内容对齐通常要改 cell 内 block 的 `QTextBlockFormat`，不是只改 cell format。
- padding 会影响布局尺寸，打印表格前要检查分页。
- 边框折叠由 table format 决定，cell 边框视觉效果会受它影响。
- 取得 format 后修改，别忘了 `cell.setFormat(cf)` 写回。

## 7. 知识点覆盖

本页覆盖：单元格 padding、边框、背景、表头高亮、cell 与内部文本格式分工。
