# Qt QThread 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QThread>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QThread`  
> 定位：创建和管理原生线程，并为该线程提供 Qt 事件循环

## 1. 先拆开最关键的概念

`QThread` 有两个经常被混为一谈的身份：

1. 它是一个管理线程的 QObject。
2. 它会启动一个实际执行 `run()` 的原生线程。

`QThread` 对象本身默认属于创建它的线程，通常就是 GUI 线程；`run()` 和它创建的事件循环才在新线程运行。

```text
GUI 线程
  QThread 对象
  Controller 对象
       |
       | thread.start()
       v
工作线程
  QThread::run()
  QThread::exec() 的事件循环
  moveToThread() 后的 Worker 槽、定时器、queued 回调
```

因此，下面写法不会自动把 `heavyWork()` 放进后台：

```cpp
QThread thread;
thread.start();
thread.heavyWork(); // 仍在调用者线程执行
```

`QThread` 解决的是两类问题：

- 把阻塞 I/O、持续计算或设备控制移出 GUI/主线程。
- 为线程中的 QObject 提供事件循环，使 queued slot、`QTimer`、socket notifier 和 `deleteLater()` 有地方运行。

它不等于自动线程池，也不负责让任意对象天然线程安全。共享数据仍要靠不共享、消息传递或明确同步保护。

## 2. 首选模型：Worker 对象移入线程

绝大多数有事件、定时器、socket、连续任务或可取消任务的场景，推荐把工作对象移动到线程，而不是把业务代码塞进 `QThread` 子类。

```cpp
#include <QThread>

class Worker final : public QObject
{
    Q_OBJECT
public slots:
    void process(const QString &path)
    {
        // 此槽由 queued connection 调用时，在 workerThread 中执行。
        const QString result = parseFile(path);
        emit finished(result);
    }

signals:
    void finished(const QString &result);
};

class Controller final : public QObject
{
    Q_OBJECT
public:
    Controller()
    {
        m_worker = new Worker;
        m_worker->moveToThread(&m_thread);

        connect(&m_thread, &QThread::finished,
                m_worker, &QObject::deleteLater);
        connect(this, &Controller::requestProcess,
                m_worker, &Worker::process);
        connect(m_worker, &Worker::finished,
                this, &Controller::showResult);

        m_thread.start();
    }

    ~Controller() override
    {
        m_thread.requestInterruption();
        m_thread.quit();
        m_thread.wait();
    }

signals:
    void requestProcess(const QString &path);

private slots:
    void showResult(const QString &result);

private:
    QThread m_thread;
    Worker *m_worker = nullptr;
};
```

这里有几条非常实用的规则：

- `Worker` 在 `moveToThread()` 前不能有 parent；有 parent 的 QObject 不能跨线程移动。
- 连接的执行位置由接收 QObject 的线程亲和性和 connection type 决定，不由“发信号的代码在哪个类里”决定。
- 用 `finished -> deleteLater` 让 Worker 在它所属线程临近结束时按 Qt 对象模型销毁。
- 析构时先发出停止意图，再 `quit()` 退出线程事件循环，最后 `wait()` 建立明确的收尾边界。

Worker 的每个槽都应尽快返回事件循环。若一个槽长期阻塞，它不仅不能处理下一条 queued 请求，也不能响应 `quit()`、定时器或 `deleteLater()`。

## 3. `moveToThread()` 的边界

`moveToThread()` 是 `QObject` 的成员，不是 `QThread` 的成员：

```cpp
worker->moveToThread(&thread);
```

它会改变对象及其 QObject 子对象的线程亲和性。它不会：

- 把普通 C++ 成员、裸指针指向的外部对象自动移动。
- 让已有 parent 的 QObject 脱离父对象。
- 让跨线程直接函数调用变成异步调用。
- 让对象的成员数据自动线程安全。

定时器、网络对象等依赖事件循环的 QObject，应在目标线程中创建，或在正确迁移后通过 queued slot 启动。不要从 GUI 线程直接 `start()` 一个已属于工作线程的 `QTimer`。

## 4. 生命周期：启动、停止、等待

### 4.1 启动

```cpp
thread.start(QThread::NormalPriority);
```

`start()` 请求创建并运行原生线程。默认 `run()` 会调用 `exec()`，所以 Worker 模式能接收 queued slot。如果你重写 `run()` 且没有调用 `exec()`，该线程就没有 Qt 事件循环。

`started()` 在关联线程开始运行时发出。它适合触发初始化，但不要假设接收槽执行前已经完成全部 Worker 配置；需要严格顺序时，把初始化放在 Worker 的显式槽中，并用一个明确的请求信号触发。

### 4.2 请求停止

```cpp
thread.requestInterruption();
thread.quit();
```

- `requestInterruption()` 只是置位一个协作式取消请求；Qt 不会强制中断你的函数。
- `quit()` 等价于 `exit(0)`，只要求该线程的事件循环结束。
- 如果 Worker 正在阻塞 I/O 或长计算，代码必须自己检查 `isInterruptionRequested()`，或调用底层取消 API。

```cpp
void Worker::scan()
{
    for (const FileEntry &entry : m_entries) {
        if (QThread::currentThread()->isInterruptionRequested())
            return;
        index(entry);
    }
}
```

`quit()` 无法终止一个不进入 `exec()` 的自定义 `run()`，也无法抢占一个正在运行的长槽函数。

### 4.3 等待

```cpp
if (!thread.wait(QDeadlineTimer(std::chrono::seconds(5)))) {
    qWarning() << "worker did not stop in time";
}
```

`wait()` 阻塞调用者，直到线程结束或 deadline 到期。它是销毁线程相关资源前的重要同步点，但 GUI 线程不应无限期等待一个可能卡死的线程。停机流程要设定超时、日志和必要时的进程级恢复策略。

### 4.4 不要把 `terminate()` 当成正常停止

```cpp
thread.terminate(); // 高风险，只能作为最后手段
```

它可能在任意指令点终止线程，跳过 RAII 收尾、保持锁不释放、破坏库状态。正常设计应总是使用请求取消、关闭 I/O、退出事件循环和 `wait()`。

## 5. 两种可选模型

### 5.1 `QThread::create()`：一次性函数

```cpp
QThread *thread = QThread::create([] {
    compressLargeFile();
});

connect(thread, &QThread::finished,
        thread, &QObject::deleteLater);
thread->start();
```

适合只有一段短生命周期函数、不需要在线程内接收 queued slot 的任务。返回的对象仍需要 `start()`。

Qt 6.3 起，删除由 `QThread::create()` 创建且仍在运行的 `QThread`，Qt 会请求中断、请求其事件循环退出并等待结束；这只是此工厂模式的特例，不可推广到普通 `new QThread` 或派生类实例。一般仍应明确管理结束流程。

### 5.2 重写 `run()`：线程本身就是执行策略

```cpp
class HashThread final : public QThread
{
protected:
    void run() override
    {
        m_hash = calculateHash(m_path);
        // 未调用 exec()：这个线程没有 Qt 事件循环。
    }

public:
    QString m_path;
    QByteArray m_hash;
};
```

适合一次性、线性的计算，或确实需要定制线程启动细节的框架代码。代价是类成员同时可能被创建线程和工作线程访问；应在 `start()` 前完整配置，在线程结束后再读取结果，或以信号/锁进行同步。

若需要 Worker 风格事件循环，不要在 `run()` 里直接写一个无限循环；让默认 `run()` 调用 `exec()`，把工作拆成 queued slot。

## 6. 事件循环和对象线程亲和性

默认 `QThread::run()` 内部运行 `exec()`。这意味着下列机制依赖其继续活着：

- 发给 Worker 的 queued signal/slot。
- 在 Worker 线程启动的 `QTimer`。
- 该线程的 `QAbstractSocket` 和 socket notifier。
- `QObject::deleteLater()` 投递的延迟删除事件。

可以查询当前嵌套层数：

```cpp
if (QThread::currentThread()->loopLevel() > 1)
    qWarning() << "nested event loop is active";
```

它适合诊断，而不是业务逻辑判断。用 `loopLevel()` 决定是否释放资源或是否执行任务，通常意味着流程设计已被嵌套循环扭曲。

## 7. 优先级、QoS 与休眠

`Priority` 和 Qt 6.9 起的 `QualityOfService` 都只是给操作系统调度器的建议：

```cpp
thread.setPriority(QThread::HighPriority);
thread.setServiceLevel(QThread::QualityOfService::Eco);
```

- 优先级可能被系统权限、负载或平台策略忽略。
- QoS 表达性能/能耗倾向，`High` 偏性能，`Eco` 偏节能，`Auto` 交给平台。
- 不能用它们修复锁竞争、阻塞 I/O 或 O(n^2) 算法。

`sleep()`、`msleep()`、`usleep()` 会阻塞当前线程：

```cpp
QThread::msleep(20);
```

它们适合极少数底层测试或轮询退避；不要在 GUI 线程使用，也不要用来等待 Worker 完成。需要延迟调度用 `QTimer`，需要等待线程结束用 `wait()`。

## 8. 常见误区

### 在 QThread 子类的槽中写耗时工作

QThread 对象通常属于 GUI 线程，所以该槽也很可能在 GUI 线程运行。把工作放进移动后的 Worker，或在 `run()` 中执行。

### 以为 `requestInterruption()` 会杀掉线程

它只是标志位。循环、阻塞读取和第三方库调用都必须自己配合取消。

### 从 Worker 线程直接操作 QWidget

`QWidget` 必须只在 GUI 线程创建和访问。Worker 只发数据结果，GUI 槽负责更新界面。

### 用 `wait()` 修复所有竞态

`wait()` 只等待线程结束；运行期间的共享数据访问仍需要消息传递、不可变数据或同步原语。

### 没有事件循环却依赖 QTimer 或 queued slot

重写 `run()` 后忘记 `exec()` 是常见原因。线性计算适合没有事件循环；事件驱动 Worker 则必须保留它。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 静态查询 | `currentThread()` | 返回调用代码当前所在的 `QThread` 包装对象。 | 适合在线程内检查中断或亲和性；返回对象不转移所有权。 |
| 静态查询 | `currentThreadId()` | 返回当前原生线程的系统标识。 | 适合日志和诊断；不是跨进程或线程重建后稳定的业务 ID。 |
| 静态查询 | `isMainThread()` | 判断调用点是否位于 Qt 主线程。 | Qt 6.8 起可用；可用于断言 GUI 边界，不能代替对象线程亲和性检查。 |
| 静态查询 | `idealThreadCount()` | 返回系统建议的并行线程数。 | 这是环境快照，可能随 CPU 亲和性变化；线程池容量还要考虑 I/O、内存和任务性质。 |
| 静态调度 | `yieldCurrentThread()` | 主动让出当前线程剩余时间片。 | 操作系统可忽略；不是同步工具，也不能解决忙等或锁竞争。 |
| 构造 | `QThread(QObject *parent = nullptr)` | 创建线程管理对象，但不立即启动原生线程。 | 对象通常属于创建它的线程；必须先 `start()`，且析构前确保实际线程已结束。 |
| 析构 | `~QThread()` | 销毁线程管理对象。 | 普通仍在运行的 QThread 不能直接销毁；先请求停止并 `wait()`。 |
| 工厂 | `QThread::create(Function &&, Args &&...)` | 创建一个执行给定函数的一次性 QThread。 | 返回后仍需 `start()`；适合短任务，不天然提供 Worker 事件循环模型。 |
| 生命周期 | `start(Priority priority = InheritPriority)` | 请求启动新线程并运行 `run()`。 | 线程已运行时不要重复启动；默认 `run()` 会进入事件循环。 |
| 生命周期 | `run()` | 新线程实际执行的虚函数；默认实现调用 `exec()`。 | 重写后若省略 `exec()`，该线程没有 queued slot、QTimer 等事件循环能力。 |
| 事件循环 | `exec()` | 在 QThread 派生类的 `run()` 内启动该线程的局部事件循环。 | 受保护接口；通常不需手动调用，只有自定义 `run()` 时才按需使用。 |
| 生命周期通知 | `started()` | 关联线程开始运行时发出的信号。 | 连接初始化槽时仍要明确对象已迁移和配置完成；不要把它当作线程完全就绪屏障。 |
| 生命周期通知 | `finished()` | 线程的 `run()` 即将结束时发出的信号。 | 常连接到 Worker 的 `deleteLater()`；析构资源前仍用 `wait()` 等待线程真正结束。 |
| 状态 | `isRunning()` | 查询线程是否已开始且尚未结束。 | 只是快照；不要用“先检查再操作”代替可靠的生命周期协议。 |
| 状态 | `isFinished()` | 查询 `run()` 是否已经返回。 | `true` 后仍建议 `wait()` 再销毁依赖原生线程资源的对象。 |
| 状态 | `isCurrentThread()` | 判断调用线程是否就是该 QThread 管理的线程。 | Qt 6.8 起可用；适合断言对象/线程代码的位置。 |
| 状态 | `loopLevel()` | 返回当前线程嵌套事件循环层数。 | 用于诊断重入；不要把数值当作通用业务状态。 |
| 协作取消 | `requestInterruption()` | 向该线程设置中断请求标志。 | 不会终止代码；任务必须周期性检查并主动返回或取消底层操作。 |
| 协作取消 | `isInterruptionRequested()` | 查询当前线程是否收到中断请求。 | 通常在线程自身代码中调用；应及时清理并返回，避免无限阻塞。 |
| 退出循环 | `quit()` | 请求线程事件循环以返回码 `0` 退出。 | 只对正在运行 `exec()` 的线程有效；不会中止正在执行的长槽或自定义死循环。 |
| 退出循环 | `exit(int retcode = 0)` | 请求线程事件循环以指定返回码退出。 | 适合需要传递退出码的低层控制；从其他线程通过 queued 方式通知更清晰。 |
| 强制终止 | `terminate()` | 尝试强制停止线程。 | 高风险，会破坏锁、RAII 和库状态；正常业务不应使用。 |
| 等待 | `wait(QDeadlineTimer deadline = Forever)` | 阻塞调用者直到线程结束或 deadline 到期。 | GUI 线程避免无限等待；返回 `false` 时不要销毁仍在运行线程。 |
| 等待 | `wait(unsigned long time)` | 用毫秒超时等待线程结束的兼容重载。 | 新代码优先 deadline 重载，语义更清晰且可表达无穷等待。 |
| 优先级 | `setPriority(Priority)` | 为运行中的线程设置调度优先级建议。 | 平台可能忽略；只调优，不能修复算法、资源竞争或错误架构。 |
| 优先级 | `priority()` | 读取线程当前请求的优先级。 | 返回值不保证操作系统实际采用了该优先级。 |
| 服务等级 | `setServiceLevel(QualityOfService)` | 设置性能或能耗倾向。 | Qt 6.9 起可用；应在启动前或线程自身中设置，避免把它当作实时保证。 |
| 服务等级 | `serviceLevel()` | 查询线程的 QoS 设置。 | 结果表示请求的服务等级，具体平台映射可能不同。 |
| 栈空间 | `setStackSize(uint stackSize)` | 设置新线程请求的栈大小。 | 必须在 `start()` 前设置；受平台最小值、最大值和对齐要求限制。 |
| 栈空间 | `stackSize()` | 查询请求的栈大小。 | `0` 表示交由平台默认；这不是已实际分配内存的精确测量。 |
| 分发器 | `eventDispatcher()` | 返回该线程的事件分发器。 | 返回对象由 Qt 管理；无事件循环或尚未建立时可能不可用。 |
| 分发器 | `setEventDispatcher(QAbstractEventDispatcher *)` | 在创建前为线程设置事件分发器。 | 仅平台/框架集成使用，且必须在线程启动前设置；Qt 接管对象所有权。 |
| 事件入口 | `event(QEvent *event)` | 处理发给 QThread 管理对象的事件。 | 管理对象通常在创建线程；不要把它与新线程的 Worker 事件混淆。 |
| 休眠 | `sleep(unsigned long)` / `sleep(std::chrono::nanoseconds)` | 让调用线程休眠指定时间。 | 阻塞事件循环；GUI 和事件驱动 Worker 中优先使用 QTimer 或异步等待。 |
| 休眠 | `msleep(unsigned long)` / `usleep(unsigned long)` | 分别以毫秒或微秒让调用线程休眠。 | 精度受操作系统限制；不应用于跨线程同步或精确计时。 |
| 终止开关 | `setTerminationEnabled(bool enabled = true)` | 控制当前线程何时允许被 `terminate()` 终止。 | 受保护的低层接口；它不能让强制终止变得安全。 |
| 枚举 | `Priority` | 包含 `IdlePriority` 到 `TimeCriticalPriority` 与 `InheritPriority` 的调度建议。 | 数值和实际效果由平台决定；`InheritPriority` 用于启动时继承，而不是运行时性能保证。 |
| 枚举 | `QualityOfService` | 包含 `Auto`、`High` 和 `Eco` 的性能/能耗提示。 | Qt 6.9 起可用；根据实际设备功耗、吞吐和响应性测试选择。 |

---

### 一句话总结

`QThread` 管理线程，但不自动把它自己的槽搬到后台。把事件驱动工作放进无 parent 的 Worker 并 `moveToThread()`，用 queued 信号传递请求和结果，用协作式中断加 `quit()` 停止，再用 `wait()` 形成明确收尾，才能把并发从偶尔能跑变成可维护的程序结构。
