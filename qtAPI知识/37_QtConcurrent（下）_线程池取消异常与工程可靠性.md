# Qt Concurrent（下）：线程池、取消、异常与工程可靠性

并发代码最难的部分通常不是启动任务，而是控制资源、停止任务、传递错误并在页面退出时正确收尾。本篇围绕 `QThreadPool`、`QFuture`、`QPromise` 和 continuation，建立适合 GUI 应用的可靠性规则。

## 1. 默认线程池与自定义线程池

未指定线程池时，Qt Concurrent 通常使用 `QThreadPool::globalInstance()`：

```cpp
QThreadPool *pool = QThreadPool::globalInstance();
qDebug() << pool->maxThreadCount();
```

全局池还可能被其他 Qt 模块和业务代码使用。长时间阻塞任务占满它，会让不相关功能一起变慢。

### 1.1 为业务创建独立池

```cpp
QThreadPool importPool;
importPool.setMaxThreadCount(2);
importPool.setExpiryTimeout(30'000);

QFuture<Result> future = QtConcurrent::run(
    &importPool,
    [] { return importLargeFile(); });
```

线程池对象必须活到所有提交任务结束。把局部 `QThreadPool` 的地址交给异步任务后立即离开作用域是严重生命周期错误。

### 1.2 如何选择线程数

- CPU 密集：通常接近可用逻辑核心数，避免过度订阅。
- 磁盘 I/O：并发数过高会导致寻道或吞吐争用。
- 网络 I/O：优先使用 `QNetworkAccessManager` 的异步 API，而不是占线程等待。
- 数据库：每个线程需要独立连接，并发受数据库连接池限制。

线程数应由最稀缺资源决定，不是越大越快。

## 2. 任务优先级与 `QTaskBuilder`

Qt Concurrent 的任务构建器可设置线程池和优先级：

```cpp
auto future = QtConcurrent::task([] {
        return buildPreview();
    })
    .onThreadPool(previewPool)
    .withPriority(-1)
    .spawn();
```

优先级只影响线程池队列选择，不能抢占一个已经运行的耗时任务。若高优先级交互任务必须快速响应，应使用独立线程池或把长任务拆成小块。

## 3. 取消不是强制终止

```cpp
future.cancel();
```

`cancel()` 表达“请求停止”，不会安全地杀死正在执行的 C++ 函数。基础模式的 `QtConcurrent::run` 无法自动取消普通函数；使用 `QPromise` 才能在函数内部检查取消状态。

```cpp
QFuture<void> future = QtConcurrent::run(
    [](QPromise<void> &promise) {
        for (const WorkItem &item : loadWork()) {
            if (promise.isCanceled())
                return;
            process(item);
        }
    });
```

检查频率需要平衡开销和响应速度。单个 `process(item)` 可能持续数秒时，还应在其内部增加检查点。

## 4. 暂停与恢复

外部可以请求暂停：

```cpp
future.suspend();
future.resume();
```

Promise 任务必须主动响应：

```cpp
for (int i = 0; i < count; ++i) {
    promise.suspendIfRequested();
    if (promise.isCanceled())
        return;
    processChunk(i);
}
```

暂停状态下仍要允许取消。不要在持有互斥锁时调用可能等待恢复的函数，否则其他线程无法获得锁来完成取消或清理。

## 5. GUI 页面的生命周期

页面关闭不代表后台任务结束。错误示例：

```cpp
QtConcurrent::run([this] {
    const auto data = loadData();
    ui->label->setText(data); // 跨线程访问 UI，且 this 可能已销毁
});
```

可靠做法是后台只计算数据，通过 `QFutureWatcher` 在 GUI 线程消费，并让 watcher 受页面管理：

```cpp
auto *watcher = new QFutureWatcher<Data>(this);
QPointer<MyPage> page(this);

connect(watcher, &QFutureWatcher<Data>::finished,
        this, [page, watcher] {
    if (page && !watcher->future().isCanceled())
        page->applyData(watcher->result());
    watcher->deleteLater();
});

watcher->setFuture(QtConcurrent::run(loadData));
```

页面析构时可以调用 `future().cancel()`，但若任务不能协作取消，仍要确保它不引用页面成员。

## 6. 错误和异常传播

任务函数抛出的异常会在 future 获取结果时传播。Qt 异常类型通常保留，其他异常可能按框架规则包装：

```cpp
try {
    const Result result = future.result();
    use(result);
} catch (const QException &e) {
    qWarning() << "并发任务失败:" << e.what();
} catch (const std::exception &e) {
    qWarning() << "标准异常:" << e.what();
}
```

异常不能跨 C ABI、插件卸载边界或不兼容运行库随意传播。大型应用更适合返回显式结果类型：

```cpp
struct ImportResult {
    bool ok = false;
    Data data;
    QString error;
};
```

这样取消、业务失败和异常故障可以清晰区分。

## 7. continuation 的失败与取消分支

```cpp
auto chain = QtConcurrent::run(loadConfiguration)
    .then(validateConfiguration)
    .then(applyConfiguration)
    .onFailed([](const std::exception &e) {
        qWarning() << e.what();
        return ApplyResult::failed();
    })
    .onCanceled([] {
        return ApplyResult::canceled();
    });
```

`onFailed` 的参数类型决定它能捕获哪些异常。不要只注册过窄的异常类型后假设所有失败都被处理。`onCanceled` 和 `onFailed` 是不同路径，用户取消不应记录为系统错误。

## 8. 嵌套 Future 与 `unwrap()`

continuation 返回另一个 future 时会形成 `QFuture<QFuture<T>>`。使用 `unwrap()` 将其展平：

```cpp
QFuture<Result> flat = firstFuture
    .then([](First value) {
        return QtConcurrent::run([value] {
            return secondStage(value);
        });
    })
    .unwrap();
```

展平后，完成和错误更容易在同一链上处理。仍要明确取消是否传播到内层任务，不能假设所有自定义 future 自动响应取消。

## 9. 嵌套并行和线程池饥饿

危险模式：线程池中的每个外层任务再启动内层任务并阻塞等待，而线程池已经没有空闲线程：

```cpp
QtConcurrent::run([&] {
    auto inner = QtConcurrent::run(expensiveWork);
    inner.waitForFinished(); // 可能造成线程池饥饿
});
```

解决方向：

1. 使用 continuation，不占线程等待。
2. 把内外任务放在不同且容量明确的线程池。
3. 扁平化任务，让调度器直接看到所有工作项。
4. 避免在池线程中同步等待同一个池的任务。

## 10. 共享状态与锁粒度

如果每个任务都频繁竞争同一互斥量，并行化反而会更慢：

```cpp
QMutex mutex;
QVector<Result> results;

QtConcurrent::map(inputs, [&](const Input &input) {
    Result result = calculate(input);
    QMutexLocker lock(&mutex);
    results.append(std::move(result));
});
```

更好的方式是每个任务返回独立结果，再归约合并。必须加锁时，把耗时计算放在锁外，并确保所有代码采用同一锁顺序。

## 11. 内存与背压

`mapped` 可能快速产生大量大对象，而消费者来不及处理。使用 watcher 的 pending results limit 控制生产速度：

```cpp
watcher->setPendingResultsLimit(8);
```

仍要避免一次把所有输入和结果同时复制。大文件处理可分批提交，或使用有界队列连接生产者与消费者。

## 12. I/O 与 Qt Concurrent 的边界

Qt Concurrent 适合阻塞式库没有异步接口时的封装，但不是所有 I/O 的首选：

- 网络：优先 `QNetworkAccessManager`。
- 定时等待：优先 `QTimer`。
- 进程：优先异步 `QProcess` 信号。
- 串口/套接字：优先事件驱动 API。

使用线程等待事件会浪费线程池容量，并使取消更难实现。

## 13. 测试方法

### 13.1 用信号等待，不用固定睡眠

```cpp
QFutureWatcher<int> watcher;
QSignalSpy finishedSpy(&watcher, &QFutureWatcher<int>::finished);
watcher.setFuture(QtConcurrent::run([] { return 42; }));

QTRY_COMPARE(finishedSpy.count(), 1);
QCOMPARE(watcher.result(), 42);
```

### 13.2 必测场景

- 正常完成和返回值。
- 开始前取消、运行中取消、完成后取消。
- 暂停后取消。
- 任务抛异常或返回业务错误。
- 页面在任务中途销毁。
- 自定义线程池容量为 1 时仍不会死锁。
- 大结果流受到背压限制。

## 14. 关闭应用时的策略

退出时先停止接收新任务，再请求取消，最后等待有硬性资源要求的任务收尾。不要无期限阻塞 GUI 线程：

```text
停止提交 -> 请求取消 -> 短时异步等待 -> 记录仍未退出任务 -> 有策略地结束
```

涉及文件替换、数据库事务的任务必须在应用退出协议中拥有明确提交或回滚点。

## 15. 工程检查表

1. 长任务使用独立线程池，并有合理并发上限。
2. 普通 `run()` 不被错误地当作可强制取消。
3. Promise 循环同时响应暂停和取消。
4. 后台函数不访问 QWidget/QML 对象。
5. 捕获的数据生命周期覆盖任务运行时间。
6. continuation 有失败和取消分支。
7. 不在池线程中阻塞等待同池任务。
8. 多结果任务有背压或分批策略。
9. 应用退出时能停止提交并可靠收尾。

Qt Concurrent 的合适定位是“受控线程池上的高层数据并行和任务执行”。当流程包含大量异步状态、网络事件和复杂依赖时，应结合状态机、TaskTree 或领域任务调度器，而不是不断嵌套阻塞 future。
