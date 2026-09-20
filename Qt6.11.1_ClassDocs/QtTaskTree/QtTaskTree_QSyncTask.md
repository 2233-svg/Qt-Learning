# QtTaskTree::QSyncTask
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QSyncTask`

## 作用定位

`QSyncTask` 把一个同步 handler 包装成 TaskTree 中的可执行节点。它适合轻量、立即完成的步骤：计算条件、设置状态、检查参数、同步整理结果。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 基类：`ExecutableItem`

## API 速查

| API | 说明 |
| --- | --- |
| `QSyncTask(Handler &&handler)` | 用同步函数创建任务节点，执行后立即给出结果。 |

## 使用场景
- 在异步步骤之间插入同步状态转换。
- 快速校验输入并决定成功/失败。
- 记录日志或更新简单进度。

## 常见坑与经验
- 不要把耗时操作塞进 `QSyncTask`；它会阻塞任务树所在线程。
- handler 捕获对象时要确认对象仍存活。
- 同步任务如果可能失败，应明确返回/报告失败语义，而不是抛出未处理异常。

## 知识点覆盖

- 同步步骤节点
- 异步流程中的轻量胶水逻辑
- 阻塞风险
