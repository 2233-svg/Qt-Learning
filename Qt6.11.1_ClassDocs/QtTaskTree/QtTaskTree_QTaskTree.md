# QtTaskTree::QTaskTree

> Qt 6.11.1 · Qt TaskTree

## 1. 先建立直觉

**一句话定位：** `QtTaskTree::QTaskTree` 是并发执行或同步类型，负责任务、线程、future、promise 或共享资源的协调。

**模块背景：** 这是 Qt TaskTree 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QtTaskTree::QTaskTree` 是 并发与任务机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

**适用场景：** 先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

## 2. 依赖与对象关系

- 头文件：`#include <qtasktree.h>`
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

- `QTaskTree(QObject *parent)`
- `QTaskTree(const QtTaskTree::Group &recipe, QObject *parent = nullptr)`
- `virtual ~QTaskTree() override`
- `qsizetype asyncCount() const`
- `void cancel()`
- `bool isRunning() const`
- `void onStorageDone(const QtTaskTree::Storage<StorageStruct> &storage, Handler &&handler)`
- `void onStorageSetup(const QtTaskTree::Storage<StorageStruct> &storage, Handler &&handler)`
- `qsizetype progressMaximum() const`
- `qsizetype progressValue() const`
- `QtTaskTree::DoneWith runBlocking()`
- `QtTaskTree::DoneWith runBlocking(const QFuture<void> &future)`
- `void setRecipe(const QtTaskTree::Group &recipe)`
- `void start()`
- `qsizetype taskCount() const`

### 信号

- `void asyncCountChanged(qsizetype count)`
- `void done(QtTaskTree::DoneWith result)`
- `void progressValueChanged(qsizetype value)`
- `void started()`

### 静态公有成员

- `QtTaskTree::DoneWith runBlocking(const QtTaskTree::Group &recipe)`
- `QtTaskTree::DoneWith runBlocking(const QtTaskTree::Group &recipe, const QFuture<void> &future)`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QTaskTree::QTaskTree(QObject *parent)`

**作用与语义：**

构建一个空任务树，并带有给定的`parent`。使用`setRecipe()`传递声明式描述，说明任务树应如何执行任务以及如何处理已完成的任务。
启动空任务树是无操作操作，相关警告信息会被触发。

### `[explicit] QTaskTree::QTaskTree(const QtTaskTree::Group &recipe, QObject *parent = nullptr)`

**作用与语义：**

构建具有给定`recipe`和`parent`的任务树。任务树启动后，执行`recipe`内的任务，并根据传递的描述处理已完成的任务。

### `[override virtual noexcept] QTaskTree::~QTaskTree()`

**作用与语义：**

破坏任务树。
当任务树在被销毁时运行，它会立即取消所有正在运行的任务。在这种情况下，不会调用处理程序，甚至组和任务的已完成处理程序或`onStorageDone()`处理程序也不会被调用。任务树也不会发出任何来自解构器的信号，甚至没有`done()`或`progressValueChanged()`信号。这种行为可以始终依赖。销毁运行中的任务树是完全安全的。
销毁运行任务树是常见的模式。只要任务以非阻塞的方式实现其解构器，销毁任务就能保证快速运行，无需等待当前任务完成。
注意：不要直接从运行任务的处理程序或任务树信号调用解构器。在这种情况下，请使用`deleteLater()`。

### `qsizetype QTaskTree::asyncCount() const`

**作用与语义：**

返回当前异步调用链的实际数量。
返回的值表示在任务树运行期间控制返回到调用者事件循环的次数。最初，此值为 `0`。如果任务树的执行完全同步完成，则此值保持为 `0`。如果任务树包含在调用 `start()` 时成功启动的任何异步任务，则在调用 `start()` 完成之前，此值被提升为 `1`。之后，当任何异步任务完成且启动任何可能的继续执行时，此值会再次增加。增加过程持续直到任务树完成。当任务树发出 `done()` 信号时，增加停止。此值每次增加时都会发出 `asyncCountChanged()` 信号。

### `[signal] void QTaskTree::asyncCountChanged(qsizetype count)`

**作用与语义：**

当运行中的任务树即将将控制权返回调用者的事件循环时，该信号会发出。当任务树启动时，该信号以`0`值`count`发出，之后每当`asyncCount()`值增加时，`count`值会更新。每一个发送的信号（除最初值为`0`的信号外）都保证发射后任务树仍在异步运行。

### `void QTaskTree::cancel()`

**作用与语义：**

取消运行任务树的执行。
立即取消所有正在运行的任务。所有正在运行的任务和组结束时都会有错误，并调用其已完成的处理程序`DoneWith::Cancel`。存储的`onStorageDone()`处理程序也会被调用。`progressValueChanged()`信号也在发送。这种行为可以始终依赖。
cancel() 函数是同步执行的，因此在调用 cancel() 后，所有正在运行的任务都已完成，树也已经被取消。只要所用任务以非阻塞的方式实现其结构函数，cancel() 就能保证运行得很快，无需阻塞等待当前任务完成。
当任务树为空，即用默认构造函数构建时，调用cancel()为no-op，相关警告消息会被触发。
否则，当任务树未启动时，取消()调用会被忽略。
注意：不要直接从运行任务的处理器或任务树信号调用该函数。

### `[signal] void QTaskTree::done(QtTaskTree::DoneWith result)`

**作用与语义：**

该信号在任务树结束时发出，传递执行的最后`result`。任务树既不调用任何处理程序，也不再发出信号。
注意：不要直接从该信号的处理程序中删除任务树。请使用`deleteLater()`。

### `[override virtual protected] bool QTaskTree::event(QEvent *event)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。

### `bool QTaskTree::isRunning() const`

**作用与语义：**

如果任务树当前运行，返回`true`;否则返回`false`。

### `template <typename StorageStruct, typename Handler> void QTaskTree::onStorageDone(const QtTaskTree::Storage<StorageStruct> &storage, Handler &&handler)`

**作用与语义：**

安装一个存储，`handler`为`storage`动态检索运行中的任务树中的最终数据。
`StorageHandler`对`StorageStruct`实例进行了`const`引用：
当运行中的任务树即将离开放置`storage`的`Group`时，它会销毁一个`StorageStruct`实例。就在`StorageStruct`实例被摧毁之前，且在该组所有可能的处理器被调用后，任务树调用传递的`handler`。这使得能够动态读取给定存储的最终内容，并将其进一步处理到任务树之外。
当运行树被取消时，也会调用该处理程序。但当运行树被摧毁时，处理程序不会被调用。

**官方示例：**

```cpp
 static QByteArray load(const QString &fileName) { ... }

 Storage<QByteArray> storage;

 const auto onLoaderSetup = [](QThreadFunction<QByteArray> &task) {
     task.setThreadFunctionData(&load, "foo.txt");
 };
 const auto onLoaderDone = [storage](const QThreadFunction<QByteArray> &task) {
     *storage = task.result();
 };

 const Group root {
     storage,
     QThreadFunctionTask(onLoaderSetup, onLoaderDone, CallDoneFlag::OnSuccess)
 };

 QTaskTree taskTree(root);
 auto collectStorage = [](const QByteArray &storage){
     qDebug() << "final content" << storage;
 };
 taskTree.onStorageDone(storage, collectStorage);
 taskTree.start();
```

### `template <typename StorageStruct, typename Handler> void QTaskTree::onStorageSetup(const QtTaskTree::Storage<StorageStruct> &storage, Handler &&handler)`

**作用与语义：**

安装存储设置 `handler`，`storage` 将初始数据动态传递到运行中的任务树。
`StorageHandler`引用了`StorageStruct`实例：
当运行中的任务树进入`storage`所在的组时，会创建一个`StorageStruct`实例，准备在该组内使用。在创建`StorageStruct`实例后，且在调用该组的任何处理程序之前，任务树调用传递的 `handler`。这使得动态设置给定存储的初始内容成为可能。随后，当调用任何组的处理程序时，任务树会激活已创建和初始化的存储，使其在任何组的处理程序中可用。

**官方示例：**

```cpp
 static void save(const QString &fileName, const QByteArray &array) { ... }

 Storage<QByteArray> storage;

 const auto onSaverSetup = [storage](QThreadFunction<QByteArray> &task) {
     task.setThreadFunctionData(&save, "foo.txt", *storage);
 };

 const Group root {
     storage,
     QThreadFunctionTask(onSaverSetup)
 };

 QTaskTree taskTree(root);
 auto initStorage = [](QByteArray &storage){
     storage = "initial content";
 };
 taskTree.onStorageSetup(storage, initStorage);
 taskTree.start();
```

### `qsizetype QTaskTree::progressMaximum() const`

**作用与语义：**

返回最大额度`progressValue()`。
注意：目前和`taskCount()`一样。未来可能会改变。

### `qsizetype QTaskTree::progressValue() const`

**作用与语义：**

返回当前进度值，该值介于 `0` 和 `progressMaximum()` 之间。
返回的数字表示在任务树运行期间已有多少任务已完成、取消或跳过。当任务树启动时，此数字设置为 `0`。当任务树完成时，此数字总是等于 `progressMaximum()`。

### `[signal] void QTaskTree::progressValueChanged(qsizetype value)`

**作用与语义：**

当运行中的任务树完成、取消或跳过某些任务时，该信号会发出。`value`显示当前已完成、取消或跳过的任务总数。当任务树启动且`started()`信号发出后，该信号初始 `value` 为 `0`。当任务树即将结束且`done()`信号发出前，该信号以最后`value` `progressMaximum()` 发出。

### `QtTaskTree::DoneWith QTaskTree::runBlocking()`

**作用与语义：**

用 `QEventLoop::ExcludeUserInputEvents` 执行本地事件循环并启动任务树。
如果任务树成功完成，返回`DoneWith::Success`;否则返回`DoneWith::Error`。
注意：避免在主线程中使用此方法。请使用异步`start()`。该方法适用于非主线程或自动测试。

### `[static] QtTaskTree::DoneWith QTaskTree::runBlocking(const QtTaskTree::Group &recipe)`

**作用与语义：**

利用传递的`recipe`构建临时任务树并以阻塞方式运行。
如果任务树成功完成，返回`DoneWith::Success`;否则返回`DoneWith::Error`。
注意：避免在主线程中使用此方法。请使用异步`start()`。该方法适用于非主线程或自动测试。

### `QtTaskTree::DoneWith QTaskTree::runBlocking(const QFuture<void> &future)`

**作用与语义：**

传递的`future`用于监听取消事件。当任务树被取消时，该方法取消已传递的`future`。
注意：该功能会让`QTaskTree::runBlocking()`重载。

### `[static] QtTaskTree::DoneWith QTaskTree::runBlocking(const QtTaskTree::Group &recipe, const QFuture<void> &future)`

**作用与语义：**

传递的`future`用于监听取消事件。当任务树被取消时，该方法会取消已传递的`future`。
注意：该函数会超载 QTaskTree：：runBlocking（const Group 和 recipe）。

### `void QTaskTree::setRecipe(const QtTaskTree::Group &recipe)`

**作用与语义：**

为任务树设置给定的`recipe`。任务树启动后，执行`recipe`中包含的任务，并根据传递的描述处理已完成的任务。
注意：当被调用运行任务树时，该调用被忽略。

### `void QTaskTree::start()`

**作用与语义：**

启动任务树。
使用`setRecipe()`或构造函数来设置声明式描述，任务树将执行包含的任务并处理已完成的任务。
当任务树为空，即用默认构造函数构建时，调用start()为no-op，并发出相应的警告消息。
否则，当任务树已经运行时，调用start()会被忽略，并发出相应的警告消息。
否则，任务树开始运行。
启动任务树可能同步结束，例如当主组的起始处理器返回`SetupResult::StopWithError`时。因此，应在调用start()之前建立与已完成信号的连接。使用`isRunning()`检测任务树在调用start（后是否仍在运行）。
任务树的实现依赖于运行事件循环。调用该方法时，确保你有`QEventLoop`、`QCoreApplication`或其子类正在运行（或即将运行）。

### `[signal] void QTaskTree::started()`

**作用与语义：**

该信号在任务树启动时发出。该信号发出后，`progressValueChanged()`信号同步发出初始`0`值。

### `qsizetype QTaskTree::taskCount() const`

**作用与语义：**

返回存储配方中包含的异步任务数量。
注意：退回的编号不包括`QSyncTask`任务。
注意：任何使用 withTimeout() 设置的任务或组都会使任务总数增加`1`。

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

`QtTaskTree::QTaskTree` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
