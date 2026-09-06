# QDBusServiceWatcher

> Qt 6.11.1 · Qt D-Bus

## 1. 先建立直觉

**一句话定位：** `QDBusServiceWatcher` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt D-Bus 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QDBusServiceWatcher` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QDBusServiceWatcher>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
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

- `flags WatchMode`
- `enum WatchModeFlag { WatchForRegistration, WatchForUnregistration, WatchForOwnerChange }`

### 属性

- `watchMode : WatchMode`
- `watchedServices : QStringList`

### 公有函数

- `QDBusServiceWatcher(QObject *parent = nullptr)`
- `QDBusServiceWatcher(const QString &service, const QDBusConnection &connection, QDBusServiceWatcher::WatchMode watchMode = WatchForOwnerChange, QObject *parent = nullptr)`
- `virtual ~QDBusServiceWatcher()`
- `void addWatchedService(const QString &newService)`
- `QBindable<QDBusServiceWatcher::WatchMode> bindableWatchMode()`
- `QBindable<QStringList> bindableWatchedServices()`
- `QDBusConnection connection() const`
- `bool removeWatchedService(const QString &service)`
- `void setConnection(const QDBusConnection &connection)`
- `void setWatchMode(QDBusServiceWatcher::WatchMode mode)`
- `void setWatchedServices(const QStringList &services)`
- `QDBusServiceWatcher::WatchMode watchMode() const`
- `QStringList watchedServices() const`

### 信号

- `void serviceOwnerChanged(const QString &serviceName, const QString &oldOwner, const QString &newOwner)`
- `void serviceRegistered(const QString &serviceName)`
- `void serviceUnregistered(const QString &serviceName)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDBusServiceWatcher::WatchModeFlagflags QDBusServiceWatcher::WatchMode`

**作用与语义：**

`QDBusServiceWatcher`支持三种不同的手表模式，这些模式由以下标志配置：
- `QDBusServiceWatcher::WatchForRegistration`：`0x01`;仅关注服务注册，忽略与其他服务所有权变更相关的信号。
- `QDBusServiceWatcher::WatchForUnregistration`：`0x02`;仅关注服务取消注册，忽略其他服务所有权变更相关的信号。
- `QDBusServiceWatcher::WatchForOwnerChange`：`0x03`;注意任何形式的服务所有权变更。
WatchMode 类型是 QFlags 的 typedef<WatchModeFlag>。它存储 WatchModeFlag 值的 OR 组合。

### `[bindable] watchMode : WatchMode`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含该`QDBusServiceWatcher`对象当前的观察模式。
该属性的默认值为 QDBusServiceWatcher：：WatchForOwnershipChange。

**如何使用：** 调用 `watchMode()` 读取当前值；它不会修改应用状态。

### `[bindable] watchedServices : QStringList`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该地产拥有被关注的服务名单。
注意：使用 setServicesWatched() 修改该列表是一项昂贵的操作。如果可以，建议通过`addWatchedService()`和`removeWatchedService()`来更改。

**如何使用：** 调用 `watchedServices()` 读取当前值；它不会修改应用状态。

### `[explicit] QDBusServiceWatcher::QDBusServiceWatcher(QObject *parent = nullptr)`

**作用与语义：**

创建一个QDBusServiceWatcher对象。注意，在你与`setConnection()`建立连接之前，这个对象不会发出任何信号。
`parent`参数传递给`QObject`以设置该对象的父节点。

### `QDBusServiceWatcher::QDBusServiceWatcher(const QString &service, const QDBusConnection &connection, QDBusServiceWatcher::WatchMode watchMode = WatchForOwnerChange, QObject *parent = nullptr)`

**作用与语义：**

创建 QDBusServiceWatcher 对象并将其附加到 `connection` 连接。此外，该函数会立即开始监控服务`service`的`watchMode`变更。
`parent`参数传递给`QObject`以设置该对象的父节点。

### `[virtual noexcept] QDBusServiceWatcher::~QDBusServiceWatcher()`

**作用与语义：**

销毁`QDBusServiceWatcher`对象并释放与之相关的资源。

### `void QDBusServiceWatcher::addWatchedService(const QString &newService)`

**作用与语义：**

将该对象需要监控的服务列表增加`newService`。该函数比`setWatchedServices()`更高效，应尽可能用于添加服务。
移除任何现有的`watchedServices`绑定。

### `QDBusConnection QDBusServiceWatcher::connection() const`

**作用与语义：**

返回此对象所附加的 `QDBusConnection`。

### `bool QDBusServiceWatcher::removeWatchedService(const QString &service)`

**作用与语义：**

将该`service`从该对象监控的服务列表中移除。注意D-Bus通知是异步的，因此可能仍有约`service`的信号等待传递。每当D-Bus消息被处理时，这些信号仍会被发出。
移除任何现有的绑定`watchedServices`。
如果有服务被移除，该函数会返回`true`。

### `[signal] void QDBusServiceWatcher::serviceOwnerChanged(const QString &serviceName, const QString &oldOwner, const QString &newOwner)`

**作用与语义：**

每当该对象检测到与`serviceName`服务相关的服务所有权发生变更时，就会发出该信号。`oldOwner`参数包含旧所有者名称，`newOwner`为新所有者。`oldOwner`和`newOwner`都是唯一的连接名称。
注意，该信号在`serviceName`服务注册或未注册时也会发出。如果注册，`oldOwner`包含空字符串;如果未注册，`newOwner`包含空字符串。
如果你只需要知道服务是注册还是未注册，而不需要通知所有权变更，可以考虑使用这些操作的特定模式。如果你使用更具体的模式，这类操作会更高效。

### `[signal] void QDBusServiceWatcher::serviceRegistered(const QString &serviceName)`

**作用与语义：**

每当该物体检测到服务`serviceName`在总线上可用时，就会发出该信号。

### `[signal] void QDBusServiceWatcher::serviceUnregistered(const QString &serviceName)`

**作用与语义：**

每当该对象检测到服务`serviceName`未注册且不再可用时，就会发出该信号。

### `void QDBusServiceWatcher::setConnection(const QDBusConnection &connection)`

**作用与语义：**

将该对象所连接的D-Bus连接设置为`connection`。所有被监控的服务都会被转移到该连接。
注意`QDBusConnection`对象是引用计数的：`QDBusServiceWatcher`会在连接存在时保留引用。连接直到引用计数降至零才关闭，因此确保在该`QDBusServiceWatcher`对象存在期间收到任何通知。

### `void QDBusServiceWatcher::setWatchedServices(const QStringList &services)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该地产拥有被关注的服务名单。
注意：使用 setServicesWatched() 修改该列表是一项昂贵的操作。如果可以，建议通过`addWatchedService()`和`removeWatchedService()`来更改。

**如何使用：** 调用 `setWatchedServices(...)` 修改 `watchedServices`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QStringList QDBusServiceWatcher::watchedServices() const`

**作用与语义：**

返回正在监控的D-Bus服务列表。
注意：服务对象的获取功能。

### `flags WatchMode`

**作用与语义：**

`QDBusServiceWatcher`支持三种不同的手表模式，这些模式由以下标志配置：
- `QDBusServiceWatcher::WatchForRegistration`：`0x01`;仅关注服务注册，忽略与其他服务所有权变更相关的信号。
- `QDBusServiceWatcher::WatchForUnregistration`：`0x02`;仅关注服务取消注册，忽略其他服务所有权变更相关的信号。
- `QDBusServiceWatcher::WatchForOwnerChange`：`0x03`;注意任何形式的服务所有权变更。
WatchMode 类型是 QFlags 的 typedef<WatchModeFlag>。它存储 WatchModeFlag 值的 OR 组合。

### `enum WatchModeFlag { WatchForRegistration, WatchForUnregistration, WatchForOwnerChange }`

**作用与语义：**

`QDBusServiceWatcher`支持三种不同的手表模式，这些模式由以下标志配置：
- `QDBusServiceWatcher::WatchForRegistration`：`0x01`;仅关注服务注册，忽略与其他服务所有权变更相关的信号。
- `QDBusServiceWatcher::WatchForUnregistration`：`0x02`;仅关注服务取消注册，忽略其他服务所有权变更相关的信号。
- `QDBusServiceWatcher::WatchForOwnerChange`：`0x03`;注意任何形式的服务所有权变更。
WatchMode 类型是 QFlags 的 typedef<WatchModeFlag>。它存储 WatchModeFlag 值的 OR 组合。

### `QBindable<QDBusServiceWatcher::WatchMode> bindableWatchMode()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含该`QDBusServiceWatcher`对象当前的观察模式。
该属性的默认值为 QDBusServiceWatcher：：WatchForOwnershipChange。

**如何使用：** 调用 `bindableWatchMode()` 取得 `watchMode` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<QStringList> bindableWatchedServices()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该地产拥有被关注的服务名单。
注意：使用 setServicesWatched() 修改该列表是一项昂贵的操作。如果可以，建议通过`addWatchedService()`和`removeWatchedService()`来更改。

**如何使用：** 调用 `bindableWatchedServices()` 取得 `watchedServices` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `void setWatchMode(QDBusServiceWatcher::WatchMode mode)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含该`QDBusServiceWatcher`对象当前的观察模式。
该属性的默认值为 QDBusServiceWatcher：：WatchForOwnershipChange。

**如何使用：** 调用 `setWatchMode(...)` 修改 `watchMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QDBusServiceWatcher::WatchMode watchMode() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含该`QDBusServiceWatcher`对象当前的观察模式。
该属性的默认值为 QDBusServiceWatcher：：WatchForOwnershipChange。

**如何使用：** 调用 `watchMode()` 读取当前值；它不会修改应用状态。

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

`QDBusServiceWatcher` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
