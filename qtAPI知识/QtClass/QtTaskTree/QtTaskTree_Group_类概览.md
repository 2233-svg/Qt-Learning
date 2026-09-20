# QtTaskTree::Group：把多个任务和控制项组合成一个异步单元

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree` · 继承：`ExecutableItem`

`Group` 是 QtTaskTree 的核心容器。它把一串 `GroupItem` 按指定执行模式和工作流策略组合起来，并在父级看来表现为一个可执行的异步任务。

## 实际场景

下载、解码、保存这三个步骤可放进一个顺序组；多个镜像地址探测可放进并行组；一个组还可嵌套其他组，让复杂异步流程仍保持声明式结构。组的直接子项受本组的 `sequential`、`parallel` 或 `ParallelLimit` 控制；嵌套子组则按自己的执行模式运行。

```cpp
const Group recipe {
    sequential,
    stopOnError,
    fetchTask,
    Group {
        parallel,
        parseTask,
        thumbnailTask
    },
    saveTask
};
```

## 结果和生命周期

默认工作流策略是 `StopOnError`：某个直接子任务失败后，组停止并报告错误。插入 `continueOnError`、`finishAllAndSuccess` 等控制项可改变结果传播。`onGroupSetup()` 在组进入、Storage 创建之后调用；返回 `StopWithSuccess` 或 `StopWithError` 会跳过子任务并立即结束。`onGroupDone()` 在组退出、Storage 销毁之前调用，并可改变最终结果。

因为 `Group` 继承 `ExecutableItem`，它可以被加 timeout、日志、取消/接受信号，也能参与 `&&`、`||`、`!` 条件组合。

## API 速查表

| API | 语义与边界 |
|---|---|
| `Group(const GroupItems &children)` | 用元素列表构造一个组。 |
| `Group(std::initializer_list<GroupItem>)` | 常用 recipe 写法。 |
| `Group::onGroupSetup(handler)` / `onGroupSetup(handler)` | 生成组 setup 控制项；handler 可返回 `SetupResult` 或 `void`。 |
| `Group::onGroupDone(handler, callDone)` / `onGroupDone(...)` | 生成组 done 控制项；handler 可返回 `DoneResult`、`bool` 或 `void`。 |
| `sequential` | 直接子任务按顺序执行。 |
| `parallel` | 直接子任务并行启动。 |
| `parallelIdealThreadCountLimit` | 并行启动但限制为理想线程数。 |
| `ParallelLimit(n)` | 并行启动但最多同时运行 `n` 个直接子任务。 |
| `workflowPolicy(policy)` | 通用策略构造函数。 |
| `stopOnError` 等策略常量 | 直接放入组中改变工作流结果与停止规则。 |
