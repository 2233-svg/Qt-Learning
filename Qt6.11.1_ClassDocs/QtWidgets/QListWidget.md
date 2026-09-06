# QListWidget

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QListWidget` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QListWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QListWidget>`
- 继承自：QListView
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

**生命周期：** 容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

**状态与结果：** 要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

**线程与事件循环：** 不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

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

### 属性

- `count : int`
- `currentRow : int`
- `sortingEnabled : bool`
- `(since 6.10) supportedDragActions : Qt::DropActions`

### 公有函数

- `QListWidget(QWidget *parent = nullptr)`
- `virtual ~QListWidget()`
- `void addItem(QListWidgetItem *item)`
- `void addItem(const QString &label)`
- `void addItems(const QStringList &labels)`
- `void closePersistentEditor(QListWidgetItem *item)`
- `int count() const`
- `QListWidgetItem * currentItem() const`
- `int currentRow() const`
- `void editItem(QListWidgetItem *item)`
- `QList<QListWidgetItem *> findItems(const QString &text, Qt::MatchFlags flags) const`
- `QModelIndex indexFromItem(const QListWidgetItem *item) const`
- `void insertItem(int row, QListWidgetItem *item)`
- `void insertItem(int row, const QString &label)`
- `void insertItems(int row, const QStringList &labels)`
- `bool isPersistentEditorOpen(QListWidgetItem *item) const`
- `bool isSortingEnabled() const`
- `QListWidgetItem * item(int row) const`
- `QListWidgetItem * itemAt(const QPoint &p) const`
- `QListWidgetItem * itemAt(int x, int y) const`
- `QListWidgetItem * itemFromIndex(const QModelIndex &index) const`
- `QWidget * itemWidget(QListWidgetItem *item) const`
- `QList<QListWidgetItem *> items(const QMimeData *data) const`
- `void openPersistentEditor(QListWidgetItem *item)`
- `void removeItemWidget(QListWidgetItem *item)`
- `int row(const QListWidgetItem *item) const`
- `QList<QListWidgetItem *> selectedItems() const`
- `void setCurrentItem(QListWidgetItem *item)`
- `void setCurrentItem(QListWidgetItem *item, QItemSelectionModel::SelectionFlags command)`
- `void setCurrentRow(int row)`
- `void setCurrentRow(int row, QItemSelectionModel::SelectionFlags command)`
- `void setItemWidget(QListWidgetItem *item, QWidget *widget)`
- `void setSortingEnabled(bool enable)`
- `void setSupportedDragActions(Qt::DropActions actions)`
- `void sortItems(Qt::SortOrder order = Qt::AscendingOrder)`
- `Qt::DropActions supportedDragActions() const`
- `QListWidgetItem * takeItem(int row)`
- `QRect visualItemRect(const QListWidgetItem *item) const`

### 重实现的公有函数

- `virtual void setSelectionModel(QItemSelectionModel *selectionModel) override`

### 公有槽函数

- `void clear()`
- `void scrollToItem(const QListWidgetItem *item, QAbstractItemView::ScrollHint hint = EnsureVisible)`

### 信号

- `void currentItemChanged(QListWidgetItem *current, QListWidgetItem *previous)`
- `void currentRowChanged(int currentRow)`
- `void currentTextChanged(const QString &currentText)`
- `void itemActivated(QListWidgetItem *item)`
- `void itemChanged(QListWidgetItem *item)`
- `void itemClicked(QListWidgetItem *item)`
- `void itemDoubleClicked(QListWidgetItem *item)`
- `void itemEntered(QListWidgetItem *item)`
- `void itemPressed(QListWidgetItem *item)`
- `void itemSelectionChanged()`

### 保护函数

- `virtual bool dropMimeData(int index, const QMimeData *data, Qt::DropAction action)`
- `virtual QMimeData * mimeData(const QList<QListWidgetItem *> &items) const`
- `virtual QStringList mimeTypes() const`
- `virtual Qt::DropActions supportedDropActions() const`

### 重实现的保护函数

- `virtual void dropEvent(QDropEvent *event) override`
- `virtual bool event(QEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only] count : int`

**作用与语义：**

此属性保存列表中项目的数量，包括任何隐藏的项目。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `currentRow : int`

**作用与语义：**

该属性包含当前项目的行。
根据当前的选择模式，也可以选择该行。

**如何使用：** 调用 `currentRow()` 读取当前值；它不会修改应用状态。

### `sortingEnabled : bool`

**作用与语义：**

该属性是否启用排序。
如果该属性为`true`，则对列表进行排序;如果该属性为假，则不启用排序。
默认值为假。

**如何使用：** 调用 `sortingEnabled()` 读取当前值；它不会修改应用状态。

### `[since 6.10] supportedDragActions : Qt::DropActions`

**作用与语义：**

该属性表示了该视图支持的阻力作用。

**如何使用：** 调用 `supportedDragActions()` 读取当前值；它不会修改应用状态。

### `[explicit] QListWidget::QListWidget(QWidget *parent = nullptr)`

**作用与语义：**

构造一个空的QListWidget，包含给定的`parent`。

### `[virtual noexcept] QListWidget::~QListWidget()`

**作用与语义：**

销毁列表控件及其所有项目。

### `void QListWidget::addItem(QListWidgetItem *item)`

**作用与语义：**

在列表小部件末尾插入`item`。
警告：一个`QListWidgetItem`只能添加到一个`QListWidget`一次。在同一`QListWidget`中多次添加相同的`QListWidgetItem`会导致行为不明确。

### `void QListWidget::addItem(const QString &label)`

**作用与语义：**

在列表小部件末尾插入带有文本`label`的项目。

### `void QListWidget::addItems(const QStringList &labels)`

**作用与语义：**

插入列表中控件末尾带有文本`labels`的项目。

### `[slot] void QListWidget::clear()`

**作用与语义：**

移除视图中的所有物品和选项。
警告：所有内容将被永久删除。

### `void QListWidget::closePersistentEditor(QListWidgetItem *item)`

**作用与语义：**

关闭给定`item`的持久编辑器。

### `QListWidgetItem *QListWidget::currentItem() const`

**作用与语义：**

退回当前的商品。

### `[signal] void QListWidget::currentItemChanged(QListWidgetItem *current, QListWidgetItem *previous)`

**作用与语义：**

每当当前项目发生变化时，该信号都会发出。
`previous`是之前拥有焦点的物品;`current`是新的当前物品。

### `[signal] void QListWidget::currentRowChanged(int currentRow)`

**作用与语义：**

该属性包含当前项目的行。
根据当前的选择模式，也可以选择该行。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentRow` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QListWidget::currentTextChanged(const QString &currentText)`

**作用与语义：**

每当当前项目发生变化时，该信号都会发出。
`currentText` 是当前项中的文本数据。如果没有当前项，`currentText`无效。

### `[override virtual protected] void QListWidget::dropEvent(QDropEvent *event)`

**作用与语义：**

重实现自：`QListView::dropEvent`（QDropEvent *事件）。

### `[virtual protected] bool QListWidget::dropMimeData(int index, const QMimeData *data, Qt::DropAction action)`

**作用与语义：**

手柄`data`外部拖放操作提供，该操作以给定`index`中的`action`结束。如果模型能处理`data`和`action`，则返回`true`;否则返回`false`。

### `void QListWidget::editItem(QListWidgetItem *item)`

**作用与语义：**

如果`item`可编辑，它会开始编辑。

### `[override virtual protected] bool QListWidget::event(QEvent *e)`

**作用与语义：**

重装：`QListView::event`（QEvent *e）。

### `QList<QListWidgetItem *> QListWidget::findItems(const QString &text, Qt::MatchFlags flags) const`

**作用与语义：**

使用给定`flags`寻找与字符串相符文本的物品`text`。

### `QModelIndex QListWidget::indexFromItem(const QListWidgetItem *item) const`

**作用与语义：**

返回与给定`item`关联的`QModelIndex`。
注意：在5.10之前的Qt版本中，该函数采用了非`const` `item`。

### `void QListWidget::insertItem(int row, QListWidgetItem *item)`

**作用与语义：**

在`row`给出的列表中插入`item`的位置。

### `void QListWidget::insertItem(int row, const QString &label)`

**作用与语义：**

在列表控件中插入一个带有文本`label`的项目，位置由`row`给出。

### `void QListWidget::insertItems(int row, const QStringList &labels)`

**作用与语义：**

从给定`row`开始，将`labels`列表中的项目插入列表中。

### `bool QListWidget::isPersistentEditorOpen(QListWidgetItem *item) const`

**作用与语义：**

返回是否开放持久编辑器以进行项`item`。

### `QListWidgetItem *QListWidget::item(int row) const`

**作用与语义：**

如果列表中有某项被设置，返回占据该`row`的项;否则返回`nullptr`。

### `[signal] void QListWidget::itemActivated(QListWidgetItem *item)`

**作用与语义：**

当`item`被激活时，该信号会发出。`item`在用户点击或双击时激活，具体取决于系统配置。用户按下激活键时也会激活（在Windows和X11中为回车键，Mac OS X为Command O）。

### `QListWidgetItem *QListWidget::itemAt(const QPoint &p) const`

**作用与语义：**

返回指向坐标`p`的项目指针。坐标相对于列表控件的 `viewport()`。

### `QListWidgetItem *QListWidget::itemAt(int x, int y) const`

**作用与语义：**

返回指向坐标（`x`，`y`）的项目的指针。坐标相对于列表控件的 `viewport()`。

### `[signal] void QListWidget::itemChanged(QListWidgetItem *item)`

**作用与语义：**

每当`item`的数据发生变化时，该信号就会发出。

### `[signal] void QListWidget::itemClicked(QListWidgetItem *item)`

**作用与语义：**

当鼠标点击控件中的某个物品时，该信号会随指定`item`发出。

### `[signal] void QListWidget::itemDoubleClicked(QListWidgetItem *item)`

**作用与语义：**

当鼠标按钮双击控件中的某个项目时，会以指定`item`发出该信号。

### `[signal] void QListWidget::itemEntered(QListWidgetItem *item)`

**作用与语义：**

当鼠标光标进入物品时，该信号会发出。`item`表示已输入的物品。该信号仅在开启鼠标追踪或移动时按下鼠标按钮时发出。

### `QListWidgetItem *QListWidget::itemFromIndex(const QModelIndex &index) const`

**作用与语义：**

返回指向与给定`index`关联的`QListWidgetItem`的指针。

### `[signal] void QListWidget::itemPressed(QListWidgetItem *item)`

**作用与语义：**

当鼠标按键点击控件中的某个物品时，该信号会与指定的`item`一起发出。

### `[signal] void QListWidget::itemSelectionChanged()`

**作用与语义：**

每当选择发生变化时，该信号都会发出。

### `QWidget *QListWidget::itemWidget(QListWidgetItem *item) const`

**作用与语义：**

返回给定`item`中显示的小部件。

### `QList<QListWidgetItem *> QListWidget::items(const QMimeData *data) const`

**作用与语义：**

返回指向`data`对象中所包含项的指针列表。如果该对象不是在同一进程中由`QListWidget`创建的，则该列表为空。

### `[virtual protected] QMimeData *QListWidget::mimeData(const QList<QListWidgetItem *> &items) const`

**作用与语义：**

返回包含指定`items`序列化描述的对象。描述这些物品的格式来源于`mimeTypes()`函数。
如果项目列表为空，则返回`nullptr`，而不是序列化的空列表。

### `[virtual protected] QStringList QListWidget::mimeTypes() const`

**作用与语义：**

返回一个MIME类型列表，可用于描述列表控件的列表。

### `void QListWidget::openPersistentEditor(QListWidgetItem *item)`

**作用与语义：**

为给定`item`打开编辑器。编辑后编辑器保持开放状态。

### `void QListWidget::removeItemWidget(QListWidgetItem *item)`

**作用与语义：**

移除给定`item`上的控件集合。
要完全移除列表中的某个项目（行），要么删除该项目，要么使用`takeItem()`。

### `int QListWidget::row(const QListWidgetItem *item) const`

**作用与语义：**

返回包含给定`item`的行。

### `[slot] void QListWidget::scrollToItem(const QListWidgetItem *item, QAbstractItemView::ScrollHint hint = EnsureVisible)`

**作用与语义：**

如有必要，滚动视图以确保`item`可见。
`hint` 规定操作后应将`item`置于何处。

### `QList<QListWidgetItem *> QListWidget::selectedItems() const`

**作用与语义：**

返回列表控件中所有选中的项目列表。

### `void QListWidget::setCurrentItem(QListWidgetItem *item)`

**作用与语义：**

将当前项目设置为`item`。
除非选择模式`NoSelection`，否则该物品也会被选中。

### `void QListWidget::setCurrentItem(QListWidgetItem *item, QItemSelectionModel::SelectionFlags command)`

**作用与语义：**

将当前物品设置为`item`，使用给定的`command`。

### `void QListWidget::setCurrentRow(int row, QItemSelectionModel::SelectionFlags command)`

**作用与语义：**

该属性包含当前项目的行。
根据当前的选择模式，也可以选择该行。

**如何使用：** 调用 `setCurrentRow(...)` 修改 `currentRow`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QListWidget::setItemWidget(QListWidgetItem *item, QWidget *widget)`

**作用与语义：**

设置显示在给定`item`中的`widget`。
该函数仅用于显示静态内容，替代列表控件项。如果你想显示自定义动态内容或实现自定义编辑器控件，请使用 `QListView` 和子类 `QStyledItemDelegate`。
注：名单对`widget`所有权。

### `[override virtual] void QListWidget::setSelectionModel(QItemSelectionModel *selectionModel)`

**作用与语义：**

Reimplements： `QAbstractItemView::setSelectionModel`（QItemSelectionModel *selectionModel）.
将当前选择模型设定为给定的`selectionModel`。
注意，如果你在该函数后调用`setModel()`，给定的`selectionModel`将被视图创建的替代。
注意：如果旧的选择模型不再需要，应用程序自行删除;即当它不再被其他视图使用时。当其父对象被删除时，这会自动发生。然而，如果它没有父对象，或者父对象是长期存在的对象，可能更倾向于调用其`deleteLater()`函数显式删除它。

### `void QListWidget::sortItems(Qt::SortOrder order = Qt::AscendingOrder)`

**作用与语义：**

根据指定的`order`对列表控件中的所有项目进行排序。

### `[virtual protected] Qt::DropActions QListWidget::supportedDropActions() const`

**作用与语义：**

返回该视图支持的投放动作。

### `QListWidgetItem *QListWidget::takeItem(int row)`

**作用与语义：**

在列表控件中移除并返回给定`row`中的项目;否则返回`nullptr`。
从列表小部件中移除的项目不会由 Qt 管理，需要手动删除。

### `QRect QListWidget::visualItemRect(const QListWidgetItem *item) const`

**作用与语义：**

返回`item`处物体所在的视口矩形。

### `int count() const`

**作用与语义：**

此属性保存列表中项目的数量，包括任何隐藏的项目。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `int currentRow() const`

**作用与语义：**

该属性包含当前项目的行。
根据当前的选择模式，也可以选择该行。

**如何使用：** 调用 `currentRow()` 读取当前值；它不会修改应用状态。

### `bool isSortingEnabled() const`

**作用与语义：**

该属性是否启用排序。
如果该属性为`true`，则对列表进行排序;如果该属性为假，则不启用排序。
默认值为假。

**如何使用：** 调用 `isSortingEnabled()` 读取当前值；它不会修改应用状态。

### `void setCurrentRow(int row)`

**作用与语义：**

该属性包含当前项目的行。
根据当前的选择模式，也可以选择该行。

**如何使用：** 调用 `setCurrentRow(...)` 修改 `currentRow`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSortingEnabled(bool enable)`

**作用与语义：**

该属性是否启用排序。
如果该属性为`true`，则对列表进行排序;如果该属性为假，则不启用排序。
默认值为假。

**如何使用：** 调用 `setSortingEnabled(...)` 修改 `sortingEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

### 状态和错误边界

要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

### 线程边界

不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QListWidget` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
