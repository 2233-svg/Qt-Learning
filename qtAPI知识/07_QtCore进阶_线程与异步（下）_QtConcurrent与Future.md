# Qt Core 进阶：线程与异步（下）——Qt Concurrent 与 Future

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Core、Qt Concurrent  
> 核心类型：`QFuture`、`QFutureWatcher`、`QPromise`、`QtConcurrent`  
> 前置知识：线程归属、排队信号槽、线程池和协作式取消。

## 1. 从“管理线程”提升到“管理任务”

很多业务并不关心任务究竟由哪个线程执行，只关心：

- 如何提交计算；
- 何时完成；
- 如何取得结果；
- 如何报告进度；
- 如何处理失败和取消；
- 如何把后续步骤串起来。

这时直接管理 `QThread` 过于底层。Qt Concurrent 和 Future 体系提供了更高层模型：

```text
生产端                                  消费端
函数 / QtConcurrent / QPromise
        │ 写入状态、结果、进度
        ▼
     共享异步状态  <────────────────>  QFuture<T>
                                          │
                         ┌────────────────┼───────────────┐
                         ▼                ▼               ▼
                   result()          then()       QFutureWatcher
```

`QFuture<T>` 不是线程，而是异步计算状态的只读句柄。

## 2. 构建与头文件

Qt Concurrent 是独立模块，需要显式链接。

### 2.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Concurrent)
target_link_libraries(mytarget PRIVATE Qt6::Core Qt6::Concurrent)
```

### 2.2 常用头文件

```cpp
#include <QtConcurrentRun>
#include <QtConcurrentMap>
#include <QtConcurrentFilter>
#include <QFuture>
#include <QFutureWatcher>
#include <QPromise>
```

也可以包含聚合头：

```cpp
#include <QtConcurrent>
```

但精确头文件可减少编译依赖。

## 3. QtConcurrent::run：最小异步函数

### 3.1 最小可用代码

```cpp
#include <QCoreApplication>
#include <QDebug>
#include <QFutureWatcher>
#include <QtConcurrentRun>

int calculate(int a, int b)
{
    return a + b;
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QFutureWatcher<int> watcher;
    QObject::connect(&watcher, &QFutureWatcher<int>::finished,
                     &app, [&] {
        qDebug() << watcher.result();
        app.quit();
    });

    watcher.setFuture(QtConcurrent::run(calculate, 20, 22));
    return app.exec();
}
```

`QtConcurrent::run()` 立即返回 `QFuture<int>`，计算通常在线程池中执行。`QFutureWatcher` 把完成状态转换为 Qt 信号，因此主线程不需要阻塞等待。

### 3.2 使用 lambda

```cpp
const QString path = selectedPath;

QFuture<QByteArray> future = QtConcurrent::run([path] {
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly))
        return QByteArray{};
    return file.readAll();
});
```

异步 lambda 优先按值捕获。按引用捕获局部变量时，任务执行前局部变量可能已经销毁。

### 3.3 调用成员函数

可以用 lambda 明确表达对象和参数：

```cpp
QPointer<Parser> parser = parser_;

auto future = QtConcurrent::run([parser, bytes] {
    if (!parser)
        return ParseResult{};
    return parser->parse(bytes);
});
```

但 `QPointer` 只检测 `QObject` 是否已销毁，不会让对象的方法自动线程安全。若 `parse()` 会访问该对象的其他可变状态，仍需同步或改为无状态函数。

## 4. QFuture 的状态

常见查询：

```cpp
future.isStarted();
future.isRunning();
future.isFinished();
future.isCanceled();
future.isSuspending();
future.isSuspended();
future.isValid();
```

状态会随生产端推进而变化。Future 可以复制，多个句柄引用同一异步计算状态。

```cpp
QFuture<int> a = QtConcurrent::run([] { return 42; });
QFuture<int> b = a; // 共享状态，不是重复执行任务
```

## 5. 取得结果：小心隐式阻塞

### 5.1 result

```cpp
int value = future.result();
```

如果第一个结果尚未可用，`result()` 会阻塞当前线程。主线程中过早调用它，会冻结界面。

错误模式：

```cpp
auto future = QtConcurrent::run(slowFunction);
ui->label->setText(QString::number(future.result())); // 立刻阻塞
```

正确方向：使用 `QFutureWatcher::finished` 或 `then(this, ...)`。

### 5.2 resultAt 与 results

支持多结果的 Future 可读取指定项或全部结果：

```cpp
T first = future.resultAt(0);
QList<T> all = future.results();
```

对应结果尚未出现时也可能阻塞。`resultCount()` 表示当前连续可用结果的数量，不应把“当前数量”误当成最终数量。

### 5.3 takeResult

```cpp
std::unique_ptr<Data> data = future.takeResult();
```

`takeResult()` 将第一个结果移出，支持移动专用类型。它假定只有一个消费者执行一次移动；取走后 Future 不应再用于常规结果访问。共享给多个读取者时使用可复制结果和 `result()`。

## 6. QFutureWatcher：把状态转成信号

`QFutureWatcher<T>` 是 `QObject`，可监控 Future 并发出：

- `started()`；
- `finished()`；
- `canceled()`；
- `progressRangeChanged()`；
- `progressValueChanged()`；
- `progressTextChanged()`；
- `resultReadyAt()`；
- `resultsReadyAt()`；
- `suspending()`、`suspended()`、`resumed()`。

### 6.1 建立连接后再 setFuture

```cpp
auto *watcher = new QFutureWatcher<Result>(this);

connect(watcher, &QFutureWatcher<Result>::finished,
        this, [this, watcher] {
    const Result result = watcher->result();
    showResult(result);
    watcher->deleteLater();
});

watcher->setFuture(QtConcurrent::run(buildResult));
```

先连接再设置 Future，生命周期和通知顺序最清楚。

### 6.2 进度绑定

```cpp
connect(watcher, &QFutureWatcher<void>::progressRangeChanged,
        ui->progressBar, &QProgressBar::setRange);
connect(watcher, &QFutureWatcher<void>::progressValueChanged,
        ui->progressBar, &QProgressBar::setValue);
```

不是所有异步计算都会报告进度。基础模式 `QtConcurrent::run()` 只返回一个结果，不会自动知道函数内部做到了百分之几。

### 6.3 结果背压

多结果生产速度高于界面消费速度时，可限制待处理结果：

```cpp
watcher->setPendingResultsLimit(32);
```

待处理通知超过上限时，相关计算会被节流，避免事件队列和内存无限增长。

## 7. Future 的取消不是强制终止

```cpp
future.cancel();
```

调用取消只是请求异步计算停止。能否响应取决于生产者实现。

必须区分：

- 基础模式 `QtConcurrent::run()` 返回的 Future 不能取消正在执行的函数；
- `mappedReduced()` 等部分 Qt Concurrent 算法支持取消；
- Promise 模式函数主动检查 `isCanceled()` 时可协作取消；
- 已经产生的结果在取消后仍可能读取；
- `isCanceled()` 为真时，底层计算不一定已经完全停止。

`QFutureWatcher::cancel()` 也是把取消请求转发给所监控的 Future，不是强杀线程。

## 8. 暂停与恢复同样需要生产端配合

调用端：

```cpp
future.suspend();
future.resume();
future.toggleSuspended();
```

只有支持暂停的计算才会响应。Promise 生产者需要在合适的检查点调用：

```cpp
promise.suspendIfRequested();
```

该调用在暂停生效时让工作线程通过条件变量休眠，不是忙等待。任务应选在一致状态下设置检查点，避免暂停时持有长期占用的业务锁或外部资源。

## 9. QtConcurrent::run 的 Promise 模式

基础模式函数只能返回单个结果：

```cpp
QFuture<int> future = QtConcurrent::run([] {
    return calculateOneValue();
});
```

Promise 模式允许多结果、进度、暂停和取消。函数的第一个参数必须是 `QPromise<T> &`，并返回 `void`：

```cpp
void produceSquares(QPromise<int> &promise, int count)
{
    promise.setProgressRange(0, count);

    for (int i = 0; i < count; ++i) {
        promise.suspendIfRequested();
        if (promise.isCanceled())
            return;

        promise.addResult(i * i);
        promise.setProgressValue(i + 1);
    }
}

QFuture<int> future =
    QtConcurrent::run(produceSquares, 100);
```

在这种模式下，`QtConcurrent::run()` 自动调用 Promise 的 `start()` 和 `finish()`，函数内部不要重复调用。

### 9.1 监控多个结果

```cpp
auto *watcher = new QFutureWatcher<int>(this);

connect(watcher, &QFutureWatcher<int>::resultReadyAt,
        this, [watcher](int index) {
    qDebug() << index << watcher->resultAt(index);
});

watcher->setFuture(QtConcurrent::run(produceSquares, 100));
```

结果可能按生产端定义的索引出现。消费端应明确是否依赖顺序。

## 10. 直接使用 QPromise

当异步生产者不是 Qt Concurrent，或需要自行控制完成时机，可手动建立 Promise/Future 对。

### 10.1 最小生产者示例

```cpp
QPromise<int> promise;
QFuture<int> future = promise.future();

QThread *thread = QThread::create(
    [promise = std::move(promise)]() mutable {
        promise.start();
        promise.setProgressRange(0, 10);

        for (int i = 0; i < 10; ++i) {
            promise.suspendIfRequested();
            if (promise.isCanceled())
                break;

            promise.addResult(i * i);
            promise.setProgressValue(i + 1);
        }

        promise.finish();
    });

QObject::connect(thread, &QThread::finished,
                 thread, &QObject::deleteLater);
thread->start();
```

手动使用时必须遵守：

1. 先通过 `future()` 取得消费句柄；
2. 把 Promise 移交给唯一生产者；
3. 调用 `start()`；
4. 添加结果和进度；
5. 无论正常、取消或错误路径都确保 `finish()`。

`QPromise` 是移动专用对象，不能复制。所有权模型因此更明确：一个生产者推进状态，多个 Future 句柄可以观察。

### 10.2 结果索引

```cpp
promise.addResult(value);          // 自动使用后续索引
promise.addResult(value, index);   // 指定索引
promise.addResults(values);        // 批量添加
```

结果索引需要连续，Future 的结果迭代和 `resultCount()` 才容易理解。除非业务确实要求，不要随意制造索引空洞。

## 11. then：把异步步骤串起来

Qt 6 的 `QFuture::then()` 创建后续 Future：

```cpp
auto finalFuture = QtConcurrent::run([] {
    return loadText();
}).then([](QString text) {
    return parse(text);
}).then([](Document document) {
    return summarize(document);
});
```

每一步的返回值成为下一步参数。相比在多层回调中手动传递结果，链式结构更接近业务流程。

### 11.1 默认在哪个线程执行

默认 continuation 通常在完成前一步的同一线程运行。如果 Future 在附加 `then()` 前已经完成，continuation 还可能立即在调用 `then()` 的线程执行。

因此，凡是对线程位置有要求，都应显式指定。

### 11.2 在主线程更新界面

把主线程中的 `QObject` 作为上下文：

```cpp
QtConcurrent::run(loadReport)
    .then(this, [this](Report report) {
        ui->reportView->setReport(report);
    });
```

continuation 会在 `this` 所属线程执行；如果上下文对象在执行前销毁，后续调用会被取消，避免访问悬空界面。

### 11.3 指定线程池

```cpp
future.then(&customPool, [](Result result) {
    return postProcess(result);
});
```

这适合把某类计算隔离到专用线程池。

### 11.4 指定启动策略

```cpp
future.then(QtFuture::Launch::Async, [](Result result) {
    return postProcess(result);
});
```

`QtFuture::Launch::Inherit` 可继承前一个 continuation 的策略。线程位置与调度时机属于正确性条件时，显式上下文通常比依赖默认策略更清楚。

## 12. 多结果 Future 的 continuation

如果前一步产生多个结果，而 continuation 只接收 `T`，它只处理单个值语义。需要访问全部结果时，让 continuation 接收 `QFuture<T>`：

```cpp
QtConcurrent::mapped(values, transform)
    .then([](QFuture<int> mappedFuture) {
        return mappedFuture.results();
    });
```

这在 `mapped()`、`filtered()` 和 Promise 多结果任务中尤其重要。

## 13. 嵌套 Future 与 unwrap

某个 continuation 自己返回 Future 时，会形成：

```cpp
QFuture<QFuture<Result>> nested;
```

调用 `unwrap()` 可扁平化：

```cpp
auto finalFuture = firstFuture
    .then([](Input input) {
        return startAnotherAsyncOperation(input);
    })
    .unwrap();
```

Qt 6.4 起，`unwrap()` 会沿嵌套层级取得内部 Future 的最终结果；内部取消或异常也会传播到扁平后的 Future。

## 14. 异常与 onFailed

异步函数抛出的异常会存入 Future，并在取结果或 continuation 中传播。可添加失败处理：

```cpp
QtConcurrent::run([]() -> Data {
    throw std::runtime_error("load failed");
}).then([](Data data) {
    return transform(data);
}).onFailed([](const std::exception &e) {
    qWarning() << e.what();
    return Data{};
});
```

处理器返回与链条兼容的值，可以把失败恢复为正常结果。

### 14.1 GUI 错误处理也要指定上下文

```cpp
future.onFailed(this, [this](const std::exception &e) {
    QMessageBox::critical(this, tr("错误"),
                          QString::fromUtf8(e.what()));
    return Result{};
});
```

不传上下文时，错误处理器可能在工作线程执行，不能直接使用 Widgets。

### 14.2 异常类型匹配

可设置多个不同参数类型的 `onFailed()`。类型匹配失败的异常会继续沿链传播。最后应有能够处理预期异常或通用错误的边界。

## 15. onCanceled 与取消链

```cpp
future.onCanceled([] {
    return Result{};
});
```

`onCanceled()` 在上游 Future 取消时提供恢复值或清理逻辑。

取消某一个 Future 不应被想当然地理解为整个 continuation 链都按业务期望停止。Qt 6.10 起可使用 `cancelChain()` 请求取消整条 continuation 链：

```cpp
finalFuture.cancelChain();
```

前提仍然是具体生产者支持取消。取消是状态传播协议，不是线程强制终止。

## 16. map、mapped 与 mappedReduced

### 16.1 map：原地修改

```cpp
QList<int> values{1, 2, 3, 4};
QFuture<void> future = QtConcurrent::map(values, [](int &value) {
    value *= 2;
});
```

任务完成前不要从其他线程读写 `values`。

### 16.2 mapped：生成新结果序列

```cpp
QList<int> values{1, 2, 3, 4};
QFuture<int> future = QtConcurrent::mapped(values, [](int value) {
    return value * value;
});
```

输入保持不变，Future 提供多个变换结果。

### 16.3 mappedReduced：映射后汇总

```cpp
auto lengths = [](const QString &text) {
    return text.size();
};

auto sum = [](int &total, int length) {
    total += length;
};

QFuture<int> total =
    QtConcurrent::mappedReduced<int>(words, lengths, sum);
```

map 阶段可以并行。reduce 函数由 Qt 保证不会被多个线程同时调用，因此通常不需要再为聚合值加互斥锁。

### 16.4 归约顺序

- `UnorderedReduce`：默认，归约顺序未定义；
- `OrderedReduce`：按原序列顺序归约；
- `SequentialReduce`：归约串行执行。

浮点加法、字符串拼接等对顺序敏感的运算，应明确选择选项。即使数学上看似可交换，浮点舍入也可能让不同顺序产生略微不同的结果。

## 17. filter、filtered 与 filteredReduced

```cpp
QList<int> values{1, 2, 3, 4, 5};

// 原地移除不满足条件的元素
QFuture<void> a = QtConcurrent::filter(values, [](int value) {
    return value % 2 == 0;
});

// 返回新的多结果 Future，输入不变
QFuture<int> b = QtConcurrent::filtered(values, [](int value) {
    return value > 2;
});
```

`filteredReduced()` 则把保留下来的元素进一步汇总为单个结果。

## 18. blocking 版本何时使用

Qt Concurrent 提供 `blockingMap()`、`blockingMapped()`、`blockingFiltered()` 等同步版本。

```cpp
QList<int> squares =
    QtConcurrent::blockingMapped(values, square);
```

它们会等所有工作完成再返回。适合：

- 命令行工具的顶层流程；
- 已经位于后台线程的同步步骤；
- 测试代码；
- 程序关闭前明确的批处理。

不要在 GUI 主线程的交互槽中使用，否则界面仍会冻结。并行执行不自动意味着调用者异步。

## 19. 自定义线程池

Qt Concurrent 重载通常允许传入 `QThreadPool *`：

```cpp
QThreadPool ioPool;
ioPool.setMaxThreadCount(4);

QFuture<Data> future = QtConcurrent::run(&ioPool, loadData);
```

使用独立池的理由包括：

- 防止某类长任务占满全局池；
- 为库提供可配置的执行资源；
- 对不同工作负载设置不同并发度。

线程池必须比所有使用它的 Future 和任务活得更久。

## 20. 参数复制、移动与生命周期

`QtConcurrent::run()` 会在调用点保存函数和参数，之后在线程池执行。仍需明确值语义：

```cpp
QString text = editor->toPlainText();
auto future = QtConcurrent::run([text = std::move(text)] {
    return parse(text);
});
```

不要捕获：

- 即将离开作用域的局部引用；
- 未受保护且会被其他线程修改的容器引用；
- 生命周期短于任务的裸指针；
- 工作函数无权跨线程访问的 `QObject` 或 GUI 对象。

跨线程任务输入最好是不可变值，输出是独立结果值。

## 21. 结构化异步错误模型

建议业务结果区分三种结束状态：

```text
成功：产生有效结果
失败：发生可说明的错误
取消：用户或上层不再需要结果
```

不要把取消记录成错误，也不要用空字符串或空容器同时表示“合法空结果”和“失败”。可使用：

- Future 的异常传播；
- 自定义 `Result<T, Error>` 风格类型；
- `std::optional<T>` 表示只有“有/无”两态的场景；
- 单独的状态枚举和错误消息。

## 22. Future 链的生命周期

仅创建 continuation 却不保存末端 Future，任务通常仍可运行，但调用方失去：

- 等待最终完成的能力；
- 获取最终结果的能力；
- 观察最终异常的能力；
- 对链执行取消的句柄。

重要任务应保存末端 Future 或由 Watcher 监控：

```cpp
finalFuture_ = startTask()
    .then(transform)
    .then(this, [this](Result result) {
        present(result);
        return result;
    });
```

需要同时运行多个请求时，不要只用一个成员 Future 覆盖旧句柄；可按任务 ID 管理或让每个 Watcher 自管理到完成。

## 23. 避免过度并行

Qt Concurrent 会使用线程池，但任务仍可能争夺：

- CPU 缓存；
- 内存带宽；
- 磁盘；
- 数据库连接；
- 网络服务配额；
- 全局互斥锁。

如果每个并行任务最终都在等待同一把锁，增加线程只会增加调度成本。性能优化应测量吞吐、延迟、CPU 使用率和内存，而不是只比较线程数量。

## 24. 常见错误与修复

### 24.1 主线程立刻调用 result

**错误**：提交任务后立即 `future.result()`。

**后果**：主线程阻塞，异步失去意义。

**修复**：Watcher 或带主线程上下文的 continuation。

### 24.2 认为基础 run 可以取消

**错误**：对基础 `QtConcurrent::run()` 调用 `cancel()` 后认为函数停止。

**修复**：使用 Promise 模式并检查取消，或自己设计原子停止标记。

### 24.3 continuation 直接更新 UI

**错误**：未指定上下文就访问 Widget。

**修复**：使用 `.then(this, ...)`，其中 `this` 属于 GUI 线程。

### 24.4 忘记 Promise finish

**错误**：手动 Promise 在提前返回路径没有 `finish()`。

**后果**：Future 永远不进入完成状态。

**修复**：集中结束路径或使用作用域守卫；若使用 `QtConcurrent::run()` Promise 模式，则由它自动 start/finish。

### 24.5 捕获 this 后对象先销毁

**修复**：复制任务输入；回调使用 QObject 上下文或 `QPointer`；所有者析构时执行取消并管理收尾。

### 24.6 对多结果 Future 只处理一个值

**修复**：continuation 接收 `QFuture<T>` 并读取 `results()`，或使用 Watcher 的逐结果信号。

### 24.7 在主线程调用 waitForFinished

它和 `result()` 一样可能阻塞事件循环。只在明确允许同步等待的非交互路径使用。

## 25. 选择指南

| 需求 | 推荐 API |
|---|---|
| 异步执行一个返回值函数 | `QtConcurrent::run()` 基础模式 |
| 多结果、进度、暂停、取消 | `QtConcurrent::run()` Promise 模式 |
| 自定义异步生产者 | `QPromise<T>` |
| 把结果接入信号槽 | `QFutureWatcher<T>` |
| 串行组合异步步骤 | `QFuture::then()` |
| GUI 线程处理后续步骤 | `then(context, function)` |
| 处理异常 | `onFailed()` |
| 处理取消 | `onCanceled()` |
| 并行转换容器 | `mapped()` |
| 并行筛选容器 | `filtered()` |
| 并行计算后汇总 | `mappedReduced()` / `filteredReduced()` |
| 同步批处理 | `blocking...` 系列，避免 GUI 主线程 |

## 26. API 速查表

| API | 作用 | 关键注意点 |
|---|---|---|
| `QtConcurrent::run()` | 在线程池执行函数 | 基础模式不可取消正在运行的函数 |
| `QFuture::result()` | 复制第一个结果 | 结果未就绪时阻塞 |
| `QFuture::takeResult()` | 移出第一个结果 | 单消费者、只取一次 |
| `QFuture::results()` | 获取全部结果 | 可能阻塞且需要可复制类型 |
| `QFuture::then()` | 添加 continuation | 对线程有要求时显式指定上下文 |
| `QFuture::onFailed()` | 处理异常 | GUI 操作传 context |
| `QFuture::onCanceled()` | 处理取消 | 不等于强制停止生产者 |
| `QFuture::unwrap()` | 扁平化嵌套 Future | Qt 6.4 起 |
| `QFuture::cancelChain()` | 请求取消 continuation 链 | Qt 6.10 起，仍需生产者支持 |
| `QFutureWatcher::setFuture()` | 开始监控 | 先 connect 再调用 |
| `setPendingResultsLimit()` | 限制待处理结果 | 提供背压 |
| `QPromise::addResult()` | 发布一个结果 | Promise 由单一生产者拥有 |
| `QPromise::setProgressValue()` | 发布进度 | 先设置合理范围 |
| `suspendIfRequested()` | 响应暂停 | 生产者主动设置检查点 |
| `isCanceled()` | 检查取消 | 生产者主动结束 |

## 27. 自测题

### 题 1：QFuture 是线程吗

<details>
<summary>答案</summary>

不是。它是共享异步状态的观察句柄。实际执行可能来自线程池、自定义线程，甚至其他异步生产者。

</details>

### 题 2：result 为什么会卡界面

<details>
<summary>答案</summary>

结果尚未就绪时 `result()` 会同步等待。若从 GUI 主线程调用，事件循环无法继续处理输入和重绘。应使用 Watcher 或 continuation。

</details>

### 题 3：基础 run 能否取消

<details>
<summary>答案</summary>

不能通过 Future 停止已经运行的基础模式函数。需要 Promise 模式主动检查取消，或由业务函数使用其他协作式停止机制。

</details>

### 题 4：如何保证 then 在主线程执行

<details>
<summary>答案</summary>

调用 `future.then(context, function)`，并传入属于主线程的 `QObject`，例如窗口的 `this`。

</details>

### 题 5：Promise 模式是否手动 start/finish

<details>
<summary>答案</summary>

通过 `QtConcurrent::run()` 使用 Promise 模式时不需要，run 会自动调用。直接自行管理 `QPromise` 时则必须正确调用 `start()` 和 `finish()`。

</details>

### 题 6：map 和 mapped 的区别

<details>
<summary>答案</summary>

`map()` 原地修改输入序列，`mapped()` 保留输入并产生新的结果序列。原地任务完成前，其他线程不能访问同一输入容器。

</details>

## 28. 本篇总结

Qt 的高层异步编程可以归纳为四个角色：

1. Qt Concurrent 或自定义生产者负责执行工作。
2. `QPromise` 负责发布结果、进度以及响应暂停和取消。
3. `QFuture` 负责观察状态、组合后续步骤和传播错误。
4. `QFutureWatcher` 负责把异步状态桥接到 QObject 信号槽世界。

最重要的实践原则是：

- 不在 GUI 主线程同步等待 Future；
- 不假设取消能够强制终止任意函数；
- 不依赖默认 continuation 线程来更新界面；
- 不把引用或短生命周期对象交给异步任务；
- 用测量决定并行度和任务粒度。

至此，线程与异步三篇已经覆盖从 `QThread`、对象线程归属，到共享数据同步、线程池，再到 Future 组合的完整主线。
