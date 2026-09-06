# QGesture

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGesture` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGesture` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGesture>`
- 继承自：QObject
- 直接派生类：QPanGesture、QPinchGesture、QSwipeGesture、QTapAndHoldGesture,、QTapGesture

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

- `enum GestureCancelPolicy { CancelNone, CancelAllInContext }`

### 属性

- `gestureCancelPolicy : QGesture::GestureCancelPolicy`
- `gestureType : Qt::GestureType`
- `hasHotSpot : bool`
- `hotSpot : QPointF`
- `state : Qt::GestureState`

### 公有函数

- `QGesture(QObject *parent = nullptr)`
- `virtual ~QGesture()`
- `QGesture::GestureCancelPolicy gestureCancelPolicy() const`
- `Qt::GestureType gestureType() const`
- `bool hasHotSpot() const`
- `QPointF hotSpot() const`
- `void setGestureCancelPolicy(QGesture::GestureCancelPolicy policy)`
- `void setHotSpot(const QPointF &value)`
- `Qt::GestureState state() const`
- `void unsetHotSpot()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QGesture::GestureCancelPolicy`

**作用与语义：**

这个枚举描述了接受一个手势时，其他手势都会自动取消。
- `QGesture::CancelNone`：`0`;接受此手势后，其他手势将不受影响。
- `QGesture::CancelAllInContext`：`1`;接受该手势后，所有在上下文中激活的手势（即订阅时指定的`Qt::GestureFlag`）将被取消。

### `gestureCancelPolicy : QGesture::GestureCancelPolicy`

**作用与语义：**

此属性保存用于决定在接受手势时发生什么的策略。
在接受一个手势时，Qt 可以自动取消属于其他目标的其他手势。该策略通常设置为不取消任何其他手势，也可以设置为取消上下文中所有活动手势。例如，对于所有子部件。

**如何使用：** 调用 `gestureCancelPolicy()` 读取当前值；它不会修改应用状态。

### `[read-only] gestureType : Qt::GestureType`

**作用与语义：**

此属性保存手势的类型。

**如何使用：** 调用 `gestureType()` 读取当前值；它不会修改应用状态。

### `[read-only] hasHotSpot : bool`

**作用与语义：**

该属性适用于手势是否存在热点。

**如何使用：** 调用 `hasHotSpot()` 读取当前值；它不会修改应用状态。

### `hotSpot : QPointF`

**作用与语义：**

该属性包含用于寻找手势事件接收者的点。
热点是全局坐标系中的一个点，使用`QWidget::mapFromGlobal()`或 `QGestureEvent::mapToGraphicsScene()` 来获得局部热点。
热点应由手势识别器设置，以便手势事件传递到`QGraphicsObject`。

**如何使用：** 调用 `hotSpot()` 读取当前值；它不会修改应用状态。

### `[read-only] state : Qt::GestureState`

**作用与语义：**

该属性表示手势当前状态。

**如何使用：** 调用 `state()` 读取当前值；它不会修改应用状态。

### `[explicit] QGesture::QGesture(QObject *parent = nullptr)`

**作用与语义：**

用给定的 `parent` 构造一个新的手势对象。
QGesture对象由`QGestureRecognizer::create()`函数中的手势识别器创建。

### `[virtual noexcept] QGesture::~QGesture()`

**作用与语义：**

会破坏手势对象。

### `QGesture::GestureCancelPolicy gestureCancelPolicy() const`

**作用与语义：**

此属性保存用于决定在接受手势时发生什么的策略。
在接受一个手势时，Qt 可以自动取消属于其他目标的其他手势。该策略通常设置为不取消任何其他手势，也可以设置为取消上下文中所有活动手势。例如，对于所有子部件。

**如何使用：** 调用 `gestureCancelPolicy()` 读取当前值；它不会修改应用状态。

### `Qt::GestureType gestureType() const`

**作用与语义：**

此属性保存手势的类型。

**如何使用：** 调用 `gestureType()` 读取当前值；它不会修改应用状态。

### `bool hasHotSpot() const`

**作用与语义：**

该属性适用于手势是否存在热点。

**如何使用：** 调用 `hasHotSpot()` 读取当前值；它不会修改应用状态。

### `QPointF hotSpot() const`

**作用与语义：**

该属性包含用于寻找手势事件接收者的点。
热点是全局坐标系中的一个点，使用`QWidget::mapFromGlobal()`或 `QGestureEvent::mapToGraphicsScene()` 来获得局部热点。
热点应由手势识别器设置，以便手势事件传递到`QGraphicsObject`。

**如何使用：** 调用 `hotSpot()` 读取当前值；它不会修改应用状态。

### `void setGestureCancelPolicy(QGesture::GestureCancelPolicy policy)`

**作用与语义：**

此属性保存用于决定在接受手势时发生什么的策略。
在接受一个手势时，Qt 可以自动取消属于其他目标的其他手势。该策略通常设置为不取消任何其他手势，也可以设置为取消上下文中所有活动手势。例如，对于所有子部件。

**如何使用：** 调用 `setGestureCancelPolicy(...)` 修改 `gestureCancelPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setHotSpot(const QPointF &value)`

**作用与语义：**

该属性包含用于寻找手势事件接收者的点。
热点是全局坐标系中的一个点，使用`QWidget::mapFromGlobal()`或 `QGestureEvent::mapToGraphicsScene()` 来获得局部热点。
热点应由手势识别器设置，以便手势事件传递到`QGraphicsObject`。

**如何使用：** 调用 `setHotSpot(...)` 修改 `hotSpot`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `Qt::GestureState state() const`

**作用与语义：**

该属性表示手势当前状态。

**如何使用：** 调用 `state()` 读取当前值；它不会修改应用状态。

### `void unsetHotSpot()`

**作用与语义：**

该属性包含用于寻找手势事件接收者的点。
热点是全局坐标系中的一个点，使用`QWidget::mapFromGlobal()`或 `QGestureEvent::mapToGraphicsScene()` 来获得局部热点。
热点应由手势识别器设置，以便手势事件传递到`QGraphicsObject`。

**如何使用：** 调用 `unsetHotSpot()` 读取当前值；它不会修改应用状态。

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

`QGesture` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
