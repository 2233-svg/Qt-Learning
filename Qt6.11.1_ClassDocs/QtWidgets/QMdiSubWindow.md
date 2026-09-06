# QMdiSubWindow

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QMdiSubWindow` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QMdiSubWindow` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QMdiSubWindow>`
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

### 公有类型

- `enum SubWindowOption { RubberBandResize, RubberBandMove }`
- `flags SubWindowOptions`

### 属性

- `keyboardPageStep : int`
- `keyboardSingleStep : int`

### 公有函数

- `QMdiSubWindow(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`
- `virtual ~QMdiSubWindow()`
- `bool isShaded() const`
- `int keyboardPageStep() const`
- `int keyboardSingleStep() const`
- `QMdiArea * mdiArea() const`
- `void setKeyboardPageStep(int step)`
- `void setKeyboardSingleStep(int step)`
- `void setOption(QMdiSubWindow::SubWindowOption option, bool on = true)`
- `void setSystemMenu(QMenu *systemMenu)`
- `void setWidget(QWidget *widget)`
- `QMenu * systemMenu() const`
- `bool testOption(QMdiSubWindow::SubWindowOption option) const`
- `QWidget * widget() const`

### 重实现的公有函数

- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void showShaded()`
- `void showSystemMenu()`

### 信号

- `void aboutToActivate()`
- `void windowStateChanged(Qt::WindowStates oldState, Qt::WindowStates newState)`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *changeEvent) override`
- `virtual void childEvent(QChildEvent *childEvent) override`
- `virtual void closeEvent(QCloseEvent *closeEvent) override`
- `virtual void contextMenuEvent(QContextMenuEvent *contextMenuEvent) override`
- `virtual bool event(QEvent *event) override`
- `virtual bool eventFilter(QObject *object, QEvent *event) override`
- `virtual void focusInEvent(QFocusEvent *focusInEvent) override`
- `virtual void focusOutEvent(QFocusEvent *focusOutEvent) override`
- `virtual void hideEvent(QHideEvent *hideEvent) override`
- `virtual void keyPressEvent(QKeyEvent *keyEvent) override`
- `virtual void leaveEvent(QEvent *leaveEvent) override`
- `virtual void mouseDoubleClickEvent(QMouseEvent *mouseEvent) override`
- `virtual void mouseMoveEvent(QMouseEvent *mouseEvent) override`
- `virtual void mousePressEvent(QMouseEvent *mouseEvent) override`
- `virtual void mouseReleaseEvent(QMouseEvent *mouseEvent) override`
- `virtual void moveEvent(QMoveEvent *moveEvent) override`
- `virtual void paintEvent(QPaintEvent *paintEvent) override`
- `virtual void resizeEvent(QResizeEvent *resizeEvent) override`
- `virtual void showEvent(QShowEvent *showEvent) override`
- `virtual void timerEvent(QTimerEvent *timerEvent) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QMdiSubWindow::SubWindowOptionflags QMdiSubWindow::SubWindowOptions`

**作用与语义：**

该枚举描述了可以自定义`QMdiSubWindow`行为的选项。
- `QMdiSubWindow::RubberBandResize`：`0x4`;如果你启用此选项，会使用橡皮筋控件来表示子窗口的轮廓，用户可以调整其大小，而不是子窗口本身。因此，子窗口保持其原始位置和大小，直到调整大小操作完成，届时它会收到一个`QResizeEvent`。默认情况下，该选项被禁用。
- `QMdiSubWindow::RubberBandMove`：`0x8`;如果你启用此选项，会用橡皮筋控制来表示子窗口的轮廓，用户移动的是子窗口，而不是子窗口本身。因此，子窗口会保持在原来的位置，直到移动操作完成，届时会向窗口发送`QMoveEvent`。默认情况下，该选项被禁用。
SubWindowOptions 类型是 QFlags 的 typedef<SubWindowOption>。它存储 SubWindowOption 值的 OR 组合。

### `keyboardPageStep : int`

**作用与语义：**

设置使用键盘页面键时，控件的移动或大小。
在键盘交互模式下，您可以使用方向键和页面键来移动或调整窗口大小。该特性控制页面键。进入键盘交互模式的常见方法是进入子窗口菜单，选择“缩小”或“移动”。
默认的键盘页面步长值是20像素。

**如何使用：** 调用 `keyboardPageStep()` 读取当前值；它不会修改应用状态。

### `keyboardSingleStep : int`

**作用与语义：**

设置使用键盘方向键时小部件应移动或调整大小。
在键盘交互模式下，您可以使用方向键和页面键来移动或调整窗口大小。该特性控制方向键。进入键盘交互模式的常见方法是进入子窗口菜单，选择“缩小”或“移动”。
默认的键盘单步数值是5像素。

**如何使用：** 调用 `keyboardSingleStep()` 读取当前值；它不会修改应用状态。

### `QMdiSubWindow::QMdiSubWindow(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`

**作用与语义：**

构造一个新的QMdiSubWindow组件。`parent`和`flags`参数传递给`QWidget`的构造器。
除了使用 addSubWindow()，也可以在`QMdiArea`添加子窗口时直接使用 `setParent()`。
注意，只有 `QMdiSubWindow` 可以设置为 `QMdiArea` 的子节点;例如，你不能写：

**官方示例：**

```cpp
 //bad code
 QMdiArea mdiArea;
 QTextEdit editor(&mdiArea); // invalid child widget
```

### `[virtual noexcept] QMdiSubWindow::~QMdiSubWindow()`

**作用与语义：**

会破坏子窗。

### `[signal] void QMdiSubWindow::aboutToActivate()`

**作用与语义：**

`QMdiSubWindow`在激活前立即发出该信号。子窗口激活后，管理子窗口的`QMdiArea`也会发出`subWindowActivated()`信号。

### `[override virtual protected] void QMdiSubWindow::changeEvent(QEvent *changeEvent)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[override virtual protected] void QMdiSubWindow::childEvent(QChildEvent *childEvent)`

**作用与语义：**

重实现自：`QObject::childEvent`（QChildEvent *event）。

### `[override virtual protected] void QMdiSubWindow::closeEvent(QCloseEvent *closeEvent)`

**作用与语义：**

重实现自：`QWidget::closeEvent`（QCloseEvent *event）。
当 Qt 收到来自窗口系统顶层控件的窗口关闭请求时，该事件处理程序会以该`event`调用。
默认情况下，事件被接受，小部件关闭。你可以重新实现这个函数，改变小部件对窗口关闭请求的响应方式。例如，你可以通过调用所有事件的 `ignore()` 来阻止窗口关闭。
主窗口应用程序通常会重新实现该函数，以检查用户的工作是否已被保存，并在关闭前请求许可。

### `[override virtual protected] void QMdiSubWindow::contextMenuEvent(QContextMenuEvent *contextMenuEvent)`

**作用与语义：**

重实现自：`QWidget::contextMenuEvent`（QContextMenuEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收控件上下文菜单事件。
当控件的 `contextMenuPolicy` `Qt::DefaultContextMenu`时调用处理器。
默认实现忽略上下文事件。详情请参见`QContextMenuEvent`文档。

### `[override virtual protected] bool QMdiSubWindow::event(QEvent *event)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[override virtual protected] bool QMdiSubWindow::eventFilter(QObject *object, QEvent *event)`

**作用与语义：**

重装：`QObject::eventFilter`（QObject *已观看，QEvent *事件）。

### `[override virtual protected] void QMdiSubWindow::focusInEvent(QFocusEvent *focusInEvent)`

**作用与语义：**

重实现自：`QWidget::focusInEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点接收）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] void QMdiSubWindow::focusOutEvent(QFocusEvent *focusOutEvent)`

**作用与语义：**

重现：`QWidget::focusOutEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点丢失）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] void QMdiSubWindow::hideEvent(QHideEvent *hideEvent)`

**作用与语义：**

重实现自：`QWidget::hideEvent`（QHideEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件隐藏事件。事件通过`event`参数传递。
隐藏事件会在小部件被隐藏后立即发送。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，恢复窗口时自发显示事件。收到自发隐藏事件后，小部件仍被视为可见，意义`isVisible()`。

### `bool QMdiSubWindow::isShaded() const`

**作用与语义：**

如果该窗口有阴影，返回`true`;否则返回`false`。
如果窗口被折叠，只显示标题栏，则称为遮蔽。

### `[override virtual protected] void QMdiSubWindow::keyPressEvent(QKeyEvent *keyEvent)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
一个小部件必须调用`setFocusPolicy()`先接受焦点，并且必须有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是 Escape 键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对该键执行时不要调用基类实现即可。

### `[override virtual protected] void QMdiSubWindow::leaveEvent(QEvent *leaveEvent)`

**作用与语义：**

重装：`QWidget::leaveEvent`（QEvent *事件）。
该事件处理程序可以被子类重新实现，以接收通过 `event` 参数传递的控件离开事件。
当鼠标光标离开控件时，会向控件发送一个离开事件。

### `QMdiArea *QMdiSubWindow::mdiArea() const`

**作用与语义：**

返回包含该子窗口的区域，若无则返回`nullptr`。

### `[override virtual] QSize QMdiSubWindow::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[override virtual protected] void QMdiSubWindow::mouseDoubleClickEvent(QMouseEvent *mouseEvent)`

**作用与语义：**

重实现自：`QWidget::mouseDoubleClickEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收小部件的鼠标双击事件。
默认实现调用`mousePressEvent()`。
注意：该小部件除了双击事件外，还会接收鼠标按键和鼠标释放事件。如果与该小部件重叠的其他小部件在新闻发布事件后消失，则该小部件只会接收双击事件。开发者有责任确保应用程序正确解读这些事件。

### `[override virtual protected] void QMdiSubWindow::mouseMoveEvent(QMouseEvent *mouseEvent)`

**作用与语义：**

重实现自：`QWidget::mouseMoveEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标移动事件。
如果关闭鼠标追踪，只有在鼠标移动过程中按下鼠标按钮时才会发生鼠标移动事件。如果开启鼠标追踪，即使未按键，鼠标移动事件也会发生。
`QMouseEvent::position()`报告鼠标光标相对于该小部件的位置。对于按下和释放事件，位置通常与最后一次鼠标移动事件的位置相同，但如果用户的手握手，可能会有所不同。这是底层窗口系统的功能，而非Qt。
如果你想在鼠标移动时立即显示提示（例如，获取鼠标坐标与`QMouseEvent::position()`并显示为提示），你必须先启用上述的鼠标追踪功能。然后，为了确保提示立即更新，你必须在鼠标移动事件（mouseMoveEvent）实现中调用`QToolTip::showText()`而不是`setToolTip()`。

### `[override virtual protected] void QMdiSubWindow::mousePressEvent(QMouseEvent *mouseEvent)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[override virtual protected] void QMdiSubWindow::mouseReleaseEvent(QMouseEvent *mouseEvent)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标释放事件。

### `[override virtual protected] void QMdiSubWindow::moveEvent(QMoveEvent *moveEvent)`

**作用与语义：**

重实现自：`QWidget::moveEvent`（QMoveEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件移动事件。当控件接收该事件时，它已经处于新位置。
旧职位可通过`QMoveEvent::oldPos()`进入。

### `[override virtual protected] void QMdiSubWindow::paintEvent(QPaintEvent *paintEvent)`

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

### `[override virtual protected] void QMdiSubWindow::resizeEvent(QResizeEvent *resizeEvent)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
警告：在最大化或恢复子窗口时，对该函数的调用可能有无效`QResizeEvent::oldSize()`。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件调整大小事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `void QMdiSubWindow::setOption(QMdiSubWindow::SubWindowOption option, bool on = true)`

**作用与语义：**

如果`on`为真，子窗口`option`启用;否则禁用。请参见`SubWindowOption`，了解每个选项的影响。

### `void QMdiSubWindow::setSystemMenu(QMenu *systemMenu)`

**作用与语义：**

将`systemMenu`设置为该子窗口当前的系统菜单。
默认情况下，每个`QMdiSubWindow`都有标准的系统菜单。
`QMdiSubWindow`创建的系统菜单的QAction会根据当前窗口状态自动更新;例如，最小化操作在窗口最小化后会被禁用。
用户添加的QAction不会被`QMdiSubWindow`更新。
`QMdiSubWindow`拥有`systemMenu`;你不必删除它。所有现有菜单都会被删除。

### `void QMdiSubWindow::setWidget(QWidget *widget)`

**作用与语义：**

将`widget`设置为该子窗口的内部控件。内部控件显示在子窗口的标题栏下方中央。
`QMdiSubWindow`会暂时拥有`widget`;你不必删除它。任何现有的内部小部件都会被移除并重新子系到根窗口。

### `[override virtual protected] void QMdiSubWindow::showEvent(QShowEvent *showEvent)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。
该事件处理程序可以在子类中重新实现，以接收传递给 `event` 参数的控件显示事件。
非自发的展示事件会在展示前立即发送到小部件。窗口的自发展示事件则在展示之后交付。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，窗口恢复时自发显示事件。收到自发隐藏事件后，小部件仍被视为`isVisible()`可见。

### `[slot] void QMdiSubWindow::showShaded()`

**作用与语义：**

调用该函数会使子窗口进入着色模式。当子窗口被着色时，只有标题栏可见。
虽然并非所有样式都支持着色，但无论是否支持着色，该功能仍会显示子窗口为着色状态。然而，当使用不支持着色的样式时，用户将无法通过用户界面（例如标题栏中的着色按钮）返回着色模式。

### `[slot] void QMdiSubWindow::showSystemMenu()`

**作用与语义：**

在标题栏系统菜单图标下方显示系统菜单。

### `[override virtual] QSize QMdiSubWindow::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `QMenu *QMdiSubWindow::systemMenu() const`

**作用与语义：**

返回当前系统菜单的指针，若未设置系统菜单则返回为零。`QMdiSubWindow`提供默认系统菜单，但你也可以用`setSystemMenu()`设置菜单。

### `bool QMdiSubWindow::testOption(QMdiSubWindow::SubWindowOption option) const`

**作用与语义：**

如果启用`option`，返回`true`;否则返回`false`。

### `[override virtual protected] void QMdiSubWindow::timerEvent(QTimerEvent *timerEvent)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。

### `QWidget *QMdiSubWindow::widget() const`

**作用与语义：**

返回当前的内部控件。

### `[signal] void QMdiSubWindow::windowStateChanged(Qt::WindowStates oldState, Qt::WindowStates newState)`

**作用与语义：**

`QMdiSubWindow`在窗口状态变化后发出该信号。`oldState`是窗口状态变化前的状态，`newState`是新的当前状态。

### `enum SubWindowOption { RubberBandResize, RubberBandMove }`

**作用与语义：**

该枚举描述了可以自定义`QMdiSubWindow`行为的选项。
- `QMdiSubWindow::RubberBandResize`：`0x4`;如果你启用此选项，会使用橡皮筋控件来表示子窗口的轮廓，用户可以调整其大小，而不是子窗口本身。因此，子窗口保持其原始位置和大小，直到调整大小操作完成，届时它会收到一个`QResizeEvent`。默认情况下，该选项被禁用。
- `QMdiSubWindow::RubberBandMove`：`0x8`;如果你启用此选项，会用橡皮筋控制来表示子窗口的轮廓，用户移动的是子窗口，而不是子窗口本身。因此，子窗口会保持在原来的位置，直到移动操作完成，届时会向窗口发送`QMoveEvent`。默认情况下，该选项被禁用。
SubWindowOptions 类型是 QFlags 的 typedef<SubWindowOption>。它存储 SubWindowOption 值的 OR 组合。

### `flags SubWindowOptions`

**作用与语义：**

该枚举描述了可以自定义`QMdiSubWindow`行为的选项。
- `QMdiSubWindow::RubberBandResize`：`0x4`;如果你启用此选项，会使用橡皮筋控件来表示子窗口的轮廓，用户可以调整其大小，而不是子窗口本身。因此，子窗口保持其原始位置和大小，直到调整大小操作完成，届时它会收到一个`QResizeEvent`。默认情况下，该选项被禁用。
- `QMdiSubWindow::RubberBandMove`：`0x8`;如果你启用此选项，会用橡皮筋控制来表示子窗口的轮廓，用户移动的是子窗口，而不是子窗口本身。因此，子窗口会保持在原来的位置，直到移动操作完成，届时会向窗口发送`QMoveEvent`。默认情况下，该选项被禁用。
SubWindowOptions 类型是 QFlags 的 typedef<SubWindowOption>。它存储 SubWindowOption 值的 OR 组合。

### `int keyboardPageStep() const`

**作用与语义：**

设置使用键盘页面键时，控件的移动或大小。
在键盘交互模式下，您可以使用方向键和页面键来移动或调整窗口大小。该特性控制页面键。进入键盘交互模式的常见方法是进入子窗口菜单，选择“缩小”或“移动”。
默认的键盘页面步长值是20像素。

**如何使用：** 调用 `keyboardPageStep()` 读取当前值；它不会修改应用状态。

### `int keyboardSingleStep() const`

**作用与语义：**

设置使用键盘方向键时小部件应移动或调整大小。
在键盘交互模式下，您可以使用方向键和页面键来移动或调整窗口大小。该特性控制方向键。进入键盘交互模式的常见方法是进入子窗口菜单，选择“缩小”或“移动”。
默认的键盘单步数值是5像素。

**如何使用：** 调用 `keyboardSingleStep()` 读取当前值；它不会修改应用状态。

### `void setKeyboardPageStep(int step)`

**作用与语义：**

设置使用键盘页面键时，控件的移动或大小。
在键盘交互模式下，您可以使用方向键和页面键来移动或调整窗口大小。该特性控制页面键。进入键盘交互模式的常见方法是进入子窗口菜单，选择“缩小”或“移动”。
默认的键盘页面步长值是20像素。

**如何使用：** 调用 `setKeyboardPageStep(...)` 修改 `keyboardPageStep`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setKeyboardSingleStep(int step)`

**作用与语义：**

设置使用键盘方向键时小部件应移动或调整大小。
在键盘交互模式下，您可以使用方向键和页面键来移动或调整窗口大小。该特性控制方向键。进入键盘交互模式的常见方法是进入子窗口菜单，选择“缩小”或“移动”。
默认的键盘单步数值是5像素。

**如何使用：** 调用 `setKeyboardSingleStep(...)` 修改 `keyboardSingleStep`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QMdiSubWindow` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
