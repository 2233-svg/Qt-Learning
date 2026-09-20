# QMutableMapIterator
> Qt 6.11.1 · Qt Core · 来自 `QMutableMapIterator`

## 作用定位
`QMutableMapIterator<Key, T>` 是 Java 风格可变 `QMap` 迭代器，可按键序遍历并修改或删除当前键值项。

## API 速查
| API | 是做什么的 |
|---|---|
| `next()` / `previous()` | 在排序键序列中移动。|
| `key()` / `value()` | 读取当前位置键和值。|
| `setValue()` | 修改当前值。|
| `remove()` | 删除当前键值项。|
| `findNext()` | 查找后续指定键。|

## 使用场景
维护旧式代码时，对按时间/ID 排序的数据做原地修正或过期项清理。

## 常见坑与经验
- key 不能通过迭代器改写；变更键应删除旧项并插入新项。
- 新代码优先 C++ iterator 和 `erase()`，更容易与算法组合。

## 知识点覆盖
可变 map 迭代、有序键、遍历删除、键不变量、旧式 API。
