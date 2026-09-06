# QDBusConnectionInterface

> Qt 6.11.1 · Qt D-Bus

## 1. 先建立直觉

**一句话定位：** 这是一个抽象接口或框架基类，重点是理解它定义的协议，并通过具体子类、工厂或回调来使用。

**模块背景：** 这是 Qt D-Bus 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QDBusConnectionInterface` 是 Qt D-Bus 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QDBusConnectionInterface>`
- 继承自：QDBusAbstractInterface
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum RegisterServiceReply { ServiceNotRegistered, ServiceRegistered, ServiceQueued }`
- `enum ServiceQueueOptions { DontQueueService, QueueService, ReplaceExistingService }`
- `enum ServiceReplacementOptions { DontAllowReplacement, AllowReplacement }`

### 属性

- `activatableServiceNames : QDBusReply<QStringList>`
- `registeredServiceNames : QDBusReply<QStringList>`

### 公有槽函数

- `QDBusReply<QStringList> activatableServiceNames() const`
- `QDBusReply<bool> isServiceRegistered(const QString &serviceName) const`
- `QDBusReply<QDBusConnectionInterface::RegisterServiceReply> registerService(const QString &serviceName, QDBusConnectionInterface::ServiceQueueOptions qoption = DontQueueService, QDBusConnectionInterface::ServiceReplacementOptions roption = DontAllowReplacement)`
- `QDBusReply<QStringList> registeredServiceNames() const`
- `(since 6.10) QDBusReply<QVariantMap> serviceCredentials(const QString &serviceName) const`
- `QDBusReply<QString> serviceOwner(const QString &name) const`
- `QDBusReply<uint> servicePid(const QString &serviceName) const`
- `QDBusReply<uint> serviceUid(const QString &serviceName) const`
- `QDBusReply<void> startService(const QString &name)`
- `QDBusReply<bool> unregisterService(const QString &serviceName)`

### 信号

- `void callWithCallbackFailed(const QDBusError &error, const QDBusMessage &call)`
- `void serviceRegistered(const QString &service)`
- `void serviceUnregistered(const QString &service)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDBusConnectionInterface::RegisterServiceReply`

**作用与语义：**

`registerService()`可能的返回值：
- `QDBusConnectionInterface::ServiceNotRegistered`：`0`;调用失败，服务名称未被注册。
- `QDBusConnectionInterface::ServiceRegistered`：`1`;调用者现在是服务名称的所有者。
- `QDBusConnectionInterface::ServiceQueued`：`2`;调用者指定了`QueueService`标志，服务已注册，因此我们处于队列中。
当该应用获得服务时，`serviceRegistered()`信号将被发射。

### `enum QDBusConnectionInterface::ServiceQueueOptions`

**作用与语义：**

用于确定服务注册应如何行为的标志，如果服务名称已经注册。
- `QDBusConnectionInterface::DontQueueService`：`0`;如果应用程序请求已拥有的名称，则不会进行队列。registeredService() 调用将直接失败。这是默认设置。
- `QDBusConnectionInterface::QueueService`：`1`;尝试注册请求的服务，但如果已有其他应用注册，则不尝试替换。只需将该应用放入队列，直到放弃为止。此时`serviceRegistered()`信号将被发射。
- `QDBusConnectionInterface::ReplaceExistingService`：`2`;如果其他应用程序已经注册了该服务名称，尝试替换它。

### `enum QDBusConnectionInterface::ServiceReplacementOptions`

**作用与语义：**

用于判断 D-Bus 服务器是否应允许其他应用程序用 `ReplaceExistingService` 选项替换该应用已注册的名称的标志。
可能的数值如下：
- `QDBusConnectionInterface::DontAllowReplacement`：`0`;不要允许其他应用取代我们。该服务必须明确未注册于`unregisterService()`，其他应用才能获得。这是默认情况。
- `QDBusConnectionInterface::AllowReplacement`：`1`;允许其他应用以`ReplaceExistingService`选择无需干预即可`registerService()`我们。如果发生这种情况，`serviceUnregistered()`信号将被发射。

### `[read-only] activatableServiceNames : QDBusReply<QStringList>`

**作用与语义：**

保持可激活的服务名称。
列出所有可以在公交车上激活的名称。

**如何使用：** 调用 `activatableServiceNames()` 读取当前值；它不会修改应用状态。

### `[read-only] registeredServiceNames : QDBusReply<QStringList>`

**作用与语义：**

持有注册的服务名称。
列出目前在公交车上登记的所有姓名。

**如何使用：** 调用 `registeredServiceNames()` 读取当前值；它不会修改应用状态。

### `[signal] void QDBusConnectionInterface::callWithCallbackFailed(const QDBusError &error, const QDBusMessage &call)`

**作用与语义：**

当`QDBusConnection::callWithCallback()`中出现错误时，该信号会发出。`error` 指定错误。`call` 是无法传递的消息。

### `[slot] QDBusReply<bool> QDBusConnectionInterface::isServiceRegistered(const QString &serviceName) const`

**作用与语义：**

如果`serviceName`拥有的服务名称目前已注册，返回`true`。

### `[slot] QDBusReply<QDBusConnectionInterface::RegisterServiceReply> QDBusConnectionInterface::registerService(const QString &serviceName, QDBusConnectionInterface::ServiceQueueOptions qoption = DontQueueService, QDBusConnectionInterface::ServiceReplacementOptions roption = DontAllowReplacement)`

**作用与语义：**

总线上`serviceName`注册服务名称的请求。`qoption`标志规定了如果D-Bus服务器已经注册`serviceName`应如何表现。`roption`标志表示服务器是否应允许其他应用程序替换我们的注册名称。
如果服务注册成功，`serviceRegistered()`信号将被发出。如果我们被列入队列，获得名称时信号会被发出。如果`roption` `AllowReplacement`，如果有其他应用程序替换，`serviceUnregistered()`信号将被发出。

### `[slot, since 6.10] QDBusReply<QVariantMap> QDBusConnectionInterface::serviceCredentials(const QString &serviceName) const`

**作用与语义：**

返回当前持有总线服务`serviceName`进程的连接凭据。
更多信息请参见<https://dbus.freedesktop.org/doc/dbus-specification.html>部分：“方法：org.freedesktop.DBus.GetConnectionCredentials”。

### `[slot] QDBusReply<QString> QDBusConnectionInterface::serviceOwner(const QString &name) const`

**作用与语义：**

返回该名称的主要所有者的唯一连接名称`name`。如果请求的名称没有所有者，则返回`org.freedesktop.DBus.Error.NameHasNoOwner`错误。

### `[slot] QDBusReply<uint> QDBusConnectionInterface::servicePid(const QString &serviceName) const`

**作用与语义：**

返回当前承载总线服务`serviceName`进程的Unix进程ID（PID）。

### `[signal] void QDBusConnectionInterface::serviceRegistered(const QString &service)`

**作用与语义：**

当该应用获取`service`提供的总线服务名称（唯一连接名称或知名服务名称）时，D-总线服务器会发出该信号。
获取是在该应用请求使用名称`registerService()`之后进行的。

### `[slot] QDBusReply<uint> QDBusConnectionInterface::serviceUid(const QString &serviceName) const`

**作用与语义：**

返回当前持有总线服务`serviceName`进程的Unix用户ID（UID）。

### `[signal] void QDBusConnectionInterface::serviceUnregistered(const QString &service)`

**作用与语义：**

当该应用失去`service`分配的总线服务名称所有权时，D-Bus服务器会发出该信号。

### `[slot] QDBusReply<void> QDBusConnectionInterface::startService(const QString &name)`

**作用与语义：**

请求公交车开始以“`name`”命名的服务。

### `[slot] QDBusReply<bool> QDBusConnectionInterface::unregisterService(const QString &serviceName)`

**作用与语义：**

释放之前已注册于`registerService()`的公交服务名称`serviceName`的权利要求。如果该应用拥有该名称的所有权，将被释放给其他申请申请。如果仅排队该名称，则放弃其在队列中的位置。

### `QDBusReply<QStringList> activatableServiceNames() const`

**作用与语义：**

保持可激活的服务名称。
列出所有可以在公交车上激活的名称。

**如何使用：** 调用 `activatableServiceNames()` 读取当前值；它不会修改应用状态。

### `QDBusReply<QStringList> registeredServiceNames() const`

**作用与语义：**

持有注册的服务名称。
列出目前在公交车上登记的所有姓名。

**如何使用：** 调用 `registeredServiceNames()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QDBusConnectionInterface` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
