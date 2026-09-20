# QTableWidget

> Qt 6.11.1 · Qt Widgets · 来自 `QTableWidget`

## 1. 先建立直觉

`QTableWidget` 是 `QTableView` 的便捷版本：它内置 item-based 模型，让你直接按行列放 `QTableWidgetItem`。它适合小型参数表、设置矩阵、临时结果表、手工编辑表格和原型工具。

它不是高性能数据表格的最终形态。数据量大、数据源已经有模型、需要代理排序过滤、需要懒加载或多视图共享时，应使用 `QTableView` + `QAbstractTableModel`。

使用它时要分清三种东西：`QTableWidgetItem` 是单元格数据和显示属性；`cellWidget` 是真的 QWidget，适合少量控件；行列 header item 也是 item，但服务于表头，不是普通单元格。

## 2. 类说明

- 头文件：`#include <QTableWidget>`
- 模块：`Qt6::Widgets`
- 继承自：`QTableView`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它继承 `QTableView` 的表头、选择、排序、网格和 delegate 能力，并提供基于 item 的行列管理接口。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTableWidget(parent)` | 创建空表格。 |
| `QTableWidget(rows, columns, parent)` | 用指定行列数创建表格。 |
| `setRowCount()` / `rowCount()` | 设置或读取行数。 |
| `setColumnCount()` / `columnCount()` | 设置或读取列数。 |
| `insertRow()` / `removeRow()` | 插入或删除行。 |
| `insertColumn()` / `removeColumn()` | 插入或删除列。 |
| `setItem(row, column, item)` / `item()` | 设置或读取单元格 item。 |
| `takeItem(row, column)` | 移除并返回单元格 item，调用者获得所有权。 |
| `clear()` | 清空内容、表头和选择。 |
| `clearContents()` | 只清空单元格内容，保留表头和尺寸。 |
| `setHorizontalHeaderLabels()` / `setVerticalHeaderLabels()` | 批量设置表头文字。 |
| `setHorizontalHeaderItem()` / `horizontalHeaderItem()` | 设置或读取水平表头 item。 |
| `setVerticalHeaderItem()` / `verticalHeaderItem()` | 设置或读取垂直表头 item。 |
| `takeHorizontalHeaderItem()` / `takeVerticalHeaderItem()` | 取走表头 item。 |
| `setCurrentCell()` / `currentRow()` / `currentColumn()` | 设置或读取当前单元格位置。 |
| `currentItem()` / `setCurrentItem()` | 设置或读取当前 item。 |
| `selectedItems()` | 读取选中的 item。 |
| `selectedRanges()` | 读取矩形选择范围。 |
| `setRangeSelected()` | 选中或取消选中一片区域。 |
| `findItems(text, flags)` | 按文本查找单元格。 |
| `editItem()` | 让某个 item 进入编辑状态。 |
| `openPersistentEditor()` / `closePersistentEditor()` | 长期开启或关闭单元格编辑器。 |
| `setCellWidget()` / `cellWidget()` | 在单元格中放真实 QWidget。 |
| `removeCellWidget()` | 移除单元格控件。 |
| `sortItems(column, order)` | 按某列排序。 |
| `setItemPrototype()` / `itemPrototype()` | 设置自动创建 item 时使用的原型。 |
| `row(item)` / `column(item)` | 查询 item 当前行列。 |
| `indexFromItem()` / `itemFromIndex()` | 与模型索引互转。 |
| `visualRow()` / `visualColumn()` | 逻辑行列到当前视觉行列的转换。 |
| `visualItemRect()` | 获取 item 在视口中的矩形。 |
| `scrollToItem()` | 滚动到指定 item。 |
| `setSupportedDragActions()` / `supportedDragActions()` | Qt 6.10 起设置可发起拖拽动作。 |
| `mimeData()` / `dropMimeData()` | 子类化自定义拖放数据。 |
| `cellClicked()` / `cellChanged()` / `cellActivated()` | 按行列报告的信号。 |
| `itemClicked()` / `itemChanged()` / `itemActivated()` | 按 item 指针报告的信号。 |
| `currentCellChanged()` / `currentItemChanged()` | 当前单元格或 item 变化。 |
| `itemSelectionChanged()` | 选择范围变化。 |

## 4. 关键用法

### 先设置行列，再放 item

`setItem()` 需要目标行列存在。常见流程是先 `setRowCount()`、`setColumnCount()`，再填充 item；动态追加时先 `insertRow()`，再设置这一行的各列。构造函数带行列数适合固定尺寸表格。

如果只想更新单元格文字，先检查 `item(row, column)` 是否为空；空的话要创建新 item。Qt 不会因为你读取空单元格就自动生成 item。

### `clear()` 和 `clearContents()` 差别很大

`clear()` 会清掉表头、内容和选择，适合完全重建表格。`clearContents()` 只删除单元格 item，保留行列数和表头，适合刷新数据。很多界面表头突然消失，就是误用了 `clear()`。

### 排序会改变行号

`sortItems()` 或开启排序后，逻辑数据对应的视觉行可能改变。若你保存了某行代表哪个业务对象，排序后必须通过 item 中保存的 id、`Qt::UserRole` 数据或重新查询 row(item) 来定位，不要继续相信旧行号。

`visualRow()` / `visualColumn()` 用于处理表头拖动、排序后的显示位置；模型逻辑位置和用户看到的位置并不总是一致。

### cell widget 适合少量交互控件

`setCellWidget()` 可以放按钮、组合框、进度条，但每个都是 QWidget。几十个可以，几千个会明显变重。大表格中的按钮、进度、开关更适合 delegate 绘制和编辑。

### 信号选择：cell 还是 item

如果你关心的是位置，用 `cellChanged(row, column)`；如果你关心 item 中的自定义数据，用 `itemChanged(item)`。程序批量填表时这些信号也会触发，必要时用 `QSignalBlocker` 避免把初始化误当作用户修改。

## 5. 常见坑与经验

- `takeItem()` 和 `takeHorizontalHeaderItem()` 不会删除对象；调用者接手所有权。
- 排序开启时边插入边设置 item，行位置可能立刻改变；批量填充前先关闭排序。
- 空单元格没有 `QTableWidgetItem`，访问前要判空。
- `selectedItems()` 只返回有 item 的单元格；空单元格被选中时要看 `selectedRanges()`。
- 大型数据表、虚拟滚动和复杂业务模型应使用 `QTableView`。
