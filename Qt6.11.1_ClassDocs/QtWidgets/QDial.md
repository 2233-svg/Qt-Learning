# QDial

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QDial` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QDial` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QDial>`
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

### 属性

- `notchSize : int`
- `notchTarget : qreal`
- `notchesVisible : bool`
- `wrapping : bool`

### 公有函数

- `QDial(QWidget *parent = nullptr)`
- `virtual ~QDial()`
- `int notchSize() const`
- `qreal notchTarget() const`
- `bool notchesVisible() const`
- `void setNotchTarget(double target)`
- `bool wrapping() const`

### 重实现的公有函数

- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void setNotchesVisible(bool visible)`
- `void setWrapping(bool on)`

### 保护函数

- `virtual void initStyleOption(QStyleOptionSlider *option) const`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual void paintEvent(QPaintEvent *pe) override`
- `virtual void resizeEvent(QResizeEvent *e) override`
- `virtual void sliderChange(QAbstractSlider::SliderChange change) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only] notchSize : int`

**作用与语义：**

该属性表示当前缺口大小。
缺口大小以距离控制单元计，而非像素，计算为`singleStep()`的整数，导致屏幕上缺口大小接近`notchTarget()`。

**如何使用：** 调用 `notchSize()` 读取当前值；它不会修改应用状态。

### `notchTarget : qreal`

**作用与语义：**

该属性表示凹槽之间的目标像素数。
缺口目标是每个缺口之间`QDial`尝试放置的像素数。
实际尺寸可能与目标尺寸不同。
默认的刘海目标是3.7像素。

**如何使用：** 调用 `notchTarget()` 读取当前值；它不会修改应用状态。

### `notchesVisible : bool`

**作用与语义：**

该属性在缺口是否被显示时成立。
如果属性`true`，则在刻度盘周围画一系列缺口以表示可用数值范围;否则不显示刻度。
默认情况下，该属性是被禁用的。

**如何使用：** 调用 `notchesVisible()` 读取当前值；它不会修改应用状态。

### `wrapping : bool`

**作用与语义：**

该属性决定是否启用包裹。
如果成立，则启用包裹;否则在表盘底部插入空格，分隔有效值范围的两端。
启用时，箭头可按表盘任意角度调整。禁用时，箭头将限制在表盘上部;如果旋转到表盘底部的空隙，则会夹在有效值范围中最近的一端。
默认情况下，该属性是`false`。

**如何使用：** 调用 `wrapping()` 读取当前值；它不会修改应用状态。

### `[explicit] QDial::QDial(QWidget *parent = nullptr)`

**作用与语义：**

制造一个旋钮。
`parent`参数被发送给`QAbstractSlider`构造器。

### `[virtual noexcept] QDial::~QDial()`

**作用与语义：**

会毁掉旋钮。

### `[override virtual protected] bool QDial::event(QEvent *e)`

**作用与语义：**

重实现自：`QAbstractSlider::event`（QEvent *e）。

### `[virtual protected] void QDial::initStyleOption(QStyleOptionSlider *option) const`

**作用与语义：**

用这个`QDial`的值初始化`option`。这种方法适用于子类需要`QStyleOptionSlider`但不想自己填满所有信息时。

### `[override virtual] QSize QDial::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[override virtual protected] void QDial::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseMoveEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标移动事件。
如果关闭鼠标追踪，只有在鼠标移动过程中按下鼠标按钮时才会发生鼠标移动事件。如果开启鼠标追踪，即使未按键，鼠标移动事件也会发生。
`QMouseEvent::position()`报告鼠标光标相对于该小部件的位置。对于按下和释放事件，位置通常与最后一次鼠标移动事件的位置相同，但如果用户的手握手，可能会有所不同。这是底层窗口系统的功能，而非Qt。
如果你想在鼠标移动时立即显示提示（例如，获取鼠标坐标与`QMouseEvent::position()`并显示为提示），你必须先启用上述的鼠标追踪功能。然后，为了确保提示立即更新，你必须在鼠标移动事件（mouseMoveEvent）实现中调用`QToolTip::showText()`而不是`setToolTip()`。

### `[override virtual protected] void QDial::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[override virtual protected] void QDial::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标释放事件。

### `[override virtual protected] void QDial::paintEvent(QPaintEvent *pe)`

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

### `[override virtual protected] void QDial::resizeEvent(QResizeEvent *e)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件调整大小事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `[override virtual] QSize QDial::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `[override virtual protected] void QDial::sliderChange(QAbstractSlider::SliderChange change)`

**作用与语义：**

重实现自：`QAbstractSlider::sliderChange`（QAbstractSlider：：SliderChange change）。
重新实现该虚拟功能以跟踪滑块的变化，如`SliderRangeChange`、`SliderOrientationChange`、`SliderStepsChange`或`SliderValueChange`。默认实现仅更新显示，忽略`change`参数。

### `int notchSize() const`

**作用与语义：**

该属性表示当前缺口大小。
缺口大小以距离控制单元计，而非像素，计算为`singleStep()`的整数，导致屏幕上缺口大小接近`notchTarget()`。

**如何使用：** 调用 `notchSize()` 读取当前值；它不会修改应用状态。

### `qreal notchTarget() const`

**作用与语义：**

该属性表示凹槽之间的目标像素数。
缺口目标是每个缺口之间`QDial`尝试放置的像素数。
实际尺寸可能与目标尺寸不同。
默认的刘海目标是3.7像素。

**如何使用：** 调用 `notchTarget()` 读取当前值；它不会修改应用状态。

### `bool notchesVisible() const`

**作用与语义：**

该属性在缺口是否被显示时成立。
如果属性`true`，则在刻度盘周围画一系列缺口以表示可用数值范围;否则不显示刻度。
默认情况下，该属性是被禁用的。

**如何使用：** 调用 `notchesVisible()` 读取当前值；它不会修改应用状态。

### `void setNotchTarget(double target)`

**作用与语义：**

该属性表示凹槽之间的目标像素数。
缺口目标是每个缺口之间`QDial`尝试放置的像素数。
实际尺寸可能与目标尺寸不同。
默认的刘海目标是3.7像素。

**如何使用：** 调用 `setNotchTarget(...)` 修改 `notchTarget`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool wrapping() const`

**作用与语义：**

该属性决定是否启用包裹。
如果成立，则启用包裹;否则在表盘底部插入空格，分隔有效值范围的两端。
启用时，箭头可按表盘任意角度调整。禁用时，箭头将限制在表盘上部;如果旋转到表盘底部的空隙，则会夹在有效值范围中最近的一端。
默认情况下，该属性是`false`。

**如何使用：** 调用 `wrapping()` 读取当前值；它不会修改应用状态。

### `void setNotchesVisible(bool visible)`

**作用与语义：**

该属性在缺口是否被显示时成立。
如果属性`true`，则在刻度盘周围画一系列缺口以表示可用数值范围;否则不显示刻度。
默认情况下，该属性是被禁用的。

**如何使用：** 调用 `setNotchesVisible(...)` 修改 `notchesVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWrapping(bool on)`

**作用与语义：**

该属性决定是否启用包裹。
如果成立，则启用包裹;否则在表盘底部插入空格，分隔有效值范围的两端。
启用时，箭头可按表盘任意角度调整。禁用时，箭头将限制在表盘上部;如果旋转到表盘底部的空隙，则会夹在有效值范围中最近的一端。
默认情况下，该属性是`false`。

**如何使用：** 调用 `setWrapping(...)` 修改 `wrapping`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QDial` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
