# QList::const_iterator
> Qt 6.11.1 · Qt Core · 来自 `QList::const_iterator`

## 作用定位
`QList::const_iterator` 是只读随机访问迭代器，用于遍历列表而不修改元素。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator*()` / `operator->()` | 读取当前元素。|
| `operator++()` / `operator--()` | 前后移动。|
| `operator+()` / `operator-()` | 按偏移随机移动。|
| `operator[]` | 读取相对偏移元素。|
| `operator==()` | 比较迭代器位置。|

## 使用场景
只读遍历模型数据、导出列表或传入需要 const iterator 的标准算法。

## 常见坑与经验
- 列表结构改变、detach 或析构后，迭代器可能失效。
- 不要从临时 `QList` 获取 iterator 后延长使用。

## 知识点覆盖
const iterator、随机访问、列表遍历、隐式共享、迭代器生命周期。
