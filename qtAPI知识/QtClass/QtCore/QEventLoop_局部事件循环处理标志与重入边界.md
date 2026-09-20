# Qt QEventLoop 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QEventLoop>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QEventLoop`  
> 定位：在当前线程进入、退出或手工推进一个事件循环

`QEventLoop` 是事件循环的对象化接口。`QCoreApplication::exec()` 运行主循环，而 `QEventLoop::exec()` 可以在某个调用栈内建立局部循环。它能把异步信号临时包装成同步等待，但也会引入嵌套循环和重入风险，因此应作为边界工具，而不是日常异步编程的默认方案。

## 1. CMake 与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

等待一个异步操作或超时：

```cpp
QEventLoop loop;
QTimer timeout;
timeout.setSingleShot(true);

connect(worker, &Worker::finished,
        &loop, &QEventLoop::quit);
connect(&timeout, &QTimer::timeout,
        &loop, &QEventLoop::quit);

timeout.start(std::chrono::seconds(5));
loop.exec();

if (timeout.isActive())
    qInfo() << "worker finished";
else
    qWarning() << "timeout";
```

循环执行期间，当前线程没有阻塞在操作系统 wait 上，而是继续分发该线程的事件。因此定时器、queued slots、删除事件和用户输入都可能进入当前调用栈。

## 2. 主循环与局部循环

```text
main()
└─ QCoreApplication::exec()        主事件循环
   └─ 某个槽函数
      └─ QEventLoop::exec()        嵌套局部循环
         └─ 其它事件/槽可再次进入业务对象
```

局部循环不会创建新线程，也不会只处理你正在等待的那个对象。它驱动当前线程的整个事件分发器，除非用 flags 排除部分事件。

## 3. 构造与生命周期

```cpp
QEventLoop loop(parent);
```

对象必须在调用 `exec()` 的线程使用。析构正在运行的 loop 前应先退出；不要让回调保存指向栈上 loop 的裸指针并在函数返回后调用。

`QEventLoop` 继承 QObject，可作为信号槽 context。栈上局部 loop 很常见，因为退出 `exec()` 后即可确定销毁。

## 4. `ProcessEventsFlag`

```cpp
enum QEventLoop::ProcessEventsFlag {
    AllEvents,
    ExcludeUserInputEvents,
    ExcludeSocketNotifiers,
    WaitForMoreEvents
};
Q_DECLARE_FLAGS(ProcessEventsFlags, ProcessEventsFlag)
```

### 4.1 `AllEvents`

处理所有允许的事件。DeferredDelete 有特殊处理规则，不应假设和普通 posted event 完全相同。

### 4.2 `ExcludeUserInputEvents`

暂不处理按钮、按键等用户输入。事件不会被丢弃，下一次不带该标志处理事件时仍会投递。

这能降低长操作中的用户重入，但不能阻止定时器、网络、queued slots 或对象删除造成的重入。

### 4.3 `ExcludeSocketNotifiers`

暂不处理 socket notifier 事件，同样只是延迟，不是删除。网络和 IPC 代码可能因此停滞，使用时要明确影响。

### 4.4 `WaitForMoreEvents`

若当前没有待处理事件，允许事件循环等待新事件，而不是立即返回。对带 deadline 的 `processEvents()` 重载，该标志没有意义并会被忽略。

标志可组合：

```cpp
const auto flags = QEventLoop::ExcludeUserInputEvents
                 | QEventLoop::ExcludeSocketNotifiers;
```

## 5. `exec()`

```cpp
const int code = loop.exec(QEventLoop::AllEvents);
```

进入循环并持续分发事件，直到 `exit()` 或 `quit()` 被调用。返回值来自 `exit(returnCode)`。

连接应在 `exec()` 前建立：

```cpp
connect(reply, &QNetworkReply::finished,
        &loop, &QEventLoop::quit);

if (!reply->isFinished())
    loop.exec();
```

先检查完成状态，避免操作在进入循环前已完成而退出信号已经错过。

## 6. `exit()` 与 `quit()`

```cpp
loop.exit(7); // exec() 返回 7
loop.quit();  // 等价于 exit(0)
```

从其他线程请求退出时使用 queued connection 或 `QMetaObject::invokeMethod`，让调用在 loop 所属线程执行：

```cpp
QMetaObject::invokeMethod(&loop, &QEventLoop::quit,
                          Qt::QueuedConnection);
```

如果在 `exec()` 开始前调用 exit，不能简单假设下一次 exec 一定立即退出；可靠做法是保存业务完成状态，进入循环前再次检查。

## 7. `isRunning()`

```cpp
if (loop.isRunning())
    loop.quit();
```

它只表示该 loop 当前是否处于 `exec()` 中。跨线程读取并不能替代同步协议，状态在返回后可能立刻变化。

## 8. `processEvents()`

### 8.1 处理当前待办事件

```cpp
const bool processed = loop.processEvents(QEventLoop::AllEvents);
```

返回 bool 的重载表示是否处理了可用事件。它是底层 dispatcher 的包装。

### 8.2 带截止时间

```cpp
loop.processEvents(
    QEventLoop::ExcludeUserInputEvents,
    QDeadlineTimer(std::chrono::milliseconds(10)));
```

Qt 6.7 起的 deadline 重载会处理调用期间新加入队列的事件，直到截止或没有事件。它保证在截止前开始的事件会完成处理，因此单个事件处理器很慢时，实际返回可晚于 deadline。

毫秒重载等价于构造 deadline：

```cpp
loop.processEvents(flags, 10);
```

## 9. 为什么不推荐用 processEvents 跑长任务

```cpp
for (int i = 0; i < 1'000'000; ++i) {
    doWork(i);
    loop.processEvents();
}
```

问题包括：

- 当前操作可能被按钮再次触发。
- 对话框或页面可能在循环中关闭并销毁。
- 模型可能在迭代中被另一个槽修改。
- deferred delete 和 queued callback 改变对象状态。
- 事件处理时间使工作耗时不可预测。

优先方案是把 CPU 工作交给 `QtConcurrent`/工作线程，或用 0 间隔 `QChronoTimer`/`QTimer` 分块处理。

## 10. 嵌套循环的典型来源

以下 API 或模式可能运行局部事件循环：

- 模态对话框的 `exec()`。
- 菜单的同步执行。
- 手写“同步网络请求”。
- 拖放等平台交互。
- 测试框架等待信号。

调用这类函数前，把当前对象视为“可能被再次调用或删除”。使用 `QPointer` 守护：

```cpp
QPointer<MyDialog> guard(this);
otherDialog.exec();
if (!guard)
    return;
```

## 11. 把异步网络包装为同步的边界

```cpp
QByteArray fetchSynchronously(QNetworkAccessManager &manager,
                              const QNetworkRequest &request)
{
    QNetworkReply *reply = manager.get(request);
    QEventLoop loop;
    QTimer timeout;
    timeout.setSingleShot(true);

    connect(reply, &QNetworkReply::finished,
            &loop, &QEventLoop::quit);
    connect(&timeout, &QTimer::timeout,
            reply, &QNetworkReply::abort);
    connect(&timeout, &QTimer::timeout,
            &loop, &QEventLoop::quit);

    timeout.start(std::chrono::seconds(10));
    loop.exec(QEventLoop::ExcludeUserInputEvents);

    const QByteArray data =
        reply->error() == QNetworkReply::NoError
            ? reply->readAll() : QByteArray{};
    reply->deleteLater();
    return data;
}
```

这种包装只适合受控边界，例如工作线程中的遗留同步接口。GUI 主线程应保留原生异步流程，否则仍有重入、窗口关闭和嵌套等待问题。

## 12. `wakeUp()`

```cpp
loop.wakeUp();
```

唤醒可能正在等待更多事件的事件分发器。它不等于退出循环，也不携带任务。跨线程通常应投递事件或 queued signal；这些操作本身会唤醒目标 dispatcher。直接 `wakeUp()` 多用于自定义调度器集成。

## 13. 重载 `event()`

`QEventLoop` 重载了 QObject 的 `event()` 处理内部控制事件。派生类若继续重载，未处理事件必须传给基类：

```cpp
bool MyLoop::event(QEvent *event)
{
    if (event->type() == MyControlEvent)
        return handleControl(event);
    return QEventLoop::event(event);
}
```

一般不需要派生 `QEventLoop`，组合使用更稳定。

## 14. 测试中等待信号

```cpp
QEventLoop loop;
QTimer timer;
timer.setSingleShot(true);

connect(object, &Object::ready, &loop, &QEventLoop::quit);
connect(&timer, &QTimer::timeout, &loop, &QEventLoop::quit);

timer.start(1000);
loop.exec();
QVERIFY(timer.isActive());
```

Qt Test 中通常优先 `QSignalSpy::wait()` 或 `QTRY_*` 宏，它们封装了超时并减少重复局部循环代码。

## 15. 常见误区

### `ExcludeUserInputEvents` 能避免全部重入

不能。定时器、网络、queued slots 和删除事件仍会运行。

### deadline 是硬实时限制

不是。已经开始处理的事件不会在 deadline 到达时被中断。

### 局部事件循环就是同步阻塞

对当前函数看起来同步，但线程仍在处理其他事件，状态可能变化得更多。

### `wakeUp()` 会让 exec 返回

不会。退出要调用 `quit()` 或 `exit()`。

### 用无限局部循环等待失败路径

所有等待都必须有超时、取消和对象销毁处理，否则遗漏一个信号就永久挂起。

## API 速查表
### 16.1 构造、执行和退出

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QEventLoop(QObject *parent = nullptr)` | 创建一个可在当前线程运行的事件循环对象。 | 它继承 QObject；通常作为栈对象等待某个异步结果，不能跨线程随意执行。 |
| 析构 | `~QEventLoop()` | 销毁事件循环对象。 | 若循环还在运行，应先让它退出；不要让异步回调保存已返回栈对象的指针。 |
| 进入循环 | `exec(ProcessEventsFlags flags = AllEvents)` | 进入局部事件循环，直到 `exit()` 或 `quit()`。 | 会分发当前线程允许的所有事件，带来嵌套循环和业务重入风险。 |
| 退出循环 | `exit(int returnCode = 0)` | 让正在运行的 `exec()` 返回指定代码。 | 跨线程请求退出时使用 queued 调用；不要依赖进入循环前已经发出的退出信号。 |
| 退出循环 | `quit()` | 以返回码 0 退出事件循环。 | 常连接到 finished/timeout 信号；本质等价于 `exit(0)`。 |
| 状态 | `isRunning()` | 查询该 `QEventLoop` 当前是否处于 `exec()` 中。 | 只是瞬时状态，不能替代跨线程同步协议。 |

### 16.2 手工推进和唤醒

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 手工处理 | `processEvents(ProcessEventsFlags flags = AllEvents)` | 处理当前已经可用的一批事件，并返回是否处理了事件。 | 仍会引入重入；不要在长循环里把它当作通用“保持响应”方案。 |
| 手工处理 | `processEvents(ProcessEventsFlags flags, int maximumTime)` | 在最多指定毫秒内处理事件。 | 单个事件处理器不会被强行中断，实际返回可能晚于时间上限。 |
| 手工处理 | `processEvents(ProcessEventsFlags flags, QDeadlineTimer deadline)` | 处理事件直到截止时间或队列耗尽。 | Qt 6.7 起会处理调用期间新加入的事件；`WaitForMoreEvents` 对 deadline 重载无意义。 |
| 唤醒 | `wakeUp()` | 唤醒可能正等待更多事件的事件分发器。 | 不会让 `exec()` 返回，也不携带任务；退出仍需 `quit()`/`exit()`。 |
| 事件入口 | `event(QEvent *event)` | 处理事件循环对象自身收到的事件。 | 很少需要派生重写；未处理事件必须交给 `QEventLoop::event()`。 |

### 16.3 ProcessEventsFlag

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 标志 | `AllEvents` | 处理所有允许的事件。 | 不表示只处理你等待的对象；DeferredDelete 等事件有特殊处理规则。 |
| 标志 | `ExcludeUserInputEvents` | 暂缓处理用户输入事件。 | 事件不会丢弃，只是延后；定时器、queued slot 和对象删除仍可能造成重入。 |
| 标志 | `ExcludeSocketNotifiers` | 暂缓处理 socket notifier 事件。 | 网络或 IPC 可能停滞；只在明确知道影响范围时使用。 |
| 标志 | `WaitForMoreEvents` | 没有待处理事件时允许等待新事件。 | 不会自动退出；deadline 重载会忽略它。 |
| 特殊标志 | `X11ExcludeTimers` | 平台相关的事件处理控制标志。 | 非通用业务选项，跨平台代码不要依赖它。 |
| 内部标志 | `EventLoopExec` / `DialogExec` / `ApplicationExec` | Qt 用来标记事件循环执行语境。 | 这些主要服务框架内部；普通业务代码不要随意组合传入。 |
| 标志集合 | `ProcessEventsFlags` | `ProcessEventsFlag` 的按位组合类型。 | 组合标志只能改变事件类别过滤，不能消除嵌套循环带来的所有状态变化。 |

---

### 一句话总结

`QEventLoop` 能在当前线程临时进入或推进事件循环，但它不会只等待目标信号；所有允许事件都可能重入当前对象，因此应带超时、取消和生命周期守护，并优先用真正的异步流程代替嵌套循环。
