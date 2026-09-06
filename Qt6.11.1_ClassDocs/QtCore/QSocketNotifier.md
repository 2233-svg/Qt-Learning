# QSocketNotifier

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QSocketNotifier` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSocketNotifier` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QSocketNotifier>`
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

- `enum Type { Read, Write, Exception }`

### 公有函数

- `(since 6.1) QSocketNotifier(QSocketNotifier::Type type, QObject *parent = nullptr)`
- `QSocketNotifier(qintptr socket, QSocketNotifier::Type type, QObject *parent = nullptr)`
- `virtual ~QSocketNotifier()`
- `bool isEnabled() const`
- `(since 6.1) bool isValid() const`
- `(since 6.1) void setSocket(qintptr socket)`
- `qintptr socket() const`
- `QSocketNotifier::Type type() const`

### 公有槽函数

- `void setEnabled(bool enable)`

### 信号

- `void activated(QSocketDescriptor socket, QSocketNotifier::Type type)`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSocketNotifier::Type`

**作用与语义：**

该枚举描述了套接字通知器能够识别的各种事件类型。在构建套接字通知器时必须指定类型。
请注意，如果你需要同时监控同一文件描述符的读写，必须创建两个套接字通知符。还请注意，不可能在同一套接字上安装两个相同类型的套接字通知符（读、写、异常）。
- `QSocketNotifier::Read`：`0`;有数据需要读取。
- `QSocketNotifier::Write`：`1`;数据可以写入。
- `QSocketNotifier::Exception`：`2`;发生了例外情况。我们建议不要使用此方法。

### `[explicit, since 6.1] QSocketNotifier::QSocketNotifier(QSocketNotifier::Type type, QObject *parent = nullptr)`

**作用与语义：**

构造一个带有给定`type`且未分配描述符的套接字通知符。`parent`参数传递给`QObject`的构造函数。
调用`setSocket()`函数来设置监控描述符。

### `QSocketNotifier::QSocketNotifier(qintptr socket, QSocketNotifier::Type type, QObject *parent = nullptr)`

**作用与语义：**

构建带有给定`parent`的套接字通知器。它启用`socket`，并监控给定`type`的事件。
通常建议明确启用或禁用套接字通知，尤其是写入通知。
给Windows用户的提示：传递给QSocketNotifier的套接字会变成非阻塞套接字，即使它是作为阻塞套接字创建的。

### `[virtual noexcept] QSocketNotifier::~QSocketNotifier()`

**作用与语义：**

摧毁了这个槽函数通知器。

### `[private signal] void QSocketNotifier::activated(QSocketDescriptor socket, QSocketNotifier::Type type)`

**作用与语义：**

每当套接字通知器被启用且发生与其`type`对应的套接字事件时，该信号就会发出。
套接字标识符通过`socket`参数传递。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。
注意：该信号重载。连接此信号：


使用 qOverload 连接：
connect（socketNotifier， qOverload（&QSocketNotifier：：activated），。
receiver， &ReceiverClass：：slot）;

或者用λ：
connect（socketNotifier， qOverload（&QSocketNotifier：：activated），。
this， []（QSocketDescriptor socket， QSocketNotifier：：Type type） { /* handle activated */ }）;


更多示例和方法，请参见连接重载信号。

### `[override virtual protected] bool QSocketNotifier::event(QEvent *e)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。
该虚拟函数接收对象事件，如果事件`e`被识别并处理，应返回真。
event() 函数可以重新实现，以自定义对象的行为。
确保你调用所有未处理的事件的父事件类实现。

### `bool QSocketNotifier::isEnabled() const`

**作用与语义：**

如果通知器已启用，则返回 `true`；否则返回 `false`。

### `[since 6.1] bool QSocketNotifier::isValid() const`

**作用与语义：**

如果通知器有效（即已分配描述符），则返回 `true`；否则返回 `false`。

### `[slot] void QSocketNotifier::setEnabled(bool enable)`

**作用与语义：**

如果`enable`为真，则通知器被启用;否则通知器被禁用。
启用通知器时，每当出现对应其`type`的套接字事件时，它就会发出`activated()`信号。禁用时，则忽略套接字事件（即未创建该套接字通知器）。
写入通知器通常应在`activated()`信号发出后立即禁用。

### `[since 6.1] void QSocketNotifier::setSocket(qintptr socket)`

**作用与语义：**

将`socket`分配给该通知者。
注意：通知器将作为副作用被禁用，需要重新启用。

### `qintptr QSocketNotifier::socket() const`

**作用与语义：**

返回分配给该对象的套接字标识符。

### `QSocketNotifier::Type QSocketNotifier::type() const`

**作用与语义：**

返回分配给构造函数的套接字事件类型。

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

`QSocketNotifier` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
