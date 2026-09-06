# QMutex

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 互斥锁，用于保护多个线程共享的临界区或共享状态。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMutex`：互斥锁，用于保护多个线程共享的临界区或共享状态。

**内部模型：** 并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

**适用场景：** 先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

## 2. 依赖与对象关系

- 头文件：`#include <QMutex>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

### 状态、生命周期和线程

**生命周期：** 任务必须有明确的开始、完成、取消和销毁路径。线程退出前先停止接受新任务，等待 worker 安全结束，再释放线程依赖；对象的线程归属和 QThread 对象本身所在的线程不能混为一谈。

**状态与结果：** 区分任务未开始、运行中、暂停、取消请求、已取消、失败和成功。发出取消请求不代表任务已经停止，资源释放要等任务确认结束；Future 的完成也不一定表示业务结果有效。

**线程与事件循环：** GUI 线程只负责启动任务、接收结果和更新界面；共享数据要么转移所有权，要么用锁/原子/消息传递保护。queued slot 需要目标线程事件循环，阻塞 worker 则不能依赖它接收 queued 控制命令。

## 3. 直接使用

先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QMutex()`
- `~QMutex()`
- `void lock()`
- `(since 6.6) bool tryLock(QDeadlineTimer timer)`
- `bool tryLock(int timeout)`
- `bool tryLock()`
- `bool try_lock()`
- `bool try_lock_for(std::chrono::duration<Rep, Period> duration)`
- `bool try_lock_until(std::chrono::time_point<Clock, Duration> timePoint)`
- `void unlock()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QMutex::QMutex()`

**作用与语义：**

构建一个新的互斥组。该互斥组是在解锁状态下创建的。

### `[noexcept] QMutex::~QMutex()`

**作用与语义：**

破坏了互斥系统。
警告：销毁锁定的互斥体可能导致行为不明确。

### `[noexcept(...)] void QMutex::lock()`

**作用与语义：**

锁定了互斥体。如果其他线程锁定了该互斥体，则该调用会阻塞，直到该线程解锁它。
如果当前线程已经锁定了互斥节，该调用将永远不会返回，导致死锁。
注意：该函数仅在`FutexAlwaysAvailable`为`true`时使用。

### `[noexcept(...), since 6.6] bool QMutex::tryLock(QDeadlineTimer timer)`

**作用与语义：**

尝试锁定互斥组。如果锁定成功，该函数返回`true`;否则返回`false`。如果其他线程锁定了该互斥组，该函数会等待`timer`到期后，直到该缺电节可用。
如果锁定成功，必须用`unlock()`解锁互斥线，其他线程才能成功锁定。
注意：该功能仅在`FutexAlwaysAvailable` `true`时才会生效。

### `[noexcept(...)] bool QMutex::tryLock(int timeout)`

**作用与语义：**

尝试锁定静止子。如果锁定成功，该函数返回`true`;否则返回`false`。如果其他线程锁定了静止子，该函数最多等待`timeout`毫秒，直到变音子可用。
注意：将负数传递为`timeout`等同于调用`lock()`，即该函数会一直等待，直到能够锁定互斥体，如果`timeout`为负。
如果锁定成功，必须用`unlock()`解锁互斥体，其他线程才能成功锁定。
注意：该功能仅在`FutexAlwaysAvailable`为`true`时使用。

### `[noexcept] bool QMutex::tryLock()`

**作用与语义：**

尝试锁定互斥组。如果锁定成功，该函数返回`true`;否则返回`false`。
如果锁被获得，必须用`unlock()`解锁互斥体，其他线程才能成功锁定它。

### `[noexcept] bool QMutex::try_lock()`

**作用与语义：**

尝试锁定静止子。如果锁定成功，该函数返回`true`;否则返回`false`。
该功能是为了兼容标准库概念`Lockable`而提供。它等同于`tryLock()`。

### `template <typename Rep, typename Period> bool QMutex::try_lock_for(std::chrono::duration<Rep, Period> duration)`

**作用与语义：**

尝试锁定 mutex。如果锁定成功，该函数返回 `true`;否则返回 `false`。如果其他线程锁定了 mutex，该函数将至少等待 `duration` 以等待 mutex 可用。
注意：通过负时长作为`duration`等同于调用`try_lock()`。这种行为与`tryLock()`不同。
如果锁定成功，必须用`unlock()`解锁互斥线，其他线程才能成功锁定它。

### `template <typename Clock, typename Duration> bool QMutex::try_lock_until(std::chrono::time_point<Clock, Duration> timePoint)`

**作用与语义：**

尝试锁定互斥体。如果锁定成功，该函数返回`true`;否则返回`false`。如果其他线程锁定了互斥体，该函数至少会等待`timePoint`，直到互斥体可用。
注意：传递已通过的`timePoint`等同于调用`try_lock()`。这种行为与`tryLock()`不同。
如果锁定成功，必须用`unlock()`解锁该互斥体，其他线程才能成功锁定。

### `[noexcept] void QMutex::unlock()`

**作用与语义：**

解锁互斥体。尝试在与锁定该线程不同的线程中解锁互斥体会导致错误。解锁未锁定的互斥体则会导致行为不明确。

## 6. 深入实践与常见坑

### 生命周期和资源边界

任务必须有明确的开始、完成、取消和销毁路径。线程退出前先停止接受新任务，等待 worker 安全结束，再释放线程依赖；对象的线程归属和 QThread 对象本身所在的线程不能混为一谈。

### 状态和错误边界

区分任务未开始、运行中、暂停、取消请求、已取消、失败和成功。发出取消请求不代表任务已经停止，资源释放要等任务确认结束；Future 的完成也不一定表示业务结果有效。

### 线程边界

GUI 线程只负责启动任务、接收结果和更新界面；共享数据要么转移所有权，要么用锁/原子/消息传递保护。queued slot 需要目标线程事件循环，阻塞 worker 则不能依赖它接收 queued 控制命令。

### 最容易出现的错误

不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QMutex` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
