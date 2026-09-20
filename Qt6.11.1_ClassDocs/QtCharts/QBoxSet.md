# QBoxSet
> Qt 6.11.1 · Qt Charts · 来自 `QBoxSet`

## 作用定位
`QBoxSet` 保存一个箱线图类别的五个统计值：下极值、下四分位数、中位数、上四分位数和上极值。

## API 速查
| API | 是做什么的 |
|---|---|
| `setLowerExtreme()` | 设置下须端。|
| `setLowerQuartile()` | 设置第一四分位数。|
| `setMedian()` | 设置中位数。|
| `setUpperQuartile()` | 设置第三四分位数。|
| `setUpperExtreme()` | 设置上须端。|
| `append()` | 按五数顺序填充统计值。|
| `setLabel()` | 设置类别标签。|

## 使用场景
先在数据层计算统计摘要，再构造 box set；绘图层不应承担排序和百分位计算。

## 常见坑与经验
- 必须满足 `lowerExtreme <= lowerQuartile <= median <= upperQuartile <= upperExtreme`；输入前校验。
- Qt 的 set 不自动替你从原始样本推导四分位。

## 知识点覆盖
统计摘要、四分位数、输入校验、数据层与视图层分工。
