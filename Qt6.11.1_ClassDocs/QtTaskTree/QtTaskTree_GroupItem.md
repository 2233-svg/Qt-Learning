# QtTaskTree::GroupItem

> Qt 6.11.1 · Qt TaskTree

## 1. 先建立直觉

**一句话定位：** `QtTaskTree::GroupItem` 是并发执行或同步类型，负责任务、线程、future、promise 或共享资源的协调。

**模块背景：** 这是 Qt TaskTree 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QtTaskTree::GroupItem` 是 并发与任务机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 并发 API 解决的是执行上下文、任务调度、共享数据和完成通知的组合问题。`QThread` 提供线程事件循环，线程池/Future 适合任务调度，同步原语保护共享状态；它们不会自动替你设计取消、异常和退出协议。

**适用场景：** 先定义数据所有权和退出条件，再选择 worker + QThread、QThreadPool、Qt Concurrent 或同步原语。把工作拆成可取消、可报告进度、可处理错误的步骤，完成后通过信号回到界面线程。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在 GUI 线程等待线程结束；不要从错误线程操作 worker；不要只调用 `requestInterruption()` 就假设任务停止；锁的获取顺序必须稳定，线程结束时不能留下悬空回调。

## 2. 依赖与对象关系

- 头文件：`#include <qtasktree.h>`
- 继承自：未在类页中列出
- 直接派生类：QtTaskTree::ExecutableItem、QtTaskTree::ExecutionMode

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

- `GroupDoneHandler`
- `GroupSetupHandler`

### 公有函数

- `GroupItem(const QtTaskTree::GroupItems &children)`
- `GroupItem(const QtTaskTree::Storage<StorageStruct> &storage)`
- `GroupItem(std::initializer_list<QtTaskTree::GroupItem> children)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] GroupItem::GroupDoneHandler`

**作用与语义：**

`std::function<DoneResult(DoneWith)>`或 `DoneResult` 的别名类型。
GroupDoneHandler 是 `onGroupDone()` 元素的一个参数。任何带有上述签名的函数，作为组完成的处理程序传递时，运行中的任务树会在组执行结束时调用。
`DoneWith`参数是可选的，你的完成处理器可以省略它。当它提供时，它保存了将报告给父组的最终结果信息。
返回的`DoneResult`值是可选的，你的处理器可以返回`void`。在这种情况下，组的最终结果将等于`DoneWith`参数所指示的值。当处理器返回`DoneResult`值时，组的最终结果可以在完成处理程序的内部通过返回值进行调整。
对于`DoneResult`类型的GroupDoneHandler，不会执行额外的处理，且该组无条件以传递的`DoneResult`值结束，忽略该组的工作流程策略。

### `[alias] GroupItem::GroupSetupHandler`

**作用与语义：**

`std::function<SetupResult()>`的别名类型。
GroupSetupHandler 是 `onGroupSetup()` 元素的一个参数。任何带有上述签名的函数，作为组设置处理程序传递时，运行中的任务树会在组执行开始时调用。
处理器的返回值指示运行组在调用完成后如何继续。默认返回值`SetupResult::Continue`指示组继续运行，即开始执行其子任务。返回值`SetupResult::StopWithSuccess`或`SetupResult::StopWithError`指示组跳过子任务的执行，并立即成功或错误完成任务。
当返回类型为`SetupResult::StopWithSuccess`或`SetupResult::StopWithError`时，组的 done handler（如提供）会立即同步调用。
注意：即使组设置处理程序返回`StopWithSuccess`或`StopWithError`，也会调用组的完成处理程序。这种行为不同于任务完成处理程序，未来可能会有所变化。
`onGroupSetup()`元素也接受`std::function<void()>`的缩写形式，即返回值为`void`。此时假设返回值为`SetupResult::Continue`。

### `GroupItem::GroupItem(const QtTaskTree::GroupItems &children)`

**作用与语义：**

构造一个包含给定列表的 GroupItem 元素`children`。
当`QTaskTree`解析该 GroupItem 元素时，它会被替换为其 `children`。
该构造器在构建包含 GroupItem 元素列表的 `Group` 元素时非常有用：
如果你想创建子树，可以用`Group`。
注意：不要将此 GroupItem 与 `Group` 元素混淆，因为 `Group` 在被任务树解析后仍保持子元素嵌套，而该 GroupItem 则不会。

**官方示例：**

```cpp
 static GroupItems getItems();

 ...

 const Group root {
     parallel,
     finishAllAndSuccess,
     getItems(), // GroupItems list is wrapped into a single GroupItem element
     onGroupSetup(...),
     onGroupDone(...)
 };
```

### `template <typename StorageStruct> GroupItem::GroupItem(const QtTaskTree::Storage<StorageStruct> &storage)`

**作用与语义：**

构建一个包含`storage`对象的 GroupItem 元素。
当运行任务树输入包含该 GroupItem 的 `Group` 元素时，该`StorageStruct`的实例会动态生成。
当该组执行后即将被留下时，之前实例化的`StorageStruct`会被删除。
动态创建的`StorageStruct`实例可通过 `Storage::operator->()`、Storage：：operator*() 或 `Storage::activeStorage()` 方法，从父`Group`元素的任一处理主体（包括嵌套组及其任务）访问。

### `GroupItem::GroupItem(std::initializer_list<QtTaskTree::GroupItem> children)`

**作用与语义：**

构造一个包含给定列表的 GroupItem 元素`children`。
当`QTaskTree`解析该 GroupItem 元素时，它会被替换为其 `children`。
该构造器在构建包含 GroupItem 元素列表的 `Group` 元素时非常有用：
如果你想创建子树，可以用`Group`。
注意：不要将此 GroupItem 与 `Group` 元素混淆，因为 `Group` 在被任务树解析后仍保持子元素嵌套，而该 GroupItem 则不会。

**官方示例：**

```cpp
 static GroupItems getItems();

 ...

 const Group root {
     parallel,
     finishAllAndSuccess,
     getItems(), // GroupItems list is wrapped into a single GroupItem element
     onGroupSetup(...),
     onGroupDone(...)
 };
```

### `GroupDoneHandler`

**作用与语义：**

`std::function<DoneResult(DoneWith)>`或 `DoneResult` 的别名类型。
GroupDoneHandler 是 `onGroupDone()` 元素的一个参数。任何带有上述签名的函数，作为组完成的处理程序传递时，运行中的任务树会在组执行结束时调用。
`DoneWith`参数是可选的，你的完成处理器可以省略它。当它提供时，它保存了将报告给父组的最终结果信息。
返回的`DoneResult`值是可选的，你的处理器可以返回`void`。在这种情况下，组的最终结果将等于`DoneWith`参数所指示的值。当处理器返回`DoneResult`值时，组的最终结果可以在完成处理程序的内部通过返回值进行调整。
对于`DoneResult`类型的GroupDoneHandler，不会执行额外的处理，且该组无条件以传递的`DoneResult`值结束，忽略该组的工作流程策略。

### `GroupSetupHandler`

**作用与语义：**

`std::function<SetupResult()>`的别名类型。
GroupSetupHandler 是 `onGroupSetup()` 元素的一个参数。任何带有上述签名的函数，作为组设置处理程序传递时，运行中的任务树会在组执行开始时调用。
处理器的返回值指示运行组在调用完成后如何继续。默认返回值`SetupResult::Continue`指示组继续运行，即开始执行其子任务。返回值`SetupResult::StopWithSuccess`或`SetupResult::StopWithError`指示组跳过子任务的执行，并立即成功或错误完成任务。
当返回类型为`SetupResult::StopWithSuccess`或`SetupResult::StopWithError`时，组的 done handler（如提供）会立即同步调用。
注意：即使组设置处理程序返回`StopWithSuccess`或`StopWithError`，也会调用组的完成处理程序。这种行为不同于任务完成处理程序，未来可能会有所变化。
`onGroupSetup()`元素也接受`std::function<void()>`的缩写形式，即返回值为`void`。此时假设返回值为`SetupResult::Continue`。

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

`QtTaskTree::GroupItem` 所属机制类型：并发与任务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
