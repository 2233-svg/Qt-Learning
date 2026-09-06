# QtTaskTree::QTcpSocketWrapper

> Qt 6.11.1 · Qt TaskTree

## 1. 先建立直觉

**一句话定位：** `QtTaskTree::QTcpSocketWrapper` 是并发执行或同步类型，负责任务、线程、future、promise 或共享资源的协调。

**模块背景：** 这是 Qt TaskTree 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QtTaskTree::QTcpSocketWrapper` 是 并发与任务机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

**适用场景：** 先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

## 2. 依赖与对象关系

- 头文件：`#include <qtcpsocketwrappertask.h>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS TaskTree)
target_link_libraries(mytarget PRIVATE Qt6::TaskTree)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

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

- `QTcpSocketWrapper(QObject *parent)`
- `virtual ~QTcpSocketWrapper() override`
- `void setAddress(const QHostAddress &address)`
- `void setData(const QByteArray &data)`
- `void setPort(quint16 port)`
- `QTcpSocket * socket() const`
- `void start()`

### 信号

- `void done(QtTaskTree::DoneResult result)`
- `void started()`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QTcpSocketWrapper::QTcpSocketWrapper(QObject *parent)`

**作用与语义：**

创建带有特定`parent`的QTcpSocketWrapper。

### `[override virtual noexcept] QTcpSocketWrapper::~QTcpSocketWrapper()`

**作用与语义：**

会破坏`QTcpSocketWrapper`。如果加速的`socket()`还在运行，就会被终止。

### `[signal] void QTcpSocketWrapper::done(QtTaskTree::DoneResult result)`

**作用与语义：**

该信号在相关`QTcpSocket`结束后发出。通过的`result`表示该信号是成功还是错误。

### `[override virtual protected] bool QTcpSocketWrapper::event(QEvent *event)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。

### `void QTcpSocketWrapper::setAddress(const QHostAddress &address)`

**作用与语义：**

把`address`设置为`start()`。

### `void QTcpSocketWrapper::setData(const QByteArray &data)`

**作用与语义：**

将`data`设置为用于`start()`。如果不是空的，连接建立后`data`会自动写入套接字。

### `void QTcpSocketWrapper::setPort(quint16 port)`

**作用与语义：**

把`port`设置为`start()`使用。

### `QTcpSocket *QTcpSocketWrapper::socket() const`

**作用与语义：**

返回指向已加写`QTcpSocket`的指针。`QTcpSocketWrapper`开始前和结束后，该函数返回`nullptr`。在`started()`信号发出后，直到信号发出`done()`，访问`QTcpSocket`是安全的。

### `void QTcpSocketWrapper::start()`

**作用与语义：**

`QTcpSocketWrapper`开始了。

### `[signal] void QTcpSocketWrapper::started()`

**作用与语义：**

该信号是在管理`QTcpSocket`连接后发出的。

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

`QtTaskTree::QTcpSocketWrapper` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
