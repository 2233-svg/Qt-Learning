# QtTaskTree::ExecutionMode
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::ExecutionMode`

## 作用定位

`ExecutionMode` 是放在 `Group` 里的执行策略项，用来声明组内子任务按顺序跑还是并行跑。它是 recipe 的控制标记，不是独立任务。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 基类：`GroupItem`
- 派生：`ParallelLimit`

## API 速查

| API | 说明 |
| --- | --- |
| `sequential` | 组内任务按顺序执行，前一步完成后再启动下一步。 |
| `parallel` | 组内可并行启动，适合彼此独立的异步任务。 |
| `parallelIdealThreadCountLimit` | 并行数量按系统理想线程数限制。 |
| `ParallelLimit(limit)` | 自定义并发上限。 |

## 使用场景

- 有依赖链时使用 `sequential`。
- 多个网络请求、独立检查、并发 I/O 使用 `parallel`。
- CPU 密集或资源受限任务使用 `ParallelLimit`。

## 常见坑与经验

- 并行不等于线程安全；并行任务共享状态时必须自己同步。
- 对同一个 QObject 的方法调用仍受线程归属影响，别把 QObject 当普通数据并发改。
- `parallel` 适合异步 I/O；CPU 任务还要看底层任务是否真的在线程池执行。

## 知识点覆盖

- 顺序和并行执行策略
- 并发上限
- recipe 控制项
- 任务依赖和资源限制
