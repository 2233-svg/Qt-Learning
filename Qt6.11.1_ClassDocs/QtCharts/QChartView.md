# QChartView
> Qt 6.11.1 · Qt Charts · 来自 `QChartView`

## 作用定位
`QChartView` 是将 `QChart` 显示在 Widgets 界面中的 `QGraphicsView`。它负责 QWidget 尺寸、绘制和鼠标事件入口。

## API 速查
| API | 是做什么的 |
|---|---|
| `setChart()` | 设置要显示的图表，view 接管其所有权。|
| `chart()` | 取得当前图表。|
| `setRubberBand()` | 开启拖拽框选缩放或点击穿透模式。|
| `rubberBand()` | 查询当前框选策略。|

## 使用场景
将实时折线图嵌入 `QMainWindow`、表单或 dock：`setCentralWidget(new QChartView(chart))`。

## 常见坑与经验
- 需要自定义滚轮缩放和鼠标拖移时重实现事件处理，并以 `chart()->mapToValue()` 转回数据坐标。
- `QChartView` 仅服务 Widgets；Qt Quick 项目应选择 Qt Graphs 或在 QML 中使用相应图表组件。

## 知识点覆盖
Widgets 集成、Graphics View、框选缩放、事件处理、所有权。
