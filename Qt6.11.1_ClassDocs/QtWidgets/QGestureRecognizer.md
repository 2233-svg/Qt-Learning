# QGestureRecognizer

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGestureRecognizer` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGestureRecognizer` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGestureRecognizer>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `flags Result`
- `enum ResultFlag { Ignore, MayBeGesture, TriggerGesture, FinishGesture, CancelGesture, ConsumeEventHint }`

### 公有函数

- `QGestureRecognizer()`
- `virtual ~QGestureRecognizer()`
- `virtual QGesture * create(QObject *target)`
- `virtual QGestureRecognizer::Result recognize(QGesture *gesture, QObject *watched, QEvent *event) = 0`
- `virtual void reset(QGesture *gesture)`

### 静态公有成员

- `Qt::GestureType registerRecognizer(QGestureRecognizer *recognizer)`
- `void unregisterRecognizer(Qt::GestureType type)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QGestureRecognizer::ResultFlagflags QGestureRecognizer::Result`

**作用与语义：**

该枚举描述了手势识别器状态机当前事件过滤步骤的结果。
结果由一个状态值组成（包括 Ignore、MayBeGesture、TriggerGesture、FinishGesture、CancelGesture）和一个可选提示（ConsumeEventHint）。
- `QGestureRecognizer::Ignore`：`0x0001`;事件不会改变识别器的状态。
- `QGestureRecognizer::MayBeGesture`：`0x0002`;该事件改变了识别器的内部状态，但尚不清楚是否属于手势。识别器需要过滤更多事件来决定。处于MayBeGesture状态的手势识别器如果识别手势过久，可能会被自动重置。
- `QGestureRecognizer::TriggerGesture`：`0x0004`;手势已触发，相应的`QGesture`物品将作为`QGestureEvent`的一部分传递给目标。
- `QGestureRecognizer::FinishGesture`：`0x0008`;动作已成功完成，相应的`QGesture`物将作为`QGestureEvent`的一部分交付给目标。
- `QGestureRecognizer::CancelGesture`：`0x0010`;该事件明确表明它不是手势。如果手势识别器之前处于手势触发状态，则该手势被取消，相应的`QGesture`对象将作为`QGestureEvent`的一部分交付给目标。
- `QGestureRecognizer::ConsumeEventHint`：`0x0100`;该提示指定手势框架应当消耗过滤后的事件，而不是将其传递给接收方。
结果类型是QFlag的typedef<ResultFlag>。它存储了ResultFlag值的OR组合。

### `QGestureRecognizer::QGestureRecognizer()`

**作用与语义：**

构建一个新的手势识别对象。

### `[virtual noexcept] QGestureRecognizer::~QGestureRecognizer()`

**作用与语义：**

会破坏手势识别器。

### `[virtual] QGesture *QGestureRecognizer::create(QObject *target)`

**作用与语义：**

Qt 调用该函数，为给定`target`（`QWidget` 或 `QGraphicsObject`）创建一个新的`QGesture`对象。
如有必要，重新实现该函数以创建自定义`QGesture`派生的手势对象。
`QApplication`对创建的手势对象拥有所有权。

### `[pure virtual] QGestureRecognizer::Result QGestureRecognizer::recognize(QGesture *gesture, QObject *watched, QEvent *event)`

**作用与语义：**

处理`watched`对象的给定`event`，根据需要更新`gesture`对象的状态，并返回当前识别步骤的合适结果。
框架调用该函数，允许识别器过滤分配给其监控的`QWidget`或`QGraphicsObject`实例的输入事件。
结果反映了该手势被识别的程度。`gesture`对象的状态根据结果而设定。

### `[static] Qt::GestureType QGestureRecognizer::registerRecognizer(QGestureRecognizer *recognizer)`

**作用与语义：**

在手势框架中注册给定的`recognizer`，并返回手势ID。
`QApplication` 拥有该`recognizer`，该函数返回与之关联的手势类型 ID。对于处理自定义`QGesture`对象（在`QGesture::gestureType()`函数中返回`Qt::CustomGesture`的手势识别器），返回值是一个生成的手势 ID，`Qt::CustomGesture` 标志已设置。

### `[virtual] void QGestureRecognizer::reset(QGesture *gesture)`

**作用与语义：**

Qt调用该函数以重置给定`gesture`。
重新实现该函数以实现自定义`QGesture`对象的额外需求。如果你实现了一个自定义`QGesture`其属性在手势重置时需要特殊处理，这可能是必要的。

### `[static] void QGestureRecognizer::unregisterRecognizer(Qt::GestureType type)`

**作用与语义：**

取消注册指定`type`的所有手势识别器。

### `flags Result`

**作用与语义：**

该枚举描述了手势识别器状态机当前事件过滤步骤的结果。
结果由一个状态值组成（包括 Ignore、MayBeGesture、TriggerGesture、FinishGesture、CancelGesture）和一个可选提示（ConsumeEventHint）。
- `QGestureRecognizer::Ignore`：`0x0001`;事件不会改变识别器的状态。
- `QGestureRecognizer::MayBeGesture`：`0x0002`;该事件改变了识别器的内部状态，但尚不清楚是否属于手势。识别器需要过滤更多事件来决定。处于MayBeGesture状态的手势识别器如果识别手势过久，可能会被自动重置。
- `QGestureRecognizer::TriggerGesture`：`0x0004`;手势已触发，相应的`QGesture`物品将作为`QGestureEvent`的一部分传递给目标。
- `QGestureRecognizer::FinishGesture`：`0x0008`;动作已成功完成，相应的`QGesture`物将作为`QGestureEvent`的一部分交付给目标。
- `QGestureRecognizer::CancelGesture`：`0x0010`;该事件明确表明它不是手势。如果手势识别器之前处于手势触发状态，则该手势被取消，相应的`QGesture`对象将作为`QGestureEvent`的一部分交付给目标。
- `QGestureRecognizer::ConsumeEventHint`：`0x0100`;该提示指定手势框架应当消耗过滤后的事件，而不是将其传递给接收方。
结果类型是QFlag的typedef<ResultFlag>。它存储了ResultFlag值的OR组合。

### `enum ResultFlag { Ignore, MayBeGesture, TriggerGesture, FinishGesture, CancelGesture, ConsumeEventHint }`

**作用与语义：**

该枚举描述了手势识别器状态机当前事件过滤步骤的结果。
结果由一个状态值组成（包括 Ignore、MayBeGesture、TriggerGesture、FinishGesture、CancelGesture）和一个可选提示（ConsumeEventHint）。
- `QGestureRecognizer::Ignore`：`0x0001`;事件不会改变识别器的状态。
- `QGestureRecognizer::MayBeGesture`：`0x0002`;该事件改变了识别器的内部状态，但尚不清楚是否属于手势。识别器需要过滤更多事件来决定。处于MayBeGesture状态的手势识别器如果识别手势过久，可能会被自动重置。
- `QGestureRecognizer::TriggerGesture`：`0x0004`;手势已触发，相应的`QGesture`物品将作为`QGestureEvent`的一部分传递给目标。
- `QGestureRecognizer::FinishGesture`：`0x0008`;动作已成功完成，相应的`QGesture`物将作为`QGestureEvent`的一部分交付给目标。
- `QGestureRecognizer::CancelGesture`：`0x0010`;该事件明确表明它不是手势。如果手势识别器之前处于手势触发状态，则该手势被取消，相应的`QGesture`对象将作为`QGestureEvent`的一部分交付给目标。
- `QGestureRecognizer::ConsumeEventHint`：`0x0100`;该提示指定手势框架应当消耗过滤后的事件，而不是将其传递给接收方。
结果类型是QFlag的typedef<ResultFlag>。它存储了ResultFlag值的OR组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGestureRecognizer` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
