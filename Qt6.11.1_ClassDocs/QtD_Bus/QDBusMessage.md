# QDBusMessage
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusMessage`

## 作用定位

`QDBusMessage` 是一帧 D-Bus 消息的 Qt 表示。它既可以表示“我要调用远端方法”，也可以表示“我发出一个信号”“这是一次调用的返回值”“这是一次调用的错误”。如果 `QDBusConnection` 是通道，`QDBusMessage` 就是通道里实际流动的信封。

更高级的 `QDBusInterface::call()` 会帮你构造消息；但只要需要精准控制目的服务、对象路径、接口名、参数、自动激活或延迟回复，就要直接理解 `QDBusMessage`。

## 类说明

- 头文件：`#include <QDBusMessage>`
- CMake：链接 `Qt6::DBus`
- 继承：无公开 QObject 继承，值类型；Qt 6.11 起支持移动构造/移动赋值
- 主要协作：`QDBusConnection::send/call/asyncCall()`、`QDBusError`、`QDBusArgument`

## API 速查

| API | 说明 |
| --- | --- |
| `createMethodCall(service, path, interface, method)` | 创建方法调用消息。通常交给 `QDBusConnection::call()` 或 `asyncCall()` 发送。 |
| `createSignal(path, interface, name)` | 创建广播式 D-Bus 信号。 |
| `createTargetedSignal(service, path, interface, name)` | 创建只发给指定 service 的定向信号。 |
| `createError(...)` | 创建独立错误消息。 |
| `createReply(...)` | 基于收到的方法调用创建正常回复。 |
| `createErrorReply(...)` | 基于收到的方法调用创建错误回复。 |
| `setArguments()` / `operator<<` | 设置或追加消息参数，参数会通过 QVariant/元类型系统封送。 |
| `arguments()` | 读取参数列表。 |
| `service()` | 目标服务名或远端地址。 |
| `path()` | 对象路径。 |
| `interface()` | 接口名。 |
| `member()` | 方法名或信号名。 |
| `signature()` | D-Bus 参数签名，常用于排查类型不匹配。 |
| `type()` | 判断消息是调用、信号、回复、错误还是无效消息。 |
| `errorName()` / `errorMessage()` | 当 `type() == ErrorMessage` 时读取错误详情。 |
| `isReplyRequired()` | 判断方法调用是否需要回复。 |
| `setDelayedReply()` / `isDelayedReply()` | 在服务端槽函数里声明“我稍后手动回复”。 |
| `setAutoStartService()` | 控制方法调用是否允许 bus 自动启动目标服务。 |
| `setInteractiveAuthorizationAllowed()` | 控制是否允许 Polkit 等交互式授权。 |
| `swap()` | 快速交换两个消息。 |

## 消息类型

| `MessageType` | 说明 |
| --- | --- |
| `MethodCallMessage` | 对远端对象某个方法的调用。 |
| `SignalMessage` | 一个 D-Bus signal，可被匹配规则订阅。 |
| `ReplyMessage` | 方法调用的正常返回。 |
| `ErrorMessage` | 方法调用失败返回的错误。 |
| `InvalidMessage` | 空消息或构造失败状态。 |

## 典型用法

```cpp
QDBusMessage call = QDBusMessage::createMethodCall(
    "org.freedesktop.DBus",
    "/org/freedesktop/DBus",
    "org.freedesktop.DBus",
    "ListNames");

call.setAutoStartService(false);

QDBusMessage reply = QDBusConnection::sessionBus().call(call);
if (reply.type() == QDBusMessage::ErrorMessage)
    qWarning() << reply.errorName() << reply.errorMessage();
```

作为服务端，如果某个槽需要异步完成：

```cpp
void Service::longJob(const QDBusMessage &message)
{
    message.setDelayedReply(true);
    startWork([message](const QVariant &result) {
        QDBusConnection::sessionBus().send(message.createReply(result));
    });
}
```

`setDelayedReply(true)` 不是“不要回复”，而是告诉 Qt D-Bus 不要自动生成回复；你承诺之后自己发送 `createReply()` 或 `createErrorReply()`。

## 使用场景

- 需要直接构造低层 D-Bus 方法调用，而不是用动态代理。
- 服务端要自定义回复、延迟回复、错误名和错误消息。
- 调试 D-Bus 类型签名、参数列表和远端错误。
- 发送不绑定到 QObject 信号的 D-Bus signal。
- 控制服务自动激活、交互式授权等消息 flag。

## 常见坑与经验

- `QDBusMessage` 副本共享内部数据，修改副本可能影响原对象；尤其 `setDelayedReply()` 是服务端代码里必须清楚的语义。
- `interface` 为空虽然在某些情况下可行，但如果远端对象多个接口有同名方法，结果可能不可预期。生产代码最好写全接口名。
- D-Bus 不能携带无效 `QVariant`；`setArguments()` 里放错类型时，错误往往到发送或远端解析时才显现。
- `createSignal()` 只负责构造消息，真正发出去要 `QDBusConnection::send()`。
- `setAutoStartService(false)` 适合“只查询已运行服务”的场景，否则默认可能触发 `.service` 激活。
- 高级封装会隐藏原始消息细节；排查问题时回到 `type()`、`signature()`、`errorName()` 更直接。

## 知识点覆盖

- D-Bus 消息四大类别：方法调用、信号、回复、错误
- service/path/interface/member 的寻址结构
- QVariant 到 D-Bus signature 的转换
- 延迟回复与自动回复机制
- D-Bus service activation
- 交互式授权 flag
- 错误名与错误消息的分离
