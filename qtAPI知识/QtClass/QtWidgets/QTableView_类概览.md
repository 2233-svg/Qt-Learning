# Qt QTableView 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QTableView>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QAbstractItemView -> QTableView`  
> 常见搭档：`QAbstractItemModel`、`QHeaderView`

## 1. QTableView 解决什么问题

`QTableView` 用二维表格方式展示模型数据。它不自己保存数据，而是从 `QAbstractItemModel` 读取内容，再把行、列、表头、网格和选择交给用户看和操作。

适合的场景：

- 数据表浏览；
- 结果列表；
- 可排序、可筛选的记录表；
- 需要列宽、行高、隐藏列和表头排序的结构化数据界面。

它的核心工作是：

1. 从模型读取每个 `QModelIndex` 的显示内容；
2. 通过 `QHeaderView` 管理行头和列头；
3. 负责把模型坐标和视图坐标互相转换；
4. 提供用户选中、滚动、排序、隐藏、合并区域等交互。

## 2. 最小可用代码

```cpp
#include <QStandardItemModel>
#include <QTableView>

auto *model = new QStandardItemModel(3, 3);
model->setHeaderData(0, Qt::Horizontal, tr("Name"));
model->setHeaderData(1, Qt::Horizontal, tr("Age"));
model->setHeaderData(2, Qt::Horizontal, tr("City"));

auto *view = new QTableView;
view->setModel(model);
view->setSortingEnabled(true);
view->horizontalHeader()->setStretchLastSection(true);
view->show();
```

这段代码的关键不是 `QTableView` 自己存了什么，而是 model 提供了什么。  
如果模型没数据，表格也不会凭空出现内容。

## 3. 表头和模型联动

`QTableView` 自带两个表头：

```cpp
QHeaderView *h = view->horizontalHeader();
QHeaderView *v = view->verticalHeader();
```

水平表头通常显示列名，垂直表头通常显示行号或行标题。  
你可以替换它们：

```cpp
view->setHorizontalHeader(customHeader);
view->setVerticalHeader(customRowHeader);
```

常见操作都绕着表头转：

- 列宽：`setColumnWidth()` / `columnWidth()`
- 行高：`setRowHeight()` / `rowHeight()`
- 列隐藏：`setColumnHidden()`
- 行隐藏：`setRowHidden()`
- 排序：`setSortingEnabled()` / `sortByColumn()`

表头的行为已经在 `QHeaderView` 里独立管理，所以表格视图本身更像是“表头 + 数据区”的协调者。

## 4. 坐标、索引和可视区域

`QTableView` 最常用的三类查询是：

```cpp
QModelIndex index = view->indexAt(QPoint(20, 30));
QRect rect = view->visualRect(index);
view->scrollTo(index);
```

它们分别解决：

- `indexAt()`：点到哪一格；
- `visualRect()`：某个索引在屏幕上的矩形；
- `scrollTo()`：把某个索引滚动到可见区域。

辅助坐标 API：

- `rowAt(y)` / `columnAt(x)`：从坐标找行列；
- `rowViewportPosition(row)` / `columnViewportPosition(column)`：从行列找坐标。

这些函数非常适合做自定义提示、命中测试和定位选中项。

## 5. 行列尺寸和隐藏

### 5.1 单独设置尺寸

```cpp
view->setRowHeight(0, 40);
view->setColumnWidth(1, 160);
```

查询对应尺寸：

```cpp
int h = view->rowHeight(0);
int w = view->columnWidth(1);
```

### 5.2 自动按内容调整

```cpp
view->resizeRowToContents(0);
view->resizeRowsToContents();
view->resizeColumnToContents(1);
view->resizeColumnsToContents();
```

这类函数会调用 item delegate 和 `sizeHintForRow/Column()` 来估算尺寸。  
数据很多时，整表自动适配可能很慢，不要毫无节制地在每次数据变化后都调用整列/整行重算。

### 5.3 隐藏行列

```cpp
view->setRowHidden(2, true);
view->setColumnHidden(3, true);
```

查询：

```cpp
bool hidden = view->isRowHidden(2);
bool hiddenCol = view->isColumnHidden(3);
```

隐藏只是视觉上不显示，不会删掉模型数据。

## 6. 排序

```cpp
view->setSortingEnabled(true);
view->sortByColumn(1, Qt::AscendingOrder);
```

`setSortingEnabled(true)` 会立即按当前排序列和顺序触发排序。  
因此在你准备好模型、表头和初始数据之前，不要随手开 sorting，否则首次插入数据时可能就已经被排序了。

排序是否真的生效，取决于模型是否支持排序语义。`QTableView` 只负责发起排序，不负责替模型造排序规则。

## 7. 网格、换行、角落按钮和跨格

### 7.1 网格

```cpp
view->setShowGrid(true);
view->setGridStyle(Qt::DotLine);
```

`showGrid` 控制是否显示格线。`gridStyle` 控制格线样式。

### 7.2 文本换行

```cpp
view->setWordWrap(true);
```

开启后，单元格文字可以换行，表格行高也可能变高。  
这个属性和 `QHeaderView::resizeContentsPrecision` 以及 delegate 的 `sizeHint` 一起影响最终行高。

### 7.3 角落按钮

```cpp
view->setCornerButtonEnabled(true);
```

这个角落按钮通常出现在表头交叉角，风格依平台而异。它更多是外观和选择上的辅助，不是常规业务功能入口。

### 7.4 跨格

```cpp
view->setSpan(0, 0, 1, 2); // 第 0 行第 0 列横跨 2 列
```

`setSpan(row, column, rowSpanCount, columnSpanCount)` 可以让单元格跨多行/多列显示。  
`rowSpan()` 和 `columnSpan()` 用来查询当前跨格设置；`clearSpans()` 清除所有跨格。

跨格适合报表标题、分组表头或特殊汇总行，但不要把它当成一般表格的常态布局手段。

## 8. 选择和局部操作

```cpp
view->selectRow(2);
view->selectColumn(1);
```

这两个函数是常见快捷操作，能快速选择整行或整列。  
表格的具体选择行为仍由选择模型和 selection mode 决定。

`selectedIndexes()`、`selectionChanged()`、`currentChanged()` 等仍然是 `QAbstractItemView` 体系里的标准入口，QTableView 主要是补充表格化行为。

## 9. QTableView 和 QTableWidget 的关系

`QTableView` 是底层视图，依赖外部模型。  
`QTableWidget` 是上层便捷封装，自己带 item 和内置模型。

简单比较：

| 类 | 适合什么 |
| --- | --- |
| `QTableView` | 需要自定义模型、代理、排序、性能优化。 |
| `QTableWidget` | 小型表格、快速原型、直接操作 item。 |

如果你的数据结构复杂、量大、需要和后台模型联动，优先 `QTableView`。

## API 速查表
### 10.1 构造、模型和头部

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QTableView(QWidget *parent = nullptr)` | 创建模型驱动的二维表格视图。 | 视图本身不保存业务数据。 |
| 析构 | `~QTableView()` | 销毁视图。 | 默认不会替你删除外部模型，模型生命周期要单独设计。 |
| 模型 | `setModel(QAbstractItemModel *model)` | 指定表格从哪个模型读取数据。 | 数据、编辑和排序能力主要由模型决定。 |
| 根索引 | `setRootIndex(const QModelIndex &index)` | 把视图限制到模型某个索引的子树或局部范围。 | 表格模型通常用无效索引作为根；传入错误索引会看不到数据。 |
| 选择 | `setSelectionModel(QItemSelectionModel *selectionModel)` | 设置该视图使用的选择模型。 | 可让多个视图共享选择状态，但模型必须匹配。 |
| 表头 | `horizontalHeader() const` / `verticalHeader() const` | 取得水平列头和垂直行头。 | 列宽、行高、排序、移动和隐藏等常见设置都在 `QHeaderView` 上完成。 |
| 表头 | `setHorizontalHeader(QHeaderView *header)` / `setVerticalHeader(QHeaderView *header)` | 替换表格使用的表头控件。 | 自定义表头应在模型和视图初始化阶段明确所有权。 |
| 布局 | `doItemsLayout()` | 要求视图重新计算项目布局。 | 一般由 Qt 内部调用，业务代码只在批量结构变化后才需要考虑。 |

### 10.2 行列、隐藏和尺寸

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 坐标转换 | `rowViewportPosition(int row)` / `columnViewportPosition(int column)` | 返回行或列在 viewport 中的像素位置。 | 适合自定义提示、绘制和命中测试。 |
| 坐标转换 | `rowAt(int y)` / `columnAt(int x)` | 通过 viewport 坐标反查行或列。 | 点在表头或空白区域时可能返回 -1。 |
| 行尺寸 | `setRowHeight(int row, int height)` / `rowHeight(int row) const` | 设置或查询指定行高度。 | 会覆盖该行的自动尺寸结果。 |
| 列尺寸 | `setColumnWidth(int column, int width)` / `columnWidth(int column) const` | 设置或查询指定列宽度。 | 适合少量关键列固定宽度。 |
| 行可见性 | `setRowHidden(int row, bool hide)` / `isRowHidden(int row) const` | 隐藏或显示某一行。 | 只影响视图，不删除模型数据。 |
| 列可见性 | `setColumnHidden(int column, bool hide)` / `isColumnHidden(int column) const` | 隐藏或显示某一列。 | 常用于业务列按权限显示。 |
| 行尺寸 | `resizeRowToContents(int row)` | 按该行内容重新计算高度。 | 会依赖 delegate 的 size hint。 |
| 行尺寸 | `resizeRowsToContents()` | 按内容重算所有行高度。 | 大模型或频繁刷新时可能很慢。 |
| 列尺寸 | `resizeColumnToContents(int column)` | 按该列内容重算宽度。 | 表头或数据变化后可局部调用。 |
| 列尺寸 | `resizeColumnsToContents()` | 按内容重算所有列宽度。 | 数据量大时避免在每次变化后调用。 |

### 10.3 排序、显示和交互

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 排序 | `setSortingEnabled(bool enable)` / `isSortingEnabled() const` | 控制表头点击和视图是否启用排序。 | 开启时可能立即按当前列触发模型排序。 |
| 排序 | `sortByColumn(int column, Qt::SortOrder order)` | 请求模型按指定列排序。 | 视图只发起请求，模型必须实现排序语义。 |
| 外观 | `showGrid() const` / `setShowGrid(bool show)` | 显示或隐藏单元格网格线。 | 只是视觉效果，不改变单元格边界和模型结构。 |
| 外观 | `gridStyle() const` / `setGridStyle(Qt::PenStyle style)` | 读取或设置网格线笔画样式。 | 最终颜色和粗细仍受 style/调色板影响。 |
| 文本 | `wordWrap() const` / `setWordWrap(bool on)` | 控制单元格文本是否允许换行。 | 可能改变行高，通常要配合 delegate 的尺寸提示。 |
| 外观 | `isCornerButtonEnabled() const` / `setCornerButtonEnabled(bool enable)` | 控制行列头交叉处角落按钮。 | 该接口受 `abstractbutton` 配置影响。 |
| 选择 | `selectRow(int row)` / `selectColumn(int column)` | 快速选中整行或整列。 | 实际效果受 selection mode 和 selection behavior 影响。 |
| 跨格 | `setSpan(int row, int column, int rowSpan, int columnSpan)` | 让一个单元格跨多行或多列显示。 | 适合报表标题和汇总行，不适合替代通用布局。 |
| 跨格 | `rowSpan(int row, int column) const` / `columnSpan(int row, int column) const` | 查询某格当前跨行/跨列范围。 | 没有设置跨格时通常返回 1。 |
| 跨格 | `clearSpans()` | 清除视图内所有跨格设置。 | 只清视图的合并显示，不改模型数据。 |

### 10.4 索引、视觉和重载点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 定位 | `visualRect(const QModelIndex &index) const` | 返回索引在 viewport 中的可视矩形。 | 索引无效或不可见时可能得到空矩形。 |
| 定位 | `scrollTo(const QModelIndex &index, ScrollHint hint = EnsureVisible)` | 把索引滚动到可见区域或指定位置。 | 只负责滚动，不会自动选中索引。 |
| 定位 | `indexAt(const QPoint &p) const` | 从 viewport 坐标反查模型索引。 | 空白区域通常返回无效索引。 |
| 尺寸估算 | `sizeHintForRow(int row) const` / `sizeHintForColumn(int column) const` | 估算一行或一列的推荐尺寸。 | 可被重写影响自动适配，但不要在这里做重计算。 |
| 滚动扩展 | `verticalScrollbarAction(int action)` / `horizontalScrollbarAction(int action)` | 处理垂直或水平滚动条动作。 | 只在自定义滚动语义时重写。 |
| 键盘导航 | `moveCursor(CursorAction cursorAction, Qt::KeyboardModifiers modifiers)` | 根据键盘动作计算下一个当前索引。 | 要同时考虑隐藏行列和 selection model。 |
| 选择 | `setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags command)` | 把 viewport 区域转换成选择范围。 | 高级选择行为才需要重写。 |
| 选择 | `visualRegionForSelection(const QItemSelection &selection) const` | 把模型选择转换为视觉区域。 | 自定义高亮或复杂跨格时有用。 |
| 选择 | `selectedIndexes() const` | 返回当前视图选择的索引列表。 | 这是视图级选择结果，不是业务数据副本。 |
| 事件 | `selectionChanged(...)` / `currentChanged(...)` | 响应选择变化和当前索引变化。 | 重写时要维护基类的选择/当前项状态。 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制表格内容。 | 普通需求应使用 delegate/style，不要全量手绘。 |
| 滚动 | `scrollContentsBy(int dx, int dy)` | 响应 viewport 内容滚动。 | 自定义绘制缓存时才需要关注。 |
| 拖放 | `dropEvent(QDropEvent *event)` | 处理拖放落点。 | 要与模型的 dropMimeData 能力配套。 |
| 样式 | `initViewItemOption(QStyleOptionViewItem *option) const` | 填充 delegate 绘制项目所需的样式状态。 | 自定义 delegate 或绘制风格时调用基类更稳妥。 |
| 几何 | `updateGeometries()` | 重新安排表头、滚动条和 viewport 几何。 | 视图结构变化时由 Qt 驱动。 |
| 尺寸 | `viewportSizeHint() const` | 返回 viewport 推荐尺寸。 | 供布局系统参考，不是强制尺寸。 |

## 11. 常见误区

### 11.1 把 QTableView 当数据容器

它只是视图。数据要放模型里，别往视图里直接塞业务状态。

### 11.2 频繁 resizeRowsToContents / resizeColumnsToContents

这类操作可能很重，尤其是大数据表。尽量只对必要列/行做局部调整。

### 11.3 打开 sortingEnabled 之前没准备模型

开启后会马上触发排序。模型和头部没准备好时，结果可能不符合预期。

### 11.4 用 setSpan 当成通用布局手段

跨格适合报表，不适合当普通表格的主要排版方式。

---

### 一句话总结

`QTableView` 是标准的模型驱动表格视图：模型提供数据，`QHeaderView` 管理行列标题和尺寸，视图负责坐标转换、选择、隐藏、排序和表格外观。
