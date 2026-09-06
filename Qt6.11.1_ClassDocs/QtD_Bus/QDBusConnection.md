# QDBusConnection

> Qt 6.11.1 · Qt D-Bus

## 1. 先建立直觉

**一句话定位：** 这是 Qt D-Bus 中围绕“DBus连接”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** 这是 Qt D-Bus 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QDBusConnection` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QDBusConnection>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum BusType { SessionBus, SystemBus, ActivationBus }`
- `flags ConnectionCapabilities`
- `enum ConnectionCapability { UnixFileDescriptorPassing }`
- `enum RegisterOption { ExportAdaptors, ExportScriptableSlots, ExportScriptableSignals, ExportScriptableProperties, ExportScriptableInvokables, …, ExportChildObjects }`
- `flags RegisterOptions`
- `enum UnregisterMode { UnregisterNode, UnregisterTree }`

### 公有函数

- `QDBusConnection(const QString &name)`
- `QDBusConnection(const QDBusConnection &other)`
- `~QDBusConnection()`
- `QDBusPendingCall asyncCall(const QDBusMessage &message, int timeout = -1) const`
- `QString baseService() const`
- `QDBusMessage call(const QDBusMessage &message, QDBus::CallMode mode = QDBus::Block, int timeout = -1) const`
- `bool callWithCallback(const QDBusMessage &message, QObject *receiver, const char *returnMethod, const char *errorMethod, int timeout = -1) const`
- `bool connect(const QString &service, const QString &path, const QString &interface, const QString &name, QObject *receiver, const char *slot)`
- `bool connect(const QString &service, const QString &path, const QString &interface, const QString &name, const QString &signature, QObject *receiver, const char *slot)`
- `bool connect(const QString &service, const QString &path, const QString &interface, const QString &name, const QStringList &argumentMatch, const QString &signature, QObject *receiver, const char *slot)`
- `QDBusConnection::ConnectionCapabilities connectionCapabilities() const`
- `bool disconnect(const QString &service, const QString &path, const QString &interface, const QString &name, QObject *receiver, const char *slot)`
- `bool disconnect(const QString &service, const QString &path, const QString &interface, const QString &name, const QString &signature, QObject *receiver, const char *slot)`
- `bool disconnect(const QString &service, const QString &path, const QString &interface, const QString &name, const QStringList &argumentMatch, const QString &signature, QObject *receiver, const char *slot)`
- `QDBusConnectionInterface * interface() const`
- `bool isConnected() const`
- `QDBusError lastError() const`
- `QString name() const`
- `QObject * objectRegisteredAt(const QString &path) const`
- `bool registerObject(const QString &path, QObject *object, QDBusConnection::RegisterOptions options = ExportAdaptors)`
- `bool registerObject(const QString &path, const QString &interface, QObject *object, QDBusConnection::RegisterOptions options = ExportAdaptors)`
- `bool registerService(const QString &serviceName)`
- `bool send(const QDBusMessage &message) const`
- `void swap(QDBusConnection &other)`
- `void unregisterObject(const QString &path, QDBusConnection::UnregisterMode mode = UnregisterNode)`
- `bool unregisterService(const QString &serviceName)`
- `QDBusConnection & operator=(const QDBusConnection &other)`

### 静态公有成员

- `QDBusConnection connectToBus(QDBusConnection::BusType type, const QString &name)`
- `QDBusConnection connectToBus(const QString &address, const QString &name)`
- `QDBusConnection connectToPeer(const QString &address, const QString &name)`
- `void disconnectFromBus(const QString &name)`
- `void disconnectFromPeer(const QString &name)`
- `QByteArray localMachineId()`
- `QDBusConnection sessionBus()`
- `QDBusConnection systemBus()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDBusConnection::BusType`

**作用与语义：**

指定总线连接类型。有效的总线类型有：
- `QDBusConnection::SessionBus`：`0`;与运行中的桌面会话相关的会话总线
- `QDBusConnection::SystemBus`：`1`;系统总线，用于与系统级进程通信
- `QDBusConnection::ActivationBus`：`2`;激活总线，是启动该服务总线的“别名”。
在会话总线上，可以找到同一用户的其他应用程序共享同一桌面会话（因此得名）。而在系统总线上，通常会找到整个系统共享的进程。

### `enum QDBusConnection::ConnectionCapabilityflags QDBusConnection::ConnectionCapabilities`

**作用与语义：**

本枚举描述了D-总线连接的可用能力。
- `QDBusConnection::UnixFileDescriptorPassing`：`0x0001`;支持将Unix文件描述符传递给其他进程（见 `QDBusUnixFileDescriptor`）
ConnectionCapabilities类型是QFlag的typedef<ConnectionCapability>。它存储ConnectionCapability值的或组合。

### `enum QDBusConnection::RegisterOptionflags QDBusConnection::RegisterOptions`

**作用与语义：**

指定连接中注册对象的选项。可能的值如下：
- `QDBusConnection::ExportAdaptors`：`0x01`;导出该对象中适配器的内容
- `QDBusConnection::ExportScriptableSlots`：`0x10`;导出该对象可脚本的槽位
- `QDBusConnection::ExportScriptableSignals`：`0x20`;导出该对象的脚本化信号
- `QDBusConnection::ExportScriptableProperties`：`0x40`;导出该对象的脚本属性
- `QDBusConnection::ExportScriptableInvokables`：`0x80`;导出该对象可脚本调用的调用
- `QDBusConnection::ExportScriptableContents`：`0xf0`;ExportScriptableSlots 的简写形式 |ExportScriptableSignals |ExportScriptableProperties
- `QDBusConnection::ExportNonScriptableSlots`：`0x100`;导出该对象的非脚本槽
- `QDBusConnection::ExportNonScriptableSignals`：`0x200`;导出该对象的非脚本信号
- `QDBusConnection::ExportNonScriptableProperties`：`0x400`;导出该对象的非脚本属性
- `QDBusConnection::ExportNonScriptableInvokables`：`0x800`;导出该对象不可脚本调用的
- `QDBusConnection::ExportNonScriptableContents`：`0xf00`;导出非脚本槽的简写形式 |导出非脚本化信号 |导出非脚本属性
- `QDBusConnection::ExportAllSlots`：`ExportScriptableSlots|ExportNonScriptableSlots`;导出该物体的所有槽位
- `QDBusConnection::ExportAllSignals`：`ExportScriptableSignals|ExportNonScriptableSignals`;导出该物体的所有信号
- `QDBusConnection::ExportAllProperties`：`ExportScriptableProperties|ExportNonScriptableProperties`;导出该对象的所有属性
- `QDBusConnection::ExportAllInvokables`：`ExportScriptableInvokables|ExportNonScriptableInvokables`;导出该对象的所有可调用项
- `QDBusConnection::ExportAllContents`：`ExportScriptableContents|ExportNonScriptableContents`;导出该对象的所有内容
- `QDBusConnection::ExportChildObjects`：`0x1000`;导出该对象的子对象
RegisterOptions 类型是 QFlags 的 typedef<RegisterOption>。它存储 RegisterOption 值的 OR 组合。

### `enum QDBusConnection::UnregisterMode`

**作用与语义：**

取消注册对象路径的模式：
- `QDBusConnection::UnregisterNode`：`0`;仅取消注册该节点：不要取消注册子节点
- `QDBusConnection::UnregisterTree`：`1`;取消注册该节点及其所有子树
但请注意，如果该对象被`ExportChildObjects`选项注册，UnregisterNode 也会取消子对象的注册。

### `[explicit] QDBusConnection::QDBusConnection(const QString &name)`

**作用与语义：**

创建一个名为 `name` 的连接对象。
这并不能打开连接。你必须打电话给`connectToBus()`才能打开。

### `QDBusConnection::QDBusConnection(const QDBusConnection &other)`

**作用与语义：**

创建`other`连接的副本。

### `[noexcept] QDBusConnection::~QDBusConnection()`

**作用与语义：**

处理该对象。这不会关闭连接：你必须调用`disconnectFromBus()`才能完成。

### `QDBusPendingCall QDBusConnection::asyncCall(const QDBusMessage &message, int timeout = -1) const`

**作用与语义：**

通过该连接发送`message`并立即返回。该函数仅适用于方法调用。它返回一个类型为`QDBusPendingCall`的对象，可用于跟踪回复状态。
如果`timeout`毫秒内未收到回复，将自动发送错误，表示调用已过期。默认`timeout`为-1，通常为实现定义的值，适用于进程间通信（通常为25秒）。该超时也是QDBusPendingCall：：waitForFinished()中等待的上限。
请参见`QDBusInterface::asyncCall()`函数，了解如何更友好地调用电话。
注意：由于实现限制，应用程序自身注册对象的方法调用从不异步。

### `QString QDBusConnection::baseService() const`

**作用与语义：**

如果该`QDBusConnection`对象连接，返回该连接的唯一连接名称;否则返回空`QString`。
唯一连接名称是D-Bus服务器守护进程在连接时分配的字符串，形式为“：x.xxx”（其中x为十进制数字）。它唯一标识该客户端在总线中。
该函数返回一个空`QString`，用于点对点连接。

### `QDBusMessage QDBusConnection::call(const QDBusMessage &message, QDBus::CallMode mode = QDBus::Block, int timeout = -1) const`

**作用与语义：**

通过该连接发送`message`，并屏蔽等待回复，最多停留`timeout`毫秒。该函数仅适用于方法调用。它返回回复消息作为返回值，返回值类型为`QDBusMessage::ReplyMessage`或`QDBusMessage::ErrorMessage`。
如果`timeout`毫秒内未收到回复，将自动发送错误，表示调用已过期。默认`timeout`为-1，通常为实现定义的值，适用于进程间通信（通常为25秒）。
请参见`QDBusInterface::call()`函数，了解如何更友好地调用电话。
警告：如果`mode` `QDBus::BlockWithGui`，该函数将重新进入Qt事件循环以等待回复。等待期间，它可能会向你的应用程序发送信号和其他方法调用。因此，必须准备好在调用调用 call()时处理重入。

### `bool QDBusConnection::callWithCallback(const QDBusMessage &message, QObject *receiver, const char *returnMethod, const char *errorMethod, int timeout = -1) const`

**作用与语义：**

通过该连接发送`message`并立即返回。收到回复后，`receiver`对象中调用方法`returnMethod`。如果发生错误，则调用方法`errorMethod`。
如果`timeout`毫秒内未收到回复，将自动发送错误，表示调用已过期。默认`timeout`为-1，通常为实现定义的值，适用于进程间通信（通常为25秒）。
该函数仅适用于方法调用。只要参数类型匹配且无错误，确保该槽只被调用一次并响应。
如果消息已发送，则返回`true`;如果无法发送消息，则返回false。

### `bool QDBusConnection::connect(const QString &service, const QString &path, const QString &interface, const QString &name, QObject *receiver, const char *slot)`

**作用与语义：**

将`service`、`path`、`interface`和`name`参数指定的信号连接到对象`receiver`的槽函数`slot`。参数`service`和`path`可以为空，表示连接到来自任何远程应用的（`interface`、`name`）对中的任何信号。
如果连接成功，返回`true`。
警告：只有参数匹配时，信号才会送达槽函数。此验证只能在信号接收时进行，不能在连接时进行。

### `bool QDBusConnection::connect(const QString &service, const QString &path, const QString &interface, const QString &name, const QString &signature, QObject *receiver, const char *slot)`

**作用与语义：**

将信号连接到对象`receiver`的槽函数`slot`。与之前的connect()重载不同，该函数允许使用`signature`变量指定要连接的参数签名。函数随后会验证该签名是否能传递到`slot`指定的槽函数，否则返回false。
如果连接成功，返回`true`。
注意：该函数验证信号签名是否与槽函数参数匹配，但不验证实际信号是否存在于该签名的远程服务中。

### `bool QDBusConnection::connect(const QString &service, const QString &path, const QString &interface, const QString &name, const QStringList &argumentMatch, const QString &signature, QObject *receiver, const char *slot)`

**作用与语义：**

将信号连接到对象`receiver`的槽函数`slot`。与之前的connect()重载不同，该函数允许使用`signature`变量指定要连接的参数签名。函数随后会验证该签名是否能传递到`slot`指定的槽函数，否则返回false。
`argumentMatch`参数按顺序列出了需要匹配的字符串参数。注意，要匹配空字符串，你需要传递一个空但非空的`QString`（即`QString`（“”））。空`QString`跳过该位置的匹配。
如果连接成功，返回`true`。
注意：该函数验证信号签名是否与槽函数参数匹配，但不验证实际信号是否存在于该签名的远程服务中。

### `[static] QDBusConnection QDBusConnection::connectToBus(QDBusConnection::BusType type, const QString &name)`

**作用与语义：**

为已知总线之一打开类型为`type`的连接，并关联连接名称`name`。返回与该连接关联的`QDBusConnection`对象。

### `[static] QDBusConnection QDBusConnection::connectToBus(const QString &address, const QString &name)`

**作用与语义：**

在地址`address`上开启连接到私有总线的连接，并关联连接名称 `name`。返回与该连接关联的`QDBusConnection`对象。

### `[static] QDBusConnection QDBusConnection::connectToPeer(const QString &address, const QString &name)`

**作用与语义：**

在地址`address`上开启点对点连接，并关联连接名称 `name`。返回与该连接关联的`QDBusConnection`对象。

### `QDBusConnection::ConnectionCapabilities QDBusConnection::connectionCapabilities() const`

**作用与语义：**

返回与总线服务器或对等体协商的连接能力。如果该`QDBusConnection`未连接，该函数不返回任何能力。

### `bool QDBusConnection::disconnect(const QString &service, const QString &path, const QString &interface, const QString &name, QObject *receiver, const char *slot)`

**作用与语义：**

将`service`、`path`、`interface`和`name`参数指定的信号与对象`receiver`的槽`slot`断开。参数必须与传递给`connect()`函数相同的。
如果断开成功，还回车`true`。

### `bool QDBusConnection::disconnect(const QString &service, const QString &path, const QString &interface, const QString &name, const QString &signature, QObject *receiver, const char *slot)`

**作用与语义：**

将`service`、`path`、`interface`、`name`和`signature`参数指定的信号与对象`receiver`中的槽`slot`断开。参数必须与传递给`connect()`函数相同的。
如果断开成功，退货`true`。

### `bool QDBusConnection::disconnect(const QString &service, const QString &path, const QString &interface, const QString &name, const QStringList &argumentMatch, const QString &signature, QObject *receiver, const char *slot)`

**作用与语义：**

断开由`service`、`path`、`interface`、`name`、`argumentMatch`和`signature`参数指定的信号与对象`receiver`中的槽`slot`断开。参数必须与传递给`connect()`函数相同的。
如果断开成功，还品`true`。

### `[static] void QDBusConnection::disconnectFromBus(const QString &name)`

**作用与语义：**

关闭了`name`号公交线路。
注意，如果仍有`QDBusConnection`个对象关联到同一连接，连接不会关闭，直到所有引用被丢弃。但不能再使用 `QDBusConnection` 构造函数创建更多引用。

### `[static] void QDBusConnection::disconnectFromPeer(const QString &name)`

**作用与语义：**

关闭了名称`name`的对等连接。
注意，如果仍有`QDBusConnection`个对象关联到同一连接，连接不会关闭，直到所有引用被丢弃。但不能再使用`QDBusConnection`构造函数创建更多引用。

### `QDBusConnectionInterface *QDBusConnection::interface() const`

**作用与语义：**

返回一个`QDBusConnectionInterface`对象，代表该连接上的D-Bus服务器接口。

### `bool QDBusConnection::isConnected() const`

**作用与语义：**

如果该`QDBusConnection`对象连接，返回`true`。

### `QDBusError QDBusConnection::lastError() const`

**作用与语义：**

返回该连接中最后一次错误。
该函数用于低级代码。如果你使用`QDBusInterface::call()`，错误代码会以其返回值报告。

### `[static] QByteArray QDBusConnection::localMachineId()`

**作用与语义：**

返回D-Bus系统已知的本地机器ID。每个运行D-Bus的节点或主机都有一个唯一的标识符，如果它们共享资源，如文件系统，可以用来区分它们与其他主机。
注意，本地机器 ID 不保证系统多次启动时保持持久，因此该标识符不应存储在持久存储（如文件系统）中。它仅保证在启动会话生命周期内保持不变。

### `QString QDBusConnection::name() const`

**作用与语义：**

返回该连接的连接名称，作为`connectToBus()`的名称参数。
连接名称可用于唯一标识总线的实际底层连接。从单一连接复制的连接始终隐式共享底层连接，因此连接名称相同。
相反，两个连接名称不同的连接总是连接到不同的总线，或者在该总线上拥有不同的唯一名称（由`baseService()`返回）。

### `QObject *QDBusConnection::objectRegisteredAt(const QString &path) const`

**作用与语义：**

返回`path`给出的对象路径上注册到`registerObject()`的对象。

### `bool QDBusConnection::registerObject(const QString &path, QObject *object, QDBusConnection::RegisterOptions options = ExportAdaptors)`

**作用与语义：**

在路径`path`处`object`对象注册，若注册成功则返回`true`。`options`参数指定通过D-Bus将暴露多少对象`object`。
该函数不替代现有对象：如果路径`path`已有对象注册，该函数将返回false。先用`unregisterObject()`取消注册。
`ExportChildObjects`标志根据注册对象的路径和子节点的 `QObject::objectName` 导出 D-Bus 上的子对象。因此，子对象必须有一个对象名称。
你不能将对象注册为已注册在`ExportChildObjects`的对象的子对象。

### `bool QDBusConnection::registerObject(const QString &path, const QString &interface, QObject *object, QDBusConnection::RegisterOptions options = ExportAdaptors)`

**作用与语义：**

在路径`object` `path`对对象进行注册，接口名为`interface`，注册成功时返回`true`。`options`参数指定通过D-Bus将暴露多少对象`object`。
该函数不替代现有对象：如果路径`path`已注册对象，该函数将返回false。先用 `unregisterObject()` 取消注册。
`ExportChildObjects` 标志根据注册对象的路径和子节点的 `QObject::objectName` 在 D-Bus 上导出子对象。因此，子对象必须有一个对象名称。
你不能将一个对象注册为已注册在`ExportChildObjects`的对象的子对象。

### `bool QDBusConnection::registerService(const QString &serviceName)`

**作用与语义：**

尝试在D-Bus服务器上注册`serviceName`，如果注册成功则返回`true`。如果该名称已被其他应用程序注册，注册将失败。

### `bool QDBusConnection::send(const QDBusMessage &message) const`

**作用与语义：**

通过该连接发送`message`，无需等待回复。这适用于错误、信号和返回值，以及那些返回值不必要的调用。
如果消息排队成功，返回`true`，否则返回false。

### `[static] QDBusConnection QDBusConnection::sessionBus()`

**作用与语义：**

返回一个`QDBusConnection`对象，该对象由会话总线打开。该函数返回的对象引用有效，直到应用程序终止，此时连接将关闭，对象被删除。

### `[noexcept] void QDBusConnection::swap(QDBusConnection &other)`

**作用与语义：**

将连接与`other`交换。这个操作非常快，且从未出错。

### `[static] QDBusConnection QDBusConnection::systemBus()`

**作用与语义：**

返回一个`QDBusConnection`对象，该对象由系统总线打开。该函数返回的对象引用有效，直到运行`QCoreApplication`的析构器，届时连接将关闭并删除对象。

### `void QDBusConnection::unregisterObject(const QString &path, QDBusConnection::UnregisterMode mode = UnregisterNode)`

**作用与语义：**

取消注册一个在`path`对象路径上与`registerObject()`注册的对象，如果`mode` `QDBusConnection::UnregisterTree`，则取消其所有子对象。
请注意，你无法取消未注册在`registerObject()`的对象。

### `bool QDBusConnection::unregisterService(const QString &serviceName)`

**作用与语义：**

注销之前注册在`registerService()`的服务`serviceName`，成功后返回`true`。

### `QDBusConnection &QDBusConnection::operator=(const QDBusConnection &other)`

**作用与语义：**

创建该对象中连接`other`的副本。注意该对象在复制前引用的连接不会自发断开。

### `flags ConnectionCapabilities`

**作用与语义：**

本枚举描述了D-总线连接的可用能力。
- `QDBusConnection::UnixFileDescriptorPassing`：`0x0001`;支持将Unix文件描述符传递给其他进程（见 `QDBusUnixFileDescriptor`）
ConnectionCapabilities类型是QFlag的typedef<ConnectionCapability>。它存储ConnectionCapability值的或组合。

### `enum ConnectionCapability { UnixFileDescriptorPassing }`

**作用与语义：**

本枚举描述了D-总线连接的可用能力。
- `QDBusConnection::UnixFileDescriptorPassing`：`0x0001`;支持将Unix文件描述符传递给其他进程（见 `QDBusUnixFileDescriptor`）
ConnectionCapabilities类型是QFlag的typedef<ConnectionCapability>。它存储ConnectionCapability值的或组合。

### `enum RegisterOption { ExportAdaptors, ExportScriptableSlots, ExportScriptableSignals, ExportScriptableProperties, ExportScriptableInvokables, …, ExportChildObjects }`

**作用与语义：**

指定连接中注册对象的选项。可能的值如下：
- `QDBusConnection::ExportAdaptors`：`0x01`;导出该对象中适配器的内容
- `QDBusConnection::ExportScriptableSlots`：`0x10`;导出该对象可脚本的槽位
- `QDBusConnection::ExportScriptableSignals`：`0x20`;导出该对象的脚本化信号
- `QDBusConnection::ExportScriptableProperties`：`0x40`;导出该对象的脚本属性
- `QDBusConnection::ExportScriptableInvokables`：`0x80`;导出该对象可脚本调用的调用
- `QDBusConnection::ExportScriptableContents`：`0xf0`;ExportScriptableSlots 的简写形式 |ExportScriptableSignals |ExportScriptableProperties
- `QDBusConnection::ExportNonScriptableSlots`：`0x100`;导出该对象的非脚本槽
- `QDBusConnection::ExportNonScriptableSignals`：`0x200`;导出该对象的非脚本信号
- `QDBusConnection::ExportNonScriptableProperties`：`0x400`;导出该对象的非脚本属性
- `QDBusConnection::ExportNonScriptableInvokables`：`0x800`;导出该对象不可脚本调用的
- `QDBusConnection::ExportNonScriptableContents`：`0xf00`;导出非脚本槽的简写形式 |导出非脚本化信号 |导出非脚本属性
- `QDBusConnection::ExportAllSlots`：`ExportScriptableSlots|ExportNonScriptableSlots`;导出该物体的所有槽位
- `QDBusConnection::ExportAllSignals`：`ExportScriptableSignals|ExportNonScriptableSignals`;导出该物体的所有信号
- `QDBusConnection::ExportAllProperties`：`ExportScriptableProperties|ExportNonScriptableProperties`;导出该对象的所有属性
- `QDBusConnection::ExportAllInvokables`：`ExportScriptableInvokables|ExportNonScriptableInvokables`;导出该对象的所有可调用项
- `QDBusConnection::ExportAllContents`：`ExportScriptableContents|ExportNonScriptableContents`;导出该对象的所有内容
- `QDBusConnection::ExportChildObjects`：`0x1000`;导出该对象的子对象
RegisterOptions 类型是 QFlags 的 typedef<RegisterOption>。它存储 RegisterOption 值的 OR 组合。

### `flags RegisterOptions`

**作用与语义：**

指定连接中注册对象的选项。可能的值如下：
- `QDBusConnection::ExportAdaptors`：`0x01`;导出该对象中适配器的内容
- `QDBusConnection::ExportScriptableSlots`：`0x10`;导出该对象可脚本的槽位
- `QDBusConnection::ExportScriptableSignals`：`0x20`;导出该对象的脚本化信号
- `QDBusConnection::ExportScriptableProperties`：`0x40`;导出该对象的脚本属性
- `QDBusConnection::ExportScriptableInvokables`：`0x80`;导出该对象可脚本调用的调用
- `QDBusConnection::ExportScriptableContents`：`0xf0`;ExportScriptableSlots 的简写形式 |ExportScriptableSignals |ExportScriptableProperties
- `QDBusConnection::ExportNonScriptableSlots`：`0x100`;导出该对象的非脚本槽
- `QDBusConnection::ExportNonScriptableSignals`：`0x200`;导出该对象的非脚本信号
- `QDBusConnection::ExportNonScriptableProperties`：`0x400`;导出该对象的非脚本属性
- `QDBusConnection::ExportNonScriptableInvokables`：`0x800`;导出该对象不可脚本调用的
- `QDBusConnection::ExportNonScriptableContents`：`0xf00`;导出非脚本槽的简写形式 |导出非脚本化信号 |导出非脚本属性
- `QDBusConnection::ExportAllSlots`：`ExportScriptableSlots|ExportNonScriptableSlots`;导出该物体的所有槽位
- `QDBusConnection::ExportAllSignals`：`ExportScriptableSignals|ExportNonScriptableSignals`;导出该物体的所有信号
- `QDBusConnection::ExportAllProperties`：`ExportScriptableProperties|ExportNonScriptableProperties`;导出该对象的所有属性
- `QDBusConnection::ExportAllInvokables`：`ExportScriptableInvokables|ExportNonScriptableInvokables`;导出该对象的所有可调用项
- `QDBusConnection::ExportAllContents`：`ExportScriptableContents|ExportNonScriptableContents`;导出该对象的所有内容
- `QDBusConnection::ExportChildObjects`：`0x1000`;导出该对象的子对象
RegisterOptions 类型是 QFlags 的 typedef<RegisterOption>。它存储 RegisterOption 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QDBusConnection` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
