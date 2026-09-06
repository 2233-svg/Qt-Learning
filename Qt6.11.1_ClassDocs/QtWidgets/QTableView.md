# QTableView

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** 表格模型/视图控件，负责按行列展示模型数据、选择、滚动和编辑。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QTableView`：表格模型/视图控件，负责按行列展示模型数据、选择、滚动和编辑。

**内部模型：** Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

**适用场景：** 创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

## 2. 依赖与对象关系

- 头文件：`#include <QTableView>`
- 继承自：QAbstractItemView
- 直接派生类：QTableWidget

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

- `cornerButtonEnabled : bool`
- `gridStyle : Qt::PenStyle`
- `showGrid : bool`
- `sortingEnabled : bool`
- `wordWrap : bool`

### 公有函数

- `QTableView(QWidget *parent = nullptr)`
- `virtual ~QTableView()`
- `void clearSpans()`
- `int columnAt(int x) const`
- `int columnSpan(int row, int column) const`
- `int columnViewportPosition(int column) const`
- `int columnWidth(int column) const`
- `Qt::PenStyle gridStyle() const`
- `QHeaderView * horizontalHeader() const`
- `bool isColumnHidden(int column) const`
- `bool isCornerButtonEnabled() const`
- `bool isRowHidden(int row) const`
- `bool isSortingEnabled() const`
- `int rowAt(int y) const`
- `int rowHeight(int row) const`
- `int rowSpan(int row, int column) const`
- `int rowViewportPosition(int row) const`
- `void setColumnHidden(int column, bool hide)`
- `void setColumnWidth(int column, int width)`
- `void setCornerButtonEnabled(bool enable)`
- `void setGridStyle(Qt::PenStyle style)`
- `void setHorizontalHeader(QHeaderView *header)`
- `void setRowHeight(int row, int height)`
- `void setRowHidden(int row, bool hide)`
- `void setSortingEnabled(bool enable)`
- `void setSpan(int row, int column, int rowSpanCount, int columnSpanCount)`
- `void setVerticalHeader(QHeaderView *header)`
- `void setWordWrap(bool on)`
- `bool showGrid() const`
- `QHeaderView * verticalHeader() const`
- `bool wordWrap() const`

### 重实现的公有函数

- `virtual QModelIndex indexAt(const QPoint &pos) const override`
- `virtual void scrollTo(const QModelIndex &index, QAbstractItemView::ScrollHint hint = EnsureVisible) override`
- `virtual void setModel(QAbstractItemModel *model) override`
- `virtual void setRootIndex(const QModelIndex &index) override`
- `virtual void setSelectionModel(QItemSelectionModel *selectionModel) override`
- `virtual QRect visualRect(const QModelIndex &index) const override`

### 公有槽函数

- `void hideColumn(int column)`
- `void hideRow(int row)`
- `void resizeColumnToContents(int column)`
- `void resizeColumnsToContents()`
- `void resizeRowToContents(int row)`
- `void resizeRowsToContents()`
- `void selectColumn(int column)`
- `void selectRow(int row)`
- `void setShowGrid(bool show)`
- `void showColumn(int column)`
- `void showRow(int row)`
- `void sortByColumn(int column, Qt::SortOrder order)`

### 重实现的保护函数

- `virtual void currentChanged(const QModelIndex &current, const QModelIndex &previous) override`
- `virtual void dropEvent(QDropEvent *event) override`
- `virtual int horizontalOffset() const override`
- `virtual void initViewItemOption(QStyleOptionViewItem *option) const override`
- `virtual bool isIndexHidden(const QModelIndex &index) const override`
- `virtual QModelIndex moveCursor(QAbstractItemView::CursorAction cursorAction, Qt::KeyboardModifiers modifiers) override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual void scrollContentsBy(int dx, int dy) override`
- `virtual QModelIndexList selectedIndexes() const override`
- `virtual void selectionChanged(const QItemSelection &selected, const QItemSelection &deselected) override`
- `virtual void setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags flags) override`
- `virtual int sizeHintForColumn(int column) const override`
- `virtual int sizeHintForRow(int row) const override`
- `virtual void timerEvent(QTimerEvent *event) override`
- `virtual void updateGeometries() override`
- `virtual int verticalOffset() const override`
- `virtual QSize viewportSizeHint() const override`
- `virtual QRegion visualRegionForSelection(const QItemSelection &selection) const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `cornerButtonEnabled : bool`

**作用与语义：**

该属性决定左上角按钮是否被启用。
如果`true`该属性，则表视图左上角的按钮将被启用。点击该按钮即可选择表视图中的所有单元格。
该属性默认`true`。

**如何使用：** 调用 `cornerButtonEnabled()` 读取当前值；它不会修改应用状态。

### `gridStyle : Qt::PenStyle`

**作用与语义：**

该属性保留了绘制网格的笔式。
该属性表示绘制网格时所使用的样式（见`showGrid`）。

**如何使用：** 调用 `gridStyle()` 读取当前值；它不会修改应用状态。

### `showGrid : bool`

**作用与语义：**

该属性在网格被显示时成立。
如果该属性`true`，则为表绘制网格;如果该属性为`false`，则不绘制网格。默认值为真。

**如何使用：** 调用 `showGrid()` 读取当前值；它不会修改应用状态。

### `sortingEnabled : bool`

**作用与语义：**

该属性是否启用排序。
如果该属性`true`，表的排序是启用的。如果该属性是`false`，则不启用排序。默认值为 false。
注意： 。将属性设置为 true，且 `setSortingEnabled()` 会立即触发调用当前排序部分和顺序的 `sortByColumn()`。

**如何使用：** 调用 `sortingEnabled()` 读取当前值；它不会修改应用状态。

### `wordWrap : bool`

**作用与语义：**

该属性包含项目文本单词打包策略。
如果`true`该属性，则在需要时对项目文本进行装帧;否则则完全不进行装帧。该属性默认`true`。
注意，即使启用了换装，单元格也不会展开以容纳所有文本。省略号将根据当前`textElideMode`插入。

**如何使用：** 调用 `wordWrap()` 读取当前值；它不会修改应用状态。

### `[explicit] QTableView::QTableView(QWidget *parent = nullptr)`

**作用与语义：**

构建带有`parent`表示数据的表格视图。

### `[virtual noexcept] QTableView::~QTableView()`

**作用与语义：**

破坏了桌面视图。

### `void QTableView::clearSpans()`

**作用与语义：**

移除表格视图中的所有行和列跨。

### `int QTableView::columnAt(int x) const`

**作用与语义：**

返回给定的 x-坐标 `x` 在目录坐标所在的列。
注意：如果给定坐标无列，该函数返回-1。

### `[protected slot] void QTableView::columnCountChanged(int oldCount, int newCount)`

**作用与语义：**

每当添加或删除列时，都会调用该槽位。之前的列数由`oldCount`指定，新的列数由`newCount`决定。

### `[protected slot] void QTableView::columnMoved(int column, int oldIndex, int newIndex)`

**作用与语义：**

调用该槽位以更改表格视图中给定`column`的索引。旧索引由`oldIndex`指定，新索引由`newIndex`表示。

### `[protected slot] void QTableView::columnResized(int column, int oldWidth, int newWidth)`

**作用与语义：**

该槽用于更改给定`column`的宽度。旧宽度由`oldWidth`指定，新宽度由`newWidth`表示。

### `int QTableView::columnSpan(int row, int column) const`

**作用与语义：**

返回表元素在（`row`， `column`）处的列张成。默认值为1。

### `int QTableView::columnViewportPosition(int column) const`

**作用与语义：**

返回给定`column`的 x-坐标，包含内容坐标。

### `int QTableView::columnWidth(int column) const`

**作用与语义：**

返回给定`column`的宽度。

### `[override virtual protected] void QTableView::currentChanged(const QModelIndex &current, const QModelIndex &previous)`

**作用与语义：**

Reimpations： `QAbstractItemView::currentChanged`（const QModelIndex ¤t， const QModelIndex &previous）.
当新项目变成当前项目时，调用该槽位。之前的当前项目由`previous`索引指定，新项目由`current`索引指定。
如果你想知道物品的变化，请查看`dataChanged()`信号。

### `[override virtual protected] void QTableView::dropEvent(QDropEvent *event)`

**作用与语义：**

重实现自：`QAbstractItemView::dropEvent`（QDropEvent *event）。

### `[slot] void QTableView::hideColumn(int column)`

**作用与语义：**

隐藏给定的`column`。

### `[slot] void QTableView::hideRow(int row)`

**作用与语义：**

隐藏给定的`row`。

### `QHeaderView *QTableView::horizontalHeader() const`

**作用与语义：**

返回表视图的横向头部。

### `[override virtual protected] int QTableView::horizontalOffset() const`

**作用与语义：**

重装：`QAbstractItemView::horizontalOffset()` const.
返回表格视图中项目的水平偏移量。
请注意，表格视图使用水平头部部分位置来确定视图中列的位置。
返回视角的水平偏移。
在基类中，这是一个纯虚拟函数。

### `[override virtual] QModelIndex QTableView::indexAt(const QPoint &pos) const`

**作用与语义：**

重装：`QAbstractItemView::indexAt`（const QPoint & point）const.
返回模型项的索引位置，对应于目录坐标中位置`pos`的表项。
返回视口坐标处的模型索引`point`。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] void QTableView::initViewItemOption(QStyleOptionViewItem *option) const`

**作用与语义：**

Reimplements： `QAbstractItemView::initViewItemOption`（QStyleOptionViewItem *option） const.
用视图的调色板、字体、状态、对齐等初始化`option`结构。
注意：该方法的实现应检查接收结构的 `version`，填充实现熟悉的所有成员，并将版本成员设置为实现支持的版本，然后返回。

### `bool QTableView::isColumnHidden(int column) const`

**作用与语义：**

如果给定`column`隐藏，返回`true`;否则返回`false`。

### `[override virtual protected] bool QTableView::isIndexHidden(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemView::isIndexHidden`（const QModelIndex & index） const.
如果给定`index`所引用的项目隐藏在视图中，返回`true`;否则返回`false`。
隐藏是视图特定的功能。例如`TableView`中可以标记为隐藏列或`TreeView`中的一行。
在基类中，这是一个纯虚拟函数。

### `bool QTableView::isRowHidden(int row) const`

**作用与语义：**

如果给定`row`隐藏，返回`true`;否则返回`false`。

### `[override virtual protected] QModelIndex QTableView::moveCursor(QAbstractItemView::CursorAction cursorAction, Qt::KeyboardModifiers modifiers)`

**作用与语义：**

重实现自：`QAbstractItemView::moveCursor`（QAbstractItemView：：CursorAction cursorAction， Qt：：KeyboardModifiers modifiers）。
根据给定的`cursorAction`，利用`modifiers`提供的信息移动光标。
返回一个`QModelIndex`对象，指向视图中的下一个对象，基于`modifiers`指定的`cursorAction`和键盘修饰符。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] void QTableView::paintEvent(QPaintEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::paintEvent`（QPaintEvent *event）。
收到给定的涂装事件`event`后涂装桌面。

### `[slot] void QTableView::resizeColumnToContents(int column)`

**作用与语义：**

根据代表用来渲染每个项目的大小提示，调整给定`column`大小。
注意：只有可见列的大小会被调整。重新实现`sizeHintForColumn()`以调整隐藏列的大小。

### `[slot] void QTableView::resizeColumnsToContents()`

**作用与语义：**

根据代表在渲染每个列中项目时的大小提示，调整所有列的大小。

### `[slot] void QTableView::resizeRowToContents(int row)`

**作用与语义：**

根据代表用来渲染每条物品的大小提示，调整给定`row`的大小。

### `[slot] void QTableView::resizeRowsToContents()`

**作用与语义：**

根据用来渲染每行物品的代理大小提示，调整所有行的大小。

### `int QTableView::rowAt(int y) const`

**作用与语义：**

返回给定 y 坐标 `y` in contents 坐标所在的行。
注意：如果给定坐标无效（无行），该函数返回-1。

### `[protected slot] void QTableView::rowCountChanged(int oldCount, int newCount)`

**作用与语义：**

每当添加或删除行时调用该槽位。之前的行数由`oldCount`指定，新的行数由`newCount`决定。

### `int QTableView::rowHeight(int row) const`

**作用与语义：**

返回给定`row`的高度。

### `[protected slot] void QTableView::rowMoved(int row, int oldIndex, int newIndex)`

**作用与语义：**

调用该槽位以更改表格视图中给定`row`的索引。旧索引由`oldIndex`指定，新索引由`newIndex`指定。

### `[protected slot] void QTableView::rowResized(int row, int oldHeight, int newHeight)`

**作用与语义：**

该槽位用于改变给定`row`的高度。旧高度由`oldHeight`指定，新高度由`newHeight`表示。

### `int QTableView::rowSpan(int row, int column) const`

**作用与语义：**

返回表元素在（`row`， `column`）处的行张成。默认值为1。

### `int QTableView::rowViewportPosition(int row) const`

**作用与语义：**

返回给定`row`的 y 坐标，包含内容坐标。

### `[override virtual protected] void QTableView::scrollContentsBy(int dx, int dy)`

**作用与语义：**

重实现自：`QAbstractScrollArea::scrollContentsBy`（智力 dx， int dy）。
将表格视图内容滚动到（`dx`，`dy`）。
当滚动条被`dx`、`dy`移动时调用了这个虚拟处理程序，因此应相应地滚动视口内容。
默认实现会调用整个`viewport()`的`update()`，子类可以重新实现该处理程序以优化，或者像`QScrollArea`一样移动内容组件。参数`dx`和`dy`是为了方便，让类知道应该滚动多少（比如像素移动时很有用）。你也可以忽略这些值，直接滚动到滚动条指示的位置。
调用该函数以进行程序滚动是错误的，建议使用滚动条（例如直接调用`QScrollBar::setValue()`）。

### `[override virtual] void QTableView::scrollTo(const QModelIndex &index, QAbstractItemView::ScrollHint hint = EnsureVisible)`

**作用与语义：**

重实现自：`QAbstractItemView::scrollTo`（const QModelIndex & index， QAbstractItemView：：ScrollHint 提示）。
确保给定`index`在表格视图中可见，必要时滚动。
如有需要，滚动视图以确保`index`的物品可见。视图会根据给定的`hint`尝试定位该物品。
在基类中，这是一个纯虚拟函数。

### `[slot] void QTableView::selectColumn(int column)`

**作用与语义：**

如果当前的 SelectionMode 和 SelectionBehavior 允许选择列，则在表格视图中选择给定的`column`。

### `[slot] void QTableView::selectRow(int row)`

**作用与语义：**

如果当前的 SelectionMode 和 SelectionBehavior 允许选择行，则在表格视图中选择给定的`row`。

### `[override virtual protected] QModelIndexList QTableView::selectedIndexes() const`

**作用与语义：**

重装：`QAbstractItemView::selectedIndexes()` const.
这个便利函数返回视图中所有已选中和非隐藏的项目索引列表。该列表没有重复，也没有排序。

### `[override virtual protected] void QTableView::selectionChanged(const QItemSelection &selected, const QItemSelection &deselected)`

**作用与语义：**

重实现自：`QAbstractItemView::selectionChanged`（const QItemSelection &selected， const QItemSelection &deselected）.
当选择发生变化时，该槽函数被调用。之前的选择（可能是空的）由`deselected`指定，新选择由`selected`表示。

### `void QTableView::setColumnHidden(int column, bool hide)`

**作用与语义：**

如果`hide`为真，给定`column`将被隐藏;否则会显示。

### `void QTableView::setColumnWidth(int column, int width)`

**作用与语义：**

将给定`column`的宽度设为`width`。

### `void QTableView::setHorizontalHeader(QHeaderView *header)`

**作用与语义：**

将用于水平头部的小部件设置为`header`。

### `[override virtual] void QTableView::setModel(QAbstractItemModel *model)`

**作用与语义：**

重实现自：`QAbstractItemView::setModel`（QAbstractItemModel *model）。
将视图的`model`设定为呈现。
该函数将创建并设置新的选择模型，替换之前用`setSelectionModel()`设置的模型。不过，旧的选择模型不会被删除，因为它可能在多个视图之间共享。如果旧的选择模型不再需要，我们建议你删除它。这可以通过以下代码完成：
如果旧模型和旧选择模型都没有父模型，或者它们的父对象是长寿命对象，可能更倾向于调用它们的`deleteLater()`函数来显式删除它们。
视图不会拥有该模型的所有权，除非它是模型的父对象，因为模型可能在多个不同视图之间共享。

### `[override virtual] void QTableView::setRootIndex(const QModelIndex &index)`

**作用与语义：**

重装：`QAbstractItemView::setRootIndex`（const QModelIndex & index）。
将根项设置为给定`index`的项。

### `void QTableView::setRowHeight(int row, int height)`

**作用与语义：**

将给定`row`的高度设置为`height`。

### `void QTableView::setRowHidden(int row, bool hide)`

**作用与语义：**

如果`hide`是真的，`row`会被隐藏，否则会被显示出来。

### `[override virtual protected] void QTableView::setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags flags)`

**作用与语义：**

重实现自：`QAbstractItemView::setSelection`（const QRect &rect， QItemSelectionModel：：SelectionFlags flags）。
根据指定`rect`并根据指定的选择`flags`选择项目。
对矩形内或被触及的物品应用选择`flags`，`rect`。
在实现自己的 itemview 时，setSelection 应调用 `selectionModel()`->select（selection， flags），其中 selection 要么是空的 `QModelIndex`，要么是包含所有 `rect` 中元素的 `QItemSelection`。

### `[override virtual] void QTableView::setSelectionModel(QItemSelectionModel *selectionModel)`

**作用与语义：**

Reimplements： `QAbstractItemView::setSelectionModel`（QItemSelectionModel *selectionModel）.
将当前选择模型设定为给定的`selectionModel`。
注意，如果你在该函数后调用`setModel()`，给定的`selectionModel`将被视图创建的替代。
注意：如果旧的选择模型不再需要，应用程序自行删除;即当它不再被其他视图使用时。当其父对象被删除时，这会自动发生。然而，如果它没有父对象，或者父对象是长期存在的对象，可能更倾向于调用其`deleteLater()`函数显式删除它。

### `void QTableView::setSortingEnabled(bool enable)`

**作用与语义：**

该属性是否启用排序。
如果该属性`true`，表的排序是启用的。如果该属性是`false`，则不启用排序。默认值为 false。
注意： 。将属性设置为 true，且 `setSortingEnabled()` 会立即触发调用当前排序部分和顺序的 `sortByColumn()`。

**如何使用：** 调用 `setSortingEnabled(...)` 修改 `sortingEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QTableView::setSpan(int row, int column, int rowSpanCount, int columnSpanCount)`

**作用与语义：**

将表元素在（`row`， `column`）的张成设置为由（`rowSpanCount`， `columnSpanCount`）指定的行和列数。

### `void QTableView::setVerticalHeader(QHeaderView *header)`

**作用与语义：**

将垂直头部的控件设置为`header`。

### `[slot] void QTableView::showColumn(int column)`

**作用与语义：**

展示给出的`column`。

### `[slot] void QTableView::showRow(int row)`

**作用与语义：**

展示给出的给定`row`。

### `[override virtual protected] int QTableView::sizeHintForColumn(int column) const`

**作用与语义：**

重实现自：`QAbstractItemView::sizeHintForColumn`（int column） const.
返回给定`column`宽度的尺寸提示，若无模型则返回-1。
如果你需要将某列的宽度设置为固定值，可以在表的横向页头调用`QHeaderView::resizeSection()`。
如果你在子类中重新实现该函数，请注意调用 `resizeColumnToContents()` 或 `QHeaderView::resizeSections()` 时，你返回的值将被使用。如果水平头部或项目代理需要更大的列宽，则会使用较宽的列。
返回指定`column`的宽度尺寸提示，若无模型则返回-1。
该函数用于带有水平头部的视图，根据给定`column`的内容查找头部部分的大小提示。

### `[override virtual protected] int QTableView::sizeHintForRow(int row) const`

**作用与语义：**

重实现自：`QAbstractItemView::sizeHintForRow`（int row） const.
返回给定`row`高度的尺寸提示，若无模型则返回-1。
如果你需要将某行的高度设置为固定值，可以在表的垂直首部调用`QHeaderView::resizeSection()`。
如果你在子类中重新实现这个函数，注意你返回的值只有在调用 `resizeRowToContents()` 时才会被使用。在这种情况下，如果垂直头部或项目代理需要更大的行高，则会使用该宽度。
返回指定`row`的高度尺寸提示，若无模型则返回-1。
返回的高度是根据给定`row`项的大小提示计算的，也就是返回的值是所有项中的最大高度。注意，要控制行的高度，必须重新实现`QAbstractItemDelegate::sizeHint()`函数。
该函数用于带有垂直头部的视图，根据给定`row`的内容查找头部部分的大小提示。

### `[slot] void QTableView::sortByColumn(int column, Qt::SortOrder order)`

**作用与语义：**

根据给定`column`和`order`的值对模型进行排序。
`column`可能为-1，此时不会显示排序指示器，模型会恢复到自然的未排序顺序。注意，并非所有模型都支持此功能，这种情况下甚至可能崩溃。

### `[override virtual protected] void QTableView::timerEvent(QTimerEvent *event)`

**作用与语义：**

重实现自：`QAbstractItemView::timerEvent`（QTimerEvent *event）。

### `[override virtual protected] void QTableView::updateGeometries()`

**作用与语义：**

重装：`QAbstractItemView::updateGeometries()`。
更新视图子控件的几何体。

### `QHeaderView *QTableView::verticalHeader() const`

**作用与语义：**

返回表视图的垂直头部。

### `[override virtual protected] int QTableView::verticalOffset() const`

**作用与语义：**

重装：`QAbstractItemView::verticalOffset()` const.
返回表格视图中项目的垂直偏移量。
注意，表格视图使用垂直头部部分位置来确定视图中行的位置。
返回视图的垂直偏移量。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] QSize QTableView::viewportSizeHint() const`

**作用与语义：**

重装：`QAbstractItemView::viewportSizeHint()` const.

### `[override virtual] QRect QTableView::visualRect(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemView::visualRect`（const QModelIndex & index） const.
返回视口上被指定`index`占据的矩形。如果索引在视图中隐藏，则返回空`QRect`。
返回该物品在视口中所在的矩形`index`。
如果你的项目显示在多个区域，visualRect 应该返回包含索引的主要区域，而不是索引可能涵盖、触摸或导致绘图的全部区域。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] QRegion QTableView::visualRegionForSelection(const QItemSelection &selection) const`

**作用与语义：**

重装：`QAbstractItemView::visualRegionForSelection`（const QItemSelection &selection） const.
返回该`selection`中物品的视口矩形。
自4.7版本起，返回区域仅包含与视口相交（或包含）的矩形。
从视口返回给定`selection`中物品的区域。
在基类中，这是一个纯虚拟函数。

### `Qt::PenStyle gridStyle() const`

**作用与语义：**

该属性保留了绘制网格的笔式。
该属性表示绘制网格时所使用的样式（见`showGrid`）。

**如何使用：** 调用 `gridStyle()` 读取当前值；它不会修改应用状态。

### `bool isCornerButtonEnabled() const`

**作用与语义：**

该属性决定左上角按钮是否被启用。
如果`true`该属性，则表视图左上角的按钮将被启用。点击该按钮即可选择表视图中的所有单元格。
该属性默认`true`。

**如何使用：** 调用 `isCornerButtonEnabled()` 读取当前值；它不会修改应用状态。

### `bool isSortingEnabled() const`

**作用与语义：**

该属性是否启用排序。
如果该属性`true`，表的排序是启用的。如果该属性是`false`，则不启用排序。默认值为 false。
注意： 。将属性设置为 true，且 `setSortingEnabled()` 会立即触发调用当前排序部分和顺序的 `sortByColumn()`。

**如何使用：** 调用 `isSortingEnabled()` 读取当前值；它不会修改应用状态。

### `void setCornerButtonEnabled(bool enable)`

**作用与语义：**

该属性决定左上角按钮是否被启用。
如果`true`该属性，则表视图左上角的按钮将被启用。点击该按钮即可选择表视图中的所有单元格。
该属性默认`true`。

**如何使用：** 调用 `setCornerButtonEnabled(...)` 修改 `cornerButtonEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setGridStyle(Qt::PenStyle style)`

**作用与语义：**

该属性保留了绘制网格的笔式。
该属性表示绘制网格时所使用的样式（见`showGrid`）。

**如何使用：** 调用 `setGridStyle(...)` 修改 `gridStyle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWordWrap(bool on)`

**作用与语义：**

该属性包含项目文本单词打包策略。
如果`true`该属性，则在需要时对项目文本进行装帧;否则则完全不进行装帧。该属性默认`true`。
注意，即使启用了换装，单元格也不会展开以容纳所有文本。省略号将根据当前`textElideMode`插入。

**如何使用：** 调用 `setWordWrap(...)` 修改 `wordWrap`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool showGrid() const`

**作用与语义：**

该属性在网格被显示时成立。
如果该属性`true`，则为表绘制网格;如果该属性为`false`，则不绘制网格。默认值为真。

**如何使用：** 调用 `showGrid()` 读取当前值；它不会修改应用状态。

### `bool wordWrap() const`

**作用与语义：**

该属性包含项目文本单词打包策略。
如果`true`该属性，则在需要时对项目文本进行装帧;否则则完全不进行装帧。该属性默认`true`。
注意，即使启用了换装，单元格也不会展开以容纳所有文本。省略号将根据当前`textElideMode`插入。

**如何使用：** 调用 `wordWrap()` 读取当前值；它不会修改应用状态。

### `void setShowGrid(bool show)`

**作用与语义：**

该属性在网格被显示时成立。
如果该属性`true`，则为表绘制网格;如果该属性为`false`，则不绘制网格。默认值为真。

**如何使用：** 调用 `setShowGrid(...)` 修改 `showGrid`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QTableView` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
