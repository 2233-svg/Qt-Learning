# QtTaskTree::If：以任务结果作为条件的分支入口

> Qt 6.11.1 · `#include <qconditional.h>` · 模块：`Qt6::TaskTree`

`If` 是 QtTaskTree 条件表达式的起点。它先执行一个条件任务；条件任务成功时执行后续 `Then` 分支，失败时进入 `ElseIf` 或 `Else`。

## 使用方式

```cpp
const Group recipe {
    If(checkTask) >> Then {
        successPath
    } >> Else {
        fallbackPath
    }
};
```

条件可以是任意 `ExecutableItem`，包括 `Group` 或由 `&&`、`||`、`!` 组合出的逻辑表达式。也可以传入同步 handler，构造器会把它包装成 `QSyncTask` 风格的条件。

## 结果语义

被选中分支的执行结果就是整个条件表达式的结果。若 `Then` 被执行，就不会再评估后续 `ElseIf` 或 `Else`。若条件失败且没有匹配的后续分支，表达式按失败路径结束。

## API 速查表

| API | 语义与边界 |
|---|---|
| `If(const ExecutableItem &condition)` | 用异步任务作为初始条件。 |
| `If(handler)` | 用同步 handler 作为条件，等价于包装为 `QSyncTask`。 |
| `operator>>(If, Then)` | 条件表达式必须接 `Then` 分支。 |
| 与 `ElseIf` / `Else` 组合 | 前一个条件失败时才继续。 |
| 条件成功 | 执行紧随的 `Then` body。 |
| 条件失败 | 跳过该 `Then`，继续尝试 `ElseIf` 或 `Else`。 |
