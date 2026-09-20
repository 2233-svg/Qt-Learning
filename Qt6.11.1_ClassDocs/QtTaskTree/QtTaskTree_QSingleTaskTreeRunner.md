# QtTaskTree::QSingleTaskTreeRunner
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QSingleTaskTreeRunner`

## 作用定位

`QSingleTaskTreeRunner` 是运行单个任务树的辅助器。它封装 `QTaskTree` 的启动、完成回调和生命周期管理，适合“同一时间只跑一个 recipe”的场景。

## 类说明

- 头文件：`#include <qtasktreerunner.h>`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `start(recipe)` | 启动一个任务树。 |
| `cancel()` | 取消当前任务树。 |
| `isRunning()` | 是否有任务正在运行。 |
| `done(result)` | 当前任务树完成。 |

## 使用场景

- UI 操作触发一个后台流程，完成前禁止重复启动。
- 对话框/向导页运行一段 TaskTree。
- 简化手写 `QTaskTree` 对象管理。

## 常见坑与经验
- 重复 start 时要明确是拒绝、取消旧任务还是排队；single runner 通常不表示队列。
- runner 生命周期要覆盖任务完成，否则回调无法交付。
- UI 按钮状态可直接绑定 `isRunning()`/done。

## 知识点覆盖

- 单任务树运行辅助
- 生命周期封装
- UI 启动/取消模型
