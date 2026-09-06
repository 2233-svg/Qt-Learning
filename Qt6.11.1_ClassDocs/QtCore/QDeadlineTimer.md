# QDeadlineTimer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Deadline定时器”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QDeadlineTimer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QDeadlineTimer>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum class ForeverConstant { Forever }`

### 公有函数

- `QDeadlineTimer()`
- `QDeadlineTimer(Qt::TimerType timerType)`
- `QDeadlineTimer(QDeadlineTimer::ForeverConstant, Qt::TimerType timerType = Qt::CoarseTimer)`
- `QDeadlineTimer(qint64 msecs, Qt::TimerType type = Qt::CoarseTimer)`
- `QDeadlineTimer(std::chrono::duration<Rep, Period> remaining, Qt::TimerType type = Qt::CoarseTimer)`
- `QDeadlineTimer(std::chrono::time_point<Clock, Duration> deadline, Qt::TimerType type = Qt::CoarseTimer)`
- `qint64 deadline() const`
- `qint64 deadlineNSecs() const`
- `bool hasExpired() const`
- `bool isForever() const`
- `qint64 remainingTime() const`
- `std::chrono::nanoseconds remainingTimeAsDuration() const`
- `qint64 remainingTimeNSecs() const`
- `void setDeadline(qint64 msecs, Qt::TimerType timerType = Qt::CoarseTimer)`
- `void setDeadline(std::chrono::time_point<Clock, Duration> deadline, Qt::TimerType type = Qt::CoarseTimer)`
- `void setPreciseDeadline(qint64 secs, qint64 nsecs = 0, Qt::TimerType timerType = Qt::CoarseTimer)`
- `void setPreciseRemainingTime(qint64 secs, qint64 nsecs = 0, Qt::TimerType timerType = Qt::CoarseTimer)`
- `void setRemainingTime(qint64 msecs, Qt::TimerType timerType = Qt::CoarseTimer)`
- `void setRemainingTime(std::chrono::duration<Rep, Period> remaining, Qt::TimerType type = Qt::CoarseTimer)`
- `void setTimerType(Qt::TimerType timerType)`
- `void swap(QDeadlineTimer &other)`
- `Qt::TimerType timerType() const`
- `QDeadlineTimer & operator+=(qint64 msecs)`
- `QDeadlineTimer & operator-=(qint64 msecs)`
- `QDeadlineTimer & operator=(std::chrono::duration<Rep, Period> remaining)`
- `QDeadlineTimer & operator=(std::chrono::time_point<Clock, Duration> deadline_)`

### 静态公有成员

- `QDeadlineTimer addNSecs(QDeadlineTimer dt, qint64 nsecs)`
- `QDeadlineTimer current(Qt::TimerType timerType = Qt::CoarseTimer)`

### 相关非成员函数

- `bool operator!=(const QDeadlineTimer &lhs, const QDeadlineTimer &rhs)`
- `QDeadlineTimer operator+(QDeadlineTimer dt, qint64 msecs)`
- `QDeadlineTimer operator+(qint64 msecs, QDeadlineTimer dt)`
- `QDeadlineTimer operator-(QDeadlineTimer dt, qint64 msecs)`
- `bool operator<(const QDeadlineTimer &lhs, const QDeadlineTimer &rhs)`
- `bool operator<=(const QDeadlineTimer &lhs, const QDeadlineTimer &rhs)`
- `bool operator==(const QDeadlineTimer &lhs, const QDeadlineTimer &rhs)`
- `bool operator>(const QDeadlineTimer &lhs, const QDeadlineTimer &rhs)`
- `bool operator>=(const QDeadlineTimer &lhs, const QDeadlineTimer &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit constexpr noexcept] QDeadlineTimer::QDeadlineTimer(Qt::TimerType timerType)`

**作用与语义：**

构造一个过期的`QDeadlineTimer`对象。对于该对象，`remainingTime()`返回0。如果`timerType`未被设置，则该对象将使用`coarse`定时器类型。
计时器类型 `timerType` 可以忽略，因为计时器已过期。同样，出于优化目的，该函数不会尝试获取当前时间，而是使用已知的过去值。因此，`deadline()` 可能返回意外值，该对象无法用于计算逾期时间。如果需要此功能，请使用 `QDeadlineTimer::current()`。

### `[constexpr noexcept] QDeadlineTimer::QDeadlineTimer(QDeadlineTimer::ForeverConstant, Qt::TimerType timerType = Qt::CoarseTimer)`

**作用与语义：**

构造一个过期的`QDeadlineTimer`对象。对于该对象，`remainingTime()`返回0。如果`timerType`未被设置，则该对象将使用`coarse`定时器类型。
计时器类型 `timerType` 可以忽略，因为计时器已过期。同样，出于优化目的，该函数不会尝试获取当前时间，而是使用已知的过去值。因此，`deadline()` 可能返回意外值，该对象无法用于计算逾期时间。如果需要此功能，请使用 `QDeadlineTimer::current()`。

### `[explicit noexcept] QDeadlineTimer::QDeadlineTimer(qint64 msecs, Qt::TimerType type = Qt::CoarseTimer)`

**作用与语义：**

用`ForeverConstant`创建的QDeadlineTimer对象永远不会过期。对于此类对象，`remainingTime()`返回-1，`deadline()`返回最大值，`isForever()`返回true。
计时器类型`timerType`可以忽略，因为计时器永远不会过期。

### `template <typename Rep, typename Period> QDeadlineTimer::QDeadlineTimer(std::chrono::duration<Rep, Period> remaining, Qt::TimerType type = Qt::CoarseTimer)`

**作用与语义：**

构造一个QDeadlineTimer对象，其到期时间为该对象创建之初起计时`msecs`毫秒，如果msecs为正。如果`msecs`为零，该QDeadlineTimer将被标记为过期，导致`remainingTime()`返回零，`deadline()`返回一个不确定的过去时间点。如果`msecs`为负，计时器将被设定为永不失效，`remainingTime()`返回-1，`deadline()`返回最大值。
QDeadlineTimer 对象将按照指定的计时器`type`构建。
为了优化，如果`msecs`为零，该函数可以跳过当前时间，而使用已知的过去值。如果发生这种情况，`deadline()`可能会返回一个意外值，该对象无法用于计算逾期时间。如果需要该功能，使用`QDeadlineTimer::current()`并添加时间。
注意：在第6.6个Qt之前，唯一导致计时器永不过期的数值是-1。

### `template <typename Clock, typename Duration = typename Clock::duration> QDeadlineTimer::QDeadlineTimer(std::chrono::time_point<Clock, Duration> deadline, Qt::TimerType type = Qt::CoarseTimer)`

**作用与语义：**

构建一个剩余时间为`remaining`的QDeadlineTimer对象。如果`remaining`为零或负数，该QDeadlineTimer对象将被标记为过期;如果`remaining`等于`duration::max()`，则该对象将被设置为永不过期。
QDeadlineTimer 对象将按照指定的计时器`type`构建。
该构造器可与C 14用户定义的时间文字一起使用，例如：
为了优化，如果`remaining`为零或负数，该函数可能会跳过当前时间，而使用已知的过去值。如果发生这种情况，`deadline()`可能会返回一个意外值，该对象无法用于计算逾期时间。如果需要该功能，使用`QDeadlineTimer::current()`并添加时间。

**官方示例：**

```cpp
     using namespace std::chrono_literals;
     QDeadlineTimer deadline(250ms);
```

### `[static noexcept] QDeadlineTimer QDeadlineTimer::addNSecs(QDeadlineTimer dt, qint64 nsecs)`

**作用与语义：**

返回一个`QDeadlineTimer`对象，其截止时间比`dt`的截止时间延长`nsecs`纳秒。如果`dt`设置为永不过期，该函数返回的`QDeadlineTimer`也不会过期。
注意：如果`dt`被创建为已过期，其截止日期不确定，增加一段时间可能会使其恢复正常，也可能不会。

### `[static noexcept] QDeadlineTimer QDeadlineTimer::current(Qt::TimerType timerType = Qt::CoarseTimer)`

**作用与语义：**

返回一个已过期但保证包含当前时间的`QDeadlineTimer`。由该函数创建的对象可以利用`deadline()`函数参与计时器逾期时间的计算。
`QDeadlineTimer`对象将按照指定的`timerType`构造。

### `[noexcept] qint64 QDeadlineTimer::deadline() const`

**作用与语义：**

返回存储在`QDeadlineTimer`对象中截止时间的绝对时间点，以毫秒为单位，与`QElapsedTimer::msecsSinceReference()`相同。如果该`QDeadlineTimer`已过期，该值将回到过去。
如果该`QDeadlineTimer`永不过期，该函数返回`std::numeric_limits<qint64>::max()`。
该函数可用于计算计时器逾期的时间，方法为减去`QDeadlineTimer::current()`或`QElapsedTimer::msecsSinceReference()`，如下例所示：
注意：创建为过期的计时器截止时间不确定，因此上述计算可能不适用。

**官方示例：**

```cpp
     qint64 realTimeLeft = deadline.deadline();
     if (realTimeLeft != (std::numeric_limits<qint64>::max)()) {
         realTimeLeft -= QDeadlineTimer::current().deadline();
         // or:
         //QElapsedTimer timer;
         //timer.start();
         //realTimeLeft -= timer.msecsSinceReference();
     }
```

### `[noexcept] qint64 QDeadlineTimer::deadlineNSecs() const`

**作用与语义：**

返回存储在`QDeadlineTimer`对象中截止时间的绝对时间点，以纳秒计算，与`QElapsedTimer::msecsSinceReference()`相同。如果该`QDeadlineTimer`已过期，该值将回到过去。
如果返回类型中无法容纳该函数，或者该函数返回该函数`QDeadlineTimer` `std::numeric_limits<qint64>::max()`，或者截止时间内的纳秒数永远不会过期。
该函数可用于通过减去`QDeadlineTimer::current()`来计算计时器逾期的时间，如下例所示：
注意：创建为过期的计时器截止时间不确定，因此上述计算可能不适用。

**官方示例：**

```cpp
     qint64 realTimeLeft = deadline.deadlineNSecs();
     if (realTimeLeft != std::numeric_limits<qint64>::max())
         realTimeLeft -= QDeadlineTimer::current().deadlineNSecs();
```

### `[noexcept] bool QDeadlineTimer::hasExpired() const`

**作用与语义：**

如果该`QDeadlineTimer`对象已过期，返回真;如果剩余时间，则返回假。对于已过期的对象，`remainingTime()`返回零，`deadline()`返回过去的时间点。
`QDeadlineTimer`用`ForeverConstant`创建的对象永远不会过期，这个函数对它们总是返回false。

### `[constexpr noexcept] bool QDeadlineTimer::isForever() const`

**作用与语义：**

如果该`QDeadlineTimer`对象永不失效，则返回真;否则返回假。对于永不失效的计时器，`remainingTime()`总是返回-1，`deadline()`返回最大值。

### `[noexcept] qint64 QDeadlineTimer::remainingTime() const`

**作用与语义：**

返回该`QDeadlineTimer`对象剩余时间（毫秒）。如果计时器已过期，该函数返回零，无法用该函数获得逾期时间（详见 `deadline()`）。如果计时器设置为永不过期，该函数返回 -1。
该函数适用于需要毫秒超时的Qt API，如`QMutex`、`QWaitCondition`、`QSemaphore`或`QReadWriteLock`中的多重`QIODevice` `waitFor`函数或定时锁函数。例如：

**官方示例：**

```cpp
     mutex.tryLock(deadline.remainingTime());
```

### `[noexcept] std::chrono::nanoseconds QDeadlineTimer::remainingTimeAsDuration() const`

**作用与语义：**

返回截止日前剩余时间。

### `[noexcept] qint64 QDeadlineTimer::remainingTimeNSecs() const`

**作用与语义：**

返回该`QDeadlineTimer`对象剩余时间，单位为纳秒。如果计时器已过期，该函数返回零，无法通过该函数获得逾期时间。如果定时器设置为永不过期，该函数返回-1。

### `[noexcept] void QDeadlineTimer::setDeadline(qint64 msecs, Qt::TimerType timerType = Qt::CoarseTimer)`

**作用与语义：**

将该`QDeadlineTimer`对象的截止时间设定为`msecs`绝对时间点，以自参考时钟起的毫秒计（与`QElapsedTimer::msecsSinceReference()`相同），定时器类型为`timerType`。如果该值是过去的，该`QDeadlineTimer`将被标记为过期。
如果`msecs` `std::numeric_limits<qint64>::max()`或截止日期已超过未来可表示的时间点，该`QDeadlineTimer`将永远不会过期。

### `template <typename Clock, typename Duration = typename Clock::duration> void QDeadlineTimer::setDeadline(std::chrono::time_point<Clock, Duration> deadline, Qt::TimerType type = Qt::CoarseTimer)`

**作用与语义：**

将该`QDeadlineTimer`设置为`deadline`时间点标记的截止时间，将时钟源`Clock`转换为Qt内部时钟源（见`QElapsedTimer::clockType()`）。
如果`deadline`是过去，这个`QDeadlineTimer`对象被设置为过期;如果`deadline`等于`Duration::max()`，则该对象被设置为永不过期。
该`QDeadlineTimer`对象的定时器类型将设置为指定的`type`。

### `[noexcept] void QDeadlineTimer::setPreciseDeadline(qint64 secs, qint64 nsecs = 0, Qt::TimerType timerType = Qt::CoarseTimer)`

**作用与语义：**

将该`QDeadlineTimer`对象的截止时间设定为自参考时钟纪元起的`secs`秒和`nsecs`纳秒（与`QElapsedTimer::msecsSinceReference()`年相同），定时器类型为`timerType`。如果该值是过去的，该`QDeadlineTimer`将被标记为已过期。
如果`secs`或`nsecs` `std::numeric_limits<qint64>::max()`，该`QDeadlineTimer`将设置为永不过期。如果`nsecs`超过10亿纳秒（1秒），则`secs`会相应调整。

### `[noexcept] void QDeadlineTimer::setPreciseRemainingTime(qint64 secs, qint64 nsecs = 0, Qt::TimerType timerType = Qt::CoarseTimer)`

**作用与语义：**

如果`secs`值为正，则将该`QDeadlineTimer`对象剩余时间设置为从现在起`secs`秒加`nsecs`纳秒。如果`secs`为负，该`QDeadlineTimer`将被设定为永不过期（此行为不适用于`nsecs`）。如果两个参数均为零，该`QDeadlineTimer`将被标记为过期。
为了优化，如果`secs`和`nsecs`均为零，该函数可以跳过当前时间，而使用已知的过去值。如果发生这种情况，`deadline()`可能会返回意外值，该对象无法用于计算逾期时间。如果需要该功能，使用`QDeadlineTimer::current()`并添加时间。
该`QDeadlineTimer`对象的定时器类型将设置为指定的`timerType`。
注意：在第6.6题之前，唯一导致计时器永不过期的条件是`secs`为-1。

### `[noexcept] void QDeadlineTimer::setRemainingTime(qint64 msecs, Qt::TimerType timerType = Qt::CoarseTimer)`

**作用与语义：**

如果`msecs`值为正，则该`QDeadlineTimer`对象剩余时间为`msecs`毫秒。如果`msecs`为零，该`QDeadlineTimer`对象将被标记为过期，负值则设置为永不过期。
为了优化，如果`msecs`为零，该函数可以跳过当前时间，而使用已知的过去值。如果发生这种情况，`deadline()`可能会返回一个意外值，该对象无法用于计算逾期时间。如果需要该功能，使用`QDeadlineTimer::current()`并添加时间。
该`QDeadlineTimer`对象的计时器类型将设置为指定的`timerType`。
注意：在第6.6个Qt之前，唯一导致计时器永不过期的数值是-1。

### `template <typename Rep, typename Period> void QDeadlineTimer::setRemainingTime(std::chrono::duration<Rep, Period> remaining, Qt::TimerType type = Qt::CoarseTimer)`

**作用与语义：**

将该`QDeadlineTimer`对象剩余时间设置为`remaining`。如果`remaining`为零或负数，该`QDeadlineTimer`对象将被标记为过期;如果`remaining`等于`duration::max()`，则该对象将被设定为永不过期。
该`QDeadlineTimer`对象的定时器类型将设置为指定的`type`。
该函数可与C 14用户定义的时间文字一起使用，例如：

**官方示例：**

```cpp
     using namespace std::chrono_literals;
     deadline.setRemainingTime(250ms);
```

### `void QDeadlineTimer::setTimerType(Qt::TimerType timerType)`

**作用与语义：**

将该对象的计时器类型改为`timerType`。
每个可能的 `timerType` 值的行为依赖于操作系统。`Qt::PreciseTimer` 会使用 Qt 能找到的最精确定时器，分辨率为 1 毫秒或更高，而 `QDeadlineTimer` 则会尝试使用更粗的计时器来处理`Qt::CoarseTimer`和`Qt::VeryCoarseTimer`。

### `[noexcept] void QDeadlineTimer::swap(QDeadlineTimer &other)`

**作用与语义：**

把这个截止时间和`other`交换。这个操作非常快，从不失败。

### `[noexcept] Qt::TimerType QDeadlineTimer::timerType() const`

**作用与语义：**

返回该对象的计时器类型是激活的。

### `QDeadlineTimer &QDeadlineTimer::operator+=(qint64 msecs)`

**作用与语义：**

将该`QDeadlineTimer`对象延长`msecs`毫秒并返回自身。如果这个对象设置为永不过期，该函数则不做任何事。
要添加大于1毫秒的精度时间，请使用`addNSecs()`。

### `QDeadlineTimer &QDeadlineTimer::operator-=(qint64 msecs)`

**作用与语义：**

将该`QDeadlineTimer`对象缩短`msecs`毫秒，并返回自身。如果该对象设置为永不过期，该函数不做任何事。
要减去大于1毫秒的精度时间，使用`addNSecs()`。

### `template <typename Rep, typename Period> QDeadlineTimer &QDeadlineTimer::operator=(std::chrono::duration<Rep, Period> remaining)`

**作用与语义：**

把这个截止时间定时器设定为`remaining`时间。

### `template <typename Clock, typename Duration = typename Clock::duration> QDeadlineTimer &QDeadlineTimer::operator=(std::chrono::time_point<Clock, Duration> deadline_)`

**作用与语义：**

给`deadline_`分配到这个截止时间。

### `[noexcept] bool operator!=(const QDeadlineTimer &lhs, const QDeadlineTimer &rhs)`

**作用与语义：**

如果 `lhs` 的截止时间与 `rhs` 的截止时间不同，则返回 true，否则返回 false。用于创建两个截止日期的计时器类型被忽略。该函数等价于：
注意：不支持比较具有不同定时器的`QDeadlineTimer`对象，可能导致不可预测的行为。

**官方示例：**

```cpp
     return lhs.deadlineNSecs() != rhs.deadlineNSecs();
```

### `QDeadlineTimer operator+(QDeadlineTimer dt, qint64 msecs)`

**作用与语义：**

返回一个`QDeadlineTimer`对象，其截止日期比`dt`中存储的截止日期晚`msecs`。如果`dt`设置为永不过期，该函数返回的`QDeadlineTimer`也不会过期。
要添加大于1毫秒的精度时间，请使用`addNSecs()`。

### `QDeadlineTimer operator+(qint64 msecs, QDeadlineTimer dt)`

**作用与语义：**

返回一个`QDeadlineTimer`对象，其截止日期比`dt`中存储的截止日期晚`msecs`。如果`dt`设置为永不过期，该函数返回的`QDeadlineTimer`也不会过期。
要添加大于1毫秒的精度时间，请使用`addNSecs()`。

### `QDeadlineTimer operator-(QDeadlineTimer dt, qint64 msecs)`

**作用与语义：**

返回一个`QDeadlineTimer`对象，其截止日期在`dt`存储的截止日期之前`msecs`。如果`dt`设置为永不过期，该函数返回的`QDeadlineTimer`也不会过期。
要减去大于1毫秒的精度时间，使用`addNSecs()`。

### `[noexcept] bool operator<(const QDeadlineTimer &lhs, const QDeadlineTimer &rhs)`

**作用与语义：**

如果 `lhs` 的截止日期早于 `rhs` 的截止日期，则返回 true，否则返回 false。用于创建两个截止日期的定时器类型被忽略。该函数等价于：
注意：不支持比较具有不同定时器的`QDeadlineTimer`对象，可能导致不可预测的行为。

**官方示例：**

```cpp
     return lhs.deadlineNSecs() < rhs.deadlineNSecs();
```

### `[noexcept] bool operator<=(const QDeadlineTimer &lhs, const QDeadlineTimer &rhs)`

**作用与语义：**

如果`lhs`的截止时间早于或与`rhs`的截止时间相同，则返回为真;否则为假。用于创建两个截止日期的定时器类型被忽略。该函数等价于：
注意：不支持比较具有不同定时器的`QDeadlineTimer`对象，可能导致不可预测的行为。

**官方示例：**

```cpp
     return lhs.deadlineNSecs() <= rhs.deadlineNSecs();
```

### `[noexcept] bool operator==(const QDeadlineTimer &lhs, const QDeadlineTimer &rhs)`

**作用与语义：**

如果`lhs`的截止日期和`rhs`的截止时间相同，则返回真;否则返回假。用于创建两个截止时间的定时器类型被忽略。该函数等价于：
注意：不支持比较具有不同定时器的`QDeadlineTimer`对象，可能导致不可预测的行为。

**官方示例：**

```cpp
     return lhs.deadlineNSecs() == rhs.deadlineNSecs();
```

### `[noexcept] bool operator>(const QDeadlineTimer &lhs, const QDeadlineTimer &rhs)`

**作用与语义：**

如果`lhs`的截止日期晚于`rhs`的截止日期，则返回真，否则返回假。用于创建两个截止日期的定时器类型被忽略。该函数等价于：
注意：不支持比较具有不同定时器的`QDeadlineTimer`对象，可能导致不可预测的行为。

**官方示例：**

```cpp
     return lhs.deadlineNSecs() > rhs.deadlineNSecs();
```

### `[noexcept] bool operator>=(const QDeadlineTimer &lhs, const QDeadlineTimer &rhs)`

**作用与语义：**

如果`lhs`的截止日期晚于或与`rhs`的截止日期相同，则返回真;否则为假。用于创建两个截止日期的定时器类型被忽略。该函数等价于：
注意：不支持比较具有不同定时器的`QDeadlineTimer`对象，可能导致不可预测的行为。

**官方示例：**

```cpp
     return lhs.deadlineNSecs() >= rhs.deadlineNSecs();
```

### `enum class ForeverConstant { Forever }`

**作用与语义：**

- `QDeadlineTimer::ForeverConstant::Forever`：`0`;创建`QDeadlineTimer`时用于表明截止日期不应过期

### `QDeadlineTimer()`

**作用与语义：**

构建一个QDeadlineTimer对象，`deadline`时间点有截止时间，从时钟源`Clock`转换为Qt的内部时钟源（见`QElapsedTimer::clockType()`）。
如果`deadline`是过去的，这个QDeadlineTimer对象被设置为过期;如果`deadline`等于`Duration::max()`，则该对象被设置为永不过期。
QDeadlineTimer 对象将按照指定的计时器`type`构建。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QDeadlineTimer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
