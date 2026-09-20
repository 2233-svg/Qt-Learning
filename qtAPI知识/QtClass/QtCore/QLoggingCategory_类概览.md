# Qt QLoggingCategory 日志分类与运行时过滤深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLoggingCategory>`  
> 所属模块：`Qt6::Core`  
> 类型性质：进程级日志分类配置对象  
> 相关类型：`QDebug`、`QMessageLogger`、`QtMsgType`、`QString`

## 1. 它解决什么问题

`QLoggingCategory` 解决的是“日志消息如何按模块、子系统和严重级别被选择性打开”的问题。

普通的 `qDebug()` 只能表达“这是一条 Debug 消息”。当程序变大以后，开发者还需要知道：

- 这条消息来自网络、数据库、界面还是文件系统；
- 部署到生产环境时，哪些类别应该保留；
- 调试某个子系统时，是否可以只打开它而不打开全局 Debug；
- 日志参数很昂贵时，类别关闭后能否连参数计算都跳过；
- 多个动态库是否可以声明同一套稳定的类别名；
- 规则能否通过环境变量或配置文件在不重新编译的情况下改变。

`QLoggingCategory` 把这些信息分成两层：

1. **类别**：例如 `app.network`、`app.storage.cache`；
2. **消息类型**：`debug`、`info`、`warning`、`critical` 和 `fatal`。

输出时使用 `qCDebug()`、`qCInfo()`、`qCWarning()`、`qCCritical()` 或 `qCFatal()` 等分类宏。类别的开关可以由默认级别、过滤规则或自定义全局过滤器决定。

它不是日志文件写入器，也不是日志轮转器：

- `QLoggingCategory` 决定消息是否启用；
- `qCDebug()` 等宏把消息交给 Qt 的消息处理系统；
- `qInstallMessageHandler()`、`QMessageLogger` 和消息模式负责后续输出与格式化；
- 文件、控制台、网络日志和轮转需要应用自己配置消息处理器或使用更高层日志系统。

## 2. 实际使用场景

### 2.1 给模块定义稳定的日志类别

头文件中声明类别：

```cpp
// loggingcategories.h
#pragma once

#include <QLoggingCategory>

Q_DECLARE_LOGGING_CATEGORY(lcNetwork)
Q_DECLARE_LOGGING_CATEGORY(lcStorage)
```

某一个源文件中定义类别：

```cpp
// loggingcategories.cpp
#include "loggingcategories.h"

Q_LOGGING_CATEGORY(lcNetwork, "app.network")
Q_LOGGING_CATEGORY(lcStorage, "app.storage", QtInfoMsg)
```

业务代码使用类别宏：

```cpp
#include "loggingcategories.h"

void sendPacket(const QByteArray &packet)
{
    qCDebug(lcNetwork) << "sending packet, bytes:" << packet.size();
}
```

这样部署者可以单独控制 `app.network`，而不必打开整个应用的所有 Debug 日志。

### 2.2 用规则临时打开某一个子系统

命令行启动时可以设置环境变量：

```text
QT_LOGGING_RULES=app.network.debug=true;app.storage.debug=false
```

也可以在程序启动阶段设置：

```cpp
QLoggingCategory::setFilterRules(
    QStringLiteral("app.network.debug=true\n"
                   "app.storage.debug=false"));
```

规则适合诊断“某一模块只在特定机器或特定运行阶段出问题”的情况。类别名应稳定、可读，并在多个版本中尽量保持兼容。

### 2.3 禁用类别时跳过昂贵参数计算

```cpp
qCDebug(lcNetwork) << "state:" << buildLargeNetworkSnapshot();
```

当 `app.network` 的 Debug 级别关闭时，`qCDebug()` 的流表达式不会继续执行，`buildLargeNetworkSnapshot()` 通常也不会被调用。这既减少日志输出，也避免为不会输出的消息分配大量临时对象。

不要把必须执行的业务副作用放进分类日志表达式：

```cpp
// 错误：类别关闭时 incrementCounter() 可能不会执行。
qCDebug(lcNetwork) << incrementCounter();
```

分类日志表达式应只做诊断数据读取或格式化。

### 2.4 为插件或动态库导出类别

公共头文件中：

```cpp
#include <QLoggingCategory>

Q_DECLARE_EXPORTED_LOGGING_CATEGORY(lcImagePlugin, IMAGE_PLUGIN_EXPORT)
```

某个实现文件中仍然只定义一次：

```cpp
Q_LOGGING_CATEGORY(lcImagePlugin, "plugin.image")
```

Qt 6.5 起的导出声明宏用于处理动态库符号可见性。它不会改变类别规则，也不会替代在一个实现文件中提供唯一的定义。

### 2.5 在单个源文件内使用静态类别

Qt 6.9 起可以使用：

```cpp
Q_STATIC_LOGGING_CATEGORY(lcParser, "app.parser")
```

这适合实现文件私有的类别，不需要把类别符号暴露给其他翻译单元。类别名仍会进入 Qt 的全局分类规则，静态只影响 C++ 符号和定义范围。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QLoggingCategory>
#include <QDebug>
#include <QString>
```

只使用类别声明、定义和分类宏时，`QLoggingCategory` 头文件是核心依赖；如果消息使用流式输出，项目也应让 `QDebug` 的包含关系清晰。

## 4. 最小使用流程

一套可维护的分类日志流程通常是：

1. 为模块选择稳定的 ASCII 类别名；
2. 在头文件用 `Q_DECLARE_LOGGING_CATEGORY()` 声明；
3. 在一个源文件用 `Q_LOGGING_CATEGORY()` 定义；
4. 在业务代码中用 `qCDebug()` 等宏输出；
5. 用 `isDebugEnabled()` 等查询避免更复杂的手工准备；
6. 用 `setFilterRules()`、环境变量或配置文件调整规则；
7. 只有确实需要全局决策时才安装 `CategoryFilter`。

```cpp
#include <QLoggingCategory>
#include <QDebug>

Q_LOGGING_CATEGORY(lcExample, "app.example")

void runTask()
{
    if (lcExample().isDebugEnabled()) {
        qCDebug(lcExample) << "task started";
    }

    qCInfo(lcExample) << "task is running";
}
```

`Q_LOGGING_CATEGORY` 生成的类别入口可以通过 `lcExample` 传给分类宏，也可以通过 `lcExample()` 得到类别引用并查询状态。

## 5. 类别、严重级别和规则

### 5.1 类别名是规则匹配的主键

类别名通常使用点分隔的层级：

```text
app
app.network
app.network.tls
app.storage
app.storage.cache
```

点号本身不是 QObject 对象树，也不会自动继承开关。`app.network` 和 `app.network.tls` 是否同时启用，取决于规则匹配和规则顺序。

建议：

- 使用应用或库的稳定前缀；
- 在类别名中表达模块边界，而不是临时函数名；
- 避免把用户数据、文件路径或随机值拼进类别名；
- 类别名尽量使用 ASCII，便于环境变量、配置文件和命令行传递；
- 不要轻易重命名已经被部署脚本使用的类别。

### 5.2 `enableForLevel` 是初始级别，不是最终规则

构造函数的第二个参数决定该类别创建时的初始启用范围：

| `enableForLevel` | 默认启用的消息类型 |
| --- | --- |
| `QtDebugMsg` | Debug、Info、Warning、Critical、Fatal |
| `QtInfoMsg` | Info、Warning、Critical、Fatal |
| `QtWarningMsg` | Warning、Critical、Fatal |
| `QtCriticalMsg` | Critical、Fatal |
| `QtFatalMsg` | Fatal；但 Fatal 本身不能被关闭 |

例如：

```cpp
Q_LOGGING_CATEGORY(lcDatabase, "app.database", QtWarningMsg)
```

这表示没有其他配置时，数据库类别默认只输出 Warning 及更严重消息。它不是“只允许 Warning”，后续规则仍可以打开 Debug 或 Info。

用户定义类别通常以 `QtDebugMsg` 开始更方便开发调试。Qt 自身以 `qt` 开头的类别有不同的默认策略，不能把 Qt 内部类别的默认值机械套用到应用类别上。

### 5.3 `QtFatalMsg` 的特殊性

Fatal 级别用于不可恢复错误。`qCFatal()` 会记录消息并终止程序，默认消息处理行为不会因为普通类别规则而变成“安全继续”。

因此：

- 不要把可恢复错误写成 Fatal；
- 不要用 `qCFatal()` 代替异常、错误返回或用户提示；
- 不要把 Fatal 当作普通可开关的调试级别；
- `setEnabled(QtFatalMsg, false)` 不能用来让 Fatal 变成普通日志。

### 5.4 规则的基本格式

规则一般写成：

```text
类别模式.消息级别=true|false
```

例如：

```text
app.network.debug=true
app.network.info=true
app.storage.debug=false
app.*.warning=true
```

类别通配模式主要用于类别名的开头或结尾，例如 `app.*`。不要把它当作完整正则表达式使用；复杂的中间通配和正则语义不属于日志规则的通用保证。

规则可以用换行或分号分隔。为了便于配置文件阅读，应用内字符串通常使用换行：

```cpp
QLoggingCategory::setFilterRules(QStringLiteral(
    "app.network.debug=true\n"
    "app.network.info=true\n"
    "app.storage.debug=false"));
```

### 5.5 规则顺序和外部配置优先级

多个来源可以提供规则。Qt 会按配置来源处理规则，后应用的匹配通常覆盖先应用的匹配。实际部署中需要特别注意：

- Qt 的日志配置文件可以提供默认规则；
- `QLoggingCategory::setFilterRules()` 可以在程序中设置规则；
- `QT_LOGGING_CONF` 可以指定日志配置文件；
- `QT_LOGGING_RULES` 可以直接通过环境变量提供规则；
- 环境变量可能覆盖程序内设置，因此调试机器上的环境配置可能让 `setFilterRules()` 看起来没有生效。

如果应用必须保证某些类别一定关闭或一定开启，应先检查环境变量和外部配置，而不是只看 C++ 源码。

## 6. 逐项 API 说明

### 6.1 `typedef void (*QLoggingCategory::CategoryFilter)(QLoggingCategory *)`

```cpp
using CategoryFilter = void (*)(QLoggingCategory *);
```

**作用：** 定义全局类别过滤器回调的函数类型。

过滤器会收到一个类别指针，然后可以根据类别名和策略调用 `setEnabled()` 设置各类消息是否启用：

```cpp
void myCategoryFilter(QLoggingCategory *category)
{
    const QByteArray name = category->categoryName();

    if (name == "app.network") {
        category->setEnabled(QtDebugMsg, true);
        category->setEnabled(QtInfoMsg, true);
    }
}
```

**关键边界：**

- 这是全局过滤器类型，一个进程通常只有一个当前过滤器；
- 过滤器可能在已有类别和新创建类别上被调用；
- 过滤器必须是普通函数、无捕获函数指针或其他可转换为该函数指针的回调；
- 如果过滤器访问外部配置，应保证外部状态的并发安全；
- 安装自定义过滤器后，常规日志规则不会再替它做最终开关决策。

### 6.2 `explicit QLoggingCategory::QLoggingCategory(const char *category, QtMsgType enableForLevel = QtDebugMsg)`

```cpp
explicit QLoggingCategory(
    const char *category,
    QtMsgType enableForLevel = QtDebugMsg);
```

**作用：** 创建一个指定名称和默认启用级别的日志类别对象。

**关键语义：**

- `category` 是以 `\0` 结尾的类别名；
- 类别名通常应使用字符串字面量或静态存储期的字符数组；
- 不要把临时 `QByteArray::constData()` 或即将销毁的字符缓冲区传进去；
- `enableForLevel` 只提供类别的初始默认状态；
- 过滤规则或自定义过滤器可能在之后修改实际启用状态；
- 类别对象通常通过 `Q_LOGGING_CATEGORY` 宏定义，不应在每条日志中反复手工构造。

安全的类别定义：

```cpp
QLoggingCategory category("app.worker");
```

有风险的写法：

```cpp
QByteArray name = makeCategoryName();
QLoggingCategory category(name.constData());
// name 变化或销毁后，category 仍可能需要使用原类别名。
```

### 6.3 `QLoggingCategory::~QLoggingCategory()`

```cpp
~QLoggingCategory();
```

**作用：** 销毁类别对象。

**关键语义：**

- 日志类别通常是静态或长生命周期对象；
- 不要在消息处理器、过滤器或其他线程仍可能使用时提前销毁类别；
- 类别销毁不会删除配置文件中的规则，也不会清除进程外的环境变量；
- 使用宏定义的静态类别时，要注意静态初始化和静态析构期间不要从其他静态对象调用它。

### 6.4 `const char *QLoggingCategory::categoryName() const`

```cpp
const char *categoryName() const;
```

**作用：** 返回类别名。

**关键语义：**

- 返回的是类别使用的字符指针，不是 `QString`；
- 指针的有效期受类别对象和类别名存储期约束；
- 适合在过滤器中做名称匹配；
- 只读类别名，不要修改返回的字符内容；
- 对环境变量和规则匹配来说，类别名的拼写和大小写应保持稳定。

```cpp
void filter(QLoggingCategory *category)
{
    if (qstrcmp(category->categoryName(), "app.storage") == 0)
        category->setEnabled(QtDebugMsg, true);
}
```

### 6.5 `QLoggingCategory *QLoggingCategory::defaultCategory()`

```cpp
static QLoggingCategory *defaultCategory();
```

**作用：** 返回 Qt 默认日志类别。

它对应没有显式指定分类的普通消息路径，例如 `qDebug()` 等非分类输出通常会落到默认类别。

**关键语义：**

- 返回的是 Qt 管理的类别指针，调用方不拥有它；
- 不要删除、替换或长期保存一个跨应用生命周期的假设；
- 过滤器可以通过它识别或修改默认类别；
- 默认类别与应用自定义的 `Q_LOGGING_CATEGORY` 不是同一个类别；
- 如果只想控制某个模块，优先定义并使用自定义类别，而不是修改默认类别。

### 6.6 `QLoggingCategory::CategoryFilter QLoggingCategory::installFilter(QLoggingCategory::CategoryFilter filter)`

```cpp
static QLoggingCategory::CategoryFilter installFilter(
    QLoggingCategory::CategoryFilter filter);
```

**作用：** 安装进程级自定义类别过滤器，并返回安装前的过滤器。

典型写法：

```cpp
void categoryFilter(QLoggingCategory *category)
{
    const QByteArray name = category->categoryName();
    const bool verbose = name == "app.network";

    category->setEnabled(QtDebugMsg, verbose);
    category->setEnabled(QtInfoMsg, verbose);
}

const auto previous =
    QLoggingCategory::installFilter(categoryFilter);
```

**关键语义：**

- 过滤器是进程级的，不是某个类别对象的局部回调；
- 安装后会影响已有类别和之后创建的类别；
- 返回值可以保存，用于之后恢复旧过滤器；
- 传入 `nullptr` 可以恢复默认过滤行为；
- 自定义过滤器安装后，`setFilterRules()` 规则会被忽略或不再作为最终决策；
- 不要在过滤器中执行慢 I/O、显示对话框或触发复杂日志递归；
- 过滤器中修改类别状态时，应只做开关决策，不要把业务逻辑塞进来。

恢复旧过滤器：

```cpp
QLoggingCategory::installFilter(previous);
```

如果应用有多个库都想安装过滤器，必须建立明确的组合策略；后安装的过滤器不会自动把之前的过滤器链式调用起来。

### 6.7 `bool QLoggingCategory::isCriticalEnabled() const`

```cpp
bool isCriticalEnabled() const;
```

**作用：** 查询当前类别是否启用 Critical 消息。

**适用场景：**

- Critical 消息参数需要复杂计算；
- 需要在输出前构造结构化诊断数据；
- 使用非标准输出路径，但仍希望复用类别开关。

```cpp
if (lcStorage().isCriticalEnabled()) {
    const auto snapshot = buildStorageSnapshot();
    qCCritical(lcStorage) << snapshot;
}
```

通常不需要在普通 `qCCritical()` 前手写判断，因为分类宏本身已经会避免禁用消息的输出表达式继续执行。

### 6.8 `bool QLoggingCategory::isDebugEnabled() const`

```cpp
bool isDebugEnabled() const;
```

**作用：** 查询当前类别是否启用 Debug 消息。

**关键边界：**

- 只表示当前类别的 Debug 开关；
- 不表示 Info、Warning 或 Critical 是否启用；
- 不能用它决定业务行为；
- 应只用于诊断工作、昂贵数据准备或条件化调试断言。

### 6.9 `bool QLoggingCategory::isEnabled(QtMsgType msgtype) const`

```cpp
bool isEnabled(QtMsgType msgtype) const;
```

**作用：** 按 `QtMsgType` 查询消息是否启用。

```cpp
if (lcNetwork().isEnabled(QtInfoMsg))
    collectConnectionDiagnostics();
```

**关键语义：**

- `QtDebugMsg`、`QtInfoMsg`、`QtWarningMsg`、`QtCriticalMsg` 和 `QtFatalMsg` 各自表示一个级别；
- `QtFatalMsg` 的语义特殊，不能把它当成普通可关闭级别；
- 查询结果可能因规则、过滤器或运行时配置改变；
- 这只是日志开关，不应控制连接重试、数据校验等业务逻辑。

### 6.10 `bool QLoggingCategory::isInfoEnabled() const`

```cpp
bool isInfoEnabled() const;
```

**作用：** 查询当前类别是否启用 Info 消息。

Info 适合记录正常但有业务意义的状态，例如连接建立、配置加载完成或任务开始。不要把高频循环中的每一项都作为 Info，否则开启后日志量可能快速增长。

### 6.11 `bool QLoggingCategory::isWarningEnabled() const`

```cpp
bool isWarningEnabled() const;
```

**作用：** 查询当前类别是否启用 Warning 消息。

Warning 表示可继续运行但值得注意的异常状态。它通常比 Debug 和 Info 默认更容易保留，因此消息内容应包含足够的上下文，不能依赖只有开发者知道的内部编号。

### 6.12 `void QLoggingCategory::setEnabled(QtMsgType type, bool enable)`

```cpp
void setEnabled(QtMsgType type, bool enable);
```

**作用：** 修改一个类别在指定消息类型上的启用状态。

**最重要的边界：** 这个函数主要用于 `CategoryFilter` 内部。一般业务代码不应在每次请求、每个对象或每条日志前调用它，否则会把全局日志策略变成分散的隐式状态。

推荐：

```cpp
void categoryFilter(QLoggingCategory *category)
{
    if (qstrcmp(category->categoryName(), "app.parser") == 0)
        category->setEnabled(QtDebugMsg, true);
}
```

不推荐：

```cpp
void parse()
{
    // 不要把类别全局开关散落在业务函数里。
    lcParser().setEnabled(QtDebugMsg, true);
    qCDebug(lcParser) << "parsing";
}
```

**关键语义：**

- 修改的是类别的日志开关，不是全局规则文本；
- 不会影响其他类别；
- 不应依赖它来关闭 Fatal；
- 如果已经安装自定义过滤器，规则配置通常不会覆盖过滤器做出的设置；
- 使用前要明确是谁拥有全局日志策略。

### 6.13 `void QLoggingCategory::setFilterRules(const QString &rules)`

```cpp
static void setFilterRules(const QString &rules);
```

**作用：** 设置进程级日志类别规则。

```cpp
QLoggingCategory::setFilterRules(QStringLiteral(
    "app.*.debug=false\n"
    "app.network.debug=true\n"
    "app.network.info=true"));
```

**关键语义：**

- 规则对匹配类别的不同消息级别设置开关；
- 可以影响已经存在和之后创建的类别；
- 规则字符串由类别模式、消息级别和布尔值组成；
- 后面的匹配规则可能覆盖前面的匹配结果；
- 环境变量 `QT_LOGGING_RULES` 或 `QT_LOGGING_CONF` 可能让程序内设置不成为最终配置；
- 如果安装了自定义 `CategoryFilter`，过滤器会接管类别开关，规则不再按普通方式生效；
- 调用它不会把规则保存到磁盘，也不会修改环境变量。

建议在应用启动早期、创建大量类别之前设置规则，以减少初始化阶段日志状态的不确定性；如果需要让用户运行时切换日志级别，也应把这次修改作为明确的全局配置操作。

### 6.14 `QLoggingCategory &QLoggingCategory::operator()()`

```cpp
QLoggingCategory &operator()();
```

**作用：** 返回当前类别对象的非 const 引用。

它使 `QLoggingCategory` 对象可以通过类别宏的调用形式交给日志 API：

```cpp
QLoggingCategory category("app.example");

if (category().isDebugEnabled())
    qCDebug(category) << "debug message";
```

在 `Q_LOGGING_CATEGORY(lcExample, "app.example")` 这种宏定义中，`lcExample` 可以作为类别入口使用，`lcExample()` 则取得类别引用。

**关键边界：**

- 返回的是对象自身，不创建新的日志类别；
- 不要把返回引用保存到超过类别对象生命周期的位置；
- 该调用不是“重新注册类别”或“复制类别配置”；
- 多线程场景下类别开关由 Qt 维护，但调用方仍需保证类别对象自身生命周期正确。

### 6.15 `const QLoggingCategory &QLoggingCategory::operator()() const`

```cpp
const QLoggingCategory &operator()() const;
```

**作用：** 返回当前类别对象的 const 引用。

它允许 const 类别对象继续用于只读查询和分类日志入口：

```cpp
void inspect(const QLoggingCategory &category)
{
    if (category().isInfoEnabled())
        qCInfo(category) << "category is enabled";
}
```

这个重载不会修改类别状态。若需要在过滤器中开关级别，应使用非常量类别指针或引用调用 `setEnabled()`。

## 7. 分类定义宏

宏不是 `QLoggingCategory` 的成员函数，但它们是实际使用该类的主要入口，必须和 API 一起理解。

### 7.1 `[since 6.5] Q_DECLARE_EXPORTED_LOGGING_CATEGORY(name, EXPORT_MACRO)`

```cpp
Q_DECLARE_EXPORTED_LOGGING_CATEGORY(lcPlugin, PLUGIN_EXPORT)
```

**作用：** 在公共头文件中声明一个需要跨动态库边界导出的日志类别。

**使用方式：**

```cpp
// pluginlogging.h
#include <QLoggingCategory>

Q_DECLARE_EXPORTED_LOGGING_CATEGORY(lcPlugin, PLUGIN_EXPORT)
```

再在一个源文件中定义：

```cpp
Q_LOGGING_CATEGORY(lcPlugin, "plugin.core")
```

**边界：**

- Qt 6.5 起可用；
- `EXPORT_MACRO` 是库自己的符号导出宏；
- 只应有一个定义源文件；
- 它解决 C++ 符号可见性，不改变日志规则或消息级别。

### 7.2 `Q_DECLARE_LOGGING_CATEGORY(name)`

```cpp
Q_DECLARE_LOGGING_CATEGORY(lcNetwork)
```

**作用：** 声明一个由其他源文件提供定义的日志类别入口。

通常放在公共头文件，配合一个 `Q_LOGGING_CATEGORY()` 定义：

```cpp
// app_logging.h
Q_DECLARE_LOGGING_CATEGORY(lcNetwork)

// app_logging.cpp
Q_LOGGING_CATEGORY(lcNetwork, "app.network")
```

**边界：**

- 只声明不定义，缺少定义会在链接阶段失败；
- 不要在多个源文件中重复使用 `Q_LOGGING_CATEGORY()` 定义同一个类别符号；
- 跨动态库时使用导出版本的声明宏。

### 7.3 `Q_LOGGING_CATEGORY(name, string)`

```cpp
Q_LOGGING_CATEGORY(lcNetwork, "app.network")
```

**作用：** 定义一个日志类别，默认从 `QtDebugMsg` 级别开始启用。

**关键语义：**

- 通常在一个 `.cpp` 文件中使用一次；
- `name` 是代码中使用的类别入口；
- `string` 是运行时规则匹配的类别名；
- 类别对象的初始化和第一次使用由 Qt 负责线程安全处理；
- 定义所在的翻译单元必须链接到最终程序或库。

### 7.4 `Q_LOGGING_CATEGORY(name, string, msgType)`

```cpp
Q_LOGGING_CATEGORY(lcStorage, "app.storage", QtInfoMsg)
```

**作用：** 定义日志类别，并指定默认启用的最低级别。

第三个参数只影响没有其他规则覆盖时的初始状态。它不能阻止之后通过 `setFilterRules()` 或环境变量打开更详细级别。

### 7.5 `[since 6.9] Q_STATIC_LOGGING_CATEGORY(name, string)`

```cpp
Q_STATIC_LOGGING_CATEGORY(lcParser, "app.parser")
```

**作用：** 在实现文件中定义一个静态日志类别。

**适用场景：**

- 类别只供当前源文件使用；
- 不想在库的公共符号中暴露类别入口；
- 避免多个实现文件意外共享相同的 C++ 符号名称。

**边界：**

- Qt 6.9 起可用；
- “静态”不代表不受全局过滤规则影响；
- 仍然要保证类别名稳定；
- 不要把这个宏放在需要跨源文件复用的公共 API 中。

### 7.6 `[since 6.9] Q_STATIC_LOGGING_CATEGORY(name, string, msgType)`

```cpp
Q_STATIC_LOGGING_CATEGORY(lcParser, "app.parser", QtWarningMsg)
```

**作用：** 定义静态类别并指定默认启用级别。

其他语义与三参数 `Q_LOGGING_CATEGORY()` 相同，只是类别定义范围更偏向当前实现文件。最低 Qt 版本低于 6.9 时不能直接使用。

## 8. 分类输出宏

### 8.1 `qCDebug(category)`

```cpp
qCDebug(lcNetwork) << "connected to" << host;
```

**作用：** 以 Debug 级别向指定类别输出流式消息。

**边界：**

- 类别关闭时，流表达式不会继续执行；
- 不要依赖流表达式中的函数副作用；
- 复杂诊断数据可以直接放在表达式中，让类别开关负责跳过；
- 需要严格控制执行路径时，可以先调用 `isDebugEnabled()`。

### 8.2 `qCDebug(category, const char *message, ...)`

```cpp
qCDebug(lcNetwork, "retrying connection to %s",
        host.toUtf8().constData());
```

**作用：** 以 printf 风格向指定类别输出 Debug 消息。

**边界：**

- 格式字符串和参数类型必须匹配；
- 这是 C 风格可变参数接口，不能获得 C++ 流式格式化的类型检查；
- 类别关闭时，参数表达式通常不会被求值；
- 需要输出 Qt 类型时，要先选择正确的 UTF-8 或数值转换方式。

### 8.3 `qCInfo(category)`

```cpp
qCInfo(lcStorage) << "cache opened";
```

**作用：** 以 Info 级别输出流式分类消息。

Info 适合记录用户或运维真正关心的正常状态。对于高频路径，应优先使用 Debug，避免生产环境默认日志量过大。

### 8.4 `qCInfo(category, const char *message, ...)`

```cpp
qCInfo(lcStorage, "loaded %d records", recordCount);
```

**作用：** 以 printf 风格输出 Info 分类消息。

使用时遵守同样的格式字符串、参数类型和副作用边界。

### 8.5 `qCWarning(category)`

```cpp
qCWarning(lcStorage) << "cache is stale";
```

**作用：** 以 Warning 级别输出流式分类消息。

Warning 表示程序仍可继续，但状态值得处理。消息应包含类别上下文之外的关键对象标识、原因和后续动作，便于单独查看日志时理解。

### 8.6 `qCWarning(category, const char *message, ...)`

```cpp
qCWarning(lcStorage, "cache entry %s is invalid",
          key.toUtf8().constData());
```

**作用：** 以 printf 风格输出 Warning 分类消息。

不要把用户可控字符串直接当作格式字符串。始终把它作为 `%s` 等参数传递。

### 8.7 `qCCritical(category)`

```cpp
qCCritical(lcDatabase) << "transaction cannot be committed";
```

**作用：** 以 Critical 级别输出流式分类消息。

Critical 表示当前功能或系统状态发生严重问题，但程序未必需要立即终止。它应与错误恢复、回滚或降级策略保持一致。

### 8.8 `qCCritical(category, const char *message, ...)`

```cpp
qCCritical(lcDatabase, "rollback failed for transaction %lld",
           transactionId);
```

**作用：** 以 printf 风格输出 Critical 分类消息。

消息本身不会替代事务回滚或故障转移；不要因为日志级别高就省略真正的错误处理。

### 8.9 `[since 6.5] qCFatal(category)`

```cpp
qCFatal(lcCore) << "unrecoverable invariant violation";
```

**作用：** 输出 Fatal 分类消息并终止程序。

**关键边界：**

- Qt 6.5 起提供；
- Fatal 不是普通可禁用日志；
- 只用于程序继续运行会导致更严重破坏的不可恢复状态；
- 不要用于用户输入错误、网络暂时断开或普通资源不足；
- 不能依赖后续清理逻辑一定执行。

### 8.10 `[since 6.5] qCFatal(category, const char *message, ...)`

```cpp
qCFatal(lcCore, "invalid protocol state: %d", state);
```

**作用：** 以 printf 风格输出 Fatal 消息并终止程序。

它的参数格式和终止语义与流式 `qCFatal()` 相同。因为程序会终止，不要在参数中安排必须执行的业务副作用。

## 9. 自定义过滤器与规则的选择

### 9.1 优先使用规则，而不是自定义过滤器

大多数应用只需要：

```cpp
QLoggingCategory::setFilterRules(QStringLiteral(
    "app.network.debug=true\n"
    "app.storage.debug=false"));
```

或者让部署环境提供 `QT_LOGGING_RULES`。规则可读、可诊断，也容易交给运维人员调整。

### 9.2 什么时候需要 `CategoryFilter`

自定义过滤器适合：

- 开关依赖运行时配置对象，而不是固定文本；
- 需要统一处理多个库的类别命名策略；
- 应用有自己的日志级别配置界面；
- 初始化时要按平台、构建类型或设备能力设定类别。

过滤器示例：

```cpp
void filterByBuildMode(QLoggingCategory *category)
{
    const QByteArray name = category->categoryName();
    const bool verbose =
#ifdef QT_DEBUG
        true;
#else
        false;
#endif

    if (name.startsWith("app."))
        category->setEnabled(QtDebugMsg, verbose);
}
```

### 9.3 过滤器是全局单槽，不是过滤器链

`installFilter()` 返回旧过滤器是为了让调用方能够保存和恢复它，但 Qt 不会自动把多个过滤器串成链。库代码随意安装全局过滤器可能破坏应用或其他插件的日志策略。

共享进程级过滤器时，要约定：

- 谁负责安装；
- 谁负责恢复；
- 是否调用旧过滤器；
- 如何避免递归安装和初始化顺序问题。

## 10. 线程、安全和初始化边界

### 10.1 类别查询和开关操作由 Qt 设计为线程安全

类别可以从多个线程输出，类别注册和规则更新由 Qt 的内部机制协调。典型的：

```cpp
qCDebug(lcNetwork) << packet;
```

可以在工作线程中使用。

这不等于业务对象自动线程安全。消息参数读取的对象、过滤器访问的配置、消息处理器写入的文件都必须由应用自己保证安全。

### 10.2 自定义过滤器要保护外部状态

如果过滤器读取一个可变配置：

```cpp
void filter(QLoggingCategory *category)
{
    category->setEnabled(QtDebugMsg, globalSettings().verbose());
}
```

需要确认 `globalSettings()` 的生命周期和并发访问协议。过滤器可能被类别创建或规则更新触发，不要假定它永远只在主线程调用。

### 10.3 静态初始化顺序

日志类别经常是静态对象或静态函数入口。不要在另一个全局对象的构造函数中依赖一个尚未初始化的业务配置来决定类别状态。

更稳妥的方式是：

- 让类别定义保持简单；
- 在 `main()` 创建应用对象后尽早设置规则；
- 对需要动态更新的级别使用明确的配置阶段；
- 静态析构阶段不要输出依赖其他静态对象的日志。

### 10.4 日志处理器不是类别过滤器

类别决定消息是否生成，消息处理器决定已经生成的消息去哪里。即使安装了自定义消息处理器，也不能绕过类别关闭后参数不求值的优化。

反过来，消息处理器也可能丢弃某类消息，但这发生在消息已经构造之后，不能替代类别级别的早期过滤。

## 11. 常见错误与排查顺序

### 11.1 在头文件中直接用 `Q_LOGGING_CATEGORY`

**症状：** 多重定义链接错误。

**原因：** `Q_LOGGING_CATEGORY` 是定义宏，不是声明宏。

**修复：** 头文件使用 `Q_DECLARE_LOGGING_CATEGORY`，只在一个源文件使用定义宏。

### 11.2 以为 `Q_LOGGING_CATEGORY` 的默认级别是最终配置

**症状：** 代码中写了 `QtWarningMsg`，但部署环境仍然看到了 Debug。

**原因：** 环境变量、配置文件或规则覆盖了默认级别。

**修复：** 检查 `QT_LOGGING_RULES`、`QT_LOGGING_CONF`、Qt 日志配置文件和自定义过滤器。

### 11.3 在每条日志前调用 `setEnabled`

**症状：** 日志状态难以追踪，多个模块互相覆盖开关。

**原因：** 把全局策略操作混进业务路径。

**修复：** 使用规则或一个集中的 `CategoryFilter`，业务代码只负责输出。

### 11.4 把禁用日志表达式当成必执行代码

**症状：** 计数器没有增加，缓存没有刷新，或者某个函数偶尔没有调用。

**原因：** 日志类别关闭时，表达式参数不会执行。

**修复：** 先单独执行必须的业务动作，再把结果传给日志：

```cpp
const auto state = updateState();
qCDebug(lcCore) << "new state:" << state;
```

### 11.5 用类别日志替代错误处理

**症状：** 日志里写了“保存失败”，但调用方仍然继续使用无效数据。

**原因：** `qCWarning()` 和 `qCCritical()` 只记录消息，不改变业务控制流。

**修复：** 返回错误、抛出合适异常或执行恢复；日志用于记录上下文。

### 11.6 把 `qCFatal` 当作高优先级 Warning

**症状：** 用户输入稍有问题程序就退出。

**原因：** 混淆了严重程度和不可恢复性。

**修复：** 可恢复问题用 Warning/Critical 加实际恢复逻辑，只有不可继续运行的内部不变量破坏才考虑 Fatal。

### 11.7 自定义过滤器中做重工作

**症状：** 类别初始化变慢、启动卡顿或日志递归。

**原因：** 过滤器本应只设置开关，却执行了 I/O、格式化或复杂业务。

**修复：** 过滤器只读取必要配置和设置启用状态，把真正工作放在业务调用路径。

### 11.8 动态类别名来自短生命周期内存

**症状：** 日志类别名异常变化或规则匹配不稳定。

**原因：** `QLoggingCategory` 依赖传入的字符数据在使用期间有效。

**修复：** 使用字符串字面量或静态存储期的字符数组，类别名不要随请求动态生成。

## 12. 推荐的项目组织方式

### 12.1 一个日志类别头文件

```cpp
// app_logging.h
#pragma once

#include <QLoggingCategory>

Q_DECLARE_LOGGING_CATEGORY(lcCore)
Q_DECLARE_LOGGING_CATEGORY(lcNetwork)
Q_DECLARE_LOGGING_CATEGORY(lcStorage)
```

### 12.2 一个定义源文件

```cpp
// app_logging.cpp
#include "app_logging.h"

Q_LOGGING_CATEGORY(lcCore, "app.core", QtInfoMsg)
Q_LOGGING_CATEGORY(lcNetwork, "app.network")
Q_LOGGING_CATEGORY(lcStorage, "app.storage", QtWarningMsg)
```

### 12.3 启动阶段设置默认规则

```cpp
int main(int argc, char **argv)
{
    QCoreApplication app(argc, argv);

    QLoggingCategory::setFilterRules(QStringLiteral(
        "app.core.debug=false\n"
        "app.network.debug=false\n"
        "app.storage.debug=false"));

    return app.exec();
}
```

若产品允许环境变量覆盖本地规则，应在文档和诊断页面中明确显示“最终规则可能来自外部配置”，避免用户误以为 `main()` 中的字符串一定拥有最高优先级。

## API 速查表

### 13.1 类型、构造与状态查询

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QLoggingCategory::CategoryFilter` | 定义全局类别过滤器函数类型 | 回调需要处理外部状态并避免重工作 |
| `QLoggingCategory(const char *category, QtMsgType enableForLevel = QtDebugMsg)` | 创建类别对象并设置初始级别 | 类别名字符存储必须保持有效；通常使用宏定义 |
| `~QLoggingCategory()` | 销毁类别对象 | 静态对象和消息处理器的生命周期要协调 |
| `categoryName() const` | 读取类别名 | 返回 `const char *`；只读且不要依赖临时字符缓冲区 |
| `defaultCategory()` | 获取默认类别 | Qt 管理所有权；自定义模块应定义自己的类别 |
| `operator()()` | 返回非常量类别引用 | 用于宏入口和状态查询；不创建新类别 |
| `operator()() const` | 返回 const 类别引用 | 只能进行只读使用，不适合调用 `setEnabled()` |

### 13.2 过滤器和开关

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `installFilter(CategoryFilter filter)` | 安装进程级自定义过滤器 | 全局单槽；自定义过滤器会接管规则决策 |
| `setFilterRules(const QString &rules)` | 设置进程级类别规则 | 可能被环境变量覆盖；与自定义过滤器不是普通叠加关系 |
| `setEnabled(QtMsgType type, bool enable)` | 设置某个级别开关 | 主要在 `CategoryFilter` 内使用，不要散落在业务路径 |
| `isEnabled(QtMsgType msgtype) const` | 查询指定消息级别是否启用 | 只影响日志生成，不控制业务逻辑 |
| `isDebugEnabled() const` | 查询 Debug 开关 | 适合跳过昂贵诊断数据准备 |
| `isInfoEnabled() const` | 查询 Info 开关 | Info 适合正常但有运维价值的状态 |
| `isWarningEnabled() const` | 查询 Warning 开关 | Warning 不替代恢复动作 |
| `isCriticalEnabled() const` | 查询 Critical 开关 | Critical 不等于必须终止 |

### 13.3 类别声明与定义宏

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `Q_DECLARE_LOGGING_CATEGORY(name)` | 在头文件声明类别 | 必须由一个源文件中的 `Q_LOGGING_CATEGORY` 提供定义 |
| `Q_DECLARE_EXPORTED_LOGGING_CATEGORY(name, EXPORT_MACRO)` | 声明跨动态库导出的类别 | Qt 6.5 起；仍只定义一次 |
| `Q_LOGGING_CATEGORY(name, string)` | 定义默认 Debug 起始级别的类别 | 通常在一个 `.cpp` 中使用一次 |
| `Q_LOGGING_CATEGORY(name, string, msgType)` | 定义并指定初始最低级别 | 初始值可能被规则或过滤器覆盖 |
| `Q_STATIC_LOGGING_CATEGORY(name, string)` | 定义实现文件内静态类别 | Qt 6.9 起；仍受全局规则影响 |
| `Q_STATIC_LOGGING_CATEGORY(name, string, msgType)` | 定义静态类别并指定初始级别 | Qt 6.9 起；不用于公共跨文件类别 |

### 13.4 分类输出宏

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `qCDebug(category)` | 输出 Debug 流式分类消息 | 类别关闭时表达式不会继续执行 |
| `qCDebug(category, const char *message, ...)` | 输出 Debug printf 风格消息 | 格式字符串与可变参数必须匹配 |
| `qCInfo(category)` | 输出 Info 流式分类消息 | 高频状态不要默认使用 Info |
| `qCInfo(category, const char *message, ...)` | 输出 Info printf 风格消息 | 不要把用户字符串当格式字符串 |
| `qCWarning(category)` | 输出 Warning 流式分类消息 | 消息应包含原因和上下文 |
| `qCWarning(category, const char *message, ...)` | 输出 Warning printf 风格消息 | 只记录，不自动执行恢复 |
| `qCCritical(category)` | 输出 Critical 流式分类消息 | 严重但不必然终止 |
| `qCCritical(category, const char *message, ...)` | 输出 Critical printf 风格消息 | 应与回滚、降级等错误处理配套 |
| `[since 6.5] qCFatal(category)` | 输出 Fatal 流式消息并终止 | 不可恢复状态专用，不能当普通开关日志 |
| `[since 6.5] qCFatal(category, const char *message, ...)` | 输出 Fatal printf 风格消息并终止 | 参数不要依赖必须执行的副作用 |

## 14. 一句话总结

`QLoggingCategory` 是 Qt 的进程级日志分类开关：用稳定类别名组织模块，用 `Q_LOGGING_CATEGORY` 定义入口，用 `qC...` 宏输出，用规则或统一过滤器控制级别；类别关闭时日志表达式可以被跳过，但日志永远只是诊断通道，不能替代真实的错误处理和业务控制流。
