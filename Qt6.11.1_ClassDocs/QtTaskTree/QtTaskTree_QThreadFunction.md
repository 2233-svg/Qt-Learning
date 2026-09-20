# QtTaskTree::QThreadFunction
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QThreadFunction`

## 作用定位

`QThreadFunction<ResultType>` 把一个函数提交到线程池执行，并作为 TaskTree 任务参与调度。它持有 `QFuture`/`QFutureWatcher`，可读取结果、设置线程池、控制自动延迟同步。

## 类说明

- 头文件：`#include <qthreadfunctiontask.h>`
- 基类：`QThreadFunctionBase`

## API 速查

| API | 说明 |
| --- | --- |
| `setThreadFunctionData(function, args...)` | 设置要在线程中运行的函数和参数。 |
| `future()` / `futureWatcher()` | 访问底层 future 和 watcher。 |
| `setThreadPool()` / `threadPool()` | 指定线程池。 |
| `isDone()` | 线程函数是否完成。 |
| `isResultAvailable()` | 是否已有可读取结果。 |
| `result()` / `resultAt()` / `results()` | 读取结果。 |
| `takeResult()` | 取走结果。 |
| `setAutoDelayedSync()` / `isAutoDelayedSync()` | 控制析构/退出时是延迟统一同步还是立即等待。 |

## 使用场景

- 在 TaskTree 中插入 CPU 计算步骤。
- 后台解析、压缩、哈希、索引。
- 需要把 `QFuture` 结果带回任务树。

## 常见坑与经验
- 函数运行在线程池，不能直接操作 GUI 或属于主线程的 QObject。
- 读取 `result()` 前确认完成，否则可能阻塞或无结果。
- 自动延迟同步能避免析构时立刻阻塞，但退出前仍要处理资源依赖。
- 线程函数捕获引用很危险，尽量捕获值或共享所有权对象。

## 知识点覆盖

- QFuture/QFutureWatcher
- 线程池任务接入 TaskTree
- 结果读取和同步
- GUI 线程边界
