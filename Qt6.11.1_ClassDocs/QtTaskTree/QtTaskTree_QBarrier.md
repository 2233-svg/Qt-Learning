# QtTaskTree::QBarrier
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QBarrier`

## 作用定位

`QBarrier` 是一个计数式异步关卡任务：启动后等待外部多次 `advance()`，达到 `limit()` 后发出完成结果。它适合把多个外部事件汇聚成 TaskTree 中的一个完成点。

## 类说明

- 头文件：`#include <qbarriertask.h>`
- 继承：`QObject`
- 派生：`QStartedBarrier`

## API 速查

| API | 说明 |
| --- | --- |
| `start()` | 开始等待关卡推进。 |
| `advance()` | 推进一次计数。 |
| `setLimit()` / `limit()` | 设置/读取需要推进的次数。 |
| `current()` | 当前已经推进的次数。 |
| `isRunning()` | 是否正在等待。 |
| `stopWithResult(result)` | 以指定结果提前结束。 |
| `result()` | 当前结束结果，可为空。 |
| `done(result)` | 关卡完成时发出。 |

## 使用场景

- 等待多个信号都到达后继续。
- 并行外部操作不方便直接放进 TaskTree 时，用 barrier 聚合。
- 等待 UI 多个步骤完成。

## 常见坑与经验

- `advance()` 次数达到 limit 后才完成，limit 配错会导致任务树挂住。
- 关卡运行前推进是否有效要按实际状态设计，最好 start 后再连接外部触发。
- 提前失败时用 `stopWithResult()`，不要只销毁对象。

## 知识点覆盖

- 异步计数关卡
- 外部事件汇聚
- 提前完成和失败
