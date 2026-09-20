# Qt QTimer 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTimer>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QTimer`  
> 定位：依赖事件循环的重复或单次定时器，通过 `timeout()` 信号触发工作

`QTimer` 不是独立计时线程。它向对象所属线程的事件分发器注册截止时间，事件循环在合适时机发出 `timeout()`。因此它适合 UI 刷新、轮询、延迟操作和分块任务，但不提供硬实时保证，也不能在没有事件循环的线程中正常工作。

## 1. CMake 与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QCoreApplication>
#include <QTimer>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QTimer timer;
    timer.setInterval(std::chrono::seconds(1));

    QObject::connect(&timer, &QTimer::timeout, [] {
        qInfo() << "tick";
    });

    timer.start();
    QTimer::singleShot(std::chrono::seconds(5),
                       &app, &QCoreApplication::quit);

    return app.exec();
}
```

## 2. 工作模型

```text
setInterval + start
        │
        ▼
向当前线程事件分发器注册 timer
        │ 到期
        ▼
事件循环投递 QTimerEvent
        │
        ▼
QTimer::timerEvent -> emit timeout()
        │
        ├─ singleShot：停止
        └─ repeating：安排下一周期
```

线程忙于执行槽或阻塞调用时，timer 无法准时运行。恢复后 Qt 通常只发一次超时，而不是把错过的每一周期全部补发，然后恢复原周期节奏。

## 3. `interval` 属性

### 3.1 毫秒与 chrono

```cpp
timer.setInterval(250);
int milliseconds = timer.interval();

timer.setInterval(std::chrono::milliseconds(250));
auto duration = timer.intervalAsDuration();
```

`QTimer` 的主要 interval 范围受 int 毫秒限制，约为正负 24 天。需要纳秒类型接口或极长范围时使用 `QChronoTimer`，其范围可达约 292 年。

### 3.2 运行中修改 interval

修改活动 timer 的 interval 会停止并重新启动它，timer ID 会改变，新周期从修改时刻重新计算。不要保存旧 ID 后继续与 `id()` 比较。

### 3.3 负间隔

Qt 6.10 起，设置负 interval 会产生运行时警告并重置为 1ms。旧版本可能表现为停止或无法启动。业务层仍应主动校验参数：

```cpp
void Poller::setPeriod(std::chrono::milliseconds value)
{
    if (value < std::chrono::milliseconds::zero())
        value = std::chrono::milliseconds::zero();
    m_timer.setInterval(value);
}
```

## 4. 启动与停止

```cpp
timer.start();                 // 使用已有 interval
timer.start(500);              // 设置为 500ms 并启动
timer.start(500ms);            // chrono 写法
timer.stop();

if (timer.isActive())
    qDebug() << "running";
```

重复调用 `start()` 会重新计时并获得新的 timer ID。`stop()` 对未运行 timer 安全，不会发 timeout。

`active` 是可绑定只读属性：

```cpp
QBindable<bool> active = timer.bindableActive();
```

## 5. 单次对象定时器

```cpp
QTimer timer;
timer.setSingleShot(true);
timer.setInterval(800ms);

connect(&timer, &QTimer::timeout,
        this, &Controller::finishDelay);
timer.start();
```

读取与绑定：

```cpp
bool once = timer.isSingleShot();
QBindable<bool> bindable = timer.bindableSingleShot();
```

单次 timer 在 timeout 后变为 inactive。若槽内再次 `start()`，它会开启新的一次计时。

## 6. 静态 `singleShot()`

### 6.1 Functor 与 context

```cpp
QTimer::singleShot(500ms, this, [this] {
    refreshView();
});
```

使用 context 重载的两个重要保证：

1. context 在到期前销毁，functor 不再调用。
2. functor 在 context 所属线程运行，该线程必须有事件循环。

不带 context：

```cpp
QTimer::singleShot(500ms, [] {
    qInfo() << "delayed";
});
```

它缺少外部对象生命周期保护。lambda 捕获 `this` 时必须使用 context 重载。

### 6.2 指定精度类型

```cpp
QTimer::singleShot(2s,
                   Qt::CoarseTimer,
                   this,
                   &Controller::poll);
```

还有兼容旧式 receiver/member 字符串的 nanoseconds 重载，新代码优先类型安全成员指针或 lambda。

## 7. `timeout()` 与 `callOnTimeout()`

传统连接：

```cpp
connect(&timer, &QTimer::timeout,
        this, &Controller::poll);
```

便捷接口：

```cpp
QMetaObject::Connection connection =
    timer.callOnTimeout(this, [this] {
        poll();
    });
```

带 context 的 `callOnTimeout()` 可指定 connection type，context 销毁时自动断开。无 context 重载等价于以 timer 自身作为连接上下文，在定义 `QT_NO_CONTEXTLESS_CONNECT` 时不可用。

## 8. `Qt::TimerType` 精度选择

```cpp
timer.setTimerType(Qt::PreciseTimer);
Qt::TimerType type = timer.timerType();
```

| 类型 | 行为 | 典型用途 |
| --- | --- | --- |
| `PreciseTimer` | 尽力达到约 1ms 精度，不提前触发 | 用户可感知精确定时、短周期测量 |
| `CoarseTimer` | 允许约 interval 的 5% 提前量 | 大多数 UI/轮询，默认平衡功耗 |
| `Qt::VeryCoarseTimer` | 允许最多约 500ms 提前量 | 长周期后台维护、省电任务 |

所有类型都可能晚到，因为线程可能忙、系统调度延迟或设备休眠。Precise 只承诺不早到，不承诺绝不晚到。

`timerType` 也有 bindable 接口：

```cpp
QBindable<Qt::TimerType> binding = timer.bindableTimerType();
```

## 9. 零间隔 timer

```cpp
timer.setInterval(0);
connect(&timer, &QTimer::timeout,
        this, &Worker::processOneItem);
timer.start();
```

零 timer 会“尽快”触发，但和窗口系统、I/O 等其它事件的顺序未指定。每次槽必须快速返回，通常只处理一项：

```cpp
void Worker::processOneItem()
{
    if (m_queue.isEmpty()) {
        m_timer.stop();
        return;
    }
    process(m_queue.dequeue());
}
```

如果槽每次仍执行大量工作，事件循环会一直忙，UI 行为变得不稳定。持续 CPU 工作优先线程池；只是把工作拆到下一轮事件循环可用零间隔 singleShot。

## 10. 剩余时间

```cpp
int ms = timer.remainingTime();
auto duration = timer.remainingTimeAsDuration();
```

`remainingTime()`：

- 大于 0：预计剩余毫秒。
- 0：已经到期或超期但尚未处理。
- -1：timer 不活动或无法确定。

chrono 版本返回负 duration 表示不活动/无法确定，zero 表示到期或超期。它是调度状态快照，不应作为精密计时测量；测量耗时使用 `QElapsedTimer`。

## 11. Timer ID

Qt 6.8 起：

```cpp
Qt::TimerId id = timer.id();
```

未运行时返回无效 ID。兼容旧接口：

```cpp
int legacyId = timer.timerId();
```

ID 主要用于诊断和底层 timer event 关联。普通 `QTimer` 用户不需要依赖它，且每次重启都可能变化。

## 12. 线程规则

QTimer 可以在任意有事件循环的线程使用：

```cpp
QThread workerThread;
Worker worker;
worker.moveToThread(&workerThread);

connect(&workerThread, &QThread::started,
        &worker, &Worker::startTimer);
workerThread.start();
```

必须在 timer 所属线程启动和停止，因为 Qt 根据线程亲和性选择在哪个线程发出 timeout。错误写法：

```cpp
// GUI 线程直接操作属于 workerThread 的 timer：错误
worker.timer()->start();
```

正确做法是 queued invocation 或 worker 槽：

```cpp
QMetaObject::invokeMethod(&worker, &Worker::startTimer,
                          Qt::QueuedConnection);
```

把 Worker 移动线程时，作为其 QObject 子对象的 QTimer 会一起移动；未设 parent 的值成员需要确认线程迁移和创建时机。

## 13. 周期任务的漂移语义

不要把重复 QTimer 当成“每 N 毫秒精确累计一次”的时钟：

```cpp
connect(&timer, &QTimer::timeout, [&] {
    ++ticks; // 不能据此推断真实经过 ticks * interval
});
```

系统挂起或事件循环阻塞时会漏周期。需要基于真实时间推进动画、超时或计费，应用 `QElapsedTimer` 计算实际 elapsed：

```cpp
const qint64 elapsed = clock.elapsed();
updateFromRealElapsed(elapsed);
```

## 14. 可恢复的超时模式

```cpp
class RequestTimeout final : public QObject
{
    Q_OBJECT
public:
    explicit RequestTimeout(QObject *parent = nullptr)
        : QObject(parent)
    {
        m_timer.setSingleShot(true);
        m_timer.setTimerType(Qt::PreciseTimer);
        connect(&m_timer, &QTimer::timeout,
                this, &RequestTimeout::expired);
    }

    void arm(std::chrono::milliseconds duration)
    {
        m_timer.start(duration);
    }

    void cancel() { m_timer.stop(); }

signals:
    void expired();

private:
    QTimer m_timer;
};
```

如果 QTimer 是值成员且外层 QObject 会移动线程，给它设置父对象需要谨慎：值成员不能由 parent 删除。更常见做法是在目标线程的启动槽中创建堆 timer，并以 worker 为 parent。

## 15. QTimer、QChronoTimer 与其它计时类

| 需求 | 推荐类型 |
| --- | --- |
| 事件循环中周期/单次回调 | `QTimer` |
| 纳秒 duration、超长范围 | `QChronoTimer` |
| 测量已用时间 | `QElapsedTimer` |
| 表示未来截止点 | `QDeadlineTimer` |
| 最低层 timer event | `QObject::startTimer` / `QBasicTimer` |

## 16. 常见误区

### 用 QTimer 测量函数耗时

QTimer 是调度器，不是秒表。使用 QElapsedTimer。

### 从其他线程 start/stop

不允许。通过 queued signal/slot 在 timer 所属线程操作。

### timeout 次数等于经过周期数

晚到时 Qt 不会把所有错过周期补发。根据真实 elapsed 计算。

### static singleShot 捕获裸 this 却不传 context

对象提前销毁会悬空。使用 `singleShot(duration, this, lambda)`。

### 认为 PreciseTimer 绝不会延迟

它只尽量提高精度并避免提前触发，系统调度仍可晚到。

### 零 timer 槽一直不返回

会饿死事件循环。每轮只处理有限工作或改用线程池。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 生命周期 | `QTimer(QObject *parent = nullptr)` | 创建一个由事件循环驱动的定时器对象 | 构造不会启动定时器；对象必须属于将要启动它的线程 |
| 生命周期 | `~QTimer()` | 销毁定时器对象并停止其活动定时器 | 不要在其他线程直接销毁；跨线程对象应通过所属线程的生命周期协议处理 |
| 状态 | `isActive()` / `bindableActive()` | 查询定时器是否活动，或取得可绑定的只读活动属性 | 只是当前瞬时状态；活动时修改 interval 会重启定时器 |
| 周期 | `setInterval(int)` / `interval()` | 以毫秒设置或读取定时周期 | `int` 毫秒范围约为正负 24 天；活动时设置会重新计时并更换 timer ID |
| 周期 | `setInterval(std::chrono::milliseconds)` / `intervalAsDuration()` | 用 chrono duration 设置或读取毫秒周期 | 仍受 QTimer 的范围和事件循环调度限制；超长或纳秒范围考虑 `QChronoTimer` |
| 周期绑定 | `bindableInterval()` | 获取 interval 属性的 `QBindable<int>` | 用于 Qt 属性绑定，不是绕过线程规则直接跨线程改 timer |
| 启动与停止 | `start()` | 使用当前 interval 启动或重新启动定时器 | 必须在 QTimer 所属线程调用；重复 `start()` 会重新计时 |
| 启动与停止 | `start(int)` / `start(std::chrono::milliseconds)` | 设置周期并立即启动定时器 | 这也是一次重启；负间隔在 Qt 6.10 起会警告并重置为 1ms |
| 启动与停止 | `stop()` | 停止活动定时器 | 不会发出补偿性的 `timeout()`；在正确线程调用 |
| 单次模式 | `setSingleShot(bool)` / `isSingleShot()` | 设置或读取定时器是否只触发一次 | 单次 timeout 后变为 inactive；槽中再次 `start()` 会开启新一轮 |
| 单次模式 | `bindableSingleShot()` | 获取 singleShot 属性的 `QBindable<bool>` | 适合属性绑定；绑定改变仍必须遵守对象所属线程规则 |
| 静态延迟 | `QTimer::singleShot(...)` | 不创建可见的 QTimer 对象，安排一次延迟调用 | 捕获 QObject 或 `this` 时使用带 context 的重载；context 销毁或无事件循环会影响是否执行 |
| 静态延迟 | `singleShot(Duration, Qt::TimerType, Context *, Functor &&)` | 以指定精度和 context 安排类型安全的单次 functor 调用 | `TimerType` 只影响调度精度/功耗取向，不提供硬实时保证 |
| 到期通知 | `timeout()` | 定时器到期时发出的信号，重复定时器可多次发出 | 可能因事件循环繁忙而晚到；不会为阻塞期间错过的每个周期逐一补发 |
| 便捷连接 | `callOnTimeout(Functor &&)` / `callOnTimeout(const QObject *, Functor &&)` | 直接把 functor 连接到 `timeout()`，返回连接句柄 | 优先使用带 context 的版本；无 context 版本的生命周期和线程语义要自己确认 |
| 精度策略 | `setTimerType(Qt::TimerType)` / `timerType()` | 设置或读取 `PreciseTimer`、`CoarseTimer`、`VeryCoarseTimer` 等策略 | PreciseTimer 只尽量避免提前触发，系统调度、休眠和线程阻塞仍可造成延迟 |
| 精度绑定 | `bindableTimerType()` | 获取 timerType 属性的 `QBindable<Qt::TimerType>` | 只是 Qt 属性绑定入口，不改变定时器依赖事件循环的本质 |
| 剩余时间 | `remainingTime()` | 返回预计剩余毫秒；`-1` 表示非活动或无法确定，`0` 表示已到期/超期 | 是调度状态快照，不是精密耗时测量；耗时测量使用 `QElapsedTimer` |
| 剩余时间 | `remainingTimeAsDuration()` | 以 chrono duration 返回预计剩余时间 | 负 duration 表示非活动或无法确定，zero 表示已到期/超期 |
| 定时器标识 | `id()` | Qt 6.8 起返回强类型 `Qt::TimerId` | 未运行时无效；重启、修改 interval 或迁移线程后不要依赖旧 ID |
| 定时器标识 | `timerId()` | 返回兼容旧代码的 `int` timer ID | 新代码优先使用 `id()`；普通 QTimer 用户通常不需要保存 ID |
| 低层事件 | `timerEvent(QTimerEvent *)` | QTimer 内部处理低层定时器事件的虚函数入口 | 一般不需要重载 QTimer 的实现；底层 `QObject::startTimer()` 更适合自定义 timer event |

---

### 一句话总结

`QTimer` 是事件循环驱动的调度器：在对象所属线程启动和停止，用 context 保护延迟 lambda，按精度与功耗选择 timer type，并把 timeout 视为“现在至少到期了”，而不是硬实时节拍或精密计时结果。
