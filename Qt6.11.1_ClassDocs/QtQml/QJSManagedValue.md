# QJSManagedValue
> Qt 6.11.1 · Qt QML · 来自 `QJSManagedValue`

## 作用定位

`QJSManagedValue` 是绑定到 `QJSEngine` 的 JS 值句柄，面向需要精确管理对象、函数、原型、QObject 包装和 QVariant 包装的场景。它比 `QJSPrimitiveValue` 能表示更多 JS 类型，也比普通 `QJSValue` 更强调“这个值由哪个 engine 管理”。

## 类说明

- 头文件：`#include <QJSManagedValue>`
- CMake：链接 `Qt6::Qml`
- 继承：无公开 QObject 继承
- 构造必须提供 `QJSEngine *`，空值除外

## API 速查

| API | 说明 |
| --- | --- |
| `Type` | `Undefined`、`Boolean`、`Number`、`String`、`Object`、`Symbol`、`Function`。 |
| 构造函数 | 从 `QJSValue`、`QJSPrimitiveValue`、QString、QVariant 以及 engine 创建托管值。 |
| `engine()` | 返回该值所属引擎。 |
| 类型判断 | `isArray()`、`isFunction()`、`isQObject()`、`isVariant()`、`isUrl()` 等。 |
| `property()` / `setProperty()` | 读取或设置对象属性/数组元素。 |
| `hasProperty()` / `hasOwnProperty()` | 判断属性是否存在以及是否为自有属性。 |
| `deleteProperty()` | 删除对象属性。 |
| `prototype()` / `setPrototype()` | 访问和修改原型。 |
| `call()` / `callWithInstance()` / `callAsConstructor()` | 调用函数、指定 this 调用或作为构造器调用。 |
| `equals()` / `strictlyEquals()` | JS 宽松/严格相等。 |
| `toPrimitive()` / `toJSValue()` | 转成原始值或普通 `QJSValue`。 |
| `toVariant()` / `toQObject()` / `toQMetaObject()` | 转回 C++/Qt 类型。 |

## 使用场景

- 在 C++ 中长期保存与某个 engine 绑定的对象或函数引用。
- 实现脚本扩展 API，需要操作对象原型或动态属性。
- 接收 QVariant/QObject 后转换成 JS 管理值，再参与脚本调用。
- 判断 JS 值是 Date、RegExp、Url、Symbol 等更细类别。

## 常见坑与经验

- 托管值离不开 engine；engine 销毁后，值引用就不应再使用。
- `toVariant()` 会把 JS 对象尽量转成 Qt 容器或 QObject 指针，但并不保留所有 JS 行为。
- `equals()` 和 `strictlyEquals()` 仍遵守 JS 语义，不是 C++ 指针或 QVariant 比较。
- 函数调用失败通常返回错误值，要检查 `isError()` 或 engine 异常状态。
- 同一 QObject 被多个 engine 包装时，ownership 和引用关系要明确，避免脚本侧误删 C++ 对象。

## 知识点覆盖

- 引擎绑定 JS 值
- 对象属性和原型
- JS 函数调用模型
- QObject/QVariant/QMetaObject 包装
- 托管值与原始值的选择
