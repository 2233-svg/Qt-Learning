# Qt QChronoTimer 深入笔记

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.8  
> 头文件：`#include <QChronoTimer>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject`  
> 核心定位：以 `std::chrono::nanoseconds` 表示间隔的 QObject 定时器

## 1. 它解决什么问题

`QTimer` 已能覆盖绝大多数 UI 刷新、延迟执行和周期任务。`QChronoTimer` 针对两类需求提供更自然的接口：

- 代码已经使用 `std::chrono`，不想在毫秒整数与 duration 之间反复换算。
- 间隔可能远大于 `int` 毫秒可表达的范围，或需要以纳秒为接口单位。

它和 `QTimer` 一样依赖事件循环、在所属线程发出 `timeout()`，并不保证操作系统真的在纳秒时刻唤醒线程。所谓“纳秒”是可设置和可表示的分辨率，不是实时系统承诺。

| 类型 | 间隔接口 | 大致可表示范围 | 适合场景 |
| --- | --- | --- | --- |
| `QTimer` | 毫秒和 chrono 便捷 API。 | 约正负 24 天。 | 普通 UI、网络超时、常规周期任务。 |
| `QChronoTimer` | `std::chrono::nanoseconds`。 | 约正负 292 年。 | 长期调度、chrono 主导代码、避免毫秒整数溢出。 |
| `QBasicTimer` | 低层定时器 ID 包装。 | 取决于底层定时器。 | 无需信号槽的轻量对象成员。 |

## 2. 最小可用示例

```cpp
#include <QChronoTimer>
#include <QObject>
#include <chrono>

using namespace std::chrono_literals;

class Poller : public QObject
{
public:
    Poller()
        : m_timer(500ms, this)
    {
        connect(&m_timer, &QChronoTimer::timeout,
                this, &Poller::pollOnce);
        m_timer.start();
    }

private:
    void pollOnce();

    QChronoTimer m_timer;
};
```

创建、连接、设置间隔和启动的顺序可以调整；关键在于对象所属线程必须有正在运行的事件循环。没有事件循环时，定时器不会按预期发出 `timeout()`。

`QChronoTimer` 禁止复制。它是 `QObject`，通常作为拥有者的成员或带 parent 的堆对象使用，不能放入要求可复制元素的普通值容器。

## 3. 线程归属：在哪个线程启动，就在哪个线程触发

Qt 以 `QObject` 的线程归属决定哪一个事件循环驱动该定时器并发出 `timeout()`。定时器可用于任何拥有事件循环的线程；非 GUI 线程通常要通过 `QThread::exec()` 启动事件循环。

```text
timer.thread()
      |
      v
that thread's event loop
      |
      v
timeout() is emitted there
```

必须在定时器所属线程调用 `start()` 与 `stop()`。不要从工作线程直接操作 GUI 线程的 timer，也不要从 GUI 线程直接启动已移动到工作线程的 timer；用 queued signal/slot 或 `QMetaObject::invokeMethod()` 把调用投递回对象所属线程。

## 4. 间隔、零间隔和负间隔

### 4.1 改变运行中的间隔会重启

`setInterval()` 在定时器运行时会改变间隔、停止并重新启动它，同时取得新的 `id()`。依赖 timer ID 或正在倒计时的逻辑，修改后必须重新读取状态。

```cpp
timer.setInterval(2s);
// 如果 timer 原本 active，它已经按 2s 重新启动，并拥有新 ID。
```

### 4.2 `0ns` 不是忙等

默认间隔是 `0ns`。启动零间隔 timer 后，Qt 会在窗口系统事件队列中的待处理事件处理完后尽快触发它；零 timer 与其它事件源之间的先后顺序未指定。

它可以把大量工作拆成很多小块，维持 UI 响应：

```cpp
connect(&timer, &QChronoTimer::timeout, this, [this] {
    processOneItem();
    if (finished()) {
        timer.stop();
    }
});
timer.start(); // interval 默认 0ns
```

回调必须快速返回。若每次 `timeout()` 做大量计算，零间隔 timer 仍会卡住界面；现代代码更应考虑把耗时工作移动到独立线程。

### 4.3 负间隔

从 Qt 6.10 起，设置负间隔会产生运行时警告，并将间隔重置为 `1ms`。此前版本对负值的行为可能令人意外，例如无法启动或让运行中的定时器停止。业务代码不要依赖 Qt 的纠正行为，应在自己的 duration 计算后先校验非负。

## 5. 精度与迟到：定时器不是实时调度器

`timerType` 让你表达对系统计时精度与功耗的取舍：

| `Qt::TimerType` | Qt 的行为目标 | 提前触发规则 | 适合场景 |
| --- | --- | --- | --- |
| `PreciseTimer` | 尽量保持 1ns 级请求精度。 | 不会比预期更早超时。 | 需要避免早触发的短周期逻辑。 |
| `CoarseTimer` | 降低系统唤醒成本。 | 最多可提前约间隔的 5%。 | 普通周期刷新与非关键轮询。 |
| `VeryCoarseTimer` | 允许更大的节能误差。 | 最多可提前 500ms。 | 分钟级、低功耗后台性质任务。 |

任何类型都可能**晚于**预期：系统繁忙、线程被阻塞或无法提供请求精度都会造成迟到。若期间错过多个周期，Qt 只发射一次 `timeout()`，之后恢复原始节奏；它不会补发多次回调。因此 timer 的回调应以当前时间计算状态，而不是假设每一次 tick 都没有丢失。

## 6. 单次、周期与剩余时间

单次模式通过 `setSingleShot(true)` 开启。它启动后只发一次 `timeout()`，随后变为 inactive；重复模式会按 interval 周期触发。

```cpp
QChronoTimer retryTimer(3s, this);
retryTimer.setSingleShot(true);
connect(&retryTimer, &QChronoTimer::timeout, this, &Client::retry);
retryTimer.start();
```

`remainingTime()` 返回到下次超时的 duration；定时器未激活时返回负 duration。这个值是观察值，不能当作同步或精确调度依据，因为调用后事件循环仍可能延迟。

## 7. `callOnTimeout()`：带生命周期保护的便捷连接

`callOnTimeout(context, slot, connectionType)` 等价于一次 `QObject::connect()`，返回 `QMetaObject::Connection`。

```cpp
const auto connection = m_timer.callOnTimeout(
    this,
    [this] { refresh(); },
    Qt::AutoConnection);
```

传入 `context` 后，context 被销毁时连接会自动断开，适合 lambda 捕获对象成员的情况。若要提前断开，保存返回的 connection 并调用 `QObject::disconnect(connection)`。

`QChronoTimer` 没有自己的静态 `singleShot()` 辅助函数；Qt 文档建议直接使用支持 chrono duration 的 `QTimer::singleShot()`。

## 8. 属性与绑定

`active`、`interval`、`singleShot` 与 `timerType` 提供 `QBindable` 访问器，可接入 Qt 属性绑定；`remainingTime` 只是只读观察属性。

属性绑定适合用声明式或响应式方式同步 timer 配置，但不要把高频 `remainingTime()` 当作进度条动画驱动源。它没有绑定接口，也不会按每一纳秒通知；需要平滑 UI 更新时另设合适的显示节拍。

## 9. 常见错误

### 9.1 在错误线程启动

定时器能存在于对象线程之外，但 `start()`、`stop()` 必须在其 thread affinity 所属线程执行。跨线程直接调用往往伴随 Qt 警告或没有触发回调的问题。

### 9.2 把 `PreciseTimer` 当成硬实时

它保证不提前超时的目标，但不保证准时。任何阻塞主线程、系统调度和电源管理都可能使回调变晚。

### 9.3 依赖 timer ID 长期不变

重新 `start()` 或在运行中 `setInterval()` 都会重新分配 ID。ID 适合短期识别内部 timer，不适合作为业务主键。

### 9.4 用零 timer 吞掉事件循环

零 timer 的 slot 必须把工作切细，每次快速返回；重计算放进 `QThread`、Qt Concurrent 或其它异步任务机制。

## API 速查表
### 构造、生命周期与状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QChronoTimer(QObject *parent = nullptr)` | 创建 timer，默认 interval 为 `0ns`。 | 只有 `start()` 后才激活；零间隔不保证事件顺序。 |
| 构造 | `explicit QChronoTimer(std::chrono::nanoseconds nsec, QObject *parent = nullptr)` | 创建 timer 并设置初始间隔。 | 传入 duration，避免手写毫秒换算。 |
| 生命周期 | `~QChronoTimer() override` | 析构 timer 并停止其底层计时。 | 带 parent 时由父对象销毁；不要重复管理 QObject 所有权。 |
| 状态 | `bool isActive() const` | 判断 timer 是否正在运行。 | 只反映激活状态，不代表回调正在执行。 |
| 状态 | `Qt::TimerId id() const` | 返回运行中 timer 的 ID。 | inactive 时返回 `Qt::TimerId::Invalid`；重启或改 interval 后会变。 |
| 属性绑定 | `QBindable<bool> bindableActive()` | 暴露 active 的可绑定入口。 | 用于属性系统，不是 timeout 信号的替代品。 |

### 间隔、单次与精度

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 间隔 | `void setInterval(std::chrono::nanoseconds nsec)` | 设置超时间隔。 | 运行中调用会 stop/start 并更换 ID；Qt 6.10 起负值被警告并改为 1ms。 |
| 间隔 | `std::chrono::nanoseconds interval() const` | 返回当前配置的间隔。 | 默认值是 `0ns`。 |
| 属性绑定 | `QBindable<std::chrono::nanoseconds> bindableInterval()` | 暴露 interval 的可绑定入口。 | 绑定更新同样会影响运行中的 timer。 |
| 剩余时间 | `std::chrono::nanoseconds remainingTime() const` | 返回距离下次 timeout 的剩余 duration。 | inactive 时为负值；它是快照，不是实时保证。 |
| 模式 | `void setSingleShot(bool singleShot)` | 设置只触发一次或周期触发。 | 单次 timer 触发后变为 inactive，下一次需要重新 start。 |
| 模式 | `bool isSingleShot() const` | 查询是否处于单次模式。 | 仅描述模式，不代表当前是否 active。 |
| 属性绑定 | `QBindable<bool> bindableSingleShot()` | 暴露 singleShot 的可绑定入口。 | 用属性系统改模式时也要考虑当前运行状态。 |
| 精度 | `void setTimerType(Qt::TimerType type)` | 设置 Precise、Coarse 或 VeryCoarse 的计时偏好。 | 不能保证准时；类型影响精度、提前触发容忍度和功耗。 |
| 精度 | `Qt::TimerType timerType() const` | 返回当前 timer 类型。 | 读取的是请求策略，不是系统最终精度测量。 |
| 属性绑定 | `QBindable<Qt::TimerType> bindableTimerType()` | 暴露 timerType 的可绑定入口。 | 适合响应式配置，不替代定时器线程规则。 |

### 连接、控制与事件

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 便捷连接 | `callOnTimeout(const QObject *context, Functor &&slot, Qt::ConnectionType type = Qt::AutoConnection)` | 把 `timeout()` 连接到给定 context 的回调并返回连接句柄。 | context 销毁时自动断开；保存连接可手动 disconnect。 |
| 启动 | `void start()` | 按 interval 启动或重新启动 timer。 | 必须在 timer 所属线程调用；重启会换 ID。 |
| 停止 | `void stop()` | 停止 timer。 | 必须在 timer 所属线程调用；停止后 remainingTime 为负。 |
| 信号 | `void timeout()` | 到期时发出。 | 由所属线程的事件循环发射；事件循环堵塞时会迟到且不会补发多个 tick。 |
| 受保护重写 | `void timerEvent(QTimerEvent *event) override` | 接收底层 timer 事件的实现点。 | 一般直接使用 `timeout()`；重写会绕开部分信号与单次等高层便利。 |

---

### 一句话总结

`QChronoTimer` 以 `std::chrono` 和更大 interval 范围提供 QObject 定时器能力，但它仍是事件循环驱动的软定时器：在线程归属处启动，在迟到时只补一次信号，精度设置不等于实时保证。
