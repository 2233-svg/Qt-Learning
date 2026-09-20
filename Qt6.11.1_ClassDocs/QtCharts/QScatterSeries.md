# QScatterSeries
> Qt 6.11.1 · Qt Charts · 来自 `QScatterSeries`

## 作用定位
`QScatterSeries` 以独立标记而非连线显示 XY 点，用于相关性、分布、离群值和实验样本。

## API 速查
| API | 是做什么的 |
|---|---|
| `setMarkerShape()` | 选择圆、矩形等点形状。|
| `setMarkerSize()` | 设置标记像素大小。|
| `setBorderColor()` | 设置标记边框色。|
| `setColor()` | 设置标记填充色。|
| `append()` / `replace()` | 写入散点数据。|

## 使用场景
观察两变量相关性、质量分布、异常点，或用散点叠加在折线上强调采样位置。

## 常见坑与经验
- 点重叠会掩盖密度；可降低透明度、抽样或改用聚合/热力方案。
- marker size 是像素视觉尺寸，不随数据坐标比例伸缩。

## 知识点覆盖
散点、相关性、离群值、视觉重叠、透明度、点标记。
