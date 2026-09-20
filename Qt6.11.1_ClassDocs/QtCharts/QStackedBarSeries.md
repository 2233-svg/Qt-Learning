# QStackedBarSeries
> Qt 6.11.1 · Qt Charts · 来自 `QStackedBarSeries`

## 作用定位
`QStackedBarSeries` 将同一类别的多个 `QBarSet` 纵向累加，突出总量和部分组成。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` | 添加一个堆叠组成部分。|
| `barSets()` | 读取堆叠层。|
| `setLabelsPosition()` | 调整层内或顶部标签。|
| `type()` | 返回堆叠柱状类型。|

## 使用场景
预算构成、渠道总量及来源、能源结构随时间变化。

## 常见坑与经验
- 只有零基线的第一层便于精确比较；中间层不适合比较小差异。
- 正负值会分别向两侧堆叠，业务解释应明确。

## 知识点覆盖
堆叠、组成与总量、正负数据、视觉比较限制。
