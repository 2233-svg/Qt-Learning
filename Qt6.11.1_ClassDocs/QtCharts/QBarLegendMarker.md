# QBarLegendMarker
> Qt 6.11.1 · Qt Charts · 来自 `QBarLegendMarker`

## 作用定位
`QBarLegendMarker` 对应柱状系列中的一个 `QBarSet`，所以图例通常代表“产品/维度”，而不是某一个类别柱。

## API 速查
| API | 是做什么的 |
|---|---|
| `series()` | 返回所属柱状系列。|
| `barset()` | 返回对应 `QBarSet`。|
| `label()` | 通常来自 bar set 标签。|
| `clicked()` | 可用于切换某个维度。|

## 使用场景
点击“Forecast”图例后，从系列中暂时移除或隐藏预测数据集。

## 常见坑与经验
- 隐藏整个 series 会连同其他 bar set 消失；按维度开关时应操作对应 set 或重建可见集合。
- 图例顺序通常反映 bar set 加入顺序，构建前确定稳定顺序。

## 知识点覆盖
柱状图例、数据维度、系列与数据集、交互筛选。
