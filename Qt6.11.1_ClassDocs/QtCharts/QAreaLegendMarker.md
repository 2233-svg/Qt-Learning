# QAreaLegendMarker
> Qt 6.11.1 · Qt Charts · 来自 `QAreaLegendMarker`

## 作用定位
`QAreaLegendMarker` 是关联 `QAreaSeries` 的图例条目，提供从 marker 回到区域系列的类型安全入口。

## API 速查
| API | 是做什么的 |
|---|---|
| `series()` | 返回所代表的 `QAreaSeries`。|
| `clicked()` | 响应图例点击。|
| `setVisible()` | 控制图例条目可见性。|

## 使用场景
点击图例时隐藏置信带，保留中心趋势线，帮助用户聚焦。

## 常见坑与经验
- 通过 series 改变可见性才影响区域绘制。
- marker 是 legend 的派生状态，数据系列重建后应重新获取。

## 知识点覆盖
面积图图例、类型安全转换、可见性、交互。
