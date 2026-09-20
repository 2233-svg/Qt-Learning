# QtTaskTree::QParallelTaskTreeRunner
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QParallelTaskTreeRunner`

## 作用定位

`QParallelTaskTreeRunner` 同时运行多个任务树，适合彼此独立的批量流程。它比在一个巨大 `Group{ parallel, ... }` 中手写所有任务更适合动态追加和统一管理。

## 类说明

- 头文件：`#include <qtasktreerunner.h>`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `start()` / 添加 recipe 的接口 | 启动多个任务树并行运行。 |
| `cancel()` | 取消正在运行的任务树集合。 |
| `isRunning()` | 是否仍有任务树未完成。 |
| `done()` | 全部完成后的通知。 |

## 使用场景

- 多个项目同时索引/检查/下载。
- 动态任务集合，不方便预先写成一个固定 Group。
- 批量独立工作流并行推进。

## 常见坑与经验
- 并行 runner 不自动解决共享资源冲突，必要时加并发上限或锁。
- 全部完成前对象必须保持存活。
- 单个子任务失败是否取消其它任务，要明确策略。

## 知识点覆盖

- 多任务树并行运行
- 动态任务集合
- 批量异步流程管理
