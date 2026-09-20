# QJSPrimitiveUndefined：显式表示 JavaScript 的 undefined

> Qt 6.11.1 · 可通过 `#include <QJSPrimitiveValue>` 使用 · 模块：`Qt6::Qml`

`QJSPrimitiveUndefined` 是空标记类型，用于明确构造 JavaScript `undefined`。它没有成员函数；价值在于把“未定义的脚本值”写成可读、可区分的 C++ 代码。

```cpp
#include <QJSPrimitiveValue>
#include <QDebug>

QJSPrimitiveValue notProvided(QJSPrimitiveUndefined{});
qDebug() << notProvided.type();      // QJSPrimitiveValue::Undefined
qDebug() << notProvided.toString();  // "undefined"
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

## undefined 表达的是“未提供”

`undefined` 通常表示值尚未定义、字段不存在、调用方没传参数或转换失败；它不等于 `null`：

```cpp
QJSPrimitiveValue omitted(QJSPrimitiveUndefined{});
QJSPrimitiveValue explicitlyEmpty(QJSPrimitiveNull{});

const bool loose = omitted.equals(explicitlyEmpty);           // true
const bool strict = omitted.strictlyEquals(explicitlyEmpty);  // false
```

更新 API 常用 `undefined` 表示“保持原值”，用 `null` 表示“清空原值”。若将二者都压成 C++ 的空状态，调用方意图就会丢失。

## 与默认构造和 QVariant 的关系

默认构造 `QJSPrimitiveValue` 同样为 `Undefined`，但在参数处使用 `QJSPrimitiveUndefined{}` 更明确。它转为 `QVariant` 时会得到无效 Variant；`QJSPrimitiveNull{}` 转出的是 `nullptr` Variant。

它不是未初始化内存，而是一个确定的 JavaScript 值。它不依赖 engine，放进 `QJSPrimitiveValue` 后可跨线程和 engine 传递。`toDouble()` 为 `NaN`、`toInteger()` 为 `0`、`toBoolean()` 为 `false`，但这些转换结果不能反推原值确实是 undefined。

还要注意：`QJSValue::isUndefined()` 对 engine 已销毁的失效脚本句柄也会返回真。因此不能仅凭它区分“脚本刻意返回 undefined”与“持久化的 engine 绑定值已失效”。

## API 速查表

| 项目 | 用途 | 语义与边界 |
| --- | --- | --- |
| `QJSPrimitiveUndefined{}` | undefined 标记值 | 没有成员状态，只表达明确的 JS 未定义值。 |
| `QJSPrimitiveValue()` | 默认创建 undefined | 参数语义中更推荐显式标记。 |
| `QJSPrimitiveValue(QJSPrimitiveUndefined{})` | 显式创建 undefined | 可跨线程、engine，因其不依赖 JS 堆。 |
| `QJSPrimitiveValue::type()` | 判断 `Undefined` | 不要用转换后的 0 或 false 代替类型判断。 |
| `QJSPrimitiveValue::toDouble()` | 转数值 | undefined 转为 `NaN`。 |
| `QJSPrimitiveValue::toInteger()` / `toBoolean()` | 转整数/布尔 | 得到 0 / false，undefined 身份会丢失。 |
| `QJSPrimitiveValue::toVariant()` | 转 Qt Variant | 结果为无效 Variant。 |
| `QJSValue(QJSValue::UndefinedValue)` | 创建通用 JS undefined | 需要同脚本对象、函数协作时使用。 |

`QJSPrimitiveUndefined` 的作用不是制造“空”，而是保存“调用方没有提供一个脚本值”这一层语义。
