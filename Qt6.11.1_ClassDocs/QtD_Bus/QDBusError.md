# QDBusError
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusError`

## 作用定位

`QDBusError` 是 D-Bus 错误的 Qt 表示。它把错误分成三层：标准化的 `ErrorType`、D-Bus 错误名 `name()`、面向人的描述 `message()`。调试 D-Bus 时不要只打印 `message()`，错误名通常才是最稳定、最适合分支处理的信息。

## 类说明

- 头文件：`#include <QDBusError>`
- CMake：链接 `Qt6::DBus`
- 继承：无公开 QObject 继承
- 常见来源：`QDBusReply::error()`、`QDBusPendingReply::error()`、`QDBusConnection::lastError()`、`QDBusMessage::createErrorReply()`

## API 速查

| API | 说明 |
| --- | --- |
| `isValid()` | 是否真的包含错误；无错误时返回 false。 |
| `type()` | 返回 Qt 归类后的标准错误类型。 |
| `name()` | 返回 D-Bus 错误名，如 `org.freedesktop.DBus.Error.ServiceUnknown`。 |
| `message()` | 返回面向人的错误说明。 |
| `errorString(type)` | 把标准 `ErrorType` 转成 D-Bus 错误名字符串。 |
| `swap()` | 快速交换两个错误对象。 |

## 常见错误类型

| `ErrorType` | 说明 |
| --- | --- |
| `NoError` | 没有错误，`QDBusError` 无效。 |
| `ServiceUnknown` | 目标服务名不存在，或不能被激活。 |
| `NoReply` / `TimedOut` / `Timeout` | 回复超时或等待失败；要检查远端是否阻塞、权限是否卡住、超时是否过短。 |
| `AccessDenied` | 权限不足，system bus 上很常见。 |
| `InvalidArgs` / `InvalidSignature` | 参数数量、类型或 D-Bus 签名不匹配。 |
| `UnknownMethod` / `UnknownInterface` / `UnknownObject` | service 存在，但对象路径、接口或方法名不对。 |
| `UnknownProperty` / `PropertyReadOnly` | 属性不存在或只读。 |
| `AddressInUse` | `QDBusServer` 绑定地址已被占用。 |
| `Disconnected` | 连接已经断开后还在发送或等待。 |
| `Other` | 错误名不是 Qt 预定义集合中的标准项。 |

## 使用场景

- 处理同步/异步调用失败。
- 服务端构造错误回复，让调用者得到规范错误名。
- 把权限、路径错误、类型错误、超时错误拆开处理。
- 日志记录时同时输出错误名和消息，方便跨语言排查。

## 常见坑与经验

- `message()` 适合给人看，不适合作为程序分支条件；分支应优先看 `type()` 或 `name()`。
- `Other` 不代表“不重要”，只代表 Qt 没把这个错误归到标准枚举里。自定义服务错误通常会落在这里。
- `NoReply` 经常不是网络问题，而是远端方法内部阻塞、授权弹窗没完成、或调用线程自己死锁。
- system bus 上的 `AccessDenied` 往往要查 D-Bus policy 或 Polkit，不是 Qt API 调错。
- `NoError` 对应无效错误对象，因此 `isValid()` 为 false 才是成功。

## 知识点覆盖

- D-Bus 错误名与 Qt 错误枚举的映射
- 调用失败、类型失败、权限失败的区分
- 错误日志的有效打印方式
- 服务端错误回复设计
