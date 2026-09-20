# QPieLegendMarker
> Qt 6.11.1 · Qt Charts · 来自 `QPieLegendMarker`

## 作用定位
`QPieLegendMarker` 是图例中对应一个 `QPieSlice` 的条目。

## API 速查
| API | 是做什么的 |
|---|---|
| `series()` | 返回所属 `QPieSeries`。|
| `slice()` | 返回对应切片。|
| `label()` | 默认反映切片标签。|
| `clicked()` | 可用于切换切片爆炸或筛选状态。|

## 使用场景
连接 `clicked()`，切换 `marker->slice()->setExploded()`，使图例成为饼图的选择控件。

## 常见坑与经验
- marker 由 legend 管理，切片删除后不能保存旧指针继续使用。
- 隐藏 marker 不是从饼图中移除切片。

## 知识点覆盖
饼图图例、对象关联、交互选择、生命周期。
