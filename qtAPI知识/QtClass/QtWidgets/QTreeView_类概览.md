# Qt QTreeView 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QTreeView>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QAbstractItemView -> QTreeView`  
> 常见搭档：`QAbstractItemModel`、`QHeaderView`

## 1. QTreeView 解决什么问题

`QTreeView` 用树形结构展示模型数据。它和 `QTableView` 的区别在于：前者强调层级关系，后者强调二维表格。

适合的场景：

- 文件系统树；
- 项目资源树；
- 组织架构；
- 可展开分组的层级数据；
- 依赖树、节点树、配置树。

树视图的核心问题不是“有几列”，而是“每个节点有没有子节点、展开后怎么显示、缩进多少、哪个列是树列”。

## 2. 最小可用代码

```cpp
#include <QStandardItemModel>
#include <QTreeView>

auto *model = new QStandardItemModel;
auto *root = model->invisibleRootItem();

auto *parentItem = new QStandardItem(tr("Parent"));
parentItem->appendRow(new QStandardItem(tr("Child")));
root->appendRow(parentItem);

auto *view = new QTreeView;
view->setModel(model);
view->expandAll();
view->show();
```

`QTreeView` 只负责展示层级；具体层级关系仍然来自模型。

## 3. 树结构和展开折叠

```cpp
view->setExpanded(index, true);
view->expand(index);
view->collapse(index);
view->expandAll();
view->collapseAll();
view->expandToDepth(2);
view->expandRecursively(index);
```

这些函数主要解决“哪些节点展开、展开到多深、用户点击后怎么变化”的问题。

常用属性：

- `itemsExpandable`：节点是否允许展开；
- `expandsOnDoubleClick`：双击是否展开/折叠；
- `autoExpandDelay`：拖拽悬停时自动展开的延迟；
- `sortingEnabled`：是否允许按列排序；
- `animated`：展开折叠是否有动画。

如果某个节点不应被展开，除了模型本身不提供子项，还可以通过 `setItemsExpandable(false)` 统一限制。

## 4. 缩进、根节点和树列

### 4.1 缩进

```cpp
view->setIndentation(20);
int indent = view->indentation();
view->resetIndentation();
```

缩进决定每一级树节点向右偏移多少像素。  
它是树形感最直接的视觉参数之一。

### 4.2 rootIsDecorated

```cpp
view->setRootIsDecorated(true);
```

`rootIsDecorated` 决定根节点是否显示展开/折叠箭头。  
如果设为 `false`，根节点看起来更像扁平列表。

### 4.3 treePosition

```cpp
view->setTreePosition(0);
int pos = view->treePosition();
```

`treePosition` 决定哪一列承载树结构和展开箭头。  
默认通常是第一列。对于有多列的树表，这个属性很有用。

## 5. 选择、导航和索引

```cpp
QModelIndex above = view->indexAbove(index);
QModelIndex below = view->indexBelow(index);
QModelIndex hit = view->indexAt(QPoint(20, 40));
```

树视图特有的导航函数：

- `indexAbove()`：上一个可见节点；
- `indexBelow()`：下一个可见节点；
- `indexAt()`：坐标命中的节点；
- `visualRect()`：节点对应的可视矩形；
- `scrollTo()`：滚动到指定节点。

这些函数非常适合做键盘导航、快捷搜索定位和自定义右键菜单定位。

## 6. 行列可见性和第一列跨度

```cpp
view->setRowHidden(2, parentIndex, true);
view->setColumnHidden(3, true);

view->setFirstColumnSpanned(0, parentIndex, true);
```

树视图里“隐藏行”通常指隐藏某个父节点下的孩子项，因此 `setRowHidden(row, parent, hide)` 需要同时提供父索引。

`setFirstColumnSpanned()` 适合树节点的标题行、分组行或需要第一列跨整行显示的情况。  
`isFirstColumnSpanned()` 可以查询当前是否已经跨列。

## 7. 性能相关属性

### 7.1 uniformRowHeights

```cpp
view->setUniformRowHeights(true);
```

如果你知道所有行高差不多，可以打开它。Qt 会更快地计算布局和滚动。  
这是大树数据里非常有价值的性能提示。

### 7.2 sortingEnabled

```cpp
view->setSortingEnabled(true);
view->sortByColumn(0, Qt::AscendingOrder);
```

树视图也能排序，但排序逻辑取决于模型如何组织层级和比较规则。  
排序对树结构的影响通常比表格更复杂，因为要考虑父子层级和兄弟节点顺序。

## 8. headerHidden 和列操作

```cpp
view->setHeaderHidden(true);
view->setColumnWidth(0, 240);
view->setColumnHidden(2, true);
```

树视图默认带水平表头。  
如果只是想做一个纯树列表，可以把表头隐藏；如果需要多列树，表头就很重要。

常见列操作：

- `columnAt()` / `columnWidth()` / `setColumnWidth()`
- `isColumnHidden()` / `setColumnHidden()`
- `resizeColumnToContents()`

## 9. 动画和双击展开

```cpp
view->setAnimated(true);
view->setExpandsOnDoubleClick(true);
```

动画让展开折叠更顺滑，但在大量节点时也可能增加视觉负担。  
`expandsOnDoubleClick` 则决定双击行为是展开/折叠还是由你自己处理。

## API 速查表
### 10.1 构造、模型和基础属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QTreeView(QWidget *parent = nullptr)` | 创建模型驱动的树形视图。 | 视图只展示层级，不保存节点数据。 |
| 析构 | `~QTreeView()` | 销毁树视图。 | 外部模型的生命周期不由视图自动决定。 |
| 模型 | `setModel(QAbstractItemModel *model)` | 指定树视图使用的层级模型。 | 父子关系来自模型的 `parent/index` 实现。 |
| 根索引 | `setRootIndex(const QModelIndex &index)` | 把视图根限制到某个节点或子树。 | 常用于文件系统某个目录；根索引本身通常不直接显示。 |
| 选择 | `setSelectionModel(QItemSelectionModel *selectionModel)` | 设置树使用的选择模型。 | 多个视图共享选择时，模型必须对应同一数据模型。 |
| 表头 | `header() const` / `setHeader(QHeaderView *header)` | 读取或替换多列树的水平表头。 | 纯树列表可直接隐藏表头。 |
| 表头 | `setHeaderHidden(bool hide)` / `isHeaderHidden() const` | 控制表头是否显示。 | 隐藏表头不影响多列数据本身。 |
| 拖放展开 | `autoExpandDelay() const` / `setAutoExpandDelay(int delay)` | 设置拖拽悬停到节点后自动展开的延迟。 | 设为负值通常表示关闭自动展开。 |
| 层级视觉 | `indentation() const` / `setIndentation(int i)` / `resetIndentation()` | 读取、设置或恢复每一级树的缩进。 | 缩进太小会看不出层级，太大则浪费横向空间。 |
| 根节点装饰 | `rootIsDecorated() const` / `setRootIsDecorated(bool show)` | 控制根节点是否显示展开/折叠装饰。 | 纯列表风格常关闭。 |
| 性能 | `uniformRowHeights() const` / `setUniformRowHeights(bool uniform)` | 声明所有可见行是否使用统一行高。 | 只有行高确实一致时才打开，否则会导致布局错误。 |
| 展开能力 | `itemsExpandable() const` / `setItemsExpandable(bool enable)` | 全局控制节点是否允许展开。 | 这是视图开关，不会改变模型是否存在子节点。 |
| 双击行为 | `expandsOnDoubleClick() const` / `setExpandsOnDoubleClick(bool enable)` | 控制双击节点是否展开/折叠。 | 关闭后可把双击留给业务打开详情。 |
| 排序 | `isSortingEnabled() const` / `setSortingEnabled(bool enable)` | 控制是否允许按列排序。 | 树排序要和模型父子层级、兄弟节点比较规则配套。 |
| 动画 | `isAnimated() const` / `setAnimated(bool enable)` | 控制展开折叠动画。 | 大量节点时可关闭以降低视觉和重绘成本。 |
| 焦点 | `allColumnsShowFocus() const` / `setAllColumnsShowFocus(bool enable)` | 控制当前行的焦点是否绘制到所有列。 | 多列树中能让当前行更容易识别。 |
| 文本 | `wordWrap() const` / `setWordWrap(bool on)` | 控制节点文本是否换行。 | 会影响行高和展开后的滚动体验。 |
| 树列 | `treePosition() const` / `setTreePosition(int logicalIndex)` | 指定展开箭头和缩进所在的逻辑列。 | 只有多列树才通常需要调整。 |

### 10.2 展开、折叠和定位

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 单节点 | `isExpanded(const QModelIndex &index) const` / `setExpanded(const QModelIndex &index, bool expand)` | 查询或设置一个节点的展开状态。 | 索引必须属于当前模型，展开状态只属于视图。 |
| 单节点 | `expand(const QModelIndex &index)` / `collapse(const QModelIndex &index)` | 直接展开或折叠一个节点。 | 节点没有子项时不会产生可见变化。 |
| 全树 | `expandAll()` / `collapseAll()` | 展开或折叠当前根下的全部节点。 | 大树可能触发大量布局和模型访问。 |
| 递归展开 | `expandRecursively(const QModelIndex &index, int depth = -1)` | 从指定节点向下递归展开到指定深度。 | 深度越大，模型访问和布局成本越高。 |
| 深度展开 | `expandToDepth(int depth)` | 把整棵可见树展开到某个层级深度。 | 适合初始化展示一个可读的层级范围。 |
| 键盘导航 | `indexAbove(const QModelIndex &index) const` / `indexBelow(const QModelIndex &index) const` | 返回当前可见节点上方或下方的索引。 | 只考虑当前展开状态下可见的节点。 |
| 定位 | `scrollTo(const QModelIndex &index, ScrollHint hint = EnsureVisible)` | 滚动到指定节点。 | 节点处于折叠父节点下时，先展开路径再滚动。 |
| 命中测试 | `indexAt(const QPoint &p) const` | 从 viewport 坐标找到对应节点索引。 | 点在空白处或分支空隙时可能返回无效索引。 |
| 视觉矩形 | `visualRect(const QModelIndex &index) const` | 返回节点在 viewport 中的矩形。 | 节点不可见时可能返回空矩形。 |
| 选择 | `selectAll()` | 选择所有符合当前视图选择规则的可见项。 | 最终结果受 selection mode 和 model flags 影响。 |

### 10.3 行列和树结构控制

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 坐标转换 | `columnViewportPosition(int column) const` / `columnAt(int x) const` | 在列号和 viewport 横坐标之间转换。 | 找不到列时通常返回 -1。 |
| 列尺寸 | `columnWidth(int column) const` / `setColumnWidth(int column, int width)` | 查询或设置列宽。 | 多列树中通常配合 `QHeaderView` 一起设计。 |
| 列可见性 | `isColumnHidden(int column) const` / `setColumnHidden(int column, bool hide)` | 查询或设置某列是否隐藏。 | 只影响视觉列，不删除模型数据。 |
| 列可见性 | `showColumn(int column)` / `hideColumn(int column)` | 显示或隐藏列的便捷 slot。 | 与 `setColumnHidden` 的结果相同，但调用意图更直观。 |
| 行可见性 | `isRowHidden(int row, const QModelIndex &parent) const` / `setRowHidden(int row, const QModelIndex &parent, bool hide)` | 隐藏或显示某个父节点下的子行。 | `parent` 不能省略，它决定 row 属于哪一级树。 |
| 跨列显示 | `isFirstColumnSpanned(int row, const QModelIndex &parent) const` / `setFirstColumnSpanned(int row, const QModelIndex &parent, bool span)` | 让某个节点的第一列跨过整行显示。 | 适合分组标题、目录节点，不适合普通数据行普遍使用。 |
| 树列 | `setTreePosition(int logicalIndex)` | 设置展开箭头和缩进所在的逻辑列。 | 与 `treePosition()` 配套使用。 |

### 10.4 信号和 protected 扩展点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 信号 | `expanded(const QModelIndex &index)` | 节点展开时通知。 | 可用于懒加载子节点或记录展开状态。 |
| 信号 | `collapsed(const QModelIndex &index)` | 节点折叠时通知。 | 保存用户视图状态时常用。 |
| 滚动 | `scrollContentsBy(int dx, int dy)` | 响应 viewport 内容滚动。 | 自定义缓存绘制时才需要重写。 |
| 模型变化 | `rowsInserted(...)` / `rowsAboutToBeRemoved(...)` / `rowsRemoved(...)` | 响应树节点插入和移除。 | 重写时要维护展开状态、当前索引和基类逻辑。 |
| 表头变化 | `columnResized(...)` / `columnCountChanged(...)` / `columnMoved()` | 响应列尺寸、数量和顺序变化。 | 多列树需要同步业务列配置时使用。 |
| 展开刷新 | `reexpand()` | 重新应用需要保持的展开状态。 | 通常是内部 slot，业务代码很少直接调用。 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制树视图。 | 普通外观优先使用 style/delegate。 |
| 绘制 | `drawTree(QPainter *painter, const QRegion &region) const` | 绘制树的整体内容区域。 | 高级派生类绘制扩展点。 |
| 绘制 | `drawRow(QPainter *painter, const QStyleOptionViewItem &options, const QModelIndex &index) const` | 绘制一行节点。 | 可派生实现特殊行背景或层级标记。 |
| 绘制 | `drawBranches(QPainter *painter, const QRect &rect, const QModelIndex &index) const` | 绘制展开箭头和分支线。 | 自定义树线样式时重写。 |
| 鼠标 | `mousePressEvent(...)` / `mouseReleaseEvent(...)` / `mouseDoubleClickEvent(...)` / `mouseMoveEvent(...)` | 处理树节点点击、展开和拖动。 | 重写时要保留选择、编辑和拖放行为。 |
| 键盘 | `keyPressEvent(QKeyEvent *event)` | 处理上下移动、展开、折叠和编辑快捷键。 | 自定义快捷键不要破坏默认树导航。 |
| 拖放 | `dragMoveEvent(QDragMoveEvent *event)` | 处理拖拽经过节点时的反馈。 | 和模型的 drop 能力、自动展开配套。 |
| viewport 事件 | `viewportEvent(QEvent *event)` | 接收树内容区域的事件。 | 复杂交互时比重写整个 widget 事件更合适。 |
| 几何 | `updateGeometries()` | 更新表头、滚动条和树内容几何。 | 由视图结构变化驱动。 |
| 尺寸 | `viewportSizeHint() const` / `sizeHintForColumn(int column) const` | 返回 viewport 或列宽的推荐尺寸。 | 只是布局建议，不是最终固定尺寸。 |
| 行尺寸 | `indexRowSizeHint(const QModelIndex &index) const` / `rowHeight(const QModelIndex &index) const` | 估算或查询某节点行高。 | 自定义 delegate、换行和统一行高会影响结果。 |
| 偏移 | `horizontalOffset() const` / `verticalOffset() const` | 返回树内容当前滚动偏移。 | 主要用于绘制和派生类布局计算。 |
| 导航 | `moveCursor(...)` | 根据键盘动作计算下一个树索引。 | 要尊重展开状态和隐藏节点。 |
| 选择 | `setSelection(...)` / `visualRegionForSelection(...)` / `selectedIndexes()` | 实现树的区域选择和选中区域换算。 | 高级选择/绘制定制时才需要重写。 |
| 事件 | `changeEvent(QEvent *event)` / `timerEvent(QTimerEvent *event)` | 响应样式变化和自动展开等定时行为。 | 重写时调用基类，避免内部计时逻辑失效。 |
| 当前项 | `currentChanged(const QModelIndex &current, const QModelIndex &previous)` | 当前索引变化时更新树视图状态。 | 与外部联动时优先连接视图/选择模型信号。 |

## 11. 常见误区

### 11.1 以为 QTreeView 自己存树数据

它不存。层级关系和节点内容都来自模型。

### 11.2 uniformRowHeights 开错场景

如果你的树每一行高度差别很大，强开统一行高会让布局和视觉都不准。

### 11.3 把隐藏列和隐藏节点混为一谈

`setColumnHidden()` 影响列，`setRowHidden(row, parent, hide)` 影响父节点下的子行，它们不是同一个概念。

### 11.4 treePosition 不理解就乱改

树列不是“显示第几列”的简单开关，而是决定树结构承载在哪一列。多列树才需要特别配置。

---

### 一句话总结

`QTreeView` 是树形模型视图：用 model 表达层级，用 indentation/rootIsDecorated/treePosition 表达树感，用 expand/collapse 和 row/column hidden 控制可见结构，用 uniformRowHeights 和 sortingEnabled 处理性能与交互。
