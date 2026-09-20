# QtTaskTree::ExecutableItem：可作为异步步骤运行的 recipe 元素

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree` · 继承：`GroupItem`

`ExecutableItem` 是所有“父组可以启动并等待结果”的元素基类。`Group`、`Forever`、`QCustomTask`、`QSyncTask` 等都属于这一类；普通控制项如 `sequential` 或 `Storage` 则不属于可执行步骤。

## 它解决的问题

可执行元素除了能放进 `Group`，还可以组合成条件表达式或附加运行时行为。比如一个任务可以加超时，可以等待某个 signal 才算真正完成，也可以被某个 signal 取消。

```cpp
const auto task =
    networkTask
        .withTimeout(5s)
        .withLog("download");
```

## 组合语义

`!item` 反转成功/失败。`first && second` 顺序执行短路与：第一个失败时第二个不会运行。`first || second` 顺序执行短路或：第一个成功时第二个不会运行。若需要并行短路，可用 `Group { parallel, stopOnError, ... }` 或 `Group { parallel, stopOnSuccess, ... }` 表达。

`withCancel()` 与 `withAccept()` 都在任务即将启动时连接 signal；如果 signal 早于启动发出，不会被事后捕获。`withTimeout()` 在超时后取消原任务并让包装结果变为错误。

## API 速查表

| API | 语义与边界 |
|---|---|
| `withTimeout(timeout, handler)` | 给任务加超时；超时后调用可选 handler、取消原任务并以错误完成。 |
| `withLog(logName)` | 返回带调试日志的包装任务，记录启动、结束、耗时和结果。 |
| `withCancel(getter, postCancelRecipe)` | 等待取消 signal；signal 到达后取消原任务，执行可选后处理 recipe，并以错误完成。 |
| `withAccept(getter)` | 原任务成功后等待指定 signal；signal 已提前到达时可跳过等待。 |
| `operator!` | 反转任务的 `DoneResult::Success` 与 `DoneResult::Error`。 |
| `operator&& (a, b)` | 顺序短路与；`a` 失败则跳过 `b`。 |
| `operator|| (a, b)` | 顺序短路或；`a` 成功则跳过 `b`。 |
| `operator&&(item, DoneResult)` | 按给定结果强制或保留任务结果，常用于 recipe 结果调整。 |
| `operator||(item, DoneResult)` | 与上类似，用于把结果调成成功路径。 |
| `makeObjectSignal(object, signal)` | 构造 `withCancel()`/`withAccept()` 所需的 signal 描述。 |
