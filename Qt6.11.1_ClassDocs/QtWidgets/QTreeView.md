# QTreeView

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** 树模型/视图控件，负责按父子层级展示模型数据、展开折叠和选择。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QTreeView`：树模型/视图控件，负责按父子层级展示模型数据、展开折叠和选择。

**内部模型：** Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

**适用场景：** 创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

## 2. 依赖与对象关系

- 头文件：`#include <QTreeView>`
- 继承自：QAbstractItemView
- 直接派生类：QHelpContentWidget、QTreeWidget

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `allColumnsShowFocus : bool`
- `animated : bool`
- `autoExpandDelay : int`
- `expandsOnDoubleClick : bool`
- `headerHidden : bool`
- `indentation : int`
- `itemsExpandable : bool`
- `rootIsDecorated : bool`
- `sortingEnabled : bool`
- `uniformRowHeights : bool`
- `wordWrap : bool`

### 公有函数

- `QTreeView(QWidget *parent = nullptr)`
- `virtual ~QTreeView()`
- `bool allColumnsShowFocus() const`
- `int autoExpandDelay() const`
- `int columnAt(int x) const`
- `int columnViewportPosition(int column) const`
- `int columnWidth(int column) const`
- `bool expandsOnDoubleClick() const`
- `QHeaderView * header() const`
- `int indentation() const`
- `QModelIndex indexAbove(const QModelIndex &index) const`
- `QModelIndex indexBelow(const QModelIndex &index) const`
- `bool isAnimated() const`
- `bool isColumnHidden(int column) const`
- `bool isExpanded(const QModelIndex &index) const`
- `bool isFirstColumnSpanned(int row, const QModelIndex &parent) const`
- `bool isHeaderHidden() const`
- `bool isRowHidden(int row, const QModelIndex &parent) const`
- `bool isSortingEnabled() const`
- `bool itemsExpandable() const`
- `void resetIndentation()`
- `bool rootIsDecorated() const`
- `void setAllColumnsShowFocus(bool enable)`
- `void setAnimated(bool enable)`
- `void setAutoExpandDelay(int delay)`
- `void setColumnHidden(int column, bool hide)`
- `void setColumnWidth(int column, int width)`
- `void setExpanded(const QModelIndex &index, bool expanded)`
- `void setExpandsOnDoubleClick(bool enable)`
- `void setFirstColumnSpanned(int row, const QModelIndex &parent, bool span)`
- `void setHeader(QHeaderView *header)`
- `void setHeaderHidden(bool hide)`
- `void setIndentation(int i)`
- `void setItemsExpandable(bool enable)`
- `void setRootIsDecorated(bool show)`
- `void setRowHidden(int row, const QModelIndex &parent, bool hide)`
- `void setSortingEnabled(bool enable)`
- `void setTreePosition(int index)`
- `void setUniformRowHeights(bool uniform)`
- `void setWordWrap(bool on)`
- `int treePosition() const`
- `bool uniformRowHeights() const`
- `bool wordWrap() const`

### 重实现的公有函数

- `virtual void dataChanged(const QModelIndex &topLeft, const QModelIndex &bottomRight, const QList<int> &roles = QList<int>()) override`
- `virtual QModelIndex indexAt(const QPoint &point) const override`
- `virtual void keyboardSearch(const QString &search) override`
- `virtual void reset() override`
- `virtual void scrollTo(const QModelIndex &index, QAbstractItemView::ScrollHint hint = EnsureVisible) override`
- `virtual void selectAll() override`
- `virtual void setModel(QAbstractItemModel *model) override`
- `virtual void setRootIndex(const QModelIndex &index) override`
- `virtual void setSelectionModel(QItemSelectionModel *selectionModel) override`
- `virtual QRect visualRect(const QModelIndex &index) const override`

### 公有槽函数

- `void collapse(const QModelIndex &index)`
- `void collapseAll()`
- `void expand(const QModelIndex &index)`
- `void expandAll()`
- `void expandRecursively(const QModelIndex &index, int depth = -1)`
- `void expandToDepth(int depth)`
- `void hideColumn(int column)`
- `void resizeColumnToContents(int column)`
- `void showColumn(int column)`
- `void sortByColumn(int column, Qt::SortOrder order)`

### 信号

- `void collapsed(const QModelIndex &index)`
- `void expanded(const QModelIndex &index)`

### 保护函数

- `virtual void drawBranches(QPainter *painter, const QRect &rect, const QModelIndex &index) const`
- `virtual void drawRow(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const`
- `void drawTree(QPainter *painter, const QRegion &region) const`
- `int indexRowSizeHint(const QModelIndex &index) const`
- `int rowHeight(const QModelIndex &index) const`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *event) override`
- `virtual void currentChanged(const QModelIndex &current, const QModelIndex &previous) override`
- `virtual void dragMoveEvent(QDragMoveEvent *event) override`
- `virtual int horizontalOffset() const override`
- `virtual bool isIndexHidden(const QModelIndex &index) const override`
- `virtual void keyPressEvent(QKeyEvent *event) override`
- `virtual void mouseDoubleClickEvent(QMouseEvent *event) override`
- `virtual void mouseMoveEvent(QMouseEvent *event) override`
- `virtual void mousePressEvent(QMouseEvent *event) override`
- `virtual void mouseReleaseEvent(QMouseEvent *event) override`
- `virtual QModelIndex moveCursor(QAbstractItemView::CursorAction cursorAction, Qt::KeyboardModifiers modifiers) override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual void rowsAboutToBeRemoved(const QModelIndex &parent, int start, int end) override`
- `virtual void rowsInserted(const QModelIndex &parent, int start, int end) override`
- `virtual void scrollContentsBy(int dx, int dy) override`
- `virtual QModelIndexList selectedIndexes() const override`
- `virtual void selectionChanged(const QItemSelection &selected, const QItemSelection &deselected) override`
- `virtual void setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags command) override`
- `virtual int sizeHintForColumn(int column) const override`
- `virtual void timerEvent(QTimerEvent *event) override`
- `virtual void updateGeometries() override`
- `virtual int verticalOffset() const override`
- `virtual bool viewportEvent(QEvent *event) override`
- `virtual QSize viewportSizeHint() const override`
- `virtual QRegion visualRegionForSelection(const QItemSelection &selection) const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `allColumnsShowFocus : bool`

**作用与语义：**

该属性决定了所有列中是否应显示键盘焦点。
如果该属性`true`，所有列都会显示焦点，否则只有一列显示焦点。
默认是假的。

**如何使用：** 调用 `allColumnsShowFocus()` 读取当前值；它不会修改应用状态。

### `animated : bool`

**作用与语义：**

该属性在动画是否被启用时仍然适用。
如果`true`该属性，树视图会动画分支的展开和折叠。如果`false`该属性，树状视图会立即展开或折叠分支，且不显示动画。
默认情况下，该属性为`false`。

**如何使用：** 调用 `animated()` 读取当前值；它不会修改应用状态。

### `autoExpandDelay : int`

**作用与语义：**

此属性保存拖放操作中树中项目在打开前的延迟时间。
此属性保存用户必须在节点上停留的毫秒数，节点才会自动打开。如果时间设置为小于0，则不会激活。
默认情况下，此属性的值为 -1，表示自动展开被禁用。

**如何使用：** 调用 `autoExpandDelay()` 读取当前值；它不会修改应用状态。

### `expandsOnDoubleClick : bool`

**作用与语义：**

该属性决定了这些物品是否可以通过双击展开。
该属性决定用户是否可以通过双击展开和折叠物品。默认值为真。

**如何使用：** 调用 `expandsOnDoubleClick()` 读取当前值；它不会修改应用状态。

### `headerHidden : bool`

**作用与语义：**

无论是否显示头部，这一属性都成立。
如果该属性为`true`，则不显示头部，否则显示为。默认值为假。

**如何使用：** 调用 `headerHidden()` 读取当前值；它不会修改应用状态。

### `indentation : int`

**作用与语义：**

在树状树视图中缩进项目。
该属性保留树视图中每个层级中单位的缩进，单位为像素。对于顶层项目，缩进指定了从视口边缘到第一列物品的水平距离;对于子项目，它指定它们与父项目之间的缩进距离。
默认情况下，该属性的值与样式相关。因此，当样式发生变化时，该属性会从中更新。调用 setIndentation() 会停止更新，调用 resetIndentation() 则会恢复默认行为。

**如何使用：** 调用 `indentation()` 读取当前值；它不会修改应用状态。

### `itemsExpandable : bool`

**作用与语义：**

该属性决定物品是否可被用户扩展。
该属性决定用户是否能交互式展开和折叠物品。
默认情况下，该属性是`true`。

**如何使用：** 调用 `itemsExpandable()` 读取当前值；它不会修改应用状态。

### `rootIsDecorated : bool`

**作用与语义：**

该属性决定是否显示扩展和折叠顶层项目的控制。
带有子项的项通常会显示出可展开和折叠的控件，允许显示或隐藏其子项。如果该属性为假，顶层项不会显示这些控制项。这可以用来使单层树结构看起来像简单的项列表。
默认情况下，该属性为`true`。

**如何使用：** 调用 `rootIsDecorated()` 读取当前值；它不会修改应用状态。

### `sortingEnabled : bool`

**作用与语义：**

该属性是否启用排序。
如果该属性`true`，则对树进行排序;如果该属性为假，则不启用排序。默认值为假。
注意：为避免性能问题，建议在将项目插入树后启用排序功能。或者，您也可以在将物品插入树之前先将项插入列表。

**如何使用：** 调用 `sortingEnabled()` 读取当前值；它不会修改应用状态。

### `uniformRowHeights : bool`

**作用与语义：**

该属性是否满足树状视图中所有物品高度是否相同。
只有当保证视图中所有物品高度相同时，该属性才应设置为true。这使得视图能够进行一些优化。
高度是从视图中的第一个项目获得的。当该项目的数据发生变化时，高度会被更新。
注意：如果编辑器大小提示大于单元格大小提示，则将使用编辑器的大小提示。
默认情况下，该属性为`false`。

**如何使用：** 调用 `uniformRowHeights()` 读取当前值；它不会修改应用状态。

### `wordWrap : bool`

**作用与语义：**

该属性包含项目文本单词打包策略。
如果该属性`true`，则在需要时在单词分隔处对条目文本进行包装;否则则完全不进行包裹。该属性默认`false`。
注意，即使启用了换行，单元格也不会扩展以容纳所有文本。省略号将根据当前`textElideMode`插入。

**如何使用：** 调用 `wordWrap()` 读取当前值；它不会修改应用状态。

### `[explicit] QTreeView::QTreeView(QWidget *parent = nullptr)`

**作用与语义：**

构建带有 `parent` 表示模型数据的树状视图。使用 `setModel()` 来设置模型。

### `[virtual noexcept] QTreeView::~QTreeView()`

**作用与语义：**

破坏了树景。

### `[override virtual protected] void QTreeView::changeEvent(QEvent *event)`

**作用与语义：**

重实现自：`QFrame::changeEvent`（QEvent *ev）。

### `[slot] void QTreeView::collapse(const QModelIndex &index)`

**作用与语义：**

`index`指定的模型项合并。

### `[slot] void QTreeView::collapseAll()`

**作用与语义：**

会折叠所有扩展物品。

### `[signal] void QTreeView::collapsed(const QModelIndex &index)`

**作用与语义：**

当`index`指定的物品被折叠时，该信号会发出。

### `int QTreeView::columnAt(int x) const`

**作用与语义：**

返回树视图中头部覆盖给定`x`坐标的列。

### `[protected slot] void QTreeView::columnCountChanged(int oldCount, int newCount)`

**作用与语义：**

通知树状视图中的列数从`oldCount`变为`newCount`。

### `[protected slot] void QTreeView::columnMoved()`

**作用与语义：**

每当列被移动时，该槽位都会被调用。

### `[protected slot] void QTreeView::columnResized(int column, int oldSize, int newSize)`

**作用与语义：**

每当`column`在头部中大小发生变化时，都会调用该函数。`oldSize`和`newSize`分别表示之前的大小和新的像素大小。

### `int QTreeView::columnViewportPosition(int column) const`

**作用与语义：**

返回视窗中`column`的水平位置。

### `int QTreeView::columnWidth(int column) const`

**作用与语义：**

返回`column`的宽度。

### `[override virtual protected] void QTreeView::currentChanged(const QModelIndex &current, const QModelIndex &previous)`

**作用与语义：**

Reimpations： `QAbstractItemView::currentChanged`（const QModelIndex ¤t， const QModelIndex &previous）.
当新项目变成当前项目时，调用该槽位。之前的当前项目由`previous`索引指定，新项目由`current`索引指定。
如果你想知道物品的变化，请查看`dataChanged()`信号。

### `[override virtual] void QTreeView::dataChanged(const QModelIndex &topLeft, const QModelIndex &bottomRight, const QList<int> &roles = QList<int>())`

**作用与语义：**

重实现自：`QAbstractItemView::dataChanged`（const QModelIndex & topLeft，const QModelIndex & bottomRight，const QList<int> and roles）。
当模型中具有相同`roles`的物品发生变化时，该槽位被调用。更改的物品包括从`topLeft`到`bottomRight`的物品。如果只更改一个物品`topLeft` == `bottomRight`。
被更改的`roles`可以是空容器（意味着一切都变了），或者是一个包含变更角色子集的非空容器。
注意：`Qt::ToolTipRole`未被 dataChanged() 在 Qt 提供的观点中认可。

### `[override virtual protected] void QTreeView::dragMoveEvent(QDragMoveEvent *event)`

**作用与语义：**

重实现自：`QAbstractItemView::dragMoveEvent`（QDragMoveEvent *event）。

### `[virtual protected] void QTreeView::drawBranches(QPainter *painter, const QRect &rect, const QModelIndex &index) const`

**作用与语义：**

在树视图中，使用与模型项目`index`同一行绘制分支，使用给定的`painter`。分支绘制在`rect`指定的矩形中。

### `[virtual protected] void QTreeView::drawRow(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const`

**作用与语义：**

在树状视图中绘制包含模型物品`index`的行，使用给出的`painter`。`option`控制物品的显示方式。

### `[protected] void QTreeView::drawTree(QPainter *painter, const QRegion &region) const`

**作用与语义：**

使用指定`painter`绘制与给定`region`相交的树部分。

### `[slot] void QTreeView::expand(const QModelIndex &index)`

**作用与语义：**

扩展`index`指定中的模型项。

### `[slot] void QTreeView::expandAll()`

**作用与语义：**

扩展所有可扩展物品。
注意：该函数不会尝试获取更多数据。
警告：如果模型包含大量项目，执行此功能需要较长时间。

### `[slot] void QTreeView::expandRecursively(const QModelIndex &index, int depth = -1)`

**作用与语义：**

将给定`index`的项目及其所有子节点展开到给定`depth`。`depth`相对于给定`index`。`depth`为-1时，所有子节点都会展开;`depth`为0时，只会扩展给定的`index`。
注意：该函数不会尝试获取更多数据。
警告：如果模型包含大量项目，执行此功能需要较长时间。

### `[slot] void QTreeView::expandToDepth(int depth)`

**作用与语义：**

将所有可扩展物品扩展到指定的物品`depth`。
注意：该函数不会尝试获取更多数据。

### `[signal] void QTreeView::expanded(const QModelIndex &index)`

**作用与语义：**

当`index`指定的项被展开时，该信号会发出。

### `QHeaderView *QTreeView::header() const`

**作用与语义：**

返回树状视图的头部。

### `[slot] void QTreeView::hideColumn(int column)`

**作用与语义：**

隐藏了`column`。
注意：该函数应仅在模型初始化后调用，因为视图需要知道列数才能隐藏`column`。

### `[override virtual protected] int QTreeView::horizontalOffset() const`

**作用与语义：**

重实现自：`QAbstractItemView::horizontalOffset()` const.
返回树状视图中物品的水平偏移量。
注意树视图使用水平头部部分位置来确定视图中列的位置。
返回视角的水平偏移。
在基类中，这是一个纯虚拟函数。

### `QModelIndex QTreeView::indexAbove(const QModelIndex &index) const`

**作用与语义：**

返回`index`上方项目的模型索引。

### `[override virtual] QModelIndex QTreeView::indexAt(const QPoint &point) const`

**作用与语义：**

重实现自：`QAbstractItemView::indexAt`（const QPoint & point） const.
返回视口坐标处的模型索引`point`。
在基类中，这是一个纯虚拟函数。

### `QModelIndex QTreeView::indexBelow(const QModelIndex &index) const`

**作用与语义：**

返回`index`下方项目的型号索引。

### `[protected] int QTreeView::indexRowSizeHint(const QModelIndex &index) const`

**作用与语义：**

返回由`index`指示的行的大小提示。

### `bool QTreeView::isColumnHidden(int column) const`

**作用与语义：**

如果 `column` 被隐藏，则返回 `true`；否则返回 `false`。

### `bool QTreeView::isExpanded(const QModelIndex &index) const`

**作用与语义：**

如果模型项`index`展开，返回`true`;否则返回false。

### `bool QTreeView::isFirstColumnSpanned(int row, const QModelIndex &parent) const`

**作用与语义：**

如果`parent`给定`row`第一列的项目跨越所有列，返回`true`;否则返回`false`。

### `[override virtual protected] bool QTreeView::isIndexHidden(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemView::isIndexHidden`（const QModelIndex & index） const.
如果给定`index`所引用的项目隐藏在视图中，返回`true`;否则返回`false`。
隐藏是视图特定的功能。例如`TableView`中可以标记为隐藏列或`TreeView`中的一行。
在基类中，这是一个纯虚拟函数。

### `bool QTreeView::isRowHidden(int row, const QModelIndex &parent) const`

**作用与语义：**

如果`parent`给定`row`中的物品被隐藏，返回`true`;否则返回`false`。

### `[override virtual protected] void QTreeView::keyPressEvent(QKeyEvent *event)`

**作用与语义：**

重实现自：`QAbstractItemView::keyPressEvent`（QKeyEvent *event）。

### `[override virtual] void QTreeView::keyboardSearch(const QString &search)`

**作用与语义：**

重实现自：`QAbstractItemView::keyboardSearch`（const QString &search）。
移动到并选择与字符串最匹配的项`search`。如果未找到任何项，则不会发生任何事。
在默认实现中，如果`search`为空，或自上次搜索到时间区间超过`QApplication::keyboardInputInterval()`，搜索将被重置。

### `[override virtual protected] void QTreeView::mouseDoubleClickEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QAbstractItemView::mouseDoubleClickEvent`（QMouseEvent *event）。

### `[override virtual protected] void QTreeView::mouseMoveEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QAbstractItemView::mouseMoveEvent`（QMouseEvent *event）。

### `[override virtual protected] void QTreeView::mousePressEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QAbstractItemView::mousePressEvent`（QMouseEvent *event）。

### `[override virtual protected] void QTreeView::mouseReleaseEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QAbstractItemView::mouseReleaseEvent`（QMouseEvent *event）。

### `[override virtual protected] QModelIndex QTreeView::moveCursor(QAbstractItemView::CursorAction cursorAction, Qt::KeyboardModifiers modifiers)`

**作用与语义：**

重实现自：`QAbstractItemView::moveCursor`（QAbstractItemView：：CursorAction cursorAction，Qt：：KeyboardModifiers modifiers）。
按照`cursorAction`描述的方式移动光标，使用按钮`modifiers`提供的信息。
返回一个指向视图中下一个对象的`QModelIndex`对象，基于`modifiers`指定的`cursorAction`和键盘修饰符。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] void QTreeView::paintEvent(QPaintEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::paintEvent`（QPaintEvent *event）。

### `[override virtual] void QTreeView::reset()`

**作用与语义：**

重装：`QAbstractItemView::reset()`。
重置视图的内部状态。
警告：该函数将重置打开的编辑器、滚动条位置、选择等。现有的更改不会被提交。如果你想在重置视图时保存你的更改，可以重新实现这个函数，提交你的更改，然后调用该超类的实现。

### `[slot] void QTreeView::resizeColumnToContents(int column)`

**作用与语义：**

调整内容物大小的`column`。

### `[protected] int QTreeView::rowHeight(const QModelIndex &index) const`

**作用与语义：**

返回由给定`index`所示行的高度。

### `[override virtual protected] void QTreeView::rowsAboutToBeRemoved(const QModelIndex &parent, int start, int end)`

**作用与语义：**

重实现自：`QAbstractItemView::rowsAboutToBeRemoved`（const QModelIndex & parent， int start， int end）。
告知视图，从第`start`行到第`end`行的行（包括包括）即将从给定的`parent`模型项目中移除。
当行即将被移除时，该格子被调用。被删除的行是从`start`到`end`包含给定`parent`下的行。

### `[override virtual protected] void QTreeView::rowsInserted(const QModelIndex &parent, int start, int end)`

**作用与语义：**

重实现自：`QAbstractItemView::rowsInserted`（const QModelIndex &parent， int start， int end）。
告知视图，从`start`行到`end`行的行已入`parent`模型项中。
插入行时调用该槽位。新行为`parent`下，从`start`到`end`包含。基类实现调用模型上的fetchMore()以检查更多数据。

### `[protected slot] void QTreeView::rowsRemoved(const QModelIndex &parent, int start, int end)`

**作用与语义：**

告知视图，从第`start`行到第`end`行的行（包括包括）已被从给定`parent`模型项中移除。

### `[override virtual protected] void QTreeView::scrollContentsBy(int dx, int dy)`

**作用与语义：**

重实现自：`QAbstractScrollArea::scrollContentsBy`（智力 dx，智力 dy）。
将树状视图内容滚动到（`dx`，`dy`）。
当滚动条被`dx`、`dy`移动时调用该虚拟处理程序，因此应相应地滚动视口内容。
默认实现只需调用整个`viewport()`的`update()`，子类可以重新实现该处理程序以优化，或者像`QScrollArea`一样移动内容控件。参数`dx`和`dy`是为了方便，让类知道应该滚动多少（例如像素移位时很有用）。你也可以忽略这些值，直接滚动到滚动条指示的位置。
调用该函数以进行程序滚动是错误的，建议使用滚动条（例如直接调用`QScrollBar::setValue()`）。

### `[override virtual] void QTreeView::scrollTo(const QModelIndex &index, QAbstractItemView::ScrollHint hint = EnsureVisible)`

**作用与语义：**

重实现自：`QAbstractItemView::scrollTo`（const QModelIndex & index， QAbstractItemView：：ScrollHint 提示）。
滚动树状视图的内容，直到给定的模型项目`index`可见。`hint`参数更精确地指定操作后该项目应位于的位置。如果模型项目的父节点被折叠，它们会展开以确保模型项目可见。
如有需要，滚动视图以确保该物品在`index`可见。视图会根据给定的`hint`尝试定位该物品。
在基类中，这是一个纯虚拟函数。

### `[override virtual] void QTreeView::selectAll()`

**作用与语义：**

重装：`QAbstractItemView::selectAll()`。
选择视图中的所有项目。该函数在选择时会使用视图中的选择行为。

### `[override virtual protected] QModelIndexList QTreeView::selectedIndexes() const`

**作用与语义：**

重装：`QAbstractItemView::selectedIndexes()` const.
这个便利函数返回视图中所有已选中和非隐藏的项目索引列表。该列表没有重复，也没有排序。

### `[override virtual protected] void QTreeView::selectionChanged(const QItemSelection &selected, const QItemSelection &deselected)`

**作用与语义：**

重实现自：`QAbstractItemView::selectionChanged`（const QItemSelection &selected， const QItemSelection &deselected）.
当选择发生变化时，该槽函数被调用。之前的选择（可能是空的）由`deselected`指定，新选择由`selected`表示。

### `void QTreeView::setColumnHidden(int column, bool hide)`

**作用与语义：**

如果`hide`为真，则`column`被隐藏，否则`column`会被显示。

### `void QTreeView::setColumnWidth(int column, int width)`

**作用与语义：**

将给定`column`的宽度设置为指定的`width`。

### `void QTreeView::setExpanded(const QModelIndex &index, bool expanded)`

**作用与语义：**

根据`expanded` `index`的值，将所指项设置为折叠或扩展。

### `void QTreeView::setFirstColumnSpanned(int row, const QModelIndex &parent, bool span)`

**作用与语义：**

如果`span`为真，`row`中第一列中与给定`parent`的项设置为跨越所有列，否则显示`row`上的所有项。

### `void QTreeView::setHeader(QHeaderView *header)`

**作用与语义：**

将树视图的首部设置为给定的`header`。
视图会对给定`header`拥有权，并在设置新头部时删除该页面。

### `[override virtual] void QTreeView::setModel(QAbstractItemModel *model)`

**作用与语义：**

重实现自：`QAbstractItemView::setModel`（QAbstractItemModel *model）。
将视图的`model`设定为呈现。
该函数将创建并设置新的选择模型，替换之前用`setSelectionModel()`设置的模型。不过，旧的选择模型不会被删除，因为它可能在多个视图之间共享。如果旧的选择模型不再需要，我们建议你删除它。这可以通过以下代码完成：
如果旧模型和旧选择模型都没有父模型，或者它们的父对象是长寿命对象，可能更倾向于调用它们的`deleteLater()`函数来显式删除它们。
视图不会拥有该模型的所有权，除非它是模型的父对象，因为模型可能在多个不同视图之间共享。

### `[override virtual] void QTreeView::setRootIndex(const QModelIndex &index)`

**作用与语义：**

重装：`QAbstractItemView::setRootIndex`（const QModelIndex & index）。
将根项设置为给定`index`的项。

### `void QTreeView::setRowHidden(int row, const QModelIndex &parent, bool hide)`

**作用与语义：**

如果`hide`为真，则带有给定`parent`的`row`被隐藏，否则显示`row`。

### `[override virtual protected] void QTreeView::setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags command)`

**作用与语义：**

重实现自：`QAbstractItemView::setSelection`（const QRect &rect， QItemSelectionModel：：SelectionFlags flags）。
将选择`command`应用到矩形内或接触到的物品，`rect`。
将选择`flags`应用于矩形内或被触及的物品，`rect`。
在实现自己的 itemview 时，setSelection 应调用 `selectionModel()`->select（selection， flags），其中 selection 要么是空的 `QModelIndex`，要么是包含所有 `rect` 中物品的`QItemSelection`。

### `[override virtual] void QTreeView::setSelectionModel(QItemSelectionModel *selectionModel)`

**作用与语义：**

Reimplements： `QAbstractItemView::setSelectionModel`（QItemSelectionModel *selectionModel）.
将当前选择模型设定为给定的`selectionModel`。
注意，如果你在该函数后调用`setModel()`，给定的`selectionModel`将被视图创建的替代。
注意：如果旧的选择模型不再需要，应用程序自行删除;即当它不再被其他视图使用时。当其父对象被删除时，这会自动发生。然而，如果它没有父对象，或者父对象是长期存在的对象，可能更倾向于调用其`deleteLater()`函数显式删除它。

### `void QTreeView::setTreePosition(int index)`

**作用与语义：**

这规定树结构应置于逻辑索引`index`。若设置为 -1，则树始终遵循视觉索引 0。

### `[slot] void QTreeView::showColumn(int column)`

**作用与语义：**

在树状视图中显示给定的`column`。

### `[override virtual protected] int QTreeView::sizeHintForColumn(int column) const`

**作用与语义：**

重实现自：`QAbstractItemView::sizeHintForColumn`（整数列）const.
返回`column`宽度的尺寸提示，若无模型则返回-1。
如果你需要将某列的宽度设置为固定值，可以在视图的头部调用`QHeaderView::resizeSection()`。
如果你在子类中重新实现该函数，请注意你返回的值只有在调用 `resizeColumnToContents()` 时才会被使用。在这种情况下，如果视图的头部或项目代理需要更大的列宽，则会使用该宽度。
返回指定`column`的宽度大小提示，若无模型则返回-1。
该函数用于带有水平头部的视图，根据给定`column`的内容查找头部部分的大小提示。

### `[slot] void QTreeView::sortByColumn(int column, Qt::SortOrder order)`

**作用与语义：**

根据给定`column`和`order`的值对模型进行排序。
`column`可能为-1，此时不会显示排序指示器，模型会恢复到自然的未排序顺序。注意，并非所有模型都支持此功能，这种情况下甚至可能崩溃。

### `[override virtual protected] void QTreeView::timerEvent(QTimerEvent *event)`

**作用与语义：**

重实现自：`QAbstractItemView::timerEvent`（QTimerEvent *event）。

### `int QTreeView::treePosition() const`

**作用与语义：**

返回树所处的逻辑索引。如果返回值为-1，则将树置于视觉索引0。

### `[override virtual protected] void QTreeView::updateGeometries()`

**作用与语义：**

重装：`QAbstractItemView::updateGeometries()`。
更新视图子控件的几何体。

### `[override virtual protected] int QTreeView::verticalOffset() const`

**作用与语义：**

重装：`QAbstractItemView::verticalOffset()` const.
返回树状视图中物品的垂直偏移量。
返回视图的垂直偏移量。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] bool QTreeView::viewportEvent(QEvent *event)`

**作用与语义：**

重装：`QAbstractItemView::viewportEvent`（QEvent *事件）。

### `[override virtual protected] QSize QTreeView::viewportSizeHint() const`

**作用与语义：**

重装：`QAbstractItemView::viewportSizeHint()` const.

### `[override virtual] QRect QTreeView::visualRect(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemView::visualRect`（const QModelIndex & index） const.
返回视口中该物品所在的矩形`index`。如果索引未可见或明确隐藏，返回矩形无效。
返回该物品在`index`处所在的视口矩形。
如果你的项目显示在多个区域，visualRect 应该返回包含索引的主要区域，而不是索引可能涵盖、触摸或导致绘图的全部区域。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] QRegion QTreeView::visualRegionForSelection(const QItemSelection &selection) const`

**作用与语义：**

重装：`QAbstractItemView::visualRegionForSelection`（const QItemSelection &selection） const.
返回该`selection`中物品的视口矩形。
自4.7版本起，返回区域仅包含与视口相交（或包含）的矩形。
从视口返回给定`selection`中物品的区域。
在基类中，这是一个纯虚拟函数。

### `bool allColumnsShowFocus() const`

**作用与语义：**

该属性决定了所有列中是否应显示键盘焦点。
如果该属性`true`，所有列都会显示焦点，否则只有一列显示焦点。
默认是假的。

**如何使用：** 调用 `allColumnsShowFocus()` 读取当前值；它不会修改应用状态。

### `int autoExpandDelay() const`

**作用与语义：**

此属性保存拖放操作中树中项目在打开前的延迟时间。
此属性保存用户必须在节点上停留的毫秒数，节点才会自动打开。如果时间设置为小于0，则不会激活。
默认情况下，此属性的值为 -1，表示自动展开被禁用。

**如何使用：** 调用 `autoExpandDelay()` 读取当前值；它不会修改应用状态。

### `bool expandsOnDoubleClick() const`

**作用与语义：**

该属性决定了这些物品是否可以通过双击展开。
该属性决定用户是否可以通过双击展开和折叠物品。默认值为真。

**如何使用：** 调用 `expandsOnDoubleClick()` 读取当前值；它不会修改应用状态。

### `int indentation() const`

**作用与语义：**

在树状树视图中缩进项目。
该属性保留树视图中每个层级中单位的缩进，单位为像素。对于顶层项目，缩进指定了从视口边缘到第一列物品的水平距离;对于子项目，它指定它们与父项目之间的缩进距离。
默认情况下，该属性的值与样式相关。因此，当样式发生变化时，该属性会从中更新。调用 setIndentation() 会停止更新，调用 resetIndentation() 则会恢复默认行为。

**如何使用：** 调用 `indentation()` 读取当前值；它不会修改应用状态。

### `bool isAnimated() const`

**作用与语义：**

该属性在动画是否被启用时仍然适用。
如果`true`该属性，树视图会动画分支的展开和折叠。如果`false`该属性，树状视图会立即展开或折叠分支，且不显示动画。
默认情况下，该属性为`false`。

**如何使用：** 调用 `isAnimated()` 读取当前值；它不会修改应用状态。

### `bool isHeaderHidden() const`

**作用与语义：**

无论是否显示头部，这一属性都成立。
如果该属性为`true`，则不显示头部，否则显示为。默认值为假。

**如何使用：** 调用 `isHeaderHidden()` 读取当前值；它不会修改应用状态。

### `bool isSortingEnabled() const`

**作用与语义：**

该属性是否启用排序。
如果该属性`true`，则对树进行排序;如果该属性为假，则不启用排序。默认值为假。
注意：为避免性能问题，建议在将项目插入树后启用排序功能。或者，您也可以在将物品插入树之前先将项插入列表。

**如何使用：** 调用 `isSortingEnabled()` 读取当前值；它不会修改应用状态。

### `bool itemsExpandable() const`

**作用与语义：**

该属性决定物品是否可被用户扩展。
该属性决定用户是否能交互式展开和折叠物品。
默认情况下，该属性是`true`。

**如何使用：** 调用 `itemsExpandable()` 读取当前值；它不会修改应用状态。

### `void resetIndentation()`

**作用与语义：**

在树状树视图中缩进项目。
该属性保留树视图中每个层级中单位的缩进，单位为像素。对于顶层项目，缩进指定了从视口边缘到第一列物品的水平距离;对于子项目，它指定它们与父项目之间的缩进距离。
默认情况下，该属性的值与样式相关。因此，当样式发生变化时，该属性会从中更新。调用 setIndentation() 会停止更新，调用 resetIndentation() 则会恢复默认行为。

**如何使用：** 调用 `resetIndentation()` 撤销对 `indentation` 的显式覆盖，让它重新采用继承值或默认值。

### `bool rootIsDecorated() const`

**作用与语义：**

该属性决定是否显示扩展和折叠顶层项目的控制。
带有子项的项通常会显示出可展开和折叠的控件，允许显示或隐藏其子项。如果该属性为假，顶层项不会显示这些控制项。这可以用来使单层树结构看起来像简单的项列表。
默认情况下，该属性为`true`。

**如何使用：** 调用 `rootIsDecorated()` 读取当前值；它不会修改应用状态。

### `void setAllColumnsShowFocus(bool enable)`

**作用与语义：**

该属性决定了所有列中是否应显示键盘焦点。
如果该属性`true`，所有列都会显示焦点，否则只有一列显示焦点。
默认是假的。

**如何使用：** 调用 `setAllColumnsShowFocus(...)` 修改 `allColumnsShowFocus`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAnimated(bool enable)`

**作用与语义：**

该属性在动画是否被启用时仍然适用。
如果`true`该属性，树视图会动画分支的展开和折叠。如果`false`该属性，树状视图会立即展开或折叠分支，且不显示动画。
默认情况下，该属性为`false`。

**如何使用：** 调用 `setAnimated(...)` 修改 `animated`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAutoExpandDelay(int delay)`

**作用与语义：**

此属性保存拖放操作中树中项目在打开前的延迟时间。
此属性保存用户必须在节点上停留的毫秒数，节点才会自动打开。如果时间设置为小于0，则不会激活。
默认情况下，此属性的值为 -1，表示自动展开被禁用。

**如何使用：** 调用 `setAutoExpandDelay(...)` 修改 `autoExpandDelay`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setExpandsOnDoubleClick(bool enable)`

**作用与语义：**

该属性决定了这些物品是否可以通过双击展开。
该属性决定用户是否可以通过双击展开和折叠物品。默认值为真。

**如何使用：** 调用 `setExpandsOnDoubleClick(...)` 修改 `expandsOnDoubleClick`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setHeaderHidden(bool hide)`

**作用与语义：**

无论是否显示头部，这一属性都成立。
如果该属性为`true`，则不显示头部，否则显示为。默认值为假。

**如何使用：** 调用 `setHeaderHidden(...)` 修改 `headerHidden`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIndentation(int i)`

**作用与语义：**

在树状树视图中缩进项目。
该属性保留树视图中每个层级中单位的缩进，单位为像素。对于顶层项目，缩进指定了从视口边缘到第一列物品的水平距离;对于子项目，它指定它们与父项目之间的缩进距离。
默认情况下，该属性的值与样式相关。因此，当样式发生变化时，该属性会从中更新。调用 setIndentation() 会停止更新，调用 resetIndentation() 则会恢复默认行为。

**如何使用：** 调用 `setIndentation(...)` 修改 `indentation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setItemsExpandable(bool enable)`

**作用与语义：**

该属性决定物品是否可被用户扩展。
该属性决定用户是否能交互式展开和折叠物品。
默认情况下，该属性是`true`。

**如何使用：** 调用 `setItemsExpandable(...)` 修改 `itemsExpandable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setRootIsDecorated(bool show)`

**作用与语义：**

该属性决定是否显示扩展和折叠顶层项目的控制。
带有子项的项通常会显示出可展开和折叠的控件，允许显示或隐藏其子项。如果该属性为假，顶层项不会显示这些控制项。这可以用来使单层树结构看起来像简单的项列表。
默认情况下，该属性为`true`。

**如何使用：** 调用 `setRootIsDecorated(...)` 修改 `rootIsDecorated`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSortingEnabled(bool enable)`

**作用与语义：**

该属性是否启用排序。
如果该属性`true`，则对树进行排序;如果该属性为假，则不启用排序。默认值为假。
注意：为避免性能问题，建议在将项目插入树后启用排序功能。或者，您也可以在将物品插入树之前先将项插入列表。

**如何使用：** 调用 `setSortingEnabled(...)` 修改 `sortingEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUniformRowHeights(bool uniform)`

**作用与语义：**

该属性是否满足树状视图中所有物品高度是否相同。
只有当保证视图中所有物品高度相同时，该属性才应设置为true。这使得视图能够进行一些优化。
高度是从视图中的第一个项目获得的。当该项目的数据发生变化时，高度会被更新。
注意：如果编辑器大小提示大于单元格大小提示，则将使用编辑器的大小提示。
默认情况下，该属性为`false`。

**如何使用：** 调用 `setUniformRowHeights(...)` 修改 `uniformRowHeights`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWordWrap(bool on)`

**作用与语义：**

该属性包含项目文本单词打包策略。
如果该属性`true`，则在需要时在单词分隔处对条目文本进行包装;否则则完全不进行包裹。该属性默认`false`。
注意，即使启用了换行，单元格也不会扩展以容纳所有文本。省略号将根据当前`textElideMode`插入。

**如何使用：** 调用 `setWordWrap(...)` 修改 `wordWrap`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool uniformRowHeights() const`

**作用与语义：**

该属性是否满足树状视图中所有物品高度是否相同。
只有当保证视图中所有物品高度相同时，该属性才应设置为true。这使得视图能够进行一些优化。
高度是从视图中的第一个项目获得的。当该项目的数据发生变化时，高度会被更新。
注意：如果编辑器大小提示大于单元格大小提示，则将使用编辑器的大小提示。
默认情况下，该属性为`false`。

**如何使用：** 调用 `uniformRowHeights()` 读取当前值；它不会修改应用状态。

### `bool wordWrap() const`

**作用与语义：**

该属性包含项目文本单词打包策略。
如果该属性`true`，则在需要时在单词分隔处对条目文本进行包装;否则则完全不进行包裹。该属性默认`false`。
注意，即使启用了换行，单元格也不会扩展以容纳所有文本。省略号将根据当前`textElideMode`插入。

**如何使用：** 调用 `wordWrap()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTreeView` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
