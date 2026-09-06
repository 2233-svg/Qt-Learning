# QMdiArea

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QMdiArea` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QMdiArea` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QMdiArea>`
- 继承自：QAbstractScrollArea
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

### 公有类型

- `enum AreaOption { DontMaximizeSubWindowOnActivation }`
- `flags AreaOptions`
- `enum ViewMode { SubWindowView, TabbedView }`
- `enum WindowOrder { CreationOrder, StackingOrder, ActivationHistoryOrder }`

### 属性

- `activationOrder : WindowOrder`
- `background : QBrush`
- `documentMode : bool`
- `tabPosition : QTabWidget::TabPosition`
- `tabShape : QTabWidget::TabShape`
- `tabsClosable : bool`
- `tabsMovable : bool`
- `viewMode : ViewMode`

### 公有函数

- `QMdiArea(QWidget *parent = nullptr)`
- `virtual ~QMdiArea()`
- `QMdiArea::WindowOrder activationOrder() const`
- `QMdiSubWindow * activeSubWindow() const`
- `QMdiSubWindow * addSubWindow(QWidget *widget, Qt::WindowFlags windowFlags = Qt::WindowFlags())`
- `QBrush background() const`
- `QMdiSubWindow * currentSubWindow() const`
- `bool documentMode() const`
- `void removeSubWindow(QWidget *widget)`
- `void setActivationOrder(QMdiArea::WindowOrder order)`
- `void setBackground(const QBrush &background)`
- `void setDocumentMode(bool enabled)`
- `void setOption(QMdiArea::AreaOption option, bool on = true)`
- `void setTabPosition(QTabWidget::TabPosition position)`
- `void setTabShape(QTabWidget::TabShape shape)`
- `void setTabsClosable(bool closable)`
- `void setTabsMovable(bool movable)`
- `void setViewMode(QMdiArea::ViewMode mode)`
- `QList<QMdiSubWindow *> subWindowList(QMdiArea::WindowOrder order = CreationOrder) const`
- `QTabWidget::TabPosition tabPosition() const`
- `QTabWidget::TabShape tabShape() const`
- `bool tabsClosable() const`
- `bool tabsMovable() const`
- `bool testOption(QMdiArea::AreaOption option) const`
- `QMdiArea::ViewMode viewMode() const`

### 重实现的公有函数

- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void activateNextSubWindow()`
- `void activatePreviousSubWindow()`
- `void cascadeSubWindows()`
- `void closeActiveSubWindow()`
- `void closeAllSubWindows()`
- `void setActiveSubWindow(QMdiSubWindow *window)`
- `void tileSubWindows()`

### 信号

- `void subWindowActivated(QMdiSubWindow *window)`

### 重实现的保护函数

- `virtual void childEvent(QChildEvent *childEvent) override`
- `virtual bool event(QEvent *event) override`
- `virtual bool eventFilter(QObject *object, QEvent *event) override`
- `virtual void paintEvent(QPaintEvent *paintEvent) override`
- `virtual void resizeEvent(QResizeEvent *resizeEvent) override`
- `virtual void scrollContentsBy(int dx, int dy) override`
- `virtual void showEvent(QShowEvent *showEvent) override`
- `virtual void timerEvent(QTimerEvent *timerEvent) override`
- `virtual bool viewportEvent(QEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QMdiArea::AreaOptionflags QMdiArea::AreaOptions`

**作用与语义：**

该枚举描述了自定义`QMdiArea`行为的选项。
- `QMdiArea::DontMaximizeSubWindowOnActivation`：`0x1`;当活跃子窗口被最大化时，默认行为是最大化下一个被激活的子窗口。如果你不希望有此行为，请设置此选项。
AreaOptions 类型是 QFlag 的 typedef<AreaOption>。它存储 AreaOption 值的 OR 组合。

### `enum QMdiArea::ViewMode`

**作用与语义：**

该枚举描述了该区域的视图模式;即子窗口将如何显示。
- `QMdiArea::SubWindowView`：`0`;带有窗框的显示子窗口（默认）。
- `QMdiArea::TabbedView`：`1`;标签栏中带有标签页的子窗口。

### `enum QMdiArea::WindowOrder`

**作用与语义：**

指定了用于排序`subWindowList()`返回子窗口列表的条件。函数 `cascadeSubWindows()` 和 `tileSubWindows()` 在排列窗口时遵循此顺序。
- `QMdiArea::CreationOrder`：`0`;窗户按创建顺序返回。
- `QMdiArea::StackingOrder`：`1`;窗口按堆叠顺序返回，列表中最顶的窗口最后。
- `QMdiArea::ActivationHistoryOrder`：`2`;窗口按激活顺序返回。

### `activationOrder : WindowOrder`

**作用与语义：**

该属性包含子窗口列表的排序标准。
该属性指定了`subWindowList()`返回子窗口列表的排序条件。默认情况下，它是窗口创建顺序。

**如何使用：** 调用 `activationOrder()` 读取当前值；它不会修改应用状态。

### `background : QBrush`

**作用与语义：**

该属性包含工作区的背景画笔。
该属性设置了工作区本身的背景画笔。默认为灰色，但可以是任何画笔（例如颜色、渐变或像素贴图）。

**如何使用：** 调用 `background()` 读取当前值；它不会修改应用状态。

### `documentMode : bool`

**作用与语义：**

该属性在标签页视图模式下是否设置为文档模式时生效。
文档模式默认被禁用。

**如何使用：** 调用 `documentMode()` 读取当前值；它不会修改应用状态。

### `tabPosition : QTabWidget::TabPosition`

**作用与语义：**

此属性保存标签式视图模式下标签的位置。
此属性的可能值由 `QTabWidget::TabPosition` 枚举描述。

**如何使用：** 调用 `tabPosition()` 读取当前值；它不会修改应用状态。

### `tabShape : QTabWidget::TabShape`

**作用与语义：**

该特性在标签视图模式下保持制表表的形状。
该属性的可能值有`QTabWidget::Rounded`（默认）或`QTabWidget::Triangular`。

**如何使用：** 调用 `tabShape()` 读取当前值；它不会修改应用状态。

### `tabsClosable : bool`

**作用与语义：**

该属性决定了在标签视图模式下，标签栏是否应该在每个标签页上放置关闭按钮。
标签页默认是无法关闭的。

**如何使用：** 调用 `tabsClosable()` 读取当前值；它不会修改应用状态。

### `tabsMovable : bool`

**作用与语义：**

该属性决定用户是否可以在标签栏视图模式下移动标签栏区域内的标签页。
标签默认是不可移动的。

**如何使用：** 调用 `tabsMovable()` 读取当前值；它不会修改应用状态。

### `viewMode : ViewMode`

**作用与语义：**

该属性决定了子窗口在`QMdiArea`中显示的方式。
默认情况下，`SubWindowView`用于显示子窗口。

**如何使用：** 调用 `viewMode()` 读取当前值；它不会修改应用状态。

### `QMdiArea::QMdiArea(QWidget *parent = nullptr)`

**作用与语义：**

构造一个空的 MDI 区域。`parent` 传递给 `QWidget` 的构造器。

### `[virtual noexcept] QMdiArea::~QMdiArea()`

**作用与语义：**

摧毁了多层防疫区。

### `[slot] void QMdiArea::activateNextSubWindow()`

**作用与语义：**

它会将键盘聚焦到子窗口列表中的另一个窗口。激活的窗口将根据当前激活顺序决定的下一个窗口。

### `[slot] void QMdiArea::activatePreviousSubWindow()`

**作用与语义：**

它将键盘聚焦到子窗口列表中的另一个窗口。激活的窗口将是当前激活顺序决定的上一个窗口。

### `QMdiSubWindow *QMdiArea::activeSubWindow() const`

**作用与语义：**

返回当前活跃子窗口的指针。如果当前没有窗口处于激活状态，则返回`nullptr`。
子窗口在窗口状态上被视为顶层窗口，即如果MDI区域外的控件是活跃窗口，则没有子窗口处于激活状态。注意，如果MDI所在窗口中的控件获得焦点，该窗口将被激活。

### `QMdiSubWindow *QMdiArea::addSubWindow(QWidget *widget, Qt::WindowFlags windowFlags = Qt::WindowFlags())`

**作用与语义：**

将`widget`作为MDI区域的新子窗口添加。如果`windowFlags`非零，它们会覆盖小部件上设置的标志。
`widget`可以是`QMdiSubWindow`或其他`QWidget`（在这种情况下，MDI区域会创建子窗口，并将`widget`设为内部小部件）。
注意：子窗口添加后，其父窗口将是`QMdiArea`的视口小部件。
当你创建自己的子窗口时，如果你想在关闭 MDI 区域时窗口被删除，必须设置 `Qt::WA_DeleteOnClose` 控件属性。如果不这样做，窗口将被隐藏，MDI 区域不会激活下一个子窗口。
返回添加到MDI区域的`QMdiSubWindow`。

**官方示例：**

```cpp
 QMdiArea mdiArea;
 QMdiSubWindow *subWindow1 = new QMdiSubWindow;
 subWindow1->setWidget(internalWidget1);
 subWindow1->setAttribute(Qt::WA_DeleteOnClose);
 mdiArea.addSubWindow(subWindow1);

 QMdiSubWindow *subWindow2 =
     mdiArea.addSubWindow(internalWidget2);
```

### `[slot] void QMdiArea::cascadeSubWindows()`

**作用与语义：**

将所有子窗户按瀑布排列。

### `[override virtual protected] void QMdiArea::childEvent(QChildEvent *childEvent)`

**作用与语义：**

重实现自：`QObject::childEvent`（QChildEvent *event）。

### `[slot] void QMdiArea::closeActiveSubWindow()`

**作用与语义：**

关闭活跃子窗口。

### `[slot] void QMdiArea::closeAllSubWindows()`

**作用与语义：**

通过向每个窗口发送`QCloseEvent`来关闭所有子窗口。如果 MDI 区域在另一个子窗口关闭时激活该子窗口，你可能会收到`subWindowActivated()`信号。
忽略关闭事件的子窗口将保持开启。

### `QMdiSubWindow *QMdiArea::currentSubWindow() const`

**作用与语义：**

返回当前子窗口的指针，如果没有当前子窗口则返回`nullptr`。
如果包含`QMdiArea`的`QApplication`处于激活状态，该函数返回的效果与`activeSubWindow()`相同。

### `[override virtual protected] bool QMdiArea::event(QEvent *event)`

**作用与语义：**

重装：`QAbstractScrollArea::event`（QEvent *事件）。

### `[override virtual protected] bool QMdiArea::eventFilter(QObject *object, QEvent *event)`

**作用与语义：**

重装：`QObject::eventFilter`（QObject *已观看，QEvent *事件）。

### `[override virtual] QSize QMdiArea::minimumSizeHint() const`

**作用与语义：**

重装：`QAbstractScrollArea::minimumSizeHint()` const.
重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[override virtual protected] void QMdiArea::paintEvent(QPaintEvent *paintEvent)`

**作用与语义：**

重实现自：`QAbstractScrollArea::paintEvent`（QPaintEvent *event）。

### `void QMdiArea::removeSubWindow(QWidget *widget)`

**作用与语义：**

从 MDI 区域移除`widget`。`widget`必须是 `QMdiSubWindow` 或作为子窗口内部控件的控件。注意 `widget` 从未被 `QMdiArea` 实际删除。如果传递一个 `QMdiSubWindow`，其父节点设为 `nullptr`，且该控件会被移除;但如果传递内部控件，子控件设置为 `nullptr`，`QMdiSubWindow`不会被移除。

### `[override virtual protected] void QMdiArea::resizeEvent(QResizeEvent *resizeEvent)`

**作用与语义：**

重实现自：`QAbstractScrollArea::resizeEvent`（QResizeEvent *event）。

### `[override virtual protected] void QMdiArea::scrollContentsBy(int dx, int dy)`

**作用与语义：**

重实现自：`QAbstractScrollArea::scrollContentsBy`（智力 dx，智力 dy）。
当滚动条被移动`dx`、`dy`时调用，因此视口内容应相应滚动。
默认实现只需调用整个`viewport()`的`update()`，子类可以重新实现该处理程序以优化，或者像`QScrollArea`一样移动内容控件。参数`dx`和`dy`是为了方便，让类知道应该滚动多少（比如像素移动时很有用）。你也可以忽略这些值，直接滚动到滚动条指示的位置。
调用该函数进行程序滚动是错误，建议使用滚动条（例如直接调用`QScrollBar::setValue()`）。

### `[slot] void QMdiArea::setActiveSubWindow(QMdiSubWindow *window)`

**作用与语义：**

激活子窗口 `window`。如果`window` `nullptr`，任何当前活跃窗口都会被关闭。

### `void QMdiArea::setOption(QMdiArea::AreaOption option, bool on = true)`

**作用与语义：**

如果`on`为真，则MDI区域`option`启用;否则禁用。请参见每个选项的效果`AreaOption`。

### `[override virtual protected slot] void QMdiArea::setupViewport(QWidget *viewport)`

**作用与语义：**

重实现自：`QAbstractScrollArea::setupViewport`（QWidget *视口）。
`QAbstractScrollArea`在调用`setViewport()`后调用该槽。在`QMdiArea`子类中重构该函数，以在使用前初始化新`viewport`。
该槽位由`QAbstractScrollArea`调用，`setViewport`（`viewport`）被调用。在`QAbstractScrollArea`的子类中重构该函数，以在使用前初始化新`viewport`。

### `[override virtual protected] void QMdiArea::showEvent(QShowEvent *showEvent)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。
该事件处理程序可以在子类中重新实现，以接收传递给 `event` 参数的控件显示事件。
非自发的展示事件会在展示前立即发送到小部件。窗口的自发展示事件则在展示之后交付。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，窗口恢复时自发显示事件。收到自发隐藏事件后，小部件仍被视为`isVisible()`可见。

### `[override virtual] QSize QMdiArea::sizeHint() const`

**作用与语义：**

重装：`QAbstractScrollArea::sizeHint()` const.

### `[signal] void QMdiArea::subWindowActivated(QMdiSubWindow *window)`

**作用与语义：**

`QMdiArea`在`window`激活后才发出该信号。当`window` `nullptr`时，`QMdiArea`刚刚关闭了最后一个活跃窗口，工作区中没有任何活跃窗口。

### `QList<QMdiSubWindow *> QMdiArea::subWindowList(QMdiArea::WindowOrder order = CreationOrder) const`

**作用与语义：**

返回MDI区域内所有子窗口的列表。如果`order`是`CreationOrder`（默认），窗口按插入工作区的顺序排序。如果`order` `StackingOrder`，窗口按堆叠顺序排列，最顶的窗口是列表的最后一项。如果`order` `ActivationHistoryOrder`，则窗口按最近激活历史排列。

### `bool QMdiArea::testOption(QMdiArea::AreaOption option) const`

**作用与语义：**

如果启用`option`，返回`true`;否则返回`false`。

### `[slot] void QMdiArea::tileSubWindows()`

**作用与语义：**

将所有子窗口按瓷砖排列。

### `[override virtual protected] void QMdiArea::timerEvent(QTimerEvent *timerEvent)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。

### `[override virtual protected] bool QMdiArea::viewportEvent(QEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::viewportEvent`（QEvent *事件）。
滚动区域（`viewport()` 控件）的主事件处理程序。它处理指定的`event`，子类可以调用以提供合理的默认行为。
返回`true`表示事件系统事件已处理，无需进一步处理;否则返回`false`表示事件应继续传播。
你可以在子类中重新实现这个函数，但我们建议使用专门的事件处理程序。
视口事件的专用处理程序有：`paintEvent()`、`mousePressEvent()`、`mouseReleaseEvent()`、`mouseDoubleClickEvent()`、`mouseMoveEvent()`、`wheelEvent()`、`dragEnterEvent()`、`dragMoveEvent()`、`dragLeaveEvent()`、`dropEvent()`、`contextMenuEvent()`和`resizeEvent()`。

### `enum AreaOption { DontMaximizeSubWindowOnActivation }`

**作用与语义：**

该枚举描述了自定义`QMdiArea`行为的选项。
- `QMdiArea::DontMaximizeSubWindowOnActivation`：`0x1`;当活跃子窗口被最大化时，默认行为是最大化下一个被激活的子窗口。如果你不希望有此行为，请设置此选项。
AreaOptions 类型是 QFlag 的 typedef<AreaOption>。它存储 AreaOption 值的 OR 组合。

### `flags AreaOptions`

**作用与语义：**

该枚举描述了自定义`QMdiArea`行为的选项。
- `QMdiArea::DontMaximizeSubWindowOnActivation`：`0x1`;当活跃子窗口被最大化时，默认行为是最大化下一个被激活的子窗口。如果你不希望有此行为，请设置此选项。
AreaOptions 类型是 QFlag 的 typedef<AreaOption>。它存储 AreaOption 值的 OR 组合。

### `QMdiArea::WindowOrder activationOrder() const`

**作用与语义：**

该属性包含子窗口列表的排序标准。
该属性指定了`subWindowList()`返回子窗口列表的排序条件。默认情况下，它是窗口创建顺序。

**如何使用：** 调用 `activationOrder()` 读取当前值；它不会修改应用状态。

### `QBrush background() const`

**作用与语义：**

该属性包含工作区的背景画笔。
该属性设置了工作区本身的背景画笔。默认为灰色，但可以是任何画笔（例如颜色、渐变或像素贴图）。

**如何使用：** 调用 `background()` 读取当前值；它不会修改应用状态。

### `bool documentMode() const`

**作用与语义：**

该属性在标签页视图模式下是否设置为文档模式时生效。
文档模式默认被禁用。

**如何使用：** 调用 `documentMode()` 读取当前值；它不会修改应用状态。

### `void setActivationOrder(QMdiArea::WindowOrder order)`

**作用与语义：**

该属性包含子窗口列表的排序标准。
该属性指定了`subWindowList()`返回子窗口列表的排序条件。默认情况下，它是窗口创建顺序。

**如何使用：** 调用 `setActivationOrder(...)` 修改 `activationOrder`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBackground(const QBrush &background)`

**作用与语义：**

该属性包含工作区的背景画笔。
该属性设置了工作区本身的背景画笔。默认为灰色，但可以是任何画笔（例如颜色、渐变或像素贴图）。

**如何使用：** 调用 `setBackground(...)` 修改 `background`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDocumentMode(bool enabled)`

**作用与语义：**

该属性在标签页视图模式下是否设置为文档模式时生效。
文档模式默认被禁用。

**如何使用：** 调用 `setDocumentMode(...)` 修改 `documentMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabPosition(QTabWidget::TabPosition position)`

**作用与语义：**

此属性保存标签式视图模式下标签的位置。
此属性的可能值由 `QTabWidget::TabPosition` 枚举描述。

**如何使用：** 调用 `setTabPosition(...)` 修改 `tabPosition`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabShape(QTabWidget::TabShape shape)`

**作用与语义：**

该特性在标签视图模式下保持制表表的形状。
该属性的可能值有`QTabWidget::Rounded`（默认）或`QTabWidget::Triangular`。

**如何使用：** 调用 `setTabShape(...)` 修改 `tabShape`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabsClosable(bool closable)`

**作用与语义：**

该属性决定了在标签视图模式下，标签栏是否应该在每个标签页上放置关闭按钮。
标签页默认是无法关闭的。

**如何使用：** 调用 `setTabsClosable(...)` 修改 `tabsClosable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabsMovable(bool movable)`

**作用与语义：**

该属性决定用户是否可以在标签栏视图模式下移动标签栏区域内的标签页。
标签默认是不可移动的。

**如何使用：** 调用 `setTabsMovable(...)` 修改 `tabsMovable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setViewMode(QMdiArea::ViewMode mode)`

**作用与语义：**

该属性决定了子窗口在`QMdiArea`中显示的方式。
默认情况下，`SubWindowView`用于显示子窗口。

**如何使用：** 调用 `setViewMode(...)` 修改 `viewMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QTabWidget::TabPosition tabPosition() const`

**作用与语义：**

此属性保存标签式视图模式下标签的位置。
此属性的可能值由 `QTabWidget::TabPosition` 枚举描述。

**如何使用：** 调用 `tabPosition()` 读取当前值；它不会修改应用状态。

### `QTabWidget::TabShape tabShape() const`

**作用与语义：**

该特性在标签视图模式下保持制表表的形状。
该属性的可能值有`QTabWidget::Rounded`（默认）或`QTabWidget::Triangular`。

**如何使用：** 调用 `tabShape()` 读取当前值；它不会修改应用状态。

### `bool tabsClosable() const`

**作用与语义：**

该属性决定了在标签视图模式下，标签栏是否应该在每个标签页上放置关闭按钮。
标签页默认是无法关闭的。

**如何使用：** 调用 `tabsClosable()` 读取当前值；它不会修改应用状态。

### `bool tabsMovable() const`

**作用与语义：**

该属性决定用户是否可以在标签栏视图模式下移动标签栏区域内的标签页。
标签默认是不可移动的。

**如何使用：** 调用 `tabsMovable()` 读取当前值；它不会修改应用状态。

### `QMdiArea::ViewMode viewMode() const`

**作用与语义：**

该属性决定了子窗口在`QMdiArea`中显示的方式。
默认情况下，`SubWindowView`用于显示子窗口。

**如何使用：** 调用 `viewMode()` 读取当前值；它不会修改应用状态。

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

`QMdiArea` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
