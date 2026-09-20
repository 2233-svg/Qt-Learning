# QDBusContext：在服务端槽函数中读取本次 D-Bus 调用上下文

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusContext>`  
> 模块：`Qt6::DBus`  
> 相关类：`QDBusMessage`、`QDBusConnection`、`QDBusAbstractAdaptor`

## 它解决什么问题

普通 Qt 槽函数只知道“自己被调用了”，但 D-Bus 服务端有时还需要知道：

- 这次调用是否真的来自 D-Bus。
- 调用从哪条 `QDBusConnection` 到来。
- 原始消息的发送者、路径、接口和序列号是什么。
- 是否应立即自动回复，还是在异步工作完成后再回复。
- 如何向本次调用者返回一个明确的 D-Bus 错误。

`QDBusContext` 是给**被导出真实对象**混入这些能力的轻量类。它不是客户端调用上下文，也不是 `QDBusMessage` 的替代品。

```text
远程客户端
  -> D-Bus method call
  -> 已 registerObject() 的真实 QObject
       + protected QDBusContext
  -> 槽函数读取 message / connection 或决定延迟回复
```

## 适用场景

- 服务端槽函数需要检查调用者、消息元数据或入站连接。
- 业务逻辑无法立即返回，需要排队到稍后完成后再发送回复。
- 服务端要把业务错误映射为规范的 D-Bus error reply。

不适合：

- 客户端等待远程回复，客户端应使用 `QDBusPendingCall`、`QDBusReply` 等。
- 与 `QDBusAbstractAdaptor` 同时作为同一个类的混入基类。

## 正确的继承位置

`QDBusContext` 应在**真实业务对象**上继承，而不是在 adaptor 上继承：

```cpp
class JobService : public QObject, protected QDBusContext
{
    Q_OBJECT
public slots:
    QString StartJob();
};
```

不要让同一个类同时继承 `QDBusContext` 和 `QDBusAbstractAdaptor`。若 adaptor 代码确实需要上下文，应让真实对象公开合适的接口，或在需要时通过其父对象访问上下文能力。

## 第一条规则：先检查 `calledFromDBus()`

服务端方法也可能被本地 C++ 直接调用、通过普通 Qt 信号触发，或者处在并非 D-Bus 分派的上下文中。只有 `calledFromDBus()` 为 `true` 时，其他上下文访问函数才可用。

在它返回 `false` 时调用 `message()`、`connection()`、`sendErrorReply()` 或延迟回复相关函数是未定义行为，甚至可能崩溃。

```cpp
void JobService::Cancel()
{
    if (!calledFromDBus()) {
        cancelLocalJob();
        return;
    }

    const QDBusMessage request = message();
    // 再根据 request.service() 等信息执行服务端策略
}
```

## 立即错误回复

遇到明确的业务错误，可调用 `sendErrorReply()`：

```cpp
void JobService::DeleteJob(const QString &id)
{
    if (!calledFromDBus())
        return;

    if (!hasJob(id)) {
        sendErrorReply(
            QDBusError::InvalidArgs,
            QStringLiteral("Unknown job: %1").arg(id));
        return;
    }

    removeJob(id);
}
```

一旦发送 error reply，槽函数的普通返回值和输出参数会被 Qt D-Bus 忽略。因此应在发错后立即结束该逻辑路径，避免代码读起来像“既成功又失败”。

## 延迟回复的完整责任

默认情况下，槽函数返回时 Qt D-Bus 会自动根据返回值生成 reply。调用 `setDelayedReply(true)` 后，Qt 不再自动回复，也会忽略该槽的返回值和输出参数；服务端必须保存原始 `QDBusMessage` 和 `QDBusConnection`，并在之后自行发送 reply 或 error。

```cpp
QString JobService::StartJob()
{
    if (!calledFromDBus())
        return {};

    const QDBusConnection bus = connection();
    const QDBusMessage request = message();
    setDelayedReply(true);

    startAsyncWork([bus, request](QString result, QString error) {
        if (!error.isEmpty()) {
            bus.send(request.createErrorReply(
                QDBusError::Failed, error));
            return;
        }
        bus.send(request.createReply(result));
    });

    return {}; // 已启用 delayed reply，这个返回值会被忽略
}
```

这不是“后台任务自动完成时就会回复”。若忘记回复，调用方最终会收到 D-Bus timeout error。捕获连接和消息的副本，而不是之后再访问已经离开原调用栈的 `QDBusContext`。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 生命周期 | `QDBusContext()` | 构造上下文混入基类。 | 通常通过真实服务对象的多重继承使用，不单独实例化。 |
| 生命周期 | `~QDBusContext()` | 销毁上下文基类。 | 由派生服务对象生命周期管理。 |
| 上下文检查 | `calledFromDBus()` | 判断当前槽调用是否处于 D-Bus 分派上下文。 | 必须先调用它；返回 `false` 时其他上下文 API 都不能访问。 |
| 入站信息 | `connection()` | 返回接收本次调用的 D-Bus 连接。 | 仅在 `calledFromDBus()` 为 `true` 时可调用；延迟回复时先复制保存。 |
| 入站信息 | `message()` | 返回触发本次槽调用的原始 D-Bus 消息。 | 返回引用只适合当前上下文；异步处理前复制成 `QDBusMessage`。 |
| 延迟回复 | `setDelayedReply(bool enable)` | 选择由 Qt 自动回复，或由服务端稍后手工回复。 | `true` 后返回值和输出参数无效，且必须最终发送 reply 或 error。 |
| 延迟回复 | `isDelayedReply()` | 判断本次调用是否已标记为延迟回复。 | 只反映当前调用；不能替代对异步任务完成状态的跟踪。 |
| 错误回复 | `sendErrorReply(QDBusError::ErrorType type, const QString &msg)` | 以 Qt 预定义错误类型回复调用方。 | 发出后普通返回值会被忽略，应立刻结束处理分支。 |
| 错误回复 | `sendErrorReply(const QString &name, const QString &msg)` | 以自定义 D-Bus 错误名回复调用方。 | 错误名应是稳定、规范的 D-Bus error name，供客户端可靠识别。 |

## 最容易踩的坑

- 在普通本地调用中访问 `message()`：必须先用 `calledFromDBus()` 守卫。
- 启用 `setDelayedReply(true)` 后仍依赖槽函数返回值：返回值已经被忽略。
- 延迟回复时只保存 `this`，稍后才读上下文：先复制 `connection()` 和 `message()`。
- 异步任务出错却没有发送 error reply：调用方只能等到超时。
- 同时在 adaptor 和真实对象上继承上下文：上下文应放在真实对象上。
- `sendErrorReply()` 后继续进行成功返回逻辑：错误和正常输出不能同时作为同一次回复生效。
