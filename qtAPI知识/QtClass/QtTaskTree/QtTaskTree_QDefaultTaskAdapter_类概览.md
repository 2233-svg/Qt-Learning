# QDefaultTaskAdapter：适配标准 QObject 异步任务

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree`

`QDefaultTaskAdapter<Task>` 是 `QCustomTask` 的默认 Adapter。它覆盖一种最常见的 Qt 异步对象形状：对象继承自 `QObject`，有公开 `start()` 方法，完成时发出 `done(DoneResult)` 或 `done(bool)` 信号。

## 适合的任务类型

如果你的 worker 类长这样，就可以直接写 `QCustomTask<Worker>`，不用自定义 adapter：

```cpp
class Worker : public QObject
{
    Q_OBJECT
public:
    void start();
signals:
    void done(QtTaskTree::DoneResult result);
};
```

`done(bool)` 也被接受，`true` 会转换为 `DoneResult::Success`，`false` 转换为 `DoneResult::Error`。

## 工作方式

adapter 在启动时连接 task 的 `done` 信号到 `QTaskInterface::reportDone()`，使用 single-shot 连接，然后调用 task 的 `start()`。也就是说，task 自己仍负责实际异步工作、错误判断和发出完成信号；adapter 只是把它翻译成 TaskTree 能理解的完成事件。

如果 task 没有继承 `QObject`、没有 public `start()`、或者完成信号不是 `done(DoneResult)`/`done(bool)`，模板静态断言会失败。这时应编写自定义 Adapter。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QDefaultTaskAdapter<Task>` | `QCustomTask` 的默认 adapter 模板。 |
| `Task : QObject` | 必须继承 `QObject`，否则编译期失败。 |
| `Task::start()` | 必须是可调用的 public 方法；adapter 会调用它启动任务。 |
| `Task::done(DoneResult)` | 支持的完成信号，直接报告结果。 |
| `Task::done(bool)` | 支持的完成信号，`true/false` 转成 success/error。 |
| `operator()(Task *task, QTaskInterface *iface)` | 连接 done 信号并调用 `task->start()`。 |
| single-shot 连接 | 任务只应报告一次完成；重复 done 不应作为正常路径依赖。 |
| 不匹配的任务形状 | 提供自定义 `Adapter`，不要强行改任务对象接口。 |
