# QtTaskTree::When：等待 barrier 或 signal 后执行 Do 体

> Qt 6.11.1 · `#include <qbarriertask.h>` · 模块：`Qt6::TaskTree`

`When` 描述一种“先启动某个任务，同时把后续 body 挂起，直到特定 barrier 前进或信号发出再继续”的流程。它必须和 `Do` 通过 `>>` 组合。

## 适用场景

启动 `QProcess` 后，希望进程一旦 started 就并行执行后续任务，而不是等进程完全结束；或者启动一个 QObject 任务后，等它发出某个中间信号再继续。`When` 就是为这种“等待中间状态而非最终 done”准备的。

```cpp
When(kicker) >> Do {
    taskAfterStarted
}
```

`kicker` 接收一个存储的 barrier，并返回一个 `ExecutableItem`。返回的任务与 `Do` 体并行运行；`Do` 体初始挂起，直到 barrier 被 advance。

## 边界

构造出的组合使用指定 `WorkflowPolicy` 协调 kicker 与 body，默认 `StopOnError`。使用 signal 构造函数时，传入的 custom task 的 `Task` 类型必须派生自 `QObject`。如果等待的信号在组合启动前已经发出，和普通 signal 连接一样不会被自动补发。

## API 速查表

| API | 语义与边界 |
|---|---|
| `When(kicker, policy)` | 用 barrier kicker 构造延迟执行结构。 |
| `When(customTask, signal, policy)` | 用 custom task 的 QObject signal 作为放行条件。 |
| `operator>>(When, Do)` | 把等待条件和 body 合成为可执行 `Group`。 |
| `BarrierKickerGetter` | 接收 `QStoredBarrier` 并返回 `ExecutableItem` 的函数类型。 |
| `WorkflowPolicy` 参数 | 控制 kicker 与 body 并行运行时的停止/结果传播策略。 |
