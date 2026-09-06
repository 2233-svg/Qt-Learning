# QDBusMessage

> Qt 6.11.1 · Qt D-Bus

## 1. 先建立直觉

**一句话定位：** 这是 Qt D-Bus 中围绕“DBusMessage”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** 这是 Qt D-Bus 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QDBusMessage` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QDBusMessage>`
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

- `enum MessageType { MethodCallMessage, SignalMessage, ReplyMessage, ErrorMessage, InvalidMessage }`

### 公有函数

- `QDBusMessage()`
- `QDBusMessage(const QDBusMessage &other)`
- `(since 6.11) QDBusMessage(QDBusMessage &&other)`
- `~QDBusMessage()`
- `QList<QVariant> arguments() const`
- `bool autoStartService() const`
- `QDBusMessage createErrorReply(const QDBusError &error) const`
- `QDBusMessage createErrorReply(QDBusError::ErrorType type, const QString &msg) const`
- `QDBusMessage createErrorReply(const QString &name, const QString &msg) const`
- `QDBusMessage createReply(const QList<QVariant> &arguments = QList<QVariant>()) const`
- `QDBusMessage createReply(const QVariant &argument) const`
- `QString errorMessage() const`
- `QString errorName() const`
- `QString interface() const`
- `bool isDelayedReply() const`
- `bool isInteractiveAuthorizationAllowed() const`
- `bool isReplyRequired() const`
- `QString member() const`
- `QString path() const`
- `QString service() const`
- `void setArguments(const QList<QVariant> &arguments)`
- `void setAutoStartService(bool enable)`
- `void setDelayedReply(bool enable) const`
- `void setInteractiveAuthorizationAllowed(bool enable)`
- `QString signature() const`
- `void swap(QDBusMessage &other)`
- `QDBusMessage::MessageType type() const`
- `QDBusMessage & operator<<(const QVariant &arg)`
- `QDBusMessage & operator=(QDBusMessage &&other)`
- `QDBusMessage & operator=(const QDBusMessage &other)`

### 静态公有成员

- `QDBusMessage createError(const QDBusError &error)`
- `QDBusMessage createError(QDBusError::ErrorType type, const QString &msg)`
- `QDBusMessage createError(const QString &name, const QString &msg)`
- `QDBusMessage createMethodCall(const QString &service, const QString &path, const QString &interface, const QString &method)`
- `QDBusMessage createSignal(const QString &path, const QString &interface, const QString &name)`
- `QDBusMessage createTargetedSignal(const QString &service, const QString &path, const QString &interface, const QString &name)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDBusMessage::MessageType`

**作用与语义：**

可能的消息类型：
- `QDBusMessage::MethodCallMessage`：`1`;表示一个输出或接收方法调用的消息
- `QDBusMessage::SignalMessage`：`4`;表示输出或输入信号发射的消息
- `QDBusMessage::ReplyMessage`：`2`;表示方法调用返回值的消息
- `QDBusMessage::ErrorMessage`：`3`;表示对方法调用响应错误条件的消息
- `QDBusMessage::InvalidMessage`：`0`;无效消息：从D-Bus接收的消息中绝不设置无效消息

### `QDBusMessage::QDBusMessage()`

**作用与语义：**

构造一个空的、无效的 QDBusMessage 对象。

### `QDBusMessage::QDBusMessage(const QDBusMessage &other)`

**作用与语义：**

构造`other`所给对象的复制品。
注意：QDBusMessage对象是共享的。对副本所做的修改也会影响原始副本。更多信息请参见 `setDelayedReply()`。

### `[noexcept, since 6.11] QDBusMessage::QDBusMessage(QDBusMessage &&other)`

**作用与语义：**

`other`进入这个物体。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋值。

### `[noexcept] QDBusMessage::~QDBusMessage()`

**作用与语义：**

处理掉物品并释放所有被持有的资源。

### `QList<QVariant> QDBusMessage::arguments() const`

**作用与语义：**

返回将要发送或已从 D-Bus 收到的参数列表。

### `bool QDBusMessage::autoStartService() const`

**作用与语义：**

返回`setAutoStartService()`设置的自动启动标志。默认情况下，该标志为真，这意味着Qt D-Bus会自动启动服务（如果服务尚未运行）。

### `[static] QDBusMessage QDBusMessage::createError(const QDBusError &error)`

**作用与语义：**

构造一个表示给定`error`的新 DBus 消息。

### `[static] QDBusMessage QDBusMessage::createError(QDBusError::ErrorType type, const QString &msg)`

**作用与语义：**

利用消息`msg`为错误类型构造新的 DBus 消息`type`。返回 DBus 消息。

### `[static] QDBusMessage QDBusMessage::createError(const QString &name, const QString &msg)`

**作用与语义：**

构造一个新的 DBus 消息，表示错误，`name` 和 `msg`。

### `QDBusMessage QDBusMessage::createErrorReply(const QDBusError &error) const`

**作用与语义：**

从给定的`error`对象构建一个新的 DBus 消息，表示错误回复消息。

### `QDBusMessage QDBusMessage::createErrorReply(QDBusError::ErrorType type, const QString &msg) const`

**作用与语义：**

利用消息`msg`构建错误类型的新 DBus 回复消息`type`。返回 DBus 消息。

### `QDBusMessage QDBusMessage::createErrorReply(const QString &name, const QString &msg) const`

**作用与语义：**

构造一个新的 DBus 消息，表示错误回复消息，包含给定的 `name` 和 `msg`。

### `[static] QDBusMessage QDBusMessage::createMethodCall(const QString &service, const QString &path, const QString &interface, const QString &method)`

**作用与语义：**

构造一个表示方法调用的新 DBus 消息。方法调用总是通知其目的地址（`service`、`path`、`interface` 和 `method`）。
如果方法名称唯一，DBus总线允许在给定远程对象上调用方法而无需指定目的接口。然而，如果远程对象上的两个接口导出相同的方法名称，结果是未定义的（可能调用其中一个或返回错误）。
在点对点环境中使用DBus（即非总线）时，`service`参数是可选的。
`QDBusInterface`类为同步方法调用提供了更简单的抽象。
该函数返回一个`QDBusMessage`对象，可以随`QDBusConnection::call()`发送。

### `QDBusMessage QDBusMessage::createReply(const QList<QVariant> &arguments = QList<QVariant>()) const`

**作用与语义：**

构造一个新的 DBus 消息，表示回复，并带有给定的`arguments`。

### `QDBusMessage QDBusMessage::createReply(const QVariant &argument) const`

**作用与语义：**

构造一个新的 DBus 消息，表示回复，并带有给定的 `argument`。

### `[static] QDBusMessage QDBusMessage::createSignal(const QString &path, const QString &interface, const QString &name)`

**作用与语义：**

构造一个新的 DBus 消息，包含给定的 `path`、`interface` 和 `name`，表示信号发射。
DBus信号由一个应用程序发出，所有监听该接口信号的应用程序都会接收到。
返回的`QDBusMessage`对象可以通过`QDBusConnection::send()`函数发送。

### `[static] QDBusMessage QDBusMessage::createTargetedSignal(const QString &service, const QString &path, const QString &interface, const QString &name)`

**作用与语义：**

构造一个新的 DBus 消息，包含给定的 `path`、`interface` 和 `name`，表示指向特定目的地的信号发射。
DBus信号由一个应用程序发出，只有拥有目的地`service`名称的应用程序才能接收。
返回的`QDBusMessage`对象可以通过`QDBusConnection::send()`函数发送。

### `QString QDBusMessage::errorMessage() const`

**作用与语义：**

返回与收到错误相关的人类可读消息。

### `QString QDBusMessage::errorName() const`

**作用与语义：**

返回收到的错误名称。

### `QString QDBusMessage::interface() const`

**作用与语义：**

返回被调用方法（方法调用时）或接收信号的接口。

### `bool QDBusMessage::isDelayedReply() const`

**作用与语义：**

返回延迟回复标志，按`setDelayedReply()`设置。默认情况下，该标志为假，这意味着Qt D-Bus在必要时会自动生成回复。

### `bool QDBusMessage::isInteractiveAuthorizationAllowed() const`

**作用与语义：**

返回消息是否设置了`ALLOW_INTERACTIVE_AUTHORIZATION`标志。

### `bool QDBusMessage::isReplyRequired() const`

**作用与语义：**

返回指示该消息是否应收到回复的标志。这仅对方法调用消息有意义：其他类型的消息不能有回复，该函数对它们总是返回false。

### `QString QDBusMessage::member() const`

**作用与语义：**

返回发出的信号名称或被调用的方法名称。

### `QString QDBusMessage::path() const`

**作用与语义：**

返回该消息发送对象（方法调用时）或接收对象（信号时）的路径。

### `QString QDBusMessage::service() const`

**作用与语义：**

返回服务名称或远程方法调用的总线地址。

### `void QDBusMessage::setArguments(const QList<QVariant> &arguments)`

**作用与语义：**

将要通过D-Bus发送的参数设置为`arguments`。这些参数是方法调用的参数或信号中的参数。
注意，`arguments`中不允许`QVariant`为无效值的`QVariantMap`。

### `void QDBusMessage::setAutoStartService(bool enable)`

**作用与语义：**

将自动启动标志设置为`enable`。该标志仅适用于方法调用消息，指示D-Bus服务器要么自动启动负责该服务名称的服务，要么不自动启动。
默认情况下，该标志为真，即服务已自动启动。这意味着：
当该方法调用的服务已经在运行时，方法调用会发送给该服务。如果服务尚未运行，则请求D-Bus守护进程自动启动分配给该服务名称的服务。这由放置在D-总线服务器已知目录中的.service文件处理。这些文件每个文件包含服务名称和请求该服务名称时应执行的程序路径。

### `void QDBusMessage::setDelayedReply(bool enable) const`

**作用与语义：**

设置消息是否会在之后回复（如果`enable`为真），或者如果`enable`为假，则是否应由Qt D-Bus生成自动回复。
在D-Bus中，所有方法调用必须生成回复，除非调用者明确表示（参见`isReplyRequired()`）。`QtDBus`自动生成被调用槽的回复，同时允许槽函数表明是否会在函数处理完成后承担回复的责任。

### `void QDBusMessage::setInteractiveAuthorizationAllowed(bool enable)`

**作用与语义：**

启用或禁用消息中的`ALLOW_INTERACTIVE_AUTHORIZATION`标志。
该标志仅适用于方法调用消息（`QDBusMessage::MethodCallMessage`）。如果`enable`设置为`true`，标志向被叫方表明调用者准备等待交互授权（例如通过Polkit）完成，然后才处理实际方法。
如果`enable`设置为`false`，则该标志未被设置，意味着对方应以非交互方式且迅速地做出授权决策。这是默认设置。
`org.freedesktop.DBus.Error.InteractiveAuthorizationRequired`错误表示授权失败，但如果设置了该标志，授权本可以成功。

### `QString QDBusMessage::signature() const`

**作用与语义：**

返回接收到的信号签名或方法调用输出参数的签名。

### `[noexcept] void QDBusMessage::swap(QDBusMessage &other)`

**作用与语义：**

将此消息与`other`交换。此操作非常快且从未失败。

### `QDBusMessage::MessageType QDBusMessage::type() const`

**作用与语义：**

返回消息类型。

### `QDBusMessage &QDBusMessage::operator<<(const QVariant &arg)`

**作用与语义：**

在方法调用或信号发射中，将参数 `arg` 附加到要通过 D-Bus 发送的参数列表中。

### `[noexcept] QDBusMessage &QDBusMessage::operator=(QDBusMessage &&other)`

**作用与语义：**

Move-assign `other`到该对象中。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋值。

### `QDBusMessage &QDBusMessage::operator=(const QDBusMessage &other)`

**作用与语义：**

复制`other`给出的对象内容。
注意：`QDBusMessage`对象是共享的。对副本所做的修改也会影响原始副本。更多信息请参见 `setDelayedReply()`。

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

`QDBusMessage` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
