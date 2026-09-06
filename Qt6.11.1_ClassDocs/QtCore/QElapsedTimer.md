# QElapsedTimer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Elapsed定时器”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QElapsedTimer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QElapsedTimer>`
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

- `enum ClockType { SystemTime, MonotonicClock, TickCounter, MachAbsoluteTime, PerformanceCounter }`
- `Duration`
- `TimePoint`

### 公有函数

- `QElapsedTimer()`
- `(since 6.6) QElapsedTimer::Duration durationElapsed() const`
- `(since 6.6) QElapsedTimer::Duration durationTo(const QElapsedTimer &other) const`
- `qint64 elapsed() const`
- `bool hasExpired(qint64 timeout) const`
- `void invalidate()`
- `bool isValid() const`
- `qint64 msecsSinceReference() const`
- `qint64 msecsTo(const QElapsedTimer &other) const`
- `qint64 nsecsElapsed() const`
- `qint64 restart()`
- `qint64 secsTo(const QElapsedTimer &other) const`
- `void start()`

### 静态公有成员

- `QElapsedTimer::ClockType clockType()`
- `bool isMonotonic()`

### 相关非成员函数

- `bool operator!=(const QElapsedTimer &lhs, const QElapsedTimer &rhs)`
- `bool operator<(const QElapsedTimer &lhs, const QElapsedTimer &rhs)`
- `bool operator==(const QElapsedTimer &lhs, const QElapsedTimer &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QElapsedTimer::ClockType`

**作用与语义：**

这个枚举包含了`QElapsedTimer`可能使用的不同时钟类型。
`QElapsedTimer`在特定机器中始终使用相同的时钟类型，因此该值在程序生命周期内不会变化。此设置旨在`QElapsedTimer`可用于其他非Qt实现，以确保使用相同的参考时钟。
- `QElapsedTimer::SystemTime`：`0`;人类可读的系统时间。该时钟并非单调。
- `QElapsedTimer::MonotonicClock`：`1`;系统的单调时钟，通常见于Unix系统中。该时钟是单调的。
- `QElapsedTimer::TickCounter`：`2`;不再使用。
- `QElapsedTimer::MachAbsoluteTime`：`3`;Mach 内核的绝对时间（macOS 和 iOS）。该时钟为单调。
- `QElapsedTimer::PerformanceCounter`：`4`;Windows提供的性能计数器。该时钟为单调。
系统时间时钟纯粹是实时时间，自1970年1月1日0：00 UTC起以毫秒为单位表示。它等价于C和POSIX `time`函数返回的数值，加上毫秒数。这种时钟类型目前仅用于不支持单调时钟的Unix系统（见下文）。
这是`QElapsedTimer`唯一能使用的非单调钟。
这是系统的单调时钟，以毫秒表示，自过去任意点起计算。该时钟类型用于支持 POSIX 单调时钟（`_POSIX_MONOTONIC_CLOCK`）的 Unix 系统。
该时钟类型基于马赫内核（如macOS上的核）所提供的绝对时间。该时钟类型与单调时钟分开呈现，因为macOS和iOS也是Unix系统，可能支持与马赫绝对时间不同的POSIX单调时钟。
这个钟是单调的。
该时钟利用Windows功能`QueryPerformanceCounter`和 `QueryPerformanceFrequency`访问系统的性能计数器。
这个钟是单调的。

### `[alias] QElapsedTimer::Duration`

**作用与语义：**

`std::chrono::nanoseconds`的同义词。

### `[alias] QElapsedTimer::TimePoint`

**作用与语义：**

`std::chrono::time_point<std::chrono::steady_clock, Duration>`的同义词。

### `[constexpr noexcept] QElapsedTimer::QElapsedTimer()`

**作用与语义：**

构造一个无效的QElapsed计时器。计时器一旦开始即有效。

### `[static noexcept] QElapsedTimer::ClockType QElapsedTimer::clockType()`

**作用与语义：**

返回该`QElapsedTimer`实现所使用的时钟类型。
自Qt 6.6起，`QElapsedTimer`使用`std::chrono::steady_clock`，因此时钟类型始终为`MonotonicClock`。

### `[noexcept, since 6.6] QElapsedTimer::Duration QElapsedTimer::durationElapsed() const`

**作用与语义：**

返回`std::chrono::nanoseconds`，显示自上次`QElapsedTimer`开始以来的时间。
在无效`QElapsedTimer`调用该函数会导致行为未定义。
在不支持纳秒分辨率的平台上，返回的数值将是可用的最佳估计值。

### `[noexcept, since 6.6] QElapsedTimer::Duration QElapsedTimer::durationTo(const QElapsedTimer &other) const`

**作用与语义：**

返回该`QElapsedTimer`与`other`之间的时间差，作为`std::chrono::nanoseconds`返回。如果`other`是在该对象之前开始的，返回的值为负。如果是较晚开始的，返回值为正。
如果该对象或`other`被失效，返回值未定义。

### `[noexcept] qint64 QElapsedTimer::elapsed() const`

**作用与语义：**

返回自上次启动`QElapsedTimer`以来的毫秒数。
在无效`QElapsedTimer`上调用该函数会导致行为未定义。

### `[noexcept] bool QElapsedTimer::hasExpired(qint64 timeout) const`

**作用与语义：**

如果 `elapsed()` 超过给定的 `timeout`，则返回 `true`，否则返回 `false`。负的 `timeout` 被解释为无限，因此在这种情况下返回 `false`。否则，这相当于 `elapsed() > timeout`。您可以通过将 `durationElapsed()` 与持续时间超时进行比较，对持续时间做同样的操作。

### `[noexcept] void QElapsedTimer::invalidate()`

**作用与语义：**

标记该`QElapsedTimer`对象为无效。
无效对象可以用`isValid()`检查。由于无效数据未定义，计时器的计算会经过，且可能产生奇怪的结果。

### `[static noexcept] bool QElapsedTimer::isMonotonic()`

**作用与语义：**

如果这是单调时钟，回`true`，否则为假。请参阅不同时钟类型的信息，了解哪些是单调的。
自Qt 6.6起，`QElapsedTimer`使用`std::chrono::steady_clock`，因此该函数现在总是返回真。

### `[noexcept] bool QElapsedTimer::isValid() const`

**作用与语义：**

如果计时器从未启动或被调用 `invalidate()` 作废，则返回 `false`。

### `[noexcept] qint64 QElapsedTimer::msecsSinceReference() const`

**作用与语义：**

返回该`QElapsedTimer`对象上次启动与其参考时钟开始之间的毫秒数。
该数字通常对除`QElapsedTimer::SystemTime`钟外的所有时钟都任意。对于该时钟类型，该数字是自1970年1月1日0：00 UTC以来的毫秒数（即Unix时间以毫秒表示）。
在Linux、Windows和苹果平台上，这个数值通常是自系统启动以来的时间，尽管通常不包括系统处于睡眠状态的时间。

### `[noexcept] qint64 QElapsedTimer::msecsTo(const QElapsedTimer &other) const`

**作用与语义：**

返回该`QElapsedTimer`与`other`之间的毫秒数。如果`other`在该对象之前启动，返回的值为负。如果是较晚开始，返回的值为正。
如果该对象或`other`被失效，返回值未定义。

### `[noexcept] qint64 QElapsedTimer::nsecsElapsed() const`

**作用与语义：**

返回自上次`QElapsedTimer`开始以来的纳秒数。
在无效`QElapsedTimer`调用该函数会导致行为未定义。
在不支持纳秒分辨率的平台上，返回的数值将是可用的最佳估计值。

### `[noexcept] qint64 QElapsedTimer::restart()`

**作用与语义：**

重启定时器，返回自上次开始以来经过的毫秒数。该功能相当于用`elapsed()`获取经过时间后再用`start()`重新启动计时器，但只需一次操作完成，避免了重复获取时钟值的需求。
在无效`QElapsedTimer`上调用该函数会导致行为未定义。
以下示例展示了如何利用该函数校准参数以适应慢速操作（例如迭代计数），使该操作至少耗时250毫秒：

**官方示例：**

```cpp
     QElapsedTimer timer;

     int count = 1;
     timer.start();
     do {
         count *= 2;
         slowOperation2(count);
     } while (timer.restart() < 250);

     return count;
```

### `[noexcept] qint64 QElapsedTimer::secsTo(const QElapsedTimer &other) const`

**作用与语义：**

返回该`QElapsedTimer`与`other`之间的秒数。如果`other`在该对象之前启动，返回的值为负。如果是较晚开始，返回值为正。
调用该函数在无效`QElapsedTimer`上或调用该函数会导致行为未定义。

### `[noexcept] void QElapsedTimer::start()`

**作用与语义：**

启动计时器。启动后，可以用`elapsed()`或 `msecsSinceReference()` 检查计时器值。
通常，定时器会在较长操作前启动，例如：
另外，启动计时器会让它再次有效。

**官方示例：**

```cpp
     QElapsedTimer timer;
     timer.start();

     slowOperation1();

     qDebug() << "The slow operation took" << timer.elapsed() << "milliseconds";
```

### `[noexcept] bool operator!=(const QElapsedTimer &lhs, const QElapsedTimer &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 包含不同的时间，则返回 `true`，否则返回 false。

### `[noexcept] bool operator<(const QElapsedTimer &lhs, const QElapsedTimer &rhs)`

**作用与语义：**

如果该`lhs`在`rhs`之前开始，返回`true`，否则为假。
如果两个参数中有一个无效，另一个无效，返回的值为未定义。然而，两个无效计时器相等，因此该函数将返回false。

### `[noexcept] bool operator==(const QElapsedTimer &lhs, const QElapsedTimer &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 包含相同的时间，则返回 `true`，否则返回 false。

### `Duration`

**作用与语义：**

`std::chrono::nanoseconds`的同义词。

### `TimePoint`

**作用与语义：**

`std::chrono::time_point<std::chrono::steady_clock, Duration>`的同义词。

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

`QElapsedTimer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
