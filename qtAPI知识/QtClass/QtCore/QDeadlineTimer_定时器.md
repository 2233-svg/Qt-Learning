# Qt QDeadlineTimer 深入笔记

> 适用版本：Qt 6.11  
> 头文件：`#include <QDeadlineTimer>`  
> 所属模块：`Qt6::Core`  
> 相关类：`QElapsedTimer`、`QTimer`、`QChronoTimer`、`QMutex`、`QWaitCondition`

## 1. 它解决什么问题：把“总共还允许等多久”传下去

`QDeadlineTimer` 表示一个未来的截止点，或者表示永不超时。它最适合限制一段由多步组成的同步操作的**总时间预算**。

假设读取响应要经过“等连接、等首包、等后续数据”三步，总预算是 5 秒。若每一步都单独写 `waitFor... (5000)`，最坏情况会等 15 秒；把同一个 `QDeadlineTimer` 传入每一步，每一步只使用 `remainingTime()`，总等待不会超过最初的预算。

```text
错误：每一层重新开始 5 秒
  connect: 5s + read header: 5s + read body: 5s = 最坏 15s

正确：一开始建立一个截止点
  deadline: 5s
  connect: 使用剩余时间
  read header: 使用更少的剩余时间
  read body: 使用更少的剩余时间
```

它和 `QElapsedTimer` 的区别：

| 需求 | 选择 | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 统计已经耗时多少 | `QElapsedTimer` | 从 `start()` 起累计经过时间 | 自己用 `elapsed()` 算剩余预算 |
| 向多层调用传递统一超时 | `QDeadlineTimer` | 保存未来截止点并直接给出剩余时间 | 传递同一个对象，不要在每层重新构造 |
| 事件循环中周期性触发回调 | `QTimer` 或 `QChronoTimer` | 异步定时发出信号 | `QDeadlineTimer` 本身不会发信号或调度回调 |

`QDeadlineTimer` 使用与 `QElapsedTimer` 相同的单调参考时钟。它不受系统墙上时钟被用户或 NTP 调整的影响，但其 `deadline()` 返回值也因此不是 Unix 时间戳，不能持久化、打印给用户或发送给另一台机器。

## 2. 最小可用代码：将剩余预算传给阻塞 API

```cpp
#include <QDeadlineTimer>
#include <QMutex>

bool lockWithBudget(QMutex &mutex)
{
    QDeadlineTimer deadline(3000); // 从现在起总共最多 3 秒

    while (!deadline.hasExpired()) {
        if (mutex.tryLock(deadline.remainingTime())) {
            mutex.unlock();
            return true;
        }
    }
    return false;
}
```

现实代码中通常不需要额外的 `while`，而是把 `deadline.remainingTime()` 交给下一个可能阻塞的接口。这里的要点是：`remainingTime()` 每次读取都会变小，后续步骤不会把时间预算重置。

## 3. 三种状态：已过期、有剩余、永不超时

```cpp
QDeadlineTimer expired;                 // 默认：已过期
QDeadlineTimer finite(1500);            // 从现在起约 1500 ms 后过期
QDeadlineTimer forever(QDeadlineTimer::Forever); // 永不过期
```

状态的可观察语义如下：

| 状态 | 状态查询结果 | 剩余时间 | 使用时重点注意 |
| --- | --- | --- | --- |
| 已过期 | `hasExpired()` 为 `true`，`isForever()` 为 `false` | `0` | 0 不表示“还能等待一会儿”，应立即停止或尝试非阻塞操作 |
| 未过期 | `hasExpired()` 与 `isForever()` 均为 `false` | 正毫秒数 | 读取与真正阻塞之间时间仍会流逝，不能把它当恒定值缓存 |
| 永不过期 | `hasExpired()` 为 `false`，`isForever()` 为 `true` | `-1` | 传给其它 API 前确认该 API 也把 `-1` 解释为无限等待 |

传给 `QDeadlineTimer(qint64 msecs)` 或 `setRemainingTime()` 的规则值得记住：

- 正数：从当前时刻起设定相应的剩余毫秒数；
- 0：立即过期；
- 负数：永不过期。Qt 6.6 前只有 `-1` 有此意义，若兼容旧 Qt，显式使用 `-1` 或 `Forever`。

默认构造和“剩余时间为 0”的实例可能为了优化而不读取当前时钟，只使用一个已知在过去的内部值。因此它们适合判断“已过期”，却不适合用 `deadline()` 计算“已经超时了多久”。后者应使用 `QDeadlineTimer::current()` 作为基准。

## 4. 实战模式：一个预算穿过多层函数

```cpp
bool receiveMessage(QIODevice &socket, QDeadlineTimer deadline)
{
    if (!socket.bytesAvailable()
        && !socket.waitForReadyRead(deadline.remainingTime())) {
        return false;
    }

    const QByteArray header = socket.read(16);
    if (header.size() != 16)
        return false;

    const qsizetype payloadSize = parseSize(header);
    while (socket.bytesAvailable() < payloadSize) {
        if (deadline.hasExpired()
            || !socket.waitForReadyRead(deadline.remainingTime())) {
            return false;
        }
    }
    return true;
}

bool receiveWithFiveSecondLimit(QIODevice &socket)
{
    return receiveMessage(socket, QDeadlineTimer(5000));
}
```

这里按值传递是有意的：`QDeadlineTimer` 是小型值类型，拷贝的是同一个截止点的值，而不是重新开始五秒。下层函数不该擅自执行 `setRemainingTime()`，否则就破坏了调用者设定的时间预算。

如果上层有取消令牌、应用退出状态或网络中断，也应在循环中同时检查；超时只是一种停止原因，不是完整的取消模型。

## 5. `remainingTime()` 和 `deadline()` 的用途不同

### 5.1 优先使用剩余时间

```cpp
const qint64 timeoutMs = deadline.remainingTime();
mutex.tryLock(timeoutMs);
```

`remainingTime()` 返回毫秒，已过期时为 0，永不过期时为 -1。这正好适配许多 Qt 等待 API，例如设备读取、互斥锁、条件变量、信号量和读写锁的超时参数。

更高精度或 C++ chrono 风格代码可用：

```cpp
const std::chrono::nanoseconds left =
    deadline.remainingTimeAsDuration();
```

已过期时它返回零时长，永不过期时返回 `std::chrono::nanoseconds::max()`。

### 5.2 `deadline()` 是参考时钟上的绝对刻度

`deadline()` / `deadlineNSecs()` 返回相对于 Qt 单调参考时钟的绝对截止刻度。它们用于比较两个 `QDeadlineTimer`、计算超时量或实现需要绝对截止点的底层接口。

```cpp
qint64 overdueMs = deadline.deadline()
    - QDeadlineTimer::current().deadline();
```

结果小于 0 表示已经超时。永不过期时 `deadline()` 返回 `qint64` 最大值；纳秒版本在永不过期或结果无法容纳时也返回最大值。常规业务不要用这些数值做跨进程数据，也不要将它们误解释为“自 1970 年以来的毫秒”。

## 6. 精度类型不是承诺的唤醒精度

构造和设置接口可以带 `Qt::TimerType`：

```cpp
QDeadlineTimer deadline(10, Qt::PreciseTimer);
```

- `Qt::CoarseTimer` 是默认值，通常更省成本，适合大多数网络和锁等待预算；
- `Qt::PreciseTimer` 请求更精确的计时，适合确有低延迟需求的场景；
- `Qt::VeryCoarseTimer` 当前按 coarse 方式解释。

这只是对 Qt 和操作系统的计时策略提示。线程调度、系统负载、所调用阻塞 API 的实现都可能让唤醒晚于截止点；不能把它当作实时系统保证。某些操作系统没有 coarse 计时支持时，Qt 会退化为精确计时路径。

## 7. C++ `std::chrono` 互操作

```cpp
using namespace std::chrono_literals;

QDeadlineTimer deadline(250ms);
deadline += 50ms;

if (deadline.remainingTimeAsDuration() > 20ms) {
    // 还有时间做一次轻量收尾。
}
```

可以用 `std::chrono::duration` 作为“从现在起的剩余时间”，也可以用 `std::chrono::time_point` 表示截止点。`time_point` 需要在外部时钟和 Qt 内部单调时钟之间转换，因此比 duration 方式成本更高，也不能期待跨时钟转换后仍精确相等。

优先在同一个调用链中使用 duration 或一个已创建好的 `QDeadlineTimer`。需要与 `std::chrono::steady_clock` 对接时，使用 time point 是合理的；不要把 `system_clock` 的墙上时间当作防止时钟跳变的超时依据。

## 8. 常见误区

| 误区 | 为什么会出问题 | 应该怎样做 | 使用时重点注意 |
| --- | --- | --- | --- |
| 每层函数都新建 `QDeadlineTimer(5000)` | 总超时会按调用层数累加 | 在入口创建一次，按值传入后续函数 | 下层只读取，不应重设剩余时间 |
| 认为默认构造表示“未开始” | 默认对象已经过期 | 用显式有限时长或 `Forever` 表示业务状态 | 要算超时量时用 `current()` |
| 把 `deadline()` 当 Unix 时间戳保存 | 它属于进程本地单调参考时钟 | 持久化真实时间用 UTC `QDateTime` 或协议时间戳 | 跨重启、跨机器的 deadline 数值没有意义 |
| 将 `remainingTime() == 0` 当作无限等待 | 0 表示已过期 | `-1` 或 `Forever` 才表示不超时 | 传给第三方接口先确认其 -1 语义 |
| 使用 `PreciseTimer` 就假设准点唤醒 | 调度和系统负载仍会造成延迟 | 用它选择更合适的策略，并容忍迟到 | 非实时 OS 没有硬实时保证 |
| 用计时器替代取消机制 | 到期前无法响应显式取消 | 与取消标志、socket 错误和应用关闭条件一起检查 | 超时只是一种终止条件 |

## API 速查表
### 9.1 构造、状态和时钟类型

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `ForeverConstant::Forever` | 表示一个永不超时的截止点 | 推荐使用 `QDeadlineTimer::Forever` 这个便捷常量 |
| 常量 | `QDeadlineTimer::Forever` | 永不过期构造器的标签 | `remainingTime()` 对它返回 `-1` |
| 构造 | `QDeadlineTimer()` | 创建一个已过期的计时器 | 不读取当前时钟，不能用它测量超时量 |
| 构造 | `QDeadlineTimer(Qt::TimerType type)` | 创建带指定类型但已过期的计时器 | timer type 对已过期对象通常没有实际效果 |
| 构造 | `QDeadlineTimer(ForeverConstant, Qt::TimerType type = Qt::CoarseTimer)` | 创建永不过期计时器 | 无限等待会影响关闭与取消响应，谨慎使用 |
| 构造 | `QDeadlineTimer(qint64 msecs, Qt::TimerType type = Qt::CoarseTimer)` | 从现在起设置毫秒级剩余时间 | 0 过期、负数永不超时；兼容 Qt 6.5 及以前时仅用 `-1` 表示 forever |
| chrono 构造 | `QDeadlineTimer(std::chrono::duration<Rep, Period>, Qt::TimerType)` | 从 chrono 剩余时长创建 | 零或负时长过期，`duration::max()` 表示 forever |
| chrono 构造 | `QDeadlineTimer(std::chrono::time_point<Clock, Duration>, Qt::TimerType)` | 从 chrono 截止时刻创建 | 需时钟转换；过去时刻过期，跨时钟比较不够精确 |
| 状态 | `hasExpired() const` | 判断是否已经到达截止点 | forever 永远返回 `false` |
| 状态 | `isForever() const` | 判断是否永不过期 | 可用来把“无限等待”与普通长超时区分 |
| 类型 | `timerType() const` | 返回当前计时精度类型 | 这是请求的策略，不是实际唤醒精度证明 |
| 类型 | `setTimerType(Qt::TimerType)` | 修改计时精度类型 | 不要频繁切换；选择应由等待场景决定 |
| 交换 | `swap(QDeadlineTimer &other)` | 高效交换两个截止状态 | 交换后 timer type 和 deadline 一并交换 |

### 9.2 剩余时间、绝对截止点和设置

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 剩余时间 | `remainingTime() const` | 返回剩余毫秒数 | 过期为 0，forever 为 -1；适合 Qt 的毫秒超时 API |
| 剩余时间 | `remainingTimeNSecs() const` | 返回剩余纳秒数 | 过期为 `0`，forever 为 `-1`；不要用其计算超时量 |
| 剩余时间 | `remainingTimeAsDuration() const` | 返回 `std::chrono::nanoseconds` 剩余时长 | 过期为 zero，forever 为 duration 最大值 |
| 设置剩余 | `setRemainingTime(qint64 msecs, Qt::TimerType type = Qt::CoarseTimer)` | 从当前时刻重设毫秒级预算 | 会覆盖旧 deadline；不要在下层函数意外重置总预算 |
| 设置剩余 | `setRemainingTime(std::chrono::duration<Rep, Period>, Qt::TimerType)` | 从 chrono 时长重设预算 | `duration::max()` 表示 forever |
| 设置剩余 | `setPreciseRemainingTime(qint64 secs, qint64 nsecs = 0, Qt::TimerType type = Qt::CoarseTimer)` | 用秒和纳秒设置剩余时间 | 用于确有子毫秒需求；系统仍可能晚唤醒 |
| 截止刻度 | `deadline() const` | 返回毫秒级绝对参考时钟刻度 | 不是墙上时间；forever 返回最大值 |
| 截止刻度 | `deadlineNSecs() const` | 返回纳秒级绝对参考时钟刻度 | 超大值或 forever 返回最大值，计算前要防溢出 |
| 设置刻度 | `setDeadline(qint64 msecs, Qt::TimerType type = Qt::CoarseTimer)` | 直接设置参考时钟上的毫秒截止刻度 | 通常更易错，普通业务优先 `setRemainingTime()` |
| 设置刻度 | `setDeadline(std::chrono::time_point<Clock, Duration>, Qt::TimerType)` | 用 chrono 时刻设截止点 | 时钟转换有成本和精度损失 |
| 设置刻度 | `setPreciseDeadline(qint64 secs, qint64 nsecs = 0, Qt::TimerType type = Qt::CoarseTimer)` | 直接设置秒加纳秒的参考时钟截止点 | 面向底层接口；避免把 Unix 秒错误传入 |
| 当前刻度 | `current(Qt::TimerType type = Qt::CoarseTimer)` | 返回保证记录当前时钟的已过期计时器 | 用它和 `deadline()` 相减计算超时量 |
| 静态运算 | `addNSecs(QDeadlineTimer dt, qint64 nsecs)` | 返回在 deadline 上加纳秒后的新对象 | 不修改传入对象；注意极大值和 forever 边界 |

### 9.3 运算符和 chrono 赋值

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 算术 | `operator+(QDeadlineTimer, qint64 msecs)` | 返回延后指定毫秒的新 deadline | 原对象不变；用作预算调整而非重新开始计时 |
| 算术 | `operator+(qint64 msecs, QDeadlineTimer)` | 同上，支持时长写在左侧 | 语义与右侧相加相同 |
| 算术 | `operator-(QDeadlineTimer, qint64 msecs)` | 返回提前指定毫秒的新 deadline | 减去负值等于延后，避免可读性差的双重负号 |
| 差值 | `operator-(QDeadlineTimer, QDeadlineTimer)` | 返回两个 deadline 的毫秒差 | 使用同一参考时钟；forever 和溢出值不适合普通差值计算 |
| 就地算术 | `operator+=(qint64 msecs)` | 原地延后 deadline | 修改调用方对象，传入共享预算时格外小心 |
| 就地算术 | `operator-=(qint64 msecs)` | 原地提前 deadline | 可能使 deadline 立刻过期 |
| chrono 算术 | `operator+(QDeadlineTimer, std::chrono::duration)` | 返回增加 chrono 时长的新 deadline | duration 会换算为纳秒 |
| chrono 算术 | `operator+(std::chrono::duration, QDeadlineTimer)` | 支持 chrono 时长放左侧 | 语义同右侧版本 |
| chrono 就地算术 | `operator+=(std::chrono::duration)` | 原地增加 chrono 时长 | 会修改预算，避免在下层随意调用 |
| chrono 赋值 | `operator=(std::chrono::duration)` | 用剩余时长替换 deadline | 替换而非增加，读代码时区分 `=` 和 `+=` |
| chrono 赋值 | `operator=(std::chrono::time_point)` | 用绝对 chrono 时刻替换 deadline | 可能涉及跨时钟转换 |
| 比较 | `==`, `!=`, `<`, `<=`, `>`, `>=` | 比较两个 deadline 的先后或相等 | 只比较 deadline 值，timer type 不参与比较 |

## 10. 一个可复用的超时组合原则

```cpp
bool doWholeOperation(QIODevice &device)
{
    QDeadlineTimer deadline(5000, Qt::CoarseTimer);

    if (!openChannel(device, deadline))
        return false;
    if (!sendRequest(device, deadline))
        return false;
    return receiveMessage(device, deadline);
}
```

将一个 deadline 按值传给每个阶段，可以让函数独立、测试清楚，又让“整个操作至多五秒”始终成立。只有调用者拥有改变预算的权利；各阶段只消耗它并报告成功、失败、取消或超时，这就是 `QDeadlineTimer` 在同步 I/O 和并发等待里最实用的角色。
