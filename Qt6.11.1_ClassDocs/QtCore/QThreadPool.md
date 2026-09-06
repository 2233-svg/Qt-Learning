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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only] activeThreadCount : int`

**作用与语义：**

此属性保存线程池中活动线程的数量。
注意：此函数返回的值可能大于 `maxThreadCount()`。有关更多详细信息，请参见 `reserveThread()`。

**如何使用：** 调用 `activeThreadCount()` 读取当前值；它不会修改应用状态。

### `expiryTimeout : int`

**作用与语义：**

该属性将线程过期超时值以毫秒计。
未使用的线程若超过超时毫秒，则视为已过期并退出。此类线程将根据需要重启。默认`expiryTimeout`为30000毫秒（30秒）。如果`expiryTimeout`为负，新创建的线程不会过期，例如，线程池被销毁前不会退出。
请注意，设置`expiryTimeout`对已运行的线程没有影响。只有新创建的线程才会使用新`expiryTimeout`。我们建议在创建线程池后立即设置`expiryTimeout`，但调用`start()`之前。

**如何使用：** 调用 `expiryTimeout()` 读取当前值；它不会修改应用状态。

### `maxThreadCount : int`

**作用与语义：**

该属性包含线程池使用的最大线程数。该属性默认值为`QThread::idealThreadCount()`，`QThreadPool`对象生成时。
注意：线程池始终至少会使用一个线程，即使`maxThreadCount`限制为零或负数。
默认`maxThreadCount`是`QThread::idealThreadCount()`。

**如何使用：** 调用 `maxThreadCount()` 读取当前值；它不会修改应用状态。

### `stackSize : uint`

**作用与语义：**

该属性包含线程池工作线程的栈大小。
该属性的值仅在线程池创建新线程时使用。更改该属性对已创建或运行中的线程没有影响。
默认值为0，这意味着`QThread`使用操作系统默认的栈大小。

**如何使用：** 调用 `stackSize()` 读取当前值；它不会修改应用状态。

### `[since 6.2] threadPriority : QThread::Priority`

**作用与语义：**

该属性为新工作线程保留线程优先级。
该属性的值仅在线程池启动新线程时使用。更改该属性对已运行的线程没有影响。
默认值是`QThread::InheritPriority`，这使得`QThread`使用与`QThreadPool`对象所在的优先级相同的优先级。

**如何使用：** 调用 `threadPriority()` 读取当前值；它不会修改应用状态。

### `QThreadPool::QThreadPool(QObject *parent = nullptr)`

**作用与语义：**

用给定的`parent`构建一个线程池。

### `[virtual noexcept] QThreadPool::~QThreadPool()`

**作用与语义：**

销毁`QThreadPool`。该功能会阻塞，直到所有可运行任务完成。

### `void QThreadPool::clear()`

**作用与语义：**

从队列中移除尚未启动的可运行程序。`runnable->autoDelete()`返回`true`的可运行程序被删除。

### `[since 6.0] bool QThreadPool::contains(const QThread *thread) const`

**作用与语义：**

如果 `thread` 是此线程池管理的线程，则返回 `true`。

### `[static] QThreadPool *QThreadPool::globalInstance()`

**作用与语义：**

返回全局`QThreadPool`实例。

### `void QThreadPool::releaseThread()`

**作用与语义：**

释放了之前由调用`reserveThread()`保留的线程。
注意：在未预留线程的情况下调用该函数会暂时增加`maxThreadCount()`。当线程进入休眠等待更多工作时，这非常有用，允许其他线程继续运行。等待结束后务必调用`reserveThread()`，以便线程池能够正确维护`activeThreadCount()`。

### `void QThreadPool::reserveThread()`

**作用与语义：**

保留一个讨论串，不考虑`activeThreadCount()`和`maxThreadCount()`。
完成线程后，打电话给`releaseThread()`允许重复使用。
注意：即使预留`maxThreadCount()`个或更多线程，线程池仍至少允许一个线程。
注意：该函数会增加报告的活跃线程数。这意味着通过使用该函数，`activeThreadCount()`返回的值可能大于`maxThreadCount()`。

### `[since 6.9] QThread::QualityOfService QThreadPool::serviceLevel() const`

**作用与语义：**

返回线程当前的服务质量水平。

### `[since 6.9] void QThreadPool::setServiceLevel(QThread::QualityOfService serviceLevel)`

**作用与语义：**

将调用该设置器后创建的线程对象的服务质量等级设置为`serviceLevel`。
并非所有平台都支持。详情请咨询`QThread::setServiceLevel()`。

### `void QThreadPool::start(QRunnable *runnable, int priority = 0)`

**作用与语义：**

预留一个线程并用它运行`runnable`，除非该线程使当前线程数超过`maxThreadCount()`。此时，`runnable`会被添加到运行队列中。`priority`参数可用于控制运行队列的执行顺序。
注意，如果`runnable->autoDelete()`返回`true`，线程池将获得`runnable`的所有权，线程池在`runnable->run()`返回后线程池会自动删除该`runnable`。如果`runnable->autoDelete()`返回`false`，`runnable`的所有权仍归调用者所有。注意，调用这些函数后更改`runnable`的自动删除会导致行为未定义。

### `template <typename Callable, QRunnable::if_callable<Callable> = true> void QThreadPool::start(Callable &&callableToRun, int priority = 0)`

**作用与语义：**

预留一个线程并用它运行`callableToRun`，除非该线程使当前线程数超过`maxThreadCount()`。此时，`callableToRun`会被添加到运行队列中。`priority`参数可用于控制运行队列的执行顺序。
注意：在 6.6 之前的 Qt 版本中，该函数使用 std：：function<void()>，因此无法处理仅移动可调用的调用。
只有当`Callable`是一个函数或函数对象且参数为零时，才参与重载决议。

### `[since 6.3] void QThreadPool::startOnReservedThread(QRunnable *runnable)`

**作用与语义：**

释放之前保留在`reserveThread()`的线程，并用它运行`runnable`。
注意，如果线程池返回`runnable->autoDelete()`返回`true`，线程池将获得该`runnable`的所有权，线程池在`runnable->run()`返回后会自动删除`runnable`。如果`runnable->autoDelete()`返回`false`，`runnable`的所有权仍归调用者所有。注意，调用这些函数后更改`runnable`自动删除会导致行为未定义。
注意：在没有预留线程时调用该程序会导致行为未定义。

### `[since 6.3] template <typename Callable, QRunnable::if_callable<Callable> = true> void QThreadPool::startOnReservedThread(Callable &&callableToRun)`

**作用与语义：**

释放之前保留给`reserveThread()`的线程，并用它运行`callableToRun`。
注意：在 6.6 之前的 Qt 版本中，该函数使用 std：：function<void()>，因此无法处理仅移动可调用的调用。
只有当`Callable`是一个函数或函数对象且参数为零时，才参与重载决议。

### `bool QThreadPool::tryStart(QRunnable *runnable)`

**作用与语义：**

尝试预留一个线程来运行`runnable`。
如果调用时没有线程可用，该函数不做任何操作，返回`false`。否则，`runnable`会立即使用一个可用线程运行，该函数返回`true`。
注意，成功时线程池会接管`runnable->autoDelete()`返回`true`，线程池将获得该`runnable`的所有权，线程池在`runnable->run()`返回后会自动删除`runnable`。如果`runnable->autoDelete()`返回`false`，`runnable`的所有权仍归调用者所有。注意，调用该函数后更改`runnable`的自动删除会导致行为未定义。

### `template <typename Callable, QRunnable::if_callable<Callable> = true> bool QThreadPool::tryStart(Callable &&callableToRun)`

**作用与语义：**

尝试预留一个线程来运行`callableToRun`。
如果调用时没有线程可用，该函数不做任何操作，返回`false`。否则，`callableToRun`会立即使用一个可用线程运行，该函数返回`true`。
注意：在 6.6 之前的 Qt 版本中，该函数使用 std：：function<void()>，因此无法处理仅移动可调用的调用。
只有当`Callable`是一个函数或函数对象且可用零参数调用时，才参与重载决议。

### `bool QThreadPool::tryTake(QRunnable *runnable)`

**作用与语义：**

如果指定`runnable`尚未启动，尝试将其从队列中移除。如果可运行程序尚未启动，返回`true`，`runnable`的所有权转移给调用者（即使已`runnable->autoDelete() == true`）。否则返回`false`。
注意：如果`runnable->autoDelete() == true`，该函数可能会移除错误的可跑函数。这被称为ABA问题：原始`runnable`可能已经执行但已被删除。内存被重新用于另一个可运行程序，而该可运行程序则被移除，而非预期的。因此，我们建议仅对未自动删除的可运行函数调用该函数。

### `[since 6.8] bool QThreadPool::waitForDone(QDeadlineTimer deadline = QDeadlineTimer::Forever)`

**作用与语义：**

等待`deadline`到期，所有线程退出，并从线程池中移除所有线程。如果所有线程都被移除，返回`true`;否则返回`false`。

### `bool QThreadPool::waitForDone(int msecs)`

**作用与语义：**

等待最多`msecs`毫秒，所有线程退出，并从线程池中移除所有线程。如果所有线程都被移除，返回`true`;否则返回`false`。如果`msecs`为-1，该函数等待最后一个线程退出。

### `int activeThreadCount() const`

**作用与语义：**

此属性保存线程池中活动线程的数量。
注意：此函数返回的值可能大于 `maxThreadCount()`。有关更多详细信息，请参见 `reserveThread()`。

**如何使用：** 调用 `activeThreadCount()` 读取当前值；它不会修改应用状态。

### `int expiryTimeout() const`

**作用与语义：**

该属性将线程过期超时值以毫秒计。
未使用的线程若超过超时毫秒，则视为已过期并退出。此类线程将根据需要重启。默认`expiryTimeout`为30000毫秒（30秒）。如果`expiryTimeout`为负，新创建的线程不会过期，例如，线程池被销毁前不会退出。
请注意，设置`expiryTimeout`对已运行的线程没有影响。只有新创建的线程才会使用新`expiryTimeout`。我们建议在创建线程池后立即设置`expiryTimeout`，但调用`start()`之前。

**如何使用：** 调用 `expiryTimeout()` 读取当前值；它不会修改应用状态。

### `int maxThreadCount() const`

**作用与语义：**

该属性包含线程池使用的最大线程数。该属性默认值为`QThread::idealThreadCount()`，`QThreadPool`对象生成时。
注意：线程池始终至少会使用一个线程，即使`maxThreadCount`限制为零或负数。
默认`maxThreadCount`是`QThread::idealThreadCount()`。

**如何使用：** 调用 `maxThreadCount()` 读取当前值；它不会修改应用状态。

### `void setExpiryTimeout(int expiryTimeout)`

**作用与语义：**

该属性将线程过期超时值以毫秒计。
未使用的线程若超过超时毫秒，则视为已过期并退出。此类线程将根据需要重启。默认`expiryTimeout`为30000毫秒（30秒）。如果`expiryTimeout`为负，新创建的线程不会过期，例如，线程池被销毁前不会退出。
请注意，设置`expiryTimeout`对已运行的线程没有影响。只有新创建的线程才会使用新`expiryTimeout`。我们建议在创建线程池后立即设置`expiryTimeout`，但调用`start()`之前。

**如何使用：** 调用 `setExpiryTimeout(...)` 修改 `expiryTimeout`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaxThreadCount(int maxThreadCount)`

**作用与语义：**

该属性包含线程池使用的最大线程数。该属性默认值为`QThread::idealThreadCount()`，`QThreadPool`对象生成时。
注意：线程池始终至少会使用一个线程，即使`maxThreadCount`限制为零或负数。
默认`maxThreadCount`是`QThread::idealThreadCount()`。

**如何使用：** 调用 `setMaxThreadCount(...)` 修改 `maxThreadCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStackSize(uint stackSize)`

**作用与语义：**

该属性包含线程池工作线程的栈大小。
该属性的值仅在线程池创建新线程时使用。更改该属性对已创建或运行中的线程没有影响。
默认值为0，这意味着`QThread`使用操作系统默认的栈大小。

**如何使用：** 调用 `setStackSize(...)` 修改 `stackSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setThreadPriority(QThread::Priority priority)`

**作用与语义：**

该属性为新工作线程保留线程优先级。
该属性的值仅在线程池启动新线程时使用。更改该属性对已运行的线程没有影响。
默认值是`QThread::InheritPriority`，这使得`QThread`使用与`QThreadPool`对象所在的优先级相同的优先级。

**如何使用：** 调用 `setThreadPriority(...)` 修改 `threadPriority`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `uint stackSize() const`

**作用与语义：**

该属性包含线程池工作线程的栈大小。
该属性的值仅在线程池创建新线程时使用。更改该属性对已创建或运行中的线程没有影响。
默认值为0，这意味着`QThread`使用操作系统默认的栈大小。

**如何使用：** 调用 `stackSize()` 读取当前值；它不会修改应用状态。

### `QThread::Priority threadPriority() const`

**作用与语义：**

该属性为新工作线程保留线程优先级。
该属性的值仅在线程池启动新线程时使用。更改该属性对已运行的线程没有影响。
默认值是`QThread::InheritPriority`，这使得`QThread`使用与`QThreadPool`对象所在的优先级相同的优先级。

**如何使用：** 调用 `threadPriority()` 读取当前值；它不会修改应用状态。

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
