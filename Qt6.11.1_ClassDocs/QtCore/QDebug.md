# QDebug
> Qt 6.11.1 · Qt Core · 来自 `QDebug`

## 作用定位
`QDebug` 是 Qt 流式诊断输出对象，`qDebug()`、`qInfo()`、`qWarning()` 和 `qCritical()` 都通过它格式化消息并交给 Qt 日志系统。

## API 速查
| API | 是做什么的 |
|---|---|
| `nospace()` / `space()` | 关闭或恢复自动空格。|
| `noquote()` / `quote()` | 控制字符串是否带引号和转义。|
| `verbosity()` | 查询当前日志详细级别。|
| `setVerbosity()` | 设置该输出流详细级别。|
| `maybeSpace()` / `maybeQuote()` | 自定义 `operator<<` 时遵从现有格式策略。|

## 使用场景
```cpp
qInfo().noquote() << "Loaded" << path << "records:" << count;
```
为自定义值类型实现 `operator<<(QDebug, const T&)` 时，使用 `QDebugStateSaver` 保存调用方已有格式。

## 常见坑与经验
- 日志中不能输出 token、密码、完整个人数据或私钥。
- 高频路径的日志会影响性能和时序，生产环境用 logging category 控制。
- `QDebug` 是临时流对象，不能保存引用到后续使用。

## 知识点覆盖
日志等级、流式输出、格式状态、敏感信息、性能、日志分类。
