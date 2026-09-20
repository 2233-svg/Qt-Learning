# QTextTableFormat
> Qt 6.11.1 · Qt GUI · 来自 `QTextTableFormat`

## 1. 先建立直觉

`QTextTableFormat` 描述富文本文档中表格整体的格式：列宽、单元格间距、padding、边框折叠、表头行数、对齐方式等。

它继承自 `QTextFrameFormat`，因为表格本质上是特殊 frame。

## 2. 类说明

- 头文件：`#include <QTextTableFormat>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QTextFrameFormat`
- 协作类：`QTextTable`、`QTextTableCellFormat`、`QTextLength`

表格整体格式和单元格格式分工明确：列宽和间距在 table format，某个 cell 的背景、row span、col span 等在 cell 或 table 操作中处理。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setColumns()` / `columns()` | 设置或读取列数提示 |
| `setColumnWidthConstraints()` / `columnWidthConstraints()` | 设置列宽约束 |
| `clearColumnWidthConstraints()` | 清除列宽约束 |
| `setCellSpacing()` / `cellSpacing()` | 单元格之间距离 |
| `setCellPadding()` / `cellPadding()` | 单元格内边距 |
| `setBorderCollapse()` / `borderCollapse()` | 边框是否折叠 |
| `setHeaderRowCount()` / `headerRowCount()` | 表头行数量 |
| `setAlignment()` / `alignment()` | 表格整体对齐 |

## 4. 关键用法

```cpp
QTextTableFormat tf;
tf.setCellPadding(4);
tf.setCellSpacing(0);
tf.setBorder(1);
tf.setHeaderRowCount(1);
tf.setColumnWidthConstraints({
    QTextLength(QTextLength::PercentageLength, 30),
    QTextLength(QTextLength::PercentageLength, 70)
});
cursor.insertTable(3, 2, tf);
```

百分比列宽依赖可用文档宽度；固定列宽适合打印精确布局。

## 5. 使用场景

- 报表和发票表格。
- HTML table 导入导出。
- 富文本编辑器插入表格。
- 打印时重复表头。
- 简单网格布局。

## 6. 常见坑与经验

- `columns()` 是格式提示，实际表格结构以 `QTextTable::columns()` 为准。
- cell spacing 和 border collapse 组合会显著改变视觉边框。
- 宽度约束数量应和列数匹配，否则布局结果可能退回默认。
- QTextTable 适合文档表格，不适合替代真正的交互表格控件。

## 7. 知识点覆盖

本页覆盖：表格整体格式、列宽约束、cell padding/spacing、边框折叠、表头行、文档表格布局。
