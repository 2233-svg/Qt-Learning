# QSystemSemaphore

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QSystemSemaphore` 是并发执行或同步类型，负责任务、线程、future、promise 或共享资源的协调。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSystemSemaphore` 是并发模块中的类型，用于组织线程执行、同步或资源访问。

**内部模型：** 并发正确性来自所有权、共享数据、同步边界和退出协议的组合，而不是仅仅“开一个线程”。先定义谁读写数据，再决定 queued connection、mutex、future 或线程池。

**适用场景：** 后台任务、阻塞 I/O、并行计算或多个执行上下文共享资源时使用。

**典型调用链：** 划分任务和数据 -> 选择线程/线程池/future -> 明确同步和取消 -> 连接完成/错误 -> 等待安全退出。

**先记住的坑：** 避免 GUI 线程阻塞等待；锁顺序要稳定；线程结束前不能释放它使用的对象；queued slot 需要目标线程事件循环。

## 2. 依赖与对象关系

- 头文件：`#include <QSystemSemaphore>`
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

### 公有类型

- `enum AccessMode { Open, Create }`
- `enum SystemSemaphoreError { NoError, PermissionDenied, KeyError, AlreadyExists, NotFound, …, UnknownError }`

### 公有函数

- `QSystemSemaphore(const QNativeIpcKey &key, int initialValue = 0, QSystemSemaphore::AccessMode mode = Open)`
- `QSystemSemaphore(const QString &key, int initialValue = 0, QSystemSemaphore::AccessMode mode = Open)`
- `~QSystemSemaphore()`
- `bool acquire()`
- `QSystemSemaphore::SystemSemaphoreError error() const`
- `QString errorString() const`
- `QString key() const`
- `QNativeIpcKey nativeIpcKey() const`
- `bool release(int n = 1)`
- `void setKey(const QString &key, int initialValue = 0, QSystemSemaphore::AccessMode mode = Open)`
- `void setNativeKey(const QNativeIpcKey &key, int initialValue = 0, QSystemSemaphore::AccessMode mode = Open)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSystemSemaphore::AccessMode`

**作用与语义：**

此枚举由构造函数和 `setKey()` 使用。其目的是处理 Unix 实现的信号量在崩溃后仍然存在的问题。在 Unix 中，当信号量在崩溃后仍然存在时，我们需要一种方法在系统重用信号量时强制其重置资源计数。在 Windows 中，由于信号量无法在崩溃后存活，此枚举没有作用。
- `QSystemSemaphore::Open`: `0`；如果信号量已存在，其初始资源计数不会被重置。如果信号量不存在，则创建它并设置其初始资源计数。
- `QSystemSemaphore::Create`: `1`；`QSystemSemaphore` 拥有信号量的所有权，并将其资源计数设置为请求的值，无论信号量是否已经存在（通过存活崩溃）。当构造特定键的第一个信号量时，并且您知道如果信号量已存在它只能是由于崩溃造成的，应将此值传递给构造函数。在 Windows 中，由于信号量无法存活崩溃，Create 和 Open 的行为相同。

### `QSystemSemaphore::QSystemSemaphore(const QNativeIpcKey &key, int initialValue = 0, QSystemSemaphore::AccessMode mode = Open)`

**作用与语义：**

请求指定`key`的系统信号量。参数`initialValue`和`mode`根据以下规则使用，这些规则取决于系统。
在Unix中，如果`mode` `Open`且系统已有`key`识别的信号量，则使用该信号量，且信号量的资源计数不被更改，即忽略`initialValue`。但如果系统尚未有`key`标识的信号量，则为该键创建新的信号量，并将资源计数设为`initialValue`。
在Unix中，如果`mode` `Create`且系统已有`key`识别的信号量，则使用该信号量，其资源计数设为`initialValue`。如果系统尚未有`key`识别的信号量，则为该键创建新的信号量，并将资源计数设为`initialValue`。
在Windows中，`mode`被忽略，系统总是尝试为指定`key`创建信号量。如果系统没有被识别为`key`的信号量，系统会创建该信号量并将资源计数设置为`initialValue`。但如果系统已有被识别为`key`的信号量，则使用该信号量并忽略`initialValue`。
`mode`参数仅用于Unix系统中处理信号量在进程崩溃后幸存的情况。在这种情况下，下一个分配具有相同`key`的信号量的进程将获得幸存的信号量，除非`mode` `Create`，否则资源计数不会重置为`initialValue`，而是保留崩溃进程最初给出的值。

### `QSystemSemaphore::QSystemSemaphore(const QString &key, int initialValue = 0, QSystemSemaphore::AccessMode mode = Open)`

**作用与语义：**

请求由遗留密钥识别的系统信号量`key`。

### `[noexcept] QSystemSemaphore::~QSystemSemaphore()`

**作用与语义：**

析构函数销毁 `QSystemSemaphore` 对象，但底层系统信号量不会从系统中移除，除非此 `QSystemSemaphore` 实例是该系统信号量存在的最后一个实例。
析构函数的两个重要副作用取决于系统。在 Windows 中，如果已为该信号量调用过 `acquire()` 但未调用 `release()`，则析构函数不会调用 `release()`，也不会在进程正常退出时释放资源。这将是一个程序错误，可能导致另一个尝试获取相同资源的进程发生死锁。在 Unix 中，在调用析构函数之前未释放的已获取资源将在进程退出时自动释放。

### `bool QSystemSemaphore::acquire()`

**作用与语义：**

如果有该信号量保护的资源，获取其中一个资源，并返回`true`。如果该信号量保护的所有资源已被获取，调用会阻塞，直到另一个拥有相同键的信号量的进程或线程释放其中一个资源。
如果返回 false，表示系统发生了错误。调用 `error()` 以获得 `QSystemSemaphore::SystemSemaphoreError` 值，表示发生了哪个错误。

### `QSystemSemaphore::SystemSemaphoreError QSystemSemaphore::error() const`

**作用与语义：**

返回一个值，表示是否发生了错误，如果发生了，以及是哪一个错误。

### `QString QSystemSemaphore::errorString() const`

**作用与语义：**

返回最后一次错误的文本描述。如果`error()`返回错误值，调用该函数获取描述错误的文本字符串。

### `QString QSystemSemaphore::key() const`

**作用与语义：**

返回分配给该系统信号量的遗留密钥。密钥是可从其他进程访问该信号量的名称。

### `QNativeIpcKey QSystemSemaphore::nativeIpcKey() const`

**作用与语义：**

返回分配给该系统信号量的密钥。密钥是信号量可从其他进程访问的名称。
您可以使用原生密钥访问未由 Qt 创建的系统信号量，或授权非 Qt 应用程序访问。更多信息请参见本地 IPC 密钥。

### `bool QSystemSemaphore::release(int n = 1)`

**作用与语义：**

释放`n`由信号板保护的资源。除非系统出现错误，否则返回`true`。
示例：创建一个包含五种资源的系统信号量;全部收集后全部释放。
该函数还可以“创建”资源。例如，紧接上述语句序列后，假设我们添加以下语句：
现在有十个新资源被信号灯守护，除了已有的五个。你通常不会用这个功能来创造更多资源。

**官方示例：**

```cpp
 QSystemSemaphore sem(QSystemSemaphore::platformSafeKey("market"), 5, QSystemSemaphore::Create);
 for (int i = 0; i < 5; ++i)  // acquire all 5 resources
     sem.acquire();
 sem.release(5);              // release the 5 resources
```

### `void QSystemSemaphore::setKey(const QString &key, int initialValue = 0, QSystemSemaphore::AccessMode mode = Open)`

**作用与语义：**

该函数的工作原理与构造函数相同。它重建了`QSystemSemaphore`对象。如果新`key`与旧键不同，调用该函数就像用旧键调用信号量的解构器，然后调用构造器用新`key`创建新的信号量。`initialValue`和`mode`参数与构造函数定义相同。

### `void QSystemSemaphore::setNativeKey(const QNativeIpcKey &key, int initialValue = 0, QSystemSemaphore::AccessMode mode = Open)`

**作用与语义：**

该函数的工作原理与构造函数相同。它重建了这个`QSystemSemaphore`对象。如果新`key`与旧键不同，调用该函数就像用旧键调用信号量的解构器，然后调用构造器用新`key`创建新的信号量。`initialValue`和`mode`参数与构造函数定义相同。
如果本地密钥是从其他进程共享的，这个功能非常有用。更多信息请参见本地IPC密钥。

### `enum SystemSemaphoreError { NoError, PermissionDenied, KeyError, AlreadyExists, NotFound, …, UnknownError }`

**作用与语义：**

- `QSystemSemaphore::NoError`: `0`; 没有发生错误。
- `QSystemSemaphore::PermissionDenied`: `1`; 操作失败，因为调用者没有所需的权限。
- `QSystemSemaphore::KeyError`: `2`; 操作失败，因为键无效。
- `QSystemSemaphore::AlreadyExists`: `3`; 操作失败，因为指定键的系统信号量已经存在。
- `QSystemSemaphore::NotFound`: `4`; 操作失败，因为无法找到指定键的系统信号量。
- `QSystemSemaphore::OutOfResources`: `5`; 操作失败，因为没有足够的内存来完成请求。
- `QSystemSemaphore::UnknownError`: `6`; 发生了其他情况，且情况很糟。

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

`QSystemSemaphore` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
