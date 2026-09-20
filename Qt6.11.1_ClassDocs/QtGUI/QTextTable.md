# QTextTable
> Qt 6.11.1 · Qt GUI · 来自 `QTextTable`

## 1. 先建立直觉

`QTextTable` 是富文本文档中的表格对象。它继承自 `QTextFrame`，每个单元格可以包含自己的 block、格式和文本内容。它适合文档表格和打印报表，不是交互式数据表控件。

## 2. 类说明

- 头文件：`#include <QTextTable>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QTextFrame`
- 协作类：`QTextTableCell`、`QTextTableFormat`、`QTextCursor`

创建通常用 `QTextCursor::insertTable(rows, columns, format)`。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `rows()` / `columns()` | 表格行列数 |
| `cellAt(row, col)` / `cellAt(position)` / `cellAt(cursor)` | 获取单元格 |
| `appendRows()` / `appendColumns()` | 追加行列 |
| `insertRows()` / `insertColumns()` | 插入行列 |
| `removeRows()` / `removeColumns()` | 删除行列 |
| `resize()` | 调整表格尺寸 |
| `mergeCells()` | 合并单元格 |
| `splitCell()` | 拆分单元格 |
| `format()` / `setFormat()` | 读取或设置表格格式 |

## 4. 关键用法

```cpp
QTextTableFormat tf;
tf.setCellPadding(4);
QTextTable *table = cursor.insertTable(3, 2, tf);
table->cellAt(0, 0).firstCursorPosition().insertText("Name");
```

## 5. 使用场景

报表、发票、HTML table 内部表示、富文本编辑器插入表格、打印布局。

## 6. 常见坑与经验

- 合并单元格后，多个网格坐标可能指向同一逻辑 cell。
- 删除行列会删除其中的文档内容。
- 表格内编辑仍通过 `QTextCursor`。
- 大规模数据表不要用 QTextTable 替代 `QTableView`。

## 7. 知识点覆盖

文档表格、单元格访问、行列操作、合并拆分、表格格式、cell cursor。
