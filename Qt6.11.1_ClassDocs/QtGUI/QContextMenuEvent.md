# QContextMenuEvent

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QContextMenuEvent` 是 Qt 的值类型，围绕“Context菜单事件”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QContextMenuEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QContextMenuEvent>`
- 继承自：QInputEvent
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

### 公有类型

- `enum Reason { Mouse, Keyboard, Other }`

### 公有函数

- `QContextMenuEvent(QContextMenuEvent::Reason reason, const QPoint &pos, const QPoint &globalPos, Qt::KeyboardModifiers modifiers = Qt::NoModifier)`
- `const QPoint & globalPos() const`
- `int globalX() const`
- `int globalY() const`
- `const QPoint & pos() const`
- `QContextMenuEvent::Reason reason() const`
- `int x() const`
- `int y() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QContextMenuEvent::Reason`

**作用与语义：**

这个枚举描述了事件被发送的原因。
- `QContextMenuEvent::Mouse`：`0`;鼠标触发了事件发送。通常这意味着点击了右键，但这取决于平台。
- `QContextMenuEvent::Keyboard`：`1`;键盘触发了该事件。在Windows上，这意味着菜单按钮被按下。
- `QContextMenuEvent::Other`：`2`;事件通过其他方式发送（即非鼠标或键盘）。

### `QContextMenuEvent::QContextMenuEvent(QContextMenuEvent::Reason reason, const QPoint &pos, const QPoint &globalPos, Qt::KeyboardModifiers modifiers = Qt::NoModifier)`

**作用与语义：**

构建一个将accept参数标志设置为false的上下文菜单事件对象。
`reason`参数必须是`QContextMenuEvent::Mouse`或`QContextMenuEvent::Keyboard`。
`pos`参数指定鼠标相对于接收控件的位置。`globalPos` 是鼠标在绝对坐标中的位置。`modifiers` 中保存键盘修改键。

### `const QPoint &QContextMenuEvent::globalPos() const`

**作用与语义：**

返回事件发生时鼠标指针的全局位置。

### `int QContextMenuEvent::globalX() const`

**作用与语义：**

返回事件发生时鼠标指针的全局x位置。

### `int QContextMenuEvent::globalY() const`

**作用与语义：**

返回事件发生时鼠标指针的全局 y 位置。

### `const QPoint &QContextMenuEvent::pos() const`

**作用与语义：**

返回鼠标指针相对于接收事件的控件的位置。
注意：如果`QContextMenuEvent`不是从右键发出，`pos()`可能`null`。

### `QContextMenuEvent::Reason QContextMenuEvent::reason() const`

**作用与语义：**

返回了该上下文事件的原因。

### `int QContextMenuEvent::x() const`

**作用与语义：**

返回鼠标指针相对于接收事件的小部件的 x 位置。

### `int QContextMenuEvent::y() const`

**作用与语义：**

返回鼠标指针相对于接收事件的小部件的y位置。

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

`QContextMenuEvent` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
