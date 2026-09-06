# QStringMatcher

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“StringMatcher”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QStringMatcher` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QStringMatcher>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QStringMatcher()`
- `QStringMatcher(QStringView pattern, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QStringMatcher(const QString &pattern, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QStringMatcher(const QChar *uc, qsizetype length, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QStringMatcher(const QStringMatcher &other)`
- `~QStringMatcher()`
- `Qt::CaseSensitivity caseSensitivity() const`
- `qsizetype indexIn(QStringView str, qsizetype from = 0) const`
- `qsizetype indexIn(const QString &str, qsizetype from = 0) const`
- `qsizetype indexIn(const QChar *str, qsizetype length, qsizetype from = 0) const`
- `QString pattern() const`
- `(since 6.7) QStringView patternView() const`
- `void setCaseSensitivity(Qt::CaseSensitivity cs)`
- `void setPattern(const QString &pattern)`
- `QStringMatcher & operator=(const QStringMatcher &other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QStringMatcher::QStringMatcher()`

**作用与语义：**

构造一个空字符串匹配器，但不会匹配任何东西。调用`setPattern()`给它匹配的模式。

### `QStringMatcher::QStringMatcher(QStringView pattern, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

构建一个字符串匹配器，它将搜索 `pattern`，区分大小写 `cs`。
调用 `indexIn()` 执行搜索。

### `[explicit] QStringMatcher::QStringMatcher(const QString &pattern, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

构建一个字符串匹配器，它将搜索 `pattern`，区分大小写 `cs`。
调用 `indexIn()` 执行搜索。

### `QStringMatcher::QStringMatcher(const QChar *uc, qsizetype length, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

构建字符串匹配器，将以`cs`指定的`length`和大小写敏感性搜索`uc`所指的模式。

### `QStringMatcher::QStringMatcher(const QStringMatcher &other)`

**作用与语义：**

将`other`字符串匹配器复制到该字符串匹配器上。

### `[noexcept] QStringMatcher::~QStringMatcher()`

**作用与语义：**

摧毁了匹配绳。

### `Qt::CaseSensitivity QStringMatcher::caseSensitivity() const`

**作用与语义：**

返回该字符串匹配器的大小写敏感度设置。

### `qsizetype QStringMatcher::indexIn(QStringView str, qsizetype from = 0) const`

**作用与语义：**

从字符位置`from`（默认0，即从第一个字符开始）搜索字符串`str`，寻找构造函数中设置的字符串`pattern()`或最近一次调用中的`setPattern()`。返回`str`中匹配`pattern()`的位置，若未匹配则返回-1。

### `qsizetype QStringMatcher::indexIn(const QString &str, qsizetype from = 0) const`

**作用与语义：**

从字符位置`from`（默认0，即从第一个字符开始）搜索字符串`str`，寻找构造函数中设置的字符串`pattern()`或最近一次调用中的`setPattern()`。返回`str`中匹配`pattern()`的位置，若未匹配则返回-1。

### `qsizetype QStringMatcher::indexIn(const QChar *str, qsizetype length, qsizetype from = 0) const`

**作用与语义：**

从字符位置`from`（默认0，即从第一个字符开始）从长度`str`（长度为`length`）开始的字符串中搜索，寻找构造函数中或最近调用`setPattern()`中设置的字符串`pattern()`。返回`str`中`pattern()`匹配的位置，若未匹配则返回-1。

### `QString QStringMatcher::pattern() const`

**作用与语义：**

返回该字符串匹配器将搜索的字符串模式。

### `[noexcept, since 6.7] QStringView QStringMatcher::patternView() const`

**作用与语义：**

返回该字符串匹配器将搜索的模式的字符串视图。

### `void QStringMatcher::setCaseSensitivity(Qt::CaseSensitivity cs)`

**作用与语义：**

将字符串匹配器的大小写敏感度设置设置为`cs`。

### `void QStringMatcher::setPattern(const QString &pattern)`

**作用与语义：**

将该字符串匹配器将要搜索的字符串设置为`pattern`。

### `QStringMatcher &QStringMatcher::operator=(const QStringMatcher &other)`

**作用与语义：**

将`other`字符串匹配器分配给该字符串匹配器。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QStringMatcher` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
