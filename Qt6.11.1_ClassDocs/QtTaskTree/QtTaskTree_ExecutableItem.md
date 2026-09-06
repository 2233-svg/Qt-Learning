# QtTaskTree::ExecutableItem

> Qt 6.11.1 · Qt TaskTree

## 1. 先建立直觉

**一句话定位：** `QtTaskTree::ExecutableItem` 是并发执行或同步类型，负责任务、线程、future、promise 或共享资源的协调。

**模块背景：** 这是 Qt TaskTree 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QtTaskTree::ExecutableItem` 是 并发与任务机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

**适用场景：** 先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

## 2. 依赖与对象关系

- 头文件：`#include <qtasktree.h>`
- 继承自：QtTaskTree::GroupItem
- 直接派生类：QtTaskTree::Forever、QtTaskTree::Group、QtTaskTree::QCustomTask,、QtTaskTree::QSyncTask

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS TaskTree)
target_link_libraries(mytarget PRIVATE Qt6::TaskTree)
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

- `QtTaskTree::Group withAccept(ObjectSignalGetter &&getter) const`
- `QtTaskTree::Group withCancel(ObjectSignalGetter &&getter, std::initializer_list<QtTaskTree::GroupItem> postCancelRecipe = {}) const`
- `QtTaskTree::Group withLog(const QString &logName) const`
- `QtTaskTree::Group withTimeout(std::chrono::milliseconds timeout, const std::function<void ()> &handler = {}) const`

### 相关非成员函数

- `QtTaskTree::Group operator!(const QtTaskTree::ExecutableItem &item)`
- `QtTaskTree::Group operator&&(const QtTaskTree::ExecutableItem &first, const QtTaskTree::ExecutableItem &second)`
- `QtTaskTree::Group operator&&(const QtTaskTree::ExecutableItem &item, QtTaskTree::DoneResult result)`
- `QtTaskTree::Group operator||(const QtTaskTree::ExecutableItem &first, const QtTaskTree::ExecutableItem &second)`
- `QtTaskTree::Group operator||(const QtTaskTree::ExecutableItem &item, QtTaskTree::DoneResult result)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `template <typename ObjectSignalGetter> QtTaskTree::Group ExecutableItem::withAccept(ObjectSignalGetter &&getter) const`

**作用与语义：**

返回`this` `ExecutableItem`的副本，并结合一个信号等待器。传递的`getter`是一个函数，返回描述发射器和其等待信号的 `ObjectSignal`。在`getter`中使用`makeObjectSignal()`来创建一个`ObjectSignal`对象。
当`this` `ExecutableItem`以错误结束时，返回`Group`立即以错误结束，无需等待等待者的信号。
当`this` `ExecutableItem`成功完成时，返回的`Group`不会立即完成，而是等待等待信号的发送。等待信号发送后，返回的`Group`成功完成。如果等待信号在`this` `ExecutableItem`结束前发送，等待阶段被跳过，返回`Group`同步完成。
当`this` `ExecutableItem`即将启动时，连接到等待者信号。如果等待信号在启动前被触发，启动`this` `ExecutableItem`后不会被察觉。

### `template <typename ObjectSignalGetter> QtTaskTree::Group ExecutableItem::withCancel(ObjectSignalGetter &&getter, std::initializer_list<QtTaskTree::GroupItem> postCancelRecipe = {}) const`

**作用与语义：**

使 的副本`this` `ExecutableItem`可取消。传递的`getter`是一个函数，返回描述发射体及其消去信号的 `ObjectSignal`。在`getter`中使用`makeObjectSignal()`来创建一个`ObjectSignal`对象。当消去信号发出时，`this` `ExecutableItem`被取消，执行一个可选提供的`postCancelRecipe`，返回 Group 以错误结束。
当`this` `ExecutableItem`在取消信号发出前结束时，返回的组立即结束，结果与`this` `ExecutableItem`结束相同。此时可选择的`postCancelRecipe`会被跳过。
与取消信号的连接是在即将启动`this` `ExecutableItem`时建立的。如果取消信号在启动前被触发，启动`this` `ExecutableItem`后不会被察觉。

### `QtTaskTree::Group ExecutableItem::withLog(const QString &logName) const`

**作用与语义：**

将自定义的调试打印输出附加到任务启动时及任务结束后发布的`this` `ExecutableItem`副本上，并返回耦合后的项目。
调试打印输出包含事件（开始或结束）的时间戳和`logName`，用于识别调试日志中的具体任务。
最终打印输出包含额外信息，如执行是同步还是异步，其结果（由`DoneWith`枚举描述的值）以及总执行时间（毫秒）。

### `QtTaskTree::Group ExecutableItem::withTimeout(std::chrono::milliseconds timeout, const std::function<void ()> &handler = {}) const`

**作用与语义：**

将`QTimeoutTask`附加到`this` `ExecutableItem`副本上，经过`timeout`毫秒，并可选择提供超时`handler`，并返回已连接的项目。
当`ExecutableItem`在`timeout`通过前结束时，返回的项目立即结束并显示任务结果。否则，`handler`会被调用（如果提供），任务会被取消，返回的项目会以错误结束。

### `QtTaskTree::Group operator!(const QtTaskTree::ExecutableItem &item)`

**作用与语义：**

回归一群被否定`item` `DoneResult`的群体。
如果`item`报告`DoneResult::Success`，退回物品报告`DoneResult::Error`。如果`item`报告`DoneResult::Error`，退回物品报告 `DoneResult::Success`。
退回的物品等同于：

**官方示例：**

```cpp
 Group {
     item,
     onGroupDone([](DoneWith doneWith) { return toDoneResult(doneWith == DoneWith::Error); })
 }
```

### `QtTaskTree::Group operator&&(const QtTaskTree::ExecutableItem &first, const QtTaskTree::ExecutableItem &second)`

**作用与语义：**

返回一个包含`first`任务和`second`任务合并的群。
`first`和`second`任务都按顺序执行。如果两个任务都报告`DoneResult::Success`，返回的项目报告`DoneResult::Success`。否则，返回的项目报告`DoneResult::Error`。
返回的项目发生短路：如果`first`任务报告`DoneResult::Error`，`second`任务会被跳过，返回的项目立即报告`DoneResult::Error`。
退回的物品等同于：
注意：通过以下代码实现并行执行合取，可以实现短路方式：`Group { parallel, stopOnError, first, second }`。在这种情况下：如果第一个完成的任务报告`DoneResult::Error`，另一个任务会被取消，组立即报告`DoneResult::Error`。

**官方示例：**

```cpp
 Group { stopOnError, first, second }
```

### `QtTaskTree::Group operator&&(const QtTaskTree::ExecutableItem &item, QtTaskTree::DoneResult result)`

**作用与语义：**

如果`result` `DoneResult::Success`，返回`item`任务;否则返回`item`任务，完成结果调整为`DoneResult::Error`。
`task && DoneResult::Error`是无条件调整任务成果为`DoneResult::Error`的等价工具。
注意：该函数会超载 ExecutableItem：：operator&&()。

### `QtTaskTree::Group operator||(const QtTaskTree::ExecutableItem &first, const QtTaskTree::ExecutableItem &second)`

**作用与语义：**

返回一个包含`first`和`second`任务的组，并与析取合并。
`first`和`second`任务都按顺序执行。如果两个任务都报告`DoneResult::Error`，返回的项目报告`DoneResult::Error`。否则，返回的项目报告`DoneResult::Success`。
返回的项目发生短路：如果`first`任务报告`DoneResult::Success`，`second`任务会被跳过，返回的项目立即报告`DoneResult::Success`。
退回的物品等同于：
注意：通过以下代码实现析取的并行短路执行：`Group { parallel, stopOnSuccess, first, second }`。此时，如果第一个完成的任务报告`DoneResult::Success`，另一个任务被取消，组立即报告`DoneResult::Success`。

**官方示例：**

```cpp
 Group { stopOnSuccess, first, second }
```

### `QtTaskTree::Group operator||(const QtTaskTree::ExecutableItem &item, QtTaskTree::DoneResult result)`

**作用与语义：**

如果`result`被`DoneResult::Error`，返回`item`任务;否则返回`item`任务，其完成结果调整为`DoneResult::Success`。
`task || DoneResult::Success`是无条件调整任务成果为`DoneResult::Success`的等价工具。
注意：该函数会超载 ExecutableItem：：operator||().

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

`QtTaskTree::ExecutableItem` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
