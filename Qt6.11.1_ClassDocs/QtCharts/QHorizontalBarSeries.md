# QHorizontalBarSeries
> Qt 6.11.1 · Qt Charts · 来自 `QHorizontalBarSeries`

## 作用定位
`QHorizontalBarSeries` 是横向并排柱图。将类别放在纵轴可容纳更长的标签。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` | 添加并排的 `QBarSet`。|
| `setBarWidth()` | 设置柱组厚度。|
| `setLabelsVisible()` | 显示数值标签。|

## 使用场景
地区、项目、长名称排名列表；排序后读者更容易比较长度。

## 常见坑与经验
- 横向只改变视觉方向，不改变 bar set 与类别索引对齐规则。
- 排名图应按数值排序，否则横向布局失去主要优势。

## 知识点覆盖
横向柱图、长标签、排名、类别排序。
