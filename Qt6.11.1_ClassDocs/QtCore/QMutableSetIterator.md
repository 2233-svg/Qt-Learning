# QMutableSetIterator
> Qt 6.11.1 · Qt Core · 来自 `QMutableSetIterator`

## 作用定位
`QMutableSetIterator<T>` 是 Java 风格可变集合迭代器，可遍历唯一元素并删除当前元素。

## API 速查
| API | 是做什么的 |
|---|---|
| `next()` / `previous()` | 前后移动。|
| `value()` | 读取当前唯一元素。|
| `remove()` | 删除当前元素。|
| `findNext()` | 向前查找指定元素。|
| `toFront()` / `toBack()` | 重置遍历位置。|

## 使用场景
维护旧代码时，遍历 `QSet` 并移除已失效或不满足条件的元素。

## 常见坑与经验
- 集合无序，遍历顺序不能用于展示或持久格式。
- 新代码多用范围遍历配合容器删除策略；不要在迭代器外并发修改集合。

## 知识点覆盖
集合、唯一性、可变迭代、删除、无序性、旧式 API。
