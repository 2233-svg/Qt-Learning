# QMap::const_iterator
> Qt 6.11.1 · Qt Core · 来自 `QMap::const_iterator`

## 作用定位
`QMap::const_iterator` 以键升序只读遍历 `QMap` 中的键值项。

## API 速查
| API | 是做什么的 |
|---|---|
| `key()` | 读取当前键。|
| `value()` | 读取当前值。|
| `operator*()` | 读取当前值。|
| `operator++()` / `operator--()` | 在有序键序列中前后移动。|
| `operator==()` | 比较迭代位置。|

## 使用场景
按稳定键顺序导出配置、生成报表或执行范围统计。

## 常见坑与经验
- const iterator 不允许修改值；需要原地更新时使用可写 iterator。
- 修改 map 结构会使迭代器失效，遍历过程避免插入/删除。

## 知识点覆盖
有序迭代、键值遍历、稳定输出、const 正确性、迭代器失效。
