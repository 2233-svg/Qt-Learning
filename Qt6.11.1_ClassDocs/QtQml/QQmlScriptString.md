# QQmlScriptString
> Qt 6.11.1 · Qt QML · 来自 `QQmlScriptString`

## 作用定位

`QQmlScriptString` 表示 QML 中传给 C++ 的脚本文本。它保留“这是脚本表达式，而不是普通字符串”的语义，C++ 可以检查它是否为字面量，也可以用 `QQmlExpression` 在合适上下文中求值。

它常用于自定义 QML 类型的属性：你希望 QML 用户写一段表达式，C++ 稍后决定如何执行。

## 类说明

- 头文件：`#include <QQmlScriptString>`
- CMake：链接 `Qt6::Qml`
- 继承：无公开 QObject 继承

## API 速查

| API | 说明 |
| --- | --- |
| 构造/赋值/比较 | 值语义保存脚本文本引用。 |
| `isEmpty()` | 是否为空脚本。 |
| `isNullLiteral()` | 是否是 `null` 字面量。 |
| `isUndefinedLiteral()` | 是否是 `undefined` 字面量。 |
| `booleanLiteral(ok)` | 如果是布尔字面量，取出 bool。 |
| `numberLiteral(ok)` | 如果是数字字面量，取出 qreal。 |
| `stringLiteral()` | 如果是字符串字面量，取出字符串。 |

## 使用场景

- 自定义 QML 属性接收表达式，而不是立即求值结果。
- 延迟执行用户提供的表达式。
- 在执行前快速识别常量字面量，避免创建表达式求值器。

## 常见坑与经验

- `QQmlScriptString` 本身不执行脚本；执行要交给 `QQmlExpression`。
- 字符串字面量和任意表达式结果为字符串不是同一回事，`stringLiteral()` 只识别字面量。
- 求值时要传入正确 context 和 scope，否则表达式里的 id、属性名无法解析。
- 动态脚本是代码执行入口，要谨慎控制能访问的上下文对象。

## 知识点覆盖

- QML 脚本属性
- 字面量识别
- 延迟表达式求值
- 与 `QQmlExpression` 的配合
