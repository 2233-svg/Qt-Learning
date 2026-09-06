# QPointerEvent

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QPointerEvent` 是 Qt 的值类型，围绕“Pointer事件”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPointerEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QPointerEvent>`
- 继承自：QInputEvent
- 直接派生类：QSinglePointEvent、QTouchEvent

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。 使用时通常按这个过程组织：Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `bool addPassiveGrabber(const QEventPoint &point, QObject *grabber)`
- `bool allPointsAccepted() const`
- `bool allPointsGrabbed() const`
- `void clearPassiveGrabbers(const QEventPoint &point)`
- `QObject * exclusiveGrabber(const QEventPoint &point) const`
- `QList<QPointer<QObject>> passiveGrabbers(const QEventPoint &point) const`
- `QEventPoint & point(qsizetype i)`
- `QEventPoint * pointById(int id)`
- `qsizetype pointCount() const`
- `QPointingDevice::PointerType pointerType() const`
- `const QPointingDevice * pointingDevice() const`
- `const QList<QEventPoint> & points() const`
- `bool removePassiveGrabber(const QEventPoint &point, QObject *grabber)`
- `void setExclusiveGrabber(const QEventPoint &point, QObject *exclusiveGrabber)`

### 重实现的公有函数

- `virtual void setAccepted(bool accepted) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `bool QPointerEvent::addPassiveGrabber(const QEventPoint &point, QObject *grabber)`

**作用与语义：**

通知交付逻辑，给定`grabber`将接收所有未来的更新事件以及包含该`point`的发布事件，无论这些事件可能在其他地方传递。
它只供 Qt 快速输入处理器使用。
如果`grabber`已经添加，退货`false`，否则`true`。

### `bool QPointerEvent::allPointsAccepted() const`

**作用与语义：**

如果isPointAccepted()对`points()`中的每个点都`true`，则返回`true`;否则`false`。

### `bool QPointerEvent::allPointsGrabbed() const`

**作用与语义：**

如果`points()`中的每个点都有一个`exclusiveGrabber()`或一个或多个`passiveGrabbers()`，则返回`true`。

### `void QPointerEvent::clearPassiveGrabbers(const QEventPoint &point)`

**作用与语义：**

移除给定`point`中所有被动抓取者。
它只供 Qt 快速输入处理器使用。

### `QObject *QPointerEvent::exclusiveGrabber(const QEventPoint &point) const`

**作用与语义：**

返回已设置为接收所有未来更新事件和包含该`point`的发布事件的对象。
目前主要用于Qt Quick。

### `QList<QPointer<QObject>> QPointerEvent::passiveGrabbers(const QEventPoint &point) const`

**作用与语义：**

返回被请求接收所有未来更新事件的对象列表，以及包含该更新`point`的发布事件。
它只供 Qt 快速输入处理器使用。

### `QEventPoint &QPointerEvent::point(qsizetype i)`

**作用与语义：**

返回索引`i`点的`QEventPoint`引用。

### `QEventPoint *QPointerEvent::pointById(int id)`

**作用与语义：**

返回`id`与给定`id`匹配的点，若未找到该点则返回`nullptr`。

### `qsizetype QPointerEvent::pointCount() const`

**作用与语义：**

返回该指针事件中的得分。

### `QPointingDevice::PointerType QPointerEvent::pointerType() const`

**作用与语义：**

返回产生事件的点类型。

### `const QPointingDevice *QPointerEvent::pointingDevice() const`

**作用与语义：**

返回该事件起源的源设备。
这和`QInputEvent::device()`一样，但为了方便被定型了。

### `const QList<QEventPoint> &QPointerEvent::points() const`

**作用与语义：**

返回该指针事件中的点列表。

### `bool QPointerEvent::removePassiveGrabber(const QEventPoint &point, QObject *grabber)`

**作用与语义：**

如果被动`grabber`之前被添加，则从给定`point`中移除。如果之前是被动抓取者，则返回`true`;如果不是，`false`返回。
它只供 Qt 快速输入处理器使用。

### `void QPointerEvent::setExclusiveGrabber(const QEventPoint &point, QObject *exclusiveGrabber)`

**作用与语义：**

通知交付逻辑，给定`exclusiveGrabber`将接收所有未来的更新事件和包含该`point`的发布事件，且可以跳过对其他项目的交付。
目前主要用于Qt Quick。

### `virtual void setAccepted(bool accepted) override`

**作用与语义：**

设置整个指针事件的接受状态。传入 `true` 表示接收者已经处理该事件，并会隐式接受事件携带的所有触点；传入 `false` 允许未处理事件继续传播。若只想接受某个触点，应设置对应 `QEventPoint` 的接受状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPointerEvent` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
