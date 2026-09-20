# Qt QPromise：手工生产 QFuture 的结果、进度与终结状态

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPromise>`  
> 所属模块：`Qt6::Core`  
> 类型性质：不可复制、可移动的 future 生产端  
> 关联类型：`QFuture<T>`、`QFutureWatcher<T>`、`QFutureInterface<T>`

## 1. 它解决什么问题

`QPromise<T>` 让代码手工驱动一个 `QFuture<T>` 的生命周期：生产端报告开始、逐步提交结果、更新进度、响应取消或暂停请求，最后报告完成。

```cpp
QPromise<int> promise;
QFuture<int> future = promise.future();

promise.start();
promise.addResult(42);
promise.finish();

Q_ASSERT(future.isFinished());
```

它适合：

- 自定义线程、回调型 API 或原生异步库需要桥接成 `QFuture`；
- 一个任务分批产生多个结果；
- 需要主动报告进度、异常、取消和暂停；
- 希望把生产端放到一个线程，把消费端放到 `QFutureWatcher` 所在线程。

它不是线程启动工具。`QPromise` 不会创建线程，也不会自动执行计算；调用者负责把 promise 移动或传入真正的异步工作环境。

## 2. 生产端与消费端模型

```text
QPromise<T>                     QFuture<T>
生产结果、进度和状态      <----> 读取结果、观察状态、请求取消/暂停
        │
        └─ future() 返回共享状态的 consumer handle
```

一个常见模式是主线程创建 promise/future，把 promise 移动给工作线程：

```cpp
QPromise<QString> promise;
QFuture<QString> future = promise.future();

auto *thread = QThread::create(
    [](QPromise<QString> promise, QString path) {
        promise.start();
        try {
            promise.addResult(readAndProcess(path));
        } catch (...) {
            promise.setException(std::current_exception());
        }
        promise.finish();
    },
    std::move(promise), path);

thread->start();
```

消费端可以把 `future` 交给 `QFutureWatcher` 或在非 GUI 的合适位置调用 `waitForFinished()`。不要在 GUI 线程用阻塞等待替代异步界面流程。

## 3. `start()`、`finish()` 和析构的终结语义

### 3.1 `start()`：报告工作已经开始

```cpp
promise.start();
```

它把共享 future 状态标记为已开始，供 observer 和 watcher 观察。应在真正开始生产结果前调用。

### 3.2 `finish()`：生产端明确结束

```cpp
promise.finish();
```

`finish()` 表示不会再提交新的结果。等待 `future.waitForFinished()` 的消费者可以继续，watcher 也可以收到完成状态。

每个正常生产路径都应保证结束：

```cpp
promise.start();
try {
    produceResults(promise);
} catch (...) {
    promise.setException(std::current_exception());
}
promise.finish();
```

在复杂控制流中，可用局部 scope guard 确保 `finish()`，但不要在 promise 已经移动走或工作未真正结束时过早 finish。

### 3.3 未完成 promise 的析构

Qt 6.11.1 中，如果 `QPromise` 析构时 future 状态尚未 finished，析构函数会取消并结束状态，以解除可能正在等待的消费者。

这是一种兜底终止，不是正常完成策略：

- 已生产的结果不应被误解为完整成功结果；
- 消费端会看到取消/结束相关状态；
- 任务线程仍可能继续做无用工作，除非工作本身协作检查取消；
- 生产端应显式调用 `finish()`，让成功、失败和取消边界清楚。

## 4. 结果生产

### 4.1 单个结果：`addResult()` 和 `emplaceResult()`

```cpp
promise.addResult(value);
promise.addResult(std::move(value));
promise.emplaceResult(arguments...);
```

默认把结果追加到下一个可用位置。`addResult()` / `emplaceResult()` 返回 `bool`：

- `true`：结果已被 future 接受；
- `false`：结果没有被接受，例如消费端已请求取消或共享状态不再接收结果。

返回 `false` 后不应继续假定该结果对消费者可见；长期任务通常把它与 `isCanceled()` 一起作为停止信号。

`T` 必须可移动构造，`QPromise<void>` 是无结果任务的特殊合法形式，不应调用结果提交 API。

### 4.2 指定结果索引

```cpp
promise.addResult(result, index);
promise.emplaceResultAt(index, args...);
```

指定 index 适合任务结果天然有固定槽位、并行子任务按编号归位的场景。调用者必须定义：

- 哪些 index 合法；
- 是否允许稀疏结果；
- 是否有多个生产者竞争同一 index；
- 消费端何时可以把结果集合视为完整。

不要把 index 当成“进度百分比”或线程编号。

### 4.3 批量结果：`addResults()`

```cpp
QList<Item> batch = makeBatch();
if (!promise.addResults(batch))
    return;
```

Qt 6.6 起可一次提交 `QList<T>`。它适合小到中等批量，减少逐项报告开销；很大的列表仍要考虑内存峰值、取消延迟和消费者处理能力。

## 5. 取消与暂停是协作式的

### 5.1 `isCanceled()`

消费者可以通过 `QFuture` 请求取消，生产端通过：

```cpp
if (promise.isCanceled())
    return;
```

检查请求。它不会自动停止线程、杀死 `run()`，也不会中断阻塞 I/O。任务本身必须定期检查并尽快返回，然后调用 `finish()`。

### 5.2 `suspendIfRequested()`

```cpp
for (const Item &item : items) {
    if (promise.isCanceled())
        break;

    promise.addResult(process(item));
    promise.suspendIfRequested();
}
promise.finish();
```

当消费端请求暂停时，`suspendIfRequested()` 会在生产端的调用点等待恢复或取消。因此它只能放在：

- 工作线程；
- 可安全暂停的位置；
- 不持有 mutex、文件锁、数据库事务或其他稀缺资源的位置。

不要在 GUI 线程调用它，也不要在持锁状态下调用，否则暂停可能把其他线程永久堵在该锁上。

取消请求会使暂停等待能够结束，生产端仍应在后续检查 `isCanceled()`。

## 6. 进度报告

```cpp
promise.setProgressRange(0, total);
for (int i = 0; i < total; ++i) {
    process(i);
    promise.setProgressValue(i + 1);
}
```

可用 API：

- `setProgressRange(minimum, maximum)`：定义进度范围；
- `setProgressValue(value)`：更新数值；
- `setProgressValueAndText(value, text)`：同时更新数值和显示文字。

进度是面向 consumer/watcher 的状态报告，不会调度工作，也不验证业务完成度。更新频率过高会增加同步和 UI 通知负担；例如处理百万项时，按批次或时间间隔报告更合适。

范围、数值和文本应由同一个生产协议维护。不要在多个无同步的生产线程随意写同一个 promise 的进度，除非已明确规定聚合方式。

## 7. 异常报告

在启用 C++ exceptions 的 Qt 构建中，可以报告：

```cpp
try {
    promise.addResult(compute());
} catch (const QException &exception) {
    promise.setException(exception);
} catch (...) {
    promise.setException(std::current_exception());
}
promise.finish();
```

支持：

- `setException(const QException &)`;
- `setException(std::exception_ptr)`。

异常 API 在 `QT_NO_EXCEPTIONS` 构建中不可用。无论是否使用异常，仍需调用 `finish()` 结束生产状态。消费端读取结果时需要按 QFuture 的异常传播规则处理，不要假设只要 `isFinished()` 就代表计算成功。

## 8. 移动语义和所有权

`QPromise<T>` 不可复制、可移动：

```cpp
QPromise<Result> promise;
QFuture<Result> future = promise.future();

startWorker(std::move(promise));
```

这是为了明确一个共享 future 状态的生产责任。移动后，源 promise 只能析构或重新赋值，不能继续 `addResult()`、`finish()` 或查询状态。

`future()` 返回的是可复制的消费端 handle。生产端可以在 `start()` 前取得 future 并交给 watcher；但 consumer 的逻辑应正确处理尚未开始、正在运行、取消和已完成状态。

## 9. 线程安全和多生产者边界

QPromise 的共享 future 状态支持跨线程生产/消费，但这不等于“任意多个生产者可以不经设计地同时写同一个 promise”。

实践上应让一个明确的生产协调者负责：

- 调用 `start()` 和 `finish()`；
- 定义结果 index 分配；
- 聚合进度；
- 处理异常和取消；
- 保证 promise 生命周期覆盖所有生产动作。

若多个线程要共同产生结果，使用原子索引、mutex 或任务汇聚器分配工作，并确保最后一个生产者才 `finish()`。不要让多个线程竞相 finish，也不要让一个线程析构 promise 时另一个线程仍在使用它。

## 10. 常见使用场景

### 10.1 将回调 API 转为 QFuture

```cpp
QFuture<QByteArray> loadAsync(Client *client, QString key)
{
    QPromise<QByteArray> promise;
    QFuture<QByteArray> future = promise.future();

    promise.start();
    client->load(key, [promise = std::move(promise)]
                 (QByteArray data, QString error) mutable {
        if (!error.isEmpty()) {
            // 按项目错误模型报告错误。
        } else {
            promise.addResult(std::move(data));
        }
        promise.finish();
    });

    return future;
}
```

这里回调必须保证只调用一次，且 promise 移动捕获后的生命周期覆盖回调调用时间。若 client 的回调可能来自任意线程，consumer 应通过 watcher/context 回到正确线程。

### 10.2 分批结果与可取消循环

```cpp
void scanFiles(QPromise<FileInfo> promise, QStringList paths)
{
    promise.start();
    promise.setProgressRange(0, paths.size());

    for (qsizetype i = 0; i < paths.size(); ++i) {
        if (promise.isCanceled())
            break;

        promise.addResult(inspect(paths.at(i)));
        promise.setProgressValue(i + 1);
        promise.suspendIfRequested();
    }

    promise.finish();
}
```

### 10.3 无结果任务

```cpp
void warmCache(QPromise<void> promise)
{
    promise.start();
    prepareCache();
    promise.finish();
}
```

`QPromise<void>` 用于只关心完成、取消、进度或异常的 future；不要试图调用 `addResult()`。

## 11. 常见错误

### 11.1 忘记调用 `finish()`

消费者可能永久等待。析构虽会兜底取消并结束，但这会把正常成功路径变成取消式终结。

### 11.2 以为 cancel 会强制停止线程

取消只是请求。生产端必须检查 `isCanceled()`，并让阻塞 I/O、子任务或外部库也有自己的取消协议。

### 11.3 在持锁状态调用 `suspendIfRequested()`

暂停点可能长时间等待，持有锁会阻塞其他线程甚至形成死锁。先释放不必要资源。

### 11.4 `addResult()` 返回 false 仍继续生产

这通常表明消费者已不再接收结果或状态已改变。应停止或调整工作，而不是继续无界计算。

### 11.5 移动 promise 后继续使用源对象

移动后的源对象不再拥有生产责任。只使用接收方。

### 11.6 多线程无协调地调用 `finish()`

完成边界会变得不可预测。指定一个协调者或最后完成者。

### 11.7 在 GUI 线程 `waitForFinished()`

会阻塞事件循环，进度、watcher 甚至任务回传可能无法及时处理。使用 `QFutureWatcher` 或 continuation。

## 12. 逐项 API 语义

### `QPromise()`

创建一个尚未开始的 promise。它不启动线程，也不自动开始计算。

### `QPromise(QPromise &&other)`

移动共享 future 状态和生产责任。源对象移动后只能析构或重新赋值。

### `QPromise(const QFutureInterface<T> &other)`

从已有 `QFutureInterface<T>` 建立 promise。它主要服务于 Qt future 基础设施集成；普通应用更常用默认构造 promise 后调用 `future()`。

### `QPromise(QFutureInterface<T> &&other)`

移动接管已有 future interface。用于底层集成代码；调用方需确保 interface 的生命周期和状态协议正确。

### `~QPromise()`

若状态尚未 finished，取消并结束共享 future 状态，解除潜在等待；随后清理 continuation。正常路径仍应显式 `finish()`。

### `operator=(QPromise &&other)`

移动赋值，接管 other 的生产状态。当前对象原先未完成的状态会按其生命周期终结规则处理；移动后 other 不应继续使用。

### `swap(QPromise &other)`

交换两个 promise 的共享 future 状态。不会启动、结束或取消任一计算，仅交换生产端句柄。

### `future() const`

返回关联的 `QFuture<T>` 消费端 handle。future 可在 promise 运行期间读取结果、观察进度、请求取消或暂停。

### `start()`

报告计算已开始。应在开始生产结果前调用。

### `finish()`

报告计算已经结束，不再接受新的正常生产结果。应保证每条生产路径都抵达 finish。

### `addResult(U &&result, int index = -1)`

添加一个可转换为 `T` 的结果；默认追加，指定 index 时放入对应位置。返回是否被共享 future 状态接受。

### `emplaceResult(Args &&...args)`

原地构造并追加一个 `T` 结果。返回是否被接受。

### `emplaceResultAt(int index, Args &&...args)`

Qt 6.6 起，在指定结果 index 原地构造 `T`。调用方负责 index 规则和并发协调。

### `addResults(const QList<T> &results)`

Qt 6.6 起批量报告结果。返回是否被接受；注意批量大小和内存峰值。

### `isCanceled() const`

查询消费端是否请求取消。它不强制终止工作，生产端应协作停止。

### `suspendIfRequested()`

若请求暂停则阻塞当前生产线程，直到恢复或取消。只能放在无锁、可安全暂停的位置。

### `setProgressRange(int minimum, int maximum)`

设置进度范围。它只是报告约定，调用者负责保持范围和数值合理。

### `setProgressValue(int progressValue)`

更新进度数值。高频循环中应节流，避免通知过多。

### `setProgressValueAndText(int progressValue, const QString &progressText)`

同时更新进度数值和文本，适合 watcher/UI 显示阶段名称。

### `setException(const QException &)` / `setException(std::exception_ptr)`

在异常支持开启时报告异常给 future 消费端。报告后仍应结束 promise；异常不应从 `run()` 或回调线程栈直接逃出。

### `swap(QPromise<T> &, QPromise<T> &)`

非成员交换函数，调用成员 `swap()`，适合泛型代码。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QPromise()` | 创建尚未开始的生产端。 | 不创建线程；需显式 `start()` / `finish()`。 |
| 移动 | `QPromise(QPromise &&)` | 转移生产责任。 | 不可复制；源对象移动后不可继续生产。 |
| 底层集成 | `QPromise(QFutureInterface<T>)` | 从 future interface 构建生产端。 | 主要用于 Qt future 基础设施，普通代码较少需要。 |
| 生命周期 | `~QPromise()` | 终结未完成状态。 | 未 finish 时会取消并结束，正常路径仍显式 finish。 |
| 赋值交换 | `operator=(QPromise &&)` / `swap()` | 移动或交换生产端状态。 | 交换不启动或结束任务；不要让多个线程失去完成协调。 |
| 消费端 | `future()` | 返回关联 `QFuture<T>`。 | future 可复制并交给 watcher；不要在 GUI 线程盲目等待。 |
| 状态 | `start()` | 报告开始。 | 应在产生结果前调用。 |
| 状态 | `finish()` | 报告结束。 | 每条生产路径都应结束；结束后不再生产。 |
| 结果 | `addResult(result, index)` | 添加一个结果。 | 返回 false 时结果未被接受；index 需由业务定义。 |
| 结果 | `emplaceResult(...)` | 原地构造并追加结果。 | `T` 必须能由参数构造。 |
| 结果 | `emplaceResultAt(index, ...)` | 在指定位置原地构造结果。 | Qt 6.6 起；多生产者必须协调 index。 |
| 结果 | `addResults(QList<T>)` | 批量添加结果。 | Qt 6.6 起；控制批量大小避免内存和取消延迟。 |
| 取消 | `isCanceled()` | 查询是否请求协作取消。 | 不会强杀线程，生产端主动停止。 |
| 暂停 | `suspendIfRequested()` | 在请求暂停时阻塞生产端。 | 不要持锁或占用稀缺资源时调用。 |
| 进度 | `setProgressRange()` | 设置进度范围。 | 不验证业务含义，生产端保持一致性。 |
| 进度 | `setProgressValue()` | 更新进度值。 | 高频更新需节流。 |
| 进度 | `setProgressValueAndText()` | 更新进度值和文字。 | 文字可能到达 UI，避免高频大字符串。 |
| 异常 | `setException(...)` | 报告异常。 | 仅 exceptions 启用时可用；仍要 `finish()`。 |

## 14. 一句话总结

`QPromise<T>` 是 `QFuture<T>` 的生产端：显式开始、提交结果/进度、协作响应取消和暂停、最后 finish。它不启动线程，不会强制取消任务；未完成即析构会取消并结束，因此真正可靠的代码要让生产责任、结果索引、取消检查和完成边界都清清楚楚。
