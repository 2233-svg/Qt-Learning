# QTreeWidget

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QTreeWidget` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QTreeWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QTreeWidget>`
- 继承自：QTreeView
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

- `columnCount : int`
- `(since 6.10) supportedDragActions : Qt::DropActions`
- `topLevelItemCount : int`

### 公有函数

- `QTreeWidget(QWidget *parent = nullptr)`
- `virtual ~QTreeWidget()`
- `void addTopLevelItem(QTreeWidgetItem *item)`
- `void addTopLevelItems(const QList<QTreeWidgetItem *> &items)`
- `void closePersistentEditor(QTreeWidgetItem *item, int column = 0)`
- `int columnCount() const`
- `int currentColumn() const`
- `QTreeWidgetItem * currentItem() const`
- `void editItem(QTreeWidgetItem *item, int column = 0)`
- `QList<QTreeWidgetItem *> findItems(const QString &text, Qt::MatchFlags flags, int column = 0) const`
- `QTreeWidgetItem * headerItem() const`
- `QModelIndex indexFromItem(const QTreeWidgetItem *item, int column = 0) const`
- `int indexOfTopLevelItem(QTreeWidgetItem *item) const`
- `void insertTopLevelItem(int index, QTreeWidgetItem *item)`
- `void insertTopLevelItems(int index, const QList<QTreeWidgetItem *> &items)`
- `QTreeWidgetItem * invisibleRootItem() const`
- `bool isPersistentEditorOpen(QTreeWidgetItem *item, int column = 0) const`
- `QTreeWidgetItem * itemAbove(const QTreeWidgetItem *item) const`
- `QTreeWidgetItem * itemAt(const QPoint &p) const`
- `QTreeWidgetItem * itemAt(int x, int y) const`
- `QTreeWidgetItem * itemBelow(const QTreeWidgetItem *item) const`
- `QTreeWidgetItem * itemFromIndex(const QModelIndex &index) const`
- `QWidget * itemWidget(QTreeWidgetItem *item, int column) const`
- `void openPersistentEditor(QTreeWidgetItem *item, int column = 0)`
- `void removeItemWidget(QTreeWidgetItem *item, int column)`
- `QList<QTreeWidgetItem *> selectedItems() const`
- `void setColumnCount(int columns)`
- `void setCurrentItem(QTreeWidgetItem *item)`
- `void setCurrentItem(QTreeWidgetItem *item, int column)`
- `void setCurrentItem(QTreeWidgetItem *item, int column, QItemSelectionModel::SelectionFlags command)`
- `void setHeaderItem(QTreeWidgetItem *item)`
- `void setHeaderLabel(const QString &label)`
- `void setHeaderLabels(const QStringList &labels)`
- `void setItemWidget(QTreeWidgetItem *item, int column, QWidget *widget)`
- `void setSupportedDragActions(Qt::DropActions actions)`
- `int sortColumn() const`
- `void sortItems(int column, Qt::SortOrder order)`
- `Qt::DropActions supportedDragActions() const`
- `QTreeWidgetItem * takeTopLevelItem(int index)`
- `QTreeWidgetItem * topLevelItem(int index) const`
- `int topLevelItemCount() const`
- `QRect visualItemRect(const QTreeWidgetItem *item) const`

### 重实现的公有函数

- `virtual void setSelectionModel(QItemSelectionModel *selectionModel) override`

### 公有槽函数

- `void clear()`
- `void collapseItem(const QTreeWidgetItem *item)`
- `void expandItem(const QTreeWidgetItem *item)`
- `void scrollToItem(const QTreeWidgetItem *item, QAbstractItemView::ScrollHint hint = EnsureVisible)`

### 信号

- `void currentItemChanged(QTreeWidgetItem *current, QTreeWidgetItem *previous)`
- `void itemActivated(QTreeWidgetItem *item, int column)`
- `void itemChanged(QTreeWidgetItem *item, int column)`
- `void itemClicked(QTreeWidgetItem *item, int column)`
- `void itemCollapsed(QTreeWidgetItem *item)`
- `void itemDoubleClicked(QTreeWidgetItem *item, int column)`
- `void itemEntered(QTreeWidgetItem *item, int column)`
- `void itemExpanded(QTreeWidgetItem *item)`
- `void itemPressed(QTreeWidgetItem *item, int column)`
- `void itemSelectionChanged()`

### 保护函数

- `virtual bool dropMimeData(QTreeWidgetItem *parent, int index, const QMimeData *data, Qt::DropAction action)`
- `virtual QMimeData * mimeData(const QList<QTreeWidgetItem *> &items) const`
- `virtual QStringList mimeTypes() const`
- `virtual Qt::DropActions supportedDropActions() const`

### 重实现的保护函数

- `virtual void dropEvent(QDropEvent *event) override`
- `virtual bool event(QEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `columnCount : int`

**作用与语义：**

此属性保存树控件中显示的列数。
默认情况下，该属性的值为 1。

**如何使用：** 调用 `columnCount()` 读取当前值；它不会修改应用状态。

### `[since 6.10] supportedDragActions : Qt::DropActions`

**作用与语义：**

该属性表示了该视图支持的阻力作用。

**如何使用：** 调用 `supportedDragActions()` 读取当前值；它不会修改应用状态。

### `[read-only] topLevelItemCount : int`

**作用与语义：**

该属性包含顶层项目的数量。
默认情况下，该属性的值为0。

**如何使用：** 调用 `topLevelItemCount()` 读取当前值；它不会修改应用状态。

### `[explicit] QTreeWidget::QTreeWidget(QWidget *parent = nullptr)`

**作用与语义：**

用给定的 `parent`构造树状小部件。

### `[virtual noexcept] QTreeWidget::~QTreeWidget()`

**作用与语义：**

摧毁树小部件及其所有物品。

### `void QTreeWidget::addTopLevelItem(QTreeWidgetItem *item)`

**作用与语义：**

作为控件的顶层项，将`item`附加在小部件中。

### `void QTreeWidget::addTopLevelItems(const QList<QTreeWidgetItem *> &items)`

**作用与语义：**

将`items`列表作为控件的顶层项附加。

### `[slot] void QTreeWidget::clear()`

**作用与语义：**

通过移除树状控件的所有项目和选择来清除树状小部件。
注意：由于每个项目在删除前都会从树小部件中移除，`QTreeWidgetItem::treeWidget()`的返回值在从物品的解构器调用时将无效。

### `void QTreeWidget::closePersistentEditor(QTreeWidgetItem *item, int column = 0)`

**作用与语义：**

关闭给定`column`中`item`的持久编辑器。
如果没有为该项目和列的组合打开持久编辑器，该函数将无效。

### `[slot] void QTreeWidget::collapseItem(const QTreeWidgetItem *item)`

**作用与语义：**

关闭`item`。这会导致包含该物品子节点的树状结构崩溃。

### `int QTreeWidget::currentColumn() const`

**作用与语义：**

返回树状控件中的当前列。

### `QTreeWidgetItem *QTreeWidget::currentItem() const`

**作用与语义：**

返回树状控件中的当前项目。

### `[signal] void QTreeWidget::currentItemChanged(QTreeWidgetItem *current, QTreeWidgetItem *previous)`

**作用与语义：**

当当前项目发生变化时，该信号会发出。当前项目由`current`指定，并取代`previous`当前项目。

### `[override virtual protected] void QTreeWidget::dropEvent(QDropEvent *event)`

**作用与语义：**

重实现自：`QAbstractItemView::dropEvent`（QDropEvent *event）。

### `[virtual protected] bool QTreeWidget::dropMimeData(QTreeWidgetItem *parent, int index, const QMimeData *data, Qt::DropAction action)`

**作用与语义：**

处理通过拖放操作提供的`data`，该操作以给定`parent`项`index`中的给定`action`结尾。
默认实现返回`true`如果成功解码哑剧数据并插入模型;否则返回`false`。

### `void QTreeWidget::editItem(QTreeWidgetItem *item, int column = 0)`

**作用与语义：**

如果`item`可编辑，会开始编辑给定`column`。

### `[override virtual protected] bool QTreeWidget::event(QEvent *e)`

**作用与语义：**

重装：`QAbstractItemView::event`（QEvent *事件）。

### `[slot] void QTreeWidget::expandItem(const QTreeWidgetItem *item)`

**作用与语义：**

扩展`item`。这会导致包含该物品子节点的树被扩展。

### `QList<QTreeWidgetItem *> QTreeWidget::findItems(const QString &text, Qt::MatchFlags flags, int column = 0) const`

**作用与语义：**

返回与给定`text`匹配的物品列表，使用给定`flags`，在给定`column`中返回。

### `QTreeWidgetItem *QTreeWidget::headerItem() const`

**作用与语义：**

返回用于树状小部件头部的项目。

### `QModelIndex QTreeWidget::indexFromItem(const QTreeWidgetItem *item, int column = 0) const`

**作用与语义：**

返回与给定`item`对应的`QModelIndex`，在给定`column`中。
注意：在5.7之前的Qt版本中，该函数采用了非 `const` `item`。

### `int QTreeWidget::indexOfTopLevelItem(QTreeWidgetItem *item) const`

**作用与语义：**

返回给定顶层`item`的索引，若找不到该项则返回-1。

### `void QTreeWidget::insertTopLevelItem(int index, QTreeWidgetItem *item)`

**作用与语义：**

在视图的顶层`index`插入`item`。
如果物品已经入到别处，就不会入。

### `void QTreeWidget::insertTopLevelItems(int index, const QList<QTreeWidgetItem *> &items)`

**作用与语义：**

在视图的顶层插入`index`的`items`列表。
已经插入到别处的项目将不会入。

### `QTreeWidgetItem *QTreeWidget::invisibleRootItem() const`

**作用与语义：**

返回树小部件的不可见根项。
隐形根项通过`QTreeWidgetItem` API访问树小部件的顶层项，使得能够以统一方式处理顶层项及其子项的函数成为可能;例如递归函数。

### `bool QTreeWidget::isPersistentEditorOpen(QTreeWidgetItem *item, int column = 0) const`

**作用与语义：**

返回是否为第`column`列`item`项打开持久编辑器。

### `QTreeWidgetItem *QTreeWidget::itemAbove(const QTreeWidgetItem *item) const`

**作用与语义：**

返回给定`item`上方的物品。

### `[signal] void QTreeWidget::itemActivated(QTreeWidgetItem *item, int column)`

**作用与语义：**

当用户通过单击或双击（取决于平台，即`QStyle::SH_ItemView_ActivateItemOnSingleClick`风格提示）或按特殊按键（例如回车键）激活物品时，会发出该信号。
指定的`item`是被点击的项目，如果没有点击，则`nullptr`。`column`是被点击的物品列，如果没有点击，则为-1。

### `QTreeWidgetItem *QTreeWidget::itemAt(const QPoint &p) const`

**作用与语义：**

返回指向坐标`p`的项目的指针。坐标相对于树控件的`viewport()`。

### `QTreeWidgetItem *QTreeWidget::itemAt(int x, int y) const`

**作用与语义：**

返回指向坐标处的项目的指针（`x`，`y`）。坐标相对于树控件的 `viewport()`。

### `QTreeWidgetItem *QTreeWidget::itemBelow(const QTreeWidgetItem *item) const`

**作用与语义：**

在给定`item`下方以视觉形式返回该物品。

### `[signal] void QTreeWidget::itemChanged(QTreeWidgetItem *item, int column)`

**作用与语义：**

当指定`item`中`column`内容发生变化时，该信号会发出。

### `[signal] void QTreeWidget::itemClicked(QTreeWidgetItem *item, int column)`

**作用与语义：**

当用户点击控件内部时，该信号会发出。
指定的`item`是被点击的项目。`column`是被点击的物品列。如果没有点击物品，则不会发出信号。

### `[signal] void QTreeWidget::itemCollapsed(QTreeWidgetItem *item)`

**作用与语义：**

当指定 `item` 被折叠，使其子不显示时，该信号会发出。
注意：如果调用`collapseAll()`时项的状态发生变化，该信号不会发出。

### `[signal] void QTreeWidget::itemDoubleClicked(QTreeWidgetItem *item, int column)`

**作用与语义：**

当用户在小部件内部双击时，会发出该信号。
指定的`item`是被点击的物品，如果没有点击，则`nullptr`。`column`是被点击的物品列。如果没有双击物品，则不会发出信号。

### `[signal] void QTreeWidget::itemEntered(QTreeWidgetItem *item, int column)`

**作用与语义：**

当鼠标光标进入指定`column`上的`item`时，会发出该信号。`QTreeWidget`鼠标追踪功能需要启用才能使此功能正常工作。

### `[signal] void QTreeWidget::itemExpanded(QTreeWidgetItem *item)`

**作用与语义：**

当指定`item`展开以显示其所有子时，该信号就会发出。

### `QTreeWidgetItem *QTreeWidget::itemFromIndex(const QModelIndex &index) const`

**作用与语义：**

返回指向与给定`index`关联的`QTreeWidgetItem`的指针。

### `[signal] void QTreeWidget::itemPressed(QTreeWidgetItem *item, int column)`

**作用与语义：**

当用户在小部件内按下鼠标按钮时，会发出该信号。
指定的`item`是被点击的项目，如果没有点击，则为`nullptr`。`column`是被点击的物品列，若没有点击，则为-1。

### `[signal] void QTreeWidget::itemSelectionChanged()`

**作用与语义：**

当树控件中的选择发生变化时，会发出该信号。当前选择可以通过`selectedItems()`找到。

### `QWidget *QTreeWidget::itemWidget(QTreeWidgetItem *item, int column) const`

**作用与语义：**

返回`item`指定单元格中显示的小部件和给定`column`。

### `[virtual protected] QMimeData *QTreeWidget::mimeData(const QList<QTreeWidgetItem *> &items) const`

**作用与语义：**

返回包含指定`items`序列化描述的对象。描述这些项的格式来自`mimeTypes()`函数。
如果项目列表为空，则返回`nullptr`而非序列化的空列表。

### `[virtual protected] QStringList QTreeWidget::mimeTypes() const`

**作用与语义：**

返回一个MIME类型的列表，可用于描述树控件项列表。

### `void QTreeWidget::openPersistentEditor(QTreeWidgetItem *item, int column = 0)`

**作用与语义：**

在给定`column`中为`item`打开一个持久编辑器。

### `void QTreeWidget::removeItemWidget(QTreeWidgetItem *item, int column)`

**作用与语义：**

移除给定`item`中给定`column`中的控件集合。

### `[slot] void QTreeWidget::scrollToItem(const QTreeWidgetItem *item, QAbstractItemView::ScrollHint hint = EnsureVisible)`

**作用与语义：**

确保`item`可见，必要时使用指定`hint`滚动视图。

### `QList<QTreeWidgetItem *> QTreeWidget::selectedItems() const`

**作用与语义：**

返回所有被选中的非隐藏项目列表。

### `void QTreeWidget::setCurrentItem(QTreeWidgetItem *item)`

**作用与语义：**

在树控件中设置当前的 `item`。
除非选择模式`NoSelection`，否则该物品也会被选中。

### `void QTreeWidget::setCurrentItem(QTreeWidgetItem *item, int column)`

**作用与语义：**

将树小部件中的当前`item`和当前列设置为`column`。

### `void QTreeWidget::setCurrentItem(QTreeWidgetItem *item, int column, QItemSelectionModel::SelectionFlags command)`

**作用与语义：**

将树小部件中的当前`item`和当前列设置为`column`，使用给定的`command`。

### `void QTreeWidget::setHeaderItem(QTreeWidgetItem *item)`

**作用与语义：**

设置树小部件的头部`item`。头部中每列的标签由项目中对应的标签提供。
树状小部件会对该物品拥有所有权。

### `void QTreeWidget::setHeaderLabel(const QString &label)`

**作用与语义：**

和`setHeaderLabels`（`QStringList`（`label`）一样。

### `void QTreeWidget::setHeaderLabels(const QStringList &labels)`

**作用与语义：**

在`labels`列表中的每个项目在头部添加一列，并为每列设置标签。
注意 setHeaderLabels() 不会移除现有列。

### `void QTreeWidget::setItemWidget(QTreeWidgetItem *item, int column, QWidget *widget)`

**作用与语义：**

将给定`widget`显示在给定`item`和`column`指定的单元格中。
给定`widget`的`autoFillBackground`属性必须设置为 true，否则控件的背景将透明，同时显示模型数据和树控件元素。
该函数仅用于显示静态内容，替代树状控件的元素。如果你想显示自定义动态内容或实现自定义编辑器控件，请使用 S `QTreeView` 和子类 `QStyledItemDelegate`。
在项目层级建立之前，无法调用该函数，即在设置`widget`之前，将持有`widget`的`QTreeWidgetItem`必须先添加到视图中。
注意：树对`widget`所有权。

### `[override virtual] void QTreeWidget::setSelectionModel(QItemSelectionModel *selectionModel)`

**作用与语义：**

为树控件安装 `selectionModel`，使选择状态由该对象管理。它必须关联当前 `QTreeWidget` 使用的模型；替换后旧选择模型不会因这次调用自动删除，共享选择模型时也要自行保证生命周期。

### `int QTreeWidget::sortColumn() const`

**作用与语义：**

返回用于排序控件内容的列。

### `void QTreeWidget::sortItems(int column, Qt::SortOrder order)`

**作用与语义：**

根据指定 `order` 中的 widget 中的物品，按给定`column`中的值排序。

### `[virtual protected] Qt::DropActions QTreeWidget::supportedDropActions() const`

**作用与语义：**

返回该视图支持的投放动作。

### `QTreeWidgetItem *QTreeWidget::takeTopLevelItem(int index)`

**作用与语义：**

移除树中给定`index`的顶层项并返回，否则返回`nullptr`;

### `QTreeWidgetItem *QTreeWidget::topLevelItem(int index) const`

**作用与语义：**

返回给定`index`的顶级物品，若不存在则返回`nullptr`。

### `QRect QTreeWidget::visualItemRect(const QTreeWidgetItem *item) const`

**作用与语义：**

返回`item`处物体所在的视口矩形。

### `int columnCount() const`

**作用与语义：**

此属性保存树控件中显示的列数。
默认情况下，该属性的值为 1。

**如何使用：** 调用 `columnCount()` 读取当前值；它不会修改应用状态。

### `void setColumnCount(int columns)`

**作用与语义：**

此属性保存树控件中显示的列数。
默认情况下，该属性的值为 1。

**如何使用：** 调用 `setColumnCount(...)` 修改 `columnCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSupportedDragActions(Qt::DropActions actions)`

**作用与语义：**

该属性表示了该视图支持的阻力作用。

**如何使用：** 调用 `setSupportedDragActions(...)` 修改 `supportedDragActions`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `Qt::DropActions supportedDragActions() const`

**作用与语义：**

该属性表示了该视图支持的阻力作用。

**如何使用：** 调用 `supportedDragActions()` 读取当前值；它不会修改应用状态。

### `int topLevelItemCount() const`

**作用与语义：**

该属性包含顶层项目的数量。
默认情况下，该属性的值为0。

**如何使用：** 调用 `topLevelItemCount()` 读取当前值；它不会修改应用状态。

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

`QTreeWidget` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
