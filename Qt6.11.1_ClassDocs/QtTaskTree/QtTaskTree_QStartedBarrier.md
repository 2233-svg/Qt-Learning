# QtTaskTree::QStartedBarrier
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QStartedBarrier`

## 作用定位

`QStartedBarrier` 是启动即进入运行状态的 barrier 变体，适合在 recipe 中更自然地表示“等这些外部启动/触发点完成”。它继承 `QBarrier`，保留 limit 和 done 语义。

## 类说明

- 头文件：`#include <qbarriertask.h>`
- 基类：`QBarrier`

## API 速查

| API | 说明 |
| --- | --- |
| `QStartedBarrier(parent)` | 创建默认 limit 的启动关卡。 |
| `QStartedBarrier(limit, parent)` | 创建指定阈值的启动关卡。 |
| `BarrierKickerGetter` | 获取推进 barrier 的回调/对象。 |
| `QStoredBarrier` | 与 TaskTree storage 结合使用的 barrier 形态。 |

## 使用场景

- 在 `When` 中等待一组外部 kick。
- 把启动后才出现的多个异步完成点集中到一个节点。
- 与 `Storage` 一起保存 barrier，供多个任务推进。

## 常见坑与经验

- limit 必须和实际会调用 kicker 的次数一致。
- 如果多个线程推进 barrier，要确认对象线程和信号连接方式。
- 用 storage 保存 barrier 时，避免在运行结束后继续触发旧 barrier。

## 知识点覆盖

- 启动型 barrier
- barrier kicker
- 与 Storage/When 的组合
