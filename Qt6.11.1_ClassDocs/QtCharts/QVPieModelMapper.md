# QVPieModelMapper
> Qt 6.11.1 · Qt Charts · 来自 `QVPieModelMapper`

## 作用定位
`QVPieModelMapper` 将同一模型列中的多个行映射为 `QPieSeries` 切片。

## API 速查
| API | 是做什么的 |
|---|---|
| `setModel()` / `setSeries()` | 绑定模型和饼图。|
| `setFirstRow()` / `setRowCount()` | 指定切片行范围。|
| `setLabelsColumn()` | 指定标签列。|
| `setValuesColumn()` | 指定数值列。|

## 使用场景
常规两列表：每行一类，第一列名称、第二列数值。

## 常见坑与经验
- 这是最接近普通数据库查询结果的饼图 mapper，但不要把超过少量类别的表直接画成饼。
- 模型排序会改变扇区顺序；通常按值降序更易读。

## 知识点覆盖
列数据、饼图切片、模型排序、类别数量、数值验证。
