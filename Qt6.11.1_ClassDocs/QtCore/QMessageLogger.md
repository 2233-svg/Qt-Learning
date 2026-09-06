# QMessageLogger

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QMessageLogger` 是 Qt 日志与诊断体系中的类型，用于按类别输出调试、信息、警告或错误消息。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMessageLogger` 是 Qt 日志与诊断机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 日志 API 把消息级别、类别、源文件/行号上下文和最终处理器分开。`qDebug`、`qInfo`、`qWarning`、`qCritical` 负责产生消息，分类规则和 message handler 决定输出到哪里、是否过滤或持久化。

**适用场景：** 用分类定义稳定的日志边界，使用合适级别记录状态和错误，必要时安装 handler 写入文件或诊断系统；敏感信息、token、密码不要输出。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要用 qFatal 代替普通错误处理；不要在 handler 里再次触发同类日志；不要把日志文本当作稳定的程序接口；注意 release 构建中的上下文宏和过滤规则。

## 2. 依赖与对象关系

- 头文件：`#include <QMessageLogger>`
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

- `CategoryFunction`

### 公有函数

- `QMessageLogger()`
- `QMessageLogger(const char *file, int line, const char *function)`
- `QMessageLogger(const char *file, int line, const char *function, const char *category)`
- `QDebug critical() const`
- `QDebug critical(QMessageLogger::CategoryFunction catFunc) const`
- `QDebug critical(const QLoggingCategory &cat) const`
- `void critical(const char *msg, ...) const`
- `void critical(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`
- `void critical(const QLoggingCategory &cat, const char *msg, ...) const`
- `QDebug debug() const`
- `QDebug debug(QMessageLogger::CategoryFunction catFunc) const`
- `QDebug debug(const QLoggingCategory &cat) const`
- `void debug(const char *msg, ...) const`
- `void debug(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`
- `void debug(const QLoggingCategory &cat, const char *msg, ...) const`
- `(since 6.5) QDebug fatal() const`
- `(since 6.5) QDebug fatal(QMessageLogger::CategoryFunction catFunc) const`
- `(since 6.5) QDebug fatal(const QLoggingCategory &cat) const`
- `void fatal(const char *msg, ...) const`
- `(since 6.5) void fatal(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`
- `(since 6.5) void fatal(const QLoggingCategory &cat, const char *msg, ...) const`
- `QDebug info() const`
- `QDebug info(QMessageLogger::CategoryFunction catFunc) const`
- `QDebug info(const QLoggingCategory &cat) const`
- `void info(const char *msg, ...) const`
- `void info(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`
- `void info(const QLoggingCategory &cat, const char *msg, ...) const`
- `QDebug warning() const`
- `QDebug warning(QMessageLogger::CategoryFunction catFunc) const`
- `QDebug warning(const QLoggingCategory &cat) const`
- `void warning(const char *msg, ...) const`
- `void warning(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`
- `void warning(const QLoggingCategory &cat, const char *msg, ...) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QMessageLogger::CategoryFunction`

**作用与语义：**

这是指向函数签名如下的指针的类型def：
`Q_DECLARE_LOGGING_CATEGORY`宏生成带有该签名的函数声明，`Q_LOGGING_CATEGORY`生成其定义。

**官方示例：**

```cpp
     const QLoggingCategory &category();
```

### `[constexpr] QMessageLogger::QMessageLogger()`

**作用与语义：**

构建默认的 QMessageLogger。请参见其他构造函数以指定上下文信息。

### `[constexpr] QMessageLogger::QMessageLogger(const char *file, int line, const char *function)`

**作用与语义：**

构建一个QMessageLogger，用于记录在`function`中 `line` `file`的日志消息。它等同于 QMessageLogger（文件、行、函数，“默认”）。

### `[constexpr] QMessageLogger::QMessageLogger(const char *file, int line, const char *function, const char *category)`

**作用与语义：**

构建一个QMessageLogger，用于记录`category`消息，用于`function`中`line`的`file`。

### `QDebug QMessageLogger::critical() const`

**作用与语义：**

使用`QDebug`流记录关键消息。

### `QDebug QMessageLogger::critical(QMessageLogger::CategoryFunction catFunc) const`

**作用与语义：**

将`catFunc`通过`QDebug`流返回的关键消息记录为类别。

### `QDebug QMessageLogger::critical(const QLoggingCategory &cat) const`

**作用与语义：**

通过`QDebug`流将关键消息`cat`分类记录。

### `void QMessageLogger::critical(const char *msg, ...) const`

**作用与语义：**

记录格式`msg`指定的关键消息。可以使用`msg`指定的额外参数。

### `void QMessageLogger::critical(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`

**作用与语义：**

记录一个关键消息，格式为`msg`指定，以符合`catFunc`返回的上下文。可以使用`msg`指定的其他参数。

### `void QMessageLogger::critical(const QLoggingCategory &cat, const char *msg, ...) const`

**作用与语义：**

记录上下文`cat`格式`msg`指定的关键消息。可以使用`msg`指定的其他参数。

### `QDebug QMessageLogger::debug() const`

**作用与语义：**

使用 `QDebug` 流记录调试消息。

### `QDebug QMessageLogger::debug(QMessageLogger::CategoryFunction catFunc) const`

**作用与语义：**

将`catFunc`通过`QDebug`流返回的调试消息记录到类别中。

### `QDebug QMessageLogger::debug(const QLoggingCategory &cat) const`

**作用与语义：**

使用`QDebug`流将调试消息记录到类别`cat`。

### `void QMessageLogger::debug(const char *msg, ...) const`

**作用与语义：**

日志一个格式`msg`指定的调试消息。可以使用`msg`指定的额外参数。

### `void QMessageLogger::debug(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`

**作用与语义：**

日志一个以格式`msg`指定的调试消息，以符合`catFunc`返回的上下文。还可以使用`msg`指定的其他参数。

### `void QMessageLogger::debug(const QLoggingCategory &cat, const char *msg, ...) const`

**作用与语义：**

日志一个以上下文`cat`格式`msg`指定的调试消息。可以使用`msg`指定的其他参数。

### `[since 6.5] QDebug QMessageLogger::fatal() const`

**作用与语义：**

使用`QDebug`流记录致命消息。

### `[since 6.5] QDebug QMessageLogger::fatal(QMessageLogger::CategoryFunction catFunc) const`

**作用与语义：**

将`catFunc`通过`QDebug`流返回的致命消息记录到类别。

### `[since 6.5] QDebug QMessageLogger::fatal(const QLoggingCategory &cat) const`

**作用与语义：**

使用`QDebug`流`cat`将致命消息记录到类别中。

### `[noexcept] void QMessageLogger::fatal(const char *msg, ...) const`

**作用与语义：**

记录格式`msg`指定的致命消息。可以使用`msg`指定的额外参数。

### `[noexcept, since 6.5] void QMessageLogger::fatal(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`

**作用与语义：**

记录一个致命消息，格式为`msg`指定，以符合`catFunc`返回的上下文。还可以使用`msg`指定的其他参数。

### `[noexcept, since 6.5] void QMessageLogger::fatal(const QLoggingCategory &cat, const char *msg, ...) const`

**作用与语义：**

记录上下文`cat`格式`msg`指定的致命消息。可以使用`msg`指定的额外参数。

### `QDebug QMessageLogger::info() const`

**作用与语义：**

通过`QDebug`流记录信息消息。

### `QDebug QMessageLogger::info(QMessageLogger::CategoryFunction catFunc) const`

**作用与语义：**

通过`QDebug`流将`catFunc`返回的信息消息归类。

### `QDebug QMessageLogger::info(const QLoggingCategory &cat) const`

**作用与语义：**

使用`QDebug`流`cat`将信息信息记录到类别中。

### `void QMessageLogger::info(const char *msg, ...) const`

**作用与语义：**

日志中以格式`msg`指定的信息信息。还可以使用`msg`指定的额外参数。

### `void QMessageLogger::info(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`

**作用与语义：**

记录一个以格式`msg`指定的信息消息，以符合`catFunc`返回的上下文。可以使用`msg`指定的额外参数。

### `void QMessageLogger::info(const QLoggingCategory &cat, const char *msg, ...) const`

**作用与语义：**

记录上下文`cat`格式`msg`指定的信息消息。可以使用`msg`指定的额外参数。

### `QDebug QMessageLogger::warning() const`

**作用与语义：**

使用`QDebug`流记录警告信息。

### `QDebug QMessageLogger::warning(QMessageLogger::CategoryFunction catFunc) const`

**作用与语义：**

将警告消息记录到`catFunc`使用`QDebug`流返回的类别。

### `QDebug QMessageLogger::warning(const QLoggingCategory &cat) const`

**作用与语义：**

使用`QDebug`流将警告消息记录到类别`cat`。

### `void QMessageLogger::warning(const char *msg, ...) const`

**作用与语义：**

记录格式`msg`指定的警告消息。可以使用`msg`指定的额外参数。

### `void QMessageLogger::warning(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`

**作用与语义：**

记录一个带有格式`msg`的警告消息，以符合`catFunc`返回的上下文。还可以使用`msg`指定的额外参数。

### `void QMessageLogger::warning(const QLoggingCategory &cat, const char *msg, ...) const`

**作用与语义：**

记录上下文`cat`格式`msg`指定的警告消息。可以使用`msg`指定的额外参数。

### `CategoryFunction`

**作用与语义：**

这是指向函数签名如下的指针的类型def：
`Q_DECLARE_LOGGING_CATEGORY`宏生成带有该签名的函数声明，`Q_LOGGING_CATEGORY`生成其定义。

**官方示例：**

```cpp
     const QLoggingCategory &category();
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

`QMessageLogger` 所属机制类型：Qt 日志与诊断机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
