# QTabletEvent

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QTabletEvent` 是 Qt 的值类型，围绕“Tablet事件”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTabletEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QTabletEvent>`
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

- `QTabletEvent(QEvent::Type type, const QPointingDevice *dev, const QPointF &pos, const QPointF &globalPos, qreal pressure, float xTilt, float yTilt, float tangentialPressure, qreal rotation, float z, Qt::KeyboardModifiers keyState, Qt::MouseButton button, Qt::MouseButtons buttons)`
- `qreal pressure() const`
- `qreal rotation() const`
- `qreal tangentialPressure() const`
- `qreal xTilt() const`
- `qreal yTilt() const`
- `qreal z() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QTabletEvent::QTabletEvent(QEvent::Type type, const QPointingDevice *dev, const QPointF &pos, const QPointF &globalPos, qreal pressure, float xTilt, float yTilt, float tangentialPressure, qreal rotation, float z, Qt::KeyboardModifiers keyState, Qt::MouseButton button, Qt::MouseButtons buttons)`

**作用与语义：**

构造给定`type`的平板事件。
`pos`参数表示事件在控件中发生的位置;`globalPos` 是绝对坐标中的对应位置。
`pressure`会施加在装置上的压力`dev`。
`xTilt`和`yTilt`分别表示器件从x轴和y轴的倾斜度。
`keyState` 指定按下哪些键盘修饰键（例如 Ctrl）。
`z`参数给出了设备在绘图板上的Z坐标;这通常由4D鼠标上的轮子给出。如果设备不支持Z轴（即`QPointingDevice::capabilities()`不包含`ZPosition`），请在这里`0`。
`tangentialPressure`参数给出气刷切向压力拇指轮值。如果设备不支持切向压力（即`QPointingDevice::capabilities()`不包含`TangentialPressure`），则在此传递`0`。
`rotation`显示设备的旋转度数。4D鼠标、Wacom艺术笔和Apple Pencil支持旋转。如果设备不支持旋转（即`QPointingDevice::capabilities()`不包含`Rotation`），请在这里传递`0`。
引发事件的`button`以`Qt::MouseButton`枚举中的值给出。如果事件`type`不是`TabletPress`或`TabletRelease`，则该事件的相应按钮是`Qt::NoButton`。
`buttons` 是事件发生时所有按钮的状态。

### `qreal QTabletEvent::pressure() const`

**作用与语义：**

返回设备的压力。0.0表示触控笔不在绘板上，1.0表示触控笔的最大压力。

### `qreal QTabletEvent::rotation() const`

**作用与语义：**

返回当前工具的旋转度数，0表示触控笔尖端朝向绘图板顶部，正值表示向右转，负值表示向左转。这可以通过4D鼠标或支持旋转的手写笔（如Wacom艺术笔或Apple Pencil）给出。如果设备不支持旋转，这个值始终为0.0。

### `qreal QTabletEvent::tangentialPressure() const`

**作用与语义：**

返回器件的切向压力。这通常由喷笔工具上的指轮给出。范围为-1.0到1.0。0.0表示中性位置。当前喷笔只能从中性位置正方向移动。如果设备不支持切向压力，该值始终为0.0。
注意：该值以单精度浮点数形式存储。

### `qreal QTabletEvent::xTilt() const`

**作用与语义：**

返回设备（例如笔）与垂直X轴方向之间的角度。正值位于平板物理右侧。角度范围为-60到60度。
注意：该值以单精度浮点数形式存储。

### `qreal QTabletEvent::yTilt() const`

**作用与语义：**

返回设备（例如笔）与垂直方向Y轴之间的角度。正值位于平板底部。角度在-60至60度范围内。
注意：该值以单精度浮点数形式存储。

### `qreal QTabletEvent::z() const`

**作用与语义：**

返回设备的z轴位置。通常这用4D鼠标上的轮子表示。如果设备不支持Z轴，这个值总是零。这和压力不同。
注意：该值以单精度浮点数形式存储。

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

`QTabletEvent` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
