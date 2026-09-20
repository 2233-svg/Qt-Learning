# Qt QBasicTimer 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QBasicTimer>`  
> 所属模块：`Qt6::Core`  
> 继承：无

## 1. 先理解它负责哪一层定时

Qt 里常见的定时需求大致分成三层：

| 层次 | 典型类型 | 主要特点 | 适合解决的问题 |
| --- | --- | --- | --- |
| 高层信号接口 | `QTimer` | 有 `timeout()` 信号，可配置 interval、single-shot 和 timer type。 | 业务逻辑、界面刷新、延迟执行。 |
| 轻量事件接口 | `QBasicTimer` | 只保存一个 timer ID，超时后给目标 `QObject` 发送 `QTimerEvent`。 | 自定义 `QObject` 内部的重复性定时事件。 |
| 更底层 ID 接口 | `QObject::startTimer()` | 直接管理 timer ID，并在 `timerEvent()` 中自己分流。 | 需要直接使用 QObject 定时器机制的底层代码。 |

`QBasicTimer` 是一个轻量、低层的值类型。它本身不会发信号，也不提供回调函数；它只是帮助你启动和停止一个定时器，并把事件送到指定 `QObject` 的 `timerEvent()`。

Qt 官方对应用层定时通常推荐 `QTimer`。选择 `QBasicTimer` 的理由一般不是“功能更多”，而是：

- 不需要额外创建一个 `QObject` 定时器对象。
- 不需要建立 `timeout()` 信号连接。
- 只想在已有 `QObject` 的 `timerEvent()` 中处理定时事件。
- 需要把多个轻量定时器作为 move-only 值放进容器。

## 2. 最小可用模型：对象接收事件，QBasicTimer 只负责登记

一个完整的 `QBasicTimer` 使用流程是：

1. 在 `QObject` 子类里保存一个 `QBasicTimer` 成员。
2. 调用 `start()`，把超时时间和接收对象传进去。
3. Qt 事件循环到期后向接收对象发送 `QTimerEvent`。
4. 在接收对象重载的 `timerEvent()` 中判断事件是否来自这个定时器。
5. 需要停止时调用 `stop()`。

```cpp
#include <QBasicTimer>
#include <QTimerEvent>
#include <QObject>

class Poller final : public QObject
{
public:
    explicit Poller(QObject *parent = nullptr)
        : QObject(parent)
    {
        m_timer.start(std::chrono::seconds(1), this);
    }

protected:
    void timerEvent(QTimerEvent *event) override
    {
        if (event->id() == m_timer.id()) {
            pollOnce();
            return;
        }

        QObject::timerEvent(event);
    }

private:
    void pollOnce()
    {
        // 读取一次状态、刷新缓存或执行周期性检查。
    }

    QBasicTimer m_timer;
};
```

这个例子里，`QBasicTimer` 不执行 `pollOnce()`；真正处理事件的是 `Poller::timerEvent()`。定时器只是把一个 Qt timer ID 封装成可自动停止、可移动的对象。

`QBasicTimer` 是重复定时器。只要不调用 `stop()`，目标对象会继续收到后续的 timer event。需要一次性执行时，应使用 `QTimer::singleShot()` 或 `QTimer` 的 single-shot 模式。

## 3. 事件循环和线程归属是前置条件

`QBasicTimer` 的超时不是独立线程回调，而是通过目标 `QObject` 所在线程的 Qt 事件循环投递 `QTimerEvent`。因此：

- 目标线程必须有正在运行的 Qt 事件循环。
- `start()` 和 `stop()` 应在目标对象所属线程中调用。
- 没有事件循环时，定时事件不会按预期到达。
- 事件循环被长时间阻塞时，事件会延迟，定时器不是实时调度器。

例如，下面的代码启动了定时器，但如果线程没有进入 `exec()`，就没有事件循环负责派发事件：

```cpp
QThread workerThread;
Poller poller;
poller.moveToThread(&workerThread);

workerThread.start();
// 还要确保 workerThread 的事件循环正在运行，
// 并在 poller 所在线程中启动和停止定时器。
```

不要从 GUI 线程直接操作属于工作线程的 `QBasicTimer`，也不要把它误认为线程安全的同步计时器。若定时逻辑要放在工作线程，通常让一个 `QObject` 工作对象进入该线程，并通过信号或队列调用在目标线程中启动定时器。

## 4. QBasicTimer 和 QTimer 怎么选

### 4.1 用 `QTimer` 的情况

优先使用 `QTimer` 的典型场景：

- 需要连接 `timeout()` 信号。
- 需要随时设置和读取 interval。
- 需要 `setSingleShot(true)` 或调用 `QTimer::singleShot()`。
- 需要通过属性系统、绑定系统或 Qt Designer 风格的高层对象接口管理定时器。
- 代码更重视可读性和业务表达，而不是减少一个轻量包装。

```cpp
auto *timer = new QTimer(this);
connect(timer, &QTimer::timeout, this, &Poller::pollOnce);
timer->start(1000);
```

### 4.2 用 `QBasicTimer` 的情况

`QBasicTimer` 适合已经有明确 `timerEvent()` 处理入口的低层 `QObject`：

- 自定义控件、事件驱动对象或 Qt 风格基础设施。
- 一个对象管理多个 timer，需要用 ID 分流。
- 不希望为每个周期性事件创建独立 `QTimer` 对象。
- 需要一个不能复制、但能移动的 timer 值类型。

如果只是想“每隔一秒执行一个成员函数”，`QTimer` 通常更直观；如果你已经在实现 `timerEvent()`，`QBasicTimer` 往往更贴合这套机制。

## 5. 时间类型与版本变化

### 5.1 `Duration` 的用途

```cpp
using Duration = QAbstractEventDispatcher::Duration;
```

在 Qt 6.11.1 的当前实现中，`QAbstractEventDispatcher::Duration` 是 `std::chrono::nanoseconds`。`QBasicTimer::Duration` 通过类型别名复用它，而不是把公共 API 永久绑定到某一个固定精度。

推荐使用 chrono 字面量或显式 duration：

```cpp
using namespace std::chrono_literals;

m_timer.start(250ms, this);
m_timer.start(2s, Qt::PreciseTimer, this);
```

### 5.2 Qt 6.5、6.8、6.9、6.10 的边界

- `QBasicTimer::start(Duration, ...)` 重载从 Qt 6.5 开始提供。
- Qt 6.8 引入 `Qt::TimerId`，`id()` 返回这个强类型 ID。
- 从 Qt 6.9 起，chrono 形式的 `Duration` 使用纳秒粒度；这一变化保持向后兼容。
- Qt 6.10 起，负时间间隔会产生运行时警告，并被重置为 `1ms`。不要依赖这个兜底行为，业务代码应在启动前校验时间间隔。
- 旧的 `start(int, ...)` 和 `timerId()` 仍用于兼容旧代码，但新的代码优先使用 chrono 重载和 `id()`。

`Qt::TimerId::Invalid` 表示无效或未运行的定时器 ID。不要仅凭一个普通整数的正负值推断新 API 的状态；使用 `isActive()` 或与 `Qt::TimerId::Invalid` 比较。

## 6. 定时精度和重复触发

不论使用 `QBasicTimer` 还是 `QTimer`，超时都受操作系统、硬件和事件循环负载影响：

- `Qt::PreciseTimer` 尽量提供更高精度，并不会早于预期触发。
- `Qt::CoarseTimer` 允许一定程度的提前唤醒，通常更节省系统资源。
- `Qt::VeryCoarseTimer` 适合不需要精确时间的低频任务。
- 系统忙或事件循环阻塞时，事件可能晚到。

不应把 `QBasicTimer` 当成高精度测量工具。测量真实经过时间应配合 `QElapsedTimer` 或 `std::chrono::steady_clock`；定时器只负责在事件循环中“提醒你可以处理一次工作”。

定时器事件晚到时，也不要在 `timerEvent()` 中假设每一个理论周期都会对应一个事件。对于周期任务，如果业务要求不丢次数，应自行记录时间并补偿；如果业务只关心“现在该刷新了”，收到一次事件后做一次刷新通常就足够。

## 7. 多个 QBasicTimer 如何分流事件

同一个 `QObject` 可以启动多个定时器，所有事件都会进入同一个 `timerEvent()`。此时用每个定时器的 `id()` 与 `QTimerEvent::id()` 比较：

```cpp
class Dashboard final : public QObject
{
protected:
    void timerEvent(QTimerEvent *event) override
    {
        if (event->id() == m_refreshTimer.id()) {
            refresh();
        } else if (event->id() == m_expireTimer.id()) {
            expireOldEntries();
        } else {
            QObject::timerEvent(event);
        }
    }

private:
    void refresh() {}
    void expireOldEntries() {}

    QBasicTimer m_refreshTimer;
    QBasicTimer m_expireTimer;
};
```

在 Qt 6.9 及以后，也可以使用 `QTimerEvent::matches(const QBasicTimer &)` 做匹配：

```cpp
void timerEvent(QTimerEvent *event) override
{
    if (event->matches(m_refreshTimer)) {
        refresh();
        return;
    }

    QObject::timerEvent(event);
}
```

`matches()` 属于 `QTimerEvent` 的 API，不是 `QBasicTimer` 的成员；这里把它列出来是为了说明两者在实际事件处理中如何协作。

## 8. 生命周期、移动语义和析构行为

### 8.1 默认构造得到非活动定时器

```cpp
QBasicTimer timer;
Q_ASSERT(!timer.isActive());
```

默认构造不会注册系统定时器，也不会绑定目标对象。调用 `start()` 后才开始拥有有效的 timer ID。

### 8.2 不能复制，只能移动

`QBasicTimer` 禁止拷贝，允许移动。这是有意设计：复制一个活动 timer 会产生“两个 C++ 对象是否共同代表同一个系统定时器”的歧义，因此 Qt 不允许这种复制。

移动构造后：

- 新对象接管原 timer 的 ID。
- 被移动对象变为非活动状态。

移动赋值前，目标对象原来代表的 timer 会被停止；赋值后目标接管源对象的 timer，源对象保持非活动状态。

```cpp
QBasicTimer first;
first.start(1s, object);

QBasicTimer second = std::move(first);
Q_ASSERT(!first.isActive());
Q_ASSERT(second.isActive());
```

这使它可以放进支持 move-only 元素的容器，例如 `std::vector<QBasicTimer>`，但要留意容器移动元素时不会改变 timer 所属的目标 `QObject`；真正的事件仍发送给 `start()` 时传入的对象。

### 8.3 析构会停止活动定时器

析构活动的 `QBasicTimer` 会停止它所代表的定时器。因此把它作为 `QObject` 成员是自然的用法：宿主对象销毁时，成员析构会清理 timer。

如果 `QBasicTimer` 是局部变量，离开作用域就会停止：

```cpp
void startTemporarily(QObject *object)
{
    QBasicTimer timer;
    timer.start(1s, object);
} // timer 析构，定时器随即停止
```

这段代码不会创建一个持续到函数返回之后的定时器。需要长期运行时，必须让 `QBasicTimer` 的生命周期覆盖整个运行期，通常把它作为对象成员。

## 9. 每个 API 的作用与用法

### 9.1 `QBasicTimer()`

```cpp
constexpr QBasicTimer() noexcept
```

构造一个非活动的基本定时器。它只初始化内部状态，不向事件分发器注册定时器。

适合在类成员声明、局部准备阶段或容器中创建。真正启动需要之后调用 `start()`。

### 9.2 `QBasicTimer(QBasicTimer &&other)`

```cpp
QBasicTimer(QBasicTimer &&other) noexcept
```

移动构造，把 `other` 所代表的 timer 转移给新对象，并使 `other` 变为非活动状态。

它是 move-only 语义的一部分，常见于把 timer 放入容器或返回一个拥有活动状态的临时对象。移动之后不要继续把 `other` 当作活动定时器使用。

### 9.3 `~QBasicTimer()`

```cpp
~QBasicTimer() noexcept
```

销毁对象；如果当前 timer 处于活动状态，会停止该定时器。

析构本身不需要手动先调用 `stop()`，但仍应保证析构发生在正确的线程上下文中，尤其是 timer 关联的对象属于带事件循环的工作线程时。

### 9.4 `id()`

```cpp
Qt::TimerId id() const noexcept
```

返回当前 timer 的强类型 ID。它用于把 `QTimerEvent::id()` 与某个 `QBasicTimer` 对应起来，也可用于日志和诊断。

从 Qt 6.8 开始提供。未启动或已经停止的 timer 返回 `Qt::TimerId::Invalid`。

```cpp
if (event->id() == timer.id())
    handleTimeout();
```

不要把这个 ID 当作跨进程、跨线程或永久稳定的业务编号；它只是当前事件循环中的定时器标识。

### 9.5 `isActive()`

```cpp
bool isActive() const noexcept
```

判断 timer 当前是否已经启动且尚未停止。

它适合在停止、重启和调试逻辑中读取状态：

```cpp
if (m_timer.isActive())
    m_timer.stop();
```

它只反映 `QBasicTimer` 当前是否持有活动 timer，不代表目标对象一定仍然存在，也不代表事件已经准确按时派发。

### 9.6 `start(Duration duration, QObject *object)`

```cpp
void start(QBasicTimer::Duration duration, QObject *object)
```

启动或重启定时器，把周期性 timer event 发送给 `object`。这个重载默认使用 `Qt::CoarseTimer`。

如果当前已经活动，调用 `start()` 会重新启动它。一个 `QBasicTimer` 同时只代表一个 timer；重启后旧的计时状态被替换。

```cpp
m_timer.start(500ms, this);
```

`object` 必须是有效的 `QObject` 指针，并且其线程需要有事件循环。目标对象不由 `QBasicTimer` 所有，也不会因为被传给 `start()` 而改变父子关系。

### 9.7 `start(Duration duration, Qt::TimerType timerType, QObject *obj)`

```cpp
void start(QBasicTimer::Duration duration,
           Qt::TimerType timerType,
           QObject *obj)
```

以指定的 `Qt::TimerType` 启动或重启定时器，并让 `obj` 接收 timer event。

```cpp
m_timer.start(16ms, Qt::PreciseTimer, this);
```

`timerType` 是精度与资源开销之间的策略选择，不是对实际触发时间的硬保证。即使选择 `PreciseTimer`，线程被阻塞时事件仍可能延迟。

### 9.8 `stop()`

```cpp
void stop()
```

停止当前定时器。停止后不会再发送后续 timer event，`isActive()` 返回 `false`，`id()` 返回无效 ID。

重复调用 `stop()` 是安全的，非活动状态下调用不会产生新的定时器。

### 9.9 `swap(QBasicTimer &other)`

```cpp
void swap(QBasicTimer &other) noexcept
```

交换两个 `QBasicTimer` 对象所持有的 timer ID。操作不抛异常且很快。

交换的是 timer 的包装状态，不会把目标 `QObject` 重新绑定到另一个对象；每个 timer ID 原本关联的事件接收对象保持不变。

这对 move assignment 和需要交换容器元素的代码有用，普通业务代码很少需要直接调用。

### 9.10 `operator=(QBasicTimer &&other)`

```cpp
QBasicTimer &operator=(QBasicTimer &&other) noexcept
```

移动赋值。目标对象原先持有的活动 timer 会被停止，然后接管 `other` 的 timer；`other` 变为非活动状态。

```cpp
QBasicTimer current;
QBasicTimer replacement;
replacement.start(1s, object);

current = std::move(replacement);
```

不要在移动赋值后继续使用源对象的 `id()` 来匹配事件；应使用接管 timer 的目标对象。

### 9.11 相关非成员 `swap`

```cpp
void swap(QBasicTimer &lhs, QBasicTimer &rhs) noexcept
```

调用 `lhs.swap(rhs)` 交换两个 timer。它存在的意义是支持通用的 `swap(lhs, rhs)` 写法和标准库交换习惯。

## 10. 旧 API 与不建议的新代码写法

Qt 6.11.1 仍提供以下兼容接口：

```cpp
void start(int msec, QObject *object);
void start(int msec, Qt::TimerType timerType, QObject *obj);
int timerId() const noexcept;
```

它们主要用于兼容旧版本代码：

- `start(int, ...)` 用毫秒整数启动，新的代码可使用 `std::chrono` duration。
- `timerId()` 返回 `int`，新的代码优先使用返回 `Qt::TimerId` 的 `id()`。
- 旧接口在文档中已经标记为废弃，迁移时不需要改变定时器的整体工作模型，只需替换参数类型和 ID 查询方式。

## 11. 常见误区与排查顺序

### 11.1 定时器启动了但没有事件

按以下顺序检查：

1. `object` 是否为有效的 `QObject`。
2. `m_timer.isActive()` 是否为 `true`。
3. `start()` 是否在目标对象所属线程中调用。
4. 目标线程是否运行 Qt 事件循环。
5. `timerEvent()` 是否真的在目标类中重载，并且没有被错误逻辑提前吞掉。
6. 处理函数或其他代码是否长时间阻塞了事件循环。

### 11.2 在 `timerEvent()` 里没有判断 ID

一个对象可能有多个 `QBasicTimer`，也可能同时接收其他来源的 timer event。不要看到 `timerEvent()` 被调用就默认它一定属于某一个成员定时器，应通过 `event->id()` 或 `event->matches(timer)` 判断。

### 11.3 把它当作 single-shot timer

`QBasicTimer` 是重复定时器。要只执行一次，应在第一次匹配到事件时调用 `stop()`，或者直接使用 `QTimer::singleShot()`。

```cpp
void timerEvent(QTimerEvent *event) override
{
    if (event->id() == m_timer.id()) {
        m_timer.stop();
        doOnce();
    }
}
```

### 11.4 把定时器精度当成实时保证

`start(16ms, Qt::PreciseTimer, ...)` 表示选择更精确的计时策略，不表示 `timerEvent()` 一定每 16 毫秒准时进入。UI 线程、工作线程或系统调度繁忙时都可能延迟。

### 11.5 用局部变量启动长期定时器

`QBasicTimer` 离开作用域会析构并停止。长期定时器应作为宿主对象成员，或由生命周期明确的管理对象持有。

### 11.6 跨线程启动和停止

`QBasicTimer` 自身是轻量值类型，但它操作的是目标对象线程中的事件分发器。不要因为它不是 `QObject` 就认为可以从任意线程调用 `start()` 或 `stop()`。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型别名 | `using QBasicTimer::Duration = QAbstractEventDispatcher::Duration` | 表示 `start()` 使用的 chrono duration 类型；Qt 6.11.1 当前为 `std::chrono::nanoseconds`。 | 使用 `std::chrono` 时注意 Qt 版本；不要把定时器当成高精度时间测量工具。 |
| 构造 | `constexpr QBasicTimer() noexcept` | 创建一个非活动的基本定时器。 | 不会注册系统定时器，必须调用 `start()` 才会产生事件。 |
| 移动构造 | `QBasicTimer(QBasicTimer &&other) noexcept` | 接管 `other` 的 timer，并让 `other` 变为非活动状态。 | `QBasicTimer` 不能复制；移动后不要继续使用源对象代表原 timer。 |
| 析构 | `~QBasicTimer() noexcept` | 销毁包装对象，活动 timer 会被停止。 | 成员析构适合自动清理；跨线程对象要在正确线程处理生命周期。 |
| 状态查询 | `Qt::TimerId id() const noexcept` | 返回当前 timer 的强类型 ID。 | Qt 6.8 引入；未活动时是 `Qt::TimerId::Invalid`，不要当永久业务 ID 保存。 |
| 状态查询 | `bool isActive() const noexcept` | 判断 timer 是否处于运行状态。 | 只表示当前包装状态，不保证事件已经准时送达。 |
| 启动 | `void start(Duration duration, QObject *object)` | 以默认的 `Qt::CoarseTimer` 周期性发送 timer event。 | 目标对象线程必须有事件循环；已活动时会重启。 |
| 启动 | `void start(Duration duration, Qt::TimerType timerType, QObject *obj)` | 以指定 timer type 启动或重启，并把事件发送给目标对象。 | 精度策略不是实时保证；负 duration 在 Qt 6.10 起会警告并重置为 1ms。 |
| 停止 | `void stop()` | 停止 timer，后续不再发送事件。 | 停止后 `isActive()` 为 `false`，`id()` 为无效 ID；重复调用安全。 |
| 成员交换 | `void swap(QBasicTimer &other) noexcept` | 交换两个包装对象持有的 timer ID。 | 只交换包装状态，不改变每个 timer 原本关联的目标对象。 |
| 移动赋值 | `QBasicTimer &operator=(QBasicTimer &&other) noexcept` | 停止目标原 timer，并接管 `other` 的 timer。 | 源对象会变为非活动状态，目标原来的 timer 不会保留。 |
| 非成员交换 | `void swap(QBasicTimer &lhs, QBasicTimer &rhs) noexcept` | 以通用 `swap(lhs, rhs)` 形式交换两个 timer。 | 与成员 `swap()` 具有相同语义，普通代码通常无需直接调用。 |
| 兼容 API | `void start(int msec, QObject *object)` | 用毫秒整数启动或重启重复定时器。 | 旧接口已废弃，新代码优先使用 chrono duration。 |
| 兼容 API | `void start(int msec, Qt::TimerType timerType, QObject *obj)` | 用毫秒整数和指定 timer type 启动或重启定时器。 | 旧接口已废弃，注意负整数间隔的版本差异。 |
| 兼容 API | `int timerId() const noexcept` | 以旧的 `int` 形式返回 timer ID。 | 新代码优先使用 `id()` 的 `Qt::TimerId`；不要混淆 `QTimerEvent::timerId()`。 |

---

### 一句话总结

`QBasicTimer` 是一个只保存 timer ID 的轻量、可移动值类型：它把周期性定时事件送进指定 `QObject` 的 `timerEvent()`，适合低层事件驱动代码；需要信号、single-shot、属性和更高层控制时，应选择 `QTimer`。
