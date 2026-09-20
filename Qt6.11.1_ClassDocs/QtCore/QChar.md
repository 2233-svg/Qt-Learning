# QChar
> Qt 6.11.1 · Qt Core · 来自 `QChar`

## 作用定位
`QChar` 表示一个 UTF-16 代码单元。它适合处理 UTF-16 层面的分类、大小写和 Unicode 属性，但不总等于一个用户感知的“字符”。

## API 速查
| API | 是做什么的 |
|---|---|
| `unicode()` | 读取 UTF-16 单元值。|
| `isHighSurrogate()` / `isLowSurrogate()` | 判断代理项。|
| `surrogateToUcs4()` | 将代理对还原为 Unicode 码点。|
| `category()` | 查询 Unicode 分类。|
| `isLetter()` / `isDigit()` | 判断字符性质。|
| `toUpper()` / `toLower()` | 进行简单大小写转换。|

## 使用场景
实现 Unicode 字符过滤、逐 UTF-16 单元解析或检查代理对时使用。

## 常见坑与经验
- Emoji、组合附加符和某些文字可能由多个 `QChar` 构成；用户可见文本的“一个字符”应使用 grapheme cluster 概念。
- 复杂大小写规则优先交给 `QString` 和 locale-aware API。

## 知识点覆盖
UTF-16、代理对、Unicode 码点、字符分类、组合字符、大小写。
