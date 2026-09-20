# QCandlestickSeries
> Qt 6.11.1 · Qt Charts · 来自 `QCandlestickSeries`

## 作用定位
`QCandlestickSeries` 显示按时间排列的 OHLC 蜡烛数据，每个 `QCandlestickSet` 包含开、高、低、收。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` / `remove()` | 管理蜡烛集合，加入后系列拥有它。|
| `sets()` | 读取当前蜡烛集合。|
| `setIncreasingColor()` | 设置上涨蜡烛颜色。|
| `setDecreasingColor()` | 设置下跌蜡烛颜色。|
| `setBodyWidth()` | 设置实体相对宽度。|
| `setMaximumColumnWidth()` | 限制高密度时的蜡烛宽度。|
| `clicked()` / `hovered()` | 处理单根蜡烛交互。|

## 使用场景
金融 K 线、按时间桶汇总的高低范围、设备每日开闭指标。

## 常见坑与经验
- 时间戳应统一时区和时间桶边界，否则相邻蜡烛会错位。
- 并不所有 OHLC 数据都代表价格涨跌，颜色语义要按业务重新定义。

## 知识点覆盖
OHLC、时间桶、金融可视化、上涨下跌、密度控制。
