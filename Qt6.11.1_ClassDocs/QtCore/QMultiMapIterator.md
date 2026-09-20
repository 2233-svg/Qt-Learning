# QMultiMapIterator
> Qt 6.11.1 · Qt Core · 来自 `QMultiMapIterator`

## 作用定位
`QMultiMapIterator<Key, T>` 是 Java 风格的只读有序多值映射迭代器，可显式前后移动并读取每条关联。

## API 速查
| API | 是做什么的 |
|---|---|
| `hasNext()` / `next()` | 判断并前进。|
| `hasPrevious()` / `previous()` | 判断并后退。|
| `key()` / `value()` | 读取当前位置关联。|
| `findNext()` | 向前定位指定键。|
| `toFront()` / `toBack()` | 重置遍历位置。|

## 使用场景
维护既有 Qt Java 风格代码，或在有序一对多数据中做显式双向只读扫描。

## 常见坑与经验
- 新代码通常选择标准/C++ 风格 iterator 或 `asKeyValueRange()`。
- 遍历期间不要修改底层 `QMultiMap`。

## 知识点覆盖
Java 风格迭代、有序多值映射、双向扫描、现代 C++ 迁移。
