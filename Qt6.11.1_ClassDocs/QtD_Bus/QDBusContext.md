# QDBusContext
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusContext`

## 作用定位

`QDBusContext` 给服务端槽函数访问“本次 D-Bus 调用上下文”的能力。一个导出的对象继承它后，可以知道当前槽是否由 D-Bus 调用触发、原始 `QDBusMessage` 是什么、调用来自哪条连接，并能发送错误回复或声明延迟回复。

它只在服务端导出对象中有意义；普通客户端代理不需要继承它。

## 类说明

- 头文件：`#include <QDBusContext>`
- CMake：链接 `Qt6::DBus`
- 继承：无公开 QObject 继承；通常与 QObject 业务类多继承
- 典型形态：`class Service : public QObject, protected QDBusContext`

## API 速查

| API | 说明 |
| --- | --- |
| `calledFromDBus()` | 当前函数是否处于 D-Bus 调用处理过程中。 |
| `connection()` | 当前调用所在连接。 |
| `message()` | 当前调用的原始消息。 |
| `setDelayedReply(bool)` | 声明当前调用稍后手动回复。 |
| `isDelayedReply()` | 查询是否已设置延迟回复。 |
| `sendErrorReply(name, msg)` | 发送自定义错误名的错误回复。 |
| `sendErrorReply(type, msg)` | 按标准 `QDBusError::ErrorType` 发送错误回复。 |

## 典型用法

```cpp
void Service::OpenFile(const QString &path)
{
    if (!QFileInfo(path).exists()) {
        sendErrorReply(QDBusError::InvalidArgs, "File does not exist");
        return;
    }

    setDelayedReply(true);
    const QDBusMessage call = message();
    startAsyncOpen(path, [call](bool ok) {
        auto reply = ok ? call.createReply() :
                          call.createErrorReply("org.example.OpenFailed", "Open failed");
        QDBusConnection::sessionBus().send(reply);
    });
}
```

## 使用场景

- 服务端根据调用者或消息内容决定权限和错误。
- 长任务需要延迟回复，避免槽函数同步阻塞。
- 返回规范 D-Bus 错误，而不是抛异常或返回魔法值。
- 调试服务端收到的原始 service/path/interface/member/signature。

## 常见坑与经验

- `message()` 只在 `calledFromDBus()` 为 true 的上下文里有意义；普通本地调用不要依赖它。
- `setDelayedReply(true)` 后必须自己发送正常或错误回复，否则调用者会等到超时。
- `sendErrorReply()` 会结束本次调用的错误路径，之后不要再返回正常业务值。
- 多继承时通常把 `QDBusContext` 设为 protected，避免把上下文 API 暴露成业务接口。
- 延迟回复要保存原始 `QDBusMessage` 的副本，并确保发送回复时连接仍可用。

## 知识点覆盖

- 服务端调用上下文
- 原始消息访问
- 错误回复与延迟回复
- D-Bus 方法调用生命周期
- QObject 导出对象中的多继承模式
