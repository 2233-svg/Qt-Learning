# QBoxPlotSeries
> Qt 6.11.1 · Qt Charts · 来自 `QBoxPlotSeries`

## 作用定位
`QBoxPlotSeries` 显示多个 `QBoxSet` 的五数概括，用于比较一组分布的中位数、四分位区间和极值。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` / `remove()` | 管理 `QBoxSet`，加入后系列拥有它。|
| `boxSets()` | 读取所有箱体。|
| `count()` | 查询箱体数。|
| `setBrush()` / `setPen()` | 设置整体外观。|
| `clicked()` / `hovered()` | 响应箱体交互。|

## 使用场景
比较多个版本的测试耗时、不同工厂批次的质量分布、多个组别的统计摘要。

## 常见坑与经验
- 箱线图不是原始点云；它会隐藏多峰、样本量和离群点细节，应按需叠加散点。
- 不同统计库对 whisker 定义不一致，文档需说明是 min/max 还是 1.5 IQR。

## 知识点覆盖
五数概括、四分位数、中位数、分布比较、统计说明。
