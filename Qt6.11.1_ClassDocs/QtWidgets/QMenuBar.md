# QMenuBar

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QMenuBar` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QMenuBar` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QMenuBar>`
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

- `defaultUp : bool`
- `nativeMenuBar : bool`

### 公有函数

- `QMenuBar(QWidget *parent = nullptr)`
- `virtual ~QMenuBar()`
- `QAction * actionAt(const QPoint &pt) const`
- `QRect actionGeometry(QAction *act) const`
- `QAction * activeAction() const`
- `QAction * addMenu(QMenu *menu)`
- `QMenu * addMenu(const QString &title)`
- `QMenu * addMenu(const QIcon &icon, const QString &title)`
- `QAction * addSeparator()`
- `void clear()`
- `QWidget * cornerWidget(Qt::Corner corner = Qt::TopRightCorner) const`
- `QAction * insertMenu(QAction *before, QMenu *menu)`
- `QAction * insertSeparator(QAction *before)`
- `bool isDefaultUp() const`
- `bool isNativeMenuBar() const`
- `void setActiveAction(QAction *act)`
- `void setCornerWidget(QWidget *widget, Qt::Corner corner = Qt::TopRightCorner)`
- `void setDefaultUp(bool)`
- `void setNativeMenuBar(bool nativeMenuBar)`
- `NSMenu * toNSMenu()`

### 重实现的公有函数

- `virtual int heightForWidth(int) const override`
- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `virtual void setVisible(bool visible) override`

### 信号

- `void hovered(QAction *action)`
- `void triggered(QAction *action)`

### 保护函数

- `virtual void initStyleOption(QStyleOptionMenuItem *option, const QAction *action) const`

### 重实现的保护函数

- `virtual void actionEvent(QActionEvent *e) override`
- `virtual void changeEvent(QEvent *e) override`
- `virtual bool event(QEvent *e) override`
- `virtual bool eventFilter(QObject *object, QEvent *event) override`
- `virtual void focusInEvent(QFocusEvent *) override`
- `virtual void focusOutEvent(QFocusEvent *) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void leaveEvent(QEvent *) override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual void paintEvent(QPaintEvent *e) override`
- `virtual void resizeEvent(QResizeEvent *) override`
- `virtual void timerEvent(QTimerEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `defaultUp : bool`

**作用与语义：**

此属性保存弹出方向。
默认弹出方向。默认情况下，菜单向屏幕“下方”弹出。将此属性设置为 true 时，菜单将向“上方”弹出。您可能会为位于其所引用文档下方的菜单调用此设置。
如果菜单无法适应屏幕，将自动使用另一个方向。

**如何使用：** 调用 `defaultUp()` 读取当前值；它不会修改应用状态。

### `nativeMenuBar : bool`

**作用与语义：**

该属性决定了菜单栏是否会作为支持该菜单栏的平台的原生菜单栏使用。
该属性指定了菜单栏是否应作为支持该功能的平台的本地菜单栏使用。目前支持的平台包括macOS和Linux桌面，这些平台使用com.canonical.dbusmenu D-Bus接口（如Ubuntu Unity）。如果`true`该属性，菜单栏会在原生菜单栏中使用，而不是在父菜单栏的窗口中;如果`false`，菜单栏则保留在窗口中。在其他平台上，设置该属性无效，读取该属性总是返回`false`。
默认情况下，是否为应用程序设置了`Qt::AA_DontUseNativeMenuBar`属性。明确设置该属性会覆盖该属性的存在（或缺失）。

**如何使用：** 调用 `nativeMenuBar()` 读取当前值；它不会修改应用状态。

### `[explicit] QMenuBar::QMenuBar(QWidget *parent = nullptr)`

**作用与语义：**

构建带有父`parent`的菜单栏。

### `[virtual noexcept] QMenuBar::~QMenuBar()`

**作用与语义：**

会毁掉菜单栏。

### `QAction *QMenuBar::actionAt(const QPoint &pt) const`

**作用与语义：**

返回`pt`的`QAction`。如果`pt`没有动作或位置有分隔符，返回`nullptr`。

### `[override virtual protected] void QMenuBar::actionEvent(QActionEvent *e)`

**作用与语义：**

重实现自：`QWidget::actionEvent`（QActionEvent *event）。
每当控件的动作发生变化时，该事件处理程序都会被调用给定的`event`。

### `QRect QMenuBar::actionGeometry(QAction *act) const`

**作用与语义：**

返回作用的几何体，`act`为`QRect`。

### `QAction *QMenuBar::activeAction() const`

**作用与语义：**

返回当前高亮的`QAction`（如有）`nullptr`。

### `QAction *QMenuBar::addMenu(QMenu *menu)`

**作用与语义：**

附加`menu`到菜单栏。返回菜单的menuAction()。菜单栏不拥有菜单的所有权。
注意：返回的 `QAction` 对象可以用来隐藏对应的菜单。

### `QMenu *QMenuBar::addMenu(const QString &title)`

**作用与语义：**

在菜单栏中添加一个带`title`的新`QMenu`。菜单栏会获得菜单的所有权。返回新菜单。

### `QMenu *QMenuBar::addMenu(const QIcon &icon, const QString &title)`

**作用与语义：**

在菜单栏中附加一个带有`icon`和`title`的新`QMenu`。菜单栏会获得菜单的所有权。返回新菜单。

### `QAction *QMenuBar::addSeparator()`

**作用与语义：**

在菜单中附加一个分隔符。

### `[override virtual protected] void QMenuBar::changeEvent(QEvent *e)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `void QMenuBar::clear()`

**作用与语义：**

菜单栏里的所有操作都被移除了。
注意：在macOS中，已合并到系统菜单栏的菜单项不会被这个功能删除。一种处理方法是自己移除额外的操作。你可以在不同菜单中设置菜单角色，这样提前知道哪些菜单项会合并，哪些不会。然后决定自己要重新创建或移除哪些。

### `QWidget *QMenuBar::cornerWidget(Qt::Corner corner = Qt::TopRightCorner) const`

**作用与语义：**

根据具体情况，返回第一个菜单左侧或最后一个菜单项右侧的小部件，具体是根据`corner`。
注意：使用非`Qt::TopRightCorner`或`Qt::TopLeftCorner`的角落将被警告。

### `[override virtual protected] bool QMenuBar::event(QEvent *e)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[override virtual protected] bool QMenuBar::eventFilter(QObject *object, QEvent *event)`

**作用与语义：**

重装：`QObject::eventFilter`（QObject *已观看，QEvent *事件）。

### `[override virtual protected] void QMenuBar::focusInEvent(QFocusEvent *)`

**作用与语义：**

重实现自：`QWidget::focusInEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点接收）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] void QMenuBar::focusOutEvent(QFocusEvent *)`

**作用与语义：**

重现：`QWidget::focusOutEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点丢失）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual] int QMenuBar::heightForWidth(int) const`

**作用与语义：**

重实现自：`QWidget::heightForWidth`（内性 w） const.
返回该小部件的首选高度，基于宽度`w`。
如果该控件有布局，默认实现返回该布局的首选高度。如果没有布局，默认实现返回 -1，表示首选高度不依赖于宽度。

### `[signal] void QMenuBar::hovered(QAction *action)`

**作用与语义：**

当菜单动作被高亮时，会发出该信号;`action` 是导致事件发送的动作。
通常用于更新状态信息。

### `[virtual protected] void QMenuBar::initStyleOption(QStyleOptionMenuItem *option, const QAction *action) const`

**作用与语义：**

用菜单栏的数值和`action`的信息初始化`option`。这种方法对需要 `QStyleOptionMenuItem` 但不想自己填写所有信息的子类很有用。

### `QAction *QMenuBar::insertMenu(QAction *before, QMenu *menu)`

**作用与语义：**

该便利函数在操作`before`前插入`menu`，并返回菜单的 menuAction()。

### `QAction *QMenuBar::insertSeparator(QAction *before)`

**作用与语义：**

这个便利函数会创建一个新的分隔符动作，即 `QAction::isSeparator()` 返回为真的动作。该函数会在动作 `before` 前将新创建的动作插入该菜单栏的动作列表并返回。

### `[override virtual protected] void QMenuBar::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
一个小部件必须调用`setFocusPolicy()`先接受焦点，并且必须有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是 Escape 键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对该键执行时不要调用基类实现即可。

### `[override virtual protected] void QMenuBar::leaveEvent(QEvent *)`

**作用与语义：**

重装：`QWidget::leaveEvent`（QEvent *事件）。
该事件处理程序可以被子类重新实现，以接收通过 `event` 参数传递的控件离开事件。
当鼠标光标离开控件时，会向控件发送一个离开事件。

### `[override virtual] QSize QMenuBar::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[override virtual protected] void QMenuBar::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseMoveEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标移动事件。
如果关闭鼠标追踪，只有在鼠标移动过程中按下鼠标按钮时才会发生鼠标移动事件。如果开启鼠标追踪，即使未按键，鼠标移动事件也会发生。
`QMouseEvent::position()`报告鼠标光标相对于该小部件的位置。对于按下和释放事件，位置通常与最后一次鼠标移动事件的位置相同，但如果用户的手握手，可能会有所不同。这是底层窗口系统的功能，而非Qt。
如果你想在鼠标移动时立即显示提示（例如，获取鼠标坐标与`QMouseEvent::position()`并显示为提示），你必须先启用上述的鼠标追踪功能。然后，为了确保提示立即更新，你必须在鼠标移动事件（mouseMoveEvent）实现中调用`QToolTip::showText()`而不是`setToolTip()`。

### `[override virtual protected] void QMenuBar::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[override virtual protected] void QMenuBar::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标释放事件。

### `[override virtual protected] void QMenuBar::paintEvent(QPaintEvent *e)`

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

### `[override virtual protected] void QMenuBar::resizeEvent(QResizeEvent *)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件调整大小事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `void QMenuBar::setActiveAction(QAction *act)`

**作用与语义：**

将当前高亮的动作设置为`act`。

### `void QMenuBar::setCornerWidget(QWidget *widget, Qt::Corner corner = Qt::TopRightCorner)`

**作用与语义：**

这会根据`corner`，将给定的`widget`直接显示在第一个菜单项的左侧或最后一个菜单项的右侧。
菜单栏会获得`widget`的所有权，并将其重新父级化到菜单栏中。然而，如果`corner`中已经包含一个小部件，这个之前的小部件将不再被管理，仍然是菜单栏的可见子组件。
注意：使用非`Qt::TopRightCorner`或`Qt::TopLeftCorner`的角落将会收到警告。

### `[override virtual slot] void QMenuBar::setVisible(bool visible)`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::visible`。

### `[override virtual] QSize QMenuBar::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `[override virtual protected] void QMenuBar::timerEvent(QTimerEvent *e)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。

### `NSMenu *QMenuBar::toNSMenu()`

**作用与语义：**

返回本菜单栏的原生NSMenu。仅在macOS上可用。
注意：Qt 可能会在本地菜单栏上设置代理。如果你需要自己设置代理，请确保保存原始代理并转发所有调用。

### `[signal] void QMenuBar::triggered(QAction *action)`

**作用与语义：**

当该菜单栏中的某个动作因鼠标点击而触发时，该信号会发出;`action` 是导致该信号发出的动作。
注意：`QMenuBar`必须拥有`QMenu`所有权，才能使该信号正常工作。
通常，你会用`QAction::triggered()`连接每个菜单操作到一个槽函数，但有时你会想把多个项目连接到一个槽函数（最常见的是用户从数组中选择）。这种信号在这种情况下非常有用。

### `bool isDefaultUp() const`

**作用与语义：**

此属性保存弹出方向。
默认弹出方向。默认情况下，菜单向屏幕“下方”弹出。将此属性设置为 true 时，菜单将向“上方”弹出。您可能会为位于其所引用文档下方的菜单调用此设置。
如果菜单无法适应屏幕，将自动使用另一个方向。

**如何使用：** 调用 `isDefaultUp()` 读取当前值；它不会修改应用状态。

### `bool isNativeMenuBar() const`

**作用与语义：**

该属性决定了菜单栏是否会作为支持该菜单栏的平台的原生菜单栏使用。
该属性指定了菜单栏是否应作为支持该功能的平台的本地菜单栏使用。目前支持的平台包括macOS和Linux桌面，这些平台使用com.canonical.dbusmenu D-Bus接口（如Ubuntu Unity）。如果`true`该属性，菜单栏会在原生菜单栏中使用，而不是在父菜单栏的窗口中;如果`false`，菜单栏则保留在窗口中。在其他平台上，设置该属性无效，读取该属性总是返回`false`。
默认情况下，是否为应用程序设置了`Qt::AA_DontUseNativeMenuBar`属性。明确设置该属性会覆盖该属性的存在（或缺失）。

**如何使用：** 调用 `isNativeMenuBar()` 读取当前值；它不会修改应用状态。

### `void setDefaultUp(bool)`

**作用与语义：**

此属性保存弹出方向。
默认弹出方向。默认情况下，菜单向屏幕“下方”弹出。将此属性设置为 true 时，菜单将向“上方”弹出。您可能会为位于其所引用文档下方的菜单调用此设置。
如果菜单无法适应屏幕，将自动使用另一个方向。

**如何使用：** 调用 `setDefaultUp(...)` 修改 `defaultUp`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setNativeMenuBar(bool nativeMenuBar)`

**作用与语义：**

该属性决定了菜单栏是否会作为支持该菜单栏的平台的原生菜单栏使用。
该属性指定了菜单栏是否应作为支持该功能的平台的本地菜单栏使用。目前支持的平台包括macOS和Linux桌面，这些平台使用com.canonical.dbusmenu D-Bus接口（如Ubuntu Unity）。如果`true`该属性，菜单栏会在原生菜单栏中使用，而不是在父菜单栏的窗口中;如果`false`，菜单栏则保留在窗口中。在其他平台上，设置该属性无效，读取该属性总是返回`false`。
默认情况下，是否为应用程序设置了`Qt::AA_DontUseNativeMenuBar`属性。明确设置该属性会覆盖该属性的存在（或缺失）。

**如何使用：** 调用 `setNativeMenuBar(...)` 修改 `nativeMenuBar`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QMenuBar` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
