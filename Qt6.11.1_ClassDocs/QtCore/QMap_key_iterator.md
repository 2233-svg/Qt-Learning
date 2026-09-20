# QMap::key_iterator
> Qt 6.11.1 · Qt Core · 来自 `QMap::key_iterator`

## 作用定位
`QMap::key_iterator` 只按升序遍历 `QMap` 的键，适合无需读取值的范围操作。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator*()` | 读取当前键。|
| `operator++()` / `operator--()` | 前后移动。|
| `keyBegin()` / `keyEnd()` | 取得键范围边界。|
| `operator==()` | 比较位置。|

## 使用场景
按排序 ID 枚举可用键、生成索引目录、执行键范围分析。

## 常见坑与经验
- 它仍依赖原 map 存活且未结构修改。
- 需要键和值一起处理时使用 `asKeyValueRange()` 或普通 iterator。

## 知识点覆盖
有序键遍历、范围、迭代器生命周期、结构化绑定选择。
