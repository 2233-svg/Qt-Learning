# Qt QElapsedTimer 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QElapsedTimer>`  
> 所属模块：`Qt6::Core`  
> 直接基类：无  
> 定位：基于单调参考时钟快速测量经过时间和执行时间预算

`QElapsedTimer` 是秒表，不会产生事件或回调。它优先使用不受系统时间校准、时区和夏令时影响的单调时钟，适合性能测量、循环时间预算和超时判断。它的参考点通常没有日历含义，不能转换成“几点几分”。

## 1. CMake 与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QElapsedTimer>

QElapsedTimer timer;
timer.start();

doExpensiveWork();

qInfo() << "elapsed ms:" << timer.elapsed();
qInfo() << "elapsed ns:" << timer.nsecsElapsed();
```

默认构造的 timer 尚未开始，调用测量 API 前先 `start()` 或检查 `isValid()`。

## 2. 为什么不用 QDateTime 测耗时

系统墙上时钟可能因为以下原因跳变：

- 用户手动校时。
- NTP 同步。
- 时区或夏令时变化。
- 虚拟机时间调整。

单调时钟只沿一个方向前进，更适合计算 duration：

```text
QDateTime：回答“现在是何时”
QElapsedTimer：回答“过去了多久”
QDeadlineTimer：回答“离截止还有多久”
```

## 3. 启动、有效与失效

```cpp
QElapsedTimer timer;
Q_ASSERT(!timer.isValid());

timer.start();
Q_ASSERT(timer.isValid());

timer.invalidate();
Q_ASSERT(!timer.isValid());
```

对无效 timer 调用 elapsed、durationTo、msecsTo 等测量/比较函数，结果可能未定义。可用 invalid 状态表达“尚未开始”或“缓存时间不存在”。

## 4. 毫秒与纳秒测量

```cpp
qint64 milliseconds = timer.elapsed();
qint64 nanoseconds = timer.nsecsElapsed();
```

`nsecsElapsed()` 提供纳秒数值接口，但实际分辨率取决于平台时钟，不代表测量误差一定小于 1ns。微小代码段应多次迭代并扣除框架开销，而不是相信一次读数。

Qt 6.6 起可直接得到 chrono duration：

```cpp
QElapsedTimer::Duration duration = timer.durationElapsed();
auto us = std::chrono::duration_cast<std::chrono::microseconds>(duration);
```

## 5. `Duration` 与 `TimePoint`

```cpp
using Duration = QElapsedTimer::Duration;
using TimePoint = QElapsedTimer::TimePoint;
```

`TimePoint` 是：

```cpp
std::chrono::time_point<std::chrono::steady_clock, Duration>
```

Qt 6.6 起 QElapsedTimer 使用 `std::chrono::steady_clock`。优先使用类型化 duration，避免把裸 qint64 的单位弄错。

## 6. `restart()`

```cpp
const qint64 previousMilliseconds = timer.restart();
```

它返回自上次 start/restart 起经过的毫秒，并立刻把起点更新为现在：

```cpp
QElapsedTimer frameTimer;
frameTimer.start();

void renderFrame()
{
    const qint64 deltaMs = frameTimer.restart();
    updateAnimation(deltaMs);
}
```

对无效 timer 调用 restart 的结果和状态语义应避免依赖；需要时先检查有效性。

## 7. 时间预算 `hasExpired()`

```cpp
QElapsedTimer budget;
budget.start();

while (!budget.hasExpired(8) && hasMoreWork())
    processOneItem();
```

`hasExpired(timeoutMs)` 等价于 `elapsed() > timeoutMs`。注意是严格大于；边界要求非常精确时直接比较 duration。

负 timeout 被解释为无限期，因此始终返回 false：

```cpp
Q_ASSERT(!budget.hasExpired(-1));
```

chrono 写法：

```cpp
while (budget.durationElapsed() <= 8ms && hasMoreWork())
    processOneItem();
```

## 8. 比较两个 timer

```cpp
QElapsedTimer first;
first.start();

doSomething();

QElapsedTimer second;
second.start();

qint64 milliseconds = first.msecsTo(second);
qint64 seconds = first.secsTo(second);
QElapsedTimer::Duration precise = first.durationTo(second);
```

结果表示从 first 起点到 second 起点的有符号距离；参数更早时可为负。两个 timer 都必须有效，并使用同一参考时钟。在同一进程/机器的 QElapsedTimer 中该条件通常成立。

## 9. `msecsSinceReference()`

```cpp
qint64 referenceValue = timer.msecsSinceReference();
```

它返回 timer 起点相对于平台参考时钟的毫秒值。除 `SystemTime` 外，参考点通常是任意过去时刻，不是 Unix epoch。

严禁把该值当时间戳保存到磁盘或通过网络发送：

- 机器重启后参考点可能不同。
- 另一台机器的参考时钟无可比性。
- 它不能转换成用户可读日期。

同一机器、同一参考时钟的多个进程之间可在明确协议下比较，但还应检查 clock type。

## 10. `ClockType`

```cpp
enum QElapsedTimer::ClockType {
    SystemTime,
    MonotonicClock,
    TickCounter,
    MachAbsoluteTime,
    PerformanceCounter
};
```

- `SystemTime`：墙上时钟，非单调，旧/受限平台回退。
- `MonotonicClock`：Unix 常见单调时钟。
- `TickCounter`：保留的 tick 计数类别。
- `MachAbsoluteTime`：Apple Mach 绝对时间。
- `PerformanceCounter`：Windows performance counter。

```cpp
QElapsedTimer::ClockType type = QElapsedTimer::clockType();
bool monotonic = QElapsedTimer::isMonotonic();
```

Qt 6.6 起使用 `std::chrono::steady_clock`，`clockType()` 报告 `MonotonicClock`。枚举仍用于兼容和与非 Qt 时钟集成。

## 11. 限时批处理

```cpp
void Controller::processSlice()
{
    QElapsedTimer slice;
    slice.start();

    while (!m_queue.isEmpty() && !slice.hasExpired(5))
        process(m_queue.dequeue());

    if (!m_queue.isEmpty())
        QTimer::singleShot(0ms, this, &Controller::processSlice);
}
```

这种模式保证每轮大致只占用一个时间片，然后把控制权还给事件循环。单个 `process()` 若本身超过预算仍会超时；无法抢占普通 C++ 函数，应继续细分工作。

## 12. 性能基准的正确使用

```cpp
QElapsedTimer timer;
timer.start();

for (int i = 0; i < iterations; ++i)
    benchmarkTarget();

const double nsPerCall =
    double(timer.nsecsElapsed()) / iterations;
```

可靠基准还要：

- 预热缓存/JIT/资源。
- 避免编译器消除结果。
- 多轮测量并报告分布，而非单次值。
- 固定输入、构建类型和设备状态。
- 使用 Qt Test benchmark 工具处理统计。

QElapsedTimer 提供时钟读数，不自动构成科学基准环境。

## 13. 线程与并发

QElapsedTimer 是值类型，不依赖事件循环。不同线程各自使用独立实例没有问题。多个线程同时读写同一个实例仍是数据竞争，需要锁或明确所有权。

同一机器上相同参考时钟的 timer 可比较，但跨线程传递前确保实例不再被另一线程修改。

## 14. 系统休眠语义

平台单调时钟是否包含设备 suspend 时间取决于底层 steady clock 实现。业务若要求“即使机器休眠也算入许可证/会话超时”，应使用合适的绝对 UTC 时间和安全服务端时间策略，而不是假设 QElapsedTimer 在所有平台一致包含休眠。

## 15. 常见误区

### 把 msecsSinceReference 写入数据库

重启或换机器后不可比。持久时间用 `QDateTime::currentDateTimeUtc()`，耗时用 QElapsedTimer。

### nsecsElapsed 代表纳秒准确度

只代表返回单位。实际精度由平台决定。

### 无效 timer 也能安全比较

很多结果未定义。先 `isValid()`。

### restart 只读取不改变状态

它会更新起点。只读使用 `elapsed()`/`durationElapsed()`。

### 单调时钟可显示为日期

参考点是任意的，不能转换为日历时间。

## API 速查表
### 16.1 类型、时钟和有效状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员类型 | `enum QElapsedTimer::ClockType` | 描述当前平台使用的参考时钟类别。 | 学习时理解语义即可；Qt 6.6 起通常基于 `std::chrono::steady_clock`。 |
| 枚举值 | `SystemTime` | 表示墙上系统时间。 | 非单调，可能受校时影响；现代平台通常不应依赖它测耗时。 |
| 枚举值 | `MonotonicClock` | 表示 Unix 等平台常见单调时钟。 | 适合 duration 测量，但参考点没有日历意义。 |
| 枚举值 | `TickCounter` | 历史 tick 计数类别。 | 已不再支持，保留用于兼容；新代码不要使用。 |
| 枚举值 | `MachAbsoluteTime` | Apple 平台 Mach 绝对时间类别。 | 平台相关，只在需要和非 Qt 时钟集成时关注。 |
| 枚举值 | `PerformanceCounter` | Windows performance counter 类别。 | 平台相关，适合高分辨率耗时测量。 |
| 类型别名 | `QElapsedTimer::Duration` | 表示 elapsed/duration API 使用的 chrono duration。 | Qt 6.11.1 中为 nanoseconds；优先用它减少裸整数单位误解。 |
| 类型别名 | `QElapsedTimer::TimePoint` | 表示 steady clock 的时间点类型。 | 参考点不对应日历时间，不能显示为“几点几分”。 |
| 构造 | `QElapsedTimer()` | 创建一个无效的秒表对象。 | 默认未开始；调用测量/比较前先 `start()` 或检查 `isValid()`。 |
| 时钟查询 | `clockType()` | 返回当前平台使用的参考时钟类型。 | 它是静态平台属性，适合诊断和跨进程协议确认。 |
| 单调性 | `isMonotonic()` | 判断当前参考时钟是否单调。 | 单调不等于包含休眠时间，也不等于可转换成 UTC。 |
| 有效性 | `isValid()` | 查询 timer 是否已经有有效起点。 | 无效 timer 参与测量或比较会得到不可依赖的结果。 |
| 有效性 | `invalidate()` | 把 timer 标记为无效。 | 用来表达“尚未开始/缓存不存在”；下次测量前必须重新 `start()`。 |

### 16.2 启动、读取和重置

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 启动 | `start()` | 把当前单调时钟读数记录为起点。 | 调用后 timer 变为有效；重复调用会覆盖旧起点。 |
| 读取 | `elapsed()` | 返回从起点到现在经过的毫秒数。 | 先确保 timer 有效；毫秒适合日志和粗粒度预算。 |
| 读取 | `nsecsElapsed()` | 返回从起点到现在经过的纳秒数。 | 返回单位是纳秒，不代表平台测量误差一定小于 1ns。 |
| 读取 | `durationElapsed()` | 返回从起点到现在经过的 chrono duration。 | Qt 6.6 起可用；适合和 chrono API 组合，避免手写单位换算。 |
| 重启 | `restart()` | 返回上个起点到现在的毫秒数，并把起点重置为现在。 | 它会改变 timer 状态；只想读取时用 `elapsed()` 或 `durationElapsed()`。 |
| 预算 | `hasExpired(qint64 timeout)` | 判断经过毫秒数是否已经超过指定预算。 | 语义是 `elapsed() > timeout`；负 timeout 表示永不过期。 |

### 16.3 timer 之间的距离和参考值

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 起点距离 | `msecsTo(const QElapsedTimer &other)` | 返回当前 timer 起点到 `other` 起点的毫秒距离。 | 两边都必须有效；`other` 更早时结果为负。 |
| 起点距离 | `secsTo(const QElapsedTimer &other)` | 返回两个起点之间的秒级距离。 | 精度较低，适合粗略判断，不适合微基准。 |
| 起点距离 | `durationTo(const QElapsedTimer &other)` | 返回两个起点之间的 chrono duration。 | Qt 6.6 起可用；更适合高精度或单位明确的计算。 |
| 参考值 | `msecsSinceReference()` | 返回起点相对于平台参考时钟的毫秒值。 | 不是 Unix timestamp；不要写入数据库、日志协议或跨机器传输后比较。 |
| 比较 | `operator<` 和相等/排序比较 | 比较两个 timer 起点的先后。 | 只比较起点，不比较已经 elapsed 的结果；双方应有效并处于同一参考时钟域。 |

### 16.4 使用边界和取舍

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 性能测量 | `elapsed()` / `nsecsElapsed()` / `durationElapsed()` | 读取某段代码或一轮任务实际耗时。 | 单次微小读数容易受调度和缓存影响；正式基准应多轮测量或用 Qt Test benchmark。 |
| 时间片预算 | `hasExpired()` | 在循环中限制本轮最多工作多久。 | 普通 C++ 函数不可被抢占，单个任务过长仍会超过预算。 |
| 类型取舍 | 与 `QDeadlineTimer` 对比 | `QElapsedTimer` 负责测过去多久，`QDeadlineTimer` 负责表达还剩多久。 | 多层等待共享总超时时，入口创建 `QDeadlineTimer` 更自然。 |
| 类型取舍 | 与 `QTimer` 对比 | `QElapsedTimer` 不会回调，`QTimer` 会通过事件循环发 `timeout()`。 | 要调度未来工作用 timer 类；要测量真实经过时间用 elapsed timer。 |
| 线程语义 | 值类型读数对象 | 不依赖事件循环，可在任意线程创建和使用。 | 不同线程各自实例没问题；多个线程同时读写同一实例仍是数据竞争。 |

---

### 一句话总结

`QElapsedTimer` 用单调 steady clock 测“过去了多久”：开始后读取 elapsed/duration，restart 用于分段，hasExpired 用于时间预算；它的参考值只在同一时钟域有效，绝不能当作持久日期或跨机器时间戳。
