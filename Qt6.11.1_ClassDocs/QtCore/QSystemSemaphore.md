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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 13 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QSystemSemaphore::AccessMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSystemSemaphore` 暴露的类型声明 `Access、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:AccessMode`。
- 属性名：`QSystemSemaphore`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSystemSemaphore::QSystemSemaphore(const QNativeIpcKey &key, int initialValue = 0, QSystemSemaphore::AccessMode mode = Open)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSystemSemaphore` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `key`：类型为 `const QNativeIpcKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `initialValue`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QSystemSemaphore::AccessMode`。默认值为 `Open`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSystemSemaphore::QSystemSemaphore(const QString &key, int initialValue = 0, QSystemSemaphore::AccessMode mode = Open)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSystemSemaphore` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `initialValue`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QSystemSemaphore::AccessMode`。默认值为 `Open`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QSystemSemaphore::~QSystemSemaphore()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSystemSemaphore` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSystemSemaphore::acquire()`

**API 类别：** 成员函数说明

**中文解读：** `QSystemSemaphore::acquire` 用于计算、查询或取得与“acquire”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSystemSemaphore::SystemSemaphoreError QSystemSemaphore::error() const`

**API 类别：** 成员函数说明

**中文解读：** `QSystemSemaphore::error` 用于计算、查询或取得与“错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSystemSemaphore::SystemSemaphoreError`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSystemSemaphore::SystemSemaphoreError`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSystemSemaphore::errorString() const`

**API 类别：** 成员函数说明

**中文解读：** `QSystemSemaphore::errorString` 用于计算、查询或取得与“错误、字符串”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSystemSemaphore::key() const`

**API 类别：** 成员函数说明

**中文解读：** `QSystemSemaphore::key` 用于计算、查询或取得与“key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNativeIpcKey QSystemSemaphore::nativeIpcKey() const`

**API 类别：** 成员函数说明

**中文解读：** `QSystemSemaphore::nativeIpcKey` 用于计算、查询或取得与“native、Ipc、Key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNativeIpcKey`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNativeIpcKey`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSystemSemaphore::release(int n = 1)`

**API 类别：** 成员函数说明

**中文解读：** `QSystemSemaphore::release` 用于计算、查询或取得与“释放”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `n`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSystemSemaphore::setKey(const QString &key, int initialValue = 0, QSystemSemaphore::AccessMode mode = Open)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setKey`。调用它会改变 `QSystemSemaphore` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `initialValue`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QSystemSemaphore::AccessMode`。默认值为 `Open`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSystemSemaphore::setNativeKey(const QNativeIpcKey &key, int initialValue = 0, QSystemSemaphore::AccessMode mode = Open)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNativeKey`。调用它会改变 `QSystemSemaphore` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QNativeIpcKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `initialValue`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QSystemSemaphore::AccessMode`。默认值为 `Open`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum SystemSemaphoreError { NoError, PermissionDenied, KeyError, AlreadyExists, NotFound, …, UnknownError }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSystemSemaphore` 暴露的类型声明 `System、Semaphore、错误`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
