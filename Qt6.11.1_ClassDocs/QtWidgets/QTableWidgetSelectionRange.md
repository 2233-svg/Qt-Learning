# QTableWidgetSelectionRange

> Qt 6.11.1 · Qt Widgets · 来自 `QTableWidgetSelectionRange`

## 1. 先建立直觉

`QTableWidgetSelectionRange` 表示 `QTableWidget` 里一个矩形选择区域：从左上角单元格到右下角单元格。它本身不选择任何东西，只是一个轻量值对象，用来描述、保存、比较或传递选择范围。

它常用于复制粘贴、批量填充、批量删除、导出选区、统计选中区域大小。和 `selectedItems()` 不同，它能表达空单元格也被选中的情况。

## 2. 类说明

- 头文件：`#include <QTableWidgetSelectionRange>`
- 模块：`Qt6::Widgets`
- 继承自：无
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

这是值类型，不是 QWidget，也不拥有表格或 item。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTableWidgetSelectionRange()` | 创建空范围，行列数量为 0。 |
| `QTableWidgetSelectionRange(top, left, bottom, right)` | 用边界行列创建矩形范围。 |
| `topRow()` / `bottomRow()` | 返回顶部和底部行号。 |
| `leftColumn()` / `rightColumn()` | 返回左侧和右侧列号。 |
| `rowCount()` / `columnCount()` | 返回范围覆盖的行数和列数。 |
| `operator==` / `operator!=` | Qt 6.3 起可直接比较两个范围是否相同。 |

## 4. 关键用法

`QTableWidget::selectedRanges()` 返回的就是这种对象。遍历区域时通常使用闭区间边界：

```cpp
for (const auto &range : table->selectedRanges()) {
    for (int row = range.topRow(); row <= range.bottomRow(); ++row) {
        for (int column = range.leftColumn(); column <= range.rightColumn(); ++column) {
            // 处理 row, column
        }
    }
}
```

注意 `rowCount()` 等于 `bottomRow() - topRow() + 1`，`columnCount()` 同理。不要把 `bottomRow()` 当作数量，也不要用 `< bottomRow()` 少处理最后一行。

如果需要把一片区域选中，调用 `QTableWidget::setRangeSelected(range, true)`；这个类本身只是描述范围，不会主动影响表格状态。

## 5. 常见坑与经验

- 选中区域可以包含没有 item 的空单元格；这时 `selectedItems()` 看不到它们，`selectedRanges()` 可以。
- 多选模式下可能有多个 range，不能默认只有一个矩形。
- 行列是逻辑坐标，不是表头拖动后的视觉坐标。
- 默认构造的空范围不适合直接遍历，先看 `rowCount()` 和 `columnCount()`。
