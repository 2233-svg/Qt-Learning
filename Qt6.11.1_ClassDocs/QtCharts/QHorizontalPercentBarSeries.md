# QHorizontalPercentBarSeries
> Qt 6.11.1 · Qt Charts · 来自 `QHorizontalPercentBarSeries`

## 作用定位
`QHorizontalPercentBarSeries` 把每行类别归一化为横向 100% 堆叠条，强调比例结构并适配长标签。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` | 加入一个比例层。|
| `setLabelsVisible()` | 显示百分比标签。|
| `type()` | 返回横向百分比柱状类型。|

## 使用场景
问卷选项结构、地区人口构成、工单状态占比。

## 常见坑与经验
- 小比例段的标签会挤压，宜仅在足够宽时显示，其他信息交给 tooltip。
- 它不能表达绝对基数，图标题和说明应避免暗示数量比较。

## 知识点覆盖
100% 堆叠、比例比较、长类别、标签拥挤、数据表达边界。
