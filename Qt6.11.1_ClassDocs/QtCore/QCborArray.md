# QCborArray
> Qt 6.11.1 · Qt Core · 来自 `QCborArray`

## 作用定位
`QCborArray` 是有序的 `QCborValue` 容器，用于表示 CBOR 数组字段。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` / `prepend()` | 在末尾或开头加入值。|
| `insert()` / `removeAt()` | 按索引改变结构。|
| `at()` | 读取指定元素。|
| `replace()` | 替换一个元素。|
| `toCborValue()` | 包装为通用 CBOR 值。|
| `fromJsonArray()` | 从 JSON 数组转换。|

## 使用场景
有序协议参数、嵌套配置和消息列表。

## 常见坑与经验
- 位置就是协议语义时，新增字段必须设计兼容默认值与版本识别。
- 修改容器结构会让已有迭代器失效。

## 知识点覆盖
CBOR 数组、顺序字段、容器更新、版本兼容、JSON 转换。
