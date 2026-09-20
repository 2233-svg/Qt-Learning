# QtTaskTree::Then
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::Then`

## 作用定位

`Then` 描述条件成立时要执行的子 recipe。它通常跟在 `If` 或 `ElseIf` 后面，使条件和动作在配方里形成清晰的一对。

## 类说明

- 头文件：`#include <qconditional.h>`

## API 速查

| API | 说明 |
| --- | --- |
| `Then(const GroupItems &children)` | 条件成立后执行给定子项列表。 |
| `Then(std::initializer_list<GroupItem>)` | 用初始化列表写分支体。 |

## 使用场景

- 条件检查通过后执行下载、解析、写入等后续任务。
- 把分支动作整理成小组，保持 recipe 可读。

## 常见坑与经验

- `Then` 只负责分支体，不负责条件本身。
- 分支体里如果有并行任务，要明确失败时是否中断整个条件结构。
- 分支体复用较多时，建议抽成返回 `Group` 的函数。

## 知识点覆盖

- 条件分支动作体
- recipe 可读性
- 分支组复用
