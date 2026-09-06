# QSinglePointEvent

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QSinglePointEvent` 是 Qt 的值类型，围绕“Single点事件”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QSinglePointEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QSinglePointEvent>`
- 继承自：QPointerEvent
- 直接派生类：QEnterEvent、QHoverEvent、QMouseEvent、QNativeGestureEvent、QTabletEvent,、QWheelEvent

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

- `exclusivePointGrabber : QObject*`

### 公有函数

- `Qt::MouseButton button() const`
- `Qt::MouseButtons buttons() const`
- `QObject * exclusivePointGrabber() const`
- `QPointF globalPosition() const`
- `QPointF position() const`
- `QPointF scenePosition() const`
- `void setExclusivePointGrabber(QObject *exclusiveGrabber)`

### 重实现的公有函数

- `virtual bool isBeginEvent() const override`
- `virtual bool isEndEvent() const override`
- `virtual bool isUpdateEvent() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `exclusivePointGrabber : QObject*`

**作用与语义：**

该属性包含将接受未来更新的对象。
独占抓取器是一个选择接收所有未来更新事件和包含该事件相同点的发布事件的对象。
设置 exclusivePointGrabber 属性是一种方便，等同于：

**如何使用：** 调用 `exclusivePointGrabber()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 setExclusiveGrabber(points().first(), exclusiveGrabber);
```

### `Qt::MouseButton QSinglePointEvent::button() const`

**作用与语义：**

返回导致事件的按钮。
返回的值总是`Qt::NoButton`鼠标移动事件，以及`TabletMove`、`TabletEnterProximity`和`TabletLeaveProximity`事件。

### `Qt::MouseButtons QSinglePointEvent::buttons() const`

**作用与语义：**

返回事件生成时的按钮状态。
按钮状态结合了`Qt::LeftButton`、`Qt::RightButton`和`Qt::MiddleButton`，使用了OR操作符。
鼠标移动或`TabletMove`事件，都是按住的按钮。
对于鼠标按压、双击或`TabletPress`事件，这包括导致事件的按钮。
对于鼠标释放或`TabletRelease`事件，这会排除导致事件的按钮。

### `QPointF QSinglePointEvent::globalPosition() const`

**作用与语义：**

返回该事件中点在屏幕或虚拟桌面上的位置。
注意：鼠标指针的全局位置会在事件发生时被记录。这在像X11这样的异步窗口系统中非常重要;每当你根据鼠标事件移动小部件时，globalPosition() 可能与当前光标位置差异很大，`QCursor::pos()` 返回。

### `[override virtual] bool QSinglePointEvent::isBeginEvent() const`

**作用与语义：**

如果该事件代表被按下的`button`，返回`true`。

### `[override virtual] bool QSinglePointEvent::isEndEvent() const`

**作用与语义：**

如果该事件代表`button`释放，返回`true`。

### `[override virtual] bool QSinglePointEvent::isUpdateEvent() const`

**作用与语义：**

如果该事件不包含按钮状态的变化，返回`true`。

### `QPointF QSinglePointEvent::position() const`

**作用与语义：**

返回该事件中点相对于接收事件的控件或项目的位置。
如果你会根据鼠标事件移动小部件，建议用`globalPosition()`。

### `QPointF QSinglePointEvent::scenePosition() const`

**作用与语义：**

返回该事件中点相对于窗口或场景的位置。

### `QObject * exclusivePointGrabber() const`

**作用与语义：**

该属性包含将接受未来更新的对象。
独占抓取器是一个选择接收所有未来更新事件和包含该事件相同点的发布事件的对象。
设置 exclusivePointGrabber 属性是一种方便，等同于：

**如何使用：** 调用 `exclusivePointGrabber()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 setExclusiveGrabber(points().first(), exclusiveGrabber);
```

### `void setExclusivePointGrabber(QObject *exclusiveGrabber)`

**作用与语义：**

该属性包含将接受未来更新的对象。
独占抓取器是一个选择接收所有未来更新事件和包含该事件相同点的发布事件的对象。
设置 exclusivePointGrabber 属性是一种方便，等同于：

**如何使用：** 调用 `setExclusivePointGrabber(...)` 修改 `exclusivePointGrabber`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 setExclusiveGrabber(points().first(), exclusiveGrabber);
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

`QSinglePointEvent` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
