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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 18 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QDBusConnectionInterface::RegisterServiceReply`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDBusConnectionInterface` 暴露的类型声明 `注册、Service、Reply`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:RegisterServiceReply`。
- 属性名：`QDBusConnectionInterface`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QDBusConnectionInterface::ServiceQueueOptions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDBusConnectionInterface` 暴露的类型声明 `Service、Queue、Options`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ServiceQueueOptions`。
- 属性名：`QDBusConnectionInterface`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QDBusConnectionInterface::ServiceReplacementOptions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDBusConnectionInterface` 暴露的类型声明 `Service、Replacement、Options`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ServiceReplacementOptions`。
- 属性名：`QDBusConnectionInterface`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] activatableServiceNames : QDBusReply<QStringList>`

**API 类别：** 属性说明

**中文解读：** 这是 `QDBusConnectionInterface` 的状态/能力属性。通常通过 `activatableServiceNames()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QDBusReply<QStringList>`。
- 属性名：`activatableServiceNames`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] registeredServiceNames : QDBusReply<QStringList>`

**API 类别：** 属性说明

**中文解读：** 这是 `QDBusConnectionInterface` 的状态/能力属性。通常通过 `registeredServiceNames()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QDBusReply<QStringList>`。
- 属性名：`registeredServiceNames`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QDBusConnectionInterface::callWithCallbackFailed(const QDBusError &error, const QDBusMessage &call)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDBusConnectionInterface` 发出的通知信号 `callWithCallbackFailed`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `error`：类型为 `const QDBusError &`。没有默认值，调用时必须提供。错误输出对象或错误状态。解析/执行后要检查它，而不能只看主返回值。
- 参数 `call`：类型为 `const QDBusMessage &`。没有默认值，调用时必须提供。传入 `const QDBusMessage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] QDBusReply<bool> QDBusConnectionInterface::isServiceRegistered(const QString &serviceName) const`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `isServiceRegistered`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`QDBusReply<bool>`。
- 参数 `serviceName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] QDBusReply<QDBusConnectionInterface::RegisterServiceReply> QDBusConnectionInterface::registerService(const QString &serviceName, QDBusConnectionInterface::ServiceQueueOptions qoption = DontQueueService, QDBusConnectionInterface::ServiceReplacementOptions roption = DontAllowReplacement)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `registerService`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`QDBusReply<QDBusConnectionInterface::RegisterServiceReply>`。
- 参数 `serviceName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `qoption`：类型为 `QDBusConnectionInterface::ServiceQueueOptions`。默认值为 `DontQueueService`。传入 `QDBusConnectionInterface::ServiceQueueOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `roption`：类型为 `QDBusConnectionInterface::ServiceReplacementOptions`。默认值为 `DontAllowReplacement`。传入 `QDBusConnectionInterface::ServiceReplacementOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot, since 6.10] QDBusReply<QVariantMap> QDBusConnectionInterface::serviceCredentials(const QString &serviceName) const`

**API 类别：** 成员函数说明

**中文解读：** `QDBusConnectionInterface::serviceCredentials` 用于计算、查询或取得与“service、Credentials”相关的操作。调用时要先确认当前状态和 `serviceName` 的有效范围；返回类型是 `QDBusReply<QVariantMap>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDBusReply<QVariantMap>`。
- 参数 `serviceName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] QDBusReply<QString> QDBusConnectionInterface::serviceOwner(const QString &name) const`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `serviceOwner`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`QDBusReply<QString>`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] QDBusReply<uint> QDBusConnectionInterface::servicePid(const QString &serviceName) const`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `servicePid`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`QDBusReply<uint>`。
- 参数 `serviceName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QDBusConnectionInterface::serviceRegistered(const QString &service)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDBusConnectionInterface` 发出的通知信号 `serviceRegistered`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `service`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] QDBusReply<uint> QDBusConnectionInterface::serviceUid(const QString &serviceName) const`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `serviceUid`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`QDBusReply<uint>`。
- 参数 `serviceName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QDBusConnectionInterface::serviceUnregistered(const QString &service)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDBusConnectionInterface` 发出的通知信号 `serviceUnregistered`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `service`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] QDBusReply<void> QDBusConnectionInterface::startService(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `startService`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`QDBusReply<void>`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] QDBusReply<bool> QDBusConnectionInterface::unregisterService(const QString &serviceName)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `unregisterService`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`QDBusReply<bool>`。
- 参数 `serviceName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDBusReply<QStringList> activatableServiceNames() const`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `activatableServiceNames`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`QDBusReply<QStringList>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDBusReply<QStringList> registeredServiceNames() const`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `registeredServiceNames`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`QDBusReply<QStringList>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
