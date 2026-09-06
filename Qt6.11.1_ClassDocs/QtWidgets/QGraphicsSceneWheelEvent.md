# QGraphicsSceneWheelEvent

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsSceneWheelEvent` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsSceneWheelEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsSceneWheelEvent>`
- 继承自：QGraphicsSceneEvent
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

**生命周期：** 场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

**状态与结果：** 区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

**线程与事件循环：** 图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

## 3. 直接使用

重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。 使用时通常按这个过程组织：Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `virtual ~QGraphicsSceneWheelEvent()`
- `Qt::MouseButtons buttons() const`
- `int delta() const`
- `(since 6.2) bool isInverted() const`
- `Qt::KeyboardModifiers modifiers() const`
- `Qt::Orientation orientation() const`
- `(since 6.2) Qt::ScrollPhase phase() const`
- `(since 6.2) QPoint pixelDelta() const`
- `QPointF pos() const`
- `QPointF scenePos() const`
- `QPoint screenPos() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[virtual noexcept] QGraphicsSceneWheelEvent::~QGraphicsSceneWheelEvent()`

**作用与语义：**

摧毁了`QGraphicsSceneWheelEvent`。

### `Qt::MouseButtons QGraphicsSceneWheelEvent::buttons() const`

**作用与语义：**

返回滚轮事件发生时按下的鼠标按钮。

### `int QGraphicsSceneWheelEvent::delta() const`

**作用与语义：**

返回轮子旋转的距离，单位为八分之一（1/8秒）度。正值表示轮子被向前旋转，远离用户;负值表示轮子被向后旋转，朝向用户方向。
大多数鼠标类型以15度为单位工作，此时Δ值为120的整数倍（== 15 * 8）。

### `[since 6.2] bool QGraphicsSceneWheelEvent::isInverted() const`

**作用与语义：**

返回事件中传递的delta值是否被反转。

### `Qt::KeyboardModifiers QGraphicsSceneWheelEvent::modifiers() const`

**作用与语义：**

返回轮子事件发生时激活的键盘修改键。

### `Qt::Orientation QGraphicsSceneWheelEvent::orientation() const`

**作用与语义：**

返回方向盘方向。

### `[since 6.2] Qt::ScrollPhase QGraphicsSceneWheelEvent::phase() const`

**作用与语义：**

返回该轮事件的滚动阶段。

### `[since 6.2] QPoint QGraphicsSceneWheelEvent::pixelDelta() const`

**作用与语义：**

返回屏幕上的滚动距离（像素单位）。该值在支持高分辨率基于像素的增量值的平台上提供，如macOS。该值应直接用于屏幕上内容滚动。

### `QPointF QGraphicsSceneWheelEvent::pos() const`

**作用与语义：**

返回轮事件发生时光标在物品坐标中的位置。

### `QPointF QGraphicsSceneWheelEvent::scenePos() const`

**作用与语义：**

返回轮事件发生时光标在场景坐标中的位置。

### `QPoint QGraphicsSceneWheelEvent::screenPos() const`

**作用与语义：**

返回轮子事件发生时光标在屏幕坐标中的位置。

## 6. 深入实践与常见坑

### 生命周期和资源边界

场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

### 状态和错误边界

区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

### 线程边界

图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

### 最容易出现的错误

不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGraphicsSceneWheelEvent` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
