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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QFutureWatcher::QFutureWatcher(QObject *parent = nullptr)`

**作用与语义：**

构建一个带有给定`parent`的新QFutureWatcher。在与`setFuture()`设定未来之前，函数 `isStarted()`、`isCanceled()`和`isFinished()`返回`true`。

### `[virtual] QFutureWatcher::~QFutureWatcher()`

**作用与语义：**

摧毁了`QFutureWatcher`。

### `[slot] void QFutureWatcher::cancel()`

**作用与语义：**

取消由 `future()` 表示的异步计算。请注意，取消是异步的。在需要同步取消时，在调用 cancel() 后使用 `waitForFinished()`。
在已取消的 `QFuture` 上仍可访问当前可用的结果，但在调用此函数后不会产生新结果。此外，一旦取消，此 `QFutureWatcher` 将不再发送进度和结果就绪信号。这包括 `progressValueChanged()`、`progressRangeChanged()`、`progressTextChanged()`、`resultReadyAt()` 和 `resultsReadyAt()` 信号。
请注意，并非所有运行中的异步计算都可以被取消。例如，由 QtConcurrent::run() 返回的 `QFuture` 无法取消；但由 QtConcurrent::mappedReduced() 返回的 `QFuture` 可以取消。

### `[signal] void QFutureWatcher::canceled()`

**作用与语义：**

如果被监视的未来被取消，该信号就会发出。

### `[signal] void QFutureWatcher::finished()`

**作用与语义：**

当被观看的未来结束时，该信号会发出。

### `QFuture<T> QFutureWatcher::future() const`

**作用与语义：**

回归被注视的未来。

### `bool QFutureWatcher::isCanceled() const`

**作用与语义：**

如果异步计算已被`cancel()`函数取消，或未设置未来，返回 `true`;否则返回 `false`。
请注意，即使该函数返回`true`，计算可能仍在运行。详情请参见 `cancel()`。

### `bool QFutureWatcher::isFinished() const`

**作用与语义：**

如果`future()`表示的异步计算已完成，或未来未被设置，返回`true`;否则返回`false`。

### `bool QFutureWatcher::isRunning() const`

**作用与语义：**

如果`future()`表示的异步计算正在运行，返回`true`;否则返回`false`。

### `bool QFutureWatcher::isStarted() const`

**作用与语义：**

如果`future()`表示的异步计算已开始，或未设置未来，返回`true`;否则返回`false`。

### `[since 6.0] bool QFutureWatcher::isSuspended() const`

**作用与语义：**

如果请求暂停异步计算并且暂停生效，则返回`true`，意味着不会有更多结果或进度变化。

### `[since 6.0] bool QFutureWatcher::isSuspending() const`

**作用与语义：**

如果异步计算已被`suspend()`函数暂停，但工作尚未暂停，计算仍在运行，则返回`true`。否则返回`false`。
要检查悬挂是否真的生效，可以用`isSuspended()`。

### `int QFutureWatcher::progressMaximum() const`

**作用与语义：**

返回最大`progressValue()`。

### `int QFutureWatcher::progressMinimum() const`

**作用与语义：**

退还最低`progressValue()`。

### `[signal] void QFutureWatcher::progressRangeChanged(int minimum, int maximum)`

**作用与语义：**

预计未来的进展范围已变为`minimum`和`maximum`。

### `QString QFutureWatcher::progressText() const`

**作用与语义：**

返回异步计算报告的（可选）文本进度表示。
请注意，并非所有计算都能提供进度的文本表示，因此该函数可能会返回空字符串。

### `[signal] void QFutureWatcher::progressTextChanged(const QString &progressText)`

**作用与语义：**

当观看的未来报告文本进展信息时，`progressText`发出该信号。

### `int QFutureWatcher::progressValue() const`

**作用与语义：**

返回当前进度值，该值介于 `progressMinimum()` 和 `progressMaximum()` 之间。

### `[signal] void QFutureWatcher::progressValueChanged(int progressValue)`

**作用与语义：**

当被观看的未来报告进展时，`progressValue`会发出该信号，显示当前的进度。为了避免GUI事件循环重载，`QFutureWatcher`限制了进度信号的发出率。这意味着连接到该时段的监听者可能无法接收到未来报告的所有进度报告。最后的进度更新（`progressValue`等于最大值）始终会被传递。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T QFutureWatcher::result() const`

**作用与语义：**

返回`future()`中的第一个结果。如果结果不能立即出现，该函数会阻塞并等待结果出现。这是一种方便调用`resultAt`（0）的方法。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T QFutureWatcher::resultAt(int index) const`

**作用与语义：**

返回`future()` `index`处的结果。如果结果暂时不可用，该函数会阻塞并等待结果出现。

### `[signal] void QFutureWatcher::resultReadyAt(int index)`

**作用与语义：**

当被观察的未来报告`index`时，该信号会发出。如果未来报告多个结果，索引会显示是哪一个。结果可能会被打乱顺序报告。要获取结果，请调用`resultAt`（index）;

### `[signal] void QFutureWatcher::resultsReadyAt(int beginIndex, int endIndex)`

**作用与语义：**

当观察的未来报告结果时，该信号发出。结果从`beginIndex`到`endIndex`进行索引。

### `[slot] void QFutureWatcher::resume()`

**作用与语义：**

恢复由`future()`表示的异步计算。这是一种便捷方法，简单调用`setSuspended`（false）。

### `[signal] void QFutureWatcher::resumed()`

**作用与语义：**

当被监视的未来被恢复时，该信号会发出。

### `void QFutureWatcher::setFuture(const QFuture<T> &future)`

**作用与语义：**

开始观看给定的`future`。
如果`future`已经开始，观察者会最初发出信号，让听众了解未来状态。如果适用，以下信号将按给定顺序发出：`started()`、`progressRangeChanged()`、`progressValueChanged()`、`progressTextChanged()`、`resultsReadyAt()`、`resultReadyAt()`、`suspending()`、`suspended()`、`canceled()`和`finished()`。其中，`resultsReadyAt()`和`resultReadyAt()`可以多次发出，以覆盖所有可用结果。`progressValueChanged()`和`progressTextChanged()`只会针对最新的可用进度值和文本发出一次。
为避免竞态条件，重要的是完成连接后调用该函数。

### `void QFutureWatcher::setPendingResultsLimit(int limit)`

**作用与语义：**

setPendingResultLimit() 提供限速控制。当待处理的`resultReadyAt()`或`resultsReadyAt()`信号数量超过该`limit`时，未来所代表的计算将自动限速。当待处理信号数量降至`limit`以下时，计算将继续。

### `[slot, since 6.0] void QFutureWatcher::setSuspended(bool suspend)`

**作用与语义：**

如果`suspend`为真，该函数会暂停由`future()`表示的异步计算。如果计算已经暂停，该函数则不做任何事。`QFutureWatcher`不会立即停止传递进度和结果准备好信号，当未来暂停时。暂停时可能仍有计算正在进行且无法停止。此类计算的信号仍会被传递。
如果`suspend`为假，该函数恢复异步计算。如果计算之前未被暂停，该函数不做任何事。
请注意，并非所有计算都可以被暂停。例如，QtConcurrent：：run() 返回的`QFuture`无法被暂停;但 QtConcurrent：：mappedReduced() 返回的`QFuture`可以。

### `[signal] void QFutureWatcher::started()`

**作用与语义：**

当`QFutureWatcher`开始观察与`setFuture()`共度的未来时，就会发出这个信号。

### `[slot, since 6.0] void QFutureWatcher::suspend()`

**作用与语义：**

暂停由该未来表示的异步计算。这是一种方便方法，简单调用 `setSuspended`（true）。

### `[signal, since 6.0] void QFutureWatcher::suspended()`

**作用与语义：**

该信号在`suspend()`生效时发出，意味着不再有运行中的计算。收到该信号后，不再期待结果准备好或进展报告信号。

### `[signal, since 6.0] void QFutureWatcher::suspending()`

**作用与语义：**

当被观察的未来状态被设置为暂停时，该信号会发出。
注意：该信号仅通知暂停请求。并不表示所有后台操作已被停止。暂停时正在进行的计算信号仍会被发送。要获得暂停生效时间，请使用`suspended()`信号。

### `[slot, since 6.0] void QFutureWatcher::toggleSuspended()`

**作用与语义：**

切换异步计算的暂停状态。换句话说，如果计算当前处于暂停状态，调用该函数即可恢复;如果计算正在运行，则暂停。这是一种方便调用`setSuspended`（！（`isSuspending()` ||`isSuspended()`））的方法。

### `void QFutureWatcher::waitForFinished()`

**作用与语义：**

等待异步计算完成（包括`cancel()`ed计算），即直到`isFinished()`返回`true`。

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
