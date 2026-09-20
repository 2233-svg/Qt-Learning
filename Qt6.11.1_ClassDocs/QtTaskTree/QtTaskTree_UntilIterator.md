# QtTaskTree::UntilIterator
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::UntilIterator`

## 作用定位

`UntilIterator` 按条件决定循环是否继续，适合“直到某个状态满足”为止的异步流程。条件通常由 `Iterator::Condition` 表示。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 基类：`Iterator`

## API 速查

| API | 说明 |
| --- | --- |
| `UntilIterator(const Iterator::Condition &condition)` | 用条件函数创建迭代器，条件满足时结束或停止继续。 |

## 使用场景

- 轮询直到服务可用。
- 重试直到成功或外部状态改变。
- 等待某个缓存/文件/网络状态出现。

## 常见坑与经验
- 条件函数要快，不要在条件里做阻塞 I/O。
- 如果条件永远不满足，就会退化成无限循环，所以仍要加超时/取消。
- 条件读取共享状态时，要注意线程和异步回调的同步。

## 知识点覆盖

- 条件循环
- 轮询和重试
- 超时/取消保护
