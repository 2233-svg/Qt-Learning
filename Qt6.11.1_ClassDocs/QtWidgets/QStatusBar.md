# QStatusBar

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QStatusBar` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QStatusBar` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QStatusBar>`
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

- `sizeGripEnabled : bool`

### 公有函数

- `QStatusBar(QWidget *parent = nullptr)`
- `virtual ~QStatusBar()`
- `void addPermanentWidget(QWidget *widget, int stretch = 0)`
- `void addWidget(QWidget *widget, int stretch = 0)`
- `QString currentMessage() const`
- `int insertPermanentWidget(int index, QWidget *widget, int stretch = 0)`
- `int insertWidget(int index, QWidget *widget, int stretch = 0)`
- `bool isSizeGripEnabled() const`
- `void removeWidget(QWidget *widget)`
- `void setSizeGripEnabled(bool)`

### 公有槽函数

- `void clearMessage()`
- `void showMessage(const QString &message, int timeout = 0)`

### 信号

- `void messageChanged(const QString &message)`

### 保护函数

- `void hideOrShow()`
- `void reformat()`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *e) override`
- `virtual void showEvent(QShowEvent *) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `sizeGripEnabled : bool`

**作用与语义：**

该属性决定状态栏右下角`QSizeGrip`是否启用。
默认情况下，尺寸握把是启用的。

**如何使用：** 调用 `sizeGripEnabled()` 读取当前值；它不会修改应用状态。

### `[explicit] QStatusBar::QStatusBar(QWidget *parent = nullptr)`

**作用与语义：**

构建一个带有握把大小和`parent`的状态条。

### `[virtual noexcept] QStatusBar::~QStatusBar()`

**作用与语义：**

摧毁该状态栏，释放所有分配的资源和子控件。

### `void QStatusBar::addPermanentWidget(QWidget *widget, int stretch = 0)`

**作用与语义：**

将给定的 `widget` 永久添加到该状态栏，如果控件还不是该`QStatusBar`对象的子节点，则重新父级。`stretch` 参数用于计算该`widget`的合适大小，随着状态栏的增长和收小。默认的拉伸因子为 0，即给控件最小空间。
永久性意味着小部件不会被临时消息遮挡。它位于状态栏的最右侧。

### `void QStatusBar::addWidget(QWidget *widget, int stretch = 0)`

**作用与语义：**

将给定的 `widget` 添加到该状态栏，如果控件本身不是该`QStatusBar`对象的子节点，则重新加长。`stretch` 参数用于计算该`widget`的适当大小，随着状态栏的增长和收小。默认拉伸因子为 0，即给控件提供最小空间。
该小部件位于第一个永久小部件的最左侧（见`addPermanentWidget()`），可能会被临时消息遮挡。

### `[slot] void QStatusBar::clearMessage()`

**作用与语义：**

移除所有显示的临时信息。

### `QString QStatusBar::currentMessage() const`

**作用与语义：**

返回当前显示的临时消息，若无则返回空字符串。

### `[override virtual protected] bool QStatusBar::event(QEvent *e)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[protected] void QStatusBar::hideOrShow()`

**作用与语义：**

确保正确的控件被可见。
`showMessage()` 和 `clearMessage()` 函数使用。

### `int QStatusBar::insertPermanentWidget(int index, QWidget *widget, int stretch = 0)`

**作用与语义：**

在给定`index`处永久插入给定的`widget`到该状态栏，如果小部件还不是该`QStatusBar`对象的子节点，则重新父级。如果`index`超出范围，则会附加小部件（此时返回的是小部件的实际索引）。
`stretch`参数用于计算当前`widget`的合适大小，随着状态栏的增长和缩小。默认拉伸因子为0，即给控件最小空间。
永久性意味着小部件不会被临时消息遮挡。它位于状态栏的最右侧。

### `int QStatusBar::insertWidget(int index, QWidget *widget, int stretch = 0)`

**作用与语义：**

将给定`index`的`widget`插入该状态栏，如果控件尚未是该`QStatusBar`对象的子节点，则重新加长。如果`index`超出范围，则附加控件（此时返回的是控件的实际索引）。
`stretch`参数用于计算给定`widget`的合适大小，随着状态栏的增长和缩小。默认的拉伸因子为0，即给控件最小空间。
该小部件位于第一个永久小部件的最左侧（见 `addPermanentWidget()`），可能会被临时消息遮挡。

### `[signal] void QStatusBar::messageChanged(const QString &message)`

**作用与语义：**

每当临时状态消息发生变化时，该信号就会发出。当消息被移除时，新的临时消息会以`message`参数传递，该参数是空字符串。

### `[override virtual protected] void QStatusBar::paintEvent(QPaintEvent *event)`

**作用与语义：**

重实现自：`QWidget::paintEvent`（QPaintEvent *event）。
如果需要，会显示针对油漆`event`的临时信息。
该事件处理程序可以在子类中重新实现，以接收`event`传递的绘画事件。
绘图事件是请求重新绘制一个小部件的全部或部分。它可能由以下原因之一发生：
- `repaint()`或`update()`被援引，
- 小部件被遮挡，现已被发现，或
- 还有很多其他原因。
许多控件在被要求时可以直接重新绘制整个表面，但一些较慢的控件需要通过只绘制请求的区域来优化：`QPaintEvent::region()`。这种速度优化不会改变结果，因为在事件处理过程中绘制会被裁剪到该区域。例如，`QListView`和`QTableView`就是这么做的。
Qt 还试图通过将多个绘画事件合并为一个来加快绘画速度。当 `update()` 被多次调用或窗口系统发送多个绘画事件时，Qt 会将这些事件合并为一个区域更大的事件（参见 `QRegion::united()`）。`repaint()` 函数不支持这种优化，因此我们建议尽可能使用 `update()`。
当绘制事件发生时，更新区域通常已经被擦除，所以你是在小部件的背景上作画。
背景可以用`setBackgroundRole()`和`setPalette()`设置。
自 Qt 4.0 起，`QWidget` 会自动对绘画进行双缓冲，因此无需在 paintEvent() 中编写双重缓冲代码以避免闪烁。
注意：通常，你应避免在paintEvent()中调用`update()`或`repaint()`。例如，在paintEvent()中调用`update()`或`repaint()`会导致行为未定义;孩子可能会获得也可能不会获得绘画事件。
警告：如果你使用没有 Qt backingstore 的自定义绘图引擎，必须设置`Qt::WA_PaintOnScreen`。否则，`QWidget::paintEngine()` 永远不会被调用;Backingstore 将被使用。

### `[protected] void QStatusBar::reformat()`

**作用与语义：**

改变状态栏的外观以适应物品的变化。
特殊子类可能需要此功能，但几何管理通常会处理必要的重排。

### `void QStatusBar::removeWidget(QWidget *widget)`

**作用与语义：**

移除状态栏中指定的`widget`。
注意：该函数不会删除小部件，而是隐藏它。要重新添加小部件，必须调用`addWidget()`和`show()`函数。

### `[override virtual protected] void QStatusBar::resizeEvent(QResizeEvent *e)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件调整大小事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `[override virtual protected] void QStatusBar::showEvent(QShowEvent *)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。
该事件处理程序可以在子类中重新实现，以接收传递给 `event` 参数的控件显示事件。
非自发的展示事件会在展示前立即发送到小部件。窗口的自发展示事件则在展示之后交付。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，窗口恢复时自发显示事件。收到自发隐藏事件后，小部件仍被视为`isVisible()`可见。

### `[slot] void QStatusBar::showMessage(const QString &message, int timeout = 0)`

**作用与语义：**

隐藏正常状态指示，并在指定毫秒（`timeout`）内显示给定的 `message`。如果 `timeout` 为 0（默认），`message` 会一直显示，直到调用 `clearMessage()` 槽函数或再次调用 showMessage() 槽函数以更改消息。
注意，showMessage() 用于显示工具提示文本的临时解释，因此仅`timeout`为 0 并不足以显示永久消息。

### `bool isSizeGripEnabled() const`

**作用与语义：**

该属性决定状态栏右下角`QSizeGrip`是否启用。
默认情况下，尺寸握把是启用的。

**如何使用：** 调用 `isSizeGripEnabled()` 读取当前值；它不会修改应用状态。

### `void setSizeGripEnabled(bool)`

**作用与语义：**

该属性决定状态栏右下角`QSizeGrip`是否启用。
默认情况下，尺寸握把是启用的。

**如何使用：** 调用 `setSizeGripEnabled(...)` 修改 `sizeGripEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QStatusBar` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
