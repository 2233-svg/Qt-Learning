# QSignalMapper

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QSignalMapper` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSignalMapper` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QSignalMapper>`
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

### 公有函数

- `QSignalMapper(QObject *parent = nullptr)`
- `virtual ~QSignalMapper()`
- `QObject * mapping(int id) const`
- `QObject * mapping(QObject *object) const`
- `QObject * mapping(const QString &id) const`
- `void removeMappings(QObject *sender)`
- `void setMapping(QObject *sender, QObject *object)`
- `void setMapping(QObject *sender, const QString &text)`
- `void setMapping(QObject *sender, int id)`

### 公有槽函数

- `void map()`
- `void map(QObject *sender)`

### 信号

- `void mappedInt(int i)`
- `void mappedObject(QObject *object)`
- `void mappedString(const QString &text)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QSignalMapper::QSignalMapper(QObject *parent = nullptr)`

**作用与语义：**

构建带有父 `parent` 的 QSignalMapper 。

### `[virtual noexcept] QSignalMapper::~QSignalMapper()`

**作用与语义：**

摧毁了`QSignalMapper`。

### `[slot] void QSignalMapper::map()`

**作用与语义：**

该槽根据向其发送信号的物体发出信号。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
signalMapper，qOverload<>（&QSignalMapper：：map））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
signalMapper，[接收器 = signalMapper]() { receiver->map(); }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] void QSignalMapper::map(QObject *sender)`

**作用与语义：**

该槽根据`sender`对象发出信号。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
signalMapper， qOverload（&QSignalMapper：：map））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
signalMapper，[接收器 = signalMapper]（QObject *发送器） { 接收器->map（sender）; }）;


更多示例和方法，请参见连接超载槽位。

### `[signal] void QSignalMapper::mappedInt(int i)`

**作用与语义：**

当`map()`信号来自具有整数映射集的对象时，该信号会发出。该物体的映射整数以`i`方式传递。

### `[signal] void QSignalMapper::mappedObject(QObject *object)`

**作用与语义：**

当`map()`从具有对象映射设置的对象发出信号时，该信号会发出。映射提供的对象会以 `object` 传递。

### `[signal] void QSignalMapper::mappedString(const QString &text)`

**作用与语义：**

当`map()`从具有字符串映射设置的对象发出信号时，该信号会发出。该对象的映射字符串会以 `text` 方式传递。

### `QObject *QSignalMapper::mapping(int id) const`

**作用与语义：**

返回与`id`关联的发送方`QObject`。

### `QObject *QSignalMapper::mapping(QObject *object) const`

**作用与语义：**

返回与`object`关联的发送方`QObject`。
注意：该功能会让`QSignalMapper::mapping()`重载。

### `QObject *QSignalMapper::mapping(const QString &id) const`

**作用与语义：**

注意：该功能会让`QSignalMapper::mapping()`重载。

### `void QSignalMapper::removeMappings(QObject *sender)`

**作用与语义：**

移除所有`sender`的映射。
当映射对象被摧毁时，会自动完成。
注意：这并不会断开任何信号。如果没有`sender`销毁，则需要明确地进行此操作。

### `void QSignalMapper::setMapping(QObject *sender, QObject *object)`

**作用与语义：**

添加映射，使得当`map()`从`sender`发出信号时，信号`mappedObject`（`object`）会被发射。
每个发送者最多只能有一个对象。

### `void QSignalMapper::setMapping(QObject *sender, const QString &text)`

**作用与语义：**

添加映射，使得当`map()`从`sender`接收信号时，信号`mappedString`（`text`）被发射。
每位发件人最多只能收到一条短信。

### `void QSignalMapper::setMapping(QObject *sender, int id)`

**作用与语义：**

添加映射，使得当`map()`从给定`sender`发出信号时，信号 `mappedInt`（`id`）被发射。
每个发送者最多只能有一个整数ID。

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

`QSignalMapper` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
