# QDateTime
> Qt 6.11.1 · Qt Core · 来自 `QDateTime`

## 作用定位
`QDateTime` 表示日期、时刻与时区/时间表示的组合。它既可表达一个绝对时间点，也可表达尚需解析的本地时间，使用时要明确两种语义。

## API 速查
| API | 是做什么的 |
|---|---|
| `currentDateTime()` / `currentDateTimeUtc()` | 获取当前本地或 UTC 时间。|
| `fromMSecsSinceEpoch()` | 从 Unix epoch 毫秒构造时间点。|
| `toMSecsSinceEpoch()` | 转为可存储/传输的 epoch 毫秒。|
| `toTimeZone()` | 转换为指定时区显示。|
| `setTimeZone()` | 改变时区解释。|
| `addSecs()` / `addDays()` | 时间或日历运算。|
| `secsTo()` / `msecsTo()` | 计算两个时刻距离。|
| `fromString()` / `toString()` | 解析或格式化。|

## 使用场景
服务端以 UTC epoch 持久化日志和事件；界面层用用户时区 `toTimeZone()` 显示。

## 常见坑与经验
- “本地 2026-11-01 01:30”在夏令时回拨时可能对应两个时刻；排班和预约必须保存时区与消歧策略。
- `addDays()` 是日历意义，`addSecs(86400)` 是绝对秒数；跨 DST 时二者可能不同。
- 仅传无时区格式字符串会导致不同机器解释不一致，协议优先 ISO 8601 UTC 或 epoch。

## 知识点覆盖
时间点、UTC、本地时间、时区、DST、epoch、格式化、日历运算。
