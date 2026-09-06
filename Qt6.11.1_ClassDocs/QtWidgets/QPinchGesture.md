# QPinchGesture

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QPinchGesture` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QPinchGesture` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QPinchGesture>`
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

- `enum ChangeFlag { ScaleFactorChanged, RotationAngleChanged, CenterPointChanged }`
- `flags ChangeFlags`

### 属性

- `centerPoint : QPointF`
- `changeFlags : ChangeFlags`
- `lastCenterPoint : QPointF`
- `lastRotationAngle : qreal`
- `lastScaleFactor : qreal`
- `rotationAngle : qreal`
- `scaleFactor : qreal`
- `startCenterPoint : QPointF`
- `totalChangeFlags : ChangeFlags`
- `totalRotationAngle : qreal`
- `totalScaleFactor : qreal`

### 公有函数

- `virtual ~QPinchGesture()`
- `QPointF centerPoint() const`
- `QPinchGesture::ChangeFlags changeFlags() const`
- `QPointF lastCenterPoint() const`
- `qreal lastRotationAngle() const`
- `qreal lastScaleFactor() const`
- `qreal rotationAngle() const`
- `qreal scaleFactor() const`
- `void setCenterPoint(const QPointF &value)`
- `void setChangeFlags(QPinchGesture::ChangeFlags value)`
- `void setLastCenterPoint(const QPointF &value)`
- `void setLastRotationAngle(qreal value)`
- `void setLastScaleFactor(qreal value)`
- `void setRotationAngle(qreal value)`
- `void setScaleFactor(qreal value)`
- `void setStartCenterPoint(const QPointF &value)`
- `void setTotalChangeFlags(QPinchGesture::ChangeFlags value)`
- `void setTotalRotationAngle(qreal value)`
- `void setTotalScaleFactor(qreal value)`
- `QPointF startCenterPoint() const`
- `QPinchGesture::ChangeFlags totalChangeFlags() const`
- `qreal totalRotationAngle() const`
- `qreal totalScaleFactor() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPinchGesture::ChangeFlagflags QPinchGesture::ChangeFlags`

**作用与语义：**

该枚举描述了手势对象属性可能发生的变化。
- `QPinchGesture::ScaleFactorChanged`：`0x1`;`scaleFactor`所持有的比例因子发生了变化。
- `QPinchGesture::RotationAngleChanged`：`0x2`;`rotationAngle`保持的旋转角度发生变化。
- `QPinchGesture::CenterPointChanged`：`0x4`;`centerPoint`持有的中心点发生变化。
ChangeFlags 类型是 QFlags 的 typedef<ChangeFlag>。它存储 ChangeFlag 值的 OR 组合。

### `centerPoint : QPointF`

**作用与语义：**

该属性表示当前的中心点。
中心点是手势中两个输入点之间的中点。

**如何使用：** 调用 `centerPoint()` 读取当前值；它不会修改应用状态。

### `changeFlags : ChangeFlags`

**作用与语义：**

该属性保留当前步骤中变化的手势属性。
该属性表示自上一次手势事件包含该手势信息以来，哪些其他属性发生了变化。你可以利用这些信息判断需要更新用户界面的哪些方面。

**如何使用：** 调用 `changeFlags()` 读取当前值；它不会修改应用状态。

### `lastCenterPoint : QPointF`

**作用与语义：**

此属性保存该手势记录的上次中心点位置。

**如何使用：** 调用 `lastCenterPoint()` 读取当前值；它不会修改应用状态。

### `lastRotationAngle : qreal`

**作用与语义：**

此属性保存手势运动记录的最后报告角度。
最后旋转角度是在先前手势事件交付时，如 `rotationAngle` 属性所报告的角度。

**如何使用：** 调用 `lastRotationAngle()` 读取当前值；它不会修改应用状态。

### `lastScaleFactor : qreal`

**作用与语义：**

此属性保存该手势记录的最后缩放因子。
最后的缩放因子包含先前手势事件中该手势信息，如 `scaleFactor` 属性所报告的缩放因子。
如果没有先前事件提供该手势的信息（即该手势对象包含手势的第一次移动信息），则此属性为零。

**如何使用：** 调用 `lastScaleFactor()` 读取当前值；它不会修改应用状态。

### `rotationAngle : qreal`

**作用与语义：**

该属性表示了手势运动所覆盖的角度。

**如何使用：** 调用 `rotationAngle()` 读取当前值；它不会修改应用状态。

### `scaleFactor : qreal`

**作用与语义：**

该属性表示当前比例因子。
比例因子衡量的是与用户触摸设备中两个输入距离相关的比例因子。

**如何使用：** 调用 `scaleFactor()` 读取当前值；它不会修改应用状态。

### `startCenterPoint : QPointF`

**作用与语义：**

该属性表示中心点的起始位置。

**如何使用：** 调用 `startCenterPoint()` 读取当前值；它不会修改应用状态。

### `totalChangeFlags : ChangeFlags`

**作用与语义：**

该属性包含了手势发生变化的属性。
该属性表示自手势开始以来，哪些其他属性发生了变化。你可以利用这些信息判断需要更新用户界面的哪个方面。

**如何使用：** 调用 `totalChangeFlags()` 读取当前值；它不会修改应用状态。

### `totalRotationAngle : qreal`

**作用与语义：**

该属性包含手势覆盖的总角度。
这个总角度衡量了手势覆盖的全部角度。通常，这等于`rotationAngle`属性所保持的值，除非用户通过移除并重新定位一个触点进行多次旋转，如上所述。在这种情况下，总角度将是手势多个阶段的旋转角度之和。

**如何使用：** 调用 `totalRotationAngle()` 读取当前值；它不会修改应用状态。

### `totalScaleFactor : qreal`

**作用与语义：**

该属性表示总比例因子。
总比例因子衡量了从原始值到当前比例因子的总变化。

**如何使用：** 调用 `totalScaleFactor()` 读取当前值；它不会修改应用状态。

### `[virtual noexcept] QPinchGesture::~QPinchGesture()`

**作用与语义：**

毁灭者。

### `enum ChangeFlag { ScaleFactorChanged, RotationAngleChanged, CenterPointChanged }`

**作用与语义：**

该枚举描述了手势对象属性可能发生的变化。
- `QPinchGesture::ScaleFactorChanged`：`0x1`;`scaleFactor`所持有的比例因子发生了变化。
- `QPinchGesture::RotationAngleChanged`：`0x2`;`rotationAngle`保持的旋转角度发生变化。
- `QPinchGesture::CenterPointChanged`：`0x4`;`centerPoint`持有的中心点发生变化。
ChangeFlags 类型是 QFlags 的 typedef<ChangeFlag>。它存储 ChangeFlag 值的 OR 组合。

### `flags ChangeFlags`

**作用与语义：**

该枚举描述了手势对象属性可能发生的变化。
- `QPinchGesture::ScaleFactorChanged`：`0x1`;`scaleFactor`所持有的比例因子发生了变化。
- `QPinchGesture::RotationAngleChanged`：`0x2`;`rotationAngle`保持的旋转角度发生变化。
- `QPinchGesture::CenterPointChanged`：`0x4`;`centerPoint`持有的中心点发生变化。
ChangeFlags 类型是 QFlags 的 typedef<ChangeFlag>。它存储 ChangeFlag 值的 OR 组合。

### `QPointF centerPoint() const`

**作用与语义：**

该属性表示当前的中心点。
中心点是手势中两个输入点之间的中点。

**如何使用：** 调用 `centerPoint()` 读取当前值；它不会修改应用状态。

### `QPinchGesture::ChangeFlags changeFlags() const`

**作用与语义：**

该属性保留当前步骤中变化的手势属性。
该属性表示自上一次手势事件包含该手势信息以来，哪些其他属性发生了变化。你可以利用这些信息判断需要更新用户界面的哪些方面。

**如何使用：** 调用 `changeFlags()` 读取当前值；它不会修改应用状态。

### `QPointF lastCenterPoint() const`

**作用与语义：**

此属性保存该手势记录的上次中心点位置。

**如何使用：** 调用 `lastCenterPoint()` 读取当前值；它不会修改应用状态。

### `qreal lastRotationAngle() const`

**作用与语义：**

此属性保存手势运动记录的最后报告角度。
最后旋转角度是在先前手势事件交付时，如 `rotationAngle` 属性所报告的角度。

**如何使用：** 调用 `lastRotationAngle()` 读取当前值；它不会修改应用状态。

### `qreal lastScaleFactor() const`

**作用与语义：**

此属性保存该手势记录的最后缩放因子。
最后的缩放因子包含先前手势事件中该手势信息，如 `scaleFactor` 属性所报告的缩放因子。
如果没有先前事件提供该手势的信息（即该手势对象包含手势的第一次移动信息），则此属性为零。

**如何使用：** 调用 `lastScaleFactor()` 读取当前值；它不会修改应用状态。

### `qreal rotationAngle() const`

**作用与语义：**

该属性表示了手势运动所覆盖的角度。

**如何使用：** 调用 `rotationAngle()` 读取当前值；它不会修改应用状态。

### `qreal scaleFactor() const`

**作用与语义：**

该属性表示当前比例因子。
比例因子衡量的是与用户触摸设备中两个输入距离相关的比例因子。

**如何使用：** 调用 `scaleFactor()` 读取当前值；它不会修改应用状态。

### `void setCenterPoint(const QPointF &value)`

**作用与语义：**

该属性表示当前的中心点。
中心点是手势中两个输入点之间的中点。

**如何使用：** 调用 `setCenterPoint(...)` 修改 `centerPoint`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setChangeFlags(QPinchGesture::ChangeFlags value)`

**作用与语义：**

该属性保留当前步骤中变化的手势属性。
该属性表示自上一次手势事件包含该手势信息以来，哪些其他属性发生了变化。你可以利用这些信息判断需要更新用户界面的哪些方面。

**如何使用：** 调用 `setChangeFlags(...)` 修改 `changeFlags`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLastCenterPoint(const QPointF &value)`

**作用与语义：**

此属性保存该手势记录的上次中心点位置。

**如何使用：** 调用 `setLastCenterPoint(...)` 修改 `lastCenterPoint`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLastRotationAngle(qreal value)`

**作用与语义：**

此属性保存手势运动记录的最后报告角度。
最后旋转角度是在先前手势事件交付时，如 `rotationAngle` 属性所报告的角度。

**如何使用：** 调用 `setLastRotationAngle(...)` 修改 `lastRotationAngle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLastScaleFactor(qreal value)`

**作用与语义：**

此属性保存该手势记录的最后缩放因子。
最后的缩放因子包含先前手势事件中该手势信息，如 `scaleFactor` 属性所报告的缩放因子。
如果没有先前事件提供该手势的信息（即该手势对象包含手势的第一次移动信息），则此属性为零。

**如何使用：** 调用 `setLastScaleFactor(...)` 修改 `lastScaleFactor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setRotationAngle(qreal value)`

**作用与语义：**

该属性表示了手势运动所覆盖的角度。

**如何使用：** 调用 `setRotationAngle(...)` 修改 `rotationAngle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setScaleFactor(qreal value)`

**作用与语义：**

该属性表示当前比例因子。
比例因子衡量的是与用户触摸设备中两个输入距离相关的比例因子。

**如何使用：** 调用 `setScaleFactor(...)` 修改 `scaleFactor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStartCenterPoint(const QPointF &value)`

**作用与语义：**

该属性表示中心点的起始位置。

**如何使用：** 调用 `setStartCenterPoint(...)` 修改 `startCenterPoint`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTotalChangeFlags(QPinchGesture::ChangeFlags value)`

**作用与语义：**

该属性包含了手势发生变化的属性。
该属性表示自手势开始以来，哪些其他属性发生了变化。你可以利用这些信息判断需要更新用户界面的哪个方面。

**如何使用：** 调用 `setTotalChangeFlags(...)` 修改 `totalChangeFlags`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTotalRotationAngle(qreal value)`

**作用与语义：**

该属性包含手势覆盖的总角度。
这个总角度衡量了手势覆盖的全部角度。通常，这等于`rotationAngle`属性所保持的值，除非用户通过移除并重新定位一个触点进行多次旋转，如上所述。在这种情况下，总角度将是手势多个阶段的旋转角度之和。

**如何使用：** 调用 `setTotalRotationAngle(...)` 修改 `totalRotationAngle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTotalScaleFactor(qreal value)`

**作用与语义：**

该属性表示总比例因子。
总比例因子衡量了从原始值到当前比例因子的总变化。

**如何使用：** 调用 `setTotalScaleFactor(...)` 修改 `totalScaleFactor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QPointF startCenterPoint() const`

**作用与语义：**

该属性表示中心点的起始位置。

**如何使用：** 调用 `startCenterPoint()` 读取当前值；它不会修改应用状态。

### `QPinchGesture::ChangeFlags totalChangeFlags() const`

**作用与语义：**

该属性包含了手势发生变化的属性。
该属性表示自手势开始以来，哪些其他属性发生了变化。你可以利用这些信息判断需要更新用户界面的哪个方面。

**如何使用：** 调用 `totalChangeFlags()` 读取当前值；它不会修改应用状态。

### `qreal totalRotationAngle() const`

**作用与语义：**

该属性包含手势覆盖的总角度。
这个总角度衡量了手势覆盖的全部角度。通常，这等于`rotationAngle`属性所保持的值，除非用户通过移除并重新定位一个触点进行多次旋转，如上所述。在这种情况下，总角度将是手势多个阶段的旋转角度之和。

**如何使用：** 调用 `totalRotationAngle()` 读取当前值；它不会修改应用状态。

### `qreal totalScaleFactor() const`

**作用与语义：**

该属性表示总比例因子。
总比例因子衡量了从原始值到当前比例因子的总变化。

**如何使用：** 调用 `totalScaleFactor()` 读取当前值；它不会修改应用状态。

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

`QPinchGesture` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
