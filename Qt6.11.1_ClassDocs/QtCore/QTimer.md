# QTimer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QTimer` 把时间间隔转换成事件循环中的 `timeout()` 通知，适合周期任务、延迟任务和 UI 刷新。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QTimer` 把时间间隔转换成事件循环中的 `timeout()` 通知，适合周期任务、延迟任务和 UI 刷新。

**内部模型：** QTimer 不会创建线程，也不会保证精确到毫秒；它只是把一个定时事件投递到所属线程的事件循环。定时器所属线程必须有事件循环，并且 start/stop 要在该线程执行。

**适用场景：** 周期刷新、重试、超时、延迟初始化和把少量工作分批执行时使用；不要用零间隔定时器长期执行重计算，也不要用它替代真正的后台线程。

**典型调用链：** 创建并设置 parent -> connect(timeout) -> setInterval/setSingleShot -> start -> 在 timeout 中执行短任务 -> stop 或自然结束。

**先记住的坑：** timeout 不能假定精确时间；超时槽不能阻塞；跨线程启动/停止是错误用法；singleShot 的 context 应覆盖回调使用的对象生命周期。

## 2. 依赖与对象关系

- 头文件：`#include <QTimer>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QTimer 不会创建线程，也不会保证精确到毫秒；它只是把一个定时事件投递到所属线程的事件循环。定时器所属线程必须有事件循环，并且 start/stop 要在该线程执行。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** `isActive()`、`remainingTime()`、`singleShot` 和 `timerType` 共同描述定时器状态。零毫秒定时器适合把少量工作分批交还事件循环，不能用来替代后台线程。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

周期刷新、重试、超时、延迟初始化和把少量工作分批执行时使用；不要用零间隔定时器长期执行重计算，也不要用它替代真正的后台线程。 使用时通常按这个过程组织：创建并设置 parent -> connect(timeout) -> setInterval/setSingleShot -> start -> 在 timeout 中执行短任务 -> stop 或自然结束。

```cpp
#include <QTimer>

QTimer *timer = new QTimer(this);
timer->setInterval(1000);
connect(timer, &QTimer::timeout, this, [this] {
    updateStatus();
});
timer->start();
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `active : bool`
- `interval : int`
- `remainingTime : int`
- `singleShot : bool`
- `timerType : Qt::TimerType`

### 公有函数

- `QTimer(QObject *parent = nullptr)`
- `virtual ~QTimer()`
- `QBindable<bool> bindableActive()`
- `QBindable<int> bindableInterval()`
- `QBindable<bool> bindableSingleShot()`
- `QBindable<Qt::TimerType> bindableTimerType()`
- `QMetaObject::Connection callOnTimeout(Functor &&slot)`
- `QMetaObject::Connection callOnTimeout(const QObject *context, Functor &&slot, Qt::ConnectionType connectionType = Qt::AutoConnection)`
- `(since 6.8) Qt::TimerId id() const`
- `int interval() const`
- `std::chrono::milliseconds intervalAsDuration() const`
- `bool isActive() const`
- `bool isSingleShot() const`
- `int remainingTime() const`
- `std::chrono::milliseconds remainingTimeAsDuration() const`
- `void setInterval(int msec)`
- `void setInterval(std::chrono::milliseconds value)`
- `void setSingleShot(bool singleShot)`
- `void setTimerType(Qt::TimerType atype)`
- `void start(std::chrono::milliseconds interval)`
- `int timerId() const`
- `Qt::TimerType timerType() const`

### 公有槽函数

- `void start(int msec)`
- `void start()`
- `void stop()`

### 信号

- `void timeout()`

### 静态公有成员

- `void singleShot(Duration interval, Functor &&functor)`
- `void singleShot(Duration interval, Qt::TimerType timerType, Functor &&functor)`
- `void singleShot(Duration interval, const QObject *context, Functor &&functor)`
- `void singleShot(Duration interval, Qt::TimerType timerType, const QObject *context, Functor &&functor)`
- `void singleShot(std::chrono::nanoseconds nsec, const QObject *receiver, const char *member)`
- `void singleShot(std::chrono::nanoseconds nsec, Qt::TimerType timerType, const QObject *receiver, const char *member)`

### 重实现的保护函数

- `virtual void timerEvent(QTimerEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[bindable read-only] active : bool`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
如果计时器正在运行，这个布尔属性`true`;否则为假。

**如何使用：** 调用 `active()` 读取当前值；它不会修改应用状态。

### `[bindable] interval : int`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示超时区间以毫秒为单位。
该属性的默认值为0。超时区间为0的`QTimer`，一旦窗口系统事件队列中的所有事件都处理完毕，就会超时。
注意：用零计时器让事件循环保持忙碌，必然会引发问题和UI的高度不稳定行为。
设置运行计时器的间隔会改变该间隔，`stop()`然后`start()`计时器，并获得新的`id()`。如果计时器未运行，仅会更改该间隔。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。

**如何使用：** 调用 `interval()` 读取当前值；它不会修改应用状态。

### `[read-only] remainingTime : int`

**作用与语义：**

该属性使剩余时间以毫秒为单位。
在超时前剩余毫秒内返回计时器的剩余值。如果计时器处于非激活状态，返回的值将为-1。如果计时器逾期，返回的值将为0。

**如何使用：** 调用 `remainingTime()` 读取当前值；它不会修改应用状态。

### `[bindable] singleShot : bool`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性适用于计时器是否为单次计时器。
单发计时器仅发射一次，非单发计时器每`interval`毫秒发射一次。
该房产的默认价值为`false`。

**如何使用：** 调用 `singleShot()` 读取当前值；它不会修改应用状态。

### `[bindable] timerType : Qt::TimerType`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
控制计时器的准确性。
该房产的默认价值为`Qt::CoarseTimer`。

**如何使用：** 调用 `timerType()` 读取当前值；它不会修改应用状态。

### `[explicit] QTimer::QTimer(QObject *parent = nullptr)`

**作用与语义：**

用给定的计时器`parent`。

### `[virtual noexcept] QTimer::~QTimer()`

**作用与语义：**

会破坏计时器。

### `template <typename Functor> QMetaObject::Connection QTimer::callOnTimeout(Functor &&slot)`

**作用与语义：**

从定时器的`timeout()`信号到`slot`建立连接。返回连接的句柄。
此方法仅为方便而提供。它等同于调用：
注意：当`QT_NO_CONTEXTLESS_CONNECT`定义时，该超载不可用，改用调用 callOnTimeout() 重载，该重载取上下文对象。

**官方示例：**

```cpp
 QObject::connect(timer, &QTimer::timeout, timer, slot, Qt::DirectConnection);
```

### `template <typename Functor> QMetaObject::Connection QTimer::callOnTimeout(const QObject *context, Functor &&slot, Qt::ConnectionType connectionType = Qt::AutoConnection)`

**作用与语义：**

从`timeout()`信号到`slot`，创建连接，置于特定事件循环中的`context`，并返回连接的句柄。
此方法仅为方便而提供。它等同于调用：
注意：该功能会`QTimer::callOnTimeout()`重载。

**官方示例：**

```cpp
 QObject::connect(timer, &QTimer::timeout, context, slot, connectionType);
```

### `[since 6.8] Qt::TimerId QTimer::id() const`

**作用与语义：**

如果计时器正在运行，返回代表计时器的`Qt::TimerId`;否则返回`Qt::TimerId::Invalid`。

### `std::chrono::milliseconds QTimer::intervalAsDuration() const`

**作用与语义：**

返回该计时器的间隔，作为`std::chrono::milliseconds`对象。

### `bool QTimer::isActive() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
如果计时器正在运行，这个布尔属性`true`;否则为假。

**如何使用：** 调用 `isActive()` 读取当前值；它不会修改应用状态。

### `std::chrono::milliseconds QTimer::remainingTimeAsDuration() const`

**作用与语义：**

返回该计时器对象剩余时间，作为`std::chrono::milliseconds`对象。如果计时器到期或逾期，返回的值为`std::chrono::milliseconds::zero()`。如果找不到剩余时间或计时器未运行，该函数返回负时长。

### `[static] template <typename Duration, typename Functor> void QTimer::singleShot(Duration interval, Qt::TimerType timerType, Functor &&functor)`

**作用与语义：**

这个静态函数在 `interval` 后调用 `functor`。
使用这个函数非常方便，因为你无需费心创建`timerEvent`或创建本地`QTimer`对象。
如果指定了`context`，则只有当`context`对象在区间发生前未被销毁时才调用`functor`。然后该函子将运行在`context`的线程上。上下文线程必须有一个运行中的Qt事件循环。
如果`functor`是`context`的成员函数，则该函数将在对象上被调用。
`interval`参数可以是`int`（被解释为毫秒计数）或隐式转换为纳秒的`std::chrono`类型。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。
注意：在6.8之前的Qt版本中，计时重载需要计时：毫秒，而非计时：：纳秒。编译器会自动帮你转换，但转换可能会溢出极大的毫秒数。
注意：该函数是重入函数。

### `[static] void QTimer::singleShot(std::chrono::nanoseconds nsec, const QObject *receiver, const char *member)`

**作用与语义：**

这个静态函数在 `interval` 后调用 `functor`。
使用这个函数非常方便，因为你无需费心创建`timerEvent`或创建本地`QTimer`对象。
如果指定了`context`，则只有当`context`对象在区间发生前未被销毁时才调用`functor`。然后该函子将运行在`context`的线程上。上下文线程必须有一个运行中的Qt事件循环。
如果`functor`是`context`的成员函数，则该函数将在对象上被调用。
`interval`参数可以是`int`（被解释为毫秒计数）或隐式转换为纳秒的`std::chrono`类型。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。
注意：在6.8之前的Qt版本中，计时重载需要计时：毫秒，而非计时：：纳秒。编译器会自动帮你转换，但转换可能会溢出极大的毫秒数。
注意：该函数是重入函数。

### `[static] void QTimer::singleShot(std::chrono::nanoseconds nsec, Qt::TimerType timerType, const QObject *receiver, const char *member)`

**作用与语义：**

这个静态函数在 `interval` 后调用 `functor`。
使用这个函数非常方便，因为你无需费心创建`timerEvent`或创建本地`QTimer`对象。
如果指定了`context`，则只有当`context`对象在区间发生前未被销毁时才调用`functor`。然后该函子将运行在`context`的线程上。上下文线程必须有一个运行中的Qt事件循环。
如果`functor`是`context`的成员函数，则该函数将在对象上被调用。
`interval`参数可以是`int`（被解释为毫秒计数）或隐式转换为纳秒的`std::chrono`类型。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。
注意：在6.8之前的Qt版本中，计时重载需要计时：毫秒，而非计时：：纳秒。编译器会自动帮你转换，但转换可能会溢出极大的毫秒数。
注意：该函数是重入函数。

### `[slot] void QTimer::start(int msec)`

**作用与语义：**

以`msec`毫秒的超时间隔启动或重启计时器。
这等价于：
如果计时器已经在运行，它会被`stopped`并重新开始。这也会改变它的 `id()`。
如果`singleShot`为真，计时器只会被激活一次。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。
注意：用零计时器让事件循环保持忙碌，必然会引发问题和UI的高度不稳定行为。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
timer， qOverload（&QTimer：：start））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
计时器，[接收者 = 计时器]（int msec） { receiver->start（msec）; }）;


更多示例和方法，请参见连接超载槽位。

**官方示例：**

```cpp
 timer.setInterval(msec);
 timer.start();
```

### `[slot] void QTimer::start()`

**作用与语义：**

按照`interval`中指定的超时时间开始或重启计时器。
如果计时器已经在运行，它会被`stopped`并重新开始。这也会改变它的计时`id()`。
如果`singleShot`为真，计时器只会被激活一次。
注意：用零计时器让事件循环保持忙碌，必然会引发问题和UI的高度不稳定行为。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
计时器，qOverload<>（&QTimer：：start））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
计时器，[接收器 = 计时器]() { 接收器->start(); }）;


更多示例和方法，请参见连接超载槽位。

### `void QTimer::start(std::chrono::milliseconds interval)`

**作用与语义：**

以`interval`毫秒的超时启动或重启计时器。
这等价于：
如果计时器已经在运行，它会被`stopped`并重新启动。这也会改变它的 `id()`。
如果`singleShot`为真，计时器只会被激活一次。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。
注意：用零计时器让事件循环保持忙碌，必然会引发问题和UI的高度不稳定行为。

**官方示例：**

```cpp
 timer.setInterval(interval);
 timer.start();
```

### `[slot] void QTimer::stop()`

**作用与语义：**

停止计时器。

### `[private signal] void QTimer::timeout()`

**作用与语义：**

当计时器超时时，该信号会发出。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[override virtual protected] void QTimer::timerEvent(QTimerEvent *e)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。
该事件处理程序可以被重新实现到子类中，以接收该对象的定时器事件。
`QChronoTimer` 提供了定时器功能的更高级接口，以及关于定时器的更通用信息。定时器事件通过 `event` 参数传递。

### `int QTimer::timerId() const`

**作用与语义：**

如果计时器正在运行，返回计时器的ID;否则返回-1。

### `QBindable<bool> bindableActive()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
如果计时器正在运行，这个布尔属性`true`;否则为假。

**如何使用：** 调用 `bindableActive()` 取得 `active` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<int> bindableInterval()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示超时区间以毫秒为单位。
该属性的默认值为0。超时区间为0的`QTimer`，一旦窗口系统事件队列中的所有事件都处理完毕，就会超时。
注意：用零计时器让事件循环保持忙碌，必然会引发问题和UI的高度不稳定行为。
设置运行计时器的间隔会改变该间隔，`stop()`然后`start()`计时器，并获得新的`id()`。如果计时器未运行，仅会更改该间隔。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。

**如何使用：** 调用 `bindableInterval()` 取得 `interval` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<bool> bindableSingleShot()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性适用于计时器是否为单次计时器。
单发计时器仅发射一次，非单发计时器每`interval`毫秒发射一次。
该房产的默认价值为`false`。

**如何使用：** 调用 `bindableSingleShot()` 取得 `singleShot` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<Qt::TimerType> bindableTimerType()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
控制计时器的准确性。
该房产的默认价值为`Qt::CoarseTimer`。

**如何使用：** 调用 `bindableTimerType()` 取得 `timerType` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `int interval() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示超时区间以毫秒为单位。
该属性的默认值为0。超时区间为0的`QTimer`，一旦窗口系统事件队列中的所有事件都处理完毕，就会超时。
注意：用零计时器让事件循环保持忙碌，必然会引发问题和UI的高度不稳定行为。
设置运行计时器的间隔会改变该间隔，`stop()`然后`start()`计时器，并获得新的`id()`。如果计时器未运行，仅会更改该间隔。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。

**如何使用：** 调用 `interval()` 读取当前值；它不会修改应用状态。

### `bool isSingleShot() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性适用于计时器是否为单次计时器。
单发计时器仅发射一次，非单发计时器每`interval`毫秒发射一次。
该房产的默认价值为`false`。

**如何使用：** 调用 `isSingleShot()` 读取当前值；它不会修改应用状态。

### `int remainingTime() const`

**作用与语义：**

该属性使剩余时间以毫秒为单位。
在超时前剩余毫秒内返回计时器的剩余值。如果计时器处于非激活状态，返回的值将为-1。如果计时器逾期，返回的值将为0。

**如何使用：** 调用 `remainingTime()` 读取当前值；它不会修改应用状态。

### `void setInterval(int msec)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示超时区间以毫秒为单位。
该属性的默认值为0。超时区间为0的`QTimer`，一旦窗口系统事件队列中的所有事件都处理完毕，就会超时。
注意：用零计时器让事件循环保持忙碌，必然会引发问题和UI的高度不稳定行为。
设置运行计时器的间隔会改变该间隔，`stop()`然后`start()`计时器，并获得新的`id()`。如果计时器未运行，仅会更改该间隔。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。

**如何使用：** 调用 `setInterval(...)` 修改 `interval`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setInterval(std::chrono::milliseconds value)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示超时区间以毫秒为单位。
该属性的默认值为0。超时区间为0的`QTimer`，一旦窗口系统事件队列中的所有事件都处理完毕，就会超时。
注意：用零计时器让事件循环保持忙碌，必然会引发问题和UI的高度不稳定行为。
设置运行计时器的间隔会改变该间隔，`stop()`然后`start()`计时器，并获得新的`id()`。如果计时器未运行，仅会更改该间隔。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。

**如何使用：** 调用 `setInterval(...)` 修改 `interval`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSingleShot(bool singleShot)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性适用于计时器是否为单次计时器。
单发计时器仅发射一次，非单发计时器每`interval`毫秒发射一次。
该房产的默认价值为`false`。

**如何使用：** 调用 `setSingleShot(...)` 修改 `singleShot`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTimerType(Qt::TimerType atype)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
控制计时器的准确性。
该房产的默认价值为`Qt::CoarseTimer`。

**如何使用：** 调用 `setTimerType(...)` 修改 `timerType`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `Qt::TimerType timerType() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
控制计时器的准确性。
该房产的默认价值为`Qt::CoarseTimer`。

**如何使用：** 调用 `timerType()` 读取当前值；它不会修改应用状态。

### `void singleShot(Duration interval, Functor &&functor)`

**作用与语义：**

这个静态函数在 `interval` 后调用 `functor`。
使用这个函数非常方便，因为你无需费心创建`timerEvent`或创建本地`QTimer`对象。
如果指定了`context`，则只有当`context`对象在区间发生前未被销毁时才调用`functor`。然后该函子将运行在`context`的线程上。上下文线程必须有一个运行中的Qt事件循环。
如果`functor`是`context`的成员函数，则该函数将在对象上被调用。
`interval`参数可以是`int`（被解释为毫秒计数）或隐式转换为纳秒的`std::chrono`类型。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。
注意：在6.8之前的Qt版本中，计时重载需要计时：毫秒，而非计时：：纳秒。编译器会自动帮你转换，但转换可能会溢出极大的毫秒数。
注意：该函数是重入函数。

### `void singleShot(Duration interval, const QObject *context, Functor &&functor)`

**作用与语义：**

该静态函数在给定时间区间后调用一个槽位。
使用这个函数非常方便，因为你无需费心创建`timerEvent`或创建本地`QTimer`对象。
`receiver`是接收对象，`member`是槽函数。时间区间在持续时间对象`nsec`中给出。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。
注意：在 6.8 之前的 Qt 版本中，这个函数的计算时间是 chrono：milliseconds，而不是 chrono：：nanoseconds。编译器会自动帮你转换，但转换可能会溢出非常长的毫秒数。
注意：该函数是重入函数。

### `void singleShot(Duration interval, Qt::TimerType timerType, const QObject *context, Functor &&functor)`

**作用与语义：**

该静态函数在给定时间区间后调用一个槽位。
使用这个函数非常方便，因为你无需费心创建`timerEvent`或创建本地`QTimer`对象。
`receiver`是接收对象，`member`是槽函数。时间间隔在持续时间对象`nsec`中给出。`timerType`影响计时器的准确性。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。
注意：在 6.8 之前的 Qt 版本中，这个函数的计算时间是 chrono：milliseconds，而不是 chrono：：nanoseconds。编译器会自动帮你转换，但转换可能会溢出非常长的毫秒数。
注意：该函数是重入函数。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

`isActive()`、`remainingTime()`、`singleShot` 和 `timerType` 共同描述定时器状态。零毫秒定时器适合把少量工作分批交还事件循环，不能用来替代后台线程。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

timeout 不能假定精确时间；超时槽不能阻塞；跨线程启动/停止是错误用法；singleShot 的 context 应覆盖回调使用的对象生命周期。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTimer` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
