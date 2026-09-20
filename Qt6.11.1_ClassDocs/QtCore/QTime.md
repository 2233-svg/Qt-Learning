# QTime
> Qt 6.11.1 · Qt Core · 来自 `QTime`
## 作用定位
`QTime` 表示一天内的时分秒毫秒，不包含日期和时区。它适合 UI 显示、每日时间点和短时间测量；跨日期和时区用 `QDateTime`。
## API 速查
| API | 是做什么的 |
|---|---|
| `QTime(h,m,s,ms)` | 创建时间。 |
| `currentTime()` | 当前本地时间。 |
| `isValid()` | 判断时间字段合法。 |
| `addSecs/addMSecs` | 按天内循环加减。 |
| `secsTo/msecsTo` | 计算两个时间差。 |
| `toString/fromString` | 格式化与解析。 |
## 使用场景
显示“每天 09:30 开始”的时间选择值。
## 常见坑与经验
- 不含日期，午夜跨越会让差值直觉出错。
- 不含时区，不能描述全球唯一时间点。
- 性能计时优先 `QElapsedTimer`。
## 知识点覆盖
本地时间、格式化、有效性、午夜跨越、日期时区边界。
