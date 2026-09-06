# QSemaphoreReleaser

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QSemaphoreReleaser` 是并发执行或同步类型，负责任务、线程、future、promise 或共享资源的协调。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSemaphoreReleaser` 是并发模块中的类型，用于组织线程执行、同步或资源访问。

**内部模型：** 并发正确性来自所有权、共享数据、同步边界和退出协议的组合，而不是仅仅“开一个线程”。先定义谁读写数据，再决定 queued connection、mutex、future 或线程池。

**适用场景：** 后台任务、阻塞 I/O、并行计算或多个执行上下文共享资源时使用。

**典型调用链：** 划分任务和数据 -> 选择线程/线程池/future -> 明确同步和取消 -> 连接完成/错误 -> 等待安全退出。

**先记住的坑：** 避免 GUI 线程阻塞等待；锁顺序要稳定；线程结束前不能释放它使用的对象；queued slot 需要目标线程事件循环。

## 2. 依赖与对象关系

- 头文件：`#include <QSemaphoreReleaser>`
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

- `QSemaphoreReleaser()`
- `QSemaphoreReleaser(QSemaphore &sem, int n = 1)`
- `QSemaphoreReleaser(QSemaphore *sem, int n = 1)`
- `QSemaphoreReleaser(QSemaphoreReleaser &&other)`
- `~QSemaphoreReleaser()`
- `QSemaphore * cancel()`
- `QSemaphore * semaphore() const`
- `void swap(QSemaphoreReleaser &other)`
- `QSemaphoreReleaser & operator=(QSemaphoreReleaser &&other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QSemaphoreReleaser::QSemaphoreReleaser()`

**作用与语义：**

默认构造函数。创建一个无效的QSemaphoreReleaser。

### `[explicit noexcept] QSemaphoreReleaser::QSemaphoreReleaser(QSemaphore &sem, int n = 1)`

**作用与语义：**

构造函数。在解构器中存储参数并调用 `sem`.release（`n`）。

### `[explicit noexcept] QSemaphoreReleaser::QSemaphoreReleaser(QSemaphore *sem, int n = 1)`

**作用与语义：**

构造函数。存储参数并在解散器中调用 `sem`->release（`n`）。

### `[noexcept] QSemaphoreReleaser::QSemaphoreReleaser(QSemaphoreReleaser &&other)`

**作用与语义：**

移动构造器。接管从`other`调用`QSemaphore::release()`的责任，而调用则被取消。

### `[noexcept] QSemaphoreReleaser::~QSemaphoreReleaser()`

**作用与语义：**

除非被取消，调用`QSemaphore::release()`基于构造函数的参数，或通过最后一步赋值进行调用。

### `[noexcept] QSemaphore *QSemaphoreReleaser::cancel()`

**作用与语义：**

取消该`QSemaphoreReleaser`，使得解构函数不再调用`semaphore()->release()`。返回调用前的值`semaphore()`。调用结束后，`semaphore()`返回`nullptr`。
要再次启用，需重新分配一个`QSemaphoreReleaser`：

**官方示例：**

```cpp
 releaser.cancel(); // avoid releasing old semaphore()
 releaser = QSemaphoreReleaser(sem, 42);
 // now will call sem.release(42) when 'releaser' is destroyed
```

### `[noexcept] QSemaphore *QSemaphoreReleaser::semaphore() const`

**作用与语义：**

返回指向构造函数提供的`QSemaphore`对象的指针，或通过最后一步的指针（如有）返回。否则返回`nullptr`。

### `[noexcept] void QSemaphoreReleaser::swap(QSemaphoreReleaser &other)`

**作用与语义：**

交换`*this`和`other`的责任。
与移动分配不同，这两件物体交换后从未释放信号板（如果有的话）。
因此，这个函数非常快速且从未失效。

### `[noexcept] QSemaphoreReleaser &QSemaphoreReleaser::operator=(QSemaphoreReleaser &&other)`

**作用与语义：**

移动分配操作员。接管调用`QSemaphore::release()`的责任，`other`调用后被取消。
如果这个信号量释放器负责调用某个`QSemaphore::release()`，它会先执行调用，然后接管`other`。

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

`QSemaphoreReleaser` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
