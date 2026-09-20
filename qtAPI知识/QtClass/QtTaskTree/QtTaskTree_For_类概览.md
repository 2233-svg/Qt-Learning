# QtTaskTree::For：用 Iterator 描述循环执行

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree`

`For` 是 QtTaskTree 的循环结构入口。它持有一个 `Iterator`，并必须通过 `>> Do { ... }` 指定循环体，组合结果是一个可放进 recipe 的 `Group`。

## 使用方式

```cpp
const Group recipe {
    For(RepeatIterator(3)) >> Do {
        task
    }
};
```

`Iterator` 决定迭代次数、停止条件或当前值来源；`Do` 决定每次迭代运行哪些任务。若使用 `ListIterator<T>`，可在 `Do` 内的任务 setup/done handler 中读取当前元素。

## 边界

`For` 本身不是完整任务，缺少 `Do` 体无法运行。循环结果由生成的组及其工作流策略决定：某轮失败时是否继续取决于 body 中的策略设置。无限迭代必须依赖任务失败、取消或外部条件来停止，否则会一直运行。

## API 速查表

| API | 语义与边界 |
|---|---|
| `For(const Iterator &iterator)` | 构造循环头。 |
| `operator>>(For, Do)` | 把循环头与 body 合成为 `Group`。 |
| `RepeatIterator(count)` | 固定次数循环。 |
| `ListIterator<T>(list)` | 按列表元素循环，并可在 body handler 中访问当前元素。 |
| `UntilIterator(condition)` | 每轮前检查条件。 |
| `ForeverIterator()` | 无限循环，需配合策略、取消或任务结果停止。 |
