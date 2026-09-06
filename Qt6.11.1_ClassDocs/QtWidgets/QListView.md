# QListView

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** 列表模型/视图控件，负责以列表形式展示模型项目、选择、滚动和编辑。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QListView`：列表模型/视图控件，负责以列表形式展示模型项目、选择、滚动和编辑。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QListView>`
- 继承自：QAbstractItemView
- 直接派生类：QHelpIndexWidget、QListWidget,、QUndoView

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

### 状态、生命周期和线程

**生命周期：** 容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

**状态与结果：** 要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

**线程与事件循环：** 不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

## 3. 直接使用

先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

```cpp
#include <QList>

QList<int> values{1, 2, 3};
values.append(4);
for (const int value : values) {
    // 使用 value
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Flow { LeftToRight, TopToBottom }`
- `enum LayoutMode { SinglePass, Batched }`
- `enum Movement { Static, Free, Snap }`
- `enum ResizeMode { Fixed, Adjust }`
- `enum ViewMode { ListMode, IconMode }`

### 属性

- `batchSize : int`
- `flow : Flow`
- `gridSize : QSize`
- `isWrapping : bool`
- `itemAlignment : Qt::Alignment`
- `layoutMode : LayoutMode`
- `modelColumn : int`
- `movement : Movement`
- `resizeMode : ResizeMode`
- `selectionRectVisible : bool`
- `spacing : int`
- `uniformItemSizes : bool`
- `viewMode : ViewMode`
- `wordWrap : bool`

### 公有函数

- `QListView(QWidget *parent = nullptr)`
- `virtual ~QListView()`
- `int batchSize() const`
- `void clearPropertyFlags()`
- `QListView::Flow flow() const`
- `QSize gridSize() const`
- `bool isRowHidden(int row) const`
- `bool isSelectionRectVisible() const`
- `bool isWrapping() const`
- `Qt::Alignment itemAlignment() const`
- `QListView::LayoutMode layoutMode() const`
- `int modelColumn() const`
- `QListView::Movement movement() const`
- `QListView::ResizeMode resizeMode() const`
- `void setBatchSize(int batchSize)`
- `void setFlow(QListView::Flow flow)`
- `void setGridSize(const QSize &size)`
- `void setItemAlignment(Qt::Alignment alignment)`
- `void setLayoutMode(QListView::LayoutMode mode)`
- `void setModelColumn(int column)`
- `void setMovement(QListView::Movement movement)`
- `void setResizeMode(QListView::ResizeMode mode)`
- `void setRowHidden(int row, bool hide)`
- `void setSelectionRectVisible(bool show)`
- `void setSpacing(int space)`
- `void setUniformItemSizes(bool enable)`
- `void setViewMode(QListView::ViewMode mode)`
- `void setWordWrap(bool on)`
- `void setWrapping(bool enable)`
- `int spacing() const`
- `bool uniformItemSizes() const`
- `QListView::ViewMode viewMode() const`
- `bool wordWrap() const`

### 重实现的公有函数

- `virtual QModelIndex indexAt(const QPoint &p) const override`
- `virtual void scrollTo(const QModelIndex &index, QAbstractItemView::ScrollHint hint = EnsureVisible) override`
- `virtual void setRootIndex(const QModelIndex &index) override`
- `virtual QRect visualRect(const QModelIndex &index) const override`

### 信号

- `void indexesMoved(const QModelIndexList &indexes)`

### 保护函数

- `QRect rectForIndex(const QModelIndex &index) const`
- `void setPositionForIndex(const QPoint &position, const QModelIndex &index)`

### 重实现的保护函数

- `virtual void currentChanged(const QModelIndex &current, const QModelIndex &previous) override`
- `virtual void dataChanged(const QModelIndex &topLeft, const QModelIndex &bottomRight, const QList<int> &roles = QList<int>()) override`
- `virtual void dragLeaveEvent(QDragLeaveEvent *e) override`
- `virtual void dragMoveEvent(QDragMoveEvent *e) override`
- `virtual void dropEvent(QDropEvent *event) override`
- `virtual bool event(QEvent *e) override`
- `virtual int horizontalOffset() const override`
- `virtual void initViewItemOption(QStyleOptionViewItem *option) const override`
- `virtual bool isIndexHidden(const QModelIndex &index) const override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual QModelIndex moveCursor(QAbstractItemView::CursorAction cursorAction, Qt::KeyboardModifiers modifiers) override`
- `virtual void paintEvent(QPaintEvent *e) override`
- `virtual void resizeEvent(QResizeEvent *e) override`
- `virtual void rowsAboutToBeRemoved(const QModelIndex &parent, int start, int end) override`
- `virtual void rowsInserted(const QModelIndex &parent, int start, int end) override`
- `virtual void scrollContentsBy(int dx, int dy) override`
- `virtual QModelIndexList selectedIndexes() const override`
- `virtual void selectionChanged(const QItemSelection &selected, const QItemSelection &deselected) override`
- `virtual void setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags command) override`
- `virtual void startDrag(Qt::DropActions supportedActions) override`
- `virtual void timerEvent(QTimerEvent *e) override`
- `virtual void updateGeometries() override`
- `virtual int verticalOffset() const override`
- `virtual QSize viewportSizeHint() const override`
- `virtual QRegion visualRegionForSelection(const QItemSelection &selection) const override`
- `virtual void wheelEvent(QWheelEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QListView::LayoutMode`

**作用与语义：**

- `QListView::SinglePass`：`0`;物品一次性摆放。
- `QListView::Batched`：`1`;物品以`batchSize`件为一组排列。

### `batchSize : int`

**作用与语义：**

如果将`layoutMode`设为`Batched`，该属性表示每批中排列的物品数量。
默认值是100。

**如何使用：** 调用 `batchSize()` 读取当前值；它不会修改应用状态。

### `flow : Flow`

**作用与语义：**

该属性决定了物品布局应朝向流动。
如果该属性`LeftToRight`，物品将从左到右排列。如果`isWrapping`属性`true`，布局在到达可见区域右侧时会包裹。如果该属性`TopToBottom`，物品将从可见区域顶部展开，达到底部时包裹。
当视图可见时设置该属性，物品会重新排列。
默认情况下，该属性设置为`TopToBottom`。

**如何使用：** 调用 `flow()` 读取当前值；它不会修改应用状态。

### `gridSize : QSize`

**作用与语义：**

该属性表示布局网格的大小。
该属性是物品摆放所在网格的大小。默认尺寸为空，意味着没有网格，布局也不是在网格中完成的。将该属性设置为非空大小，网格布局会被切换。（当网格布局生效时，`spacing`属性被忽略。）。
当视图可见时设置该属性，物品会重新排列。

**如何使用：** 调用 `gridSize()` 读取当前值；它不会修改应用状态。

### `isWrapping : bool`

**作用与语义：**

该属性决定了物品布局是否应进行包裹。
该属性决定了当可见区域没有更多空间时，布局是否应进行包裹。布局折叠的地点取决于`flow`属性。
当视图可见时设置该属性，物品会重新排列。
默认情况下，该属性是`false`的。

**如何使用：** 调用 `isWrapping()` 读取当前值；它不会修改应用状态。

### `itemAlignment : Qt::Alignment`

**作用与语义：**

该属性保留了每个单元格中的对齐。
这只在`ListMode`中支持，且`TopToBottom`流且启用包裹。默认对齐为0，意味着项目会完全填满其单元格。

**如何使用：** 调用 `itemAlignment()` 读取当前值；它不会修改应用状态。

### `layoutMode : LayoutMode`

**作用与语义：**

决定物品的布局是应立即进行还是延迟。
该属性包含了物品的布局模式。当该模式`SinglePass`（默认）时，物品会一次性摆放好。当该模式`Batched`时，物品会分批`batchSize`件物品摆放，同时处理事件。这使得在其他物品摆放时，可以即时查看和交互可见物品。

**如何使用：** 调用 `layoutMode()` 读取当前值；它不会修改应用状态。

### `modelColumn : int`

**作用与语义：**

该属性表示模型中可见的列。
默认情况下，该属性包含0，表示模型的第一列将被显示。

**如何使用：** 调用 `modelColumn()` 读取当前值；它不会修改应用状态。

### `movement : Movement`

**作用与语义：**

该属性适用于物品是否可以自由移动、被吸附到网格上，还是完全无法移动。
该属性决定了用户如何在视图中移动这些物品。`Static` 表示用户不能移动这些物品。`Free` 意味着用户可以拖拽物品到视图中的任何位置。`Snap` 意味着用户可以拖放物品，但只能拖拽到 `gridSize` 属性所指示的假想网格中的位置。
当视图可见时设置该属性，物品会重新排列。
默认情况下，该属性设为`Static`。

**如何使用：** 调用 `movement()` 读取当前值；它不会修改应用状态。

### `resizeMode : ResizeMode`

**作用与语义：**

该属性是否在视图调整时重新布局。
如果该属性被`Adjust`，视图调整大小时项目将重新排列。如果值`Fixed`，视图调整时物品不会被布局。
默认情况下，该属性设置为`Fixed`。

**如何使用：** 调用 `resizeMode()` 读取当前值；它不会修改应用状态。

### `selectionRectVisible : bool`

**作用与语义：**

如果选择矩形应该是可见的。
如果`true`该属性，则选择矩形是可见的;否则它将被隐藏。
注意：只有当选择模式允许多项选择时，选区矩形才会显示;即如果选区模式为`QAbstractItemView::SingleSelection`，则不会绘制选区矩形。
默认情况下，该属性为`false`。

**如何使用：** 调用 `selectionRectVisible()` 读取当前值；它不会修改应用状态。

### `spacing : int`

**作用与语义：**

该属性保留了布局中物品周围的空间。
该属性是指布局中围绕物品填充的空白空间的大小。
当视图可见时设置该属性，物品会重新排列。
默认情况下，该属性的值为0。

**如何使用：** 调用 `spacing()` 读取当前值；它不会修改应用状态。

### `uniformItemSizes : bool`

**作用与语义：**

该属性确定列表视图中所有项目大小是否相同。
只有当保证视图中所有项目大小相同时，该属性才应设置为 true。这使得视图能够为性能进行一些优化。
默认情况下，该属性为`false`。

**如何使用：** 调用 `uniformItemSizes()` 读取当前值；它不会修改应用状态。

### `viewMode : ViewMode`

**作用与语义：**

该属性表示`QListView`的视模式。
该属性会将其他未设置属性调整为符合集合视图模式。已设置的 `QListView` 特定属性不会被更改，除非调用了 `clearPropertyFlags()`。
设置视图模式会根据所选移动开启或禁用拖放。`ListMode`时，默认移动为`Static`（拖放禁用）;`IconMode`中默认移动为`Free`（启用拖放）。

**如何使用：** 调用 `viewMode()` 读取当前值；它不会修改应用状态。

### `wordWrap : bool`

**作用与语义：**

该属性包含项目文本单词打包策略。
如果该属性`true`，则在词分隔处必要时对条目文本进行装帧;否则则完全不进行装包。该属性默认`false`。
请注意，即使启用了换行，单元格也不会被展开以腾出文本空间。根据视图的 `textElideMode`，对于无法显示的文本，它会打印省略号。

**如何使用：** 调用 `wordWrap()` 读取当前值；它不会修改应用状态。

### `[explicit] QListView::QListView(QWidget *parent = nullptr)`

**作用与语义：**

创建一个新的QListView，并使用给定的`parent`来查看模型。使用`setModel()`设置模型。

### `[virtual noexcept] QListView::~QListView()`

**作用与语义：**

破坏了视野。

### `void QListView::clearPropertyFlags()`

**作用与语义：**

清除`QListView`特定属性的标志。详见`viewMode`。
从`QAbstractItemView`继承的属性不被属性标志覆盖。具体来说，`dragEnabled`和`acceptsDrops`在调用`setMovement()`或`setViewMode()`时通过`QListView`计算。

### `[override virtual protected] void QListView::currentChanged(const QModelIndex &current, const QModelIndex &previous)`

**作用与语义：**

Reimpations： `QAbstractItemView::currentChanged`（const QModelIndex ¤t， const QModelIndex &previous）.
当新项目变成当前项目时，调用该槽位。之前的当前项目由`previous`索引指定，新项目由`current`索引指定。
如果你想知道物品的变化，请查看`dataChanged()`信号。

### `[override virtual protected] void QListView::dataChanged(const QModelIndex &topLeft, const QModelIndex &bottomRight, const QList<int> &roles = QList<int>())`

**作用与语义：**

重实现自：`QAbstractItemView::dataChanged`（const QModelIndex & topLeft，const QModelIndex & bottomRight，const QList<int> and roles）。
当模型中具有相同`roles`的物品发生变化时，该槽位被调用。更改的物品包括从`topLeft`到`bottomRight`的物品。如果只更改一个物品`topLeft` == `bottomRight`。
被更改的`roles`可以是空容器（意味着一切都变了），或者是一个包含变更角色子集的非空容器。
注意：`Qt::ToolTipRole`未被 dataChanged() 在 Qt 提供的观点中认可。

### `[override virtual protected] void QListView::dragLeaveEvent(QDragLeaveEvent *e)`

**作用与语义：**

重实现自：`QAbstractItemView::dragLeaveEvent`（QDragLeaveEvent *event）。

### `[override virtual protected] void QListView::dragMoveEvent(QDragMoveEvent *e)`

**作用与语义：**

重实现自：`QAbstractItemView::dragMoveEvent`（QDragMoveEvent *event）。

### `[override virtual protected] void QListView::dropEvent(QDropEvent *event)`

**作用与语义：**

重实现自：`QAbstractItemView::dropEvent`（QDropEvent *event）。

### `[override virtual protected] bool QListView::event(QEvent *e)`

**作用与语义：**

重装：`QAbstractItemView::event`（QEvent *事件）。

### `[override virtual protected] int QListView::horizontalOffset() const`

**作用与语义：**

重装：`QAbstractItemView::horizontalOffset()` const.
返回视角的水平偏移。
在基类中，这是一个纯虚拟函数。

### `[override virtual] QModelIndex QListView::indexAt(const QPoint &p) const`

**作用与语义：**

重实现自：`QAbstractItemView::indexAt`（const QPoint & point） const.
返回视口坐标处的模型索引`point`。
在基类中，这是一个纯虚拟函数。

### `[signal] void QListView::indexesMoved(const QModelIndexList &indexes)`

**作用与语义：**

当指定`indexes`在视野中移动时，该信号会发出。

### `[override virtual protected] void QListView::initViewItemOption(QStyleOptionViewItem *option) const`

**作用与语义：**

Reimplements： `QAbstractItemView::initViewItemOption`（QStyleOptionViewItem *option） const.
用视图的调色板、字体、状态、对齐等初始化`option`结构。
注意：该方法的实现应检查接收结构的 `version`，填充实现熟悉的所有成员，并将版本成员设置为实现支持的版本，然后返回。

### `[override virtual protected] bool QListView::isIndexHidden(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemView::isIndexHidden`（const QModelIndex & index） const.
如果给定`index`所引用的项目隐藏在视图中，返回`true`;否则返回`false`。
隐藏是视图特定的功能。例如`TableView`中可以标记为隐藏列或`TreeView`中的一行。
在基类中，这是一个纯虚拟函数。

### `bool QListView::isRowHidden(int row) const`

**作用与语义：**

如果`row`被隐藏，返回`true`;否则返回`false`。

### `[override virtual protected] void QListView::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractItemView::mouseMoveEvent`（QMouseEvent *event）。

### `[override virtual protected] void QListView::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractItemView::mouseReleaseEvent`（QMouseEvent *event）。

### `[override virtual protected] QModelIndex QListView::moveCursor(QAbstractItemView::CursorAction cursorAction, Qt::KeyboardModifiers modifiers)`

**作用与语义：**

重实现自：`QAbstractItemView::moveCursor`（QAbstractItemView：：CursorAction cursorAction， Qt：：KeyboardModifiers modifiers）。
返回一个`QModelIndex`对象，指向视图中的下一个对象，基于`modifiers`指定的`cursorAction`和键盘修饰符。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] void QListView::paintEvent(QPaintEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::paintEvent`（QPaintEvent *event）。

### `[protected] QRect QListView::rectForIndex(const QModelIndex &index) const`

**作用与语义：**

返回模型中位置`index`的矩形。矩形位于目录坐标中。

### `[override virtual protected] void QListView::resizeEvent(QResizeEvent *e)`

**作用与语义：**

重实现自：`QAbstractItemView::resizeEvent`（QResizeEvent *event）。

### `[override virtual protected] void QListView::rowsAboutToBeRemoved(const QModelIndex &parent, int start, int end)`

**作用与语义：**

重构：`QAbstractItemView::rowsAboutToBeRemoved`（const QModelIndex & parent， int start， int end）。
当即将移除的行时，会调用该槽位。被删除的行是`parent`从`start`到`end`包含的列。

### `[override virtual protected] void QListView::rowsInserted(const QModelIndex &parent, int start, int end)`

**作用与语义：**

重实现自：`QAbstractItemView::rowsInserted`（const QModelIndex & parent， int start， int end）。
插入行时调用该槽位。新行为`parent`下，从`start`到`end`包含。基类实现调用模型中的fetchMore()以检查更多数据。

### `[override virtual protected] void QListView::scrollContentsBy(int dx, int dy)`

**作用与语义：**

重实现自：`QAbstractScrollArea::scrollContentsBy`（智力 dx，智力 dy）。
按`dx`和`dy`滚动查看内容。
当滚动条被`dx`、`dy`移动时调用该虚拟处理程序，因此应相应地滚动视口内容。
默认实现只需调用整个`viewport()`的`update()`，子类可以重新实现该处理程序以优化，或者像`QScrollArea`一样移动内容控件。参数`dx`和`dy`是为了方便，让类知道应该滚动多少（比如像素位移时很有用）。你也可以忽略这些值，直接滚动到滚动条指示的位置。
调用该函数以进行程序滚动是错误的，建议使用滚动条（例如直接调用`QScrollBar::setValue()`）。

### `[override virtual] void QListView::scrollTo(const QModelIndex &index, QAbstractItemView::ScrollHint hint = EnsureVisible)`

**作用与语义：**

重实现自：`QAbstractItemView::scrollTo`（const QModelIndex & index， QAbstractItemView：：ScrollHint 提示）。
如有必要，滚动视图以确保该物品在`index`可见。视图会尝试根据给定的`hint`定位该物品。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] QModelIndexList QListView::selectedIndexes() const`

**作用与语义：**

重装：`QAbstractItemView::selectedIndexes()` const.
这个便利函数返回视图中所有已选中和非隐藏的项目索引列表。该列表没有重复，也没有排序。

### `[override virtual protected] void QListView::selectionChanged(const QItemSelection &selected, const QItemSelection &deselected)`

**作用与语义：**

重实现自：`QAbstractItemView::selectionChanged`（const QItemSelection &selected， const QItemSelection &deselected）.
当选择发生变化时，该槽函数被调用。之前的选择（可能是空的）由`deselected`指定，新选择由`selected`表示。

### `[protected] void QListView::setPositionForIndex(const QPoint &position, const QModelIndex &index)`

**作用与语义：**

将模型中`index`项的内容位置设置为给定的`position`。如果列表视图的移动模式是静态或视图模式为`ListView`，该函数将无效。

### `[override virtual] void QListView::setRootIndex(const QModelIndex &index)`

**作用与语义：**

重装：`QAbstractItemView::setRootIndex`（const QModelIndex & index）。
将根项设置为给定`index`的项。

### `void QListView::setRowHidden(int row, bool hide)`

**作用与语义：**

如果`hide`为真，给定`row`将被隐藏;否则`row`会被显示出来。

### `[override virtual protected] void QListView::setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags command)`

**作用与语义：**

重实现自：`QAbstractItemView::setSelection`（const QRect &rect， QItemSelectionModel：：SelectionFlags flags）。
将选择`flags`应用于矩形内或被触及的物品，`rect`。
在实现自己的 itemview 时，setSelection 应调用 `selectionModel()`->select（selection， flags），其中 selection 要么是空的 `QModelIndex`，要么是包含所有 `rect` 中的项的 `QItemSelection`。

### `[override virtual protected] void QListView::startDrag(Qt::DropActions supportedActions)`

**作用与语义：**

重实现自：`QAbstractItemView::startDrag`（Qt：:D ropActions supportedActions）。
通过调用 drag->exec() 使用给定的 `supportedActions` 来启动拖拽。

### `[override virtual protected] void QListView::timerEvent(QTimerEvent *e)`

**作用与语义：**

重实现自：`QAbstractItemView::timerEvent`（QTimerEvent *event）。

### `[override virtual protected] void QListView::updateGeometries()`

**作用与语义：**

重装：`QAbstractItemView::updateGeometries()`。
更新视图子控件的几何体。

### `[override virtual protected] int QListView::verticalOffset() const`

**作用与语义：**

重装：`QAbstractItemView::verticalOffset()` const.
返回视图的垂直偏移量。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] QSize QListView::viewportSizeHint() const`

**作用与语义：**

重装：`QAbstractItemView::viewportSizeHint()` const.

### `[override virtual] QRect QListView::visualRect(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemView::visualRect`（const QModelIndex & index） const.
返回该物品在视口上的矩形，该物体在`index`。
如果你的项目显示在多个区域，visualRect 应该返回包含索引的主要区域，而不是索引可能涵盖、触摸或导致绘图的全部区域。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] QRegion QListView::visualRegionForSelection(const QItemSelection &selection) const`

**作用与语义：**

重实现自：`QAbstractItemView::visualRegionForSelection`（const QItemSelection &selection） const.
自4.7版本起，返回区域仅包含与视口相交（或包含）的矩形。
从视口返回给定`selection`中物品的区域。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] void QListView::wheelEvent(QWheelEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::wheelEvent`（QWheelEvent *e）。

### `enum Flow { LeftToRight, TopToBottom }`

**作用与语义：**

- `QListView::LeftToRight`：`0`;物品按视角从左到右排列。
- `QListView::TopToBottom`：`1`;物品从上到下排列成视角。

### `enum Movement { Static, Free, Snap }`

**作用与语义：**

- `QListView::Static`：`0`;用户无法移动这些物品。
- `QListView::Free`：`1`;用户可以自由移动这些物品。
- `QListView::Snap`：`2`;物品移动时会吸附到指定的网格上;详见`setGridSize()`。

### `enum ResizeMode { Fixed, Adjust }`

**作用与语义：**

- `QListView::Fixed`：`0`;这些物品只会在第一次展示视图时摆放。
- `QListView::Adjust`：`1`;每次视角调整时，这些物品都会被排版。

### `enum ViewMode { ListMode, IconMode }`

**作用与语义：**

- `QListView::ListMode`：`0`;物品采用`TopToBottom`流程布局，采用小尺寸和静态移动
- `QListView::IconMode`：`1`;物品采用`LeftToRight`流布局，采用大尺寸和自由移动

### `int batchSize() const`

**作用与语义：**

如果将`layoutMode`设为`Batched`，该属性表示每批中排列的物品数量。
默认值是100。

**如何使用：** 调用 `batchSize()` 读取当前值；它不会修改应用状态。

### `QListView::Flow flow() const`

**作用与语义：**

该属性决定了物品布局应朝向流动。
如果该属性`LeftToRight`，物品将从左到右排列。如果`isWrapping`属性`true`，布局在到达可见区域右侧时会包裹。如果该属性`TopToBottom`，物品将从可见区域顶部展开，达到底部时包裹。
当视图可见时设置该属性，物品会重新排列。
默认情况下，该属性设置为`TopToBottom`。

**如何使用：** 调用 `flow()` 读取当前值；它不会修改应用状态。

### `QSize gridSize() const`

**作用与语义：**

该属性表示布局网格的大小。
该属性是物品摆放所在网格的大小。默认尺寸为空，意味着没有网格，布局也不是在网格中完成的。将该属性设置为非空大小，网格布局会被切换。（当网格布局生效时，`spacing`属性被忽略。）。
当视图可见时设置该属性，物品会重新排列。

**如何使用：** 调用 `gridSize()` 读取当前值；它不会修改应用状态。

### `bool isSelectionRectVisible() const`

**作用与语义：**

如果选择矩形应该是可见的。
如果`true`该属性，则选择矩形是可见的;否则它将被隐藏。
注意：只有当选择模式允许多项选择时，选区矩形才会显示;即如果选区模式为`QAbstractItemView::SingleSelection`，则不会绘制选区矩形。
默认情况下，该属性为`false`。

**如何使用：** 调用 `isSelectionRectVisible()` 读取当前值；它不会修改应用状态。

### `bool isWrapping() const`

**作用与语义：**

该属性决定了物品布局是否应进行包裹。
该属性决定了当可见区域没有更多空间时，布局是否应进行包裹。布局折叠的地点取决于`flow`属性。
当视图可见时设置该属性，物品会重新排列。
默认情况下，该属性是`false`的。

**如何使用：** 调用 `isWrapping()` 读取当前值；它不会修改应用状态。

### `Qt::Alignment itemAlignment() const`

**作用与语义：**

该属性保留了每个单元格中的对齐。
这只在`ListMode`中支持，且`TopToBottom`流且启用包裹。默认对齐为0，意味着项目会完全填满其单元格。

**如何使用：** 调用 `itemAlignment()` 读取当前值；它不会修改应用状态。

### `QListView::LayoutMode layoutMode() const`

**作用与语义：**

决定物品的布局是应立即进行还是延迟。
该属性包含了物品的布局模式。当该模式`SinglePass`（默认）时，物品会一次性摆放好。当该模式`Batched`时，物品会分批`batchSize`件物品摆放，同时处理事件。这使得在其他物品摆放时，可以即时查看和交互可见物品。

**如何使用：** 调用 `layoutMode()` 读取当前值；它不会修改应用状态。

### `int modelColumn() const`

**作用与语义：**

该属性表示模型中可见的列。
默认情况下，该属性包含0，表示模型的第一列将被显示。

**如何使用：** 调用 `modelColumn()` 读取当前值；它不会修改应用状态。

### `QListView::Movement movement() const`

**作用与语义：**

该属性适用于物品是否可以自由移动、被吸附到网格上，还是完全无法移动。
该属性决定了用户如何在视图中移动这些物品。`Static` 表示用户不能移动这些物品。`Free` 意味着用户可以拖拽物品到视图中的任何位置。`Snap` 意味着用户可以拖放物品，但只能拖拽到 `gridSize` 属性所指示的假想网格中的位置。
当视图可见时设置该属性，物品会重新排列。
默认情况下，该属性设为`Static`。

**如何使用：** 调用 `movement()` 读取当前值；它不会修改应用状态。

### `QListView::ResizeMode resizeMode() const`

**作用与语义：**

该属性是否在视图调整时重新布局。
如果该属性被`Adjust`，视图调整大小时项目将重新排列。如果值`Fixed`，视图调整时物品不会被布局。
默认情况下，该属性设置为`Fixed`。

**如何使用：** 调用 `resizeMode()` 读取当前值；它不会修改应用状态。

### `void setBatchSize(int batchSize)`

**作用与语义：**

如果将`layoutMode`设为`Batched`，该属性表示每批中排列的物品数量。
默认值是100。

**如何使用：** 调用 `setBatchSize(...)` 修改 `batchSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFlow(QListView::Flow flow)`

**作用与语义：**

该属性决定了物品布局应朝向流动。
如果该属性`LeftToRight`，物品将从左到右排列。如果`isWrapping`属性`true`，布局在到达可见区域右侧时会包裹。如果该属性`TopToBottom`，物品将从可见区域顶部展开，达到底部时包裹。
当视图可见时设置该属性，物品会重新排列。
默认情况下，该属性设置为`TopToBottom`。

**如何使用：** 调用 `setFlow(...)` 修改 `flow`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setGridSize(const QSize &size)`

**作用与语义：**

该属性表示布局网格的大小。
该属性是物品摆放所在网格的大小。默认尺寸为空，意味着没有网格，布局也不是在网格中完成的。将该属性设置为非空大小，网格布局会被切换。（当网格布局生效时，`spacing`属性被忽略。）。
当视图可见时设置该属性，物品会重新排列。

**如何使用：** 调用 `setGridSize(...)` 修改 `gridSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setItemAlignment(Qt::Alignment alignment)`

**作用与语义：**

该属性保留了每个单元格中的对齐。
这只在`ListMode`中支持，且`TopToBottom`流且启用包裹。默认对齐为0，意味着项目会完全填满其单元格。

**如何使用：** 调用 `setItemAlignment(...)` 修改 `itemAlignment`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLayoutMode(QListView::LayoutMode mode)`

**作用与语义：**

决定物品的布局是应立即进行还是延迟。
该属性包含了物品的布局模式。当该模式`SinglePass`（默认）时，物品会一次性摆放好。当该模式`Batched`时，物品会分批`batchSize`件物品摆放，同时处理事件。这使得在其他物品摆放时，可以即时查看和交互可见物品。

**如何使用：** 调用 `setLayoutMode(...)` 修改 `layoutMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setModelColumn(int column)`

**作用与语义：**

该属性表示模型中可见的列。
默认情况下，该属性包含0，表示模型的第一列将被显示。

**如何使用：** 调用 `setModelColumn(...)` 修改 `modelColumn`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMovement(QListView::Movement movement)`

**作用与语义：**

该属性适用于物品是否可以自由移动、被吸附到网格上，还是完全无法移动。
该属性决定了用户如何在视图中移动这些物品。`Static` 表示用户不能移动这些物品。`Free` 意味着用户可以拖拽物品到视图中的任何位置。`Snap` 意味着用户可以拖放物品，但只能拖拽到 `gridSize` 属性所指示的假想网格中的位置。
当视图可见时设置该属性，物品会重新排列。
默认情况下，该属性设为`Static`。

**如何使用：** 调用 `setMovement(...)` 修改 `movement`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setResizeMode(QListView::ResizeMode mode)`

**作用与语义：**

该属性是否在视图调整时重新布局。
如果该属性被`Adjust`，视图调整大小时项目将重新排列。如果值`Fixed`，视图调整时物品不会被布局。
默认情况下，该属性设置为`Fixed`。

**如何使用：** 调用 `setResizeMode(...)` 修改 `resizeMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSelectionRectVisible(bool show)`

**作用与语义：**

如果选择矩形应该是可见的。
如果`true`该属性，则选择矩形是可见的;否则它将被隐藏。
注意：只有当选择模式允许多项选择时，选区矩形才会显示;即如果选区模式为`QAbstractItemView::SingleSelection`，则不会绘制选区矩形。
默认情况下，该属性为`false`。

**如何使用：** 调用 `setSelectionRectVisible(...)` 修改 `selectionRectVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSpacing(int space)`

**作用与语义：**

该属性保留了布局中物品周围的空间。
该属性是指布局中围绕物品填充的空白空间的大小。
当视图可见时设置该属性，物品会重新排列。
默认情况下，该属性的值为0。

**如何使用：** 调用 `setSpacing(...)` 修改 `spacing`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUniformItemSizes(bool enable)`

**作用与语义：**

该属性确定列表视图中所有项目大小是否相同。
只有当保证视图中所有项目大小相同时，该属性才应设置为 true。这使得视图能够为性能进行一些优化。
默认情况下，该属性为`false`。

**如何使用：** 调用 `setUniformItemSizes(...)` 修改 `uniformItemSizes`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setViewMode(QListView::ViewMode mode)`

**作用与语义：**

该属性表示`QListView`的视模式。
该属性会将其他未设置属性调整为符合集合视图模式。已设置的 `QListView` 特定属性不会被更改，除非调用了 `clearPropertyFlags()`。
设置视图模式会根据所选移动开启或禁用拖放。`ListMode`时，默认移动为`Static`（拖放禁用）;`IconMode`中默认移动为`Free`（启用拖放）。

**如何使用：** 调用 `setViewMode(...)` 修改 `viewMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWordWrap(bool on)`

**作用与语义：**

该属性包含项目文本单词打包策略。
如果该属性`true`，则在词分隔处必要时对条目文本进行装帧;否则则完全不进行装包。该属性默认`false`。
请注意，即使启用了换行，单元格也不会被展开以腾出文本空间。根据视图的 `textElideMode`，对于无法显示的文本，它会打印省略号。

**如何使用：** 调用 `setWordWrap(...)` 修改 `wordWrap`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWrapping(bool enable)`

**作用与语义：**

该属性决定了物品布局是否应进行包裹。
该属性决定了当可见区域没有更多空间时，布局是否应进行包裹。布局折叠的地点取决于`flow`属性。
当视图可见时设置该属性，物品会重新排列。
默认情况下，该属性是`false`的。

**如何使用：** 调用 `setWrapping(...)` 修改 `isWrapping`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int spacing() const`

**作用与语义：**

该属性保留了布局中物品周围的空间。
该属性是指布局中围绕物品填充的空白空间的大小。
当视图可见时设置该属性，物品会重新排列。
默认情况下，该属性的值为0。

**如何使用：** 调用 `spacing()` 读取当前值；它不会修改应用状态。

### `bool uniformItemSizes() const`

**作用与语义：**

该属性确定列表视图中所有项目大小是否相同。
只有当保证视图中所有项目大小相同时，该属性才应设置为 true。这使得视图能够为性能进行一些优化。
默认情况下，该属性为`false`。

**如何使用：** 调用 `uniformItemSizes()` 读取当前值；它不会修改应用状态。

### `QListView::ViewMode viewMode() const`

**作用与语义：**

该属性表示`QListView`的视模式。
该属性会将其他未设置属性调整为符合集合视图模式。已设置的 `QListView` 特定属性不会被更改，除非调用了 `clearPropertyFlags()`。
设置视图模式会根据所选移动开启或禁用拖放。`ListMode`时，默认移动为`Static`（拖放禁用）;`IconMode`中默认移动为`Free`（启用拖放）。

**如何使用：** 调用 `viewMode()` 读取当前值；它不会修改应用状态。

### `bool wordWrap() const`

**作用与语义：**

该属性包含项目文本单词打包策略。
如果该属性`true`，则在词分隔处必要时对条目文本进行装帧;否则则完全不进行装包。该属性默认`false`。
请注意，即使启用了换行，单元格也不会被展开以腾出文本空间。根据视图的 `textElideMode`，对于无法显示的文本，它会打印省略号。

**如何使用：** 调用 `wordWrap()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

### 状态和错误边界

要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

### 线程边界

不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

### 最容易出现的错误

不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QListView` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
