# QCandlestickModelMapper
> Qt 6.11.1 · Qt Charts · 来自 `QCandlestickModelMapper`

## 作用定位
`QCandlestickModelMapper` 是蜡烛图 mapper 的共同基类，统一持有 model 和目标 `QCandlestickSeries`。

## API 速查
| API | 是做什么的 |
|---|---|
| `setModel()` | 指定 OHLC 数据模型。|
| `setSeries()` | 指定接收数据的蜡烛系列。|
| `model()` / `series()` | 查询当前绑定。|

## 使用场景
构建能切换“按行读”与“按列读”的通用 OHLC 图表组件时，针对实际数据布局选其水平或垂直子类。

## 常见坑与经验
- 只设置 model 不等于确定 OHLC 字段位置，仍需在子类设置各列或各行。
- 数据刷新频率高时应评估 mapper 全量同步成本。

## 知识点覆盖
抽象 mapper、OHLC 模型、系列绑定、数据更新成本。
