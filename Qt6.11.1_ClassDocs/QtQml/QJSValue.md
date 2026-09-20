# QJSValue
> Qt 6.11.1 · Qt QML · 来自 `QJSValue`

## 作用定位

`QJSValue` 是 JavaScript 值的通用包装：一个变量可能是 `undefined`、`null`、布尔、数字、字符串、对象、数组、函数、错误、QObject 包装或 QMetaObject 包装。它是脚本世界和 C++ 世界之间最常见的值载体。

如果值是对象或函数，它通常依附于创建它的 `QJSEngine`。这点决定了它不能像普通 QVariant 那样随意跨引擎、跨线程长期使用。

## 类说明

- 头文件：`#include <QJSValue>`
- CMake：链接 `Qt6::Qml`
- 继承：无公开 QObject 继承，值类型句柄
- 相关：`QJSEngine`、`QJSValueIterator`、`QJSPrimitiveValue`、`QJSManagedValue`

## API 速查

| API | 说明 |
| --- | --- |
| 构造函数 | 从特殊值、布尔、字符串、数字或另一个 `QJSValue` 创建值。 |
| `SpecialValue` | `UndefinedValue`、`NullValue`，用于明确构造 JS 特殊值。 |
| `ErrorType` | 描述 JS 错误类别，如普通错误、类型错误、引用错误等。 |
| `isUndefined()` / `isNull()` | 判断 JS 特殊值。 |
| `isBool()` / `isNumber()` / `isString()` | 判断基础类型。 |
| `isObject()` / `isArray()` / `isCallable()` | 判断对象、数组、可调用函数。 |
| `isError()` / `errorType()` | 判断并识别 JS 错误对象。 |
| `isQObject()` / `toQObject()` | 处理由 QObject 包装来的 JS 对象。 |
| `isQMetaObject()` / `toQMetaObject()` | 处理元对象包装。 |
| `property(name/index)` | 读取对象属性或数组元素。 |
| `setProperty(name/index, value)` | 写入对象属性或数组元素。 |
| `deleteProperty(name)` | 删除自有属性，遵守 JS 可配置属性规则。 |
| `hasProperty()` / `hasOwnProperty()` | 区分原型链属性和自有属性。 |
| `prototype()` / `setPrototype()` | 读取或修改 JS 原型。 |
| `call()` | 把值当函数调用。 |
| `callWithInstance()` | 指定 `this` 对象调用函数。 |
| `callAsConstructor()` | 把函数当构造器调用。 |
| `equals()` / `strictlyEquals()` | 分别对应 JS `==` 和 `===` 语义。 |
| `toBool()` / `toNumber()` / `toString()` | 按 JS 规则转换基础值。 |
| `toInt()` / `toUInt()` | 转为 32 位整数。 |
| `toDateTime()` / `toPrimitive()` | 转为日期或原始值。 |
| `toVariant()` | 转到 `QVariant`；可选择对象转换策略。 |

## 使用场景

- 接收 `QJSEngine::evaluate()` 的结果。
- 调用 JS 函数并读取返回值。
- 在 C++ 中操作脚本对象属性。
- 把 QObject 暴露给 JS 后，在 C++ 中识别和取回。

## 常见坑与经验

- `equals()` 是 JS 宽松相等，`"1" == 1` 可能为真；需要严格语义就用 `strictlyEquals()`。
- `isObject()` 包括数组、函数、Date、RegExp、QObject 包装等，后续还要细分。
- `toVariant()` 可能递归转换对象；如果想保留 JS 对象身份，要使用保留对象的转换策略。
- `call()` 前先判断 `isCallable()`，否则返回错误值而不是 C++ 异常。
- 不要把来自一个 `QJSEngine` 的对象值丢到另一个 engine 使用。

## 知识点覆盖

- JS 类型系统在 Qt 中的表示
- 属性、数组索引、原型链
- 函数调用与构造调用
- JS 宽松/严格相等
- QJSValue 与 QVariant 转换边界
