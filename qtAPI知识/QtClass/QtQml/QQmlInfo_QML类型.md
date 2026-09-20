# QQmlInfo：把 C++ 诊断消息定位回 QML 源码

> Qt 6.11.1 | `#include <QQmlInfo>` | CMake: `Qt6::Qml`

`QQmlInfo` 不是供业务代码长期保存的日志对象，而是 QML 诊断输出的短命句柄。它解决的具体问题是：C++ 实现的 QML 类型在报错时，怎样把信息附带到实例所在的 QML 文件和行号，而不是只留下难以追踪的 C++ 日志。

## 什么时候值得用

假设 `Gauge` 是注册到 QML 的 C++ 类型。用户在 `Dashboard.qml` 中写了不合法的配置，属性 setter 发现错误。使用普通 `qWarning()` 能输出错误文本，却不知道是哪一个 QML 实例触发的；使用 `qmlWarning(this)` 则会尝试附上该对象被 QML 创建的位置。

它尤其适合：

- QML 可配置的 C++ 控件、数据模型和服务对象报告配置错误；
- 希望开发期日志能直接跳回 QML 文件的组件库；
- 在 `QQmlError` 已经保存位置和描述时，继续补充上下文。

它不替代分类日志系统。需要日志分类、运行时过滤或长期统一格式时，仍应围绕 `QLoggingCategory` 设计；`QQmlInfo` 负责的是 QML 源位置。

## 输出发生在析构时

三个工厂函数 `qmlDebug()`、`qmlInfo()`、`qmlWarning()` 返回 `QQmlInfo`。随后用 `<<` 写入文本；临时对象在完整表达式结束时析构，届时才连同上下文一次性输出。

```cpp
#include <QQmlInfo>

void Gauge::setMaximum(int maximum)
{
    if (maximum < 0) {
        qmlWarning(this) << "maximum must not be negative:" << maximum;
        return;
    }

    m_maximum = maximum;
    emit maximumChanged();
}
```

这也是它不应被存进成员变量的原因：保存句柄会推迟日志出现，析构发生在哪个作用域也变得不直观。将一条消息在一条表达式中写完最清楚。

传入的 `QObject *` 必须是相关的 QML 对象。若对象不是由 QML 引擎实例化，或该实例的位置跟踪不可用，日志会显示 `unknown location`；这不是异常，也不能通过该类凭空恢复源位置。

## 级别和错误对象

`qmlDebug()`、`qmlInfo()`、`qmlWarning()` 的差别是 Qt 消息类型，而不是格式或生命周期。`qmlInfo()` 在 Qt 5.9 起输出 info 级别，不能把它当 warning 使用。三者都可以附带一个 `QQmlError` 或 `QList<QQmlError>`，以复用已有的错误位置和文字。

```cpp
QQmlError error;
error.setDescription(u"Theme file could not be parsed"_s);
error.setUrl(url);
error.setLine(17);

qmlWarning(this, error) << "falling back to the built-in theme";
```

当 `QQmlError` 已足够表达失败时，不必额外拼出一份重复的文件、行号和错误文本。反过来，`QQmlInfo` 也不会把错误转换成可恢复的控制流；加载失败仍应通过调用方的错误处理路径处理。

## 使用边界

- `QQmlInfo` 继承 `QDebug`，可使用常见的 `operator<<`；但它是由工厂函数构造的 opaque handle，没有公开构造函数可供业务代码自行创建。
- 目标对象在日志表达式执行期间必须有效。不要在对象销毁后保存裸指针再调用 `qmlWarning()`。
- 日志只说明“某个 QML 实例在哪里”，不等同于当前 QML JavaScript 调用栈。
- 不要把用户可控的大量数据无节制写入 warning，避免日志淹没真正的配置问题。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `qmlDebug(const QObject *)` | 创建带 QML 上下文的 debug 消息句柄 | 未知源位置时仍输出消息，但位置为 `unknown location` |
| `qmlInfo(const QObject *)` | 创建 info 消息句柄 | Qt 5.9 起是 info，不是 warning |
| `qmlWarning(const QObject *)` | 创建 warning 消息句柄 | 适合可行动的配置或运行时异常，不替代错误恢复 |
| 三个函数的 `QQmlError` 重载 | 让输出带一个已有错误对象的定位信息 | 错误对象的内容由调用方负责正确填充 |
| 三个函数的 `QList<QQmlError>` 重载 | 一次关联一组解析/加载错误 | 适合批量报告，避免逐项丢失上下文 |
| `QQmlInfo::~QQmlInfo()` | 输出累积的消息与上下文 | 析构触发输出，因此不应长期保存句柄 |
| `QQmlInfo::operator<<` | 以 `QDebug` 风格追加内容 | 保持在同一完整表达式中，得到一条原子且易读的诊断 |

## 相关类型

- `QQmlError`：保存 QML URL、行列号和错误描述。
- `QDebug`：提供流式输出行为。
- `QQmlEngine`：负责创建 QML 对象，也决定对象是否有可用的 QML 实例上下文。
