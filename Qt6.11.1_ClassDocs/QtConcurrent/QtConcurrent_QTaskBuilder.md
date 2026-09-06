# QtConcurrent::QTaskBuilder

> Qt 6.11.1 · Qt Concurrent

## 1. 先建立直觉

**一句话定位：** `QtConcurrent::QTaskBuilder` 是并发执行或同步类型，负责任务、线程、future、promise 或共享资源的协调。

**模块背景：** Qt Concurrent 提供线程池、异步计算和 QFuture 相关并发抽象。

### 这是什么

`QtConcurrent::QTaskBuilder` 是 并发与任务机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

**适用场景：** 先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

## 2. 依赖与对象关系

- 头文件：`#include <QTaskBuilder>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Concurrent)
target_link_libraries(mytarget PRIVATE Qt6::Concurrent)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

### 状态、生命周期和线程

**生命周期：** 任务必须有明确的开始、完成、取消和销毁路径。线程退出前先停止接受新任务，等待 worker 安全结束，再释放线程依赖；对象的线程归属和 QThread 对象本身所在的线程不能混为一谈。

**状态与结果：** 区分任务未开始、运行中、暂停、取消请求、已取消、失败和成功。发出取消请求不代表任务已经停止，资源释放要等任务确认结束；Future 的完成也不一定表示业务结果有效。

**线程与事件循环：** GUI 线程只负责启动任务、接收结果和更新界面；共享数据要么转移所有权，要么用锁/原子/消息传递保护。queued slot 需要目标线程事件循环，阻塞 worker 则不能依赖它接收 queued 控制命令。

## 3. 直接使用

先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QtConcurrent::QTaskBuilder<Task, Args...> & onThreadPool(QThreadPool &newThreadPool)`
- `QFuture<QtConcurrent::InvokeResultType> spawn()`
- `void spawn(QtConcurrent::FutureResult)`
- `QtConcurrent::QTaskBuilder<Task, ExtraArgs...> withArguments(ExtraArgs &&... args)`
- `QtConcurrent::QTaskBuilder<Task, Args...> & withPriority(int newPriority)`

### 相关非成员函数

- `InvokeResultType`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 6 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QtConcurrent::QTaskBuilder<Task, Args...> &QTaskBuilder::onThreadPool(QThreadPool &newThreadPool)`

**API 类别：** 成员函数说明

**中文解读：** `QtConcurrent::QTaskBuilder::onThreadPool` 用于计算、查询或取得与“on、Thread、Pool”相关的操作。调用时要先确认当前状态和 `newThreadPool` 的有效范围；返回类型是 `QtConcurrent::QTaskBuilder<Task, Args...> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QtConcurrent::QTaskBuilder<Task, Args...> &`。
- 参数 `newThreadPool`：类型为 `QThreadPool &`。没有默认值，调用时必须提供。传入 `QThreadPool &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFuture<QtConcurrent::InvokeResultType> QTaskBuilder::spawn()`

**API 类别：** 成员函数说明

**中文解读：** `QtConcurrent::QTaskBuilder::spawn` 用于计算、查询或取得与“spawn”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFuture<QtConcurrent::InvokeResultType>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFuture<QtConcurrent::InvokeResultType>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTaskBuilder::spawn(QtConcurrent::FutureResult)`

**API 类别：** 成员函数说明

**中文解读：** `QtConcurrent::QTaskBuilder::spawn` 用于执行与“spawn”相关的操作。调用时要先确认当前状态和 `FutureResult` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `FutureResult`：类型为 `QtConcurrent::`。没有默认值，调用时必须提供。传入 `QtConcurrent::` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename... ExtraArgs> QtConcurrent::QTaskBuilder<Task, ExtraArgs...> QTaskBuilder::withArguments(ExtraArgs &&... args)`

**API 类别：** 成员函数说明

**中文解读：** `QtConcurrent::QTaskBuilder::withArguments` 用于计算、查询或取得与“with、Arguments”相关的操作。调用时要先确认当前状态和 `args` 的有效范围；返回类型是 `template <typename... ExtraArgs> QtConcurrent::QTaskBuilder<Task, ExtraArgs...>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename... ExtraArgs> QtConcurrent::QTaskBuilder<Task, ExtraArgs...>`。
- 参数 `args`：类型为 `ExtraArgs &&...`。没有默认值，调用时必须提供。传入 `ExtraArgs &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QtConcurrent::QTaskBuilder<Task, Args...> &QTaskBuilder::withPriority(int newPriority)`

**API 类别：** 成员函数说明

**中文解读：** `QtConcurrent::QTaskBuilder::withPriority` 用于计算、查询或取得与“with、Priority”相关的操作。调用时要先确认当前状态和 `newPriority` 的有效范围；返回类型是 `QtConcurrent::QTaskBuilder<Task, Args...> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QtConcurrent::QTaskBuilder<Task, Args...> &`。
- 参数 `newPriority`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] InvokeResultType`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QtConcurrent::QTaskBuilder` 的 `Invoke、结果、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

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

`QtConcurrent::QTaskBuilder` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
