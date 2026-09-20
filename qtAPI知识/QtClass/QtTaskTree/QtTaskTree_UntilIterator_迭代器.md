# QtTaskTree::UntilIterator：条件满足前持续循环

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree` · 继承：`Iterator`

`UntilIterator` 在每轮开始前调用条件函数，并在条件返回 `true` 时停止。它表达的是“重复直到条件成立”，不是“当条件成立时执行”。

## 使用场景

轮询共享状态、等待计数达到阈值、按运行期条件停止重试，都适合用它。条件函数接收当前迭代序号，可用来实现最大轮次保护。

```cpp
UntilIterator untilDone([](qsizetype i) {
    return i >= 10 || externalStateReady();
});
```

## 边界

条件在每次迭代前执行，因此如果第一次就返回 `true`，body 不会运行。条件函数应快速、无阻塞；耗时异步判断应建模为任务结果，而不是卡在条件函数里。

## API 速查表

| API | 语义与边界 |
|---|---|
| `UntilIterator(const Iterator::Condition &condition)` | 构造条件停止迭代器。 |
| `condition(qsizetype iteration)` | 每轮开始前调用；返回 `true` 表示停止。 |
| 继承的 `iteration()` | body handler 内读取当前轮次。 |
| 第一次条件为真 | body 一次也不执行。 |
