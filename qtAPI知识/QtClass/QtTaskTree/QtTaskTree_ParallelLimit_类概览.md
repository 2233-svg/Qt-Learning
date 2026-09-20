# QtTaskTree::ParallelLimit：带自定义并发上限的执行模式

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree` · 继承：`ExecutionMode`

`ParallelLimit` 是一种执行模式：组仍按并行方式调度直接子任务，但同时运行的数量不超过给定上限。它适合网络请求、CPU 任务或进程启动这类需要节流的批处理。

## 使用场景

如果有 100 个下载任务，直接 `parallel` 可能压垮网络、服务器或本机资源；`ParallelLimit(4)` 会保持最多 4 个直接子任务运行，某个任务完成后再启动后续任务。

```cpp
Group {
    ParallelLimit(4),
    task1,
    task2,
    task3
}
```

限制只作用于所在组的直接子任务。若直接子任务是嵌套组，该子组内部仍按自己的模式运行。

## API 速查表

| API | 语义与边界 |
|---|---|
| `ParallelLimit(int limit)` | 构造并发上限为 `limit` 的并行执行模式。 |
| `parallelIdealThreadCountLimit` | 使用 Qt 认为合适的线程数作为上限的预定义模式。 |
| 直接子任务 | 计入本组限制；嵌套组内部任务不直接计入父组限制。 |
