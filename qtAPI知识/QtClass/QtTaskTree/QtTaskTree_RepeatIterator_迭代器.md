# QtTaskTree::RepeatIterator：固定次数循环

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree` · 继承：`Iterator`

`RepeatIterator` 让 `For` 循环执行固定次数。它适合重试、批量占位步骤、固定轮次轮询等场景。

## 使用方式

```cpp
const Group recipe {
    For(RepeatIterator(3)) >> Do {
        attemptTask
    }
};
```

每轮的序号可通过捕获同一个迭代器并在 body handler 中调用 `iteration()` 取得。不要在 recipe 构造期或循环外读取它。

## API 速查表

| API | 语义与边界 |
|---|---|
| `RepeatIterator(qsizetype count)` | 构造固定重复 `count` 次的迭代器。 |
| 继承的 `iteration()` | 当前轮次序号，范围通常为 `0..count-1`，只能在 body handler 内读取。 |
| `For(RepeatIterator(count)) >> Do { ... }` | 固定次数循环的完整写法。 |
