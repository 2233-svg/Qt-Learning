# Qt QElapsedTimer 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QElapsedTimer>`  
> 所属模块：`Qt6::Core`  
> 定位：基于参考时钟的耗时测量与时间预算  
> 常见协作类：`QDeadlineTimer`、`QIODevice`、`QTime`

## 1. 它解决什么问题

`QElapsedTimer` 用来回答“从某个起点到现在经过了多久”或“两个计时起点相差多久”。它面向耗时测量，不面向日历时间和用户可读时间。

最常见的写法是：

```cpp
QElapsedTimer timer;
timer.start();

slowOperation();

qDebug() << "elapsed:" << timer.elapsed() << "ms";
```

与 `QTime` 不同，`QElapsedTimer` 尽量使用单调参考时钟。用户修改系统时间、时区切换或夏令时变化不会让一次耗时测量倒退或突然跳变。Qt 6.6 起它使用 `std::chrono::steady_clock`，所以 `isMonotonic()` 为 `true`，`clockType()` 为 `MonotonicClock`。

它适合：

- 测量函数、帧、批处理或 I/O 操作耗时；
- 在一个总超时预算内分配多个步骤的剩余时间；
- 在循环中执行工作直到时间片耗尽；
- 比较同一机器上由相同参考时钟产生的计时点。

它不适合：

- 显示当前日期和时间；
- 把“系统启动以来的毫秒数”保存到磁盘；
- 将计时点通过网络发送到另一台机器；
- 代替有明确未来截止时刻语义的 `QDeadlineTimer`。

## 2. 有效状态：构造后不能立即读取耗时

默认构造的对象是无效计时器，必须先 `start()`：

```cpp
QElapsedTimer timer;
Q_ASSERT(!timer.isValid());

timer.start();
Q_ASSERT(timer.isValid());
const qint64 ms = timer.elapsed();
```

以下函数在无效计时器上调用会产生未定义行为：

- `elapsed()`；
- `nsecsElapsed()`；
- `durationElapsed()`；
- `restart()`；
- `secsTo()`；
- `msecsTo()`；
- `durationTo()`。

`isValid()` 是读取前的边界检查。`invalidate()` 会把计时器重新置为无效状态；之后必须再次 `start()` 才能进行耗时计算。

## 3. 时间测量与时间预算

### 3.1 测量一个操作

```cpp
QElapsedTimer timer;
timer.start();
loadCache();

const qint64 elapsedMs = timer.elapsed();
qInfo() << "loadCache took" << elapsedMs << "ms";
```

`elapsed()` 返回自最近一次 `start()` 以来经过的毫秒数。`nsecsElapsed()` 和 Qt 6.6 起的 `durationElapsed()` 可以提供更细的接口单位，但底层平台没有纳秒硬件分辨率时，返回值只是可获得的最佳估计，不代表实际测量精度一定达到 1 纳秒。

### 3.2 在多个步骤之间传递剩余预算

```cpp
bool executeWithBudget(qint64 timeoutMs)
{
    QElapsedTimer timer;
    timer.start();

    operationA();

    const qint64 remaining = timeoutMs - timer.elapsed();
    if (remaining <= 0)
        return false;

    return operationB(remaining);
}
```

这种写法比为每个步骤分别读取墙上时钟更可靠。`elapsed()` 是单调时间差，不会因用户校准系统时间而突然增加或减少。

如果 API 本身接受 `QDeadlineTimer`，可以直接建立一个未来截止点并在多个调用间传递：

```cpp
#include <QDeadlineTimer>
#include <chrono>

using namespace std::chrono_literals;

QDeadlineTimer deadline(500ms);
operationA(deadline);
operationB(deadline);
```

选择原则是：只关心“已经过去多久”用 `QElapsedTimer`；要表达“不能晚于某个截止点”用 `QDeadlineTimer`。

### 3.3 用 `hasExpired()` 执行一个时间片

```cpp
void processFor(qint64 budgetMs)
{
    QElapsedTimer timer;
    timer.start();

    while (!timer.hasExpired(budgetMs))
        processOneItem();
}
```

负的 `timeout` 被解释为无限时间，因此 `hasExpired(negative)` 返回 `false`。这在“负值代表不设限”的接口中有用，但如果负数本来代表配置错误，业务代码应在传入前主动拒绝，而不要依赖这个特殊语义。

## 4. `restart()`：测量并重新开始的一次原子式操作

```cpp
QElapsedTimer timer;
timer.start();

while (timer.restart() < 250)
    calibrateNextBatch();
```

`restart()` 返回上一次 `start()` 以来经过的毫秒数，然后立即把新的起点设为当前时刻。它等价于先调用 `elapsed()` 再调用 `start()`，但只读取一次底层时钟，适合循环测量连续批次。

它要求计时器当前有效。对从未 `start()` 或已 `invalidate()` 的对象调用 `restart()` 是未定义行为。

## 5. 参考时钟与序列化边界

### 5.1 只能在同一参考时钟下比较

`msecsSinceReference()` 返回计时点距离参考时钟起点的毫秒数。这个值通常是任意的，除了 `SystemTime` 外不能直接当作 Unix 时间戳。Linux、Windows 和 Apple 平台上，它通常接近系统启动后的时间，但是否包含睡眠时间取决于平台时钟。

这个数可以在同一台机器的不同进程之间比较，前提是双方使用同一参考时钟；不应发送到另一台机器，也不应保存后跨重启使用：

```text
可以：同一机器、同一参考时钟、短时间内比较
不可以：写入文件后下次启动继续当时间戳
不可以：发送到另一台机器比较
```

如果要记录日志时间、协议时间或持久化时间点，应使用 `QDateTime`、Unix 时间戳或明确的协议时钟，而不是 `QElapsedTimer` 的内部参考值。

### 5.2 比较两个计时器的前提

```cpp
QElapsedTimer first;
QElapsedTimer second;
first.start();
second.start();

const qint64 gap = first.msecsTo(second);
```

`msecsTo()`、`secsTo()` 和 `durationTo()` 比较两个有效计时器的起点。若 `other` 比当前对象更早启动，结果为负；若更晚启动，结果为正。

只比较使用同一参考时钟的值。Qt 创建的 `QElapsedTimer` 在同一机器上会使用一致的时钟；如果要和其它平台 API 的时间值比较，先确认它们采用相同的时钟来源。

## 6. `std::chrono` API

Qt 6.6 增加了：

```cpp
using Duration = std::chrono::nanoseconds;
using TimePoint =
    std::chrono::time_point<std::chrono::steady_clock, Duration>;
```

`durationElapsed()` 返回 `Duration`，`durationTo()` 返回两个有效计时器之间的 duration。它们适合已经以 `std::chrono` 表达超时的代码，避免在毫秒整数与 duration 之间手工转换。

```cpp
using namespace std::chrono_literals;

QElapsedTimer timer;
timer.start();

if (timer.durationElapsed() >= 250ms)
    flushBatch();
```

即使返回类型是纳秒，平台实际分辨率仍可能更低；接口单位和测量精度是两个概念。

## 7. 常见误区

| 误区 | 为什么会出问题 | 应该怎样做 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造后直接调用 `elapsed()` | 默认对象无效，调用未定义 | 先 `start()` 或检查 `isValid()` | 无效不是“0 毫秒” |
| 用它显示当前时间 | 参考点通常不是人类可读的日期 | 用 `QDateTime` 或 Unix 时间 | `msecsSinceReference()` 不是通用时间戳 |
| 把值存盘或发到另一台机器 | 参考时钟起点和机器状态不可保证一致 | 传递明确的墙上时间或协议时间 | 同机跨进程才可能安全比较 |
| 以为纳秒 API 保证纳秒精度 | 平台可能没有纳秒分辨率 | 把它当作更细单位的最佳估计 | 不要据此设计硬实时逻辑 |
| 用负 timeout 表示“已经超时” | `hasExpired()` 将负值解释为无限时间 | 在业务层先校验配置 | 只有明确采用该约定时才传负值 |
| 用 `QElapsedTimer` 代替 deadline | 多次调用间容易重复换算剩余时间 | API 接受 deadline 时使用 `QDeadlineTimer` | 两者表达的抽象不同 |
| 比较无效计时器 | `secsTo()`、`msecsTo()` 等结果未定义 | 先确认两者都 `isValid()` | 两个无效值的相等比较也不能替代有效性检查 |

## API 速查表

### 8.1 类型与状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `ClockType` | 表示实现所使用的参考时钟类型 | 同一机器上 Qt 使用的类型在程序生命周期内保持一致 |
| 枚举值 | `SystemTime` | 人类可读的系统时间，非单调时钟 | 目前只在不支持单调时钟的平台上使用 |
| 枚举值 | `MonotonicClock` | 系统单调时钟 | Qt 6.6 起通常由 `std::chrono::steady_clock` 对应 |
| 枚举值 | `TickCounter` | 历史 tick counter 类型 | 文档标记为不再使用，不要依赖它设计新代码 |
| 枚举值 | `MachAbsoluteTime` | macOS/iOS 的 Mach 绝对时间 | 单调；仅用于描述底层时钟类型 |
| 枚举值 | `PerformanceCounter` | Windows 性能计数器 | 单调；仅用于描述底层时钟类型 |
| 类型别名 | `Duration` | `std::chrono::nanoseconds` 的别名 | 单位是 duration，不等于平台必有纳秒精度 |
| 类型别名 | `TimePoint` | 以 `Duration` 为周期的 steady clock time point | 不要当成日历时间或跨机器时间戳 |
| 构造 | `QElapsedTimer()` | 创建无效的计时器 | 只有 `start()` 后才可读取耗时 |
| 状态 | `bool isValid() const` | 判断计时器是否已启动且未失效 | 读取其它耗时 API 前可用于前置检查 |
| 状态 | `void invalidate()` | 将计时器标记为无效 | 无效后所有 elapsed/to 计算都必须停止，重新 `start()` 才能恢复 |

### 8.2 启动、读取与预算

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 启动 | `void start()` | 以当前参考时钟值作为新的起点，并使计时器有效 | 可重复调用，后一次会覆盖前一次起点 |
| 读取 | `qint64 elapsed() const` | 返回自最近一次启动以来经过的毫秒数 | 无效计时器调用是未定义行为 |
| 读取 | `qint64 nsecsElapsed() const` | 返回自最近一次启动以来经过的纳秒数估计 | 平台分辨率可能低于纳秒 |
| 读取 | `Duration durationElapsed() const` | 返回自最近一次启动以来的 chrono duration | Qt 6.6 起；无效计时器调用是未定义行为 |
| 预算 | `bool hasExpired(qint64 timeout) const` | 判断 `elapsed()` 是否大于给定毫秒 timeout | 负 timeout 表示无限时间并返回 false |
| 重启 | `qint64 restart()` | 返回旧起点的毫秒耗时并立即重新启动 | 必须先启动；无效状态调用未定义 |
| 参考值 | `qint64 msecsSinceReference() const` | 返回起点距实现参考时钟起点的毫秒数 | 不是通用时间戳，不要跨机器或跨重启持久化 |

### 8.3 两个计时点的比较

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 比较 | `qint64 msecsTo(const QElapsedTimer &other) const` | 返回当前计时点到 other 的毫秒差 | 两个对象都必须有效且使用同一参考时钟；方向决定正负 |
| 比较 | `qint64 secsTo(const QElapsedTimer &other) const` | 返回当前计时点到 other 的秒差 | 无效对象调用未定义；秒级结果会丢失更细粒度 |
| 比较 | `Duration durationTo(const QElapsedTimer &other) const` | 返回两个起点之间的 chrono duration | Qt 6.6 起；无效对象调用未定义 |
| 静态查询 | `static ClockType clockType()` | 返回当前 Qt 实现使用的时钟类型 | Qt 6.6 起通常返回 `MonotonicClock` |
| 静态查询 | `static bool isMonotonic()` | 判断实现是否使用单调时钟 | Qt 6.6 起总是 `true` |
| 比较运算 | `operator==(lhs, rhs)` | 判断两个计时器保存的时间点是否相同 | 先确保无效/有效状态符合业务语义 |
| 比较运算 | `operator!=(lhs, rhs)` | 判断两个计时器时间点不同 | 不等同于“其中一个已过期” |
| 比较运算 | `operator<(lhs, rhs)` | 判断 lhs 是否比 rhs 更早启动 | 一方有效、一方无效时结果未定义；两个无效值相等，因此返回 false |

## 9. 一个可复用的剩余时间辅助函数

```cpp
#include <QElapsedTimer>

qint64 remainingMilliseconds(QElapsedTimer &timer, qint64 budget)
{
    if (!timer.isValid())
        return budget;

    return qMax<qint64>(0, budget - timer.elapsed());
}
```

这个辅助函数仍然只是一次快照。调用者不能把返回的剩余毫秒数当成锁或线程同步保证；在下一次系统调用前，时间预算仍会继续消耗。

## 10. 一句话总结

`QElapsedTimer` 用单调参考时钟测量耗时和剩余预算；先 `start()`、再读取，区分 elapsed 与 deadline，且绝不要把参考时钟数当成人类时间、持久化时间戳或跨机器协议时间。
