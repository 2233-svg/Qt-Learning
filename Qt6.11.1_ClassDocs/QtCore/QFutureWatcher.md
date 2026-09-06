# QFutureWatcher

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QFutureWatcher` 是并发执行或同步类型，负责任务、线程、future、promise 或共享资源的协调。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QFutureWatcher` 是 并发与任务机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

**适用场景：** 先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

## 2. 依赖与对象关系

- 头文件：`#include <QFutureWatcher>`
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

先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QFutureWatcher(QObject *parent = nullptr)`
- `virtual ~QFutureWatcher()`
- `QFuture<T> future() const`
- `bool isCanceled() const`
- `bool isFinished() const`
- `bool isRunning() const`
- `bool isStarted() const`
- `(since 6.0) bool isSuspended() const`
- `(since 6.0) bool isSuspending() const`
- `int progressMaximum() const`
- `int progressMinimum() const`
- `QString progressText() const`
- `int progressValue() const`
- `T result() const`
- `T resultAt(int index) const`
- `void setFuture(const QFuture<T> &future)`
- `void setPendingResultsLimit(int limit)`
- `void waitForFinished()`

### 公有槽函数

- `void cancel()`
- `void resume()`
- `(since 6.0) void setSuspended(bool suspend)`
- `(since 6.0) void suspend()`
- `(since 6.0) void toggleSuspended()`

### 信号

- `void canceled()`
- `void finished()`
- `void progressRangeChanged(int minimum, int maximum)`
- `void progressTextChanged(const QString &progressText)`
- `void progressValueChanged(int progressValue)`
- `void resultReadyAt(int index)`
- `void resultsReadyAt(int beginIndex, int endIndex)`
- `void resumed()`
- `void started()`
- `(since 6.0) void suspended()`
- `(since 6.0) void suspending()`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 34 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[explicit] QFutureWatcher::QFutureWatcher(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFutureWatcher` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QFutureWatcher::~QFutureWatcher()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFutureWatcher` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QFutureWatcher::cancel()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `cancel`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFutureWatcher::canceled()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFutureWatcher` 发出的通知信号 `canceled`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFutureWatcher::finished()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFutureWatcher` 发出的通知信号 `finished`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFuture<T> QFutureWatcher::future() const`

**API 类别：** 成员函数说明

**中文解读：** `QFutureWatcher::future` 用于计算、查询或取得与“future”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFuture<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFuture<T>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFutureWatcher::isCanceled() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isCanceled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFutureWatcher::isFinished() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isFinished`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFutureWatcher::isRunning() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRunning`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFutureWatcher::isStarted() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isStarted`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QFutureWatcher::isSuspended() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSuspended`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QFutureWatcher::isSuspending() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSuspending`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QFutureWatcher::progressMaximum() const`

**API 类别：** 成员函数说明

**中文解读：** `QFutureWatcher::progressMaximum` 用于计算、查询或取得与“progress、最大值”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QFutureWatcher::progressMinimum() const`

**API 类别：** 成员函数说明

**中文解读：** `QFutureWatcher::progressMinimum` 用于计算、查询或取得与“progress、最小值”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFutureWatcher::progressRangeChanged(int minimum, int maximum)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFutureWatcher` 发出的通知信号 `progressRangeChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `minimum`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `maximum`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFutureWatcher::progressText() const`

**API 类别：** 成员函数说明

**中文解读：** `QFutureWatcher::progressText` 用于计算、查询或取得与“progress、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFutureWatcher::progressTextChanged(const QString &progressText)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFutureWatcher` 发出的通知信号 `progressTextChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `progressText`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QFutureWatcher::progressValue() const`

**API 类别：** 成员函数说明

**中文解读：** `QFutureWatcher::progressValue` 用于计算、查询或取得与“progress、值访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFutureWatcher::progressValueChanged(int progressValue)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFutureWatcher` 发出的通知信号 `progressValueChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `progressValue`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T QFutureWatcher::result() const`

**API 类别：** 成员函数说明

**中文解读：** `QFutureWatcher::result` 用于计算、查询或取得与“结果”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T QFutureWatcher::resultAt(int index) const`

**API 类别：** 成员函数说明

**中文解读：** `QFutureWatcher::resultAt` 用于计算、查询或取得与“结果、按位置访问”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFutureWatcher::resultReadyAt(int index)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFutureWatcher` 发出的通知信号 `resultReadyAt`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFutureWatcher::resultsReadyAt(int beginIndex, int endIndex)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFutureWatcher` 发出的通知信号 `resultsReadyAt`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `beginIndex`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `endIndex`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QFutureWatcher::resume()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `resume`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFutureWatcher::resumed()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFutureWatcher` 发出的通知信号 `resumed`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFutureWatcher::setFuture(const QFuture<T> &future)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFuture`。调用它会改变 `QFutureWatcher` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `future`：类型为 `const QFuture<T> &`。没有默认值，调用时必须提供。传入 `const QFuture<T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFutureWatcher::setPendingResultsLimit(int limit)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPendingResultsLimit`。调用它会改变 `QFutureWatcher` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `limit`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot, since 6.0] void QFutureWatcher::setSuspended(bool suspend)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSuspended`。调用它会改变 `QFutureWatcher` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `suspend`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFutureWatcher::started()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFutureWatcher` 发出的通知信号 `started`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常与完成、取消、错误和安全退出信号配合；启动成功不等于任务完成。

### `[slot, since 6.0] void QFutureWatcher::suspend()`

**API 类别：** 成员函数说明

**中文解读：** `QFutureWatcher::suspend` 用于执行与“suspend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal, since 6.0] void QFutureWatcher::suspended()`

**API 类别：** 成员函数说明

**中文解读：** `QFutureWatcher::suspended` 用于执行与“suspended”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal, since 6.0] void QFutureWatcher::suspending()`

**API 类别：** 成员函数说明

**中文解读：** `QFutureWatcher::suspending` 用于执行与“suspending”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot, since 6.0] void QFutureWatcher::toggleSuspended()`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toggleSuspended`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFutureWatcher::waitForFinished()`

**API 类别：** 成员函数说明

**中文解读：** `QFutureWatcher::waitForFinished` 用于执行与“等待、For、Finished”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

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

不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QFutureWatcher` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
