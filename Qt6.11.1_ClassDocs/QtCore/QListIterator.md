# QListIterator
> Qt 6.11.1 · Qt Core · 来自 `QListIterator`

## 作用定位
`QListIterator<T>` 是 Java 风格的只读列表迭代器，提供显式的 `next()`、`previous()` 和查找方法。

## API 速查
| API | 是做什么的 |
|---|---|
| `hasNext()` / `next()` | 判断并移动到下一元素。|
| `hasPrevious()` / `previous()` | 判断并移到前一元素。|
| `peekNext()` / `peekPrevious()` | 查看相邻元素但不移动。|
| `findNext()` / `findPrevious()` | 查找指定值。|
| `toFront()` / `toBack()` | 重置到首尾。|

## 使用场景
维护既有 Qt 代码，或需要可读性较强的双向只读遍历。

## 常见坑与经验
- 新代码优先 range-for 或 C++ iterator，便于配合标准算法。
- 底层列表在迭代期间被修改时，迭代器不会提供并发安全保护。

## 知识点覆盖
Java 风格迭代器、双向遍历、列表、容器修改、现代 C++ 迁移。
