# QMessageLogContext

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QMessageLogContext` 是 Qt 日志与诊断体系中的类型，用于按类别输出调试、信息、警告或错误消息。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMessageLogContext` 是 Qt 日志与诊断机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 日志 API 把消息级别、类别、源文件/行号上下文和最终处理器分开。`qDebug`、`qInfo`、`qWarning`、`qCritical` 负责产生消息，分类规则和 message handler 决定输出到哪里、是否过滤或持久化。

**适用场景：** 用分类定义稳定的日志边界，使用合适级别记录状态和错误，必要时安装 handler 写入文件或诊断系统；敏感信息、token、密码不要输出。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要用 qFatal 代替普通错误处理；不要在 handler 里再次触发同类日志；不要把日志文本当作稳定的程序接口；注意 release 构建中的上下文宏和过滤规则。

## 2. 依赖与对象关系

- 头文件：`#include <QMessageLogContext>`
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

### 配套与继承 API

- `QMessageLogContext::QMessageLogContext()`
- `QMessageLogContext::QMessageLogContext(const char *fileName, int lineNumber, const char *functionName, const char *categoryName)`
- `static constexpr int QMessageLogContext::CurrentVersion`
- `int QMessageLogContext::line`
- `const char *QMessageLogContext::file`
- `const char *QMessageLogContext::function`
- `const char *QMessageLogContext::category`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QMessageLogContext::QMessageLogContext()`

**作用与语义：**

构造空日志上下文：行号为 0，文件、函数和分类指针为 `nullptr`，版本字段设为 `CurrentVersion`。

### `QMessageLogContext::QMessageLogContext(const char *fileName, int lineNumber, const char *functionName, const char *categoryName)`

**作用与语义：**

用源码文件名、行号、函数名和日志分类构造一条日志上下文。它通常由 Qt 日志宏自动创建；四个字符串以指针保存而不复制，因此手工构造时必须保证它们在记录日志期间仍有效。

### `static constexpr int QMessageLogContext::CurrentVersion`

**作用与语义：**

当前日志上下文结构版本，Qt 6.11.1 中为 2。自定义消息处理器可用它判断哪些字段可安全读取。

### `int QMessageLogContext::line`

**作用与语义：**

产生日志调用的源码行号；无法取得位置信息时为 0。它与 `file` 和 `function` 一起用于定位日志来源。

### `const char *QMessageLogContext::file`

**作用与语义：**

产生日志调用的源码文件名指针；构建配置未保留上下文时可能为 `nullptr`，读取前应先判空。

### `const char *QMessageLogContext::function`

**作用与语义：**

产生日志调用的函数名指针；构建配置未保留上下文时可能为 `nullptr`，读取前应先判空。

### `const char *QMessageLogContext::category`

**作用与语义：**

该消息所属日志分类的名称指针；没有分类信息时可能为 `nullptr`，读取前应先判空。

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

`QMessageLogContext` 所属机制类型：Qt 日志与诊断机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
