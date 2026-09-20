# QHCandlestickModelMapper
> Qt 6.11.1 · Qt Charts · 来自 `QHCandlestickModelMapper`

## 作用定位
`QHCandlestickModelMapper` 将每一模型行作为一根蜡烛，并从不同列读取时间戳、开高低收。

## API 速查
| API | 是做什么的 |
|---|---|
| `setTimestampColumn()` | 指定时间列。|
| `setOpenColumn()` / `setHighColumn()` | 指定开、高列。|
| `setLowColumn()` / `setCloseColumn()` | 指定低、收列。|
| `setFirstSetRow()` / `setLastSetRow()` | 限定蜡烛行范围。|

## 使用场景
数据库查询每行是一根 K 线的标准 OHLC 表。

## 常见坑与经验
- 列的显示顺序不一定等于 OHLC 含义，必须显式配置。
- 时间列应为毫秒时间戳或可一致转换的数值。

## 知识点覆盖
OHLC 行映射、字段列、时间序列、范围控制。
