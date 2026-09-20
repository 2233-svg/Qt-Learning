# QVXYModelMapper
> Qt 6.11.1 · Qt Charts · 来自 `QVXYModelMapper`

## 作用定位
`QVXYModelMapper` 按“列是数据点”的方向，将两行映射为 `QXYSeries` 的 X 与 Y。

## API 速查
| API | 是做什么的 |
|---|---|
| `setModel()` / `setSeries()` | 绑定模型和目标系列。|
| `setXRow()` / `setYRow()` | 指定 X、Y 所在行。|
| `setFirstColumn()` / `setColumnCount()` | 限定映射列区间。|

## 使用场景
矩阵或宽表中，一行存时间、一行存对应测量值的科学数据。

## 常见坑与经验
- 行方向和 `QHXYModelMapper` 恰好相反；选错不会报错，只会得到错误图形。
- 频繁列插入时确认 mapper 能收到模型结构变更。

## 知识点覆盖
列方向映射、矩阵数据、模型变更、XY 系列。
