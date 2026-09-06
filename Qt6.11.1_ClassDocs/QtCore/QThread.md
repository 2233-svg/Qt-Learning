# QThread

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QThread` 管理一个线程执行上下文。Qt 推荐把工作对象移动到线程，而不是把业务逻辑都写进 QThread 子类的 run。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QThread` 管理一个线程执行上下文。Qt 推荐把工作对象移动到线程，而不是把业务逻辑都写进 QThread 子类的 run。

**内部模型：** QThread 对象本身通常属于创建它的线程，run/exec 才是新线程里的执行内容；worker QObject 移动到线程后，它的 queued slots 才会在目标线程事件循环中执行。

**适用场景：** 后台计算、阻塞 I/O、设备访问和需要独立事件循环的 worker 使用。纯并行计算也可以评估 Qt Concurrent/QThreadPool。

**典型调用链：** 创建 worker 和 thread -> worker->moveToThread(thread) -> 连接 started/finished/quit/deleteLater -> thread->start -> finished 后 wait。

**先记住的坑：** 不要从 GUI 线程直接操作 worker 成员；不要在线程还运行时销毁 QThread；阻塞任务没有事件循环时 queued slot 不会执行；连接类型要结合线程归属判断。

## 2. 依赖与对象关系

- 头文件：`#include <QThread>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QThread 对象本身通常属于创建它的线程，run/exec 才是新线程里的执行内容；worker QObject 移动到线程后，它的 queued slots 才会在目标线程事件循环中执行。

### 状态、生命周期和线程

**生命周期：** 任务必须有明确的开始、完成、取消和销毁路径。线程退出前先停止接受新任务，等待 worker 安全结束，再释放线程依赖；对象的线程归属和 QThread 对象本身所在的线程不能混为一谈。

**状态与结果：** 区分任务未开始、运行中、暂停、取消请求、已取消、失败和成功。发出取消请求不代表任务已经停止，资源释放要等任务确认结束；Future 的完成也不一定表示业务结果有效。

**线程与事件循环：** GUI 线程只负责启动任务、接收结果和更新界面；共享数据要么转移所有权，要么用锁/原子/消息传递保护。queued slot 需要目标线程事件循环，阻塞 worker 则不能依赖它接收 queued 控制命令。

## 3. 直接使用

后台计算、阻塞 I/O、设备访问和需要独立事件循环的 worker 使用。纯并行计算也可以评估 Qt Concurrent/QThreadPool。 使用时通常按这个过程组织：创建 worker 和 thread -> worker->moveToThread(thread) -> 连接 started/finished/quit/deleteLater -> thread->start -> finished 后 wait。

```cpp
QThread *thread = new QThread(this);
Worker *worker = new Worker;
worker->moveToThread(thread);
connect(thread, &QThread::started, worker, &Worker::run);
connect(worker, &Worker::finished, thread, &QThread::quit);
connect(worker, &Worker::finished, worker, &QObject::deleteLater);
connect(thread, &QThread::finished, thread, &QObject::deleteLater);
thread->start();
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Priority { IdlePriority, LowestPriority, LowPriority, NormalPriority, HighPriority, …, InheritPriority }`
- `(since 6.9) enum class QualityOfService { Auto, High, Eco }`

### 公有函数

- `QThread(QObject *parent = nullptr)`
- `virtual ~QThread()`
- `QAbstractEventDispatcher * eventDispatcher() const`
- `(since 6.8) bool isCurrentThread() const`
- `bool isFinished() const`
- `bool isInterruptionRequested() const`
- `bool isRunning() const`
- `int loopLevel() const`
- `QThread::Priority priority() const`
- `void requestInterruption()`
- `(since 6.9) QThread::QualityOfService serviceLevel() const`
- `void setEventDispatcher(QAbstractEventDispatcher *eventDispatcher)`
- `void setPriority(QThread::Priority priority)`
- `(since 6.9) void setServiceLevel(QThread::QualityOfService serviceLevel)`
- `void setStackSize(uint stackSize)`
- `uint stackSize() const`
- `bool wait(QDeadlineTimer deadline = QDeadlineTimer(QDeadlineTimer::Forever))`
- `bool wait(unsigned long time)`

### 重实现的公有函数

- `virtual bool event(QEvent *event) override`

### 公有槽函数

- `void exit(int returnCode = 0)`
- `void quit()`
- `void start(QThread::Priority priority = InheritPriority)`
- `void terminate()`

### 信号

- `void finished()`
- `void started()`

### 静态公有成员

- `QThread * create(Function &&f, Args &&... args)`
- `QThread * currentThread()`
- `Qt::HANDLE currentThreadId()`
- `int idealThreadCount()`
- `(since 6.8) bool isMainThread()`
- `void msleep(unsigned long msecs)`
- `(since 6.6) void sleep(std::chrono::nanoseconds nsecs)`
- `void sleep(unsigned long secs)`
- `void usleep(unsigned long usecs)`
- `void yieldCurrentThread()`

### 保护函数

- `int exec()`
- `virtual void run()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QThread::Priority`

**作用与语义：**

该枚举类型表示操作系统应如何调度新创建的线程。
- `QThread::IdlePriority`：`0`;仅在没有其他线程运行时调度。
- `QThread::LowestPriority`：`1`;排班频率低于低优先级。
- `QThread::LowPriority`：`2`;排程频率低于NormalPriority。
- `QThread::NormalPriority`：`3`;操作系统的默认优先级。
- `QThread::HighPriority`：`4`;排程频率高于NormalPriority。
- `QThread::HighestPriority`：`5`;排班频率高于高优先级。
- `QThread::TimeCriticalPriority`：`6`;尽可能频繁地安排。
- `QThread::InheritPriority`：`7`;使用与创建线程相同的优先级。这是默认设置。

### `[since 6.9] enum class QThread::QualityOfService`

**作用与语义：**

该枚举描述线程的服务质量水平，并为调度器提供线程执行工作类型的信息。在拥有不同CPU配置或能够降频CPU核心的平台上，调度器可以选择或配置具有适当性能和能耗特性的CPU核心。
- `QThread::QualityOfService::Auto`：`0`;默认值，由调度器决定线程运行在哪个CPU核心上。
- `QThread::QualityOfService::High`：`1`;调度器应将该线程运行到高性能CPU核心。
- `QThread::QualityOfService::Eco`：`2`;调度器应将该线程运行到节能的CPU核心。
这个枚举是在Qt 6.9引入的。

### `[explicit] QThread::QThread(QObject *parent = nullptr)`

**作用与语义：**

构建一个新的QThread来管理一个新的线程。`parent`对QThread拥有所有权。线程在调用`start()`之前不会开始执行。

### `[virtual noexcept] QThread::~QThread()`

**作用与语义：**

摧毁了`QThread`。
注意，删除`QThread`对象不会停止其管理线程的执行。删除正在运行的`QThread`（即返回`isFinished()`返回`false`）会导致程序崩溃。在删除`QThread`之前，等待`finished()`信号。
自 Qt 6.3 起，即使对应线程仍在运行，调用 `QThread::create()` 创建的 `QThread` 实例也被允许删除。在这种情况下，Qt 会通过 `requestInterruption()` 向该线程发布中断请求;通过 `quit()` 请求线程的事件循环（如有）退出;并会阻塞直到线程结束。

### `[static] template <typename Function, typename... Args> QThread *QThread::create(Function &&f, Args &&... args)`

**作用与语义：**

创建一个新的`QThread`对象，执行函数`f`，参数为`args`。
新线程不是被启动的——必须通过显式调用`start()`来启动。这允许你连接到它的信号，将QObjects移动到线程，选择新线程的优先级，等等。函数`f`会在新线程中被调用。
返回新创建的`QThread`实例。
注意：调用者获得返回`QThread`实例的所有权。
警告：不要在返回的`QThread`实例上多次调用`start()`;这样做会导致行为未定义。

### `[static] QThread *QThread::currentThread()`

**作用与语义：**

返回一个指向管理当前执行线程的 `QThread`的指针。

### `[static noexcept] Qt::HANDLE QThread::currentThreadId()`

**作用与语义：**

返回当前执行线程的线程句柄。
警告：该函数返回的句柄用于内部用途，不应在任何应用代码中使用。
注意：在Windows上，该函数返回由Win32函数GetCurrentThreadId（返回的DWORD，Windows线程ID），而不是由Win32函数GetCurrentThread()返回的伪HANDLE（Windows线程HANDLE）。

### `[override virtual] bool QThread::event(QEvent *event)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。
该虚拟函数接收对象事件，如果事件`e`被识别并处理，应返回真。
event() 函数可以重新实现，以自定义对象的行为。
确保你调用所有未处理的事件的父事件类实现。

### `QAbstractEventDispatcher *QThread::eventDispatcher() const`

**作用与语义：**

返回指向该线程事件调度器对象的指针。如果线程不存在事件调度器，该函数返回`nullptr`。

### `[protected] int QThread::exec()`

**作用与语义：**

进入事件循环，等待 `exit()` 被调用，并返回传递给 `exit()` 的值。如果 `exit()` 通过 `quit()` 调用，则返回值为 0。
此函数旨在在 `run()` 内部调用。必须调用此函数以启动事件处理。
注意：此函数只能在线程自身内调用，即当它是当前线程时。

### `[slot] void QThread::exit(int returnCode = 0)`

**作用与语义：**

告诉线程的事件循环用返回码退出。
调用该函数后，线程离开事件循环，返回调用`QEventLoop::exec()`。`QEventLoop::exec()`函数返回`returnCode`。
按照惯例，`returnCode`为0表示成功，任何非零值表示错误。
注意，与同名的 C 库函数不同，该函数会返回调用者——停止的是事件处理。
在本线程中，在再次调用`QThread::exec()`之前，不会再启动 QEventLoops。如果 `QThread::exec()` 中的 eventloop 没有运行，那么下一次调用 `QThread::exec()` 也会立即返回。
注意：该功能是线程安全的。

### `[private signal] void QThread::finished()`

**作用与语义：**

该信号是在关联线程执行完成前发出的。
当该信号发出时，事件循环已经停止运行。线程中不会再处理事件，除非是延迟删除事件。该信号可以连接到`QObject::deleteLater()`，以释放该线程中的对象。
注意：如果关联线程是用 `terminate()` 终止的，则该信号从哪个线程发出未定义。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[static noexcept] int QThread::idealThreadCount()`

**作用与语义：**

返回该进程可并行运行的理想线程数。通过查询该进程可用的逻辑处理器数量（如果该操作系统支持）或系统中逻辑处理器总数来实现。如果这两个值都无法确定，该函数返回1。
注意：在支持将线程亲和性设置为所有逻辑处理器子集的操作系统上，该函数返回的值可能会在不同线程之间以及随时间变化。
注意：在支持 CPU 热插拔和热拔除的操作系统上，该函数返回的值也可能随时间变化（注意 CPU 可以通过软件开关，无需物理硬件更改）。

### `[noexcept, since 6.8] bool QThread::isCurrentThread() const`

**作用与语义：**

如果该线程`QThread::currentThread`，则返回为真。

### `bool QThread::isFinished() const`

**作用与语义：**

如果线程已完成，返回`true`;否则返回`false`。
如果线程从`run()`函数返回且`finished()`信号已发出，则视线程结束。
注意，线程在`finished()`信号发出后仍可运行任意时间，执行清理操作，如对`thread_local`变量执行解构函数。要同步线程的所有效果，调用`wait()`并验证其返回为真。
注意：该功能是线程安全的。

### `bool QThread::isInterruptionRequested() const`

**作用与语义：**

如果该线程上运行的任务应停止，则返回 true。`requestInterruption()` 可以请求中断。
该函数可用于使长时间运行的任务干净利落地可中断。从不检查或操作该函数返回的值是安全的，但在长运行函数中建议定期这样做。注意不要频繁调用，以保持开销较低。
注意：这只能在线程内部调用，即当前线程时调用。

**官方示例：**

```cpp
 void long_task() {
      forever {
         if ( QThread::currentThread()->isInterruptionRequested() ) {
             return;
         }
     }
 }
```

### `[static noexcept, since 6.8] bool QThread::isMainThread()`

**作用与语义：**

返回当前执行的线程是否为主线程。
主线程是创建`QCoreApplication`线程的线程。这通常是调用`main()`函数的线程，但不一定如此。它是处理图形用户界面事件并可以创建图形对象（`QWindow`、`QWidget`）的线程。

### `bool QThread::isRunning() const`

**作用与语义：**

如果线程正在运行，返回`true`;否则返回`false`。
`QThread`如果线程已用`start()`启动但尚未完成，则该线程被视为正在运行。
注意，线程在`finished()`信号发出后仍可运行任意时间，执行清理操作，如执行对`thread_local`变量的解构子。要与线程的所有效果同步，调用`wait()`并验证其返回为真。
注意：该功能是线程安全的。

### `int QThread::loopLevel() const`

**作用与语义：**

返回线程当前的事件循环级别。
注意：这只能在线程内部调用，即当前线程时调用。

### `[static] void QThread::msleep(unsigned long msecs)`

**作用与语义：**

这是一个重载函数，等价于调用：
注意：该函数不保证准确性。在高负载条件下，应用程序可能睡眠时间超过`msecs`。部分操作系统可能将`msecs`四舍五入至10毫秒或15毫秒。

**官方示例：**

```cpp
 QThread::sleep(std::chrono::milliseconds{msecs});
```

### `QThread::Priority QThread::priority() const`

**作用与语义：**

返回运行中的线程的优先级。如果线程未运行，该函数返回`InheritPriority`。

### `[slot] void QThread::quit()`

**作用与语义：**

告诉线程的事件循环以返回码0（成功）退出。相当于调用`QThread::exit`（0）。
如果线程没有事件循环，这个函数就不做任何事。
注意：该功能是线程安全的。

### `void QThread::requestInterruption()`

**作用与语义：**

请求线程中断。该请求是咨询性的，是否以及如何处理由线程上的代码决定。该函数不会停止线程上运行的任何事件循环，也不会以任何方式终止该请求。
该函数对主线程没有影响，如果线程当前未运行，则无效。
注意：该功能是线程安全的。

### `[virtual protected] void QThread::run()`

**作用与语义：**

线程的起点。调用`start()`后，新创建的线程调用此函数。默认实现只是调用`exec()`。
您可以重新实现此函数以便进行高级线程管理。从此方法返回将终止线程的执行。

### `[since 6.9] QThread::QualityOfService QThread::serviceLevel() const`

**作用与语义：**

返回该线程当前的服务质量水平。

### `void QThread::setEventDispatcher(QAbstractEventDispatcher *eventDispatcher)`

**作用与语义：**

将线程的事件调度器设置为`eventDispatcher`。这只有在线程尚未安装事件调度器的情况下才可行。
当主线程实例化时`QCoreApplication`事件调度器会自动生成，辅助线程则在`start()`中。
这种方法拥有该物体的所有权。

### `void QThread::setPriority(QThread::Priority priority)`

**作用与语义：**

该函数为运行中的线程设置了`priority`。如果线程未运行，该函数不做任何操作，立即返回。使用`start()`启动具有特定优先级的线程。
`priority`参数可以是`QThread::Priority`枚举中的任意值，唯独`InheritPriority`。
`priority`参数的影响取决于操作系统的调度策略。特别是，在不支持线程优先级的系统（如Linux，详见 http://linux.die.net/man/2/sched_setscheduler）上，`priority`会被忽略。

### `[since 6.9] void QThread::setServiceLevel(QThread::QualityOfService serviceLevel)`

**作用与语义：**

将线程对象的服务质量设置为`serviceLevel`。这只能从线程本身调用，或者线程启动前调用！
目前仅在苹果平台和Windows上实现此功能。函数调用在其他平台上会成功完成，但目前不会有任何影响。

### `void QThread::setStackSize(uint stackSize)`

**作用与语义：**

将线程的栈大小设置为`stackSize`。如果`stackSize`为零，操作系统或运行时会选择默认值。否则，线程的栈大小将是提供的值（可以向上取整或向下取整）。
在大多数操作系统中，分配给堆栈的内存最初会小于`stackSize`，随着线程使用栈的使用会逐渐增长。该参数决定了栈允许增长的最大大小（即决定栈允许占用的虚拟内存空间大小）。
该函数只能在线程启动前调用。
警告：大多数操作系统对线程栈大小设定最小和最大限制。如果栈大小超出这些限制，线程将无法启动。

### `[static protected] void QThread::setTerminationEnabled(bool enabled = true)`

**作用与语义：**

根据`enabled`参数启用或禁用当前线程的终止。线程必须由`QThread`启动。
当`enabled`为假时，终止将被禁用。未来的`QThread::terminate()`调用将立即返回，且无效。相反，终止会被推迟，直到终止功能被启用。
当`enabled`为真时，终止被启用。未来调用`QThread::terminate()`会正常终止线程。如果终止被推迟（`QThread::terminate()`即调用时禁用终止），该函数将立即终止调用线程。注意此函数在此情况下不会返回。

### `[static, since 6.6] void QThread::sleep(std::chrono::nanoseconds nsecs)`

**作用与语义：**

强制当前线程休眠 `nsecs`。
如果需要等待某一条件变化，请避免使用该函数。相反，应将一个槽连接到指示变化的信号，或使用事件处理程序（见 `QObject::event()`）。
注意：此功能不保证准确性。在高负载条件下，应用可能比`nsecs`更长时间。

### `[static] void QThread::sleep(unsigned long secs)`

**作用与语义：**

强制当前线程休眠`secs`秒。
这是一个重载函数，等价于调用：

**官方示例：**

```cpp
 QThread::sleep(std::chrono::seconds{secs});
```

### `uint QThread::stackSize() const`

**作用与语义：**

返回线程的最大栈大小（如果设置为 `setStackSize()`）;否则返回零。

### `[slot] void QThread::start(QThread::Priority priority = InheritPriority)`

**作用与语义：**

通过调用`run()`开始线程执行。操作系统会根据`priority`参数调度线程。如果线程已经在运行，这个函数不会做任何事。
`priority`参数的影响取决于操作系统的调度策略。特别是在不支持线程优先级的系统（如Linux，详见sched_setscheduler文档）上，`priority`会被忽略。

### `[private signal] void QThread::started()`

**作用与语义：**

该信号由关联线程在开始执行时发出，因此任何连接该线程的槽位都可以通过队列调用被调用。虽然事件可能在调用`run()`之前就已发布，但任何跨线程传递信号仍可能处于待处理状态。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[slot] void QThread::terminate()`

**作用与语义：**

终止线程的执行。线程可能会立即终止，也可能不会，这取决于操作系统的调度策略。在 terminate() 之后使用 `QThread::wait()`，以确保线程终止。
当线程被终止时，所有等待该线程完成的线程将被唤醒。
警告：此函数危险，不建议使用。线程可能在其代码路径中的任何点被终止。线程可能在修改数据时被终止。线程没有机会在终止前清理自己，解锁持有的互斥锁等。简而言之，只有在绝对必要时才使用此函数。
可以调用 `QThread::setTerminationEnabled()` 显式启用或禁用终止。在终止被禁用时调用此函数将导致终止被延迟，直到再次启用终止。更多信息请参阅 `QThread::setTerminationEnabled()` 的文档。
注意：此函数是线程安全的。

### `[static] void QThread::usleep(unsigned long usecs)`

**作用与语义：**

这是一个重载函数，等价于调用：
注意：该函数不保证准确性。在高负载条件下，应用程序可能睡眠时间超过`usecs`。部分操作系统可能将`usecs`四舍五入至10毫秒或15毫秒;在Windows上，四舍五入为1毫秒的倍数。

**官方示例：**

```cpp
 QThread::sleep(std::chrono::microseconds{secs});
```

### `bool QThread::wait(QDeadlineTimer deadline = QDeadlineTimer(QDeadlineTimer::Forever))`

**作用与语义：**

在满足以下任一条件之前，阻塞线程：
- 与该`QThread`对象关联的线程已完成执行（即从`run()`返回时）。如果线程已完成，该函数返回为true。如果线程尚未启动，该函数也返回true。
- `deadline`已达。如果到达截止日期，该函数将返回假值。
将截止日期定时器设置为`QDeadlineTimer::Forever`（默认值）永远不会超时：此时函数仅在线程从`run()`返回或线程尚未开始时返回。
这提供了与POSIX的 `pthread_join()` 功能类似的功能。
注意：在某些操作系统上，该函数可能在操作系统线程仍在运行时返回为真，且可能执行如 C 11 `thread_local` 解构函数等清理代码。只有在操作系统线程完全退出后才返回该函数的操作系统包括 Linux、Windows 和苹果操作系统。

### `bool QThread::wait(unsigned long time)`

**作用与语义：**

`time` 是毫秒级等待时间。如果`time` ULONG_MAX，那么等待永远不会超时。

### `[static] void QThread::yieldCurrentThread()`

**作用与语义：**

将当前线程的执行权交给另一个可运行线程（如果有的话）。注意操作系统决定切换到哪个线程。

## 6. 深入实践与常见坑

### 生命周期和资源边界

任务必须有明确的开始、完成、取消和销毁路径。线程退出前先停止接受新任务，等待 worker 安全结束，再释放线程依赖；对象的线程归属和 QThread 对象本身所在的线程不能混为一谈。

### 状态和错误边界

区分任务未开始、运行中、暂停、取消请求、已取消、失败和成功。发出取消请求不代表任务已经停止，资源释放要等任务确认结束；Future 的完成也不一定表示业务结果有效。

### 线程边界

GUI 线程只负责启动任务、接收结果和更新界面；共享数据要么转移所有权，要么用锁/原子/消息传递保护。queued slot 需要目标线程事件循环，阻塞 worker 则不能依赖它接收 queued 控制命令。

### 最容易出现的错误

不要从 GUI 线程直接操作 worker 成员；不要在线程还运行时销毁 QThread；阻塞任务没有事件循环时 queued slot 不会执行；连接类型要结合线程归属判断。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QThread` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
