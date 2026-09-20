# Qt QFuture 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFuture>`  
> 所属模块：`Qt6::Core`  
> 类型性质：模板值类型，内部共享异步计算状态  
> 相关类型：`QPromise`、`QFutureWatcher`、`QtConcurrent`、`QtFuture`

## 1. 它解决什么问题

`QFuture<T>` 是“异步计算结果”的句柄。它本身通常不执行计算，而是指向由 `QPromise`、`QtConcurrent` 或 `QtFuture` 创建的共享状态，让调用方可以：

- 查询任务是否启动、运行、暂停、取消或完成；
- 等待一个结果或一组结果；
- 在结果就绪后继续执行下一段工作；
- 把异常和取消转化为 continuation 链中的分支；
- 把同一个异步状态交给多个函数、线程或 `QFutureWatcher`。

它和 `std::future` 的重要区别是：一个 `QFuture` 可以描述多个结果、进度、取消/暂停状态和 continuation 链；复制 `QFuture` 也不会复制计算，而是复制一个共享状态句柄。

`QFuture` 不是线程对象，也不是任务启动器。真正启动并写入结果的通常是：

- `QtConcurrent::run()`、`mapped()`、`mappedReduced()` 等 Qt Concurrent API；
- `QPromise<T>` 配合工作线程；
- `QtFuture::connect()`、`makeReadyValueFuture()` 等辅助 API。

## 2. 适合哪些场景

### 2.1 后台计算完成后继续处理

例如后台读取文件、计算哈希、解析 JSON，完成后在另一个 continuation 中更新模型：

```cpp
auto future = QtConcurrent::run([] {
    return expensiveCalculation();
}).then([](int value) {
    return QString::number(value);
});

future.waitForFinished();
const QString text = future.result();
```

真正的 GUI 程序通常不应在主线程调用 `waitForFinished()`，而应把最后一步放到 `then(context, ...)` 或使用 `QFutureWatcher`。

### 2.2 逐个消费多个结果

`QtConcurrent::mapped()`、`QPromise` 等生产者可能报告多个结果。此时 `resultCount()`、`isResultReadyAt()`、`resultAt()` 和只读迭代器比只调用 `result()` 更合适。

### 2.3 可取消或可暂停的长任务

用户点击“取消导入”“暂停索引”时，可以保留 `QFuture` 句柄并调用 `cancel()` 或 `setSuspended(true)`。但这些操作是对生产者的请求，不是强制终止；任务是否支持它们由生产者决定。

### 2.4 把异步步骤串成流水线

`then()` 适合表达“下载后解析、解析后转换、转换后保存”。当某一步返回另一个 `QFuture` 时，使用 `unwrap()` 展平嵌套结果。

## 3. 构建与最小示例

只使用 `QFuture` 类型时链接 Core；示例中的 `QtConcurrent::run()` 还需要 Concurrent：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Concurrent)
target_link_libraries(mytarget PRIVATE Qt6::Core Qt6::Concurrent)
```

```cpp
#include <QFuture>
#include <QtConcurrentRun>

QFuture<int> startWork()
{
    return QtConcurrent::run([] {
        return 42;
    });
}

void useFuture()
{
    QFuture<int> future = startWork();
    future.waitForFinished();
    const int answer = future.result();
}
```

这个例子适合说明 API 关系，不适合直接套进 GUI 槽函数：`waitForFinished()` 会阻塞调用线程。

## 4. 先建立正确的状态模型

### 4.1 `QFuture` 是共享句柄，不是计算副本

```cpp
QFuture<int> first = startWork();
QFuture<int> second = first;
```

`first` 和 `second` 观察的是同一个底层状态。复制、赋值和析构只改变句柄数量，不会复制或自动停止任务。对共享状态进行 `cancel()`、`suspend()` 等操作，其他句柄也能观察到状态变化。

因此，复制并不能制造两个独立的 continuation 订阅点。Qt 文档特别提醒：同一状态上的 continuation 设计要谨慎；把 `then()` 附加到共享 future 时，后附加的 continuation 可能覆盖前一个 continuation。需要分叉时，应在设计上明确创建独立的 future 链，而不是把复制当作广播机制。

### 4.2 默认构造不是“还没开始但将来会有结果”

```cpp
QFuture<int> future;
```

默认构造得到的是 empty/canceled future。它不关联一个会自行启动的生产者。不要对它直接调用 `result()`、`resultAt()` 或 `isResultReadyAt()`；先确认 `isValid()` 和实际的生产来源。

### 4.3 `isValid()` 与“结果已就绪”不是一回事

- `isValid() == false`：结果不能从这个句柄安全消费，常见原因是关联的 `QPromise` 尚未启动，或结果已经被 `takeResult()` 取走。
- `isValid() == true`：结果具备被消费的资格，不表示结果已经准备完成。
- 判断具体结果是否立即可取，用 `isResultReadyAt(index)`。
- 判断整个计算是否结束，用 `isFinished()`。

文档对无效 future 上的结果 API 明确标为未定义行为。对尚未启动的 future，在调用结果 API 前也应先 `waitForFinished()`，避免未定义行为。

### 4.4 结果访问可能阻塞

`result()`、`resultAt()`、`results()`、`takeResult()` 和迭代器的推进都可能等待生产者提供结果。它们不是“只读内存”的无阻塞查询。

在 GUI 线程、持有业务锁的线程或需要持续处理事件的线程中调用它们，可能造成界面冻结、锁反转或事件循环无法推进。需要无阻塞判断时先调用 `isResultReadyAt()`，需要异步响应时用 `then()` 或 `QFutureWatcher`。

### 4.5 结果集合可能有 gaps

多结果 future 的结果索引不一定按顺序到达。`resultCount()` 返回的是从索引 0 开始连续可用的结果数量，不一定等于底层已经存储的结果总数。读取任意索引前，应使用 `isResultReadyAt(index)` 或等待相应信号。

## 5. 取消、暂停和完成

### 5.1 `cancel()` 是请求，不是强杀

调用 `cancel()` 后：

- 取消请求立即写入共享状态，但底层计算可能还在运行；
- 已经可用的结果仍可能读取；
- 不会再有新的结果被报告为可用；
- 需要知道任务何时真正结束时，再调用 `waitForFinished()` 或等待 `finished`；
- `QFutureWatcher` 不再投递进度和结果就绪信号。

`QtConcurrent::run()` 返回的 future 不能取消；`mappedReduced()` 等使用 `QPromise` 协作的计算通常可以取消。这是生产者能力差异，不是 `QFuture::cancel()` 返回值能表达的差异。

### 5.2 `cancelChain()` 取消 continuation 链

Qt 6.10 新增的 `cancelChain()` 面向整条 continuation 链：

- 已经完成的 future 不受影响，已有结果仍可用；
- 尚未执行的 continuation 会被取消；
- 链中对应的 `onCanceled()` 处理器会被调用；
- 对已经完成的 future 调用没有效果；
- 如果 continuation 已经启动了一个嵌套异步任务，取消不会自动传播到那个已经启动的内层 future。

因此，内层 future 需要由业务代码保存并单独 `cancel()`。`cancelChain()` 更适合对表示“整条流程”的最后一个 future 调用。

### 5.3 暂停有“请求中”和“已生效”两个阶段

- `isSuspending()`：已经请求暂停，但仍有计算在运行；
- `isSuspended()`：暂停已生效，不再期待新的结果或进度变化；
- `suspending()` / `suspended()` 是 `QFutureWatcher` 对应的两个阶段信号。

暂停同样由生产者支持与否决定。`QtConcurrent::run()` 的 future 不能暂停；支持 `QPromise` 暂停协作的算法可以响应暂停。

暂停期间已经在执行的工作可能完成，所以 watcher 仍可能交付当时已经产生的结果或进度信号。不要把调用 `suspend()` 的瞬间当作“所有后台代码已停止”。

Qt 6.0 以前的 `pause()`、`setPaused()`、`isPaused()`、`togglePaused()` 已弃用，使用 suspended API。

## 6. continuation 和异常链

### 6.1 `then()` 的输入形式

对 `QFuture<T>`，continuation 通常写成：

```cpp
QFuture<int> input = startWork();

auto output = input.then([](int value) {
    return value * 2;
});
```

对 `QFuture<void>`，回调不接参数：

```cpp
QFuture<void> input = startVoidWork();
auto output = input.then([] {
    return QStringLiteral("done");
});
```

如果 future 包含多个结果，而回调参数是 `T`，该 continuation 只处理第一个结果。需要访问整个 future、多个结果或上一阶段异常时，可以让回调接收 `QFuture<T>`：

```cpp
auto output = input.then([](QFuture<int> previous) {
    previous.waitForFinished();
    return previous.results();
});
```

### 6.2 默认 launch 策略不是“总会开新线程”

`then(function)` 使用 `QtFuture::Launch::Sync`。continuation 通常在前一个 future 报告完成的线程执行；如果附加时 future 已完成，也可能直接在调用 `then()` 的线程执行。

需要控制执行位置时使用：

- `then(QtFuture::Launch::Async, function)`：调度到新线程；
- `then(QtFuture::Launch::Inherit, function)`：继承前一步的 launch 策略和线程池；
- `then(QThreadPool *pool, function)`：交给指定线程池；
- `then(QObject *context, function)`：在 context 所在线程执行，适合更新 GUI 对象。

`then(context, ...)` 依赖 context 的生命周期。context 被销毁时，该 continuation 链会取消，但之前已经开始的 future 不会被反向取消。取消处理器如果还要访问 context，应捕获 `QPointer` 并检查空指针。

### 6.3 `onFailed()` 处理异常

Qt 的 QFuture continuation 错误处理依赖 C++ exceptions。`onFailed()` 的处理器可以：

- 不接参数，匹配所有异常；
- 接收某个异常类型的 `const T &`，按类型筛选；
- 返回与 future 相同的结果类型，用恢复值接续后续链。

多个处理器按附加顺序尝试，第一个匹配异常类型的处理器执行。没有匹配时，异常继续传播到返回的 future。

`onFailed(context, handler)` 保证处理器在 context 所在线程执行，Qt 6.1 起提供。无 context 的重载在异常报告线程执行；如果 future 在附加处理器前已经失败，则可能立即在调用 `onFailed()` 的线程执行。

如果项目关闭了 C++ exceptions，不要假设 `onFailed()` 能替代错误值模型。可把错误状态设计成 `std::variant<Value, Error>`、`std::expected` 风格自定义类型等，让失败成为正常结果的一部分。

### 6.4 `onCanceled()` 把取消转成恢复值

`onCanceled()` 的处理器不接参数，返回 `T`；取消发生后，返回的 future 会携带这个恢复值。future 未取消时，返回 future 与原状态和结果一致。

它和 `onFailed()` 不同：取消不是异常，不会由 `onFailed()` 捕获。对 `QFuture<void>`，处理器返回 `void` 即可。

## 7. `QFuture<void>` 的特殊点

`QFuture<void>` 专门去掉结果获取 API，只保留状态、进度、取消、暂停、等待和 continuation 能力。任意 `QFuture<T>` 都可以复制或赋值为 `QFuture<void>`，适合只关心任务是否完成的代码：

```cpp
QFuture<int> valueFuture = startWork();
QFuture<void> statusOnly = valueFuture;

statusOnly.waitForFinished();
```

不要在 `QFuture<void>` 上寻找 `result()`、`resultAt()`、`results()` 或 `takeResult()`。如果需要值，保留 `QFuture<T>`。

## 8. 多线程和生命周期边界

- `QFuture` 的句柄可以复制并在多个线程使用，但共享状态不等于业务数据自动无竞态；结果对象本身仍需满足自身的线程安全要求。
- 析构 `QFuture` 不会等待计算，也不会取消计算。需要同步收尾时显式调用 `waitForFinished()`，或使用 `QFutureSynchronizer` 管理一组 future。
- continuation 可能因为 work-stealing 在请求结果的线程执行，即使逻辑上指定了线程池；不要用“我把它放进线程池了”推导出绝对的线程归属。
- 在持锁状态下调用可能阻塞的结果 API 或执行用户 continuation，容易造成死锁。
- future 结果类型至少要满足可移动构造要求；结果复制、`results()` 和 `result()` 是否可用还取决于类型的复制能力。

## 9. 逐项 API 说明

### 成员类型

#### `QFuture::const_iterator`

只读 STL 风格迭代器，遍历 future 报告的结果。解引用返回 `const T &`，不能用于 `QFuture<void>`。迭代器推进可能等待对应结果，所以它不是无阻塞遍历器。

#### `QFuture::ConstIterator`

Qt 风格的别名，等价于 `QFuture::const_iterator`。选择哪一个主要取决于项目现有迭代器风格。

### 构造、赋值和销毁

#### `QFuture::QFuture()`

构造 empty/canceled future。它不启动任何计算，不能把它当作“尚未设置的任务槽位”直接读取结果。

#### `QFuture::QFuture(const QFuture<T> &other)`

复制 future 句柄并共享底层状态，不复制计算或结果存储。复制后的对象可以独立保存，但取消、完成和结果状态是共同的。

#### `QFuture::~QFuture()`

销毁句柄，不等待、不取消异步计算。需要确保后台工作结束时，先调用 `waitForFinished()` 或使用 `QFutureSynchronizer`。

#### `QFuture<T> &QFuture::operator=(const QFuture<T> &other)`

让当前句柄改为共享 `other` 的状态并返回自身引用。原来关联的状态不会因为这次赋值自动取消；其生命周期由其他 future 和生产者共同决定。

### 迭代器

#### `QFuture<T>::const_iterator QFuture::begin() const`

返回指向第一个结果的只读迭代器。结果尚未就绪时，后续解引用或推进可能等待。

#### `QFuture<T>::const_iterator QFuture::constBegin() const`

与 `begin()` 相同，显式表达只读遍历。

#### `QFuture<T>::const_iterator QFuture::constEnd() const`

返回末尾后的只读迭代器。用于和 `constBegin()` 配对。

#### `QFuture<T>::const_iterator QFuture::end() const`

返回末尾后的只读迭代器。用于 range-for 或和 `begin()` 配对。

### 状态查询

#### `bool QFuture::isCanceled() const`

返回是否已请求取消。返回 `true` 不代表后台线程已经停止；要等待最终收尾使用 `waitForFinished()`。

#### `bool QFuture::isFinished() const`

返回异步计算是否已经完成，包括已经取消但仍在收尾的计算在内，只有真正完成后才为 `true`。

#### `bool QFuture::isRunning() const`

返回当前是否正在运行。暂停请求中、已暂停、已完成和未启动状态都不应简单视为 running。

#### `bool QFuture::isStarted() const`

返回关联的异步计算是否已经启动。它不表示已经完成，也不表示已经有结果。

#### `[since 6.0] bool QFuture::isValid() const`

返回结果是否仍可从该 future 消费。它不检查结果是否就绪；`true` 也可能需要等待。`takeResult()` 后该 future 会失效。

#### `[since 6.0] bool QFuture::isSuspending() const`

返回是否已请求暂停但暂停尚未完全生效。此时仍可能有运行中的工作和后续结果。

#### `[since 6.0] bool QFuture::isSuspended() const`

返回暂停是否已经生效。生效后不应再期待新的结果或进度变化。

### 结果访问

#### `bool QFuture::isResultReadyAt(int index) const`

无阻塞检查指定索引的结果是否立即可取。调用前 future 必须有效；对尚未启动的 future，应先 `waitForFinished()`，否则文档标记为未定义行为。

#### `int QFuture::resultCount() const`

返回从索引 0 开始连续可用的结果数量。底层可能已经有更高索引的结果，因此它不是结果总数的可靠替代。

#### `T QFuture::result() const`

返回第一个结果，等价于 `resultAt(0)`。结果未就绪会阻塞，并返回内部结果的副本。move-only 类型或不想复制时使用 `takeResult()`。

无效 future 上调用它是未定义行为；`QFuture<void>` 没有此函数。

#### `T QFuture::resultAt(int index) const`

返回指定索引的结果。结果未就绪会阻塞；索引的可用性由生产者和结果集合决定，不要把“当前 `resultCount()` 较小”理解成所有更高索引都不存在。

#### `QList<T> QFuture::results() const`

等待并返回结果列表的副本。适合结果数量有限、结果类型可复制的场景。它不能直接解决 move-only 结果的整批提取问题；move-only 结果应使用只读迭代器逐项访问。

#### `[since 6.0] T QFuture::takeResult()`

等待并移动取出第一个结果，适合 move-only 类型或明确不想复制结果的场景。取出后 future 失效，后续访问结果属于未定义行为。

同一个共享 future 的结果只能由一个线程取出一次。不要把 `takeResult()` 当作可重复读取 API；需要共享读取时用 `result()` 或 `results()`。

### 进度

#### `int QFuture::progressMinimum() const`

返回进度范围下限。进度是否有意义取决于生产者是否报告了进度。

#### `int QFuture::progressMaximum() const`

返回进度范围上限。它不保证任务已经完成；完成状态应单独查询 `isFinished()`。

#### `int QFuture::progressValue() const`

返回当前进度值，通常位于最小值和最大值之间。GUI 展示应同时读取范围，而不要默认范围固定为 0 到 100。

#### `QString QFuture::progressText() const`

返回生产者报告的可选文本进度。很多计算不提供文本，因此空字符串是正常结果。

### 取消和暂停

#### `void QFuture::cancel()`

异步请求取消当前计算。已存在的结果仍可能读取，新结果不会再成为可用结果。并非所有生产者都支持取消。

#### `[since 6.10] void QFuture::cancelChain()`

取消尚未完成的 continuation 链，并触发其中适用的 `onCanceled()`。已完成阶段不受影响；已启动的嵌套 future 不会自动收到取消请求。

#### `[since 6.0] void QFuture::setSuspended(bool suspend)`

传入 `true` 请求暂停，传入 `false` 请求恢复。调用返回只表示请求已发出，不代表暂停已经完成；用 `isSuspended()` 或 watcher 的 `suspended()` 判断生效。

#### `[since 6.0] void QFuture::suspend()`

`setSuspended(true)` 的便捷形式。

#### `void QFuture::resume()`

`setSuspended(false)` 的便捷形式。

#### `[since 6.0] void QFuture::toggleSuspended()`

在运行、暂停请求中和已暂停之间切换。其判断逻辑等价于根据 `isSuspending()` 或 `isSuspended()` 决定是否恢复。

#### `[deprecated since 6.0] void QFuture::setPaused(bool paused)`

旧暂停 API。新代码使用 `setSuspended()`。

#### `[deprecated since 6.0] bool QFuture::isPaused() const`

旧暂停状态查询。新代码分别使用 `isSuspending()` 和 `isSuspended()`，因为新 API 能区分“请求中”和“已生效”。

#### `[deprecated since 6.0] void QFuture::pause()`

旧暂停便捷函数。新代码使用 `suspend()`。

#### `[deprecated since 6.0] void QFuture::togglePaused()`

旧暂停切换函数。新代码使用 `toggleSuspended()`。

### continuation 和错误处理

#### `QFuture<ResultType<Function>> QFuture::then(Function &&function)`

附加 continuation。默认使用 `QtFuture::Launch::Sync`，通常在前一步完成的线程运行；如果前一步已经完成，也可能在调用 `then()` 的线程立即运行。

有值 future 的回调可以接收 `T`，无值 future 的回调不接参数，也可以接收前一个 `QFuture<T>` 以自行处理多个结果或异常。回调返回值成为新 future 的结果；返回 `QFuture<U>` 时新 future 类型是嵌套的 `QFuture<QFuture<U>>`，可再用 `unwrap()`。

#### `[since 6.1] QFuture<ResultType<Function>> QFuture::then(QObject *context, Function &&function)`

在 context 所在线程执行 continuation。适合从后台计算回到 GUI 线程更新 QObject。context 销毁会取消该 continuation 链，但不会取消已经完成或之前正在执行的 future。

如果 future 已经完成，附加时机可能使后续无 context 的 continuation 改在线程中立即执行；线程归属重要时，后续每个步骤都显式传 context 或 launch policy。

#### `[since 6.0] QFuture<ResultType<Function>> QFuture::then(QThreadPool *pool, Function &&function)`

把 continuation 调度到指定线程池。它只约束该 continuation 的调度入口，不能推导出整个链或结果请求线程的绝对归属。

#### `[since 6.0] QFuture<ResultType<Function>> QFuture::then(QtFuture::Launch policy, Function &&function)`

按 `QtFuture::Launch` 策略执行 continuation。常见策略是：

- `Sync`：沿用同步执行语义；
- `Async`：在新线程中执行；
- `Inherit`：继承前一步的策略和线程池。

没有指定策略的 `then(function)` 使用 `Sync`。

#### `[since 6.0] QFuture<T> QFuture::onFailed(Function &&handler)`

为异常附加恢复处理器。处理器可无参数，或接收具体异常类型；返回值必须能构造当前 future 的 `T`。第一个匹配的处理器接管异常，不匹配则继续向后传播。

无 context 重载的执行线程取决于异常报告时机：可能是报告异常的线程，也可能是调用 `onFailed()` 的线程。

#### `[since 6.1] QFuture<T> QFuture::onFailed(QObject *context, Function &&handler)`

与无 context 版本相同，但在 context 所在线程运行处理器。context 必须在设置链时保持有效；销毁会使这段链取消。

#### `[since 6.0] QFuture<T> QFuture::onCanceled(Function &&handler)`

为取消附加恢复处理器。处理器无参数，返回当前 future 的 `T`；future 未取消时，返回 future 继续携带原结果。

处理器附加在取消之后时，可能立即在调用 `onCanceled()` 的线程执行。

#### `[since 6.1] QFuture<T> QFuture::onCanceled(QObject *context, Function &&handler)`

在 context 所在线程执行取消处理器。适合把取消状态转换成 UI 或业务对象可理解的恢复结果；同样要处理 context 的生命周期。

#### `[since 6.4] QFuture<U> QFuture::unwrap()`

展平 `QFuture<QFuture<U>>`，等待外层 future 产生内层 future，再等待内层 future 完成。内层结果、异常和取消状态会传给展平后的 future。多层嵌套时会继续展开到最内层。

`cancelChain()` 不会因为 `unwrap()` 自动取消已经启动的内层异步任务；需要时保存内层 future 并单独取消。

### 等待

#### `void QFuture::waitForFinished()`

阻塞当前线程，直到计算完成，包括已经请求取消但尚未收尾的计算。调用后可以安全地按完成状态读取结果，但它不会把无效 future 变成有效 future。

## API 速查表
| API | 作用 | 关键边界 |
|---|---|---|
| `QFuture()` | 构造 empty/canceled future | 不会启动任务，不要直接取结果 |
| `QFuture(other)` | 复制共享句柄 | 不复制计算，不产生独立状态 |
| `~QFuture()` | 销毁句柄 | 不等待、不取消 |
| `operator=` | 改为共享另一个状态 | 原状态不因赋值自动取消 |
| `begin()` / `end()` | STL 风格只读遍历 | 迭代可能阻塞；`void` 不支持 |
| `constBegin()` / `constEnd()` | 显式只读遍历 | 与上组语义相同 |
| `isStarted()` | 查询是否启动 | 不代表有结果 |
| `isRunning()` | 查询是否运行 | 暂停和完成需单独判断 |
| `isFinished()` | 查询是否完成 | 取消后可能仍为 false |
| `isCanceled()` | 查询是否请求取消 | 不代表线程已停止 |
| `isValid()` | 查询结果是否可消费 | 不代表结果已就绪 |
| `isResultReadyAt(i)` | 无阻塞检查某索引 | future 无效或未启动时有 UB 边界 |
| `resultCount()` | 连续可用结果数 | 不一定是底层结果总数 |
| `result()` | 读取第一个结果副本 | 未就绪会阻塞；`void` 无此 API |
| `resultAt(i)` | 读取指定结果副本 | 未就绪会阻塞 |
| `results()` | 读取全部结果副本 | 不适合直接提取 move-only |
| `takeResult()` | 移动取出第一个结果 | 取出后 future 失效，只能取一次 |
| `progressMinimum()` | 进度下限 | 由生产者报告 |
| `progressMaximum()` | 进度上限 | 不等于完成状态 |
| `progressValue()` | 当前进度 | 不保证每次变化都被观察 |
| `progressText()` | 文本进度 | 可能为空 |
| `cancel()` | 异步取消当前计算 | 生产者可能不支持 |
| `cancelChain()` | 取消未完成 continuation 链 | Qt 6.10；不传播到已启动内层 future |
| `setSuspended(bool)` | 请求暂停或恢复 | Qt 6.0；请求与生效分离 |
| `suspend()` / `resume()` | 暂停/恢复便捷函数 | 生产者必须支持 |
| `toggleSuspended()` | 切换暂停状态 | Qt 6.0 |
| `then(function)` | 链接下一步 | 默认 `Sync`，可能在当前线程执行 |
| `then(context, function)` | 在 context 线程执行 | Qt 6.1；context 销毁会取消链 |
| `then(pool, function)` | 在指定线程池调度 | Qt 6.0 |
| `then(policy, function)` | 按 launch 策略执行 | Qt 6.0；常用 `Async`、`Inherit` |
| `onFailed(handler)` | 处理异常 | Qt 6.0；不匹配继续传播 |
| `onFailed(context, handler)` | 在指定线程处理异常 | Qt 6.1 |
| `onCanceled(handler)` | 取消时返回恢复值 | Qt 6.0；处理器无参数 |
| `onCanceled(context, handler)` | 在指定线程处理取消 | Qt 6.1 |
| `unwrap()` | 展平嵌套 future | Qt 6.4；内层取消需单独关注 |
| `waitForFinished()` | 阻塞等待收尾 | GUI 线程慎用 |

## 11. 版本迁移提示

- Qt 6.0：`isValid()`、suspended API、continuation、异常和取消处理器可用；旧 paused API 开始弃用。
- Qt 6.1：`then(QObject *, ...)`、`onFailed(QObject *, ...)`、`onCanceled(QObject *, ...)` 可用。
- Qt 6.4：`unwrap()` 可用。
- Qt 6.10：`cancelChain()` 可用。
- 使用低于 Qt 6.0 的项目时，不能照搬本页的 continuation 和 suspended API。

## 12. 排查顺序

1. 先确认 future 是否来自真实生产者，而不是默认构造的 empty future。
2. 读取结果前检查 `isValid()`；需要无阻塞读取时检查 `isResultReadyAt()`。
3. 发现界面卡顿，搜索主线程中的 `result()`、`results()`、迭代器和 `waitForFinished()`。
4. 发现取消后线程仍在运行，确认生产者是否支持取消，再等待 `isFinished()`。
5. 发现暂停后仍有信号，区分 `isSuspending()` 和 `isSuspended()`，检查暂停请求发出时已经在途的工作。
6. 发现 continuation 在线程不对，显式传 `QObject *context`、`QThreadPool *` 或 `QtFuture::Launch`。
7. 发现异常没有被处理，确认项目启用了 C++ exceptions，并检查处理器类型是否匹配。
8. 发现 move-only 结果读取失败，改用 `takeResult()` 或只读迭代器，不要调用 `results()` 取整批副本。
