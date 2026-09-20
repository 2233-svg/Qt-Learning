# Qt QDBusMessage 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusMessage>`  
> 所属模块：`Qt6::DBus`  
> 类型特征：显式共享的原始 D-Bus 消息值类型

## 1. 它解决什么问题

`QDBusInterface` 和已生成的代理类适合调用已经明确的远端接口；但需要动态决定 service、path、interface、method，或需要手动构造回复、错误和信号时，就必须直接面对一条 D-Bus 消息。

`QDBusMessage` 表示消息本身的信封和参数：

```text
service / destination
path
interface
member
arguments
message type
```

它可以表示方法调用、信号、正常回复、错误回复或无效消息。它只负责**描述、构造与检查**消息，不负责把消息送上总线；发送、同步调用和异步调用由 `QDBusConnection` 完成。

## 2. 消息类型与方向

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举值 | `InvalidMessage` | 表示无效或尚未形成的消息。 | 常见于默认构造或异步回复尚未完成的占位状态。 |
| 枚举值 | `MethodCallMessage` | 表示请求远端方法执行。 | 可要求回复、控制服务自动启动和交互授权。 |
| 枚举值 | `ReplyMessage` | 表示方法调用成功后的回复。 | 参数是远端方法的输出值。 |
| 枚举值 | `ErrorMessage` | 表示方法调用失败后的回复。 | 用 `errorName()`、`errorMessage()` 读取错误详情。 |
| 枚举值 | `SignalMessage` | 表示广播或定向信号。 | 不会有回复；普通 signal 可被所有匹配监听者接收。 |

收到或构造消息时，先用 `type()` 确认它是什么。不要把 `arguments()` 的存在当作“这是方法成功回复”的判断依据。

## 3. 构造并发送一个方法调用

```cpp
#include <QDBusConnection>
#include <QDBusMessage>

QDBusMessage request = QDBusMessage::createMethodCall(
    "org.example.Player",
    "/org/example/Player",
    "org.example.Player",
    "Pause");

request << QVariant::fromValue(true);

QDBusMessage reply = QDBusConnection::sessionBus().call(request);
if (reply.type() == QDBusMessage::ErrorMessage) {
    qWarning() << reply.errorName() << reply.errorMessage();
}
```

`createMethodCall()` 只是构造信封，`QDBusConnection::call()` 才真正发送并等待回复。对于固定接口，`QDBusInterface::call()` 更简洁；对于动态路由、协议工具和虚拟对象处理器，直接使用 `QDBusMessage` 更合适。

总线场景中应尽量提供 interface。虽然 D-Bus 允许在 method 名唯一时省略 interface，但同一路径多个接口有同名方法时，结果会歧义或报错。点对点连接中 `service` 可以省略。

## 4. 构造信号与回复

### 4.1 发送信号

```cpp
QDBusMessage signal = QDBusMessage::createSignal(
    "/org/example/Player",
    "org.example.Player",
    "StateChanged");

signal.setArguments({QStringLiteral("paused")});
connection.send(signal);
```

`createSignal()` 构造普通信号，所有订阅匹配规则的应用都有机会接收。`createTargetedSignal(service, ...)` 则只发送给拥有指定 destination service 的应用。

### 4.2 从收到的调用构造回复

服务端不应凭空调用静态 `createError()` 来回复某条请求；应基于原始 method call 使用成员函数：

```cpp
QDBusMessage response = request.createReply(QVariant(QStringLiteral("ok")));
connection.send(response);
```

发生错误时：

```cpp
connection.send(request.createErrorReply(
    QDBusError::InvalidArgs,
    QStringLiteral("expected one string argument")));
```

`createReply()` 和 `createErrorReply()` 保留了与原请求对应的 reply 信息；静态 `createError()` 仅创建一条独立错误消息。

## 5. 延迟回复：接管自动回复责任

由 Qt D-Bus 导出的槽函数通常返回后，Qt 会自动发送回复。某些操作需要异步完成，此时可从当前调用消息设置延迟回复：

```cpp
message.setDelayedReply(true);
startLongOperation([message, connection](const Result &result) {
    connection.send(message.createReply(QVariant::fromValue(result.text)));
});
```

`setDelayedReply(true)` 的真实含义是：**不要让 Qt 自动回复，这条调用的回复由你之后负责发送**。如果设置后既不发送正常回复，也不发送错误回复，调用方会等待到超时。

只对需要回复的 method call 使用它。若 `isReplyRequired()` 为 `false`，调用方本就不等回复；signal 和其他消息类型也没有回复语义。

## 6. 三个方法调用标志

### 6.1 是否要求回复

`isReplyRequired()` 只对 `MethodCallMessage` 有意义。其他类型永远为 `false`。

### 6.2 是否自动启动服务

`autoStartService()` 默认是 `true`。当目标 service 未运行时，D-Bus daemon 可以按 `.service` 配置尝试拉起它。

```cpp
request.setAutoStartService(false);
```

禁用后，目标服务未运行时不会请求 daemon 自动启动。这个标志只适用于方法调用。

### 6.3 是否允许交互式授权

`setInteractiveAuthorizationAllowed(true)` 设置 `ALLOW_INTERACTIVE_AUTHORIZATION`。它表示调用方可以等待对端进行交互式授权，例如 Polkit 弹窗。

这也只适用于方法调用。默认是 `false`，表示对端应尽快以非交互方式做出授权决定。收到 `org.freedesktop.DBus.Error.InteractiveAuthorizationRequired` 时，说明如果允许交互授权，调用本可能成功。

## 7. 参数、签名与共享状态

### 7.1 参数

`arguments()` 返回消息将要发送或已经收到的 `QList<QVariant>`。`setArguments()` 整体替换参数，`operator<<(const QVariant &)` 在尾部追加参数。

```cpp
request.setArguments({42, QStringLiteral("Alice")});
request << QVariant::fromValue(QStringLiteral("extra"));
```

参数中的 `QVariantMap` 不能含有无效 `QVariant` value。对于 D-Bus `VARIANT`，应显式使用 `QDBusVariant`，不要混淆为任意 `QVariant`。

### 7.2 签名

`signature()` 返回 signal 的参数签名，或 method call 的输出参数签名。它是协议诊断信息，不应用字符串比较替代类型化 API；复杂类型应使用 `QDBusArgument`、`QDBusObjectPath`、`QDBusSignature` 等正确包装。

### 7.3 显式共享

`QDBusMessage` 的复制对象共享底层状态。修改一份副本会影响另一份副本，而不是触发独立 detach：

```cpp
QDBusMessage first = request;
QDBusMessage second = first;
second.setDelayedReply(true); // first 也会看到同一延迟回复状态
```

需要独立可变消息时，不要依赖复制隔离；应重新构造消息或明确按业务避免共享后修改。

## 8. 常见误区

### 8.1 误区：创建 message 就完成发送

没有。静态工厂和成员 `createReply()` 只创建对象；调用 `QDBusConnection::send()`、`call()` 或 `asyncCall()` 才进行通信。

### 8.2 误区：`createError()` 可以当作对当前请求的回复

不能。回复当前 method call 应使用 `createErrorReply()`，以保留原请求的 reply 关联。

### 8.3 误区：设置延迟回复后可以什么都不做

不能。自动回复被关闭，之后必须手动发送 reply 或 error，否则调用方超时。

### 8.4 误区：复制 message 后随便修改不会影响原对象

不对。该类型显式共享，副本修改会影响共享状态。

### 8.5 误区：错误文字适合做业务分支

不稳妥。使用 `errorName()` 或转换出的 `QDBusError::type()` 分类；`errorMessage()` 只适合日志和用户展示。

## 9. 逐项 API 说明

### 生命周期与共享

#### `QDBusMessage()`、复制、移动和赋值

默认构造得到无效消息。复制与复制赋值共享内容，移动构造、移动赋值在 Qt 6.11 起可用；被移动对象只应析构或重新赋值。

#### `swap(QDBusMessage &other)`

快速交换两个消息对象。适用于容器算法或实现代码，不会发送消息。

### 静态工厂

#### `createMethodCall(service, path, interface, method)`

构造方法调用消息。目标四元组决定调用路由；之后添加参数并交给连接发送。

#### `createSignal(path, interface, name)`

构造普通广播信号。使用 `send()` 发送给所有匹配的订阅者。

#### `createTargetedSignal(service, path, interface, name)`

构造发往特定 destination service 的信号。适合只希望某一个已知服务接收的情形。

#### `createError(error)`、`createError(type, msg)`、`createError(name, msg)`

构造独立错误消息。根据现有 `QDBusError`、标准错误类型或自定义错误名选择重载；它们不是对某条请求的关联回复。

### 基于原调用创建回复

#### `createReply(arguments)` 与 `createReply(argument)`

从 method call 创建成功回复。前者可含零个或多个输出参数，后者用于单输出值。

#### `createErrorReply(error)`、`createErrorReply(type, msg)`、`createErrorReply(name, msg)`

从 method call 创建错误回复。适用于虚拟对象、上下文延迟回复或手工服务端分派。

### 元数据与标志

#### `service()`、`path()`、`interface()`、`member()`

读取消息路由信息。service 是目标服务名或点对点地址，path 是对象路径，interface 与 member 分别表示接口和方法或信号名。

#### `type()`、`signature()`

读取消息类型与签名。先用 `type()` 确认消息角色，再按协议解析签名和参数。

#### `isReplyRequired()`、`setDelayedReply()`、`isDelayedReply()`

检查是否需要回复，或控制是否由业务稍后回复。延迟回复会关闭 Qt 自动回复，调用者必须保证最终发送结果。

#### `setAutoStartService()` 与 `autoStartService()`

设置或读取是否在目标服务尚未运行时请求 D-Bus daemon 自动启动它。只适用于 method call，默认开启。

#### `setInteractiveAuthorizationAllowed()` 与 `isInteractiveAuthorizationAllowed()`

设置或读取是否允许远端进行交互式授权。只适用于 method call，默认关闭。

### 参数与错误

#### `setArguments()`、`arguments()`、`operator<<(const QVariant &)`

整体替换、读取或追加消息参数。参数类型必须可映射到 D-Bus 类型，且保持与远端协议一致。

#### `errorName()` 与 `errorMessage()`

读取错误消息中的机器可判定名称与可读文本。它们只在错误消息场景有业务意义。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `MessageType` | 区分无效、调用、成功回复、错误回复和信号。 | 解析参数或处理回复前先检查 `type()`。 |
| 构造 | `QDBusMessage()` | 创建无效消息。 | 不能直接代表可发送的调用，通常使用工厂函数。 |
| 复制构造 | `QDBusMessage(const QDBusMessage &other)` | 创建共享同一消息状态的副本。 | 修改副本会影响原对象的共享状态。 |
| 移动构造 | `QDBusMessage(QDBusMessage &&other)` | 移入消息状态。 | Qt 6.11 起可用；移动后只析构或重新赋值源对象。 |
| 析构 | `~QDBusMessage()` | 释放消息资源。 | 不会发送、取消或自动回复消息。 |
| 移动赋值 | `operator=(QDBusMessage &&other)` | 用移动状态替换当前消息。 | Qt 6.11 起可用；源对象状态不可再依赖。 |
| 复制赋值 | `operator=(const QDBusMessage &other)` | 改为共享另一条消息状态。 | 后续修改同样是共享的。 |
| 交换 | `swap(QDBusMessage &other)` | 快速交换两个消息对象。 | 只交换本地对象，不发生总线通信。 |
| 调用工厂 | `createMethodCall(service, path, interface, method)` | 创建远端方法调用。 | 还需添加参数并用 QDBusConnection 发送；总线场景尽量指定 interface。 |
| 广播信号工厂 | `createSignal(path, interface, name)` | 创建普通 D-Bus 信号。 | 使用 `send()`；会面向所有匹配监听者。 |
| 定向信号工厂 | `createTargetedSignal(service, path, interface, name)` | 创建指定 destination 的信号。 | 仅目标服务拥有者接收。 |
| 独立错误工厂 | `createError(QDBusError)` | 从错误对象创建错误消息。 | 不关联当前 method call。 |
| 独立错误工厂 | `createError(ErrorType, msg)` | 用标准错误类型创建错误消息。 | 用标准 ErrorType 可保留一致的错误命名。 |
| 独立错误工厂 | `createError(name, msg)` | 用自定义错误名创建错误消息。 | name 应符合 D-Bus 错误命名约定。 |
| 成功回复 | `createReply(QList<QVariant>)` | 为当前调用创建多参数成功回复。 | 只对收到的 method call 有意义。 |
| 成功回复 | `createReply(QVariant)` | 为当前调用创建单参数成功回复。 | 发送前确认该参数类型符合远端调用方的协议。 |
| 错误回复 | `createErrorReply(QDBusError)` | 为当前调用创建错误回复。 | 延迟回复和手动分派应使用此类成员函数。 |
| 错误回复 | `createErrorReply(ErrorType, msg)` | 用标准错误类型回复当前调用。 | 不要用静态 `createError()` 代替。 |
| 错误回复 | `createErrorReply(name, msg)` | 用自定义错误名回复当前调用。 | 发送一次明确回复后不要重复处理同一调用。 |
| 服务查询 | `QString service() const` | 读取目标服务名或点对点地址。 | 点对点消息中的 service 可为空。 |
| 路径查询 | `QString path() const` | 读取目标或来源 object path。 | virtual object 应按它路由动态子路径。 |
| 接口查询 | `QString interface() const` | 读取接口名。 | 手动分派时与 `member()` 共同确定处理器。 |
| 成员查询 | `QString member() const` | 读取方法名或信号名。 | 不能单独假定全局唯一。 |
| 消息类型 | `MessageType type() const` | 获取消息类型。 | 先判断它，再读错误或回复参数。 |
| 签名查询 | `QString signature() const` | 获取参数 D-Bus signature。 | 用于诊断或动态处理；固定协议更推荐类型化 API。 |
| 回复要求 | `bool isReplyRequired() const` | 判断 method call 是否要求回复。 | 其他消息类型总为 false。 |
| 延迟回复设置 | `void setDelayedReply(bool)` | 控制 Qt 是否自动回复当前调用。 | 设置 true 后必须由你的代码最终发送 reply 或 error。 |
| 延迟回复查询 | `bool isDelayedReply() const` | 查询是否已接管延迟回复责任。 | true 时不要让槽函数普通返回后期待 Qt 自动回。 |
| 服务自启设置 | `void setAutoStartService(bool)` | 设置目标服务未运行时是否允许自动启动。 | 只适用 method call，默认 true。 |
| 服务自启查询 | `bool autoStartService() const` | 查询自动启动标志。 | 不代表服务一定能成功启动。 |
| 授权设置 | `void setInteractiveAuthorizationAllowed(bool)` | 设置是否允许交互式授权。 | 只适用 method call；开启后调用可等待更久。 |
| 授权查询 | `bool isInteractiveAuthorizationAllowed() const` | 查询交互授权标志。 | 默认 false。 |
| 参数设置 | `void setArguments(const QList<QVariant> &)` | 整体设置方法或信号参数。 | QVariantMap 不得含无效 QVariant；类型要符合协议。 |
| 参数读取 | `QList<QVariant> arguments() const` | 获取接收或待发送参数。 | 不要仅凭参数存在判断消息是否成功。 |
| 参数追加 | `operator<<(const QVariant &arg)` | 向消息尾部追加一个参数。 | 仍需把消息交给 QDBusConnection 发送。 |
| 错误名称 | `QString errorName() const` | 获取错误的机器可判定名称。 | 适合程序分支；仅 ErrorMessage 有意义。 |
| 错误文本 | `QString errorMessage() const` | 获取错误的人类可读文本。 | 适合日志与展示，不宜作为程序判断依据。 |

---

### 一句话总结

`QDBusMessage` 是原始 D-Bus 消息的信封和参数容器；它只负责构造与检查，通信交给 `QDBusConnection`，而延迟回复开启后则必须由你的代码负责把最终结果送回调用者。
