# QColumnView

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QColumnView` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QColumnView` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QColumnView>`
- 继承自：QAbstractItemView
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `(since 6.11) previewColumnVisible : bool`
- `resizeGripsVisible : bool`

### 公有函数

- `QColumnView(QWidget *parent = nullptr)`
- `virtual ~QColumnView()`
- `QList<int> columnWidths() const`
- `bool isPreviewColumnVisible() const`
- `QWidget * previewWidget() const`
- `bool resizeGripsVisible() const`
- `void setColumnWidths(const QList<int> &list)`
- `void setPreviewColumnVisible(bool visible)`
- `void setPreviewWidget(QWidget *widget)`
- `void setResizeGripsVisible(bool visible)`

### 重实现的公有函数

- `virtual QModelIndex indexAt(const QPoint &point) const override`
- `virtual void scrollTo(const QModelIndex &index, QAbstractItemView::ScrollHint hint = EnsureVisible) override`
- `virtual void selectAll() override`
- `virtual void setModel(QAbstractItemModel *model) override`
- `virtual void setRootIndex(const QModelIndex &index) override`
- `virtual void setSelectionModel(QItemSelectionModel *newSelectionModel) override`
- `virtual QSize sizeHint() const override`
- `virtual QRect visualRect(const QModelIndex &index) const override`

### 信号

- `void updatePreviewWidget(const QModelIndex &index)`

### 保护函数

- `virtual QAbstractItemView * createColumn(const QModelIndex &index)`
- `void initializeColumn(QAbstractItemView *column) const`

### 重实现的保护函数

- `virtual void currentChanged(const QModelIndex &current, const QModelIndex &previous) override`
- `virtual int horizontalOffset() const override`
- `virtual bool isIndexHidden(const QModelIndex &index) const override`
- `virtual QModelIndex moveCursor(QAbstractItemView::CursorAction cursorAction, Qt::KeyboardModifiers modifiers) override`
- `virtual void resizeEvent(QResizeEvent *event) override`
- `virtual void rowsInserted(const QModelIndex &parent, int start, int end) override`
- `virtual void scrollContentsBy(int dx, int dy) override`
- `virtual void setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags command) override`
- `virtual int verticalOffset() const override`
- `virtual QRegion visualRegionForSelection(const QItemSelection &selection) const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.11] previewColumnVisible : bool`

**作用与语义：**

该属性决定预览列是否可见。
默认情况下，`visible` 设置为 true（真）。

**如何使用：** 调用 `previewColumnVisible()` 读取当前值；它不会修改应用状态。

### `resizeGripsVisible : bool`

**作用与语义：**

这个特性可以指定列表视图是否会被调整大小的握持。
默认情况下，`visible` 设置为 true。

**如何使用：** 调用 `resizeGripsVisible()` 读取当前值；它不会修改应用状态。

### `[explicit] QColumnView::QColumnView(QWidget *parent = nullptr)`

**作用与语义：**

构建带有`parent`的列视图以表示模型数据。使用`setModel()`设置模型。

### `[virtual noexcept] QColumnView::~QColumnView()`

**作用与语义：**

破坏了柱状视角。

### `QList<int> QColumnView::columnWidths() const`

**作用与语义：**

返回该视图中所有列的宽度列表。

### `[virtual protected] QAbstractItemView *QColumnView::createColumn(const QModelIndex &index)`

**作用与语义：**

如果要在选择项目时使用自定义控件作为最后一列，请使用该函数并返回控件。`index` 是将被分配给视图的根索引。
返回新视图。`QColumnView`会自动获得该小部件的所有权。

### `[override virtual protected] void QColumnView::currentChanged(const QModelIndex &current, const QModelIndex &previous)`

**作用与语义：**

Reimpations： `QAbstractItemView::currentChanged`（const QModelIndex ¤t， const QModelIndex &previous）.
当新项目变成当前项目时，调用该槽位。之前的当前项目由`previous`索引指定，新项目由`current`索引指定。
如果你想知道物品的变化，请查看`dataChanged()`信号。

### `[override virtual protected] int QColumnView::horizontalOffset() const`

**作用与语义：**

重装：`QAbstractItemView::horizontalOffset()` const.
返回视角的水平偏移。
在基类中，这是一个纯虚拟函数。

### `[override virtual] QModelIndex QColumnView::indexAt(const QPoint &point) const`

**作用与语义：**

重实现自：`QAbstractItemView::indexAt`（const QPoint & point） const.
返回视口坐标处的模型索引`point`。
在基类中，这是一个纯虚拟函数。

### `[protected] void QColumnView::initializeColumn(QAbstractItemView *column) const`

**作用与语义：**

复制列视图的行为和选项，并将其应用到`column`如`iconSize()`、`textElideMode()`和`alternatingRowColors()`上。这在重新实现`createColumn()`时非常有用。

### `[override virtual protected] bool QColumnView::isIndexHidden(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemView::isIndexHidden`（const QModelIndex & index） const.
如果给定`index`所引用的项目隐藏在视图中，返回`true`;否则返回`false`。
隐藏是视图特定的功能。例如`TableView`中可以标记为隐藏列或`TreeView`中的一行。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] QModelIndex QColumnView::moveCursor(QAbstractItemView::CursorAction cursorAction, Qt::KeyboardModifiers modifiers)`

**作用与语义：**

重实现自：`QAbstractItemView::moveCursor`（QAbstractItemView：：CursorAction cursorAction， Qt：：KeyboardModifiers modifiers）。
向左移动应指向父索引，向右移动应指向子索引，若没有子节点则向下移动。
返回一个指向视图中下一个对象的`QModelIndex`对象，基于`modifiers`指定的`cursorAction`和键盘修饰符。
在基类中，这是一个纯虚拟函数。

### `QWidget *QColumnView::previewWidget() const`

**作用与语义：**

返回预览小部件，或者如果没有就返回`nullptr`。

### `[override virtual protected] void QColumnView::resizeEvent(QResizeEvent *event)`

**作用与语义：**

重实现自：`QAbstractItemView::resizeEvent`（QResizeEvent *event）。

### `[override virtual protected] void QColumnView::rowsInserted(const QModelIndex &parent, int start, int end)`

**作用与语义：**

重实现自：`QAbstractItemView::rowsInserted`（const QModelIndex & parent， int start， int end）。
插入行时调用该槽位。新行为`parent`下，从`start`到`end`包含。基类实现调用模型中的fetchMore()以检查更多数据。

### `[override virtual protected] void QColumnView::scrollContentsBy(int dx, int dy)`

**作用与语义：**

重实现自：`QAbstractScrollArea::scrollContentsBy`（智力 dx，智力 dy）。
当滚动条被移动`dx`、`dy`时调用，因此视口内容应相应滚动。
默认实现只需调用整个`viewport()`的`update()`，子类可以重新实现该处理程序以优化，或者像`QScrollArea`一样移动内容控件。参数`dx`和`dy`是为了方便，让类知道应该滚动多少（比如像素移动时很有用）。你也可以忽略这些值，直接滚动到滚动条指示的位置。
调用该函数进行程序滚动是错误，建议使用滚动条（例如直接调用`QScrollBar::setValue()`）。

### `[override virtual] void QColumnView::scrollTo(const QModelIndex &index, QAbstractItemView::ScrollHint hint = EnsureVisible)`

**作用与语义：**

重实现自：`QAbstractItemView::scrollTo`（const QModelIndex & index， QAbstractItemView：：ScrollHint 提示）。
如有必要，滚动视图以确保该物品在`index`可见。视图会尝试根据给定的`hint`定位该物品。
在基类中，这是一个纯虚拟函数。

### `[override virtual] void QColumnView::selectAll()`

**作用与语义：**

重装：`QAbstractItemView::selectAll()`。
选择视图中的所有项目。该函数在选择时会使用视图中的选择行为。

### `void QColumnView::setColumnWidths(const QList<int> &list)`

**作用与语义：**

将列宽设置为`list`中给出的值。列表中多余的值保留并在创建列时使用。
如果列表中值过少，只有其余列的宽度不会被修改。

### `[override virtual] void QColumnView::setModel(QAbstractItemModel *model)`

**作用与语义：**

重实现自：`QAbstractItemView::setModel`（QAbstractItemModel *model）。
将视图的`model`设定为呈现。
该函数将创建并设置新的选择模型，替换之前用`setSelectionModel()`设置的模型。不过，旧的选择模型不会被删除，因为它可能在多个视图之间共享。如果旧的选择模型不再需要，我们建议你删除它。这可以通过以下代码完成：
如果旧模型和旧选择模型都没有父模型，或者它们的父对象是长寿命对象，可能更倾向于调用它们的`deleteLater()`函数来显式删除它们。
视图不会拥有该模型的所有权，除非它是模型的父对象，因为模型可能在多个不同视图之间共享。

### `void QColumnView::setPreviewWidget(QWidget *widget)`

**作用与语义：**

设定了预览的基础`widget`。
该`widget`会成为列视图的子节点，当列区域被删除或设置新控件时，会被销毁。

### `[override virtual] void QColumnView::setRootIndex(const QModelIndex &index)`

**作用与语义：**

重装：`QAbstractItemView::setRootIndex`（const QModelIndex & index）。
将根项设置为给定`index`的项。

### `[override virtual protected] void QColumnView::setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags command)`

**作用与语义：**

重实现自：`QAbstractItemView::setSelection`（const QRect &rect， QItemSelectionModel：：SelectionFlags flags）。
将选择`flags`应用于矩形内或被触及的物品，`rect`。
在实现自己的 itemview 时，setSelection 应调用 `selectionModel()`->select（selection， flags），其中 selection 要么是空的 `QModelIndex`，要么是包含所有 `rect` 中的项的 `QItemSelection`。

### `[override virtual] void QColumnView::setSelectionModel(QItemSelectionModel *newSelectionModel)`

**作用与语义：**

Reimplements： `QAbstractItemView::setSelectionModel`（QItemSelectionModel *selectionModel）.
将当前选择模型设定为给定的`selectionModel`。
注意，如果你在该函数后调用`setModel()`，给定的`selectionModel`将被视图创建的替代。
注意：如果旧的选择模型不再需要，应用程序自行删除;即当它不再被其他视图使用时。当其父对象被删除时，这会自动发生。然而，如果它没有父对象，或者父对象是长期存在的对象，可能更倾向于调用其`deleteLater()`函数显式删除它。

### `[override virtual] QSize QColumnView::sizeHint() const`

**作用与语义：**

重装：`QAbstractScrollArea::sizeHint()` const.

### `[signal] void QColumnView::updatePreviewWidget(const QModelIndex &index)`

**作用与语义：**

当预览小部件需要更新以提供丰富的信息时，会发出该信号`index`。

### `[override virtual protected] int QColumnView::verticalOffset() const`

**作用与语义：**

重装：`QAbstractItemView::verticalOffset()` const.
返回视图的垂直偏移量。
在基类中，这是一个纯虚拟函数。

### `[override virtual] QRect QColumnView::visualRect(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemView::visualRect`（const QModelIndex & index） const.
返回该物品在视口上的矩形，该物体在`index`。
如果你的项目显示在多个区域，visualRect 应该返回包含索引的主要区域，而不是索引可能涵盖、触摸或导致绘图的全部区域。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] QRegion QColumnView::visualRegionForSelection(const QItemSelection &selection) const`

**作用与语义：**

重实现自：`QAbstractItemView::visualRegionForSelection`（const QItemSelection &selection） const.
从视口返回给定`selection`中物品的区域。
在基类中，这是一个纯虚拟函数。

### `bool isPreviewColumnVisible() const`

**作用与语义：**

该属性决定预览列是否可见。
默认情况下，`visible` 设置为 true（真）。

**如何使用：** 调用 `isPreviewColumnVisible()` 读取当前值；它不会修改应用状态。

### `bool resizeGripsVisible() const`

**作用与语义：**

这个特性可以指定列表视图是否会被调整大小的握持。
默认情况下，`visible` 设置为 true。

**如何使用：** 调用 `resizeGripsVisible()` 读取当前值；它不会修改应用状态。

### `void setPreviewColumnVisible(bool visible)`

**作用与语义：**

该属性决定预览列是否可见。
默认情况下，`visible` 设置为 true（真）。

**如何使用：** 调用 `setPreviewColumnVisible(...)` 修改 `previewColumnVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setResizeGripsVisible(bool visible)`

**作用与语义：**

这个特性可以指定列表视图是否会被调整大小的握持。
默认情况下，`visible` 设置为 true。

**如何使用：** 调用 `setResizeGripsVisible(...)` 修改 `resizeGripsVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QColumnView` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
