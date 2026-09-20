# QListView

> Qt 6.11.1 · Qt Widgets · 来自 `QListView`

## 1. 先建立直觉

`QListView` 用一维模型显示项目，但它不只能做“竖列表”。通过 `viewMode`、`flow`、`wrapping`、`gridSize` 和 `movement`，它也能做图标墙、文件缩略图、可拖动的图标视图、联系人列表和侧边导航。

它展示的是模型中的某一列，默认第 0 列。对于多列模型，`setModelColumn()` 决定列表拿哪一列当显示数据；更复杂的显示应交给 delegate，而不是把多个字段提前拼成字符串。

选择 `QListView` 还是 `QListWidget` 的关键在数据来源：数据已经存在于业务模型、需要排序过滤、可能很大或会被多个视图共享时，用 `QListView`；只是十几个固定选项，`QListWidget` 更快上手。

## 2. 类说明

- 头文件：`#include <QListView>`
- 模块：`Qt6::Widgets`
- 继承自：`QAbstractItemView`
- 直接派生类：`QListWidget`、`QUndoView`，以及 Qt Help 中的索引控件

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它继承 item view 的模型、选择、委托、拖放和编辑机制；本类新增的重点是项目布局方式。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QListView(parent)` | 创建列表视图。 |
| `setModelColumn()` / `modelColumn()` | 指定多列模型中显示哪一列。 |
| `setViewMode()` / `viewMode()` | 在 `ListMode` 和 `IconMode` 之间切换。 |
| `setFlow()` / `flow()` | 项目按从上到下或从左到右排列。 |
| `setWrapping()` / `isWrapping()` | 空间不足时是否换到下一列或下一行。 |
| `setGridSize()` / `gridSize()` | 设置每个项目占用的网格尺寸。 |
| `setSpacing()` / `spacing()` | 项目之间的间距。 |
| `setItemAlignment()` / `itemAlignment()` | 项目在自身区域内的对齐方式。 |
| `setWordWrap()` / `wordWrap()` | 文本是否换行。 |
| `setUniformItemSizes()` / `uniformItemSizes()` | 告诉视图所有项目尺寸一致，可显著提升大列表性能。 |
| `setLayoutMode()` / `layoutMode()` | 一次性布局或分批布局。 |
| `setBatchSize()` / `batchSize()` | 分批布局时每批处理多少项目。 |
| `setResizeMode()` / `resizeMode()` | 视口尺寸变化时是否重新布局项目。 |
| `setMovement()` / `movement()` | 项目位置固定、自由移动或吸附到网格。 |
| `setSelectionRectVisible()` | 拖选时是否显示选择矩形。 |
| `setRowHidden()` / `isRowHidden()` | 隐藏或显示指定行。 |
| `clearPropertyFlags()` | 清除由便捷模式设置的属性标记，让后续模式切换重新应用默认组合。 |
| `indexAt()` / `visualRect()` | 坐标与模型索引互转。 |
| `scrollTo()` | 滚动到指定项目。 |
| `rectForIndex()` | 获取项目矩形，常用于子类化布局或命中判断。 |
| `setPositionForIndex()` | 在可移动视图中设置项目位置。 |
| `indexesMoved()` | 用户拖动项目导致索引位置变化时发出。 |

## 4. 关键用法

### 列表模式和图标模式不是皮肤差异

`ListMode` 默认更像传统列表，适合名称、状态、摘要这类纵向扫描。`IconMode` 更像桌面图标或文件缩略图，通常配合 `LeftToRight`、`wrapping`、`gridSize` 和较大的 `iconSize`。

如果只是想让列表项更高、更好看，优先写 delegate 或调 `iconSize`、`spacing`，不要盲目切到 `IconMode`。模式会改变布局假设，也会影响键盘导航和拖拽感受。

### 大列表性能：`uniformItemSizes` 是一个诚实承诺

当每个项目高度相同，开启 `setUniformItemSizes(true)` 可以减少视图反复询问 delegate size hint 的成本。它适合日志列表、联系人列表、固定高度搜索结果。不适合多行摘要高度不一的项目；否则滚动位置和绘制可能看起来不自然。

`Batched` 布局适合一次加载大量项目时减少界面卡顿。它不是分页数据源，只是把布局计算拆成批次；模型数据仍然已经在 model 中。

### 网格、间距和换行要成套配置

图标墙常用组合是：`setViewMode(QListView::IconMode)`、`setFlow(QListView::LeftToRight)`、`setWrapping(true)`、`setResizeMode(QListView::Adjust)`、`setGridSize(...)`。如果只设图标模式而不控制 grid size，长文件名、不同字体和图标尺寸会让排列显得松散。

`gridSize` 一旦非空，项目会按网格摆放，`spacing` 的直觉效果会变弱。要么用网格统一尺寸，要么用 spacing 调自然布局，二者不要混着期待精确像素。

### 拖动项目：视图只管交互，模型仍要支持

`movement` 影响用户是否能移动项目的视觉位置；真正的拖放重排仍要看 `dragDropMode` 和模型的拖放实现。若只是做类似桌面图标的自由摆放，常常还需要把位置作为模型数据保存，否则刷新后位置会丢。

`indexesMoved()` 告诉你视图中的项目被移动了，但不要把它当成数据已经永久重排的证明。是否改变模型顺序，要看你的 model 是否处理了移动。

## 5. 常见坑与经验

- `QListView` 只显示模型的一列；要显示多字段卡片，写 delegate，而不是换成 `QTableView` 硬拼。
- `setRowHidden()` 是视图层隐藏，过滤数据更推荐 `QSortFilterProxyModel`。
- `IconMode` 下长文本通常需要 `wordWrap` 和合适的 `textElideMode` 配合，否则视觉高度不可控。
- `setIndexWidget()` 可以放少量真实控件，但大量列表项应使用 delegate 绘制。
- 需要简单 item API 时用 `QListWidget`；需要业务数据模型时用 `QListView`，不要中途混用两套数据来源。
