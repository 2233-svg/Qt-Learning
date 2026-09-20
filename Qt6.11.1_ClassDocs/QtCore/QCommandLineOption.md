# QCommandLineOption
> Qt 6.11.1 · Qt Core · 来自 `QCommandLineOption`

## 作用定位
`QCommandLineOption` 描述一个命令行选项的名称、帮助说明、取值占位符、默认值与隐藏状态；解析工作由 `QCommandLineParser` 完成。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数的名称列表 | 指定短选项和长选项，如 `v`、`verbose`。|
| `setDescription()` | 设置帮助文本。|
| `setValueName()` | 声明选项接收的值名称。|
| `setDefaultValue()` | 设置缺省值。|
| `setFlags()` | 设置隐藏、重复等行为标记。|
| `names()` | 读取所有别名。|

## 使用场景
为桌面工具、CLI 程序或测试程序定义 `--config <path>`、`--verbose`、`--format <type>` 等选项。

## 常见坑与经验
- 选项只描述语义，必须把它 `addOption()` 到 parser 才能解析。
- 帮助文本应说明值单位、默认值和互斥关系，不能只复述选项名。

## 知识点覆盖
CLI 设计、短长选项、默认值、帮助文本、参数语义。
