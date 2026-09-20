# QtTaskTree::QProcessTaskDeleter
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QProcessTaskDeleter`

## 作用定位

`QProcessTaskDeleter` 是 TaskTree 进程任务的清理策略对象。它负责在任务结束、取消或销毁路径中正确处理 `QProcess`，避免进程对象泄漏或外部进程悬挂。

## 类说明

- 头文件：`#include <qprocesstask.h>`

## API 速查

| API | 说明 |
| --- | --- |
| 析构/调用策略 | 按 TaskTree 进程任务约定清理 `QProcess`。 |

## 使用场景

- 使用预置 `QProcessTask` 时由框架自动配合。
- 自定义进程任务时复用默认删除策略。

## 常见坑与经验

- 删除 `QProcess` 不等于优雅终止外部进程；需要时先 terminate/kill 并等待状态。
- 进程输出读取、退出码检查和清理由不同层负责，不要混为一谈。
- 取消任务时要决定外部进程是继续运行、请求退出还是强制杀掉。

## 知识点覆盖

- 进程任务资源清理
- QProcess 生命周期
- 取消与外部进程终止策略
