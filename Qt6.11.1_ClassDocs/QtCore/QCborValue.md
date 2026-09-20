# QCborValue
> Qt 6.11.1 · Qt Core · 来自 `QCborValue`

## 作用定位
`QCborValue` 是 CBOR 的通用值类型：整数、浮点、字节串、文本、数组、映射、tag 和简单值都通过它统一保存。

## API 速查
| API | 是做什么的 |
|---|---|
| `type()` | 查询实际 CBOR 类型。|
| `isArray()` / `isMap()` | 判断容器类型。|
| `toInteger()` / `toString()` | 提取基础值。|
| `toArray()` / `toMap()` | 提取容器。|
| `fromCbor()` | 解码完整 CBOR 数据。|
| `toCbor()` | 编码为 CBOR 字节。|
| `toJsonValue()` | 转为 JSON 可表达值。|

## 使用场景
紧凑设备协议、包含二进制字段的配置、需要保持部分 CBOR tag 的消息。

## 常见坑与经验
- 外部输入转换前先检查类型；默认转换值可能掩盖格式错误。
- CBOR 的字节串、tag 和部分数值不能无损映射为 JSON。

## 知识点覆盖
CBOR、动态类型、二进制序列化、JSON 互操作、输入验证。
