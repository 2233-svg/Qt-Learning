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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 40 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QThread::Priority`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QThread` 暴露的类型声明 `Priority`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Priority`。
- 属性名：`QThread`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] enum class QThread::QualityOfService`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QThread` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:QualityOfService`。
- 属性名：`QThread`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QThread::QThread(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QThread` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QThread::~QThread()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QThread` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename Function, typename... Args> QThread *QThread::create(Function &&f, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `create`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Function, typename... Args> QThread *`。
- 参数 `f`：类型为 `Function &&`。没有默认值，调用时必须提供。传入 `Function &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QThread *QThread::currentThread()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `currentThread`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QThread *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept] Qt::HANDLE QThread::currentThreadId()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `currentThreadId`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`Qt::HANDLE`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QThread::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QThread::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractEventDispatcher *QThread::eventDispatcher() const`

**API 类别：** 成员函数说明

**中文解读：** `QThread::eventDispatcher` 用于计算、查询或取得与“event、Dispatcher”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractEventDispatcher *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractEventDispatcher *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] int QThread::exec()`

**API 类别：** 成员函数说明

**中文解读：** `QThread::exec` 用于计算、查询或取得与“执行”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QThread::exit(int returnCode = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `exit`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `returnCode`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[private signal] void QThread::finished()`

**API 类别：** 成员函数说明

**中文解读：** `QThread::finished` 用于执行与“finished”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept] int QThread::idealThreadCount()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `idealThreadCount`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.8] bool QThread::isCurrentThread() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isCurrentThread`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QThread::isFinished() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isFinished`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QThread::isInterruptionRequested() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isInterruptionRequested`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept, since 6.8] bool QThread::isMainThread()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isMainThread`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QThread::isRunning() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRunning`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QThread::loopLevel() const`

**API 类别：** 成员函数说明

**中文解读：** `QThread::loopLevel` 用于计算、查询或取得与“loop、Level”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QThread::msleep(unsigned long msecs)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `msleep`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `msecs`：类型为 `unsigned long`。没有默认值，调用时必须提供。传入 `unsigned long` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QThread::Priority QThread::priority() const`

**API 类别：** 成员函数说明

**中文解读：** `QThread::priority` 用于计算、查询或取得与“priority”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QThread::Priority`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QThread::Priority`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QThread::quit()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `quit`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QThread::requestInterruption()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QThread` 的核心操作 `requestInterruption`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QThread::run()`

**API 类别：** 成员函数说明

**中文解读：** `QThread::run` 用于执行与“运行”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] QThread::QualityOfService QThread::serviceLevel() const`

**API 类别：** 成员函数说明

**中文解读：** `QThread::serviceLevel` 用于计算、查询或取得与“service、Level”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QThread::QualityOfService`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QThread::QualityOfService`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QThread::setEventDispatcher(QAbstractEventDispatcher *eventDispatcher)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setEventDispatcher`。调用它会改变 `QThread` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `eventDispatcher`：类型为 `QAbstractEventDispatcher *`。没有默认值，调用时必须提供。传入 `QAbstractEventDispatcher *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QThread::setPriority(QThread::Priority priority)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPriority`。调用它会改变 `QThread` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `priority`：类型为 `QThread::Priority`。没有默认值，调用时必须提供。传入 `QThread::Priority` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] void QThread::setServiceLevel(QThread::QualityOfService serviceLevel)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setServiceLevel`。调用它会改变 `QThread` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `serviceLevel`：类型为 `QThread::QualityOfService`。没有默认值，调用时必须提供。传入 `QThread::QualityOfService` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QThread::setStackSize(uint stackSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStackSize`。调用它会改变 `QThread` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `stackSize`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static protected] void QThread::setTerminationEnabled(bool enabled = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setTerminationEnabled`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.6] void QThread::sleep(std::chrono::nanoseconds nsecs)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sleep`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `nsecs`：类型为 `std::chrono::nanoseconds`。没有默认值，调用时必须提供。传入 `std::chrono::nanoseconds` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QThread::sleep(unsigned long secs)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sleep`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `secs`：类型为 `unsigned long`。没有默认值，调用时必须提供。传入 `unsigned long` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uint QThread::stackSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QThread::stackSize` 用于计算、查询或取得与“stack、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uint`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QThread::start(QThread::Priority priority = InheritPriority)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `start`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `priority`：类型为 `QThread::Priority`。默认值为 `InheritPriority`。传入 `QThread::Priority` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常与完成、取消、错误和安全退出信号配合；启动成功不等于任务完成。

### `[private signal] void QThread::started()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `started`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常与完成、取消、错误和安全退出信号配合；启动成功不等于任务完成。

### `[slot] void QThread::terminate()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `terminate`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QThread::usleep(unsigned long usecs)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `usleep`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `usecs`：类型为 `unsigned long`。没有默认值，调用时必须提供。传入 `unsigned long` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QThread::wait(QDeadlineTimer deadline = QDeadlineTimer(QDeadlineTimer::Forever))`

**API 类别：** 成员函数说明

**中文解读：** `QThread::wait` 用于计算、查询或取得与“等待”相关的操作。调用时要先确认当前状态和 `deadline` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `deadline`：类型为 `QDeadlineTimer`。默认值为 `QDeadlineTimer(QDeadlineTimer::Forever)`。传入 `QDeadlineTimer` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QThread::wait(unsigned long time)`

**API 类别：** 成员函数说明

**中文解读：** `QThread::wait` 用于计算、查询或取得与“等待”相关的操作。调用时要先确认当前状态和 `time` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `time`：类型为 `unsigned long`。没有默认值，调用时必须提供。传入 `unsigned long` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QThread::yieldCurrentThread()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `yieldCurrentThread`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
