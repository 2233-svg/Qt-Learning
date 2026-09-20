# QBoxPlotLegendMarker
> Qt 6.11.1 · Qt Charts · 来自 `QBoxPlotLegendMarker`

## 作用定位
`QBoxPlotLegendMarker` 是箱线图系列的图例条目，提供关联 `QBoxPlotSeries` 的入口。

## API 速查
| API | 是做什么的 |
|---|---|
| `series()` | 返回对应箱线图系列。|
| `clicked()` | 响应图例交互。|
| `setVisible()` | 显示或隐藏图例条目。|

## 使用场景
在多组统计图中，让用户通过图例控制某一整套分布是否显示。

## 常见坑与经验
- 与 bar/pie marker 不同，它通常关联系列而非单个五数箱。
- 样式应以 series 的画笔画刷为主，别把 marker 单独改成误导色。

## 知识点覆盖
箱线图图例、系列关联、样式一致性、交互。
