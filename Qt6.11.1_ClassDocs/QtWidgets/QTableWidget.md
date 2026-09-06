# QTableWidget

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QTableWidget` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QTableWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QTableWidget>`
- 继承自：QTableView
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
- `rowCount : int`
- `(since 6.10) supportedDragActions : Qt::DropActions`

### 公有函数

- `QTableWidget(QWidget *parent = nullptr)`
- `QTableWidget(int rows, int columns, QWidget *parent = nullptr)`
- `virtual ~QTableWidget()`
- `QWidget * cellWidget(int row, int column) const`
- `void closePersistentEditor(QTableWidgetItem *item)`
- `int column(const QTableWidgetItem *item) const`
- `int columnCount() const`
- `int currentColumn() const`
- `QTableWidgetItem * currentItem() const`
- `int currentRow() const`
- `void editItem(QTableWidgetItem *item)`
- `QList<QTableWidgetItem *> findItems(const QString &text, Qt::MatchFlags flags) const`
- `QTableWidgetItem * horizontalHeaderItem(int column) const`
- `QModelIndex indexFromItem(const QTableWidgetItem *item) const`
- `bool isPersistentEditorOpen(QTableWidgetItem *item) const`
- `QTableWidgetItem * item(int row, int column) const`
- `QTableWidgetItem * itemAt(const QPoint &point) const`
- `QTableWidgetItem * itemAt(int ax, int ay) const`
- `QTableWidgetItem * itemFromIndex(const QModelIndex &index) const`
- `const QTableWidgetItem * itemPrototype() const`
- `QList<QTableWidgetItem *> items(const QMimeData *data) const`
- `void openPersistentEditor(QTableWidgetItem *item)`
- `void removeCellWidget(int row, int column)`
- `int row(const QTableWidgetItem *item) const`
- `int rowCount() const`
- `QList<QTableWidgetItem *> selectedItems() const`
- `QList<QTableWidgetSelectionRange> selectedRanges() const`
- `void setCellWidget(int row, int column, QWidget *widget)`
- `void setColumnCount(int columns)`
- `void setCurrentCell(int row, int column)`
- `void setCurrentCell(int row, int column, QItemSelectionModel::SelectionFlags command)`
- `void setCurrentItem(QTableWidgetItem *item)`
- `void setCurrentItem(QTableWidgetItem *item, QItemSelectionModel::SelectionFlags command)`
- `void setHorizontalHeaderItem(int column, QTableWidgetItem *item)`
- `void setHorizontalHeaderLabels(const QStringList &labels)`
- `void setItem(int row, int column, QTableWidgetItem *item)`
- `void setItemPrototype(const QTableWidgetItem *item)`
- `void setRangeSelected(const QTableWidgetSelectionRange &range, bool select)`
- `void setRowCount(int rows)`
- `void setSupportedDragActions(Qt::DropActions actions)`
- `void setVerticalHeaderItem(int row, QTableWidgetItem *item)`
- `void setVerticalHeaderLabels(const QStringList &labels)`
- `void sortItems(int column, Qt::SortOrder order = Qt::AscendingOrder)`
- `Qt::DropActions supportedDragActions() const`
- `QTableWidgetItem * takeHorizontalHeaderItem(int column)`
- `QTableWidgetItem * takeItem(int row, int column)`
- `QTableWidgetItem * takeVerticalHeaderItem(int row)`
- `QTableWidgetItem * verticalHeaderItem(int row) const`
- `int visualColumn(int logicalColumn) const`
- `QRect visualItemRect(const QTableWidgetItem *item) const`
- `int visualRow(int logicalRow) const`

### 公有槽函数

- `void clear()`
- `void clearContents()`
- `void insertColumn(int column)`
- `void insertRow(int row)`
- `void removeColumn(int column)`
- `void removeRow(int row)`
- `void scrollToItem(const QTableWidgetItem *item, QAbstractItemView::ScrollHint hint = EnsureVisible)`

### 信号

- `void cellActivated(int row, int column)`
- `void cellChanged(int row, int column)`
- `void cellClicked(int row, int column)`
- `void cellDoubleClicked(int row, int column)`
- `void cellEntered(int row, int column)`
- `void cellPressed(int row, int column)`
- `void currentCellChanged(int currentRow, int currentColumn, int previousRow, int previousColumn)`
- `void currentItemChanged(QTableWidgetItem *current, QTableWidgetItem *previous)`
- `void itemActivated(QTableWidgetItem *item)`
- `void itemChanged(QTableWidgetItem *item)`
- `void itemClicked(QTableWidgetItem *item)`
- `void itemDoubleClicked(QTableWidgetItem *item)`
- `void itemEntered(QTableWidgetItem *item)`
- `void itemPressed(QTableWidgetItem *item)`
- `void itemSelectionChanged()`

### 保护函数

- `virtual bool dropMimeData(int row, int column, const QMimeData *data, Qt::DropAction action)`
- `virtual QMimeData * mimeData(const QList<QTableWidgetItem *> &items) const`
- `virtual QStringList mimeTypes() const`
- `virtual Qt::DropActions supportedDropActions() const`

### 重实现的保护函数

- `virtual void dropEvent(QDropEvent *event) override`
- `virtual bool event(QEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `columnCount : int`

**作用与语义：**

此属性保存表格中的列数。
默认情况下，对于未指定行和列数构造的表格，此属性的值为 0。

**如何使用：** 调用 `columnCount()` 读取当前值；它不会修改应用状态。

### `rowCount : int`

**作用与语义：**

该属性表示表中的行数。
默认情况下，对于没有行和列计数的表，该属性包含 0。

**如何使用：** 调用 `rowCount()` 读取当前值；它不会修改应用状态。

### `[since 6.10] supportedDragActions : Qt::DropActions`

**作用与语义：**

该属性表示了该视图支持的阻力作用。

**如何使用：** 调用 `supportedDragActions()` 读取当前值；它不会修改应用状态。

### `[explicit] QTableWidget::QTableWidget(QWidget *parent = nullptr)`

**作用与语义：**

创建一个新的表格视图，包含给定的`parent`。

### `QTableWidget::QTableWidget(int rows, int columns, QWidget *parent = nullptr)`

**作用与语义：**

创建一个新的表格视图，包含给定的`rows`和`columns`，以及给定的`parent`。

### `[virtual noexcept] QTableWidget::~QTableWidget()`

**作用与语义：**

毁了这个`QTableWidget`。

### `[signal] void QTableWidget::cellActivated(int row, int column)`

**作用与语义：**

当`row`指定的单元被激活时，该信号`column`会发出。

### `[signal] void QTableWidget::cellChanged(int row, int column)`

**作用与语义：**

每当`row`和`column`指定的单元内物品数据发生变化时，就会发出该信号。

### `[signal] void QTableWidget::cellClicked(int row, int column)`

**作用与语义：**

每当点击表中的某个单元格时，该信号都会发出。`row`和`column`即为被点击的单元格。

### `[signal] void QTableWidget::cellDoubleClicked(int row, int column)`

**作用与语义：**

每当双击表中的某个单元格时，都会发出该信号。指定的`row`和`column`就是被双击的单元格。

### `[signal] void QTableWidget::cellEntered(int row, int column)`

**作用与语义：**

当鼠标光标进入一个单元格时，该信号会发出。单元由`row`和`column`指定。
该信号仅在开启鼠标追踪或移动时按下鼠标按钮时发出。

### `[signal] void QTableWidget::cellPressed(int row, int column)`

**作用与语义：**

每当表格中的某个单元被按下时，该信号都会发出。`row`和`column`就是被按下的单元格。

### `QWidget *QTableWidget::cellWidget(int row, int column) const`

**作用与语义：**

返回给定的`row`和`column`中显示在单元格中的控件。
注意：桌面拥有该小部件的所有权。

### `[slot] void QTableWidget::clear()`

**作用与语义：**

移除视图中的所有项目。这也会移除所有选择和头部。如果你不想移除头部，可以用`QTableWidget::clearContents()`。表格尺寸保持不变。

### `[slot] void QTableWidget::clearContents()`

**作用与语义：**

移除视图中所有不在头部的项目。这也会移除所有选择。表格尺寸保持不变。

### `void QTableWidget::closePersistentEditor(QTableWidgetItem *item)`

**作用与语义：**

关闭持久编辑器`item`。

### `int QTableWidget::column(const QTableWidgetItem *item) const`

**作用与语义：**

返回`item`列。

### `int QTableWidget::columnCount() const`

**作用与语义：**

返回列数。
注意：属性 columnCount 的获取函数。

### `[signal] void QTableWidget::currentCellChanged(int currentRow, int currentColumn, int previousRow, int previousColumn)`

**作用与语义：**

每当当前单元发生变化时，该信号都会发出。由`previousRow`和`previousColumn`指定的单元是之前有焦点的单元，由`currentRow`和`currentColumn`指定的单元是新的当前单元。

### `int QTableWidget::currentColumn() const`

**作用与语义：**

返回当前项目的列。

### `QTableWidgetItem *QTableWidget::currentItem() const`

**作用与语义：**

退回当前的商品。

### `[signal] void QTableWidget::currentItemChanged(QTableWidgetItem *current, QTableWidgetItem *previous)`

**作用与语义：**

每当当前物品发生变化时，该信号都会发出。`previous`物品是之前拥有焦点的物品，`current`是新的当前物品。

### `int QTableWidget::currentRow() const`

**作用与语义：**

返回当前项目的行。

### `[override virtual protected] void QTableWidget::dropEvent(QDropEvent *event)`

**作用与语义：**

重实现自：`QTableView::dropEvent`（QDropEvent *event）。

### `[virtual protected] bool QTableWidget::dropMimeData(int row, int column, const QMimeData *data, Qt::DropAction action)`

**作用与语义：**

处理拖放操作提供的`data`，该操作以给定`row`和`column`中给定的`action`结尾。如果数据和动作能被模型处理，返回`true`;否则返回`false`。

### `void QTableWidget::editItem(QTableWidgetItem *item)`

**作用与语义：**

如果`item`可编辑，它会开始编辑。

### `[override virtual protected] bool QTableWidget::event(QEvent *e)`

**作用与语义：**

重装：`QAbstractItemView::event`（QEvent *事件）。

### `QList<QTableWidgetItem *> QTableWidget::findItems(const QString &text, Qt::MatchFlags flags) const`

**作用与语义：**

用给定的`flags`找到与`text`匹配的物品。

### `QTableWidgetItem *QTableWidget::horizontalHeaderItem(int column) const`

**作用与语义：**

如果设置了横向头项，返回列 `column` 的水平头项;否则返回 `nullptr`。

### `QModelIndex QTableWidget::indexFromItem(const QTableWidgetItem *item) const`

**作用与语义：**

返回与给定`item`关联的`QModelIndex`。
注意：在5.10之前的Qt版本中，该函数采用了非`const` `item`。

### `[slot] void QTableWidget::insertColumn(int column)`

**作用与语义：**

在表`column`处插入一个空列。

### `[slot] void QTableWidget::insertRow(int row)`

**作用与语义：**

在`row`处插入一行空行。

### `bool QTableWidget::isPersistentEditorOpen(QTableWidgetItem *item) const`

**作用与语义：**

返回是否开放持久编辑器以进行项`item`。

### `QTableWidgetItem *QTableWidget::item(int row, int column) const`

**作用与语义：**

如果已设置，返回给定`row`和`column`的项目;否则返回`nullptr`。

### `[signal] void QTableWidget::itemActivated(QTableWidgetItem *item)`

**作用与语义：**

当指定`item`被激活时，该信号会发出。

### `QTableWidgetItem *QTableWidget::itemAt(const QPoint &point) const`

**作用与语义：**

返回给定`point`的指针，或者如果`point`未被表控件中的项目覆盖，则返回`nullptr`。

### `QTableWidgetItem *QTableWidget::itemAt(int ax, int ay) const`

**作用与语义：**

返回表格控件坐标系中等价于`QPoint`（`ax`， `ay`）的位置的项目，或者如果指定点未被表格控件中的项目覆盖，则返回`nullptr`。

### `[signal] void QTableWidget::itemChanged(QTableWidgetItem *item)`

**作用与语义：**

每当`item`的数据发生变化时，该信号就会发出。

### `[signal] void QTableWidget::itemClicked(QTableWidgetItem *item)`

**作用与语义：**

每当点击表中的某个项目时，该信号都会发出。指定的`item`是被点击的项目。

### `[signal] void QTableWidget::itemDoubleClicked(QTableWidgetItem *item)`

**作用与语义：**

每当双击表中的某个项目时，都会发出该信号。指定的`item`是被双击的项目。

### `[signal] void QTableWidget::itemEntered(QTableWidgetItem *item)`

**作用与语义：**

当鼠标光标进入某个项目时，会发出该信号。`item`表示被输入的物品。
该信号仅在开启鼠标追踪或移动时按下鼠标按钮时发出。

### `QTableWidgetItem *QTableWidget::itemFromIndex(const QModelIndex &index) const`

**作用与语义：**

返回与给定`index`相关的`QTableWidgetItem`指针。

### `[signal] void QTableWidget::itemPressed(QTableWidgetItem *item)`

**作用与语义：**

每当表格中的某项被按下时，该信号都会发出。指定的`item`是按下的那个项。

### `const QTableWidgetItem *QTableWidget::itemPrototype() const`

**作用与语义：**

返回表格中使用的物品原型。

### `[signal] void QTableWidget::itemSelectionChanged()`

**作用与语义：**

每当选择发生变化时，该信号都会发出。

### `QList<QTableWidgetItem *> QTableWidget::items(const QMimeData *data) const`

**作用与语义：**

返回指向`data`对象中所包含项的指针列表。如果该对象不是在同一进程中由`QTreeWidget`创建的，则该列表为空。

### `[virtual protected] QMimeData *QTableWidget::mimeData(const QList<QTableWidgetItem *> &items) const`

**作用与语义：**

返回包含指定`items`序列化描述的对象。描述这些项的格式来自`mimeTypes()`函数。
如果项目列表为空，则返回`nullptr`而非序列化的空列表。

### `[virtual protected] QStringList QTableWidget::mimeTypes() const`

**作用与语义：**

返回一个MIME类型列表，可用于描述tablewidget项目列表。

### `void QTableWidget::openPersistentEditor(QTableWidgetItem *item)`

**作用与语义：**

打开一个编辑器进行`item`。编辑后编辑器保持开启状态。

### `void QTableWidget::removeCellWidget(int row, int column)`

**作用与语义：**

移除由`row`和`column`指示的单元格上的控件。

### `[slot] void QTableWidget::removeColumn(int column)`

**作用与语义：**

移除`column`列及其所有项目。

### `[slot] void QTableWidget::removeRow(int row)`

**作用与语义：**

移除`row`行及其所有物品。

### `int QTableWidget::row(const QTableWidgetItem *item) const`

**作用与语义：**

还原`item`的排。

### `int QTableWidget::rowCount() const`

**作用与语义：**

返回行数。
注意：属性行计数的获取函数。

### `[slot] void QTableWidget::scrollToItem(const QTableWidgetItem *item, QAbstractItemView::ScrollHint hint = EnsureVisible)`

**作用与语义：**

如有必要，滚动视图以确保`item`可见。`hint`参数更精确地指定操作后 `item` 应位于何处。

### `QList<QTableWidgetItem *> QTableWidget::selectedItems() const`

**作用与语义：**

返回所有选中的物品列表。
该函数返回指向所选单元格内容的指针列表。使用`selectedIndexes()`函数检索包括空单元在内的完整选择。

### `QList<QTableWidgetSelectionRange> QTableWidget::selectedRanges() const`

**作用与语义：**

返回所有选中的范围列表。

### `void QTableWidget::setCellWidget(int row, int column, QWidget *widget)`

**作用与语义：**

将给定`widget`显示在给定`row`和`column`的单元格中，将控件的所有权传递给表。
如果单元控件A被单元控件B替换，单元控件A将被删除。例如，在下面的代码片段中，`QLineEdit`对象将被删除。

**官方示例：**

```cpp
 setCellWidget(row, column, new QLineEdit);
 ...
 setCellWidget(row, column, new QTextEdit);
```

### `void QTableWidget::setColumnCount(int columns)`

**作用与语义：**

此属性保存表格中的列数。
默认情况下，对于未指定行和列数构造的表格，此属性的值为 0。

**如何使用：** 调用 `setColumnCount(...)` 修改 `columnCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QTableWidget::setCurrentCell(int row, int column)`

**作用与语义：**

将当前单元设置为位置为（`row`， `column`）。
根据当前的选择模式，单元也可能被选中。

### `void QTableWidget::setCurrentCell(int row, int column, QItemSelectionModel::SelectionFlags command)`

**作用与语义：**

将当前单元设置为位置为位置（`row`， `column`），使用给定的`command`。

### `void QTableWidget::setCurrentItem(QTableWidgetItem *item)`

**作用与语义：**

将当前项目设置为`item`。
除非选择模式`NoSelection`，否则该物品也会被选中。

### `void QTableWidget::setCurrentItem(QTableWidgetItem *item, QItemSelectionModel::SelectionFlags command)`

**作用与语义：**

将当前项目设置为`item`，使用给定的`command`。

### `void QTableWidget::setHorizontalHeaderItem(int column, QTableWidgetItem *item)`

**作用与语义：**

将第`column`列的水平头项设置为`item`。如有必要，列数增加以适应该项。之前的头部项（如果有的话）被删除。

### `void QTableWidget::setHorizontalHeaderLabels(const QStringList &labels)`

**作用与语义：**

用`labels`设置水平头标签。

### `void QTableWidget::setItem(int row, int column, QTableWidgetItem *item)`

**作用与语义：**

为给定`row`设置物品，`column`为`item`。
桌子会对物品拥有所有权。
注意，如果启用排序（见 `sortingEnabled`），且当前排序列`column`，`row`将被移动到由`item`确定的排序位置。
如果你想设置某一行的多个项目（比如循环调用 setItem()，你可能需要先关闭排序功能，之后再重新开启;这样你就可以对同一行的所有项目使用相同的`row`参数（即 setItem() 不会移动该行）。

### `void QTableWidget::setItemPrototype(const QTableWidgetItem *item)`

**作用与语义：**

将表格的项目原型设置为指定的`item`。
当需要创建新的表项时，表格小部件会使用项目原型克隆函数。例如，当用户在空单元格中编辑时。这在你有一个`QTableWidgetItem`子类并希望确保`QTableWidget`创建你子类实例时非常有用。
桌子拥有原型的所有权。

### `void QTableWidget::setRangeSelected(const QTableWidgetSelectionRange &range, bool select)`

**作用与语义：**

根据`select`选择或取消`range`。

### `void QTableWidget::setRowCount(int rows)`

**作用与语义：**

该属性表示表中的行数。
默认情况下，对于没有行和列计数的表，该属性包含 0。

**如何使用：** 调用 `setRowCount(...)` 修改 `rowCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QTableWidget::setVerticalHeaderItem(int row, QTableWidgetItem *item)`

**作用与语义：**

将第`row`行的垂直头项设置为`item`。

### `void QTableWidget::setVerticalHeaderLabels(const QStringList &labels)`

**作用与语义：**

使用 `labels` 设置垂直头部标签。

### `void QTableWidget::sortItems(int column, Qt::SortOrder order = Qt::AscendingOrder)`

**作用与语义：**

根据`column`和 `order`对表格小部件中的所有行进行排序。

### `[virtual protected] Qt::DropActions QTableWidget::supportedDropActions() const`

**作用与语义：**

返回该视图支持的投放动作。

### `QTableWidgetItem *QTableWidget::takeHorizontalHeaderItem(int column)`

**作用与语义：**

在不删除`column`的情况下，将横向首部项从头部移除。

### `QTableWidgetItem *QTableWidget::takeItem(int row, int column)`

**作用与语义：**

移除`row`的物品，并`column`从桌面上移除，但不会删除它。

### `QTableWidgetItem *QTableWidget::takeVerticalHeaderItem(int row)`

**作用与语义：**

在不删除首部的话，直接移除`row`的垂直头项。

### `QTableWidgetItem *QTableWidget::verticalHeaderItem(int row) const`

**作用与语义：**

返回第`row`行的垂直头项。

### `int QTableWidget::visualColumn(int logicalColumn) const`

**作用与语义：**

返回给定`logicalColumn`的视觉列。

### `QRect QTableWidget::visualItemRect(const QTableWidgetItem *item) const`

**作用与语义：**

返回`item`处物体所在的视口矩形。

### `int QTableWidget::visualRow(int logicalRow) const`

**作用与语义：**

返回给定`logicalRow`的视觉行。

### `void setSupportedDragActions(Qt::DropActions actions)`

**作用与语义：**

该属性表示了该视图支持的阻力作用。

**如何使用：** 调用 `setSupportedDragActions(...)` 修改 `supportedDragActions`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `Qt::DropActions supportedDragActions() const`

**作用与语义：**

该属性表示了该视图支持的阻力作用。

**如何使用：** 调用 `supportedDragActions()` 读取当前值；它不会修改应用状态。

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

`QTableWidget` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
