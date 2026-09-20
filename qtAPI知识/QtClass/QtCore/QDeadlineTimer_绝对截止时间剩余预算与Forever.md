# Qt QDeadlineTimer 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDeadlineTimer>`  
> 所属模块：`Qt6::Core`  
> 直接基类：无  
> 定位：保存单调时钟域中的绝对截止点，并统一传递一整条调用链的剩余时间预算

`QDeadlineTimer` 不是会回调的 timer，而是一个截止时间值。与每层函数都重新传“再等 100ms”相比，传递同一个 deadline 能保证重试、锁等待和 I/O 总共不超过原始预算。

## 1. CMake 与最小代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
QDeadlineTimer deadline(std::chrono::seconds(2));

while (!deadline.hasExpired()) {
    if (tryOneStep(deadline.remainingTime()))
        break;
}
```

`remainingTime()` 返回毫秒，可直接传给许多 `waitFor...` 或 `tryLock(timeout)` API。

## 2. 为什么传 deadline 而不是重复 duration

错误模式：

```cpp
connectWithTimeout(1000);
authenticateWithTimeout(1000);
readWithTimeout(1000); // 总耗时可能接近 3 秒
```

统一预算：

```cpp
QDeadlineTimer deadline(1000);
connectWithDeadline(deadline);
authenticateWithDeadline(deadline);
readWithDeadline(deadline);
```

每层只使用剩余时间，整个调用链共享同一个绝对终点。

## 3. 构造方式

默认构造或只传 timer type：

```cpp
QDeadlineTimer expired;
QDeadlineTimer preciseExpired(Qt::PreciseTimer);
```

相对毫秒和 chrono duration：

```cpp
QDeadlineTimer a(1500); // 1500ms 后到期
QDeadlineTimer b(1500ms, Qt::PreciseTimer);
```

chrono time_point：

```cpp
auto point = std::chrono::steady_clock::now() + 2s;
QDeadlineTimer c(point);
```

Qt 会把传入 clock 的 time point 转换到内部参考时钟。优先使用 steady clock；system_clock 在转换瞬间遇到校时仍可能带来语义差异。

## 4. Forever

```cpp
QDeadlineTimer deadline(QDeadlineTimer::Forever);

Q_ASSERT(deadline.isForever());
Q_ASSERT(!deadline.hasExpired());
Q_ASSERT(deadline.remainingTime() == -1);
```

`ForeverConstant` 只有 `Forever`。它对应 Qt 许多等待 API 中 `-1` 表示无限期的约定，但类型化写法更明确。

chrono 的 `duration::max()`/特殊最大 time point 也可转换为 never-expire 语义。

## 5. 查询到期和剩余时间

```cpp
bool expired = deadline.hasExpired();
bool forever = deadline.isForever();

qint64 ms = deadline.remainingTime();
qint64 ns = deadline.remainingTimeNSecs();
std::chrono::nanoseconds duration =
    deadline.remainingTimeAsDuration();
```

| 状态 | remainingTime | hasExpired |
| --- | ---: | --- |
| 尚有时间 | 正数 | false |
| 已到期 | 0 | true |
| Forever | -1 | false |

剩余时间函数把超期钳制为 0，不能直接告诉你“超了多久”。要计算超期量，读取绝对 deadline 并与 `current()` 比较。

## 6. 设置相对剩余时间

```cpp
deadline.setRemainingTime(500, Qt::CoarseTimer);
deadline.setRemainingTime(750us, Qt::PreciseTimer);
```

int 毫秒重载中：正值表示从现在起，0 表示已过期，负值表示 Forever。

chrono duration 重载不同：zero 或负 duration 表示已过期，只有 `duration::max()` 表示 Forever。不要混淆两个重载的负值语义。

精确秒/纳秒接口：

```cpp
deadline.setPreciseRemainingTime(1, 250'000'000,
                                 Qt::PreciseTimer);
```

表示从现在起 1.25 秒。秒为负会设为 Forever；全零表示已过期。

## 7. 设置绝对 deadline

参考时钟毫秒：

```cpp
deadline.setDeadline(referenceMilliseconds);
```

精确参考时钟点：

```cpp
deadline.setPreciseDeadline(secondsSinceReference,
                            nanosecondsPart,
                            Qt::PreciseTimer);
```

chrono time point：

```cpp
deadline.setDeadline(std::chrono::steady_clock::now() + 500ms);
```

绝对 qint64 数值属于 QElapsedTimer 的参考时钟域，不是 Unix 时间。不要写入数据库或跨机器传输。

## 8. 读取绝对截止点

```cpp
qint64 deadlineMs = deadline.deadline();
qint64 deadlineNs = deadline.deadlineNSecs();
```

过期时返回过去的参考点；Forever 或无法表示时返回 `std::numeric_limits<qint64>::max()`。

计算超期纳秒：

```cpp
const qint64 overdue =
    QDeadlineTimer::current().deadlineNSecs()
    - deadline.deadlineNSecs();
```

先排除 Forever/最大值并处理溢出，再做减法。

## 9. `current()` 与精度类型

```cpp
QDeadlineTimer now = QDeadlineTimer::current(Qt::PreciseTimer);
```

它表示当前参考时钟点，通常已经到期，可用于绝对时间计算。

```cpp
deadline.setTimerType(Qt::CoarseTimer);
Qt::TimerType type = deadline.timerType();
```

timer type 表示等待方可采用的精度/功耗偏好，不会安排任何回调。传给支持 QDeadlineTimer 的同步原语时，该信息可帮助底层选择等待策略。

## 10. 调整 deadline

毫秒调整：

```cpp
deadline += 100;
deadline -= 50;

QDeadlineTimer later = deadline + 250;
QDeadlineTimer earlier = deadline - 250;
```

纳秒调整：

```cpp
QDeadlineTimer shifted =
    QDeadlineTimer::addNSecs(deadline, 500'000);
```

这些操作移动绝对终点，不是从“现在”重新计时。Forever 加减有限时长仍应保持 Forever 语义。

## 11. 比较与交换

```cpp
if (first < second)
    qDebug() << "first expires earlier";

first.swap(second);
```

支持 `== != < <= > >=`。比较的是绝对截止关系，Forever 排在有限未来之后。只有处于可比较参考时钟语义的值才有业务意义。

## 12. chrono 赋值

duration 赋值表示从现在起：

```cpp
deadline = 2s;
```

time_point 赋值表示指定绝对时间点：

```cpp
deadline = std::chrono::steady_clock::now() + 2s;
```

两种写法外观相似但语义不同，接口命名和变量类型应清楚表达 remaining duration 还是 absolute deadline。

## 13. 等待循环示例

```cpp
bool acquireAll(QMutex &first, QMutex &second,
                QDeadlineTimer deadline)
{
    if (!first.tryLock(deadline.remainingTime()))
        return false;

    const auto unlockFirst = qScopeGuard([&] { first.unlock(); });

    if (!second.tryLock(deadline.remainingTime()))
        return false;

    second.unlock();
    return true;
}
```

第二次等待只获得第一次等待后的剩余预算。每次进入阻塞 API 前再次读取 remaining time。

## 14. 线程与序列化

QDeadlineTimer 是值类型，不依赖事件循环。不同线程使用各自副本安全；同一实例并发写仍需同步。

不要持久化 `deadline()`/`deadlineNSecs()`，也不要跨机器传输。要持久化业务截止时刻，保存 UTC `QDateTime`；恢复后再根据当前时刻构造新的单调 deadline。

## 15. 常见误区

- 把 QDeadlineTimer 当回调 timer：它不会发信号，调度用 QTimer/QChronoTimer。
- 每层重新用完整 timeout 构造 deadline：会重置预算，应传同一个值。
- 把 `deadline()` 当 Unix timestamp：它属于单调参考时钟。
- 忽略 int 与 chrono 重载的负 duration 差异。
- 认为 timer type 提供硬实时保证：它只是精度偏好。
- 用 remainingTime 计算超期量：到期后它固定返回 0。

## API 速查表
### 16.1 构造和无限期状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员类型 | `enum class ForeverConstant { Forever }` | 表示永不过期的特殊构造标签。 | 它是类型化常量，不是一个会触发等待或回调的对象。 |
| 成员常量 | `QDeadlineTimer::Forever` | 以 `QDeadlineTimer::Forever` 表示无限等待。 | `isForever()` 为 `true`，chrono 剩余时间为 `duration::max()`。 |
| 构造 | `QDeadlineTimer()` | 创建一个默认值对象。 | 默认值表示已到期/没有未来预算，不等于 Forever。 |
| 构造 | `QDeadlineTimer(Qt::TimerType type)` | 创建默认截止值并指定精度偏好。 | timer type 只影响后续等待策略，不会启动定时器。 |
| 构造 | `QDeadlineTimer(ForeverConstant, Qt::TimerType type = Qt::CoarseTimer)` | 创建永不过期的 deadline。 | 适合把无限等待明确传给支持 deadline 的同步 API。 |
| 构造 | `QDeadlineTimer(qint64 msecs, Qt::TimerType type = Qt::CoarseTimer)` | 从当前时刻起建立毫秒级相对截止时间。 | `msecs < 0` 表示 Forever，`0` 表示已到期；不要与 chrono duration 的规则混用。 |
| 构造 | `QDeadlineTimer(std::chrono::duration remaining, Qt::TimerType type = Qt::CoarseTimer)` | 用 chrono duration 建立从现在起的截止时间。 | `duration::max()` 表示 Forever；普通零或负 duration 表示已过期。 |
| 构造 | `QDeadlineTimer(std::chrono::time_point deadline, Qt::TimerType type = Qt::CoarseTimer)` | 用 chrono 绝对时间点建立 deadline。 | 优先使用单调的 `steady_clock`；绝对 deadline 不能直接当 Unix 时间保存。 |
| 生命周期 | `swap(QDeadlineTimer &other)` | 交换两个 deadline 值。 | 只交换值和 timer type，不涉及线程同步或外部资源。 |

### 16.2 到期、剩余时间和精度类型

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 到期查询 | `isForever()` | 判断当前 deadline 是否永不过期。 | Forever 不代表事件循环会一直运行，只是这个值不会因时间流逝而过期。 |
| 到期查询 | `hasExpired()` | 判断截止点是否已经到达。 | Forever 始终返回 `false`；默认构造值通常已经到期。 |
| 精度类型 | `timerType()` | 读取当前 timer type。 | 这是等待精度/功耗偏好，不是硬实时保证。 |
| 精度类型 | `setTimerType(Qt::TimerType type)` | 修改等待方使用的精度偏好。 | 不会改变绝对截止点，也不会产生回调。 |
| 剩余时间 | `remainingTime()` | 返回截至当前时刻的剩余毫秒数。 | 尚未到期返回正数，过期钳制为 `0`，Forever 返回 `-1`。 |
| 剩余时间 | `remainingTimeNSecs()` | 返回剩余纳秒数。 | 过期会钳制为 `0`；Forever 使用最大值语义，不能直接拿来做普通差值。 |
| 剩余时间 | `remainingTimeAsDuration()` | 以 `std::chrono::nanoseconds` 返回剩余时间。 | Forever 返回 `nanoseconds::max()`；过期返回零 duration。 |
| 相对设置 | `setRemainingTime(qint64 msecs, Qt::TimerType type = Qt::CoarseTimer)` | 从现在起重新设置毫秒级剩余预算。 | 正数建立未来 deadline，`0` 立即过期，负数表示 Forever。 |
| 相对设置 | `setRemainingTime(std::chrono::duration remaining, Qt::TimerType type = Qt::CoarseTimer)` | 用 chrono duration 重新设置剩余预算。 | `duration::max()` 表示 Forever；其他零或负 duration 表示过期。 |
| 精确相对设置 | `setPreciseRemainingTime(qint64 secs, qint64 nsecs = 0, Qt::TimerType type = Qt::CoarseTimer)` | 以秒和纳秒设置从现在起的相对截止时间。 | 秒为负时表示 Forever；纳秒进位和溢出要由调用方控制。 |

### 16.3 绝对 deadline 和当前参考点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 绝对读取 | `deadline()` | 返回参考时钟中的毫秒级绝对截止点。 | 这是单调参考时钟值，不是 Unix 时间戳，不能直接持久化或跨机器传输。 |
| 绝对读取 | `deadlineNSecs()` | 返回参考时钟中的纳秒级绝对截止点。 | Forever 使用最大值语义；与其他值相减前要排除特殊值和溢出。 |
| chrono 读取 | `deadline<Clock, Duration>()` | 把内部 deadline 转换成指定 chrono clock 的 time point。 | 不同 clock 的转换语义不同；计算时要保持 clock 域一致。 |
| 绝对设置 | `setDeadline(qint64 msecs, Qt::TimerType type = Qt::CoarseTimer)` | 直接设置参考时钟域中的毫秒级绝对截止点。 | 参数不是日历时间；通常来自同一参考时钟域的 deadline 值。 |
| 绝对设置 | `setDeadline(std::chrono::time_point deadline, Qt::TimerType type = Qt::CoarseTimer)` | 用 chrono 绝对时间点设置截止点。 | `steady_clock` 最适合表达等待预算；最大 time point 可表示 Forever。 |
| 精确绝对设置 | `setPreciseDeadline(qint64 secs, qint64 nsecs = 0, Qt::TimerType type = Qt::CoarseTimer)` | 以参考时钟的秒和纳秒设置绝对截止点。 | 秒和纳秒属于 Qt 单调参考时钟域，不是墙上时钟。 |
| 当前时间 | `current(Qt::TimerType type = Qt::CoarseTimer)` | 创建一个表示当前参考时钟点的 deadline。 | 返回值通常立即到期，主要用于绝对时间计算和统一参考点。 |

### 16.4 调整、运算和比较

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 纳秒调整 | `addNSecs(QDeadlineTimer deadline, qint64 nsecs)` | 返回把绝对截止点平移指定纳秒后的新值。 | 调整的是绝对终点，不是从现在重新开始计时；Forever 应保持无限期语义。 |
| 毫秒加法 | `operator+(QDeadlineTimer, qint64)` / `operator+(qint64, QDeadlineTimer)` | 返回向后平移指定毫秒的新 deadline。 | 结果是值对象，不修改原对象。 |
| 毫秒减法 | `operator-(QDeadlineTimer, qint64)` | 返回向前平移指定毫秒的新 deadline。 | 向前移动可能使 deadline 立即过期。 |
| deadline 差值 | `operator-(QDeadlineTimer, QDeadlineTimer)` | 返回两个 deadline 的毫秒差。 | 只有同一参考时钟域的值才有业务意义；注意特殊值和溢出。 |
| 原地加法 | `operator+=(qint64 msecs)` | 把当前 deadline 向后平移毫秒数。 | 会修改当前值；Forever 加有限时长仍保持 Forever。 |
| 原地减法 | `operator-=(qint64 msecs)` | 把当前 deadline 向前平移毫秒数。 | 可能把值移动到过去；不会改变 timer type。 |
| chrono 加法 | `operator+(QDeadlineTimer, std::chrono::duration)` | 按 chrono duration 平移并返回新值。 | duration 会转换为纳秒；极大值要注意溢出。 |
| chrono 原地加法 | `operator+=(QDeadlineTimer &, std::chrono::duration)` | 按 chrono duration 原地平移当前值。 | 只改变 deadline，不改变外部等待对象。 |
| 比较 | `==`、`!=`、`<`、`<=`、`>`、`>=` | 按绝对截止点比较两个值。 | Forever 排在有限未来之后；比较前确保参考时钟语义一致。 |

### 16.5 赋值和等待链路中的使用

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| chrono 赋值 | `operator=(std::chrono::time_point)` | 把当前对象设置为指定绝对 chrono 时间点。 | 和 duration 赋值外观相似但语义不同，变量命名应明确区分。 |
| chrono 赋值 | `operator=(std::chrono::duration)` | 把当前对象设置为从现在起的相对 duration。 | `duration::max()` 表示 Forever，负 duration 通常表示过期。 |
| 等待预算 | `remainingTime()` / `remainingTimeAsDuration()` | 在每次阻塞调用前读取尚未消费的预算。 | 不要在函数入口读取一次后反复复用旧值，否则后续等待可能超出总预算。 |
| 值语义 | `QDeadlineTimer` 的复制和按值传递 | 让同一个绝对终点沿调用链传递。 | 复制的是值，不是共享计时器；同一实例并发写仍需外部同步。 |

---

### 一句话总结

`QDeadlineTimer` 把“还能等多久”固定成单调时钟上的绝对终点：在入口创建一次并沿调用链传递，每层只消费剩余预算；它可表示 Forever，却不会主动回调，且绝对参考值不能持久化或跨机器使用。
