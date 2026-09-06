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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QFuture::ConstIterator`

**作用与语义：**

Qt风格的同义词`QFuture::const_iterator`。

### `QFuture::QFuture()`

**作用与语义：**

构建一个空洞、被取消的未来。

### `QFuture::QFuture(const QFuture<T> &other)`

**作用与语义：**

复制了`other`。

### `QFuture::~QFuture()`

**作用与语义：**

毁掉未来。
注意，这既不等待也不取消异步计算。当你需要确保计算在未来被毁灭前完成时，可以使用`waitForFinished()`或`QFutureSynchronizer`。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator QFuture::begin() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向未来的第一个结果。

### `void QFuture::cancel()`

**作用与语义：**

取消由此 future 表示的异步计算。请注意，取消是异步的。在需要同步取消时，在调用 cancel() 后使用 `waitForFinished()`。
在已取消的 future 上仍可访问当前可用的结果，但在调用此函数后不会产生新结果。任何正在观察此 future 的 `QFutureWatcher` 对象都不会在已取消的 future 上发送进度和结果就绪信号。
请注意，并非所有运行中的异步计算都可以被取消。例如，由 QtConcurrent::run() 返回的 future 无法取消；但由 QtConcurrent::mappedReduced() 返回的 future 可以取消。

### `[since 6.10] void QFuture::cancelChain()`

**作用与语义：**

取消整个续延链。所有已完成的 future 保持不变，其结果仍然可用。每个待定的续延都会被取消，并调用其 `onCanceled()` 处理程序（如果它在续延链中存在的话）。
在示例中，如果在执行 `Then 2` 续延之前取消链，则 `OnCanceled 1` 和 `OnCanceled 2` 取消处理程序都会被调用。
如果在 `Then 2` 之后但在 `Then 4` 之前取消链，则仅 `OnCanceled 2` 会被调用。
注意：在已结束的 future 上调用此方法无效果。建议在表示整个续延链的 `QFuture` 对象上使用，如上例所示。
如果链中的任何续延执行异步计算并返回表示该计算的 `QFuture`，则 `cancelChain()` 调用不会传递到此类嵌套计算中。一原因是嵌套 future 仅在外部 future 完成后在续延链中可用，而取消可能在外部和嵌套 future 都在等待计算完成时发生。在这种情况下，需要显式捕获并取消嵌套 future。
在此示例中，如果 `runNestedComputation()` 正在进行中，只能通过调用 `nested.cancel()` 来取消它。

**官方示例：**

```cpp
 auto f = QtConcurrent::run([] {/*...*/})
                 .then([]{
                     // Then 1
                 })
                 .then([]{
                     // Then 2
                 })
                 .onCanceled([]{
                     // OnCanceled 1
                 })
                 .then([]{
                     // Then 3
                 })
                 .then([]{
                     // Then 4
                 })
                 .onCanceled([]{
                     // OnCanceled 2
                 });
 //...
 f.cancelChain();
```

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator QFuture::constBegin() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向未来的第一个结果。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator QFuture::constEnd() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向未来最后一个结果之后的虚数结果。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QFuture<T>::const_iterator QFuture::end() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向未来最后一个结果之后的虚数结果。

### `bool QFuture::isCanceled() const`

**作用与语义：**

如果异步计算已被`cancel()`函数取消，返回`true`;否则返回`false`。
请注意，即使该函数返回`true`，计算过程可能仍在运行。详情请参见 `cancel()`。

### `bool QFuture::isFinished() const`

**作用与语义：**

如果该未来所代表的异步计算已完成，返回`true`;否则返回`false`。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> bool QFuture::isResultReadyAt(int index) const`

**作用与语义：**

如果`index`结果立即可用，返回`true`;否则返回`false`。
注意：调用该函数后，如果`isValid()`返回该`QFuture`的`false`，会导致行为未定义。如果该`QFuture`尚未启动，请在调用该函数前调用`waitForFinished()`，以避免无定义行为。

### `bool QFuture::isRunning() const`

**作用与语义：**

如果该未来所表示的异步计算正在运行，返回`true`;否则返回`false`。

### `bool QFuture::isStarted() const`

**作用与语义：**

如果该未来所代表的异步计算已开始，返回`true`;否则返回`false`。

### `[since 6.0] bool QFuture::isSuspended() const`

**作用与语义：**

如果请求暂停异步计算并且暂停生效，则返回`true`，意味着不会有更多结果或进度变化。

### `[since 6.0] bool QFuture::isSuspending() const`

**作用与语义：**

如果异步计算已被`suspend()`函数暂停，但工作尚未暂停，计算仍在运行，则返回`true`。否则返回`false`。
要检查悬挂是否真的生效，可以用`isSuspended()`。

### `[since 6.0] bool QFuture::isValid() const`

**作用与语义：**

返回`true`是否可以访问或从该`QFuture`对象中提取结果。返回`false`如果相关`QPromise`尚未开始，或者该结果已从未来收集。
注意：该函数的返回值仅表示未来结果是否可以被消耗，不包括是否准备好。当相关`QPromise`启动时，该函数会返回`true`，但结果尚未准备好。要测试准备度，请调用`isResultReadyAt()`或`isFinished()`。

### `[since 6.0] template <typename Function, typename = std::enable_if_t<std::is_invocable_r_v<T, Function>>> QFuture<T> QFuture::onCanceled(Function &&handler)`

**作用与语义：**

为该未来附加一个取消`handler`。返回的未来表现与该未来完全相同（状态和结果相同），除非取消该未来。该`handler`是一个可调用的，不接受参数，返回该未来打包的类型值。取消后，返回的未来打包`handler`返回的值。
如果在取消前附加，`handler`会在同一线程中调用，该线程报告取消后未来已完成。如果处理程序是在该未来已被取消后连接的，则会立即在执行`onCanceled()`的线程中调用。因此，处理程序不能总是假设它将运行在哪个线程上。如果你想控制处理程序调用在哪个线程上，可以使用上下文对象的超载功能。
下面的示例演示了如何附加消去处理程序：
如果`testFuture`被取消，`Block 3`会被调用，`resultFuture`的结果将是`-1`。与`testFuture`不同，它不会处于`Canceled`状态。这意味着你可以获得它的结果，附加计数，等等。
还要注意，你可以在继续链执行时，通过启动链的未来取消链。假设`testFuture.cancel()`在`Block 1`已经执行时被调用。下一个续接会检测到取消请求，因此跳过`Block 2`，调用取消处理程序（`Block 3`）。
注意：该方法返回一个新的`QFuture`，代表延续链的结果。取消生成的`QFuture`本身不会调用通往该链的消销处理程序。这意味着如果你调用`resultFuture.cancel()`，`Block 3`不会被调用：因为`resultFuture`是将消销处理程序附加到`testFuture`后产生的未来，因此没有任何消销处理程序附加到`resultFuture`本身。只有取消`testFuture`或在`onCancelled()`叫机前附加的延期期货才会触发`Block 3`。

**官方示例：**

```cpp
 QFuture<int> testFuture /*...*/;
 auto resultFuture = testFuture.then([](int res) {
     // Block 1
     //...
     return 1;
 }).then([](int res) {
     // Block 2
     //...
     return 2;
 }).onCanceled([] {
     // Block 3
     //...
     return -1;
 });
```

### `[since 6.1] template <typename Function, typename = std::enable_if_t<std::is_invocable_r_v<T, Function>>> QFuture<T> QFuture::onCanceled(QObject *context, Function &&handler)`

**作用与语义：**

将取消`handler`附加到该未来节点，当未来被取消时调用。该`handler`是一个可调用的，不接受任何参数。它会在`context`对象的线程中调用。如果需要在特定线程中处理消去，这非常有用。
如果`context`在链条结束前被销毁，未来将被取消。详情请参见 `then()`。
注意：调用此方法时，应保证链建立过程中`context`保持活跃。
有关`handler`的更多细节，请参见其他超载的文档。

### `[since 6.0] template <typename Function, typename = std::enable_if_t<!QtPrivate::ArgResolver<Function>::HasExtraArgs>> QFuture<T> QFuture::onFailed(Function &&handler)`

**作用与语义：**

将故障处理程序附加到该未来，以处理任何异常。返回的未来表现与此未来完全相同（状态和结果相同），除非该未来失败且有例外。
`handler`是一个可调用的，可以选择无参数或只接受一个参数，通过特定错误类型进行过滤，类似于 catch 语句。它返回的是 this future 打包的类型值。失败后，返回的 future 打包了 `handler` 返回的值。
只有在异常被触发时，处理器才会被调用。如果异常是在该处理器附加后触发的，则该处理器会在报告未来因异常而结束的线程中执行。如果处理程序是在该未来失败后才附加的，则该程序会立即在执行`onFailed()`的线程中被调用。因此，处理器不能总是假设它会在哪个线程上运行。如果你想控制处理程序被调用到哪个线程，可以使用上下文对象的超载功能。
下面的示例演示了如何附加失效处理程序：
如果有多个处理程序连接，则调用第一个与抛出异常类型匹配的处理程序。例如：
如果没有任何处理程序与抛出的异常类型匹配，则该异常将传播到结果的未来：
注意：你总可以附加一个不接受参数的处理程序，以处理所有异常类型，避免写入try-catch块。

**官方示例：**

```cpp
 QFuture<int> future = someIntFuture;
 auto resultFuture = future.then([](int res) {
     //...
     throw Error();
     //...
     return res;
 }).onFailed([](const Error &e) {
     // Handle exceptions of type Error
     //...
     return -1;
 }).onFailed([] {
     // Handle all other types of errors
     //...
     return -1;
 });

 auto result = resultFuture.result(); // result is -1
```

### `[since 6.1] template <typename Function, typename = std::enable_if_t<!QtPrivate::ArgResolver<Function>::HasExtraArgs>> QFuture<T> QFuture::onFailed(QObject *context, Function &&handler)`

**作用与语义：**

将故障处理程序附加到该未来，处理未来提出或已提出的任何异常。返回与该未来类型相同的`QFuture`。处理程序仅在`context`对象线程中异常时被调用。如果需要在特定线程中处理失败，这非常有用。例如：
`QtConcurrent::run` 附带的失败处理程序会更新 UI 元素，不能从非 GUI 线程调用。因此，`this` 作为上下文提供给 `.onFailed()`，确保它会在主线程中被调用。
如果`context`在链条结束前被销毁，未来将被取消。详情请参见 `then()`。
注意：调用此方法时，应保证链建立过程中`context`保持活跃。
关于`handler`的更多细节，请参见其他超载的文档。

**官方示例：**

```cpp
 // somewhere in the main thread
 auto future = QtConcurrent::run([] {
     // This will run in a separate thread
     //...
     throw std::exception();
 }).onFailed(this, [] {
     // Update UI elements
 });
```

### `int QFuture::progressMaximum() const`

**作用与语义：**

返回最大`progressValue()`。

### `int QFuture::progressMinimum() const`

**作用与语义：**

退还最低`progressValue()`。

### `QString QFuture::progressText() const`

**作用与语义：**

返回异步计算报告的（可选）文本进度表示。
请注意，并非所有计算都能提供进度的文本表示，因此该函数可能会返回空字符串。

### `int QFuture::progressValue() const`

**作用与语义：**

返回当前进度值，该值介于 `progressMinimum()` 和 `progressMaximum()` 之间。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T QFuture::result() const`

**作用与语义：**

返回未来第一个结果。如果结果无法立即获得，该函数会阻塞并等待结果可用。这是一种方便调用 `resultAt`（0） 的方法。注意 `result()` 返回的是内部存储结果的副本。如果 `T` 是仅移动类型，或者你不想复制结果，请使用 `takeResult()`。
注意：调用该函数后，如果`isValid()`返回`false`，则会导致未定义的行为`QFuture`。如果尚未启动该`QFuture`，请在调用该函数前调用`waitForFinished()`，以避免不确定的行为。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T QFuture::resultAt(int index) const`

**作用与语义：**

未来返回`index` 结果。如果结果暂时不可用，该函数会阻塞并等待结果出现。
注意：调用该函数时，如果`isValid()`返回该`QFuture`的 `false`，则会导致未定义的行为。如果该`QFuture`尚未启动，请在调用该函数前调用 `waitForFinished()`，以避免不确定的行为。

### `int QFuture::resultCount() const`

**作用与语义：**

返回未来可用连续结果的数量。由于结果集存在空白，实际存储的结果数量可能与此值不同。从0遍历到resultCount()总是安全的。

### `template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> QList<T> QFuture::results() const`

**作用与语义：**

返回未来所有结果。如果结果暂时不可用，该函数会阻塞并等待它们可用。注意 `results()` 返回内部存储结果的副本。目前不支持获取所有仅移动类型 `T` 的结果。不过你仍然可以通过使用 STL 风格的迭代器或只读的 Java 风格迭代器遍历仅移动结果列表。
注意：如果`isValid()`返回`false`，调用该函数会导致行为未定义`QFuture`。如果该`QFuture`尚未启动，请在调用该函数前调用`waitForFinished()`以避免不确定行为。

### `void QFuture::resume()`

**作用与语义：**

恢复由未来()表示的异步计算。这是一种方便方法，简单调用`setSuspended`（false）。

### `[since 6.0] void QFuture::setSuspended(bool suspend)`

**作用与语义：**

如果`suspend`为真，该函数会暂停由未来()表示的异步计算。如果计算已经被暂停，该函数则不做任何事。`QFutureWatcher`不会立即停止发送进度和结果准备好的信号。在暂停的瞬间，可能仍有无法停止的计算正在进行中。这些计算的信号仍然会被传递。
如果`suspend`为假，该函数恢复异步计算。如果计算之前未被暂停，该函数不做任何事。
请注意，并非所有计算都可以被暂停。例如，QtConcurrent：：run() 返回的`QFuture`无法被暂停;但 QtConcurrent：：mappedReduced() 返回的`QFuture`可以。

### `[since 6.0] void QFuture::suspend()`

**作用与语义：**

暂停由该未来表示的异步计算。这是一种方便方法，简单调用 `setSuspended`（true）。

### `[since 6.0] template <typename U = T, typename = QtPrivate::EnableForNonVoid<U>> T QFuture::takeResult()`

**作用与语义：**

只有当`isValid()`返回`true`时才调用该函数，否则行为未定义。该函数从`QFuture`对象中取第一个结果（移动），当预期只有一个结果时。如果有其他结果，取第一个结果后丢弃。如果结果不能立即可用，该函数会阻塞并等待结果出现。`QFuture`会尽量使用移动语义，如果类型不可移动，则退回到复制构造。取结果后，`isValid()` 作为 `false` 计算。
注意：`QFuture` 通常允许在不同 `QFuture` 对象之间（甚至可能在不同线程之间）共享结果。takeResult() 的引入是为了让`QFuture`也能支持只移动的类型（如 std：：unique_ptr），因此它假设只有一个线程可以将结果移出未来，而且只能移动一次。另外请注意，目前不支持收集所有结果的列表。不过你仍然可以通过使用 STL 风格的迭代器或只读的 Java 风格迭代器来遍历仅移动结果的列表。

### `[since 6.0] template <typename Function> QFuture<QFuture<T>::ResultType<Function>> QFuture::then(Function &&function)`

**作用与语义：**

为该未来附加延续，允许使用`Sync`策略串联多个异步计算。`function` 是一个可调用，如果有结果（非`QFuture`），则取该未来打包的参数<void>。否则不接受参数。该方法返回一个新`QFuture`，打包 `function` 返回的类型值。返回的未来将处于未初始化状态，直到调用附加的延续，或该未来失败或被取消。
注意：如果你需要在单独的线程中启动续写，可以使用该方法的其他重载。
你可以像这样串联多个操作：
或者：
延续还可以取一个`QFuture`参数（而非其值），表示之前的未来。例如，如果`QFuture`有多个结果，用户希望在续写中访问这些结果，这非常有用。或者用户需要处理续写中前一个未来的异常，以避免打断多个延续链。例如：
警告：如果前一个未来包含多个类型为`T`的结果，且延续以类型`T`的参数为参数，延续中只处理前一`QFuture`的第一个结果！
如果前一个未来抛出异常且未在续写中处理，该异常将传播到延续未来，以便调用者处理：
在这种情况下，整个延续链都会被打断。
注意：如果这个未来被取消，附带的续集也会被取消。

**官方示例：**

```cpp
 QFuture<int> future = ...;
 future.then([](int res1){ ... }).then([](int res2){ ... })...
```

### `[since 6.1] template <typename Function> QFuture<QFuture<T>::ResultType<Function>> QFuture::then(QObject *context, Function &&function)`

**作用与语义：**

为该未来附加延续，允许链式多次异步计算。当该未来表示的异步计算结束后，`function`将在`context`对象的线程中调用。如果需要在特定线程中调用延续，这非常有用。例如：
`QtConcurrent::run` 中附加的延续会更新 UI 元素，且无法从非 GUI 线程调用。因此，`this` 作为上下文提供给 `.then()`，确保它会在主线程中被调用。
以下续述也将从同一上下文调用，除非指定不同的上下文或发射策略：
这是因为默认情况下`.then()`调用的是与前一个线程相同的线程。
但请注意，如果续写是在该未来结束后附加的，它会立即在执行`then()`的线程中调用：
在上述例子中，如果`cachedResultsReady` `true`且返回了准备好的未来，那么第一个`.then()`可能在第二个附加之前就完成了。在这种情况下，它将在当前线程中被解析。因此，当有疑问时，显式传递上下文。
如果`context`在链结束前被销毁，未来将被取消。这意味着当`context`不再有效时，可能会调用取消处理程序。为防止这种情况，捕获`context`为`QPointer`：
当上下文对象被销毁时，取消立即发生。链中之前的未来不会被取消，会持续运行直到完成。
注意：调用此方法时，应保证链建立过程中`context`保持活跃。

**官方示例：**

```cpp
 // somewhere in the main thread
 auto future = QtConcurrent::run([] {
     // This will run in a separate thread
     //...
 }).then(this, [] {
     // Update UI elements
 });
```

### `[since 6.0] template <typename Function> QFuture<QFuture<T>::ResultType<Function>> QFuture::then(QThreadPool *pool, Function &&function)`

**作用与语义：**

附加一个延续，允许在需要时串联多个异步计算。当该未来所代表的异步计算结束后，`function`将在`pool`日安排。

### `[since 6.0] template <typename Function> QFuture<QFuture<T>::ResultType<Function>> QFuture::then(QtFuture::Launch policy, Function &&function)`

**作用与语义：**

将延续连接到该未来，允许串联多个异步计算。当该未来表示的异步计算结束后，将根据给定的发射 `policy`调用`function`。返回一个表示延续结果的新 `QFuture`。
根据`policy`不同，续接会在与未来相同的线程中调用，或在新线程中调用，或者继承该未来的启动策略和线程池。如果未指定启动策略（参见仅调用可调用的超载），则使用`Sync`策略。
在下面的示例中，两个续写都会在一个新线程中调用（但在同一线程内）。
在以下示例中，两个延续将在使用同一线程池的新线程中调用。
有关其他超载的文档，`function`详情请参见。

**官方示例：**

```cpp
 QFuture<int> future = ...;
 future.then(QtFuture::Launch::Async, [](int res){ ... }).then([](int res2){ ... });
```

### `[since 6.0] void QFuture::toggleSuspended()`

**作用与语义：**

切换异步计算的暂停状态。换句话说，如果计算当前处于暂停状态，调用该函数即可恢复;如果计算正在运行，则暂停。这是一种方便调用`setSuspended`（！（`isSuspending()` ||`isSuspended()`））的方法。

### `[since 6.4] template <typename U> QFuture<U> QFuture::unwrap()`

**作用与语义：**

从该`QFuture<T>`展开内在未来，其中`T` 是类型`QFuture<U>`的未来，即该未来具有类型`QFuture<QFuture<U>>`。例如：
`unwrappedFuture`将在`outerFuture`内嵌套的内未来实现后立即实现，结果或异常情况一致，且在同一报告内未来完成的线程中。如果内未来被取消，`unwrappedFuture`也会被取消。
这在串联多个计算时尤其有用，其中一个计算会返回`QFuture`作为结果类型。例如，假设我们想从一个URL下载多张图片，放大这些图像，并用QtConcurrent：：mappedReduced()将其缩减为单一图像。我们可以写成这样：
这里`QtConcurrent::mappedReduced()`返回一个`QFuture<QImage>`，因此`.then(processImages)`返回一个`QFuture<QFuture<QImage>>`。由于`show()`以`QImage`为参数，`.then(processImages)`的结果不能直接传递给它。我们需要调用`.unwrap()`，它会在内在未来准备好时获得结果，并传递给下一个延续。
如果是多重嵌套，`.unwrap()`会下降到最内层：

**官方示例：**

```cpp
 QFuture<QFuture<int>> outerFuture /*...*/;
 QFuture<int> unwrappedFuture = outerFuture.unwrap();
```

### `void QFuture::waitForFinished()`

**作用与语义：**

等待异步计算完成（包括`cancel()`ed计算），即直到`isFinished()`返回`true`。

### `QFuture<T> &QFuture::operator=(const QFuture<T> &other)`

**作用与语义：**

将`other`分配到这个未来，并返回对该未来的引用。

### `class const_iterator`

**作用与语义：**

QFuture::const_iterator 类提供了 QFuture 的 STL 风格常量迭代器。
`QFuture` 提供 STL 风格迭代器和 Java 风格迭代器。STL 风格迭代器更底层，使用起来更繁琐；另一方面，它们略快，并且对于已经熟悉 STL 的开发者，有熟悉度的优势。
默认的 `QFuture::const_iterator` 构造函数创建未初始化的迭代器。你必须使用 `QFuture` 函数（如 `QFuture::constBegin()` 或 `QFuture::constEnd()`）初始化它，然后才能开始迭代。下面是一个打印未来中所有可用结果的典型循环：

**官方示例：**

```cpp
 QFuture<QString> future = someQStringFuture;

 QFuture<QString>::const_iterator i;
 for (i = future.constBegin(); i != future.constEnd(); ++i)
     cout << qPrintable(*i) << endl;
```

### `ConstIterator`

**作用与语义：**

Qt风格的同义词`QFuture::const_iterator`。

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
