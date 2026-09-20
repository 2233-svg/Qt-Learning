# QCandlestickLegendMarker
> Qt 6.11.1 · Qt Charts · 来自 `QCandlestickLegendMarker`

## 作用定位
`QCandlestickLegendMarker` 是关联 `QCandlestickSeries` 的图例条目。

## API 速查
| API | 是做什么的 |
|---|---|
| `series()` | 返回对应蜡烛系列。|
| `clicked()` | 响应图例点击。|
| `setVisible()` | 控制该图例条目。|

## 使用场景
多市场或多个聚合周期叠加时，通过 marker 切换某一个蜡烛系列。

## 常见坑与经验
- 单个 marker 代表整套 series，不代表上涨和下跌两种颜色。
- 切换隐藏后仍应保留必要的轴范围逻辑，避免视图突然缩放得难以比较。

## 知识点覆盖
蜡烛图图例、系列开关、可见范围、交互。
