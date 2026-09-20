# QCandlestickSet
> Qt 6.11.1 · Qt Charts · 来自 `QCandlestickSet`

## 作用定位
`QCandlestickSet` 保存一个时间点或时间桶的开盘、最高、最低、收盘值以及时间戳。

## API 速查
| API | 是做什么的 |
|---|---|
| `setOpen()` | 设置开值。|
| `setHigh()` | 设置最高值。|
| `setLow()` | 设置最低值。|
| `setClose()` | 设置收值。|
| `setTimestamp()` | 设置毫秒时间戳。|
| `setBrush()` / `setPen()` | 覆盖单根蜡烛外观。|

## 使用场景
从交易、传感器或日志流按固定窗口聚合 OHLC，再追加一个 set。

## 常见坑与经验
- 应满足 `low <= min(open, close) <= max(open, close) <= high`；异常输入会产生误导性图形。
- timestamp 是数值毫秒，不含时区；展示时间轴时统一选择 UTC 或本地时间。

## 知识点覆盖
OHLC 约束、时间戳、单项样式、数据聚合、输入校验。
