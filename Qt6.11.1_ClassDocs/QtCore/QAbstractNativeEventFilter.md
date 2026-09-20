# QAbstractNativeEventFilter
> Qt 6.11.1 · Qt Core · 来自 `QAbstractNativeEventFilter`

## 作用定位
`QAbstractNativeEventFilter` 允许应用在 Qt 转换前查看 Windows、X11、macOS 等平台原生事件。

## API 速查
| API | 是做什么的 |
|---|---|
| `nativeEventFilter()` | 接收原生事件并决定是否拦截。|
| `installNativeEventFilter()` | 安装到 `QCoreApplication`。|
| `removeNativeEventFilter()` | 移除过滤器。|

## 使用场景
集成平台 SDK、处理系统热键或特殊窗口消息。

## 常见坑与经验
- `message` 的真实类型由 `eventType` 和平台决定，错误强转会崩溃。
- 过滤器应极轻量，且必须避免把平台专属代码散入跨平台业务层。

## 知识点覆盖
原生事件、平台差异、事件过滤、ABI 指针、跨平台隔离。
