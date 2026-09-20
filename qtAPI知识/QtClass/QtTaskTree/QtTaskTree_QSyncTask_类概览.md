# QSyncTask：在任务树中插入同步处理步骤

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree` · 继承：`ExecutableItem`

`QSyncTask` 用来在 TaskTree recipe 中执行一段立即返回的同步代码。它让“记录日志、检查状态、更新 storage、做一个很轻的分支判断”这类动作也能作为任务树节点参与顺序和工作流策略。

## 什么时候使用

适合非常短的逻辑：把上一步结果写入 storage、验证参数、选择性返回失败、触发一个轻量通知。它运行在当前调用线程，不会自动移到后台线程；如果 handler 可能耗时，应该改用 `QThreadFunctionTask` 或自定义异步任务。

`QSyncTask` 被父 `Group` 当作普通任务处理结果，但它不计入 `QTaskTree::taskCount()` 和 `progressMaximum()`，因此不会增加进度条最大值。

## 返回值语义

handler 可以返回 `DoneResult`、`bool` 或 `void`。返回 `DoneResult::Success/Error` 会参与父组的 `WorkflowPolicy` 判断；返回 `bool` 时 true 表示成功、false 表示失败；返回 `void` 时视为成功。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QSyncTask(handler)` | 构造一个同步执行节点。 |
| `handler -> DoneResult` | 精确控制该节点成功或失败。 |
| `handler -> bool` | true 转成功，false 转失败。 |
| `handler -> void` | 执行后默认成功。 |
| 执行线程 | 在调用任务树推进逻辑的线程中同步执行。 |
| 长耗时 handler | 会阻塞当前线程；应改用 `QThreadFunctionTask`。 |
| 进度统计 | 不计入 `taskCount()` / `progressMaximum()`。 |
| 与 `If`/`ElseIf` | `If(handler)` 的非 `ExecutableItem` 条件会包装成 `QSyncTask`。 |
