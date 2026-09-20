# QJSValue：保存并操作一个 JavaScript 值

> Qt 6.11.1 · `#include <QJSValue>` · 模块：`Qt6::Qml`

`QJSValue` 是 C++ 侧的 JavaScript 值句柄。它可保存 `undefined`、`null`、布尔、数值、字符串，也能引用某台 `QJSEngine` 中的对象、数组、函数、QObject 包装器和异常对象。

它用于 C++/JS 边界上的通用参数和返回值，例如调用脚本函数、读取配置对象或把对象交给插件。它不是 JSON 值类型，也不是对象的深拷贝容器。

## 构建与最小示例

```cpp
#include <QJSEngine>
#include <QJSValue>
#include <QDebug>

QJSEngine engine;
QJSValue order = engine.newObject();
order.setProperty(u"id"_s, 42);
order.setProperty(u"amount"_s, 99.5);

const QJSValue value = engine.evaluate(u"({ id: order.id, total: order.amount * 1.13 })"_s);
qDebug() << value.property(u"total"_s).toNumber();
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

## 对象值是引用，不是快照

基本值可以直接构造；对象、数组、函数则由 engine 创建或从脚本执行结果取得。复制对象型 `QJSValue` 复制的是同一个 JavaScript 对象的引用：

```cpp
QJSValue a = engine.newObject();
QJSValue b = a;
b.setProperty(u"name"_s, u"Ada"_s);
// a.property("name") 同样为 "Ada"
```

需要隔离数据时，应显式新建对象并复制字段，或转换到适当的 `QVariant` / JSON 数据结构。长期保存脚本值时，engine 必须比该值活得更久；engine 已销毁后，相关句柄会表现为 `undefined`。

## 属性、函数和隐式执行

`property()` / `setProperty()` 支持字符串键和数组下标，数组应优先使用下标重载。`hasProperty()` 会沿原型链查找；`hasOwnProperty()` 只查对象自己的属性。

属性访问并不必然是无副作用操作：getter 可以执行任意脚本并抛异常。`property()` 或函数调用返回的 `QJSValue` 可能就是异常值，不能把它们都当正常结果。

```cpp
QJSValue fn = engine.evaluate(u"(function (x) { return x * 2; })"_s);
QJSValue result = fn.call({ QJSValue(21) });
if (!result.isError())
    qDebug() << result.toInt();
```

对非对象调用 `setProperty()` 是静默无效的；对非函数调用 `call()` 也不会自动变成函数，先用 `isObject()`、`isCallable()` 判断。

## 转换和比较的边界

`toNumber()`、`toString()` 等遵循 JavaScript 强制转换。若值是对象，它们可能调用对象的 `valueOf()` 或 `toString()`，因此可能有副作用或异常。`equals()` 对应 JS `==`，会类型强制；业务比较通常应使用 `strictlyEquals()` 对应的 `===`。

`toVariant()` 的 `ConvertJSObjects` 会递归转换对象/数组为 Qt 数据；`RetainJSObjects` 保留 JS 对象形式。选择前要明确是否需要保留对象身份、原型和可调用性。

`toQObject()` / `toQMetaObject()` 取回包装目标，不转移 QObject 所有权。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QJSValue(...)` | 创建基本 JS 值 | 支持 bool、整数、double、字符串、`UndefinedValue`、`NullValue`。 |
| `isUndefined()` / `isNull()` | 区分空状态 | 不能以 `toBool()` 代替此判断。 |
| `isBool()` / `isNumber()` / `isString()` | 判断基本类型 | 不会触发 JS 转换。 |
| `isObject()` / `isArray()` / `isCallable()` | 判断可操作对象 | 读写属性、调用函数前优先检查。 |
| `isQObject()` / `isQMetaObject()` | 判断 Qt 包装类型 | 不意味着取得 QObject 所有权。 |
| `isDate()` / `isRegExp()` / `isUrl()` / `isError()` | 判断特殊对象 | `isError()` 不能覆盖 `throw 42`。 |
| `property(name/index)` | 读属性或数组项 | getter 可执行脚本或返回异常值。 |
| `setProperty(name/index, value)` | 写属性或数组项 | 对非对象无效；索引重载适合数组。 |
| `deleteProperty(name)` | 删除自身属性 | 返回是否成功，受属性描述符约束。 |
| `hasProperty()` | 查属性及原型链 | 与 JS 属性可见性一致。 |
| `hasOwnProperty()` | 只查自身属性 | 枚举或导出字段时通常更合适。 |
| `prototype()` / `setPrototype()` | 读取/修改原型 | 原型会改变属性查找；避免形成循环。 |
| `call(args)` | 普通函数调用 | 目标必须可调用；异常会作为返回值出现。 |
| `callWithInstance(instance, args)` | 指定 `this` 调用 | 用于依赖接收者状态的方法。 |
| `callAsConstructor(args)` | 构造方式调用 | 对应 JavaScript `new` 语义。 |
| `equals(other)` | 宽松相等 `==` | 会进行类型强制。 |
| `strictlyEquals(other)` | 严格相等 `===` | 对对象比较身份，而不是字段。 |
| `toBool()` / `toInt()` / `toUInt()` / `toNumber()` | 数值/布尔转换 | 使用 JavaScript 转换规则。 |
| `toString()` | 转字符串 | 对对象可能调用脚本的转换方法。 |
| `toDateTime()` / `toQObject()` / `toQMetaObject()` | 转特殊 Qt 类型 | 先验证类型并处理无效结果。 |
| `toPrimitive()` | 获得无 engine 的 primitive | 对象和 Symbol 不能完整保留。 |
| `toVariant(behavior)` | 转 Qt 元类型数据 | 是否递归失去 JS 对象身份取决于转换策略。 |
| `errorType()` | 读取 Error 类别 | 仅对 Error 对象有意义。 |

使用 `QJSValue` 时最重要的判断是：当前拿到的是 C++ 基本值、一个复制的值，还是某台 engine 中对象的引用。
