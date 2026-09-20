# QHXYModelMapper
> Qt 6.11.1 · Qt Charts · 来自 `QHXYModelMapper`

## 作用定位
`QHXYModelMapper` 按“行是数据点”的方向，把 model 的两列映射为 `QXYSeries` 的 X、Y。

## API 速查
| API | 是做什么的 |
|---|---|
| `setModel()` | 指定数据模型。|
| `setSeries()` | 指定目标 XY 系列。|
| `setXColumn()` / `setYColumn()` | 指定坐标列。|
| `setFirstRow()` / `setRowCount()` | 限定映射行区间。|

## 使用场景
表格每行是一条测量记录，列 0 为时间、列 1 为数值时使用。

## 常见坑与经验
- 模型角色必须能转换为数值；格式化字符串应留给轴标签而非模型数值列。
- 表头行不要误映射成第一条数据。

## 知识点覆盖
模型视图、行方向映射、XY 数据、数值转换、范围控制。
