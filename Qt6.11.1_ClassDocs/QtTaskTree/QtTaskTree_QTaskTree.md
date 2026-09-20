# QtTaskTree::QTaskTree
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QTaskTree`

## 作用定位

`QTaskTree` 是 recipe 的运行器。你把 `Group` 配方交给它，它负责启动、调度、取消、统计进度、报告完成结果，并发出 Qt 信号。它是 TaskTree 从“描述”进入“执行”的入口。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `QTaskTree(recipe, parent)` | 用 recipe 创建运行器。 |
| `setRecipe()` | 替换要执行的任务配方。 |
| `start()` | 异步启动任务树。 |
| `cancel()` | 请求取消当前运行。 |
| `runBlocking()` | 同步运行直到完成，适合命令行或测试。 |
| 静态 `runBlocking(recipe)` | 无需显式创建对象的阻塞运行。 |
| `isRunning()` | 是否正在执行。 |
| `done(result)` | 整棵树完成时发出。 |
| `started()` | 启动时发出。 |
| `taskCount()` / `asyncCount()` | 任务总量和当前异步任务数。 |
| `progressMaximum()` / `progressValue()` | 进度统计。 |
| `onStorageSetup()` / `onStorageDone()` | 为特定 `Storage<T>` 绑定生命周期回调。 |

## 使用场景

- 在 QObject 应用中运行异步工作流。
- 用 `runBlocking()` 写测试或命令行工具。
- 连接进度条、取消按钮和完成信号。
- 为存储对象集中做 setup/done。

## 常见坑与经验
- `start()` 后不要修改正在运行的 recipe。
- `cancel()` 是请求取消，底层任务也要配合报告 done/canceled。
- GUI 线程慎用 `runBlocking()`，除非明确知道不会卡界面。
- progress 是 TaskTree 视角的任务计数，不等于业务字节进度或下载百分比。

## 知识点覆盖

- 任务树运行生命周期
- 异步启动和阻塞运行
- 取消、完成、进度
- 存储生命周期 hook
