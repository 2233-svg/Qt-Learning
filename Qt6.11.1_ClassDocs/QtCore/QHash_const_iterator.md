# QHash::const_iterator
> Qt 6.11.1 · Qt Core · 来自 `QHash::const_iterator`

## 作用定位
`QHash::const_iterator` 用于只读遍历哈希表中的键值对。

## API 速查
| API | 是做什么的 |
|---|---|
| `key()` | 读取当前键。|
| `value()` | 读取当前值。|
| `operator*()` | 读取当前值。|
| `operator++()` | 前进到下一项。|
| `operator==()` | 比较迭代位置。|

## 使用场景
只读导出、调试打印、聚合统计哈希表内容。

## 常见坑与经验
- 不保证键顺序；需要稳定输出时先收集键并排序。
- 任何导致 hash 结构变更的操作都可能使迭代器失效。

## 知识点覆盖
const iterator、哈希遍历、无序性、迭代器失效、稳定输出。
