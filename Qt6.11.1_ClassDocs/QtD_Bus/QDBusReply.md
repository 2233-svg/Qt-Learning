# QDBusReply
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusReply`

## 作用定位

`QDBusReply<T>` 是同步 D-Bus 调用结果的轻量包装：它把 `QDBusMessage`、`QDBusPendingCall` 或 `QDBusPendingReply<T>` 中的第一个返回值转换成 C++ 类型 `T`，同时保存错误对象。

它适合“一个调用只返回一个值”的场景，比如查询布尔状态、字符串列表、PID、UID。返回多个值时，应优先用 `QDBusPendingReply<T1, T2...>` 或直接解析 `QDBusMessage`。

## 类说明

- 头文件：`#include <QDBusReply>`
- CMake：链接 `Qt6::DBus`
- 模板类型：远端返回的第一个输出参数类型；`QDBusReply<void>` 用于只关心成功/失败
- 继承：无公开 QObject 继承

## API 速查

| API | 说明 |
| --- | --- |
| `QDBusReply(error)` | 构造一个错误结果。 |
| `QDBusReply(message)` | 从方法回复消息取第一个返回值；错误消息会转为 `error()`。 |
| `QDBusReply(pcall)` | 从 pending call 构造；如果未完成会阻塞等待。 |
| `QDBusReply(QDBusPendingReply<T>)` | 从类型化 pending reply 构造。 |
| `isValid()` | 是否成功且没有 D-Bus 错误。 |
| `error()` | 返回远端或本地转换错误。 |
| `value()` | 读取返回值；无效时结果未定义。 |
| `operator T()` | 便利转换，语义同 `value()`。 |
| `operator=` | 用错误、消息或 pending call 替换当前结果。 |

## 典型用法

```cpp
QDBusReply<QStringList> names =
    QDBusConnection::sessionBus().interface()->registeredServiceNames();

if (!names.isValid()) {
    qWarning() << names.error().name() << names.error().message();
    return;
}

for (const QString &name : names.value())
    qDebug() << name;
```

## 使用场景

- 调用 `QDBusConnectionInterface` 的管理函数。
- 包装 `QDBusInterface::call()` 的单返回值结果。
- 只需要成功/失败与一个返回值，不需要保留原始消息细节。

## 常见坑与经验

- 一定先检查 `isValid()` 再取 `value()`；错误时返回值可能与合法默认值无法区分。
- 从 `QDBusPendingCall` 构造会阻塞，这是很多“明明用了 asyncCall 却卡住”的来源。
- 类型不匹配也会成为错误。远端实际返回 `uint`，你用 `int` 接，不一定按你预期转换。
- `operator T()` 虽然简洁，但会弱化错误检查；库代码更建议显式 `isValid()` + `value()`。
- `QDBusReply<void>` 没有 `value()`，只能看 `isValid()` 和 `error()`。

## 知识点覆盖

- 同步 D-Bus 回复解析
- 单返回值与 void 返回
- D-Bus 错误和类型转换错误
- pending call 的隐式阻塞风险
- `QDBusConnectionInterface` 常见返回类型
