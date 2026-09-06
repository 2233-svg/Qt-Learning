# QDragMoveEvent

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QDragMoveEvent` 是 Qt 的值类型，围绕“拖拽Move事件”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QDragMoveEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QDragMoveEvent>`
- 继承自：QDropEvent
- 直接派生类：QDragEnterEvent

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

- `QDragMoveEvent(const QPoint &pos, Qt::DropActions actions, const QMimeData *data, Qt::MouseButtons buttons, Qt::KeyboardModifiers modifiers, QEvent::Type type = DragMove)`
- `void accept(const QRect &rectangle)`
- `void accept()`
- `QRect answerRect() const`
- `void ignore(const QRect &rectangle)`
- `void ignore()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QDragMoveEvent::QDragMoveEvent(const QPoint &pos, Qt::DropActions actions, const QMimeData *data, Qt::MouseButtons buttons, Qt::KeyboardModifiers modifiers, QEvent::Type type = DragMove)`

**作用与语义：**

创建所需`type`的QDragMoveEvent，表示鼠标处于小部件内`pos`给定的位置。
鼠标和键盘状态由`buttons`和`modifiers`指定，`actions`描述了可能的拖拽操作类型。拖拽数据以MIME编码的信息传递`data`。
警告：请勿自行创建 QDragMoveEvent。这些对象依赖于 Qt 的内部状态。

### `void QDragMoveEvent::accept(const QRect &rectangle)`

**作用与语义：**

与accept()相同，但也会通知如果未来的移动保持在控件上给定的`rectangle`范围内，也将被接受。这可以提升性能，但也可能被底层系统忽略。
如果矩形为空，拖动移动事件将持续发送。这在源节点在定时事件中滚动时非常有用。

### `void QDragMoveEvent::accept()`

**作用与语义：**

打电话`QDropEvent::accept()`。

### `QRect QDragMoveEvent::answerRect() const`

**作用与语义：**

如果被接受，会返回组件中掉落的矩形。你可以利用这些信息限制掉落只在小部件的特定位置。

### `void QDragMoveEvent::ignore(const QRect &rectangle)`

**作用与语义：**

accept（const `QRect`&） 函数的相反。`rectangle`内的移动不可接受，将被忽略。

### `void QDragMoveEvent::ignore()`

**作用与语义：**

调用`QDropEvent::ignore()`。

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

`QDragMoveEvent` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
