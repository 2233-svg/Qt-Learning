# QtTaskTree::Do：For 和 When 的任务体

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree`

`Do` 是配合 `For (...) >> Do { ... }` 和 `When (...) >> Do { ... }` 使用的 body 元素。它不独立放进普通 `Group`，而是通过 `operator>>` 和前置控制结构组合成可执行组。

## 循环体语义

在 `For` 中，`Do` 的 children 会在每次迭代执行。一个容易踩的边界是：如果 `onGroupSetup()`、`onGroupDone()` 或 `Storage` 是 `Do` 的直接子项，它们围绕的是整个循环，而不是每次迭代。若需要每轮都创建 Storage 或调用组处理器，应在 `Do` 里再包一层 `Group`。

```cpp
For(RepeatIterator(3)) >> Do {
    Group {
        perIterationStorage,
        task
    }
}
```

在 `When` 中，`Do` 是 barrier 或 signal 放行后继续执行的任务体。

## 并行边界

在 `For` 的 `Do` 体中放入 `parallel` 会让迭代之间也可能并行展开，尤其与 `ForeverIterator` 组合时可能无限启动任务。需要串行循环时保持默认顺序模式或显式放入 `sequential`。

## API 速查表

| API | 语义与边界 |
|---|---|
| `Do(const GroupItems &children)` | 构造 `For` 或 `When` 使用的 body。 |
| `Do(std::initializer_list<GroupItem>)` | 常用初始化列表写法。 |
| `For(iterator) >> Do { ... }` | 形成循环组，可放进 recipe。 |
| `When(...) >> Do { ... }` | 形成延迟执行组，可放进 recipe。 |
| 直接 `Storage` 子项 | 在整个循环/When 体范围创建一次；每轮独立需要再包 `Group`。 |
| 直接组处理器子项 | 对整个 body 范围调用一次；每轮独立需要再包 `Group`。 |
