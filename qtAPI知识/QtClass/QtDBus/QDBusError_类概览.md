# QDBusError：读取 D-Bus 调用失败的结构化信息

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusError>`  
> 模块：`Qt6::DBus`  
> 相关类：`QDBusReply`、`QDBusMessage`、`QDBusContext`

## 它解决什么问题

D-Bus 调用失败时，失败并不只是一个布尔值。可能是服务名不存在、对象路径错误、方法未知、权限被拒绝、服务端主动返回业务错误，或总线超时。

`QDBusError` 把这类失败表示为三个互补信息：

```text
ErrorType  -> Qt 可识别的常见错误类别
name       -> 原始 D-Bus 错误名，可用于协议级判断
message    -> 远端或总线附带的说明文本
```

它是客户端检查 `QDBusReply::error()`、`QDBusPendingReply::error()` 和 `QDBusAbstractInterface::lastError()` 的值类型。它不是 C++ 异常，也不是服务端创建 error reply 的首选工具。

## 什么时候使用

- 同步 D-Bus 调用后检查 `QDBusReply<T>`。
- 异步调用完成后检查 `QDBusPendingReply<T>`。
- 需要按错误类别决定重试、提示、重新发现服务或提示权限问题。
- 需要记录原始 D-Bus error name 以便排查跨进程协议问题。

服务端主动回错误时，使用 `QDBusContext::sendErrorReply()` 或 `QDBusMessage::createError()` 加 `QDBusConnection::send()`；不要为了“制造一个错误”自行构造 `QDBusError`。

## 正确的客户端处理方式

```cpp
QDBusReply<QString> reply = player.call("CurrentTrack");
if (!reply.isValid()) {
    const QDBusError error = reply.error();

    switch (error.type()) {
    case QDBusError::ServiceUnknown:
    case QDBusError::Disconnected:
        reconnectOrRediscoverService();
        break;
    case QDBusError::AccessDenied:
        showPermissionHelp();
        break;
    default:
        qWarning() << error.name() << error.message();
        break;
    }
    return;
}

useTrack(reply.value());
```

这里的关键是按 `type()` 或稳定的 `name()` 分支，而不是用 `message()` 做程序逻辑。错误消息是实现定义的人类可读文本，可能随服务版本、语言环境和后端变化。

## 常见错误类别如何理解

- 定位失败：`ServiceUnknown`、`UnknownObject`、`UnknownInterface`、`UnknownMethod`。
- 调用契约失败：`InvalidArgs`、`InvalidSignature`、`InvalidObjectPath`、`InvalidMember`。
- 可恢复的连接问题：`NoReply`、`Timeout`、`TimedOut`、`Disconnected`、`NoNetwork`。
- 权限和能力问题：`AccessDenied`、`NotSupported`、`PropertyReadOnly`。
- 服务端或总线内部失败：`Failed`、`InternalError`、`Other`。

`NoError` 表示没有错误，因此对应的 `QDBusError` 是无效对象。这个命名容易反直觉：`error.isValid()` 为 `false` 才意味着没有 D-Bus error。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `QDBusError::ErrorType` | 将常见 D-Bus 错误映射为稳定的 Qt 枚举。 | 用于程序分支；未知或自定义错误会归入 `Other`。 |
| 枚举值 | `NoError` | 表示没有错误。 | 此时 `QDBusError::isValid()` 返回 `false`。 |
| 枚举值 | `ServiceUnknown`、`UnknownObject`、`UnknownInterface`、`UnknownMethod` | 表示服务、对象、接口或方法定位失败。 | 先核对 service、path、interface、method 四段定位信息。 |
| 枚举值 | `InvalidArgs`、`InvalidSignature`、`InvalidObjectPath`、`InvalidService`、`InvalidInterface`、`InvalidMember` | 表示调用参数或 D-Bus 标识符不合法。 | 多为协议契约错误，重试通常无效，应修正调用方。 |
| 枚举值 | `NoReply`、`Timeout`、`TimedOut`、`Disconnected`、`NoNetwork` | 表示等待、连接或网络失败。 | 根据业务幂等性决定重试；不要对非幂等命令盲目重发。 |
| 枚举值 | `AccessDenied`、`NotSupported`、`PropertyReadOnly` | 表示权限、能力或只读限制。 | 向用户显示可理解说明，并保留原始错误名用于诊断。 |
| 枚举值 | `Failed`、`InternalError`、`NoMemory`、`LimitsExceeded`、`Other` | 表示服务端、总线或未归类失败。 | `Other` 时尤其要记录 `name()` 与 `message()`。 |
| 静态函数 | `errorString(ErrorType error)` | 返回枚举对应的标准 D-Bus 错误名。 | 用于服务端构造规范错误名或诊断，不替代实际错误对象。 |
| 状态 | `isValid()` | 判断此对象是否真的包含一个错误。 | `true` 表示发生错误，和一般“有效即成功”的直觉相反。 |
| 错误内容 | `type()` | 返回标准化错误类别。 | 适合业务代码分类；自定义错误可能是 `Other`。 |
| 错误内容 | `name()` | 返回远端或总线提供的完整 D-Bus 错误名。 | 适合稳定协议匹配和日志；不要只依赖 `ErrorType` 覆盖所有自定义错误。 |
| 错误内容 | `message()` | 返回错误的文字说明。 | 面向日志或用户提示时可加工；不可作为稳定程序判断依据。 |
| 生命周期 | `swap(QDBusError &other)` | 高效交换两个错误对象。 | `noexcept`；在泛型容器或状态转移中偶尔有用。 |

## 最容易踩的坑

- 把 `isValid()` 当“调用成功”：对 `QDBusError` 来说它表示“确实有错误”。
- 用 `message()` 判断错误种类：改用 `type()` 或 `name()`。
- 将 `NoReply` 与 `TimedOut` 视为一定可安全重试：先判断远程命令是否幂等。
- 服务端直接构造 `QDBusError`：应发送 `QDBusMessage` 错误回复。
- 只记录一个翻译后的提示：同时记录 `name()` 和原始 `message()`，排查会轻松很多。
