# QJsonArray::iterator
> Qt 6.11.1 · Qt Core · 来自 `QJsonArray::iterator`

## 作用定位
`QJsonArray::iterator` 是可写 JSON 数组迭代器，可按位置访问和替换数组中的 `QJsonValue`。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator*()` | 读取或修改当前 JSON 值。|
| `operator++()` / `operator--()` | 前后移动。|
| `operator[]` | 按相对偏移访问。|
| `operator+()` / `operator-()` | 随机访问移动。|

## 使用场景
将数组内旧格式字段迁移为新格式，或逐项清理无效值。

## 常见坑与经验
- 结构插入或删除会使迭代器失效；需要删除时按返回的新位置继续。
- `QJsonValueRef` 是代理引用，不要把它当成长寿命的普通引用保存。

## 知识点覆盖
JSON 修改、代理引用、随机访问、迭代器失效、数据迁移。
