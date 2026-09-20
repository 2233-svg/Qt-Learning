# Qt QListView 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QListView>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QAbstractScrollArea -> QAbstractItemView -> QListView`  
> 定位：列表视图和图标视图

## 1. 先建立整体认识：它解决什么问题

`QListView` 用来把模型中的一组同级项目显示成：

- 普通纵向列表；
- 横向流式列表；
- 文件管理器式图标网格。

它不是 `QListWidget` 的简单父类替代，而是模型/视图版本的列表控件：

```text
QAbstractItemModel -> QListView -> QAbstractItemDelegate
```

模型负责数据，`QListView` 负责排列和滚动，delegate 负责每一项怎么画、怎么编辑。

## 2. 什么时候用 `QListView`

| 场景 | 建议 |
| --- | --- |
| 数据来自模型或数据库 | 用 `QListView` |
| 只需要一列项目 | 用 `QListView` |
| 要做文件图标、缩略图网格 | `IconMode` |
| 要支持拖拽重新排列 | `movement` + item model 的拖放接口 |
| 项目数量很多 | 使用模型、delegate 和 `uniformItemSizes` |
| 临时少量项目、代码极简 | 可以考虑 `QListWidget` |

如果需要行列结构、表头或多列数据，应考虑 `QTableView`；需要层级关系，应考虑 `QTreeView`。

## 3. 两种视图模式

### 3.1 `ListMode`

```cpp
listView->setViewMode(QListView::ListMode);
```

适合：

- 菜单列表；
- 文件名列表；
- 搜索结果；
- 设置项列表。

### 3.2 `IconMode`

```cpp
listView->setViewMode(QListView::IconMode);
listView->setGridSize(QSize(96, 96));
listView->setWrapping(true);
listView->setMovement(QListView::Static);
```

适合：

- 文件管理器图标；
- 图片缩略图；
- 应用启动器；
- 可视化资源面板。

`IconMode` 下，`gridSize`、`flow`、`wrapping`、`spacing` 的关系会直接影响视觉布局。

## 4. 最小可用代码

```cpp
auto *view = new QListView(this);
auto *model = new QStringListModel(
    { "首页", "设置", "帮助", "关于" }, view);

view->setModel(model);
view->setSelectionMode(QAbstractItemView::SingleSelection);
view->setEditTriggers(QAbstractItemView::DoubleClicked);
view->setUniformItemSizes(true);
```

做图标网格：

```cpp
view->setViewMode(QListView::IconMode);
view->setFlow(QListView::LeftToRight);
view->setWrapping(true);
view->setGridSize(QSize(100, 100));
view->setSpacing(8);
view->setResizeMode(QListView::Adjust);
```

## 5. 布局方向、换行和网格

### 5.1 `flow`

- `TopToBottom`：从上到下排，超出后换列；
- `LeftToRight`：从左到右排，超出后换行。

### 5.2 `isWrapping`

决定项目排满当前方向后是否换到下一行/列。  
它在图标视图里尤其常用。

### 5.3 `gridSize`

它为项目提供一个“逻辑网格尺寸”。  
`Snap` 移动模式会以它作为吸附参考。

网格太小会裁切内容，网格太大又会浪费空间；应该根据图标和文字的实际尺寸设置。

### 5.4 `spacing`

控制项目之间的额外间距。  
它和 `gridSize` 不是一回事：

- `gridSize` 约束项目所在格子；
- `spacing` 控制格子之间的距离。

## 6. 项目移动和拖拽

`movement` 有三个值：

| 取值 | 含义 |
| --- | --- |
| `Static` | 项目不能由用户移动。 |
| `Free` | 项目可以自由移动。 |
| `Snap` | 项目移动时吸附到网格。 |

要让拖拽真正改变模型中的顺序，不能只设置 view，还要保证模型实现对应的拖放能力：

- `flags()` 返回可拖放标志；
- `mimeData()` 提供拖出数据；
- `dropMimeData()` 处理放下；
- `supportedDropActions()` 返回允许的动作。

`indexesMoved()` 只表示视图中的索引移动了，数据最终是否持久化仍由模型决定。

## 7. 布局性能

### 7.1 `uniformItemSizes`

如果所有项目尺寸相同：

```cpp
view->setUniformItemSizes(true);
```

视图不必逐个询问 delegate 的尺寸，布局效率会更好。

只有在项目尺寸确实统一时才设置，否则会造成内容裁切或布局错误。

### 7.2 `layoutMode` 和 `batchSize`

- `SinglePass`：一次性完成布局；
- `Batched`：分批布局；
- `batchSize`：每批布局多少个项目。

大模型首次加载时，`Batched` 可以减少界面长时间卡住的感觉，但布局会分多次完成。

### 7.3 `resizeMode`

- `Fixed`：只在第一次显示时布局；
- `Adjust`：视图尺寸改变时重新布局。

图标网格通常需要 `Adjust`；项目位置固定且模型很大时，可以考虑 `Fixed`。

## 8. `modelColumn`

如果模型有多列，`QListView` 默认通常显示第 0 列。  
通过 `setModelColumn()` 可以指定显示哪一列：

```cpp
view->setModelColumn(1);
```

它只改变列表使用哪一列，不会把多列模型变成表格。

## 9. 隐藏行和选区矩形

```cpp
view->setRowHidden(3, true);
```

这只影响 view 是否显示该行，不会从模型删除数据。

`selectionRectVisible` 控制用户拖拽选择时是否显示选择矩形。  
它解决的是视觉反馈问题，不会改变选择模型本身。

## API 速查表
### 10.1 类型、布局和常用 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `Movement` | 定义项目能否移动以及移动方式。 | `Static`、`Free`、`Snap` 只控制视图交互，模型是否真正改变顺序仍由拖放接口决定。 |
| 枚举值 | `Static` / `Free` / `Snap` | 分别表示不可移动、自由移动、按网格吸附移动。 | 图标模式常用 `Snap`；需要持久化顺序时必须配合模型的 `dropMimeData()`。 |
| 类型 | `Flow` | 定义项目的主排列方向。 | `LeftToRight` 适合图标网格，`TopToBottom` 适合普通列表。 |
| 枚举值 | `LeftToRight` / `TopToBottom` | 分别表示横向排列后换行、纵向排列后换列。 | 和 `wrapping`、`resizeMode` 一起决定最终网格。 |
| 类型 | `ResizeMode` | 定义窗口尺寸变化时是否重新布局项目。 | `Fixed` 减少重排，`Adjust` 适合响应式图标网格。 |
| 枚举值 | `Fixed` / `Adjust` | 分别表示固定布局策略和尺寸变化时重新调整。 | 项目很多且位置稳定时才考虑 `Fixed`。 |
| 类型 | `LayoutMode` | 定义列表布局一次完成还是分批完成。 | 大模型首次显示时，`Batched` 能降低一次性卡顿。 |
| 枚举值 | `SinglePass` / `Batched` | 分别表示一次布局全部项目、分批布局项目。 | 分批布局会让界面逐步稳定，读取布局结果前要考虑尚未完成。 |
| 类型 | `ViewMode` | 定义普通列表还是图标网格。 | 模式切换会改变 flow、网格和项目排列语义。 |
| 枚举值 | `ListMode` / `IconMode` | 分别表示列表模式和图标模式。 | 文件、缩略图、启动器常用 `IconMode`。 |
| 构造 | `QListView(QWidget *parent = nullptr)` | 创建模型驱动的列表/图标视图。 | 视图不保存业务数据，数据来自模型。 |
| 析构 | `~QListView()` | 销毁列表视图。 | 外部模型和 delegate 的生命周期要单独设计。 |
| 排列 | `setMovement(Movement movement)` / `movement() const` | 设置或读取项目移动策略。 | 仅打开 Free/Snap 不足以持久化顺序，模型还要支持拖放。 |
| 排列 | `setFlow(Flow flow)` / `flow() const` | 设置或读取项目排列方向。 | 图标网格通常配合 `LeftToRight`。 |
| 排列 | `setWrapping(bool enable)` / `isWrapping() const` | 设置或读取排满后是否换行/换列。 | 关闭后项目可能沿主方向继续延伸。 |
| 排列 | `setResizeMode(ResizeMode mode)` / `resizeMode() const` | 设置或读取窗口变化时的布局策略。 | `Adjust` 会在 resize 时重新计算项目位置。 |
| 布局 | `setLayoutMode(LayoutMode mode)` / `layoutMode() const` | 设置或读取布局执行方式。 | 大列表可配合 `batchSize()` 调整首次布局体验。 |
| 布局 | `setSpacing(int space)` / `spacing() const` | 设置或读取项目之间的额外间距。 | 与 `gridSize` 不同，它不决定项目格子大小。 |
| 布局 | `setBatchSize(int batchSize)` / `batchSize() const` | 设置或读取分批布局每批处理的项目数。 | 批次太大仍可能卡顿，太小则布局完成时间更长。 |
| 网格 | `setGridSize(const QSize &size)` / `gridSize() const` | 设置或读取图标项目使用的逻辑网格尺寸。 | 网格太小会裁切文字或图标，Snap 也依赖它。 |
| 模式 | `setViewMode(ViewMode mode)` / `viewMode() const` | 切换列表模式和图标模式。 | 切换后检查 flow、wrapping、gridSize 是否仍符合预期。 |
| 属性状态 | `clearPropertyFlags()` | 清除由程序显式设置的内部属性标记，让默认行为重新生效。 | 只在需要恢复 Qt 默认联动时使用，普通业务很少需要。 |
| 可见性 | `isRowHidden(int row) const` / `setRowHidden(int row, bool hide)` | 隐藏或显示模型中的某一行。 | 只影响视图，不删除模型数据。 |
| 模型列 | `setModelColumn(int column)` / `modelColumn() const` | 指定列表从多列模型中显示哪一列。 | 不会把列表变成表格，其他列仍由模型保留。 |
| 性能 | `setUniformItemSizes(bool enable)` / `uniformItemSizes() const` | 声明所有项目尺寸是否一致。 | 只有尺寸确实一致时才打开，否则会裁切或布局错误。 |
| 文本 | `setWordWrap(bool on)` / `wordWrap() const` | 设置或读取项目文本是否换行。 | 会改变项目高度和图标网格排布。 |
| 选择 | `setSelectionRectVisible(bool show)` / `isSelectionRectVisible() const` | 控制拖拽选择时是否绘制选区矩形。 | 只影响视觉反馈，不改变 selection model。 |
| 对齐 | `setItemAlignment(Qt::Alignment alignment)` / `itemAlignment() const` | 设置或读取项目内容在项目矩形中的对齐方式。 | 图标模式常用居中；列表模式要结合文字宽度。 |
| 定位 | `visualRect(const QModelIndex &index) const` | 返回项目在 viewport 中的矩形。 | 索引无效或隐藏时可能返回空矩形。 |
| 定位 | `scrollTo(const QModelIndex &index, ScrollHint hint = EnsureVisible)` | 把指定项目滚动到可见区域。 | 不会自动改变当前项或选择状态。 |
| 命中测试 | `indexAt(const QPoint &p) const` | 从 viewport 坐标查找项目索引。 | 空白区域返回无效索引。 |
| 布局 | `doItemsLayout()` | 要求视图重新计算项目布局。 | 模型批量更新后才可能需要业务侧主动调用。 |
| 重置 | `reset()` | 重置视图内部状态。 | 不等于清空模型数据。 |
| 根索引 | `setRootIndex(const QModelIndex &index)` | 限制列表显示某个模型子树或局部范围。 | 传入的根索引来自当前模型。 |
| 信号 | `indexesMoved(const QModelIndexList &indexes)` | 项目在视图中移动后通知。 | 只说明视图发生了移动，最终顺序是否写回由模型负责。 |
| 事件 | `event(QEvent *e)` | 列表视图统一事件入口。 | 只有处理特殊事件时才重写。 |
| 滚动 | `scrollContentsBy(int dx, int dy)` | 响应内容滚动。 | 自定义绘制缓存或滚动效果时才需要关注。 |
| 布局扩展 | `resizeContents(int width, int height)` / `contentsSize() const` | 计算和查询内容区域尺寸。 | 主要给派生类调整自定义布局使用。 |
| 模型变化 | `dataChanged(...)` / `rowsInserted(...)` / `rowsAboutToBeRemoved(...)` | 响应模型数据和行结构变化。 | 重写时要同步布局、选中状态并调用基类。 |
| 鼠标 | `mouseMoveEvent(...)` / `mouseReleaseEvent(...)` | 处理项目选择、移动和拖放相关鼠标行为。 | 不要轻易破坏默认拖拽和选择逻辑。 |
| 滚轮 | `wheelEvent(QWheelEvent *e)` | 处理滚轮滚动。 | 自定义滚动时保留焦点和滚动条语义。 |
| 定时 | `timerEvent(QTimerEvent *e)` | 处理延迟布局等内部定时操作。 | 通常不重写。 |
| 尺寸 | `resizeEvent(QResizeEvent *e)` | 在视图尺寸变化时重新安排项目。 | 图标模式和 `Adjust` 模式尤其依赖它。 |
| 拖放 | `dragMoveEvent(...)` / `dragLeaveEvent(...)` / `dropEvent(...)` | 处理拖拽经过、离开和放下项目。 | 必须与模型 flags、mimeData、dropMimeData 配套。 |
| 拖放 | `startDrag(Qt::DropActions supportedActions)` | 启动项目拖拽并声明支持的动作。 | 高级拖放定制才重写。 |
| `initViewItemOption(QStyleOptionViewItem *) const` | 初始化列表项目绘制选项。 |
| `paintEvent(QPaintEvent *)` | 绘制列表项目。 |
| `horizontalOffset() const` / `verticalOffset() const` | 返回当前滚动偏移。 |
| `moveCursor(CursorAction, Qt::KeyboardModifiers)` | 处理键盘导航。 |
| `rectForIndex(const QModelIndex &) const` | 返回项目在内容坐标中的矩形。 |
| `setPositionForIndex(const QPoint &, const QModelIndex &)` | 设置可移动项目的位置。 |
| `setSelection(const QRect &, QItemSelectionModel::SelectionFlags)` | 根据矩形更新选择。 |
| `visualRegionForSelection(const QItemSelection &) const` | 返回选区在 viewport 中的区域。 |
| `selectedIndexes() const` | 返回当前选中的索引。 |
| `updateGeometries()` | 更新滚动条和内容几何。 |
| `isIndexHidden(const QModelIndex &) const` | 判断索引是否隐藏。 |
| `selectionChanged(...)` / `currentChanged(...)` | 响应选择和当前项变化。 |
| `viewportSizeHint() const` | 返回 viewport 建议大小。 |

---

### 一句话总结

`QListView` 是一个以模型为数据源的列表/图标视图；`viewMode` 决定长相，`flow` 和 `gridSize` 决定排列，`uniformItemSizes` 和 `layoutMode` 决定性能。
