# QJsonObject
> Qt 6.11.1 · Qt Core · 来自 `QJsonObject`

## 作用定位
`QJsonObject` 是由字符串键和 `QJsonValue` 组成的 JSON 对象值类型，适合表达具名配置、API 请求与响应记录。

## API 速查
| API | 是做什么的 |
|---|---|
| `insert()` | 写入或替换一个字段。|
| `value()` | 读取字段，缺失时返回 Undefined 值。|
| `contains()` | 判断字段是否存在。|
| `remove()` / `take()` | 删除字段；`take()` 返还旧值。|
| `find()` | 返回字段迭代器。|
| `keys()` | 返回字段名列表。|
| `toVariantMap()` | 转为 QVariantMap。|
| `fromVariantMap()` | 从 QVariantMap 构造。|

## 使用场景
构造 REST JSON body、读取具名配置、对接口响应做 schema 前置验证。

## 常见坑与经验
- 区分字段缺失的 `Undefined` 与显式 `null`，它们在 API 兼容性中语义不同。
- JSON key 大小写敏感，服务端字段名不要凭经验变换。
- `keys()` 生成副本且顺序不应被依赖；需要稳定输出时自行排序。

## 知识点覆盖
JSON object、字段存在性、null 与 undefined、QVariantMap、schema 校验、键大小写。
