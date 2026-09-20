# QtTaskTree::Iterator：For 循环的运行期迭代状态

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree`

`Iterator` 是 `For(iterator) >> Do { ... }` 的基类。它负责告诉任务树是否还有下一轮，以及在 handler 内提供当前迭代序号。

## 核心语义

用户通常不直接构造 `Iterator`，而是使用 `RepeatIterator`、`ListIterator`、`UntilIterator` 或 `ForeverIterator`。这些对象在 recipe 构造期只是描述循环；真正的当前轮次由运行中的 `QTaskTree` 激活。

`iteration()` 只能在 `Do` body 内部的任务或组 handler 中调用。离开运行上下文调用它没有活跃迭代，文档明确提示可能崩溃。并行 body 中，setup handler 的迭代号与对应 done handler 匹配，但多个 done handler 到达顺序不保证递增。

## API 速查表

| API | 语义与边界 |
|---|---|
| `iteration()` | 返回当前 handler 所属的迭代序号；只能在对应 `Do` body 的运行期 handler 内调用。 |
| `Iterator::Condition` | `std::function<bool(qsizetype)>`，用于条件型迭代器；参数为迭代序号。 |
| `Iterator::ValueGetter` | 内部用于按轮次取得当前值指针，`ListIterator` 借此提供 `operator*`。 |
| 复制/赋值 | 迭代器是可复制的 recipe 值；当前状态由运行中的树激活。 |
| 并行 body | done handler 的完成顺序可能乱序，但 `iteration()` 仍对应原始迭代。 |
