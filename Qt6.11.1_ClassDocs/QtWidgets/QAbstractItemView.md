# QAbstractItemView

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** 模型/视图视图端的抽象基类，负责选择、滚动、编辑和展示模型数据。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QAbstractItemView`：模型/视图视图端的抽象基类，负责选择、滚动、编辑和展示模型数据。

**内部模型：** Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

**适用场景：** 创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractItemView>`
- 继承自：QAbstractScrollArea
- 直接派生类：QColumnView、QHeaderView、QListView、QTableView,、QTreeView

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

### 公有类型

- `enum DragDropMode { NoDragDrop, DragOnly, DropOnly, DragDrop, InternalMove }`
- `enum EditTrigger { NoEditTriggers, CurrentChanged, DoubleClicked, SelectedClicked, EditKeyPressed, …, AllEditTriggers }`
- `flags EditTriggers`
- `enum ScrollHint { EnsureVisible, PositionAtTop, PositionAtBottom, PositionAtCenter }`
- `enum ScrollMode { ScrollPerItem, ScrollPerPixel }`
- `enum SelectionBehavior { SelectItems, SelectRows, SelectColumns }`
- `enum SelectionMode { SingleSelection, ContiguousSelection, ExtendedSelection, MultiSelection, NoSelection }`

### 属性

- `alternatingRowColors : bool`
- `autoScroll : bool`
- `autoScrollMargin : int`
- `defaultDropAction : Qt::DropAction`
- `dragDropMode : DragDropMode`
- `dragDropOverwriteMode : bool`
- `dragEnabled : bool`
- `editTriggers : EditTriggers`
- `horizontalScrollMode : ScrollMode`
- `iconSize : QSize`
- `(since 6.11) keyboardSearchFlags : Qt::MatchFlags`
- `selectionBehavior : SelectionBehavior`
- `selectionMode : SelectionMode`
- `showDropIndicator : bool`
- `tabKeyNavigation : bool`
- `textElideMode : Qt::TextElideMode`
- `(since 6.9) updateThreshold : int`
- `verticalScrollMode : ScrollMode`

### 公有函数

- `QAbstractItemView(QWidget *parent = nullptr)`
- `virtual ~QAbstractItemView()`
- `bool alternatingRowColors() const`
- `int autoScrollMargin() const`
- `void closePersistentEditor(const QModelIndex &index)`
- `QModelIndex currentIndex() const`
- `Qt::DropAction defaultDropAction() const`
- `QAbstractItemView::DragDropMode dragDropMode() const`
- `bool dragDropOverwriteMode() const`
- `bool dragEnabled() const`
- `QAbstractItemView::EditTriggers editTriggers() const`
- `bool hasAutoScroll() const`
- `QAbstractItemView::ScrollMode horizontalScrollMode() const`
- `QSize iconSize() const`
- `virtual QModelIndex indexAt(const QPoint &point) const = 0`
- `QWidget * indexWidget(const QModelIndex &index) const`
- `bool isPersistentEditorOpen(const QModelIndex &index) const`
- `QAbstractItemDelegate * itemDelegate() const`
- `QAbstractItemDelegate * itemDelegateForColumn(int column) const`
- `(since 6.0) virtual QAbstractItemDelegate * itemDelegateForIndex(const QModelIndex &index) const`
- `QAbstractItemDelegate * itemDelegateForRow(int row) const`
- `virtual void keyboardSearch(const QString &search)`
- `Qt::MatchFlags keyboardSearchFlags() const`
- `QAbstractItemModel * model() const`
- `void openPersistentEditor(const QModelIndex &index)`
- `void resetHorizontalScrollMode()`
- `void resetVerticalScrollMode()`
- `QModelIndex rootIndex() const`
- `virtual void scrollTo(const QModelIndex &index, QAbstractItemView::ScrollHint hint = EnsureVisible) = 0`
- `QAbstractItemView::SelectionBehavior selectionBehavior() const`
- `QAbstractItemView::SelectionMode selectionMode() const`
- `QItemSelectionModel * selectionModel() const`
- `void setAlternatingRowColors(bool enable)`
- `void setAutoScroll(bool enable)`
- `void setAutoScrollMargin(int margin)`
- `void setDefaultDropAction(Qt::DropAction dropAction)`
- `void setDragDropMode(QAbstractItemView::DragDropMode behavior)`
- `void setDragDropOverwriteMode(bool overwrite)`
- `void setDragEnabled(bool enable)`
- `void setDropIndicatorShown(bool enable)`
- `void setEditTriggers(QAbstractItemView::EditTriggers triggers)`
- `void setHorizontalScrollMode(QAbstractItemView::ScrollMode mode)`
- `void setIconSize(const QSize &size)`
- `void setIndexWidget(const QModelIndex &index, QWidget *widget)`
- `void setItemDelegate(QAbstractItemDelegate *delegate)`
- `void setItemDelegateForColumn(int column, QAbstractItemDelegate *delegate)`
- `void setItemDelegateForRow(int row, QAbstractItemDelegate *delegate)`
- `void setKeyboardSearchFlags(Qt::MatchFlags searchFlags)`
- `virtual void setModel(QAbstractItemModel *model)`
- `void setSelectionBehavior(QAbstractItemView::SelectionBehavior behavior)`
- `void setSelectionMode(QAbstractItemView::SelectionMode mode)`
- `virtual void setSelectionModel(QItemSelectionModel *selectionModel)`
- `void setTabKeyNavigation(bool enable)`
- `void setTextElideMode(Qt::TextElideMode mode)`
- `void setUpdateThreshold(int threshold)`
- `void setVerticalScrollMode(QAbstractItemView::ScrollMode mode)`
- `bool showDropIndicator() const`
- `virtual int sizeHintForColumn(int column) const`
- `QSize sizeHintForIndex(const QModelIndex &index) const`
- `virtual int sizeHintForRow(int row) const`
- `bool tabKeyNavigation() const`
- `Qt::TextElideMode textElideMode() const`
- `int updateThreshold() const`
- `QAbstractItemView::ScrollMode verticalScrollMode() const`
- `virtual QRect visualRect(const QModelIndex &index) const = 0`

### 重实现的公有函数

- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery query) const override`

### 公有槽函数

- `void clearSelection()`
- `void edit(const QModelIndex &index)`
- `virtual void reset()`
- `void scrollToBottom()`
- `void scrollToTop()`
- `virtual void selectAll()`
- `void setCurrentIndex(const QModelIndex &index)`
- `virtual void setRootIndex(const QModelIndex &index)`
- `void update(const QModelIndex &index)`

### 信号

- `void activated(const QModelIndex &index)`
- `void clicked(const QModelIndex &index)`
- `void doubleClicked(const QModelIndex &index)`
- `void entered(const QModelIndex &index)`
- `void iconSizeChanged(const QSize &size)`
- `void pressed(const QModelIndex &index)`
- `void viewportEntered()`

### 保护函数

- `QPoint dirtyRegionOffset() const`
- `QAbstractItemView::DropIndicatorPosition dropIndicatorPosition() const`
- `virtual bool edit(const QModelIndex &index, QAbstractItemView::EditTrigger trigger, QEvent *event)`
- `void executeDelayedItemsLayout()`
- `virtual int horizontalOffset() const = 0`
- `(since 6.0) virtual void initViewItemOption(QStyleOptionViewItem *option) const`
- `virtual bool isIndexHidden(const QModelIndex &index) const = 0`
- `virtual QModelIndex moveCursor(QAbstractItemView::CursorAction cursorAction, Qt::KeyboardModifiers modifiers) = 0`
- `void scheduleDelayedItemsLayout()`
- `void scrollDirtyRegion(int dx, int dy)`
- `virtual QModelIndexList selectedIndexes() const`
- `virtual QItemSelectionModel::SelectionFlags selectionCommand(const QModelIndex &index, const QEvent *event = nullptr) const`
- `void setDirtyRegion(const QRegion &region)`
- `virtual void setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags flags) = 0`
- `void setState(QAbstractItemView::State state)`
- `virtual void startDrag(Qt::DropActions supportedActions)`
- `QAbstractItemView::State state() const`
- `virtual int verticalOffset() const = 0`
- `virtual QRegion visualRegionForSelection(const QItemSelection &selection) const = 0`

### 重实现的保护函数

- `virtual void dragEnterEvent(QDragEnterEvent *event) override`
- `virtual void dragLeaveEvent(QDragLeaveEvent *event) override`
- `virtual void dragMoveEvent(QDragMoveEvent *event) override`
- `virtual void dropEvent(QDropEvent *event) override`
- `virtual bool event(QEvent *event) override`
- `virtual bool eventFilter(QObject *object, QEvent *event) override`
- `virtual void focusInEvent(QFocusEvent *event) override`
- `virtual bool focusNextPrevChild(bool next) override`
- `virtual void focusOutEvent(QFocusEvent *event) override`
- `virtual void inputMethodEvent(QInputMethodEvent *event) override`
- `virtual void keyPressEvent(QKeyEvent *event) override`
- `virtual void mouseDoubleClickEvent(QMouseEvent *event) override`
- `virtual void mouseMoveEvent(QMouseEvent *event) override`
- `virtual void mousePressEvent(QMouseEvent *event) override`
- `virtual void mouseReleaseEvent(QMouseEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *event) override`
- `virtual void timerEvent(QTimerEvent *event) override`
- `virtual bool viewportEvent(QEvent *event) override`
- `virtual QSize viewportSizeHint() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAbstractItemView::CursorAction`

**作用与语义：**

这个枚举描述了在物品之间导航的不同方式，。
- `QAbstractItemView::MoveUp`：`0`;移动到当前物品上方的物品。
- `QAbstractItemView::MoveDown`：`1`;移动到当前物品下方的物品。
- `QAbstractItemView::MoveLeft`：`2`;移动到当前物品左侧。
- `QAbstractItemView::MoveRight`：`3`;移动到当前物品的右侧。
- `QAbstractItemView::MoveHome`：`4`;移动到左上角的项目。
- `QAbstractItemView::MoveEnd`：`5`;移动到右下角的项目。
- `QAbstractItemView::MovePageUp`：`6`;将当前项目向上移动一页。
- `QAbstractItemView::MovePageDown`：`7`;向下移动一页，位于当前项目下方。
- `QAbstractItemView::MoveNext`：`8`;在当前物品之后移动到该项目。
- `QAbstractItemView::MovePrevious`：`9`;移动到当前物品之前的物品。

### `enum QAbstractItemView::DragDropMode`

**作用与语义：**

描述视图可以操作的各种拖拽事件。默认情况下，视图不支持拖拽或拖拽（`NoDragDrop`）。
- `QAbstractItemView::NoDragDrop`：`0`;不支持拖拽或拖拽。
- `QAbstractItemView::DragOnly`：`1`;视图支持拖拽自身项目
- `QAbstractItemView::DropOnly`：`2`;视图接受落差
- `QAbstractItemView::DragDrop`：`3`;视图支持拖拽和拖放
- `QAbstractItemView::InternalMove`：`4`;视图只接受自身的移动（不复制）操作。
请注意，所用模型需要支持拖拽操作。

### `enum QAbstractItemView::DropIndicatorPosition`

**作用与语义：**

该枚举表示掉落指示器在当前鼠标位置相对于索引的位置：
- `QAbstractItemView::OnItem`：`0`;该项将被丢弃在索引中。
- `QAbstractItemView::AboveItem`：`1`;该项目将被丢弃在索引之上。
- `QAbstractItemView::BelowItem`：`2`;该项目将被降至索引以下。
- `QAbstractItemView::OnViewport`：`3`;该项目会被丢弃到没有物品的视口区域。每个视图处理丢弃到视口的物品的方式取决于所用底层模型的行为。

### `enum QAbstractItemView::EditTriggerflags QAbstractItemView::EditTriggers`

**作用与语义：**

这个枚举描述了将启动项目编辑的动作。
- `QAbstractItemView::NoEditTriggers`：`0`;无法编辑。
- `QAbstractItemView::CurrentChanged`：`1`;当前项目发生变化时，编辑开始。
- `QAbstractItemView::DoubleClicked`：`2`;编辑当双击项目时开始。
- `QAbstractItemView::SelectedClicked`：`4`;点击已选中的项目后开始编辑。
- `QAbstractItemView::EditKeyPressed`：`8`;当平台编辑键被按在某个项目上时，编辑开始。
- `QAbstractItemView::AnyKeyPressed`：`16`;当按下任意键时，编辑开始。
- `QAbstractItemView::AllEditTriggers`：`31`;所有上述操作开始编辑。
EditTriggers 类型是 QFlags 的 typedef<EditTrigger>。它存储 EditTrigger 值的 OR 组合。

### `enum QAbstractItemView::ScrollMode`

**作用与语义：**

描述滚动条应如何表现。将滚动模式设置为ScrollPerPixel时，除非用`setSingleStep()`明确设置，否则单步长会自动调整。通过将单步长设置为-1可以恢复自动调整。
- `QAbstractItemView::ScrollPerItem`：`0`;视图将逐项滚动内容。
- `QAbstractItemView::ScrollPerPixel`：`1`;视图将逐像素滚动内容。

### `enum QAbstractItemView::SelectionMode`

**作用与语义：**

该枚举显示视图对用户选择的响应：
- `QAbstractItemView::SingleSelection`：`1`;当用户选择一个项目时，任何已选中的项目都会被取消选择。用户可以通过点击选中的项目时按Ctrl键取消选择该项目。
- `QAbstractItemView::ContiguousSelection`：`4`;当用户以常规方式选择物品时，选择会被清除，新物品被选中。然而，如果用户在点击物品时按下Shift键，当前物品与被点击物品之间的所有物品都会被选择或取消，具体取决于点击物品的状态。
- `QAbstractItemView::ExtendedSelection`：`3`;当用户以常规方式选择物品时，选择会被清除，新物品被选中。但如果用户点击物品时按Ctrl键，点击的物品会被切换，其他物品保持不动。如果用户点击物品时按下Shift键，当前物品与被点击物品之间的所有物品都会被选择或取消，具体取决于点击物品的状态。通过拖动鼠标可以选择多个物品。
- `QAbstractItemView::MultiSelection`：`2`;当用户以常规方式选择某个物品时，该物品的选择状态会被切换，其他物品保持不动。通过拖动鼠标可以切换多个物品。
- `QAbstractItemView::NoSelection`：`0`;物品不可选择。
最常用的模式是单选（SingleElection）和扩展选择（ExtendedSelection）。

### `enum QAbstractItemView::State`

**作用与语义：**

描述视图可能处于的不同状态。这通常只有在重新实现你自己的视图时才有趣。
- `QAbstractItemView::NoState`：`0`;是默认状态。
- `QAbstractItemView::DraggingState`：`1`;用户正在拖拽物品。
- `QAbstractItemView::DragSelectingState`：`2`;用户正在选择项目。
- `QAbstractItemView::EditingState`：`3`;用户正在小部件编辑器中编辑一个项目。
- `QAbstractItemView::ExpandingState`：`4`;用户正在打开一个物品分支。
- `QAbstractItemView::CollapsingState`：`5`;用户正在关闭一个分支的物品。
- `QAbstractItemView::AnimatingState`：`6`;物品视图正在进行动画。

### `alternatingRowColors : bool`

**作用与语义：**

该属性决定是否使用交替颜色绘制背景。
如果该属性`true`，物品背景将使用 `QPalette::Base` 和 `QPalette::AlternateBase` 绘制;否则背景将使用 `QPalette::Base` 颜色绘制。
默认情况下，该属性为`false`。

**如何使用：** 调用 `alternatingRowColors()` 读取当前值；它不会修改应用状态。

### `autoScroll : bool`

**作用与语义：**

该属性适用于拖动移动事件中是否启用自动滚动。
如果将该属性设置为 true（默认值），则当用户拖动到视口边缘 16 像素范围内时，`QAbstractItemView` 会自动滚动视图内容。如果当前项目发生变化，则视图会自动滚动以确保当前项目完全可见。
此属性仅在视口接受放置操作时有效。将此属性设置为 false 可关闭自动滚动。

**如何使用：** 调用 `autoScroll()` 读取当前值；它不会修改应用状态。

### `autoScrollMargin : int`

**作用与语义：**

该属性表示触发自动滚动时区域的大小。
该属性控制视口边缘触发自动滚动区域的大小。默认值为16像素。

**如何使用：** 调用 `autoScrollMargin()` 读取当前值；它不会修改应用状态。

### `defaultDropAction : Qt::DropAction`

**作用与语义：**

该属性包含了 QAbstractItemView：:d rag() 默认使用的 drop 动作。
如果该属性未被设置，当支持的动作支持 CopyAction 时，drop 动作是 CopyAction。

**如何使用：** 调用 `defaultDropAction()` 读取当前值；它不会修改应用状态。

### `dragDropMode : DragDropMode`

**作用与语义：**

该属性包含视图将对拖拽事件的反应。

**如何使用：** 调用 `dragDropMode()` 读取当前值；它不会修改应用状态。

### `dragDropOverwriteMode : bool`

**作用与语义：**

该属性保留了视图的拖拽行为。
如果其值`true`，所选数据在丢弃时会覆盖现有的项目数据;移动数据则清除该项目。如果其值为`false`，则在丢弃数据时，所选数据将作为新项目插入。当数据被移动时，该项目也会被移除。
默认值为`false`，与`QListView`和`QTreeView`子类相同。而`QTableView`子类则设定为`true`。
注意：这并非为了防止项目被覆盖。模型中标志()的实现应通过不返回`Qt::ItemIsDropEnabled`来实现这一点。

**如何使用：** 调用 `dragDropOverwriteMode()` 读取当前值；它不会修改应用状态。

### `dragEnabled : bool`

**作用与语义：**

该属性是否支持视图拖拽自身项目，则判定。

**如何使用：** 调用 `dragEnabled()` 读取当前值；它不会修改应用状态。

### `editTriggers : EditTriggers`

**作用与语义：**

该属性决定哪些动作将启动物品编辑。
该属性是`EditTrigger`定义的一系列标志，并结合 OR 操作符。只有当执行的动作被设置在该属性中时，视图才会启动对项目的编辑。
默认值为：
- `QTableView`：`DoubleClicked`|`AnyKeyPressed`
- 其他视角：`DoubleClicked`|`EditKeyPressed`

**如何使用：** 调用 `editTriggers()` 读取当前值；它不会修改应用状态。

### `horizontalScrollMode : ScrollMode`

**作用与语义：**

视图如何横向滚动内容。
该属性控制视图如何横向滚动内容。滚动可以按像素或按项目滚动。默认值来自样式，通过`QStyle::SH_ItemView_ScrollMode`样式提示。

**如何使用：** 调用 `horizontalScrollMode()` 读取当前值；它不会修改应用状态。

### `iconSize : QSize`

**作用与语义：**

该属性会显示物品图标的大小。
当视图可见时设置该属性，物品会重新排列。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `[since 6.11] keyboardSearchFlags : Qt::MatchFlags`

**作用与语义：**

该属性决定了`keyboardSearch()`默认实现如何将给定字符串与模型数据匹配。
默认值是`Qt::MatchStartsWith|Qt::MatchWrap`。

**如何使用：** 调用 `keyboardSearchFlags()` 读取当前值；它不会修改应用状态。

### `selectionBehavior : SelectionBehavior`

**作用与语义：**

该属性决定了视图所采用的选择行为。
无论选择是单项、行还是列，都适用该属性。

**如何使用：** 调用 `selectionBehavior()` 读取当前值；它不会修改应用状态。

### `selectionMode : SelectionMode`

**作用与语义：**

该属性决定了视图在哪种选择模式下运行。
该属性控制用户是否可以选择一个或多个项目，以及在多项目选择中，选择是否必须是连续的项目范围。

**如何使用：** 调用 `selectionMode()` 读取当前值；它不会修改应用状态。

### `showDropIndicator : bool`

**作用与语义：**

该属性是否在拖曳物品和投放时显示掉落指示器时成立。

**如何使用：** 调用 `showDropIndicator()` 读取当前值；它不会修改应用状态。

### `tabKeyNavigation : bool`

**作用与语义：**

该属性决定是否启用了带有标签页和后页的项目导航。

**如何使用：** 调用 `tabKeyNavigation()` 读取当前值；它不会修改应用状态。

### `textElideMode : Qt::TextElideMode`

**作用与语义：**

此属性保存省略文本中“...”的位置。
所有项视图的默认值是 `Qt::ElideRight`。

**如何使用：** 调用 `textElideMode()` 读取当前值；它不会修改应用状态。

### `[since 6.9] updateThreshold : int`

**作用与语义：**

该属性包含了索引的变化数量，以直接触发`dataChanged()`内视图的全面更新。
`dataChanged()` 内部的算法试图通过计算变更后的索引是否可见，来最小化视图的全面更新。对于非常大的模型，且有大量大变更，这可能比实际更新时间更长，因此适得其反。这一特性使算法能够控制，当变更的索引数量超过给定值时，跳过检查并直接触发完整更新。
默认数值是200。

**如何使用：** 调用 `updateThreshold()` 读取当前值；它不会修改应用状态。

### `verticalScrollMode : ScrollMode`

**作用与语义：**

视图如何沿垂直方向滚动内容。
该属性控制视图如何垂直滚动内容。滚动可以按像素或按项目滚动。默认值来自样式，通过`QStyle::SH_ItemView_ScrollMode`样式提示。

**如何使用：** 调用 `verticalScrollMode()` 读取当前值；它不会修改应用状态。

### `[explicit] QAbstractItemView::QAbstractItemView(QWidget *parent = nullptr)`

**作用与语义：**

基于给定`parent`构造抽象项目视图。

### `[virtual noexcept] QAbstractItemView::~QAbstractItemView()`

**作用与语义：**

破坏了视野。

### `[signal] void QAbstractItemView::activated(const QModelIndex &index)`

**作用与语义：**

当用户激活`index`指定的物品时，会发出该信号。激活方式取决于平台;例如，单击或双击该物品，或当前物品时按回车或回车键。

### `[slot] void QAbstractItemView::clearSelection()`

**作用与语义：**

取消所有选中的项目。当前索引不会被更改。

### `[signal] void QAbstractItemView::clicked(const QModelIndex &index)`

**作用与语义：**

当鼠标按钮左键点击时，该信号会发出。鼠标被点击的物品由`index`指定。只有当索引有效时才会发出该信号。

### `[virtual protected slot] void QAbstractItemView::closeEditor(QWidget *editor, QAbstractItemDelegate::EndEditHint hint)`

**作用与语义：**

关闭给定的`editor`，并释放它。`hint`用于指定视图在编辑操作结束时应如何响应。例如，提示可能表明视图中的下一个项目应被打开进行编辑。

### `void QAbstractItemView::closePersistentEditor(const QModelIndex &index)`

**作用与语义：**

在给定的 `index` 关闭该项目的持久编辑器。

### `[virtual protected slot] void QAbstractItemView::commitData(QWidget *editor)`

**作用与语义：**

将 `editor` 中的数据提交到模型中。

### `[virtual protected slot] void QAbstractItemView::currentChanged(const QModelIndex &current, const QModelIndex &previous)`

**作用与语义：**

当新项目变成当前项目时调用该槽。之前的当前项目由`previous`索引指定，新项目由`current`索引指定。
如果你想知道物品的变化，请查看`dataChanged()`信号。

### `QModelIndex QAbstractItemView::currentIndex() const`

**作用与语义：**

返回当前项目的模型索引。

### `[virtual protected slot] void QAbstractItemView::dataChanged(const QModelIndex &topLeft, const QModelIndex &bottomRight, const QList<int> &roles = QList<int>())`

**作用与语义：**

当模型中具有相同`roles`的物品发生变化时，该槽位被调用。更改的物品包括从`topLeft`到`bottomRight`的物品。如果只更改一个物品`topLeft` == `bottomRight`。
被更改的`roles`可以是空容器（意味着一切都变了），也可以是包含角色子集的非空容器。
注意：`Qt::ToolTipRole` 未被 dataChanged() 认可，在 Qt 提供的观点中。

### `[protected] QPoint QAbstractItemView::dirtyRegionOffset() const`

**作用与语义：**

返回视图中脏区域的偏移量。
如果你用`scrollDirtyRegion()`并在`QAbstractItemView`子类中实现`paintEvent()`，你应该将绘画事件给出的面积与该函数返回的偏移量进行转换。

### `[signal] void QAbstractItemView::doubleClicked(const QModelIndex &index)`

**作用与语义：**

当双击鼠标按钮时，该信号会发出。鼠标被双击的项目由`index`指定。只有当索引有效时才会发出该信号。

### `[override virtual protected] void QAbstractItemView::dragEnterEvent(QDragEnterEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dragEnterEvent`（QDragEnterEvent *event）。
当拖拽操作进入控件时，调用该函数`event`。如果拖拽地点是有效的投放地点（例如允许投放的物品），则该事件被接受;否则将被忽略。

### `[override virtual protected] void QAbstractItemView::dragLeaveEvent(QDragLeaveEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dragLeaveEvent`（QDragLeaveEvent *event）。
当被拖拽的物品离开视图时调用该函数。`event`描述拖拽操作的状态。

### `[override virtual protected] void QAbstractItemView::dragMoveEvent(QDragMoveEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dragMoveEvent`（QDragMoveEvent *event）。
该函数在拖拽控件时连续调用给定`event`。例如，当用户将选区拖到视图的右侧或底部时，视图可能会滚动。此时事件会被接受;否则会被忽略。

### `[override virtual protected] void QAbstractItemView::dropEvent(QDropEvent *event)`

**作用与语义：**

重现：`QAbstractScrollArea::dropEvent`（QDropEvent *事件）。
当组件上发生掉落事件时，该函数会被调用给定`event`。如果模型接受偶数位置，则接受掉落事件;否则会被忽略。

### `[protected] QAbstractItemView::DropIndicatorPosition QAbstractItemView::dropIndicatorPosition() const`

**作用与语义：**

返回掉落指示器相对于最近物品的位置。

### `[slot] void QAbstractItemView::edit(const QModelIndex &index)`

**作用与语义：**

如果该项目可编辑，`index`会开始编辑。
请注意，该函数不会改变当前索引。由于当前索引定义了接下来和之前需要编辑的项目，用户可能会发现键盘导航无法如预期般工作。为了提供一致的导航行为，请在使用相同模型索引的函数前调用 `setCurrentIndex()`。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
abstractItemView， qOverload（&QAbstractItemView：：edit））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
abstractItemView， [receiver = abstractItemView]（const QModelIndex &index） { receiver->edit（index）; }）;


更多示例和方法，请参见连接超载槽位。

### `[virtual protected] bool QAbstractItemView::edit(const QModelIndex &index, QAbstractItemView::EditTrigger trigger, QEvent *event)`

**作用与语义：**

从`index`开始编辑该项，必要时创建编辑器，若视图`State` `EditingState`，返回`true`;否则返回`false`。
导致编辑过程的动作由`trigger`描述，相关事件由`event`指定。
编辑可以通过指定`QAbstractItemView::AllEditTriggers`的`trigger`来强制进行。

### `[virtual protected slot] void QAbstractItemView::editorDestroyed(QObject *editor)`

**作用与语义：**

当给定`editor`被销毁时，调用该函数。

### `[signal] void QAbstractItemView::entered(const QModelIndex &index)`

**作用与语义：**

当鼠标光标进入`index`指定的项目时，会发出该信号。此功能需要启用鼠标追踪功能。

### `[override virtual protected] bool QAbstractItemView::event(QEvent *event)`

**作用与语义：**

重装：`QAbstractScrollArea::event`（QEvent *事件）。

### `[override virtual protected] bool QAbstractItemView::eventFilter(QObject *object, QEvent *event)`

**作用与语义：**

重装：`QObject::eventFilter`（QObject *已观看，QEvent *事件）。

### `[protected] void QAbstractItemView::executeDelayedItemsLayout()`

**作用与语义：**

在不等待事件处理开始的情况下执行预约布局。

### `[override virtual protected] void QAbstractItemView::focusInEvent(QFocusEvent *event)`

**作用与语义：**

重实现自：`QWidget::focusInEvent`（QFocusEvent *event）。
当控件获得焦点时，该函数会以给定的`event`调用。默认情况下，该事件被忽略。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点接收）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] bool QAbstractItemView::focusNextPrevChild(bool next)`

**作用与语义：**

重构：`QWidget::focusNextPrevChild`（下一个布尔）。
根据 Tab 和 Shift Tab 找到一个新的控件来给键盘焦点，如果能找到新控件，则返回 `true`，找不到则返回 false。
如果`next`为真，该函数向前搜索;如果`next`为假，则向后搜索。
有时，你会想重新实现这个函数。例如，浏览器可能会重新实现它，将“当前活跃链接”向前或向后移动，只有当它到达“页面”的最后或第一个链接时才调用 focusNextPrevChild()。
子控件调用其父控件的 focusNextPrevChild()，但只有包含子控件的窗口决定将焦点重定向到哪里。通过重新实现该函数，你就能控制所有子控件的焦点遍历。

### `[override virtual protected] void QAbstractItemView::focusOutEvent(QFocusEvent *event)`

**作用与语义：**

重实现自：`QWidget::focusOutEvent`（QFocusEvent *event）。
当控件失去焦点时，该函数会被调用给定的`event`。默认情况下，该事件被忽略。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点丢失）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件上的`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非有没有指定`focusPolicy()`的窗口）。

### `[pure virtual protected] int QAbstractItemView::horizontalOffset() const`

**作用与语义：**

返回视角的水平偏移。
在基类中，这是一个纯虚拟函数。

### `[pure virtual] QModelIndex QAbstractItemView::indexAt(const QPoint &point) const`

**作用与语义：**

返回视口坐标处的模型索引`point`。
在基类中，这是一个纯虚拟函数。

### `QWidget *QAbstractItemView::indexWidget(const QModelIndex &index) const`

**作用与语义：**

在给定`index`返回该物品的小部件。

### `[virtual protected, since 6.0] void QAbstractItemView::initViewItemOption(QStyleOptionViewItem *option) const`

**作用与语义：**

用视图的调色板、字体、状态、对齐等初始化`option`结构。
注意：该方法的实现应检查接收结构的 `version`，填充实现熟悉的所有成员，并将版本成员设置为实现支持的版本，然后返回。

### `[override virtual protected] void QAbstractItemView::inputMethodEvent(QInputMethodEvent *event)`

**作用与语义：**

重实现自：`QWidget::inputMethodEvent`（QInputMethodEvent *event）。
对于事件`event`，该事件处理程序可以被重新实现到子类中以接收输入法组合事件。当输入方法的状态发生变化时，调用该处理程序。
注意，在创建自定义文本编辑小部件时，必须明确设置`Qt::WA_InputMethodEnabled`窗口属性（使用`setAttribute()`函数），才能接收输入法事件。
默认实现调用 event->ignore()，拒绝输入法事件。详情请参见 `QInputMethodEvent` 文档。

### `[override virtual] QVariant QAbstractItemView::inputMethodQuery(Qt::InputMethodQuery query) const`

**作用与语义：**

重实现自：`QWidget::inputMethodQuery`（Qt：：InputMethodQuery query） const.
该方法仅适用于输入控件。输入方法用于查询控件的一组属性，以支持复杂的输入法操作，以支持周围文本和重新转换。
`query` 指定查询的属性。

### `[pure virtual protected] bool QAbstractItemView::isIndexHidden(const QModelIndex &index) const`

**作用与语义：**

如果给定`index`所引用的项目隐藏在视图中，返回`true`，否则返回`false`。
隐藏是视图特定的功能。例如在`TableView`中，可以标记一列为隐藏，或者标记为`TreeView`中的一行。
在基类中，这是一个纯虚拟函数。

### `bool QAbstractItemView::isPersistentEditorOpen(const QModelIndex &index) const`

**作用与语义：**

返回索引`index`时是否打开了持久编辑器。

### `QAbstractItemDelegate *QAbstractItemView::itemDelegate() const`

**作用与语义：**

返回该视图和模型所使用的项目代理。这要么是带有`setItemDelegate()`的一组，要么是默认的。

### `QAbstractItemDelegate *QAbstractItemView::itemDelegateForColumn(int column) const`

**作用与语义：**

返回该视图和模型对给定`column`所使用的项目代理。你可以调用`itemDelegate()`获取指向当前代理的指针。

### `[virtual, since 6.0] QAbstractItemDelegate *QAbstractItemView::itemDelegateForIndex(const QModelIndex &index) const`

**作用与语义：**

返回该视图和模型在给定`index`中使用的项目代理。

### `QAbstractItemDelegate *QAbstractItemView::itemDelegateForRow(int row) const`

**作用与语义：**

返回该视图和模型用于给定`row`的项目代理，若未分配代理则返回`nullptr`。你可以调用`itemDelegate()`获取当前索引代理的指针。

### `[override virtual protected] void QAbstractItemView::keyPressEvent(QKeyEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::keyPressEvent`（QKeyEvent *e）。
当向控件发送键事件时，该函数会以给定的`event`调用。默认实现处理基本的光标移动，例如上下、左、右、主页、PageUp和PageDown;如果当前索引有效且激活键被按下（例如按回车或回车，取决于平台），就会发出`activated()`信号。该功能是通过按键启动编辑，例如按F2时。

### `[virtual] void QAbstractItemView::keyboardSearch(const QString &search)`

**作用与语义：**

移动到并选择与字符串最匹配的`search`项。如果未找到任何项，则不会发生任何事。
在默认实现中，如果`search`为空，或自上次搜索到时间区间超过`QApplication::keyboardInputInterval()`，搜索将被重置。

### `QAbstractItemModel *QAbstractItemView::model() const`

**作用与语义：**

返回该视图所呈现的模型。

### `[override virtual protected] void QAbstractItemView::mouseDoubleClickEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mouseDoubleClickEvent`（QMouseEvent *e）。
当鼠标按钮在控件内双击时，调用该函数的 `event`。如果双击点击在有效物品上，会发出 `doubleClicked()` 信号并调用该物品的 `edit()`。

### `[override virtual protected] void QAbstractItemView::mouseMoveEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mouseMoveEvent`（QMouseEvent *e）。
当向控件发送鼠标移动事件时，该函数会被调用给定的`event`。如果选择正在进行中且有新项目被移动，则选择会被扩展;如果正在进行拖动，则继续。

### `[override virtual protected] void QAbstractItemView::mousePressEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mousePressEvent`（QMouseEvent *e）。
当鼠标按键且光标位于控件内时，调用该函数的 `event`。如果点击有效物品，则该项被转换为当前物品。该函数发出`pressed()`信号。

### `[override virtual protected] void QAbstractItemView::mouseReleaseEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mouseReleaseEvent`（QMouseEvent *e）。
该函数在小部件上按下鼠标事件后，按`event`时调用。如果用户在小部件内按下鼠标，然后在松开前将鼠标拖到另一个位置，小部件会接收释放事件。如果有物品被按下，该函数会发出`clicked()`信号。

### `[pure virtual protected] QModelIndex QAbstractItemView::moveCursor(QAbstractItemView::CursorAction cursorAction, Qt::KeyboardModifiers modifiers)`

**作用与语义：**

返回一个指向视图中下一个对象的`QModelIndex`对象，基于`modifiers`指定的`cursorAction`和键盘修饰符。
在基类中，这是一个纯虚拟函数。

### `void QAbstractItemView::openPersistentEditor(const QModelIndex &index)`

**作用与语义：**

在给定`index`处对该项目打开持久编辑器。如果没有编辑器存在，代理将创建一个新的编辑器。

### `[signal] void QAbstractItemView::pressed(const QModelIndex &index)`

**作用与语义：**

当鼠标按下按钮时，该信号会发出。鼠标被按下的物品由`index`指定。只有当索引有效时，才会发出该信号。
用`QGuiApplication::mouseButtons()`功能获取鼠标按键的状态。

### `[virtual slot] void QAbstractItemView::reset()`

**作用与语义：**

重置视图的内部状态。
警告：该函数将重置打开的编辑器、滚动条位置、选择等。现有的更改不会被提交。如果你想在重置视图时保存你的更改，可以重新实现这个函数，提交你的更改，然后调用该超类的实现。

### `[override virtual protected] void QAbstractItemView::resizeEvent(QResizeEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::resizeEvent`（QResizeEvent *event）。
当向控件发送缩放事件时，调用该函数的具体`event`。

### `QModelIndex QAbstractItemView::rootIndex() const`

**作用与语义：**

返回模型根项的模型索引。根项是视图顶层项的父项。根项可能无效。

### `[virtual protected slot] void QAbstractItemView::rowsAboutToBeRemoved(const QModelIndex &parent, int start, int end)`

**作用与语义：**

当行即将被移除时，会调用该栏位。被删除的行是从`start`到`end`包含给定`parent`下的行。

### `[virtual protected slot] void QAbstractItemView::rowsInserted(const QModelIndex &parent, int start, int end)`

**作用与语义：**

插入行时调用该槽位。新行为`start`至`end`包含给定`parent`下的行。基类实现调用模型中的fetchMore()以检查更多数据。

### `[protected] void QAbstractItemView::scheduleDelayedItemsLayout()`

**作用与语义：**

在事件处理开始时，安排视图中项目的布局。
即使在事件处理前多次调用 scheduleDelayedItemsLayout()，视图也只会执行一次布局。

### `[protected] void QAbstractItemView::scrollDirtyRegion(int dx, int dy)`

**作用与语义：**

通过将脏区域向相反方向移动，为按 （`dx`，`dy`） 像素滚动做准备。只有在你的视图子类中实现滚动视口时，才需要调用这个函数。
如果你在`QAbstractItemView`的子类中实现`scrollContentsBy()`，请先调用这个函数，再调用视口上的`QWidget::scroll()`。或者，直接调用`update()`。

### `[pure virtual] void QAbstractItemView::scrollTo(const QModelIndex &index, QAbstractItemView::ScrollHint hint = EnsureVisible)`

**作用与语义：**

如有需要，滚动视图以确保`index`的物品可见。视图会尝试根据给定的`hint`定位该物品。
在基类中，这是一个纯虚拟函数。

### `[slot] void QAbstractItemView::scrollToBottom()`

**作用与语义：**

将视图滚动到底部。

### `[slot] void QAbstractItemView::scrollToTop()`

**作用与语义：**

将视图滚动到顶部。

### `[virtual slot] void QAbstractItemView::selectAll()`

**作用与语义：**

选择视图中的所有项目。该函数在选择时会使用视图中的选择行为。

### `[virtual protected] QModelIndexList QAbstractItemView::selectedIndexes() const`

**作用与语义：**

此便捷函数返回视图中所有已选择且未隐藏的项目索引的列表。该列表不包含重复项，也未排序。

### `[virtual protected slot] void QAbstractItemView::selectionChanged(const QItemSelection &selected, const QItemSelection &deselected)`

**作用与语义：**

当选择发生变化时，该槽被调用。之前的选择（可能是空的）由`deselected`指定，新选择由`selected`指定。

### `[virtual protected] QItemSelectionModel::SelectionFlags QAbstractItemView::selectionCommand(const QModelIndex &index, const QEvent *event = nullptr) const`

**作用与语义：**

返回用于更新指定`index`选择模型时使用的SelectionFlags。结果取决于当前`selectionMode()`以及用户输入事件`event`，该事件可以`nullptr`。
重新实现这个函数，定义你自己的选择行为。

### `QItemSelectionModel *QAbstractItemView::selectionModel() const`

**作用与语义：**

返回当前的选择模型。

### `[slot] void QAbstractItemView::setCurrentIndex(const QModelIndex &index)`

**作用与语义：**

将当前项目设置为`index`的项目。
除非当前选择模式`NoSelection`，否则该项目也会被选中。注意，该功能还会更新用户新选择的起始位置。
要将某个项目设置为当前项目但未选择该项目，请调用。
`selectionModel()->setCurrentIndex(index, QItemSelectionModel::NoUpdate);`。

### `[protected] void QAbstractItemView::setDirtyRegion(const QRegion &region)`

**作用与语义：**

将给定`region`标记为脏的，并安排更新。只有在实现自己的视图子类时才需要调用这个函数。

### `void QAbstractItemView::setIndexWidget(const QModelIndex &index, QWidget *widget)`

**作用与语义：**

在给定`index`对物品设置给定的`widget`，将小部件的所有权传递给视口。
如果`index`无效（例如，传递根索引），该函数将无效。
给定`widget`的`autoFillBackground`属性必须设置为true，否则小部件的背景将透明，同时显示模型数据和该`index`的物品。
注意：视图拥有`widget`的所有权。这意味着如果索引控件A被替换为索引控件B，索引控件A将被删除。例如，在下面的代码片段中，`QLineEdit`对象将被删除。
该函数应仅用于显示对应数据项可见区域内的静态内容。如果你想显示自定义动态内容或实现自定义编辑器小部件，则改用子类`QStyledItemDelegate`。

**官方示例：**

```cpp
 setIndexWidget(index, new QLineEdit);
 ...
 setIndexWidget(index, new QTextEdit);
```

### `void QAbstractItemView::setItemDelegate(QAbstractItemDelegate *delegate)`

**作用与语义：**

将该视图及其模型的项目代理设置为`delegate`。如果你想完全控制项目的编辑和显示，这非常有用。
任何现有代表都会被移除，但不会被删除。`QAbstractItemView`不对`delegate`拥有所有权。
警告：你不应在不同视图之间共享同一个代理实例。这样做可能导致错误或不直观的编辑行为，因为连接到某代理的每个视图都可能收到`closeEditor()`信号，并试图访问、修改或关闭已被关闭的编辑器。

### `void QAbstractItemView::setItemDelegateForColumn(int column, QAbstractItemDelegate *delegate)`

**作用与语义：**

设置该视图和模型在给定的`column`中`delegate`所用的项目。`column`上的所有项目都将由`delegate`绘制和管理，而不是使用默认代理（即`itemDelegate()`）。
任何已有的`column`列代表都会被移除，但不会被删除。`QAbstractItemView`不对`delegate`拥有所有权。
注意：如果代理被分配到行和列，行代理将优先管理交叉单元索引。
警告：你不应在不同视图之间共享同一个代理实例。这样做可能导致错误或不直观的编辑行为，因为连接到某代理的每个视图都可能收到`closeEditor()`信号，并试图访问、修改或关闭已被关闭的编辑器。

### `void QAbstractItemView::setItemDelegateForRow(int row, QAbstractItemDelegate *delegate)`

**作用与语义：**

为该视图和模型对给定`row`设置`delegate`所使用物品。`row`上的所有物品都将由`delegate`绘制和管理，而不是使用默认代理（即`itemDelegate()`）。
任何现有的行`row`代表都会被移除，但不会被删除。`QAbstractItemView`不对`delegate`拥有所有权。
注意：如果代理被分配到行和列，行代理（即该代理）将优先管理交叉单元索引。
警告：您不应在不同视图之间共享同一个代理实例。这样做可能导致错误或不直观的编辑行为，因为连接到某个代理的每个视图都可能收到`closeEditor()`信号，并试图访问、修改或关闭已关闭的编辑器。

### `[virtual] void QAbstractItemView::setModel(QAbstractItemModel *model)`

**作用与语义：**

设定视角呈现的`model`。
该函数将创建并设置新的选择模型，替换之前用`setSelectionModel()`设置的模型。不过，旧的选择模型不会被删除，因为它可能在多个视图之间共享。如果不再需要，建议您删除旧的选择模型。这可以通过以下代码完成：
如果旧模型和旧选择模型都没有父对象，或者它们的父对象是长寿命对象，可能更倾向于调用它们的`deleteLater()`函数来显式删除它们。
视图不会拥有该模型的所有权，除非它是模型的父对象，因为模型可能在多个不同视图之间共享。

**官方示例：**

```cpp
 QItemSelectionModel *m = view->selectionModel();
 view->setModel(new model);
 delete m;
```

### `[virtual slot] void QAbstractItemView::setRootIndex(const QModelIndex &index)`

**作用与语义：**

将根项设置为给定`index`的项。

### `[pure virtual protected] void QAbstractItemView::setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags flags)`

**作用与语义：**

将选择`flags`应用到矩形内或被触及的物品，`rect`。
在实现自己的 itemview 时，setSelection 应调用 `selectionModel()`->select（selection， flags），其中 select 要么是空的 `QModelIndex`，要么是包含所有 `rect` 中元素的 `QItemSelection`。

### `[virtual] void QAbstractItemView::setSelectionModel(QItemSelectionModel *selectionModel)`

**作用与语义：**

将当前选择模型设置为给定的`selectionModel`。
注意，如果你在该函数之后调用`setModel()`，给定的`selectionModel`将被视图创建的替代。
注意：如果旧的选择模型不再需要，应用程序自行删除;即当它不再被其他视图使用时。当其父对象被删除时，这会自动发生。然而，如果它没有父对象，或者父对象是长寿命对象，可能更倾向于调用其`deleteLater()`函数显式删除它。

### `[protected] void QAbstractItemView::setState(QAbstractItemView::State state)`

**作用与语义：**

将项目视图的状态设置为给定的`state`。

### `[virtual] int QAbstractItemView::sizeHintForColumn(int column) const`

**作用与语义：**

返回指定`column`的宽度尺寸提示，若无模型则返回-1。
该函数用于带有水平头部的视图，根据给定`column`的内容查找头部部分的大小提示。

### `QSize QAbstractItemView::sizeHintForIndex(const QModelIndex &index) const`

**作用与语义：**

返回指定`index`项的大小提示，或对无效索引返回无效大小。

### `[virtual] int QAbstractItemView::sizeHintForRow(int row) const`

**作用与语义：**

返回指定`row`的高度尺寸提示，若无模型则返回-1。
返回的高度是根据给定`row`项的大小提示计算的，也就是说，返回的值是所有项中的最大高度。注意，要控制行的高度，必须重新实现`QAbstractItemDelegate::sizeHint()`函数。
该函数用于带有垂直头部的视图，根据给定`row`的内容查找头部部分的大小提示。

### `[virtual protected] void QAbstractItemView::startDrag(Qt::DropActions supportedActions)`

**作用与语义：**

通过调用 drag->exec() 并使用给定的 `supportedActions` 启动拖动。

### `[protected] QAbstractItemView::State QAbstractItemView::state() const`

**作用与语义：**

返回物品视图的状态。

### `[override virtual protected] void QAbstractItemView::timerEvent(QTimerEvent *event)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。
当向控件发送计时器事件时，该函数会以该`event`调用。

### `[slot] void QAbstractItemView::update(const QModelIndex &index)`

**作用与语义：**

更新该`index`所占据的区域。

### `[virtual protected slot] void QAbstractItemView::updateGeometries()`

**作用与语义：**

更新视图子控件的几何体。

### `[pure virtual protected] int QAbstractItemView::verticalOffset() const`

**作用与语义：**

返回视图的垂直偏移量。
在基类中，这是一个纯虚拟函数。

### `[signal] void QAbstractItemView::viewportEntered()`

**作用与语义：**

当鼠标光标进入视口时，会发出该信号。该功能需要启用鼠标追踪。

### `[override virtual protected] bool QAbstractItemView::viewportEvent(QEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::viewportEvent`（QEvent *事件）。
该函数用于处理工具提示和“这是什么？”模式。如果给定的`event`是`QEvent::ToolTip`或`QEvent::WhatsThis`。它会将所有其他事件传递给其基类 ViewportEvent() 处理程序。
如果`event`已被识别和处理，返回`true`;否则，返回`false`。
滚动区域（`viewport()` 小部件）的主事件处理程序。它处理指定的`event`，子类可以调用以提供合理的默认行为。
返回`true`表示事件系统事件已处理，无需进一步处理;否则返回 `false`表示事件应继续传播。
你可以在子类中重新实现这个函数，但我们建议使用专门的事件处理程序。
视口事件的专用处理程序包括：`paintEvent()`、`mousePressEvent()`、`mouseReleaseEvent()`、`mouseDoubleClickEvent()`、`mouseMoveEvent()`、`wheelEvent()`、`dragEnterEvent()`、`dragMoveEvent()`、`dragLeaveEvent()`、`dropEvent()`、`contextMenuEvent()`和`resizeEvent()`。

### `[override virtual protected] QSize QAbstractItemView::viewportSizeHint() const`

**作用与语义：**

重装：`QAbstractScrollArea::viewportSizeHint()` const.
返回视口推荐大小。默认实现返回`viewport()`->`sizeHint()`。注意，大小仅为视口大小，没有可见的滚动条。

### `[pure virtual] QRect QAbstractItemView::visualRect(const QModelIndex &index) const`

**作用与语义：**

返回该物品在视口中`index`的矩形。
如果你的项目显示在多个区域，visualRect 应该返回包含索引的主要区域，而不是索引可能涵盖、触摸或导致绘图的全部区域。
在基类中，这是一个纯虚拟函数。

### `[pure virtual protected] QRegion QAbstractItemView::visualRegionForSelection(const QItemSelection &selection) const`

**作用与语义：**

从视口返回给定`selection`中物品的区域。
在基类中，这是一个纯虚拟函数。

### `enum EditTrigger { NoEditTriggers, CurrentChanged, DoubleClicked, SelectedClicked, EditKeyPressed, …, AllEditTriggers }`

**作用与语义：**

这个枚举描述了将启动项目编辑的动作。
- `QAbstractItemView::NoEditTriggers`：`0`;无法编辑。
- `QAbstractItemView::CurrentChanged`：`1`;当前项目发生变化时，编辑开始。
- `QAbstractItemView::DoubleClicked`：`2`;编辑当双击项目时开始。
- `QAbstractItemView::SelectedClicked`：`4`;点击已选中的项目后开始编辑。
- `QAbstractItemView::EditKeyPressed`：`8`;当平台编辑键被按在某个项目上时，编辑开始。
- `QAbstractItemView::AnyKeyPressed`：`16`;当按下任意键时，编辑开始。
- `QAbstractItemView::AllEditTriggers`：`31`;所有上述操作开始编辑。
EditTriggers 类型是 QFlags 的 typedef<EditTrigger>。它存储 EditTrigger 值的 OR 组合。

### `flags EditTriggers`

**作用与语义：**

这个枚举描述了将启动项目编辑的动作。
- `QAbstractItemView::NoEditTriggers`：`0`;无法编辑。
- `QAbstractItemView::CurrentChanged`：`1`;当前项目发生变化时，编辑开始。
- `QAbstractItemView::DoubleClicked`：`2`;编辑当双击项目时开始。
- `QAbstractItemView::SelectedClicked`：`4`;点击已选中的项目后开始编辑。
- `QAbstractItemView::EditKeyPressed`：`8`;当平台编辑键被按在某个项目上时，编辑开始。
- `QAbstractItemView::AnyKeyPressed`：`16`;当按下任意键时，编辑开始。
- `QAbstractItemView::AllEditTriggers`：`31`;所有上述操作开始编辑。
EditTriggers 类型是 QFlags 的 typedef<EditTrigger>。它存储 EditTrigger 值的 OR 组合。

### `enum ScrollHint { EnsureVisible, PositionAtTop, PositionAtBottom, PositionAtCenter }`

**作用与语义：**

- `QAbstractItemView::EnsureVisible`：`0`;滚动确保物品可见。
- `QAbstractItemView::PositionAtTop`：`1`;滚动将物品定位在视口顶部。
- `QAbstractItemView::PositionAtBottom`：`2`;滚动将物品置于视窗底部。
- `QAbstractItemView::PositionAtCenter`：`3`;滚动将物品置于视窗中央。

### `enum SelectionBehavior { SelectItems, SelectRows, SelectColumns }`

**作用与语义：**

- `QAbstractItemView::SelectItems`：`0`;选择单一物品。
- `QAbstractItemView::SelectRows`：`1`;仅选择行。
- `QAbstractItemView::SelectColumns`：`2`;仅选择列。

### `bool alternatingRowColors() const`

**作用与语义：**

该属性决定是否使用交替颜色绘制背景。
如果该属性`true`，物品背景将使用 `QPalette::Base` 和 `QPalette::AlternateBase` 绘制;否则背景将使用 `QPalette::Base` 颜色绘制。
默认情况下，该属性为`false`。

**如何使用：** 调用 `alternatingRowColors()` 读取当前值；它不会修改应用状态。

### `int autoScrollMargin() const`

**作用与语义：**

该属性表示触发自动滚动时区域的大小。
该属性控制视口边缘触发自动滚动区域的大小。默认值为16像素。

**如何使用：** 调用 `autoScrollMargin()` 读取当前值；它不会修改应用状态。

### `Qt::DropAction defaultDropAction() const`

**作用与语义：**

该属性包含了 QAbstractItemView：:d rag() 默认使用的 drop 动作。
如果该属性未被设置，当支持的动作支持 CopyAction 时，drop 动作是 CopyAction。

**如何使用：** 调用 `defaultDropAction()` 读取当前值；它不会修改应用状态。

### `QAbstractItemView::DragDropMode dragDropMode() const`

**作用与语义：**

该属性包含视图将对拖拽事件的反应。

**如何使用：** 调用 `dragDropMode()` 读取当前值；它不会修改应用状态。

### `bool dragDropOverwriteMode() const`

**作用与语义：**

该属性保留了视图的拖拽行为。
如果其值`true`，所选数据在丢弃时会覆盖现有的项目数据;移动数据则清除该项目。如果其值为`false`，则在丢弃数据时，所选数据将作为新项目插入。当数据被移动时，该项目也会被移除。
默认值为`false`，与`QListView`和`QTreeView`子类相同。而`QTableView`子类则设定为`true`。
注意：这并非为了防止项目被覆盖。模型中标志()的实现应通过不返回`Qt::ItemIsDropEnabled`来实现这一点。

**如何使用：** 调用 `dragDropOverwriteMode()` 读取当前值；它不会修改应用状态。

### `bool dragEnabled() const`

**作用与语义：**

该属性是否支持视图拖拽自身项目，则判定。

**如何使用：** 调用 `dragEnabled()` 读取当前值；它不会修改应用状态。

### `QAbstractItemView::EditTriggers editTriggers() const`

**作用与语义：**

该属性决定哪些动作将启动物品编辑。
该属性是`EditTrigger`定义的一系列标志，并结合 OR 操作符。只有当执行的动作被设置在该属性中时，视图才会启动对项目的编辑。
默认值为：
- `QTableView`：`DoubleClicked`|`AnyKeyPressed`
- 其他视角：`DoubleClicked`|`EditKeyPressed`

**如何使用：** 调用 `editTriggers()` 读取当前值；它不会修改应用状态。

### `bool hasAutoScroll() const`

**作用与语义：**

该属性适用于拖动移动事件中是否启用自动滚动。
如果将该属性设置为 true（默认值），则当用户拖动到视口边缘 16 像素范围内时，`QAbstractItemView` 会自动滚动视图内容。如果当前项目发生变化，则视图会自动滚动以确保当前项目完全可见。
此属性仅在视口接受放置操作时有效。将此属性设置为 false 可关闭自动滚动。

**如何使用：** 调用 `hasAutoScroll()` 读取当前值；它不会修改应用状态。

### `QAbstractItemView::ScrollMode horizontalScrollMode() const`

**作用与语义：**

视图如何横向滚动内容。
该属性控制视图如何横向滚动内容。滚动可以按像素或按项目滚动。默认值来自样式，通过`QStyle::SH_ItemView_ScrollMode`样式提示。

**如何使用：** 调用 `horizontalScrollMode()` 读取当前值；它不会修改应用状态。

### `QSize iconSize() const`

**作用与语义：**

该属性会显示物品图标的大小。
当视图可见时设置该属性，物品会重新排列。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `Qt::MatchFlags keyboardSearchFlags() const`

**作用与语义：**

该属性决定了`keyboardSearch()`默认实现如何将给定字符串与模型数据匹配。
默认值是`Qt::MatchStartsWith|Qt::MatchWrap`。

**如何使用：** 调用 `keyboardSearchFlags()` 读取当前值；它不会修改应用状态。

### `void resetHorizontalScrollMode()`

**作用与语义：**

视图如何横向滚动内容。
该属性控制视图如何横向滚动内容。滚动可以按像素或按项目滚动。默认值来自样式，通过`QStyle::SH_ItemView_ScrollMode`样式提示。

**如何使用：** 调用 `resetHorizontalScrollMode()` 撤销对 `horizontalScrollMode` 的显式覆盖，让它重新采用继承值或默认值。

### `void resetVerticalScrollMode()`

**作用与语义：**

视图如何沿垂直方向滚动内容。
该属性控制视图如何垂直滚动内容。滚动可以按像素或按项目滚动。默认值来自样式，通过`QStyle::SH_ItemView_ScrollMode`样式提示。

**如何使用：** 调用 `resetVerticalScrollMode()` 撤销对 `verticalScrollMode` 的显式覆盖，让它重新采用继承值或默认值。

### `QAbstractItemView::SelectionBehavior selectionBehavior() const`

**作用与语义：**

该属性决定了视图所采用的选择行为。
无论选择是单项、行还是列，都适用该属性。

**如何使用：** 调用 `selectionBehavior()` 读取当前值；它不会修改应用状态。

### `QAbstractItemView::SelectionMode selectionMode() const`

**作用与语义：**

该属性决定了视图在哪种选择模式下运行。
该属性控制用户是否可以选择一个或多个项目，以及在多项目选择中，选择是否必须是连续的项目范围。

**如何使用：** 调用 `selectionMode()` 读取当前值；它不会修改应用状态。

### `void setAlternatingRowColors(bool enable)`

**作用与语义：**

该属性决定是否使用交替颜色绘制背景。
如果该属性`true`，物品背景将使用 `QPalette::Base` 和 `QPalette::AlternateBase` 绘制;否则背景将使用 `QPalette::Base` 颜色绘制。
默认情况下，该属性为`false`。

**如何使用：** 调用 `setAlternatingRowColors(...)` 修改 `alternatingRowColors`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAutoScroll(bool enable)`

**作用与语义：**

该属性适用于拖动移动事件中是否启用自动滚动。
如果将该属性设置为 true（默认值），则当用户拖动到视口边缘 16 像素范围内时，`QAbstractItemView` 会自动滚动视图内容。如果当前项目发生变化，则视图会自动滚动以确保当前项目完全可见。
此属性仅在视口接受放置操作时有效。将此属性设置为 false 可关闭自动滚动。

**如何使用：** 调用 `setAutoScroll(...)` 修改 `autoScroll`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAutoScrollMargin(int margin)`

**作用与语义：**

该属性表示触发自动滚动时区域的大小。
该属性控制视口边缘触发自动滚动区域的大小。默认值为16像素。

**如何使用：** 调用 `setAutoScrollMargin(...)` 修改 `autoScrollMargin`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDefaultDropAction(Qt::DropAction dropAction)`

**作用与语义：**

该属性包含了 QAbstractItemView：:d rag() 默认使用的 drop 动作。
如果该属性未被设置，当支持的动作支持 CopyAction 时，drop 动作是 CopyAction。

**如何使用：** 调用 `setDefaultDropAction(...)` 修改 `defaultDropAction`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDragDropMode(QAbstractItemView::DragDropMode behavior)`

**作用与语义：**

该属性包含视图将对拖拽事件的反应。

**如何使用：** 调用 `setDragDropMode(...)` 修改 `dragDropMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDragDropOverwriteMode(bool overwrite)`

**作用与语义：**

该属性保留了视图的拖拽行为。
如果其值`true`，所选数据在丢弃时会覆盖现有的项目数据;移动数据则清除该项目。如果其值为`false`，则在丢弃数据时，所选数据将作为新项目插入。当数据被移动时，该项目也会被移除。
默认值为`false`，与`QListView`和`QTreeView`子类相同。而`QTableView`子类则设定为`true`。
注意：这并非为了防止项目被覆盖。模型中标志()的实现应通过不返回`Qt::ItemIsDropEnabled`来实现这一点。

**如何使用：** 调用 `setDragDropOverwriteMode(...)` 修改 `dragDropOverwriteMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDragEnabled(bool enable)`

**作用与语义：**

该属性是否支持视图拖拽自身项目，则判定。

**如何使用：** 调用 `setDragEnabled(...)` 修改 `dragEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDropIndicatorShown(bool enable)`

**作用与语义：**

该属性是否在拖曳物品和投放时显示掉落指示器时成立。

**如何使用：** 调用 `setDropIndicatorShown(...)` 修改 `showDropIndicator`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setEditTriggers(QAbstractItemView::EditTriggers triggers)`

**作用与语义：**

该属性决定哪些动作将启动物品编辑。
该属性是`EditTrigger`定义的一系列标志，并结合 OR 操作符。只有当执行的动作被设置在该属性中时，视图才会启动对项目的编辑。
默认值为：
- `QTableView`：`DoubleClicked`|`AnyKeyPressed`
- 其他视角：`DoubleClicked`|`EditKeyPressed`

**如何使用：** 调用 `setEditTriggers(...)` 修改 `editTriggers`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setHorizontalScrollMode(QAbstractItemView::ScrollMode mode)`

**作用与语义：**

视图如何横向滚动内容。
该属性控制视图如何横向滚动内容。滚动可以按像素或按项目滚动。默认值来自样式，通过`QStyle::SH_ItemView_ScrollMode`样式提示。

**如何使用：** 调用 `setHorizontalScrollMode(...)` 修改 `horizontalScrollMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIconSize(const QSize &size)`

**作用与语义：**

该属性会显示物品图标的大小。
当视图可见时设置该属性，物品会重新排列。

**如何使用：** 调用 `setIconSize(...)` 修改 `iconSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setKeyboardSearchFlags(Qt::MatchFlags searchFlags)`

**作用与语义：**

该属性决定了`keyboardSearch()`默认实现如何将给定字符串与模型数据匹配。
默认值是`Qt::MatchStartsWith|Qt::MatchWrap`。

**如何使用：** 调用 `setKeyboardSearchFlags(...)` 修改 `keyboardSearchFlags`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSelectionBehavior(QAbstractItemView::SelectionBehavior behavior)`

**作用与语义：**

该属性决定了视图所采用的选择行为。
无论选择是单项、行还是列，都适用该属性。

**如何使用：** 调用 `setSelectionBehavior(...)` 修改 `selectionBehavior`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSelectionMode(QAbstractItemView::SelectionMode mode)`

**作用与语义：**

该属性决定了视图在哪种选择模式下运行。
该属性控制用户是否可以选择一个或多个项目，以及在多项目选择中，选择是否必须是连续的项目范围。

**如何使用：** 调用 `setSelectionMode(...)` 修改 `selectionMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabKeyNavigation(bool enable)`

**作用与语义：**

该属性决定是否启用了带有标签页和后页的项目导航。

**如何使用：** 调用 `setTabKeyNavigation(...)` 修改 `tabKeyNavigation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTextElideMode(Qt::TextElideMode mode)`

**作用与语义：**

此属性保存省略文本中“...”的位置。
所有项视图的默认值是 `Qt::ElideRight`。

**如何使用：** 调用 `setTextElideMode(...)` 修改 `textElideMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUpdateThreshold(int threshold)`

**作用与语义：**

该属性包含了索引的变化数量，以直接触发`dataChanged()`内视图的全面更新。
`dataChanged()` 内部的算法试图通过计算变更后的索引是否可见，来最小化视图的全面更新。对于非常大的模型，且有大量大变更，这可能比实际更新时间更长，因此适得其反。这一特性使算法能够控制，当变更的索引数量超过给定值时，跳过检查并直接触发完整更新。
默认数值是200。

**如何使用：** 调用 `setUpdateThreshold(...)` 修改 `updateThreshold`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVerticalScrollMode(QAbstractItemView::ScrollMode mode)`

**作用与语义：**

视图如何沿垂直方向滚动内容。
该属性控制视图如何垂直滚动内容。滚动可以按像素或按项目滚动。默认值来自样式，通过`QStyle::SH_ItemView_ScrollMode`样式提示。

**如何使用：** 调用 `setVerticalScrollMode(...)` 修改 `verticalScrollMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool showDropIndicator() const`

**作用与语义：**

该属性是否在拖曳物品和投放时显示掉落指示器时成立。

**如何使用：** 调用 `showDropIndicator()` 读取当前值；它不会修改应用状态。

### `bool tabKeyNavigation() const`

**作用与语义：**

该属性决定是否启用了带有标签页和后页的项目导航。

**如何使用：** 调用 `tabKeyNavigation()` 读取当前值；它不会修改应用状态。

### `Qt::TextElideMode textElideMode() const`

**作用与语义：**

此属性保存省略文本中“...”的位置。
所有项视图的默认值是 `Qt::ElideRight`。

**如何使用：** 调用 `textElideMode()` 读取当前值；它不会修改应用状态。

### `int updateThreshold() const`

**作用与语义：**

该属性包含了索引的变化数量，以直接触发`dataChanged()`内视图的全面更新。
`dataChanged()` 内部的算法试图通过计算变更后的索引是否可见，来最小化视图的全面更新。对于非常大的模型，且有大量大变更，这可能比实际更新时间更长，因此适得其反。这一特性使算法能够控制，当变更的索引数量超过给定值时，跳过检查并直接触发完整更新。
默认数值是200。

**如何使用：** 调用 `updateThreshold()` 读取当前值；它不会修改应用状态。

### `QAbstractItemView::ScrollMode verticalScrollMode() const`

**作用与语义：**

视图如何沿垂直方向滚动内容。
该属性控制视图如何垂直滚动内容。滚动可以按像素或按项目滚动。默认值来自样式，通过`QStyle::SH_ItemView_ScrollMode`样式提示。

**如何使用：** 调用 `verticalScrollMode()` 读取当前值；它不会修改应用状态。

### `void iconSizeChanged(const QSize &size)`

**作用与语义：**

该属性会显示物品图标的大小。
当视图可见时设置该属性，物品会重新排列。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `iconSize` 的变化，不要把它当作普通函数主动调用。

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

`QAbstractItemView` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
