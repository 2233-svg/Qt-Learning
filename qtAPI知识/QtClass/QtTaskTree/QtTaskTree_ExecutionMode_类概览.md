# QtTaskTree::ExecutionMode：声明组内直接子任务的启动方式

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree` · 继承：`GroupItem`

`ExecutionMode` 是放在 `Group` 里的控制元素，用来说明本组的直接子任务是顺序启动还是并行启动。它本身不是任务，也不会单独产生进度。

## 语义

默认或显式 `sequential` 表示先启动第一个直接子任务，完成后再启动下一个。`parallel` 表示按 recipe 顺序启动直接子任务，但不等待前一个完成。嵌套组作为父组的一个直接子任务运行；它内部的执行方式由自己的 `ExecutionMode` 决定。

```cpp
Group {
    parallel,
    taskA,
    taskB,
    Group {
        sequential,
        taskC,
        taskD
    }
}
```

这里 `taskA`、`taskB`、内层组会并行启动，而 `taskC`、`taskD` 在内层组里顺序执行。

## API 速查表

| API / 常量 | 语义与边界 |
|---|---|
| `ExecutionMode` | 控制项基类；构造细节通常不直接使用。 |
| `sequential` | 本组直接子任务顺序执行。 |
| `parallel` | 本组直接子任务并行执行。 |
| `parallelIdealThreadCountLimit` | 并行执行，但并发数按理想线程数限制。 |
| `ParallelLimit(limit)` | 自定义并发上限的执行模式。 |
| 嵌套组 | 作为父组的一个任务；内部模式独立。 |
