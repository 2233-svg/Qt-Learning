# QTranslator
> Qt 6.11.1 · Qt Core · 来自 `QTranslator`
## 作用定位
`QTranslator` 加载 `.qm` 翻译文件并参与 `QObject::tr()` 的文本查找。它负责提供翻译表，不自动重建界面文本。
## API 速查
| API | 是做什么的 |
|---|---|
| `load()` | 加载翻译文件或资源。 |
| `translate()` | 查询上下文、源文本对应译文。 |
| `isEmpty()` | 判断是否加载了内容。 |
| `filePath()` / `language()` | 查询来源路径和语言。 |
| `QCoreApplication::installTranslator()` | 安装到应用翻译链。 |
| `removeTranslator()` | 移除翻译器。 |
## 使用场景
启动时按 `QLocale` 选择语言包，安装 translator，再创建 UI。
## 常见坑与经验
- 运行时切换语言后，需要响应 `LanguageChange` 并重新设置界面文本。
- translator 对象必须在安装期间保持存活。
- 翻译上下文通常是类名，重构类名可能影响旧翻译。
## 知识点覆盖
国际化、`.qm`、上下文、运行时切换、资源加载、对象生命周期。
