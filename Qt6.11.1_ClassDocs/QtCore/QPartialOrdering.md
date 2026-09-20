# QPartialOrdering
> Qt 6.11.1 · Qt Core · 来自 `QPartialOrdering`

## 作用定位
`QPartialOrdering` 表示两个值的三路比较结果：小于、等价、大于或不可比较。它适合浮点 NaN 等不存在完整全序关系的值。

## API 速查
| API | 是做什么的 |
|---|---|
| `less` | 表示左值小于右值。|
| `equivalent` | 表示两值等价。|
| `greater` | 表示左值大于右值。|
| `unordered` | 表示两值不可比较。|
| `operator<` 等 | 与零比较结果状态。|

## 使用场景
实现或消费 Qt 三路比较 API，特别是可能出现 NaN、缺失值或语义上不具备全序的领域值。

## 常见坑与经验
- `unordered` 不是等价；排序算法若要求严格弱序，必须先定义 NaN/缺失值应放在何处。
- 不要把 partial ordering 的结果直接当 bool 比较，否则会丢失不可比较状态。

## 知识点覆盖
三路比较、部分序、NaN、排序契约、缺失值、C++ 比较语义。
