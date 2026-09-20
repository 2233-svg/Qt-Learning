# QList::iterator
> Qt 6.11.1 · Qt Core · 来自 `QList::iterator`

## 作用定位
`QList::iterator` 是可写随机访问迭代器，用于遍历或就地修改列表元素。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator*()` | 读取或修改当前元素。|
| `operator->()` | 访问当前对象成员。|
| `operator++()` / `operator--()` | 前后移动。|
| `operator+()` / `operator-()` | 随机偏移。|
| `operator[]` | 访问相对位置元素。|

## 使用场景
批量规范化列表值、对已有对象序列原地修正状态。

## 常见坑与经验
- 写入共享 `QList` 可能触发 detach，旧迭代器或其他副本的引用不能再假定共享同一存储。
- 插入、移除或重分配后重新获取迭代器。

## 知识点覆盖
可写迭代器、随机访问、隐式共享、detach、迭代器失效。
