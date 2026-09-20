# QAbstractBarSeries
> Qt 6.11.1 · Qt Charts · 来自 `QAbstractBarSeries`

## 作用定位
`QAbstractBarSeries` 是柱状系列的共同基类，管理一个或多个 `QBarSet`、标签显示和柱体宽度。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` / `remove()` | 加入或移除 `QBarSet`。|
| `barSets()` | 查询当前数据集。|
| `setLabelsVisible()` | 显示柱体数值标签。|
| `setLabelsFormat()` | 定义标签内容格式。|
| `setLabelsPosition()` | 设置标签在柱内、柱顶等位置。|
| `setBarWidth()` | 设置同一类别中柱组占据的相对宽度。|

## 使用场景
做一套通用柱状图控制逻辑，如统一标签、悬停反馈与 set 的增删。

## 常见坑与经验
- `QBarSet` 是数据维度，类别轴是横向索引；不要把二者混为一谈。
- 标签过多会互相遮挡，应按尺寸或交互状态选择显示。

## 知识点覆盖
柱状数据结构、bar set、标签、宽度、系列多态。
