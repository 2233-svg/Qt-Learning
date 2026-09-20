# QMessageLogger
> Qt 6.11.1 · Qt Core · 来自 `QMessageLogger`

## 作用定位
`QMessageLogger` 是 Qt 日志宏背后的消息构建器，可携带指定分类和源代码上下文创建 debug、info、warning、critical 或 fatal 输出流。

## API 速查
| API | 是做什么的 |
|---|---|
| `debug()` | 创建 debug 日志流。|
| `info()` | 创建 info 日志流。|
| `warning()` | 创建 warning 日志流。|
| `critical()` | 创建 critical 日志流。|
| `fatal()` | 输出 fatal 日志并终止进程。|
| `noDebug()` | 构建禁用的 debug 流。|

## 使用场景
框架或封装层需要保留调用位置、明确分类，并统一创建 Qt 日志输出时使用；业务代码通常直接写 `qCInfo()` 等宏。

## 常见坑与经验
- `fatal()` 不可用于普通错误恢复；它会结束进程，只适合无法继续保证正确性的情况。
- 自定义日志包装应尽量保留原调用点，避免所有日志都显示为同一个封装函数。
- 日志输出仍需脱敏，logger 本身不会过滤数据内容。

## 知识点覆盖
日志构建、日志等级、源位置、fatal、日志封装、脱敏。
