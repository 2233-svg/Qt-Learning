# QThreadPool

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 线程池管理器，负责复用工作线程并调度 QRunnable 任务。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QThreadPool`：线程池管理器，负责复用工作线程并调度 QRunnable 任务。

**内部模型：** 并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

**适用场景：** 先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

## 2. 依赖与对象关系

- 头文件：`#include <QThreadPool>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

### 状态、生命周期和线程

**生命周期：** 任务必须有明确的开始、完成、取消和销毁路径。线程退出前先停止接受新任务，等待 worker 安全结束，再释放线程依赖；对象的线程归属和 QThread 对象本身所在的线程不能混为一谈。

**状态与结果：** 区分任务未开始、运行中、暂停、取消请求、已取消、失败和成功。发出取消请求不代表任务已经停止，资源释放要等任务确认结束；Future 的完成也不一定表示业务结果有效。

**线程与事件循环：** GUI 线程只负责启动任务、接收结果和更新界面；共享数据要么转移所有权，要么用锁/原子/消息传递保护。queued slot 需要目标线程事件循环，阻塞 worker 则不能依赖它接收 queued 控制命令。

## 3. 直接使用

先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `activeThreadCount : int`
- `expiryTimeout : int`
- `maxThreadCount : int`
- `stackSize : uint`
- `(since 6.2) threadPriority : QThread::Priority`

### 公有函数

- `QThreadPool(QObject *parent = nullptr)`
- `virtual ~QThreadPool()`
- `int activeThreadCount() const`
- `void clear()`
- `(since 6.0) bool contains(const QThread *thread) const`
- `int expiryTimeout() const`
- `int maxThreadCount() const`
- `void releaseThread()`
- `void reserveThread()`
- `(since 6.9) QThread::QualityOfService serviceLevel() const`
- `void setExpiryTimeout(int expiryTimeout)`
- `void setMaxThreadCount(int maxThreadCount)`
- `(since 6.9) void setServiceLevel(QThread::QualityOfService serviceLevel)`
- `void setStackSize(uint stackSize)`
- `void setThreadPriority(QThread::Priority priority)`
- `uint stackSize() const`
- `void start(QRunnable *runnable, int priority = 0)`
- `void start(Callable &&callableToRun, int priority = 0)`
- `(since 6.3) void startOnReservedThread(QRunnable *runnable)`
- `(since 6.3) void startOnReservedThread(Callable &&callableToRun)`
- `QThread::Priority threadPriority() const`
- `bool tryStart(QRunnable *runnable)`
- `bool tryStart(Callable &&callableToRun)`
- `bool tryTake(QRunnable *runnable)`
- `(since 6.8) bool waitForDone(QDeadlineTimer deadline = QDeadlineTimer::Forever)`
- `bool waitForDone(int msecs)`

### 静态公有成员

- `QThreadPool * globalInstance()`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 32 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[read-only] activeThreadCount : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QThreadPool` 的状态/能力属性。通常通过 `activeThreadCount()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`activeThreadCount`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `expiryTimeout : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QThreadPool` 的配置属性。初始化或状态切换时通过 `setExpiryTimeout(...)` 设置，之后用 `expiryTimeout()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`expiryTimeout`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `maxThreadCount : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QThreadPool` 的配置属性。初始化或状态切换时通过 `setMaxThreadCount(...)` 设置，之后用 `maxThreadCount()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`maxThreadCount`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `stackSize : uint`

**API 类别：** 属性说明

**中文解读：** 这是 `QThreadPool` 的配置属性。初始化或状态切换时通过 `setStackSize(...)` 设置，之后用 `stackSize()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`uint`。
- 属性名：`stackSize`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] threadPriority : QThread::Priority`

**API 类别：** 属性说明

**中文解读：** 这是 `QThreadPool` 的配置属性。初始化或状态切换时通过 `setPriority(...)` 设置，之后用 `Priority()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QThread::Priority`。
- 属性名：`threadPriority`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QThreadPool::QThreadPool(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QThreadPool` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QThreadPool::~QThreadPool()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QThreadPool` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QThreadPool::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QThreadPool::contains(const QThread *thread) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `thread`：类型为 `const QThread *`。没有默认值，调用时必须提供。传入 `const QThread *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QThreadPool *QThreadPool::globalInstance()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `globalInstance`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QThreadPool *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QThreadPool::releaseThread()`

**API 类别：** 成员函数说明

**中文解读：** `QThreadPool::releaseThread` 用于执行与“释放、Thread”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QThreadPool::reserveThread()`

**API 类别：** 成员函数说明

**中文解读：** `QThreadPool::reserveThread` 用于执行与“reserve、Thread”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] QThread::QualityOfService QThreadPool::serviceLevel() const`

**API 类别：** 成员函数说明

**中文解读：** `QThreadPool::serviceLevel` 用于计算、查询或取得与“service、Level”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QThread::QualityOfService`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QThread::QualityOfService`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] void QThreadPool::setServiceLevel(QThread::QualityOfService serviceLevel)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setServiceLevel`。调用它会改变 `QThreadPool` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `serviceLevel`：类型为 `QThread::QualityOfService`。没有默认值，调用时必须提供。传入 `QThread::QualityOfService` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QThreadPool::start(QRunnable *runnable, int priority = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `start`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `runnable`：类型为 `QRunnable *`。没有默认值，调用时必须提供。传入 `QRunnable *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `priority`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常与完成、取消、错误和安全退出信号配合；启动成功不等于任务完成。

### `template <typename Callable, QRunnable::if_callable<Callable> = true> void QThreadPool::start(Callable &&callableToRun, int priority = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `start`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`template <typename Callable, QRunnable::if_callable<Callable> = true> void`。
- 参数 `callableToRun`：类型为 `Callable &&`。没有默认值，调用时必须提供。传入 `Callable &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `priority`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常与完成、取消、错误和安全退出信号配合；启动成功不等于任务完成。

### `[since 6.3] void QThreadPool::startOnReservedThread(QRunnable *runnable)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startOnReservedThread`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `runnable`：类型为 `QRunnable *`。没有默认值，调用时必须提供。传入 `QRunnable *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常与完成、取消、错误和安全退出信号配合；启动成功不等于任务完成。

### `[since 6.3] template <typename Callable, QRunnable::if_callable<Callable> = true> void QThreadPool::startOnReservedThread(Callable &&callableToRun)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startOnReservedThread`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`template <typename Callable, QRunnable::if_callable<Callable> = true> void`。
- 参数 `callableToRun`：类型为 `Callable &&`。没有默认值，调用时必须提供。传入 `Callable &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常与完成、取消、错误和安全退出信号配合；启动成功不等于任务完成。

### `bool QThreadPool::tryStart(QRunnable *runnable)`

**API 类别：** 成员函数说明

**中文解读：** `QThreadPool::tryStart` 用于计算、查询或取得与“try、启动”相关的操作。调用时要先确认当前状态和 `runnable` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `runnable`：类型为 `QRunnable *`。没有默认值，调用时必须提供。传入 `QRunnable *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Callable, QRunnable::if_callable<Callable> = true> bool QThreadPool::tryStart(Callable &&callableToRun)`

**API 类别：** 成员函数说明

**中文解读：** `QThreadPool::tryStart` 用于计算、查询或取得与“try、启动”相关的操作。调用时要先确认当前状态和 `callableToRun` 的有效范围；返回类型是 `template <typename Callable, QRunnable::if_callable<Callable> = true> bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Callable, QRunnable::if_callable<Callable> = true> bool`。
- 参数 `callableToRun`：类型为 `Callable &&`。没有默认值，调用时必须提供。传入 `Callable &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QThreadPool::tryTake(QRunnable *runnable)`

**API 类别：** 成员函数说明

**中文解读：** `QThreadPool::tryTake` 用于计算、查询或取得与“try、取出”相关的操作。调用时要先确认当前状态和 `runnable` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `runnable`：类型为 `QRunnable *`。没有默认值，调用时必须提供。传入 `QRunnable *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] bool QThreadPool::waitForDone(QDeadlineTimer deadline = QDeadlineTimer::Forever)`

**API 类别：** 成员函数说明

**中文解读：** `QThreadPool::waitForDone` 用于计算、查询或取得与“等待、For、Done”相关的操作。调用时要先确认当前状态和 `deadline` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `deadline`：类型为 `QDeadlineTimer`。默认值为 `QDeadlineTimer::Forever`。传入 `QDeadlineTimer` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QThreadPool::waitForDone(int msecs)`

**API 类别：** 成员函数说明

**中文解读：** `QThreadPool::waitForDone` 用于计算、查询或取得与“等待、For、Done”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int activeThreadCount() const`

**API 类别：** 公有函数

**中文解读：** `QThreadPool::activeThreadCount` 用于计算、查询或取得与“活动状态、Thread、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int expiryTimeout() const`

**API 类别：** 公有函数

**中文解读：** `QThreadPool::expiryTimeout` 用于计算、查询或取得与“expiry、超时”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int maxThreadCount() const`

**API 类别：** 公有函数

**中文解读：** `QThreadPool::maxThreadCount` 用于计算、查询或取得与“max、Thread、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setExpiryTimeout(int expiryTimeout)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setExpiryTimeout`。调用它会改变 `QThreadPool` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `expiryTimeout`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMaxThreadCount(int maxThreadCount)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMaxThreadCount`。调用它会改变 `QThreadPool` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `maxThreadCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setStackSize(uint stackSize)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setStackSize`。调用它会改变 `QThreadPool` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `stackSize`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setThreadPriority(QThread::Priority priority)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setThreadPriority`。调用它会改变 `QThreadPool` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `priority`：类型为 `QThread::Priority`。没有默认值，调用时必须提供。传入 `QThread::Priority` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uint stackSize() const`

**API 类别：** 公有函数

**中文解读：** `QThreadPool::stackSize` 用于计算、查询或取得与“stack、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uint`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QThread::Priority threadPriority() const`

**API 类别：** 公有函数

**中文解读：** `QThreadPool::threadPriority` 用于计算、查询或取得与“thread、Priority”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QThread::Priority`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QThread::Priority`。
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

不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QThreadPool` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
