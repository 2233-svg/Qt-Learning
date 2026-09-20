# QtTaskTree::Else：条件表达式的默认分支

> Qt 6.11.1 · `#include <qconditional.h>` · 模块：`Qt6::TaskTree`

`Else` 是条件表达式的兜底 body。当前面的 `If` 和所有 `ElseIf` 条件都失败时，运行它包含的 children。

## 使用方式与边界

`Else` 必须跟在 `Then` 后面，不能作为普通 `Group` 子项独立表达条件。它没有条件任务，只提供默认 body；被执行时，其 children 的执行结果就是整个条件表达式的结果。

```cpp
If(check) >> Then {
    normalPath
} >> Else {
    fallbackPath
}
```

## API 速查表

| API | 语义与边界 |
|---|---|
| `Else(const GroupItems &children)` | 用元素列表构造默认分支 body。 |
| `Else(std::initializer_list<GroupItem>)` | 常用初始化列表写法。 |
| 前置要求 | 必须跟在 `Then` 之后。 |
| 执行条件 | 所有前置条件均失败。 |
| 结果 | children 的结果成为整个条件表达式结果。 |
