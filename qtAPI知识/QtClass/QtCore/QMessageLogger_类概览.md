# Qt QMessageLogger 日志调用器深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMessageLogger>`  
> 所属模块：`Qt6::Core`  
> 类型性质：携带源码上下文并发出 Qt 日志消息的轻量调用器  
> 相关类型：`QMessageLogContext`、`QLoggingCategory`、`QDebug`、`QtMsgType`

## 1. 它解决什么问题

`QMessageLogger` 是 Qt 日志系统中“带上下文发出一条消息”的调用器。它把：

- 文件名；
- 行号；
- 函数信息；
- 日志类别；

组合成一个 `QMessageLogContext`，然后通过 `debug()`、`info()`、`warning()`、`critical()` 或 `fatal()` 发出消息。

它同时提供两种写法：

1. `QDebug` 流式写法，适合 Qt 类型和类型安全的链式输出；
2. 类 `printf` 的格式字符串写法，适合已有 C 风格格式化代码。

```cpp
QMessageLogger(__FILE__, __LINE__, Q_FUNC_INFO)
    .warning() << "connection retry:" << retryCount;

QMessageLogger(__FILE__, __LINE__, Q_FUNC_INFO)
    .warning("connection retry: %d", retryCount);
```

日常代码通常直接使用 `qDebug()`、`qWarning()`、`qInfo()` 和 `qCritical()` 宏；需要自定义来源位置、转发已有错误位置或显式绑定类别时，再直接使用 `QMessageLogger`。

### 1.1 它不解决什么问题

`QMessageLogger` 不是：

- 日志文件写入器；
- 全局日志过滤规则管理器；
- `QLoggingCategory` 本身；
- 可长期保存的日志记录对象；
- 异步日志队列；
- C++ 异常或错误返回值的替代品。

消息最终如何显示、过滤和存储，由 Qt 消息处理器、类别规则、消息模式和应用自己的处理逻辑决定。

## 2. 实际使用场景

### 2.1 使用流式输出记录 Qt 类型

```cpp
QMessageLogger(__FILE__, __LINE__, Q_FUNC_INFO)
    .debug() << "rect:" << rect
             << "size:" << size;
```

流式形式可以直接使用 `QByteArray`、`QString`、`QRect`、容器等已有 `QDebug` 输出支持，避免手工转换成格式字符串。

### 2.2 转发外部错误的来源位置

```cpp
void logComponentErrors(const QList<QQmlError> &errors)
{
    for (const QQmlError &error : errors) {
        const QByteArray file = error.url().toEncoded();
        QMessageLogger(file.constData(), error.line(), nullptr)
            .debug() << error.description();
    }
}
```

这里的上下文不是当前 C++ 调用点，而是外部错误对象报告的文件和行号。`file` 必须活到完整日志表达式结束；不能把临时字符串的 `constData()` 保存到异步任务中。

### 2.3 为模块或子系统指定类别

```cpp
Q_LOGGING_CATEGORY(storageLog, "app.storage")

QMessageLogger(__FILE__, __LINE__, Q_FUNC_INFO)
    .warning(storageLog)
    << "cache entry missing";
```

更常见的写法是：

```cpp
qCWarning(storageLog) << "cache entry missing";
```

`qCWarning` 这类类别宏会把类别开关检查放在消息表达式之前，适合避免昂贵参数的无意义求值。

### 2.4 使用 printf 风格格式化

```cpp
QMessageLogger(__FILE__, __LINE__, Q_FUNC_INFO)
    .warning("retry %d failed for %s", retryCount,
             qUtf8Printable(hostName));
```

格式字符串重载适用于已经使用 C 风格格式的代码。格式说明符和参数类型必须匹配；需要输出 Qt 对象时，流式写法通常更稳妥。

### 2.5 在不可恢复分支发出 fatal 消息

```cpp
if (!criticalInvariantHolds)
    QMessageLogger(__FILE__, __LINE__, Q_FUNC_INFO)
        .fatal() << "invariant violated";
```

`fatal()` 表示不可恢复错误。消息处理后程序会终止，不能把它当作普通的可捕获异常或返回错误使用。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QMessageLogger>
#include <QLoggingCategory>
#include <QDebug>
```

使用 `QString`、`QByteArray` 或具体 Qt 类型时，还应包含对应的公开头文件。`QMessageLogger` 属于 `Qt6::Core`。

## 4. 核心使用模型

### 4.1 先创建带上下文的临时调用器

```cpp
QMessageLogger logger(
    QT_MESSAGELOG_FILE,
    QT_MESSAGELOG_LINE,
    QT_MESSAGELOG_FUNC);
```

Qt 的 `qDebug()` 等宏本质上会使用类似的源码位置构造方式。通常不需要把 `QMessageLogger` 长期保存；它是轻量、不可复制、用于一次或少数几次调用的对象。

### 4.2 再选择日志等级

| 成员 | 日志等级 | 常见用途 |
| --- | --- | --- |
| `debug` | `QtDebugMsg` | 开发诊断、细节状态 |
| `info` | `QtInfoMsg` | 正常运行信息 |
| `warning` | `QtWarningMsg` | 可恢复异常、配置问题 |
| `critical` | `QtCriticalMsg` | 严重错误 |
| `fatal` | `QtFatalMsg` | 不可恢复错误并终止 |

日志等级由成员选择决定，不由 `QMessageLogContext` 的字段决定。

### 4.3 再选择输出风格

流式：

```cpp
logger.info() << "items:" << count;
```

格式字符串：

```cpp
logger.info("items: %d", count);
```

两种写法最终都进入 Qt 消息系统，但格式化时机、类型安全性和参数求值方式不同。

### 4.4 需要类别时传类别对象或类别函数

类别对象：

```cpp
logger.debug(storageLog) << "loaded";
```

类别函数：

```cpp
logger.debug(storageCategory) << "loaded";
```

其中 `storageCategory` 的类型是 `QMessageLogger::CategoryFunction`，也就是返回 `const QLoggingCategory &` 的函数指针。`Q_DECLARE_LOGGING_CATEGORY` 生成的类别声明正是这种调用形式。

## 5. 上下文和生命周期边界

### 5.1 `QMessageLogger` 不拥有上下文字符串

构造函数保存的是 `const char *`：

```cpp
QMessageLogger(const char *file,
               int line,
               const char *function,
               const char *category);
```

它不会复制文件名、函数名或类别名。使用字符串字面量、`__FILE__`、`Q_FUNC_INFO` 或静态类别名最稳妥。

如果传入 `QByteArray::constData()`：

```cpp
const QByteArray file = error.url().toEncoded();
QMessageLogger(file.constData(), error.line(), nullptr)
    .warning() << error.description();
```

必须确保 `file` 活到整个日志表达式完成。不要把 logger 或其中的上下文指针放到 `file` 销毁之后继续使用。

### 5.2 不要长期保存 logger

`QMessageLogger` 禁止复制，且内部上下文通常指向调用点的静态字符串。它适合：

```cpp
QMessageLogger(...).warning() << message;
```

不适合把一个带临时字符串指针的 logger 保存到成员变量、跨线程队列或异步任务中。

### 5.3 `QMessageLogContext` 只在消息调用链中携带来源

logger 发出的消息会把上下文交给 Qt 的消息处理器。处理器若要异步保存，必须复制 `QMessageLogContext` 中的非拥有字段和实际消息文本。不要保存上下文地址或其中的 `const char *` 指针。

## 6. 流式和 printf 风格的边界

### 6.1 流式 API 的优点

```cpp
logger.debug() << "name:" << name
               << "value:" << value;
```

流式 API：

- 对 Qt 类型有现成输出运算符；
- 不需要手工计算格式说明符；
- 可以在表达式中组合多个值；
- 对 `QString`、容器和自定义 `QDebug` 输出更自然。

### 6.2 printf 风格 API 的约束

```cpp
logger.debug("name: %s, value: %d",
             qUtf8Printable(name), value);
```

格式字符串重载使用 C 风格可变参数。注意：

- `%s` 需要 `const char *`，不能直接传 `QString`；
- `%d`、`%lld`、`%f` 等必须与实际提升后的参数类型匹配；
- 不要把用户可控文本当作 format 参数，应该把它作为格式参数传入；
- 格式字符串错误可能导致未定义行为；
- 复杂 Qt 类型通常应改用流式写法；
- `QString::toUtf8()` 的临时值需要在完整表达式内保持有效，使用 `qUtf8Printable()` 时也应遵守表达式生命周期。

### 6.3 参数求值和类别宏的差异

直接调用：

```cpp
logger.debug() << expensiveObject();
```

或：

```cpp
logger.debug("value: %d", expensiveValue());
```

在进入调用前，C++ 参数和流插入表达式可能已经被求值。若希望类别关闭时连昂贵计算都不发生，优先使用：

```cpp
if (storageLog().isDebugEnabled())
    qCDebug(storageLog) << expensiveObject();
```

更常见的是直接写 `qCDebug(storageLog) << expensiveObject();`，类别宏内部会先判断输出控制。不要把“最终没有显示”误认为“参数完全没有求值”。

## 7. 成员类型和构造函数

### 7.1 `CategoryFunction`

```cpp
using CategoryFunction = const QLoggingCategory &(*)();
```

它表示一个返回日志类别对象引用的函数指针：

```cpp
const QLoggingCategory &storageCategory();
```

类别声明宏通常生成这种函数。传入类别函数可以让 logger 按 Qt 的类别接口获取类别对象：

```cpp
logger.info(storageCategory) << "opened";
```

不要把 `QLoggingCategory *`、类别名称字符串或普通无参函数返回值传给这个参数；签名必须匹配。

### 7.2 `QMessageLogger()`

```cpp
constexpr QMessageLogger();
```

构造默认上下文的 logger。它主要用于 Qt 的禁用输出宏和需要一个空 logger 的内部路径，普通应用日志更适合传入明确的源码位置或直接使用 `qDebug()` 等宏。

默认上下文中的文件、函数和类别可能为空；不要把默认构造当作自动捕获当前调用点。

### 7.3 `QMessageLogger(const char *, int, const char *)`

```cpp
constexpr QMessageLogger(const char *file,
                         int line,
                         const char *function);
```

构造使用默认类别的 logger。Qt 头文件中该构造会把类别设置为 `"default"`：

```cpp
QMessageLogger(__FILE__, __LINE__, Q_FUNC_INFO)
    .warning() << "something unusual";
```

`file`、`function` 可以为空；`line` 为 0 表示未知行号。

### 7.4 `QMessageLogger(const char *, int, const char *, const char *)`

```cpp
constexpr QMessageLogger(const char *file,
                         int line,
                         const char *function,
                         const char *category);
```

构造带显式类别的 logger：

```cpp
QMessageLogger(__FILE__, __LINE__, Q_FUNC_INFO,
               "app.storage")
    .info() << "cache ready";
```

类别字符串由调用方保证生命周期。这个构造设置消息上下文中的类别名；类别启用状态仍由 Qt 类别规则和处理器决定。

## 8. 逐项日志 API

下面每个等级都有两组重载：

- 不带类别参数的流式和格式字符串重载；
- 带 `QLoggingCategory` 对象或 `CategoryFunction` 的流式和格式字符串重载。

### 8.1 `debug() const`

```cpp
QDebug debug() const;
```

返回 debug 等级的 `QDebug` 流：

```cpp
logger.debug() << "state:" << state;
```

返回值是临时流对象，通常在同一条表达式中完成输出。它适合 Qt 类型和链式输出。

### 8.2 `debug(const QLoggingCategory &) const`

```cpp
QDebug debug(const QLoggingCategory &cat) const;
```

以指定类别发出 debug 流：

```cpp
logger.debug(storageLog) << "cache hit";
```

类别对象必须在调用期间有效。对于需要在类别关闭时避免昂贵表达式求值的代码，优先使用 `qCDebug(storageLog)`.

### 8.3 `debug(CategoryFunction) const`

```cpp
QDebug debug(CategoryFunction catFunc) const;
```

通过类别工厂函数获取类别并发出 debug 流：

```cpp
logger.debug(storageCategory) << "cache hit";
```

`catFunc` 应返回有效的 `const QLoggingCategory &`。类别函数通常来自 Qt 的类别声明宏。

### 8.4 `debug(const char *, ...) const`

```cpp
void debug(const char *msg, ...) const;
```

使用 printf 风格格式字符串发出 debug 消息：

```cpp
logger.debug("cache entries: %d", count);
```

`msg` 是格式字符串，不是已经完成格式化的任意文本模板。参数类型必须匹配格式说明符。

### 8.5 `debug(const QLoggingCategory &, const char *, ...) const`

```cpp
void debug(const QLoggingCategory &cat,
           const char *msg, ...) const;
```

以指定类别和 printf 风格格式发出 debug 消息：

```cpp
logger.debug(storageLog,
             "cache entries: %d", count);
```

类别参数不是格式参数，必须位于格式字符串之前。

### 8.6 `debug(CategoryFunction, const char *, ...) const`

```cpp
void debug(CategoryFunction catFunc,
           const char *msg, ...) const;
```

通过类别函数获取类别后，以 printf 风格发出 debug 消息：

```cpp
logger.debug(storageCategory,
             "cache entries: %d", count);
```

注意函数指针的类型和格式字符串参数的顺序。

### 8.7 `info() const`

```cpp
QDebug info() const;
```

返回 info 等级的流：

```cpp
logger.info() << "service started";
```

适合记录正常运行状态。是否输出仍受 Qt 输出配置和消息处理器影响。

### 8.8 `info(const QLoggingCategory &) const`

```cpp
QDebug info(const QLoggingCategory &cat) const;
```

以类别对象发出 info 流：

```cpp
logger.info(storageLog) << "service started";
```

类别对象只提供分类信息；类别的启用和过滤不通过修改 logger 实例完成。

### 8.9 `info(CategoryFunction) const`

```cpp
QDebug info(CategoryFunction catFunc) const;
```

通过类别函数发出 info 流：

```cpp
logger.info(storageCategory) << "service started";
```

适合使用由 `Q_DECLARE_LOGGING_CATEGORY` 声明的类别。

### 8.10 `info(const char *, ...) const`

```cpp
void info(const char *msg, ...) const;
```

以 printf 风格发出 info 消息：

```cpp
logger.info("loaded %d records", recordCount);
```

格式参数必须与 C 可变参数调用约定匹配。

### 8.11 `info(const QLoggingCategory &, const char *, ...) const`

```cpp
void info(const QLoggingCategory &cat,
          const char *msg, ...) const;
```

以类别对象和 printf 风格发出 info 消息。

### 8.12 `info(CategoryFunction, const char *, ...) const`

```cpp
void info(CategoryFunction catFunc,
          const char *msg, ...) const;
```

以类别函数和 printf 风格发出 info 消息。

### 8.13 `warning() const`

```cpp
QDebug warning() const;
```

返回 warning 等级的流：

```cpp
logger.warning() << "using fallback configuration";
```

warning 通常表示可以继续运行但需要关注的状态。它不是异常抛出，也不会自动回滚业务操作。

### 8.14 `warning(const QLoggingCategory &) const`

```cpp
QDebug warning(const QLoggingCategory &cat) const;
```

以类别对象发出 warning 流。适合把配置、网络、存储等子系统的警告分开过滤。

### 8.15 `warning(CategoryFunction) const`

```cpp
QDebug warning(CategoryFunction catFunc) const;
```

以类别函数发出 warning 流。类别函数必须返回有效类别引用。

### 8.16 `warning(const char *, ...) const`

```cpp
void warning(const char *msg, ...) const;
```

使用 printf 风格格式输出 warning：

```cpp
logger.warning("retry %d of %d", attempt, maxAttempts);
```

不应把可控字符串直接作为 `msg`：

```cpp
// 不要这样：用户文本可能包含格式控制符
logger.warning(userText.constData());
```

应改用流式形式或固定格式：

```cpp
logger.warning("user text: %s",
               qUtf8Printable(userText));
```

### 8.17 `warning(const QLoggingCategory &, const char *, ...) const`

```cpp
void warning(const QLoggingCategory &cat,
             const char *msg, ...) const;
```

以类别对象和 printf 风格输出 warning。

### 8.18 `warning(CategoryFunction, const char *, ...) const`

```cpp
void warning(CategoryFunction catFunc,
             const char *msg, ...) const;
```

以类别函数和 printf 风格输出 warning。

### 8.19 `critical() const`

```cpp
QDebug critical() const;
```

返回 critical 等级的流：

```cpp
logger.critical() << "database unavailable";
```

critical 表示严重问题，但不等同于 `fatal()`。默认情况下它不必然终止程序；是否把 critical 配置为终止还取决于应用和 Qt 的相关设置。

### 8.20 `critical(const QLoggingCategory &) const`

```cpp
QDebug critical(const QLoggingCategory &cat) const;
```

以类别对象发出 critical 流。

### 8.21 `critical(CategoryFunction) const`

```cpp
QDebug critical(CategoryFunction catFunc) const;
```

以类别函数发出 critical 流。

### 8.22 `critical(const char *, ...) const`

```cpp
void critical(const char *msg, ...) const;
```

使用 printf 风格格式输出 critical：

```cpp
logger.critical("database error code: %d", errorCode);
```

格式字符串和可变参数仍需严格匹配。

### 8.23 `critical(const QLoggingCategory &, const char *, ...) const`

```cpp
void critical(const QLoggingCategory &cat,
              const char *msg, ...) const;
```

以类别对象和 printf 风格输出 critical。

### 8.24 `critical(CategoryFunction, const char *, ...) const`

```cpp
void critical(CategoryFunction catFunc,
              const char *msg, ...) const;
```

以类别函数和 printf 风格输出 critical。

### 8.25 `fatal() const`

```cpp
QDebug fatal() const;
```

返回 fatal 等级的流：

```cpp
logger.fatal() << "cannot continue";
```

该调用表示不可恢复错误。消息处理之后程序会终止，不能把返回的 `QDebug` 当作普通可继续使用的流，也不能在其后依赖正常控制流。

Qt 6.5 起，Qt 文档将流式 `fatal` 入口作为可用 API；项目支持更低版本时应核对最低 Qt 版本。

### 8.26 `fatal(const QLoggingCategory &) const`

```cpp
QDebug fatal(const QLoggingCategory &cat) const;
```

以类别对象发出 fatal 流并终止。类别信息仍会随消息上下文传递，但 fatal 的终止语义不会因为类别关闭而变成可恢复流程。

### 8.27 `fatal(CategoryFunction) const`

```cpp
QDebug fatal(CategoryFunction catFunc) const;
```

以类别函数发出 fatal 流并终止。类别函数应返回有效的类别引用。

### 8.28 `fatal(const char *, ...) const`

```cpp
void fatal(const char *msg, ...) const noexcept;
```

以 printf 风格发出 fatal 消息并终止：

```cpp
logger.fatal("unrecoverable error: %d", code);
```

该函数标记为不返回。不要在调用后依赖资源清理、事务提交或普通错误恢复路径；需要可恢复报告时使用 warning 或 critical。

### 8.29 `fatal(const QLoggingCategory &, const char *, ...) const`

```cpp
void fatal(const QLoggingCategory &cat,
           const char *msg, ...) const noexcept;
```

以类别对象和 printf 风格发出 fatal 消息并终止。Qt 6.5 起的类别重载需要项目最低版本满足要求。

### 8.30 `fatal(CategoryFunction, const char *, ...) const`

```cpp
void fatal(CategoryFunction catFunc,
           const char *msg, ...) const noexcept;
```

以类别函数和 printf 风格发出 fatal 消息并终止。它同样不返回，且格式参数必须有效。

### 8.31 `noDebug(...) const`

```cpp
QNoDebug noDebug(...) const noexcept;
```

返回一个禁用输出对象，主要供 Qt 的输出禁用宏使用。普通业务代码不应把它当成一种日志等级；它的意义是“在编译配置或宏展开中丢弃调试输出”。

在 Qt 6.11.1 头文件中，旧的无参数 `noDebug()` 入口已受移除版本条件控制；代码应以当前 Qt 版本实际可见声明为准，不要依赖被移除的旧重载。

## 9. 类别、过滤和宏的协作

### 9.1 `QMessageLogger` 负责发消息，`QLoggingCategory` 负责开关

```cpp
Q_LOGGING_CATEGORY(networkLog, "app.network")

if (networkLog().isDebugEnabled())
    qCDebug(networkLog) << "packet:" << packet;
```

职责分工是：

- `QMessageLogger`：附带来源并选择等级；
- `QLoggingCategory`：提供类别名称和等级启用状态；
- `qCDebug` 等宏：在表达式前进行类别控制；
- 消息处理器：最终接收、过滤、格式化和写出。

### 9.2 直接 logger 调用不等于类别宏

下面两者都能发类别日志：

```cpp
logger.debug(networkLog) << expensivePacketInfo();
qCDebug(networkLog) << expensivePacketInfo();
```

但类别宏专门设计了条件控制，可以在类别关闭时跳过后续流式表达式。若性能或副作用重要，优先使用 `qCDebug`、`qCInfo`、`qCWarning`、`qCCritical` 和 `qCFatal`。

### 9.3 消息处理器是全局接收点

```cpp
void handler(QtMsgType type,
             const QMessageLogContext &context,
             const QString &message);

qInstallMessageHandler(handler);
```

logger 不决定最终输出位置。自定义处理器中应考虑：

- 多线程写入；
- 上下文指针的及时复制；
- 不在处理器中再次触发日志；
- 敏感信息脱敏；
- fatal 消息的终止流程。

## 10. 常见错误与排查顺序

### 10.1 把 printf 风格格式串当普通文本

**症状：** 用户输入中的 `%` 导致异常输出或崩溃。

**原因：** 第一个参数被解释为 format string。

**修复：** 使用流式输出，或使用固定格式把用户文本作为参数传入。

### 10.2 把 `QString` 直接传给 `%s`

**症状：** 编译警告、乱码或未定义行为。

**原因：** `%s` 需要 `const char *`，而 `QString` 不是 C 字符串。

**修复：** 使用 `qUtf8Printable()`、`toLocal8Bit().constData()` 配合正确生命周期，或改为流式形式。

### 10.3 误以为日志被过滤就不会求值

**症状：** 类别关闭时仍执行昂贵计算或产生副作用。

**原因：** 直接调用 logger 的参数和流表达式可能在过滤结果确定前就被求值。

**修复：** 使用类别宏，或显式调用 `isDebugEnabled()` 等检查后再计算。

### 10.4 把 `critical()` 和 `fatal()` 混为一谈

**症状：** 可恢复错误导致程序直接终止，或严重错误没有按策略终止。

**原因：** `critical` 是严重日志等级，`fatal` 明确表示终止。

**修复：** 根据控制流需求选择等级；不要用 fatal 代替普通错误返回。

### 10.5 保存带临时字符串指针的 logger

**症状：** 异步日志中出现悬空指针。

**原因：** logger 和上下文只保存 `const char *`，不拥有底层字符串。

**修复：** 立即发出消息，或在异步任务中保存拥有数据的日志记录。

### 10.6 把日志类别当作安全字段

**症状：** 类别字符串被直接拼接进文件路径、SQL 或权限逻辑。

**原因：** 类别只是诊断和过滤名称，不是经过验证的安全标识。

**修复：** 对外部输入做独立校验，不把日志上下文当权限数据。

### 10.7 以为日志一定保留

**症状：** 某些 debug 或 info 消息在发布构建、规则变化或平台配置下看不到。

**原因：** Qt 输出宏、类别规则、消息处理器和构建选项都可能丢弃或重定向消息。

**修复：** 对必须持久化的审计事件使用独立的审计或事件记录路径，不把普通调试日志当可靠存档。

## 11. 推荐设计模板

### 11.1 使用 Qt 宏自动捕获源码上下文

```cpp
qInfo() << "server listening on" << port;
qWarning("configuration file not found: %s",
         qUtf8Printable(path));
```

宏比手写 `__FILE__`、`__LINE__`、`Q_FUNC_INFO` 更不容易漏传上下文。

### 11.2 转发外部来源时保证字符串生命周期

```cpp
void logError(const QUrl &url, int line,
              const QString &description)
{
    const QByteArray file = url.toEncoded();
    QMessageLogger(file.constData(), line, Q_FUNC_INFO)
        .warning() << description;
}
```

`file` 在完整表达式结束前仍然存在，因此 logger 使用的指针有效。若要异步处理，应在处理器中再次复制。

### 11.3 类别日志优先使用类别宏

```cpp
Q_LOGGING_CATEGORY(parserLog, "app.parser")

void parse(const QByteArray &data)
{
    qCDebug(parserLog) << "input size:" << data.size();
}
```

这样类别过滤和参数求值控制都更接近 Qt 预期的使用路径。

### 11.4 需要结构化字段时避免 format string

```cpp
qCWarning(parserLog)
    << "parse failed"
    << "offset:" << offset
    << "token:" << token;
```

流式写法可以减少格式说明符错配，也更容易在以后迁移到结构化消息处理器。

## API 速查表
### 12.1 类型和构造

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `CategoryFunction` | 类别工厂函数指针类型 | 签名必须返回 `const QLoggingCategory &` |
| `QMessageLogger()` | 创建默认上下文 logger | 不自动捕获当前调用点 |
| `QMessageLogger(file, line, function)` | 创建默认类别 logger | 字符串不复制；默认类别为 `default` |
| `QMessageLogger(file, line, function, category)` | 创建显式类别 logger | 类别指针必须在使用期间有效 |

### 12.2 Debug 和 Info

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `debug() const` | 返回 debug 流 | 直接调用不保证昂贵表达式跳过 |
| `debug(const QLoggingCategory &) const` | 按类别返回 debug 流 | 类别宏更适合惰性求值 |
| `debug(CategoryFunction) const` | 按类别函数返回 debug 流 | 使用 Qt 类别声明生成的函数 |
| `debug(const char *, ...) const` | printf 风格 debug | 格式说明符必须匹配 |
| `debug(const QLoggingCategory &, const char *, ...) const` | 类别 + printf debug | 类别参数在格式串之前 |
| `debug(CategoryFunction, const char *, ...) const` | 类别函数 + printf debug | 注意函数指针签名 |
| `info() const` | 返回 info 流 | 记录正常运行信息 |
| `info(const QLoggingCategory &) const` | 按类别返回 info 流 | 类别只提供分类，不负责存储 |
| `info(CategoryFunction) const` | 按类别函数返回 info 流 | 类别函数须返回有效引用 |
| `info(const char *, ...) const` | printf 风格 info | 不要让用户文本成为格式串 |
| `info(const QLoggingCategory &, const char *, ...) const` | 类别 + printf info | 类型和格式串要匹配 |
| `info(CategoryFunction, const char *, ...) const` | 类别函数 + printf info | Qt 6 Core 类别接口 |

### 12.3 Warning 和 Critical

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `warning() const` | 返回 warning 流 | 不等于抛异常 |
| `warning(const QLoggingCategory &) const` | 按类别返回 warning 流 | 适合子系统分类 |
| `warning(CategoryFunction) const` | 按类别函数返回 warning 流 | 类别函数生命周期由程序保证 |
| `warning(const char *, ...) const` | printf 风格 warning | 固定格式串；避免用户文本注入 |
| `warning(const QLoggingCategory &, const char *, ...) const` | 类别 + printf warning | 类别不是可变参数 |
| `warning(CategoryFunction, const char *, ...) const` | 类别函数 + printf warning | 格式参数必须匹配 |
| `critical() const` | 返回 critical 流 | 严重但默认不等于终止 |
| `critical(const QLoggingCategory &) const` | 按类别返回 critical 流 | 受类别和处理器配置影响 |
| `critical(CategoryFunction) const` | 按类别函数返回 critical 流 | 使用稳定类别函数 |
| `critical(const char *, ...) const` | printf 风格 critical | 不要依赖它执行恢复逻辑 |
| `critical(const QLoggingCategory &, const char *, ...) const` | 类别 + printf critical | 仍是可变参数格式接口 |
| `critical(CategoryFunction, const char *, ...) const` | 类别函数 + printf critical | 类别函数签名必须正确 |

### 12.4 Fatal 和禁用输出

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `fatal() const` | 返回 fatal 流并终止 | Qt 6.5 起流式入口；不可恢复 |
| `fatal(const QLoggingCategory &) const` | 类别 + fatal 流并终止 | 类别不会取消终止语义 |
| `fatal(CategoryFunction) const` | 类别函数 + fatal 流并终止 | Qt 6.5 起类别流式入口 |
| `fatal(const char *, ...) const` | printf 风格 fatal 并终止 | `noexcept`、不返回 |
| `fatal(const QLoggingCategory &, const char *, ...) const` | 类别 + printf fatal | Qt 6.5 起类别重载 |
| `fatal(CategoryFunction, const char *, ...) const` | 类别函数 + printf fatal | `noexcept`、不返回 |
| `noDebug(...) const` | 返回禁用输出对象 | 主要供 Qt 宏和构建配置使用 |

## 13. 一句话总结

`QMessageLogger` 是带源码上下文的 Qt 日志调用器：用流式 API 输出 Qt 类型，用 printf 重载兼容格式字符串，用类别重载绑定 `QLoggingCategory`，用 `qDebug()`/`qCWarning()` 等宏获得更合适的上下文和惰性过滤；`fatal()` 表示终止，不是普通错误报告。
