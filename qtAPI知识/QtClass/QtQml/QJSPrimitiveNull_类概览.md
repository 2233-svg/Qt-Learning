# QJSPrimitiveNull：显式表示 JavaScript 的 null

> Qt 6.11.1 · 可通过 `#include <QJSPrimitiveValue>` 使用 · 模块：`Qt6::Qml`

`QJSPrimitiveNull` 是空标记类型。它没有数据和成员函数，作用是让 C++ 调用点明确表达“构造 JavaScript 的 `null`”，而不是 C++ 空指针、无效 `QVariant` 或 JavaScript `undefined`。

```cpp
#include <QJSPrimitiveValue>
#include <QDebug>

QJSPrimitiveValue value(QJSPrimitiveNull{});
qDebug() << value.type();       // QJSPrimitiveValue::Null
qDebug() << value.toString();   // "null"
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

## 它解决的歧义

| 表达 | JavaScript/Qt 含义 | 常见业务解释 |
| --- | --- | --- |
| `QJSPrimitiveNull{}` | JavaScript `null` | 字段存在，值明确为空。 |
| `QJSPrimitiveUndefined{}` | JavaScript `undefined` | 没有赋值、缺少字段或未知。 |
| 默认 `QVariant()` | 无效 Variant | Qt 元类型层面没有值。 |

三者转布尔都可能得到假，却不能互换。更新接口中，`null` 常表示“清空字段”，而 `undefined` 常表示“不要修改字段”。

## 边界与配合

- 它不是 `std::nullptr_t`，也不是任何可解引用指针。
- 放进 `QJSPrimitiveValue` 后可跨 engine 和线程传递，因为 primitive 不依赖 JS 堆。
- `QJSPrimitiveValue::toVariant()` 会将它转为承载 `nullptr` 的有效 `QVariant`；默认 primitive 的 `undefined` 则转为无效 Variant。
- 要在脚本对象中设置 null，可用 `QJSValue(QJSValue::NullValue)`；不要混入 C++ 指针的所有权语义。

## API 速查表

| 项目 | 用途 | 语义与边界 |
| --- | --- | --- |
| `QJSPrimitiveNull{}` | `null` 标记值 | 没有成员状态，只表达 JavaScript 空值。 |
| `QJSPrimitiveValue(QJSPrimitiveNull{})` | 创建无 engine 的 null | `type()` 为 `Null`，可跨线程、engine 使用。 |
| `QJSPrimitiveValue::toString()` | 得到脚本文本形式 | null 返回 `"null"`。 |
| `QJSPrimitiveValue::toBoolean()` | 按 JS 转布尔 | null 为 false，但不等于 undefined。 |
| `QJSPrimitiveValue::toVariant()` | 转 Qt Variant | 得到 `nullptr` Variant，不是无效 Variant。 |
| `QJSValue(QJSValue::NullValue)` | 创建通用 JS null | 需要同对象/函数协作时使用。 |

这个类型很小，但它使“明确清空”与“没有提供值”在 C++ 接口中可被准确区分。
