# QtTaskTree::Do
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::Do`

## 作用定位

`Do` 是循环或条件结构中的执行体标记。它让 `For >> Do{...}`、`When >> Do{...}` 这类 DSL 能把“控制条件”和“要执行的子项”分开。

## 类说明

- 头文件：`#include <qtasktree.h>`

## API 速查

| API | 说明 |
| --- | --- |
| `Do(const GroupItems &children)` | 用子项列表构造执行体。 |
| `Do(std::initializer_list<GroupItem>)` | 初始化列表版本。 |

## 使用场景

- `For(iterator) >> Do{...}` 的循环体。
- `When(barrier) >> Do{...}` 的触发后动作。
- 让 DSL 读起来接近自然语言。

## 常见坑与经验

- `Do` 只是 body，不会自己启动循环或等待信号。
- 执行体里访问迭代器当前值时，要确认值的生命周期来自 iterator 而不是临时对象。

## 知识点覆盖

- TaskTree DSL body 节点
- 控制节点与执行体分离
- 循环/触发结构组合
