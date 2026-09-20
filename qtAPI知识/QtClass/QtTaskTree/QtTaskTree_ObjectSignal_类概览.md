# QtTaskTree::ObjectSignal：描述一个 QObject 信号

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree`

`ObjectSignal<Signal>` 是一个小结构，用来把 QObject 实例和它的 signal 成员指针打包在一起。它主要服务于 `ExecutableItem::withCancel()` 和 `withAccept()`。

## 使用方式

这些包装函数接收一个 getter，而不是直接接收 signal 描述。getter 会在任务即将启动时执行，这样可以从当时的任务对象或上下文里取得正确的 QObject。

```cpp
task.withCancel([obj] {
    return makeObjectSignal(obj, &Controller::cancelRequested);
});
```

连接建立后使用 queued single-shot 语义。若 signal 在任务启动前已经发出，包装任务不会回溯发现它。

## API 速查表

| API / 字段 | 语义与边界 |
|---|---|
| `object` | 发出 signal 的 QObject 指针。 |
| `signal` | QObject 子类的 signal 成员指针。 |
| `makeObjectSignal(object, signal)` | 推荐构造函数，自动推导模板参数。 |
| `withCancel(getter)` | 用该 signal 取消任务。 |
| `withAccept(getter)` | 用该 signal 作为任务成功后的接受/确认条件。 |
| 启动前 signal | 不会被缓存，任务启动后才建立连接。 |
