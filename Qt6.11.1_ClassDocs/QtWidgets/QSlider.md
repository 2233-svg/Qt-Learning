# QSlider

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QSlider` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QSlider` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QSlider>`
- 继承自：QAbstractSlider
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

- `enum TickPosition { NoTicks, TicksBothSides, TicksAbove, TicksBelow, TicksLeft, TicksRight }`

### 属性

- `tickInterval : int`
- `tickPosition : TickPosition`

### 公有函数

- `QSlider(QWidget *parent = nullptr)`
- `QSlider(Qt::Orientation orientation, QWidget *parent = nullptr)`
- `virtual ~QSlider()`
- `void setTickInterval(int ti)`
- `void setTickPosition(QSlider::TickPosition position)`
- `int tickInterval() const`
- `QSlider::TickPosition tickPosition() const`

### 重实现的公有函数

- `virtual bool event(QEvent *event) override`
- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 保护函数

- `virtual void initStyleOption(QStyleOptionSlider *option) const`

### 重实现的保护函数

- `virtual void mouseMoveEvent(QMouseEvent *ev) override`
- `virtual void mousePressEvent(QMouseEvent *ev) override`
- `virtual void mouseReleaseEvent(QMouseEvent *ev) override`
- `virtual void paintEvent(QPaintEvent *ev) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSlider::TickPosition`

**作用与语义：**

该枚举指定了刻度标记相对于滑块槽和用户移动手柄的位置。
- `QSlider::NoTicks`：`0`;不要画任何勾号。
- `QSlider::TicksBothSides`：`3`;在沟槽两侧画刻痕。
- `QSlider::TicksAbove`：`1`;在（水平）滑块上方画勾
- `QSlider::TicksBelow`：`2`;在（水平）滑块下方画刻号
- `QSlider::TicksLeft`：`TicksAbove`;在（垂直）滑块左侧画刻号
- `QSlider::TicksRight`：`TicksBelow`;在（垂直）滑块右侧画刻号

### `tickInterval : int`

**作用与语义：**

该属性表示刻度之间的区间。
这是一个值区间，而不是像素区间。如果是0，滑块会在singleStep和pageStep之间选择。
默认值是0。

**如何使用：** 调用 `tickInterval()` 读取当前值；它不会修改应用状态。

### `tickPosition : TickPosition`

**作用与语义：**

该属性表示该滑块的勾选位置。
有效值由`QSlider::TickPosition`枚举描述。
默认值是`QSlider::NoTicks`。

**如何使用：** 调用 `tickPosition()` 读取当前值；它不会修改应用状态。

### `[explicit] QSlider::QSlider(QWidget *parent = nullptr)`

**作用与语义：**

用给定的`parent`构造一个垂直滑块。

### `[explicit] QSlider::QSlider(Qt::Orientation orientation, QWidget *parent = nullptr)`

**作用与语义：**

构造一个带有给定`parent`的滑块。`orientation`参数决定滑块是水平还是垂直;有效值为`Qt::Vertical`和`Qt::Horizontal`。

### `[virtual noexcept] QSlider::~QSlider()`

**作用与语义：**

摧毁了这个滑球。

### `[override virtual] bool QSlider::event(QEvent *event)`

**作用与语义：**

重实现自：`QAbstractSlider::event`（QEvent *e）。

### `[virtual protected] void QSlider::initStyleOption(QStyleOptionSlider *option) const`

**作用与语义：**

用这个`QSlider`的值初始化`option`。这种方法适用于需要`QStyleOptionSlider`但不想自己填满所有信息的子类。

### `[override virtual] QSize QSlider::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[override virtual protected] void QSlider::mouseMoveEvent(QMouseEvent *ev)`

**作用与语义：**

重实现自：`QWidget::mouseMoveEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标移动事件。
如果关闭鼠标追踪，只有在鼠标移动过程中按下鼠标按钮时才会发生鼠标移动事件。如果开启鼠标追踪，即使未按键，鼠标移动事件也会发生。
`QMouseEvent::position()`报告鼠标光标相对于该小部件的位置。对于按下和释放事件，位置通常与最后一次鼠标移动事件的位置相同，但如果用户的手握手，可能会有所不同。这是底层窗口系统的功能，而非Qt。
如果你想在鼠标移动时立即显示提示（例如，获取鼠标坐标与`QMouseEvent::position()`并显示为提示），你必须先启用上述的鼠标追踪功能。然后，为了确保提示立即更新，你必须在鼠标移动事件（mouseMoveEvent）实现中调用`QToolTip::showText()`而不是`setToolTip()`。

### `[override virtual protected] void QSlider::mousePressEvent(QMouseEvent *ev)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[override virtual protected] void QSlider::mouseReleaseEvent(QMouseEvent *ev)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标释放事件。

### `[override virtual protected] void QSlider::paintEvent(QPaintEvent *ev)`

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

### `[override virtual] QSize QSlider::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `void setTickInterval(int ti)`

**作用与语义：**

该属性表示刻度之间的区间。
这是一个值区间，而不是像素区间。如果是0，滑块会在singleStep和pageStep之间选择。
默认值是0。

**如何使用：** 调用 `setTickInterval(...)` 修改 `tickInterval`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTickPosition(QSlider::TickPosition position)`

**作用与语义：**

该属性表示该滑块的勾选位置。
有效值由`QSlider::TickPosition`枚举描述。
默认值是`QSlider::NoTicks`。

**如何使用：** 调用 `setTickPosition(...)` 修改 `tickPosition`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int tickInterval() const`

**作用与语义：**

该属性表示刻度之间的区间。
这是一个值区间，而不是像素区间。如果是0，滑块会在singleStep和pageStep之间选择。
默认值是0。

**如何使用：** 调用 `tickInterval()` 读取当前值；它不会修改应用状态。

### `QSlider::TickPosition tickPosition() const`

**作用与语义：**

该属性表示该滑块的勾选位置。
有效值由`QSlider::TickPosition`枚举描述。
默认值是`QSlider::NoTicks`。

**如何使用：** 调用 `tickPosition()` 读取当前值；它不会修改应用状态。

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

`QSlider` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
