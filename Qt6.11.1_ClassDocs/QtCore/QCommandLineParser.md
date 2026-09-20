# QCommandLineParser
> Qt 6.11.1 · Qt Core · 来自 `QCommandLineParser`

## 作用定位
`QCommandLineParser` 将 `QCoreApplication::arguments()` 解析为具名选项和位置参数，并生成统一帮助与版本输出。

## API 速查
| API | 是做什么的 |
|---|---|
| `addOption()` / `addOptions()` | 注册选项描述。|
| `addPositionalArgument()` | 声明位置参数。|
| `process()` | 解析参数；出错时可能输出并退出。|
| `parse()` | 解析但由调用者处理错误。|
| `isSet()` | 判断选项是否出现。|
| `value()` / `values()` | 读取一个或多个选项值。|
| `showHelp()` / `showVersion()` | 输出帮助或版本并退出。|
| `setSingleDashWordOptionMode()` | 定义单横线多字符选项的解释方式。|

## 使用场景
应用启动后构建 parser，注册标准 help/version 选项，解析后将配置传入业务层。

## 常见坑与经验
- 需要测试错误分支时用 `parse()`；`process()` 更适合普通命令行入口。
- 不要同时让位置参数和可选参数模糊匹配同一个用户输入。
- 读取路径/数字后仍需进行业务级校验。

## 知识点覆盖
参数解析、位置参数、错误处理、帮助文本、CLI 测试、输入校验。
