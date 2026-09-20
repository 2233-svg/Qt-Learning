# QStaticLatin1StringMatcher
> Qt 6.11.1 · Qt Core · 来自 `QStaticLatin1StringMatcher`

## 作用定位
`QStaticLatin1StringMatcher` 针对静态 Latin-1 文本模式做快速匹配，适合在大量 `QString` 或字符串视图中查找固定 ASCII/Latin-1 关键字。

## API 速查
| API | 是做什么的 |
|---|---|
| 静态模式构造 | 将字面量预处理为 matcher。 |
| `indexIn()` | 返回模式在文本中的位置。 |
| `pattern()` | 查询固定 Latin-1 模式。 |

## 使用场景
日志分类、HTTP 头名、配置关键字等模式固定且属于 Latin-1 的文本扫描。

## 常见坑与经验
- 非 Latin-1 文本不要强行用它表达；中文等内容使用 `QStringMatcher` 或正则。
- 位置以 Qt 字符索引计，与 UTF-8 字节偏移不同。
- 大小写敏感性按 API 设定处理，别依赖本地化大小写规则。

## 知识点覆盖
Latin-1、静态文本匹配、字符串视图、大小写、字符索引。
