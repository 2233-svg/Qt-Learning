# QTest::ThrowOnFailDisabler
> Qt 6.11.1 · Qt Test · 来自 `QTest::ThrowOnFailDisabler`

## 1. 先建立直觉

`ThrowOnFailDisabler` 是 `ThrowOnFailEnabler` 的反向作用域工具：构造时关闭“失败抛异常”，析构时重新启用。它用于你已经处在 throw-on-fail 环境中，但某一小段代码希望恢复传统 Qt Test 失败报告。

## 2. 类说明

保留类说明：这些 API 来自 `QTest::ThrowOnFailDisabler`，属于 Qt Test 模块，用于临时禁用失败抛异常模式。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `ThrowOnFailDisabler()` | 调用 `setThrowOnFail(false)`。 |
| `~ThrowOnFailDisabler()` | 调用 `setThrowOnFail(true)`，退出作用域时恢复。 |

## 4. 使用场景

| 场景 | 为什么使用 |
| --- | --- |
| 外层已启用 throw-on-fail | 局部测试希望按普通失败继续收集信息。 |
| 验证失败报告本身 | 测 Qt Test 集成时避免异常提前终止。 |
| 兼容旧辅助函数 | 老函数不适合异常式控制流。 |

## 5. 常见坑与经验

它析构时会重新打开 throw-on-fail，所以只应该在外层明确已经启用该模式时使用。若在普通环境中误用，离开作用域反而可能改变后续测试行为。

## 6. 知识点覆盖

- 失败抛异常模式的局部屏蔽。
- RAII 恢复顺序。
- 测试辅助代码的行为隔离。
