# QWaitCondition

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 等待条件，用于让线程在条件不满足时休眠，并由其他线程唤醒。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QWaitCondition`：等待条件，用于让线程在条件不满足时休眠，并由其他线程唤醒。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QWaitCondition>`
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

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QWaitCondition()`
- `~QWaitCondition()`
- `void notify_all()`
- `void notify_one()`
- `bool wait(QMutex *lockedMutex, QDeadlineTimer deadline = QDeadlineTimer(QDeadlineTimer::Forever))`
- `bool wait(QReadWriteLock *lockedReadWriteLock, QDeadlineTimer deadline = QDeadlineTimer(QDeadlineTimer::Forever))`
- `bool wait(QMutex *lockedMutex, unsigned long time)`
- `bool wait(QReadWriteLock *lockedReadWriteLock, unsigned long time)`
- `void wakeAll()`
- `void wakeOne()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QWaitCondition::QWaitCondition()`

**作用与语义：**

构建一个新的等待条件对象。

### `[noexcept] QWaitCondition::~QWaitCondition()`

**作用与语义：**

会破坏等待条件对象。

### `void QWaitCondition::notify_all()`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于`wakeAll()`。

### `void QWaitCondition::notify_one()`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于`wakeOne()`。

### `bool QWaitCondition::wait(QMutex *lockedMutex, QDeadlineTimer deadline = QDeadlineTimer(QDeadlineTimer::Forever))`

**作用与语义：**

释放`lockedMutex`并在等待条件下等待。调用线程必须先锁定`lockedMutex`。如果`lockedMutex`未处于锁定状态，行为未定义。如果`lockedMutex`是递归互斥组，该函数立即返回。`lockedMutex`将被解锁，调用线程会阻塞，直到满足以下任一条件：
- 另一线程用`wakeOne()`或`wakeAll()`来表示信号。此时该函数返回为真。
- 达到`deadline`给出的截止时间。如果`deadline`是`QDeadlineTimer::Forever`（默认），则等待永远不会超时（事件必须被通知）。如果等待超时，该函数将返回false。
`lockedMutex`会返回到相同的锁定状态。该函数旨在实现从锁定状态到等待状态的原子级转换。

### `bool QWaitCondition::wait(QReadWriteLock *lockedReadWriteLock, QDeadlineTimer deadline = QDeadlineTimer(QDeadlineTimer::Forever))`

**作用与语义：**

释放`lockedReadWriteLock`并在等待条件下等待。`lockedReadWriteLock`必须被调用线程最初锁定。如果`lockedReadWriteLock`未处于锁定状态，该函数立即返回。`lockedReadWriteLock`不能递归锁定，否则该函数无法正确释放锁。`lockedReadWriteLock`将被解锁，调用线程会阻塞，直到满足以下任一条件：
- 另一线程通过`wakeOne()`或`wakeAll()`来发信号。此时该函数返回为真。
- 达到`deadline`给出的截止时间。如果`deadline`是`QDeadlineTimer::Forever`（默认），则等待永远不会超时（事件必须被通知）。如果等待超时，该函数将返回false。
`lockedReadWriteLock`将返回相同的锁定状态。该函数旨在实现从锁定状态向等待状态的原子转换。

### `bool QWaitCondition::wait(QMutex *lockedMutex, unsigned long time)`

**作用与语义：**

释放`lockedMutex`，等待状态持续`time`毫秒。

### `bool QWaitCondition::wait(QReadWriteLock *lockedReadWriteLock, unsigned long time)`

**作用与语义：**

释放`lockedReadWriteLock`，并在等待状态下等待`time`毫秒。

### `void QWaitCondition::wakeAll()`

**作用与语义：**

唤醒所有等待等待条件的线程。线程被唤醒的顺序取决于操作系统的调度策略，无法控制或预测。

### `void QWaitCondition::wakeOne()`

**作用与语义：**

唤醒一个等待条件的线程。被唤醒的线程取决于操作系统的调度策略，无法控制或预测。
如果你想唤醒某个特定线程，通常的解决办法是使用不同的等待条件，让不同的线程在不同条件下等待。

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

`QWaitCondition` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
