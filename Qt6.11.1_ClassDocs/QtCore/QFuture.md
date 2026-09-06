# QFuture

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 异步计算结果句柄，负责查询完成状态、读取结果、取消或等待任务。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QFuture`：异步计算结果句柄，负责查询完成状态、读取结果、取消或等待任务。

**内部模型：** 并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

**适用场景：** 先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

## 2. 依赖与对象关系

- 头文件：`#include <QFuture>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

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

### 公有类型

- `class const_iterator`
- `ConstIterator`

### 公有函数

- `QFuture()`
- `QFuture(const QFuture<T> &other)`
- `~QFuture()`
- `QFuture<T>::const_iterator begin() const`
- `void cancel()`
- `(since 6.10) void cancelChain()`
- `QFuture<T>::const_iterator constBegin() const`
- `QFuture<T>::const_iterator constEnd() const`
- `QFuture<T>::const_iterator end() const`
- `bool isCanceled() const`
- `bool isFinished() const`
- `bool isResultReadyAt(int index) const`
- `bool isRunning() const`
- `bool isStarted() const`
- `(since 6.0) bool isSuspended() const`
- `(since 6.0) bool isSuspending() const`
- `(since 6.0) bool isValid() const`
- `(since 6.0) QFuture<T> onCanceled(Function &&handler)`
- `(since 6.1) QFuture<T> onCanceled(QObject *context, Function &&handler)`
- `(since 6.0) QFuture<T> onFailed(Function &&handler)`
- `(since 6.1) QFuture<T> onFailed(QObject *context, Function &&handler)`
- `int progressMaximum() const`
- `int progressMinimum() const`
- `QString progressText() const`
- `int progressValue() const`
- `T result() const`
- `T resultAt(int index) const`
- `int resultCount() const`
- `QList<T> results() const`
- `void resume()`
- `(since 6.0) void setSuspended(bool suspend)`
- `(since 6.0) void suspend()`
- `(since 6.0) T takeResult()`
- `(since 6.0) QFuture<QFuture<T>::ResultType<Function>> then(Function &&function)`
- `(since 6.1) QFuture<QFuture<T>::ResultType<Function>> then(QObject *context, Function &&function)`
- `(since 6.0) QFuture<QFuture<T>::ResultType<Function>> then(QThreadPool *pool, Function &&function)`
- `(since 6.0) QFuture<QFuture<T>::ResultType<Function>> then(QtFuture::Launch policy, Function &&function)`
- `(since 6.0) void toggleSuspended()`
- `(since 6.4) QFuture<U> unwrap()`
- `void waitForFinished()`
- `QFuture<T> & operator=(const QFuture<T> &other)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 44 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QFuture::ConstIterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFuture` 的配置属性。初始化或状态切换时通过 `setConstIterator(...)` 设置，之后用 `ConstIterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:ConstIterator`。
- 属性名：`QFuture`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFuture::QFuture()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFuture` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFuture::QFuture(const QFuture<T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFuture` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QFuture<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFuture::~QFuture()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFuture` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator QFuture::begin() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFuture::cancel()`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `cancel`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] void QFuture::cancelChain()`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `cancelChain`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator QFuture::constBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::constBegin` 用于计算、查询或取得与“const、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator QFuture::constEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::constEnd` 用于计算、查询或取得与“const、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator QFuture::end() const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFuture::isCanceled() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isCanceled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFuture::isFinished() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isFinished`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> bool QFuture::isResultReadyAt(int index) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isResultReadyAt`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> bool`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFuture::isRunning() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRunning`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFuture::isStarted() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isStarted`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QFuture::isSuspended() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSuspended`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QFuture::isSuspending() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSuspending`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QFuture::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] template <typename Function, typename = std::enable_if_t<std::is_invocable_r_v<T, Function>>> QFuture<T> QFuture::onCanceled(Function &&handler)`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::onCanceled` 用于计算、查询或取得与“on、Canceled”相关的操作。调用时要先确认当前状态和 `handler` 的有效范围；返回类型是 `template <typename Function, typename = std::enable_if_t<std::is_invocable_r_v<T, Function>>> QFuture<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Function, typename = std::enable_if_t<std::is_invocable_r_v<T, Function>>> QFuture<T>`。
- 参数 `handler`：类型为 `Function &&`。没有默认值，调用时必须提供。传入 `Function &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename Function, typename = std::enable_if_t<std::is_invocable_r_v<T, Function>>> QFuture<T> QFuture::onCanceled(QObject *context, Function &&handler)`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::onCanceled` 用于计算、查询或取得与“on、Canceled”相关的操作。调用时要先确认当前状态和 `context`、`handler` 的有效范围；返回类型是 `template <typename Function, typename = std::enable_if_t<std::is_invocable_r_v<T, Function>>> QFuture<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Function, typename = std::enable_if_t<std::is_invocable_r_v<T, Function>>> QFuture<T>`。
- 参数 `context`：类型为 `QObject *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `handler`：类型为 `Function &&`。没有默认值，调用时必须提供。传入 `Function &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] template <typename Function, typename = std::enable_if_t<!QtPrivate::ArgResolver<Function>::HasExtraArgs>> QFuture<T> QFuture::onFailed(Function &&handler)`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::onFailed` 用于计算、查询或取得与“on、Failed”相关的操作。调用时要先确认当前状态和 `handler` 的有效范围；返回类型是 `template <typename Function, typename = std::enable_if_t<!QtPrivate::ArgResolver<Function>::HasExtraArgs>> QFuture<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Function, typename = std::enable_if_t<!QtPrivate::ArgResolver<Function>::HasExtraArgs>> QFuture<T>`。
- 参数 `handler`：类型为 `Function &&`。没有默认值，调用时必须提供。传入 `Function &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename Function, typename = std::enable_if_t<!QtPrivate::ArgResolver<Function>::HasExtraArgs>> QFuture<T> QFuture::onFailed(QObject *context, Function &&handler)`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::onFailed` 用于计算、查询或取得与“on、Failed”相关的操作。调用时要先确认当前状态和 `context`、`handler` 的有效范围；返回类型是 `template <typename Function, typename = std::enable_if_t<!QtPrivate::ArgResolver<Function>::HasExtraArgs>> QFuture<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Function, typename = std::enable_if_t<!QtPrivate::ArgResolver<Function>::HasExtraArgs>> QFuture<T>`。
- 参数 `context`：类型为 `QObject *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `handler`：类型为 `Function &&`。没有默认值，调用时必须提供。传入 `Function &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QFuture::progressMaximum() const`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::progressMaximum` 用于计算、查询或取得与“progress、最大值”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QFuture::progressMinimum() const`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::progressMinimum` 用于计算、查询或取得与“progress、最小值”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFuture::progressText() const`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::progressText` 用于计算、查询或取得与“progress、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QFuture::progressValue() const`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::progressValue` 用于计算、查询或取得与“progress、值访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T QFuture::result() const`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::result` 用于计算、查询或取得与“结果”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T QFuture::resultAt(int index) const`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::resultAt` 用于计算、查询或取得与“结果、按位置访问”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QFuture::resultCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::resultCount` 用于计算、查询或取得与“结果、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QList<T> QFuture::results() const`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::results` 用于计算、查询或取得与“results”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QList<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QList<T>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFuture::resume()`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::resume` 用于执行与“恢复运行”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QFuture::setSuspended(bool suspend)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSuspended`。调用它会改变 `QFuture` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `suspend`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QFuture::suspend()`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::suspend` 用于执行与“suspend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T QFuture::takeResult()`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::takeResult` 用于计算、查询或取得与“取出、结果”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] template <typename Function> QFuture<QFuture<T>::ResultType<Function>> QFuture::then(Function &&function)`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::then` 用于计算、查询或取得与“then”相关的操作。调用时要先确认当前状态和 `function` 的有效范围；返回类型是 `template <typename Function> QFuture<QFuture<T>::ResultType<Function>>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Function> QFuture<QFuture<T>::ResultType<Function>>`。
- 参数 `function`：类型为 `Function &&`。没有默认值，调用时必须提供。传入 `Function &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename Function> QFuture<QFuture<T>::ResultType<Function>> QFuture::then(QObject *context, Function &&function)`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::then` 用于计算、查询或取得与“then”相关的操作。调用时要先确认当前状态和 `context`、`function` 的有效范围；返回类型是 `template <typename Function> QFuture<QFuture<T>::ResultType<Function>>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Function> QFuture<QFuture<T>::ResultType<Function>>`。
- 参数 `context`：类型为 `QObject *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `function`：类型为 `Function &&`。没有默认值，调用时必须提供。传入 `Function &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] template <typename Function> QFuture<QFuture<T>::ResultType<Function>> QFuture::then(QThreadPool *pool, Function &&function)`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::then` 用于计算、查询或取得与“then”相关的操作。调用时要先确认当前状态和 `pool`、`function` 的有效范围；返回类型是 `template <typename Function> QFuture<QFuture<T>::ResultType<Function>>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Function> QFuture<QFuture<T>::ResultType<Function>>`。
- 参数 `pool`：类型为 `QThreadPool *`。没有默认值，调用时必须提供。传入 `QThreadPool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `function`：类型为 `Function &&`。没有默认值，调用时必须提供。传入 `Function &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] template <typename Function> QFuture<QFuture<T>::ResultType<Function>> QFuture::then(QtFuture::Launch policy, Function &&function)`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::then` 用于计算、查询或取得与“then”相关的操作。调用时要先确认当前状态和 `policy`、`function` 的有效范围；返回类型是 `template <typename Function> QFuture<QFuture<T>::ResultType<Function>>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Function> QFuture<QFuture<T>::ResultType<Function>>`。
- 参数 `policy`：类型为 `QtFuture::Launch`。没有默认值，调用时必须提供。传入 `QtFuture::Launch` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `function`：类型为 `Function &&`。没有默认值，调用时必须提供。传入 `Function &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QFuture::toggleSuspended()`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toggleSuspended`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] template <typename U> QFuture<U> QFuture::unwrap()`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::unwrap` 用于计算、查询或取得与“unwrap”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `template <typename U> QFuture<U>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename U> QFuture<U>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFuture::waitForFinished()`

**API 类别：** 成员函数说明

**中文解读：** `QFuture::waitForFinished` 用于执行与“等待、For、Finished”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFuture<T> &QFuture::operator=(const QFuture<T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFuture` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QFuture<T> &`。
- 参数 `other`：类型为 `const QFuture<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class const_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QFuture` 暴露的类型声明 `const、iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `ConstIterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QFuture` 的 `Const、Iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

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

`QFuture` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
