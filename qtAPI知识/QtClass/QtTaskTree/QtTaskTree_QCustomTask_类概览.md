# QCustomTask：把自定义异步对象接入 TaskTree

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree` · 继承：`ExecutableItem`

`QCustomTask<Task, Adapter, Deleter>` 是 TaskTree 的任务接入模板。它告诉 `QTaskTree`：运行到这个 recipe 节点时，要创建什么 `Task` 对象、如何启动它、它完成时怎样把结果报告回任务树，以及销毁时用什么 deleter。

## 解决的问题

Qt 项目里的异步对象形状很不统一：有的对象是 `start()` 加 `done(bool)`，有的是 `QNetworkReply`，有的是 `QProcess`，还有的是线程池里的函数。`QCustomTask` 把这些对象统一成 `ExecutableItem`，让它们能参与 `Group`、条件、循环、timeout、cancel/accept 等 TaskTree 组合。

库内常见别名也都基于它：`QNetworkReplyWrapperTask`、`QTcpSocketWrapperTask`、`QProcessTask`、`QThreadFunctionTask<T>`、`QBarrierTask`、`QTaskTreeTask`、`QTimeoutTask`。

## 模板参数契约

`Task` 必须可默认构造；真正的任务实例在 `QTaskTree` 运行到该节点时创建，不是在 recipe 构造时创建。

`Adapter` 必须可默认构造，并提供 `void operator()(Task *task, QTaskInterface *iface)`。它负责启动 task，并在 task 完成时调用 `iface->reportDone(...)`。如果任务符合 `QObject + start() + done(DoneResult/bool)` 的形状，可使用默认的 `QDefaultTaskAdapter<Task>`。

`Deleter` 默认是 `std::default_delete<Task>`。当 task 析构可能阻塞当前线程时，可提供自定义 deleter，例如 `QProcessTaskDeleter`。

## setup 与 done

构造 `QCustomTask` 时可传 setup handler 和 done handler。setup 在 task 创建之后、Adapter 启动之前调用，用来配置 task；不要在 setup 里自己启动 task。setup 可返回 `SetupResult::Continue`、`StopWithSuccess` 或 `StopWithError`；返回 stop 时实际 task 不会启动，done handler 也不会再被调用。

done handler 在 task 完成后、结果报告给父组前调用。它可以读取 task 的最终数据，也可以通过返回 `DoneResult` 或 `bool` 改写最终结果。`callDone` 控制 done handler 在成功、错误、取消哪些路径上触发，默认全部触发。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QCustomTask<Task, Adapter, Deleter>` | 把某个任务类型包装成 `ExecutableItem`。 |
| `Task` | 运行时创建的任务对象；必须 default constructible。 |
| `Adapter` | 启动 task 并通过 `QTaskInterface` 报告完成；必须 default constructible。 |
| `Deleter` | 销毁 task 的策略；默认 `std::default_delete<Task>`。 |
| `TaskSetupHandler` | `std::function<SetupResult(Task &)>`；也接受返回 `void` 的简写。 |
| `TaskDoneHandler` | 可接收 `const Task &`、`DoneWith`，可返回 `DoneResult`、`bool` 或 `void`。 |
| `QCustomTask(setup, done, callDone)` | 构造 recipe 元素；handler 保存到 recipe，实际调用发生在运行时。 |
| `SetupResult::Continue` | setup 后继续由 Adapter 启动 task。 |
| `SetupResult::StopWithSuccess` | 跳过 task，当前节点直接成功；不调用 task done handler。 |
| `SetupResult::StopWithError` | 跳过 task，当前节点直接失败；不调用 task done handler。 |
| `CallDoneFlag::Always` | 默认值；成功、失败、取消都调用 done handler。 |
| `CallDoneFlag::OnSuccess/OnError/OnCancel` | 过滤 done handler 的触发结果，可按位组合。 |
| `QBarrierTask` | `QCustomTask<QBarrier>`。 |
| `QNetworkReplyWrapperTask` | `QCustomTask<QNetworkReplyWrapper>`。 |
| `QTcpSocketWrapperTask` | `QCustomTask<QTcpSocketWrapper>`。 |
| `QProcessTask` | `QCustomTask<QProcess, QProcessTaskAdapter, QProcessTaskDeleter>`。 |
| `QThreadFunctionTask<T>` | `QCustomTask<QThreadFunction<T>, QThreadFunctionTaskAdapter<T>>`。 |
| `QTaskTreeTask` | `QCustomTask<QTaskTree, QTaskTreeTaskAdapter>`，用于嵌套任务树。 |
