# QVCandlestickModelMapper
> Qt 6.11.1 · Qt Charts · 来自 `QVCandlestickModelMapper`

## 作用定位
`QVCandlestickModelMapper` 将每一模型列作为一根蜡烛，并从不同行读取时间戳和 OHLC。

## API 速查
| API | 是做什么的 |
|---|---|
| `setTimestampRow()` | 指定时间戳行。|
| `setOpenRow()` / `setHighRow()` | 指定开、高行。|
| `setLowRow()` / `setCloseRow()` | 指定低、收行。|
| `setFirstSetColumn()` / `setLastSetColumn()` | 限定蜡烛列范围。|

## 使用场景
来自表格/矩阵且每列代表一个时间桶的 OHLC 数据。

## 常见坑与经验
- 使用前确认数据是“记录按行”还是“时间按列”；这是 mapper 选择的唯一关键。
- 不规范数据先整理到模型层，别在绘制阶段猜字段。

## 知识点覆盖
OHLC 列映射、矩阵数据、字段方向、数据预处理。
