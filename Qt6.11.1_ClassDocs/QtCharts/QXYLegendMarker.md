# QXYLegendMarker
> Qt 6.11.1 · Qt Charts · 来自 `QXYLegendMarker`

## 作用定位
`QXYLegendMarker` 是折线、散点、样条等 XY 系列的图例条目。

## API 速查
| API | 是做什么的 |
|---|---|
| `series()` | 返回对应 `QXYSeries`。|
| `label()` | 读取显示名称。|
| `clicked()` | 处理图例点击。|
| `setVisible()` | 控制 marker 自身可见性。|

## 使用场景
实现可点击曲线图例：点击后 `marker->series()->setVisible(!...)`，并同步调整 marker 透明度。

## 常见坑与经验
- 系列隐藏后可保留图例以便恢复，还是同时隐藏，应按交互设计明确。
- 不要把 legend marker 当作持久数据模型；它只是一层视图对象。

## 知识点覆盖
XY 图例、可见性切换、视图模型分离、交互反馈。
