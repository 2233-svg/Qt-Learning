# QVBoxPlotModelMapper
> Qt 6.11.1 · Qt Charts · 来自 `QVBoxPlotModelMapper`

## 作用定位
`QVBoxPlotModelMapper` 将模型列映射为多个 `QBoxSet`，用连续行读取五数概括。

## API 速查
| API | 是做什么的 |
|---|---|
| `setModel()` / `setSeries()` | 绑定模型和箱线图。|
| `setFirstColumn()` / `setColumnCount()` | 指定箱体列范围。|
| `setFirstRow()` / `setLastRow()` | 指定五数行范围。|

## 使用场景
电子表格中每列一个组别、每五行依次存统计摘要。

## 常见坑与经验
- 行/列方向与 `QHBoxPlotModelMapper` 相反，先画出表格坐标再配置。
- 模型表头不是五数数据，范围必须排除。

## 知识点覆盖
列记录、五数映射、表格方向、数据范围。
