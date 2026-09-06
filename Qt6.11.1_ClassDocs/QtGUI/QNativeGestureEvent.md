# QNativeGestureEvent

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QNativeGestureEvent` 是 Qt 的值类型，围绕“NativeGesture事件”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QNativeGestureEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QNativeGestureEvent>`
- 继承自：QSinglePointEvent
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

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。 使用时通常按这个过程组织：Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `(since 6.2) QNativeGestureEvent(Qt::NativeGestureType type, const QPointingDevice *device, int fingerCount, const QPointF &localPos, const QPointF &scenePos, const QPointF &globalPos, qreal value, const QPointF &delta, quint64 sequenceId = UINT64_MAX)`
- `(since 6.2) QPointF delta() const`
- `(since 6.2) int fingerCount() const`
- `Qt::NativeGestureType gestureType() const`
- `qreal value() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.2] QNativeGestureEvent::QNativeGestureEvent(Qt::NativeGestureType type, const QPointingDevice *device, int fingerCount, const QPointF &localPos, const QPointF &scenePos, const QPointF &globalPos, qreal value, const QPointF &delta, quint64 sequenceId = UINT64_MAX)`

**作用与语义：**

构建一个类型`type`的本土手势事件，源自`device`描述`scenePos`涉及`fingerCount`手指的手势。
`localPos`、`scenePos`和`globalPos`分别指定了手势相对于接收小部件或物品、窗口和屏幕或桌面的位置。
`value`有手势相关的解释：对于RotateNativeGesture或SwipeNativeGesture，它是度数的角度。对于ZoomNativeGesture，`value`是一个增量缩放因子，通常远小于1，表明目标物品的比例应调整如下：item.scale = item.scale * （1 event.value）。
对于PanNativeGesture，`delta`表示视口、控件或物品需要移动或平移的像素距离。
注意：`delta`以单精度（`QVector2D`）存储，因此在某些情况下`delta()`返回的值可能略有不同。这可能会在Qt的未来版本中有所更改。

### `[since 6.2] QPointF QNativeGestureEvent::delta() const`

**作用与语义：**

返回自上一事件以来移动的距离，单位为像素。平移手势表示目标控件、物品或视口内容应移动的像素距离。

### `[since 6.2] int QNativeGestureEvent::fingerCount() const`

**作用与语义：**

如果已知，返回参与该手势的手指数量。当`gestureType()`为`Qt::BeginNativeGesture`或`Qt::EndNativeGesture`时，通常信息未知，fingerCount() 返回`0`。

### `Qt::NativeGestureType QNativeGestureEvent::gestureType() const`

**作用与语义：**

返回手势类型。

### `qreal QNativeGestureEvent::value() const`

**作用与语义：**

返回手势值。该值应根据手势类型进行解释。例如，Zoom 手势提供比例因子的差值，而旋转手势提供旋转的差值。

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

`QNativeGestureEvent` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
