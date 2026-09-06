# QScroller

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QScroller` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QScroller` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QScroller>`
- 继承自：QObject
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

- `enum Input { InputPress, InputMove, InputRelease }`
- `enum ScrollerGestureType { TouchGesture, LeftMouseButtonGesture, MiddleMouseButtonGesture, RightMouseButtonGesture }`
- `enum State { Inactive, Pressed, Dragging, Scrolling }`

### 属性

- `scrollerProperties : QScrollerProperties`
- `state : State`

### 公有函数

- `QPointF finalPosition() const`
- `bool handleInput(QScroller::Input input, const QPointF &position, qint64 timestamp = 0)`
- `QPointF pixelPerMeter() const`
- `QScrollerProperties scrollerProperties() const`
- `void setSnapPositionsX(const QList<qreal> &positions)`
- `void setSnapPositionsX(qreal first, qreal interval)`
- `void setSnapPositionsY(const QList<qreal> &positions)`
- `void setSnapPositionsY(qreal first, qreal interval)`
- `QScroller::State state() const`
- `void stop()`
- `QObject * target() const`
- `QPointF velocity() const`

### 公有槽函数

- `void ensureVisible(const QRectF &rect, qreal xmargin, qreal ymargin)`
- `void ensureVisible(const QRectF &rect, qreal xmargin, qreal ymargin, int scrollTime)`
- `void resendPrepareEvent()`
- `void scrollTo(const QPointF &pos)`
- `void scrollTo(const QPointF &pos, int scrollTime)`
- `void setScrollerProperties(const QScrollerProperties &prop)`

### 信号

- `void scrollerPropertiesChanged(const QScrollerProperties &newProperties)`
- `void stateChanged(QScroller::State newState)`

### 静态公有成员

- `QList<QScroller *> activeScrollers()`
- `Qt::GestureType grabGesture(QObject *target, QScroller::ScrollerGestureType scrollGestureType = TouchGesture)`
- `Qt::GestureType grabbedGesture(QObject *target)`
- `bool hasScroller(QObject *target)`
- `QScroller * scroller(QObject *target)`
- `const QScroller * scroller(const QObject *target)`
- `void ungrabGesture(QObject *target)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QScroller::Input`

**作用与语义：**

该枚举包含一个输入设备无关的视图，涵盖与`QScroller`相关的输入事件。
- `QScroller::InputPress`：`1`;用户按下输入设备（例如`QEvent::MouseButtonPress`、`QEvent::GraphicsSceneMousePress`、`QEvent::TouchBegin`）
- `QScroller::InputMove`：`2`;用户移动输入设备（例如`QEvent::MouseMove`、`QEvent::GraphicsSceneMouseMove`、`QEvent::TouchUpdate`）
- `QScroller::InputRelease`：`3`;用户释放输入设备（例如`QEvent::MouseButtonRelease`、`QEvent::GraphicsSceneMouseRelease`、`QEvent::TouchEnd`）

### `enum QScroller::ScrollerGestureType`

**作用与语义：**

该枚举包含了`QScroller`手势识别器支持的不同手势类型。
- `QScroller::TouchGesture`：`0`;手势识别器仅在触摸事件时触发。具体来说，使用触摸屏时对单点反应，使用触摸板时对双重触点有反应。
- `QScroller::LeftMouseButtonGesture`：`1`;手势识别器仅在左键事件时触发。
- `QScroller::MiddleMouseButtonGesture`：`3`;手势识别器仅在中键事件时触发。
- `QScroller::RightMouseButtonGesture`：`2`;手势识别器仅在右键事件时触发。

### `enum QScroller::State`

**作用与语义：**

该枚举包含了不同的`QScroller`状态。
- `QScroller::Inactive`：`0`;滚动器没有滚动，也没有按压任何按钮。
- `QScroller::Pressed`：`1`;收到触摸事件或鼠标按钮被按下，但滚动区域目前未被拖动。
- `QScroller::Dragging`：`2`;滚动区域当前跟随触摸点或鼠标。
- `QScroller::Scrolling`：`3`;卷轴区域会自行移动。

### `scrollerProperties : QScrollerProperties`

**作用与语义：**

该属性包含该滚动器的滚动属性。`QScroller`利用这些属性来确定其滚动行为。

**如何使用：** 调用 `scrollerProperties()` 读取当前值；它不会修改应用状态。

### `[read-only] state : State`

**作用与语义：**

该属性表示滚轴的状态。

**如何使用：** 调用 `state()` 读取当前值；它不会修改应用状态。

### `[static] QList<QScroller *> QScroller::activeScrollers()`

**作用与语义：**

返回当前活跃`QScroller`对象的全应用列表。活跃`QScroller`对象位于未`QScroller::Inactive`的`state()`中。该函数在编写自己的手势识别器时非常有用。

### `[slot] void QScroller::ensureVisible(const QRectF &rect, qreal xmargin, qreal ymargin)`

**作用与语义：**

开始滚动，使矩形`rect`在视口内可见，并通过`xmargin`像素数和`ymargin`在矩形周围设置额外边距。
如果无法将矩形和边距放入视口内，内容会被滚动，以便尽可能多地从`rect`中可见。
滚动速度计算使得在平台定义的时间跨度后达到给定位置。
该函数通过调用`scrollTo()`来执行实际滚动。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
scroller， qOverload（&QScroller：：ensureVisible））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
scroller， [receiver = scroller]（const QRectF &rect， qreal xmargin， qreal ymargin） { receiver->ensureVisible（rect， xmargin， ymargin）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] void QScroller::ensureVisible(const QRectF &rect, qreal xmargin, qreal ymargin, int scrollTime)`

**作用与语义：**

该版本将在`scrollTime`毫秒内到达目的地位置。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
scroller， qOverload（&QScroller：：ensureVisible））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
scroller， [receiver = scroller]（const QRectF &rect， qreal xmargin， qreal ymargin， int scrollTime） { receiver->ensureVisible（rect， xmargin， ymargin， scrollTime）; }）;


更多示例和方法，请参见连接超载槽位。

### `QPointF QScroller::finalPosition() const`

**作用与语义：**

返回当前滚动移动的估计最终位置。如果滚动状态未滚动，返回当前位置。当滚动状态为非激活时，结果未定义。
目标位置以像素为单位。

### `[static] Qt::GestureType QScroller::grabGesture(QObject *target, QScroller::ScrollerGestureType scrollGestureType = TouchGesture)`

**作用与语义：**

注册一个自定义滚动手势识别器，获取`target`并返回最终手势类型。如果`scrollGestureType`设置为`TouchGesture`，手势在触摸事件触发。如果设置为`LeftMouseButtonGesture`、`RightMouseButtonGesture`或`MiddleMouseButtonGesture`，则在对应按钮的鼠标事件中触发。
同一对象同时只能激活一个滚动手势。如果你在同一对象上调用两次该函数，它会先取消抓取已有的手势，再抓取新的手势。
注意：为避免不良副作用，触发手势时会消耗鼠标事件。由于初始鼠标按键事件未被消耗，手势会在全局位置`(INT_MIN, INT_MIN)`发送假鼠标释放事件。这确保了收到原始鼠标按压的小部件内部状态一致。

### `[static] Qt::GestureType QScroller::grabbedGesture(QObject *target)`

**作用与语义：**

返回当前抓取的手势类型，`target`返回;如果没有手势，则返回0。

### `bool QScroller::handleInput(QScroller::Input input, const QPointF &position, qint64 timestamp = 0)`

**作用与语义：**

该功能被手势识别器用来通知滚动器新的输入事件。滚动器根据输入事件及其附加的滚动属性改变其内部`state()`。滚动器不会区分事件来自哪种输入设备。因此，事件需要被拆分为`input`类型、`position`和毫秒`timestamp`。`position`必须处于目标的坐标系内。
返回值`true`是否应被调用的过滤器消耗事件，或`false`是否应转发事件给控制。
注意：大多数使用场景下，使用`grabGesture()`应该足够。

### `[static] bool QScroller::hasScroller(QObject *target)`

**作用与语义：**

如果`target`已经创建了`QScroller`对象，返回`true`;否则`false`。

### `QPointF QScroller::pixelPerMeter() const`

**作用与语义：**

返回滚动小部件的像素每米指标。
该值通过使用`QPointF`分别报告x轴和y轴。
注意：请注意，该值应在物理上正确。Qt 返回的实际 DPI 设置可能被底层窗口系统（例如 macOS）故意错误报告。

### `[slot] void QScroller::resendPrepareEvent()`

**作用与语义：**

该函数会重新发送`QScrollPrepareEvent`。调用 resendPrepareEvent 会触发滚动器`QScrollPrepareEvent`。这允许接收方在滚动时重置内容位置和大小。在非活动状态下调用该函数无用，因为准备事件会在滚动开始前再次发送。

### `[slot] void QScroller::scrollTo(const QPointF &pos)`

**作用与语义：**

开始滚动控件，使`pos`点位于视口左上角。
当滚动超出有效滚动区域时的行为是未定义的。在这种情况下，滚动者可能会超出也可能不会。
滚动速度将被计算为在平台定义的时间跨度后到达给定位置。
`pos`以视口坐标表示。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
scroller，qOverload（&QScroller：：scrollTo））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
scroller， [receiver = scroller]（const QPointF &pos） { receiver->scrollTo（pos）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] void QScroller::scrollTo(const QPointF &pos, int scrollTime)`

**作用与语义：**

该版本将在`scrollTime`毫秒内到达目的地位置。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
scroller，qOverload（&QScroller：：scrollTo））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
scroller， [receiver = scroller]（const QPointF &pos， int scrollTime） { receiver->rollTo（pos， scrollTime）; }）;


更多示例和方法，请参见连接超载槽位。

### `[static] QScroller *QScroller::scroller(QObject *target)`

**作用与语义：**

返回给定`target`的滚动器。只要该对象存在，该函数总是返回相同的`QScroller`实例。如果该`target`不存在`QScroller`，则隐式创建一个。在任何时刻，一个对象上不会有超过一个`QScroller`激活。

### `[static] const QScroller *QScroller::scroller(const QObject *target)`

**作用与语义：**

这是scroller()的const版本。

### `[signal] void QScroller::scrollerPropertiesChanged(const QScrollerProperties &newProperties)`

**作用与语义：**

该属性包含该滚动器的滚动属性。`QScroller`利用这些属性来确定其滚动行为。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `scrollerProperties` 的变化，不要把它当作普通函数主动调用。

### `void QScroller::setSnapPositionsX(const QList<qreal> &positions)`

**作用与语义：**

将水平轴的吸附位置设置为`positions`列表。这会覆盖之前设置的所有吸附位置和之前设定的吸附间隔。通过设置空位置列表可以停用吸附。

### `void QScroller::setSnapPositionsX(qreal first, qreal interval)`

**作用与语义：**

将水平轴的吸附位置设置为规则间隔。第一个吸附位置位于`first`。下一个位于`first` `interval`。这可以用来实现列表头部。它覆盖了之前设置的所有吸附位置以及之前设定的吸附区间。吸附可以通过设置间隔 0.0 来停用。

### `void QScroller::setSnapPositionsY(const QList<qreal> &positions)`

**作用与语义：**

将垂直轴的吸附位置设置为`positions`列表。这会覆盖之前设置的所有吸附位置和之前设定的吸附间隔。通过设置空位置列表可以禁用吸附。

### `void QScroller::setSnapPositionsY(qreal first, qreal interval)`

**作用与语义：**

将垂直轴的吸附位置设置为规则间隔。第一个吸附位置位于`first`。下一个吸附位置在`first` `interval`。这覆盖了之前设置的所有吸附位置和之前设定的吸附间隔。吸附可以通过设置间隔为0.0来停用。

### `[signal] void QScroller::stateChanged(QScroller::State newState)`

**作用与语义：**

该属性表示滚轴的状态。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `state` 的变化，不要把它当作普通函数主动调用。

### `void QScroller::stop()`

**作用与语义：**

停止滚动器并重置状态为非激活。

### `QObject *QScroller::target() const`

**作用与语义：**

返回该滚动器的目标对象。

### `[static] void QScroller::ungrabGesture(QObject *target)`

**作用与语义：**

把手势拿回来`target`。如果没有手势，什么都不做。

### `QPointF QScroller::velocity() const`

**作用与语义：**

当状态处于滚动或拖动状态时，返回当前滚动速度（单位为米每秒）。否则返回零速度。
速度分别通过`QPointF`分别报告x轴和y轴。

### `QScrollerProperties scrollerProperties() const`

**作用与语义：**

该属性包含该滚动器的滚动属性。`QScroller`利用这些属性来确定其滚动行为。

**如何使用：** 调用 `scrollerProperties()` 读取当前值；它不会修改应用状态。

### `QScroller::State state() const`

**作用与语义：**

该属性表示滚轴的状态。

**如何使用：** 调用 `state()` 读取当前值；它不会修改应用状态。

### `void setScrollerProperties(const QScrollerProperties &prop)`

**作用与语义：**

该属性包含该滚动器的滚动属性。`QScroller`利用这些属性来确定其滚动行为。

**如何使用：** 调用 `setScrollerProperties(...)` 修改 `scrollerProperties`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QScroller` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
