# QLoggingCategory

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QLoggingCategory` 是 Qt 日志与诊断体系中的类型，用于按类别输出调试、信息、警告或错误消息。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QLoggingCategory` 是 Qt 日志与诊断机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 日志 API 把消息级别、类别、源文件/行号上下文和最终处理器分开。`qDebug`、`qInfo`、`qWarning`、`qCritical` 负责产生消息，分类规则和 message handler 决定输出到哪里、是否过滤或持久化。

**适用场景：** 用分类定义稳定的日志边界，使用合适级别记录状态和错误，必要时安装 handler 写入文件或诊断系统；敏感信息、token、密码不要输出。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要用 qFatal 代替普通错误处理；不要在 handler 里再次触发同类日志；不要把日志文本当作稳定的程序接口；注意 release 构建中的上下文宏和过滤规则。

## 2. 依赖与对象关系

- 头文件：`#include <QLoggingCategory>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Qt 日志 API 把消息级别、类别、源文件/行号上下文和最终处理器分开。`qDebug`、`qInfo`、`qWarning`、`qCritical` 负责产生消息，分类规则和 message handler 决定输出到哪里、是否过滤或持久化。

### 状态、生命周期和线程

**生命周期：** 日志上下文通常是一次消息表达式的临时对象；自定义 message handler 的安装和卸载要覆盖整个使用期，处理器内部不要递归调用会再次触发日志的代码。

**状态与结果：** 日志是否输出受级别、类别规则、编译宏和运行时过滤影响。看到某条消息缺失时，要区分代码没有执行、日志级别被过滤、上下文被关闭和 handler 改写输出。

**线程与事件循环：** 日志可能来自多个线程，handler 必须考虑并发、输出原子性和不能阻塞业务线程；不要在 handler 中访问未加锁的 GUI 控件。

## 3. 直接使用

用分类定义稳定的日志边界，使用合适级别记录状态和错误，必要时安装 handler 写入文件或诊断系统；敏感信息、token、密码不要输出。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
#include <QDebug>

qInfo() << "operation started";
qWarning() << "operation failed";
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `CategoryFilter`

### 公有函数

- `QLoggingCategory(const char *category, QtMsgType enableForLevel = QtDebugMsg)`
- `~QLoggingCategory()`
- `const char * categoryName() const`
- `bool isCriticalEnabled() const`
- `bool isDebugEnabled() const`
- `bool isEnabled(QtMsgType msgtype) const`
- `bool isInfoEnabled() const`
- `bool isWarningEnabled() const`
- `void setEnabled(QtMsgType type, bool enable)`
- `QLoggingCategory & operator()()`
- `const QLoggingCategory & operator()() const`

### 静态公有成员

- `QLoggingCategory * defaultCategory()`
- `QLoggingCategory::CategoryFilter installFilter(QLoggingCategory::CategoryFilter filter)`
- `void setFilterRules(const QString &rules)`

### 公开宏

- `(since 6.5) Q_DECLARE_EXPORTED_LOGGING_CATEGORY(name, EXPORT_MACRO)`
- `Q_DECLARE_LOGGING_CATEGORY(name)`
- `Q_LOGGING_CATEGORY(name, string)`
- `Q_LOGGING_CATEGORY(name, string, msgType)`
- `(since 6.9) Q_STATIC_LOGGING_CATEGORY(name, string)`
- `(since 6.9) Q_STATIC_LOGGING_CATEGORY(name, string, msgType)`
- `qCCritical(category)`
- `qCCritical(category, const char *message, ...)`
- `qCDebug(category)`
- `qCDebug(category, const char *message, ...)`
- `(since 6.5) qCFatal(category)`
- `(since 6.5) qCFatal(category, const char *message, ...)`
- `qCInfo(category)`
- `qCInfo(category, const char *message, ...)`
- `qCWarning(category)`
- `qCWarning(category, const char *message, ...)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QLoggingCategory::CategoryFilter`

**作用与语义：**

这是指向函数签名如下的指针的类型def：
带有该签名的函数可以用`installFilter()`安装。

**官方示例：**

```cpp
 void myCategoryFilter(QLoggingCategory *);
```

### `[explicit] QLoggingCategory::QLoggingCategory(const char *category, QtMsgType enableForLevel = QtDebugMsg)`

**作用与语义：**

构建一个带有`category`名称的QLoggingCategory对象，并启用所有类型至少与`enableForLevel`一样冗长的消息，默认为`QtDebugMsg`（启用所有类别）。
如果`category` `nullptr`，则使用类别名称`"default"`。
注意：`category`必须在该对象的生命周期内保持有效。通常使用字符串字面值来实现这一点。

### `[noexcept] QLoggingCategory::~QLoggingCategory()`

**作用与语义：**

摧毁一个`QLoggingCategory`物体。

### `const char *QLoggingCategory::categoryName() const`

**作用与语义：**

返回类别名称。

### `[static] QLoggingCategory *QLoggingCategory::defaultCategory()`

**作用与语义：**

返回指向全局范畴`"default"`的指针，例如被 `qDebug()`、`qInfo()`、`qWarning()`、`qCritical()` 或 `qFatal()` 使用。
注意：在销毁静态对象时，返回的指针可能是空的。另外，不要`delete`该指针，因为类别的所有权不会转移。

### `[static] QLoggingCategory::CategoryFilter QLoggingCategory::installFilter(QLoggingCategory::CategoryFilter filter)`

**作用与语义：**

掌控日志分类的配置。
安装一个函数`filter`，用于确定应启用哪些类别和消息类型。如果`filter` `nullptr`，默认消息过滤器将被恢复。返回指向之前安装的过滤器的指针。
所有已存在的`QLoggingCategory`对象都会在`installFilter()`返回前传递给过滤器，过滤器可以自由地用`setEnabled()`更改每个类别的配置。任何未被更改的类别都会保留之前过滤器给出的配置，因此新过滤器在首次处理现有类别时无需委托给之前的过滤器。
之后添加的任何新类别都会传递给新过滤器;仅针对少数特定类别的配置调整，而非完全覆盖日志策略的过滤器，可以先将新类别传递给前一个过滤器，使其获得标准配置，然后根据需要调整该类别，前提是该类别对过滤器有特定兴趣。安装新过滤器的代码可以记录`installFilter()`返回，供过滤器在后续调用中使用。
定义过滤器时，请注意它可以从不同线程调用;但绝不能同时调用。该过滤器不能调用`QLoggingCategory`中的任何静态函数。
安装（例如`main()`）由。
或者，你可以通过`setFilterRules()`配置默认过滤器。

**官方示例：**

```cpp
 static QLoggingCategory::CategoryFilter oldCategoryFilter = nullptr;

 void myCategoryFilter(QLoggingCategory *category)
 {
     // For a category set up after this filter is installed, we first set it up
     // with the old filter. This ensures that any driver.usb logging configured
     // by the user is kept, aside from the one level we override; and any new
     // categories we're not interested in get configured by the old filter.
     if (oldCategoryFilter)
         oldCategoryFilter(category);

     // Tweak driver.usb's logging, over-riding the default filter:
     if (qstrcmp(category->categoryName(), "driver.usb") == 0)
         category->setEnabled(QtDebugMsg, true);
 }
```

### `bool QLoggingCategory::isCriticalEnabled() const`

**作用与语义：**

如果此类别应显示关键消息，则返回 `true`；否则返回 `false`。
注意：`qCCritical()` 宏在执行任何代码之前已经进行了此检查。然而，调用此方法可能有助于避免仅为调试输出而生成数据的高开销。

### `bool QLoggingCategory::isDebugEnabled() const`

**作用与语义：**

返回`true`该类别是否应显示调试消息;否则`false`。
注意：`qCDebug()`宏在运行任何代码前已经完成了这种检查。不过，调用此方法可能有助于避免仅用于调试输出时生成昂贵的数据。

### `bool QLoggingCategory::isEnabled(QtMsgType msgtype) const`

**作用与语义：**

如果该类别应显示类型为`msgtype`的消息，返回`true`;否则`false`。

### `bool QLoggingCategory::isInfoEnabled() const`

**作用与语义：**

如果该类别需要显示信息信息，返回`true`;否则`false`。
注意：`qCInfo()`宏在执行任何代码前已经完成了此检查。不过，调用此方法可能有助于避免仅为调试输出生成昂贵的数据。

### `bool QLoggingCategory::isWarningEnabled() const`

**作用与语义：**

返回`true`该类别是否应显示警告信息;否则`false`。
注意：`qCWarning()`宏在执行任何代码前已经会进行此检查。不过，调用此方法可能有助于避免仅为调试输出生成昂贵的数据。

### `void QLoggingCategory::setEnabled(QtMsgType type, bool enable)`

**作用与语义：**

将该类别的消息类型`type`更改为`enable`。
该方法仅适用于安装在`installFilter()`的过滤器内部使用。关于如何全局配置类别的概述，请参见“配置类别”。
注意：`QtFatalMsg`无法更改;它将始终保持`true`。

### `[static] void QLoggingCategory::setFilterRules(const QString &rules)`

**作用与语义：**

通过一组 `rules`配置应启用哪些类别和消息类型。
注意：如果`installFilter()`安装了自定义类别过滤器，或用户已定义`QT_LOGGING_CONF`或`QT_LOGGING_RULES`环境变量，规则可能会被忽略。

**官方示例：**

```cpp
     QLoggingCategory::setFilterRules(QStringLiteral("driver.usb.debug=true"));
```

### `QLoggingCategory &QLoggingCategory::operator()()`

**作用与语义：**

返回对象本身。这允许同时使用`QLoggingCategory`变量和返回`QLoggingCategory`的工厂方法，分别用于`qCDebug()`、`qCWarning()`、`qCCritical()`或`qCFatal()`宏。

### `const QLoggingCategory &QLoggingCategory::operator()() const`

**作用与语义：**

返回对象本身。这允许同时使用`QLoggingCategory`变量和返回`QLoggingCategory`的工厂方法，分别用于`qCDebug()`、`qCWarning()`、`qCCritical()`或`qCFatal()`宏。

### `[since 6.5] Q_DECLARE_EXPORTED_LOGGING_CATEGORY(name, EXPORT_MACRO)`

**作用与语义：**

声明日志类别`name`。宏可用来声明程序不同部分共享的通用日志类别。
这与`Q_DECLARE_LOGGING_CATEGORY()`完全相同。然而，该宏声明的日志类别还带有 `EXPORT_MACRO` 的限定。如果日志类别需要从动态库导出，这非常有用。
该宏必须在类或函数之外使用。
该宏在第6.5季度引入。

**官方示例：**

```cpp
 Q_DECLARE_EXPORTED_LOGGING_CATEGORY(lcCore, LIB_EXPORT_MACRO)
```

### `Q_DECLARE_LOGGING_CATEGORY(name)`

**作用与语义：**

声明日志类别`name`。宏可用于声明程序不同部分共享的日志类别。
该宏必须在类或方法之外使用。

### `Q_LOGGING_CATEGORY(name, string)`

**作用与语义：**

定义日志类别`name`，并使其可根据`string`标识符进行配置。默认情况下，所有消息类型均为启用。
库或可执行文件中只有一个翻译单元可以定义带有特定名称的类别。隐式定义的`QLoggingCategory`对象在首次使用时以线程安全的方式创建。
该宏必须在类或方法之外使用。

### `Q_LOGGING_CATEGORY(name, string, msgType)`

**作用与语义：**

定义日志类别`name`，并使其可配置为`string`标识符。默认情况下，`QtMsgType` `msgType`及更严重的消息被启用，低严重程度的类型被禁用。
库或可执行文件中只有一个翻译单元可以定义带有特定名称的类别。隐式定义的`QLoggingCategory`对象在首次使用时以线程安全的方式创建。
该宏必须在类或方法之外使用。

### `[since 6.9] Q_STATIC_LOGGING_CATEGORY(name, string)`

**作用与语义：**

定义静态日志类别`name`，并使其可配置为`string`标识符。默认情况下，所有消息类型均为启用。
日志类别是用`static`限定符创建的，这样你只能在同一翻译单元中访问它。这样可以避免符号的意外冲突。
隐式定义的`QLoggingCategory`对象在首次使用时以线程安全的方式创建。
该宏必须在类或方法之外使用。
该宏在Qt 6.9引入。

### `[since 6.9] Q_STATIC_LOGGING_CATEGORY(name, string, msgType)`

**作用与语义：**

定义静态日志类别`name`，并使其可配置为`string`标识符。默认情况下，`QtMsgType` `msgType`及更严重的消息被启用，严重性较低的类型被禁用。
日志类别是用`static`限定词创建的，所以你只能在同一翻译单元中访问它。这样可以避免符号的意外冲突。
隐式定义的`QLoggingCategory`对象在首次使用时以线程安全的方式创建。
该宏必须在类或方法之外使用。
该宏在Qt 6.9引入。

### `qCCritical(category)`

**作用与语义：**

返回日志类别`category`的关键消息输出流。
宏扩展为检查`QLoggingCategory::isCriticalEnabled()`是否对`true`进行评估的代码。如果是，流的参数会被处理并发送给消息处理程序。
注意：如果某个类别的临界输出未被启用，参数将不会被处理，因此不要依赖任何副作用。

**官方示例：**

```cpp
     QLoggingCategory category("driver.usb");
     qCCritical(category) << "a critical message";
```

### `qCCritical(category, const char *message, ...)`

**作用与语义：**

记录日志类别中的关键消息 `message` `category`。`message` 可能包含占位符，并用额外参数替换，类似于 C 的 printf() 函数。
注意：如果某个类别的临界输出未被启用，参数将不会被处理，因此不要依赖任何副作用。

**官方示例：**

```cpp
     QLoggingCategory category("driver.usb");
     qCCritical(category, "a critical message logged into category %s", category.categoryName());
```

### `qCDebug(category)`

**作用与语义：**

返回日志类别`category`的调试消息输出流。
宏展开为检测`QLoggingCategory::isDebugEnabled()`是否对`true`进行评估的代码。如果是，流的参数会被处理并发送给消息处理器。
注意：如果该`category`的调试输出未启用，参数不会被处理，所以不要依赖任何副作用。

**官方示例：**

```cpp
     QLoggingCategory category("driver.usb");
     qCDebug(category) << "a debug message";
```

### `qCDebug(category, const char *message, ...)`

**作用与语义：**

记录日志类别`category`中的调试消息`message`。`message`可能包含用额外参数替换的占位符，类似于C的printf()函数。
注意：如果该`category`的调试输出未启用，参数不会被处理，所以不要依赖任何副作用。

**官方示例：**

```cpp
     QLoggingCategory category("driver.usb");
     qCDebug(category, "a debug message logged into category %s", category.categoryName());
```

### `[since 6.5] qCFatal(category)`

**作用与语义：**

返回日志类别中致命消息的输出流，`category`。
如果你使用默认的消息处理程序，返回的流会中止以创建核心转储。在 Windows 上，对于调试构建，这个函数会报告一个`_CRT_ERROR`，使你能够将调试器连接到应用程序。
该宏在第6.5季度引入。

**官方示例：**

```cpp
     QLoggingCategory category("driver.usb");
     qCFatal(category) << "a fatal message. Program will be terminated!";
```

### `[since 6.5] qCFatal(category, const char *message, ...)`

**作用与语义：**

在日志类别`category`中记录致命消息`message`。`message`可能包含占位符，并用额外的参数替换，类似于 C 的 printf() 函数。
如果你使用默认消息处理程序，这个函数会中止以创建核心转储。在 Windows 上，对于调试构建，这个函数会报告一个`_CRT_ERROR`，使你能够将调试器连接到应用程序。
该宏在第6.5季度引入。

**官方示例：**

```cpp
     QLoggingCategory category("driver.usb");
     qCFatal(category, "a fatal message. Program will be terminated!");
```

### `qCInfo(category)`

**作用与语义：**

返回日志类别`category`的信息消息输出流。
宏扩展为检查 `QLoggingCategory::isInfoEnabled()` 是否对 `true` 进行评估的代码。如果是，流的参数会被处理并发送给消息处理程序。
注意：如果某个类别的调试输出未被启用，参数将不会被处理，因此不要依赖任何副作用。

**官方示例：**

```cpp
     QLoggingCategory category("driver.usb");
     qCInfo(category) << "an informational message";
```

### `qCInfo(category, const char *message, ...)`

**作用与语义：**

记录日志类别中的信息消息 `message`，`category`。`message` 可能包含用额外参数替换的占位符，类似于 C 的 printf() 函数。
注意：如果某个类别的调试输出未被启用，参数将不会被处理，因此不要依赖任何副作用。

**官方示例：**

```cpp
     QLoggingCategory category("driver.usb");
     qCInfo(category, "an informational message logged into category %s", category.categoryName());
```

### `qCWarning(category)`

**作用与语义：**

返回日志类别`category`的警告消息输出流。
宏扩展为检查`QLoggingCategory::isWarningEnabled()`是否对`true`进行评估的代码。如果是，流的参数会被处理并发送给消息处理程序。
注意：如果某个类别的警告输出未被启用，论元将不会被处理，因此不要依赖任何副作用。

**官方示例：**

```cpp
     QLoggingCategory category("driver.usb");
     qCWarning(category) << "a warning message";
```

### `qCWarning(category, const char *message, ...)`

**作用与语义：**

在日志类别`category`中记录警告消息 `message`。`message` 可能包含用额外参数替换的占位符，类似于 C 的 printf() 函数。
注意：如果某个类别的警告输出未被启用，论元将不会被处理，因此不要依赖任何副作用。

**官方示例：**

```cpp
     QLoggingCategory category("driver.usb");
     qCWarning(category, "a warning message logged into category %s", category.categoryName());
```

### `CategoryFilter`

**作用与语义：**

这是指向函数签名如下的指针的类型def：
带有该签名的函数可以用`installFilter()`安装。

**官方示例：**

```cpp
 void myCategoryFilter(QLoggingCategory *);
```

## 6. 深入实践与常见坑

### 生命周期和资源边界

日志上下文通常是一次消息表达式的临时对象；自定义 message handler 的安装和卸载要覆盖整个使用期，处理器内部不要递归调用会再次触发日志的代码。

### 状态和错误边界

日志是否输出受级别、类别规则、编译宏和运行时过滤影响。看到某条消息缺失时，要区分代码没有执行、日志级别被过滤、上下文被关闭和 handler 改写输出。

### 线程边界

日志可能来自多个线程，handler 必须考虑并发、输出原子性和不能阻塞业务线程；不要在 handler 中访问未加锁的 GUI 控件。

### 最容易出现的错误

不要用 qFatal 代替普通错误处理；不要在 handler 里再次触发同类日志；不要把日志文本当作稳定的程序接口；注意 release 构建中的上下文宏和过滤规则。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QLoggingCategory` 所属机制类型：Qt 日志与诊断机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
