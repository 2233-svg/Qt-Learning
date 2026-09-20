# Qt QDebug 深入笔记

> 适用版本：Qt 6.11  
> 头文件：`#include <QDebug>`  
> 所属模块：`Qt6::Core`  
> 相关类：`QMessageLogger`、`QLoggingCategory`、`QDebugStateSaver`、`QTextStream`

## 1. 它解决什么问题：把诊断信息组织成一条可配置的日志消息

`QDebug` 是 Qt 的调试输出流。最常见的写法是 `qDebug() << ...`，它创建一个临时 `QDebug`，将多个 `<<` 的内容组成一条消息，并在临时对象析构时交给 Qt 的消息处理系统输出。

```cpp
qDebug() << "connected:" << host << "port:" << port;
```

它解决的是开发、测试和线上排障中的“看见运行时状态”问题：打印对象值、协议字段、状态迁移、失败原因和性能上下文。它不是业务数据传输协议，也不是稳定的机器可解析日志格式。

`QDebug` 虽继承 `QIODeviceBase`，但它不是一个让你 `open()` / `read()` / `write()` 的普通 `QIODevice`。这个继承主要服务于流格式能力；日常使用应把它理解为一次性的输出构建器。

| 输出目标 | 适合的入口 | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 默认 Qt 日志 | `qDebug()`、`qInfo()`、`qWarning()` 等 | 发送带消息类型和源码位置的 Qt 日志 | 生产代码更推荐分类日志，便于按规则过滤 |
| 自定义分类日志 | `qCDebug(category)` 等 | 将消息归入 `QLoggingCategory` | 分类禁用时可避免构造和计算日志参数 |
| 临时字符串表示 | `QDebug::toString(value)` | 调用已有流输出运算符生成 QString | 这是调试表示，不是稳定序列化格式 |
| 写到字符串或字节数组 | `QDebug(&string)`、`QDebug(&bytes)` | 将调试流内容写入调用方容器 | 容器必须比所有共享的 QDebug 实例活得久 |
| 结构化、长期日志 | 日志库或自定义消息处理器 | 记录可查询字段、时间戳和关联 ID | 不要解析默认 QDebug 文本作为长期接口 |

## 2. 最小可用代码：一条日志就是一个临时流

```cpp
#include <QDebug>

void connectToServer(const QString &host, quint16 port)
{
    qInfo() << "Connecting to" << host << "on port" << port;
}
```

`qDebug()`、`qInfo()`、`qWarning()`、`qCritical()` 和 `qFatal()` 都返回相应消息类型的 `QDebug` 流。每次调用应只组织一条逻辑消息，避免把同一个对象长时间保存为成员并跨线程写入。

Qt 默认会在写入项之间插入空格，并给 `QString`、`QByteArray`、`QChar` 加引号和转义不可打印字符：

```cpp
qDebug() << "name:" << "Ada";       // 类似：name: "Ada"
qDebug().noquote() << "name:" << "Ada"; // 类似：name: Ada
```

默认格式更利于辨别空字符串、换行、二进制数据和转义字符。排障日志通常保留默认引号；只有输出本来就面向人阅读的整段文本时再用 `noquote()`。

## 3. 日志级别与分类：级别表示严重性，分类控制噪声

### 3.1 选择消息级别

| 入口 | 用于什么 | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| `qDebug()` | 开发期细节、临时追踪 | 发送 Debug 级消息 | 构建可定义 `QT_NO_DEBUG_OUTPUT` 使其不产生输出 |
| `qInfo()` | 正常但值得记录的业务事件 | 发送 Info 级消息 | 不要把高频循环的细节都写成 info |
| `qWarning()` | 可恢复异常、降级、输入不合规 | 发送 Warning 级消息 | 要提供足够上下文，方便定位并评估频率 |
| `qCritical()` | 严重失败、当前操作无法完成 | 发送 Critical 级消息 | 记录错误码、请求标识和恢复动作 |
| `qFatal()` | 程序无法继续的不可恢复错误 | 输出 Fatal 消息后终止进程 | 不能用于普通错误分支；析构和锁清理策略要经得住终止 |

`qFatal()` 不是“比 `qCritical()` 更醒目一点”。它会使程序终止，所以只应放在不继续运行反而会造成更大损害的断言级失败中。网络超时、用户输入错误、文件不存在等常规失败应返回错误或写 warning/critical，而不是 fatal。

### 3.2 新代码优先使用 `QLoggingCategory`

```cpp
#include <QLoggingCategory>

Q_LOGGING_CATEGORY(logTransport, "app.transport")

void sendFrame(const QByteArray &frame)
{
    qCDebug(logTransport) << "Sending frame bytes:" << frame.size();
}
```

分类日志允许部署者通过 Qt logging rules 启用、关闭或调整不同模块的输出。更重要的是，当某个分类的 debug 日志关闭时，`qCDebug()` 的流表达式不会继续执行，因此昂贵的字符串拼接、容器格式化或临时计算可以避免发生。

```cpp
qCDebug(logTransport) << buildHugeDiagnosticSnapshot();
```

这比先判断开关再手写一套日志更简洁，但也别把有副作用的业务操作塞进日志表达式；日志被禁用时该表达式可能根本不执行。

## 4. 格式状态：空格、引号和 verbosity 都会持续到流结束

`QDebug` 的格式设置不是“只影响下一个值”，而是持续影响同一个流后续的输出。

```cpp
QDebug debug = qDebug();
debug.nospace() << '(' << x << ", " << y << ')';
debug << "next"; // 仍然处于 nospace 模式
```

这也是自定义输出运算符最常见的隐患：一个类型为了输出 `(x, y)` 改成 `nospace()`，却把调用方后续日志的格式也改坏了。解决办法是创建 `QDebugStateSaver`，使格式仅在当前作用域内变化。

```cpp
class Coordinate
{
public:
    int x() const;
    int y() const;
};

QDebug operator<<(QDebug debug, const Coordinate &value)
{
    QDebugStateSaver saver(debug);
    debug.nospace() << "Coordinate(" << value.x()
                    << ", " << value.y() << ')';
    return debug;
}
```

这个运算符有三个故意的设计：

1. `QDebug` 按值传入并按值返回，符合 Qt 的流式输出模式；
2. `QDebugStateSaver` 在返回前恢复空格、引号和 verbosity 等格式状态；
3. 运算符应定义在 `Coordinate` 所在命名空间，使参数依赖查找能在 `qDebug() << coordinate` 时找到它。

不要在该运算符里调用 `qDebug()` 创建第二条消息，也不要输出密码、访问令牌、用户隐私或大量二进制内容。一个值的 `operator<<` 应只向传入的那条消息追加紧凑、可诊断的表示。

### 4.1 与格式有关的 API

```cpp
qDebug().nospace().noquote()
    << '[' << categoryName << "] " << message;
```

- `nospace()` 关闭后续项之间的自动空格；`space()` 会立刻写入一个空格，并重新启用自动空格。
- `noquote()` 关闭字符串、字节数组和字符的自动引号与转义；`quote()` 重新启用，默认就是启用。
- `maybeSpace()` / `maybeQuote()` 只在相应自动选项开启时才写出字符，主要供自定义 `operator<<` 实现使用。
- `resetFormat()` 将流的格式选项恢复为构造时状态；局部自定义输出通常更适合 `QDebugStateSaver`。

## 5. 写到容器或设备：所有权仍在调用方

除默认日志目标外，`QDebug` 可直接写入 `QString`、`QByteArray` 或 `QIODevice`：

```cpp
QString text;
{
    QDebug stream(&text);
    stream.noquote() << "requestId=" << requestId;
} // 析构时刷新

QByteArray utf8;
{
    QDebug stream(&utf8);
    stream << "status" << 200;
    stream << Qt::flush; // 需要立刻取 byte array 时可显式刷新
}
```

这些构造函数不会接管 `text`、`utf8` 或 `device` 的所有权。目标对象必须在 `QDebug` 及其任何副本都析构前保持有效；目标设备还应当已经按需要打开并可写。

`QDebug(QByteArray *)` 从 Qt 6.9 起提供，输出编码为 UTF-8，可能缓冲到 `Qt::flush` 或流析构时才写入。不要把该字节数组当作本地 8 位编码文本，尤其在 Windows 等系统上 UTF-8 不一定等于系统 locale 编码。

## 6. 从已有流输出获得字符串：方便，但不是序列化

```cpp
const QString description = QDebug::toString(myObject);
const QByteArray utf8Description = QDebug::toBytes(myObject);
```

这两个模板函数要求 `myObject` 可被 `QDebug << myObject` 输出：

- `toString()` 从 Qt 6.0 起可用，会以 `nospace()` 模式构造 QString；
- `toBytes()` 从 Qt 6.9 起可用，效果等同 `toString(object).toUtf8()`，但更高效。

它们很适合断言失败信息、测试失败报告、调试面板和日志字段。不要把结果存入数据库后再依赖它反向解析：类型的调试输出可以在 Qt 版本、你的 `operator<<` 实现或格式偏好变化后改变。

## 7. verbosity：让自定义类型按诊断需求控制细节

`QDebug` 带一个 0 到 7 的 verbosity 值，默认是 2。它不是全局日志级别，也不会自动过滤消息；它只是传给流输出运算符的“希望输出多少细节”的提示。

```cpp
QDebug operator<<(QDebug debug, const ConnectionState &state)
{
    QDebugStateSaver saver(debug);
    debug.nospace() << "ConnectionState(" << state.id();

    if (debug.verbosity() >= QDebug::MaximumVerbosity)
        debug << ", pending=" << state.pendingCount();

    return debug << ')';
}
```

调用方可使用 `debug.verbosity(7)` 链式设置，或 `setVerbosity(7)` 修改流。不要用它替代 `QLoggingCategory`：类别决定消息是否应生成，verbosity 决定同一条已生成消息里对象打印多少细节。

## 8. 生命周期、线程和性能边界

### 8.1 临时对象何时真正输出

`qDebug() << ...` 的消息通常在该完整表达式结束、临时 `QDebug` 析构时提交。把 `QDebug` 复制给另一个对象会共享底层流状态；不要让副本跨越目标容器、设备或日志上下文的生命周期。

日志消息处理器可能同步执行，格式化大型容器也可能昂贵。高频路径应：

- 使用 `qCDebug()` 分类开关；
- 只输出关键字段和大小，而不是完整 payload；
- 避免在日志表达式中执行会修改状态、分配大量内存或触发 I/O 的函数；
- 对敏感字段做掩码，而不是期待日志规则永远正确配置。

### 8.2 自定义消息处理器不是 QDebug 的职责

`QDebug` 负责组织消息文本；最终写到终端、文件、系统日志或遥测后端由 Qt 消息处理机制决定。需要统一 JSON 日志、时间戳、线程标识或发送到外部服务时，应设计消息处理器和后台队列，并认真处理重入、崩溃路径与敏感数据。

## API 速查表
### 9.1 构造、共享与输出目标

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `MinimumVerbosity` | 最低 verbosity 值 `0` | 只是对象输出细节提示，不是日志过滤规则 |
| 枚举 | `DefaultVerbosity` | 默认 verbosity 值 `2` | 自定义类型不应假定调用方永远使用默认值 |
| 枚举 | `MaximumVerbosity` | 最高 verbosity 值 `7` | 适合输出昂贵诊断细节，但仍要避免敏感数据 |
| 构造 | `QDebug(QIODevice *device)` | 创建写入指定设备的调试流 | 不接管 device；设备必须在流存活期保持可写 |
| 构造 | `QDebug(QString *string)` | 创建写入指定 QString 的调试流 | 不接管 string；适合临时显示，不是稳定序列化 |
| 构造 | `QDebug(QByteArray *bytes)` | 创建写入指定 UTF-8 字节数组的调试流 | Qt 6.9 起；可能缓冲，立刻读取前使用 `Qt::flush` |
| 构造 | `QDebug(QtMsgType type)` | 创建提交给指定 Qt 消息处理器的流 | 直接构造缺少 `qDebug()` 宏自动携带的源码位置上下文 |
| 拷贝 | `QDebug(const QDebug &other)` | 复制并共享另一个流的内部状态 | 副本会共享格式与目标，目标对象必须活到所有副本结束 |
| 移动 | `QDebug(QDebug &&other)` | 转移流状态 | 移动后不要继续使用源对象来输出 |
| 赋值 | `operator=(const QDebug &other)` | 令当前流共享 other 的状态 | 覆盖前若有未完成输出，避免让生命周期难以判断 |
| 赋值 | `operator=(QDebug &&other)` | 通过移动替换当前流状态 | 用于封装时保持目标和源对象生命周期清楚 |
| 析构 | `~QDebug()` | 刷新待写数据并销毁流 | 这也是临时日志表达式通常提交消息的时机 |
| 交换 | `swap(QDebug &other)` | 高效交换两个流状态 | 目标、格式和待写数据会一同交换 |

### 9.2 格式、verbosity 与工具函数

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 空格 | `autoInsertSpaces() const` | 查询是否自动插入项间空格 | 只反映当前流状态，可能被自定义运算符改变 |
| 空格 | `setAutoInsertSpaces(bool enabled)` | 设置是否自动插入项间空格 | 自定义输出中优先用 `QDebugStateSaver` 恢复状态 |
| 空格 | `space()` | 立即写一个空格并启用后续自动空格 | 不只是状态切换，会产生一个实际空格 |
| 空格 | `nospace()` | 关闭后续自动空格 | 用于括号、逗号等紧凑格式；不要泄露到调用方 |
| 空格 | `maybeSpace()` | 在自动空格启用时写一个空格 | 多用于自定义 `operator<<` 的末尾 |
| 引号 | `quoteStrings() const` | 查询字符串是否自动带引号 | Qt 6.7 起；默认启用，便于观察不可打印字符 |
| 引号 | `setQuoteStrings(bool enabled)` | 设置字符串自动引号 | Qt 6.7 起；关闭后不再自动转义不可打印字符 |
| 引号 | `quote()` | 启用字符串、字符和字节数组自动引号 | 恢复安全且可读的默认诊断格式 |
| 引号 | `noquote()` | 关闭自动引号与转义 | 原始内容可能含换行或控制字符，避免用于不可信文本 |
| 引号 | `maybeQuote(char c = '"')` | 在自动引号启用时写指定字符 | 供格式实现使用；默认字符是双引号 |
| 重置 | `resetFormat()` | 恢复构造时的格式选项 | 局部运算符仍更适合 RAII 的 `QDebugStateSaver` |
| verbosity | `verbosity() const` | 读取 0 到 7 的详细程度提示 | 高值不等于分类已启用，也不等于消息更严重 |
| verbosity | `setVerbosity(int level)` | 设置详细程度提示 | 只应传 0 到 7；默认是 2 |
| verbosity | `verbosity(int level)` | 链式设置详细程度并返回流 | 适合 `debug.verbosity(7) << value` |
| 文本化 | `toString(const T &object)` | 用 `operator<<` 得到对象的 QString 调试表示 | Qt 6.0 起；内部使用 `nospace()`，不可作为协议序列化 |
| 文本化 | `toBytes(const T &object)` | 用 `operator<<` 得到对象的 UTF-8 字节表示 | Qt 6.9 起；等价于 toString 后 UTF-8 编码但更高效 |

### 9.3 `operator<<`：内建值、字符串、容器和自定义类型

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 基础值 | `operator<<(bool)` | 输出 `true` 或 `false` | 不要把日志文本当作可反序列化布尔格式 |
| 基础值 | `operator<<(char)`, `operator<<(QChar)`, `operator<<(char16_t)`, `operator<<(char32_t)` | 输出字符值 | 默认会引用或转义部分字符；原样输出需谨慎使用 `noquote()` |
| 整数 | `operator<<(signed/unsigned short)`, `operator<<(signed/unsigned int)`, `operator<<(signed/unsigned long)`, `operator<<(qint64)`, `operator<<(quint64)` | 输出整型数值 | 输出进制和格式仅用于诊断，协议字段应明确格式化 |
| 扩展整数 | `operator<<(qint128)`, `operator<<(quint128)` | 输出 128 位整数文本 | Qt 6.7 起且仅在构建支持 128 位整数时可用 |
| 浮点 | `operator<<(qfloat16)`, `operator<<(float)`, `operator<<(double)` | 输出浮点数 | 受显示精度影响；不要比较日志中的浮点文本 |
| 指针 | `operator<<(const void *)`, `operator<<(std::nullptr_t)` | 输出地址或空指针标识 | 地址可能泄露实现细节，不要在面向用户的日志中输出 |
| Qt 文本 | `operator<<(QString)`, `operator<<(QStringView)`, `operator<<(QLatin1StringView)` | 输出 Unicode 或 Latin-1 文本 | 默认引号和转义有助于识别空白和控制字符 |
| UTF-8 文本 | `operator<<(QUtf8StringView)`, `operator<<(const char *)`, `operator<<(const char16_t *)` | 输出 UTF-8 或 C 风格文本 | `const char *` 必须非空且指向有效终止字符串 |
| 字节数据 | `operator<<(QByteArray)`, `operator<<(QByteArrayView)` | 输出二进制或文本字节序列 | 默认转义以保持 7-bit 可读；大量 payload 只输出长度或摘要 |
| 标准字符串 | `operator<<(std::basic_string<Char>)`, `operator<<(std::basic_string_view<Char>)` | 输出 C++ 标准字符串和视图 | Qt 6.5 起；视图在调用期间必须有效 |
| chrono | `operator<<(std::chrono::duration)` | 输出数值及时间单位 | Qt 6.6 起；用于诊断，不要把文字单位用于机器协议 |
| 可选值 | `operator<<(std::optional<T>)`, `operator<<(std::nullopt_t)` | 输出 optional 的值或 `nullopt` | Qt 6.7 起；`T` 必须能被 QDebug 输出 |
| 元组 | `operator<<(std::tuple<Ts...>)` | 输出 tuple 中每个可输出元素 | Qt 6.9 起；所有元素都必须存在合适的 `operator<<` |
| Qt 容器 | `operator<<(QList)`, `operator<<(QSet)`, `operator<<(QMap)`, `operator<<(QMultiMap)`, `operator<<(QHash)`, `operator<<(QMultiHash)` | 输出常用 Qt 容器内容 | 大容器格式化昂贵；哈希容器顺序不应当被业务依赖 |
| 其它 Qt 值 | `operator<<(QContiguousCache)`, `operator<<(QVarLengthArray)`, `operator<<(QFlags)` | 输出这些 Qt 辅助类型 | `QVarLengthArray` 重载 Qt 6.3 起；flags 文本依赖枚举元信息 |
| 标准容器 | `operator<<(std::array)`, `operator<<(std::vector)`, `operator<<(std::list)`, `operator<<(std::set)`, `operator<<(std::multiset)` | 输出常用顺序或集合容器 | 部分重载 Qt 6.9 起；只用于受控大小的诊断 |
| 标准映射 | `operator<<(std::map)`, `operator<<(std::multimap)`, `operator<<(std::unordered_map)`, `operator<<(std::unordered_set)` | 输出标准映射和哈希集合 | unordered 容器遍历顺序不稳定，日志快照不可比较顺序 |
| 标准组合 | `operator<<(std::pair<T1, T2>)` | 输出一对可输出值 | 两个元素都要可通过 QDebug 输出 |
| 排序结果 | `operator<<(Qt::partial_ordering / weak_ordering / strong_ordering)` | 输出 Qt 三路比较结果 | Qt 6.9 起；用于诊断比较逻辑，不应用作持久化 |
| 自定义类型 | `operator<<(QDebug debug, const T &value)` | 让 `qDebug() << value` 能输出你的类型 | 定义在 T 的命名空间，按值传入返回，并用 `QDebugStateSaver` |

### 9.4 产生消息的宏

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 宏 | `qDebug()` | 创建 Debug 消息流，并记录调用位置 | 可被 `QT_NO_DEBUG_OUTPUT` 编译配置关闭；高频日志用分类版本 |
| 宏 | `qInfo()` | 创建 Info 消息流，并记录调用位置 | 适合重要正常事件，不要把常规细节淹没进 info |
| 宏 | `qWarning()` | 创建 Warning 消息流，并记录调用位置 | 写出可操作的上下文和恢复建议 |
| 宏 | `qCritical()` | 创建 Critical 消息流，并记录调用位置 | 不会自动终止；调用方仍需处理错误控制流 |
| 宏 | `qFatal()` | 创建 Fatal 消息流并在消息后终止进程 | 只用于不能安全继续的场景 |
| 分类宏 | `qCDebug(category)` | 创建受分类规则控制的 Debug 消息流 | 分类禁用时流表达式不执行，日志参数不能依赖副作用 |
| 分类宏 | `qCInfo(category)`, `qCWarning(category)`, `qCCritical(category)` | 创建受分类规则控制的其它级别消息流 | 用同一分类名组织模块，避免每个调用点新造类别 |

## 10. 一个既可读又不污染调用方格式的自定义类型

```cpp
namespace protocol {

struct FrameHeader {
    quint16 type;
    quint32 length;
};

QDebug operator<<(QDebug debug, const FrameHeader &header)
{
    QDebugStateSaver saver(debug);
    debug.nospace() << "FrameHeader(type=0x"
                    << Qt::hex << header.type
                    << Qt::dec << ", length="
                    << header.length << ')';
    return debug;
}

} // namespace protocol
```

这样调用：

```cpp
qCDebug(logTransport) << "received" << header;
```

输出运算符提供了足够的字段让开发者定位问题，又不会把整帧 payload、隐私字段或调用者的格式状态拖进日志。对复杂对象，这种克制通常比“把所有成员递归打印出来”更有排障价值。
