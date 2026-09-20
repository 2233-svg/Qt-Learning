# QCborMap
> Qt 6.11.1 · Qt Core · 来自 `QCborMap`

## 作用定位
`QCborMap` 是以 `QCborValue` 作为键和值的 CBOR 映射容器，适合表达带命名字段或非字符串键的结构化消息。

## API 速查
| API | 是做什么的 |
|---|---|
| `insert()` | 写入键值对。|
| `value()` | 按键读取值。|
| `contains()` | 判断键是否存在。|
| `remove()` | 删除键。|
| `keys()` | 读取键集合。|
| `toCborValue()` | 包装为通用值。|
| `fromJsonObject()` | 从 JSON 对象转换。|

## 使用场景
设备配置、消息对象、可选字段丰富的版本化协议。

## 常见坑与经验
- 用整数键可节省空间，但调试性较差；跨团队协议应维护键号表。
- 不要假设键一定是字符串，解析外部 CBOR 时应验证类型。

## 知识点覆盖
CBOR map、动态键、版本化协议、JSON 互操作、字段验证。
