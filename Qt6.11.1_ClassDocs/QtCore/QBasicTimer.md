# QBasicTimer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Basic定时器”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QBasicTimer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QBasicTimer>`
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

### 公有类型

- `Duration`

### 公有函数

- `QBasicTimer()`
- `QBasicTimer(QBasicTimer &&other)`
- `~QBasicTimer()`
- `(since 6.8) Qt::TimerId id() const`
- `bool isActive() const`
- `(since 6.5) void start(QBasicTimer::Duration duration, QObject *object)`
- `(since 6.5) void start(QBasicTimer::Duration duration, Qt::TimerType timerType, QObject *obj)`
- `void stop()`
- `void swap(QBasicTimer &other)`
- `QBasicTimer & operator=(QBasicTimer &&other)`

### 相关非成员函数

- `void swap(QBasicTimer &lhs, QBasicTimer &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QBasicTimer::Duration`

**作用与语义：**

这是该类API中使用的`std::chrono::duration`类型。该类型存在的目的是促进向更高或更低粒度的可能过渡。
在所有现有站台中，它都被`nanoseconds`。

### `[constexpr noexcept] QBasicTimer::QBasicTimer()`

**作用与语义：**

构建一个基本的计时器。

### `[noexcept] QBasicTimer::QBasicTimer(QBasicTimer &&other)`

**作用与语义：**

Move-构造一个基本计时器，`other`留`inactive`。

### `[noexcept] QBasicTimer::~QBasicTimer()`

**作用与语义：**

会破坏基本计时器。

### `[noexcept, since 6.8] Qt::TimerId QBasicTimer::id() const`

**作用与语义：**

返回计时器的ID。

### `[noexcept] bool QBasicTimer::isActive() const`

**作用与语义：**

如果计时器正在运行且未被停止，则返回`true`;否则返回`false`。

### `[since 6.5] void QBasicTimer::start(QBasicTimer::Duration duration, QObject *object)`

**作用与语义：**

用`duration`超时启动（或重启）计时器。计时器将是`Qt::CoarseTimer`。有关不同定时器类型的信息请参见`Qt::TimerType`。
给定`object`会收到计时事件。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。
注意：从Qt 6.9开始，该方法使用标准：：chrono：：纳秒，之前则采用标准：：chrono：：毫秒。此更改向后兼容。

### `[since 6.5] void QBasicTimer::start(QBasicTimer::Duration duration, Qt::TimerType timerType, QObject *obj)`

**作用与语义：**

以`duration`超时和给定`timerType`启动（或重启）计时器。有关不同计时器类型的信息请参见`Qt::TimerType`。
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。
`obj`会收到计时事件。
注意：从Qt 6.9开始，该方法使用标准：：chrono：：纳秒，之前则采用标准：：chrono：：毫秒。此更改向后兼容。

### `void QBasicTimer::stop()`

**作用与语义：**

停止计时器。

### `[noexcept] void QBasicTimer::swap(QBasicTimer &other)`

**作用与语义：**

将计时器与`other`交换。这个操作非常快，从未失败过。

### `[noexcept] QBasicTimer &QBasicTimer::operator=(QBasicTimer &&other)`

**作用与语义：**

移动为该基本计时器分配`other`。之前由该基本计时器表示的计时器被停止。`other`保持为`inactive`。

### `[noexcept] void swap(QBasicTimer &lhs, QBasicTimer &rhs)`

**作用与语义：**

将计时器`lhs`与`rhs`交换。此操作非常快速且从未失败。

### `Duration`

**作用与语义：**

这是该类API中使用的`std::chrono::duration`类型。该类型存在的目的是促进向更高或更低粒度的可能过渡。
在所有现有站台中，它都被`nanoseconds`。

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

`QBasicTimer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
