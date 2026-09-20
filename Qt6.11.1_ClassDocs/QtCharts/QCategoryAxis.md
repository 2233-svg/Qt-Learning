# QCategoryAxis
> Qt 6.11.1 · Qt Charts · 来自 `QCategoryAxis`

## 作用定位
`QCategoryAxis` 在连续数值区间上按分段显示类别标签，适合阈值、等级和不等宽区间。

## API 速查
| API | 是做什么的 |
|---|---|
| `append(label, endValue)` | 添加一个结束于指定数值的类别区间。|
| `remove(label)` | 删除标签区间。|
| `setStartValue()` | 设置第一个区间的起点。|
| `setLabelsPosition()` | 选择标签居中或放在值线上。|
| `categoriesLabels()` | 读取标签列表。|

## 使用场景
质量等级区间、温度警戒带、薪资档位、风险评分分段。

## 常见坑与经验
- `endValue` 是连续坐标边界，不是数组索引；区间应严格递增。
- 它不适合等间隔的普通类别柱图，那里用 `QBarCategoryAxis`。

## 知识点覆盖
分段坐标、阈值、连续值分类、标签位置、区间验证。
