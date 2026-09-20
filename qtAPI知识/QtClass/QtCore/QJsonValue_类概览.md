# QJsonValue 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QJsonValue>`  
> 模块：`Qt6::Core`  
> 定位：一个 JSON 基本值或容器值的统一包装

## 它解决什么问题

JSON 的一个位置可能是 `null`、布尔、数字、字符串、数组或对象。`QJsonValue` 统一表示这些可能性，是 `QJsonObject` 的成员值和 `QJsonArray` 的元素类型。

它适合在 JSON 边界上承接数据，不替代领域模型。解析到业务数据后，应尽早校验必填字段、类型、范围和单位，并转为强类型 C++ 数据，而不是让整段业务逻辑都围绕 `QJsonValue` 运行。

## 类型系统：`Null` 不等于 `Undefined`

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| JSON 类型 | `Null` | 对应合法 JSON 值 `null`。 | 常表示明确清空，不等于字段缺失。 |
| JSON 类型 | `Bool` | 对应 `true` 或 `false`。 | 用 `isBool()` 验证后读取。 |
| JSON 类型 | `Double` | 对应 JSON number。 | JSON 数值受双精度语义限制。 |
| JSON 类型 | `String` | 对应 JSON string。 | Qt 内部用 `QString`。 |
| JSON 类型 | `Array` | 保存 `QJsonArray`。 | 取出后修改的是副本，要写回父容器。 |
| JSON 类型 | `Object` | 保存 `QJsonObject`。 | 同样遵守值语义和写回规则。 |
| JSON 类型 | `Undefined` | 表示程序层面的无值。 | 常见于缺失键或数组越界，不能出现在合法 JSON 文本中。 |

```cpp
QJsonObject object{{"knownNull", QJsonValue::Null}};

object.value("knownNull").isNull();     // true
object.value("missing").isUndefined();  // true
```

`Null` 与 `Undefined` 的差异会影响 PATCH、配置覆盖和接口兼容：前者可能是“清空值”，后者可能是“保持默认值”。

## 转换前先验证类型

`toString()`、`toInt()`、`toBool()` 等在类型不匹配时返回默认值。它们便于处理可信的可选字段，却不能证明外部输入正确。

```cpp
const QJsonValue portValue = config.value("port");
if (!portValue.isDouble())
    return; // 报告协议错误

const int port = portValue.toInt();
if (port < 1 || port > 65535)
    return;
```

网络响应、导入文件等不可信数据应先 `isXxx()` 或 `type()`，再做范围和业务规则校验。只有本地默认配置等可信数据，才适合直接使用转换接口的默认值。

## 数字精度边界

JSON 没有独立的整数类型，`QJsonValue` 的数值类型是 `Double`。虽然可以用 `int` 和 `qint64` 构造，跨语言传输时仍要考虑 IEEE 754 双精度的精确整数范围。

数据库主键、金额最小单位、纳秒时间戳等可能超过 JavaScript 安全整数范围的数据，协议最好编码成字符串，或明确限制数值范围。`toInteger()` 能读成 `qint64`，但不让 JSON 自动获得任意精度。

## 解析与写出单个根值

Qt 6.9 起，`fromJson()` 能解析任意 JSON 根值，包括对象、数组和标量：

```cpp
#include <QJsonParseError>
#include <QJsonValue>

QJsonParseError error;
const QJsonValue value = QJsonValue::fromJson(R"({"enabled":true})", &error);
if (error.error != QJsonParseError::NoError) {
    qWarning() << error.offset << error.errorString();
    return;
}

const QByteArray compact = value.toJson(QJsonValue::JsonFormat::Compact);
```

维护 Qt 6.8 或更低版本时，`QJsonValue::fromJson()` 和 `toJson()` 不可用，应使用适合根类型的 `QJsonDocument` 路径。

## 容器副本、链式读取和引用代理

`toObject()`、`toArray()` 返回副本，修改后要插回来源容器。const `operator[]` 可用于链式读取：

```cpp
const QJsonValue city = root["profile"]["address"]["city"];
```

中途任一层类型不对、键缺失或数组越界，后续结果为 `Undefined`。它适合简单可选字段；严格协议校验最好分层检查并给出具体错误。

从非 const 对象或数组下标得到的 `QJsonValueRef` 是指向元素的代理：

```cpp
QJsonArray flags{false};
QJsonValueRef first = flags[0];
first = true;
```

它不是可长期脱离容器存在的普通值。容器被修改、销毁或分离后，不再保存和使用该代理；需要跨函数传递时转为 `QJsonValue`。

## 常见误区

- 把 `Undefined` 视为 JSON 的 `null`。
- 未检查类型就转换，让默认值掩盖协议错误。
- 让超大整数以 JSON number 跨语言传递。
- 修改 `toObject()` / `toArray()` 的结果却不写回。
- 长期保存 `QJsonValueRef`。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QJsonValue(Type = Null)` | 按指定 JSON 类型构造值。 | `Undefined` 只用于程序内的无值状态。 |
| 构造 | `QJsonValue(bool)` | 构造 JSON 布尔值。 | 不用它表达数字或文本标记。 |
| 构造 | `QJsonValue(int)`、`QJsonValue(qint64)`、`QJsonValue(double)` | 构造 JSON 数字。 | 跨语言前考虑大整数精度。 |
| 构造 | `QJsonValue(QString / QLatin1StringView / const char *)` | 构造 JSON 字符串。 | `const char *` 按 UTF-8 转换，输入编码应明确。 |
| 构造 | `QJsonValue(const QJsonArray &)`、`QJsonValue(QJsonArray &&)` | 用数组构造容器值。 | 取回数组修改后需要写回外层。 |
| 构造 | `QJsonValue(const QJsonObject &)`、`QJsonValue(QJsonObject &&)` | 用对象构造容器值。 | 是值语义，不存在 QObject 所有权。 |
| 构造与赋值 | 拷贝、移动构造和 `operator=` | 复制或转移 JSON 值。 | 隐式共享，适合按值传递。 |
| 构造与赋值 | `swap(QJsonValue &)` | 交换两个值。 | 值及其 JSON 类型一起交换。 |
| JSON 文本，Qt 6.9 起 | `fromJson(QByteArrayView, QJsonParseError *)` | 从 UTF-8 JSON 文本解析任意根值。 | 必须检查 `QJsonParseError`。 |
| JSON 文本，Qt 6.9 起 | `toJson(JsonFormat)` | 输出 UTF-8 JSON 文本。 | `Indented` 便于阅读，`Compact` 节省传输体积。 |
| QVariant | `fromVariant(const QVariant &)` | 从动态 Qt 值转换为 JSON 值。 | 非 JSON 原生类型的协议语义须显式约定。 |
| QVariant | `toVariant()` | 转换为 `QVariant`。 | 适合动态边界，不替代业务层强类型。 |
| 类型查询 | `type()` | 返回 `Type` 枚举。 | 复杂分支可用 `switch`。 |
| 类型查询 | `isNull()`、`isUndefined()` | 判断空值或无值。 | 前者合法 JSON，后者常表示缺失或越界。 |
| 类型查询 | `isBool()`、`isDouble()`、`isString()` | 判断基本值类型。 | 转换前检查可避免默认值掩盖错误。 |
| 类型查询 | `isArray()`、`isObject()` | 判断容器类型。 | 通过检查后再取出容器。 |
| 标量转换 | `toBool(defaultValue)` | 读取布尔值。 | 类型不匹配返回默认值。 |
| 标量转换 | `toInt(defaultValue)` | 读取 `int`。 | 验证类型和范围，大值考虑 `toInteger()`。 |
| 标量转换 | `toInteger(defaultValue)` | 读取 `qint64`。 | Qt 6.0 起提供，仍受 JSON 数字精度限制。 |
| 标量转换 | `toDouble(defaultValue)` | 读取双精度数。 | 适合确实允许小数的协议字段。 |
| 字符串转换 | `toString()`、`toString(defaultValue)` | 读取 `QString`。 | 不匹配时返回空或指定默认值。 |
| 字符串转换，Qt 6.10 起 | `toStringView(defaultValue)` | 返回字符串视图以减少部分拷贝。 | 视图不能超过源值的存活期。 |
| 容器转换 | `toArray()`、`toArray(defaultValue)` | 读取数组副本。 | 错误类型返回空或默认数组。 |
| 容器转换 | `toObject()`、`toObject(defaultValue)` | 读取对象副本。 | 修改后插回外层容器。 |
| 链式读取 | const `operator[](QString / QStringView / QLatin1StringView)` | 作为对象继续按键读取。 | 类型不对或键缺失返回 `Undefined`。 |
| 链式读取 | const `operator[](qsizetype)` | 作为数组继续按索引读取。 | 越界或类型不对返回 `Undefined`。 |
| 相关代理 | `QJsonValueConstRef`、`QJsonValueRef` | 表示容器元素的只读或可写代理。 | 不让代理脱离来源对象或数组长期使用。 |
| 散列、调试与流 | `qHash()`、`QDebug operator<<`、`QDataStream << / >>` | 支持哈希、调试输出和 Qt 二进制流。 | `QDataStream` 不是 JSON 文本格式。 |

## 一句话总结

`QJsonValue` 是 Qt JSON API 的统一值载体。先检查类型再转换，分清 `Null` 和 `Undefined`，给大整数明确协议表示，才能让 JSON 安全进入业务代码。
