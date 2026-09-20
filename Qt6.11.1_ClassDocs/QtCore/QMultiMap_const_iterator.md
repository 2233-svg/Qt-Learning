# QMultiMap::const_iterator
> Qt 6.11.1 · Qt Core · 来自 `QMultiMap::const_iterator`

## 作用定位
`QMultiMap::const_iterator` 按键排序只读遍历多值映射中的每一条键值关联。

## API 速查
| API | 是做什么的 |
|---|---|
| `key()` | 读取当前键。|
| `value()` | 读取当前关联值。|
| `operator++()` / `operator--()` | 在有序关联中前后移动。|
| `operator==()` | 比较迭代位置。|

## 使用场景
按键顺序导出一对多数据、对某个 `equal_range()` 做只读分组处理。

## 常见坑与经验
- 同键项的 value 顺序不应被当成永久协议保证。
- 容器结构发生变化后，旧迭代器不能继续使用。

## 知识点覆盖
有序多值映射、只读迭代、分组范围、迭代器失效。
