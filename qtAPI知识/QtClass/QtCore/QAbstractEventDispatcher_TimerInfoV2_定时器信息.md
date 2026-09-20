# QAbstractEventDispatcher::TimerInfoV2 定时器信息深入笔记

> 适用版本：Qt 6.8 起，本文按 Qt 6.11.1 的接口说明  
> 所属模块：`Qt6::Core`  
> 所属类型：`QAbstractEventDispatcher` 的公开嵌套结构体  
> 相关 API：`QAbstractEventDispatcher::timersForObject()`

## 1. 它解决什么问题

`QAbstractEventDispatcher::TimerInfoV2` 是一个很小的值类型，用来描述某个 `QObject` 当前登记在事件分发器里的定时器。

它不是一个会“运行”的定时器，也不会发出 `timeout()` 信号。真正负责调度的是线程中的 `QAbstractEventDispatcher`；`TimerInfoV2` 只是把 dispatcher 已经登记的定时器信息拿出来，交给你观察或诊断。

可以把关系理解成：

```text
QObject / QTimer
       ↓ startTimer() 或 QTimer::start()
QAbstractEventDispatcher 登记底层定时器
       ↓ timersForObject(object)
QList<QAbstractEventDispatcher::TimerInfoV2>
```

如果你平时只是写业务定时逻辑，通常接触的是 `QTimer`。只有在调试“这个对象到底启动了哪些底层定时器”、实现自定义事件分发器、或者做 Qt 6.8 之后的定时器接口迁移时，`TimerInfoV2` 才会变得重要。

## 2. 它和旧 `TimerInfo` 的区别

旧结构体 `TimerInfo` 长这样：

```cpp
struct TimerInfo {
    int timerId;
    int interval;
    Qt::TimerType timerType;
};
```

旧接口的问题在于：

- `timerId` 是普通 `int`，语义不够明确。
- `interval` 是整数毫秒，无法表达更现代的 `std::chrono` 时间接口。
- 它和 Qt 6.8 之后的新定时器 API 不匹配。

`TimerInfoV2` 改成：

```cpp
struct TimerInfoV2 {
    QAbstractEventDispatcher::Duration interval;
    Qt::TimerId timerId;
    Qt::TimerType timerType;
};
```

核心变化是：

- `timerId` 使用 `Qt::TimerId`，这是专门表达定时器 ID 的类型。
- `interval` 使用 `QAbstractEventDispatcher::Duration`，当前 Qt 6.11.1 中是 `std::chrono::nanoseconds`。
- 它对应 `timersForObject()`，而不是旧的 `registeredTimers()`。

这让代码的意图更清楚：你拿到的不是任意整数，而是一个 Qt 定时器 ID；你处理的不是裸毫秒数字，而是 chrono duration。

## 3. 三个字段分别表示什么

### 3.1 `interval`

```cpp
QAbstractEventDispatcher::Duration interval;
```

表示定时器登记时使用的间隔。它不是“距离下一次触发还剩多久”，而是定时器本身的周期或间隔配置。

如果要查询剩余时间，应该使用：

```cpp
QAbstractEventDispatcher::instance()
    ->remainingTime(info.timerId);
```

因此：

- `interval` 回答“这个定时器设成多久触发一次”。
- `remainingTime()` 回答“这个定时器距离下一次触发还有多久”。

这两个值在事件循环繁忙、定时器已经逾期、或者粗略定时器被系统合并唤醒时，不能混为一谈。

### 3.2 `timerId`

```cpp
Qt::TimerId timerId;
```

表示活动定时器的唯一标识。这个 ID 可以来自：

```cpp
Qt::TimerId id = object->startTimer(1000ms);
```

也可以来自 dispatcher 的新式登记函数：

```cpp
Qt::TimerId id =
    QAbstractEventDispatcher::instance()->registerTimer(
        1000ms,
        Qt::CoarseTimer,
        object);
```

只要定时器还处于活动状态，这个 ID 就能用来取消或查询它：

```cpp
dispatcher->unregisterTimer(info.timerId);
dispatcher->remainingTime(info.timerId);
```

注意它是“活动期间的标识”。定时器被注销后，不应该继续把旧 ID 当成有效句柄保存并复用。

### 3.3 `timerType`

```cpp
Qt::TimerType timerType;
```

表示定时器调度精度策略。常见取值包括：

- `Qt::PreciseTimer`：尽量精确，适合需要较高时间精度的场景。
- `Qt::CoarseTimer`：允许一定误差，适合普通 UI 刷新、状态轮询等场景。
- `Qt::VeryCoarseTimer`：误差更大，适合低频、节能、不敏感的任务。

`timerType` 不只是一个标签，它会影响底层 dispatcher 如何向操作系统登记等待时间。移动端、省电场景和大量定时器并存时，粗略定时器通常比精确定时器更友好。

## 4. 如何实际拿到 `TimerInfoV2`

典型方式是通过 `QAbstractEventDispatcher::timersForObject()`：

```cpp
using namespace std::chrono_literals;

class Worker : public QObject
{
public:
    void start()
    {
        m_timerId = startTimer(500ms, Qt::CoarseTimer);
    }

protected:
    void timerEvent(QTimerEvent *event) override
    {
        if (event->id() == m_timerId)
            doWork();
    }

private:
    void doWork();
    Qt::TimerId m_timerId {};
};

Worker worker;
worker.start();

auto *dispatcher = QAbstractEventDispatcher::instance();
const QList<QAbstractEventDispatcher::TimerInfoV2> timers =
    dispatcher->timersForObject(&worker);

for (const auto &info : timers) {
    qDebug() << info.timerId
             << info.interval
             << info.timerType
             << dispatcher->remainingTime(info.timerId);
}
```

这段代码的重点不是“用 `TimerInfoV2` 启动定时器”，而是展示它适合做观察。启动、停止和业务响应仍然由 `QObject::startTimer()`、`QObject::killTimer()`、`QTimer` 或 dispatcher 的注册 API 完成。

## 5. 使用场景

### 5.1 诊断对象是否泄漏了定时器

某些对象被复用多次后，可能重复启动定时器却没有正确停止。`timersForObject()` 可以帮助确认这个对象当前到底登记了多少个底层定时器。

### 5.2 自定义事件分发器时做状态导出

如果你实现 `QAbstractEventDispatcherV2`，就需要能返回 `QList<TimerInfoV2>`。这要求内部保存的 timer watcher 不只知道“下次什么时候醒”，还要保留 Qt 层的 `timerId`、`interval` 和 `timerType`。

### 5.3 从旧定时器接口迁移

旧代码可能依赖 `registeredTimers()` 和 `TimerInfo`。迁移到 Qt 6.8 之后的新接口时，可以把关注点从 `int` 和毫秒转成 `Qt::TimerId` 与 `Duration`。

### 5.4 写调试工具或事件循环监控

当你想观察某个线程里对象的定时器行为，例如 UI 卡顿、定时器积压、某个对象过度唤醒线程，`TimerInfoV2` 能提供比业务日志更底层的线索。

## 6. 常见误区

### 6.1 把 `interval` 当成剩余时间

`interval` 是登记间隔，不是剩余时间。剩余时间必须调用 `remainingTime(timerId)` 查询。

### 6.2 把 `TimerInfoV2` 当成定时器句柄

它只是一次查询结果。定时器是否仍然存在，要以后续 `remainingTime()`、`unregisterTimer()` 的结果为准。

### 6.3 忽略线程归属

定时器属于对象所在的线程事件循环。跨线程拿到一个对象指针后随便查 dispatcher，很容易查错线程或在错误上下文里操作。

### 6.4 继续使用旧 `TimerInfo`

Qt 6.8 已经把旧 `TimerInfo` 标为过时。新代码应优先围绕 `TimerInfoV2` 设计，尤其是库代码和自定义 dispatcher。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员变量 | `interval` | 保存定时器登记时的间隔，类型为 `QAbstractEventDispatcher::Duration` | 它不是剩余时间；剩余时间用 `remainingTime(timerId)` 查询 |
| 成员变量 | `timerId` | 保存活动定时器的 `Qt::TimerId` | 只在定时器活动期间有意义，注销后不要继续当有效句柄使用 |
| 成员变量 | `timerType` | 保存定时器的精度和调度策略 | 会影响底层调度精度和唤醒策略，不只是注释性字段 |

## 8. 一句话抓住它

`TimerInfoV2` 是“事件分发器里某个活动定时器的快照”：它告诉你这个定时器是谁、多久触发一次、按什么精度策略调度；它不负责启动定时器，也不保证查询之后定时器仍然存在。
