# QDBusPendingReply
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusPendingReply`

## 作用定位

`QDBusPendingReply<Types...>` 是异步 D-Bus 回复的类型化读取器。它把 `QDBusPendingCall` 或 watcher 中的原始回复，按模板参数解释成一个或多个返回值。

它和 `QDBusReply<T>` 的区别在于：`QDBusPendingReply` 可以表示“还没完成”，并能在完成后读取多个输出参数；`QDBusReply` 更偏同步调用返回的单值结果。

## 类说明

- 头文件：`#include <QDBusPendingReply>`
- CMake：链接 `Qt6::DBus`
- 继承：`QDBusPendingReplyBase`
- 模板参数：返回值类型列表；`QDBusPendingReply<void>` 表示没有返回值
- Qt 6.10 起支持移动构造/移动赋值

## API 速查

| API | 说明 |
| --- | --- |
| `QDBusPendingReply()` | 空回复，没有绑定调用。 |
| `QDBusPendingReply(message)` | 从已完成消息构造。 |
| `QDBusPendingReply(call)` | 从 pending call 构造，共享同一异步结果。 |
| `QDBusPendingReply(other)` | 复制 reply，仍共享同一异步调用引用。 |
| `count()` / `Count` | 模板声明的返回参数个数。 |
| `isFinished()` | 是否已收到并处理回复。 |
| `isValid()` | 是否是正常回复且类型匹配。 |
| `isError()` | 是否是错误；未完成时也会返回 true，所以要结合 `isFinished()`。 |
| `error()` | 读取错误详情。 |
| `reply()` | 读取原始 `QDBusMessage`。 |
| `argumentAt(index)` | 按位置读取返回参数，适合多返回值。 |
| `value()` / 转换运算符 | 读取第一个返回值；未完成时会阻塞等待。 |
| `waitForFinished()` | 显式阻塞等待完成。 |
| `operator=` | 用消息、pending call、另一个 pending reply 替换当前引用。 |

## 典型用法

```cpp
QDBusPendingReply<QString, int> reply = iface.asyncCall("ReadInfo");
reply.waitForFinished();

if (reply.isError()) {
    qWarning() << reply.error().name();
    return;
}

QString name = reply.argumentAt(0).toString();
int version = reply.argumentAt(1).toInt();
```

在事件驱动代码中，更推荐由 watcher 完成后再读取：

```cpp
QDBusPendingReply<QString> reply = *watcher;
if (!reply.isError())
    consume(reply.value());
```

## 使用场景

- 异步方法返回一个或多个值。
- 希望在 C++ 类型层面约束 D-Bus 返回签名。
- watcher 完成后把原始 pending call 转成易读结果。
- 测试中从已完成消息构造类型化回复。

## 常见坑与经验

- `value()` 和转换运算符可能阻塞；如果你在 GUI 线程里调用它而回复未到，界面会停住。
- `isError()` 在未完成时也可能为 true，不要把它当作“远端失败”的唯一判断。
- 模板类型数量或类型与远端签名不一致时，reply 会变成错误状态。
- `argumentAt()` 返回 `QVariant`，多返回值读取时要清楚每个位置的类型。
- 赋值替换当前 pending 引用时，如果旧引用是最后一个引用且尚未完成，旧结果将无法再读取。

## 知识点覆盖

- 异步回复的类型化解析
- 多输出参数读取
- 签名匹配与错误状态
- 阻塞等待和事件循环完成的差别
- 与 watcher、pending call 的共享引用关系
