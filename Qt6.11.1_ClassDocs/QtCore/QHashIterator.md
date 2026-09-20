# QHashIterator
> Qt 6.11.1 · Qt Core · 来自 `QHashIterator`

## 作用定位
`QHashIterator<Key, T>` 是 Qt 提供的 Java 风格只读哈希迭代器，保留当前位置并通过 `next()`/`previous()` 移动。

## API 速查
| API | 是做什么的 |
|---|---|
| `hasNext()` / `next()` | 判断并移动到下一项。|
| `hasPrevious()` / `previous()` | 判断并移到前一项。|
| `key()` | 读取当前位置键。|
| `value()` | 读取当前位置值。|
| `findNext()` | 向前查找指定键。|
| `toFront()` / `toBack()` | 重置遍历位置。|

## 使用场景
维护既有 Qt Java 风格迭代代码，或需要反向移动的简单只读遍历。

## 常见坑与经验
- 新代码通常更适合 C++ 风格 iterator 或 range-for，能与标准算法更自然协作。
- 迭代期间不要修改底层 hash；它不提供并发安全快照。

## 知识点覆盖
Java 风格迭代器、哈希遍历、双向移动、容器修改限制、现代 C++ 迁移。
