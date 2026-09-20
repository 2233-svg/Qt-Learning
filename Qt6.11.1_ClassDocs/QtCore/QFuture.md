# QFuture
> Qt 6.11.1 · Qt Core · 来自 `QFuture`

## 作用定位
`QFuture<T>` 表示一个正在执行或已结束的异步计算结果。它可等待、查询进度、读取一个或多个结果、取消支持取消的任务，并在结果传播点重新抛出异常。

## API 速查
| API | 是做什么的 |
|---|---|
| `isStarted()` / `isFinished()` | 查询任务生命周期状态。|
| `waitForFinished()` | 阻塞当前线程直到任务结束。|
| `result()` / `results()` | 取得一个或全部结果。|
| `resultAt()` | 读取指定结果。|
| `isResultReadyAt()` | 判断指定结果是否可读。|
| `cancel()` | 请求取消可取消任务。|
| `isCanceled()` | 查询是否已取消。|
| `progressValue()` / `progressText()` | 查询进度。|
| `then()` | 在前序完成后衔接后续任务。|

## 使用场景
由 `QtConcurrent::run()`、`QPromise` 或 task tree 返回，在 UI 中配合 `QFutureWatcher` 更新进度和结果。

## 常见坑与经验
- GUI 线程不要调用 `waitForFinished()`，否则会冻结界面并可能阻断依赖事件循环的完成过程。
- `cancel()` 通常是协作式请求，任务代码必须主动检查取消状态。
- `result()` 可能重新抛出任务异常；需要明确 try/catch 或使用错误值模型。
- 一个 future 可有多个结果，别把 `result()` 当成唯一值的无条件接口。

## 知识点覆盖
异步结果、等待、取消、进度、多结果、异常传播、continuation、GUI 线程。
