# QtTaskTree::If
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::If`

## 作用定位

`If` 是 TaskTree 条件分支的起点。条件可以是一个 `ExecutableItem`，也可以是一个 handler。它通常与 `Then`、`ElseIf`、`Else` 拼成声明式条件结构。

## 类说明

- 头文件：`#include <qconditional.h>`

## API 速查

| API | 说明 |
| --- | --- |
| `If(const ExecutableItem &condition)` | 用任务结果作为条件。 |
| `If(Handler &&handler)` | 用同步 handler 返回/报告的结果作为条件。 |

## 使用场景

- 先检查条件，再决定是否执行后续任务。
- 用异步探测任务决定分支，例如网络可用性、文件是否存在。
- 在 recipe 中替代嵌套回调式 if/else。

## 常见坑与经验
- 条件如果是异步任务，分支会等它完成，而不是构造 recipe 时立即判断。
- handler 捕获变量时要考虑任务树运行时机。
- 分支内部仍可以放组、并行和循环，不必把逻辑塞进条件函数里。

## 知识点覆盖

- 声明式条件分支
- 同步/异步条件
- 条件结果驱动流程
