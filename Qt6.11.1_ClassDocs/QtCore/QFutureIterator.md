# QFutureIterator
> Qt 6.11.1 · Qt Core · 来自 `QFutureIterator`

## 作用定位
`QFutureIterator<T>` 是遍历 `QFuture<T>` 多个结果的 Java 风格迭代器，会在需要时等待下一个结果可用。

## API 速查
| API | 是做什么的 |
|---|---|
| `hasNext()` | 判断是否仍有结果。|
| `next()` | 前进到下一个结果。|
| `peekNext()` | 读取下一个结果但不移动。|
| `value()` | 读取当前位置结果。|
| `toFront()` / `toBack()` | 重置到首尾位置。|

## 使用场景
后台任务逐步产生多个结果，消费者希望按结果序列依次处理。

## 常见坑与经验
- 迭代可能阻塞等待未来结果；不能在 GUI 线程使用它实现实时 UI。
- 新代码通常偏向 `QFuture` 的现代迭代器或 `QFutureWatcher`，仅在既有 Java 风格代码中使用。

## 知识点覆盖
Future 多结果、阻塞迭代、Java 风格迭代器、GUI 线程、渐进消费。
