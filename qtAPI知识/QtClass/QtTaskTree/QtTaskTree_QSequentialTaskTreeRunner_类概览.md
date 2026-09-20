# QSequentialTaskTreeRunner：把任务树请求排成串行队列

> Qt 6.11.1 · `#include <qtasktreerunner.h>` · 模块：`Qt6::TaskTree`

`QSequentialTaskTreeRunner` 用来接收多次 recipe 请求，并保证同一时间只运行一棵 `QTaskTree`。后续请求进入队列，当前树结束后自动启动下一棵。

## 适合的场景

它适合必须保持顺序的异步工作：按用户操作顺序写入文件、串行提交远端命令、逐个处理批量导入项，或避免同一资源被多个任务树同时修改。相比自己维护队列，它把“当前任务取消后是否继续下一个”“丢弃当前但保留队列”等边界行为做成明确 API。

如果新请求应该覆盖旧请求，用 `QSingleTaskTreeRunner`；如果请求可以同时跑，用 `QParallelTaskTreeRunner`。

## 队列与取消边界

`enqueue()` 把 recipe 放入队列；如果当前没有运行项，会立即启动。`cancel()` 取消当前任务树并清空等待队列，因此它表示“整个队列都不要了”。`cancelCurrent()` 只取消当前树，之后继续启动下一个排队项。

`reset()` 和 `resetCurrent()` 是无通知丢弃版本：前者丢弃当前和队列，后者丢弃当前并继续下一个。reset 系列不调用被丢弃项的 done handler；cancel 系列会按取消流程和 `CallDone` 规则调用。

## Handler 语义

每个排队项都有自己的 setup、done 和 `CallDone`。setup 在该项真正成为当前树并启动前调用，不是在 `enqueue()` 时调用。done handler 可用来读取那棵树的最终进度、storage 状态或结果；默认成功、错误、取消都调用。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QSequentialTaskTreeRunner()` | 构造串行 runner；通常作为服务对象或控制器成员。 |
| `~QSequentialTaskTreeRunner()` | 丢弃当前和等待队列；不调用尚未通知的 done handler。 |
| `isRunning() const` | 当前是否有正在运行或等待运行的任务树。 |
| `enqueue(recipe, setup, done, callDone)` | 将 recipe 加入队列；空闲时立即启动，否则等待当前结束。 |
| `setupHandler(QTaskTree &)` | 仅在该项实际启动前调用，可连接该树的信号。 |
| `doneHandler(const QTaskTree &, DoneWith)` | 该项结束后调用；签名可省略树、结果或全部参数。 |
| `cancel()` | 取消当前树并清空队列；当前树的 done handler 按 `CallDone` 调用。 |
| `cancelCurrent()` | 只取消当前树；取消完成后继续队列中的下一项。 |
| `reset()` | 无通知丢弃当前树和队列；不调用 done handler。 |
| `resetCurrent()` | 无通知丢弃当前树，然后继续下一项；被丢弃当前项不调用 done handler。 |
| `CallDone` | 控制 done handler 对 Success、Error、Cancel 的触发范围。 |
