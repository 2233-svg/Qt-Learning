# QTableWidgetSelectionRange：QTableWidget 的矩形选择范围

> Qt 6.11.1 · `#include <QTableWidgetSelectionRange>` · 模块：`Qt6::Widgets`

`QTableWidgetSelectionRange` 是一个轻量值类型，用 top/bottom row 和 left/right column 描述 `QTableWidget` 中的一块矩形选择区域。它让你在 convenience table 中不用直接操作 `QModelIndex` 和 selection model。

## 使用场景

`QTableWidget::selectedRanges()` 会返回一个或多个范围；`setRangeSelected(range, true/false)` 可选择或取消选择矩形区域。表格中不可选择的 item 不会真正出现在选择结果里，即使它落在矩形范围内。

默认构造得到空范围，行数和列数为 0。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QTableWidgetSelectionRange()` | 构造空范围。 |
| `QTableWidgetSelectionRange(top, left, bottom, right)` | 构造闭区间矩形范围。 |
| `topRow() const` | 返回顶部行。 |
| `bottomRow() const` | 返回底部行。 |
| `leftColumn() const` | 返回左列。 |
| `rightColumn() const` | 返回右列。 |
| `rowCount() const` | 返回 `bottom - top + 1`；空范围为 0。 |
| `columnCount() const` | 返回 `right - left + 1`；空范围为 0。 |
| `operator==` / `operator!=` | 比较四个边界是否相同。 |
| 选择边界 | 不可选择 item 会被选择系统排除。 |
