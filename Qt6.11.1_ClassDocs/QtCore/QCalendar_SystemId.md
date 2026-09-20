# QCalendar::SystemId
> Qt 6.11.1 · Qt Core · 来自 `QCalendar::SystemId`

## 作用定位
`QCalendar::SystemId` 是 Qt 内置历法系统的枚举标识，用于让 `QCalendar` 明确采用何种日期字段解释规则。

## API 速查
| API | 是做什么的 |
|---|---|
| `Gregorian` | 公历。|
| `Julian` | 儒略历。|
| `Milankovic` | 修订儒略历。|
| `IslamicCivil` | 伊斯兰民用历。|
| `Persian` | 波斯历。|

## 使用场景
构造 `QCalendar` 时指定用户需要的历法，而不是把月日年转换写死在界面代码里。

## 常见坑与经验
- 它只改变日期的解释与显示，不会改变时区、语言或地区格式。

## 知识点覆盖
历法枚举、国际化、日期解释、地区化。
