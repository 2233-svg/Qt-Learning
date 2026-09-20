# QSetIterator
> Qt 6.11.1 · Qt Core · 来自 `QSetIterator<T>`
## 作用定位
`QSetIterator` 是 Java 风格的只读 `QSet` 迭代器，适合需要 `hasNext()/next()` 控制流的旧式 Qt 代码；新代码通常更简洁地使用范围 for。
## API 速查
| API | 是做什么的 |
|---|---|
| `hasNext()` / `next()` | 前向检查与读取元素。 |
| `peekNext()` | 查看下一个元素但不前进。 |
| `toFront()` | 回到迭代前位置。 |
## 使用场景
遍历一个不会在过程中修改的集合。  
## 常见坑与经验
- 容器修改后迭代器失效；`QSet` 顺序不保证稳定。
- `next()` 前必须 `hasNext()`。
## 知识点覆盖
只读迭代、迭代器失效、无序集合、范围 for 替代。
