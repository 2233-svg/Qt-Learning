# QEventPoint

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是一个事件/输入数据对象，通常由 Qt 创建并通过事件处理函数、过滤器或信号传递给应用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QEventPoint` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QEventPoint>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。 使用时通常按这个过程组织：Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum State { Unknown, Stationary, Pressed, Updated, Released }`
- `flags States`

### 属性

- `accepted : bool`
- `device : const QPointingDevice*`
- `ellipseDiameters : const QSizeF`
- `globalGrabPosition : const QPointF`
- `globalLastPosition : const QPointF`
- `globalPosition : const QPointF`
- `globalPressPosition : const QPointF`
- `grabPosition : const QPointF`
- `id : const int`
- `lastPosition : const QPointF`
- `lastTimestamp : const ulong`
- `position : const QPointF`
- `pressPosition : const QPointF`
- `pressTimestamp : const ulong`
- `pressure : const qreal`
- `rotation : const qreal`
- `sceneGrabPosition : const QPointF`
- `sceneLastPosition : const QPointF`
- `scenePosition : const QPointF`
- `scenePressPosition : const QPointF`
- `state : const State`
- `timeHeld : const qreal`
- `timestamp : const ulong`
- `uniqueId : const QPointingDeviceUniqueId`
- `velocity : const QVector2D`

### 公有函数

- `QEventPoint(int pointId, QEventPoint::State state, const QPointF &scenePosition, const QPointF &globalPosition)`
- `QEventPoint(const QEventPoint &other)`
- `QEventPoint(QEventPoint &&other)`
- `~QEventPoint()`
- `const QPointingDevice * device() const`
- `QSizeF ellipseDiameters() const`
- `QPointF globalGrabPosition() const`
- `QPointF globalLastPosition() const`
- `QPointF globalPosition() const`
- `QPointF globalPressPosition() const`
- `QPointF grabPosition() const`
- `int id() const`
- `bool isAccepted() const`
- `QPointF lastPosition() const`
- `ulong lastTimestamp() const`
- `QPointF normalizedPosition() const`
- `QPointF position() const`
- `QPointF pressPosition() const`
- `ulong pressTimestamp() const`
- `qreal pressure() const`
- `qreal rotation() const`
- `QPointF sceneGrabPosition() const`
- `QPointF sceneLastPosition() const`
- `QPointF scenePosition() const`
- `QPointF scenePressPosition() const`
- `void setAccepted(bool accepted = true)`
- `QEventPoint::State state() const`
- `qreal timeHeld() const`
- `ulong timestamp() const`
- `QPointingDeviceUniqueId uniqueId() const`
- `QVector2D velocity() const`
- `bool operator!=(const QEventPoint &other) const`
- `QEventPoint & operator=(QEventPoint &&other)`
- `QEventPoint & operator=(const QEventPoint &other)`
- `bool operator==(const QEventPoint &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QEventPoint::Stateflags QEventPoint::States`

**作用与语义：**

指定该事件点的状态。
- `QEventPoint::Unknown`：`Qt::TouchPointUnknownState`;状态不明。
- `QEventPoint::Stationary`：`Qt::TouchPointStationary`;事件点未移动。
- `QEventPoint::Pressed`：`Qt::TouchPointPressed`;按下触摸点或按钮。
- `QEventPoint::Updated`：`Qt::TouchPointMoved`;事件点已更新。
- `QEventPoint::Released`：`Qt::TouchPointReleased`;触点或按钮被松开。
状态类型是QFlag的typedef<State>。它存储状态值的或组合。

### `accepted : bool`

**作用与语义：**

该属性表示事件点的公认状态。
在基于控件的应用中，这一属性不被使用，因为只有小部件接受或拒绝完整`QInputEvent`才有意义。
然而，在 Qt Quick 中，通常项目或事件处理程序只接受实际参与手势的`QTouchEvent`中单个点，而其他点则可以传递给其他项目或处理者。为了保持一致，这适用于任何`QPointerEvent`;只有当`QPointerEvent`中的所有点都被接受后，才会进行交付。

**如何使用：** 调用 `accepted()` 读取当前值；它不会修改应用状态。

### `[read-only] device : const QPointingDevice*`

**作用与语义：**

此属性保存生成此事件点的指点设备。

**如何使用：** 调用 `device()` 读取当前值；它不会修改应用状态。

### `[read-only] ellipseDiameters : const QSizeF`

**作用与语义：**

该属性包含触摸点边界椭圆的宽度和高度。
返回值以逻辑像素为单位。大多数触摸屏无法检测接触点的形状，鼠标或平板电脑设备也无法检测，因此空尺寸是最常见的数值。在某些触摸屏上，直径可能非零且始终相等（椭圆近似为圆形）。

**如何使用：** 调用 `ellipseDiameters()` 读取当前值；它不会修改应用状态。

### `[read-only] globalGrabPosition : const QPointF`

**作用与语义：**

该属性表示该点被抓取的全局位置。
全局位置相对于屏幕或虚拟桌面表示。

**如何使用：** 调用 `globalGrabPosition()` 读取当前值；它不会修改应用状态。

### `[read-only] globalLastPosition : const QPointF`

**作用与语义：**

该属性表示该点在上一次按键或移动事件中的全局位置。
全局位置相对于屏幕或虚拟桌面表示。

**如何使用：** 调用 `globalLastPosition()` 读取当前值；它不会修改应用状态。

### `[read-only] globalPosition : const QPointF`

**作用与语义：**

该属性表示该点的全局位置。
全局位置相对于屏幕或虚拟桌面表示。

**如何使用：** 调用 `globalPosition()` 读取当前值；它不会修改应用状态。

### `[read-only] globalPressPosition : const QPointF`

**作用与语义：**

该属性表示该点被按下的全局位置。
全局位置相对于屏幕或虚拟桌面表示。

**如何使用：** 调用 `globalPressPosition()` 读取当前值；它不会修改应用状态。

### `[read-only] grabPosition : const QPointF`

**作用与语义：**

此属性保存抓取此点时的位置。
位置相对于接收事件的部件或项。

**如何使用：** 调用 `grabPosition()` 读取当前值；它不会修改应用状态。

### `[read-only] id : const int`

**作用与语义：**

该属性包含该事件点的ID编号。
注意：不要假设ID编号从零开始或它们是连续的。由于底层驱动的工作方式，这种假设往往是错误的。

**如何使用：** 调用 `id()` 读取当前值；它不会修改应用状态。

### `[read-only] lastPosition : const QPointF`

**作用与语义：**

该属性表示该点在上一次按键或移动事件中的位置。
位置相对于接收事件的小部件或项目。

**如何使用：** 调用 `lastPosition()` 读取当前值；它不会修改应用状态。

### `[read-only] lastTimestamp : const ulong`

**作用与语义：**

该属性包含包含该点的前一根`QPointerEvent`的时间。

**如何使用：** 调用 `lastTimestamp()` 读取当前值；它不会修改应用状态。

### `[read-only] position : const QPointF`

**作用与语义：**

该属性表示该点的位置。
位置相对于接收事件的小部件或项目。

**如何使用：** 调用 `position()` 读取当前值；它不会修改应用状态。

### `[read-only] pressPosition : const QPointF`

**作用与语义：**

此属性保存按下此点时的位置。
位置相对于接收事件的部件或项。

**如何使用：** 调用 `pressPosition()` 读取当前值；它不会修改应用状态。

### `[read-only] pressTimestamp : const ulong`

**作用与语义：**

该属性记录了该点被压制的最近时间。

**如何使用：** 调用 `pressTimestamp()` 读取当前值；它不会修改应用状态。

### `[read-only] pressure : const qreal`

**作用与语义：**

该属性承受了该点的压力。
回报值范围在`0.0`到`1.0`之间。

**如何使用：** 调用 `pressure()` 读取当前值；它不会修改应用状态。

### `[read-only] rotation : const qreal`

**作用与语义：**

该属性表示该点的角度方向。
返回值以度为单位，0（默认）表示手指、标记或触控笔朝上，负角度表示向左旋转，正角度表示向右旋转。大多数触摸屏不检测旋转，因此0是最常见的数值。

**如何使用：** 调用 `rotation()` 读取当前值；它不会修改应用状态。

### `[read-only] sceneGrabPosition : const QPointF`

**作用与语义：**

该属性保留了该点被抓取的场景位置。
如果在`QQuickItem::event()`中处理，场景位置是相对于`QQuickWindow`的位置;如果通过覆盖QGraphicsItem：：touchEvent()处理，则是相对于`QGraphicsScene`坐标的位置;在控件应用中则是窗口位置。

**如何使用：** 调用 `sceneGrabPosition()` 读取当前值；它不会修改应用状态。

### `[read-only] sceneLastPosition : const QPointF`

**作用与语义：**

该属性保留了该点在上一次按键或移动事件中的位置。
如果在`QQuickItem::event()`中处理场景位置，则相对于`QQuickWindow`的位置;如果通过覆盖QGraphicsItem：：touchEvent()，则相对于`QGraphicsScene`坐标的位置;在控件应用中则表示窗口位置。

**如何使用：** 调用 `sceneLastPosition()` 读取当前值；它不会修改应用状态。

### `[read-only] scenePosition : const QPointF`

**作用与语义：**

该属性表示该点的场景位置。
如果在`QQuickItem::event()`中处理场景位置，则相对于`QQuickWindow`的位置;如果通过覆盖QGraphicsItem：：touchEvent()处理，则为`QGraphicsScene`坐标位置;在控件应用中则是窗口位置。

**如何使用：** 调用 `scenePosition()` 读取当前值；它不会修改应用状态。

### `[read-only] scenePressPosition : const QPointF`

**作用与语义：**

该属性表示该点被按下的场景位置。
如果在`QQuickItem::event()`中处理场景位置，则相对于`QQuickWindow`的位置;如果通过覆盖QGraphicsItem：：touchEvent()处理，则相对于`QGraphicsScene`坐标的位置;在小部件应用中则是窗口位置。

**如何使用：** 调用 `scenePressPosition()` 读取当前值；它不会修改应用状态。

### `[read-only] state : const State`

**作用与语义：**

该属性表示事件点的当前状态。

**如何使用：** 调用 `state()` 读取当前值；它不会修改应用状态。

### `[read-only] timeHeld : const qreal`

**作用与语义：**

该属性表示持续时间，单位为秒，因为这个点是按压而非松开的。

**如何使用：** 调用 `timeHeld()` 读取当前值；它不会修改应用状态。

### `[read-only] timestamp : const ulong`

**作用与语义：**

该地产是该地点最近一次被纳入`QPointerEvent`。

**如何使用：** 调用 `timestamp()` 读取当前值；它不会修改应用状态。

### `[read-only] uniqueId : const QPointingDeviceUniqueId`

**作用与语义：**

此属性保存此点或标记的唯一 ID（如果有的话）。
它通常无效（参见 `isValid()`），因为触摸屏无法唯一识别手指。
当它来自 `QTabletEvent` 时，它标识正在使用的手写笔的序列号。
当使用 TUIO 驱动程序并与支持它们的触摸屏配合使用时，它可能标识特定标记（指示物对象）。

**如何使用：** 调用 `uniqueId()` 读取当前值；它不会修改应用状态。

### `[read-only] velocity : const QVector2D`

**作用与语义：**

该属性在坐标上保持一个速度矢量，单位为像素每秒。屏幕或桌面系统。
注意：如果设备功能包含`QInputDevice::Velocity`，表示速度来自操作系统（触摸硬件或驱动程序提供）。但通常`Velocity`能力未被设置，表明速度由Qt计算，使用简单的卡尔曼滤波器提供平滑的平均速度而非瞬时值。它实际上告诉用户在过去几次事件中拖拽该点的速度和方向，最近事件影响最大。

**如何使用：** 调用 `velocity()` 读取当前值；它不会修改应用状态。

### `QEventPoint::QEventPoint(int pointId, QEventPoint::State state, const QPointF &scenePosition, const QPointF &globalPosition)`

**作用与语义：**

构造一个事件点，包含给定的`pointId`、`state`、`scenePosition`和`globalPosition`。

### `[noexcept] QEventPoint::QEventPoint(const QEventPoint &other)`

**作用与语义：**

通过制作`other`的浅复制来构造事件点。

### `[constexpr noexcept] QEventPoint::QEventPoint(QEventPoint &&other)`

**作用与语义：**

通过移动`other`构造事件点。

### `[noexcept] QEventPoint::~QEventPoint()`

**作用与语义：**

会摧毁事件点。

### `QPointF QEventPoint::normalizedPosition() const`

**作用与语义：**

返回该点的归一化位置。
坐标通过将`globalPosition()`变换为`QInputDevice::availableVirtualGeometry()`空间来计算，即`(0, 0)`为左上角，`(1, 1)`为右下角。

### `[noexcept] bool QEventPoint::operator!=(const QEventPoint &other) const`

**作用与语义：**

如果该事件点不等于`other`，返回`true`，否则返回`false`。

### `[noexcept] QEventPoint &QEventPoint::operator=(QEventPoint &&other)`

**作用与语义：**

移动会将`other`分配到该事件点实例。

### `[noexcept] QEventPoint &QEventPoint::operator=(const QEventPoint &other)`

**作用与语义：**

将`other`分配到该事件点，并返回对该事件点的引用。

### `[noexcept] bool QEventPoint::operator==(const QEventPoint &other) const`

**作用与语义：**

如果该事件点等于`other`，返回`true`，否则返回`false`。

### `enum State { Unknown, Stationary, Pressed, Updated, Released }`

**作用与语义：**

指定该事件点的状态。
- `QEventPoint::Unknown`：`Qt::TouchPointUnknownState`;状态不明。
- `QEventPoint::Stationary`：`Qt::TouchPointStationary`;事件点未移动。
- `QEventPoint::Pressed`：`Qt::TouchPointPressed`;按下触摸点或按钮。
- `QEventPoint::Updated`：`Qt::TouchPointMoved`;事件点已更新。
- `QEventPoint::Released`：`Qt::TouchPointReleased`;触点或按钮被松开。
状态类型是QFlag的typedef<State>。它存储状态值的或组合。

### `flags States`

**作用与语义：**

指定该事件点的状态。
- `QEventPoint::Unknown`：`Qt::TouchPointUnknownState`;状态不明。
- `QEventPoint::Stationary`：`Qt::TouchPointStationary`;事件点未移动。
- `QEventPoint::Pressed`：`Qt::TouchPointPressed`;按下触摸点或按钮。
- `QEventPoint::Updated`：`Qt::TouchPointMoved`;事件点已更新。
- `QEventPoint::Released`：`Qt::TouchPointReleased`;触点或按钮被松开。
状态类型是QFlag的typedef<State>。它存储状态值的或组合。

### `const QPointingDevice * device() const`

**作用与语义：**

此属性保存生成此事件点的指点设备。

**如何使用：** 调用 `device()` 读取当前值；它不会修改应用状态。

### `QSizeF ellipseDiameters() const`

**作用与语义：**

该属性包含触摸点边界椭圆的宽度和高度。
返回值以逻辑像素为单位。大多数触摸屏无法检测接触点的形状，鼠标或平板电脑设备也无法检测，因此空尺寸是最常见的数值。在某些触摸屏上，直径可能非零且始终相等（椭圆近似为圆形）。

**如何使用：** 调用 `ellipseDiameters()` 读取当前值；它不会修改应用状态。

### `QPointF globalGrabPosition() const`

**作用与语义：**

该属性表示该点被抓取的全局位置。
全局位置相对于屏幕或虚拟桌面表示。

**如何使用：** 调用 `globalGrabPosition()` 读取当前值；它不会修改应用状态。

### `QPointF globalLastPosition() const`

**作用与语义：**

该属性表示该点在上一次按键或移动事件中的全局位置。
全局位置相对于屏幕或虚拟桌面表示。

**如何使用：** 调用 `globalLastPosition()` 读取当前值；它不会修改应用状态。

### `QPointF globalPosition() const`

**作用与语义：**

该属性表示该点的全局位置。
全局位置相对于屏幕或虚拟桌面表示。

**如何使用：** 调用 `globalPosition()` 读取当前值；它不会修改应用状态。

### `QPointF globalPressPosition() const`

**作用与语义：**

该属性表示该点被按下的全局位置。
全局位置相对于屏幕或虚拟桌面表示。

**如何使用：** 调用 `globalPressPosition()` 读取当前值；它不会修改应用状态。

### `QPointF grabPosition() const`

**作用与语义：**

此属性保存抓取此点时的位置。
位置相对于接收事件的部件或项。

**如何使用：** 调用 `grabPosition()` 读取当前值；它不会修改应用状态。

### `int id() const`

**作用与语义：**

该属性包含该事件点的ID编号。
注意：不要假设ID编号从零开始或它们是连续的。由于底层驱动的工作方式，这种假设往往是错误的。

**如何使用：** 调用 `id()` 读取当前值；它不会修改应用状态。

### `bool isAccepted() const`

**作用与语义：**

该属性表示事件点的公认状态。
在基于控件的应用中，这一属性不被使用，因为只有小部件接受或拒绝完整`QInputEvent`才有意义。
然而，在 Qt Quick 中，通常项目或事件处理程序只接受实际参与手势的`QTouchEvent`中单个点，而其他点则可以传递给其他项目或处理者。为了保持一致，这适用于任何`QPointerEvent`;只有当`QPointerEvent`中的所有点都被接受后，才会进行交付。

**如何使用：** 调用 `isAccepted()` 读取当前值；它不会修改应用状态。

### `QPointF lastPosition() const`

**作用与语义：**

该属性表示该点在上一次按键或移动事件中的位置。
位置相对于接收事件的小部件或项目。

**如何使用：** 调用 `lastPosition()` 读取当前值；它不会修改应用状态。

### `ulong lastTimestamp() const`

**作用与语义：**

该属性包含包含该点的前一根`QPointerEvent`的时间。

**如何使用：** 调用 `lastTimestamp()` 读取当前值；它不会修改应用状态。

### `QPointF position() const`

**作用与语义：**

该属性表示该点的位置。
位置相对于接收事件的小部件或项目。

**如何使用：** 调用 `position()` 读取当前值；它不会修改应用状态。

### `QPointF pressPosition() const`

**作用与语义：**

此属性保存按下此点时的位置。
位置相对于接收事件的部件或项。

**如何使用：** 调用 `pressPosition()` 读取当前值；它不会修改应用状态。

### `ulong pressTimestamp() const`

**作用与语义：**

该属性记录了该点被压制的最近时间。

**如何使用：** 调用 `pressTimestamp()` 读取当前值；它不会修改应用状态。

### `qreal pressure() const`

**作用与语义：**

该属性承受了该点的压力。
回报值范围在`0.0`到`1.0`之间。

**如何使用：** 调用 `pressure()` 读取当前值；它不会修改应用状态。

### `qreal rotation() const`

**作用与语义：**

该属性表示该点的角度方向。
返回值以度为单位，0（默认）表示手指、标记或触控笔朝上，负角度表示向左旋转，正角度表示向右旋转。大多数触摸屏不检测旋转，因此0是最常见的数值。

**如何使用：** 调用 `rotation()` 读取当前值；它不会修改应用状态。

### `QPointF sceneGrabPosition() const`

**作用与语义：**

该属性保留了该点被抓取的场景位置。
如果在`QQuickItem::event()`中处理，场景位置是相对于`QQuickWindow`的位置;如果通过覆盖QGraphicsItem：：touchEvent()处理，则是相对于`QGraphicsScene`坐标的位置;在控件应用中则是窗口位置。

**如何使用：** 调用 `sceneGrabPosition()` 读取当前值；它不会修改应用状态。

### `QPointF sceneLastPosition() const`

**作用与语义：**

该属性保留了该点在上一次按键或移动事件中的位置。
如果在`QQuickItem::event()`中处理场景位置，则相对于`QQuickWindow`的位置;如果通过覆盖QGraphicsItem：：touchEvent()，则相对于`QGraphicsScene`坐标的位置;在控件应用中则表示窗口位置。

**如何使用：** 调用 `sceneLastPosition()` 读取当前值；它不会修改应用状态。

### `QPointF scenePosition() const`

**作用与语义：**

该属性表示该点的场景位置。
如果在`QQuickItem::event()`中处理场景位置，则相对于`QQuickWindow`的位置;如果通过覆盖QGraphicsItem：：touchEvent()处理，则为`QGraphicsScene`坐标位置;在控件应用中则是窗口位置。

**如何使用：** 调用 `scenePosition()` 读取当前值；它不会修改应用状态。

### `QPointF scenePressPosition() const`

**作用与语义：**

该属性表示该点被按下的场景位置。
如果在`QQuickItem::event()`中处理场景位置，则相对于`QQuickWindow`的位置;如果通过覆盖QGraphicsItem：：touchEvent()处理，则相对于`QGraphicsScene`坐标的位置;在小部件应用中则是窗口位置。

**如何使用：** 调用 `scenePressPosition()` 读取当前值；它不会修改应用状态。

### `void setAccepted(bool accepted = true)`

**作用与语义：**

该属性表示事件点的公认状态。
在基于控件的应用中，这一属性不被使用，因为只有小部件接受或拒绝完整`QInputEvent`才有意义。
然而，在 Qt Quick 中，通常项目或事件处理程序只接受实际参与手势的`QTouchEvent`中单个点，而其他点则可以传递给其他项目或处理者。为了保持一致，这适用于任何`QPointerEvent`;只有当`QPointerEvent`中的所有点都被接受后，才会进行交付。

**如何使用：** 调用 `setAccepted(...)` 修改 `accepted`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QEventPoint::State state() const`

**作用与语义：**

该属性表示事件点的当前状态。

**如何使用：** 调用 `state()` 读取当前值；它不会修改应用状态。

### `qreal timeHeld() const`

**作用与语义：**

该属性表示持续时间，单位为秒，因为这个点是按压而非松开的。

**如何使用：** 调用 `timeHeld()` 读取当前值；它不会修改应用状态。

### `ulong timestamp() const`

**作用与语义：**

该地产是该地点最近一次被纳入`QPointerEvent`。

**如何使用：** 调用 `timestamp()` 读取当前值；它不会修改应用状态。

### `QPointingDeviceUniqueId uniqueId() const`

**作用与语义：**

此属性保存此点或标记的唯一 ID（如果有的话）。
它通常无效（参见 `isValid()`），因为触摸屏无法唯一识别手指。
当它来自 `QTabletEvent` 时，它标识正在使用的手写笔的序列号。
当使用 TUIO 驱动程序并与支持它们的触摸屏配合使用时，它可能标识特定标记（指示物对象）。

**如何使用：** 调用 `uniqueId()` 读取当前值；它不会修改应用状态。

### `QVector2D velocity() const`

**作用与语义：**

该属性在坐标上保持一个速度矢量，单位为像素每秒。屏幕或桌面系统。
注意：如果设备功能包含`QInputDevice::Velocity`，表示速度来自操作系统（触摸硬件或驱动程序提供）。但通常`Velocity`能力未被设置，表明速度由Qt计算，使用简单的卡尔曼滤波器提供平滑的平均速度而非瞬时值。它实际上告诉用户在过去几次事件中拖拽该点的速度和方向，最近事件影响最大。

**如何使用：** 调用 `velocity()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QEventPoint` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
