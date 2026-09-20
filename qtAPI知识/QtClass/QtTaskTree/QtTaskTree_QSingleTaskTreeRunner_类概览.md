# QSingleTaskTreeRunner：只保留一个正在运行的任务树

> Qt 6.11.1 · `#include <qtasktreerunner.h>` · 模块：`Qt6::TaskTree`

`QSingleTaskTreeRunner` 是“最新一次请求覆盖旧请求”的运行器。它内部管理一个 `QTaskTree`，每次 `start()` 都会丢掉当前正在运行的树并启动新的 recipe。

## 适合的场景

典型例子是 UI 上的刷新按钮、搜索框输入变化、预览生成：用户连续触发多次时，旧任务的结果已经没有意义，只希望最新一次任务继续运行。直接手写 `QTaskTree *current` 也能做到，但容易漏掉取消、析构和 handler 调用规则；runner 把这些规则收在一个小对象里。

如果你要保留每个请求并逐个执行，用 `QSequentialTaskTreeRunner`；如果每个请求都应并行跑，用 `QParallelTaskTreeRunner`。

## start、cancel、reset 的差异

`start()` 无条件启动新的任务树。同一时刻最多只有一棵树；当前树若还在运行，会先被替换。`cancel()` 面向“正常取消”：它会让当前树走取消流程，并按 `CallDone` 规则调用 done handler。`reset()` 面向“直接丢弃”：它移除当前树，不调用 done handler，语义更接近对象清理或失效。

析构 runner 时如果还有树在运行，也会删除内部树；这不是业务取消，不会调用 done handler。

## Handler 语义

`start(recipe, setup, done, callDone)` 的 setup handler 可接收 `QTaskTree &` 或不接收参数，只能返回 `void`。done handler 可接收 `const QTaskTree &`、`DoneWith`、两者都接收，或不接收参数，也只能返回 `void`。是否调用 done handler 由 `CallDone` 决定，默认成功、错误、取消都调用。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QSingleTaskTreeRunner()` | 构造空 runner；不继承 `QObject`，通常作为成员变量使用。 |
| `~QSingleTaskTreeRunner()` | 删除仍在运行的内部树；不调用该树的 done handler。 |
| `isRunning() const` | 当前是否持有正在运行的任务树。 |
| `start(recipe, setup, done, callDone)` | 启动新的 recipe；会替换当前运行树，同一时间最多一个。 |
| `setupHandler(QTaskTree &)` | 在内部树启动前调用，可连接信号、设置 storage handler。 |
| `doneHandler(const QTaskTree &, DoneWith)` | 内部树结束后调用；签名可省略树或结果参数。 |
| `CallDoneFlag::Always` | 默认值；成功、错误、取消都会调用 done handler。 |
| `CallDoneFlag::OnSuccess` / `OnError` / `OnCancel` | 只在指定结果下调用 done handler，可按位组合。 |
| `cancel()` | 取消当前树；会走取消流程，符合条件时调用 done handler。 |
| `reset()` | 丢弃当前树；不调用 done handler，适合对象失效或无需通知的替换。 |
