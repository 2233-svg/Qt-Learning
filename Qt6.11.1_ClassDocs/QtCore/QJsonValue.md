# QJsonValue
> Qt 6.11.1 · Qt Core · 来自 `QJsonValue`

## 作用定位
`QJsonValue` 是 JSON 标量或容器的通用值类型，表示 null、bool、double、string、array、object 或 undefined。

## API 速查
| API | 是做什么的 |
|---|---|
| `type()` | 查询实际 JSON 类型。|
| `isNull()` / `isUndefined()` | 区分显式 null 与缺失值。|
| `isBool()` / `isDouble()` 等 | 判断具体类型。|
| `toBool()` / `toDouble()` | 转换标量。|
| `toString()` | 提取字符串。|
| `toArray()` / `toObject()` | 提取嵌套容器。|
| `fromVariant()` | 从 QVariant 转换。|
| `toVariant()` | 转为 QVariant。|

## 使用场景
编写 JSON schema 校验器、解析可选字段、构建对象或数组的嵌套值。

## 常见坑与经验
- JSON number 以双精度表达，64 位整数 ID 在安全整数范围外应使用字符串。
- `toString(defaultValue)` 等转换 API 不替代类型校验，外部协议应先使用 `isString()` 等判断。
- `Undefined` 多用于对象字段不存在，序列化时通常与 `null` 的行为不同。

## 知识点覆盖
JSON 类型、null/undefined、数值精度、类型转换、QVariant、schema 校验。
