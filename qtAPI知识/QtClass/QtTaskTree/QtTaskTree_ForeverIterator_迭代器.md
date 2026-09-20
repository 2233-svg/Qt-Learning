# QtTaskTree::ForeverIterator：无限循环迭代器

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree` · 继承：`Iterator`

`ForeverIterator` 表示没有内建次数上限的 `For` 循环。它适合持续任务，但必须由 body 的工作流策略、任务结果、取消信号或外部条件来停止。

## 风险边界

最危险的组合是 `ForeverIterator` 加并行 `Do` body：任务树可能持续实例化新任务，直到资源耗尽。若需要周期性循环，通常在 body 中加入 timeout 或等待信号，并保持顺序执行。

`Forever { ... }` 是它的便捷替代写法；二者语义相近。

## API 速查表

| API | 语义与边界 |
|---|---|
| `ForeverIterator()` | 构造无限迭代器。 |
| `For(ForeverIterator()) >> Do { ... }` | 无限循环完整写法。 |
| 继承的 `iteration()` | 返回当前轮次序号；长时间运行时不要假设业务上永远不会变大。 |
| `Forever { ... }` | 常用便捷形式。 |
| 并行 body | 极易无限扩张任务数量，需要明确限流或避免。 |
