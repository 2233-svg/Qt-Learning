# QTextBoundaryFinder
> Qt 6.11.1 · Qt Core · 来自 `QTextBoundaryFinder`

## 作用定位
`QTextBoundaryFinder` 按 Unicode 规则查找字符、单词、句子或行边界，比按代码单元切字符串更适合用户可见文本。
## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 指定边界类型和文本。 |
| `toNextBoundary()` / `toPreviousBoundary()` | 前后移动到边界。 |
| `position()` / `setPosition()` | 查询或设置当前位置。 |
| `isAtBoundary()` | 判断当前位置是否边界。 |
| `boundaryReasons()` | 查询为什么这里是边界。 |
## 使用场景
实现按词跳转、双击选词、文本换行或截断预览。
## 常见坑与经验
- Unicode 用户可见字符不等于 `QString` 单个 `QChar`。
- 语言和脚本规则复杂，不要手写空格分词代替。
- 文本数据必须在 finder 使用期间保持有效。
## 知识点覆盖
Unicode 边界、字素簇、分词、换行、国际化文本编辑。
