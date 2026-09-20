# QTest::ThrowOnFailEnabler
> Qt 6.11.1 · Qt Test · 来自 `QTest::ThrowOnFailEnabler`

## 1. 先建立直觉

`ThrowOnFailEnabler` 是一个 RAII 开关：构造时启用“测试失败时抛异常”，析构时恢复为关闭。它让一段作用域内的 `QVERIFY`、`QCOMPARE` 等失败可以用异常方式中断控制流。

## 2. 类说明

保留类说明：这些 API 来自 `QTest::ThrowOnFailEnabler`，属于 Qt Test 模块，用于临时启用失败抛异常模式。

它适合测试辅助函数、嵌套断言或需要借助 C++ 控制流清理资源的场景。普通测试函数里通常不需要手动使用。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `ThrowOnFailEnabler()` | 调用 `setThrowOnFail(true)`，进入失败抛异常模式。 |
| `~ThrowOnFailEnabler()` | 调用 `setThrowOnFail(false)`，离开作用域时关闭该模式。 |

## 4. 典型流程

```cpp
{
    QTest::ThrowOnFailEnabler guard;
    helperThatUsesQCOMPARE();
}
```

作用域是重点：把 guard 放在尽可能小的范围，别影响同一测试函数后面的普通断言语义。

## 5. 使用场景

| 场景 | 为什么使用 |
| --- | --- |
| 测试辅助函数内部断言 | 失败时立即跳出深层调用。 |
| 需要异常边界统一处理 | 和已有异常清理逻辑配合。 |
| 临时改变 Qt Test 行为 | RAII 比手动开关更不容易忘记恢复。 |

## 6. 常见坑与经验

不要跨很大作用域启用。测试框架、清理函数和你自己的异常处理混在一起时，失败路径会变得难读。

RAII 对象本身很小，但改变的是全局/线程相关测试行为。并发测试或嵌套工具函数里要小心影响范围。

## 7. 知识点覆盖

- Qt Test 失败处理模式。
- RAII 开关和作用域恢复。
- 测试辅助函数里的断言控制流。
