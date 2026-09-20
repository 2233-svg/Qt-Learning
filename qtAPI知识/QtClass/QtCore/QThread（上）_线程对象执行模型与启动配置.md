# Qt QThread 深入笔记（上）：线程对象、执行模型与启动配置

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QThread>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QThread`  
> 定位：创建并管理一个平台线程，提供启动、事件循环、状态、优先级和完成通知

`QThread` 最重要也最容易误解的一点是：**QThread 对象本身不是那个新线程**。QThread 对象通常创建并生活在主线程，而它的 `run()` 在新线程执行。对 QThread 对象调用普通成员函数时，代码不会因此自动进入新线程。

本类拆为两篇：上篇讲执行模型、启动方式和配置；下篇讲 worker-object、事件循环、中断、等待和安全销毁。

## 1. CMake 与最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

最小派生模式：

```cpp
#include <QCoreApplication>
#include <QThread>

class WorkerThread final : public QThread
{
protected:
    void run() override
    {
        qInfo() << "worker thread:" << QThread::currentThreadId();
        doCpuWork();
    }
};

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    auto *thread = new WorkerThread;
    QObject::connect(thread, &QThread::finished,
                     thread, &QObject::deleteLater);
    QObject::connect(thread, &QThread::finished,
                     &app, &QCoreApplication::quit);

    thread->start();
    return app.exec();
}
```

派生模式适合一个明确的阻塞计算或自包含循环。若线程内要运行多个 QObject、定时器或异步 I/O，通常使用下一篇的 worker-object 模式。

## 2. 两个身份必须分开

```text
主线程
├─ 创建 QThread 对象
├─ QThread 对象的 thread() 通常仍是主线程
├─ 调用 start()/quit()/wait()
└─ 接收 QThread 对象自身的 queued 调用

新平台线程
└─ 执行 QThread::run()
   └─ 默认 run() 调用 exec()，开启该线程事件循环
```

因此下面的槽不会因为写在 QThread 子类中就自动在新线程执行：

```cpp
class WrongThread : public QThread
{
    Q_OBJECT
public slots:
    void doWork(); // queued 调用通常在 QThread 对象所属的创建线程执行
};
```

需要在新线程执行的 QObject 槽应放在独立 Worker 中，再 `moveToThread()`。

## 3. 构造、启动和状态

```cpp
QThread thread(parent);
thread.start();
```

`start(priority)` 创建平台线程并让它进入 `run()`。线程启动过程是异步的，`start()` 返回不代表 `run()` 已执行。

```cpp
connect(&thread, &QThread::started,
        [] { qInfo() << "started"; });
connect(&thread, &QThread::finished,
        [] { qInfo() << "finished"; });
```

状态查询：

```cpp
bool running = thread.isRunning();
bool finished = thread.isFinished();
```

状态在并发环境中只是一瞬间快照。不能先检查 `isRunning()` 再假定后续操作期间线程仍运行。

## 4. `run()` 与默认事件循环

QThread 默认实现：

```cpp
void QThread::run()
{
    exec();
}
```

这意味着未重载 run 的线程启动后会运行事件循环，可处理：

- queued signal/slot；
- `postEvent()`；
- `QTimer`；
- socket notifier；
- `deleteLater()`。

如果重载 run 但不调用 `exec()`：

```cpp
void WorkerThread::run()
{
    calculate();
} // 返回后线程结束
```

该线程没有 Qt 事件循环，移动到其中的 QObject 无法正常接收 queued 事件和 timer。对纯阻塞算法这可以接受，对事件驱动 worker 则不合适。

## 5. `QThread::create()`

不需要自定义类时，可从函数创建线程：

```cpp
QThread *thread = QThread::create([](QString path) {
    processFile(path);
}, filePath);

connect(thread, &QThread::finished,
        thread, &QObject::deleteLater);
thread->start();
```

传入参数会按模板规则保存并在新线程调用。不要捕获生命周期短于线程的引用：

```cpp
// 危险：函数返回后 local 可能已销毁
QThread *thread = QThread::create([&local] { use(local); });
```

Qt 6.3 起，可以删除由 `QThread::create()` 创建且仍在运行的 QThread；Qt 会请求中断、请求事件循环退出并阻塞等待线程结束。这个特殊保证不适用于普通构造或自定义派生的运行中 QThread。

## 6. 当前线程相关静态 API

### 6.1 `currentThread()`

```cpp
QThread *current = QThread::currentThread();
```

返回管理当前执行线程的 QThread 对象。对于不是由 QThread 创建的原生线程，Qt 可能按需创建包装对象。返回指针的生命周期和所有权不应由调用者接管。

### 6.2 `currentThreadId()`

```cpp
Qt::HANDLE id = QThread::currentThreadId();
```

这是平台线程句柄/标识，只保证适合当前进程中的诊断和平台接口。不要持久化、跨进程传输或假设它是连续整数。

### 6.3 `isCurrentThread()` 与 `isMainThread()`

```cpp
if (thread.isCurrentThread())
    qDebug() << "running in the managed thread";

if (QThread::isMainThread())
    updateGui();
```

二者自 Qt 6.8 提供。`isCurrentThread()` 比比较包装对象指针更清楚；`isMainThread()` 适合断言 GUI/主线程约束，但不替代正确调度。

## 7. 理想线程数量

```cpp
const int count = QThread::idealThreadCount();
```

返回当前系统建议并行线程数，可能为 `-1`（无法确定），也可能因 CPU affinity 或热插拔在进程运行中变化。

它不是“所有任务都应创建这么多 QThread”的命令。CPU 密集任务、I/O 任务、数据库连接和内存带宽有不同上限；批量任务通常交给 `QThreadPool`。

## 8. 优先级 `Priority`

```cpp
enum QThread::Priority {
    IdlePriority,
    LowestPriority,
    LowPriority,
    NormalPriority,
    HighPriority,
    HighestPriority,
    TimeCriticalPriority,
    InheritPriority
};
```

启动时指定：

```cpp
thread.start(QThread::LowPriority);
```

运行中修改：

```cpp
thread.setPriority(QThread::HighPriority);
qDebug() << thread.priority();
```

`setPriority()` 对未运行线程无效果；启动参数才适合首次配置。操作系统可能忽略优先级，尤其普通用户没有调度权限时。高优先级不是性能修复，可能导致 UI、音频或系统线程饥饿。

`InheritPriority` 只用于 start 的继承语义，不能传给运行中的 `setPriority()`。

## 9. 服务质量 `QualityOfService`

Qt 6.9 起：

```cpp
enum class QThread::QualityOfService {
    Auto,
    High,
    Eco
};
```

```cpp
thread.setServiceLevel(QThread::QualityOfService::Eco);
auto qos = thread.serviceLevel();
```

- `Auto`：交给调度器。
- `High`：偏向高性能 CPU 核心。
- `Eco`：偏向节能核心。

它描述异构 CPU 的性能/能效倾向，与传统 Priority 不是同一维度。Qt 6.11.1 中 `setServiceLevel()` 只在 Apple 平台和 Windows 实现实际效果；其它平台调用可成功返回但未必改变调度。

调用时机通常是线程启动前，或从线程自身调用。平台支持和权限必须实测。

## 10. 栈大小

```cpp
thread.setStackSize(2 * 1024 * 1024);
uint bytes = thread.stackSize();
```

值 0 表示由操作系统选择默认值。非零值通常设置最大虚拟栈空间，系统可能按合法边界向上/下取整；超过平台限制会导致线程无法启动。

只有深递归、大型栈数组或第三方库明确要求时才修改。更常见的修复是把大对象放到堆上并消除不受控递归。

必须在 `start()` 前设置。

## 11. 自定义事件分发器

```cpp
thread.setEventDispatcher(customDispatcher);
```

只能在线程尚未安装事件 dispatcher 时设置，QThread 会接管对象所有权。默认 dispatcher 在 `start()` 时自动创建。

这是把 Qt 事件循环嵌入特殊平台循环的底层接口，普通应用不应替换。错误 dispatcher 会破坏 timer、socket notifier、queued event 和 `deleteLater()`。

读取：

```cpp
QAbstractEventDispatcher *dispatcher = thread.eventDispatcher();
```

## 12. `loopLevel()`

```cpp
int nesting = QThread::currentThread()->loopLevel();
```

返回当前线程事件循环嵌套层级，只能由线程自身调用。主 `exec()` 通常形成一层，模态对话框或手写局部 QEventLoop 会增加层级。

它适合诊断重入，不应成为业务控制条件；正确代码不应依赖当前恰好处于第几层事件循环。

## 13. 睡眠与让出 CPU

```cpp
QThread::sleep(1);
QThread::msleep(10);
QThread::usleep(100);
QThread::sleep(250ms); // chrono 重载
QThread::yieldCurrentThread();
```

这些函数阻塞当前执行线程。GUI 线程中调用会冻结界面，worker 事件循环线程中调用会阻塞 timer、queued slots 和 I/O。

多数事件驱动等待应使用 QTimer、异步 I/O 或条件变量。sleep 只适合没有事件处理职责的专用循环、测试替身或受控退避。

`yieldCurrentThread()` 只是向调度器提示让出时间片，不保证其它线程立即运行，也不能作为同步机制。

## 14. 何时派生 QThread

适合派生：

- 一个自包含的阻塞算法。
- 需要控制 `run()` 的完整生命周期。
- 不需要在新线程接收多个 QObject queued slots。
- 集成阻塞式第三方 API。

不适合派生：

- 想把若干业务槽放进新线程。
- 需要 QTimer、socket、network 等事件驱动对象。
- 需要反复发送命令给长期 worker。

这些情况使用 worker-object 模式。

## 15. 常见误区

### QThread 子类的槽自动在新线程运行

错误。QThread QObject 通常仍属于创建线程，只有 `run()` 在新线程。

### start 返回后线程一定已开始

错误。监听 `started()` 或建立明确握手。

### 提高 Priority 一定更快

系统可能忽略；过高还会造成其它任务饥饿。

### sleep 能让事件循环等待

sleep 会阻塞事件循环。事件驱动延迟用 timer。

### 任何运行中的 QThread 都可以直接 delete

错误。普通 QThread 运行中析构会导致程序错误；仅 `QThread::create()` 对象自 Qt 6.3 有特殊收尾行为。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 生命周期 | `QThread(QObject *parent = nullptr)` | 创建一个线程管理对象，但此时还没有启动平台线程 | QThread 对象通常属于创建它的线程；对象身份和将要执行的线程必须分开理解 |
| 生命周期 | `~QThread()` | 销毁线程管理对象 | 普通 QThread 仍在运行时析构会导致程序错误；销毁前应建立线程已结束的协议 |
| 启动与执行 | `start(QThread::Priority)` | 异步创建并启动平台线程，随后进入 `run()` | `start()` 返回不代表 `run()` 已经执行；重复启动要遵守当前状态和平台规则 |
| 启动与执行 | `run()` | 新平台线程的入口函数 | 默认实现调用 `exec()`；重载后不调用基类就不会自动拥有 Qt 事件循环 |
| 启动与执行 | `exec()` | 在当前线程运行 Qt 事件循环，直到退出 | 只能在合适的线程执行；没有事件循环时 queued 调用、QTimer 和 `deleteLater()` 不能按预期工作 |
| 生命周期通知 | `started()` | 线程开始运行时发出的信号 | 适合做初始化握手；接收槽在哪个线程执行仍由连接类型和 receiver 亲和性决定 |
| 生命周期通知 | `finished()` | `run()` 返回、线程即将完成时发出的信号 | 常用于触发 worker 的 `deleteLater()` 和清理资源；不能替代等待线程结束的同步 |
| 状态查询 | `isRunning()` | 查询线程当前是否处于运行状态 | 是并发瞬时快照，不能检查一次后就假定状态不会改变 |
| 状态查询 | `isFinished()` | 查询线程是否已经完成 | 不能代替 `wait()`；检查结果和后续访问之间仍可能发生并发变化 |
| 工厂与入口 | `QThread::create(Callable &&, Args &&...)` | 用 callable 和参数创建一个执行该函数的 QThread | 参数会被保存到线程对象；不要捕获短命引用，线程结束和对象销毁仍需明确处理 |
| 当前线程 | `QThread::currentThread()` | 获取当前执行线程对应的 QThread 管理对象 | 返回的对象不由调用者接管；它表示执行上下文，不等于当前代码所在 QObject 的亲和性 |
| 当前线程 | `QThread::currentThreadId()` | 获取当前平台线程的句柄或标识 | 主要用于诊断和平台 API；不要假设它跨进程稳定或是连续整数 |
| 当前线程 | `isCurrentThread()` | 判断当前执行代码是否运行在该 QThread 管理的线程 | Qt 6.8 起提供；比手动比较线程包装对象更直接，但不能替代正确调度 |
| 当前线程 | `QThread::isMainThread()` | 判断当前执行线程是否为 Qt 主线程 | Qt 6.8 起提供；GUI 访问仍应通过设计保证主线程，而不是只靠运行时判断 |
| 并行度 | `QThread::idealThreadCount()` | 返回系统建议的理想并行线程数量 | 可能返回 `-1`，也可能因 CPU affinity 或热插拔动态变化；不是必须创建的线程数 |
| 调度优先级 | `QThread::Priority` | 描述线程调度优先级的枚举 | 操作系统可能忽略，`InheritPriority` 只适合启动时的继承语义 |
| 调度优先级 | `setPriority(Priority)` / `priority()` | 设置或读取运行线程的调度优先级 | 通常只对运行中的线程有意义；不接受 `InheritPriority` 作为运行时优先级 |
| 服务质量 | `QThread::QualityOfService` | 描述在异构 CPU 上偏向高性能核还是节能核 | Qt 6.9 起提供，实际效果依赖平台；它与 Priority 是不同维度 |
| 服务质量 | `setServiceLevel(QualityOfService)` / `serviceLevel()` | 设置或读取线程服务质量级别 | 通常在启动前或线程自身调用；平台不支持时可能没有实际调度变化 |
| 线程资源 | `setStackSize(uint)` / `stackSize()` | 设置或读取新线程的栈空间配置 | 必须在 `start()` 前设置；过大或不合法的值可能导致线程启动失败 |
| 事件循环底层 | `eventDispatcher()` | 获取该线程当前使用的事件分发器 | 主要用于底层诊断和集成特殊事件源；普通业务不应依赖具体实现 |
| 事件循环底层 | `setEventDispatcher(QAbstractEventDispatcher *)` | 在线程安装默认分发器前注入自定义事件分发器 | QThread 会接管分发器所有权；必须在正确时机设置，错误实现会破坏 timer、queued event 和 socket notifier |
| 事件循环诊断 | `loopLevel()` | 返回当前线程嵌套事件循环的层数 | 只能由线程自身调用；适合诊断重入，不应成为业务逻辑分支条件 |
| 线程休眠 | `sleep(...)` / `msleep(...)` / `usleep(...)` | 阻塞当前执行线程指定时间 | 会冻结 GUI 或阻塞 worker 事件循环；事件驱动等待优先用 QTimer、异步 I/O 或同步原语 |
| 调度提示 | `yieldCurrentThread()` | 向调度器提示当前线程可以让出时间片 | 不保证其他线程立即运行，也不是互斥、等待或内存同步机制 |

下篇将完成 worker-object 模式、`quit()`/`exit()`、中断请求、`wait(QDeadlineTimer)`、`terminate()` 风险、对象销毁顺序和线程关闭协议。
