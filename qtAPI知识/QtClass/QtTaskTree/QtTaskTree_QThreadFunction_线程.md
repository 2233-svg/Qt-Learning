# QThreadFunction：用 QtConcurrent 在线程池里运行函数

> Qt 6.11.1 · `#include <qthreadfunctiontask.h>` · 模块：`Qt6::TaskTree` · 继承：`QThreadFunctionBase`

`QThreadFunction<ResultType>` 把“稍后在线程池执行的函数”和 `QFutureWatcher<ResultType>` 包在一起。配合 `QThreadFunctionTask<ResultType>`，它可以作为 TaskTree recipe 中的后台计算节点。

## 使用场景

适合把 CPU 计算、文件解析、压缩、图像处理等不应阻塞当前线程的函数放进任务树。setup handler 中调用 `setThreadFunctionData()` 设置函数和参数；任务启动时 adapter 使用 `QtConcurrent::run()` 执行，并在 future 完成时把未取消映射为成功、取消映射为错误。

如果函数需要主动报告错误，可使用带 `QPromise<ResultType> &` 首参的 QtConcurrent 写法，在函数内部取消 promise 的 future。

## 结果和取消边界

读取 `result()` 或 `takeResult()` 前先检查 `isResultAvailable()`。结果未就绪时调用可能阻塞；函数结束但没有产生结果时还可能触发错误。需要进度、暂停、完成等更细控制时，连接 `futureWatcher()` 的信号。

析构运行中的 `QThreadFunction` 时会取消关联 future。默认自动延迟同步开启，析构不会一直等后台函数结束，因此函数捕获或引用的数据必须比后台函数活得更久；不能保证时可关闭自动延迟同步，接受析构阻塞。应用退出前调用 `QThreadFunctionBase::syncAll()` 清理延迟同步的函数。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QThreadFunction<ResultType>()` | 构造空任务；未设置函数时启动会失败。 |
| `~QThreadFunction()` | 运行中析构会取消 future；同步方式受 `setAutoDelayedSync()` 影响。 |
| `setThreadFunctionData(function, args...)` | 保存稍后用 `QtConcurrent::run()` 执行的函数和参数。 |
| `setThreadPool(QThreadPool *pool)` | 设置执行线程池；`nullptr` 使用全局线程池。 |
| `threadPool() const` | 查询当前线程池设置。 |
| `setAutoDelayedSync(bool on)` | 开启时析构不阻塞等待后台函数；关闭时析构等待完成。 |
| `isAutoDelayedSync() const` | 查询自动延迟同步状态。 |
| `futureWatcher()` | 返回内部 `QFutureWatcher<ResultType>`，生命周期绑定到本对象。 |
| `future() const` | 返回关联 `QFuture<ResultType>`。 |
| `isDone() const` | 查询函数执行是否完成。 |
| `isResultAvailable() const` | 查询是否已有可读结果；读结果前先检查。 |
| `result() const` | 读取第一个结果；未就绪时可能阻塞或在无结果时出错。 |
| `takeResult() const` | 移出结果；同样要求结果已可用。 |
| `resultAt(int index) const` | 读取指定索引结果。 |
| `results() const` | 返回全部结果列表。 |
| `QThreadFunctionTask<ResultType>` | `QCustomTask<QThreadFunction<ResultType>, QThreadFunctionTaskAdapter<ResultType>>`。 |
| `QThreadFunctionBase::syncAll()` | 应用退出时同步所有延迟清理的线程函数。 |
