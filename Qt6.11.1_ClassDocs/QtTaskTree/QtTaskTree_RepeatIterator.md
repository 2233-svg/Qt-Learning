# QtTaskTree::RepeatIterator
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::RepeatIterator`

## 作用定位

`RepeatIterator` 用来重复执行固定次数。它是重试、定量批处理、固定轮询次数的简单迭代器。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 基类：`Iterator`

## API 速查

| API | 说明 |
| --- | --- |
| `RepeatIterator(qsizetype count)` | 指定循环执行次数。 |

## 使用场景

| 场景 | 说明 |
| --- | --- |
| 固定重试 | 最多尝试 N 次。 |
| 固定批次 | 按次数执行同一任务片段。 |
| 测试流程 | 重复执行相同 recipe 验证稳定性。 |

## 常见坑与经验

- `count` 为 0 时循环体不会执行，业务上要明确这是合法跳过还是配置错误。
- 固定重试常要配合延迟和失败条件，避免瞬间打爆资源。
- 迭代编号可用于指数退避等策略。

## 知识点覆盖

- 固定次数循环
- 重试上限
- 迭代编号驱动策略
