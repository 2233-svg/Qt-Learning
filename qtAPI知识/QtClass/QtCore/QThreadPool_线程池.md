# Qt QThreadPool 线程池

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QThreadPool>`  
> 所属模块：`Qt6::Core`  
> 继承关系：`QObject -> QThreadPool`  
> 线程特征：文档标注所有成员函数为 thread-safe  
> 定位：复用一组 `QThread` 执行短任务，降低频繁创建/销毁线程的成本

## 它解决什么问题

如果每个后台任务都手动 `new QThread`，线程创建成本、生命周期、回收和并发上限都会很快失控。`QThreadPool` 维护一组可复用 worker 线程，你把 `QRunnable` 或零参数 callable 丢进去，它负责排队、调度、复用空闲线程，并在默认情况下回收 `QRunnable` 对象。

它适合大量短任务、互相独立的后台工作：

- 图片缩略图、文件扫描、索引构建。
- CPU 密集的分块计算。
- 不需要长期驻留线程状态的后台处理。
- 与 `QFuture`、`QtConcurrent`、`QPromise` 等上层并发工具协作。

它不适合需要长期事件循环、持久 QObject 线程归属、复杂线程内状态机的场景。这类需求通常应使用专门的 `QThread`、worker QObject 模式，或者更高层的 Qt Concurrent API。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QThreadPool>
#include <QRunnable>
```

qmake 工程使用：

```qmake
QT += core
```

## 最小可用示例

```cpp
#include <QDebug>
#include <QRunnable>
#include <QThread>
#include <QThreadPool>

class PrintTask : public QRunnable
{
public:
    void run() override
    {
        qDebug() << "running on" << QThread::currentThread();
    }
};

void submit()
{
    auto *task = new PrintTask;
    QThreadPool::globalInstance()->start(task);
} // 默认 autoDelete=true，线程池在 run() 返回后删除 task
```

Qt 6 的 callable 重载更适合轻量任务：

```cpp
QThreadPool::globalInstance()->start([] {
    expensiveStep();
});
```

callable 必须是零参数可调用对象。Qt 6.6 起这些重载不再局限于 `std::function<void()>`，可以处理 move-only callable。

## 核心使用模型

`start()` 并不保证立即创建新线程。线程池会先看当前活动线程数是否会超过 `maxThreadCount()`：

- 未超过：保留一个线程并运行任务。
- 会超过：把任务放入队列，等已有线程空闲后再执行。

`start(runnable, priority)` 的 `priority` 控制的是运行队列顺序，不是操作系统线程优先级。OS 线程优先级由 `threadPriority` 属性控制；服务质量由 Qt 6.9 的 `serviceLevel` 控制，且平台支持有限。

每个 Qt 应用有一个全局线程池，可通过 `QThreadPool::globalInstance()` 取得。需要隔离并发上限、过期策略或线程栈大小时，可以创建自己的 `QThreadPool` 对象。

## QRunnable 所有权

`QRunnable` 默认 `autoDelete() == true`。把这样的 runnable 交给 `start()` 或成功的 `tryStart()` 后，线程池取得所有权，并在 `run()` 返回后自动删除它。

如果你希望自己管理 runnable：

```cpp
auto *task = new MyRunnable;
task->setAutoDelete(false);
pool.start(task);
```

必须在提交前设置 `autoDelete`。文档明确说：提交后再修改 auto-delete 标志是未定义行为。

同一个 auto-delete runnable 不应多次从外部调用 `start()` 提交；这会制造竞争。若确实需要 runnable 自己在运行中再次排队，文档支持在 `QRunnable::run()` 内调用 `tryStart(this)`；auto-delete 开启时，最后一个退出 `run()` 的线程负责删除对象。

callable 重载内部会用 `QRunnable::create()` 生成 runnable。`tryStart(callable)` 若抢不到线程，会删除刚创建的 runnable 并返回 `false`。

## 线程数量与过期

`maxThreadCount` 默认取线程池创建时的 `QThread::idealThreadCount()`。即使设置为 `0` 或负数，线程池仍至少允许一个线程运行。

`activeThreadCount()` 表示正在工作的线程数量，但它可能大于 `maxThreadCount()`：`reserveThread()` 会增加报告的活动线程数，用于告诉线程池“有一个外部耗时操作应当算进容量”。

空闲线程默认 30000 ms 后过期退出。`setExpiryTimeout()` 可调整这个时间；负数表示新创建线程不因空闲过期，只在线程池销毁时退出。`expiryTimeout`、`stackSize`、`threadPriority`、`serviceLevel` 这类设置通常只影响之后创建的新线程，不会改变已经运行或已经创建的线程。

## 保留线程

`reserveThread()` 表示你要为外部用途预留一个线程名额，即使这会让活动线程数超过上限。完成后必须调用 `releaseThread()`。

`startOnReservedThread()`（Qt 6.3）会释放一个之前保留的线程，并用它运行给定 runnable 或 callable。如果没有保留线程却调用它，结果是未定义行为。

`releaseThread()` 有一个特殊用法：如果没有先 reserve 就调用，它会临时增加 `maxThreadCount()`。文档指出这适合线程睡眠等待更多工作时，让其他线程继续运行；等等待结束后要调用 `reserveThread()` 把计数恢复一致。普通业务代码不应把它当作扩大线程池的常规接口。

## 等待与清理

`clear()` 只移除尚未开始的队列任务；已经运行的任务不会被中断。被移除且 `autoDelete()==true` 的 runnable 会被删除。

`tryTake(runnable)` 只在 runnable 尚未开始时能移出队列。成功后所有权转回调用方，即使 runnable 原本 `autoDelete()==true`。如果 runnable 是 auto-delete，文档警告有 ABA 风险：原对象可能已经执行并释放，同一内存地址被新 runnable 复用，导致移错对象。因此建议只对非 auto-delete runnable 使用 `tryTake()`。

`waitForDone()` 阻塞当前线程，直到所有线程退出并从池里移除，或超时/截止时间到达。`waitForDone(int msecs)` 中 `msecs == -1` 表示一直等待。Qt 6.8 起推荐使用 `QDeadlineTimer` 重载。

`~QThreadPool()` 会阻塞，直到所有 runnable 完成。不要在 GUI 线程销毁仍有长任务的线程池，否则界面会卡住；也不要在持有任务所需锁时调用 `waitForDone()`，这很容易死锁。

## 与 QObject 和线程安全

`QThreadPool` 继承 `QObject`，可以带 parent 管理自身生命周期。但运行在线程池中的 `QRunnable` 不是 QObject 线程归属模型；它只是在线程池线程中执行 `run()`。

虽然文档说 `QThreadPool` 成员函数是 thread-safe，这不代表你的任务代码自动线程安全。任务之间共享数据时仍需锁、原子、队列信号槽或其他同步机制。不要直接从任务线程更新 GUI；要用 queued signal/slot、`QMetaObject::invokeMethod()` 或带上下文对象的 continuation 回到目标线程。

## 常见误区

- 把 `start()` 的 `priority` 当成 OS 线程优先级；它只影响队列顺序。
- 提交后修改 `QRunnable::autoDelete()`。
- 对同一个 auto-delete runnable 多次从外部 `start()`。
- 以为 `clear()` 会取消正在运行的任务；它只清理未开始的队列项。
- 对 auto-delete runnable 调 `tryTake()`，忽略 ABA 风险。
- 调用 `startOnReservedThread()` 前没有 `reserveThread()`。
- 设置 `expiryTimeout`、`stackSize`、`threadPriority` 后期待已存在的线程马上改变。
- 在 GUI 线程无期限 `waitForDone()`，或在持锁期间等待线程池完成。
- 在线程池任务里直接操作 GUI 对象。

## 逐项 API 语义

### `QThreadPool(QObject *parent = nullptr)`

创建线程池。默认 `maxThreadCount` 取创建时的 `QThread::idealThreadCount()`，`expiryTimeout` 为 30000 ms，`stackSize` 为 0，`threadPriority` 为 `QThread::InheritPriority`。

### `~QThreadPool()`

销毁线程池，并阻塞直到所有 runnable 完成。析构不是取消任务的工具。

### `globalInstance()`

返回应用全局线程池。适合普通短任务；需要独立调度策略时创建单独实例。

### `start(QRunnable *runnable, int priority = 0)`

排队或立即执行 runnable。若 `autoDelete()` 为 `true`，成功提交后线程池取得所有权并在 `run()` 返回后删除。`priority` 控制队列顺序。

### `start(Callable &&callableToRun, int priority = 0)`

把零参数 callable 包装为 runnable 并提交。适合 lambda 和函数对象。

### `tryStart(QRunnable *runnable)`

只有当前有可用线程时才立即运行。成功返回 `true`；失败不排队并返回 `false`，调用方仍需处理 runnable 所有权。

### `tryStart(Callable &&callableToRun)`

callable 版抢占执行。若没有可用线程，内部创建的 runnable 会被删除并返回 `false`。

### `startOnReservedThread(QRunnable *runnable)`（Qt 6.3）

释放一个预留线程并用它执行 runnable。调用前必须已经 `reserveThread()`；否则未定义。

### `startOnReservedThread(Callable &&callableToRun)`（Qt 6.3）

callable 版预留线程执行接口，约束同 `start(callable)`。

### `reserveThread()` / `releaseThread()`

手动调整线程池容量统计，用于外部耗时操作或预留执行。必须成对理解；错误使用会让 `activeThreadCount()` 与实际容量语义偏离。

### `activeThreadCount()`

返回当前活动线程数。可能大于 `maxThreadCount()`，尤其是使用 `reserveThread()` 后。

### `maxThreadCount()` / `setMaxThreadCount(int)`

查询或设置最大线程数。即使设置为非正数，线程池仍至少允许一个线程。

### `expiryTimeout()` / `setExpiryTimeout(int)`

查询或设置空闲线程过期时间。默认 30000 ms；负数禁用新线程的过期。只影响之后创建的线程，建议在线程池启动任务前设置。

### `stackSize()` / `setStackSize(uint)`

查询或设置新 worker 线程栈大小。默认 0 表示使用系统默认。只影响后续创建的新线程。

### `threadPriority()` / `setThreadPriority(QThread::Priority)`（Qt 6.2）

查询或设置新 worker 线程的 `QThread::Priority`。默认 `InheritPriority`。只影响之后启动的新线程。

### `serviceLevel()` / `setServiceLevel(QThread::QualityOfService)`（Qt 6.9）

查询或设置新线程的 QoS 级别。平台支持有限，具体行为参考 `QThread::setServiceLevel()`。

### `contains(const QThread *thread)`（Qt 6.0）

判断某个 `QThread` 是否由该线程池管理。

### `clear()`

移除尚未开始的 queued runnables；auto-delete runnable 会被删除。不会停止正在运行的任务。

### `tryTake(QRunnable *runnable)`

尝试从队列移除尚未开始的 runnable。成功后所有权转回调用方。建议只用于 `autoDelete()==false` 的 runnable，避免 ABA 风险。

### `waitForDone(QDeadlineTimer deadline = QDeadlineTimer::Forever)`（Qt 6.8）

等待所有线程退出并从池中移除，直到 deadline 到达。全部完成返回 `true`，超时返回 `false`。

### `waitForDone(int msecs)`

毫秒超时版本。`msecs == -1` 表示一直等到最后一个线程退出。

## API 速查表

| API | 作用 | 重点边界 |
| --- | --- | --- |
| `QThreadPool()` | 创建线程池 | 默认上限为 `QThread::idealThreadCount()` |
| `~QThreadPool()` | 销毁线程池 | 会阻塞直到任务完成 |
| `globalInstance()` | 获取全局线程池 | 适合普通短任务共享 |
| `start(QRunnable *, priority)` | 提交 runnable，必要时排队 | auto-delete 时线程池接管所有权；priority 是队列优先级 |
| `start(Callable, priority)` | 提交零参数 callable | Qt 6.6 起支持 move-only callable |
| `tryStart(QRunnable *)` | 有空闲线程才立即运行 | 失败不排队，调用方保留所有权 |
| `tryStart(Callable)` | callable 抢占执行 | 失败会删除内部 runnable |
| `startOnReservedThread(QRunnable *)`（Qt 6.3） | 用预留线程运行 runnable | 没有预留线程时未定义 |
| `startOnReservedThread(Callable)`（Qt 6.3） | 用预留线程运行 callable | callable 必须零参数 |
| `reserveThread()` | 预留一个线程名额 | 会提高报告的活动线程数 |
| `releaseThread()` | 释放预留名额 | 无 reserve 调用时有特殊容量语义 |
| `activeThreadCount()` | 查询活动线程数 | 可能大于 `maxThreadCount()` |
| `maxThreadCount()` / `setMaxThreadCount()` | 查询/设置最大线程数 | 至少仍会允许一个线程 |
| `expiryTimeout()` / `setExpiryTimeout()` | 查询/设置空闲过期时间 | 默认 30 秒；负数禁用新线程过期 |
| `stackSize()` / `setStackSize()` | 查询/设置新线程栈大小 | 已创建线程不受影响 |
| `threadPriority()` / `setThreadPriority()` | 查询/设置新线程优先级 | 只影响新 worker 线程 |
| `serviceLevel()` / `setServiceLevel()`（Qt 6.9） | 查询/设置新线程 QoS | 平台支持有限 |
| `contains()`（Qt 6.0） | 判断线程是否归该池管理 | 传入 `QThread *` |
| `clear()` | 清除未开始的队列任务 | 不停止运行中的任务 |
| `tryTake()` | 移出尚未开始的 runnable | auto-delete runnable 有 ABA 风险 |
| `waitForDone(QDeadlineTimer)`（Qt 6.8） | 等待全部线程退出 | 超时返回 `false` |
| `waitForDone(int)` | 毫秒超时等待 | `-1` 表示无限等待 |

## 一句话总结

`QThreadPool` 是执行短任务的低层线程复用器；用好它的关键是提交前确定 `QRunnable` 所有权，分清队列优先级和线程优先级，并谨慎处理 `clear()`、`tryTake()`、`waitForDone()` 这些会改变队列或阻塞调用线程的接口。
