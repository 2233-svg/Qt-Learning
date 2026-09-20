# Qt QDBusPendingCallWatcher 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusPendingCallWatcher>`  
> 所属模块：`Qt6::DBus`  
> 继承：`QObject`、`QDBusPendingCall`

## 1. 它解决什么问题

`QDBusPendingCall` 能保存一次异步 D-Bus 调用，却没有完成信号。若每次都自己轮询，既浪费代码又很容易因为事件循环没有运行而永远看不到状态变化。

`QDBusPendingCallWatcher` 为一笔 `QDBusPendingCall` 加上 `QObject` 能力：它在回复到达或调用超时时发出 `finished()`。因此它解决的是“异步调用完成后，在正确的对象生命周期中继续处理结果”。

```text
发起 asyncCall()
      │
      ▼
QDBusPendingCall
      │  交给 watcher
      ▼
QDBusPendingCallWatcher
      │  finished()
      ▼
QDBusPendingReply<T...> 读取成功值或 QDBusError
```

它同时继承 `QObject` 和 `QDBusPendingCall`。这意味着 watcher 既可以用 parent 管理内存，又持有 pending call 的共享引用。创建 watcher 后通常不必保留原始 `QDBusPendingCall`。

## 2. 构建与最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
```

```cpp
#include <QDBusPendingCallWatcher>
#include <QDBusPendingReply>

QDBusPendingCall call = iface.asyncCall("GetDisplayName");
auto *watcher = new QDBusPendingCallWatcher(call, this);

connect(watcher, &QDBusPendingCallWatcher::finished, this,
        [watcher] {
            QDBusPendingReply<QString> reply = *watcher;

            if (reply.isError())
                qWarning() << reply.error().name() << reply.error().message();
            else
                setDisplayName(reply.value());

            watcher->deleteLater();
        });
```

这里的 `this` 是接收结果的 `QObject`。它同时充当 signal-slot 的上下文对象和 watcher 的父对象：页面或服务对象销毁时，watcher 会一同销毁，连接也会自动断开。

## 3. 使用模型

### 3.1 创建 watcher 后立即连接 `finished`

先建立 watcher，再连接信号。对于正常的异步 D-Bus 请求，回复通常在下一轮事件处理后到达；但把连接写在紧邻构造的位置仍是更稳妥的习惯。

### 3.2 在槽或 lambda 中转换为 `QDBusPendingReply`

watcher 不知道你的远端方法返回哪些类型。应在完成回调中按协议构造 `QDBusPendingReply<T...>`：

```cpp
connect(watcher, &QDBusPendingCallWatcher::finished, this,
        [watcher](QDBusPendingCallWatcher *) {
            QDBusPendingReply<QString, QByteArray> reply = *watcher;
            if (reply.isError())
                return;

            const QString title = reply.argumentAt<0>();
            const QByteArray payload = reply.argumentAt<1>();
            consume(title, payload);
        });
```

若返回参数数量或类型不符合模板声明，`reply.isError()` 会为真。这样能把 D-Bus 协议错误留在边界处处理。

### 3.3 watcher 的销毁时机

如果 watcher 是未完成调用的最后一个引用，它析构会取消调用。通常将 watcher 设为拥有结果对象的子对象，并在 `finished()` 后 `deleteLater()`；不要把栈上的 watcher 跨越异步返回范围使用。

## 4. 事件循环与 `waitForFinished()`

`isFinished()` 只有在回复被处理后才会变为 `true`。这通常依赖线程返回事件循环，或者由当前线程调用 `waitForFinished()` 处理等待。

```cpp
watcher->waitForFinished();
Q_ASSERT(watcher->isFinished());
```

`waitForFinished()` 会挂起调用线程直到回复被接收和处理。它适合命令行程序、测试代码、启动阶段或专用工作线程；不要在 GUI 主线程使用，否则窗口无法重绘、输入也无法响应。

对于 UI，始终让事件循环运行并在 `finished()` 中继续后续逻辑。

## 5. 常见误区

### 5.1 误区：Watcher 是纯通知器，不影响请求

它也是 `QDBusPendingCall` 的一个引用。若它是最后一个未完成引用，销毁 watcher 会取消调用。

### 5.2 误区：调用 `isFinished()` 会主动刷新状态

不会。状态的变化依赖外部 D-Bus 事件被事件循环处理，或你调用 `waitForFinished()`。

### 5.3 误区：`finished()` 一定表示成功

不一定。完成意味着回复可读，回复可能是远端错误、超时，或与预期类型不匹配。回调中必须调用 `reply.isError()`。

### 5.4 误区：为 watcher 分配内存后无需清理

父对象可在整体销毁时清理它，但若请求频繁且父对象长期存活，已完成 watcher 会积累。完成后 `deleteLater()` 是常用做法。

## 6. 逐项 API 说明

### 构造与析构

#### `explicit QDBusPendingCallWatcher(const QDBusPendingCall &call, QObject *parent = nullptr)`

开始观察 `call` 的回复，并将 watcher 的父对象设为 `parent`。watcher 自己也持有该 pending call，构造成功后原始 `call` 可以离开作用域。

#### `virtual ~QDBusPendingCallWatcher()`

销毁 watcher。若它是未完成调用的最后一个引用，该调用会被取消；所以不要在仍期待回复时过早销毁它。

### 完成状态

#### `void finished(QDBusPendingCallWatcher *self = nullptr)`

当调用完成、回复已可访问时发出。`self` 是 watcher 本身，方便传统槽函数直接读取结果；lambda 中通常直接捕获或使用参数即可。

完成仅表示“有回复可处理”，不是“远端成功”。请将 `*self` 或 `*watcher` 构造成 `QDBusPendingReply<T...>` 后检查 `isError()`。

#### `bool isFinished() const`

若调用已完成且回复已处理则返回 `true`。它不是主动轮询网络的 API；要让异步回复推进，线程需要运行事件循环。

#### `void waitForFinished()`

阻塞调用线程，直到回复已接收和处理。返回后 `isFinished()` 应为 `true`，但回复仍可能是错误；不能用它替代错误判断。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDBusPendingCallWatcher(const QDBusPendingCall &call, QObject *parent)` | 观察一笔异步调用，并可绑定到 `parent`。 | watcher 自己持有调用引用；推荐传入管理结果的 QObject 作为父对象。 |
| 析构 | `~QDBusPendingCallWatcher()` | 销毁 watcher 和它持有的调用引用。 | 若为最后一个未完成引用，会取消调用。 |
| 信号 | `finished(QDBusPendingCallWatcher *self)` | 在回复已到达、可读取时通知。 | 完成不等于成功；转换为 `QDBusPendingReply<T...>` 后检查 `isError()`。 |
| 状态查询 | `bool isFinished() const` | 判断回复是否已完成处理。 | 事件循环未运行时状态不会靠轮询自动推进。 |
| 阻塞等待 | `void waitForFinished()` | 等到回复被接收和处理。 | 会阻塞当前线程，不要在 GUI 主线程调用。 |

---

### 一句话总结

`QDBusPendingCallWatcher` 是异步 D-Bus 调用的完成通知器和生命周期锚点；在 `finished()` 中读取 `QDBusPendingReply`，并把阻塞等待留给不会卡住界面的线程。
