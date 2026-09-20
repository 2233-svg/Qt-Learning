# QCollator
> Qt 6.11.1 · Qt Core · 来自 `QCollator`

## 作用定位
`QCollator` 按指定 `QLocale` 的语言排序规则比较字符串，而不是按 Unicode 代码单元机械比较。

## API 速查
| API | 是做什么的 |
|---|---|
| `compare()` | 依据 locale 比较两个字符串。|
| `sortKey()` | 预生成可高效重复比较的排序键。|
| `setCaseSensitivity()` | 配置大小写是否影响排序。|
| `setNumericMode()` | 将嵌入数字按数值而非文本排序。|
| `setIgnorePunctuation()` | 配置是否忽略标点。|
| `setLocale()` | 设置排序语言环境。|

## 使用场景
文件名、联系人、产品名等面向用户的排序；如 `"file2"` 排在 `"file10"` 前可启用 numeric mode。

## 常见坑与经验
- 不要用 locale 排序结果做稳定数据库键或安全比较。
- 大量排序时预先计算 `QCollatorSortKey`，避免比较器反复做语言规则解析。

## 知识点覆盖
本地化排序、自然排序、大小写、标点、排序键、性能。
