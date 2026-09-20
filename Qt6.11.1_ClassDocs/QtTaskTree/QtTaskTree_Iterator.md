# QtTaskTree::Iterator
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::Iterator`

## 作用定位

`Iterator` 是 TaskTree 循环的抽象状态。它记录当前第几次迭代，并由派生类决定何时继续、何时结束、当前值是什么。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 派生：`ListIterator`、`RepeatIterator`、`ForeverIterator`、`UntilIterator`

## API 速查

| API | 说明 |
| --- | --- |
| `iteration()` | 返回当前迭代编号，常用于日志、进度或构造重试延迟。 |

## 使用场景

- `For(iterator) >> Do{...}` 的循环控制。
- 给重试、批处理、轮询提供统一迭代状态。
- 在循环体中根据第几次执行决定行为。

## 常见坑与经验

- `iteration()` 是运行时状态，不是构造时固定值。
- 迭代器对象如果携带外部数据，要保证数据生命周期覆盖任务运行。
- 循环的退出语义来自具体派生类，读基类文档不够。

## 知识点覆盖

- TaskTree 循环状态
- 迭代次数
- 派生迭代器策略
