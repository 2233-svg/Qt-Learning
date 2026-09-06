# QAbstractButton

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QAbstractButton` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QAbstractButton` 是 Qt Widgets 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractButton>`
- 继承自：QWidget
- 直接派生类：QCheckBox、QPushButton、QRadioButton,、QToolButton

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `autoExclusive : bool`
- `autoRepeat : bool`
- `autoRepeatDelay : int`
- `autoRepeatInterval : int`
- `checkable : bool`
- `checked : bool`
- `down : bool`
- `icon : QIcon`
- `iconSize : QSize`
- `shortcut : QKeySequence`
- `text : QString`

### 公有函数

- `QAbstractButton(QWidget *parent = nullptr)`
- `virtual ~QAbstractButton()`
- `bool autoExclusive() const`
- `bool autoRepeat() const`
- `int autoRepeatDelay() const`
- `int autoRepeatInterval() const`
- `QButtonGroup * group() const`
- `QIcon icon() const`
- `QSize iconSize() const`
- `bool isCheckable() const`
- `bool isChecked() const`
- `bool isDown() const`
- `void setAutoExclusive(bool)`
- `void setAutoRepeat(bool)`
- `void setAutoRepeatDelay(int)`
- `void setAutoRepeatInterval(int)`
- `void setCheckable(bool)`
- `void setDown(bool)`
- `void setIcon(const QIcon &icon)`
- `void setShortcut(const QKeySequence &key)`
- `void setText(const QString &text)`
- `QKeySequence shortcut() const`
- `QString text() const`

### 公有槽函数

- `void animateClick()`
- `void click()`
- `void setChecked(bool)`
- `void setIconSize(const QSize &size)`
- `void toggle()`

### 信号

- `void clicked(bool checked = false)`
- `void pressed()`
- `void released()`
- `void toggled(bool checked)`

### 保护函数

- `virtual void checkStateSet()`
- `virtual bool hitButton(const QPoint &pos) const`
- `virtual void nextCheckState()`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *e) override`
- `virtual bool event(QEvent *e) override`
- `virtual void focusInEvent(QFocusEvent *e) override`
- `virtual void focusOutEvent(QFocusEvent *e) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void keyReleaseEvent(QKeyEvent *e) override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual void paintEvent(QPaintEvent *e) override = 0`
- `virtual void timerEvent(QTimerEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `autoExclusive : bool`

**作用与语义：**

该属性适用于是否启用自动排他性。
如果启用自动排他性，则属于同一父部件的可选中按钮的行为就像它们属于同一排他按钮组一样。在排他按钮组中，任意时刻只能选中一个按钮；选中另一个按钮会自动取消先前选中的按钮。
该属性对属于按钮组的按钮无效。
autoExclusive 默认关闭，单选按钮除外。

**如何使用：** 调用 `autoExclusive()` 读取当前值；它不会修改应用状态。

### `autoRepeat : bool`

**作用与语义：**

该属性适用于是否启用自动重复。
如果启用自动重复，则当按钮按下时，`pressed()`、`released()` 和 `clicked()` 信号将按固定间隔发出。autoRepeat 默认关闭。初始延迟和重复间隔以毫秒为单位由 `autoRepeatDelay` 和 `autoRepeatInterval` 定义。
注意：如果按钮通过快捷键按下，则自动重复由系统计时而非本类计时。`pressed()`、`released()` 和 `clicked()` 信号将像正常情况一样发出。

**如何使用：** 调用 `autoRepeat()` 读取当前值；它不会修改应用状态。

### `autoRepeatDelay : int`

**作用与语义：**

该属性表示了自动重复的初始延迟。
如果启用`autoRepeat`，autoRepeatDelay 定义了初始延迟（以毫秒为单位），然后自动重复启动。

**如何使用：** 调用 `autoRepeatDelay()` 读取当前值；它不会修改应用状态。

### `autoRepeatInterval : int`

**作用与语义：**

该属性表示自重复区间。
如果启用`autoRepeat`，则autoRepeatInterval定义了millisecons中自动重复间隔的长度。

**如何使用：** 调用 `autoRepeatInterval()` 读取当前值；它不会修改应用状态。

### `checkable : bool`

**作用与语义：**

该属性决定按钮是否可被检查。
默认情况下，该按钮不可勾选。

**如何使用：** 调用 `checkable()` 读取当前值；它不会修改应用状态。

### `checked : bool`

**作用与语义：**

该属性决定按钮是否被检查。
只能勾选可勾选的按钮。默认情况下，按钮是未勾选的。

**如何使用：** 调用 `checked()` 读取当前值；它不会修改应用状态。

### `down : bool`

**作用与语义：**

该属性是否按键时适用。
如果该属性`true`，按钮被按下。如果你将该属性设为true，信号`pressed()`和`clicked()`不会发出。默认为false。

**如何使用：** 调用 `down()` 读取当前值；它不会修改应用状态。

### `icon : QIcon`

**作用与语义：**

该属性保留按钮上的图标。
图标的默认大小由图形界面样式定义，但可以通过设置`iconSize`属性进行调整。

**如何使用：** 调用 `icon()` 读取当前值；它不会修改应用状态。

### `iconSize : QSize`

**作用与语义：**

该属性包含该按钮所用图标大小。
默认大小由图形界面样式定义。这是图标的最大尺寸。较小的图标不会被放大。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `shortcut : QKeySequence`

**作用与语义：**

该属性包含了与按钮相关的助记法。

**如何使用：** 调用 `shortcut()` 读取当前值；它不会修改应用状态。

### `text : QString`

**作用与语义：**

该属性保留按钮上显示的文本。
如果按钮没有文本，text() 函数会返回一个空字符串。
如果文本中包含一个&字符（'&'），会自动为其创建一个快捷方式。'&'后面的字符将用作快捷键。如果文本中没有定义快捷方式，任何之前的快捷方式都会被覆盖或清除。详情请参见`QShortcut`文档。要显示实际的&&符号，请使用'&&'。
没有默认文本。

**如何使用：** 调用 `text()` 读取当前值；它不会修改应用状态。

### `[explicit] QAbstractButton::QAbstractButton(QWidget *parent = nullptr)`

**作用与语义：**

构建一个带有`parent`的抽象按钮。

### `[virtual noexcept] QAbstractButton::~QAbstractButton()`

**作用与语义：**

会破坏按钮。

### `[slot] void QAbstractButton::animateClick()`

**作用与语义：**

执行动画点击：按钮立即按下，100毫秒后松开。
在按钮松开前再次调用该函数会重置释放计时器。
所有与点击声相关的信号均按需发射。
如果按钮`disabled.`，这个功能就没有作用。

### `[override virtual protected] void QAbstractButton::changeEvent(QEvent *e)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[virtual protected] void QAbstractButton::checkStateSet()`

**作用与语义：**

当使用`setChecked()`时调用该虚拟处理器，除非在`nextCheckState()`内部调用。它允许子类重置其中间按钮状态。

### `[slot] void QAbstractButton::click()`

**作用与语义：**

点击声。
按键通常会发出所有常见的信号。如果按钮可勾选，按钮的状态会被切换。
如果按钮处于`disabled.`，这个功能就没有任何作用。

### `[signal] void QAbstractButton::clicked(bool checked = false)`

**作用与语义：**

当按钮被激活（即按下后放开，鼠标光标在按钮内）、快捷键输入，或`click()`或`animateClick()`时，会发出该信号。值得注意的是，如果你调用`setDown()`、`setChecked()`或`toggle()`，则不会发出该信号。
如果按钮可勾选，`checked`为真（按钮被勾选），键未勾选为假。

### `[override virtual protected] bool QAbstractButton::event(QEvent *e)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[override virtual protected] void QAbstractButton::focusInEvent(QFocusEvent *e)`

**作用与语义：**

重实现自：`QWidget::focusInEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点接收）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] void QAbstractButton::focusOutEvent(QFocusEvent *e)`

**作用与语义：**

重现：`QWidget::focusOutEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点丢失）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `QButtonGroup *QAbstractButton::group() const`

**作用与语义：**

返回该按钮所属的组。
如果按钮不属于任何`QButtonGroup`，该函数返回`nullptr`。

### `[virtual protected] bool QAbstractButton::hitButton(const QPoint &pos) const`

**作用与语义：**

如果 `pos` 在可点击按钮矩形内，则返回 `true`；否则返回 `false`。
默认情况下，可点击区域是整个小部件。子类可以重新实现此函数，以支持不同形状和大小的可点击区域。

### `[override virtual protected] void QAbstractButton::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
一个小部件必须调用`setFocusPolicy()`先接受焦点，并且必须有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是 Escape 键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对该键执行时不要调用基类实现即可。

### `[override virtual protected] void QAbstractButton::keyReleaseEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyReleaseEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该小部件的密钥释放事件。
小部件必须先接受焦点并拥有焦点，才能接收密钥释放事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现忽略事件，以便小部件的父节点能够解释事件。
注意`QKeyEvent`以 isAccepted() == true开头，所以你不需要调用`QKeyEvent::accept()`——只要你对密钥操作时不要调用基类实现即可。

### `[override virtual protected] void QAbstractButton::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseMoveEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标移动事件。
如果关闭鼠标追踪，只有在鼠标移动过程中按下鼠标按钮时才会发生鼠标移动事件。如果开启鼠标追踪，即使未按键，鼠标移动事件也会发生。
`QMouseEvent::position()`报告鼠标光标相对于该小部件的位置。对于按下和释放事件，位置通常与最后一次鼠标移动事件的位置相同，但如果用户的手握手，可能会有所不同。这是底层窗口系统的功能，而非Qt。
如果你想在鼠标移动时立即显示提示（例如，获取鼠标坐标与`QMouseEvent::position()`并显示为提示），你必须先启用上述的鼠标追踪功能。然后，为了确保提示立即更新，你必须在鼠标移动事件（mouseMoveEvent）实现中调用`QToolTip::showText()`而不是`setToolTip()`。

### `[override virtual protected] void QAbstractButton::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[override virtual protected] void QAbstractButton::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标释放事件。

### `[virtual protected] void QAbstractButton::nextCheckState()`

**作用与语义：**

当按钮被点击时，会调用这个虚拟处理器。默认实现调用`setChecked`（！如果按钮`isCheckable()`，`isChecked()`）。它允许子类实现中间按钮状态。

### `[override pure virtual protected] void QAbstractButton::paintEvent(QPaintEvent *e)`

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

### `[signal] void QAbstractButton::pressed()`

**作用与语义：**

当按下按钮时，会发出该信号。

### `[signal] void QAbstractButton::released()`

**作用与语义：**

当按钮松开时，该信号会发出。

### `[override virtual protected] void QAbstractButton::timerEvent(QTimerEvent *e)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。

### `[slot] void QAbstractButton::toggle()`

**作用与语义：**

切换可勾选按钮的状态。

### `[signal] void QAbstractButton::toggled(bool checked)`

**作用与语义：**

该属性决定按钮是否被检查。
只能勾选可勾选的按钮。默认情况下，按钮是未勾选的。

**如何使用：** 调用 `toggled()` 读取当前值；它不会修改应用状态。

### `bool autoExclusive() const`

**作用与语义：**

该属性适用于是否启用自动排他性。
如果启用自动排他性，则属于同一父部件的可选中按钮的行为就像它们属于同一排他按钮组一样。在排他按钮组中，任意时刻只能选中一个按钮；选中另一个按钮会自动取消先前选中的按钮。
该属性对属于按钮组的按钮无效。
autoExclusive 默认关闭，单选按钮除外。

**如何使用：** 调用 `autoExclusive()` 读取当前值；它不会修改应用状态。

### `bool autoRepeat() const`

**作用与语义：**

该属性适用于是否启用自动重复。
如果启用自动重复，则当按钮按下时，`pressed()`、`released()` 和 `clicked()` 信号将按固定间隔发出。autoRepeat 默认关闭。初始延迟和重复间隔以毫秒为单位由 `autoRepeatDelay` 和 `autoRepeatInterval` 定义。
注意：如果按钮通过快捷键按下，则自动重复由系统计时而非本类计时。`pressed()`、`released()` 和 `clicked()` 信号将像正常情况一样发出。

**如何使用：** 调用 `autoRepeat()` 读取当前值；它不会修改应用状态。

### `int autoRepeatDelay() const`

**作用与语义：**

该属性表示了自动重复的初始延迟。
如果启用`autoRepeat`，autoRepeatDelay 定义了初始延迟（以毫秒为单位），然后自动重复启动。

**如何使用：** 调用 `autoRepeatDelay()` 读取当前值；它不会修改应用状态。

### `int autoRepeatInterval() const`

**作用与语义：**

该属性表示自重复区间。
如果启用`autoRepeat`，则autoRepeatInterval定义了millisecons中自动重复间隔的长度。

**如何使用：** 调用 `autoRepeatInterval()` 读取当前值；它不会修改应用状态。

### `QIcon icon() const`

**作用与语义：**

该属性保留按钮上的图标。
图标的默认大小由图形界面样式定义，但可以通过设置`iconSize`属性进行调整。

**如何使用：** 调用 `icon()` 读取当前值；它不会修改应用状态。

### `QSize iconSize() const`

**作用与语义：**

该属性包含该按钮所用图标大小。
默认大小由图形界面样式定义。这是图标的最大尺寸。较小的图标不会被放大。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `bool isCheckable() const`

**作用与语义：**

该属性决定按钮是否可被检查。
默认情况下，该按钮不可勾选。

**如何使用：** 调用 `isCheckable()` 读取当前值；它不会修改应用状态。

### `bool isChecked() const`

**作用与语义：**

该属性决定按钮是否被检查。
只能勾选可勾选的按钮。默认情况下，按钮是未勾选的。

**如何使用：** 调用 `isChecked()` 读取当前值；它不会修改应用状态。

### `bool isDown() const`

**作用与语义：**

该属性是否按键时适用。
如果该属性`true`，按钮被按下。如果你将该属性设为true，信号`pressed()`和`clicked()`不会发出。默认为false。

**如何使用：** 调用 `isDown()` 读取当前值；它不会修改应用状态。

### `void setAutoExclusive(bool)`

**作用与语义：**

该属性适用于是否启用自动排他性。
如果启用自动排他性，则属于同一父部件的可选中按钮的行为就像它们属于同一排他按钮组一样。在排他按钮组中，任意时刻只能选中一个按钮；选中另一个按钮会自动取消先前选中的按钮。
该属性对属于按钮组的按钮无效。
autoExclusive 默认关闭，单选按钮除外。

**如何使用：** 调用 `setAutoExclusive(...)` 修改 `autoExclusive`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAutoRepeat(bool)`

**作用与语义：**

该属性适用于是否启用自动重复。
如果启用自动重复，则当按钮按下时，`pressed()`、`released()` 和 `clicked()` 信号将按固定间隔发出。autoRepeat 默认关闭。初始延迟和重复间隔以毫秒为单位由 `autoRepeatDelay` 和 `autoRepeatInterval` 定义。
注意：如果按钮通过快捷键按下，则自动重复由系统计时而非本类计时。`pressed()`、`released()` 和 `clicked()` 信号将像正常情况一样发出。

**如何使用：** 调用 `setAutoRepeat(...)` 修改 `autoRepeat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAutoRepeatDelay(int)`

**作用与语义：**

该属性表示了自动重复的初始延迟。
如果启用`autoRepeat`，autoRepeatDelay 定义了初始延迟（以毫秒为单位），然后自动重复启动。

**如何使用：** 调用 `setAutoRepeatDelay(...)` 修改 `autoRepeatDelay`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAutoRepeatInterval(int)`

**作用与语义：**

该属性表示自重复区间。
如果启用`autoRepeat`，则autoRepeatInterval定义了millisecons中自动重复间隔的长度。

**如何使用：** 调用 `setAutoRepeatInterval(...)` 修改 `autoRepeatInterval`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCheckable(bool)`

**作用与语义：**

该属性决定按钮是否可被检查。
默认情况下，该按钮不可勾选。

**如何使用：** 调用 `setCheckable(...)` 修改 `checkable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDown(bool)`

**作用与语义：**

该属性是否按键时适用。
如果该属性`true`，按钮被按下。如果你将该属性设为true，信号`pressed()`和`clicked()`不会发出。默认为false。

**如何使用：** 调用 `setDown(...)` 修改 `down`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIcon(const QIcon &icon)`

**作用与语义：**

该属性保留按钮上的图标。
图标的默认大小由图形界面样式定义，但可以通过设置`iconSize`属性进行调整。

**如何使用：** 调用 `setIcon(...)` 修改 `icon`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setShortcut(const QKeySequence &key)`

**作用与语义：**

该属性包含了与按钮相关的助记法。

**如何使用：** 调用 `setShortcut(...)` 修改 `shortcut`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setText(const QString &text)`

**作用与语义：**

该属性保留按钮上显示的文本。
如果按钮没有文本，text() 函数会返回一个空字符串。
如果文本中包含一个&字符（'&'），会自动为其创建一个快捷方式。'&'后面的字符将用作快捷键。如果文本中没有定义快捷方式，任何之前的快捷方式都会被覆盖或清除。详情请参见`QShortcut`文档。要显示实际的&&符号，请使用'&&'。
没有默认文本。

**如何使用：** 调用 `setText(...)` 修改 `text`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QKeySequence shortcut() const`

**作用与语义：**

该属性包含了与按钮相关的助记法。

**如何使用：** 调用 `shortcut()` 读取当前值；它不会修改应用状态。

### `QString text() const`

**作用与语义：**

该属性保留按钮上显示的文本。
如果按钮没有文本，text() 函数会返回一个空字符串。
如果文本中包含一个&字符（'&'），会自动为其创建一个快捷方式。'&'后面的字符将用作快捷键。如果文本中没有定义快捷方式，任何之前的快捷方式都会被覆盖或清除。详情请参见`QShortcut`文档。要显示实际的&&符号，请使用'&&'。
没有默认文本。

**如何使用：** 调用 `text()` 读取当前值；它不会修改应用状态。

### `void setChecked(bool)`

**作用与语义：**

该属性决定按钮是否被检查。
只能勾选可勾选的按钮。默认情况下，按钮是未勾选的。

**如何使用：** 调用 `setChecked(...)` 修改 `checked`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIconSize(const QSize &size)`

**作用与语义：**

该属性包含该按钮所用图标大小。
默认大小由图形界面样式定义。这是图标的最大尺寸。较小的图标不会被放大。

**如何使用：** 调用 `setIconSize(...)` 修改 `iconSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractButton` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
