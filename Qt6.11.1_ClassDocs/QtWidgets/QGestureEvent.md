# QGestureEvent

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGestureEvent` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGestureEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QGestureEvent>`
- 继承自：QEvent
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。 使用时通常按这个过程组织：Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QGestureEvent(const QList<QGesture *> &gestures)`
- `virtual ~QGestureEvent()`
- `void accept(QGesture *gesture)`
- `void accept(Qt::GestureType gestureType)`
- `QList<QGesture *> activeGestures() const`
- `QList<QGesture *> canceledGestures() const`
- `QGesture * gesture(Qt::GestureType type) const`
- `QList<QGesture *> gestures() const`
- `void ignore(QGesture *gesture)`
- `void ignore(Qt::GestureType gestureType)`
- `bool isAccepted(QGesture *gesture) const`
- `bool isAccepted(Qt::GestureType gestureType) const`
- `QPointF mapToGraphicsScene(const QPointF &gesturePoint) const`
- `void setAccepted(QGesture *gesture, bool value)`
- `void setAccepted(Qt::GestureType gestureType, bool value)`
- `QWidget * widget() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QGestureEvent::QGestureEvent(const QList<QGesture *> &gestures)`

**作用与语义：**

创建包含`gestures`列表的新QGestureEvent。

### `[virtual noexcept] QGestureEvent::~QGestureEvent()`

**作用与语义：**

毁了`QGestureEvent`。

### `void QGestureEvent::accept(QGesture *gesture)`

**作用与语义：**

设置给定`gesture`对象的接受标志，相当于调用 `setAccepted`（手势，真）。
设置 accept 标志表示事件接收方需要该手势。不需要的手势可以传播到父控件。

### `void QGestureEvent::accept(Qt::GestureType gestureType)`

**作用与语义：**

设置给定`gestureType`的接受标志，相当于调用 `setAccepted`（gestureType， true）。
设置 accept 标志表示事件接收方需要该手势。不需要的手势可以传播到父控件。

### `QList<QGesture *> QGestureEvent::activeGestures() const`

**作用与语义：**

返回一个激活（未取消）手势列表。

### `QList<QGesture *> QGestureEvent::canceledGestures() const`

**作用与语义：**

返回已取消的手势列表。

### `QGesture *QGestureEvent::gesture(Qt::GestureType type) const`

**作用与语义：**

返回一个手势对象`type`。

### `QList<QGesture *> QGestureEvent::gestures() const`

**作用与语义：**

返回活动中所有手势。

### `void QGestureEvent::ignore(QGesture *gesture)`

**作用与语义：**

清除给定 `gesture` 对象的 accept flag 参数，相当于调用 `setAccepted`(gesture, false)。
清除 accept flag 表明事件接收器不希望该手势。未被接受的手势可能会传播到父部件。

### `void QGestureEvent::ignore(Qt::GestureType gestureType)`

**作用与语义：**

清除给定`gestureType`的接受标志参数，相当于调用 `setAccepted`（手势，false）。
清除接受标志表示事件接收方不想要该手势。不需要的手势可能会传播到父控件。

### `bool QGestureEvent::isAccepted(QGesture *gesture) const`

**作用与语义：**

如果接受 `gesture`，则返回 `true`；否则返回 `false`。

### `bool QGestureEvent::isAccepted(Qt::GestureType gestureType) const`

**作用与语义：**

如果接受类型`gestureType`的手势，返回`true`;否则返回`false`。

### `QPointF QGestureEvent::mapToGraphicsScene(const QPointF &gesturePoint) const`

**作用与语义：**

如果`gesturePoint`位于图形视图内，则返回场景本地坐标。
当手势事件传递给`QGraphicsObject`，将屏幕中的某个点转换为场景本地坐标时，这个函数可能非常有用。

### `void QGestureEvent::setAccepted(QGesture *gesture, bool value)`

**作用与语义：**

将给定`gesture`对象的接受标志设置为指定的`value`。
设置接受标志表示事件接收方需要该`gesture`。不需要的手势可能会传播到父控件。
默认情况下，类型`QEvent::Gesture`事件中的手势被接受，`QEvent::GestureOverride`事件中的手势被忽略。
为了方便起见，接受标志也可以用`accept`（手势）设置，并用`ignore`（手势）来清除。

### `void QGestureEvent::setAccepted(Qt::GestureType gestureType, bool value)`

**作用与语义：**

将给定`gestureType`对象的接受标志设置为指定的`value`。
设置接受标志表示事件接收方希望接收指定类型的手势 `gestureType`。不需要的手势可能会传播到父控件。
默认情况下，类型`QEvent::Gesture`事件中的手势被接受，`QEvent::GestureOverride`事件中的手势被忽略。
为了方便起见，接受标志也可以用 `accept`（gestureType）设置，并用 `ignore`（gestureType）来清除。

### `QWidget *QGestureEvent::widget() const`

**作用与语义：**

返回事件发生的控件。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGestureEvent` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
