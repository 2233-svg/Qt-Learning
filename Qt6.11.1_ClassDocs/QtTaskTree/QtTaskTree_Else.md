# QtTaskTree::Else
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::Else`

## 作用定位

`Else` 是条件链的兜底分支：前面的 `If`/`ElseIf` 都不成立时执行。它没有自己的条件，语义上应只放真正的 fallback 工作。

## 类说明

- 头文件：`#include <qconditional.h>`

## API 速查

| API | 说明 |
| --- | --- |
| `Else(const GroupItems &children)` | 兜底执行给定子项列表。 |
| `Else(std::initializer_list<GroupItem>)` | 初始化列表版本。 |

## 使用场景

- 使用默认配置。
- 条件不满足时跳过主流程并做降级处理。
- 多分支流程里的最终 fallback。

## 常见坑与经验
- `Else` 不应放必须无条件执行的收尾逻辑；收尾更适合放在外层 group 的后续步骤或 done handler。
- 兜底分支也可能失败，要设计它的失败结果如何影响外层任务树。

## 知识点覆盖

- 条件兜底
- fallback 语义
- 分支失败传播
