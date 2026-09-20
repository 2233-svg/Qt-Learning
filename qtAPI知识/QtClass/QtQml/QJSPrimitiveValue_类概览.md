# QJSPrimitiveValue：脱离 JavaScript 堆的原始 JS 值

> Qt 6.11.1 · `#include <QJSPrimitiveValue>` · 模块：`Qt6::Qml`

`QJSPrimitiveValue` 保存 JavaScript 原始值，但不依附任何 `QJSEngine`。它解决的是“需要 JavaScript 的类型和强制转换语义，却不想创建或持有 JavaScript 堆对象”的问题。

它能表示 `undefined`、`null`、布尔、`int`、`double` 和 `QString`；不能表示对象、数组、函数、QObject 或 `Symbol`。

## 适用场景

- 在线程、队列或容器中传递脚本风格的简单结果。
- 在不同 engine 间传递标量配置，而不携带某台 engine 的生命周期。
- 在 C++ 中复现 JavaScript 的基本算术、比较和空值转换。

```cpp
#include <QJSPrimitiveValue>
#include <QDebug>

QJSPrimitiveValue absent; // undefined
QJSPrimitiveValue nullValue(QJSPrimitiveNull{});
QJSPrimitiveValue text(u"12"_s);

qDebug() << text.toInteger(); // 12
qDebug() << (nullValue + QJSPrimitiveValue(4)).toInteger(); // 4
qDebug() << absent.toDouble(); // NaN
```

它是普通值类型，可跨 engine 和线程使用并在任意线程销毁；这正是它与 `QJSManagedValue` 的分界。工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

## 不要把 JS 语义误认为 C++ 语义

四则运算和比较遵循 JavaScript primitive 的强制转换规则：

```cpp
QJSPrimitiveValue a(u"2"_s);
QJSPrimitiveValue b(3);
qDebug() << (a + b).toString(); // "23"，加号执行字符串拼接
qDebug() << (a - b).toDouble(); // -1，减号先转数字
```

`operator==` / `operator!=` 使用严格相等语义；想要 JavaScript 宽松 `==`，使用 `equals()`。`strictlyEquals()` 对 `NaN` 仍返回 false，不能把它作为普通数值相等比较。

## QVariant 与元类型边界

从 `QVariant` 或 `QMetaType` 构造时，仅接受未知类型、空指针、`bool`、`int`、`double` 和 `QString`。其他类型不会“尽力转换”，而是得到 `Undefined`。例如把 `qint64`、`QUrl`、`QDateTime` 直接传入时，必须自行检查结果类型。

`metaType()`、`data()`、`constData()`（Qt 6.6 起）用于元类型互操作。它们提供的指针指向对象内部存储，不可在对象销毁、移动或改值后保留。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QJSPrimitiveValue()` | 构造 `undefined` | 默认构造不是 `null`。 |
| `QJSPrimitiveValue(QJSPrimitiveUndefined{})` | 显式构造 `undefined` | 适合让接口调用点表达“未提供”。 |
| `QJSPrimitiveValue(QJSPrimitiveNull{})` | 显式构造 `null` | 与 undefined 和无效 Variant 不同。 |
| `QJSPrimitiveValue(bool/int/double/QString)` | 构造支持的 primitive | 整数只存为 `int`。 |
| `QJSPrimitiveValue(QVariant)` | 从 Variant 创建 | 不支持的元类型变成 `Undefined`。 |
| `QJSPrimitiveValue(QMetaType, data)` | 从元类型读取 | `data` 必须指向匹配且有效的对象。 |
| `type()` | 查询 primitive 类型 | 不触发转换。 |
| `toBoolean()` | JS 规则转布尔 | `null`、`undefined`、空字符串、零、`NaN` 为假。 |
| `toInteger()` | JS 规则转 int | `undefined` 和 `null` 都转为 0，类型身份会丢失。 |
| `toDouble()` | JS 规则转 double | `undefined`、不可解析字符串转为 `NaN`。 |
| `toString()` | JS 规则转字符串 | 保留 `"undefined"`、`"null"`、`"NaN"` 等脚本形式。 |
| `toVariant()` | 转 Variant | undefined 为无效 Variant，null 为 `nullptr` Variant。 |
| `to<Type>()` | 转指定 primitive 类型 | Qt 6.6 起，模板参数为 `Type`。 |
| `metaType()` / `data()` / `constData()` | 元类型互操作 | Qt 6.6 起；返回的内部指针不拥有数据。 |
| `equals(other)` | JS 宽松 `==` | 会发生字符串、数字、null/undefined 强制转换。 |
| `strictlyEquals(other)` | JS 严格 `===` | 通常用于确定性比较。 |
| `+ - * / %` | JS 基本算术 | `+` 可拼接字符串；无效转换会产生 `NaN`。 |
| `< > <= >=` | JS 关系比较 | `NaN` 与 undefined 不构成可排序的总序。 |
| `++ -- +value -value` | JS 一元运算 | 会隐式转换，业务模型中应谨慎使用。 |

`QJSPrimitiveValue` 的优势在于：值脱离 engine 仍保留 JavaScript primitive 语义。一旦需要对象身份、函数调用或异常状态，就应使用 `QJSValue` 或 `QJSManagedValue`。
