# Qt Core 进阶：线程与异步（上）——QThread 与线程归属

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Core  
> 核心类型：`QThread`、`QObject`、`QMetaObject`  
> 本篇目标：理解线程、事件循环、对象线程归属以及跨线程信号槽，并能正确管理工作线程的生命周期。

## 1. 为什么 GUI 程序需要异步

Qt GUI 通常运行在主线程。鼠标事件、键盘事件、窗口重绘、定时器和大多数界面更新，都依赖主线程中的事件循环。

如果某个槽函数长时间不返回：

```cpp
void MainWindow::onStartClicked()
{
    doHeavyCalculation(); // 持续 10 秒
}
```

在这 10 秒内，主线程无法继续取出和分发事件，程序就会表现为：

- 窗口无法拖动；
- 按钮没有响应；
- 重绘停滞，窗口可能变白；
- 定时器和排队连接不能及时处理；
- 操作系统判断应用“未响应”。

真正的问题并不是“计算慢”，而是“承担界面事件循环的线程被阻塞”。

解决思路是：

```text
主线程：界面、短小的事件处理、发起任务、显示结果
工作线程：耗时计算、阻塞式 I/O、可并行任务
```

## 2. 先分清四个概念

### 2.1 并发

多个任务在一段时间内交替推进。即使只有一个 CPU 核心，也可以由操作系统快速切换任务形成并发。

### 2.2 并行

多个任务在同一时刻由不同 CPU 核心真正执行。并行是并发的一种实现状态。

### 2.3 异步

发起操作后不原地等待结果，而是在稍后通过信号、回调或 `QFuture` 接收结果。异步描述的是控制流程，不等于一定创建线程。

例如 `QNetworkAccessManager` 是异步 API，但通常依赖当前线程的事件循环，本身不要求调用者手动开线程。

### 2.4 线程安全与可重入

- **可重入**：多个线程可同时调用不同对象实例，只要每个线程只访问自己的实例。
- **线程安全**：多个线程可以同时调用同一共享对象或函数，内部已经正确同步。

“Qt 类是可重入的”不代表“一个对象可以被多个线程随意读写”。共享可变状态仍然需要同步。

## 3. Qt 线程体系怎么选

| 需求 | 优先选择 | 原因 |
|---|---|---|
| 长期存在、需要定时器或套接字的工作对象 | `QObject + QThread` | 工作线程可运行事件循环 |
| 自己完全控制的一段阻塞算法 | 继承 `QThread` 并重写 `run()` | 逻辑集中，不依赖槽和事件循环 |
| 大量短任务 | `QThreadPool` / `QRunnable` | 复用线程，避免频繁创建 |
| 调用函数并异步取结果 | `QtConcurrent::run()` | 直接返回 `QFuture` |
| 对容器并行 map/filter/reduce | Qt Concurrent | 已封装任务拆分和结果汇总 |
| 手动发布进度、多个结果或取消 | `QPromise` + `QFuture` | 适合自定义异步生产者 |

本篇先解决前两种；线程池和 Future 放在下篇。

## 4. 构建与头文件

`QThread` 和基础同步类型属于 Qt Core。

### 4.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 4.2 常用头文件

```cpp
#include <QThread>
#include <QObject>
#include <QCoreApplication>
```

Widgets 项目链接 `Qt6::Widgets` 时会传递 Qt Core 依赖，但在公共库中最好按实际使用明确声明组件。

## 5. QThread 到底是什么

`QThread` 对象是一个**线程控制器**，它管理一个操作系统线程。必须区分：

```text
创建 QThread 对象的线程           QThread 管理的新线程
        │                                  │
        │  thread.start()                  │
        ├─────────────────────────────────>│ run()
        │                                  │ 默认调用 exec()
        │                                  │ 运行事件循环
```

最容易犯错的一点是：

> `QThread` 对象本身仍然属于创建它的线程，并不会因为 `start()` 而“搬进”新线程。

因此，给 `QThread` 子类添加普通槽，并通过排队连接调用该槽时，槽通常在 `QThread` 对象所属的旧线程执行，而不是在 `run()` 所在的新线程执行。

## 6. QThread 的基本状态变化

典型生命周期：

```text
构造
  ↓
start()
  ↓ started()
run()
  ↓ 默认进入 exec() 事件循环
quit() / exit() / run() 返回
  ↓ finished()
wait() 确认底层线程完全结束
  ↓
销毁 QThread 对象
```

常用 API：

| API | 作用 |
|---|---|
| `start()` | 启动所管理的线程，随后执行 `run()` |
| `run()` | 新线程入口；默认实现调用 `exec()` |
| `exec()` | 启动当前线程的 Qt 事件循环 |
| `quit()` | 请求事件循环以返回码 0 退出 |
| `exit(code)` | 请求事件循环以指定返回码退出 |
| `wait()` | 阻塞调用线程，等待工作线程结束 |
| `isRunning()` | 是否已经启动且尚未结束 |
| `isFinished()` | 是否已经完成 |
| `requestInterruption()` | 设置协作式中断请求 |
| `isInterruptionRequested()` | 工作代码检查中断请求 |

`quit()` 只对正在运行事件循环的线程有效。如果 `run()` 只是一个计算循环且从未调用 `exec()`，`quit()` 不会让计算自动停止。

## 7. 推荐模式：Worker Object

需要在线程中使用槽、定时器、套接字或其他事件驱动对象时，优先使用工作对象模式：

1. 工作类继承 `QObject`；
2. 创建 `QThread`；
3. 调用 `worker->moveToThread(thread)`；
4. 用信号触发工作槽；
5. 用信号把结果发回主线程；
6. 在线程结束时正确清理对象。

### 7.1 一个最小可用 Worker

```cpp
#include <QCoreApplication>
#include <QDebug>
#include <QObject>
#include <QThread>

class Worker : public QObject
{
    Q_OBJECT
public slots:
    void calculate()
    {
        qint64 sum = 0;
        for (int i = 1; i <= 1'000'000; ++i)
            sum += i;
        emit resultReady(sum);
    }

signals:
    void resultReady(qint64 value);
};

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    auto *thread = new QThread(&app);
    auto *worker = new Worker;
    worker->moveToThread(thread);

    QObject::connect(thread, &QThread::started,
                     worker, &Worker::calculate);
    QObject::connect(worker, &Worker::resultReady,
                     [](qint64 value) { qDebug() << value; });
    QObject::connect(worker, &Worker::resultReady,
                     thread, &QThread::quit);
    QObject::connect(thread, &QThread::finished,
                     worker, &QObject::deleteLater);
    QObject::connect(thread, &QThread::finished,
                     &app, &QCoreApplication::quit);

    thread->start();
    const int code = app.exec();

    thread->wait();
    return code;
}

#include "main.moc"
```

这个例子表达的是生命周期和通信模式。实际项目还应在所有正常退出路径中安排 `thread->deleteLater()`，或者让拥有者在确认线程结束后销毁它。

### 7.2 信号为什么能跨线程

`Qt::AutoConnection` 是默认连接类型。信号发出时，Qt 比较**当前执行线程**和接收对象的线程归属：

- 相同：直接调用槽，效果类似普通函数调用；
- 不同：把调用封装成事件，投递到接收对象所属线程的事件队列。

跨线程时，发送者不会直接进入接收对象的槽。接收线程必须运行事件循环，排队调用才会被处理。

## 8. QObject 的线程归属

每个 `QObject` 都有线程归属，可通过 `thread()` 查询：

```cpp
qDebug() << object->thread();
qDebug() << QThread::currentThread();
```

对象的排队信号、投递事件和定时器由它所属线程的事件循环处理。

### 8.1 moveToThread 的核心规则

```cpp
worker->moveToThread(targetThread);
```

应记住：

- 有父对象的 `QObject` 不能移动；
- 移动对象时，它的所有子对象一起移动；
- 成员指针指向的对象不一定是子对象，除非正确设置了 parent；
- 通常只能从对象当前所属线程把它“推”到目标线程；
- 目标线程必须存在，并在需要排队事件时运行事件循环；
- GUI 对象不能移动到工作线程。

错误示例：

```cpp
auto *worker = new Worker(this); // this 在主线程
worker->moveToThread(thread);    // 失败：worker 有父对象
```

正确思路：创建时不设父对象，移动后通过 `deleteLater()` 在正确时机清理。

### 8.2 构造函数在哪里执行

`moveToThread()` 只改变后续的线程归属，不会让已经执行过的构造函数重新在线程中运行：

```cpp
auto *worker = new Worker;       // 构造函数在当前线程执行
worker->moveToThread(thread);    // 此后排队槽在目标线程执行
```

如果工作对象内部需要创建 `QTimer` 或 `QTcpSocket`，更稳妥的方式是在工作槽或初始化槽中创建，让它们从出生起就在工作线程：

```cpp
void Worker::initialize()
{
    timer_ = new QTimer(this); // 此槽在工作线程执行
    connect(timer_, &QTimer::timeout,
            this, &Worker::poll);
    timer_->start(1000);
}
```

## 9. 连接类型讲透

`QObject::connect()` 的最后一个参数可指定连接类型。

### 9.1 Qt::DirectConnection

槽在发出信号的当前线程立即执行。

```cpp
connect(sender, &Sender::valueReady,
        receiver, &Receiver::accept,
        Qt::DirectConnection);
```

跨线程强行使用 Direct Connection 意味着接收对象的方法会在错误线程执行，除非该方法明确设计成线程安全，否则非常危险。

### 9.2 Qt::QueuedConnection

调用被投递到接收对象所属线程，发出信号后发送者立即继续：

```cpp
connect(sender, &Sender::valueReady,
        receiver, &Receiver::accept,
        Qt::QueuedConnection);
```

要求接收线程能处理事件。

### 9.3 Qt::BlockingQueuedConnection

与排队连接相似，但发送线程会等待槽执行完成。

```cpp
connect(sender, &Sender::request,
        receiver, &Receiver::handle,
        Qt::BlockingQueuedConnection);
```

风险：

- 同一线程使用会死锁；
- 两个线程互相阻塞等待会死锁；
- 主线程等待耗时槽会冻结界面。

除非确实需要同步 RPC 式语义并证明不会形成等待环，否则不要使用。

### 9.4 Qt::AutoConnection

绝大多数场景保留默认值即可。它是在**发射信号时**决定直接还是排队，不是在 `connect()` 时固定。

### 9.5 Qt::UniqueConnection 与 SingleShotConnection

- `Qt::UniqueConnection`：阻止同一成员函数连接重复建立；对 lambda 的唯一性判断不适用。
- `Qt::SingleShotConnection`：连接触发一次后自动断开。

可以和基本连接类型按位组合。

## 10. 跨线程参数如何传递

排队连接不会立即调用槽，因此参数必须能够被 Qt 元对象系统复制并保存到事件中。

Qt 内建类型通常已经注册。自定义类型应：

```cpp
struct Result
{
    int code;
    QString message;
};

Q_DECLARE_METATYPE(Result)
```

必要时在建立连接前注册：

```cpp
qRegisterMetaType<Result>("Result");
```

现代 Qt 对很多完整、可复制类型能够自动处理，但显式声明仍能表达跨线程传输意图，并避免旧式字符串连接或动态调用中的类型问题。

不要跨线程发送指向短生命周期栈对象的裸指针：

```cpp
Result result;
emit ready(&result); // 排队槽执行时 result 可能已销毁
```

优先传值，或使用具有明确共享所有权的智能指针。

## 11. 不要从工作线程直接操作界面

`QWidget` 及其子类只能在 GUI 主线程创建和使用。错误示例：

```cpp
void Worker::runTask()
{
    ui->progressBar->setValue(50); // 工作线程直接碰 UI
}
```

正确方式是发信号：

```cpp
// Worker
emit progressChanged(50);

// MainWindow 中建立连接
connect(worker, &Worker::progressChanged,
        ui->progressBar, &QProgressBar::setValue);
```

由于接收者 `QProgressBar` 属于主线程，默认 Auto Connection 会转为排队连接。

## 12. 协作式取消

Qt 不会安全地强制中断任意 C++ 代码。推荐工作线程定期检查取消请求：

```cpp
void Worker::calculate()
{
    for (qsizetype i = 0; i < items_.size(); ++i) {
        if (QThread::currentThread()->isInterruptionRequested()) {
            emit canceled();
            return;
        }

        process(items_.at(i));
    }
    emit finished();
}
```

控制端请求取消：

```cpp
thread->requestInterruption();
```

必须理解：

- 请求只是设置一个标志；
- 不会终止线程；
- 不会自动退出事件循环；
- 不会唤醒正在无限期等待的系统调用；
- 检查频率决定取消响应速度。

对于事件循环型 Worker，常见停止流程是同时通知 Worker 停止资源，并让线程退出：

```cpp
thread->requestInterruption();
QMetaObject::invokeMethod(worker, "stop", Qt::QueuedConnection);
thread->quit();
```

具体顺序取决于 `stop()` 是否需要工作线程的事件循环。不要先让事件循环退出，再期待排队的清理槽一定执行。

## 13. quit、requestInterruption、terminate 的区别

| 方法 | 实际效果 | 推荐程度 |
|---|---|---|
| `quit()` | 请求 Qt 事件循环退出 | 推荐用于事件循环线程 |
| `requestInterruption()` | 设置协作式中断标志 | 推荐用于循环算法 |
| 自定义 `stop()` | 释放资源、停止定时器等 | 推荐用于 Worker |
| `terminate()` | 在不可控位置强制终止 | 极不推荐 |

`terminate()` 可能在持有互斥锁、修改容器或分配内存的中间位置停止线程，造成死锁、资源泄漏和数据损坏。它最多只能作为进程即将放弃整个状态时的最后手段，不能作为正常取消机制。

## 14. 正确结束与销毁

### 14.1 QThread 析构不等于停止线程

对普通 `QThread` 对象，如果它仍在运行就直接析构，通常会导致程序异常终止。正确流程是：

```cpp
thread->requestInterruption();
thread->quit();
thread->wait();
delete thread;
```

界面线程中调用 `wait()` 可能阻塞 UI，因此正常运行期间优先让 `finished()` 驱动异步清理；只在关闭流程中短暂等待，并确保工作代码能快速响应退出。

Qt 6.3 起，`QThread::create()` 创建的线程对象有特殊析构行为：运行中删除时 Qt 会请求中断、要求事件循环退出并等待结束。这个特例不应被误套到普通 `QThread` 上。

### 14.2 为什么连接 finished 到 deleteLater

经典连接：

```cpp
connect(thread, &QThread::finished,
        worker, &QObject::deleteLater);
```

线程的常规事件循环虽然已经停止，但 Qt 会处理与线程结束相关的延迟删除，因此这是官方推荐的 Worker 清理方式。

线程控制对象也可以异步清理：

```cpp
connect(thread, &QThread::finished,
        thread, &QObject::deleteLater);
```

但调用方随后不能再解引用该指针。实践中可用 `QPointer<QThread>` 观察它是否仍存在。

### 14.3 窗口关闭时的处理

拥有线程的类应明确实现停止协议：

```cpp
Controller::~Controller()
{
    workerThread_.requestInterruption();
    workerThread_.quit();
    workerThread_.wait();
}
```

若任务中有长时间不可中断的阻塞调用，应先让底层 API 支持超时或取消，否则析构中的 `wait()` 仍可能永久卡住。

## 15. 继承 QThread：什么时候合理

继承 `QThread` 并不是绝对错误。它适合一个清晰、独立、不需要事件循环的线程过程：

```cpp
class HashThread : public QThread
{
    Q_OBJECT
public:
    explicit HashThread(QByteArray data, QObject *parent = nullptr)
        : QThread(parent), data_(std::move(data)) {}

signals:
    void hashReady(const QByteArray &hash);

protected:
    void run() override
    {
        const QByteArray hash =
            QCryptographicHash::hash(data_, QCryptographicHash::Sha256);
        emit hashReady(hash);
    }

private:
    QByteArray data_;
};
```

调用：

```cpp
auto *thread = new HashThread(data, this);
connect(thread, &HashThread::hashReady,
        this, &Window::showHash);
connect(thread, &QThread::finished,
        thread, &QObject::deleteLater);
thread->start();
```

这个模式中：

- `run()` 确实在新线程执行；
- `HashThread` 对象仍属于创建它的线程；
- 不要把期望在新线程运行的工作槽放在 `HashThread` 对象上；
- 重写 `run()` 后如果不调用 `exec()`，线程中没有 Qt 事件循环。

## 16. QThread::create：轻量启动一个函数

Qt 可以从函数或 lambda 创建线程：

```cpp
QThread *thread = QThread::create([data] {
    processData(data);
});

connect(thread, &QThread::finished,
        thread, &QObject::deleteLater);
thread->start();
```

适合一次性的独立过程。需要返回值、进度或任务组合时，`QtConcurrent::run()` 与 `QFuture` 往往更自然。

捕获变量必须考虑生命周期：

```cpp
QString text = loadText();
QThread *thread = QThread::create([&text] { // 危险：引用可能先失效
    process(text);
});
```

优先按值捕获只读输入，或使用明确的共享所有权。

## 17. 线程中的事件循环

默认 `QThread::run()` 调用 `exec()`，因此支持：

- 排队信号槽；
- `QTimer`；
- `QTcpSocket` 等异步设备；
- `deleteLater()`；
- `QCoreApplication::postEvent()` 投递的事件。

如果重写为：

```cpp
void MyThread::run()
{
    compute();
}
```

则 `compute()` 返回时线程结束，期间没有事件循环。发送给该线程对象的排队调用也不会因此在 `run()` 中执行，因为线程对象并不属于它管理的线程。

### 17.1 不要用死循环模拟事件循环

```cpp
while (running) {
    checkSomething();
    QThread::msleep(10);
}
```

这种轮询会增加延迟和 CPU 消耗，也让取消、错误和资源管理更复杂。若数据源能以信号、系统通知或异步 I/O 表达，优先使用事件循环。

## 18. QMetaObject::invokeMethod 跨线程调用

当调用点没有合适的业务信号时，可排队调用对象方法：

```cpp
QMetaObject::invokeMethod(
    worker,
    [worker, path] { worker->openFile(path); },
    Qt::QueuedConnection);
```

也可调用可被元对象系统识别的命名方法：

```cpp
QMetaObject::invokeMethod(worker, "stop",
                          Qt::QueuedConnection);
```

使用 lambda 时仍要保证捕获对象在调用执行前有效。若捕获 `worker` 裸指针，关闭阶段尤其要警惕对象已被删除。

## 19. 线程优先级与服务质量

### 19.1 Priority

`QThread::Priority` 提供从 `IdlePriority` 到 `TimeCriticalPriority` 等提示。优先级是否生效以及具体效果由操作系统调度器决定。

不要用提高优先级修复算法慢、锁竞争或主线程阻塞。过高优先级还可能让 GUI 和系统服务得不到运行时间。

### 19.2 QualityOfService

Qt 6.9 起提供：

```cpp
thread->setServiceLevel(QThread::QualityOfService::Eco);
```

枚举值：

| 值 | 意图 |
|---|---|
| `Auto` | 由调度器决定 |
| `High` | 倾向高性能核心 |
| `Eco` | 倾向高能效核心 |

这是调度提示，不保证所有平台都按相同方式实现。

## 20. Qt 6.11 中值得知道的查询 API

```cpp
if (QThread::isMainThread()) {
    // 当前是否主线程，Qt 6.8 起
}

QThread *current = QThread::currentThread();
Qt::HANDLE id = QThread::currentThreadId();
int recommended = QThread::idealThreadCount();
```

`currentThreadId()` 适合日志诊断，不应被当成长期对象身份或业务键值。

## 21. 常见错误与根因

### 21.1 在 QThread 子类槽中写工作逻辑

**现象**：以为槽在新线程，实际仍在主线程。

**根因**：`QThread` 对象属于创建它的线程。

**修复**：使用 Worker Object，或者把一次性逻辑放进 `run()`。

### 21.2 start 后立刻 wait

```cpp
thread->start();
thread->wait(); // 主线程同步等待，界面仍然冻结
```

启动线程本身不等于异步体验；主线程立即等待会把异步重新变成同步。通过信号接收完成通知。

### 21.3 在线程运行中销毁 QThread

**现象**：出现 `QThread: Destroyed while thread is still running`，甚至进程终止。

**修复**：建立清晰的停止、完成、等待和销毁顺序。

### 21.4 工作线程直接修改 QWidget

**现象**：偶发崩溃、刷新错乱、调试正常而发布版异常。

**修复**：工作线程只发数据，由主线程槽更新界面。

### 21.5 moveToThread 没有效果

常见原因：

- 对象有 parent；
- 从错误线程调用移动；
- 目标线程已经结束；
- 实际调用的是 `QThread` 子类自身的槽；
- 接收线程没有事件循环。

### 21.6 用 sleep 等待条件

```cpp
while (!ready)
    QThread::msleep(10);
```

这是轮询，不提供正确的内存同步，还增加响应延迟。共享条件应使用互斥锁配合 `QWaitCondition`，或改用信号槽；详见下篇。

### 21.7 认为隐式共享自动解决线程安全

`QString`、`QByteArray`、Qt 容器的隐式共享让按值传递很便宜，但不允许多个线程无同步地修改同一实例。最简单的设计是：跨线程传值，各线程修改自己的副本。

## 22. 设计线程任务的检查清单

开始编码前回答：

1. 任务是 CPU 密集、阻塞 I/O，还是本来就有异步 API？
2. 是否真的需要独占线程，还是线程池更合适？
3. 工作对象是否依赖事件循环？
4. 输入数据由谁拥有，任务期间是否可能失效？
5. 结果通过什么方式回到主线程？
6. 取消是如何请求、检查和确认的？
7. 错误如何传递，是否区分取消与失败？
8. 应用关闭时谁负责停止并等待线程？
9. 是否存在工作线程直接访问 GUI 的路径？
10. 是否存在两个线程互相等待的可能？

## 23. API 速查表

| 类 / API | 用途 | 关键注意点 |
|---|---|---|
| `QThread::start()` | 启动线程 | 异步返回 |
| `QThread::run()` | 线程入口 | 默认调用 `exec()` |
| `QThread::quit()` | 退出事件循环 | 对无事件循环的计算无效 |
| `QThread::wait()` | 等待线程结束 | 主线程调用可能冻结 UI |
| `requestInterruption()` | 请求协作取消 | 不会强制停止 |
| `isInterruptionRequested()` | 检查取消 | 工作代码需主动检查 |
| `QObject::moveToThread()` | 改变对象线程归属 | 有 parent 的对象不能移动 |
| `QObject::thread()` | 查询对象归属 | 不等于当前执行线程 |
| `QThread::currentThread()` | 查询当前执行线程 | 适合断言和诊断 |
| `QThread::isMainThread()` | 判断 GUI 主线程 | Qt 6.8 起 |
| `QThread::create()` | 从函数创建线程 | 注意捕获生命周期 |
| `QMetaObject::invokeMethod()` | 排队调用方法 | 注意连接类型和对象寿命 |
| `QObject::deleteLater()` | 延迟到所属线程删除 | 依赖事件派发时机 |

## 24. 自测题

### 题 1：QThread 对象在哪里生活

在主线程创建 `QThread thread;` 并调用 `thread.start()` 后，`thread` 对象属于哪个线程？

<details>
<summary>答案</summary>

仍属于主线程。新线程执行的是 `run()`。这正是不要把工作槽直接放在 `QThread` 对象上的原因。

</details>

### 题 2：quit 为什么没有停止计算

某个 `QThread` 子类的 `run()` 中执行长循环，控制端调用 `quit()` 后循环仍继续，为什么？

<details>
<summary>答案</summary>

`quit()` 请求的是线程事件循环退出，而该 `run()` 没有进入事件循环。应使用 `requestInterruption()` 并在循环中检查，或设计自己的线程安全停止标志。

</details>

### 题 3：为什么 Worker 不能带主线程 parent

为什么 `new Worker(mainWindow)` 后不能再移动到工作线程？

<details>
<summary>答案</summary>

Qt 要求父子 `QObject` 位于同一线程。带父对象的 Worker 不能单独迁移，应无 parent 创建，移动后用明确的结束连接清理。

</details>

### 题 4：AutoConnection 何时决定类型

是建立连接时还是发射信号时决定直接调用或排队调用？

<details>
<summary>答案</summary>

发射信号时，根据当前执行线程与接收对象线程归属决定。

</details>

### 题 5：为什么不能立即 wait

主线程执行 `start()` 后马上 `wait()` 有什么问题？

<details>
<summary>答案</summary>

主线程被阻塞，仍无法处理界面事件，用户体验与直接在主线程计算相似。应通过完成信号异步接收结果，仅在受控的关闭阶段必要时等待。

</details>

## 25. 本篇总结

线程编程首先是归属与生命周期问题，其次才是“把代码放到另一个核上”。

请牢牢记住五条：

1. `QThread` 是线程控制对象，它自身不生活在所管理的新线程。
2. 依赖信号槽、定时器和异步 I/O 的长期任务优先使用 Worker Object。
3. 跨线程只传数据，不直接操作 GUI，并让接收线程的事件循环完成排队调用。
4. 取消必须协作完成，`requestInterruption()` 只是请求，`terminate()` 不是正常方案。
5. 线程退出、Worker 删除、`QThread` 销毁必须形成明确且可验证的顺序。

下篇将继续讲：共享数据为什么会产生竞态，如何使用 `QMutex`、`QReadWriteLock`、`QWaitCondition` 和 `QSemaphore`，以及如何用 `QThreadPool`、Qt Concurrent、`QFuture` 和 `QPromise` 构建更高层的异步任务。
