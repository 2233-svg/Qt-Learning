# QMutableMultiMapIterator
> Qt 6.11.1 · Qt Core · 来自 `QMutableMultiMapIterator`

## 作用定位
`QMutableMultiMapIterator<Key, T>` 是 Java 风格的可变有序多值映射迭代器，可在遍历一对多关联时修改或删除当前关系。

## API 速查
| API | 是做什么的 |
|---|---|
| `next()` / `previous()` | 在按键排序的关联中移动。|
| `key()` / `value()` | 读取当前位置键和值。|
| `setValue()` | 修改当前关联值。|
| `remove()` | 删除当前键值关联。|
| `findNext()` | 向前查找指定键。|

## 使用场景
清理按时间或类别排序的一对多关联数据，或迁移同键多条记录的值格式。

## 常见坑与经验
- 删除的是一条关联，不一定删除该键的所有关联。
- 迭代器外部的结构修改会破坏遍历状态；新代码可优先 C++ iterator 与 `erase()`。

## 知识点覆盖
多值映射、可变迭代、单条关联删除、有序遍历、旧式 API。
