# QRegularExpression
> Qt 6.11.1 · Qt Core · 来自 `QRegularExpression`

## 作用定位
`QRegularExpression` 是基于 PCRE2 的正则模式对象。它负责保存、校验和编译规则，再通过 `match()` 或 `globalMatch()` 对文本产生结果；模式应复用，而不是在高频循环中反复构造。

## API 速查
| API | 是做什么的 |
|---|---|
| `QRegularExpression(pattern, options)` | 创建模式及匹配选项。 |
| `isValid()` / `errorString()` / `patternErrorOffset()` | 校验用户或配置提供的模式。 |
| `match()` | 返回一次匹配结果。 |
| `globalMatch()` | 返回所有匹配的惰性迭代器。 |
| `matchView()` / `globalMatchView()` | 以 `QStringView` 避免拷贝；源文本必须持续有效。 |
| `setPattern()` / `setPatternOptions()` | 改变模式并使其重新编译。 |
| `escape()` | 把普通文本转成字面量正则片段。 |
| `anchoredPattern()` | 包成完整字符串匹配规则。 |
| `fromWildcard()` | 将文件名式通配符转换成正则。 |
| `optimize()` | 提前优化已知将反复匹配的模式。 |

## 使用场景
```cpp
const QRegularExpression re(
    R"(^([A-Za-z][A-Za-z0-9_]*)=(.+)$)");
const auto match = re.match(line);
if (match.hasMatch())
    setValue(match.captured(1), match.captured(2));
```
外部输入模式先 `isValid()`；外部输入的“文本片段”拼进模式前先 `escape()`，不要让用户数据意外变成正则语法。

## 常见坑与经验
- `match()` 默认寻找第一个可匹配位置，不代表整个字符串符合；校验完整格式使用 `anchoredPattern()` 或明确的 `\A...\z`。
- `globalMatchView()` 的 match/iterator 引用源字符；不要传临时 `QString`。
- `.*` 在大文本和复杂回溯模式中可能造成性能灾难；限制字符类、长度或使用非贪婪量词。
- `DontCheckSubjectStringMatchOption` 只适合受控的有效 UTF-16，错误使用存在稳定性和安全风险。

## 知识点覆盖
PCRE2、捕获组、命名组、Unicode、锚定、通配符、输入校验、ReDoS、零拷贝视图。
