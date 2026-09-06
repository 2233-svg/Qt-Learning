# QtTaskTree::QCustomTask

> Qt 6.11.1 · Qt TaskTree

## 1. 先建立直觉

**一句话定位：** `QtTaskTree::QCustomTask` 是并发执行或同步类型，负责任务、线程、future、promise 或共享资源的协调。

**模块背景：** 这是 Qt TaskTree 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QtTaskTree::QCustomTask` 是 并发与任务机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

**适用场景：** 先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

## 2. 依赖与对象关系

- 头文件：`#include <qtasktree.h>`
- 继承自：QtTaskTree::ExecutableItem
- 直接派生类：未在类页中列出

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

### 公有类型

- `TaskDoneHandler`
- `TaskSetupHandler`

### 公有函数

- `QCustomTask(SetupHandler &&setup = QCustomTask::TaskSetupHandler(), DoneHandler &&done = QCustomTask::TaskDoneHandler(), QtTaskTree::CallDone callDone = QtTaskTree::CallDoneFlag::Always)`

### 相关非成员函数

- `QBarrierTask`
- `QNetworkReplyWrapperTask`
- `QProcessTask`
- `QTaskTreeTask`
- `QTcpSocketWrapperTask`
- `QThreadFunctionTask`
- `QTimeoutTask`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QCustomTask::TaskDoneHandler`

**作用与语义：**

类型别名用于`std::function<QtTaskTree::DoneResult(const Task &, QtTaskTree::DoneWith)>`或 `DoneResult`。
TaskDoneHandler 是自定义任务元素构造函数的一个可选参数。任何带有上述签名的函数，作为任务已完成的处理程序传递时，运行中的任务树会在任务执行结束后、最终结果报告给父组之前调用。
在处理器内部，你可以从完成任务中获取最终数据。额外参数，包括存储，可以通过 lambda 捕获传递给处理器。也可以动态决定任务是否应以返回值结束，或调整最终结果。
`DoneWith`参数是可选的，完成处理程序可以省略它。当参数提供时，它保存任务最终结果的信息，并将报告给其父任务。
如果你不打算从完成的任务中读取任何数据，可以省略`const Task &`论点。
返回的`DoneResult`值是可选的，你的处理器可以返回`void`。在这种情况下，任务的最终结果将等于`DoneResult`参数所指示的值。当处理器返回`DoneResult`值时，任务的最终结果可以在完成处理程序的主体内通过返回值进行调整。
对于`DoneResult`类型的TaskDoneHandler，不执行额外的处理，任务无条件结束时传递值为`DoneResult`。

### `[alias] QCustomTask::TaskSetupHandler`

**作用与语义：**

`std::function<SetupResult(Task &)>`的别名。
TaskSetupHandler 是自定义任务元素构造函数的一个可选参数。任何带有上述特征的函数，作为任务设置处理程序传递时，任务树会在任务创建后且启动前调用。
在处理器内部，你可以根据需求配置任务。额外参数，包括存储，可以通过 lambda 捕获传递给处理器。你可以动态决定任务是成功启动还是跳过。
注意：不要自己在启动处理器内启动任务。留给`QTaskTree`，否则行为未定义。`QTaskTree`已经知道如何启动任务，这要归功于传递给`QCustomTask`<任务、适配器、删除器>构造程序的适配器模板参数。
处理程序的返回值指示正在运行的任务树在处理程序调用完成后如何继续。`SetupResult::Continue` 的返回值指示任务树继续运行，即执行相关的 `Task`。返回值 `SetupResult::StopWithSuccess` 或 `SetupResult::StopWithError` 分别指示任务树跳过任务执行并立即成功或错误完成任务。
当返回类型为`SetupResult::StopWithSuccess`或`SetupResult::StopWithError`时，任务已完成处理程序（如果提供了）之后不会被调用。
自定义任务的构造函数也接受`std::function<void(Task &)>`的简化形式，即返回值为`void`。在这种情况下，假设返回值是`SetupResult::Continue`。

### `[explicit] template < typename SetupHandler = QtTaskTree::QCustomTask<Task, Adapter, Deleter>::TaskSetupHandler, typename DoneHandler = QtTaskTree::QCustomTask<Task, Adapter, Deleter>::TaskDoneHandler, std::enable_if_t<!std::is_same_v<q20::remove_cvref_t<SetupHandler>, QCustomTask<Task, Adapter, Deleter>>, bool> = true > QCustomTask::QCustomTask(SetupHandler &&setup = QCustomTask::TaskSetupHandler(), DoneHandler &&done = QCustomTask::TaskDoneHandler(), QtTaskTree::CallDone callDone = QtTaskTree::CallDoneFlag::Always)`

**作用与语义：**

构建一个QCustomTask实例，并将`setup`和`done`处理器附加到任务上。当运行中的任务树即将启动任务时，实例化关联的`Task`对象，调用`setup`处理程序并引用已创建任务，并启动该任务。当运行任务结束时，任务树调用一个`done`处理程序，并`const`引用已创建任务。
传递的`setup`处理器属于`TaskSetupHandler`类型。例如：
`done` handler 属于 `TaskDoneHandler` 类型。默认情况下，每当任务完成时调用 `done` 处理器。当你希望处理程序仅在成功、失败或取消执行时调用时，传递一个非默认值作为 `callDone` 参数。

**官方示例：**

```cpp
 static void parseAndLog(const QString &input);

 ...

 const QString input = ...;

 const auto onFirstSetup = [input](QThreadFunction<void> &task) {
     if (input == "Skip")
         return SetupResult::StopWithSuccess; // This task won't start, the next one will
     if (input == "Error")
         return SetupResult::StopWithError; // This task and the next one won't start
     task.setThreadFunctionData(parseAndLog, input);
     // This task will start, and the next one will start after this one finished with success
     return SetupResult::Continue;
 };

 const auto onSecondSetup = [input](QThreadFunction<void> &task) {
     task.setThreadFunctionData(parseAndLog, input);
 };

 const Group group {
     QThreadFunctionTask<void>(onFirstSetup),
     QThreadFunctionTask<void>(onSecondSetup)
 };
```

### `[alias] QBarrierTask`

**作用与语义：**

`QCustomTask`的别名<`QBarrier`>类型，用于配方内。

### `[alias] QNetworkReplyWrapperTask`

**作用与语义：**

`QCustomTask`的别名类型<`QNetworkReplyWrapper`>，用于配方中。

### `[alias] QProcessTask`

**作用与语义：**

`QCustomTask`用`QProcessTaskDeleter`输入别名，<`QProcess`>用于配方中。

### `[alias] QTaskTreeTask`

**作用与语义：**

`QCustomTask`的别名<`QTaskTree`>类型，用于配方中。

### `[alias] QTcpSocketWrapperTask`

**作用与语义：**

`QCustomTask`的别名<`QTcpSocketWrapper`>类型，用于配方中。

### `[alias] QTimeoutTask`

**作用与语义：**

为`QCustomTask`<`std::chrono::milliseconds>`类型别名，用于配方中。`std::chrono::milliseconds`用于设置超时时间。默认超时是`std::chrono::milliseconds::zero()`，即QTimeout任务在控制返回运行事件循环时立即完成。
用例：

**官方示例：**

```cpp
 using namespace std::chrono;
 using namespace std::chrono_literals;

 const auto onSetup = [](milliseconds &timeout) { timeout = 1000ms; }
 const auto onDone = [] { qDebug() << "Timed out."; }

 const Group root {
     QTimeoutTask(onSetup, onDone)
 };
```

### `TaskDoneHandler`

**作用与语义：**

类型别名用于`std::function<QtTaskTree::DoneResult(const Task &, QtTaskTree::DoneWith)>`或 `DoneResult`。
TaskDoneHandler 是自定义任务元素构造函数的一个可选参数。任何带有上述签名的函数，作为任务已完成的处理程序传递时，运行中的任务树会在任务执行结束后、最终结果报告给父组之前调用。
在处理器内部，你可以从完成任务中获取最终数据。额外参数，包括存储，可以通过 lambda 捕获传递给处理器。也可以动态决定任务是否应以返回值结束，或调整最终结果。
`DoneWith`参数是可选的，完成处理程序可以省略它。当参数提供时，它保存任务最终结果的信息，并将报告给其父任务。
如果你不打算从完成的任务中读取任何数据，可以省略`const Task &`论点。
返回的`DoneResult`值是可选的，你的处理器可以返回`void`。在这种情况下，任务的最终结果将等于`DoneResult`参数所指示的值。当处理器返回`DoneResult`值时，任务的最终结果可以在完成处理程序的主体内通过返回值进行调整。
对于`DoneResult`类型的TaskDoneHandler，不执行额外的处理，任务无条件结束时传递值为`DoneResult`。

### `TaskSetupHandler`

**作用与语义：**

`std::function<SetupResult(Task &)>`的别名。
TaskSetupHandler 是自定义任务元素构造函数的一个可选参数。任何带有上述特征的函数，作为任务设置处理程序传递时，任务树会在任务创建后且启动前调用。
在处理器内部，你可以根据需求配置任务。额外参数，包括存储，可以通过 lambda 捕获传递给处理器。你可以动态决定任务是成功启动还是跳过。
注意：不要自己在启动处理器内启动任务。留给`QTaskTree`，否则行为未定义。`QTaskTree`已经知道如何启动任务，这要归功于传递给`QCustomTask`<任务、适配器、删除器>构造程序的适配器模板参数。
处理程序的返回值指示正在运行的任务树在处理程序调用完成后如何继续。`SetupResult::Continue` 的返回值指示任务树继续运行，即执行相关的 `Task`。返回值 `SetupResult::StopWithSuccess` 或 `SetupResult::StopWithError` 分别指示任务树跳过任务执行并立即成功或错误完成任务。
当返回类型为`SetupResult::StopWithSuccess`或`SetupResult::StopWithError`时，任务已完成处理程序（如果提供了）之后不会被调用。
自定义任务的构造函数也接受`std::function<void(Task &)>`的简化形式，即返回值为`void`。在这种情况下，假设返回值是`SetupResult::Continue`。

### `QThreadFunctionTask`

**作用与语义：**

`QCustomTask`<`QThreadFunction`> 的别名，用于<ResultType>配方中。

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

`QtTaskTree::QCustomTask` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
