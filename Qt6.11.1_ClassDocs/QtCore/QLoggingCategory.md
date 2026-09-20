# QLoggingCategory
> Qt 6.11.1 · Qt Core · 来自 `QLoggingCategory`

## 作用定位
`QLoggingCategory` 为 Qt 日志按功能域分组，并允许运行时通过过滤规则控制 debug、info、warning 和 critical 是否输出。

## API 速查
| API | 是做什么的 |
|---|---|
| `Q_LOGGING_CATEGORY()` | 声明一个具名日志类别。|
| `qCDebug()` / `qCInfo()` | 按类别输出调试或信息日志。|
| `qCWarning()` / `qCCritical()` | 按类别输出警告或严重日志。|
| `isDebugEnabled()` | 判断某级别是否启用，避免昂贵构造。|
| `setFilterRules()` | 以规则字符串配置类别过滤。|
| `installFilter()` | 安装程序化过滤函数。|

## 使用场景
为网络、存储、同步、渲染等模块设置独立类别，生产环境按问题临时开启某一类诊断。

## 常见坑与经验
- 不要在日志表达式中无条件计算昂贵数据；先检查 `isDebugEnabled()`。
- 类别命名应稳定且分层，例如 `app.sync.upload`，便于精确过滤。
- 过滤控制输出量，不替代敏感信息脱敏。

## 知识点覆盖
结构化日志、日志级别、运行时过滤、性能、分类命名、隐私。
