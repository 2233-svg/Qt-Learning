# Qt QTimer：把延迟和周期任务交给事件循环

`QTimer` 是 Qt 中最常用的高层定时器。它不创建线程，也不保证在某个绝对时刻执行代码；它向所属线程的事件循环注册一个定时事件，在到期后发出 `timeout()`，由你连接的槽或回调完成实际工作。

它适合：

- 周期刷新 UI、轮询轻量状态、更新时钟显示。
- 延迟执行一次操作，例如等待控件稳定后再布局。
- 用单线程事件循环分批处理任务，避免一次性阻塞界面。
- 在有事件循环的 worker 线程中周期处理属于该线程的工作。

它不适合：

- 高精度硬实时控制。普通操作系统和 GUI 事件循环都可能延迟回调。
- 需要独立并行执行的耗时任务。定时器槽本身仍然运行在对象所属线程。
- 需要超过约 24 天或纳秒级长期计时的场景。Qt 6.8 起可以考虑 `QChronoTimer`。

```cpp
#include <QCoreApplication>
#include <QTimer>

int main(int argc, char **argv)
{
    QCoreApplication app(argc, argv);

    QTimer timer;
    timer.setInterval(1000);
    QObject::connect(&timer, &QTimer::timeout, [] {
        qInfo() << "tick";
    });
    timer.start();

    QTimer::singleShot(5000, &app, &QCoreApplication::quit);
    return app.exec();
}
```

## 定时器的工作模型

一个 `QTimer` 的基本流程是：

1. 创建对象并确定 parent/线程归属。
2. 连接 `timeout()`。
3. 设置间隔、定时器类型和是否单次。
4. 在对象所属线程调用 `start()`。
5. 事件循环到期后投递定时事件，Qt 发出 `timeout()`。
6. 周期定时器继续注册下一次；单次定时器触发后停止。

`QTimer` 只负责调度通知，不负责保证工作完成时间。如果 `timeout()` 槽执行了 500 ms，而定时器间隔是 100 ms，事件循环会被这个槽占住，后续通知只能延迟处理。定时器不是把槽函数放进后台线程的快捷方式。

## 生命周期、线程和事件循环

`QTimer` 是 `QObject`。给它设置 parent 是最常见的生命周期管理方式：

```cpp
auto *timer = new QTimer(this);
connect(timer, &QTimer::timeout, this, &Controller::poll);
timer->start(1000);
```

定时器依赖所属线程的 Qt 事件循环。GUI 线程通常由 `QApplication`/`QCoreApplication::exec()` 提供；非 GUI 线程必须运行自己的事件循环，例如通过 `QThread::exec()`。

Qt 根据 `QTimer` 的 thread affinity 决定在哪个线程发出 `timeout()`。因此必须在定时器所属线程启动和停止它，不能从其它线程直接调用 `start()` 或 `stop()`。要跨线程控制，使用 queued signal/slot 或把调用投递到目标线程。

对象被移动到其它线程时，先停止定时器，再移动对象，最后在目标线程重新启动。不要让一个活动定时器跨线程漂移。

## 周期定时器和单次定时器

默认 `singleShot` 是 `false`，每隔 `interval` 毫秒重复触发。需要停止时调用 `stop()`；重新调用 `start()` 会从新的周期开始。

```cpp
timer.setSingleShot(false);
timer.start(1000);

// 需要时停止
timer.stop();
```

单次定时器只触发一次：

```cpp
timer.setSingleShot(true);
timer.start(250);
```

如果只是延迟一次回调，不需要保留一个 `QTimer` 对象，可以用静态 `QTimer::singleShot()`。带 `context` 的形式更安全：context 在间隔到期前销毁时，回调不会执行，回调会投递到 context 所在线程的事件循环。

```cpp
QTimer::singleShot(250, this, [this] {
    refreshCaption();
});
```

使用无 context 的 lambda 时，Qt 不会替你管理 lambda 捕获的业务对象。不要在延迟回调里捕获可能提前销毁的裸指针；优先传入合适的 context，或使用 `QPointer`/明确的生命周期管理。

## 间隔、重新启动与边界值

`interval` 单位是毫秒，默认值是 `0`。修改正在运行的定时器间隔会先停止再重新启动，并取得新的定时器 ID；它不是从原来的剩余时间平滑调整。

- `interval > 0`：按照普通延迟/周期语义工作。
- `interval == 0`：在当前事件队列暂时清空后尽快触发，和其它事件的先后顺序未定义。
- Qt 6.10 起 `interval < 0`：产生运行时警告并重置为 1 ms。业务代码仍应主动拒绝负数，避免把版本差异藏在运行时。

```cpp
if (interval < 0)
    throw std::invalid_argument("timer interval must be non-negative");

timer.start(interval);
```

零间隔定时器可以用来分批处理工作：每次 `timeout()` 只处理一个小步骤，并在没有工作后停止。若槽函数持续处理大量任务，零定时器会长期占用事件循环，导致 UI 卡顿和事件饥饿；现代程序更适合把重活交给 worker 线程。

传统 `int` 毫秒间隔的范围受 `int` 和平台实现限制，通常可理解为约正负 24 天。需要更长范围或纳秒精度时，使用 `QChronoTimer`。

## 精度和 `Qt::TimerType`

计时器的“分辨率”不是“实际触发精度”。操作系统负载、线程是否被阻塞、平台计时器能力都会造成延迟。

- `Qt::PreciseTimer`：Qt 尽量保持 1 ms 精度，并且不会比预期更早触发，但仍可能更晚。
- `Qt::CoarseTimer`：允许在间隔的约 5% 范围内提前唤醒，通常是默认值，适合一般周期任务。
- `Qt::VeryCoarseTimer`：允许最多约 500 ms 的提前唤醒，适合不敏感的低频任务。

所有类型都可能晚于预期触发。若系统繁忙导致多个周期同时到期，Qt 会只发出一次 `timeout()`，然后恢复原本的周期，不会为了补齐每一次过期通知而连续发出多次信号。因此不要把 `timeout()` 次数当作精确经过的周期数；需要计算真实进度时，在槽里读取单调时钟或根据业务时间戳补偿。

## 查看状态和剩余时间

`isActive()` 表示定时器当前是否运行。`remainingTime()` 的返回值有明确的三态语义：

- `-1`：定时器未激活。
- `0`：已到期或已经 overdue。
- 正数：预计剩余毫秒数。

`remainingTimeAsDuration()` 返回 `std::chrono::milliseconds`。未运行或无法取得剩余时间时返回负时长；已到期时返回零时长。

这些值是诊断和界面展示信息，不是调度契约。不要通过轮询 `remainingTime()` 来代替 `timeout()`。

Qt 6.8 起 `id()` 返回 `Qt::TimerId`。定时器未运行时返回 `Qt::TimerId::Invalid`；修改间隔、重启定时器时 ID 会变化。ID 适合诊断，不适合保存成跨生命周期的业务标识。

## `singleShot()` 的重载选择

Qt 6 支持传统整数毫秒和 `std::chrono` 时长。新代码优先使用带单位的 chrono：

```cpp
using namespace std::chrono_literals;

QTimer::singleShot(250ms, this, &Controller::refresh);
QTimer::singleShot(2s, Qt::PreciseTimer, this, [this] {
    saveLater();
});
```

带 context 的 functor 形式可以自动处理 context 的销毁和线程投递。旧式 `receiver + const char *member` 仍可用，但编译期检查能力较弱；现代 C++ 代码优先使用成员函数指针或 lambda。

Qt 6.8 以前 chrono 重载的接口细节不同，Qt 6.8 起内部可使用纳秒表示；如果项目要兼容更低版本，应以最低 Qt 版本的声明为准，并注意极大毫秒值转换时的溢出风险。

## `callOnTimeout()` 与连接生命周期

`callOnTimeout()` 是把 `timeout()` 连接到 functor 的便捷写法，并返回 `QMetaObject::Connection`：

```cpp
auto connection = timer.callOnTimeout(this, [this] {
    pollOnce();
});
```

带 context 的重载会把调用放进 context 的事件循环，并在 context 销毁时自动断开。无 context 的重载等价于使用 `DirectConnection`，而且在定义了 `QT_NO_CONTEXTLESS_CONNECT` 时不可用；需要明确生命周期或线程语义时，应使用带 context 的重载或直接调用 `QObject::connect()`。

## 替代方案

- `QChronoTimer`：Qt 6.8 起提供，更大的时间范围和纳秒级 `std::chrono` 表示。
- `QBasicTimer`：轻量值类型，配合自定义 `timerEvent()`，适合已有 QObject 想减少信号连接开销的场景。
- `QObject::startTimer()` / `killTimer()`：更底层的定时器 ID 接口，需要自己重写 `timerEvent()`。
- `QElapsedTimer`：测量耗时，不负责周期通知。

多数应用优先使用 `QTimer`。只有在需要更低层控制、特殊性能约束或不同时间范围时才换方案。

## 常见错误

- 以为 `QTimer` 会创建后台线程。它只在所属线程的事件循环中发出信号。
- 在另一个线程直接调用 `start()` 或 `stop()`。必须在定时器所属线程操作。
- 让 `timeout()` 槽执行长时间阻塞工作。后续事件和 UI 都会被拖住。
- 把零间隔当作高性能任务队列。零定时器会占用事件循环，任务应拆小或移到 worker。
- 把每次 `timeout()` 当作严格周期。系统繁忙时过期事件可能合并成一次信号。
- 用 `remainingTime()` 做精确倒计时。它是当前调度状态的估计值。
- 无 context 的 lambda 捕获已经销毁的对象。延迟回调应绑定到合适的 context。
- 忘记重载歧义。连接 `start()` 时用 `qOverload<>(&QTimer::start)` 或 lambda 明确选择。
- 需要 30 天以上间隔仍使用 `QTimer`。应考虑 `QChronoTimer` 或持久化的日期时间计划。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QTimer(QObject *parent = nullptr)` | 创建定时器 | 对象属于当前线程；parent 负责生命周期 |
| `~QTimer()` | 销毁定时器 | 销毁时停止定时器；不要重复释放 QObject |
| `start()` | 按当前 interval 启动 | 已运行时会重新开始周期；需要明确重载时用 `qOverload<>` |
| `start(int msec)` | 设置间隔并启动 | 运行中会停止再重启；负值在 Qt 6.10 起警告并变为 1 ms |
| `start(std::chrono::milliseconds)` | 用 chrono 间隔启动 | 用类型表达单位，仍受事件循环和平台精度影响 |
| `stop()` | 停止定时器 | 停止后 `isActive()` 为 false，剩余时间通常为 -1 |
| `timeout()` | 监听到期事件 | 信号在定时器所属线程发出；周期过期可能合并通知 |
| `setInterval(int)` / `setInterval(milliseconds)` | 修改间隔 | 默认 0；修改运行中定时器会重启并更换 ID |
| `interval()` | 读取毫秒间隔 | 返回配置值，不代表实际触发精度 |
| `intervalAsDuration()` | 以 chrono 读取间隔 | 返回 `std::chrono::milliseconds` |
| `isActive()` | 判断是否运行 | 等价于 `active` 属性读取 |
| `bindableActive()` | 访问 active 绑定 | 只读 bindable |
| `remainingTime()` | 读取剩余毫秒数 | 未运行 `-1`；已到期 `0`；否则为正数 |
| `remainingTimeAsDuration()` | 读取剩余时长 | 未运行/无法取得时为负时长；已到期为零 |
| `setSingleShot(bool)` | 设置是否单次 | `true` 只触发一次；默认 `false` |
| `isSingleShot()` | 查询是否单次 | 只描述模式，不表示当前是否已经触发 |
| `bindableSingleShot()` | 访问单次属性绑定 | 支持 `QProperty` |
| `setTimerType(Qt::TimerType)` | 设置精度/唤醒策略 | `PreciseTimer` 不提前，`CoarseTimer` 默认允许约 5% 提前，`VeryCoarseTimer` 允许约 500 ms 提前 |
| `timerType()` | 查询定时器类型 | 默认 `Qt::CoarseTimer` |
| `bindableTimerType()` | 访问类型属性绑定 | 支持 `QProperty` |
| `timerId()` | 读取旧式整数 ID | 未运行时表示无有效运行 ID |
| `id()` | 读取 `Qt::TimerId` | Qt 6.8 起提供；未运行返回 `Qt::TimerId::Invalid` |
| `QTimer::singleShot(interval, context, functor)` | 延迟执行一次 functor | context 销毁则不调用；回调在 context 所在线程事件循环中执行 |
| `QTimer::singleShot(interval, timerType, context, functor)` | 指定类型的单次回调 | 适合对提前/精度有明确要求的延迟任务 |
| `QTimer::singleShot(interval, functor)` | 无 context 的单次回调 | 要自行保证捕获对象生命周期；事件循环仍是前提 |
| `QTimer::singleShot(interval, receiver, member)` | 旧式单次槽调用 | 兼容性好但类型检查较弱；新代码优先 functor |
| `callOnTimeout(functor)` | 便捷连接 timeout | 无 context 形式使用 DirectConnection，受 `QT_NO_CONTEXTLESS_CONNECT` 影响 |
| `callOnTimeout(context, functor, connectionType)` | 带上下文连接 timeout | context 销毁时自动断开，并按连接类型投递 |
| `timerEvent(QTimerEvent *)` | 内部定时器事件处理 | protected 重写点；需要底层控制时才考虑 |
