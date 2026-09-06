# QChronoTimer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QChronoTimer` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QChronoTimer` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QChronoTimer>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

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

- `active : bool`
- `interval : std::chrono::nanoseconds`
- `remainingTime : std::chrono::nanoseconds`
- `singleShot : bool`
- `timerType : Qt::TimerType`

### 公有函数

- `QChronoTimer(QObject *parent = nullptr)`
- `QChronoTimer(std::chrono::nanoseconds nsec, QObject *parent = nullptr)`
- `virtual ~QChronoTimer() override`
- `QBindable<bool> bindableActive()`
- `QBindable<std::chrono::nanoseconds> bindableInterval()`
- `QBindable<bool> bindableSingleShot()`
- `QBindable<Qt::TimerType> bindableTimerType()`
- `QMetaObject::Connection callOnTimeout(const QObject *context, Functor &&slot, Qt::ConnectionType connectionType = Qt::AutoConnection)`
- `Qt::TimerId id() const`
- `std::chrono::nanoseconds interval() const`
- `bool isActive() const`
- `bool isSingleShot() const`
- `std::chrono::nanoseconds remainingTime() const`
- `void setInterval(std::chrono::nanoseconds nsec)`
- `void setSingleShot(bool singleShot)`
- `void setTimerType(Qt::TimerType atype)`
- `Qt::TimerType timerType() const`

### 公有槽函数

- `void start()`
- `void stop()`

### 信号

- `void timeout()`

### 重实现的保护函数

- `virtual void timerEvent(QTimerEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[bindable read-only] active : bool`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
如果计时器正在运行，这个布尔属性`true`;否则`false`。

**如何使用：** 调用 `active()` 读取当前值；它不会修改应用状态。

### `[bindable] interval : std::chrono::nanoseconds`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示超时区间。
该房产的默认值为`0ns`。
超时为`0ns`的`QChronoTimer`一旦窗口系统事件队列中的所有事件都处理完毕，就会超时。
设置运行计时器的间隔会改变该间隔，`stop()`然后`start()`计时器，并获得新的`id()`。如果计时器未运行，仅会更改间隔。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。

**如何使用：** 调用 `interval()` 读取当前值；它不会修改应用状态。

### `[read-only] remainingTime : std::chrono::nanoseconds`

**作用与语义：**

该属性表示剩余时间。
返回剩余的持续时间直到超时。
如果计时器处于非激活状态，返回的持续时间将为负。
如果计时器逾期，返回的时长将`0ns`。

**如何使用：** 调用 `remainingTime()` 读取当前值；它不会修改应用状态。

### `[bindable] singleShot : bool`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性适用于计时器是否为单次计时器。
单发计时器只发射一次，非单发计时器每隔`interval`发射一次。
该房产的默认价值为`false`。

**如何使用：** 调用 `singleShot()` 读取当前值；它不会修改应用状态。

### `[bindable] timerType : Qt::TimerType`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
控制计时器的准确性。
该房产的默认价值为`Qt::CoarseTimer`。

**如何使用：** 调用 `timerType()` 读取当前值；它不会修改应用状态。

### `[explicit] QChronoTimer::QChronoTimer(QObject *parent = nullptr)`

**作用与语义：**

利用默认区间 `0ns` 构造一个定时器，`parent`。

### `[explicit] QChronoTimer::QChronoTimer(std::chrono::nanoseconds nsec, QObject *parent = nullptr)`

**作用与语义：**

构造一个计时器，使用给定的`parent`，区间为`nsec`。

### `[override virtual noexcept] QChronoTimer::~QChronoTimer()`

**作用与语义：**

会破坏计时器。

### `template <typename Functor> QMetaObject::Connection QChronoTimer::callOnTimeout(const QObject *context, Functor &&slot, Qt::ConnectionType connectionType = Qt::AutoConnection)`

**作用与语义：**

从`timeout()`信号到`slot`建立连接，置于特定事件环`context`中，连接类型为`connectionType`，并返回连接的句柄。
此方法仅供方便使用。它等同于调用：

**官方示例：**

```cpp
 QObject::connect(timer, &QChronoTimer::timeout, context, slot, connectionType);
```

### `Qt::TimerId QChronoTimer::id() const`

**作用与语义：**

如果计时器正在运行，返回代表计时器的`Qt::TimerId`;否则返回`Qt::TimerId::Invalid`。

### `bool QChronoTimer::isActive() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
如果计时器正在运行，这个布尔属性`true`;否则`false`。

**如何使用：** 调用 `isActive()` 读取当前值；它不会修改应用状态。

### `[slot] void QChronoTimer::start()`

**作用与语义：**

在`interval`中指定超时时的情况下启动或重启计时器。
如果计时器已经在运行，它会被`stopped`并重新启动。这也会改变它的`id()`。
如果`singleShot`为真，计时器只会被激活一次。

### `[slot] void QChronoTimer::stop()`

**作用与语义：**

停止计时器。

### `[private signal] void QChronoTimer::timeout()`

**作用与语义：**

当计时器超时时，该信号会发出。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[override virtual protected] void QChronoTimer::timerEvent(QTimerEvent *e)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。
该事件处理程序可以被重新实现到子类中，以接收该对象的定时器事件。
`QChronoTimer` 提供了定时器功能的更高级接口，以及关于定时器的更通用信息。定时器事件通过 `event` 参数传递。

### `QBindable<bool> bindableActive()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
如果计时器正在运行，这个布尔属性`true`;否则`false`。

**如何使用：** 调用 `bindableActive()` 取得 `active` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<std::chrono::nanoseconds> bindableInterval()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示超时区间。
该房产的默认值为`0ns`。
超时为`0ns`的`QChronoTimer`一旦窗口系统事件队列中的所有事件都处理完毕，就会超时。
设置运行计时器的间隔会改变该间隔，`stop()`然后`start()`计时器，并获得新的`id()`。如果计时器未运行，仅会更改间隔。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。

**如何使用：** 调用 `bindableInterval()` 取得 `interval` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<bool> bindableSingleShot()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性适用于计时器是否为单次计时器。
单发计时器只发射一次，非单发计时器每隔`interval`发射一次。
该房产的默认价值为`false`。

**如何使用：** 调用 `bindableSingleShot()` 取得 `singleShot` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<Qt::TimerType> bindableTimerType()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
控制计时器的准确性。
该房产的默认价值为`Qt::CoarseTimer`。

**如何使用：** 调用 `bindableTimerType()` 取得 `timerType` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `std::chrono::nanoseconds interval() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示超时区间。
该房产的默认值为`0ns`。
超时为`0ns`的`QChronoTimer`一旦窗口系统事件队列中的所有事件都处理完毕，就会超时。
设置运行计时器的间隔会改变该间隔，`stop()`然后`start()`计时器，并获得新的`id()`。如果计时器未运行，仅会更改间隔。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。

**如何使用：** 调用 `interval()` 读取当前值；它不会修改应用状态。

### `bool isSingleShot() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性适用于计时器是否为单次计时器。
单发计时器只发射一次，非单发计时器每隔`interval`发射一次。
该房产的默认价值为`false`。

**如何使用：** 调用 `isSingleShot()` 读取当前值；它不会修改应用状态。

### `std::chrono::nanoseconds remainingTime() const`

**作用与语义：**

该属性表示剩余时间。
返回剩余的持续时间直到超时。
如果计时器处于非激活状态，返回的持续时间将为负。
如果计时器逾期，返回的时长将`0ns`。

**如何使用：** 调用 `remainingTime()` 读取当前值；它不会修改应用状态。

### `void setInterval(std::chrono::nanoseconds nsec)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示超时区间。
该房产的默认值为`0ns`。
超时为`0ns`的`QChronoTimer`一旦窗口系统事件队列中的所有事件都处理完毕，就会超时。
设置运行计时器的间隔会改变该间隔，`stop()`然后`start()`计时器，并获得新的`id()`。如果计时器未运行，仅会更改间隔。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。

**如何使用：** 调用 `setInterval(...)` 修改 `interval`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSingleShot(bool singleShot)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性适用于计时器是否为单次计时器。
单发计时器只发射一次，非单发计时器每隔`interval`发射一次。
该房产的默认价值为`false`。

**如何使用：** 调用 `setSingleShot(...)` 修改 `singleShot`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTimerType(Qt::TimerType atype)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
控制计时器的准确性。
该房产的默认价值为`Qt::CoarseTimer`。

**如何使用：** 调用 `setTimerType(...)` 修改 `timerType`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `Qt::TimerType timerType() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
控制计时器的准确性。
该房产的默认价值为`Qt::CoarseTimer`。

**如何使用：** 调用 `timerType()` 读取当前值；它不会修改应用状态。

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

`QChronoTimer` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
