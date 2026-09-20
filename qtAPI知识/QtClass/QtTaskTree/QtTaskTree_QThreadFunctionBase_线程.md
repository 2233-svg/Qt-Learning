# QThreadFunctionBase：线程函数任务的同步控制基类

> Qt 6.11.1 · `#include <qthreadfunctiontask.h>` · 模块：`Qt6::TaskTree`

`QThreadFunctionBase` 是 `QThreadFunction<ResultType>` 的非模板基类，集中保存线程池、自动延迟同步和全局同步能力。日常不会直接把它放进 recipe，但理解它能解释 `QThreadFunction` 析构和应用退出时为什么需要 `syncAll()`。

## 解决的问题

`QThreadFunction` 通过 `QtConcurrent::run()` 启动函数。若任务树取消或对象销毁时函数还没退出，立刻阻塞等待可能卡住主线程；完全不等待又可能让后台函数在应用退出时访问失效数据。`QThreadFunctionBase` 提供这两种策略之间的开关和最终同步点。

## 同步策略

默认自动延迟同步开启：销毁运行中的 `QThreadFunction` 时会取消 future，但不在析构点阻塞等待函数真正结束。函数可以通过 `QPromise` 观察取消并尽快退出。代价是应用退出前必须调用 `syncAll()`，把所有仍在收尾的函数同步干净。

关闭自动延迟同步时，析构会等待函数完成，局部生命周期更确定，但可能阻塞调用线程。

## API 速查表

| API | 语义与边界 |
|---|---|
| `setThreadPool(QThreadPool *pool)` | 设置 `QtConcurrent::run()` 使用的线程池；`nullptr` 表示全局线程池。 |
| `threadPool() const` | 返回当前线程池；`nullptr` 代表使用 `QThreadPool::globalInstance()`。 |
| `setAutoDelayedSync(bool on)` | 控制析构运行中函数时是否延迟同步；默认开启。 |
| `isAutoDelayedSync() const` | 查询自动延迟同步开关。 |
| `setSyncSkipped(bool on)` | 控制是否跳过同步，供内部/高级生命周期策略使用。 |
| `isSyncSkipped() const` | 查询同步跳过状态。 |
| `syncAll()` | 应用退出时从主线程调用，等待所有延迟同步的函数收尾。 |
| `storeFuture(const QFuture<void> &future)` | 受保护接口，派生类保存待同步 future。 |
