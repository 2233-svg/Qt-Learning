# QTimeLine

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QTimeLine` 是 动画时间轴机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QTimeLine` 是 动画时间轴机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 动画对象在一段时间内根据进度和 easing 计算值，再写入目标属性或驱动状态。duration、start/end value、loop、direction 和 easing 共同决定时间轴；动画完成、停止和重置是不同状态。

**适用场景：** 确定目标属性和起止值，设置 duration/easing/loop，连接 finished/stateChanged，再 start；多个动画用 group 组织，并在状态变化时明确暂停、停止和重启语义。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在每次状态变化时无条件创建新动画；不要让动画回调持有悬空目标；不要把视觉动画完成当作业务操作完成；属性绑定和动画直接赋值可能互相覆盖。

## 2. 依赖与对象关系

- 头文件：`#include <QTimeLine>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

动画对象在一段时间内根据进度和 easing 计算值，再写入目标属性或驱动状态。duration、start/end value、loop、direction 和 easing 共同决定时间轴；动画完成、停止和重置是不同状态。

### 状态、生命周期和线程

**生命周期：** 动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

**状态与结果：** 区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

**线程与事件循环：** 界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

## 3. 直接使用

确定目标属性和起止值，设置 duration/easing/loop，连接 finished/stateChanged，再 start；多个动画用 group 组织，并在状态变化时明确暂停、停止和重启语义。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Direction { Forward, Backward }`
- `enum State { NotRunning, Paused, Running }`

### 属性

- `currentTime : int`
- `direction : Direction`
- `duration : int`
- `easingCurve : QEasingCurve`
- `loopCount : int`
- `updateInterval : int`

### 公有函数

- `QTimeLine(int duration = 1000, QObject *parent = nullptr)`
- `virtual ~QTimeLine()`
- `QBindable<int> bindableCurrentTime()`
- `QBindable<QTimeLine::Direction> bindableDirection()`
- `QBindable<int> bindableDuration()`
- `QBindable<QEasingCurve> bindableEasingCurve()`
- `QBindable<int> bindableLoopCount()`
- `QBindable<int> bindableUpdateInterval()`
- `int currentFrame() const`
- `int currentTime() const`
- `qreal currentValue() const`
- `QTimeLine::Direction direction() const`
- `int duration() const`
- `QEasingCurve easingCurve() const`
- `int endFrame() const`
- `int frameForTime(int msec) const`
- `int loopCount() const`
- `void setDirection(QTimeLine::Direction direction)`
- `void setDuration(int duration)`
- `void setEasingCurve(const QEasingCurve &curve)`
- `void setEndFrame(int frame)`
- `void setFrameRange(int startFrame, int endFrame)`
- `void setLoopCount(int count)`
- `void setStartFrame(int frame)`
- `void setUpdateInterval(int interval)`
- `int startFrame() const`
- `QTimeLine::State state() const`
- `int updateInterval() const`
- `virtual qreal valueForTime(int msec) const`

### 公有槽函数

- `void resume()`
- `void setCurrentTime(int msec)`
- `void setPaused(bool paused)`
- `void start()`
- `void stop()`
- `void toggleDirection()`

### 信号

- `void finished()`
- `void frameChanged(int frame)`
- `void stateChanged(QTimeLine::State newState)`
- `void valueChanged(qreal value)`

### 重实现的保护函数

- `virtual void timerEvent(QTimerEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTimeLine::Direction`

**作用与语义：**

这个枚举描述了处于`Running`状态时时间线的方向。
- `QTimeLine::Forward`：`0`;时间线当前时间随时间增加（即从0到结束/持续时间）。
- `QTimeLine::Backward`：`1`;时间线当前时间随时间减少（即从结束/持续时间向0移动）。

### `enum QTimeLine::State`

**作用与语义：**

这个枚举描述了时间线的状态。
- `QTimeLine::NotRunning`：`0`;时间线未运行。这是`QTimeLine`的初始状态，完成后`QTimeLine`状态重新进入。当前时间、帧和值保持不变，直到调用`setCurrentTime()`或通过调用`start()`启动时间线。
- `QTimeLine::Paused`：`1`;时间线暂停（即暂时暂停）。调用`setPaused`（false）将恢复时间线活动。
- `QTimeLine::Running`：`2`;时间线正在运行。控制处于事件循环中时，`QTimeLine`会定期更新当前时间，并在适当时发送`valueChanged()`和`frameChanged()`。

### `[bindable] currentTime : int`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示时间线当前时间。
当`QTimeLine`处于运行状态时，该值会根据时间线的持续时间和方向持续更新。否则，该值是`stop()`最后被调用时当前的值，或由 setCurrentTime() 设定的值。
注意：你可以将其他属性绑定到currentTime，但不建议为其设置绑定。随着动画的推进，当前时间会自动更新，从而取消其绑定。
默认情况下，该属性的值为0。

**如何使用：** 调用 `currentTime()` 读取当前值；它不会修改应用状态。

### `[bindable] direction : Direction`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性在`QTimeLine`处于`Running`状态时，保持时间线的方向。
该方向表示时间是从0向时间线时长移动，还是从时长值到0，`start()`被调用后。
任何方向绑定不仅会被 setDirection() 移除，还会被 `toggleDirection()` 移除。
默认情况下，该属性设置为`Forward`。

**如何使用：** 调用 `direction()` 读取当前值；它不会修改应用状态。

### `[bindable] duration : int`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示时间线的总持续时间以毫秒为单位。
默认情况下，这个值是1000（即1秒），但你可以通过将时长传递给`QTimeLine`的构造函数，或者调用setDuration()来更改。时长必须大于0。
注意：更改持续时间不会导致当前时间重置为零或新的持续时间。你还需要用目标值调用`setCurrentTime()`。

**如何使用：** 调用 `duration()` 读取当前值；它不会修改应用状态。

### `[bindable] easingCurve : QEasingCurve`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
指定时间线将使用的缓和曲线。如果`valueForTime()`重新实现，该值将被忽略。

**如何使用：** 调用 `easingCurve()` 读取当前值；它不会修改应用状态。

### `[bindable] loopCount : int`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
这个属性包含时间线在完成前应循环的次数。
循环数为0意味着时间线将永远循环。
默认情况下，该属性包含1的值。

**如何使用：** 调用 `loopCount()` 读取当前值；它不会修改应用状态。

### `[bindable] updateInterval : int`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示每次更新时间之间的时间以毫秒为单位`QTimeLine`。
更新当前时间时，如果当前值发生变化，则`QTimeLine`会发出`valueChanged()`，如果帧发生变化则`frameChanged()`。
默认间隔为40毫秒，相当于每秒25次更新。

**如何使用：** 调用 `updateInterval()` 读取当前值；它不会修改应用状态。

### `[explicit] QTimeLine::QTimeLine(int duration = 1000, QObject *parent = nullptr)`

**作用与语义：**

构建一个持续时间为`duration`毫秒的时间线。`parent`传递给`QObject`的构建器。默认持续时间为1000毫秒。

### `[virtual noexcept] QTimeLine::~QTimeLine()`

**作用与语义：**

毁掉了时间线。

### `int QTimeLine::currentFrame() const`

**作用与语义：**

返回对应当前时间的帧。

### `qreal QTimeLine::currentValue() const`

**作用与语义：**

返回对应当前时间的值。

### `int QTimeLine::endFrame() const`

**作用与语义：**

返回结束帧，即对应时间线结束的帧（即当前值为1的帧）。

### `[private signal] void QTimeLine::finished()`

**作用与语义：**

该信号在`QTimeLine`结束（即到达时间线结束）时发出，且不循环。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QTimeLine::frameChanged(int frame)`

**作用与语义：**

`QTimeLine`在`Running`状态时会定期发出该信号，但仅在当前帧发生变化时才会这样。`frame` 是当前帧编号。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `int QTimeLine::frameForTime(int msec) const`

**作用与语义：**

返回对应时间的帧`msec`。该值通过基于`valueForTime()`返回的值对起始和结束帧进行线性插值计算得出。

### `[slot] void QTimeLine::resume()`

**作用与语义：**

恢复当前时间线。`QTimeLine`会重新进入运行状态，一旦进入事件循环，会定期更新当前时间、帧和值。
与`start()`不同，该功能不会在时间线恢复前重启。

### `void QTimeLine::setEndFrame(int frame)`

**作用与语义：**

将结束帧（即对应时间线结束的帧，即当前值为1的帧）设为`frame`。

### `void QTimeLine::setFrameRange(int startFrame, int endFrame)`

**作用与语义：**

设置时间线的帧计数器从`startFrame`开始，结束和 `endFrame`。对于每个时间值，`QTimeLine`通过插值调用 `currentFrame()` 或 `frameForTime()` 找到对应的帧，并使用返回值 `valueForTime()`。
在运行状态下，帧变化时`QTimeLine`也会发出`frameChanged()`信号。

### `[slot] void QTimeLine::setPaused(bool paused)`

**作用与语义：**

如果`paused`为真，时间线暂停，`QTimeLine`进入暂停状态。在调用`start()`或setPaused（false）之前，不会有更新信号。如果`paused`为假，时间线会恢复并从中断处继续。

### `void QTimeLine::setStartFrame(int frame)`

**作用与语义：**

将起始帧（即对应时间线起点的帧，即当前值为0的帧）设为`frame`。

### `[slot] void QTimeLine::start()`

**作用与语义：**

启动时间线。`QTimeLine` 会进入运行状态，一旦进入事件循环，会定期更新当前时间、帧和值。默认间隔为 40 毫秒（即每秒 25 次）。你可以通过调用 `setUpdateInterval()` 来更改更新间隔。
时间线将从位置0开始，或者如果往回看则从结束。如果你想在不重启的情况下继续暂停的时间线，可以调用`resume()`。

### `int QTimeLine::startFrame() const`

**作用与语义：**

返回起始帧，即对应时间线起点的帧（即当前值为0的帧）。

### `QTimeLine::State QTimeLine::state() const`

**作用与语义：**

返回时间线的状态。

### `[private signal] void QTimeLine::stateChanged(QTimeLine::State newState)`

**作用与语义：**

每当`QTimeLine`的状态发生变化时，就会发出这个信号。新的状态是`newState`。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[slot] void QTimeLine::stop()`

**作用与语义：**

停止时间线，使`QTimeLine`进入`NotRunning`状态。

### `[override virtual protected] void QTimeLine::timerEvent(QTimerEvent *event)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。
该事件处理程序可以被重新实现到子类中，以接收该对象的定时器事件。
`QChronoTimer` 提供了定时器功能的更高级接口，以及关于定时器的更通用信息。定时器事件通过 `event` 参数传递。

### `[slot] void QTimeLine::toggleDirection()`

**作用与语义：**

切换时间线的方向。如果方向是前进，则变成后退，反之亦然。
现有的`direction`绑定被移除。

### `[private signal] void QTimeLine::valueChanged(qreal value)`

**作用与语义：**

`QTimeLine`在`Running`状态时会定期发出该信号，但只有当前值发生变化时才会这样。`value` 是当前值。`value` 是介于 0.0 到 1.0 之间的数字。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[virtual] qreal QTimeLine::valueForTime(int msec) const`

**作用与语义：**

返回时间`msec`的时间线值。返回值根据曲线形状变化，始终在0到1之间。如果`msec`为0，默认实现总是返回0。
重新实现这个函数，为你的时间线提供自定义的曲线形状。

### `QBindable<int> bindableCurrentTime()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示时间线当前时间。
当`QTimeLine`处于运行状态时，该值会根据时间线的持续时间和方向持续更新。否则，该值是`stop()`最后被调用时当前的值，或由 setCurrentTime() 设定的值。
注意：你可以将其他属性绑定到currentTime，但不建议为其设置绑定。随着动画的推进，当前时间会自动更新，从而取消其绑定。
默认情况下，该属性的值为0。

**如何使用：** 调用 `bindableCurrentTime()` 取得 `currentTime` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<QTimeLine::Direction> bindableDirection()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性在`QTimeLine`处于`Running`状态时，保持时间线的方向。
该方向表示时间是从0向时间线时长移动，还是从时长值到0，`start()`被调用后。
任何方向绑定不仅会被 setDirection() 移除，还会被 `toggleDirection()` 移除。
默认情况下，该属性设置为`Forward`。

**如何使用：** 调用 `bindableDirection()` 取得 `direction` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<int> bindableDuration()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示时间线的总持续时间以毫秒为单位。
默认情况下，这个值是1000（即1秒），但你可以通过将时长传递给`QTimeLine`的构造函数，或者调用setDuration()来更改。时长必须大于0。
注意：更改持续时间不会导致当前时间重置为零或新的持续时间。你还需要用目标值调用`setCurrentTime()`。

**如何使用：** 调用 `bindableDuration()` 取得 `duration` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<QEasingCurve> bindableEasingCurve()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
指定时间线将使用的缓和曲线。如果`valueForTime()`重新实现，该值将被忽略。

**如何使用：** 调用 `bindableEasingCurve()` 取得 `easingCurve` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<int> bindableLoopCount()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
这个属性包含时间线在完成前应循环的次数。
循环数为0意味着时间线将永远循环。
默认情况下，该属性包含1的值。

**如何使用：** 调用 `bindableLoopCount()` 取得 `loopCount` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<int> bindableUpdateInterval()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示每次更新时间之间的时间以毫秒为单位`QTimeLine`。
更新当前时间时，如果当前值发生变化，则`QTimeLine`会发出`valueChanged()`，如果帧发生变化则`frameChanged()`。
默认间隔为40毫秒，相当于每秒25次更新。

**如何使用：** 调用 `bindableUpdateInterval()` 取得 `updateInterval` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `int currentTime() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示时间线当前时间。
当`QTimeLine`处于运行状态时，该值会根据时间线的持续时间和方向持续更新。否则，该值是`stop()`最后被调用时当前的值，或由 setCurrentTime() 设定的值。
注意：你可以将其他属性绑定到currentTime，但不建议为其设置绑定。随着动画的推进，当前时间会自动更新，从而取消其绑定。
默认情况下，该属性的值为0。

**如何使用：** 调用 `currentTime()` 读取当前值；它不会修改应用状态。

### `QTimeLine::Direction direction() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性在`QTimeLine`处于`Running`状态时，保持时间线的方向。
该方向表示时间是从0向时间线时长移动，还是从时长值到0，`start()`被调用后。
任何方向绑定不仅会被 setDirection() 移除，还会被 `toggleDirection()` 移除。
默认情况下，该属性设置为`Forward`。

**如何使用：** 调用 `direction()` 读取当前值；它不会修改应用状态。

### `int duration() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示时间线的总持续时间以毫秒为单位。
默认情况下，这个值是1000（即1秒），但你可以通过将时长传递给`QTimeLine`的构造函数，或者调用setDuration()来更改。时长必须大于0。
注意：更改持续时间不会导致当前时间重置为零或新的持续时间。你还需要用目标值调用`setCurrentTime()`。

**如何使用：** 调用 `duration()` 读取当前值；它不会修改应用状态。

### `QEasingCurve easingCurve() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
指定时间线将使用的缓和曲线。如果`valueForTime()`重新实现，该值将被忽略。

**如何使用：** 调用 `easingCurve()` 读取当前值；它不会修改应用状态。

### `int loopCount() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
这个属性包含时间线在完成前应循环的次数。
循环数为0意味着时间线将永远循环。
默认情况下，该属性包含1的值。

**如何使用：** 调用 `loopCount()` 读取当前值；它不会修改应用状态。

### `void setDirection(QTimeLine::Direction direction)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性在`QTimeLine`处于`Running`状态时，保持时间线的方向。
该方向表示时间是从0向时间线时长移动，还是从时长值到0，`start()`被调用后。
任何方向绑定不仅会被 setDirection() 移除，还会被 `toggleDirection()` 移除。
默认情况下，该属性设置为`Forward`。

**如何使用：** 调用 `setDirection(...)` 修改 `direction`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDuration(int duration)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示时间线的总持续时间以毫秒为单位。
默认情况下，这个值是1000（即1秒），但你可以通过将时长传递给`QTimeLine`的构造函数，或者调用setDuration()来更改。时长必须大于0。
注意：更改持续时间不会导致当前时间重置为零或新的持续时间。你还需要用目标值调用`setCurrentTime()`。

**如何使用：** 调用 `setDuration(...)` 修改 `duration`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setEasingCurve(const QEasingCurve &curve)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
指定时间线将使用的缓和曲线。如果`valueForTime()`重新实现，该值将被忽略。

**如何使用：** 调用 `setEasingCurve(...)` 修改 `easingCurve`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLoopCount(int count)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
这个属性包含时间线在完成前应循环的次数。
循环数为0意味着时间线将永远循环。
默认情况下，该属性包含1的值。

**如何使用：** 调用 `setLoopCount(...)` 修改 `loopCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUpdateInterval(int interval)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示每次更新时间之间的时间以毫秒为单位`QTimeLine`。
更新当前时间时，如果当前值发生变化，则`QTimeLine`会发出`valueChanged()`，如果帧发生变化则`frameChanged()`。
默认间隔为40毫秒，相当于每秒25次更新。

**如何使用：** 调用 `setUpdateInterval(...)` 修改 `updateInterval`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int updateInterval() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示每次更新时间之间的时间以毫秒为单位`QTimeLine`。
更新当前时间时，如果当前值发生变化，则`QTimeLine`会发出`valueChanged()`，如果帧发生变化则`frameChanged()`。
默认间隔为40毫秒，相当于每秒25次更新。

**如何使用：** 调用 `updateInterval()` 读取当前值；它不会修改应用状态。

### `void setCurrentTime(int msec)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示时间线当前时间。
当`QTimeLine`处于运行状态时，该值会根据时间线的持续时间和方向持续更新。否则，该值是`stop()`最后被调用时当前的值，或由 setCurrentTime() 设定的值。
注意：你可以将其他属性绑定到currentTime，但不建议为其设置绑定。随着动画的推进，当前时间会自动更新，从而取消其绑定。
默认情况下，该属性的值为0。

**如何使用：** 调用 `setCurrentTime(...)` 修改 `currentTime`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

### 状态和错误边界

区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

### 线程边界

界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

### 最容易出现的错误

不要在每次状态变化时无条件创建新动画；不要让动画回调持有悬空目标；不要把视觉动画完成当作业务操作完成；属性绑定和动画直接赋值可能互相覆盖。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTimeLine` 所属机制类型：动画时间轴机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
