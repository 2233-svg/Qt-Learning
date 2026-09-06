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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 12 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[explicit] QSemaphore::QSemaphore(int n = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSemaphore` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `n`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QSemaphore::~QSemaphore()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSemaphore` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSemaphore::acquire(int n = 1)`

**API 类别：** 成员函数说明

**中文解读：** `QSemaphore::acquire` 用于执行与“acquire”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSemaphore::available() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `available`，返回 `QSemaphore` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSemaphore::release(int n = 1)`

**API 类别：** 成员函数说明

**中文解读：** `QSemaphore::release` 用于执行与“释放”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSemaphore::tryAcquire(int n = 1)`

**API 类别：** 成员函数说明

**中文解读：** `QSemaphore::tryAcquire` 用于计算、查询或取得与“try、Acquire”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `n`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] bool QSemaphore::tryAcquire(int n, QDeadlineTimer timer)`

**API 类别：** 成员函数说明

**中文解读：** `QSemaphore::tryAcquire` 用于计算、查询或取得与“try、Acquire”相关的操作。调用时要先确认当前状态和 `n`、`timer` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `n`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `timer`：类型为 `QDeadlineTimer`。没有默认值，调用时必须提供。传入 `QDeadlineTimer` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSemaphore::tryAcquire(int n, int timeout)`

**API 类别：** 成员函数说明

**中文解读：** `QSemaphore::tryAcquire` 用于计算、查询或取得与“try、Acquire”相关的操作。调用时要先确认当前状态和 `n`、`timeout` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `n`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `timeout`：类型为 `int`。没有默认值，调用时必须提供。超时时间或超时对象，可能表示等待时长，也可能表示 QNetworkReply/QTimer 等异步对象，不能只看名称判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] template <typename Rep, typename Period> bool QSemaphore::tryAcquire(int n, std::chrono::duration<Rep, Period> timeout)`

**API 类别：** 成员函数说明

**中文解读：** `QSemaphore::tryAcquire` 用于计算、查询或取得与“try、Acquire”相关的操作。调用时要先确认当前状态和 `n`、`timeout` 的有效范围；返回类型是 `template <typename Rep, typename Period> bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Rep, typename Period> bool`。
- 参数 `n`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `timeout`：类型为 `std::chrono::duration<Rep, Period>`。没有默认值，调用时必须提供。超时时间或超时对象，可能表示等待时长，也可能表示 QNetworkReply/QTimer 等异步对象，不能只看名称判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.3] bool QSemaphore::try_acquire()`

**API 类别：** 成员函数说明

**中文解读：** `QSemaphore::try_acquire` 用于计算、查询或取得与“try、acquire”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] template <typename Rep, typename Period> bool QSemaphore::try_acquire_for(const std::chrono::duration<Rep, Period> &timeout)`

**API 类别：** 成员函数说明

**中文解读：** `QSemaphore::try_acquire_for` 用于计算、查询或取得与“try、acquire、for”相关的操作。调用时要先确认当前状态和 `timeout` 的有效范围；返回类型是 `template <typename Rep, typename Period> bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Rep, typename Period> bool`。
- 参数 `timeout`：类型为 `const std::chrono::duration<Rep, Period> &`。没有默认值，调用时必须提供。超时时间或超时对象，可能表示等待时长，也可能表示 QNetworkReply/QTimer 等异步对象，不能只看名称判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] template <typename Clock, typename Duration> bool QSemaphore::try_acquire_until(const std::chrono::time_point<Clock, Duration> &tp)`

**API 类别：** 成员函数说明

**中文解读：** `QSemaphore::try_acquire_until` 用于计算、查询或取得与“try、acquire、until”相关的操作。调用时要先确认当前状态和 `tp` 的有效范围；返回类型是 `template <typename Clock, typename Duration> bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Clock, typename Duration> bool`。
- 参数 `tp`：类型为 `const std::chrono::time_point<Clock, Duration> &`。没有默认值，调用时必须提供。传入 `const std::chrono::time_point<Clock, Duration> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
