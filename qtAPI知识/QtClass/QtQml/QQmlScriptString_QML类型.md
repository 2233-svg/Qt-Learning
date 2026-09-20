# QQmlScriptString：把 QML 表达式本身连同作用域交给 C++

> Qt 6.11.1 | `#include <QQmlScriptString>` | CMake: `Qt6::Qml`

通常 QML 看到 `property: expression` 会立即建立绑定，并把 expression 的计算结果交给属性。`QQmlScriptString` 改变了这个规则：当 QObject 属性的类型是它时，C++ 接收到的是表达式文本及其原始 QML 上下文和作用域，能决定何时、是否以及怎样执行。

它解决了延迟求值和可控执行的问题。例如规则组件要保存一条由 QML 写出的计算表达式，等数据齐备、用户点击或特定事件发生时才运行，而不是组件加载时就计算一次。

## 把“结果”改为“脚本”

```cpp
class RuleRunner : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QQmlScriptString rule READ rule WRITE setRule)

public:
    QQmlScriptString rule() const { return m_rule; }
    void setRule(const QQmlScriptString &rule) { m_rule = rule; }

    QVariant run()
    {
        QQmlExpression expression(m_rule);
        return expression.evaluate();
    }

private:
    QQmlScriptString m_rule;
};
```

```qml
RuleRunner {
    rule: account.balance > 0 ? "approved" : "review"
}
```

这个赋值不会把三元表达式的字符串结果直接存入 `rule`；`QQmlScriptString` 保存的是表达式和它被声明时可见的 context/scope。随后 `QQmlExpression(m_rule).evaluate()` 才在那个环境中执行。

因此它用于“把 QML 当作受控规则输入”，而不是普通配置字段。表达式可以访问对象、调用方法并产生副作用；是否允许不受信任的 QML 写入该属性是安全设计问题，不能只靠该类型解决。

## 求值时机由 C++ 决定

`QQmlScriptString` 本身没有公开的“执行”成员函数。用 `QQmlExpression` 求值时，应在正确线程、正确生命周期内检查错误，并避免高频重复构造/执行复杂脚本：

```cpp
QQmlExpression expression(m_rule);
const QVariant value = expression.evaluate();
if (expression.hasError())
    qmlWarning(this, expression.error()) << "rule evaluation failed";
```

空对象 `isEmpty()` 为 true，不能把它等同于 QML 的 `undefined` 或 `null`。后两者是有效的脚本文字，分别用 `isUndefinedLiteral()` 和 `isNullLiteral()` 识别。

## 文字量快捷路径

当需求只接受常量而不想运行任意脚本，先尝试 literal API：

```cpp
bool ok = false;
const qreal interval = m_rule.numberLiteral(&ok);
if (!ok)
    return; // 不是数字字面量，不要误把返回的 0.0 当作合法值
```

`booleanLiteral(&ok)` 在失败时返回 `false`，这和合法字面量 `false` 相同，所以 `ok` 不是可选装饰。`numberLiteral(&ok)` 同理，失败值 `0.0` 与合法数值零无法仅靠返回值区分。`stringLiteral()` 失败时返回 null `QString`，不要将其与空字符串混为一谈。

literal API 只判断内容是否为该种字面量，不会执行 `1 + 2`、`config.enabled` 或函数调用。需要计算表达式时仍然使用 `QQmlExpression`。

## 生命周期与可比性

该类型是可复制值类型，内部共享脚本相关数据；复制不会把表达式变成独立的纯文本。相等比较判断两个 `QQmlScriptString` 是否相等，适合缓存和属性变更判断，但不应据此推测两段脚本“运行效果相同”。

它由 QML 引擎在属性赋值时创建。业务代码无法用公开构造函数从任意 QString 拼出一个具有正确 QML context 的实例；空构造只得到空值。若需求是执行 C++ 生成的脚本，应明确提供 `QQmlContext` 和 scope 来构造 `QQmlExpression`，不要伪造 `QQmlScriptString`。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQmlScriptString()` | 构造空脚本值 | 不能由此创建带 QML 上下文的脚本 |
| 复制、赋值、`==` / `!=` | 传递和比较封装的脚本值 | 相等不表示运行结果或副作用相同 |
| `isEmpty()` | 是否为空值 | 与 `null`、`undefined` 字面量不同 |
| `isUndefinedLiteral()` | 是否恰为 `undefined` | 不执行表达式 |
| `isNullLiteral()` | 是否恰为 `null` | 不执行表达式 |
| `stringLiteral()` | 取得字符串字面量 | 非字符串时返回 null `QString`，不是普通空字符串 |
| `numberLiteral(bool *ok)` | 取得数字字面量 | 必须检查 `ok`，失败返回 `0.0` |
| `booleanLiteral(bool *ok)` | 取得布尔字面量 | 必须检查 `ok`，失败返回 `false` |
| `QQmlExpression(QQmlScriptString)` | 按保存的上下文创建可求值表达式 | 求值可能报错、有副作用，也应遵守对象线程边界 |

## 相关类型

- `QQmlExpression`：实际执行 `QQmlScriptString` 的表达式对象。
- `QQmlContext` 与 QML scope：脚本保存并依赖的名字解析环境。
- `QQmlError`：表达式求值失败时的结构化错误信息。
