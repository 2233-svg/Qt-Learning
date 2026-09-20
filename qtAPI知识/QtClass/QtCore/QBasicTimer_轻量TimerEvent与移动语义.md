# Qt QBasicTimer 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QBasicTimer>`  
> 所属模块：`Qt6::Core`  
> 直接基类：无  
> 定位：不发信号、直接向 QObject 投递 `QTimerEvent` 的轻量可移动定时器句柄

`QBasicTimer` 只保存一个底层 timer 注册，不是 QObject，也没有 `timeout()` 信号。到期时，事件循环调用目标 QObject 的 `timerEvent()`。它适合自定义控件、动画驱动器和大量轻量对象；普通业务代码通常使用更易组合的 `QTimer`。

## 1. CMake 与最小代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QBasicTimer>
#include <QCoreApplication>
#include <QTimerEvent>

class Poller final : public QObject
{
public:
    using QObject::QObject;

    void start()
    {
        m_timer.start(std::chrono::milliseconds(500), this);
    }

protected:
    void timerEvent(QTimerEvent *event) override
    {
        if (event->timerId() == static_cast<int>(m_timer.id())) {
            poll();
            return;
        }
        QObject::timerEvent(event);
    }

private:
    void poll() { qInfo() << "poll"; }
    QBasicTimer m_timer;
};
```

若编译器/Qt 版本不允许直接把强类型 `Qt::TimerId` 转为 int，可比较适配后的 ID API；核心原则是只消费属于当前 `QBasicTimer` 的事件。

## 2. QBasicTimer、QTimer 与 QObject timer

| 方式                      | 回调             | 特点               |
| ----------------------- | -------------- | ---------------- |
| `QBasicTimer`           | `timerEvent()` | 轻量、可移动、无信号       |
| `QTimer`                | `timeout()`    | 属性和信号丰富，最常用      |
| `QObject::startTimer()` | `timerEvent()` | 直接管理 int/TimerId |
| `QChronoTimer`          | `timeout()`    | 纳秒 duration、长范围  |

QBasicTimer 本质上封装了 QObject 基础 timer ID，并在析构/移动赋值时自动管理停止行为。

## 3. `Duration` 类型别名

```cpp
using Duration = QBasicTimer::Duration;
```

它是一个 `std::chrono::duration` 类型。Qt 6.11.1 当前所有平台上是 nanoseconds，但代码应使用别名，不要依赖其永远固定：

```cpp
QBasicTimer::Duration interval = std::chrono::microseconds(750);
timer.start(interval, this);
```

## 4. 启动

默认精度类型：

```cpp
timer.start(std::chrono::seconds(1), receiver);
```

显式 timer type：

```cpp
timer.start(std::chrono::milliseconds(16),
            Qt::PreciseTimer,
            receiver);
```

`receiver` 必须是有效 QObject，并且 timer 应在 receiver 所属线程启动。该线程需要运行事件循环。

已活动时再次 `start()` 会先停止旧 timer 再注册新 timer，ID 可能改变。

## 5. 处理 `timerEvent()`

一个对象可以拥有多个 basic timer：

```cpp
void Controller::timerEvent(QTimerEvent *event)
{
    const auto id = static_cast<Qt::TimerId>(event->timerId());

    if (id == m_fastTimer.id()) {
        updateFastState();
        return;
    }
    if (id == m_slowTimer.id()) {
        saveCheckpoint();
        return;
    }

    QObject::timerEvent(event);
}
```

未识别事件要交给基类。不要假设对象只会收到自己显式创建的 timer event，基类或未来代码也可能注册 timer。

Timer ID 是运行时句柄，不是稳定业务编号；重启后可能变化。

## 6. 停止与活动状态

```cpp
if (timer.isActive())
    timer.stop();
```

`isActive()` 表示已经启动且尚未停止。`stop()` 可重复调用。QBasicTimer 析构时会停止所代表的 timer，但工程代码仍应在业务状态结束时显式 stop，避免对象保持不必要的周期唤醒。

## 7. 强类型 ID

Qt 6.8 起：

```cpp
Qt::TimerId id = timer.id();
```

inactive timer 返回 `Qt::TimerId::Invalid`。强类型可以降低把普通业务 int 误当 timer ID 的风险。旧资料中的 `timerId()` 已由 `id()` 取代。

## 8. 移动构造

QBasicTimer 不可复制，但可以移动：

```cpp
QBasicTimer first;
first.start(1s, receiver);

QBasicTimer second(std::move(first));
Q_ASSERT(!first.isActive());
Q_ASSERT(second.isActive());
```

移动后，源对象变为 inactive，目标对象代表原 timer。timer 的接收 QObject 不因句柄移动而改变。

这允许放入支持 move-only 类型的容器，例如 `std::vector<QBasicTimer>`。

## 9. 移动赋值与 swap

```cpp
target = std::move(source);
```

移动赋值会先停止 target 原来代表的 timer，再接管 source；source 变为 inactive。

```cpp
first.swap(second);
swap(first, second);
```

`swap()` 交换两个 timer 句柄且不抛异常。交换后 `timerEvent()` 的路由逻辑必须仍按当前 `id()` 判断，不能缓存“成员名对应旧 ID”的假设。

## 10. 生命周期约束

QBasicTimer 不拥有 receiver。receiver 析构会清理其 timer 注册，但 timer 句柄的业务状态应一起结束。最清晰的模式是把 QBasicTimer 作为 receiver 的值成员：

```cpp
class AnimationDriver : public QObject
{
    QBasicTimer m_timer;
};
```

不要让独立 timer 句柄活得比 receiver 久后再调用 `start()`/`stop()`；也不要把 receiver 指针换成已销毁对象。

## 11. 线程规则

QBasicTimer 与 QObject timer 一样遵守线程亲和性：

- 在 receiver 所属线程 start/stop。
- `timerEvent()` 在 receiver 所属线程调用。
- receiver 线程必须有事件循环。
- 跨线程操作通过 queued signal/slot。
- receiver 移动线程时底层 timer 会由 Qt 重新注册，可能推迟到期。

QBasicTimer 本身不是线程安全同步工具。把它移动到另一个 C++ 变量，不等于把 receiver 迁移到另一个线程。

## 12. 精度与晚到

显式 `Qt::TimerType` 只请求精度/功耗策略：

- Precise 不应提前，但可能晚到。
- Coarse/VeryCoarse 允许一定提前量。
- 事件循环忙时 timeout 会延迟。
- 错过多个周期通常只收到一次事件。

需要计算实际经过时间时同时使用 `QElapsedTimer`。

## 13. 适用场景

### 适合

- 自定义 QWidget/QObject 已经重载 `timerEvent()`。
- 一个对象管理多个低开销周期任务。
- 大量实例中不需要 timeout 信号连接。
- 需要 move-only timer 句柄。

### 不适合

- 需要 lambda/context 自动生命周期连接。
- QML 属性绑定。
- 需要动态暴露 interval、remaining time。
- 需要静态 singleShot。

这些场景使用 QTimer/QChronoTimer。

## 14. 常见误区

### QBasicTimer 是 QObject 子对象

不是。它是值类型句柄，没有 parent 和信号。

### 移动 timer 会移动接收对象线程

不会。只转移 timer 注册的句柄所有权。

### 在 `timerEvent()` 处理所有 timer

必须比较 ID，未知事件传给基类。

### 保存一次 ID 永久使用

重新 start、移动或赋值后 ID 关系可能变化，查询当前 `id()`。

### 析构自动停止，所以业务无需 stop

析构会收尾，但页面隐藏、任务结束等较早时机应主动停止，减少无意义唤醒。

## API 速查表
### 15.1 类型、构造和移动语义

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型别名 | `QBasicTimer::Duration` | 表示 `start()` 接收的 chrono duration 类型。 | Qt 6.11.1 中来自 `QAbstractEventDispatcher::Duration`，代码应使用别名，避免依赖具体单位永远不变。 |
| 构造 | `QBasicTimer()` | 创建一个 inactive 的轻量 timer 句柄。 | 它不是 `QObject`，没有 parent、属性和信号；创建后不会自动开始计时。 |
| 析构 | `~QBasicTimer()` | 销毁句柄，并在仍 active 时停止底层 timer。 | 析构能兜底，但业务结束、页面隐藏或对象停用时仍应主动 `stop()`。 |
| 移动构造 | `QBasicTimer(QBasicTimer &&other)` | 从另一个句柄接管底层 timer 注册。 | 源对象变为 inactive；timer 的接收 `QObject` 不会因为句柄移动而改变线程或所有权。 |
| 移动赋值 | `operator=(QBasicTimer &&other)` | 停止当前句柄原先代表的 timer，再接管另一个句柄。 | 目标旧 timer 会被停止，源对象变 inactive；不要缓存移动前的 timer ID。 |
| 禁止复制 | `Q_DISABLE_COPY(QBasicTimer)` | 明确禁止复制 timer 句柄。 | 一个底层 timer 注册只能由一个 `QBasicTimer` 句柄管理；需要转移时使用移动。 |
| 交换 | `swap(QBasicTimer &other)` / `swap(lhs, rhs)` | 交换两个 timer 句柄。 | 交换后事件路由必须重新按当前 `id()` 判断，不要按成员变量名字假设旧 ID。 |

### 15.2 启动、停止和 ID

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 启动 | `start(Duration duration, QObject *object)` | 用默认 `Qt::CoarseTimer` 启动，让 `object` 接收 `QTimerEvent`。 | 必须在 `object` 所属线程操作，并且该线程需要事件循环。 |
| 启动 | `start(Duration duration, Qt::TimerType timerType, QObject *object)` | 按指定精度/功耗策略启动底层 timer。 | timer type 不是硬实时保证；已 active 时再次启动会重启并改变 ID。 |
| 启动 | `start(int msec, QObject *object)` | 以毫秒整数启动的兼容重载。 | 新代码优先使用 chrono duration；整数单位容易在封装层被误读。 |
| 启动 | `start(int msec, Qt::TimerType timerType, QObject *object)` | 以毫秒整数和指定 timer type 启动。 | 同样必须在接收对象所属线程调用；负值/极端值应由业务入口校验。 |
| 停止 | `stop()` | 停止当前句柄代表的底层 timer。 | 可重复调用；停止后不会再收到该 ID 的后续 timer 事件。 |
| 活动状态 | `isActive()` | 判断句柄当前是否代表一个已注册 timer。 | 只是句柄状态，不说明接收对象业务是否仍需要计时。 |
| 强类型 ID | `id()` | 返回 `Qt::TimerId`。 | inactive 时为 `Qt::TimerId::Invalid`；重启、移动赋值后都可能改变。 |
| 兼容 ID | `timerId()` | 返回旧式整数 timer ID。 | 需要和旧 API 或 `QTimerEvent::timerId()` 对接时使用；新代码优先保留强类型 ID 语义。 |

### 15.3 接收对象配合接口

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 事件回调 | `QObject::timerEvent(QTimerEvent *event)` | `QBasicTimer` 到期后，Qt 调用接收对象的这个虚函数。 | 这是接收对象的 API，不是 `QBasicTimer` 成员；必须比较 event 的 timer ID，未识别事件交给基类。 |
| 事件数据 | `QTimerEvent::timerId()` / `QTimerEvent::id()` | 读取到期事件对应的 timer ID。 | 不要假设对象只会收到一个 timer；多个 timer 或基类 timer 都可能进入同一个 `timerEvent()`。 |
| 线程规则 | 接收对象线程亲和性 | 决定 timer 注册在哪个事件循环、回调在哪个线程执行。 | 移动 `QBasicTimer` 句柄不等于移动接收对象；跨线程 start/stop 用 queued 调用。 |
| 使用取舍 | 与 `QTimer` / `QChronoTimer` 对比 | 省掉信号和 QObject 成本，直接走事件。 | 需要 `timeout()`、lambda context、属性绑定、singleShot 或 remaining time 时选更高级的 timer 类。 |

---

### 一句话总结

`QBasicTimer` 是直接驱动 `QObject::timerEvent()` 的轻量 move-only 句柄：把它作为接收对象成员，在正确线程启动/停止，按当前强类型 ID 路由事件，并在不需要信号和属性时换取更简单的底层开销。
