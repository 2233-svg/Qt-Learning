# QDBusPendingCallWatcher
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusPendingCallWatcher`

## 作用定位

`QDBusPendingCallWatcher` 把 `QDBusPendingCall` 变成 QObject 世界里的完成通知。它继承 `QObject` 和 `QDBusPendingCall`：一边保留 pending 结果，一边在结果到达时发出 `finished()` 信号。

它是 GUI 或事件驱动程序里处理异步 D-Bus 调用最常用的桥。

## 类说明

- 头文件：`#include <QDBusPendingCallWatcher>`
- CMake：链接 `Qt6::DBus`
- 继承：`QObject`、`QDBusPendingCall`
- 生命周期：通常 `new` 出来并设置 parent，在 `finished()` 槽里 `deleteLater()`

## API 速查

| API | 说明 |
| --- | --- |
| `QDBusPendingCallWatcher(call, parent)` | 监听一条 pending call，并按 QObject parent 管理生命周期。 |
| `~QDBusPendingCallWatcher()` | 销毁 watcher；不会让已经发出的远端调用自动回滚。 |
| `finished(self)` | 调用完成时发出，`self` 通常就是 watcher 自己。 |
| `isFinished()` | 查询结果是否已经到达并处理。 |
| `waitForFinished()` | 阻塞当前线程直到完成；GUI 线程慎用。 |

## 典型用法

```cpp
auto *watcher = new QDBusPendingCallWatcher(iface.asyncCall("ListNames"), this);
connect(watcher, &QDBusPendingCallWatcher::finished,
        this, [watcher] {
    QDBusPendingReply<QStringList> reply = *watcher;
    watcher->deleteLater();

    if (!reply.isError())
        qDebug() << reply.value();
});
```

## 使用场景

- 在 QObject/信号槽代码里等待 D-Bus 异步结果。
- GUI 中避免同步 `call()` 阻塞界面。
- 让异步调用结果跟随某个 context 对象自动断开。

## 常见坑与经验

- `finished()` 发出后仍要先构造 `QDBusPendingReply<T...>` 并检查 `isError()`。
- watcher 常见泄漏点是忘记在回调里 `deleteLater()`，或者没有设置 parent。
- `waitForFinished()` 适合后台线程或测试，不适合主线程响应用户操作。
- lambda 捕获 watcher 指针时，优先把 watcher 设为 parent 管理对象，降低提前销毁风险。
- `finished(QDBusPendingCallWatcher *self)` 的参数让同一个槽可处理多个 watcher。

## 知识点覆盖

- pending call 到 QObject 信号的转换
- `QDBusPendingReply` 解析 watcher
- 事件循环与异步完成通知
- QObject 生命周期和 `deleteLater()`
