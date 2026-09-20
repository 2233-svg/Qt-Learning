# QHash::key_iterator
> Qt 6.11.1 · Qt Core · 来自 `QHash::key_iterator`

## 作用定位
`QHash::key_iterator` 只遍历 `QHash` 的键，不需要读取或复制对应值。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator*()` | 读取当前键。|
| `operator++()` | 前进到下一个键。|
| `operator==()` | 比较迭代位置。|
| `keyBegin()` / `keyEnd()` | 获取键遍历边界。|

## 使用场景
仅需枚举已缓存的 ID、收集键集合或对键做存在性统计。

## 常见坑与经验
- 仍然不保证顺序；需要有序键列表时复制后排序。
- 修改 hash 结构会使该迭代器失效。

## 知识点覆盖
键迭代、无序容器、范围遍历、排序需求、迭代器失效。
