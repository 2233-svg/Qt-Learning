# QSwipeGesture

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QSwipeGesture` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QSwipeGesture` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QSwipeGesture>`
- 继承自：QGesture
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

- `enum SwipeDirection { NoDirection, Left, Right, Up, Down }`

### 属性

- `horizontalDirection : SwipeDirection`
- `swipeAngle : qreal`
- `verticalDirection : SwipeDirection`

### 公有函数

- `virtual ~QSwipeGesture()`
- `QSwipeGesture::SwipeDirection horizontalDirection() const`
- `void setSwipeAngle(qreal value)`
- `qreal swipeAngle() const`
- `QSwipeGesture::SwipeDirection verticalDirection() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSwipeGesture::SwipeDirection`

**作用与语义：**

该枚举描述了手势沿水平和垂直轴运动的可能方向。
- `QSwipeGesture::NoDirection`：`0`;该手势在特定轴上没有运动。
- `QSwipeGesture::Left`：`1`;该手势涉及向左水平移动。
- `QSwipeGesture::Right`：`2`;该手势涉及向右水平移动。
- `QSwipeGesture::Up`：`3`;该手势涉及向上的垂直动作。
- `QSwipeGesture::Down`：`4`;该手势涉及向下的垂直动作。

### `[read-only] horizontalDirection : SwipeDirection`

**作用与语义：**

该属性表示手势的水平方向。
如果手势包含水平分量，水平方向是左或右;否则则是`NoDirection`。

**如何使用：** 调用 `horizontalDirection()` 读取当前值；它不会修改应用状态。

### `swipeAngle : qreal`

**作用与语义：**

该属性包含与手势相关的运动角度。
如果手势具有水平或垂直分量，滑动角度描述了运动方向与x轴之间的夹角，该角度是使用标准控件坐标系定义的。

**如何使用：** 调用 `swipeAngle()` 读取当前值；它不会修改应用状态。

### `[read-only] verticalDirection : SwipeDirection`

**作用与语义：**

该属性表示手势的垂直方向。
如果手势有垂直成分，垂直方向是向上或向下;否则则为`NoDirection`。

**如何使用：** 调用 `verticalDirection()` 读取当前值；它不会修改应用状态。

### `[virtual noexcept] QSwipeGesture::~QSwipeGesture()`

**作用与语义：**

毁灭者。

### `QSwipeGesture::SwipeDirection horizontalDirection() const`

**作用与语义：**

该属性表示手势的水平方向。
如果手势包含水平分量，水平方向是左或右;否则则是`NoDirection`。

**如何使用：** 调用 `horizontalDirection()` 读取当前值；它不会修改应用状态。

### `void setSwipeAngle(qreal value)`

**作用与语义：**

该属性包含与手势相关的运动角度。
如果手势具有水平或垂直分量，滑动角度描述了运动方向与x轴之间的夹角，该角度是使用标准控件坐标系定义的。

**如何使用：** 调用 `setSwipeAngle(...)` 修改 `swipeAngle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `qreal swipeAngle() const`

**作用与语义：**

该属性包含与手势相关的运动角度。
如果手势具有水平或垂直分量，滑动角度描述了运动方向与x轴之间的夹角，该角度是使用标准控件坐标系定义的。

**如何使用：** 调用 `swipeAngle()` 读取当前值；它不会修改应用状态。

### `QSwipeGesture::SwipeDirection verticalDirection() const`

**作用与语义：**

该属性表示手势的垂直方向。
如果手势有垂直成分，垂直方向是向上或向下;否则则为`NoDirection`。

**如何使用：** 调用 `verticalDirection()` 读取当前值；它不会修改应用状态。

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

`QSwipeGesture` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
