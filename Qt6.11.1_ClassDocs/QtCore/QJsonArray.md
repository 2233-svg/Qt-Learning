# QJsonArray
> Qt 6.11.1 · Qt Core · 来自 `QJsonArray`

## 作用定位
`QJsonArray` 是 JSON 有序数组的隐式共享值类型，元素为 `QJsonValue`，适合读取、构造和修改 API 列表、配置项或嵌套数据。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` / `prepend()` | 在两端加入 JSON 值。|
| `insert()` / `removeAt()` | 按索引改变结构。|
| `at()` | 按索引读取值。|
| `replace()` | 替换指定元素。|
| `contains()` | 判断值是否出现。|
| `fromStringList()` | 从字符串列表构建数组。|
| `toVariantList()` | 转为 QVariant 列表。|

## 使用场景
构造 REST 请求的列表字段、读取配置数组、遍历服务端返回的对象列表。

## 常见坑与经验
- JSON 数组只保存 JSON 支持的类型；任意 C++ 对象需要先明确序列化格式。
- 隐式共享下修改会 detach，循环中反复复制/修改大型数组需注意成本。
- 外部 JSON 数组的元素类型可能混杂，解析前逐项验证。

## 知识点覆盖
JSON、隐式共享、有序列表、QJsonValue、QVariant 转换、输入校验。
