# QQmlExpression
> Qt 6.11.1 · Qt QML · 来自 `QQmlExpression`

## 作用定位

`QQmlExpression` 用来在指定 `QQmlContext` 和 scope object 下求值一段 QML/JS 表达式。它不是完整组件加载器，而是“在 QML 作用域里算一段表达式”的工具。

它适合表达式配置、调试、少量动态逻辑；不适合承载大段业务脚本。

## 类说明

- 头文件：`#include <QQmlExpression>`
- CMake：链接 `Qt6::Qml`
- 继承：`QObject`
- 输入：上下文、作用域对象、表达式文本或 `QQmlScriptString`

## API 速查

| API | 说明 |
| --- | --- |
| 构造函数 | 可空构造，也可用 context、scope、表达式字符串或 `QQmlScriptString` 构造。 |
| `setExpression()` / `expression()` | 设置或读取表达式文本。 |
| `evaluate(valueIsUndefined)` | 求值，返回 `QVariant`；可区分结果是否为 JS `undefined`。 |
| `setNotifyOnValueChanged()` | 开启依赖变化追踪，依赖值变更时发出 `valueChanged()`。 |
| `notifyOnValueChanged()` | 查询是否启用变化通知。 |
| `valueChanged()` | 表达式依赖值变化时发出。 |
| `hasError()` / `error()` / `clearError()` | 处理求值错误。 |
| `context()` / `engine()` / `scopeObject()` | 查询表达式求值环境。 |
| `setSourceLocation()` | 设置错误定位用的 URL、行、列。 |
| `sourceFile()` / `lineNumber()` / `columnNumber()` | 读取来源定位。 |

## 使用场景

- 在 C++ 中求值用户配置的简单 QML 表达式。
- 基于 QML 上下文读取绑定结果。
- 调试某个 scope object 下的表达式解析。
- 需要跟踪表达式依赖变化时做轻量响应。

## 常见坑与经验

- 表达式能访问上下文中的名字，因此安全边界取决于你给它的 context 和 scope。
- `evaluate()` 返回无效 QVariant、null、undefined 都可能有不同含义，要使用 `valueIsUndefined` 区分。
- 开启 `notifyOnValueChanged` 会建立依赖跟踪，不要给大量临时表达式随意打开。
- 动态表达式难以静态分析，复杂逻辑更适合写成 QML 组件或明确的 C++ API。
- 错误定位要设置 `setSourceLocation()`，否则日志很难回到配置文件源头。

## 知识点覆盖

- QML 上下文中的表达式求值
- scope object 与名字解析
- 表达式依赖跟踪
- undefined/null/无效 QVariant 区分
- 错误定位和调试
