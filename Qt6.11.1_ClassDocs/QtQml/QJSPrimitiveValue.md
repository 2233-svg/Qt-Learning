# QJSPrimitiveValue
> Qt 6.11.1 · Qt QML · 来自 `QJSPrimitiveValue`

## 作用定位

`QJSPrimitiveValue` 是不依赖 `QJSEngine` 的 JavaScript 原始值容器。它只覆盖 `undefined`、`null`、布尔、整数、double、字符串这些基础值，不表示对象、数组、函数或 QObject。

它适合在不想绑定引擎生命周期时保存 JS 基础值，也适合做轻量转换和比较。

## 类说明

- 头文件：`#include <QJSPrimitiveValue>`
- CMake：链接 `Qt6::Qml`
- 继承：无公开 QObject 继承
- 特点：可不依赖 JS 引擎独立存在

## API 速查

| API | 说明 |
| --- | --- |
| `Type` | `Undefined`、`Null`、`Boolean`、`Integer`、`Double`、`String`。 |
| 构造函数 | 从 undefined/null 标记、QString、bool、QVariant、double、int、元类型数据构造。 |
| `type()` | 读取当前原始值类别。 |
| `metaType()` / `data()` / `constData()` | Qt 6.6 起访问底层元类型和数据。 |
| `toBoolean()` / `toDouble()` / `toInteger()` / `toString()` | 按 JS 原始值规则转换。 |
| `to<type>()` | Qt 6.6 起模板化转换到指定原始值类型。 |
| `equals()` | JS 宽松相等。 |
| `strictlyEquals()` | JS 严格相等。 |
| 算术/比较运算符 | 按 JS 原始值规则执行 `+ - * /` 与比较。 |

## 使用场景

- 保存脚本计算得到的标量配置。
- 在不创建 `QJSEngine` 的库层处理 JS 风格原始值。
- 区分 `undefined`、`null` 和空字符串等容易混淆的状态。
- 做 JS 规则的基础比较或数值运算。

## 常见坑与经验

- JavaScript 没有真正的整数类型；`Integer` 是 Qt 为常见整数路径提供的表示。
- `Null` 和 `Undefined` 在业务语义上要分清：前者通常是显式空，后者是缺失。
- `operator+` 遵守 JS 语义，字符串参与时可能变成拼接，不是纯数学加法。
- 它不能表示对象。如果值可能是数组、函数或 QObject，请用 `QJSValue` 或 `QJSManagedValue`。

## 知识点覆盖

- JS 原始类型
- undefined/null 差异
- JS 转换和相等规则
- 无引擎值保存
- 元类型数据访问
