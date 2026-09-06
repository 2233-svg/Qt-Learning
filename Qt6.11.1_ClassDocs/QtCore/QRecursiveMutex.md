# QRecursiveMutex

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QRecursiveMutex` 是并发执行或同步类型，负责任务、线程、future、promise 或共享资源的协调。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QRecursiveMutex` 是并发模块中的类型，用于组织线程执行、同步或资源访问。

**内部模型：** 并发正确性来自所有权、共享数据、同步边界和退出协议的组合，而不是仅仅“开一个线程”。先定义谁读写数据，再决定 queued connection、mutex、future 或线程池。

**适用场景：** 后台任务、阻塞 I/O、并行计算或多个执行上下文共享资源时使用。

**典型调用链：** 划分任务和数据 -> 选择线程/线程池/future -> 明确同步和取消 -> 连接完成/错误 -> 等待安全退出。

**先记住的坑：** 避免 GUI 线程阻塞等待；锁顺序要稳定；线程结束前不能释放它使用的对象；queued slot 需要目标线程事件循环。

## 2. 依赖与对象关系

- 头文件：`#include <QRecursiveMutex>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

并发正确性来自所有权、共享数据、同步边界和退出协议的组合，而不是仅仅“开一个线程”。先定义谁读写数据，再决定 queued connection、mutex、future 或线程池。

### 状态、生命周期和线程

**生命周期：** 任务必须有明确的开始、完成、取消和销毁路径。线程退出前先停止接受新任务，等待 worker 安全结束，再释放线程依赖；对象的线程归属和 QThread 对象本身所在的线程不能混为一谈。

**状态与结果：** 区分任务未开始、运行中、暂停、取消请求、已取消、失败和成功。发出取消请求不代表任务已经停止，资源释放要等任务确认结束；Future 的完成也不一定表示业务结果有效。

**线程与事件循环：** GUI 线程只负责启动任务、接收结果和更新界面；共享数据要么转移所有权，要么用锁/原子/消息传递保护。queued slot 需要目标线程事件循环，阻塞 worker 则不能依赖它接收 queued 控制命令。

## 3. 直接使用

后台任务、阻塞 I/O、并行计算或多个执行上下文共享资源时使用。 使用时通常按这个过程组织：划分任务和数据 -> 选择线程/线程池/future -> 明确同步和取消 -> 连接完成/错误 -> 等待安全退出。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QRecursiveMutex()`
- `~QRecursiveMutex()`
- `void lock()`
- `(since 6.6) bool tryLock(QDeadlineTimer timeout = {})`
- `bool tryLock(int timeout)`
- `bool try_lock()`
- `bool try_lock_for(std::chrono::duration<Rep, Period> duration)`
- `bool try_lock_until(std::chrono::time_point<Clock, Duration> timePoint)`
- `void unlock()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QRecursiveMutex::QRecursiveMutex()`

**作用与语义：**

构造一个新的递归互斥体。该互斥体是在解锁状态下创建的。

### `[noexcept] QRecursiveMutex::~QRecursiveMutex()`

**作用与语义：**

破坏了互斥系统。
警告：销毁锁定的互斥体可能导致行为不明确。

### `[noexcept(...)] void QRecursiveMutex::lock()`

**作用与语义：**

锁定了互斥体。如果其他线程锁定了该互斥体，则该调用会阻塞，直到该线程解锁它。
允许在同一线程的同一互斥体上多次调用该函数。
注意：该功能仅在`LockIsNoexcept`为`true`时使用。

### `[noexcept(...), since 6.6] bool QRecursiveMutex::tryLock(QDeadlineTimer timeout = {})`

**作用与语义：**

尝试锁定互斥体。如果锁定成功，该函数返回`true`;否则返回`false`。如果其他线程锁定了互斥体，该函数会等待`timeout`到期后，直到互斥体可用。
如果锁定成功，必须用`unlock()`解锁互斥组，其他线程才能成功锁定它。
允许在同一线程的同一互斥体上多次调用该函数。
注意：该功能仅在`LockIsNoexcept` `true`时使用。

### `[noexcept(...)] bool QRecursiveMutex::tryLock(int timeout)`

**作用与语义：**

尝试锁定互斥组。如果锁定成功，该函数返回`true`;否则返回`false`。如果其他线程锁定了互斥组，该函数最多等待`timeout`毫秒，直到该互斥组可用。
注意：将负数传递为`timeout`等同于调用`lock()`，即该函数将永远等待，直到`timeout`为负时互斥候选被锁定。
如果锁定成功，必须用`unlock()`解锁互斥线，其他线程才能成功锁定。
允许在同一线程的同一互斥体上多次调用该函数。
注意：该功能仅在`LockIsNoexcept` `true`时使用。

### `[noexcept(...)] bool QRecursiveMutex::try_lock()`

**作用与语义：**

尝试锁定静止子。如果锁定成功，该函数返回`true`;否则返回`false`。
该功能是为了兼容标准库概念`Lockable`而提供。它等同于`tryLock()`。
注意：该功能仅在`LockIsNoexcept` `true`时使用。

### `template <typename Rep, typename Period> bool QRecursiveMutex::try_lock_for(std::chrono::duration<Rep, Period> duration)`

**作用与语义：**

尝试锁定静止面。如果锁定成功，该函数返回`true`;否则返回`false`。如果其他线程锁定了互斥体，该函数将至少等待`duration`以等待互斥体可用。
注意：将负时长传递为`duration`等同于调用`try_lock()`。这种行为与`tryLock()`不同。
如果锁被获得，必须用`unlock()`解锁互斥体，其他线程才能成功锁定它。
允许在同一线程的同一互斥体上多次调用该函数。

### `template <typename Clock, typename Duration> bool QRecursiveMutex::try_lock_until(std::chrono::time_point<Clock, Duration> timePoint)`

**作用与语义：**

尝试锁定该互斥体。如果锁定成功，该函数返回`true`;否则返回`false`。如果其他线程锁定了互斥体，该函数至少会等待`timePoint`，直到该互斥体可用。
注意：传递已通过的`timePoint`等同于调用`try_lock()`。这种行为与`tryLock()`不同。
如果锁定成功，必须用`unlock()`解锁，其他线程才能成功锁定该锁。
允许在同一线程的同一互斥体上多次调用该函数。

### `[noexcept] void QRecursiveMutex::unlock()`

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

避免 GUI 线程阻塞等待；锁顺序要稳定；线程结束前不能释放它使用的对象；queued slot 需要目标线程事件循环。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QRecursiveMutex` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
