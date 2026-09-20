# QTaskInterface：自定义 Adapter 向任务树报告完成

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree` · 继承：`QObject`

`QTaskInterface` 是 `QCustomTask` 自定义 Adapter 和 `QTaskTree` 之间的完成通知接口。Adapter 启动你的 task 后，必须在 task 结束时调用 `reportDone()`，否则任务树会一直认为该节点仍在运行。

## 解决的问题

不同异步对象有不同的完成信号、回调或轮询方式。`QTaskInterface` 给 Adapter 一个统一出口：无论你监听的是 `finished(bool)`、`QProcess::finished`、`QFutureWatcher::finished`，最后都转换成一次 `reportDone(DoneResult)`。

## Adapter 中的使用方式

自定义 Adapter 通常长这样：

```cpp
class WorkerAdapter
{
public:
    void operator()(Worker *task, QTaskInterface *iface) const
    {
        QObject::connect(task, &Worker::finished, iface, [iface](bool ok) {
            iface->reportDone(toDoneResult(ok));
        }, Qt::SingleShotConnection);
        task->start();
    }
};
```

`Task` 和 `QTaskInterface` 的生命周期由任务树管理；官方契约保证传入的 task 和 iface 会活得比 Adapter 调用过程长。Adapter 可以保存连接，但不应在完成后继续持有裸指针做业务访问。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QTaskInterface(QObject *parent = nullptr)` | 构造接口对象；通常由 `QTaskTree` 内部创建。 |
| `reportDone(DoneResult result)` | Adapter 在 task 完成时必须调用一次，用于通知任务树结果。 |
| `done(DoneResult, QPrivateSignal)` | 内部信号；由 `reportDone()` 驱动，不作为用户主动发射入口。 |
| `event(QEvent *)` | 内部事件处理；一般不需要直接调用。 |
| 调用次数 | 正常任务应只报告一次完成；重复报告属于任务/adapter 设计错误。 |
| 不调用 `reportDone()` | 任务树会一直等待该任务。 |
| 与 `QCustomTask` | 自定义 `Adapter::operator()(Task *, QTaskInterface *)` 的核心协作对象。 |
