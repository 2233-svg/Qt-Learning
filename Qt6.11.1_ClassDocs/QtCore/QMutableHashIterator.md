# QMutableHashIterator
> Qt 6.11.1 · Qt Core · 来自 `QMutableHashIterator`

## 作用定位
`QMutableHashIterator<Key, T>` 是 Java 风格的可变哈希迭代器，可在遍历时修改当前值或移除当前键值项。

## API 速查
| API | 是做什么的 |
|---|---|
| `next()` / `previous()` | 前后移动到一条关联。|
| `key()` / `value()` | 读取当前键和值。|
| `setValue()` | 修改当前值。|
| `remove()` | 删除当前项。|
| `findNext()` | 向前定位键。|

## 使用场景
维护既有 Qt 代码时，在遍历 `QHash` 的同时清理过期缓存或原地修改值。

## 常见坑与经验
- 新代码通常使用 C++ iterator 配合 `erase()`，更易与标准算法协作。
- 迭代器之外同时修改底层 hash 会破坏遍历状态。

## 知识点覆盖
可变迭代器、哈希、遍历删除、缓存清理、旧式 API。
