# QtTaskTree::QCustomTask
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QCustomTask`

## 作用定位

`QCustomTask` 是把任意 QObject 异步对象包装进 TaskTree 的通用任务节点。你提供 setup handler 启动或连接对象，done handler 处理完成结果，TaskTree 负责把它放进 recipe 调度。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 基类：`ExecutableItem`

## API 速查

| API | 说明 |
| --- | --- |
| `TaskSetupHandler` | 任务启动/setup 阶段回调。 |
| `TaskDoneHandler` | 任务完成时回调。 |
| `QCustomTask(setup, done, callDone)` | 构造自定义任务节点。 |
| 相关别名 | `QBarrierTask`、`QNetworkReplyWrapperTask`、`QProcessTask`、`QTcpSocketWrapperTask`、`QThreadFunctionTask` 等。 |

## 使用场景

- 把网络请求、进程、socket、线程函数接入 TaskTree。
- 封装项目内已有 QObject 异步类。
- 为任务添加统一 setup/done 行为。

## 常见坑与经验
- setup handler 中启动异步操作后要保证最终会报告 done，否则任务树会挂住。
- done handler 不应做长阻塞工作；需要重任务就拆成另一个任务节点。
- `callDone` 决定 done handler 何时调用，设计时要和失败/取消路径一致。

## 知识点覆盖

- 自定义异步任务封装
- setup/done 分离
- QObject 任务适配
- 结果回传协议
