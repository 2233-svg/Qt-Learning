# QtTaskTree::ElseIf
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::ElseIf`

## 作用定位

`ElseIf` 是 TaskTree 条件链中的中间分支：前面的 `If` 或 `ElseIf` 不成立时，才评估它自己的条件。它让多路选择保持在 recipe 层，而不是散落在各个任务回调中。

## 类说明

- 头文件：`#include <qconditional.h>`

## API 速查

| API | 说明 |
| --- | --- |
| `ElseIf(const ExecutableItem &condition)` | 用任务完成结果作为分支条件。 |
| `ElseIf(Handler &&handler)` | 用 handler 计算分支条件。 |

## 使用场景

- 多级 fallback：本地缓存 -> 网络 -> 默认值。
- 根据异步检查结果进入不同修复流程。
- 避免把多分支状态机写成嵌套 lambda。

## 常见坑与经验

- `ElseIf` 的条件只有前序分支未命中时才执行；不要把必须总执行的清理逻辑放这里。
- 分支越多越要命名日志或拆成小组，否则排查路径困难。
- 条件任务失败和“条件为假”的语义要在设计时区分清楚。

## 知识点覆盖

- 多分支条件链
- fallback 流程
- 条件任务结果语义
