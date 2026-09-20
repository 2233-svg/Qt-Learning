# QtTaskTree::When
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::When`

## 作用定位

`When` 用来把“某个 barrier 或任务信号发生”转换成 TaskTree 的触发节点，再通过 `>> Do{...}` 指定触发后的动作。它常用于等待外部条件满足后继续流程。

## 类说明

- 头文件：`#include <qbarriertask.h>`

## API 速查

| API | 说明 |
| --- | --- |
| `When(kicker, policy)` | 用 barrier kicker 创建触发节点，并指定工作流策略。 |
| `When(customTask, signal, policy)` | 监听自定义任务的某个信号作为触发来源。 |
| `operator>>(When, Do)` | 把触发条件和执行体组合成 `Group`。 |

## 使用场景

- 等多个外部事件累计到阈值后启动子流程。
- 某个 QObject 信号出现后运行一段任务。
- 用 barrier 把分散的异步完成点汇聚回 TaskTree。

## 常见坑与经验
- `When` 只定义触发，不定义动作；动作在 `Do` 中。
- 被监听对象的生命周期必须覆盖等待过程。
- 触发策略要和错误处理一致：遇到失败是停、继续还是取消，需要明确。

## 知识点覆盖

- barrier/信号触发任务
- `When >> Do` DSL
- 外部事件汇聚
- workflow policy
