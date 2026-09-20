# QTest::ThrowOnSkipEnabler
> Qt 6.11.1 · Qt Test · 来自 `QTest::ThrowOnSkipEnabler`

## 1. 先建立直觉

`ThrowOnSkipEnabler` 让 `QSKIP` 这类跳过测试的动作在当前作用域内通过异常表达。它常用于测试辅助函数：深层检测到环境不满足时，可以直接把“跳过”传回 Qt Test，而不是继续执行无意义步骤。

## 2. 类说明

保留类说明：这些 API 来自 `QTest::ThrowOnSkipEnabler`，属于 Qt Test 模块，用于临时启用跳过测试时抛异常模式。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `ThrowOnSkipEnabler()` | 调用 `setThrowOnSkip(true)`。 |
| `~ThrowOnSkipEnabler()` | 调用 `setThrowOnSkip(false)`。 |

## 4. 使用场景

| 场景 | 为什么使用 |
| --- | --- |
| 环境检查在辅助函数深处 | 不满足条件时直接跳过当前测试。 |
| 平台/驱动/权限条件测试 | 把不可测和失败区分清楚。 |
| 需要 RAII 保证恢复 | 避免手动开关漏恢复。 |

## 5. 常见坑与经验

跳过不是成功也不是失败。不要用 skip 掩盖随机失败；只有环境确实不满足测试前提时才跳过。

作用域要小。长期启用会让辅助函数里某个意外 `QSKIP` 改变上层控制流，诊断起来不直观。

## 6. 知识点覆盖

- Qt Test skip 语义。
- 环境前提检查和测试可执行性。
- RAII 控制跳过异常模式。
