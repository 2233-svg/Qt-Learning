# QVBarModelMapper
> Qt 6.11.1 · Qt Charts · 来自 `QVBarModelMapper`

## 作用定位
`QVBarModelMapper` 将模型的连续列映射为 bar categories，并用行范围生成多个 `QBarSet`。

## API 速查
| API | 是做什么的 |
|---|---|
| `setModel()` / `setSeries()` | 绑定模型与柱状系列。|
| `setFirstBarSetRow()` / `setLastBarSetRow()` | 指定 bar set 行范围。|
| `setFirstColumn()` / `setColumnCount()` | 指定类别列范围。|

## 使用场景
每列一个时间点、每行一个度量项的交叉表。

## 常见坑与经验
- 与横向 mapper 的区别是数据矩阵方向，不是最终柱图的显示方向。
- 当模型中混有文本列时，限制映射范围以避免转换失败。

## 知识点覆盖
转置数据、柱状映射、行列语义、模型范围。
