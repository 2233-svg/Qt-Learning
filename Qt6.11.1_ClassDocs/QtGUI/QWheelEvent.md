# QWheelEvent

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QWheelEvent` 是 Qt 的值类型，围绕“Wheel事件”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QWheelEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QWheelEvent>`
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

### 属性

- `angleDelta : QPoint`
- `device : const QPointingDevice*`
- `inverted : bool`
- `phase : Qt::ScrollPhase`
- `pixelDelta : QPoint`

### 公有函数

- `QWheelEvent(const QPointF &pos, const QPointF &globalPos, QPoint pixelDelta, QPoint angleDelta, Qt::MouseButtons buttons, Qt::KeyboardModifiers modifiers, Qt::ScrollPhase phase, bool inverted, Qt::MouseEventSource source = Qt::MouseEventNotSynthesized, const QPointingDevice *device = QPointingDevice::primaryPointingDevice())`
- `QPoint angleDelta() const`
- `bool inverted() const`
- `Qt::ScrollPhase phase() const`
- `QPoint pixelDelta() const`

### 重实现的公有函数

- `virtual bool isBeginEvent() const override`
- `virtual bool isEndEvent() const override`
- `virtual bool isUpdateEvent() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only] angleDelta : QPoint`

**作用与语义：**

该属性表示车轮旋转的相对长度，单位为八分之一度。
正值表示滚轮被向前旋转，远离用户;负值表示转轮被向后旋转，朝向用户方向。`angleDelta().y()`表示自上次事件以来，常见垂直鼠标滚轮旋转的角度。`angleDelta().x()`表示如果鼠标有水平滚轮，水平滚轮被旋转的角度;否则保持零。
大多数鼠标类型以15度为单位工作，此时δ值为120的整数倍;即120单位 × 1/8 = 15度。
注意：在支持滚动`phases`的平台上，滚动即将开始（`Qt::ScrollBegin`）或结束（`Qt::ScrollEnd`）时，delta可能会为空。

**如何使用：** 调用 `angleDelta()` 读取当前值；它不会修改应用状态。

### `[read-only] device : const QPointingDevice*`

**作用与语义：**

此属性保存发生滚轮事件的设备。

**如何使用：** 调用 `device()` 读取当前值；它不会修改应用状态。

### `[read-only] inverted : bool`

**作用与语义：**

该属性在事件传递的 delta 值是否被反转时成立。
通常，如果垂直轮子顶部朝向操作手的方向旋转，则会产生正的 delta 值`QWheelEvent`。同样，水平方向的轮子移动时，如果轮子顶部向左移动，则会产生正 delta 值的`QWheelEvent`。
然而，在某些平台上，这种操作是可配置的，使得上述操作会产生负的 delta 值（但大小相同）。利用反转特性，轮子事件消费者可以选择始终遵循轮子方向，无论系统设置如何，但仅限于特定控件。
注意：许多平台不提供此类信息。在这些平台上`inverted`总是错误的。

**如何使用：** 调用 `inverted()` 读取当前值；它不会修改应用状态。

### `[read-only] phase : Qt::ScrollPhase`

**作用与语义：**

该属性表示该轮事件的滚动相位。
注意：目前仅支持macOS上的`Qt::ScrollBegin`和`Qt::ScrollEnd`阶段。

**如何使用：** 调用 `phase()` 读取当前值；它不会修改应用状态。

### `[read-only] pixelDelta : QPoint`

**作用与语义：**

该属性表示屏幕上的滚动距离（像素单位）。
该值适用于支持高分辨率像素差异值的平台，如macOS。该值应直接用于屏幕上内容滚动。
注意：在支持滚动`phases`的平台上，滚动即将开始（`Qt::ScrollBegin`）或结束（`Qt::ScrollEnd`）时，delta可能会为零。
注意：在X11上，这个值是驱动程序特定的且不可靠，建议使用`angleDelta()`。

**如何使用：** 调用 `pixelDelta()` 读取当前值；它不会修改应用状态。

### `QWheelEvent::QWheelEvent(const QPointF &pos, const QPointF &globalPos, QPoint pixelDelta, QPoint angleDelta, Qt::MouseButtons buttons, Qt::KeyboardModifiers modifiers, Qt::ScrollPhase phase, bool inverted, Qt::MouseEventSource source = Qt::MouseEventNotSynthesized, const QPointingDevice *device = QPointingDevice::primaryPointingDevice())`

**作用与语义：**

构造一个轮事件对象。
`pos`显示鼠标光标在窗口内的位置。全局坐标中的位置由`globalPos`指定。
`pixelDelta` 表示屏幕上的滚动距离（像素单位），而 `angleDelta` 表示轮子旋转角度。`pixelDelta`为可选，且可为空。
事件发生时的鼠标和键盘状态由`buttons`和`modifiers`指定。
事件的滚动阶段由`phase`指定，`source`表示这是真实事件还是人工（合成）事件。
如果系统配置为反转事件中提供的 delta 值（例如在 macOS 上触摸板的自然滚动），`inverted`应被`true`。否则，`inverted` 是`false`。
轮事件起源的装置由`device`规定。

### `QPoint QWheelEvent::angleDelta() const`

**作用与语义：**

返回滚轮被旋转的相对长度，单位为八分之一度。正值表示滚轮被向前旋转，远离用户;负值表示滚轮向后向后向用户旋转。`angleDelta().y()`表示自上次事件以来，常见垂直鼠标滚轮旋转的角度。`angleDelta().x()`表示水平滚轮旋转的角度（如果鼠标有水平滚轮）;否则保持零。部分鼠标允许用户倾斜滚轮进行水平滚动，部分触摸板支持水平滚动手势;该操作也会在`angleDelta().x()`中出现。
大多数鼠标类型以15度为单位工作，此时δ值为120的整数倍;即120单位 × 1/8 = 15度。
不过，有些鼠标的轮子分辨率更细，发送的 delta 值小于 120 单位（小于 15 度）。为了支持这种可能性，你可以从事件中累计加到 120 的 delta 值，然后滚动控件，或者根据每个控件事件部分滚动控件。但为了更原生的感觉，你应该优先选择在有 Delta 的平台上`pixelDelta()`。
注意：在支持滚动`phases`的平台上，当以下情况时，delta可能为无效：
- 滚动即将开始，但距离尚未改变（`Qt::ScrollBegin`），
- 或滚动结束，距离不再变化（`Qt::ScrollEnd`）。
注意：属性angleDelta的获取函数。

**官方示例：**

```cpp
 void MyWidget::wheelEvent(QWheelEvent *event)
 {
     QPoint numPixels = event->pixelDelta();
     QPoint numDegrees = event->angleDelta() / 8;

     if (!numPixels.isNull()) {
         scrollWithPixels(numPixels);
     } else if (!numDegrees.isNull()) {
         QPoint numSteps = numDegrees / 15;
         scrollWithDegrees(numSteps);
     }

     event->accept();
 }
```

### `bool QWheelEvent::inverted() const`

**作用与语义：**

返回事件中传递的delta值是否被反转。
通常，如果垂直轮子顶部朝向操作手的方向旋转，垂直轮子会产生正的δ值`QWheelEvent`。同样，水平方向的轮子移动时，如果轮子顶部向左移动，则会产生正δ值的`QWheelEvent`。
然而，在某些平台上，这种操作是可配置的，使得上述操作会产生负的 delta 值（但幅度相同）。利用反转特性，转盘事件消费者可以选择始终跟随转盘方向，无论系统设置如何，但仅限于特定控件。（其中一种用例是用户将转轮旋转方向与视觉 Tumbler 旋转方向相同。另一种用例是让滑块手柄随触控板手指的移动方向移动，无论系统配置如何。）。
注意：许多平台不提供此类信息。在这些平台上，反转总是返回错误信息。
注意：属性的获取函数反转。

### `[override virtual] bool QWheelEvent::isBeginEvent() const`

**作用与语义：**

重装：`QSinglePointEvent::isBeginEvent()` const.
如果该事件的`phase()` `Qt::ScrollBegin`，还`true`。
如果该事件代表被按下的`button`，返回`true`。

### `[override virtual] bool QWheelEvent::isEndEvent() const`

**作用与语义：**

重实现自：`QSinglePointEvent::isEndEvent()` const.
如果该事件的`phase()`是`Qt::ScrollEnd`，则`true`返回。
如果该事件代表`button`的释放，返回`true`。

### `[override virtual] bool QWheelEvent::isUpdateEvent() const`

**作用与语义：**

重实现自：`QSinglePointEvent::isUpdateEvent()` const.
如果该事件的`phase()`是`Qt::ScrollUpdate`还是`Qt::ScrollMomentum`，返回`true`。
如果该事件不包含按钮状态的变化，返回`true`。

### `Qt::ScrollPhase QWheelEvent::phase() const`

**作用与语义：**

返回该轮事件的滚动阶段。
注意：`Qt::ScrollBegin`和`Qt::ScrollEnd`阶段目前仅支持macOS。
注意：属性阶段使用获取函数。

### `QPoint QWheelEvent::pixelDelta() const`

**作用与语义：**

返回屏幕上的滚动距离（像素单位）。该值在支持高分辨率基于像素的增量值的平台上提供，如macOS。该值应直接用于屏幕上内容滚动。
注意：在支持滚动`phases`的平台上，当以下情况时，delta可能为无效：
- 滚动即将开始，但距离尚未改变（`Qt::ScrollBegin`），
- 或滚动结束且距离不再变化（`Qt::ScrollEnd`）。
注意：在X11上，这个值是驱动程序特定的且不可靠，建议用`angleDelta()`。
注意：属性 pixelDelta 的获取函数。

**官方示例：**

```cpp
 void MyWidget::wheelEvent(QWheelEvent *event)
 {
     QPoint numPixels = event->pixelDelta();
     QPoint numDegrees = event->angleDelta() / 8;

     if (!numPixels.isNull()) {
         scrollWithPixels(numPixels);
     } else if (!numDegrees.isNull()) {
         QPoint numSteps = numDegrees / 15;
         scrollWithDegrees(numSteps);
     }

     event->accept();
 }
```

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

`QWheelEvent` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
