# QStringMatcher
> Qt 6.11.1 · Qt Core · 来自 `QStringMatcher`

## 作用定位
`QStringMatcher` 为重复查找同一个子串预处理匹配状态，比每次 `QString::indexOf()` 重新准备更适合热路径扫描。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 设置模式串和大小写敏感性。 |
| `setPattern()` | 更换查找模式。 |
| `setCaseSensitivity()` | 设置大小写规则。 |
| `indexIn()` | 在目标字符串或视图中找首次出现位置。 |
| `pattern()` | 查询当前模式。 |

## 使用场景
反复在多行日志中查找相同关键字。

## 常见坑与经验
- 模式经常变化时收益有限，直接 `indexOf()` 更简单。
- 它不是正则表达式，只做字面子串查找。
- 返回位置是 UTF-16 索引，不是 UTF-8 字节偏移。

## 知识点覆盖
子串搜索、预处理、大小写、Unicode 索引、正则与字面匹配区别。
