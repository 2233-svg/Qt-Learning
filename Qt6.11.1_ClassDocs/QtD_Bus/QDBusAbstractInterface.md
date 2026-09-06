# QDBusAbstractInterface

> Qt 6.11.1 · Qt D-Bus

## 1. 先建立直觉

**一句话定位：** `QDBusAbstractInterface` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt D-Bus 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QDBusAbstractInterface` 是 Qt D-Bus 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QDBusAbstractInterface>`
- 继承自：QObject
- 直接派生类：QDBusConnectionInterface、QDBusInterface

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `virtual ~QDBusAbstractInterface()`
- `QDBusPendingCall asyncCall(const QString &method, Args &&... args)`
- `QDBusPendingCall asyncCallWithArgumentList(const QString &method, const QList<QVariant> &args)`
- `QDBusMessage call(const QString &method, Args &&... args)`
- `QDBusMessage call(QDBus::CallMode mode, const QString &method, Args &&... args)`
- `QDBusMessage callWithArgumentList(QDBus::CallMode mode, const QString &method, const QList<QVariant> &args)`
- `bool callWithCallback(const QString &method, const QList<QVariant> &args, QObject *receiver, const char *returnMethod, const char *errorMethod)`
- `bool callWithCallback(const QString &method, const QList<QVariant> &args, QObject *receiver, const char *slot)`
- `QDBusConnection connection() const`
- `QString interface() const`
- `(since 6.7) bool isInteractiveAuthorizationAllowed() const`
- `bool isValid() const`
- `QDBusError lastError() const`
- `QString path() const`
- `QString service() const`
- `(since 6.7) void setInteractiveAuthorizationAllowed(bool enable)`
- `void setTimeout(int timeout)`
- `int timeout() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[virtual noexcept] QDBusAbstractInterface::~QDBusAbstractInterface()`

**作用与语义：**

释放该物体的资源。

### `template <typename... Args> QDBusPendingCall QDBusAbstractInterface::asyncCall(const QString &method, Args &&... args)`

**作用与语义：**

调用该接口上的方法`method`并将`args`传递给该方法。所有`args`必须可转换为`QVariant`。
`call`的参数通过D-Bus作为输入参数传递给远程函数。返回的`QDBusPendingCall`对象可用于获取关于回复的信息。
它可以以下方式使用：
本示例展示了函数调用时参数为0、1和2，并展示了每个参数中传递的不同参数类型（第一次调用`"ProcessWorkUnicode"`包含一个Unicode字符串，第二次调用`"ProcessWork"`包含一个字符串和一个字节数组）。有关分组（同步）调用的同一示例，请参见`call()`。
注意：在Qt 5.14之前，该函数最多只接受八（8）个参数。
注意：由于实现限制，对本地`QDBusServer`的方法调用从不异步。

**官方示例：**

```cpp
 QDBusPendingCall pcall = interface->asyncCall("GetAPIVersion"_L1);
 auto watcher = new QDBusPendingCallWatcher(pcall, this);

 QObject::connect(watcher, &QDBusPendingCallWatcher::finished, this,
                  [&](QDBusPendingCallWatcher *w) {
     QString value = retrieveValue();
     QDBusPendingReply<int> reply(*w);
     QDBusPendingCall pcall;
     if (reply.argumentAt<0>() >= 14)
         pcall = interface->asyncCall("ProcessWorkUnicode"_L1, value);
     else
         pcall = interface->asyncCall("ProcessWork"_L1, "UTF-8"_L1, value.toUtf8());

     w = new QDBusPendingCallWatcher(pcall);
     QObject::connect(w,  &QDBusPendingCallWatcher::finished, this,
                      &Abstract_DBus_Interface::callFinishedSlot);
 });
```

### `QDBusPendingCall QDBusAbstractInterface::asyncCallWithArgumentList(const QString &method, const QList<QVariant> &args)`

**作用与语义：**

调用该接口上`method`指定的远程方法，使用`args`作为参数。该函数返回一个`QDBusPendingCall`对象，可用于跟踪回复状态并在回复到达后访问其内容。
通常，你应该用`asyncCall()`打电话。
注意：由于实现限制，应用程序自身注册对象的方法调用从不异步。
注意：该功能是线程安全的。

### `template <typename... Args> QDBusMessage QDBusAbstractInterface::call(const QString &method, Args &&... args)`

**作用与语义：**

调用该接口上的`method`方法，并将`args`传递给该方法。所有`args`必须可转换为`QVariant`。
`call`的参数通过D-Bus作为输入参数传递给远程函数。输出参数返回于`QDBusMessage`回复中。如果回复是错误回复，`lastError()`也会被设置为错误消息的内容。
它可以以下方式使用：
本示例展示了使用0、1和2参数的函数调用，并展示了每个参数中传递的不同参数类型（第一次调用`"ProcessWorkUnicode"`包含一个Unicode字符串，第二次调用`"ProcessWork"`包含一个字符串和一个字节数组）。关于非分组（异步）调用中的同一示例，请参见`asyncCall()`。
注意：在Qt 5.14之前，该函数最多只接受八（8）个参数。

**官方示例：**

```cpp
 QString value = retrieveValue();
 QDBusMessage reply;

 QDBusReply<int> api = interface->call("GetAPIVersion"_L1);
 if (api >= 14)
   reply = interface->call("ProcessWorkUnicode"_L1, value);
 else
   reply = interface->call("ProcessWork"_L1, "UTF-8"_L1, value.toUtf8());
```

### `template <typename... Args> QDBusMessage QDBusAbstractInterface::call(QDBus::CallMode mode, const QString &method, Args &&... args)`

**作用与语义：**

调用该接口上的方法`method`并将`args`传递给该方法。所有`args`必须可转换为`QVariant`。
如果`mode` `NoWaitForReply`，则该函数在发出调用后立即返回，无需等待远程方法的回复。否则，`mode`指示该函数是否应在等待回复到达时激活Qt事件循环。
如果该函数重新进入Qt事件循环以等待回复，则会排除用户输入。在等待期间，它可能会向你的应用程序传递信号和其他方法调用。因此，必须准备好在调用时处理重入。
注意：在Qt 5.14之前，该函数最多只接受八（8）个参数。

### `QDBusMessage QDBusAbstractInterface::callWithArgumentList(QDBus::CallMode mode, const QString &method, const QList<QVariant> &args)`

**作用与语义：**

调用该接口上`method`指定的远程方法，使用`args`作为参数。该函数返回收到的回复消息，回复可以是正常`QDBusMessage::ReplyMessage`（表示成功）或`QDBusMessage::ErrorMessage`（如果调用失败）。`mode`参数指定该调用的配置方式。
如果调用成功，`lastError()`将被清除;否则，它将包含该调用产生的错误。
通常，你应该用`call()`打电话。
警告：如果您使用 `UseEventLoop`，您的代码必须准备好应对任何重入：在该函数返回之前，可能会先传递其他方法调用和信号，以及其他 Qt 队列中的信号和事件。
注意：该功能是线程安全的。

### `bool QDBusAbstractInterface::callWithCallback(const QString &method, const QList<QVariant> &args, QObject *receiver, const char *returnMethod, const char *errorMethod)`

**作用与语义：**

调用该接口上`method`指定的远程方法，使用`args`作为参数。该函数在排队调用后立即返回。远程函数的回复会传递给对象`receiver`的`returnMethod`。如果发生错误，则调用对象`receiver`的`errorMethod`。
如果队列成功，该函数返回`true`。它并不表示已执行调用成功。如果失败，调用`errorMethod`。如果队列失败，该函数返回`false`，且不会调用任何槽位。
`returnMethod`必须包含函数调用返回的类型作为参数。可选地，其最后或唯一的参数可以是`QDBusMessage`参数。`errorMethod`必须以`QDBusError`作为唯一的参数。
注意：由于实现限制，应用程序自身注册对象的方法调用从不异步。

### `bool QDBusAbstractInterface::callWithCallback(const QString &method, const QList<QVariant> &args, QObject *receiver, const char *slot)`

**作用与语义：**

该函数已被弃用。请使用重载版本。
调用该接口上`method`指定的远程方法，使用`args`作为参数。该函数在排队调用后立即返回。远程函数的回复或其发出的任何错误会被传递到对象`receiver`的`slot`槽。
该函数返回`true`队列是否成功：它并不表示调用成功。如果失败，该槽位将被调用并发送错误消息。在这种情况下，`lastError()`不会被设置。

### `QDBusConnection QDBusAbstractInterface::connection() const`

**作用与语义：**

返回该接口关联的连接。

### `QString QDBusAbstractInterface::interface() const`

**作用与语义：**

返回该接口的名称。

### `[since 6.7] bool QDBusAbstractInterface::isInteractiveAuthorizationAllowed() const`

**作用与语义：**

返回异步调用时，调用者是否准备等待交互式授权。
默认是`false`。

### `bool QDBusAbstractInterface::isValid() const`

**作用与语义：**

返回`true`是否为远程对象的有效引用。如果在创建该接口时出现错误（例如，远程应用程序不存在），它返回`false`。
注意：处理远程对象时，创建`QDBusInterface`时并不总能确定其存在。

### `QDBusError QDBusAbstractInterface::lastError() const`

**作用与语义：**

返回上一次操作产生的错误，或返回无效错误（如果上一次操作未产生错误）。

### `QString QDBusAbstractInterface::path() const`

**作用与语义：**

返回该接口关联的对象路径。

### `QString QDBusAbstractInterface::service() const`

**作用与语义：**

返回该接口所关联的服务名称。

### `[since 6.7] void QDBusAbstractInterface::setInteractiveAuthorizationAllowed(bool enable)`

**作用与语义：**

配置异步通话时，调用者是否愿意等待交互式授权。
如果`enable`设置为`true`，通过该接口为异步调用生成的D-Bus消息将设置`ALLOW_INTERACTIVE_AUTHORIZATION`标志。
该标志仅在非特权代码调用更高特权的方法调用时有用，且部署了允许交互式授权的授权框架。
默认是`false`。

### `void QDBusAbstractInterface::setTimeout(int timeout)`

**作用与语义：**

为所有未来向`timeout`调用的DBus设置毫秒超时。-1表示默认的DBus超时（通常为25秒）。

### `int QDBusAbstractInterface::timeout() const`

**作用与语义：**

返回当前超时值（毫秒）。-1 表示默认的 DBus 超时（通常为 25 秒）。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QDBusAbstractInterface` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
