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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 158 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QAbstractItemView::CursorAction`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QAbstractItemView` 暴露的类型声明 `Cursor、Action`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:CursorAction`。
- 属性名：`QAbstractItemView`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QAbstractItemView::DragDropMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QAbstractItemView` 暴露的类型声明 `Drag、Drop、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:DragDropMode`。
- 属性名：`QAbstractItemView`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QAbstractItemView::DropIndicatorPosition`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QAbstractItemView` 暴露的类型声明 `Drop、Indicator、Position`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:DropIndicatorPosition`。
- 属性名：`QAbstractItemView`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QAbstractItemView::EditTriggerflags QAbstractItemView::EditTriggers`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QAbstractItemView` 暴露的类型声明 `Edit、Triggerflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:EditTriggerflags QAbstractItemView::EditTriggers`。
- 属性名：`QAbstractItemView`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QAbstractItemView::ScrollMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QAbstractItemView` 暴露的类型声明 `Scroll、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ScrollMode`。
- 属性名：`QAbstractItemView`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QAbstractItemView::SelectionMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QAbstractItemView` 暴露的类型声明 `Selection、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SelectionMode`。
- 属性名：`QAbstractItemView`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QAbstractItemView::State`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QAbstractItemView` 暴露的类型声明 `State`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:State`。
- 属性名：`QAbstractItemView`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `alternatingRowColors : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setAlternatingRowColors(...)` 设置，之后用 `alternatingRowColors()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`alternatingRowColors`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `autoScroll : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setAutoScroll(...)` 设置，之后用 `autoScroll()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`autoScroll`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `autoScrollMargin : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setAutoScrollMargin(...)` 设置，之后用 `autoScrollMargin()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`autoScrollMargin`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `defaultDropAction : Qt::DropAction`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setDropAction(...)` 设置，之后用 `DropAction()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::DropAction`。
- 属性名：`defaultDropAction`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `dragDropMode : DragDropMode`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setDragDropMode(...)` 设置，之后用 `dragDropMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`DragDropMode`。
- 属性名：`dragDropMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `dragDropOverwriteMode : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setDragDropOverwriteMode(...)` 设置，之后用 `dragDropOverwriteMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`dragDropOverwriteMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `dragEnabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setDragEnabled(...)` 设置，之后用 `dragEnabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`dragEnabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `editTriggers : EditTriggers`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setEditTriggers(...)` 设置，之后用 `editTriggers()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`EditTriggers`。
- 属性名：`editTriggers`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `horizontalScrollMode : ScrollMode`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setHorizontalScrollMode(...)` 设置，之后用 `horizontalScrollMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`ScrollMode`。
- 属性名：`horizontalScrollMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `iconSize : QSize`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setIconSize(...)` 设置，之后用 `iconSize()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSize`。
- 属性名：`iconSize`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] keyboardSearchFlags : Qt::MatchFlags`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setMatchFlags(...)` 设置，之后用 `MatchFlags()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::MatchFlags`。
- 属性名：`keyboardSearchFlags`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `selectionBehavior : SelectionBehavior`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setSelectionBehavior(...)` 设置，之后用 `selectionBehavior()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`SelectionBehavior`。
- 属性名：`selectionBehavior`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `selectionMode : SelectionMode`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setSelectionMode(...)` 设置，之后用 `selectionMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`SelectionMode`。
- 属性名：`selectionMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `showDropIndicator : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setShowDropIndicator(...)` 设置，之后用 `showDropIndicator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`showDropIndicator`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `tabKeyNavigation : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setTabKeyNavigation(...)` 设置，之后用 `tabKeyNavigation()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`tabKeyNavigation`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `textElideMode : Qt::TextElideMode`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setTextElideMode(...)` 设置，之后用 `TextElideMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::TextElideMode`。
- 属性名：`textElideMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] updateThreshold : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setUpdateThreshold(...)` 设置，之后用 `updateThreshold()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`updateThreshold`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `verticalScrollMode : ScrollMode`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractItemView` 的配置属性。初始化或状态切换时通过 `setVerticalScrollMode(...)` 设置，之后用 `verticalScrollMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`ScrollMode`。
- 属性名：`verticalScrollMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QAbstractItemView::QAbstractItemView(QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractItemView` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QAbstractItemView::~QAbstractItemView()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractItemView` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QAbstractItemView::activated(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractItemView` 发出的通知信号 `activated`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QAbstractItemView::clearSelection()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `clearSelection`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QAbstractItemView::clicked(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractItemView` 发出的通知信号 `clicked`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected slot] void QAbstractItemView::closeEditor(QWidget *editor, QAbstractItemDelegate::EndEditHint hint)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `closeEditor`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `editor`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `hint`：类型为 `QAbstractItemDelegate::EndEditHint`。没有默认值，调用时必须提供。传入 `QAbstractItemDelegate::EndEditHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractItemView::closePersistentEditor(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `closePersistentEditor`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected slot] void QAbstractItemView::commitData(QWidget *editor)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::commitData` 用于执行与“提交、数据访问”相关的操作。调用时要先确认当前状态和 `editor` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `editor`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected slot] void QAbstractItemView::currentChanged(const QModelIndex &current, const QModelIndex &previous)`

**API 类别：** 成员函数说明

**中文解读：** 这是状态变化通知 `currentChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `current`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。
- 参数 `previous`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QModelIndex QAbstractItemView::currentIndex() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::currentIndex` 用于计算、查询或取得与“当前、索引”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected slot] void QAbstractItemView::dataChanged(const QModelIndex &topLeft, const QModelIndex &bottomRight, const QList<int> &roles = QList<int>())`

**API 类别：** 成员函数说明

**中文解读：** 这是状态变化通知 `dataChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `topLeft`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。
- 参数 `bottomRight`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。
- 参数 `roles`：类型为 `const QList<int> &`。默认值为 `QList<int>()`。传入 `const QList<int> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] QPoint QAbstractItemView::dirtyRegionOffset() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::dirtyRegionOffset` 用于计算、查询或取得与“dirty、Region、Offset”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPoint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPoint`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QAbstractItemView::doubleClicked(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractItemView` 发出的通知信号 `doubleClicked`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::dragEnterEvent(QDragEnterEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::dragEnterEvent` 用于执行与“drag、Enter、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDragEnterEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::dragLeaveEvent(QDragLeaveEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::dragLeaveEvent` 用于执行与“drag、Leave、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDragLeaveEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::dragMoveEvent(QDragMoveEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::dragMoveEvent` 用于执行与“drag、移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDragMoveEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::dropEvent(QDropEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::dropEvent` 用于执行与“drop、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDropEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] QAbstractItemView::DropIndicatorPosition QAbstractItemView::dropIndicatorPosition() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::dropIndicatorPosition` 用于计算、查询或取得与“drop、Indicator、Position”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemView::DropIndicatorPosition`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemView::DropIndicatorPosition`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QAbstractItemView::edit(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `edit`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] bool QAbstractItemView::edit(const QModelIndex &index, QAbstractItemView::EditTrigger trigger, QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::edit` 用于计算、查询或取得与“edit”相关的操作。调用时要先确认当前状态和 `index`、`trigger`、`event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `trigger`：类型为 `QAbstractItemView::EditTrigger`。没有默认值，调用时必须提供。传入 `QAbstractItemView::EditTrigger` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected slot] void QAbstractItemView::editorDestroyed(QObject *editor)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::editorDestroyed` 用于执行与“editor、Destroyed”相关的操作。调用时要先确认当前状态和 `editor` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `editor`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QAbstractItemView::entered(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractItemView` 发出的通知信号 `entered`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QAbstractItemView::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QAbstractItemView::eventFilter(QObject *object, QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::eventFilter` 用于计算、查询或取得与“event、Filter”相关的操作。调用时要先确认当前状态和 `object`、`event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QAbstractItemView::executeDelayedItemsLayout()`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::executeDelayedItemsLayout` 用于执行与“execute、Delayed、Items、Layout”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::focusInEvent(QFocusEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::focusInEvent` 用于执行与“focus、In、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QAbstractItemView::focusNextPrevChild(bool next)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::focusNextPrevChild` 用于计算、查询或取得与“focus、移动到下一项、Prev、Child”相关的操作。调用时要先确认当前状态和 `next` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `next`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::focusOutEvent(QFocusEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::focusOutEvent` 用于执行与“focus、Out、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual protected] int QAbstractItemView::horizontalOffset() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::horizontalOffset` 用于计算、查询或取得与“水平、Offset”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QModelIndex QAbstractItemView::indexAt(const QPoint &point) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::indexAt` 用于计算、查询或取得与“索引、按位置访问”相关的操作。调用时要先确认当前状态和 `point` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `point`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QAbstractItemView::indexWidget(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::indexWidget` 用于计算、查询或取得与“索引、Widget”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected, since 6.0] void QAbstractItemView::initViewItemOption(QStyleOptionViewItem *option) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::initViewItemOption` 用于执行与“init、View、项目访问、Option”相关的操作。调用时要先确认当前状态和 `option` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `option`：类型为 `QStyleOptionViewItem *`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::inputMethodEvent(QInputMethodEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::inputMethodEvent` 用于执行与“input、Method、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QInputMethodEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QVariant QAbstractItemView::inputMethodQuery(Qt::InputMethodQuery query) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::inputMethodQuery` 用于计算、查询或取得与“input、Method、查询”相关的操作。调用时要先确认当前状态和 `query` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `query`：类型为 `Qt::InputMethodQuery`。没有默认值，调用时必须提供。传入 `Qt::InputMethodQuery` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual protected] bool QAbstractItemView::isIndexHidden(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isIndexHidden`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QAbstractItemView::isPersistentEditorOpen(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isPersistentEditorOpen`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractItemDelegate *QAbstractItemView::itemDelegate() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::itemDelegate` 用于计算、查询或取得与“项目访问、Delegate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemDelegate *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemDelegate *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractItemDelegate *QAbstractItemView::itemDelegateForColumn(int column) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::itemDelegateForColumn` 用于计算、查询或取得与“项目访问、Delegate、For、列”相关的操作。调用时要先确认当前状态和 `column` 的有效范围；返回类型是 `QAbstractItemDelegate *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemDelegate *`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual, since 6.0] QAbstractItemDelegate *QAbstractItemView::itemDelegateForIndex(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::itemDelegateForIndex` 用于计算、查询或取得与“项目访问、Delegate、For、索引”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QAbstractItemDelegate *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemDelegate *`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractItemDelegate *QAbstractItemView::itemDelegateForRow(int row) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::itemDelegateForRow` 用于计算、查询或取得与“项目访问、Delegate、For、行”相关的操作。调用时要先确认当前状态和 `row` 的有效范围；返回类型是 `QAbstractItemDelegate *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemDelegate *`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::keyPressEvent(QKeyEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::keyPressEvent` 用于执行与“key、Press、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QAbstractItemView::keyboardSearch(const QString &search)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::keyboardSearch` 用于执行与“keyboard、Search”相关的操作。调用时要先确认当前状态和 `search` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `search`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractItemModel *QAbstractItemView::model() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::model` 用于计算、查询或取得与“model”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemModel *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemModel *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::mouseDoubleClickEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::mouseDoubleClickEvent` 用于执行与“mouse、Double、Click、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::mouseMoveEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::mouseMoveEvent` 用于执行与“mouse、移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::mousePressEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::mousePressEvent` 用于执行与“mouse、Press、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::mouseReleaseEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::mouseReleaseEvent` 用于执行与“mouse、释放、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual protected] QModelIndex QAbstractItemView::moveCursor(QAbstractItemView::CursorAction cursorAction, Qt::KeyboardModifiers modifiers)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::moveCursor` 用于计算、查询或取得与“移动、Cursor”相关的操作。调用时要先确认当前状态和 `cursorAction`、`modifiers` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `cursorAction`：类型为 `QAbstractItemView::CursorAction`。没有默认值，调用时必须提供。传入 `QAbstractItemView::CursorAction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `modifiers`：类型为 `Qt::KeyboardModifiers`。没有默认值，调用时必须提供。传入 `Qt::KeyboardModifiers` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractItemView::openPersistentEditor(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `openPersistentEditor`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QAbstractItemView::pressed(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractItemView` 发出的通知信号 `pressed`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual slot] void QAbstractItemView::reset()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `reset`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::resizeEvent(QResizeEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::resizeEvent` 用于执行与“调整尺寸、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QResizeEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QModelIndex QAbstractItemView::rootIndex() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::rootIndex` 用于计算、查询或取得与“root、索引”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected slot] void QAbstractItemView::rowsAboutToBeRemoved(const QModelIndex &parent, int start, int end)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::rowsAboutToBeRemoved` 用于执行与“行、About、转换输出、Be、Removed”相关的操作。调用时要先确认当前状态和 `parent`、`start`、`end` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `parent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `start`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected slot] void QAbstractItemView::rowsInserted(const QModelIndex &parent, int start, int end)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::rowsInserted` 用于执行与“行、Inserted”相关的操作。调用时要先确认当前状态和 `parent`、`start`、`end` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `parent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `start`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QAbstractItemView::scheduleDelayedItemsLayout()`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::scheduleDelayedItemsLayout` 用于执行与“schedule、Delayed、Items、Layout”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QAbstractItemView::scrollDirtyRegion(int dx, int dy)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::scrollDirtyRegion` 用于执行与“scroll、Dirty、Region”相关的操作。调用时要先确认当前状态和 `dx`、`dy` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `dx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dy`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QAbstractItemView::scrollTo(const QModelIndex &index, QAbstractItemView::ScrollHint hint = EnsureVisible)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::scrollTo` 用于执行与“scroll、转换输出”相关的操作。调用时要先确认当前状态和 `index`、`hint` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `hint`：类型为 `QAbstractItemView::ScrollHint`。默认值为 `EnsureVisible`。传入 `QAbstractItemView::ScrollHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QAbstractItemView::scrollToBottom()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `scrollToBottom`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QAbstractItemView::scrollToTop()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `scrollToTop`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual slot] void QAbstractItemView::selectAll()`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::selectAll` 用于执行与“select、All”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] QModelIndexList QAbstractItemView::selectedIndexes() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::selectedIndexes` 用于计算、查询或取得与“selected、Indexes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QModelIndexList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndexList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected slot] void QAbstractItemView::selectionChanged(const QItemSelection &selected, const QItemSelection &deselected)`

**API 类别：** 成员函数说明

**中文解读：** 这是状态变化通知 `selectionChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `selected`：类型为 `const QItemSelection &`。没有默认值，调用时必须提供。传入 `const QItemSelection &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `deselected`：类型为 `const QItemSelection &`。没有默认值，调用时必须提供。传入 `const QItemSelection &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] QItemSelectionModel::SelectionFlags QAbstractItemView::selectionCommand(const QModelIndex &index, const QEvent *event = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::selectionCommand` 用于计算、查询或取得与“selection、Command”相关的操作。调用时要先确认当前状态和 `index`、`event` 的有效范围；返回类型是 `QItemSelectionModel::SelectionFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QItemSelectionModel::SelectionFlags`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `event`：类型为 `const QEvent *`。默认值为 `nullptr`。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QItemSelectionModel *QAbstractItemView::selectionModel() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::selectionModel` 用于计算、查询或取得与“selection、Model”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QItemSelectionModel *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QItemSelectionModel *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QAbstractItemView::setCurrentIndex(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setCurrentIndex`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QAbstractItemView::setDirtyRegion(const QRegion &region)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDirtyRegion`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `region`：类型为 `const QRegion &`。没有默认值，调用时必须提供。传入 `const QRegion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractItemView::setIndexWidget(const QModelIndex &index, QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setIndexWidget`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractItemView::setItemDelegate(QAbstractItemDelegate *delegate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setItemDelegate`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `delegate`：类型为 `QAbstractItemDelegate *`。没有默认值，调用时必须提供。传入 `QAbstractItemDelegate *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractItemView::setItemDelegateForColumn(int column, QAbstractItemDelegate *delegate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setItemDelegateForColumn`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `delegate`：类型为 `QAbstractItemDelegate *`。没有默认值，调用时必须提供。传入 `QAbstractItemDelegate *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractItemView::setItemDelegateForRow(int row, QAbstractItemDelegate *delegate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setItemDelegateForRow`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `delegate`：类型为 `QAbstractItemDelegate *`。没有默认值，调用时必须提供。传入 `QAbstractItemDelegate *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QAbstractItemView::setModel(QAbstractItemModel *model)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setModel`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `model`：类型为 `QAbstractItemModel *`。没有默认值，调用时必须提供。数据模型对象。要确认模型生命周期、线程归属、索引有效期和变化通知协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual slot] void QAbstractItemView::setRootIndex(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRootIndex`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual protected] void QAbstractItemView::setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags flags)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSelection`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRect &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。
- 参数 `flags`：类型为 `QItemSelectionModel::SelectionFlags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QAbstractItemView::setSelectionModel(QItemSelectionModel *selectionModel)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSelectionModel`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `selectionModel`：类型为 `QItemSelectionModel *`。没有默认值，调用时必须提供。传入 `QItemSelectionModel *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QAbstractItemView::setState(QAbstractItemView::State state)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setState`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `state`：类型为 `QAbstractItemView::State`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] int QAbstractItemView::sizeHintForColumn(int column) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::sizeHintForColumn` 用于计算、查询或取得与“尺寸或数量、Hint、For、列”相关的操作。调用时要先确认当前状态和 `column` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize QAbstractItemView::sizeHintForIndex(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::sizeHintForIndex` 用于计算、查询或取得与“尺寸或数量、Hint、For、索引”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] int QAbstractItemView::sizeHintForRow(int row) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::sizeHintForRow` 用于计算、查询或取得与“尺寸或数量、Hint、For、行”相关的操作。调用时要先确认当前状态和 `row` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QAbstractItemView::startDrag(Qt::DropActions supportedActions)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startDrag`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `supportedActions`：类型为 `Qt::DropActions`。没有默认值，调用时必须提供。传入 `Qt::DropActions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] QAbstractItemView::State QAbstractItemView::state() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::state` 用于计算、查询或取得与“state”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemView::State`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemView::State`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractItemView::timerEvent(QTimerEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::timerEvent` 用于执行与“timer、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QTimerEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QAbstractItemView::update(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `update`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `[virtual protected slot] void QAbstractItemView::updateGeometries()`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::updateGeometries` 用于执行与“更新、Geometries”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `[pure virtual protected] int QAbstractItemView::verticalOffset() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::verticalOffset` 用于计算、查询或取得与“垂直、Offset”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QAbstractItemView::viewportEntered()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractItemView` 发出的通知信号 `viewportEntered`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QAbstractItemView::viewportEvent(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::viewportEvent` 用于计算、查询或取得与“viewport、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] QSize QAbstractItemView::viewportSizeHint() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::viewportSizeHint` 用于计算、查询或取得与“viewport、尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QRect QAbstractItemView::visualRect(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::visualRect` 用于计算、查询或取得与“visual、Rect”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual protected] QRegion QAbstractItemView::visualRegionForSelection(const QItemSelection &selection) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractItemView::visualRegionForSelection` 用于计算、查询或取得与“visual、Region、For、Selection”相关的操作。调用时要先确认当前状态和 `selection` 的有效范围；返回类型是 `QRegion`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRegion`。
- 参数 `selection`：类型为 `const QItemSelection &`。没有默认值，调用时必须提供。传入 `const QItemSelection &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum EditTrigger { NoEditTriggers, CurrentChanged, DoubleClicked, SelectedClicked, EditKeyPressed, …, AllEditTriggers }`

**API 类别：** 公有类型

**中文解读：** 这是 `QAbstractItemView` 暴露的类型声明 `Edit、触发`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags EditTriggers`

**API 类别：** 公有类型

**中文解读：** 这是 `QAbstractItemView` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum ScrollHint { EnsureVisible, PositionAtTop, PositionAtBottom, PositionAtCenter }`

**API 类别：** 公有类型

**中文解读：** 这是 `QAbstractItemView` 暴露的类型声明 `Scroll、Hint`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum SelectionBehavior { SelectItems, SelectRows, SelectColumns }`

**API 类别：** 公有类型

**中文解读：** 这是 `QAbstractItemView` 暴露的类型声明 `Selection、Behavior`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool alternatingRowColors() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::alternatingRowColors` 用于计算、查询或取得与“alternating、行、Colors”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int autoScrollMargin() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::autoScrollMargin` 用于计算、查询或取得与“auto、Scroll、Margin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::DropAction defaultDropAction() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::defaultDropAction` 用于计算、查询或取得与“default、Drop、Action”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::DropAction`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::DropAction`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractItemView::DragDropMode dragDropMode() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::dragDropMode` 用于计算、查询或取得与“drag、Drop、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemView::DragDropMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemView::DragDropMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool dragDropOverwriteMode() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::dragDropOverwriteMode` 用于计算、查询或取得与“drag、Drop、Overwrite、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool dragEnabled() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::dragEnabled` 用于计算、查询或取得与“drag、启用状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractItemView::EditTriggers editTriggers() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::editTriggers` 用于计算、查询或取得与“edit、Triggers”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemView::EditTriggers`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemView::EditTriggers`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool hasAutoScroll() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `hasAutoScroll`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractItemView::ScrollMode horizontalScrollMode() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::horizontalScrollMode` 用于计算、查询或取得与“水平、Scroll、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemView::ScrollMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemView::ScrollMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize iconSize() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::iconSize` 用于计算、查询或取得与“icon、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::MatchFlags keyboardSearchFlags() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::keyboardSearchFlags` 用于计算、查询或取得与“keyboard、Search、标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::MatchFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::MatchFlags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void resetHorizontalScrollMode()`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::resetHorizontalScrollMode` 用于执行与“重置、水平、Scroll、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void resetVerticalScrollMode()`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::resetVerticalScrollMode` 用于执行与“重置、垂直、Scroll、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractItemView::SelectionBehavior selectionBehavior() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::selectionBehavior` 用于计算、查询或取得与“selection、Behavior”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemView::SelectionBehavior`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemView::SelectionBehavior`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractItemView::SelectionMode selectionMode() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::selectionMode` 用于计算、查询或取得与“selection、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemView::SelectionMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemView::SelectionMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAlternatingRowColors(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAlternatingRowColors`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAutoScroll(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAutoScroll`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAutoScrollMargin(int margin)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAutoScrollMargin`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `margin`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDefaultDropAction(Qt::DropAction dropAction)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDefaultDropAction`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `dropAction`：类型为 `Qt::DropAction`。没有默认值，调用时必须提供。传入 `Qt::DropAction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDragDropMode(QAbstractItemView::DragDropMode behavior)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDragDropMode`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `behavior`：类型为 `QAbstractItemView::DragDropMode`。没有默认值，调用时必须提供。传入 `QAbstractItemView::DragDropMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDragDropOverwriteMode(bool overwrite)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDragDropOverwriteMode`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `overwrite`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDragEnabled(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDragEnabled`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDropIndicatorShown(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDropIndicatorShown`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setEditTriggers(QAbstractItemView::EditTriggers triggers)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setEditTriggers`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `triggers`：类型为 `QAbstractItemView::EditTriggers`。没有默认值，调用时必须提供。传入 `QAbstractItemView::EditTriggers` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setHorizontalScrollMode(QAbstractItemView::ScrollMode mode)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setHorizontalScrollMode`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QAbstractItemView::ScrollMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setIconSize(const QSize &size)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setIconSize`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setKeyboardSearchFlags(Qt::MatchFlags searchFlags)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setKeyboardSearchFlags`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `searchFlags`：类型为 `Qt::MatchFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSelectionBehavior(QAbstractItemView::SelectionBehavior behavior)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSelectionBehavior`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `behavior`：类型为 `QAbstractItemView::SelectionBehavior`。没有默认值，调用时必须提供。传入 `QAbstractItemView::SelectionBehavior` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSelectionMode(QAbstractItemView::SelectionMode mode)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSelectionMode`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QAbstractItemView::SelectionMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setTabKeyNavigation(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setTabKeyNavigation`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setTextElideMode(Qt::TextElideMode mode)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setTextElideMode`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `Qt::TextElideMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setUpdateThreshold(int threshold)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setUpdateThreshold`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `threshold`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setVerticalScrollMode(QAbstractItemView::ScrollMode mode)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setVerticalScrollMode`。调用它会改变 `QAbstractItemView` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QAbstractItemView::ScrollMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool showDropIndicator() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::showDropIndicator` 用于计算、查询或取得与“显示、Drop、Indicator”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `bool tabKeyNavigation() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::tabKeyNavigation` 用于计算、查询或取得与“tab、Key、Navigation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::TextElideMode textElideMode() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::textElideMode` 用于计算、查询或取得与“文本、Elide、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::TextElideMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::TextElideMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int updateThreshold() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::updateThreshold` 用于计算、查询或取得与“更新、Threshold”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `QAbstractItemView::ScrollMode verticalScrollMode() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractItemView::verticalScrollMode` 用于计算、查询或取得与“垂直、Scroll、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemView::ScrollMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemView::ScrollMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void iconSizeChanged(const QSize &size)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `iconSizeChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
