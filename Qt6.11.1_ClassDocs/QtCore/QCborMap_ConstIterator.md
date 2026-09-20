# QCborMap::ConstIterator
> Qt 6.11.1 · Qt Core · 来自 `QCborMap::ConstIterator`

## 作用定位
`QCborMap::ConstIterator` 只读遍历 CBOR map 的键值项。

## API 速查
| API | 是做什么的 |
|---|---|
| `key()` | 读取当前键。|
| `value()` | 读取当前值。|
| `operator*()` | 访问当前键值对。|
| `operator++()` | 移到下一项。|

## 使用场景
诊断或解析未知字段的 CBOR map，同时保持源对象不变。

## 常见坑与经验
- 不应假设迭代顺序等于 JSON 文本字段顺序；协议不能依赖 map 迭代顺序。

## 知识点覆盖
map 迭代、键值对、只读解析、协议顺序无关性。
