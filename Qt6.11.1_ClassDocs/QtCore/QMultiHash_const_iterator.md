# QMultiHash::const_iterator
> Qt 6.11.1 · Qt Core · 来自 `QMultiHash::const_iterator`

## 作用定位
`QMultiHash::const_iterator` 只读遍历无序多值哈希中的每一条键值关联，同一键可出现多次。

## API 速查
| API | 是做什么的 |
|---|---|
| `key()` | 读取当前键。|
| `value()` | 读取当前关联值。|
| `operator++()` | 移到下一条关联。|
| `operator==()` | 比较迭代位置。|

## 使用场景
导出一对多索引、按 key 分组统计或在 `equal_range()` 内只读处理某键的值。

## 常见坑与经验
- 无序容器不保证任何稳定遍历顺序。
- 插入、删除和 rehash 后，现有迭代器可能失效。

## 知识点覆盖
多值哈希、只读迭代、键重复、无序性、迭代器失效。
