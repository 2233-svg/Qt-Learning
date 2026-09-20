# QDirListing::sentinel
> Qt 6.11.1 · Qt Core · 来自 `QDirListing::sentinel`

## 作用定位
`QDirListing::sentinel` 是 `QDirListing` range 的结束标记类型，用于判断迭代器是否已到达遍历末尾。

## API 速查
| API | 是做什么的 |
|---|---|
| `iterator == sentinel` | 判断是否已无更多目录条目。|
| `iterator != sentinel` | 判断是否可继续遍历。|

## 使用场景
通常由 range-for 隐式使用；自定义 ranges 算法或调试迭代协议时才会直接遇到。

## 常见坑与经验
- sentinel 不是可解引用元素，也不能递增；它只表示终点。

## 知识点覆盖
C++ ranges、sentinel、结束条件、输入范围。
