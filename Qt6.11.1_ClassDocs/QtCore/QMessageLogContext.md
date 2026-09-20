# QMessageLogContext
> Qt 6.11.1 · Qt Core · 来自 `QMessageLogContext`

## 作用定位
`QMessageLogContext` 是 Qt 日志消息的源位置上下文，包含分类、文件、函数和行号，主要传给自定义 message handler。

## API 速查
| API | 是做什么的 |
|---|---|
| `category` | 日志类别名称。|
| `file` | 产生消息的源文件。|
| `line` | 源代码行号。|
| `function` | 产生消息的函数名。|
| `version` | 上下文结构版本。|

## 使用场景
安装 `qInstallMessageHandler()` 后，把 Qt 日志转为 JSON、系统日志或远程诊断事件，并附带可定位的源信息。

## 常见坑与经验
- 源文件路径和函数名可能暴露构建布局，不应在对外用户日志中无条件输出。
- message handler 运行在任意产生日志的线程中，必须线程安全且避免再次调用 Qt 日志造成递归。

## 知识点覆盖
日志上下文、源位置、message handler、线程安全、隐私、递归风险。
