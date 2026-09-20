# QJsonObject::const_iterator
> Qt 6.11.1 · Qt Core · 来自 `QJsonObject::const_iterator`

## 作用定位
`QJsonObject::const_iterator` 只读遍历 JSON 对象的键和值。

## API 速查
| API | 是做什么的 |
|---|---|
| `key()` | 读取当前成员名。|
| `value()` | 读取当前 JSON 值。|
| `operator*()` | 读取当前值。|
| `operator++()` | 前进到下一个成员。|

## 使用场景
通用配置检查、调试输出和未知字段收集。

## 常见坑与经验
- JSON object 的成员顺序不应作为协议语义；要稳定输出时按键排序。
- 改动 object 结构后旧迭代器失效。

## 知识点覆盖
JSON 对象、键值遍历、顺序无关、输入验证、迭代器失效。
