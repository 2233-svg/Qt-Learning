# QDirListing::const_iterator
> Qt 6.11.1 · Qt Core · 来自 `QDirListing::const_iterator`

## 作用定位
`QDirListing::const_iterator` 是 `QDirListing` 用于 range-for 的只读输入迭代器，每次解引用得到一个 `DirEntry`。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator*()` | 读取当前目录条目。|
| `operator->()` | 访问当前条目成员。|
| `operator++()` | 推进到下一条目。|
| `operator==()` | 与终止哨兵比较。|

## 使用场景
由 range-for 自动使用；只有封装通用目录遍历算法时才直接操作它。

## 常见坑与经验
- 这是单趟输入迭代器思维模型，不要复制后期待多个副本独立稳定遍历。
- 不要在条目引用生命周期之外保存其内部临时视图。

## 知识点覆盖
输入迭代器、ranges、只读遍历、迭代器生命周期。
