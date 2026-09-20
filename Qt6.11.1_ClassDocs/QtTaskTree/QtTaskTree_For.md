# QtTaskTree::For
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::For`

## 作用定位

`For` 把 `Iterator` 接入 TaskTree，用来重复执行一个 `Do` 执行体。它不是 C++ `for` 的语法糖，而是任务树运行时根据迭代器状态一次次调度子 recipe。

## 类说明

- 头文件：`#include <qtasktree.h>`

## API 速查

| API | 说明 |
| --- | --- |
| `For(const Iterator &iterator)` | 用指定迭代器创建循环控制节点。 |
| `operator>>(For, Do)` | 把循环控制和循环体组合成可执行 `Group`。 |

## 使用场景

- 对列表中的每个元素执行异步任务。
- 重试固定次数或直到条件满足。
- 把循环流程写在 recipe 层，而不是手动递归启动任务。

## 常见坑与经验
- 循环体异步完成后才进入下一次迭代，具体顺序/并行仍取决于内部 group。
- 无限或条件循环必须有取消/超时出口。
- 列表迭代时不要在循环体里破坏被迭代容器。

## 知识点覆盖

- 任务树循环
- Iterator 与 Do 组合
- 异步循环和退出条件
