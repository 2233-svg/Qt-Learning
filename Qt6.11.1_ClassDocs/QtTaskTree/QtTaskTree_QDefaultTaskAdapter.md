# QtTaskTree::QDefaultTaskAdapter
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QDefaultTaskAdapter`

## 作用定位

`QDefaultTaskAdapter<Task>` 是默认任务适配器。它假设 `Task` 是 QObject 派生对象，提供 `start()` 方法，并在完成时发出 `done(DoneResult)` 或兼容完成信号。适配器负责连接完成信号、调用 `start()`，再把结果交给 `QTaskInterface`。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 模板适配器，不是 QObject

## API 速查

| API | 说明 |
| --- | --- |
| `operator()(Task *task, QTaskInterface *interface)` | 连接任务完成信号，启动 task，并通过 interface 回报结果。 |
| `Task::start()` | 默认适配器要求任务提供的启动入口。 |
| `Task::done(DoneResult)` | 默认适配器期望任务完成时发出的信号。 |

## 使用场景

| 场景 | 说明 |
| --- | --- |
| 已有 QObject 异步类 | 只要它有 start/done 约定，就能直接接入 TaskTree。 |
| 快速封装任务 | 不想写自定义 adapter 时使用默认约定。 |
| 统一任务接口 | 让不同任务类遵守同一完成协议。 |

## 常见坑与经验
- `done` 必须只发一次；重复完成会让 TaskTree 状态不可预测。
- `start()` 应尽快返回，不能用同步阻塞冒充异步任务。
- 如果任务完成信号签名不同，就需要自定义 adapter。
- task 生命周期由创建它的 TaskTree 节点管理策略决定，别在外部提前删除。

## 知识点覆盖

- QObject 任务适配
- start/done 约定
- QTaskInterface 完成回报
- 默认适配与自定义适配边界
