# QQmlError：把 QML 诊断信息作为结构化值传递

> Qt 6.11.1 · `#include <QQmlError>` · 模块：`Qt6::Qml`

`QQmlError` 封装一次 QML 错误或警告的描述、文件 URL、行列位置、关联对象和日志级别。它解决的是组件加载、绑定求值和引擎警告不能只靠一段字符串排查的问题。

常见来源是 `QQmlComponent::errors()`、`QQuickView::errors()` 与 `QQmlEngine::warnings()`。拿到列表后，应保留每一项的位置与级别，而不是立即拼成一条没有结构的日志。

## 使用方式

```cpp
QQmlComponent component(&engine, QUrl(u"qrc:/ui/Panel.qml"_s));
if (component.isError()) {
    for (const QQmlError &error : component.errors())
        qWarning().noquote() << error.toString();
}
```

`toString()` 生成适合人读的一行文本，含 URL、行、列和描述。将 `QQmlError` 直接输出到 `QDebug` / `qWarning`，Qt 会尽力打开源文件并附带出错行及指示符，因此开发日志往往比手动只打印 `description()` 更有用。

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

## 字段的真实含义

- `url`、`line`、`column` 描述诊断位置。行列缺失不代表错误不严重，只表示该错误没有精确源位置。
- `description` 是人可读描述；不要用它做稳定机器匹配，Qt 版本和语言环境可能改变文案。
- `object` 是最接近出错位置的 QObject。绑定表达式异常通常会关联属性所属对象，其他异常可能为 `nullptr`。
- `messageType` 决定日志系统按 debug/info/warning/critical/fatal 中哪类处理；它不是 QML 编译阶段的“错误码”。
- 默认构造的 `QQmlError` 无效。`QQmlExpression::error()` 在无错误时正是返回这种无效值。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QQmlError()` | 创建空诊断 | 默认值 `isValid()` 为假。 |
| 拷贝/移动/赋值/`swap()` | 在错误列表间传递 | 是值类型，适合保存最近诊断。 |
| `isValid()` | 判断是否有诊断内容 | 在读取错误字段前做必要判断。 |
| `url()` / `setUrl()` | 读取/设置源文件 URL | 用 `QUrl` 保留 qrc、文件和网络来源。 |
| `line()` / `column()` | 读取/设置定位行列 | 缺失或零值不应被误解为“第一行错误”。 |
| `description()` / `setDescription()` | 读取/设置说明文本 | 面向展示与日志，不作稳定解析协议。 |
| `object()` / `setObject()` | 关联最近 QObject | 可能为空；不代表 QObject 所有权。 |
| `messageType()` / `setMessageType()` | 读取/设置 Qt 日志级别 | 决定相应日志 handler 的处理方式。 |
| `toString()` | 生成人类可读单行文本 | 适合日志和错误提示，不用于结构化存储。 |
| `operator<<(QDebug, error)` | 输出带上下文的诊断 | 可能附带源代码行和位置指示。 |
| `operator==` | 比较两个诊断值 | 适合测试或去重，不是错误恢复机制。 |

`QQmlError` 的价值在于保留错误位置和上下文。日志里若只剩“加载失败”，通常是因为这份结构化信息在边界处被过早丢掉了。
