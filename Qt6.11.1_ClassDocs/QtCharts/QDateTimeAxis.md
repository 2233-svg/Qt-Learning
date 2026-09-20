# QDateTimeAxis
> Qt 6.11.1 · Qt Charts · 来自 `QDateTimeAxis`

## 作用定位
`QDateTimeAxis` 用 `QDateTime` 表达连续时间轴，自动按时间格式生成标签。

## API 速查
| API | 是做什么的 |
|---|---|
| `setRange(min, max)` | 设置时间窗口。|
| `setMin()` / `setMax()` | 改变起止时间。|
| `setFormat()` | 设置显示格式，如 `HH:mm`。|
| `setTickCount()` | 设置主要时间标签数。|

## 使用场景
监控趋势、日志频率、市场数据、传感器时序。序列 X 值仍以自 epoch 起的毫秒数写入，轴负责把它解释为时间。

## 常见坑与经验
- 数据 X 坐标使用 `dateTime.toMSecsSinceEpoch()`，时区只影响标签解释；存储和展示应分别明确 UTC/本地时区。
- 时间窗口很短和很长时使用不同格式，避免标签都显示成相同日期或时间。

## 知识点覆盖
时间戳、时区、格式化、连续时间范围、时序数据。
