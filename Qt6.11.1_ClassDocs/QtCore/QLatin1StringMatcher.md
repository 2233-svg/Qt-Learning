# QLatin1StringMatcher
> Qt 6.11.1 · Qt Core · 来自 `QLatin1StringMatcher`

## 作用定位
`QLatin1StringMatcher` 为固定 Latin-1 模式预处理搜索状态，以便在多个 `QString` 或字符串视图中重复查找。

## API 速查
| API | 是做什么的 |
|---|---|
| `setPattern()` | 设置固定 Latin-1 模式。|
| `pattern()` | 读取当前模式。|
| `indexIn()` | 在目标文本中查找首次匹配。|

## 使用场景
日志或协议文本反复检查固定 ASCII 标记，例如 header 名、分隔关键字。

## 常见坑与经验
- 它只按字符序列匹配，不提供 Unicode 归一化、locale 比较或正则表达式能力。
- 模式一旦含非 Latin-1 字符，应改用 `QStringMatcher` 或其他 Unicode 方案。

## 知识点覆盖
字符串搜索、模式预处理、Latin-1、Unicode 选择、性能。
