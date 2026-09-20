# QJSManagedValue：绑定某台 QJSEngine 的堆值句柄

> Qt 6.11.1 · `#include <QJSManagedValue>` · 模块：`Qt6::Qml`

`QJSManagedValue` 是对 JavaScript 堆值的移动型句柄。它用于在 C++ 中高效操作属于某台 `QJSEngine` 的对象、函数、符号和原始值，同时明确表达“这个值不能离开该 engine”。

它适合短时间、同线程、同一 engine 内的连续操作，例如 C++ 扩展实现一段复杂的对象访问或函数调用。它不适合作为长期成员缓存，也不适合跨线程传递。

## 生命周期是它的核心语义

```cpp
#include <QJSEngine>
#include <QJSManagedValue>
#include <QDebug>

QJSEngine engine;
QJSManagedValue object(engine.newObject(), &engine);
object.setProperty(u"state"_s, QJSValue(u"ready"_s));

if (engine.hasError())
    qWarning() << engine.catchError().toString();
else
    qDebug() << object.property(u"state"_s).toString();
```

`QJSManagedValue` 不可复制、可以移动。默认构造值和移动后的源值代表没有关联 engine 的 `undefined`。非默认值要在 engine 内登记并释放其堆槽位，因此必须：

- 在创建它的 engine 存活期间使用和销毁；
- 留在该 engine 所在线程；
- 不与另一个 engine 的 managed value 直接组合。

把它放进跨线程队列、静态对象或生命周期晚于 engine 的成员对象，都可能与 GC 或 engine 析构发生竞争。实用准则是：**局部计算用 `QJSManagedValue`，跨函数存储或对外返回用 `QJSValue`。**

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

## 它解决的问题

### 在 C++ 扩展中连续操纵同一套 JS 堆

```cpp
QJSManagedValue fn(engine.evaluate(u"(x) => x + 1"_s), &engine);
QJSValue result = fn.call({ QJSValue(4) });
```

它可以直接访问属性、调用函数、修改原型，并在需要离开局部作用域时用 `toJSValue()` 转为通用句柄。相比在每一步创建通用值句柄，它更贴近 engine 的内存模型。

### 将异常统一保存在 engine 中

`QJSManagedValue` 的操作不会像 `QJSValue` 那样把 JavaScript 异常包装进每个返回值。出现异常时，操作会得到默认/失败结果，并把错误留在所属 `QJSEngine`；随后用 `hasError()` 和 `catchError()` 处理。

因此每个可能执行 JavaScript 的步骤后都应设置清晰的错误检查点。不要在多次属性访问、转换、调用之后才检查，否则真正的失败位置难以判断。

## engine 一致性与原型边界

写属性时传入的 `QJSValue` 必须是 primitive，或属于同一台 engine。把另一台 engine 的对象、数组、函数直接设置进去是不允许的。原型也必须属于同一 engine，并且只能是对象或 `null`；形成环形原型链会失败并留下 engine 错误。

`equals()` 是宽松 `==`，`strictlyEquals()` 是严格 `===`。跨 engine 的对象不应被拿来实现可移植的对象比较或对象传递。

`toString()`、`toNumber()`、`toBoolean()` 使用 JavaScript 转换规则，对对象可能执行 `valueOf()` 或 `toString()`。`toPrimitive()` 只能完整表达 primitive；对象、函数、symbol 的行为和身份不能被它保留。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QJSManagedValue()` | 创建无 engine 的 `undefined` | 可作空哨兵，不能执行有意义的堆操作。 |
| `QJSManagedValue(QJSValue, engine)` | 将通用 JS 值纳入管理 | 对象值必须属于该 engine。 |
| `QJSManagedValue(QJSPrimitiveValue, engine)` | 将 primitive 放入 engine | primitive 可跨 engine，新 managed value 归目标 engine。 |
| `QJSManagedValue(QVariant/QString, engine)` | 创建受管理值 | 转换遵循 Qt/JS 桥接规则。 |
| 移动构造与移动赋值 | 转交句柄 | 不可复制；移动后源值无关联。 |
| `engine()` | 取得所属 engine | 空指针代表默认/移动后值；不延长 engine 生命周期。 |
| `type()` 与 `is...()` | 查询 JS 与特殊对象类型 | 在转换前优先做纯查询。 |
| `property(name/index)` | 读取属性 | getter 可执行脚本，异常写入 engine 错误状态。 |
| `setProperty(name/index, value)` | 写入属性 | `value` 必须是 primitive 或来自同一 engine。 |
| `hasProperty()` / `hasOwnProperty()` | 查属性 | 前者遍历原型链，后者仅自身属性。 |
| `deleteProperty()` | 删除属性 | 返回是否成功，受属性描述符限制。 |
| `prototype()` / `setPrototype()` | 读写原型 | 原型须同 engine、为对象或 null，且不得成环。 |
| `call()` | 调用函数 | 非函数或异常后检查 `engine->hasError()`。 |
| `callWithInstance()` | 指定 `this` | `instance` 同样要满足 engine 一致性。 |
| `callAsConstructor()` | 构造调用 | 失败后从 engine 取错误。 |
| `equals()` | JS 宽松相等 | 会发生类型强制。 |
| `strictlyEquals()` | JS 严格相等 | 对对象是身份比较，不比较字段内容。 |
| `toString()` / `toNumber()` / `toBoolean()` | JS 原生转换 | 对对象可能执行用户脚本。 |
| `toInteger()` | 转 `int` | 使用 JavaScript 整数转换规则。 |
| `toPrimitive()` | 转无 engine primitive | 只能完整表达 primitive。 |
| `toJSValue()` | 转通用句柄 | 适合返回与缓存；对象仍依赖原 engine。 |
| `toVariant()` | 转 Qt 元类型值 | 适合数据边界，不保留 JS 对象行为。 |
| `toQObject()` / `toQMetaObject()` | 取 Qt 包装目标 | 不改变 QObject 所有权。 |
| `toDateTime()` / `toUrl()` / `toRegularExpression()` | 转特殊 Qt 值 | 验证类型并处理转换失败。 |
| `jsMetaType()` | 取关联 JS 元类型 | 仅对 JavaScript 元类型对象使用。 |
| `jsMetaMembers()` | 列举 JS 元类型成员 | 不等同普通对象的可枚举字段。 |
| `jsMetaInstantiate(values)` | 实例化 JS 元类型 | 失败后检查 engine 错误状态。 |

`QJSManagedValue` 是局部的高效工具；engine、线程和析构顺序始终一致时它很直接，任何一项跨边界时都该改用别的表示。
