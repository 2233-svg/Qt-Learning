# QEventLoop

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QEventLoop` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QEventLoop` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QEventLoop>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ProcessEventsFlag { AllEvents, ExcludeUserInputEvents, ExcludeSocketNotifiers, WaitForMoreEvents }`
- `flags ProcessEventsFlags`

### 公有函数

- `QEventLoop(QObject *parent = nullptr)`
- `virtual ~QEventLoop()`
- `int exec(QEventLoop::ProcessEventsFlags flags = AllEvents)`
- `bool isRunning() const`
- `bool processEvents(QEventLoop::ProcessEventsFlags flags = AllEvents)`
- `(since 6.7) void processEvents(QEventLoop::ProcessEventsFlags flags, QDeadlineTimer deadline)`
- `void processEvents(QEventLoop::ProcessEventsFlags flags, int maxTime)`
- `void wakeUp()`

### 重实现的公有函数

- `virtual bool event(QEvent *event) override`

### 公有槽函数

- `void exit(int returnCode = 0)`
- `void quit()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QEventLoop::ProcessEventsFlagflags QEventLoop::ProcessEventsFlags`

**作用与语义：**

该枚举控制`processEvents()`函数处理的事件类型。
- `QEventLoop::AllEvents`：`0x00`;所有事件。注意`DeferredDelete`事件会被特别处理。详情请参见 `QObject::deleteLater()`。
- `QEventLoop::ExcludeUserInputEvents`：`0x01`;不要处理用户输入事件，如ButtonPress和KeyPress。注意，这些事件不会被丢弃;下次调用`processEvents()`时，事件会在没有ExcludeUserInputEvents标志的情况下被传递。
- `QEventLoop::ExcludeSocketNotifiers`：`0x02`;不要处理套接字通知事件。注意，这些事件不会被丢弃;下次调用`processEvents()`时，它们会被传递，而没有ExcludeSocketNotifiers标志。
- `QEventLoop::WaitForMoreEvents`：`0x04`;如果没有待处理事件，则等待事件。
ProcessEventsFlags 类型是 QFlags 的 typedef<ProcessEventsFlag>。它存储 ProcessEventsFlag 值的 OR 组合。

### `[explicit] QEventLoop::QEventLoop(QObject *parent = nullptr)`

**作用与语义：**

构造一个事件循环对象，`parent`。

### `[virtual noexcept] QEventLoop::~QEventLoop()`

**作用与语义：**

摧毁事件循环对象。

### `[override virtual] bool QEventLoop::event(QEvent *event)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。
该虚拟函数接收对象事件，如果事件`e`被识别并处理，应返回真。
event() 函数可以重新实现，以自定义对象的行为。
确保你调用所有未处理的事件的父事件类实现。

### `int QEventLoop::exec(QEventLoop::ProcessEventsFlags flags = AllEvents)`

**作用与语义：**

进入主事件循环，等待调用`exit()`。返回传递给`exit()`的值。
如果指定了`flags`，只处理`flags`允许的事件类型。
启动事件处理需要调用该函数。主事件循环接收来自窗口系统的事件，并将其分发给应用控件。
一般来说，调用exec()之前不能进行任何用户交互。作为特殊情况，像`QMessageBox`这样的模态小部件可以在调用exec()之前使用，因为模态小部件使用自身的本地事件循环。
为了让你的应用程序执行空闲处理（即在没有待处理事件时执行特殊函数），可以使用超时为0ns的`QChronoTimer`。更复杂的空闲处理方案可以通过`processEvents()`实现。

### `[slot] void QEventLoop::exit(int returnCode = 0)`

**作用与语义：**

告诉事件循环退出并返回代码。
调用该函数后，事件循环从调用返回`exec()`。`exec()`函数返回`returnCode`。
按照惯例，`returnCode`为0表示成功，任何非零值表示错误。
注意，与同名的 C 库函数不同，该函数会返回调用者——停止的是事件处理。

### `bool QEventLoop::isRunning() const`

**作用与语义：**

如果事件循环正在运行，则返回`true`;否则返回false。事件循环从调用`exec()`到调用`exit()`之间被视为运行。

### `bool QEventLoop::processEvents(QEventLoop::ProcessEventsFlags flags = AllEvents)`

**作用与语义：**

处理一些与`flags`匹配的待处理事件。如果处理了待处理事件，返回`true`;否则返回`false`。
当你有一个运行时间较长的操作，并且希望在不允许用户输入的情况下显示其进度时，这个函数尤其有用;即通过使用`ExcludeUserInputEvents`标志。
这个函数只是`QAbstractEventDispatcher::processEvents()`的包装器。详情请参见该函数的文档。

### `[since 6.7] void QEventLoop::processEvents(QEventLoop::ProcessEventsFlags flags, QDeadlineTimer deadline)`

**作用与语义：**

处理与`flags`匹配的待处理事件，直到`deadline`过期或无更多事件可处理，以先发生者为准。该功能特别适用于运行时间较长且希望在不允许用户输入的情况下显示其进度，即使用`ExcludeUserInputEvents`标志。
注释：
- 该函数不连续处理事件;在处理完所有可用事件后返回。
- 指定`WaitForMoreEvents`标志无意义，将被忽略。

### `void QEventLoop::processEvents(QEventLoop::ProcessEventsFlags flags, int maxTime)`

**作用与语义：**

处理与`flags`匹配的待处理事件，最长为`maxTime`毫秒，或直到无更多事件可处理，以较短者为准。
相当于调用：

**官方示例：**

```cpp
 processEvents(flags, QDeadlineTimer(maxTime));
```

### `[slot] void QEventLoop::quit()`

**作用与语义：**

告诉事件循环正常退出。
与出口（0）同理。

### `void QEventLoop::wakeUp()`

**作用与语义：**

唤醒事件循环。

### `enum ProcessEventsFlag { AllEvents, ExcludeUserInputEvents, ExcludeSocketNotifiers, WaitForMoreEvents }`

**作用与语义：**

该枚举控制`processEvents()`函数处理的事件类型。
- `QEventLoop::AllEvents`：`0x00`;所有事件。注意`DeferredDelete`事件会被特别处理。详情请参见 `QObject::deleteLater()`。
- `QEventLoop::ExcludeUserInputEvents`：`0x01`;不要处理用户输入事件，如ButtonPress和KeyPress。注意，这些事件不会被丢弃;下次调用`processEvents()`时，事件会在没有ExcludeUserInputEvents标志的情况下被传递。
- `QEventLoop::ExcludeSocketNotifiers`：`0x02`;不要处理套接字通知事件。注意，这些事件不会被丢弃;下次调用`processEvents()`时，它们会被传递，而没有ExcludeSocketNotifiers标志。
- `QEventLoop::WaitForMoreEvents`：`0x04`;如果没有待处理事件，则等待事件。
ProcessEventsFlags 类型是 QFlags 的 typedef<ProcessEventsFlag>。它存储 ProcessEventsFlag 值的 OR 组合。

### `flags ProcessEventsFlags`

**作用与语义：**

该枚举控制`processEvents()`函数处理的事件类型。
- `QEventLoop::AllEvents`：`0x00`;所有事件。注意`DeferredDelete`事件会被特别处理。详情请参见 `QObject::deleteLater()`。
- `QEventLoop::ExcludeUserInputEvents`：`0x01`;不要处理用户输入事件，如ButtonPress和KeyPress。注意，这些事件不会被丢弃;下次调用`processEvents()`时，事件会在没有ExcludeUserInputEvents标志的情况下被传递。
- `QEventLoop::ExcludeSocketNotifiers`：`0x02`;不要处理套接字通知事件。注意，这些事件不会被丢弃;下次调用`processEvents()`时，它们会被传递，而没有ExcludeSocketNotifiers标志。
- `QEventLoop::WaitForMoreEvents`：`0x04`;如果没有待处理事件，则等待事件。
ProcessEventsFlags 类型是 QFlags 的 typedef<ProcessEventsFlag>。它存储 ProcessEventsFlag 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QEventLoop` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
