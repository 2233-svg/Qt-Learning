# Qt TaskTree（下）：自定义任务、共享存储、屏障与可靠性

当内置的同步、线程函数或 `QFuture` 适配无法表达业务流程时，可以使用 `QCustomTask` 和 `QTaskInterface` 接入任意异步 API。本篇还介绍跨节点共享结果的 `Storage`、协调并发的 `QBarrier`/`QStartedBarrier`、条件和循环节点，以及取消、超时和资源释放策略。

## 1. 自定义任务的核心协议

自定义任务需要回答三个问题：

1. 任务何时开始执行。
2. 任务何时成功、失败或取消。
3. 任务如何响应取消并释放资源。

`QTaskInterface` 是任务适配器与运行器之间的桥梁。适配器完成工作后调用 `reportDone()`，而不是直接操作任务树对象。

## 2. `QCustomTask` 与适配器

### 2.1 基本结构

```cpp
#include <QCustomTask>
#include <QTaskInterface>

struct Worker
{
    void start();
    void stop();
    bool succeeded() const;
};

struct WorkerTaskAdapter
{
    void operator()(Worker *worker, QTaskInterface *iface)
    {
        QObject::connect(workerObject, &WorkerObject::finished,
                         workerObject, [worker, iface] {
            iface->reportDone(worker->succeeded()
                              ? QtTaskTree::DoneResult::Success
                              : QtTaskTree::DoneResult::Error);
        });
        worker->start();
    }
};

using WorkerTask = QCustomTask<Worker, WorkerTaskAdapter>;
```

实际适配器签名、完成枚举和删除器模板参数应以 Qt 6.11.1 的头文件为准。示例强调生命周期：适配器获得任务接口后负责在异步完成点报告结果，任务对象由 `QCustomTask` 按配置销毁。

### 2.2 取消处理

```cpp
struct CancelAwareAdapter
{
    void operator()(Worker *worker, QTaskInterface *iface)
    {
        QObject::connect(iface, &QTaskInterface::canceled,
                         workerObject, [worker] {
            worker->stop();
        });
        worker->start();
    }
};
```

取消槽必须是幂等的：多次收到取消请求不能重复释放同一资源。若底层 API 没有取消能力，应在完成回调中检查任务是否已经取消，并丢弃迟到结果。

## 3. `Storage`：跨任务共享类型化状态

### 3.1 声明存储结构

```cpp
struct DownloadState
{
    QUrl url;
    QByteArray payload;
    QString error;
};

QtTaskTree::Storage<DownloadState> state;
```

`Storage<T>` 为任务树提供受控的共享对象。任务可以在 setup 阶段初始化它，在后续节点读取或更新。与捕获共享指针相比，Storage 的生命周期绑定到任务树，更容易在取消和失败时统一清理。

### 3.2 在 setup/done 中访问

```cpp
QTaskTree tree(recipe);

tree.onStorageSetup(state, [](DownloadState &s) {
    s.url = QUrl("https://example.test/data.json");
});

tree.onStorageDone(state, [](const DownloadState &s) {
    if (!s.error.isEmpty())
        qWarning() << s.error;
    else
        qDebug() << "字节数:" << s.payload.size();
});
```

setup 处理器适合填充输入参数，done 处理器适合读取最终结果。不要在多个并行分支中无保护地写同一字段；可以给每个分支分配独立字段，或使用互斥量/消息汇总节点。

## 4. 屏障：等待多个异步分支

### 4.1 `QBarrier`

屏障用于等待一组参与者全部到达，再继续后续任务：

```cpp
QtTaskTree::QBarrier barrier(2);

Group recipe = Group {
    startDownloadA(barrier),
    startDownloadB(barrier),
    Then([&barrier] {
        barrier.arrive();
    })
};
```

调用方式应以本机文档为准；核心原则是预先设置参与者数量，每个分支恰好调用一次到达操作。分支提前失败或取消时也必须到达或显式终止屏障，否则后续节点会永久等待。

### 4.2 `QStartedBarrier`

`QStartedBarrier` 适合“所有任务都已启动后再执行下一步”的场景，例如同时打开多个连接：

```cpp
QtTaskTree::QStartedBarrier started(3);
// 三个任务在真正开始时通知 started，随后统一放行。
```

屏障只协调时序，不传递业务结果。结果仍应放入 Storage、`QFuture` 或自定义结果对象中。

## 5. 条件、循环与迭代器节点

TaskTree 提供 `If`、`Else`、`ElseIf`、`For`、`Forever`、`RepeatIterator` 等声明式节点，用来表达控制流。

### 5.1 条件分支

```cpp
Group recipe = Group {
    If([] { return QFile::exists("cache.json"); })
        .Then(loadCache)
        .Else(fetchFromNetwork)
};
```

条件函数应快速完成且无副作用。若条件依赖异步结果，先把结果写入 Storage，再在后续同步节点读取它。

### 5.2 有限迭代

```cpp
Group recipe = For(files, [](const QString &file) {
    return processFile(file);
});
```

有限循环适合批量文件、分页请求和重试列表。要为每次迭代设置明确的取消检查和资源上限，避免输入集合巨大导致任务树占用过多内存。

### 5.3 无限或重复任务

`Forever` 适合轮询或长期监控，但必须提供取消出口：

```cpp
auto monitor = Forever([&] {
    return pollOnce();
});

QTaskTree tree(monitor);
QObject::connect(stopButton, &QPushButton::clicked,
                 &tree, &QTaskTree::cancel);
```

轮询间隔应使用可取消的计时器或异步等待，避免 `while (true)` 加 `sleep` 占满线程。

## 6. 并发限制：`ParallelLimit`

并行并不意味着无限制地创建线程或连接。`ParallelLimit` 用来限制同时运行的分支数量：

```cpp
QtTaskTree::ParallelLimit limit(4);

Group recipe = Parallel {
    limit,
    For(urls, [](const QUrl &url) {
        return download(url);
    })
};
```

限制值应结合 CPU、网络、文件描述符和服务端配额选择。过大可能导致上下文切换和服务端限流，过小则降低吞吐。生产环境可以通过配置文件或运行时指标动态调整。

## 7. 网络任务的可靠性模式

### 7.1 超时、取消和迟到回调

网络任务至少需要：

- 连接和响应超时。
- 取消时断开或终止请求。
- 完成回调只执行一次。
- 树已结束后忽略迟到回调。

```cpp
struct ReplyAdapter
{
    void operator()(QNetworkReply *reply, QTaskInterface *iface)
    {
        QPointer<QNetworkReply> safeReply = reply;
        QObject::connect(reply, &QNetworkReply::finished,
                         reply, [safeReply, iface] {
            if (!safeReply)
                return;
            const auto result = safeReply->error() == QNetworkReply::NoError
                ? DoneResult::Success : DoneResult::Error;
            iface->reportDone(result);
        });

        QObject::connect(iface, &QTaskInterface::canceled,
                         reply, [safeReply] {
            if (safeReply)
                safeReply->abort();
        });
    }
};
```

示例中的 `QNetworkReply` 应由所属线程的 `QNetworkAccessManager` 管理。不要跨线程直接调用它的方法；必要时通过队列信号把取消请求发送到网络线程。

### 7.2 重试和退避

重试应只针对临时错误，例如连接重置或 HTTP 5xx，不应对参数错误、认证失败或明确的 4xx 无限重试。使用指数退避并设置最大次数：

```text
delay = min(base * 2^attempt + jitter, maxDelay)
```

每次重试都应重新检查取消状态，并在最终失败时保留最后一个可诊断的错误码和响应摘要。

## 8. 进程任务与资源释放

`QProcess` 任务需要处理启动失败、非零退出码、标准错误和取消时的进程终止：

```cpp
QObject::connect(iface, &QTaskInterface::canceled,
                 process, [process] {
    process->terminate();
    if (!process->waitForFinished(500))
        process->kill();
});
```

不要在 GUI 线程中调用长时间 `waitForFinished()`。如果必须等待，应把进程对象和适配器放在工作线程，并通过信号把最终结果送回主线程。

## 9. 失败恢复与补偿

任务树失败后，已经完成的副作用不会自动回滚。例如文件已写入、远端订单已创建。需要显式设计补偿节点：

```text
创建临时文件
   ├─ 成功：提交并重命名
   └─ 失败/取消：删除临时文件
```

把不可逆操作放在树的后段，并让前置任务尽可能只产生临时结果。对数据库、文件和网络副作用分别记录幂等键，重试时避免重复提交。

## 10. 测试策略

### 10.1 确定性测试

把真实网络、文件和进程替换为可控的 fake 任务，验证：

- 顺序节点不会提前执行。
- 并行节点全部完成后才进入汇总。
- 取消会传播到每个自定义任务。
- 屏障参与者缺失时能超时或失败，而不是永久挂起。
- 失败结果只触发一次 done 处理器。

### 10.2 时间控制

不要在测试中依赖任意 `sleep(100)`。使用 `QSignalSpy`、可注入的时钟和手动完成信号，让测试在事件循环中等待明确事件：

```cpp
QSignalSpy spy(&tree, &QTaskTree::done);
tree.start();
fakeWorker->finishSuccessfully();
QTRY_COMPARE(spy.count(), 1);
```

## 11. 工程化检查表

1. 每个自定义任务都有明确的成功、失败、取消出口。
2. 所有异步回调都检查对象生命周期和任务是否仍有效。
3. 并行分支共享数据时有明确同步策略。
4. 网络、进程和文件任务具备超时、重试上限和资源清理。
5. 长期运行的 `Forever` 节点可以被取消并报告状态。
6. 运行器析构时不会留下线程、定时器或 QObject 回调。
7. 使用日志记录树 ID、节点 ID 和最终 `DoneWith` 结果。

TaskTree 的价值不在于替代所有异步 API，而在于把复杂流程的依赖、并发和终止语义显式化。掌握这些边界后，才能在网络、数据库、文件和进程混合场景中保持可测试、可取消、可恢复。
