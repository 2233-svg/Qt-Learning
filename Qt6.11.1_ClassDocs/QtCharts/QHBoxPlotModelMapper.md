# QHBoxPlotModelMapper
> Qt 6.11.1 · Qt Charts · 来自 `QHBoxPlotModelMapper`

## 作用定位
`QHBoxPlotModelMapper` 将模型行映射为多个 `QBoxSet`，并用连续列取五数概括。

## API 速查
| API | 是做什么的 |
|---|---|
| `setModel()` / `setSeries()` | 绑定模型与箱线图系列。|
| `setFirstRow()` / `setRowCount()` | 指定箱体行。|
| `setFirstColumn()` | 指定五数起始列。|
| `setLastColumn()` | 指定五数结束列。|

## 使用场景
每行是一组统计摘要，列按低值、Q1、中位数、Q3、高值排列的报表。

## 常见坑与经验
- mapper 不会检查五数单调性；必须在数据层验证。
- 五个数的列顺序必须固定。

## 知识点覆盖
箱线图映射、五数概括、行记录、统计校验。
