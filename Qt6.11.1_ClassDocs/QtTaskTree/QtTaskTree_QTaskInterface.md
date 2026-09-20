# QtTaskTree::QTaskInterface
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QTaskInterface`

## 作用定位

`QTaskInterface` 是自定义任务向 TaskTree 报告完成结果的桥。适配器启动任务后，任务最终通过它的 `reportDone()` 把 `DoneResult` 交回调度器。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `reportDone(result)` | 向 TaskTree 报告当前任务完成、失败或取消等结果。 |
| `event(event)` | 内部事件分发，TaskTree 用它把完成报告切回合适上下文。 |

## 使用场景

- 编写自定义 task adapter。
- 把外部异步对象的完成信号接回 TaskTree。
- 对复杂任务手动控制何时报告完成。

## 常见坑与经验
- 每个任务通常只能报告一次完成；重复报告会破坏调度语义。
- 不要长期保存 interface 指针超过任务生命周期。
- 跨线程报告完成时，依赖 Qt 事件投递，目标线程需要事件循环。

## 知识点覆盖

- 自定义任务完成报告
- DoneResult 传播
- Qt 事件投递与线程边界
