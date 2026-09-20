# QAbstractEventDispatcherV2 事件分发器过渡接口深入笔记

> 适用版本：Qt 6.8 到 Qt 6.x，本文按 Qt 6.11.1 的接口说明  
> 头文件：`#include <QAbstractEventDispatcherV2>`  
> 所属模块：`Qt6::Core`  
> 继承关系：`QObject -> QAbstractEventDispatcher -> QAbstractEventDispatcherV2`

## 1. 它为什么存在

`QAbstractEventDispatcherV2` 不是一个新的业务事件循环，也不是比 `QAbstractEventDispatcher` 更高级的日常使用类。它是 Qt 6 中为了迁移事件分发器定时器接口而引入的过渡层。

Qt 旧的 dispatcher 定时器接口长期使用：

```cpp
int timerId;
qint64 interval; // 毫秒语义
```

Qt 6.8 开始把方向改成：

```cpp
Qt::TimerId timerId;
QAbstractEventDispatcher::Duration interval; // std::chrono 风格
```

问题在于 `QAbstractEventDispatcher` 原本已经有一组纯虚函数。如果直接在 Qt 6 中替换纯虚函数，会让现有自定义 dispatcher 子类全部破坏 ABI 或源码兼容。于是 Qt 引入 `QAbstractEventDispatcherV2`：让愿意迁移的实现类先继承 V2，在 Qt 6 阶段提供新接口；等 Qt 7 时，再把这些新接口合并回 `QAbstractEventDispatcher`。

所以这类文件最重要的不是构造函数和析构函数，而是这句话：

```text
它是 Qt 6 到 Qt 7 之间，事件分发器定时器 API 从 int/毫秒迁移到 Qt::TimerId/chrono 的桥。
```

## 2. 谁需要关心它

普通 Qt 应用通常不用直接接触 `QAbstractEventDispatcherV2`。如果你只是：

- 使用 `QTimer`；
- 在对象里重写 `timerEvent()`；
- 用 `QObject::startTimer()` 和 `killTimer()`；
- 调用 `QCoreApplication::processEvents()`；
- 使用 `QTcpSocket`、`QSocketNotifier`；

那么你主要理解 `QTimer`、`QObject`、`QEventLoop` 和 `QAbstractEventDispatcher` 的行为即可。

你需要认真看 `QAbstractEventDispatcherV2` 的场景通常是：

- 自己实现事件分发器；
- 把 Qt 事件循环接入 libuv、glib、游戏引擎主循环或其他外部 loop；
- 维护一套跨 Qt 6 和 Qt 7 的底层平台适配代码；
- 把旧的 `registeredTimers()`、`remainingTime(int)`、`registerTimer(int, qint64, ...)` 迁移到新式 chrono 接口。

## 3. 它和 `QAbstractEventDispatcher` 的关系

继承关系是：

```text
QAbstractEventDispatcher
  └─ QAbstractEventDispatcherV2
```

在 Qt 6.11.1 头文件中，V2 在 `QT_VERSION < 7.0.0` 时是一个真实类；Qt 7 开始会变成：

```cpp
using QAbstractEventDispatcherV2 = QAbstractEventDispatcher;
```

这意味着：

- Qt 6 中继承 V2，是为了提前实现 Qt 7 方向的新虚函数。
- Qt 7 中 V2 不再是额外层级，只是兼容名称。
- 迁移代码时，不要把 V2 当成长期独立抽象；它的身份就是过渡。

## 4. V2 新增或强调的定时器虚函数

V2 声明了新式定时器纯虚函数：

```cpp
virtual void registerTimer(Qt::TimerId timerId,
                           Duration interval,
                           Qt::TimerType timerType,
                           QObject *object) = 0;

virtual bool unregisterTimer(Qt::TimerId timerId) = 0;

virtual QList<TimerInfoV2> timersForObject(QObject *object) const = 0;

virtual Duration remainingTime(Qt::TimerId timerId) const = 0;
```

这组函数解决的是同一个问题：dispatcher 内部不能再只按 `int` 和毫秒组织定时器状态，而要用 Qt 专门的 timer ID 类型和 chrono duration。

一个自定义 dispatcher 的内部 timer 记录，至少应该能表达：

```cpp
struct TimerRecord
{
    Qt::TimerId id;
    QAbstractEventDispatcher::Duration interval;
    Qt::TimerType type;
    QObject *receiver;
    QDeadlineTimer nextDeadline;
};
```

这不是 Qt 要求你必须这样写的结构，只是说明 V2 接口会逼着实现者保留这些语义。否则 `timersForObject()`、`remainingTime()` 和取消定时器时就会丢信息。

## 5. 它如何桥接旧接口

Qt 6 中 `QAbstractEventDispatcher` 仍保留旧的纯虚函数：

```cpp
virtual void registerTimer(int timerId,
                           qint64 interval,
                           Qt::TimerType timerType,
                           QObject *object) = 0;

virtual bool unregisterTimer(int timerId) = 0;
virtual QList<TimerInfo> registeredTimers(QObject *object) const = 0;
virtual int remainingTime(int timerId) = 0;
```

V2 在内部把这些旧接口做成 final override，然后把长期方向转给新接口。对实现者来说，含义是：

- 继承 `QAbstractEventDispatcher`：你面对的是旧式纯虚接口，同时还要注意 Qt 6.8 的新非虚包装。
- 继承 `QAbstractEventDispatcherV2`：你实现新式纯虚接口，旧式接口由 V2 做桥接。

这能减少迁移期的重复实现，也能让底层 dispatcher 的真实状态更早转向 `Qt::TimerId` 和 `Duration`。

## 6. `processEventsWithDeadline()` 是什么

头文件中还有一个 V2 成员：

```cpp
virtual bool processEventsWithDeadline(QEventLoop::ProcessEventsFlags flags,
                                       QDeadlineTimer deadline);
```

源码注释标明它是为后续版本保留的接口。它表达的方向很清楚：事件处理不只由 flags 控制，还可能由一个明确的截止时间控制。

它和普通 `processEvents(flags)` 的区别可以这样理解：

- `processEvents(flags)` 处理符合条件的一批事件，是否等待由 flags 决定。
- `processEventsWithDeadline(flags, deadline)` 额外给出“最多处理到什么时候”的边界。

在 Qt 6.11.1 文档页中，这个成员没有像构造函数那样单独展开说明，所以使用时要以头文件、目标 Qt 版本和实际平台实现为准。库代码不要在没有版本保护的情况下假定所有 Qt 6 小版本都提供完全相同的行为。

## 7. 最小派生轮廓

下面不是可直接运行的完整 dispatcher，只是说明继承 V2 后，你要实现的新式接口长什么样：

```cpp
class MyDispatcher : public QAbstractEventDispatcherV2
{
public:
    using QAbstractEventDispatcherV2::QAbstractEventDispatcherV2;

    bool processEvents(QEventLoop::ProcessEventsFlags flags) override;
    void wakeUp() override;
    void interrupt() override;

    void registerSocketNotifier(QSocketNotifier *notifier) override;
    void unregisterSocketNotifier(QSocketNotifier *notifier) override;

    void registerTimer(Qt::TimerId timerId,
                       Duration interval,
                       Qt::TimerType timerType,
                       QObject *object) override;

    bool unregisterTimer(Qt::TimerId timerId) override;
    bool unregisterTimers(QObject *object) override;
    QList<TimerInfoV2> timersForObject(QObject *object) const override;
    Duration remainingTime(Qt::TimerId timerId) const override;
};
```

要注意，继承 V2 并不会替你实现事件循环本身。你仍然要处理等待、唤醒、打断、socket notifier、原生事件过滤、定时器到期投递等完整 dispatcher 契约。

## 8. 实现时最容易错的地方

### 8.1 只保存毫秒数

如果内部结构仍然只保存 `qint64 msec`，`Duration` 接口就会被迫截断或舍入。迁移到 V2 时，内部状态也应跟着变成 chrono 语义。

### 8.2 把 `Qt::TimerId` 当普通 int 随便转换

`Qt::TimerId` 的意义是让 timer ID 的语义更明确。实现内部可以有必要的兼容转换，但公开边界应尽量保持 `Qt::TimerId`。

### 8.3 忘记 `unregisterTimers(QObject *)`

V2 替换的是部分定时器接口，不代表基类契约消失。对象销毁或批量清理时，仍需要能按对象移除全部定时器。

### 8.4 以为 V2 只需要实现构造和析构

离线文档页只在公共函数列表里展示构造和析构，但头文件中的纯虚定时器接口才是 V2 的重点。读这种过渡类时，一定要结合头文件。

### 8.5 忽略 Qt 7 兼容目标

V2 的存在就是为了让 Qt 7 合并更顺滑。新代码如果还围绕旧接口设计，短期可能能编译，长期维护成本会更高。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造函数 | `QAbstractEventDispatcherV2(QObject *parent = nullptr)` | 构造 V2 事件分发器基类部分 | 抽象类不能直接实例化，通常由自定义 dispatcher 子类调用 |
| 析构函数 | `~QAbstractEventDispatcherV2()` | 多态销毁 V2 dispatcher | 子类要释放外部 loop、timer watcher、I/O watcher 等资源 |
| 新式定时器虚函数 | `registerTimer(Qt::TimerId timerId, Duration interval, Qt::TimerType timerType, QObject *object)` | 按指定新式 ID 和 chrono 间隔登记定时器 | 这是 V2 的核心迁移点，内部状态不要只按整数毫秒保存 |
| 新式定时器虚函数 | `unregisterTimer(Qt::TimerId timerId)` | 取消一个新式 ID 对应的定时器 | 成功移除返回 `true`，找不到或无法移除返回 `false` |
| 新式定时器虚函数 | `timersForObject(QObject *object) const` | 返回某个对象当前登记的 `TimerInfoV2` 列表 | 查询结果应反映 dispatcher 内部真实 timer 状态 |
| 新式定时器虚函数 | `remainingTime(Qt::TimerId timerId) const` | 查询指定定时器距离下一次触发的剩余时间 | 不存在返回负 duration，已经到期但未处理返回零 duration |
| 预留虚函数 | `processEventsWithDeadline(QEventLoop::ProcessEventsFlags flags, QDeadlineTimer deadline)` | 在普通事件处理 flags 之外加入截止时间边界 | Qt 6.11.1 文档页未展开说明，库代码要做版本和行为确认 |
| 继承职责 | `processEvents(QEventLoop::ProcessEventsFlags flags)` | 处理符合 flags 的事件批次 | V2 不替你实现事件循环主体，仍要遵守基类分发语义 |
| 继承职责 | `wakeUp()` | 唤醒正在等待的事件循环 | 需要具备线程安全唤醒能力 |
| 继承职责 | `interrupt()` | 让当前事件分发尽快返回 | 不能只设置标志而不唤醒可能正在阻塞的等待 |
| 继承职责 | `registerSocketNotifier(QSocketNotifier *notifier)` | 把 socket notifier 接入底层等待机制 | 与定时器迁移无关，但仍是完整 dispatcher 必须实现的契约 |
| 继承职责 | `unregisterSocketNotifier(QSocketNotifier *notifier)` | 从底层等待机制移除 socket notifier | 重实现仍应遵守基类要求 |
| 继承职责 | `unregisterTimers(QObject *object)` | 移除某个对象关联的全部定时器 | V2 没有取消这个职责，内部 timer 表必须能按对象查找 |

## 10. 一句话抓住它

`QAbstractEventDispatcherV2` 是 Qt 6 里的迁移桥：它让自定义事件分发器提前实现 `Qt::TimerId` 和 `std::chrono` 风格的定时器接口，为 Qt 7 合并回 `QAbstractEventDispatcher` 做准备。
