# QtTaskTree::ForeverIterator
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::ForeverIterator`

## 作用定位

`ForeverIterator` 是永不自然结束的迭代器。它让 `For(ForeverIterator{}) >> Do{...}` 这类循环持续运行，直到任务树被取消、外层策略中断或进程退出。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 基类：`Iterator`

## API 速查

| API | 说明 |
| --- | --- |
| `ForeverIterator()` | 创建无限迭代器。 |

## 使用场景
- 长期监听事件并处理。
- 持续轮询外部状态。
- 后台守护式任务。

## 常见坑与经验
- 必须设计取消出口；无限任务没有自然完成点。
- 循环体失败后是否重试要明确定义，否则可能形成快速失败循环。
- 适合与 `withCancel()`、`withTimeout()` 或外部 stop 信号组合。

## 知识点覆盖

- 无限循环
- 取消和关闭
- 常驻任务模式
