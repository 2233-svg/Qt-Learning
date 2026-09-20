# QTimeZone
> Qt 6.11.1 · Qt Core · 来自 `QTimeZone`
## 作用定位
`QTimeZone` 描述时区规则、UTC 偏移、夏令时和显示名称，用于把绝对时间与当地民用时间互相转换。
## API 速查
| API | 是做什么的 |
|---|---|
| `systemTimeZone()` | 当前系统时区。 |
| `utc()` | UTC 时区。 |
| `availableTimeZoneIds()` | 列出可用 IANA id。 |
| `isValid()` | 判断时区是否识别。 |
| `offsetFromUtc()` | 某时刻相对 UTC 偏移秒数。 |
| `hasDaylightTime()` / `isDaylightTime()` | 查询夏令时规则。 |
| `displayName()` | 本地化显示名。 |
## 使用场景
存储 UTC 时间，显示时按用户选择的 `QTimeZone` 转为当地时间。
## 常见坑与经验
- 时区偏移不是常量，同一地区随日期可能变化。
- 不要用缩写如 CST 做唯一标识，使用 IANA id。
- 夏令时跳变会产生不存在或重复的本地时间。
## 知识点覆盖
IANA 时区、UTC 偏移、DST、本地化显示、时间存储策略。
