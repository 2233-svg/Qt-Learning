# QTest::ThrowOnSkipDisabler
> Qt 6.11.1 · Qt Test · 来自 `QTest::ThrowOnSkipDisabler`

## 1. 先建立直觉

`ThrowOnSkipDisabler` 用来在已经启用 throw-on-skip 的环境中，临时关闭“跳过测试时抛异常”。它是一个很窄的工具，主要服务 Qt Test 内部或高级测试框架集成。

## 2. 类说明

保留类说明：这些 API 来自 `QTest::ThrowOnSkipDisabler`，属于 Qt Test 模块，用于临时禁用跳过测试时抛异常模式。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `ThrowOnSkipDisabler()` | 调用 `setThrowOnSkip(false)`。 |
| `~ThrowOnSkipDisabler()` | 调用 `setThrowOnSkip(true)`，退出作用域时恢复。 |

## 4. 使用场景

| 场景 | 为什么使用 |
| --- | --- |
| 外层已启用 throw-on-skip | 局部代码希望按传统 skip 处理。 |
| 测试 skip 机制本身 | 避免异常打断验证流程。 |
| 框架适配层 | 在不同测试语义之间做短暂切换。 |

## 5. 常见坑与经验

和 `ThrowOnFailDisabler` 一样，它析构时会重新开启对应模式。不要在不清楚当前全局状态时随手使用，否则可能让后续测试行为和预期相反。

## 6. 知识点覆盖

- skip 异常模式的局部屏蔽。
- RAII 恢复和作用域控制。
- 高级测试框架集成边界。
