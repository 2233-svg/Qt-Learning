# QSemaphore

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 信号量，用于限制并发资源数量或在执行上下文之间计数同步。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSemaphore`：信号量，用于限制并发资源数量或在执行上下文之间计数同步。

**内部模型：** 并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

**适用场景：** 先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

## 2. 依赖与对象关系

- 头文件：`#include <QSemaphore>`
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

- `QSemaphore(int n = 0)`
- `~QSemaphore()`
- `void acquire(int n = 1)`
- `int available() const`
- `void release(int n = 1)`
- `bool tryAcquire(int n = 1)`
- `(since 6.6) bool tryAcquire(int n, QDeadlineTimer timer)`
- `bool tryAcquire(int n, int timeout)`
- `(since 6.3) bool tryAcquire(int n, std::chrono::duration<Rep, Period> timeout)`
- `(since 6.3) bool try_acquire()`
- `(since 6.3) bool try_acquire_for(const std::chrono::duration<Rep, Period> &timeout)`
- `(since 6.3) bool try_acquire_until(const std::chrono::time_point<Clock, Duration> &tp)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QSemaphore::QSemaphore(int n = 0)`

**作用与语义：**

创建新的信号量，并将它守护的资源数量初始化为`n`（默认为0）。

### `[noexcept] QSemaphore::~QSemaphore()`

**作用与语义：**

摧毁信号旗。
警告：销毁正在使用的信号量可能导致不明确的行为。

### `void QSemaphore::acquire(int n = 1)`

**作用与语义：**

尝试获取信号量保护的`n`资源。如果`n` > `available()`，该调用将被阻塞，直到资源充足。

### `int QSemaphore::available() const`

**作用与语义：**

返回当前可用资源数量。该数字永远不会为负。

### `void QSemaphore::release(int n = 1)`

**作用与语义：**

释放资源`n`由信号旗守护。
该函数也可以用来“创建”资源。例如：
`QSemaphoreReleaser` 是围绕该函数的 RAII 封装器。

**官方示例：**

```cpp
 QSemaphore sem(5);      // a semaphore that guards 5 resources
 sem.acquire(5);         // acquire all 5 resources
 sem.release(5);         // release the 5 resources
 sem.release(10);        // "create" 10 new resources
```

### `bool QSemaphore::tryAcquire(int n = 1)`

**作用与语义：**

尝试获取由信号板守护的`n`资源，成功后返回`true`。如果`available()` < `n`，该调用立即返回`false`，且不获得任何资源。

**官方示例：**

```cpp
 QSemaphore sem(5);      // sem.available() == 5
 sem.tryAcquire(250);    // sem.available() == 5, returns false
 sem.tryAcquire(3);      // sem.available() == 2, returns true
```

### `[since 6.6] bool QSemaphore::tryAcquire(int n, QDeadlineTimer timer)`

**作用与语义：**

试图获取由信号机守护的`n`资源，成功后返回`true`。如果`available()` < `n`，该调用将等待`timer`到期后资源开放。

**官方示例：**

```cpp
 QSemaphore sem(5);                          // sem.available() == 5
 sem.tryAcquire(250, QDeadlineTimer(1000));  // sem.available() == 5, waits 1000 milliseconds and returns false
 sem.tryAcquire(3, QDeadlineTimer(30s));     // sem.available() == 2, returns true without waiting
```

### `bool QSemaphore::tryAcquire(int n, int timeout)`

**作用与语义：**

尝试获取由信号量保护的`n`资源，成功后返回`true`。如果`available()` < `n`，该调用最多等待`timeout`毫秒以待资源可用。注意：将负数作为`timeout`等同于调用`acquire()`，即如果`timeout`为负，该函数将永远等待资源可用的时间。

**官方示例：**

```cpp
 QSemaphore sem(5);            // sem.available() == 5
 sem.tryAcquire(250, 1000);    // sem.available() == 5, waits 1000 milliseconds and returns false
 sem.tryAcquire(3, 30000);     // sem.available() == 2, returns true without waiting
```

### `[since 6.3] template <typename Rep, typename Period> bool QSemaphore::tryAcquire(int n, std::chrono::duration<Rep, Period> timeout)`

**作用与语义：**

尝试获取由信号板守护的`n`资源，成功后返回`true`。如果`available()` < `n`，该调用立即返回`false`，且不获得任何资源。

**官方示例：**

```cpp
 QSemaphore sem(5);      // sem.available() == 5
 sem.tryAcquire(250);    // sem.available() == 5, returns false
 sem.tryAcquire(3);      // sem.available() == 2, returns true
```

### `[noexcept, since 6.3] bool QSemaphore::try_acquire()`

**作用与语义：**

此功能是为了`std::counting_semaphore`兼容性而提供。
它等价于调用`tryAcquire(1)`，函数在成功获取资源后返回`true`。

### `[since 6.3] template <typename Rep, typename Period> bool QSemaphore::try_acquire_for(const std::chrono::duration<Rep, Period> &timeout)`

**作用与语义：**

此功能是为了`std::counting_semaphore`兼容性而提供。
它等价于调用`tryAcquire(1, timeout)`，即调用在给定的`timeout`值上超时。函数在成功获取资源后返回`true`。

### `[since 6.3] template <typename Clock, typename Duration> bool QSemaphore::try_acquire_until(const std::chrono::time_point<Clock, Duration> &tp)`

**作用与语义：**

此功能是为了`std::counting_semaphore`兼容性而提供。
它等同于调用`tryAcquire(1, tp - Clock::now())`，意味着记录`tp`（时间点），在等待时忽略对`Clock`的调整。函数在成功获取资源后返回`true`。

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

`QSemaphore` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
