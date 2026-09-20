# QSet::const_iterator
> Qt 6.11.1 · Qt Core · 来自 `QSet<T>::const_iterator`
## 作用定位
这是 `QSet` 的 STL 风格只读迭代器，用于范围 for、算法和 `constBegin()/constEnd()`。
## API 速查
| API | 是做什么的 |
|---|---|
| `operator*` / `operator->` | 只读访问当前元素。 |
| `++` / `--` | 前后移动迭代器。 |
| `==` / `!=` | 判断位置是否相同。 |
## 使用场景
`for (auto it = set.cbegin(); it != set.cend(); ++it) use(*it);`
## 常见坑与经验
- 任何可能 rehash 的修改都会使迭代器失效。
- 不要依赖无序遍历顺序。
## 知识点覆盖
STL 迭代器、const 正确性、哈希重排、范围遍历。
