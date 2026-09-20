# QDBusPendingCall
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusPendingCall`

## 作用定位

`QDBusPendingCall` 表示一次已经发出去、但回复可能还没到的 D-Bus 方法调用。它本身不是 QObject，也不发信号；你通常把它交给 `QDBusPendingCallWatcher` 等待完成，或包装成 `QDBusPendingReply<T...>` 读取类型化结果。

它适合保存“异步调用句柄”，但不适合直接承担 UI 通知逻辑。

## 类说明

- 头文件：`#include <QDBusPendingCall>`
- CMake：链接 `Qt6::DBus`
- 继承：无公开 QObject 继承
- 直接派生：`QDBusPendingCallWatcher`
- Qt 6.10 起支持移动构造/移动赋值

## API 速查

| API | 说明 |
| --- | --- |
| `QDBusPendingCall(const QDBusPendingCall &)` | 复制 pending 句柄；副本共享同一条待完成调用。 |
| `QDBusPendingCall(QDBusPendingCall &&)` | 移动 pending 句柄，减少引用复制。 |
| `~QDBusPendingCall()` | 释放引用；若最后一个引用消失且调用未完成，结果将无法再被取回。 |
| `fromCompletedCall(msg)` | 把一个已有 `QDBusMessage` 包装成已完成 pending call，常用于测试或适配同步结果。 |
| `fromError(error)` | 创建一个已完成的错误 pending call。 |
| `swap()` | 快速交换两个 pending 句柄。 |
| `operator=` | 复制或移动赋值，当前引用会被替换。 |

## 典型流程

```cpp
QDBusPendingCall call = iface.asyncCall("GetStatus");
auto *watcher = new QDBusPendingCallWatcher(call, this);

connect(watcher, &QDBusPendingCallWatcher::finished,
        this, [watcher] {
    QDBusPendingReply<QString> reply = *watcher;
    watcher->deleteLater();

    if (reply.isError()) {
        qWarning() << reply.error().name() << reply.error().message();
        return;
    }
    qDebug() << reply.value();
});
```

## 使用场景

- 保存 `asyncCall()` 返回值，稍后交给 watcher 或 reply 解析。
- 编写不依赖事件循环的测试，把同步消息封装为已完成 pending call。
- 在框架层统一传递“一个 D-Bus 异步结果”，暂时不关心具体返回类型。

## 常见坑与经验

- `QDBusPendingCall` 只是句柄，不能自己通知完成；需要 watcher 或事件循环推进状态。
- 复制 pending call 不会复制一次远端调用，只是共享引用。
- 析构不等于取消远端已经执行的操作；它只影响本进程能否再取得结果。
- 直接把 pending call 转成 `QDBusReply` 可能阻塞，因为 `QDBusReply(const QDBusPendingCall &)` 会等待完成。
- 从 `fromError()` 创建的对象已经完成，适合统一错误路径，不适合模拟网络延迟。

## 知识点覆盖

- D-Bus 异步调用句柄
- pending 共享引用语义
- watcher 与 reply 的职责分离
- 已完成调用与错误调用的构造
- 异步结果生命周期
