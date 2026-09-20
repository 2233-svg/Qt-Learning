# QJsonArray::const_iterator
> Qt 6.11.1 · Qt Core · 来自 `QJsonArray::const_iterator`

## 作用定位
`QJsonArray::const_iterator` 用于只读遍历 JSON 数组中的 `QJsonValue`，不允许通过迭代器修改原数组。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator*()` / `operator->()` | 读取当前位置的 JSON 值。|
| `operator++()` / `operator--()` | 前后移动迭代位置。|
| `operator+()` / `operator-()` | 按偏移随机访问。|
| `operator==()` | 比较两个位置。|

## 使用场景
校验外部 JSON 数组、统计元素类型或转换为业务对象时使用。

## 常见坑与经验
- JSON 数组结构被修改后，旧迭代器不可继续使用。
- 读取外部数组时先判断值类型，不能把数组元素默认当作对象或字符串。

## 知识点覆盖
JSON 数组、只读迭代、类型校验、迭代器失效、外部输入。
