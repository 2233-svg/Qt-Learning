# QParallelTaskTreeRunner：并行管理多棵任务树

> Qt 6.11.1 · `#include <qtasktreerunner.h>` · 模块：`Qt6::TaskTree`

`QParallelTaskTreeRunner` 每次 `start()` 都创建并启动一棵新的 `QTaskTree`，多棵树可以同时运行。它适合“每个请求都独立有效”的场景，而不是覆盖或排队。

## 实际使用场景

比如用户同时打开多个文件预览、多个后台检查任务并行进行、一次操作触发多个互不依赖的远端请求。runner 负责保存这些树的生命周期，树完成后自动移除。调用方不需要手写列表、连接 `done()` 再 `deleteLater()`。

如果并行项需要按业务 key 替换或取消，优先用 `QMappedTaskTreeRunner<Key>`；如果所有项只允许串行，用 `QSequentialTaskTreeRunner`。

## 取消与 reset

`cancel()` 会取消 runner 管理的全部任务树，并让每棵树走正常取消流程；符合 `CallDone` 时会调用各自的 done handler。由于内部保存的是集合，取消顺序不要作为业务逻辑依赖。

`reset()` 直接丢弃全部任务树，不调用 done handler。析构 runner 时也属于清理内部资源，不是业务完成通知。

## 并发边界

`QParallelTaskTreeRunner` 不限制同时运行数量。需要限制并发时，应在 recipe 内用 `ParallelLimit` 控制直接子任务并发，或在外层自己做排队。每棵树之间的 storage、进度和结果彼此独立。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QParallelTaskTreeRunner()` | 构造并行 runner；不继承 `QObject`。 |
| `~QParallelTaskTreeRunner()` | 删除仍在运行的树；不把析构当作业务取消通知。 |
| `isRunning() const` | 是否至少有一棵任务树仍由 runner 管理。 |
| `start(recipe, setup, done, callDone)` | 创建一棵新树并立即启动；不会影响已有运行树。 |
| `setupHandler(QTaskTree &)` | 新树启动前调用，可连接该树自己的信号。 |
| `doneHandler(const QTaskTree &, DoneWith)` | 对应树结束后调用；默认 Success、Error、Cancel 都触发。 |
| `cancel()` | 取消全部正在运行的树；调用顺序不保证，done handler 按规则触发。 |
| `reset()` | 直接丢弃全部树；不调用 done handler。 |
| `CallDone` | 每次 `start()` 单独指定，用来过滤对应树的 done handler。 |
