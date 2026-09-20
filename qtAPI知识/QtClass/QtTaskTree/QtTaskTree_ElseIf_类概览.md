# QtTaskTree::ElseIf：条件表达式中的备用条件

> Qt 6.11.1 · `#include <qconditional.h>` · 模块：`Qt6::TaskTree`

`ElseIf` 是 `If >> Then` 之后的备用条件。只有前面的条件失败时，它的条件任务才会被执行；它必须前接一个 `Then` 分支，也必须后接一个新的 `Then` 分支。

## 使用方式

```cpp
If(primaryCheck) >> Then {
    primaryPath
} >> ElseIf(secondaryCheck) >> Then {
    secondaryPath
} >> Else {
    fallbackPath
}
```

和 `If` 一样，`ElseIf` 可以接收 `ExecutableItem`，也可以接收同步 handler 并由库包装成同步条件任务。

## API 速查表

| API | 语义与边界 |
|---|---|
| `ElseIf(const ExecutableItem &condition)` | 用异步任务作为备用条件。 |
| `ElseIf(handler)` | 用同步 handler 作为备用条件。 |
| `Then >> ElseIf >> Then` | 合法位置；不能单独使用，也不能缺少后续 `Then`。 |
| 条件成功 | 执行紧随的 `Then` body，后续分支跳过。 |
| 条件失败 | 继续尝试后续 `ElseIf` 或 `Else`。 |
