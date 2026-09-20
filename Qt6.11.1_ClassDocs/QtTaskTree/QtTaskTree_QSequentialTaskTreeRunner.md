# QtTaskTree::QSequentialTaskTreeRunner
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QSequentialTaskTreeRunner`

## 作用定位

`QSequentialTaskTreeRunner` 按顺序运行多个任务树。它适合把多个 recipe 当作队列处理：前一个完成后再启动下一个。

## 类说明

- 头文件：`#include <qtasktreerunner.h>`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `start()` / 添加 recipe 的接口 | 把任务树加入顺序运行流程。 |
| `cancel()` | 取消当前和/或后续流程。 |
| `isRunning()` | 是否仍在处理队列。 |
| `done()` | 整体完成通知。 |

## 使用场景

| 场景 | 说明 |
| --- | --- |
| 批量项目处理 | 一个项目完成后再处理下一个。 |
| 串行迁移流程 | 每步都是独立 recipe，但必须按顺序。 |
| 避免资源竞争 | 共享设备/文件/服务一次只允许一个流程。 |

## 常见坑与经验

- 某个任务失败后是否继续后续队列，要看 runner 策略和你的完成处理。
- 队列很长时要提供取消和进度反馈。
- 如果各任务彼此独立且耗时，可能 `QParallelTaskTreeRunner` 更合适。

## 知识点覆盖

- 多任务树串行队列
- 批处理
- 失败后继续/中断策略
