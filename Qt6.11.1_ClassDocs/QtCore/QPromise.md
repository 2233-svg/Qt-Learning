# QPromise

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 异步任务生产者接口，负责向 QFuture 报告进度、结果、暂停和取消状态。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QPromise`：异步任务生产者接口，负责向 QFuture 报告进度、结果、暂停和取消状态。

**内部模型：** 并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

**适用场景：** 先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

## 2. 依赖与对象关系

- 头文件：`#include <QPromise>`
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

### 公有函数

- `QPromise()`
- `QPromise(QPromise<T> &&other)`
- `~QPromise()`
- `bool addResult(T &&result, int index = -1)`
- `bool addResult(const T &result, int index = -1)`
- `(since 6.6) bool addResults(const QList<T> &results)`
- `(since 6.6) bool emplaceResult(Args &&... args)`
- `(since 6.6) bool emplaceResultAt(int index, Args &&... args)`
- `void finish()`
- `QFuture<T> future() const`
- `bool isCanceled() const`
- `void setException(const QException &e)`
- `void setException(std::__exception_ptr::exception_ptr e)`
- `void setProgressRange(int minimum, int maximum)`
- `void setProgressValue(int progressValue)`
- `void setProgressValueAndText(int progressValue, const QString &progressText)`
- `void start()`
- `void suspendIfRequested()`
- `void swap(QPromise<T> &other)`
- `QPromise<T> & operator=(QPromise<T> &&other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QPromise::QPromise()`

**作用与语义：**

构建一个带有默认状态的QPromise。

### `QPromise::QPromise(QPromise<T> &&other)`

**作用与语义：**

Move从`other`构建了一个新的QPromise。

### `QPromise::~QPromise()`

**作用与语义：**

毁掉了承诺。
注意：除非用户事先调用`finish()`，否则承诺在销毁时隐含地转为取消状态。

### `bool QPromise::addResult(T &&result, int index = -1)`

**作用与语义：**

和。
或者，如果`index == -1`（默认）。

**官方示例：**

```cpp
 emplaceResultAt(index, result);            // first overload
 emplaceResultAt(index, std::move(result)); // second overload
```

### `[since 6.6] bool QPromise::addResults(const QList<T> &results)`

**作用与语义：**

在内部结果收集的最后添加`results`。
退货在`results`加入合集时会`true`。
当该承诺处于取消或完成状态时，退货`false`。
这比循环`addResult()`更高效，因为关联的未来每个 addResults() 调用只通知一次，而每个 `results` 中包含的元素则通知一次，而单个 `addResult()` 调用则是如此。但如果每个元素的计算需要时间，那么接收端（未来）的代码在所有结果报告前无法继续，因此只有在连续元素的计算相对快速时才使用该函数。

### `[since 6.6] template <typename... Args, std::enable_if_t<std::is_constructible_v<T, Args...>, bool> = true> bool QPromise::emplaceResult(Args &&... args)`

**作用与语义：**

将从`args...`构造的结果添加到`index`位置（`emplaceResultAt()`）或集合末端（`emplaceResult()`）的内部结果集合中。
返回`true`结果加入集合时。
当该承诺处于取消或已完成状态，或结果被拒绝时，`false`返回。`addResult()`拒绝添加结果，如果集合中已经存在同一个索引的另一个结果。
这些函数只有在`T`可由`args....`构造时才参与重载决议。
你可以通过调用`QFuture::resultAt()`获得特定指数的结果。
注意：可以指定任意索引并在该索引上请求结果。然而，一些`QFuture`方法以连续结果为基础。例如，使用`QFuture::resultCount()`或`QFuture::const_iterator`的迭代方法。为了获得所有可用结果而不考虑是否存在索引缺口，可以使用`QFuture::results()`。

### `void QPromise::finish()`

**作用与语义：**

报告计算已完成。完成后，调用`addResult()`时不会添加新结果。该方法伴随`start()`。

### `QFuture<T> QPromise::future() const`

**作用与语义：**

还原了与这个承诺相关的未来。

### `bool QPromise::isCanceled() const`

**作用与语义：**

返回计算是否已被`QFuture::cancel()`函数取消。返回的值`true`表示计算应完成并调用`finish()`。
注意：取消后，未来仍可访问当前可用结果，但拨`addResult()`时不会添加新结果。

### `void QPromise::setException(const QException &e)`

**作用与语义：**

将异常设置为`e`计算的结果。
注意：在计算执行过程中，最多只能设置一个例外。
注意：此方法在 `QFuture::cancel()` 或 `finish()` 后无效。

### `void QPromise::setException(std::__exception_ptr::exception_ptr e)`

**作用与语义：**

将异常设置为`e`计算的结果。
注意：在计算执行过程中，最多只能设置一个例外。
注意：此方法在 `QFuture::cancel()` 或 `finish()` 后无效。

### `void QPromise::setProgressRange(int minimum, int maximum)`

**作用与语义：**

将计算的进度范围设在`minimum`到`maximum`之间。
如果`maximum`小于`minimum`，`minimum`成为唯一的法定价值。
进度值会被重置为`minimum`。
通过使用 setProgressRange（0， 0） 来禁用进度范围的使用。此时进度值也会重置为 0。

### `void QPromise::setProgressValue(int progressValue)`

**作用与语义：**

将计算的进度值设为`progressValue`。可以只递增进度值。这是一种方便调用 `setProgressValueAndText`（progressValue， QString()）的方法。
如果`progressValue`超出进度范围，这种方法就没有效果。

### `void QPromise::setProgressValueAndText(int progressValue, const QString &progressText)`

**作用与语义：**

将进度值和计算的进度文本分别设为`progressValue`和`progressText`。只能递增进度值。
注意：如果承诺处于取消或已完成状态，该功能无效。

### `void QPromise::start()`

**作用与语义：**

报告计算已开始。调用该方法时表示计算开始时间很重要，因为`QFuture`方法依赖于这些信息。
注意：当从新创建的线程调用start()时需要额外注意。在这种情况下，由于线程调度的实现细节，调用可能会自然延迟。

### `void QPromise::suspendIfRequested()`

**作用与语义：**

有条件地暂停当前执行线程，等待相应方法恢复或取消`QFuture`。除非`QFuture::suspend()`或相关方法请求暂停计算，否则该方法不会阻塞。如果你想检查执行是否被暂停，可以使用`QFuture::isSuspended()`。
注意：当多个线程使用相同的承诺时，只要至少有一个带有承诺的线程暂停，就会`QFuture::isSuspended()` `true`。
以下代码片段展示了悬挂机构的使用情况：
`QFuture::suspend()`请求相应的暂停承诺：
当`QFuture::isSuspended()`变成`true`后，你可以得到中间效果：
暂停时，您可以恢复或取消等待的计算：

**官方示例：**

```cpp
     // Create promise and future
     QPromise<int> promise;
     QFuture<int> future = promise.future();

     promise.start();
     // Start a computation thread that supports suspension and cancellation
     const std::unique_ptr<QThread> thread(QThread::create([] (QPromise<int> promise) {
         for (int i = 0; i < 100; ++i) {
             promise.addResult(i);
             promise.suspendIfRequested();   // support suspension
             if (promise.isCanceled())       // support cancellation
                 break;
         }
         promise.finish();
     }, std::move(promise)));
     thread->start();
```

### `[noexcept] void QPromise::swap(QPromise<T> &other)`

**作用与语义：**

用`other`交换了这个承诺。这个操作非常快，从不失误。

### `[noexcept] QPromise<T> &QPromise::operator=(QPromise<T> &&other)`

**作用与语义：**

Move 为该承诺分配`other`，并返回该承诺的引用。

### `bool addResult(const T &result, int index = -1)`

**作用与语义：**

和。
或者，如果`index == -1`（默认）。

**官方示例：**

```cpp
 emplaceResultAt(index, result);            // first overload
 emplaceResultAt(index, std::move(result)); // second overload
```

### `(since 6.6) bool emplaceResultAt(int index, Args &&... args)`

**作用与语义：**

将从`args...`构造的结果添加到`index`位置（`emplaceResultAt()`）或集合末端（`emplaceResult()`）的内部结果集合中。
返回`true`结果加入集合时。
当该承诺处于取消或已完成状态，或结果被拒绝时，`false`返回。`addResult()`拒绝添加结果，如果集合中已经存在同一个索引的另一个结果。
这些函数只有在`T`可由`args....`构造时才参与重载决议。
你可以通过调用`QFuture::resultAt()`获得特定指数的结果。
注意：可以指定任意索引并在该索引上请求结果。然而，一些`QFuture`方法以连续结果为基础。例如，使用`QFuture::resultCount()`或`QFuture::const_iterator`的迭代方法。为了获得所有可用结果而不考虑是否存在索引缺口，可以使用`QFuture::results()`。

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

`QPromise` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
