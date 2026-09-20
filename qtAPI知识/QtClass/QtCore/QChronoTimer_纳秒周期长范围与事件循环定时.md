# Qt QChronoTimer 深入笔记

> 适用版本：Qt 6.11.1（类自 Qt 6.8 引入）  
> 头文件：`#include <QChronoTimer>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QChronoTimer`  
> 定位：以 `std::chrono::nanoseconds` 表示周期、范围约 ±292 年的事件循环定时器

`QChronoTimer` 与 `QTimer` 的调度模型相同，区别主要是接口精度和可表示范围：QChronoTimer 原生使用纳秒 duration，避免 int 毫秒在长周期上的溢出。它并不让普通操作系统变成纳秒硬实时系统。

## 1. CMake 与最小代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QChronoTimer>
using namespace std::chrono_literals;

QChronoTimer timer(250ms, this);
timer.setTimerType(Qt::PreciseTimer);

connect(&timer, &QChronoTimer::timeout,
        this, &Controller::sample);
timer.start();
```

也可以先默认构造：

```cpp
QChronoTimer timer(this);
timer.setInterval(1500us);
timer.start();
```

## 2. 与 QTimer 的核心区别

| 能力 | `QTimer` | `QChronoTimer` |
| --- | --- | --- |
| interval 原生类型 | int 毫秒 / milliseconds 辅助 | `std::chrono::nanoseconds` |
| 可表示范围 | 约 ±24 天 | 约 ±292 年 |
| 精度请求 | 最细约毫秒接口 | 最细纳秒接口 |
| 静态 singleShot | 有，支持 chrono | 无，直接使用 `QTimer::singleShot` |
| 事件循环/线程规则 | 相同 | 相同 |

需要微秒/纳秒 duration 或很长周期时选 QChronoTimer；普通 UI 延迟和秒级轮询继续使用 QTimer 更普遍。

## 3. interval 属性

```cpp
timer.setInterval(2s);
std::chrono::nanoseconds interval = timer.interval();
```

任何 chrono duration 都会转换为 nanoseconds：

```cpp
timer.setInterval(std::chrono::microseconds(750));
```

转换时注意表示范围和截断。浮点 duration 应先按业务规则取整，不要隐式依赖 duration_cast 的截断方向。

Qt 6.10 起设置负周期会警告并重置为 1ms。虽然类型支持负数是为了完整表示范围，活动 timer 的负周期没有业务意义，应在接口入口校验。

运行中修改 interval 会停止并重启 timer，从修改时刻重新计算期限，ID 也会变化。

## 4. 启动、停止与活动状态

```cpp
timer.start();

if (timer.isActive())
    timer.stop();
```

QChronoTimer 没有 `start(duration)` 重载；先 `setInterval()`，再 `start()`。构造函数可直接接收 duration。

`active` 和 interval 都支持 Qt bindable property：

```cpp
QBindable<bool> active = timer.bindableActive();
QBindable<std::chrono::nanoseconds> interval =
    timer.bindableInterval();
```

## 5. 重复与单次模式

默认重复触发：

```cpp
timer.setSingleShot(false);
```

单次模式：

```cpp
timer.setSingleShot(true);
connect(&timer, &QChronoTimer::timeout,
        this, &Controller::finishDelay);
timer.start();
```

```cpp
bool once = timer.isSingleShot();
QBindable<bool> binding = timer.bindableSingleShot();
```

QChronoTimer 没有静态 `singleShot()`。需要无对象的一次调用时：

```cpp
QTimer::singleShot(250us, this, [this] {
    sampleOnce();
});
```

## 6. timeout 与便捷连接

```cpp
connect(&timer, &QChronoTimer::timeout,
        this, &Controller::sample);
```

`callOnTimeout()` 强制要求 context：

```cpp
QMetaObject::Connection connection =
    timer.callOnTimeout(this, [this] {
        sample();
    });
```

还可传 `Qt::ConnectionType`。context 销毁后连接自动断开，回调在 context 所属线程按连接类型执行。

## 7. Timer Type 与真实精度

```cpp
timer.setTimerType(Qt::PreciseTimer);
Qt::TimerType type = timer.timerType();
```

- `Qt::PreciseTimer`：请求最高精度，QChronoTimer 尝试 1ns 精度且不提前触发。
- `Qt::CoarseTimer`：可能在周期约 5% 的提前范围内触发。
- `Qt::VeryCoarseTimer`：可能最多约提前 500ms。

“尝试 1ns”是 API 分辨率和精度请求，不是实际调度保证。硬件时钟、操作系统 tick、线程调度、功耗策略和槽执行时间通常远大于 1ns。

所有 timer 都可能晚到。系统忙时，Qt 通常只发一次 timeout，再恢复原周期，不会补发全部错过次数。

## 8. 剩余时间

```cpp
std::chrono::nanoseconds remaining = timer.remainingTime();
```

- 正数：预计剩余时间。
- zero：已到期或超期等待处理。
- 负数：timer 不活动或无法获得剩余时间。

remainingTime 是调度快照，不能用于精密测量。测量函数耗时使用 `QElapsedTimer`；表示一个可跨 API 传递的截止时间使用 `QDeadlineTimer`。

## 9. Timer ID

```cpp
Qt::TimerId id = timer.id();
```

未运行时 ID 无效；重新 start 或修改 interval 后 ID 可能改变。它主要用于诊断和低层集成，不应作为业务身份。

## 10. 零周期与空闲处理

Qt 文档建议可用 0ns QChronoTimer 做空闲处理：

```cpp
QChronoTimer idle(0ns, this);
connect(&idle, &QChronoTimer::timeout,
        this, &Controller::processOneItem);
idle.start();
```

每次必须快速返回。零周期与其它事件源的先后未指定，持续有工作时可能让事件循环保持高负载。大量 CPU 工作应放到线程池，不能靠 0ns timer 伪装成异步。

## 11. 线程亲和性

QChronoTimer 可在任意有事件循环的线程工作，但必须在它所属线程启动和停止：

```cpp
connect(thread, &QThread::started,
        worker, [worker] {
    worker->chronoTimer()->start();
});
```

不要从 GUI 线程直接启动位于工作线程的 timer。跨线程通过 queued signal/slot 请求操作。

移动拥有子 timer 的父 QObject 时，timer 一起迁移，活动 timer 会在迁移过程中重新注册。频繁迁移会延迟到期。

## 12. 极长周期的工程边界

接口能表示数十年，不代表进程能可靠存活数十年。系统重启、休眠、时钟源变化、应用升级都会打断 timer。对于“明年执行”的业务，应持久化绝对计划时间，并在每次启动后重新计算：

```cpp
const auto remaining = targetUtc - QDateTime::currentDateTimeUtc();
```

QChronoTimer 适合避免 duration 溢出，不替代持久化调度器。

## 13. 周期采样不等于真实时间

```cpp
connect(&timer, &QChronoTimer::timeout, [&] {
    ++sampleNumber;
});
```

不能用 `sampleNumber * interval` 推断实际时间。需要计算真实变化量时结合 `QElapsedTimer`：

```cpp
const qint64 nanoseconds = elapsed.nsecsElapsed();
advanceSimulation(std::chrono::nanoseconds(nanoseconds));
elapsed.restart();
```

## 14. 常见误区

### 纳秒 interval 等于纳秒回调精度

不等于。它只是接口分辨率和系统精度请求。

### QChronoTimer 有静态 singleShot

没有。使用支持 chrono 的 `QTimer::singleShot()`。

### 长达数年的 timer 无需持久化

进程和设备生命周期不可靠。保存目标时间并在重启时恢复。

### 可从任意线程 start

不可以。必须在 timer 所属线程操作。

### 每次超时都代表正好经过一个 interval

系统繁忙或休眠会晚到且不补全部周期。测量真实 elapsed。

## API 速查表
### 15.1 构造、生命周期和属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QChronoTimer(QObject *parent = nullptr)` | 创建一个 QObject timer，周期稍后通过 `setInterval()` 设置。 | 构造后不会自动启动；parent 只管理对象生命周期，不决定业务是否开始计时。 |
| 构造 | `QChronoTimer(std::chrono::nanoseconds nsec, QObject *parent = nullptr)` | 创建时直接设置纳秒 interval。 | 仍需调用 `start()` 才会注册 timer；纳秒是接口单位，不代表系统一定能纳秒准时回调。 |
| 析构 | `~QChronoTimer()` | 销毁 timer 对象并停止底层 timer。 | 不能在销毁后继续依赖已排队的回调；连接应有 context 或由对象树管理。 |
| 属性 | `singleShot` | 控制 timer 是只触发一次还是周期触发。 | 单次触发后会变为 inactive；再次使用需要重新 `start()`。 |
| 属性 | `interval` | 保存 timer 的 chrono 纳秒周期。 | 活动时修改会重启 timer 并改变 ID；Qt 6.10 起负周期会警告并重置为 1ms。 |
| 属性 | `remainingTime` | 暴露当前剩余时间。 | 只读快照；负值表示 inactive 或不可确定，零表示到期/超期但尚未处理。 |
| 属性 | `timerType` | 保存精度/功耗策略。 | `PreciseTimer` 仍可能晚到，不能作为硬实时承诺。 |
| 属性 | `active` | 表示底层 timer 是否正在运行。 | 是状态观察，不等于业务任务是否完成。 |

### 15.2 interval、启动和停止

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 周期设置 | `setInterval(std::chrono::nanoseconds nsec)` | 设置 timer 周期。 | 接口接受纳秒；其他 duration 需显式或隐式转换，浮点 duration 建议先按业务规则取整。 |
| 周期读取 | `interval()` | 返回当前周期，类型为 `std::chrono::nanoseconds`。 | 范围远大于 `QTimer` 的 int 毫秒，但不等于进程能可靠运行数十年。 |
| 启动 | `start()` | 按当前 interval 注册或重启 timer。 | 必须在对象所属线程调用；`QChronoTimer` 没有 `start(duration)` 重载。 |
| 停止 | `stop()` | 停止当前 timer。 | 必须在对象所属线程调用；停止后不会继续发出该轮 `timeout()`。 |
| 活动状态 | `isActive()` | 查询 timer 是否处于 active 状态。 | 重启、停止、单次 timeout 后都可能改变这个值。 |
| 剩余时间 | `remainingTime()` | 返回距离下一次 timeout 的 chrono 纳秒数。 | 这是调度快照，不适合测量真实耗时；测量用 `QElapsedTimer`。 |
| Timer ID | `id()` | 返回当前底层 timer 的 `Qt::TimerId`。 | inactive 时无效；重新 `start()` 或修改 interval 后 ID 可能变化。 |
| 低层屏蔽 | `startTimer()` / `killTimer()` | 从 QObject 继承但在 `QChronoTimer` 中被删除。 | 使用 `QChronoTimer::start()`/`stop()` 管理，不要绕过它直接操作底层 timer。 |

### 15.3 单次模式、精度和信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 单次设置 | `setSingleShot(bool singleShot)` | 设置 timeout 后是否自动停止。 | 类本身没有静态 `singleShot()`；临时延迟调用仍用 `QTimer::singleShot()`。 |
| 单次读取 | `isSingleShot()` | 查询当前是否为单次模式。 | 返回模式设置，不代表 timer 当前 active。 |
| 精度设置 | `setTimerType(Qt::TimerType type)` | 选择 `PreciseTimer`、`CoarseTimer` 或 `VeryCoarseTimer`。 | 它影响提前/功耗策略，不保证不晚到。 |
| 精度读取 | `timerType()` | 返回当前 timer type。 | 用于确认调度策略；真实精度取决于系统和事件循环负载。 |
| 到期信号 | `timeout()` | timer 到期时发出。 | 系统忙或休眠时可能晚到；错过多个周期通常只补发一次。 |
| 便捷连接 | `callOnTimeout(context, functor, connectionType)` | 便捷连接 `timeout()` 到 functor 或槽。 | 优先传 context，context 销毁后自动断开，回调线程由连接类型和对象亲和性决定。 |

### 15.4 Bindable 接口和使用边界

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 绑定 | `bindableActive()` | 返回 active 属性的绑定入口。 | 适合 Qt property binding；不要用绑定替代线程同步。 |
| 绑定 | `bindableInterval()` | 返回 interval 属性的绑定入口。 | 绑定写入 active timer 的 interval 仍会造成重启。 |
| 绑定 | `bindableTimerType()` | 返回 timerType 属性的绑定入口。 | 绑定变化只改变策略，不改变业务截止时间。 |
| 绑定 | `bindableSingleShot()` | 返回 singleShot 属性的绑定入口。 | 绑定的是模式；timeout 后 active 状态仍会独立变化。 |
| 场景选择 | `QChronoTimer` vs `QTimer` | 用于需要纳秒 duration 或极长范围的事件循环 timer。 | 普通 UI 延迟、静态 singleShot 和毫秒级轮询仍常用 `QTimer`；真实 elapsed 用 `QElapsedTimer`。 |

---

### 一句话总结

`QChronoTimer` 是以纳秒 duration 表示、范围极长的事件循环定时器；它解决表示精度和溢出问题，却不提供硬实时调度，仍必须遵守事件循环、线程亲和性和晚到不补周期的规则。
