# QAbstractAxis
> Qt 6.11.1 · Qt Charts · 来自 `QAbstractAxis`

## 作用定位
`QAbstractAxis` 是所有图表坐标轴的基类，统一管理标题、标签、网格线、可见性、反向方向和与 chart 的关系。

## API 速查
| API | 是做什么的 |
|---|---|
| `setTitleText()` | 设置轴标题。|
| `setLabelsVisible()` | 控制刻度标签显示。|
| `setGridLineVisible()` | 控制主网格线显示。|
| `setMinorGridLineVisible()` | 控制次网格线显示。|
| `setLineVisible()` | 控制轴线显示。|
| `setReverse()` | 反转轴方向。|
| `setShadesVisible()` | 显示交替色带。|
| `orientation()` / `alignment()` | 查询轴方向与 chart 边缘位置。|

## 使用场景
统一设置多张图的视觉规范，或在用户切换“从新到旧”时反转时间轴。

## 常见坑与经验
- 该类不定义数值范围；需要用 `QValueAxis`、`QDateTimeAxis` 等具体轴。
- 反转轴只影响显示方向，不改变原始数据顺序。

## 知识点覆盖
坐标轴基类、标签、网格、反向坐标、图表布局。
