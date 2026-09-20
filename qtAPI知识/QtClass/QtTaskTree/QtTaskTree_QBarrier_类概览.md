# QBarrier：等待外部推进的异步屏障

> Qt 6.11.1 · `#include <qbarriertask.h>` · 模块：`Qt6::TaskTree` · 继承：`QObject`

`QBarrier` 是一个“由外部事件决定何时完成”的任务对象。它启动后不会自己做耗时工作，而是等待若干次 `advance()`；计数达到 `limit()` 后以 `DoneResult::Success` 完成。

## 实际使用场景

在任务树里，某个顺序步骤有时必须等并行分支交付数据后才能继续。例如并行启动一个网络任务和一个 UI/对象信号监听，后续解析任务只有在信号到达后才有足够输入。`QBarrier` 可以作为中间屏障，把“等待外部推进”显式放入 recipe。

常见用法不是裸用对象，而是通过 `QBarrierTask`、`QStartedBarrier`、`barrierAwaiterTask()` 或 `signalAwaiterTask()` 接入任务树。

## 运行模型

默认 limit 是 1。调用 `start()` 后，`current()` 从 0 开始计数；每次 `advance()` 增加进度。达到 limit 时发出私有信号 `done(DoneResult::Success)`。也可以调用 `stopWithResult()` 强制结束，传入成功或错误结果，此时不再等待 limit。

`result()` 只在一次运行结束后有值；未启动或仍在运行时返回空 optional。`done` 是 private signal，用户可以连接它，但不能从外部发射它。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QBarrier(QObject *parent = nullptr)` | 构造未启动屏障；默认 limit 为 1。 |
| `setLimit(qsizetype value)` | 设置需要多少次 `advance()` 才完成；通常在 `start()` 前设置。 |
| `limit() const` | 返回当前目标计数。 |
| `start()` | 启动屏障并开始等待推进。 |
| `advance()` | 推进一次；计数达到 limit 后以 `DoneResult::Success` 完成。 |
| `stopWithResult(DoneResult result)` | 无条件结束运行中的屏障，忽略当前计数和 limit。 |
| `isRunning() const` | 查询屏障是否处于等待状态。 |
| `current() const` | 返回当前已推进次数。 |
| `result() const` | 结束后返回最终结果；未启动或运行中为空。 |
| `done(DoneResult)` | 完成时发出的 private signal；可连接，不可由用户发射。 |
| `QBarrierTask` | `QCustomTask<QBarrier>` 的别名，用于把屏障作为 recipe 任务。 |
| `signalAwaiterTask(sender, signal)` | 生成等待某个 signal 的任务；signal 到达时调用 `advance()`。 |
