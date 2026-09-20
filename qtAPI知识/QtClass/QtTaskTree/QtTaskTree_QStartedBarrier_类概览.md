# QStartedBarrier：构造后已启动的屏障

> Qt 6.11.1 · `#include <qbarriertask.h>` · 模块：`Qt6::TaskTree` · 继承：`QBarrier`

`QStartedBarrier` 是一个构造完成后已经处于 running 状态的 `QBarrier`。它主要用于 `Storage<QStartedBarrier>`：把同一个屏障对象放进任务树存储里，让多个任务可以拿到它并推进同一个等待点。

## 为什么需要它

普通 `QBarrier` 需要显式 `start()`。在 recipe 的 storage 场景里，屏障常常需要一创建就开始等待，这样并行分支可以直接连接 signal 或调用 `advance()`。`QStartedBarrier` 把“创建并启动”合成一步，减少忘记启动造成的死等。

## 与 When 的协作

`QStoredBarrier` 是 `Storage<QStartedBarrier>` 的别名。`When` 和 `barrierAwaiterTask()` 使用它构建“启动一个触发者，然后让后续任务等屏障”的 recipe 片段。一个典型模式是：kicker 任务在收到某个中间信号时推进屏障，awaiter 任务阻塞顺序流直到屏障完成。

## 继承边界

`QStartedBarrier` 继承 `QBarrier` 的 `advance()`、`stopWithResult()`、`result()` 等 API。它新增的是构造时自动启动和带 limit 的构造函数；完成规则仍由 `QBarrier` 决定。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QStartedBarrier(QObject *parent = nullptr)` | 创建并启动 limit 为 1 的屏障。 |
| `QStartedBarrier(qsizetype limit, QObject *parent = nullptr)` | 创建并启动指定 limit 的屏障。 |
| `~QStartedBarrier()` | 普通 QObject 析构；不要把析构当作完成通知。 |
| `advance()` | 继承自 `QBarrier`；推进计数，达到 limit 后成功完成。 |
| `stopWithResult(DoneResult)` | 继承自 `QBarrier`；强制结束屏障。 |
| `isRunning() const` | 构造后通常立即为 true，完成后为 false。 |
| `QStoredBarrier` | `Storage<QStartedBarrier>` 的别名，供 recipe 内共享屏障。 |
| `BarrierKickerGetter` | `std::function<ExecutableItem(const QStoredBarrier &)>`，用于 `When` 构造。 |
| `barrierAwaiterTask(storedBarrier)` | 生成等待指定 stored barrier 完成的任务。 |
