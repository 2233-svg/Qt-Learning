# Qt QThreadPool 深入笔记：任务调度、线程复用与所有权

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QThreadPool>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QThreadPool`  
> 定位：用有限数量的平台线程执行大量独立任务，并复用空闲线程

`QThreadPool` 管理一组工作线程和一个等待队列。调用者提交的是“任务”，线程池决定由哪条线程、在什么时候执行。它适合短到中等长度、彼此大体独立的工作，不适合要求某个 QObject 永久固定在线程中并依赖事件循环的服务。

## 1. CMake 与最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

Qt 6 可以直接提交 callable：

```cpp
#include <QCoreApplication>
#include <QDebug>
#include <QThread>
#include <QThreadPool>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QThreadPool *pool = QThreadPool::globalInstance();
    pool->start([] {
        qInfo() << "running on" << QThread::currentThread();
        performIndependentWork();
    });

    pool->waitForDone();
    return 0;
}
```

`start()` 返回时任务可能尚未开始。lambda 在某条池线程上运行，不能直接操作 GUI 控件；结果应通过线程安全数据结构、queued signal 或 `QMetaObject::invokeMethod()` 送回对象所属线程。

## 2. 线程池解决什么问题

每个任务都创建一个 QThread 会反复支付线程创建、销毁、栈内存和调度成本。线程池把“任务数量”和“线程数量”解耦：

```text
提交方                     QThreadPool
Task A --\                 ┌─ Worker 1：执行 A
Task B ----> 等待队列 ---->├─ Worker 2：执行 B
Task C --/                 └─ Worker 3：空闲/复用
```

当活动线程数未达到 `maxThreadCount()`，池可立即安排任务；否则任务进入运行队列。工作线程完成当前任务后继续取下一项，而不是立刻销毁。

线程复用意味着：

- 不保证同一个任务类型总在同一线程执行；
- 不保证两个连续任务使用同一线程；
- 不应在线程局部状态中偷偷保存跨任务业务上下文；
- 一个任务返回后，线程可能继续执行其他调用者提交的任务。

## 3. 全局池与私有池

### 3.1 全局实例

```cpp
QThreadPool *pool = QThreadPool::globalInstance();
```

全局池由 Qt 管理，也常被 Qt Concurrent 等设施使用。它适合全应用共享的普通 CPU 任务，但某个模块若提交大量阻塞任务，可能耗尽线程并拖慢其他不相关功能。

### 3.2 私有实例

```cpp
QThreadPool pool;
pool.setMaxThreadCount(4);
pool.start([] { doWork(); });
pool.waitForDone();
```

私有池可隔离并发额度、栈大小、优先级、服务等级和销毁时机。析构函数会等待所有 Runnable 完成，所以不要在仍可能无限阻塞的任务上让局部线程池突然离开作用域。

选择原则：共享池节省资源，私有池提供隔离；不要机械地为每个对象创建一个池。

## 4. 提交任务：`start()`

### 4.1 提交 callable

```cpp
pool->start([path = std::move(path)] {
    indexFile(path);
});
```

callable 会被内部保存，捕获对象的生命周期必须覆盖实际执行时刻。避免按引用捕获即将离开作用域的局部变量：

```cpp
QString path = obtainPath();
pool->start([&path] { use(path); }); // 错误：执行时 path 可能已销毁
```

应按值捕获，或使用具有清晰共享所有权的值对象。若捕获 QObject 指针，需要考虑对象可能先销毁，可使用 `QPointer` 检查；但即使指针仍有效，也不能跨线程直接调用非线程安全成员。

### 4.2 提交 `QRunnable`

```cpp
class HashTask final : public QRunnable
{
public:
    explicit HashTask(QByteArray data) : data(std::move(data)) {}

    void run() override
    {
        result = QCryptographicHash::hash(data,
                                          QCryptographicHash::Sha256);
    }

private:
    QByteArray data;
    QByteArray result;
};

pool->start(new HashTask(payload));
```

QRunnable 默认 `autoDelete() == true`，池在 `run()` 返回后自动删除任务对象。提交后调用者不再拥有它，也不能继续解引用原指针。

若关闭自动删除：

```cpp
auto *task = new HashTask(payload);
task->setAutoDelete(false); // 必须在提交前设置
pool->start(task);
pool->waitForDone();
delete task;
```

提交后再修改 auto-delete 标志是未定义行为。关闭自动删除意味着调用者必须证明任务不再排队或运行后才能销毁它。

## 5. 队列优先级不是线程优先级

```cpp
pool->start(highTask, 10);
pool->start(normalTask, 0);
pool->start(lowTask, -10);
```

`start(..., priority)` 的整数只用于决定等待队列的取出顺序，数值越高越优先。它不会抢占已经运行的任务，也不改变操作系统线程优先级。

```cpp
pool->setThreadPriority(QThread::LowPriority);
```

`threadPriority` 才是新建工作线程使用的 QThread 优先级。默认是 `InheritPriority`，从 QThreadPool 对象所属线程继承。已创建的池线程不应被假定会因后续 setter 立即更新。

高队列优先级也不等于严格实时保证。若所有线程都被长任务占满，更高优先级的新任务仍要等待。

## 6. 并发上限与活动计数

```cpp
pool->setMaxThreadCount(QThread::idealThreadCount());
int limit = pool->maxThreadCount();
int active = pool->activeThreadCount();
```

默认上限为 `QThread::idealThreadCount()`。即使将最大数设置为 0 或负数，池仍会使用至少一条线程。

`activeThreadCount()` 是瞬时观测值，不是同步屏障。它可能刚读完就变化，也可能因 `reserveThread()` 大于 `maxThreadCount()`。不要写“active 为 0 就能安全释放共享资源”这样的逻辑；用任务完成信号、future 或 `waitForDone()` 建立完成关系。

并发数并非越高越快：

- CPU 密集任务通常接近可用核心数；
- 内存带宽密集任务可能在更低并发就饱和；
- I/O 阻塞任务能容忍更高并发，但大量阻塞可能仍应使用异步 I/O；
- 第三方库、数据库连接池或远端服务可能有更低的容量上限。

## 7. 空闲线程过期：`expiryTimeout`

```cpp
pool->setExpiryTimeout(30'000);
int timeout = pool->expiryTimeout();
```

空闲超过该毫秒数的线程会退出，需要时再创建。默认 30 秒。负值关闭过期机制，使新建线程一直保留到池销毁。

修改值不会影响已经运行的线程，只影响之后创建的线程，所以应在第一次 `start()` 前配置。

短过期时间降低空闲资源占用，却增加下一批任务重建线程的延迟；负值减少抖动，却长期保留线程栈和系统资源。它是容量与延迟的权衡，不是任务超时。

## 8. 栈大小、优先级与服务等级

### 8.1 栈大小

```cpp
pool->setStackSize(2 * 1024 * 1024);
uint bytes = pool->stackSize();
```

0 表示使用操作系统默认值。设置超出平台限制可能导致线程启动失败。深递归或大栈对象需要更多栈，但通常更应先消除无界递归、把大数据放到堆上。

### 8.2 线程优先级

```cpp
pool->setThreadPriority(QThread::NormalPriority);
```

该属性应用于新工作线程，平台可能忽略某些优先级。它不能替代正确的任务拆分和背压。

### 8.3 Quality of Service（Qt 6.9）

```cpp
pool->setServiceLevel(QThread::QualityOfService::Eco);
auto qos = pool->serviceLevel();
```

`Auto` 让平台采用默认策略，`High` 偏向高性能核心，`Eco` 偏向节能核心。只有调用 setter 后创建的线程使用新等级，而且并非所有平台都支持。

QoS 是调度提示，不是速度、核心位置或截止时间保证。队列 priority、QThread priority 和 QoS 分别处于不同层次，不要混为一谈。

## 9. `tryStart()`：无空闲容量就不排队

```cpp
if (!pool->tryStart([] { refreshPreview(); })) {
    qInfo() << "skip this optional refresh";
}
```

`tryStart()` 只在调用时存在可用线程时启动任务；否则返回 `false`，任务不会进入等待队列。它适合允许丢弃或由调用者降级处理的工作，如过期缩略图刷新。

对于 `QRunnable *`，成功时按 auto-delete 规则转移所有权；失败时 Runnable 所有权仍在调用者：

```cpp
auto *task = new PreviewTask(input);
if (!pool->tryStart(task))
    delete task;
```

它不是“任务最终一定执行”的 API。需要可靠执行就用 `start()` 或建立自己的有界队列与重试策略。

## 10. 清理等待队列：`clear()` 与 `tryTake()`

### 10.1 `clear()`

```cpp
pool->clear();
```

移除所有尚未开始的 Runnable。已经运行的任务不会停止；auto-delete 为 true 的待执行对象会被删除。callable 任务也不再执行。

因此 `clear()` 是“清空等待队列”，不是“取消线程池”。运行中任务仍需要自己的协作式取消机制。

### 10.2 `tryTake()`

```cpp
if (pool->tryTake(task)) {
    // 任务尚未开始，所有权已回到调用者。
    delete task;
}
```

若任务仍在队列中，`tryTake()` 移除它并返回 true；不论其 auto-delete 设置如何，成功后所有权都交回调用者。若已经开始或找不到则返回 false。

不要对 auto-delete Runnable 依赖 `tryTake()`。原对象可能已经运行并被删除，其地址随后被另一对象复用，线程池按同一指针值移除错误任务，这就是 ABA 问题。官方建议只对 `autoDelete() == false` 的 Runnable 使用它。

## 11. 预留线程与容量记账

### 11.1 外部阻塞占用：`reserveThread()` / `releaseThread()`

```cpp
pool->reserveThread();
performBlockingWorkOutsidePool();
pool->releaseThread();
```

这对调用不会把一条 QThread 指针交给你。它调整池的容量记账：告诉线程池“有一份线程资源正被看不见的外部工作占用”，完成后归还。

`reserveThread()` 会增加报告的活动数，所以 `activeThreadCount()` 可能超过最大数。即使预留达到或超过最大数，池仍至少允许一条线程继续运行任务。

一个容易忽略的高级用法：没有先 reserve 就调用 `releaseThread()`，会临时提高可用容量，适合某个池任务即将长时间睡眠时让别的任务继续；等待结束后必须调用 `reserveThread()` 恢复记账。配对错误会让池长期过量或不足调度。

### 11.2 在预留容量上启动任务

```cpp
pool->reserveThread();
pool->startOnReservedThread([] {
    performReservedWork();
});
```

`startOnReservedThread()`（Qt 6.3）释放此前的一份预留，并使用它运行 Runnable 或 callable。调用它之前必须确实有配对的预留。

它不是线程亲和性 API：不能指定某条具体平台线程，也不能依赖后续任务仍在同一线程。

## 12. 重复运行同一个 Runnable

QThreadPool 支持 Runnable 在自己的 `run()` 内调用 `tryStart(this)` 再次调度：

```cpp
void RepeatingTask::run()
{
    processOneBatch();
    if (hasMoreWork())
        QThreadPool::globalInstance()->tryStart(this);
}
```

auto-delete 开启时，最后一个执行 `run()` 的线程退出后才删除对象。这里可能有多个 `run()` 并发访问同一对象，所以状态必须同步。

不要从外部对同一个 auto-delete Runnable 多次调用 `start()`，这会产生删除竞态。多数周期任务更适合每轮创建独立任务，或使用明确的共享状态和 future 链。

## 13. 等待全部任务完成

Qt 6.8 起可传绝对截止时间：

```cpp
bool complete = pool->waitForDone(QDeadlineTimer(5000));
```

传统重载接受毫秒数：

```cpp
bool complete = pool->waitForDone(5000);
```

返回 true 表示所有线程完成并退出，false 表示截止时仍有工作。无参数的 QDeadlineTimer 版本默认 `Forever`。

`waitForDone()` 会阻塞调用线程。GUI 线程中调用会冻结界面；若池任务又用 BlockingQueuedConnection 等待 GUI 线程，会死锁。日常流程应通过结果信号或 QFutureWatcher 异步收尾，只在明确的关闭阶段使用有界等待。

线程池无法强制让一个无限阻塞的任务完成。超时返回 false 后，必须继续保证池和任务引用的数据仍存活。

## 14. `contains()`

```cpp
bool managed = pool->contains(QThread::currentThread());
```

`contains(const QThread *)` 判断某个线程是否由该池管理。它适合断言或诊断当前执行环境，不应被当作业务同步条件。

## 15. 返回结果的正确方式

普通 `start()` 不直接返回值。可以把结果投递给具有稳定生命周期的接收对象：

```cpp
QPointer<ResultReceiver> receiver = this;

pool->start([receiver, input] {
    Result value = calculate(input);
    if (!receiver)
        return;

    QMetaObject::invokeMethod(receiver, [receiver, value = std::move(value)] {
        if (receiver)
            receiver->accept(value);
    }, Qt::QueuedConnection);
});
```

外层检查与 queued lambda 执行之间仍可能发生销毁，因此内层再次检查 `QPointer`。接收代码在 receiver 所属线程运行。

更复杂的结果、进度、取消和异常传播通常使用 `QtConcurrent`、`QPromise`、`QFuture` 和 `QFutureWatcher`，它们仍可建立在线程池之上。

## 16. 背压与任务粒度

线程数有限不代表等待队列有界。生产速度长期高于消费速度时，队列会增长，输入数据和捕获对象也随之占用内存。

常见治理方式：

- 合并重复任务，只保留最新状态；
- 使用 `tryStart()` 丢弃非关键刷新；
- 在提交层维护有界队列；
- 把许多极小任务合成批次，降低排队和调度成本；
- 将大任务切成能公平轮转且可取消的块；
- 为阻塞型和 CPU 型负载使用不同私有池，避免互相饿死。

任务太小，调度开销可能超过计算；任务太大，取消延迟和队头阻塞增大。应测量真实工作负载，而不是只看 CPU 占用。

## 17. 常见错误

### 错误 1：在线程池任务中直接更新 QWidget

GUI 对象只能在 GUI 线程访问。把结果 queued 回 GUI 对象。

### 错误 2：按引用捕获局部变量

任务异步执行时引用可能悬空。优先按值捕获，明确共享所有权。

### 错误 3：提交 auto-delete Runnable 后继续访问

提交成功后池可能立刻执行并删除它。把指针视为已经失效。

### 错误 4：把 `clear()` 当成取消

它只清除未开始项。运行中任务必须支持协作停止。

### 错误 5：认为队列 priority 会抢占运行任务

priority 只改变尚未开始项的顺序，不能暂停当前任务。

### 错误 6：把池线程当作固定事件线程

任务没有固定线程身份，且不能假定存在为业务对象长期服务的事件循环。需要 QObject 亲和性、timer 或 socket 时使用 QThread + Worker。

### 错误 7：私有池先析构，任务引用的数据随后才销毁

析构会等待任务；若任务依赖当前线程继续处理事件，可能卡住。成员声明/析构顺序和关闭协议必须清晰。

## API 速查表
`QThreadPool` 的接口围绕四件事：提交任务、控制容量、配置新建池线程、收尾等待。它调度的是“任务”，不是固定的业务线程；查表时要特别分清 queued、running、finished 三种状态，因为所有权和取消策略在这三种状态下完全不同。

| 类别 | API | 是做什么的 | 使用时重点注意 |
|---|---|---|---|
| 构造 | `QThreadPool(QObject *parent = nullptr)` | 创建私有线程池 | 析构会等待任务结束；适合隔离某一类任务容量 |
| 生命周期 | `~QThreadPool()` | 销毁线程池 | 运行中任务不应无限阻塞，否则析构可能卡住 |
| 全局池 | `globalInstance()` | 获取应用级共享线程池 | Qt Concurrent 等也可能使用它，别让阻塞任务占满全局池 |
| 提交 | `start(QRunnable *runnable, int priority = 0)` | 启动或排队 `QRunnable` | priority 只影响等待队列顺序；默认 auto-delete 任务提交后不要再访问 |
| 提交 | `start(Callable &&functionToRun, int priority = 0)` | 用 callable 创建 runnable 并提交 | 捕获值的生命周期要覆盖实际执行时刻；不要直接操作 GUI |
| 提交 | `tryStart(QRunnable *runnable)` | 有即时容量才启动 runnable | 失败时不排队，调用者仍要处理 runnable 所有权 |
| 提交 | `tryStart(Callable &&functionToRun)` | 有即时容量才启动 callable | 失败时 Qt 会删除内部创建的 runnable |
| 预留提交 | `startOnReservedThread(QRunnable *runnable)` | 在预留容量上启动 runnable | 需先 `reserveThread()`；不保证具体线程身份 |
| 预留提交 | `startOnReservedThread(Callable &&functionToRun)` | 在预留容量上启动 callable | 同样只是容量记账，不是绑定某条线程 |
| 空闲线程 | `expiryTimeout() const` | 读取空闲线程过期时间 | 单位毫秒；负值通常表示不自动过期 |
| 空闲线程 | `setExpiryTimeout(int expiryTimeout)` | 设置空闲线程多久后退出 | 只影响之后创建或空闲的池线程 |
| 容量 | `maxThreadCount() const` | 读取最大线程数 | 这是上限设置，不等于当前运行数 |
| 容量 | `setMaxThreadCount(int maxThreadCount)` | 设置最大并发线程数 | 即使小于 1，线程池通常仍至少可运行一个任务 |
| 容量 | `activeThreadCount() const` | 读取当前活动线程数 | 是瞬时快照；预留线程可能使其超过最大值 |
| 栈 | `setStackSize(uint stackSize)` | 设置新建池线程栈大小 | `0` 使用平台默认；已存在的线程不一定受影响 |
| 栈 | `stackSize() const` | 读取新线程栈大小设置 | |
| 优先级 | `setThreadPriority(QThread::Priority priority)` | 设置新建池线程的 OS 优先级 | 平台可能忽略或限制 |
| 优先级 | `threadPriority() const` | 读取池线程优先级设置 | 不等于任务队列 priority |
| 服务等级 | `setServiceLevel(QThread::QualityOfService serviceLevel)` | 设置新建池线程 QoS | Qt 6.9 起；只在部分平台有实际效果 |
| 服务等级 | `serviceLevel() const` | 读取 QoS 设置 | |
| 预留 | `reserveThread()` | 预留或占用一份线程池容量 | 必须和 `releaseThread()` 配对 |
| 预留 | `releaseThread()` | 释放预留容量 | 错配会破坏容量统计 |
| 等待 | `waitForDone(QDeadlineTimer deadline = QDeadlineTimer::Forever)` | 等待全部任务完成或到截止时间 | 只等待，不取消；调用线程会被阻塞 |
| 等待 | `waitForDone(int msecs)` | 按毫秒等待全部任务完成 | Qt 6.8 起内联便利形式；超时后任务仍可能继续运行 |
| 队列清理 | `clear()` | 移除尚未开始的任务 | 不影响正在运行的任务，也不是取消机制 |
| 检查 | `contains(const QThread *thread) const` | 判断线程是否由该池管理 | 只做归属检查，不提供同步保证 |
| 队列清理 | `tryTake(QRunnable *runnable)` | 尝试从等待队列移除指定 runnable | 对 auto-delete runnable 有 ABA 风险，通常只用于非自动删除任务 |

## 19. 总结

1. QThreadPool 调度任务并复用有限的线程，任务与线程没有固定一对一关系。
2. callable 适合简洁任务，QRunnable 适合自定义任务对象和所有权控制。
3. QRunnable 默认自动删除，auto-delete 必须在提交前决定。
4. `start()` 会排队，`tryStart()` 没有即时容量就失败。
5. 队列 priority、线程 Priority 和 QualityOfService 是三个不同概念。
6. `clear()` 与 `tryTake()` 只能处理未开始任务，无法强制取消正在执行的代码。
7. `tryTake()` 应只用于不自动删除的 Runnable，以避开 ABA 风险。
8. reserve/release 操作的是容量记账，不是取得或归还具体 QThread。
9. `waitForDone()` 只等待，不取消；GUI 线程中阻塞等待还可能造成死锁。
10. 真正稳定的线程池设计还需要结果回传、协作取消、背压、生命周期和任务粒度策略。
