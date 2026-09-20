# QtTaskTree::Group
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::Group`

## 作用定位

`Group` 是 TaskTree 最常用的组合节点：它把若干 `GroupItem` 组织成一个可执行单元。组内可以指定顺序/并行执行、嵌套子组、插入存储、任务、循环和条件。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 基类：`ExecutableItem`

## API 速查

| API | 说明 |
| --- | --- |
| `Group(const GroupItems &children)` | 用已有子项列表构造组。 |
| `Group(std::initializer_list<GroupItem>)` | 用 DSL 初始化列表构造组。 |

## 使用场景
- 表达一段完整工作流：初始化 -> 异步请求 -> 处理结果 -> 收尾。
- 把多个任务封装成可复用 recipe。
- 嵌套顺序和并行逻辑。

## 常见坑与经验

- 组默认语义要结合放入的 `sequential`、`parallel` 或 `ParallelLimit` 理解。
- 子组失败如何影响父组，取决于 workflow policy 和组合节点；不要假设所有失败都继续。
- 组里 lambda 捕获对象时，要考虑任务树可能异步运行很久。

## 知识点覆盖

- TaskTree 分层组合
- 顺序/并行混合 recipe
- 组结果和错误传播
- 可复用工作流片段
