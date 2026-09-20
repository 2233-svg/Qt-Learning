# QTableView

> Qt 6.11.1 · Qt Widgets · 来自 `QTableView`

## 1. 先建立直觉

`QTableView` 是按行列展示 `QAbstractItemModel` 的表格视图。它适合数据库结果、参数矩阵、报表、属性表、可编辑业务清单等场景。它不保存单元格数据，只负责把模型的二维索引显示出来。

表格的难点通常不在“显示一个格子”，而在列宽、表头、排序、选择粒度、合并单元格和编辑器策略。`QTableView` 把这些能力拆给 `QHeaderView`、model、delegate 和 selection model，因此要避免把业务数据塞进 view 子类。

小型静态表格可以用 `QTableWidget`；数据来自模型、需要代理排序过滤、几万行以上、或者多个视图共享同一份数据时，优先 `QTableView`。

## 2. 类说明

- 头文件：`#include <QTableView>`
- 模块：`Qt6::Widgets`
- 继承自：`QAbstractItemView`
- 直接派生类：`QTableWidget`

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它继承了 item view 的模型、选择、委托和拖放机制；本类重点补充二维表格几何、表头、网格线、行列隐藏、排序入口和单元格 span。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTableView(parent)` | 创建表格视图。 |
| `setModel()` | 绑定二维模型。 |
| `horizontalHeader()` / `verticalHeader()` | 获取水平和垂直表头。 |
| `setHorizontalHeader()` / `setVerticalHeader()` | 替换表头控件。 |
| `setColumnWidth()` / `columnWidth()` | 设置或读取列宽。 |
| `setRowHeight()` / `rowHeight()` | 设置或读取行高。 |
| `resizeColumnToContents()` / `resizeColumnsToContents()` | 根据内容调整列宽。 |
| `resizeRowToContents()` / `resizeRowsToContents()` | 根据内容调整行高。 |
| `hideColumn()` / `showColumn()` | 隐藏或显示列。 |
| `hideRow()` / `showRow()` | 隐藏或显示行。 |
| `setColumnHidden()` / `isColumnHidden()` | 程序化控制列隐藏。 |
| `setRowHidden()` / `isRowHidden()` | 程序化控制行隐藏。 |
| `selectColumn()` / `selectRow()` | 选中整列或整行。 |
| `setSortingEnabled()` / `isSortingEnabled()` | 开启表头排序交互。 |
| `sortByColumn()` | 按某列和方向排序。 |
| `setShowGrid()` / `showGrid()` | 控制是否显示网格线。 |
| `setGridStyle()` / `gridStyle()` | 控制网格线样式。 |
| `setWordWrap()` / `wordWrap()` | 单元格文本是否换行。 |
| `setCornerButtonEnabled()` | 左上角全选按钮是否可用。 |
| `setSpan()` / `rowSpan()` / `columnSpan()` | 设置或读取合并单元格范围。 |
| `clearSpans()` | 清除所有合并单元格。 |
| `rowAt()` / `columnAt()` | 视口坐标转换为行列号。 |
| `rowViewportPosition()` / `columnViewportPosition()` | 行列号转换为视口位置。 |
| `indexAt()` / `visualRect()` | 坐标与模型索引互转。 |
| `scrollTo()` | 滚动到指定单元格。 |
| `sizeHintForRow()` / `sizeHintForColumn()` | 查询行列推荐尺寸。 |

## 4. 关键用法

### 排序：视图触发，模型执行

`setSortingEnabled(true)` 会让用户点击表头排序，也会立即按当前排序列触发一次排序。真正怎么排序取决于模型的 `sort()` 实现；如果源模型不适合直接排序，常用 `QSortFilterProxyModel` 放在中间。

表格里混有数字、日期、字符串时，不要把所有值都转成显示字符串再排序。模型应在合适的 role 中提供真实类型，代理模型才能做符合直觉的比较。

### 表头是 `QHeaderView`，不是装饰条

列宽拖拽、隐藏列、stretch、按内容调整、排序指示器都在 `QHeaderView` 上。`horizontalHeader()` 和 `verticalHeader()` 是调表格体验的核心入口。比如报表常让最后一列 stretch，属性表常隐藏垂直表头。

频繁调用 `resizeColumnsToContents()` 在大模型上可能很慢，因为它需要检查内容尺寸。大表格通常只对关键列调用，或设置合理默认宽度，再允许用户调整。

### 合并单元格只影响视图

`setSpan()` 改的是表格视图如何显示某片区域，不会改变模型数据结构。导出、复制、排序、代理过滤时，模型仍然是原来的行列。复杂报表如果大量依赖 span，要单独设计导出和选择行为。

### 选择粒度要符合任务

记录列表通常用 `SelectRows + SingleSelection` 或 `ExtendedSelection`；矩阵编辑才适合 `SelectItems`。选择行为不只是视觉差异，它会影响复制、删除、批量操作和用户对“当前对象”的理解。

### 换行和省略号

`wordWrap(true)` 允许单元格文字换行，但不会自动把行高撑到完整显示所有文字。行高仍由 header resize mode、delegate size hint、`resizeRowsToContents()` 等共同决定。很多“为什么换行后还是省略”的问题，原因就在这里。

## 5. 常见坑与经验

- `QTableView` 不拥有数据；释放或重置模型时，视图只是响应模型信号。
- 隐藏列是视图行为；权限过滤或业务过滤应放到 model/proxy model。
- 大数据表不要给每个单元格放 QWidget，写 delegate 更轻。
- 打开排序前确认模型能正确响应 `sort()`，否则用户点击表头可能没有效果。
- 行列坐标 API 使用视口坐标，不是全局屏幕坐标；鼠标事件里通常直接用 `event->position()` 转点即可。
