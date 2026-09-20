# QHPieModelMapper
> Qt 6.11.1 · Qt Charts · 来自 `QHPieModelMapper`

## 作用定位
`QHPieModelMapper` 将同一模型行中的多个列映射为 `QPieSeries` 切片。

## API 速查
| API | 是做什么的 |
|---|---|
| `setModel()` / `setSeries()` | 绑定模型和饼图系列。|
| `setFirstColumn()` / `setColumnCount()` | 指定切片值列范围。|
| `setLabelsRow()` | 指定标签所在行。|
| `setValuesRow()` | 指定数值所在行。|

## 使用场景
一个记录行表示某个时点的类别构成，列对应各组成。

## 常见坑与经验
- 标签行和值行必须对应同一列序列。
- 非数值、负数和全零数据应在模型层过滤。

## 知识点覆盖
饼图映射、行数据、标签和值、比例校验。
