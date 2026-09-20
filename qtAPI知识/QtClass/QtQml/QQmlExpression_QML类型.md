# QQmlExpression：在指定 QML 上下文中求值一段 JavaScript

> Qt 6.11.1 · `#include <QQmlExpression>` · 模块：`Qt6::Qml` · 基类：`QObject`

`QQmlExpression` 用于在 C++ 中按某个 `QQmlContext` 和 scope object 的名称解析规则执行 JavaScript 表达式。它解决动态规则、可配置计算和需要复用 QML 上下文可见对象的场景。

它不是通用脚本沙箱，也不应成为把业务逻辑藏进字符串的默认机制。若表达式来自不可信输入，必须先设计权限与资源限制；它能访问该 context 与 scope 中可见的能力。

## 一次性计算

```cpp
#include <QQmlExpression>
#include <QQmlEngine>

QQmlExpression expression(
    engine.rootContext(), scopeObject, u"width * scaleFactor"_s);

bool undefined = false;
const QVariant result = expression.evaluate(&undefined);
if (expression.hasError()) {
    qWarning().noquote() << expression.error().toString();
} else if (undefined) {
    qWarning() << "expression returned undefined";
} else {
    qDebug() << result;
}
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

`evaluate()` 出错或表达式本身无效时返回无效 `QVariant`；表达式正常返回 JavaScript `undefined` 时也无法只靠返回 Variant 判断。因此同时检查 `hasError()` 与 `valueIsUndefined` 输出参数。

## context、scope 与 QQmlScriptString

构造函数的 `context` 决定能访问哪些 QML `id`、context property、导入和环境；可选 `scopeObject` 的属性也会进入表达式作用域。不要随意把 root context 和高权限 QObject 作为 scope 交给外部规则。

从 `QQmlScriptString` 构造时，脚本可携带自己的 context 与 scope；显式传入的 `context` 或 `scope` 会覆盖脚本中携带的对应信息。默认构造的 `QQmlExpression` 没有关联 context，始终是无效表达式，`evaluate()` 只会返回无效 Variant。

## 监听依赖变化会有成本

默认 `notifyOnValueChanged` 为 false，适合一次性求值，且不会追踪表达式依赖。设置为 true 后，Qt 会监控本次求值中用到的属性；表达式**至少先成功/尝试求值一次**，之后依赖值变化才会触发 `valueChanged()`。

这可用来实现动态计算，但它会建立绑定观察关系。短命、频繁创建的 expression 不要无谓开启通知；需要长期响应变化时也要让它的 parent、context 和 scope 都有明确生命周期。

## 错误与源位置

`error()` 返回最近一次 `evaluate()` 的 `QQmlError`，无错时为无效 error；`clearError()` 只清错误状态，不修复表达式文本或 context。`setSourceLocation(file, line, column)` 让脚本引擎在异常中报出准确来源，适合由配置文件或模板生成的表达式。

`context()` 和 `engine()` 会在关联对象已销毁时返回空。不要假设 expression 自己会延长 context、engine 或 scopeObject 的寿命。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QQmlExpression()` | 创建无效表达式 | 无 context，`evaluate()` 返回无效 Variant。 |
| `QQmlExpression(context, scope, text, parent)` | 按指定环境创建 | context 决定名称解析，scope 属性额外可见。 |
| `QQmlExpression(QQmlScriptString, ...)` | 从携带上下文的脚本创建 | 显式 context/scope 会覆盖 script 提供的值。 |
| `expression()` / `setExpression()` | 读写表达式文本 | 改文本不等于自动证明其安全或有效。 |
| `evaluate(valueIsUndefined)` | 执行表达式 | 无效 Variant 既可能是错误也可能是无效表达式；另查 error/undefined。 |
| `hasError()` / `error()` | 读取最近求值错误 | 无错误时 `error()` 为无效 `QQmlError`。 |
| `clearError()` | 清除已记录错误 | 不会修复表达式，也不重新计算。 |
| `notifyOnValueChanged` | 控制依赖监听 | 默认关闭；开启后需先 evaluate 才能产生变化通知。 |
| `valueChanged()` | 通知上次求值结果变化 | 基于被监控依赖，避免在槽中制造递归更新。 |
| `context()` / `engine()` / `scopeObject()` | 查询执行环境 | 关联 context/engine 销毁后可能为空。 |
| `setSourceLocation(file, line, column)` | 设置诊断源位置 | 改善脚本错误的定位质量。 |
| `sourceFile()` / `lineNumber()` / `columnNumber()` | 查询诊断位置 | 只有设置过 source location 才有意义。 |

`QQmlExpression` 最需要防范的不是语法错误，而是把作用域、依赖监听和返回值的三态语义混在一起。先界定谁可见、是否订阅变化、如何区分 undefined 与 error，动态表达式才可控。
