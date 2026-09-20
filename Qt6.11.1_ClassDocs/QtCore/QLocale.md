# QLocale
> Qt 6.11.1 · Qt Core · 来自 `QLocale`

## 作用定位
`QLocale` 表示语言、脚本和地区的格式规则，用于用户可见的数字、货币、日期、时间、百分比和文本比较格式化。

## API 速查
| API | 是做什么的 |
|---|---|
| `system()` | 获取系统当前 locale。|
| `setDefault()` | 设置进程默认 locale。|
| `toString()` | 按 locale 格式化数字、日期和时间。|
| `toInt()` / `toDouble()` | 按 locale 解析文本数字。|
| `toCurrencyString()` | 格式化货币。|
| `decimalPoint()` / `groupSeparator()` | 查询数字格式符号。|
| `dateFormat()` / `timeFormat()` | 查询默认日期时间格式。|
| `language()` / `territory()` | 查询 locale 组成。|

## 使用场景
界面向用户显示金额、日期、数量和百分比；导入用户按本地区格式输入的数字。

## 常见坑与经验
- 存储与协议格式不要使用 `QLocale`；机器可读数据使用 ISO 8601、UTC、固定小数点或 JSON 数字。
- 系统 locale 可能在程序运行中变化，长期会话应决定是跟随系统还是固定用户设置。
- `1,234` 在不同地区可能表示一千二百三十四或一又二三四，解析外部文本必须知道来源 locale。

## 知识点覆盖
国际化、数字格式、货币、日期时间、输入解析、机器格式与用户格式区分。
