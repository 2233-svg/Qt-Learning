# Qt QTimerEvent：底层定时事件载荷

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTimerEvent>`  
> 所属模块：`Qt6::Core`  
> 继承：`QEvent -> QTimerEvent`  
> 类型性质：由事件循环投递给 `QObject::timerEvent()` 的定时事件

## 1. 它解决什么问题

`QTimerEvent` 表示“某个 QObject 定时器到期了”。它只携带一个定时器 ID，不负责创建定时器、计时、发信号或执行回调。

最典型的使用位置是重载 `QObject::timerEvent()`：

```cpp
class Poller final : public QObject
{
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
    QBasicTimer m_timer;
};
```

启动动作来自 `QBasicTimer::start()`、`QObject::startTimer()` 或其他 Qt 内部定时器机制；事件循环到期后才创建并投递 `QTimerEvent`。

## 2. 它不是什么

`QTimerEvent` 不是：

- 定时器本身；
- 独立线程或实时计时器；
- `QTimer::timeout()` 信号；
- 可以长期保存的事件对象；
- 负责释放 socket、文件描述符或其他资源的 owner；
- 用来测量精确耗时的时钟。

如果需要信号、单次延迟、定时器属性或 context 生命周期保护，使用 `QTimer`。如果只需要轻量地把事件送进已有 QObject 的 `timerEvent()`，使用 `QBasicTimer`。

## 3. 事件处理的最小模型

```cpp
class Controller final : public QObject
{
public:
    using QObject::QObject;

    void start()
    {
        m_timer.start(std::chrono::seconds(1), this);
    }

protected:
    void timerEvent(QTimerEvent *event) override
    {
        if (event->matches(m_timer)) {
            refresh();
            return;
        }

        QObject::timerEvent(event);
    }

private:
    void refresh() {}
    QBasicTimer m_timer;
};
```

`timerEvent()` 中应只在当前事件确实属于目标 timer 时处理。一个 QObject 可以同时拥有多个 timer，也可能在基类或其他代码中注册定时器。

未知事件通常交给 `QObject::timerEvent(event)`，避免吞掉基类或未来逻辑需要处理的事件。

## 4. 生命周期、线程和有效性

### 4.1 事件指针只在回调期间有效

`QTimerEvent *event` 是 Qt 在事件分发期间传入的对象。一般只在 `timerEvent()` 调用栈内读取 `id()` 或 `timerId()`：

```cpp
void timerEvent(QTimerEvent *event) override
{
    const Qt::TimerId id = event->id();
    handleTimer(id);
}
```

不要把 `event` 裸指针保存到成员变量或异步任务中。需要保存标识时，保存 `Qt::TimerId` 值；需要保存业务状态时，保存自己的对象数据。

### 4.2 事件在接收 QObject 所在线程处理

定时事件由接收对象所属线程的事件循环分发。线程没有运行事件循环，或事件循环被长时间阻塞，事件就不会按期到达。

定时器的启动和停止也应遵守接收对象的线程亲和性。把 `QTimerEvent` 移到另一个线程没有意义，它不是可转移的工作对象。

### 4.3 ID 是运行时句柄，不是业务编号

定时器 ID 只在当前事件循环和当前注册周期内有意义。重新启动、改变 interval、移动对象或停止后再次启动，都可能产生新的 ID。

不要把 ID 持久化，也不要在业务协议中把它当作稳定对象身份。

## 5. `id()` 与 `timerId()` 的区别

Qt 6.8 引入强类型的 `Qt::TimerId`：

```cpp
const Qt::TimerId id = event->id();
```

旧式 API 返回 `int`：

```cpp
const int legacyId = event->timerId();
```

新代码优先使用 `id()`，这样可以减少把普通整数和 timer ID 混用的机会。只有和旧接口、旧代码或整数型 `QBasicTimer::timerId()` 对接时才使用 `timerId()`。

二者描述同一个运行时定时器标识，不是两个不同的 timer。

## 6. `matches()`：和 `QBasicTimer` 对应

Qt 6.9 起可以直接写：

```cpp
if (event->matches(m_timer)) {
    handleTimeout();
}
```

`matches()` 本质上比较事件的 `Qt::TimerId` 与 `QBasicTimer::id()`。它不会检查：

- timer 是否仍然在业务上需要运行；
- 事件是否一定来自当前 QObject；
- 是否已经处理过这个事件；
- 目标对象是否拥有该 timer。

所以它适合替代手工的 ID 比较，但仍应在正确的 `timerEvent()` 和对象生命周期内使用。

如果事件 ID 和一个非活动 timer 都是无效值，单纯比较无效 ID 可能得到相等结果。正常代码应只对已启动的 `QBasicTimer` 做匹配，并让无效状态显式退出。

## 7. 与不同定时器 API 的关系

| 创建/驱动来源 | 接收方式 | `QTimerEvent` 的典型位置 |
| --- | --- | --- |
| `QBasicTimer` | `QObject::timerEvent()` | 应用或控件重载的事件函数 |
| `QObject::startTimer()` | `QObject::timerEvent()` | 应用或基础设施的事件函数 |
| `QTimer` | `QTimer` 内部处理后发出 `timeout()` | 普通代码通常不直接处理 |
| `QChronoTimer` | `QChronoTimer` 内部处理后发出 `timeout()` | 普通代码通常不直接处理 |

`QTimerEvent` 是低层事件接口的一部分。不要为了读取一个 `QTimer` 的 interval 或剩余时间而尝试拦截其底层事件；直接使用 `QTimer` 的公开 API。

## 8. 定时精度边界

`QTimerEvent` 到达只表示“事件循环现在处理到了这个定时器事件”。它不保证：

- 事件恰好在 interval 到期的瞬间处理；
- 每个理论周期都对应一个事件；
- 事件循环阻塞期间错过的周期会全部补发；
- `id()` 能反映实际经过时间。

需要测量真实经过时间，使用 `QElapsedTimer` 或 `std::chrono::steady_clock`。需要表示截止时间，使用 `QDeadlineTimer`。定时事件只适合触发一次检查或刷新。

## 9. 常见使用场景

### 9.1 一个对象分流多个轻量 timer

```cpp
void Dashboard::timerEvent(QTimerEvent *event)
{
    if (event->matches(m_refreshTimer)) {
        refresh();
        return;
    }

    if (event->matches(m_cleanupTimer)) {
        cleanup();
        return;
    }

    QObject::timerEvent(event);
}
```

### 9.2 实现一次性事件

`QBasicTimer` 本身是重复定时器。若业务只需要一次，可以在第一次匹配后停止：

```cpp
void Controller::timerEvent(QTimerEvent *event)
{
    if (event->matches(m_onceTimer)) {
        m_onceTimer.stop();
        finish();
        return;
    }

    QObject::timerEvent(event);
}
```

如果没有低层 `timerEvent()` 需求，直接使用 `QTimer::singleShot()` 更清晰。

### 9.3 处理未知定时器事件

```cpp
void Worker::timerEvent(QTimerEvent *event)
{
    if (event->id() == m_workTimer.id()) {
        processOne();
        return;
    }

    QObject::timerEvent(event);
}
```

不要无条件把所有 `timerEvent()` 都当成自己的工作 timer；这会让新增的 timer 或基类逻辑难以共存。

## 10. 常见错误

### 10.1 把 QTimerEvent 当作定时器保存

它只是一次事件载荷。长期运行应保存 `QBasicTimer`、`QTimer` 或自己的 timer ID。

### 10.2 保存事件指针

回调返回后，事件对象的生命周期由 Qt 管理。保存裸指针会形成悬空指针风险。

### 10.3 不比较 timer ID

同一个 QObject 可能收到多个 timer 的事件。必须用 `id()`、`timerId()` 或 `matches()` 分流。

### 10.4 用 timer ID 测量时间

ID 不是时间戳。要计算 elapsed，使用单调时钟。

### 10.5 在错误线程启动或停止 timer

事件最终由接收 QObject 的线程处理。跨线程请求应通过 queued signal/slot 或 `QMetaObject::invokeMethod()`。

### 10.6 期待阻塞期间补发全部周期

事件循环恢复后通常只处理当前到期状态，不会为每个错过的周期生成一串业务回调。需要补偿时，自己根据 elapsed 计算。

## 11. 逐项 API 语义

### `QTimerEvent(int timerId)`

用旧式 `int` timer ID 构造一个定时事件。普通应用通常不需要手工构造；该构造主要服务于 Qt 的事件分发和兼容代码。

### `QTimerEvent(Qt::TimerId timerId)`

用 Qt 6.8 引入的强类型 timer ID 构造事件。它仍然只保存标识，不注册或启动定时器。

### `~QTimerEvent()`

销毁事件对象。普通代码通常不直接管理由 Qt 投递的事件生命周期。

### `id() const`

返回事件携带的 `Qt::TimerId`。Qt 6.8 起提供。无效 ID 只能表示没有有效注册句柄，不能被当作一个可触发的 timer。

### `timerId() const`

以 `int` 返回同一个事件 ID，用于兼容旧代码。新代码优先使用 `id()`。

### `matches(const QBasicTimer &timer) const`

Qt 6.9 起比较当前事件 ID 与 `timer.id()`。它是轻量的 ID 比较，不执行额外的生命周期或线程检查；通常在 `timerEvent()` 中配合活动的 `QBasicTimer` 使用。

### `clone() const`

`QTimerEvent` 通过 `QEvent` 的事件复制机制支持克隆。普通 `timerEvent()` 处理代码不需要调用它，也不应把克隆当作重新调度定时器的方式。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QTimerEvent(int timerId)` | 用旧式整数 ID 创建定时事件。 | 只创建事件载荷，不启动定时器；普通业务通常不需要手工构造。 |
| 构造 | `QTimerEvent(Qt::TimerId timerId)` | 用强类型 ID 创建定时事件。 | Qt 6.8 起；同样不负责注册底层 timer。 |
| 生命周期 | `~QTimerEvent()` | 销毁事件对象。 | Qt 投递的事件由框架管理，不要保存事件指针。 |
| 标识 | `id()` | 返回 `Qt::TimerId`。 | Qt 6.8 起；ID 是运行时句柄，不是业务编号。 |
| 标识 | `timerId()` | 以 `int` 返回同一个 ID。 | 兼容旧代码；新代码优先使用 `id()`。 |
| 匹配 | `matches(const QBasicTimer &)` | 比较事件 ID 与 basic timer ID。 | Qt 6.9 起；仍要保证 timer 对象和事件处于正确生命周期。 |
| 事件复制 | `clone()` | 按 `QEvent` 机制复制事件。 | 不会重新注册 timer，也不是普通定时器 API。 |
| 协作 | `QObject::timerEvent(QTimerEvent *)` | 接收定时事件的虚函数入口。 | 事件指针只在回调中使用；未识别事件交给基类。 |

## 13. 一句话总结

`QTimerEvent` 只是事件循环投递的一次定时通知：它携带运行时 timer ID，不负责计时和所有权。低层代码在 `timerEvent()` 中用 `id()` 或 `matches()` 分流，事件指针不保存，真实时间不靠 ID 推断。
