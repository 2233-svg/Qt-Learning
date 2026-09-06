# QAbstractAnimation

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QAbstractAnimation` 是 动画时间轴机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QAbstractAnimation` 是 Qt Core 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractAnimation>`
- 继承自：QObject
- 直接派生类：QAnimationGroup、QPauseAnimation,、QVariantAnimation

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

**状态与结果：** 区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

**线程与事件循环：** 界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum DeletionPolicy { KeepWhenStopped, DeleteWhenStopped }`
- `enum Direction { Forward, Backward }`
- `enum State { Stopped, Paused, Running }`

### 属性

- `currentLoop : int`
- `currentTime : int`
- `direction : Direction`
- `duration : int`
- `loopCount : int`
- `state : State`

### 公有函数

- `QAbstractAnimation(QObject *parent = nullptr)`
- `virtual ~QAbstractAnimation()`
- `QBindable<int> bindableCurrentLoop() const`
- `QBindable<int> bindableCurrentTime()`
- `QBindable<QAbstractAnimation::Direction> bindableDirection()`
- `QBindable<int> bindableLoopCount()`
- `QBindable<QAbstractAnimation::State> bindableState() const`
- `int currentLoop() const`
- `int currentLoopTime() const`
- `int currentTime() const`
- `QAbstractAnimation::Direction direction() const`
- `virtual int duration() const = 0`
- `QAnimationGroup * group() const`
- `int loopCount() const`
- `void setDirection(QAbstractAnimation::Direction direction)`
- `void setLoopCount(int loopCount)`
- `QAbstractAnimation::State state() const`
- `int totalDuration() const`

### 公有槽函数

- `void pause()`
- `void resume()`
- `void setCurrentTime(int msecs)`
- `void setPaused(bool paused)`
- `void start(QAbstractAnimation::DeletionPolicy policy = KeepWhenStopped)`
- `void stop()`

### 信号

- `void currentLoopChanged(int currentLoop)`
- `void directionChanged(QAbstractAnimation::Direction newDirection)`
- `void finished()`
- `void stateChanged(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)`

### 保护函数

- `virtual void updateCurrentTime(int currentTime) = 0`
- `virtual void updateDirection(QAbstractAnimation::Direction direction)`
- `virtual void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAbstractAnimation::Direction`

**作用与语义：**

这个枚举描述了处于`Running`状态时动画的方向。
- `QAbstractAnimation::Forward`：`0`;动画当前时间随时间增加（即从0到结束/时长）。
- `QAbstractAnimation::Backward`：`1`;动画当前时间随时间减少（即从结束/时长向0移动）。

### `enum QAbstractAnimation::State`

**作用与语义：**

这个枚举描述了动画的状态。
- `QAbstractAnimation::Stopped`：`0`;动画未运行。这是`QAbstractAnimation`的初始状态，完成后状态`QAbstractAnimation`重新进入。当前时间保持不变，直到调用`setCurrentTime()`或通过调用`start()`开始动画。
- `QAbstractAnimation::Paused`：`1`;动画暂停（即暂时暂停）。调用`resume()`将恢复动画活动。
- `QAbstractAnimation::Running`：`2`;动画正在运行。当控制处于事件循环中时，`QAbstractAnimation`会定期更新当前时间，并在适当时调用`updateCurrentTime()`。

### `[bindable read-only] currentLoop : int`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示动画当前循环。
该属性描述了动画当前循环。默认情况下，动画的循环计数为1，因此当前循环始终为0。如果循环计数为2且动画超过时长，动画会自动倒带并重新开始，当前时间为0，当前循环为1，依此类推。
当电流环发生变化时，`QAbstractAnimation`发出`currentLoopChanged()`信号。

**如何使用：** 调用 `currentLoop()` 读取当前值；它不会修改应用状态。

### `[bindable] currentTime : int`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含动画当前的时间和进度。
该属性描述了动画当前时间。您可以通过调用 setCurrentTime() 来更改当前时间，或者调用 `start()` 让动画运行，随着动画进行自动设置当前时间。
动画当前时间从0开始，到`totalDuration()`结束。
注意：你可以将其他属性绑定到currentTime，但不建议为其设置绑定。随着动画的推进，当前时间会自动更新，从而取消其绑定。

**如何使用：** 调用 `currentTime()` 读取当前值；它不会修改应用状态。

### `[bindable] direction : Direction`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示动画在`Running`状态时的方向。
该方向表示时间是从0趋向动画时长，还是从时长值趋向0，`start()`被调用后。
默认情况下，该属性设置为`Forward`。

**如何使用：** 调用 `direction()` 读取当前值；它不会修改应用状态。

### `[read-only] duration : int`

**作用与语义：**

该属性表示动画的持续时间。
如果时长为-1，表示时长未定义。此时忽略`loopCount`。

**如何使用：** 调用 `duration()` 读取当前值；它不会修改应用状态。

### `[bindable] loopCount : int`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示动画的循环计数。
该属性将动画的循环计数描述为整数。默认值为1，表示动画只运行一次，然后停止。通过更改它，你可以让动画循环多次。当值为0时，动画将完全不运行;当值为-1时，动画将无限循环直到停止。不支持在未定义时长的动画上循环。它只会运行一次。

**如何使用：** 调用 `loopCount()` 读取当前值；它不会修改应用状态。

### `[bindable read-only] state : State`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
动画状态。
该属性描述了动画当前的状态。当动画状态发生变化时，`QAbstractAnimation`会发出`stateChanged()`信号。
注意：状态更新可能导致`currentTime`属性的更新，进而取消其绑定。因此，在为`currentTime`属性设置绑定时要小心，因为你预期动画状态会发生变化。

**如何使用：** 调用 `state()` 读取当前值；它不会修改应用状态。

### `QAbstractAnimation::QAbstractAnimation(QObject *parent = nullptr)`

**作用与语义：**

构造 QAbstractAnimation 基类，并将`parent`传递给 `QObject` 的构造函数。

### `[virtual noexcept] QAbstractAnimation::~QAbstractAnimation()`

**作用与语义：**

如果动画正在运行，它会停止，然后销毁`QAbstractAnimation`。如果动画属于`QAnimationGroup`，动画在被摧毁前会自动移除。

### `[signal] void QAbstractAnimation::currentLoopChanged(int currentLoop)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示动画当前循环。
该属性描述了动画当前循环。默认情况下，动画的循环计数为1，因此当前循环始终为0。如果循环计数为2且动画超过时长，动画会自动倒带并重新开始，当前时间为0，当前循环为1，依此类推。
当电流环发生变化时，`QAbstractAnimation`发出`currentLoopChanged()`信号。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentLoop` 的变化，不要把它当作普通函数主动调用。

### `int QAbstractAnimation::currentLoopTime() const`

**作用与语义：**

返回当前循环内的当前时间。它可以从0到`duration()`。

### `[signal] void QAbstractAnimation::directionChanged(QAbstractAnimation::Direction newDirection)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示动画在`Running`状态时的方向。
该方向表示时间是从0趋向动画时长，还是从时长值趋向0，`start()`被调用后。
默认情况下，该属性设置为`Forward`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `direction` 的变化，不要把它当作普通函数主动调用。

### `[pure virtual] int QAbstractAnimation::duration() const`

**作用与语义：**

这个纯虚拟函数返回动画的时长，并定义`QAbstractAnimation`当前时间的更新时间。该时长是局部的，不包括循环计数。
返回值为-1表示动画没有定义的时长;动画应持续直到停止。这对非时间驱动的动画或难以预测其时长的动画（例如游戏中的事件驱动音频播放）非常有用。
如果动画是平行的`QAnimationGroup`，时长将是所有动画中最长的时长。如果是连续`QAnimationGroup`，则时长是所有动画时长的总和。
注意：属性持续时间的获取函数。

### `[override virtual protected] bool QAbstractAnimation::event(QEvent *event)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。
该虚拟函数接收对象事件，如果事件`e`被识别并处理，应返回真。
event() 函数可以重新实现，以自定义对象的行为。
确保你调用所有未处理的事件的父事件类实现。

### `[signal] void QAbstractAnimation::finished()`

**作用与语义：**

`QAbstractAnimation`在动画结束并完成后发出该信号。
该信号在`stateChanged()`后发出。

### `QAnimationGroup *QAbstractAnimation::group() const`

**作用与语义：**

如果该动画属于`QAnimationGroup`，该函数返回指向该组的指针;否则返回`nullptr`。

### `[slot] void QAbstractAnimation::pause()`

**作用与语义：**

暂停动画。当动画暂停时，`state()`返回暂停。`currentTime`的值会保持不变，直到调用`resume()`或`start()`。如果你想从当前时间继续，请调用`resume()`。

### `[slot] void QAbstractAnimation::resume()`

**作用与语义：**

暂停后恢复动画。动画恢复时，会发出`stateChanged()`信号。`currentTime`属性不变。

### `[slot] void QAbstractAnimation::setPaused(bool paused)`

**作用与语义：**

如果`paused`为真，动画暂停。如果`paused`为假，动画继续。

### `[slot] void QAbstractAnimation::start(QAbstractAnimation::DeletionPolicy policy = KeepWhenStopped)`

**作用与语义：**

开始动画。`policy`参数说明动画完成后是否应删除。动画开始时，`stateChanged()`信号发出，`state()`返回运行。当控制键进入事件循环时，动画会自动运行，并定期调用`updateCurrentTime()`。
如果动画当前停止或已到达结束，调用 start() 会倒带动画并从头开始。当动画结束时，动画会停止，或者如果循环等级超过1，则倒带并从头继续。
如果动画已经在运行，这个函数就不做任何事。

### `[signal] void QAbstractAnimation::stateChanged(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
动画状态。
该属性描述了动画当前的状态。当动画状态发生变化时，`QAbstractAnimation`会发出`stateChanged()`信号。
注意：状态更新可能导致`currentTime`属性的更新，进而取消其绑定。因此，在为`currentTime`属性设置绑定时要小心，因为你预期动画状态会发生变化。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `state` 的变化，不要把它当作普通函数主动调用。

### `[slot] void QAbstractAnimation::stop()`

**作用与语义：**

停止动画。当动画停止时，会发出`stateChanged()`信号，`state()`返回为停止。当前时间不会改变。
如果动画结束后自行停止（即`currentLoopTime()` == `duration()` 和 `currentLoop()` > `loopCount()` - 1），则`finished()`信号会被发出。

### `int QAbstractAnimation::totalDuration() const`

**作用与语义：**

返回动画的总时长和有效时长，包括循环次数。

### `[pure virtual protected] void QAbstractAnimation::updateCurrentTime(int currentTime)`

**作用与语义：**

每次动画`currentTime`变化时都会调用这个纯虚拟函数。

### `[virtual protected] void QAbstractAnimation::updateDirection(QAbstractAnimation::Direction direction)`

**作用与语义：**

当动画方向改变时，`QAbstractAnimation`调用了这个虚拟函数。`direction`参数就是新的方向。

### `[virtual protected] void QAbstractAnimation::updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)`

**作用与语义：**

当动画状态从`oldState`变为`newState`时，`QAbstractAnimation`调用了这个虚拟函数。

### `enum DeletionPolicy { KeepWhenStopped, DeleteWhenStopped }`

**作用与语义：**

- `QAbstractAnimation::KeepWhenStopped`：`0`;停止动画时不会被删除。
- `QAbstractAnimation::DeleteWhenStopped`：`1`;停止时动画会自动删除。

### `QBindable<int> bindableCurrentLoop() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示动画当前循环。
该属性描述了动画当前循环。默认情况下，动画的循环计数为1，因此当前循环始终为0。如果循环计数为2且动画超过时长，动画会自动倒带并重新开始，当前时间为0，当前循环为1，依此类推。
当电流环发生变化时，`QAbstractAnimation`发出`currentLoopChanged()`信号。

**如何使用：** 调用 `bindableCurrentLoop()` 取得 `currentLoop` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<int> bindableCurrentTime()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含动画当前的时间和进度。
该属性描述了动画当前时间。您可以通过调用 setCurrentTime() 来更改当前时间，或者调用 `start()` 让动画运行，随着动画进行自动设置当前时间。
动画当前时间从0开始，到`totalDuration()`结束。
注意：你可以将其他属性绑定到currentTime，但不建议为其设置绑定。随着动画的推进，当前时间会自动更新，从而取消其绑定。

**如何使用：** 调用 `bindableCurrentTime()` 取得 `currentTime` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<QAbstractAnimation::Direction> bindableDirection()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示动画在`Running`状态时的方向。
该方向表示时间是从0趋向动画时长，还是从时长值趋向0，`start()`被调用后。
默认情况下，该属性设置为`Forward`。

**如何使用：** 调用 `bindableDirection()` 取得 `direction` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<int> bindableLoopCount()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示动画的循环计数。
该属性将动画的循环计数描述为整数。默认值为1，表示动画只运行一次，然后停止。通过更改它，你可以让动画循环多次。当值为0时，动画将完全不运行;当值为-1时，动画将无限循环直到停止。不支持在未定义时长的动画上循环。它只会运行一次。

**如何使用：** 调用 `bindableLoopCount()` 取得 `loopCount` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<QAbstractAnimation::State> bindableState() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
动画状态。
该属性描述了动画当前的状态。当动画状态发生变化时，`QAbstractAnimation`会发出`stateChanged()`信号。
注意：状态更新可能导致`currentTime`属性的更新，进而取消其绑定。因此，在为`currentTime`属性设置绑定时要小心，因为你预期动画状态会发生变化。

**如何使用：** 调用 `bindableState()` 取得 `state` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `int currentLoop() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示动画当前循环。
该属性描述了动画当前循环。默认情况下，动画的循环计数为1，因此当前循环始终为0。如果循环计数为2且动画超过时长，动画会自动倒带并重新开始，当前时间为0，当前循环为1，依此类推。
当电流环发生变化时，`QAbstractAnimation`发出`currentLoopChanged()`信号。

**如何使用：** 调用 `currentLoop()` 读取当前值；它不会修改应用状态。

### `int currentTime() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含动画当前的时间和进度。
该属性描述了动画当前时间。您可以通过调用 setCurrentTime() 来更改当前时间，或者调用 `start()` 让动画运行，随着动画进行自动设置当前时间。
动画当前时间从0开始，到`totalDuration()`结束。
注意：你可以将其他属性绑定到currentTime，但不建议为其设置绑定。随着动画的推进，当前时间会自动更新，从而取消其绑定。

**如何使用：** 调用 `currentTime()` 读取当前值；它不会修改应用状态。

### `QAbstractAnimation::Direction direction() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示动画在`Running`状态时的方向。
该方向表示时间是从0趋向动画时长，还是从时长值趋向0，`start()`被调用后。
默认情况下，该属性设置为`Forward`。

**如何使用：** 调用 `direction()` 读取当前值；它不会修改应用状态。

### `int loopCount() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示动画的循环计数。
该属性将动画的循环计数描述为整数。默认值为1，表示动画只运行一次，然后停止。通过更改它，你可以让动画循环多次。当值为0时，动画将完全不运行;当值为-1时，动画将无限循环直到停止。不支持在未定义时长的动画上循环。它只会运行一次。

**如何使用：** 调用 `loopCount()` 读取当前值；它不会修改应用状态。

### `void setDirection(QAbstractAnimation::Direction direction)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示动画在`Running`状态时的方向。
该方向表示时间是从0趋向动画时长，还是从时长值趋向0，`start()`被调用后。
默认情况下，该属性设置为`Forward`。

**如何使用：** 调用 `setDirection(...)` 修改 `direction`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLoopCount(int loopCount)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示动画的循环计数。
该属性将动画的循环计数描述为整数。默认值为1，表示动画只运行一次，然后停止。通过更改它，你可以让动画循环多次。当值为0时，动画将完全不运行;当值为-1时，动画将无限循环直到停止。不支持在未定义时长的动画上循环。它只会运行一次。

**如何使用：** 调用 `setLoopCount(...)` 修改 `loopCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QAbstractAnimation::State state() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
动画状态。
该属性描述了动画当前的状态。当动画状态发生变化时，`QAbstractAnimation`会发出`stateChanged()`信号。
注意：状态更新可能导致`currentTime`属性的更新，进而取消其绑定。因此，在为`currentTime`属性设置绑定时要小心，因为你预期动画状态会发生变化。

**如何使用：** 调用 `state()` 读取当前值；它不会修改应用状态。

### `void setCurrentTime(int msecs)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含动画当前的时间和进度。
该属性描述了动画当前时间。您可以通过调用 setCurrentTime() 来更改当前时间，或者调用 `start()` 让动画运行，随着动画进行自动设置当前时间。
动画当前时间从0开始，到`totalDuration()`结束。
注意：你可以将其他属性绑定到currentTime，但不建议为其设置绑定。随着动画的推进，当前时间会自动更新，从而取消其绑定。

**如何使用：** 调用 `setCurrentTime(...)` 修改 `currentTime`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

### 状态和错误边界

区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

### 线程边界

界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractAnimation` 所属机制类型：动画时间轴机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
