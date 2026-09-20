# QHBarModelMapper
> Qt 6.11.1 · Qt Charts · 来自 `QHBarModelMapper`

## 作用定位
`QHBarModelMapper` 将模型的连续行映射为 bar categories，并用指定列范围生成柱状系列的多个 `QBarSet`。

## API 速查
| API | 是做什么的 |
|---|---|
| `setModel()` / `setSeries()` | 绑定模型和柱状系列。|
| `setFirstBarSetColumn()` / `setLastBarSetColumn()` | 指定生成 bar set 的列范围。|
| `setFirstRow()` / `setRowCount()` | 指定类别行范围。|

## 使用场景
每行一个月份，每列一个产品的业务报表。

## 常见坑与经验
- 列标题不会自动成为 `QBarSet` 标签，需按模型 header 或业务规则设置。
- 类别轴标签仍需单独从模型提取或维护。

## 知识点覆盖
宽表、柱状组、行类别、列维度、模型映射。
