# QColorAxis

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QColorAxis` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QColorAxis` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QColorAxis>`
- 继承自：QAbstractAxis
- 直接派生类：未在类页中列出

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `autoRange : bool`
- `max : qreal`
- `min : qreal`
- `size : qreal`
- `tickCount : int`

### 公有函数

- `virtual ~QColorAxis()`
- `bool autoRange() const`
- `QLinearGradient gradient() const`
- `qreal max() const`
- `qreal min() const`
- `void setAutoRange(bool autoRange)`
- `void setGradient(const QLinearGradient &gradient)`
- `void setMax(qreal max)`
- `void setMin(qreal min)`
- `void setSize(const qreal size)`
- `void setTickCount(int count)`
- `qreal size() const`
- `int tickCount() const`

### 信号

- `void autoRangeChanged(bool autoRange)`
- `void maxChanged(qreal max)`
- `void minChanged(qreal min)`
- `void rangeChanged(qreal min, qreal max)`
- `void sizeChanged(const qreal size)`
- `void tickCountChanged(int tickCount)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `autoRange : bool`

**作用与语义：**

该属性包含了指示区间是从方法中传递的值列表中设置，还是从轴本身中取`QXYSeries::colorBy`属性。
默认值为`true`。

**如何使用：** 调用 `autoRange()` 读取当前值；它不会修改应用状态。

### `max : qreal`

**作用与语义：**

该属性在轴上占最大值。
设置该属性时，必要时会调整最小值，以确保范围有效。

**如何使用：** 调用 `max()` 读取当前值；它不会修改应用状态。

### `min : qreal`

**作用与语义：**

该属性在轴上保持最小值。
设置该属性时，如有必要会调整最大值，以确保范围有效。

**如何使用：** 调用 `min()` 读取当前值；它不会修改应用状态。

### `size : qreal`

**作用与语义：**

该属性表示颜色尺度大小。
根据对齐方式，数值表示宽度或高度。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `tickCount : int`

**作用与语义：**

该属性表示轴上的刻度数。如果QColorAxis：：gridVisible等于`true`，则表示图表上绘制的网格线数量。默认值为5，且该数目不能小于2。
注意：网格线在`QColorAxis`中默认是故意不可见的，因为这种轴不代表几何值。

**如何使用：** 调用 `tickCount()` 读取当前值；它不会修改应用状态。

### `[virtual noexcept] QColorAxis::~QColorAxis()`

**作用与语义：**

摧毁了该物体。

### `[signal] void QColorAxis::autoRangeChanged(bool autoRange)`

**作用与语义：**

该属性包含了指示区间是从方法中传递的值列表中设置，还是从轴本身中取`QXYSeries::colorBy`属性。
默认值为`true`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `autoRange` 的变化，不要把它当作普通函数主动调用。

### `QLinearGradient QColorAxis::gradient() const`

**作用与语义：**

返回当前色阶上的渐变。
注意：如果轴连接到系列，`QXYSeries::colorBy`方法也会使用梯度。

### `[signal] void QColorAxis::maxChanged(qreal max)`

**作用与语义：**

该属性在轴上占最大值。
设置该属性时，必要时会调整最小值，以确保范围有效。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `max` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QColorAxis::minChanged(qreal min)`

**作用与语义：**

该属性在轴上保持最小值。
设置该属性时，如有必要会调整最大值，以确保范围有效。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `min` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QColorAxis::rangeChanged(qreal min, qreal max)`

**作用与语义：**

当轴的最小值或最大值（由`min`和`max`指定）发生变化时，会发出该信号。

### `void QColorAxis::setGradient(const QLinearGradient &gradient)`

**作用与语义：**

将色阶上的渐变设置为`gradient`。
注意：如果轴连接到系列，`QXYSeries::colorBy`方法也会使用梯度。

### `[signal] void QColorAxis::tickCountChanged(int tickCount)`

**作用与语义：**

该属性表示轴上的刻度数。如果QColorAxis：：gridVisible等于`true`，则表示图表上绘制的网格线数量。默认值为5，且该数目不能小于2。
注意：网格线在`QColorAxis`中默认是故意不可见的，因为这种轴不代表几何值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `tickCount` 的变化，不要把它当作普通函数主动调用。

### `bool autoRange() const`

**作用与语义：**

该属性包含了指示区间是从方法中传递的值列表中设置，还是从轴本身中取`QXYSeries::colorBy`属性。
默认值为`true`。

**如何使用：** 调用 `autoRange()` 读取当前值；它不会修改应用状态。

### `qreal max() const`

**作用与语义：**

该属性在轴上占最大值。
设置该属性时，必要时会调整最小值，以确保范围有效。

**如何使用：** 调用 `max()` 读取当前值；它不会修改应用状态。

### `qreal min() const`

**作用与语义：**

该属性在轴上保持最小值。
设置该属性时，如有必要会调整最大值，以确保范围有效。

**如何使用：** 调用 `min()` 读取当前值；它不会修改应用状态。

### `void setAutoRange(bool autoRange)`

**作用与语义：**

该属性包含了指示区间是从方法中传递的值列表中设置，还是从轴本身中取`QXYSeries::colorBy`属性。
默认值为`true`。

**如何使用：** 调用 `setAutoRange(...)` 修改 `autoRange`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMax(qreal max)`

**作用与语义：**

该属性在轴上占最大值。
设置该属性时，必要时会调整最小值，以确保范围有效。

**如何使用：** 调用 `setMax(...)` 修改 `max`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMin(qreal min)`

**作用与语义：**

该属性在轴上保持最小值。
设置该属性时，如有必要会调整最大值，以确保范围有效。

**如何使用：** 调用 `setMin(...)` 修改 `min`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSize(const qreal size)`

**作用与语义：**

该属性表示颜色尺度大小。
根据对齐方式，数值表示宽度或高度。

**如何使用：** 调用 `setSize(...)` 修改 `size`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTickCount(int count)`

**作用与语义：**

该属性表示轴上的刻度数。如果QColorAxis：：gridVisible等于`true`，则表示图表上绘制的网格线数量。默认值为5，且该数目不能小于2。
注意：网格线在`QColorAxis`中默认是故意不可见的，因为这种轴不代表几何值。

**如何使用：** 调用 `setTickCount(...)` 修改 `tickCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `qreal size() const`

**作用与语义：**

该属性表示颜色尺度大小。
根据对齐方式，数值表示宽度或高度。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `int tickCount() const`

**作用与语义：**

该属性表示轴上的刻度数。如果QColorAxis：：gridVisible等于`true`，则表示图表上绘制的网格线数量。默认值为5，且该数目不能小于2。
注意：网格线在`QColorAxis`中默认是故意不可见的，因为这种轴不代表几何值。

**如何使用：** 调用 `tickCount()` 读取当前值；它不会修改应用状态。

### `void sizeChanged(const qreal size)`

**作用与语义：**

该属性表示颜色尺度大小。
根据对齐方式，数值表示宽度或高度。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `size` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QColorAxis` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
