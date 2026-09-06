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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 35 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QMessageLogger::CategoryFunction`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMessageLogger` 的配置属性。初始化或状态切换时通过 `setCategoryFunction(...)` 设置，之后用 `CategoryFunction()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:CategoryFunction`。
- 属性名：`QMessageLogger`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] QMessageLogger::QMessageLogger()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMessageLogger` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] QMessageLogger::QMessageLogger(const char *file, int line, const char *function)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMessageLogger` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `file`：类型为 `const char *`。没有默认值，调用时必须提供。文件或设备对象。要确认打开状态、读写模式、当前位置和错误状态。
- 参数 `line`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `function`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] QMessageLogger::QMessageLogger(const char *file, int line, const char *function, const char *category)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMessageLogger` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `file`：类型为 `const char *`。没有默认值，调用时必须提供。文件或设备对象。要确认打开状态、读写模式、当前位置和错误状态。
- 参数 `line`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `function`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `category`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug QMessageLogger::critical() const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::critical` 用于计算、查询或取得与“critical”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug QMessageLogger::critical(QMessageLogger::CategoryFunction catFunc) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::critical` 用于计算、查询或取得与“critical”相关的操作。调用时要先确认当前状态和 `catFunc` 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `catFunc`：类型为 `QMessageLogger::CategoryFunction`。没有默认值，调用时必须提供。传入 `QMessageLogger::CategoryFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug QMessageLogger::critical(const QLoggingCategory &cat) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::critical` 用于计算、查询或取得与“critical”相关的操作。调用时要先确认当前状态和 `cat` 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `cat`：类型为 `const QLoggingCategory &`。没有默认值，调用时必须提供。传入 `const QLoggingCategory &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageLogger::critical(const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::critical` 用于执行与“critical”相关的操作。调用时要先确认当前状态和 `msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageLogger::critical(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::critical` 用于执行与“critical”相关的操作。调用时要先确认当前状态和 `catFunc`、`msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `catFunc`：类型为 `QMessageLogger::CategoryFunction`。没有默认值，调用时必须提供。传入 `QMessageLogger::CategoryFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageLogger::critical(const QLoggingCategory &cat, const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::critical` 用于执行与“critical”相关的操作。调用时要先确认当前状态和 `cat`、`msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `cat`：类型为 `const QLoggingCategory &`。没有默认值，调用时必须提供。传入 `const QLoggingCategory &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug QMessageLogger::debug() const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::debug` 用于计算、查询或取得与“调试输出”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug QMessageLogger::debug(QMessageLogger::CategoryFunction catFunc) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::debug` 用于计算、查询或取得与“调试输出”相关的操作。调用时要先确认当前状态和 `catFunc` 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `catFunc`：类型为 `QMessageLogger::CategoryFunction`。没有默认值，调用时必须提供。传入 `QMessageLogger::CategoryFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug QMessageLogger::debug(const QLoggingCategory &cat) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::debug` 用于计算、查询或取得与“调试输出”相关的操作。调用时要先确认当前状态和 `cat` 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `cat`：类型为 `const QLoggingCategory &`。没有默认值，调用时必须提供。传入 `const QLoggingCategory &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageLogger::debug(const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::debug` 用于执行与“调试输出”相关的操作。调用时要先确认当前状态和 `msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageLogger::debug(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::debug` 用于执行与“调试输出”相关的操作。调用时要先确认当前状态和 `catFunc`、`msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `catFunc`：类型为 `QMessageLogger::CategoryFunction`。没有默认值，调用时必须提供。传入 `QMessageLogger::CategoryFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageLogger::debug(const QLoggingCategory &cat, const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::debug` 用于执行与“调试输出”相关的操作。调用时要先确认当前状态和 `cat`、`msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `cat`：类型为 `const QLoggingCategory &`。没有默认值，调用时必须提供。传入 `const QLoggingCategory &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QDebug QMessageLogger::fatal() const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::fatal` 用于计算、查询或取得与“fatal”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QDebug QMessageLogger::fatal(QMessageLogger::CategoryFunction catFunc) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::fatal` 用于计算、查询或取得与“fatal”相关的操作。调用时要先确认当前状态和 `catFunc` 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `catFunc`：类型为 `QMessageLogger::CategoryFunction`。没有默认值，调用时必须提供。传入 `QMessageLogger::CategoryFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QDebug QMessageLogger::fatal(const QLoggingCategory &cat) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::fatal` 用于计算、查询或取得与“fatal”相关的操作。调用时要先确认当前状态和 `cat` 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `cat`：类型为 `const QLoggingCategory &`。没有默认值，调用时必须提供。传入 `const QLoggingCategory &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QMessageLogger::fatal(const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::fatal` 用于执行与“fatal”相关的操作。调用时要先确认当前状态和 `msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.5] void QMessageLogger::fatal(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::fatal` 用于执行与“fatal”相关的操作。调用时要先确认当前状态和 `catFunc`、`msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `catFunc`：类型为 `QMessageLogger::CategoryFunction`。没有默认值，调用时必须提供。传入 `QMessageLogger::CategoryFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.5] void QMessageLogger::fatal(const QLoggingCategory &cat, const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::fatal` 用于执行与“fatal”相关的操作。调用时要先确认当前状态和 `cat`、`msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `cat`：类型为 `const QLoggingCategory &`。没有默认值，调用时必须提供。传入 `const QLoggingCategory &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug QMessageLogger::info() const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::info` 用于计算、查询或取得与“info”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug QMessageLogger::info(QMessageLogger::CategoryFunction catFunc) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::info` 用于计算、查询或取得与“info”相关的操作。调用时要先确认当前状态和 `catFunc` 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `catFunc`：类型为 `QMessageLogger::CategoryFunction`。没有默认值，调用时必须提供。传入 `QMessageLogger::CategoryFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug QMessageLogger::info(const QLoggingCategory &cat) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::info` 用于计算、查询或取得与“info”相关的操作。调用时要先确认当前状态和 `cat` 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `cat`：类型为 `const QLoggingCategory &`。没有默认值，调用时必须提供。传入 `const QLoggingCategory &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageLogger::info(const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::info` 用于执行与“info”相关的操作。调用时要先确认当前状态和 `msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageLogger::info(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::info` 用于执行与“info”相关的操作。调用时要先确认当前状态和 `catFunc`、`msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `catFunc`：类型为 `QMessageLogger::CategoryFunction`。没有默认值，调用时必须提供。传入 `QMessageLogger::CategoryFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageLogger::info(const QLoggingCategory &cat, const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::info` 用于执行与“info”相关的操作。调用时要先确认当前状态和 `cat`、`msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `cat`：类型为 `const QLoggingCategory &`。没有默认值，调用时必须提供。传入 `const QLoggingCategory &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug QMessageLogger::warning() const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::warning` 用于计算、查询或取得与“warning”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug QMessageLogger::warning(QMessageLogger::CategoryFunction catFunc) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::warning` 用于计算、查询或取得与“warning”相关的操作。调用时要先确认当前状态和 `catFunc` 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `catFunc`：类型为 `QMessageLogger::CategoryFunction`。没有默认值，调用时必须提供。传入 `QMessageLogger::CategoryFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug QMessageLogger::warning(const QLoggingCategory &cat) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::warning` 用于计算、查询或取得与“warning”相关的操作。调用时要先确认当前状态和 `cat` 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `cat`：类型为 `const QLoggingCategory &`。没有默认值，调用时必须提供。传入 `const QLoggingCategory &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageLogger::warning(const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::warning` 用于执行与“warning”相关的操作。调用时要先确认当前状态和 `msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageLogger::warning(QMessageLogger::CategoryFunction catFunc, const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::warning` 用于执行与“warning”相关的操作。调用时要先确认当前状态和 `catFunc`、`msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `catFunc`：类型为 `QMessageLogger::CategoryFunction`。没有默认值，调用时必须提供。传入 `QMessageLogger::CategoryFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageLogger::warning(const QLoggingCategory &cat, const char *msg, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageLogger::warning` 用于执行与“warning”相关的操作。调用时要先确认当前状态和 `cat`、`msg`、`...` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `cat`：类型为 `const QLoggingCategory &`。没有默认值，调用时必须提供。传入 `const QLoggingCategory &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `msg`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `CategoryFunction`

**API 类别：** 公有类型

**中文解读：** 这是 `QMessageLogger` 的 `类别、Function` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
