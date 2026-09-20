# Qt QMessageLogContext 日志上下文笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMessageLogContext>`  
> 所属模块：`Qt6::Core`  
> 类型性质：传给 Qt 消息处理器的轻量上下文结构  
> 相关类型：`QtMsgType`、`QMessageLogger`、`QLoggingCategory`、`QtMessageHandler`

## 1. 它解决什么问题

`QMessageLogContext` 描述一条 Qt 日志消息的来源上下文。它把“消息内容”之外的定位信息交给消息处理器：

- 源文件名；
- 源代码行号；
- 函数签名；
- 日志类别；
- 上下文结构版本。

它本身不负责输出日志、不负责格式化文本，也不负责决定某一日志级别是否启用。它更像是 Qt 在调用自定义消息处理器时附带的一张“来源标签”：

```text
QtMsgType + QMessageLogContext + QString message
                    |
                    +-- file / line / function / category
```

典型接收接口是：

```cpp
void messageHandler(QtMsgType type,
                    const QMessageLogContext &context,
                    const QString &message);
```

### 1.1 它不解决什么问题

`QMessageLogContext` 不是：

- 日志记录器，记录操作使用 `QMessageLogger` 或 `qDebug()` 等 API；
- 日志类别控制器，类别启用状态使用 `QLoggingCategory`；
- 日志格式化器，格式化可使用 `qFormatLogMessage()` 或自定义逻辑；
- 拥有字符串存储的日志对象，`file`、`function`、`category` 都是非拥有指针；
- `QtMsgType`，日志级别由消息处理器收到的第一个参数提供。

## 2. 实际使用场景

### 2.1 自定义消息处理器输出来源位置

```cpp
void messageHandler(QtMsgType type,
                    const QMessageLogContext &context,
                    const QString &message)
{
    const char *file = context.file ? context.file : "<unknown>";
    const char *function =
        context.function ? context.function : "<unknown>";
    const char *category =
        context.category ? context.category : "default";

    writeLog(type, category, file, context.line,
             function, message);
}
```

消息处理器收到的是 `const QMessageLogContext &`。上下文通常只需要在当前回调中读取；如果异步写日志，应复制为自己的拥有数据，而不是把这些 `const char *` 指针直接排队。

### 2.2 使用 Qt 的默认格式化规则

```cpp
void messageHandler(QtMsgType type,
                    const QMessageLogContext &context,
                    const QString &message)
{
    const QString line =
        qFormatLogMessage(type, context, message);
    writeText(line);
}
```

`qFormatLogMessage()` 会根据当前消息模式使用上下文。若要完全自定义 JSON、结构化日志或脱敏策略，则应显式读取字段并自行处理。

### 2.3 根据类别写入不同目标

```cpp
const QByteArray category =
    context.category ? QByteArray(context.category)
                     : QByteArrayLiteral("default");

if (category == "network")
    writeNetworkLog(message);
else
    writeGeneralLog(message);
```

类别来源于 `QLoggingCategory` 或 `QMessageLogger` 的 category 参数。它不是安全边界，不能直接当作未经验证的文件名、数据库表名或权限标识。

### 2.4 测试消息处理器

自定义测试处理器可以检查某条消息是否包含预期的文件、行号或类别：

```cpp
void testHandler(QtMsgType,
                 const QMessageLogContext &context,
                 const QString &message)
{
    Q_ASSERT(context.version == QMessageLogContext::CurrentVersion);
    Q_ASSERT(context.category != nullptr);
    record(message, context.file, context.line);
}
```

测试代码仍应处理字段为空的情况，因为手工构造的上下文和关闭源码上下文宏时可能得到 `nullptr` 或 0。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QMessageLogContext>
#include <QLoggingCategory>
#include <QDebug>
```

注册全局消息处理器通常还需要 `QCoreApplication` 或其他 Qt 应用初始化代码，但 `QMessageLogContext` 本身是 `Qt6::Core` 的简单上下文类型。

## 4. 日志调用链和上下文来源

### 4.1 `qDebug()` 等宏如何产生上下文

Qt 的日志宏会把编译器提供的源码信息传给 `QMessageLogger`：

```cpp
qDebug() << "connected";
qWarning("retry failed");
```

在默认配置下，`QT_MESSAGELOG_FILE`、`QT_MESSAGELOG_LINE` 和 `QT_MESSAGELOG_FUNC` 分别来自 `__FILE__`、`__LINE__` 和 `Q_FUNC_INFO`。如果构建配置关闭了消息上下文，宏会把对应字段设置为 `nullptr` 或 0。

因此，`context.file == nullptr` 或 `context.line == 0` 不一定表示 Qt 出错，也可能表示程序构建时有意关闭了源码上下文。

### 4.2 类别来自日志类别系统

```cpp
Q_LOGGING_CATEGORY(networkLog, "app.network")
qCDebug(networkLog) << "connected";
```

这类消息的 `context.category` 通常是类别名。类别是否启用由 `QLoggingCategory` 和规则系统决定；上下文只携带名称，不携带类别配置对象。

### 4.3 消息级别不在 `context` 中

```cpp
void handler(QtMsgType type,
             const QMessageLogContext &context,
             const QString &message)
{
    switch (type) {
    case QtDebugMsg:
        break;
    case QtInfoMsg:
        break;
    case QtWarningMsg:
        break;
    case QtCriticalMsg:
        break;
    case QtFatalMsg:
        break;
    }
}
```

不要从 `context.category` 或文件名推断 `debug`、`warning` 等级。真正的等级是消息处理器的 `QtMsgType` 参数。

## 5. 数据所有权、生命周期和线程边界

### 5.1 四个字符串字段都是非拥有指针

类的公开字段类型是：

```cpp
const char *file;
const char *function;
const char *category;
```

`QMessageLogContext` 不分配、不释放，也不复制这些字符串。不要把它当作 `QString` 或 `QByteArray` 来管理。

在当前消息处理器调用期间读取通常是安全的；如果要保存到异步任务、队列或跨线程结构中，应立即复制：

```cpp
const QByteArray file =
    context.file ? QByteArray(context.file) : QByteArray();
const QByteArray function =
    context.function ? QByteArray(context.function) : QByteArray();
const QByteArray category =
    context.category ? QByteArray(context.category) : QByteArray();
```

具体的 `QByteArray`、`QString` 或结构化日志对象由异步系统拥有。

### 5.2 消息处理器回调不应阻塞或递归记录

`QMessageLogContext` 本身没有线程同步机制。全局消息处理器可能在多个线程收到消息，处理器内部应自行保证写入目标的线程安全，并避免在处理器中再次调用会触发日志的代码，否则可能产生递归。

如果处理器把上下文放入异步队列，除了复制字符串，还要复制 `message` 和 `QtMsgType`。只保存 `const QMessageLogContext *` 指针是不安全的。

### 5.3 构造参数的字符串也必须由调用方保证有效

手工创建上下文时：

```cpp
constexpr QMessageLogContext context(
    "example.cpp", 42, "main()", "app.startup");
```

字符串字面量的生命周期足够长。如果传入临时 `QByteArray::constData()`，必须保证底层数组在所有读取期间仍然存在；不要把短生命周期的指针放入需要长期保存的上下文中。

## 6. 版本字段和默认值

### 6.1 `CurrentVersion`

```cpp
static constexpr int CurrentVersion = 2;
```

它表示 `QMessageLogContext` 结构的当前版本，用于让接收方知道当前上下文布局和字段契约。它不是 Qt 版本号，也不是日志格式版本，更不是消息等级。

代码可以用它记录或断言当前头文件的预期版本：

```cpp
static_assert(QMessageLogContext::CurrentVersion == 2);
```

对于面向多个 Qt 版本的库，应避免把未来版本的字段布局假定写死；读取上下文时至少把版本当作兼容性信息保留下来。

### 6.2 默认构造值

默认构造后，头文件中的字段初始化为：

| 字段 | 默认值 | 含义 |
| --- | --- | --- |
| `version` | `CurrentVersion` | 当前上下文版本 |
| `line` | `0` | 没有有效源码行号或未提供 |
| `file` | `nullptr` | 没有文件名 |
| `function` | `nullptr` | 没有函数信息 |
| `category` | `nullptr` | 没有类别名 |

默认构造的上下文不是一条完整日志，也不会自动填充调用点信息。

## 7. 逐项 API 和公开字段

### 7.1 `QMessageLogContext()`

```cpp
constexpr QMessageLogContext() noexcept = default;
```

创建一个带默认字段值的上下文。适合：

- 作为需要可构造上下文的测试对象；
- 先创建再逐项填充的内部适配代码；
- 需要传递“没有来源信息”的上下文。

它不会自动获得当前调用点的 `__FILE__`、`__LINE__` 或 `Q_FUNC_INFO`。

### 7.2 `QMessageLogContext(const char *, int, const char *, const char *)`

```cpp
constexpr QMessageLogContext(
    const char *fileName,
    int lineNumber,
    const char *functionName,
    const char *categoryName) noexcept;
```

按文件、行号、函数和类别初始化上下文：

```cpp
constexpr QMessageLogContext context(
    "worker.cpp", 80, "Worker::run()", "app.worker");
```

构造函数只保存指针和整数，不复制字符串，也不验证：

- 指针是否为空；
- 行号是否为正；
- 类别名是否符合某种命名规则；
- 函数名是否是编译器生成的格式。

传入的字符串必须由调用方保证生命周期和内容有效性。

### 7.3 `CurrentVersion`

```cpp
static constexpr int QMessageLogContext::CurrentVersion = 2;
```

提供当前上下文结构版本。它适合用于调试、兼容性分支和结构化日志字段记录。

不要把它写成日志输出中的“应用版本”；两者是不同概念。

### 7.4 `version`

```cpp
int version = CurrentVersion;
```

表示当前实例的上下文版本。正常情况下由构造和默认初始化得到 `CurrentVersion`，但它是公开字段，代码可以修改。除非实现协议适配，否则不应随意改成另一个数字，因为接收方会据此理解字段契约。

### 7.5 `line`

```cpp
int line = 0;
```

记录产生日志的源代码行号。它来自 `__LINE__` 时通常是正数；关闭消息上下文或手工构造无来源上下文时可以是 0。

行号不是消息在文件中的字节偏移，也不是日志序号。不要仅凭 `line == 0` 判断日志无效。

### 7.6 `file`

```cpp
const char *file = nullptr;
```

指向产生日志的源文件名。它通常来自 `__FILE__`，具体是完整路径、相对路径还是编译器提供的其他形式取决于构建工具链和编译选项。

使用时先检查空指针，并把它当作诊断信息，不要依赖路径格式做跨平台逻辑：

```cpp
const QString fileName =
    context.file ? QString::fromLocal8Bit(context.file)
                 : QString();
```

### 7.7 `function`

```cpp
const char *function = nullptr;
```

指向编译器或 Qt 宏提供的函数信息，通常来自 `Q_FUNC_INFO`。不同编译器的格式可能不同，包含类名、参数列表或修饰信息。

它适合显示和诊断，不适合当作稳定的函数 ID 或解析协议。

### 7.8 `category`

```cpp
const char *category = nullptr;
```

指向日志类别名。通过 `QLoggingCategory` 生成的类别日志通常带有类别名；默认日志或手工构造上下文可能使用 `"default"` 或空指针，具体取决于创建路径。

类别名称可用于路由和过滤，但仍应将其作为不透明诊断字符串处理。

## 8. 与相关类型配合

### 8.1 `QMessageLogger` 负责生成上下文

```cpp
QMessageLogger logger(
    QT_MESSAGELOG_FILE,
    QT_MESSAGELOG_LINE,
    QT_MESSAGELOG_FUNC,
    "app.worker");
logger.warning("worker retry failed");
```

`QMessageLogger` 保存 `QMessageLogContext`，再通过 `debug()`、`warning()` 等成员将消息交给 Qt 日志系统。通常应用代码不需要直接手工创建上下文。

### 8.2 `QLoggingCategory` 负责类别开关

```cpp
Q_LOGGING_CATEGORY(workerLog, "app.worker")
qCWarning(workerLog) << "retry failed";
```

这里：

- `QLoggingCategory` 决定某个等级是否启用；
- `QMessageLogger` 组织消息调用；
- `QMessageLogContext` 携带类别和源码来源；
- `QtMessageHandler` 接收最终消息。

不要用修改 `context.category` 的方式开启或关闭类别。类别过滤应使用规则或 `QLoggingCategory` API。

### 8.3 `qInstallMessageHandler` 接收上下文

```cpp
static void handler(QtMsgType type,
                    const QMessageLogContext &context,
                    const QString &message)
{
    writeRecord(type, context, message);
}

int main(int argc, char **argv)
{
    QCoreApplication app(argc, argv);
    qInstallMessageHandler(handler);
    return app.exec();
}
```

安装消息处理器后，处理器负责决定写文件、写控制台、写系统日志或转发到结构化日志系统。Qt 不会替你解决异步队列、文件轮转和敏感信息脱敏。

### 8.4 `qFormatLogMessage` 使用上下文生成文本

```cpp
const QString formatted =
    qFormatLogMessage(type, context, message);
```

它适合保留 Qt 的消息模式行为。若自定义格式，应明确处理空字段、行号 0、类别名和函数名中的特殊字符。

## 9. 常见错误与排查顺序

### 9.1 把 `QMessageLogContext` 当成拥有字符串的对象

**症状：** 异步写日志时出现乱码、崩溃或不同消息共享同一内容。

**原因：** `file`、`function` 和 `category` 都是非拥有指针，不能脱离原始上下文生命周期使用。

**修复：** 在消息处理器回调中复制成 `QByteArray`、`QString` 或项目自己的拥有字段。

### 9.2 没有检查空指针

**症状：** 使用 `%s` 或字符串构造时访问空指针。

**原因：** 关闭源码上下文、默认构造或手工构造都可能让字段为 `nullptr`。

**修复：** 为每个指针字段提供缺省文本或空值分支。

### 9.3 把 `line == 0` 当成日志无效

**症状：** 构建配置变化后日志被错误丢弃。

**原因：** `QT_NO_MESSAGELOGCONTEXT` 或相关编译选项可能关闭文件、函数和行号信息。

**修复：** 把行号 0 当作“未知来源”，仍保留消息本身和等级。

### 9.4 从 `context` 读取日志等级

**症状：** warning 被当成 debug，或类别名被误当作等级。

**原因：** 等级是消息处理器的 `QtMsgType` 参数，不在 `QMessageLogContext` 字段中。

**修复：** 同时处理 `type` 和 `context`。

### 9.5 用函数名做稳定业务标识

**症状：** 更换编译器或构建配置后日志聚合规则失效。

**原因：** `Q_FUNC_INFO` 的内容和格式不是跨编译器稳定协议。

**修复：** 使用显式事件名、类别名或结构化字段做聚合键。

### 9.6 在消息处理器中再次记录日志

**症状：** 无限递归、堆栈耗尽或日志量异常增长。

**原因：** 处理器内部调用 `qWarning()` 等 API 会再次触发同一个处理器。

**修复：** 处理器内部使用无日志的底层写入路径，并设置必要的递归保护。

### 9.7 直接修改上下文试图改变 Qt 日志行为

**症状：** 修改了 `category` 或 `line`，但过滤和输出行为没有按预期改变。

**原因：** 上下文主要是交给处理器的来源数据，不是日志分类控制器。

**修复：** 用 `QLoggingCategory`、过滤规则、消息模式和自定义处理器控制行为。

## 10. 推荐设计模板

### 10.1 立即提取为拥有数据

```cpp
struct LogContextCopy
{
    int version = 0;
    int line = 0;
    QByteArray file;
    QByteArray function;
    QByteArray category;
};

LogContextCopy copyContext(const QMessageLogContext &context)
{
    return {
        context.version,
        context.line,
        context.file ? QByteArray(context.file) : QByteArray(),
        context.function ? QByteArray(context.function) : QByteArray(),
        context.category ? QByteArray(context.category) : QByteArray()
    };
}
```

这样异步系统不依赖 Qt 内部上下文指针的生命周期。

### 10.2 统一处理缺失来源

```cpp
const char *safeFile(const QMessageLogContext &context)
{
    return context.file ? context.file : "<unknown-file>";
}

const char *safeCategory(const QMessageLogContext &context)
{
    return context.category ? context.category : "default";
}
```

统一缺省策略比在各个日志输出分支中重复空指针判断更容易维护。

### 10.3 结构化记录同时保存等级和上下文

```cpp
void writeRecord(QtMsgType type,
                 const QMessageLogContext &context,
                 const QString &message)
{
    const auto copied = copyContext(context);
    enqueue(type, copied.version, copied.category,
            copied.file, copied.line, copied.function,
            message);
}
```

不要只保存 `message`；来源信息对于定位问题和按类别查询同样重要。

## API 速查表
### 11.1 构造和版本

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMessageLogContext()` | 创建默认上下文 | 不自动填充当前文件、行号和函数 |
| `QMessageLogContext(const char *, int, const char *, const char *)` | 指定来源字段创建上下文 | 只保存指针，不复制字符串 |
| `CurrentVersion` | 当前上下文结构版本 | 是结构版本，不是日志等级或 Qt 版本 |

### 11.2 公开字段

| 字段 | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `version` | 实例的上下文版本 | 默认是 `CurrentVersion`，不要随意伪造 |
| `line` | 源代码行号 | 可能是 0，0 表示未知而非消息无效 |
| `file` | 源文件名指针 | 非拥有、可为 `nullptr`、格式受工具链影响 |
| `function` | 函数信息指针 | 非拥有、可为 `nullptr`、不适合作稳定 ID |
| `category` | 日志类别名指针 | 非拥有、可为 `nullptr`，不等于日志等级 |

### 11.3 协作 API

| API 或类型 | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QtMessageHandler` | 接收 `QtMsgType`、上下文和消息 | 回调中读取上下文，异步化前复制字段 |
| `qInstallMessageHandler()` | 安装全局消息处理器 | 处理器要考虑线程安全和递归日志 |
| `qFormatLogMessage()` | 按 Qt 消息模式格式化 | 仍需考虑空字段和模式配置 |
| `QMessageLogger` | 创建并发出带上下文的日志 | 通常由 `qDebug()` 等宏间接使用 |
| `QLoggingCategory` | 控制类别和等级开关 | 不通过修改 context 来过滤日志 |

## 12. 一句话总结

`QMessageLogContext` 是 Qt 日志处理器收到的来源上下文：它只携带版本、行号、文件、函数和类别指针，不拥有字符串，也不决定日志等级或过滤规则；在当前回调中读取，跨线程或异步保存前复制，遇到空字段和关闭源码上下文的构建配置要按“来源未知”处理。
