# QToolBar

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QToolBar` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QToolBar` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QToolBar>`
- 继承自：QWidget
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

- `allowedAreas : Qt::ToolBarAreas`
- `floatable : bool`
- `floating : bool`
- `iconSize : QSize`
- `movable : bool`
- `orientation : Qt::Orientation`
- `toolButtonStyle : Qt::ToolButtonStyle`

### 公有函数

- `QToolBar(QWidget *parent = nullptr)`
- `QToolBar(const QString &title, QWidget *parent = nullptr)`
- `virtual ~QToolBar()`
- `QAction * actionAt(const QPoint &p) const`
- `QAction * actionAt(int x, int y) const`
- `QAction * addSeparator()`
- `QAction * addWidget(QWidget *widget)`
- `Qt::ToolBarAreas allowedAreas() const`
- `void clear()`
- `QSize iconSize() const`
- `QAction * insertSeparator(QAction *before)`
- `QAction * insertWidget(QAction *before, QWidget *widget)`
- `bool isAreaAllowed(Qt::ToolBarArea area) const`
- `bool isFloatable() const`
- `bool isFloating() const`
- `bool isMovable() const`
- `Qt::Orientation orientation() const`
- `void setAllowedAreas(Qt::ToolBarAreas areas)`
- `void setFloatable(bool floatable)`
- `void setMovable(bool movable)`
- `void setOrientation(Qt::Orientation orientation)`
- `QAction * toggleViewAction() const`
- `Qt::ToolButtonStyle toolButtonStyle() const`
- `QWidget * widgetForAction(QAction *action) const`

### 公有槽函数

- `void setIconSize(const QSize &iconSize)`
- `void setToolButtonStyle(Qt::ToolButtonStyle toolButtonStyle)`

### 信号

- `void actionTriggered(QAction *action)`
- `void allowedAreasChanged(Qt::ToolBarAreas allowedAreas)`
- `void iconSizeChanged(const QSize &iconSize)`
- `void movableChanged(bool movable)`
- `void orientationChanged(Qt::Orientation orientation)`
- `void toolButtonStyleChanged(Qt::ToolButtonStyle toolButtonStyle)`
- `void topLevelChanged(bool topLevel)`
- `void visibilityChanged(bool visible)`

### 重实现的保护函数

- `virtual void actionEvent(QActionEvent *event) override`
- `virtual void changeEvent(QEvent *event) override`
- `virtual bool event(QEvent *event) override`
- `virtual void paintEvent(QPaintEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `allowedAreas : Qt::ToolBarAreas`

**作用与语义：**

工具栏可能放置的区域。
默认是`Qt::AllToolBarAreas`。
这个特性只有在工具栏处于`QMainWindow`时才有意义。

**如何使用：** 调用 `allowedAreas()` 读取当前值；它不会修改应用状态。

### `floatable : bool`

**作用与语义：**

该属性决定工具栏是否可以作为独立窗口拖拽。
默认是真的。

**如何使用：** 调用 `floatable()` 读取当前值；它不会修改应用状态。

### `[read-only] floating : bool`

**作用与语义：**

该属性是否成立工具栏是否为独立窗口。
默认情况下，该属性为`true`。

**如何使用：** 调用 `floating()` 读取当前值；它不会修改应用状态。

### `iconSize : QSize`

**作用与语义：**

工具栏图标的大小。
默认大小由应用程序样式决定，并基于`QStyle::PM_ToolBarIconSize`像素度量。它是图标的最大尺寸。较小的图标不会被放大。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `movable : bool`

**作用与语义：**

该属性适用于用户是否可以在工具栏区域内移动工具栏，或在工具栏区域之间移动。
默认情况下，该属性为`true`。
这个特性只有在工具栏处于`QMainWindow`时才有意义。

**如何使用：** 调用 `movable()` 读取当前值；它不会修改应用状态。

### `orientation : Qt::Orientation`

**作用与语义：**

工具栏的朝向。
默认是`Qt::Horizontal`。
当工具栏由`QMainWindow`管理时，该功能不应使用。如果你想将已添加到主窗口的工具栏移动到另一个`Qt::ToolBarArea`，可以使用`QMainWindow::addToolBar()`或`QMainWindow::insertToolBar()`。

**如何使用：** 调用 `orientation()` 读取当前值；它不会修改应用状态。

### `toolButtonStyle : Qt::ToolButtonStyle`

**作用与语义：**

该属性保留了工具栏按钮的样式。
该属性定义了所有添加为 `QAction` 的工具按钮样式。注意，如果你用 `addWidget()` 方法添加`QToolButton`，它不会获得该按钮样式。
为了让工具按钮的样式符合系统设置，请将此属性设置为`Qt::ToolButtonFollowStyle`。在 Unix 上，桌面环境的用户设置将被使用。在其他平台上，`Qt::ToolButtonFollowStyle` 仅指图标。
默认是`Qt::ToolButtonIconOnly`。

**如何使用：** 调用 `toolButtonStyle()` 读取当前值；它不会修改应用状态。

### `[explicit] QToolBar::QToolBar(QWidget *parent = nullptr)`

**作用与语义：**

构造一个带有给定`parent`的QToolBar。

### `[explicit] QToolBar::QToolBar(const QString &title, QWidget *parent = nullptr)`

**作用与语义：**

用给定的 `parent`构造一个 QToolBar。
给定的窗口`title`标识工具栏，并显示在`QMainWindow`提供的右键菜单中。

### `[virtual noexcept] QToolBar::~QToolBar()`

**作用与语义：**

会毁掉工具栏。

### `QAction *QToolBar::actionAt(const QPoint &p) const`

**作用与语义：**

返回点`p`的动作。如果未找到动作，该函数返回零。

### `QAction *QToolBar::actionAt(int x, int y) const`

**作用与语义：**

返回点`x` `y`的动作。如果未找到动作，该函数返回零。

### `[override virtual protected] void QToolBar::actionEvent(QActionEvent *event)`

**作用与语义：**

重实现自：`QWidget::actionEvent`（QActionEvent *event）。
每当控件的动作发生变化时，该事件处理程序都会被调用给定的`event`。

### `[signal] void QToolBar::actionTriggered(QAction *action)`

**作用与语义：**

当该工具栏中的动作被触发时，该信号会发出。当该动作的工具按钮被按下时，或该动作以工具栏外的其他方式触发时，就会发出该信号。参数中保留了触发的`action`。

### `QAction *QToolBar::addSeparator()`

**作用与语义：**

在工具栏末端加了一个分隔符。

### `QAction *QToolBar::addWidget(QWidget *widget)`

**作用与语义：**

将给定的`widget`添加到工具栏，作为工具栏的最后一项。
工具栏负责`widget`。
如果你用这种方法添加`QToolButton`，工具栏的`Qt::ToolButtonStyle`将不会被尊重。
注意：你应该用`QAction::setVisible()`来更改小部件的可见性。使用`QWidget::setVisible()`、`QWidget::show()`和`QWidget::hide()`功能是无效的。

### `[signal] void QToolBar::allowedAreasChanged(Qt::ToolBarAreas allowedAreas)`

**作用与语义：**

工具栏可能放置的区域。
默认是`Qt::AllToolBarAreas`。
这个特性只有在工具栏处于`QMainWindow`时才有意义。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `allowedAreas` 的变化，不要把它当作普通函数主动调用。

### `[override virtual protected] void QToolBar::changeEvent(QEvent *event)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `void QToolBar::clear()`

**作用与语义：**

工具栏中的所有动作都被移除。

### `[override virtual protected] bool QToolBar::event(QEvent *event)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[signal] void QToolBar::iconSizeChanged(const QSize &iconSize)`

**作用与语义：**

工具栏图标的大小。
默认大小由应用程序样式决定，并基于`QStyle::PM_ToolBarIconSize`像素度量。它是图标的最大尺寸。较小的图标不会被放大。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `iconSize` 的变化，不要把它当作普通函数主动调用。

### `QAction *QToolBar::insertSeparator(QAction *before)`

**作用与语义：**

在工具栏前方插入一个分隔符，位于与`before`动作相关的工具栏项目前方。

### `QAction *QToolBar::insertWidget(QAction *before, QWidget *widget)`

**作用与语义：**

将给定的`widget`插入到与`before`动作相关的工具栏项目前。
注意：你应该用`QAction::setVisible()`来更改小部件的可见性。使用`QWidget::setVisible()`、`QWidget::show()`和`QWidget::hide()`功能是无效的。

### `bool QToolBar::isAreaAllowed(Qt::ToolBarArea area) const`

**作用与语义：**

如果此工具栏可以停靠在给定的 `area` 中，则返回 `true`；否则返回 `false`。

### `[signal] void QToolBar::movableChanged(bool movable)`

**作用与语义：**

该属性适用于用户是否可以在工具栏区域内移动工具栏，或在工具栏区域之间移动。
默认情况下，该属性为`true`。
这个特性只有在工具栏处于`QMainWindow`时才有意义。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `movable` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QToolBar::orientationChanged(Qt::Orientation orientation)`

**作用与语义：**

工具栏的朝向。
默认是`Qt::Horizontal`。
当工具栏由`QMainWindow`管理时，该功能不应使用。如果你想将已添加到主窗口的工具栏移动到另一个`Qt::ToolBarArea`，可以使用`QMainWindow::addToolBar()`或`QMainWindow::insertToolBar()`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `orientation` 的变化，不要把它当作普通函数主动调用。

### `[override virtual protected] void QToolBar::paintEvent(QPaintEvent *event)`

**作用与语义：**

重实现自：`QWidget::paintEvent`（QPaintEvent *event）。
该事件处理程序可以在子类中重新实现，以接收 `event` 传递的绘画事件。
绘图事件是请求重新绘制一个小部件的全部或部分。它可能由以下原因之一发生：
- `repaint()`或`update()`被援引，
- 小部件被遮挡，现已被发现，或
- 还有很多其他原因。
许多控件可以在被要求时重新绘制整个表面，但一些慢速控件需要通过仅绘制请求的区域来优化：`QPaintEvent::region()`。这种速度优化不会改变结果，因为在事件处理过程中绘制会被裁剪到该区域。例如，`QListView`和`QTableView`就是这样做的。
Qt 还试图通过将多个绘画事件合并为一个来加快绘画速度。当 `update()` 被多次调用或窗口系统发送多个绘画事件时，Qt 会将这些事件合并为一个区域更大的事件（参见 `QRegion::united()`）。`repaint()` 函数不支持这种优化，因此我们建议尽可能使用 `update()`。
当绘制事件发生时，更新区域通常已经被擦除，所以你是在小部件的背景上作画。
背景可以用`setBackgroundRole()`和`setPalette()`设置。
自 Qt 4.0 起，`QWidget` 会自动双缓冲绘制，因此无需在 paintEvent() 中编写双缓冲代码以避免闪烁。
注意：通常，你应避免在paintEvent()中调用`update()`或`repaint()`。例如，在paintEvent()中调用`update()`或`repaint()`会导致行为未定义;孩子可能会或不会获得绘画事件。
警告：如果你使用没有 Qt backingstore 的自定义绘图引擎，`Qt::WA_PaintOnScreen`必须设置。否则，`QWidget::paintEngine()` 永远不会被调用;Backingstore 将被使用。

### `QAction *QToolBar::toggleViewAction() const`

**作用与语义：**

返回一个可检查的操作，可用于显示或隐藏该工具栏。
动作的文本被设置为工具栏的窗口标题。

### `[signal] void QToolBar::toolButtonStyleChanged(Qt::ToolButtonStyle toolButtonStyle)`

**作用与语义：**

该属性保留了工具栏按钮的样式。
该属性定义了所有添加为 `QAction` 的工具按钮样式。注意，如果你用 `addWidget()` 方法添加`QToolButton`，它不会获得该按钮样式。
为了让工具按钮的样式符合系统设置，请将此属性设置为`Qt::ToolButtonFollowStyle`。在 Unix 上，桌面环境的用户设置将被使用。在其他平台上，`Qt::ToolButtonFollowStyle` 仅指图标。
默认是`Qt::ToolButtonIconOnly`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `toolButtonStyle` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QToolBar::topLevelChanged(bool topLevel)`

**作用与语义：**

当`floating`属性发生变化时，该信号会发出。如果工具栏现在处于浮点状态，`topLevel`参数为真;否则为假。

### `[signal] void QToolBar::visibilityChanged(bool visible)`

**作用与语义：**

当工具栏变`visible`（或不可见）时，会发出这个信号。当控件被隐藏或显示时，就会发生这种情况。

### `QWidget *QToolBar::widgetForAction(QAction *action) const`

**作用与语义：**

返回与指定`action`关联的小部件。

### `Qt::ToolBarAreas allowedAreas() const`

**作用与语义：**

工具栏可能放置的区域。
默认是`Qt::AllToolBarAreas`。
这个特性只有在工具栏处于`QMainWindow`时才有意义。

**如何使用：** 调用 `allowedAreas()` 读取当前值；它不会修改应用状态。

### `QSize iconSize() const`

**作用与语义：**

工具栏图标的大小。
默认大小由应用程序样式决定，并基于`QStyle::PM_ToolBarIconSize`像素度量。它是图标的最大尺寸。较小的图标不会被放大。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `bool isFloatable() const`

**作用与语义：**

该属性决定工具栏是否可以作为独立窗口拖拽。
默认是真的。

**如何使用：** 调用 `isFloatable()` 读取当前值；它不会修改应用状态。

### `bool isFloating() const`

**作用与语义：**

该属性是否成立工具栏是否为独立窗口。
默认情况下，该属性为`true`。

**如何使用：** 调用 `isFloating()` 读取当前值；它不会修改应用状态。

### `bool isMovable() const`

**作用与语义：**

该属性适用于用户是否可以在工具栏区域内移动工具栏，或在工具栏区域之间移动。
默认情况下，该属性为`true`。
这个特性只有在工具栏处于`QMainWindow`时才有意义。

**如何使用：** 调用 `isMovable()` 读取当前值；它不会修改应用状态。

### `Qt::Orientation orientation() const`

**作用与语义：**

工具栏的朝向。
默认是`Qt::Horizontal`。
当工具栏由`QMainWindow`管理时，该功能不应使用。如果你想将已添加到主窗口的工具栏移动到另一个`Qt::ToolBarArea`，可以使用`QMainWindow::addToolBar()`或`QMainWindow::insertToolBar()`。

**如何使用：** 调用 `orientation()` 读取当前值；它不会修改应用状态。

### `void setAllowedAreas(Qt::ToolBarAreas areas)`

**作用与语义：**

工具栏可能放置的区域。
默认是`Qt::AllToolBarAreas`。
这个特性只有在工具栏处于`QMainWindow`时才有意义。

**如何使用：** 调用 `setAllowedAreas(...)` 修改 `allowedAreas`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFloatable(bool floatable)`

**作用与语义：**

该属性决定工具栏是否可以作为独立窗口拖拽。
默认是真的。

**如何使用：** 调用 `setFloatable(...)` 修改 `floatable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMovable(bool movable)`

**作用与语义：**

该属性适用于用户是否可以在工具栏区域内移动工具栏，或在工具栏区域之间移动。
默认情况下，该属性为`true`。
这个特性只有在工具栏处于`QMainWindow`时才有意义。

**如何使用：** 调用 `setMovable(...)` 修改 `movable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOrientation(Qt::Orientation orientation)`

**作用与语义：**

工具栏的朝向。
默认是`Qt::Horizontal`。
当工具栏由`QMainWindow`管理时，该功能不应使用。如果你想将已添加到主窗口的工具栏移动到另一个`Qt::ToolBarArea`，可以使用`QMainWindow::addToolBar()`或`QMainWindow::insertToolBar()`。

**如何使用：** 调用 `setOrientation(...)` 修改 `orientation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `Qt::ToolButtonStyle toolButtonStyle() const`

**作用与语义：**

该属性保留了工具栏按钮的样式。
该属性定义了所有添加为 `QAction` 的工具按钮样式。注意，如果你用 `addWidget()` 方法添加`QToolButton`，它不会获得该按钮样式。
为了让工具按钮的样式符合系统设置，请将此属性设置为`Qt::ToolButtonFollowStyle`。在 Unix 上，桌面环境的用户设置将被使用。在其他平台上，`Qt::ToolButtonFollowStyle` 仅指图标。
默认是`Qt::ToolButtonIconOnly`。

**如何使用：** 调用 `toolButtonStyle()` 读取当前值；它不会修改应用状态。

### `void setIconSize(const QSize &iconSize)`

**作用与语义：**

工具栏图标的大小。
默认大小由应用程序样式决定，并基于`QStyle::PM_ToolBarIconSize`像素度量。它是图标的最大尺寸。较小的图标不会被放大。

**如何使用：** 调用 `setIconSize(...)` 修改 `iconSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setToolButtonStyle(Qt::ToolButtonStyle toolButtonStyle)`

**作用与语义：**

该属性保留了工具栏按钮的样式。
该属性定义了所有添加为 `QAction` 的工具按钮样式。注意，如果你用 `addWidget()` 方法添加`QToolButton`，它不会获得该按钮样式。
为了让工具按钮的样式符合系统设置，请将此属性设置为`Qt::ToolButtonFollowStyle`。在 Unix 上，桌面环境的用户设置将被使用。在其他平台上，`Qt::ToolButtonFollowStyle` 仅指图标。
默认是`Qt::ToolButtonIconOnly`。

**如何使用：** 调用 `setToolButtonStyle(...)` 修改 `toolButtonStyle`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QToolBar` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
