# QtTaskTree::Then：条件成立后的分支体

> Qt 6.11.1 · `#include <qconditional.h>` · 模块：`Qt6::TaskTree`

`Then` 是 QtTaskTree 条件表达式里的“分支体”。它本身不是一个完整条件，也不应该单独放进 recipe；它必须跟在 `If` 或 `ElseIf` 后面，通过 `operator>>` 组合成可执行的条件项。

## 解决的问题

异步流程里经常需要“先跑一个条件任务，成功就执行 A，否则试 B 或执行兜底”。`Then` 把“条件成功后的子 recipe”包起来，让条件链保持声明式，而不是在 signal 回调里手写分支状态机。

典型形态是：

```cpp
const Group recipe {
    If(checkCache) >> Then { loadFromCache }
        >> ElseIf(checkNetwork) >> Then { fetchFromNetwork, saveCache }
        >> Else { showError }
};
```

## 语义边界

前面的 `If` 或 `ElseIf` 条件以成功结束时，`Then` 内的 children 会被执行；这个分支体的执行结果就是整个条件表达式当前命中分支的结果。如果条件失败，则跳过该 `Then`，继续检查后续 `ElseIf` 或执行 `Else`。

`Then` 可后接 `ElseIf` 或 `Else`。缺少前置 `If`/`ElseIf` 时没有语义入口；缺少后续分支时，条件失败的结果由条件表达式自身规则处理，而不是由 `Then` 兜底。

## API 速查表

| API | 语义与边界 |
|---|---|
| `Then(const GroupItems &children)` | 用一组 `GroupItem` 构造分支体；只用于条件表达式。 |
| `Then(std::initializer_list<GroupItem>)` | 常用 recipe 写法，直接写 `Then { task1, task2 }`。 |
| `If(condition) >> Then { ... }` | 条件成功时执行该分支体。 |
| `ElseIf(condition) >> Then { ... }` | 前面分支未命中且当前条件成功时执行。 |
| `ThenItem >> ElseIf(...)` | 在当前分支后继续挂接下一个条件。 |
| `ThenItem >> Else { ... }` | 增加兜底分支。 |
| 分支体结果 | `Then` 内 children 的执行结果会成为命中分支的结果。 |
| 单独使用 `Then` | 没有前置条件，不是完整可执行项。 |
