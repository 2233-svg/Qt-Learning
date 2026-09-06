# QtTaskTree::QThreadFunction

> Qt 6.11.1 · Qt TaskTree

## 1. 先建立直觉

**一句话定位：** `QtTaskTree::QThreadFunction` 是并发执行或同步类型，负责任务、线程、future、promise 或共享资源的协调。

**模块背景：** 这是 Qt TaskTree 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QtTaskTree::QThreadFunction` 是并发模块中的类型，用于组织线程执行、同步或资源访问。

**内部模型：** 并发正确性来自所有权、共享数据、同步边界和退出协议的组合，而不是仅仅“开一个线程”。先定义谁读写数据，再决定 queued connection、mutex、future 或线程池。

**适用场景：** 后台任务、阻塞 I/O、并行计算或多个执行上下文共享资源时使用。

**典型调用链：** 划分任务和数据 -> 选择线程/线程池/future -> 明确同步和取消 -> 连接完成/错误 -> 等待安全退出。

**先记住的坑：** 避免 GUI 线程阻塞等待；锁顺序要稳定；线程结束前不能释放它使用的对象；queued slot 需要目标线程事件循环。

## 2. 依赖与对象关系

- 头文件：`#include <qthreadfunctiontask.h>`
- 继承自：QtTaskTree::QThreadFunctionBase
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS TaskTree)
target_link_libraries(mytarget PRIVATE Qt6::TaskTree)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

并发正确性来自所有权、共享数据、同步边界和退出协议的组合，而不是仅仅“开一个线程”。先定义谁读写数据，再决定 queued connection、mutex、future 或线程池。

### 状态、生命周期和线程

**生命周期：** 任务必须有明确的开始、完成、取消和销毁路径。线程退出前先停止接受新任务，等待 worker 安全结束，再释放线程依赖；对象的线程归属和 QThread 对象本身所在的线程不能混为一谈。

**状态与结果：** 区分任务未开始、运行中、暂停、取消请求、已取消、失败和成功。发出取消请求不代表任务已经停止，资源释放要等任务确认结束；Future 的完成也不一定表示业务结果有效。

**线程与事件循环：** GUI 线程只负责启动任务、接收结果和更新界面；共享数据要么转移所有权，要么用锁/原子/消息传递保护。queued slot 需要目标线程事件循环，阻塞 worker 则不能依赖它接收 queued 控制命令。

## 3. 直接使用

后台任务、阻塞 I/O、并行计算或多个执行上下文共享资源时使用。 使用时通常按这个过程组织：划分任务和数据 -> 选择线程/线程池/future -> 明确同步和取消 -> 连接完成/错误 -> 等待安全退出。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QThreadFunction(QObject *parent = nullptr)`
- `virtual ~QThreadFunction() override`
- `QFuture<ResultType> future() const`
- `QFutureWatcher<ResultType> * futureWatcher()`
- `const QFutureWatcher<ResultType> * futureWatcher() const`
- `bool isAutoDelayedSync() const`
- `bool isDone() const`
- `bool isResultAvailable() const`
- `ResultType result() const`
- `ResultType resultAt(int index) const`
- `QList<ResultType> results() const`
- `void setAutoDelayedSync(bool on)`
- `void setThreadFunctionData(Function &&function, Args &&... args)`
- `void setThreadPool(QThreadPool *pool)`
- `ResultType takeResult() const`
- `QThreadPool * threadPool() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[default] QThreadFunction::QThreadFunction(QObject *parent = nullptr)`

**作用与语义：**

构造一个具有给定`parent`的QThreadFunction。

### `[override virtual] QThreadFunction::~QThreadFunction()`

**作用与语义：**

销毁`QThreadFunction`。如果`QThreadFunction`未运行，则不执行其他操作，否则相关未来被取消，根据自动延迟同步执行以下操作：
- `Automatic Delayed Synchronization`：行动
- `On`：关联的 `QFuture` 存储在全局注册表中。在应用退出时使用 `QThreadFunctionBase::syncAll()` 同步之前存储在全局注册表中的所有未来。
- `Off`：直接执行对`QFuture::waitForFinished()`的阻塞调用。
当自动延迟同步开启时，未来的取消可以在仍在运行的独立线程中拦截，以便尽快完成任务而不完成任务。
最后，在应用退出时，应调用`QThreadFunctionBase::syncAll()`以同步所有可能在独立线程中运行的函数。调用`QThreadFunctionBase::syncAll()`是阻塞，以防部分函数仍在最终确定。
注意：当自动延迟同步开启时，函数在`QThreadFunction`的解构器完成后仍会运行一段时间，因此用户有责任确保该函数可能操作的所有数据仍然可用。如果无法保证，请通过`QThreadFunction::setAutoDelayedSync`（false）将自动延迟同步设置为关闭。此时`QThreadFunction`解构器会阻塞等待函数完成后再删除`QThreadFunction`。请参阅`QCustomTask`文档了解`Deleter`模板参数的更多信息。

### `QFuture<ResultType> QThreadFunction::future() const`

**作用与语义：**

返回<ResultType>与该函数相关的`QFuture`，在独立线程中执行。

### `QFutureWatcher<ResultType> *QThreadFunction::futureWatcher()`

**作用与语义：**

返回指向与该函数关联的`QFutureWatcher<ResultType>`的指针，该函数在独立线程中执行。返回的监视者的生命周期绑定到`QThreadFunction`实例。
例如，如果你需要对未来执行有更多控制，比如连接返回观察者的进度信号，可以使用这个函数。

### `const QFutureWatcher<ResultType> *QThreadFunction::futureWatcher() const`

**作用与语义：**

返回与该函数相关的`QFutureWatcher<ResultType>`的`const`指针，在独立线程中执行。

### `bool QThreadFunction::isAutoDelayedSync() const`

**作用与语义：**

返回自动延迟同步是否开启。

### `bool QThreadFunction::isDone() const`

**作用与语义：**

返回函数是否已完成。

### `bool QThreadFunction::isResultAvailable() const`

**作用与语义：**

返回结果是否准备好。

### `ResultType QThreadFunction::result() const`

**作用与语义：**

返回在独立线程中执行的函数报告的结果类型。
注意：请通过调用 `isResultAvailable()` 确保结果已准备好，否则调用 result() 可能会阻塞，如果结果尚未报告，甚至函数执行完成时未报告任何结果也会崩溃。

### `ResultType QThreadFunction::resultAt(int index) const`

**作用与语义：**

返回由在 `index` 处执行的独立线程中函数报告的结果类型。

### `QList<ResultType> QThreadFunction::results() const`

**作用与语义：**

返回由在独立线程中执行的函数报告的 ResultType 列表。

### `void QThreadFunction::setAutoDelayedSync(bool on)`

**作用与语义：**

将自动延迟同步设置为`on`。
默认情况下，自动延迟同步是开启的，这意味着运行中的`QThreadFunction`对象不会阻塞等待，直到在独立线程中运行的函数完成。相反，关联的`QFuture`会被取消，函数会一直运行直到完成。通过`QPromise`参数，函数可以在独立线程中运行，从而提前完成，从而完成工作。如果自动延迟同步开启，需要在应用退出时调用`QThreadFunctionBase::syncAll()`，以同步所有可能运行的独立线程函数。
当自动延迟同步关闭时，同步发生在`QThreadFunction`的销毁时，这可能会阻断调用线程相当长的时间。
自动同步仅在主线程执行`QThreadFunction`时使用。

### `template <typename Function, typename... Args> void QThreadFunction::setThreadFunctionData(Function &&function, Args &&... args)`

**作用与语义：**

在调用start()时，将要执行的`function`设置在一个独立线程中，传递`args`。

### `void QThreadFunction::setThreadPool(QThreadPool *pool)`

**作用与语义：**

设置执行调用时使用的`QThreadPool` `pool`。如果传递的`pool` `nullptr`，则使用该`QThreadPool::globalInstance()`。

### `ResultType QThreadFunction::takeResult() const`

**作用与语义：**

会在独立线程中执行函数报告的结果类型。
注意：确保结果已准备好，方法是调用 `isResultAvailable()`，否则调用 takeResult() 可能会阻塞，如果结果尚未报告，甚至函数执行完成时未报告任何结果，可能会崩溃。

### `QThreadPool *QThreadFunction::threadPool() const`

**作用与语义：**

返回执行调用时使用的线程池。如果返回`nullptr`，则使用该`QThreadPool::globalInstance()`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

任务必须有明确的开始、完成、取消和销毁路径。线程退出前先停止接受新任务，等待 worker 安全结束，再释放线程依赖；对象的线程归属和 QThread 对象本身所在的线程不能混为一谈。

### 状态和错误边界

区分任务未开始、运行中、暂停、取消请求、已取消、失败和成功。发出取消请求不代表任务已经停止，资源释放要等任务确认结束；Future 的完成也不一定表示业务结果有效。

### 线程边界

GUI 线程只负责启动任务、接收结果和更新界面；共享数据要么转移所有权，要么用锁/原子/消息传递保护。queued slot 需要目标线程事件循环，阻塞 worker 则不能依赖它接收 queued 控制命令。

### 最容易出现的错误

避免 GUI 线程阻塞等待；锁顺序要稳定；线程结束前不能释放它使用的对象；queued slot 需要目标线程事件循环。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QtTaskTree::QThreadFunction` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
