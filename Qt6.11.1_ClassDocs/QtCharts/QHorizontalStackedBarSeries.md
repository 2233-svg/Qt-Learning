# QHorizontalStackedBarSeries
> Qt 6.11.1 · Qt Charts · 来自 `QHorizontalStackedBarSeries`

## 作用定位
`QHorizontalStackedBarSeries` 将组成部分横向堆叠，适合带长类别标签的总量与构成比较。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` | 添加一个组成层。|
| `barSets()` | 查询所有层。|
| `setLabelsPosition()` | 设置分段标签位置。|

## 使用场景
按部门显示人力组成、按地区显示订单状态，类别名称很长时尤其合适。

## 常见坑与经验
- 中间堆叠段的比较仍不精确；强调某一部分时可单独展示或排序。
- 负数与正数构成应有清晰颜色和零线。

## 知识点覆盖
横向堆叠、构成比较、长标签、零线、排序。
