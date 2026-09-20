# QMapIterator
> Qt 6.11.1 · Qt Core · 来自 `QMapIterator`

## 作用定位
`QMapIterator<Key, T>` 是 Java 风格的只读有序映射迭代器，按键排序顺序移动并支持前后查找。

## API 速查
| API | 是做什么的 |
|---|---|
| `hasNext()` / `next()` | 判断并移动到下一项。|
| `hasPrevious()` / `previous()` | 判断并移到前一项。|
| `key()` / `value()` | 读取当前位置键和值。|
| `findNext()` | 向前查找指定键。|
| `toFront()` / `toBack()` | 重置位置。|

## 使用场景
维护既有 Java 风格 Qt 代码，或需要显式反向移动的只读 map 遍历。

## 常见坑与经验
- 新代码更适合使用 C++ iterator、键值 range 或标准算法。
- 迭代期间修改底层 map 会使遍历行为不可靠。

## 知识点覆盖
Java 风格迭代、有序 map、双向遍历、容器修改、现代迁移。
