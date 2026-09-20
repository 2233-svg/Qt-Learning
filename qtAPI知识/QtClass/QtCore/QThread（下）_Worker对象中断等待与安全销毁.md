# Qt QThread 深入笔记（下）：Worker 对象、中断等待与安全销毁

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QThread>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QThread`  
> 前置阅读：`QThread（上）_线程对象执行模型与启动配置.md`

上篇建立了最重要的模型：`QThread` 对象通常属于创建它的线程，而 `run()` 才在它管理的新线程中执行。本篇在这个模型上解决实践中的核心问题：如何让 Worker 真正在目标线程运行，如何请求停止、等待结束，以及怎样销毁才不会留下竞态或触发 `QThread: Destroyed while thread is still running`。

## 1. CMake 与最小可用 Worker 代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

下面是一个完整但仍保持最小的 worker-object 模式。`Worker` 不继承 `QThread`，业务槽通过 queued connection 在工作线程执行：

```cpp
#include <QCoreApplication>
#include <QObject>
#include <QThread>

class Worker final : public QObject
{
    Q_OBJECT

public slots:
    void process()
    {
        // 此槽由工作线程的事件循环调用。
        for (int i = 0; i < 100; ++i) {
            if (QThread::currentThread()->isInterruptionRequested()) {
                emit finished();
                return;
            }
            doOneSmallStep(i);
        }
        emit finished();
    }

signals:
    void finished();
};

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    auto *thread = new QThread(&app);
    auto *worker = new Worker;       // 暂时属于主线程，无父对象
    worker->moveToThread(thread);    // 迁移到工作线程

    QObject::connect(thread, &QThread::started,
                     worker, &Worker::process);
    QObject::connect(worker, &Worker::finished,
                     thread, &QThread::quit);
    QObject::connect(thread, &QThread::finished,
                     worker, &QObject::deleteLater);
    QObject::connect(thread, &QThread::finished,
                     thread, &QObject::deleteLater);
    QObject::connect(thread, &QThread::finished,
                     &app, &QCoreApplication::quit);

    thread->start();
    return app.exec();
}
```

这个例子表达的是一套生命周期协议，而不只是几条连接：

1. `start()` 启动平台线程，默认 `run()` 随后进入 `exec()`。
2. `started()` 触发 `Worker::process()`，接收者决定槽在哪个线程执行。
3. Worker 完成后发出自己的 `finished()`，要求线程事件循环退出。
4. `QThread::finished()` 发出时，工作线程的普通事件处理已经停止，但 deferred-delete 事件仍可执行，所以此时连接 `worker->deleteLater()`。
5. QThread 对象本身属于主线程，随后在主线程删除。

## 2. Worker 模式为什么正确

### 2.1 两个对象、两个归属

```text
主线程                              工作线程
┌─────────────────────┐             ┌─────────────────────┐
│ QThread 对象         │  管理 ----> │ 平台线程             │
│ thread() == 主线程   │             │ 默认执行 run/exec    │
└─────────────────────┘             │                     │
                                    │ Worker 对象          │
                                    │ thread() == QThread  │
                                    └─────────────────────┘
```

`QThread` 对象是线程控制器，不是业务代码的天然容器。将槽写进 `QThread` 子类后，queued 调用仍由这个 QThread 对象的线程归属决定，通常会落回主线程。

Worker 模式把业务状态和槽放进单独的 `QObject`，再移动该对象。于是 AutoConnection 跨线程时会自动采用 queued delivery，槽最终在 Worker 所属线程的事件循环中执行。

### 2.2 `moveToThread()` 的约束

```cpp
bool ok = worker->moveToThread(thread);
```

必须注意：

- 只能从对象当前所属线程“推走”对象，不能任意从第三个线程把对象“拉过来”。
- 有父对象的 QObject 不能移动；因此示例中的 `worker` 创建时不能把 `thread` 当父对象。
- 移动父对象时，其所有子对象会一起移动。
- 普通成员指针不会自动成为子对象；若成员 QObject 没有正确 parent，它不会自动迁移。
- Widget 只能生活在 GUI 线程，不能移动到工作线程。
- 迁移会改变定时器服务线程；频繁来回移动可能不断推迟定时器事件。

检查结果，不要忽略 Qt 6 中的布尔返回值：

```cpp
if (!worker->moveToThread(thread)) {
    qFatal("cannot move worker to target thread");
}
```

## 3. `started()` 与启动时序

```cpp
connect(thread, &QThread::started,
        worker, &Worker::process);
thread->start();
```

`started()` 从关联的新线程发出，但跨线程槽的实际执行仍取决于连接类型与接收者归属。信号已发出，不代表接收槽已经执行，因为 queued 调用可能仍在接收线程队列中。

不应在 `start()` 后立刻读一个普通布尔变量来判断 Worker 是否已初始化；那既有时序问题，也可能产生数据竞争。需要确认初始化完成时，应让 Worker 发出 `ready()` 信号。

```cpp
connect(worker, &Worker::ready, this, &Controller::onWorkerReady);
```

## 4. 事件循环决定 queued 工作能否运行

QThread 默认的 `run()` 会调用 `exec()`：

```cpp
void QThread::run()
{
    exec();
}
```

只要事件循环正常运转，目标线程中的 QObject 才能接收 queued signal、投递事件、`deleteLater()` 和定时器超时。

若派生类重载 `run()` 却不调用 `exec()`：

```cpp
class ComputeThread final : public QThread
{
protected:
    void run() override
    {
        calculate();
        // 返回后线程结束；这里从未运行事件循环。
    }
};
```

这适合自包含的阻塞计算，但不能再假设移动进去的 Worker 槽、`QTimer` 或 queued invocation 会运行。事件被排入队列并不等于有人处理队列。

还有一个常见饥饿问题：即使调用过 `exec()`，一个长时间不返回的 Worker 槽仍会独占事件循环。应将任务拆成小步、使用真正的异步 API，或者在专用阻塞循环中自行检查停止条件；不要把 `processEvents()` 当作通用并发方案。

## 5. `exec()`、`quit()` 与 `exit()`

### 5.1 `exec()`

```cpp
int code = exec();
```

`exec()` 在当前 QThread 管理的线程中进入事件循环，直到有人调用 `exit(code)` 或 `quit()`。它返回传给 `exit()` 的退出码；由 `quit()` 退出时返回 0。

`exec()` 是 protected 成员，通常只会在重载的 `run()` 中直接调用。默认 `run()` 已经调用它，不必再次嵌套事件循环。

### 5.2 `quit()`

```cpp
thread->quit();
```

等价于 `exit(0)`，要求线程事件循环退出。若线程没有事件循环，它什么也不做。它也不会自动打断正在执行的长槽；只有槽返回，事件循环才有机会处理退出。

### 5.3 `exit(returnCode)`

```cpp
thread->exit(2);
```

`exit()` 让事件循环带指定返回码离开。多数应用只需要 `quit()`；退出码只有在自定义 `run()` 读取 `exec()` 返回值时才有实际意义。

`quit()` / `exit()` 控制的是事件循环，`requestInterruption()` 控制的是业务任务的协作停止意图，两者不是同一件事。健壮的关闭流程经常需要两者一起使用。

## 6. 协作式中断

### 6.1 请求不是强杀

```cpp
thread->requestInterruption();
```

这只设置线程的中断请求状态：

- 不会终止线程；
- 不会自动退出事件循环；
- 不会抛异常；
- 不会强制打断系统调用或一个正在运行的槽；
- 业务代码必须主动查询并退出。

工作线程内部检查：

```cpp
void Worker::processBatch()
{
    for (const Item &item : items) {
        if (QThread::currentThread()->isInterruptionRequested())
            return;
        processOne(item);
    }
}
```

不要在每条极轻量指令后查询，通常在批次边界、循环轮次或可安全提交状态的位置检查。检查太少会导致停止延迟过大，检查位置不安全则可能留下半更新状态。

### 6.2 谁能查询

```cpp
bool requested = QThread::currentThread()->isInterruptionRequested();
```

该查询本意是供当前正在运行的任务使用。返回值只说明“有人希望停止”，不代表线程已经或马上结束。对主线程调用 `requestInterruption()` 没有效果，Qt 会给出警告。

### 6.3 事件驱动 Worker 的停止槽

可给 Worker 提供停止槽：

```cpp
class Worker : public QObject
{
    Q_OBJECT
public slots:
    void stop() { stopping = true; }
private:
    bool stopping = false; // 只在 Worker 所属线程访问
};
```

但如果 Worker 正被一个长槽占用，queued 的 `stop()` 也无法及时执行。此时应使用线程安全的原子标志或 `requestInterruption()`，让长任务在内部轮询；或者从根本上把任务拆小。

## 7. `wait()`：等待线程真正结束

Qt 6 提供截止时间版本：

```cpp
bool done = thread->wait(QDeadlineTimer(3000));
```

以及传统毫秒版本：

```cpp
bool done = thread->wait(3000);           // 最多 3000 ms
bool doneForever = thread->wait();        // 默认 ULONG_MAX，近似无限等待
```

返回 `true` 表示线程已经结束或本来就未运行，`false` 表示截止时间到达但线程仍未结束。

推荐把总等待预算作为一个截止时间传递：

```cpp
QDeadlineTimer deadline(3000);
thread->requestInterruption();
thread->quit();

if (!thread->wait(deadline)) {
    qWarning() << "worker did not stop within shutdown budget";
}
```

相对毫秒数在多层函数中容易被每层重新计算，导致总等待超过预期；`QDeadlineTimer` 表达同一个绝对预算，适合贯穿关闭链。

### 7.1 不要等待自己

工作线程若对代表自己的 QThread 调用 `wait()`，它在等待自己结束，而自己必须先从 `wait()` 返回才能结束，构成自死锁。

### 7.2 GUI 线程中的无限等待

GUI 线程调用无限期 `wait()` 会冻结界面，也阻止 GUI 线程处理 queued 回调。若 Worker 的退出又依赖 GUI 线程执行某个槽，就会互相等待。

程序退出阶段可以在清晰、有限的关闭协议中短暂阻塞；交互期间更适合监听 `finished()`。若必须等待，设置有意义的上限并明确超时策略。

### 7.3 BlockingQueuedConnection 的死锁

`Qt::BlockingQueuedConnection` 会让发送线程等待接收槽完成。在同线程使用会直接死锁；跨线程时，如果接收线程又在 `wait()` 当前发送线程，也会形成循环等待。

线程通信优先设计为异步信号与结果信号。只有明确画出等待关系、能证明无环时，才考虑阻塞式连接。

## 8. `finished()` 与删除时机

```cpp
connect(thread, &QThread::finished,
        worker, &QObject::deleteLater);
```

`finished()` 发出时，关联线程的事件循环已经停止，不再处理普通事件；但 Qt 保证 deferred-delete 事件仍可用于清理该线程中的对象，因此这是官方推荐的 Worker 清理连接。

不要从主线程直接 `delete worker`。QObject 的定时器、socket、子对象及析构逻辑都可能依赖其所属线程，跨线程直接删除可能造成竞态和警告。

QThread 控制对象则通常属于主线程：

```cpp
connect(thread, &QThread::finished,
        thread, &QObject::deleteLater);
```

这里信号从关联线程发出，但接收对象 `thread` 的归属通常是主线程，所以删除事件会投递到主线程。

### 8.1 析构前必须结束

销毁仍在运行的普通 QThread 对象会导致程序崩溃。拥有线程的控制器应建立明确析构协议：

```cpp
Controller::~Controller()
{
    workerThread.requestInterruption();
    workerThread.quit();
    if (!workerThread.wait(3000))
        qWarning() << "worker shutdown timed out";
}
```

实际工程中不能在超时后直接让作为成员的 QThread 析构，因为线程仍可能运行。应确保任务本身存在可靠的协作停止点；超时必须升级为应用层错误处理，而不是忽略。

一个特殊例外是 Qt 6.3 起由 `QThread::create()` 创建的 QThread：运行中删除它时，Qt 会请求中断、要求事件循环退出并阻塞等待完成。这个便利不适用于任意 QThread 子类或普通构造的 QThread。

## 9. `terminate()` 与 `setTerminationEnabled()`

```cpp
thread->terminate();
thread->wait();
```

`terminate()` 可能在目标线程执行任意一条指令时将其终止。它可能恰好发生在：

- mutex 已加锁但尚未解锁；
- 容器正在修改内部结构；
- 文件只写入一半；
- 数据库事务尚未提交或回滚；
- RAII 对象尚未析构；
- 第三方库持有内部全局锁。

因此它可能造成永久死锁、资源泄漏或数据损坏。操作系统何时真正终止也不确定，所以调用后仍需 `wait()`；这并不能修复已破坏的状态。

protected 静态函数 `setTerminationEnabled(bool)` 只能控制调用线程是否允许被 `terminate()`：

```cpp
QThread::setTerminationEnabled(false);
updateCriticalState();
QThread::setTerminationEnabled(true);
```

这不是普通意义上的安全临界区。若禁用期间收到终止请求，重新启用时调用线程会立即被终止，函数甚至不会返回。它也不能替代 mutex 或事务。除非是在封装极底层、已经理解平台后果的线程运行时中，否则不要依赖这组 API。

## 10. 一套可复用的关闭协议

### 10.1 事件驱动任务

```cpp
void Controller::stopWorker()
{
    if (!thread->isRunning())
        return;

    thread->requestInterruption(); // 长步骤可主动观察
    thread->quit();                // 让事件循环退出
}

void Controller::onThreadFinished()
{
    thread = nullptr;              // 对象已安排 deleteLater
}
```

正常交互中不要紧跟 `wait()`，让 `finished()` 异步完成收尾。应用析构阶段若必须保证资源已经释放，再使用有界等待。

### 10.2 阻塞式任务

```cpp
void WorkerThread::run()
{
    while (!isInterruptionRequested()) {
        WorkItem item;
        if (!queue.take(item, 200))
            continue;              // 定期回到中断检查点
        process(item);
    }
}
```

若底层阻塞调用可以无限等待，中断标志永远没有机会被检查。应选用带超时或可取消的 API，或在关闭时唤醒条件变量/socket。`requestInterruption()` 不能神奇地中断任意阻塞系统调用。

### 10.3 状态机比零散布尔值更可靠

复杂 Worker 建议明确状态：

```text
Idle -> Starting -> Running -> StopRequested -> Finishing -> Stopped
```

只允许控制线程发起状态迁移，Worker 用信号报告确认。这样可以定义重复 start/stop、启动途中停止、失败退出和超时等边界，避免“看起来已经停了”的模糊状态。

## 11. 常见错误与修正

### 错误 1：把槽直接写进 QThread 子类

```cpp
class MyThread : public QThread
{
public slots:
    void doWork(); // 不会仅因继承 QThread 就进入新线程
};
```

修正：业务槽放到独立 Worker 并 `moveToThread()`；若任务只是一个同步函数，则重载 `run()`，不要混用两种模型。

### 错误 2：给 Worker 设置 QThread 父对象

```cpp
auto *worker = new Worker(thread);
worker->moveToThread(thread); // 失败：有父对象
```

修正：Worker 创建时无 parent，在线程结束时通过 `finished() -> deleteLater()` 清理。

### 错误 3：只调用 `quit()` 停止长计算

`quit()` 只要求事件循环退出。长槽若还没有返回，事件循环无法响应；无事件循环的 `run()` 中它更是无效。修正：同时设计协作式停止检查。

### 错误 4：只调用 `requestInterruption()` 停止事件循环

中断请求不会自动停止事件循环。修正：事件驱动线程通常同时 `requestInterruption()` 和 `quit()`，分别覆盖业务循环和事件循环。

### 错误 5：在主线程直接删除 Worker

修正：把 `QThread::finished` 连接到 Worker 的 `deleteLater()`，让 deferred deletion 在正确线程完成。

### 错误 6：线程对象离开作用域但线程还在跑

```cpp
void startBadly()
{
    QThread thread;
    thread.start();
} // thread 析构时关联线程可能仍在运行
```

修正：让控制对象的生命周期覆盖整个任务，并在析构前完成停止与等待。

### 错误 7：用 `sleep()` 等待状态变化

休眠既不提供同步关系，也不能保证另一线程已经执行到目标位置。使用信号、mutex/condition、future 或 `finished()`；时间不是同步原语。

## 12. 如何选择并发工具

| 需求 | 更合适的工具 |
|---|---|
| 一个长期存在、拥有 QObject/定时器/socket 的事件线程 | `QThread + Worker` |
| 一个自包含的阻塞循环 | QThread 子类并重载 `run()` |
| 一次性函数，仍需直接管理线程对象 | `QThread::create()` |
| 大量短任务 | `QThreadPool + QRunnable` |
| 映射、过滤、归约等数据并行 | Qt Concurrent |
| 需要进度、结果、取消组合 | `QFuture` / `QPromise` / `QFutureWatcher` |

不要为每个很小的工作项创建一个长期 QThread。平台线程有栈空间、调度和创建成本；任务型负载通常交给线程池更合理。

## API 速查表
本篇只收录和 Worker 模式、事件循环、停止等待、安全销毁直接相关的 `QThread` API；线程标识、优先级、栈大小、`QThread::create()` 等启动配置放在上篇理解更顺。查表时先区分“让事件循环退出”“请求业务停止”和“等待线程结束”，这三件事不能互相替代。

| 类别 | API | 是做什么的 | 使用时重点注意 |
|---|---|---|---|
| 事件循环 | `exec()` | 在当前线程中进入 Qt 事件循环 | 通常由默认 `run()` 调用；没有事件循环就没有 queued 槽、timer、`deleteLater()` 的正常处理 |
| 事件循环 | `exit(int retcode = 0)` | 请求事件循环带返回码退出 | 不会打断正在执行的长槽；无事件循环时没有实际退出对象 |
| 事件循环 | `quit()` | 请求事件循环以 `0` 返回 | 等价于 `exit(0)`；不能代替业务取消 |
| 协作停止 | `requestInterruption()` | 设置中断请求标记 | 只是请求，工作代码必须主动检查 |
| 协作停止 | `isInterruptionRequested() const` | 查询当前线程对象是否收到中断请求 | 阻塞调用、长循环和批处理步骤里要安排安全检查点 |
| 等待 | `wait(QDeadlineTimer deadline = QDeadlineTimer::Forever)` | 阻塞等待线程结束或到达截止时间 | 不能等待当前线程自己；GUI 线程无限等待会冻结界面 |
| 等待 | `wait(unsigned long time)` | 按毫秒等待线程结束 | `ULONG_MAX` 语义接近永久等待；超时不会取消线程 |
| 信号 | `started()` | 线程开始执行时发出 | queued 接收槽会在接收者所属线程按事件循环时序执行 |
| 信号 | `finished()` | `run()` 即将结束或已经结束时发出 | 常连接 Worker 的 `deleteLater()`，让对象在所属线程清理 |
| 强制终止 | `terminate()` | 请求强制结束线程 | 极危险，可能让锁、文件、共享状态停在半更新状态 |
| 强制终止 | `setTerminationEnabled(bool enabled = true)` | 控制当前线程是否允许被 `terminate()` 终止 | 若终止请求已挂起，重新启用时可能立刻终止当前线程 |
| 扩展点 | `run()` | 新线程实际执行入口 | 默认实现调用 `exec()`；重写后若不调用 `exec()` 就没有事件循环 |

## 14. 延伸理解：线程正确性来自协议

QThread 只提供线程的生命周期和事件循环机制。真正的正确性来自应用自己定义的协议：

- 谁拥有控制对象和 Worker；
- 哪个线程可以读写哪一份状态；
- 工作怎样被提交、确认和取消；
- 阻塞点怎样被唤醒；
- 关闭是否有总时间预算；
- 超时后如何避免带着活动线程析构；
- 最终由谁在什么线程删除对象。

把这些问题写成明确的状态和信号流，远比在各处零散调用 `quit()`、`wait()` 更可靠。最稳妥的默认原则是：业务状态只在 Worker 线程访问，跨线程通过信号传递不可变参数，停止采用协作协议，销毁由 `finished()` 驱动。

## 15. 总结

1. QThread 控制对象通常属于创建线程，Worker 才属于工作线程。
2. `moveToThread()` 改变 QObject 的线程归属，但有 parent 的对象不能移动。
3. queued 槽、定时器和 `deleteLater()` 都依赖目标线程事件循环。
4. `quit()` 停事件循环，`requestInterruption()` 表达业务停止请求，两者解决不同问题。
5. `wait()` 用于确认线程已经结束，最好设置截止时间且绝不能等待自己。
6. `finished() -> worker->deleteLater()` 是 Worker 清理的标准连接。
7. 普通 QThread 析构前必须已经停止；`QThread::create()` 的运行中删除规则是特殊例外。
8. `terminate()` 无法保证清理和状态一致性，只能视为极端失败手段。
9. 长任务必须主动提供取消点，阻塞调用也必须能超时或被唤醒。
10. 可靠线程代码的核心不是“启动一个线程”，而是完整、无环、可验证的关闭与所有权协议。
