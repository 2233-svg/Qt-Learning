# QToolButton

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QToolButton` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QToolButton` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QToolButton>`
- 继承自：QAbstractButton
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

- `enum ToolButtonPopupMode { DelayedPopup, MenuButtonPopup, InstantPopup }`

### 属性

- `arrowType : Qt::ArrowType`
- `autoRaise : bool`
- `popupMode : ToolButtonPopupMode`
- `toolButtonStyle : Qt::ToolButtonStyle`

### 公有函数

- `QToolButton(QWidget *parent = nullptr)`
- `virtual ~QToolButton()`
- `Qt::ArrowType arrowType() const`
- `bool autoRaise() const`
- `QAction * defaultAction() const`
- `QMenu * menu() const`
- `QToolButton::ToolButtonPopupMode popupMode() const`
- `void setArrowType(Qt::ArrowType type)`
- `void setAutoRaise(bool enable)`
- `void setMenu(QMenu *menu)`
- `void setPopupMode(QToolButton::ToolButtonPopupMode mode)`
- `Qt::ToolButtonStyle toolButtonStyle() const`

### 重实现的公有函数

- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void setDefaultAction(QAction *action)`
- `void setToolButtonStyle(Qt::ToolButtonStyle style)`
- `void showMenu()`

### 信号

- `void triggered(QAction *action)`

### 保护函数

- `virtual void initStyleOption(QStyleOptionToolButton *option) const`

### 重实现的保护函数

- `virtual void actionEvent(QActionEvent *event) override`
- `virtual void changeEvent(QEvent *e) override`
- `virtual void checkStateSet() override`
- `virtual void enterEvent(QEnterEvent *e) override`
- `virtual bool event(QEvent *event) override`
- `virtual bool hitButton(const QPoint &pos) const override`
- `virtual void leaveEvent(QEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual void nextCheckState() override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual void timerEvent(QTimerEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QToolButton::ToolButtonPopupMode`

**作用与语义：**

描述了如何弹出带有菜单集或包含操作列表的工具按钮的菜单。
- `QToolButton::DelayedPopup`：`0`;按住工具按钮一定时间（超时取决于样式，见`QStyle::SH_ToolButton_PopupDelay`），菜单会显示。一个典型的应用例子是某些浏览器工具栏中的“返回”按钮。用户点击后，浏览器会直接返回上一页。如果用户按住按钮一段时间，工具按钮会显示包含当前历史列表的菜单
- `QToolButton::MenuButtonPopup`：`1`;在此模式下，工具按钮会显示一个特殊箭头，表示菜单存在。当按下按钮的箭头部分时，菜单会显示出来。
- `QToolButton::InstantPopup`：`2`;当按下工具按钮时，菜单会无延迟地显示。在此模式下，按钮本身的动作不会被触发。

### `arrowType : Qt::ArrowType`

**作用与语义：**

该属性适用于按钮是否显示箭头而非普通图标。
该图标显示一个箭头作为`QToolButton`。
默认情况下，该属性设置为`Qt::NoArrow`。

**如何使用：** 调用 `arrowType()` 读取当前值；它不会修改应用状态。

### `autoRaise : bool`

**作用与语义：**

该属性适用于是否启用自动提升。
默认值为禁用（即 false）。
在 macOS 使用 QMacStyle 时，该属性目前被忽略。

**如何使用：** 调用 `autoRaise()` 读取当前值；它不会修改应用状态。

### `popupMode : ToolButtonPopupMode`

**作用与语义：**

描述弹出菜单与工具按钮的使用方式。
默认情况下，该属性设置为`DelayedPopup`。

**如何使用：** 调用 `popupMode()` 读取当前值；它不会修改应用状态。

### `toolButtonStyle : Qt::ToolButtonStyle`

**作用与语义：**

该属性适用于工具按钮仅显示图标、仅显示文本，还是图标旁边/下方显示文字。
默认是`Qt::ToolButtonIconOnly`。
为了让工具按钮的样式符合系统设置，请将该属性设置为`Qt::ToolButtonFollowStyle`。在 Unix 上，桌面环境的用户设置将被使用。在其他平台上，`Qt::ToolButtonFollowStyle` 仅指图标。
`QToolButton`会自动将该槽函数连接到其所在`QMainWindow`中的相关信号。

**如何使用：** 调用 `toolButtonStyle()` 读取当前值；它不会修改应用状态。

### `[explicit] QToolButton::QToolButton(QWidget *parent = nullptr)`

**作用与语义：**

构建一个带有父`parent`的空工具按钮。

### `[virtual noexcept] QToolButton::~QToolButton()`

**作用与语义：**

摧毁该物体并释放所有分配的资源。

### `[override virtual protected] void QToolButton::actionEvent(QActionEvent *event)`

**作用与语义：**

重实现自：`QWidget::actionEvent`（QActionEvent *event）。
每当控件的动作发生变化时，该事件处理程序都会被调用给定的`event`。

### `[override virtual protected] void QToolButton::changeEvent(QEvent *e)`

**作用与语义：**

重实现自：`QAbstractButton::changeEvent`（QEvent *e）。

### `[override virtual protected] void QToolButton::checkStateSet()`

**作用与语义：**

重装：`QAbstractButton::checkStateSet()`。
当使用 `setChecked()` 时调用该虚拟处理器，除非在 `nextCheckState()` 内部调用。它允许子类重置其中间按钮状态。

### `QAction *QToolButton::defaultAction() const`

**作用与语义：**

返回默认动作。

### `[override virtual protected] void QToolButton::enterEvent(QEnterEvent *e)`

**作用与语义：**

重实现自：`QWidget::enterEvent`（QEnterEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件进入事件。
当鼠标光标进入控件时，会发送一个事件到控件。

### `[override virtual protected] bool QToolButton::event(QEvent *event)`

**作用与语义：**

重实现自：`QAbstractButton::event`（QEvent *e）。

### `[override virtual protected] bool QToolButton::hitButton(const QPoint &pos) const`

**作用与语义：**

重装：`QAbstractButton::hitButton`（const QPoint & pos） const.
如果`pos`在可点击的按钮矩形内，返回`true`;否则返回`false`。
默认情况下，可点击区域是整个小部件。子类可能会重新实现此功能，以支持不同形状和大小的可点击区域。

### `[virtual protected] void QToolButton::initStyleOption(QStyleOptionToolButton *option) const`

**作用与语义：**

用这个`QToolButton`的值初始化`option`。这种方法适用于需要 `QStyleOptionToolButton`但不想自己填满所有信息的子类。

### `[override virtual protected] void QToolButton::leaveEvent(QEvent *e)`

**作用与语义：**

重装：`QWidget::leaveEvent`（QEvent *事件）。
该事件处理程序可以被子类重新实现，以接收通过 `event` 参数传递的控件离开事件。
当鼠标光标离开控件时，会向控件发送一个离开事件。

### `QMenu *QToolButton::menu() const`

**作用与语义：**

返回关联菜单，若未定义菜单则返回`nullptr`。

### `[override virtual] QSize QToolButton::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[override virtual protected] void QToolButton::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractButton::mousePressEvent`（QMouseEvent *e）。

### `[override virtual protected] void QToolButton::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractButton::mouseReleaseEvent`（QMouseEvent *e）。

### `[override virtual protected] void QToolButton::nextCheckState()`

**作用与语义：**

重装：`QAbstractButton::nextCheckState()`。
当按钮被点击时调用这个虚拟处理器。默认实现调用`setChecked`（！`isChecked()`），如果按钮`isCheckable()`。它允许子类实现中间按钮状态。

### `[override virtual protected] void QToolButton::paintEvent(QPaintEvent *event)`

**作用与语义：**

重构：`QAbstractButton::paintEvent`（QPaintEvent *e）。
会根据涂装`event`来给按钮上色。

### `[slot] void QToolButton::setDefaultAction(QAction *action)`

**作用与语义：**

默认动作设置为`action`。
如果工具按钮有默认动作，该动作定义按钮的以下属性：
- `checkable`
- `checked`
- `enabled`
- `font`
- `icon`
- `popupMode`（假设动作有菜单）
- `statusTip`
- `text`
- `toolTip`
- `whatsThis`
其他属性，如`autoRepeat`，不受作用影响。

### `void QToolButton::setMenu(QMenu *menu)`

**作用与语义：**

将给定`menu`与这个工具按钮关联起来。
菜单会根据按钮的`popupMode`显示。
菜单的所有权不会转移到工具按钮上。

### `[slot] void QToolButton::showMenu()`

**作用与语义：**

显示（弹出）相关的弹出菜单。如果没有这样的菜单，这个功能就不会有任何作用。直到用户关闭弹出菜单后，这个功能才会返回。

### `[override virtual] QSize QToolButton::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `[override virtual protected] void QToolButton::timerEvent(QTimerEvent *e)`

**作用与语义：**

重实现自：`QAbstractButton::timerEvent`（QTimerEvent *e）。

### `[signal] void QToolButton::triggered(QAction *action)`

**作用与语义：**

当给定`action`被触发时，该信号会被发射。
该动作还可以与用户界面的其他部分关联，如菜单项和键盘快捷键。以这种方式共享操作有助于使用户界面更一致，且实现工作量通常更少。

### `Qt::ArrowType arrowType() const`

**作用与语义：**

该属性适用于按钮是否显示箭头而非普通图标。
该图标显示一个箭头作为`QToolButton`。
默认情况下，该属性设置为`Qt::NoArrow`。

**如何使用：** 调用 `arrowType()` 读取当前值；它不会修改应用状态。

### `bool autoRaise() const`

**作用与语义：**

该属性适用于是否启用自动提升。
默认值为禁用（即 false）。
在 macOS 使用 QMacStyle 时，该属性目前被忽略。

**如何使用：** 调用 `autoRaise()` 读取当前值；它不会修改应用状态。

### `QToolButton::ToolButtonPopupMode popupMode() const`

**作用与语义：**

描述弹出菜单与工具按钮的使用方式。
默认情况下，该属性设置为`DelayedPopup`。

**如何使用：** 调用 `popupMode()` 读取当前值；它不会修改应用状态。

### `void setArrowType(Qt::ArrowType type)`

**作用与语义：**

该属性适用于按钮是否显示箭头而非普通图标。
该图标显示一个箭头作为`QToolButton`。
默认情况下，该属性设置为`Qt::NoArrow`。

**如何使用：** 调用 `setArrowType(...)` 修改 `arrowType`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAutoRaise(bool enable)`

**作用与语义：**

该属性适用于是否启用自动提升。
默认值为禁用（即 false）。
在 macOS 使用 QMacStyle 时，该属性目前被忽略。

**如何使用：** 调用 `setAutoRaise(...)` 修改 `autoRaise`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPopupMode(QToolButton::ToolButtonPopupMode mode)`

**作用与语义：**

描述弹出菜单与工具按钮的使用方式。
默认情况下，该属性设置为`DelayedPopup`。

**如何使用：** 调用 `setPopupMode(...)` 修改 `popupMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `Qt::ToolButtonStyle toolButtonStyle() const`

**作用与语义：**

该属性适用于工具按钮仅显示图标、仅显示文本，还是图标旁边/下方显示文字。
默认是`Qt::ToolButtonIconOnly`。
为了让工具按钮的样式符合系统设置，请将该属性设置为`Qt::ToolButtonFollowStyle`。在 Unix 上，桌面环境的用户设置将被使用。在其他平台上，`Qt::ToolButtonFollowStyle` 仅指图标。
`QToolButton`会自动将该槽函数连接到其所在`QMainWindow`中的相关信号。

**如何使用：** 调用 `toolButtonStyle()` 读取当前值；它不会修改应用状态。

### `void setToolButtonStyle(Qt::ToolButtonStyle style)`

**作用与语义：**

该属性适用于工具按钮仅显示图标、仅显示文本，还是图标旁边/下方显示文字。
默认是`Qt::ToolButtonIconOnly`。
为了让工具按钮的样式符合系统设置，请将该属性设置为`Qt::ToolButtonFollowStyle`。在 Unix 上，桌面环境的用户设置将被使用。在其他平台上，`Qt::ToolButtonFollowStyle` 仅指图标。
`QToolButton`会自动将该槽函数连接到其所在`QMainWindow`中的相关信号。

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

`QToolButton` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
