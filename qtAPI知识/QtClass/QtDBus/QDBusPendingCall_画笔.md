# Qt QDBusPendingCall 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusPendingCall>`  
> 所属模块：`Qt6::DBus`  
> 类型特征：显式共享的异步调用句柄，不继承 `QObject`

## 1. 它解决什么问题

D-Bus 方法调用可能要等待另一个进程响应。同步调用虽然写起来像普通函数返回，但会阻塞当前线程；在 GUI 线程中尤其容易让界面失去响应。

`QDBusPendingCall` 表示“一次已经发出、但回复还未到达的异步方法调用”。它不是结果容器，也不是可直接操作的请求对象，而是一个不透明句柄：持有它，就还能跟踪这次调用；失去最后一个引用时，尚未完成的调用会被取消。

典型关系如下：

```text
QDBusInterface::asyncCall()
        │
        └─> QDBusPendingCall
                ├─ QDBusPendingReply<T...>：以类型安全方式读结果
                └─ QDBusPendingCallWatcher：用 finished 信号获知完成
```

实际程序中，通常不直接长期使用裸 `QDBusPendingCall`，而是立即将它交给 `QDBusPendingReply<T...>` 或 `QDBusPendingCallWatcher`。

## 2. 构建与最小调用

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
```

```cpp
#include <QDBusConnection>
#include <QDBusInterface>
#include <QDBusPendingCall>

QDBusInterface iface(
    "org.example.Service",
    "/org/example/Service",
    "org.example.Service",
    QDBusConnection::sessionBus());

QDBusPendingCall call = iface.asyncCall("Refresh");
```

上面语句返回时，请求已进入异步调用流程，但并不表示远端方法已经执行成功。成功、远端错误和超时都要在调用完成后判断。

## 3. 选择正确的协作类型

### 3.1 需要非阻塞地处理结果：`QDBusPendingCallWatcher`

```cpp
QDBusPendingCall call = iface.asyncCall("GetName");
auto *watcher = new QDBusPendingCallWatcher(call, this);

connect(watcher, &QDBusPendingCallWatcher::finished, this,
        [watcher] {
            QDBusPendingReply<QString> reply = *watcher;
            if (reply.isError())
                qWarning() << reply.error().message();
            else
                qDebug() << reply.value();

            watcher->deleteLater();
        });
```

这是界面和事件驱动服务中最常用的方式。watcher 自身持有这次 pending call，因此在创建 watcher 后不必额外保存原始 `call`。

### 3.2 需要类型化结果：`QDBusPendingReply<T...>`

```cpp
QDBusPendingReply<QString, int> reply = iface.asyncCall("GetInfo");
reply.waitForFinished();

if (!reply.isError()) {
    const QString name = reply.argumentAt<0>();
    const int version = reply.argumentAt<1>();
}
```

`QDBusPendingReply` 会验证回复参数是否与模板类型匹配。类型、参数个数不匹配也会表现为错误，避免把 `QVariant` 列表硬转换后才发现协议不一致。

### 3.3 只是在测试中构造“已完成调用”

`fromCompletedCall()` 与 `fromError()` 可构造无需等待的 pending call，适合测试异步处理分支或适配层，不用于发送真实请求。

## 4. 显式共享与取消语义

`QDBusPendingCall` 是**显式共享**对象。复制它并不会复制请求，也不会让两份副本各自等待；副本都引用同一笔 pending call，且没有 detach 操作。

```cpp
QDBusPendingCall first = iface.asyncCall("Refresh");
QDBusPendingCall second = first; // 两者跟踪同一笔调用
```

这带来一个关键生命周期规则：

- 调用未完成时，最后一个 `QDBusPendingCall` 或 watcher 被销毁，会取消调用。
- 取消后不再收到完成通知，也无法在回复最终抵达时读取内容。
- 复制赋值若丢弃了某次调用的最后一个引用，也会触发同样的取消。

因此，异步调用不应写成临时对象后立即消失：

```cpp
iface.asyncCall("Refresh"); // 返回值马上销毁，未完成调用可能被取消
```

应该保存结果，或直接创建 watcher。

## 5. 超时、事件循环与阻塞

调用的超时由发起异步调用的 API 决定，例如 `QDBusConnection::asyncCall()` 的默认 `timeout` 是实现定义值，通常约为 25 秒。超时时结果会变成错误回复。

`QDBusPendingCall` 自己不提供完成信号。事件驱动代码应使用 watcher；需要同步等待时使用 `QDBusPendingReply::waitForFinished()` 或 watcher 的同名函数。

在 GUI 主线程调用 `waitForFinished()` 会冻结事件处理，应只在确实允许阻塞的工作线程、命令行工具或启动阶段使用。

## 6. 常见误区

### 6.1 误区：复制得到两次独立请求

复制只增加同一次调用的引用数。若要发两次请求，就调用两次 `asyncCall()`。

### 6.2 误区：析构只是释放一个轻量对象

最后一个引用析构会取消尚未完成的调用。这个规则使对象生命周期直接影响网络行为。

### 6.3 误区：`asyncCall()` 返回就说明成功

只说明请求已按异步路径提交。远端不存在、权限不足、参数类型不对或超时，都要在 `QDBusPendingReply::isError()` 中处理。

### 6.4 误区：移动后还能继续查询原对象

Qt 6.10 起提供移动构造和移动赋值。被移动对象处于部分形成状态，只能销毁或重新赋值。

## 7. 逐项 API 说明

### 构造、复制与析构

#### `QDBusPendingCall(const QDBusPendingCall &other)`

创建 `other` 的共享副本。两个对象指向同一次未完成或已完成调用；复制可防止某一处过早销毁就取消请求。

#### `QDBusPendingCall(QDBusPendingCall &&other)`，Qt 6.10 起

移动 `other` 的句柄状态，避免增加共享引用。移动后的 `other` 只能销毁或重新赋值。

#### `~QDBusPendingCall()`

销毁当前引用。若这是未完成调用的最后一个引用，该调用被取消，之后不能再获得其回复。

### 工厂函数

#### `static QDBusPendingCall fromCompletedCall(const QDBusMessage &msg)`

从一条已经完成的回复消息构造 pending call。`msg` 必须是 `QDBusMessage::ReplyMessage` 或 `QDBusMessage::ErrorMessage`，适合测试和统一处理已完成结果。

#### `static QDBusPendingCall fromError(const QDBusError &error)`

构造一个已完成的错误调用。把它转换为 `QDBusPendingReply<T...>` 后，`isError()` 会返回 `true`。

### 赋值与交换

#### `void swap(QDBusPendingCall &other)`

快速交换两个句柄。常用于泛型代码或实现内部操作，不会等待网络，也不会改变两笔调用本身。

#### `operator=(QDBusPendingCall &&other)`，Qt 6.10 起

移动赋值。当前对象放弃原先引用；若原引用是未完成调用的最后一个引用，该调用会被取消。

#### `operator=(const QDBusPendingCall &other)`

复制赋值为 `other` 所代表的调用，同时丢弃当前引用。与析构一样，要注意是否因此取消当前对象原先跟踪的调用。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 复制构造 | `QDBusPendingCall(const QDBusPendingCall &other)` | 创建同一次异步调用的共享句柄。 | 副本不是新请求；保留任一副本都可避免过早取消。 |
| 移动构造 | `QDBusPendingCall(QDBusPendingCall &&other)` | 移入 `other` 的句柄状态。 | Qt 6.10 起可用；移动后只销毁或重新赋值 `other`。 |
| 析构 | `~QDBusPendingCall()` | 释放当前调用引用。 | 最后一个未完成引用析构会取消调用。 |
| 静态工厂 | `fromCompletedCall(const QDBusMessage &msg)` | 将已完成回复包装成 pending call。 | 仅接受 ReplyMessage 或 ErrorMessage；适合测试、适配层。 |
| 静态工厂 | `fromError(const QDBusError &error)` | 构造一个已完成的错误调用。 | 转换为 `QDBusPendingReply` 后应通过 `isError()` 处理。 |
| 交换 | `swap(QDBusPendingCall &other)` | 交换两个调用句柄。 | 不会发送、取消或等待任何请求。 |
| 移动赋值 | `operator=(QDBusPendingCall &&other)` | 用移动方式替换当前句柄。 | Qt 6.10 起可用；被替换调用可能因失去最后引用而取消。 |
| 复制赋值 | `operator=(const QDBusPendingCall &other)` | 改为跟踪 `other` 所代表的调用。 | 覆盖前保存当前调用的其他引用，避免意外取消。 |

---

### 一句话总结

`QDBusPendingCall` 是一次异步 D-Bus 方法调用的共享句柄；不要让最后一个引用过早消失，实际结果处理优先交给 `QDBusPendingReply` 与 `QDBusPendingCallWatcher`。
