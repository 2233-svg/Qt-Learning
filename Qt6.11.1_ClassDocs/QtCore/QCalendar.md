# QCalendar
> Qt 6.11.1 · Qt Core · 来自 `QCalendar`

## 作用定位
`QCalendar` 在儒略日与指定历法的年、月、日之间转换，支持公历以外的内置历法。

## API 速查
| API | 是做什么的 |
|---|---|
| `dateFromParts()` | 用历法字段构造日期。|
| `partsFromDate()` | 将日期拆为历法字段。|
| `monthsInYear()` | 查询一年中的月份数。|
| `daysInMonth()` | 查询某月天数。|
| `monthName()` | 返回本地化月份名。|
| `isLeapYear()` | 判断历法闰年。|

## 使用场景
按用户选定历法显示、输入和校验日期。

## 常见坑与经验
- 历法解释与时区无关；跨日计算仍要使用 `QDateTime` 和 `QTimeZone`。

## 知识点覆盖
历法、儒略日、日期转换、闰年、本地化。
