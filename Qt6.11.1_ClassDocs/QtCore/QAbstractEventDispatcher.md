# QAbstractEventDispatcher

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QAbstractEventDispatcher` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QAbstractEventDispatcher` 是 Qt Core 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractEventDispatcher>`
- 继承自：QObject
- 直接派生类：QAbstractEventDispatcherV2

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct TimerInfoV2`
- `Duration`

### 公有函数

- `QAbstractEventDispatcher(QObject *parent = nullptr)`
- `virtual ~QAbstractEventDispatcher()`
- `bool filterNativeEvent(const QByteArray &eventType, void *message, qintptr *result)`
- `void installNativeEventFilter(QAbstractNativeEventFilter *filterObj)`
- `virtual void interrupt() = 0`
- `virtual bool processEvents(QEventLoop::ProcessEventsFlags flags) = 0`
- `virtual void registerSocketNotifier(QSocketNotifier *notifier) = 0`
- `(since 6.8) void registerTimer(Qt::TimerId timerId, QAbstractEventDispatcher::Duration interval, Qt::TimerType timerType, QObject *object)`
- `virtual void registerTimer(int timerId, qint64 interval, Qt::TimerType timerType, QObject *object) = 0`
- `(since 6.8) Qt::TimerId registerTimer(QAbstractEventDispatcher::Duration interval, Qt::TimerType timerType, QObject *object)`
- `virtual QList<QAbstractEventDispatcher::TimerInfo> registeredTimers(QObject *object) const = 0`
- `virtual int remainingTime(int timerId) = 0`
- `QAbstractEventDispatcher::Duration remainingTime(Qt::TimerId timerId) const`
- `void removeNativeEventFilter(QAbstractNativeEventFilter *filter)`
- `(since 6.8) QList<QAbstractEventDispatcher::TimerInfoV2> timersForObject(QObject *object) const`
- `virtual void unregisterSocketNotifier(QSocketNotifier *notifier) = 0`
- `(since 6.8) bool unregisterTimer(Qt::TimerId timerId)`
- `virtual bool unregisterTimer(int timerId) = 0`
- `virtual bool unregisterTimers(QObject *object) = 0`
- `virtual void wakeUp() = 0`

### 信号

- `void aboutToBlock()`
- `void awake()`

### 静态公有成员

- `QAbstractEventDispatcher * instance(QThread *thread = nullptr)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QAbstractEventDispatcher::Duration`

**作用与语义：**

这是该类API中使用的`std::chrono::duration`类型。该类型存在的目的是促进向更高或更低粒度的可能过渡。
在所有现有站台中，它都被`nanoseconds`。

### `[explicit] QAbstractEventDispatcher::QAbstractEventDispatcher(QObject *parent = nullptr)`

**作用与语义：**

用给定的`parent`构建一个新的事件调度器。

### `[virtual noexcept] QAbstractEventDispatcher::~QAbstractEventDispatcher()`

**作用与语义：**

摧毁事件调度器。

### `[signal] void QAbstractEventDispatcher::aboutToBlock()`

**作用与语义：**

该信号在事件循环调用可能阻塞的函数之前发出。

### `[signal] void QAbstractEventDispatcher::awake()`

**作用与语义：**

该信号是在事件循环返回后，可能被阻挡的函数返回。

### `bool QAbstractEventDispatcher::filterNativeEvent(const QByteArray &eventType, void *message, qintptr *result)`

**作用与语义：**

通过`installNativeEventFilter()`设置的事件过滤器发送`message`。该函数在事件过滤器返回 `true` 时返回 `true`，否则返回 false 表示事件处理应继续。
`QAbstractEventDispatcher`的子类必须对系统收到的所有消息调用该函数，以确保与应用中可能使用的扩展兼容。事件`eventType`的类型特定于运行时选择的平台插件，可用于将消息投射到正确的类型。`result`指针仅在Windows上使用，对应于LRESULT指针。
请注意，`message`类型取决于平台。详情请参见 `QAbstractNativeEventFilter`。

### `void QAbstractEventDispatcher::installNativeEventFilter(QAbstractNativeEventFilter *filterObj)`

**作用与语义：**

安装一个事件过滤器`filterObj`，涵盖应用程序接收的所有本地事件。
事件过滤器 `filterObj` 通过其 `nativeEventFilter()` 函数接收事件，调用所有线程接收的所有事件。
如果事件需要被过滤（在此情况下是停止），`nativeEventFilter()`函数应返回true。它应返回false以允许正常的Qt处理继续：本地事件随后可以转换为`QEvent`，并由标准的Qt过滤`event`处理，例如`QObject::installEventFilter()`。
如果安装了多个事件过滤器，最后安装的过滤器会先被激活。
注意：这里的过滤函数集接收本地消息，即 MSG 或 XEvent 结构。
为了最大化便携性，你应该尽量使用`QEvent`物品和`QObject::installEventFilter()`。

### `[static] QAbstractEventDispatcher *QAbstractEventDispatcher::instance(QThread *thread = nullptr)`

**作用与语义：**

返回指定 `thread` 的事件调度器对象的指针。如果 `thread` `nullptr`，则使用当前线程。如果指定线程不存在事件调度器，该函数返回 `nullptr`。
注意：如果 Qt 是在不支持线程的情况下构建的，`thread` 论点将被忽略。

### `[pure virtual] void QAbstractEventDispatcher::interrupt()`

**作用与语义：**

中断事件调度。事件调度员会尽快从 `processEvents()` 返回。

### `[pure virtual] bool QAbstractEventDispatcher::processEvents(QEventLoop::ProcessEventsFlags flags)`

**作用与语义：**

处理与`flags`匹配的待处理事件，直到没有更多事件可处理。如果事件被处理，返回`true`;否则返回`false`。
这个函数尤其适用于运行时间较长的操作，并且希望通过 `QEventLoop::ExcludeUserInputEvents` 标志显示其进度而不允许用户输入。
如果`QEventLoop::WaitForMoreEvents`标志设置为`flags`，该函数的行为如下：
- 如果事件可用，处理后该函数返回。
- 如果没有可用的事件，该函数会等待更多事件可用，并在处理新事件后返回。
如果`flags`中未设置`QEventLoop::WaitForMoreEvents`标志且无事件可用，该函数将立即返回。
注意：该函数不会连续处理事件;在处理完所有可用事件后返回。

### `[pure virtual] void QAbstractEventDispatcher::registerSocketNotifier(QSocketNotifier *notifier)`

**作用与语义：**

寄存器`notifier`事件循环。子类必须实现此方法，将套接字通知符与另一个事件循环绑定。

### `[since 6.8] void QAbstractEventDispatcher::registerTimer(Qt::TimerId timerId, QAbstractEventDispatcher::Duration interval, Qt::TimerType timerType, QObject *object)`

**作用与语义：**

注册一个定时器，包含指定`timerId`、`interval`和`timerType`，针对给定`object`。

### `[pure virtual] void QAbstractEventDispatcher::registerTimer(int timerId, qint64 interval, Qt::TimerType timerType, QObject *object)`

**作用与语义：**

注册一个定时器，包含指定`timerId`、`interval`和`timerType`，针对给定`object`。

### `[since 6.8] Qt::TimerId QAbstractEventDispatcher::registerTimer(QAbstractEventDispatcher::Duration interval, Qt::TimerType timerType, QObject *object)`

**作用与语义：**

注册指定定时器，`interval`和`timerType`对应给定`object`，并返回计时器ID。

### `[pure virtual] QList<QAbstractEventDispatcher::TimerInfo> QAbstractEventDispatcher::registeredTimers(QObject *object) const`

**作用与语义：**

返回`object`注册计时器的列表。TimerInfo结构体有`timerId`、`interval`和`timerType`成员。

### `[pure virtual] int QAbstractEventDispatcher::remainingTime(int timerId)`

**作用与语义：**

返回剩余时间（以毫秒计），并返回给定`timerId`。如果计时器不活跃，返回的值为-1。如果计时器逾期，返回的值为0。

### `QAbstractEventDispatcher::Duration QAbstractEventDispatcher::remainingTime(Qt::TimerId timerId) const`

**作用与语义：**

返回计时器剩余时间，并返回给定`timerId`。如果计时器处于非激活状态，返回的值为负数。如果计时器逾期，返回的值为0。

### `void QAbstractEventDispatcher::removeNativeEventFilter(QAbstractNativeEventFilter *filter)`

**作用与语义：**

移除该对象中的事件过滤器`filter`。如果未安装此类事件过滤器，请求将被忽略。
当该对象被销毁时，所有针对该对象的事件过滤器都会自动移除。
即使在激活事件过滤器时（即在`nativeEventFilter()`函数内），移除事件过滤器始终是安全的。

### `[since 6.8] QList<QAbstractEventDispatcher::TimerInfoV2> QAbstractEventDispatcher::timersForObject(QObject *object) const`

**作用与语义：**

返回`object`注册计时器的列表。`TimerInfoV2`结构体有`timerId`、`interval`和`timerType`成员。

### `[pure virtual] void QAbstractEventDispatcher::unregisterSocketNotifier(QSocketNotifier *notifier)`

**作用与语义：**

从事件调度器中卸载`notifier`。子类必须重新实现该方法，将套接字通知符绑定到另一个事件循环中。重实现必须调用基础实现。

### `[since 6.8] bool QAbstractEventDispatcher::unregisterTimer(Qt::TimerId timerId)`

**作用与语义：**

取消对定时器的注册，并用给定的 `timerId`。如果成功，返回 `true`;否则返回 `false`。

### `[pure virtual] bool QAbstractEventDispatcher::unregisterTimer(int timerId)`

**作用与语义：**

取消对定时器的注册，并用给定的 `timerId`。如果成功，返回 `true`;否则返回 `false`。

### `[pure virtual] bool QAbstractEventDispatcher::unregisterTimers(QObject *object)`

**作用与语义：**

取消注册与给定`object`相关的所有计时器。如果所有计时器都被成功移除，返回`true`;否则返回`false`。

### `[pure virtual] void QAbstractEventDispatcher::wakeUp()`

**作用与语义：**

唤醒事件循环。
注意：该功能是线程安全的。

### `struct TimerInfoV2`

**作用与语义：**

该结构表示关于计时器的信息：`timerId`、`interval`和`timerType`。

### `Duration`

**作用与语义：**

这是该类API中使用的`std::chrono::duration`类型。该类型存在的目的是促进向更高或更低粒度的可能过渡。
在所有现有站台中，它都被`nanoseconds`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractEventDispatcher` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
