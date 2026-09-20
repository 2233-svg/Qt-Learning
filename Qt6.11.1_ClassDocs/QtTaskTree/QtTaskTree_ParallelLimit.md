# QtTaskTree::ParallelLimit
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::ParallelLimit`

## 作用定位

`ParallelLimit` 是 `ExecutionMode` 的具体变体，用来限制一个组内同时运行的子任务数量。它比裸 `parallel` 更适合网络连接数、磁盘 I/O、线程池或第三方服务有上限的场景。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 基类：`ExecutionMode`

## API 速查

| API | 说明 |
| --- | --- |
| `ParallelLimit(int limit)` | 设置最大并发任务数。 |

## 使用场景

- 批量下载但限制同时请求数。
- 批量处理文件，避免磁盘或 CPU 被打满。
- 对外部服务限流。

## 常见坑与经验

- `limit` 太小会拖慢整体流程，太大可能造成资源拥塞。
- 它限制的是 TaskTree 调度启动数量，不自动限制任务内部再创建的线程或请求。
- 如果任务会长期挂起，后续任务也会被并发上限卡住，超时策略很重要。

## 知识点覆盖

- 并发限流
- 资源保护
- 批处理工作流
- 调度层限制与任务内部行为区别
