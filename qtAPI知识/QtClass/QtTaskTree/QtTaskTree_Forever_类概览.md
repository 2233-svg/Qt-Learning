# QtTaskTree::Forever：重复执行 body 直到策略停止

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree` · 继承：`ExecutableItem`

`Forever` 是无限循环的便捷写法，本质上等价于 `For(ForeverIterator()) >> Do { ... }`。它持续重复执行 children，直到 body 的工作流策略因成功、错误、取消或外部条件让循环停止。

## 使用场景

周期性轮询、持续消费队列、重试某个异步动作，都可以用 `Forever` 表达。但它不会自己睡眠或限速；如果需要间隔，应在 body 里加入 timeout task 或等待信号的结构。

```cpp
const ExecutableItem loop = Forever {
    timeoutTask(1s, DoneResult::Success),
    pollTask
};
```

## 停止边界

默认 body 会重复到某个任务失败为止。若 body 内设置 `continueOnError`，可能导致循环无法因错误停止；使用时要非常明确停止条件。和 `Do` 一样，直接放在 body 里的 `Storage` 或组处理器围绕整个循环生命周期，而不是每轮重新创建。

## API 速查表

| API | 语义与边界 |
|---|---|
| `Forever(const GroupItems &children)` | 构造无限循环体。 |
| `Forever(std::initializer_list<GroupItem>)` | 常用初始化列表写法。 |
| 等价形式 | `For(ForeverIterator()) >> Do { children }`。 |
| 默认停止 | body 中任务失败时停止。 |
| Storage/组处理器 | 直接子项按整个循环范围生效；每轮独立需再包 `Group`。 |
