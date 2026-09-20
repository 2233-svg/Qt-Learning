# QDBusAbstractInterface：远程 D-Bus 接口的客户端基类

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusAbstractInterface>`  
> 模块：`Qt6::DBus`  
> 继承：`QObject`  
> 相关类：`QDBusInterface`、`QDBusPendingCall`、`QDBusMessage`、`QDBusError`

## 它解决什么问题

`QDBusAbstractInterface` 表示“本进程持有的一个远程 D-Bus 对象接口引用”。它保存四个定位信息：

```text
QDBusConnection + service + object path + interface name
```

在这个定位之上，它提供同步调用、异步调用、回调调用、超时配置和错误查询。`QDBusInterface` 是它的通用具体子类；`qdbusxml2cpp` 生成的强类型客户端类也继承它。

它本身不实现某个业务接口。若接口 XML 已知，优先用生成的代理类获得编译期参数、返回值和属性类型检查；若接口动态发现或只调用少量方法，使用 `QDBusInterface`。

## 适用场景

- 客户端调用远程服务对象的方法。
- 为某个 D-Bus interface 生成或编写强类型 C++ 代理。
- 统一设置一组远程调用的超时与授权策略。

不适合：

- 服务端导出本地对象，应使用 `QDBusAbstractAdaptor`。
- 只想发送裸 `QDBusMessage`，可直接通过 `QDBusConnection`。

## 最小调用：用具体子类 `QDBusInterface`

```cpp
#include <QDBusInterface>
#include <QDBusReply>

QDBusInterface player(
    "org.example.Player",
    "/Player",
    "org.example.Player",
    QDBusConnection::sessionBus());

if (!player.isValid()) {
    qWarning() << player.lastError().message();
    return;
}

QDBusReply<QString> reply = player.call("CurrentTrack");
if (!reply.isValid())
    qWarning() << reply.error().message();
else
    qDebug() << reply.value();
```

`isValid()` 能发现创建接口时的明显错误，但远程对象在网络或总线另一端，创建引用时未必能完全确认其仍存在。因此每次实际调用也要处理返回消息或 `QDBusReply` 的错误。

## 三种调用模型

### 1. 同步 `call()`

`call()` 返回 `QDBusMessage`。它适合结果马上决定后续流程的短调用，但调用线程会等待回复。某些 `QDBus::CallMode` 会在等待期间处理事件；此时其他信号、远程方法和 queued event 可能重入当前对象，代码必须能承受重入。

不要在 UI 主线程对慢服务使用同步调用。更重要的是，不能把“事件循环仍在转”误解为没有阻塞：用户输入可能被排除，状态仍然会在等待期间变化。

### 2. 异步 `asyncCall()`

`asyncCall()` 返回 `QDBusPendingCall`。将其交给 `QDBusPendingCallWatcher`，在 `finished` 信号中读取 `QDBusPendingReply`，是最适合界面和长耗时服务的方式。

本应用自己注册到 D-Bus 的对象有实现限制，方法调用不会真正异步；不要用本地回环测试来推断跨进程调用的时序。

### 3. 回调 `callWithCallback()`

该函数提交后立即返回，回复被投递到接收对象的指定槽。其布尔返回值只表示“调用是否成功排队”，不表示远程方法成功执行；远程错误会走错误槽，而不会可靠地反映到 `lastError()`。

新代码通常更容易用 `QDBusPendingCallWatcher` 管理生命周期和错误分支；回调 API 更适合已有的槽式架构。

## 超时和交互式授权

`setTimeout(-1)` 表示使用 D-Bus 默认超时，通常约 25 秒。不要把超时设得无限长来掩盖服务故障；调用方需要明确的取消、重试或降级策略。

Qt 6.7 的 `setInteractiveAuthorizationAllowed(true)` 会让**异步**调用携带 `ALLOW_INTERACTIVE_AUTHORIZATION` 标志，表示调用方愿意等待授权框等交互式授权流程。它只适用于低权限客户端调用高权限服务且部署了相应授权框架的情形，默认关闭。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 生命周期 | `~QDBusAbstractInterface()` | 释放远程接口代理占用的本地资源。 | 父对象销毁会一并销毁代理；未完成调用的结果处理要有自己的生命周期策略。 |
| 异步调用 | `asyncCall(const QString &method, Args &&... args)` | 以可变参数形式发起远程异步调用。 | 参数必须可转换为 `QVariant`；用 `QDBusPendingCallWatcher` 读取回复。 |
| 异步调用 | `asyncCallWithArgumentList(const QString &method, const QList<QVariant> &args)` | 以 `QList<QVariant>` 发起远程异步调用。 | 动态参数场景使用；返回 pending call 不等于远程调用成功。 |
| 同步调用 | `call(const QString &method, Args &&... args)` | 用默认调用模式同步调用远程方法。 | 检查返回 `QDBusMessage` 类型和 `lastError()`；避免在 UI 线程调用慢服务。 |
| 同步调用 | `call(QDBus::CallMode mode, const QString &method, Args &&... args)` | 按指定调用模式调用远程方法。 | 可能重入 Qt 事件循环；共享状态必须能应对重入。 |
| 同步调用 | `callWithArgumentList(QDBus::CallMode mode, const QString &method, const QList<QVariant> &args)` | 用动态参数列表和指定模式调用远程方法。 | 成功返回 ReplyMessage，失败返回 ErrorMessage；调用后检查错误。 |
| 回调调用 | `callWithCallback(..., QObject *receiver, const char *returnMethod, const char *errorMethod)` | 异步调用并分别把成功、错误回复交给两个槽。 | 返回 `true` 只表示成功排队；成功槽参数必须匹配远程返回类型。 |
| 回调调用 | `callWithCallback(..., QObject *receiver, const char *slot)` | 异步调用并把结果或错误交给一个槽。 | 槽签名需能处理 `QDBusError` 或返回消息约定；接收对象销毁后不会再回调。 |
| 远程定位 | `connection()` | 返回关联的 D-Bus 连接。 | 它是连接句柄副本；服务可用性仍由实际调用决定。 |
| 远程定位 | `service()` | 返回目标服务名。 | 可能是总线名或唯一名；不要与 interface 名混淆。 |
| 远程定位 | `path()` | 返回目标对象路径。 | 必须是合法 D-Bus object path，例如 `/org/example/Player`。 |
| 远程定位 | `interface()` | 返回目标接口名。 | 接口名是 ABI 的一部分，应保持稳定。 |
| 状态与错误 | `isValid()` | 判断创建时是否得到有效远程对象引用。 | `true` 不能保证远端之后仍在线；调用时仍须处理错误。 |
| 状态与错误 | `lastError()` | 返回最近一次操作产生的 D-Bus 错误。 | 回调调用的远程错误走错误槽，不能只依赖这里。 |
| 超时 | `setTimeout(int timeout)` | 设置未来 D-Bus 调用的超时毫秒数。 | `-1` 为默认超时，通常约 25 秒；不要用无限等待替代错误处理。 |
| 超时 | `timeout()` | 返回当前超时配置。 | 仅是该接口代理的配置，不会修改总线全局策略。 |
| 交互授权 | `setInteractiveAuthorizationAllowed(bool enable)` | 配置异步调用是否允许等待交互式授权。 | Qt 6.7 引入；只在高权限授权框架真实存在时开启。 |
| 交互授权 | `isInteractiveAuthorizationAllowed()` | 返回异步调用的交互授权允许状态。 | Qt 6.7 引入；默认是 `false`。 |

## 最容易踩的坑

- 把 `callWithCallback()` 的 `true` 当作远程方法成功：它只表示请求已排队。
- 在 UI 线程用同步 `call()` 调慢服务：改用 pending call 或回调。
- 使用会处理事件的调用模式却不考虑重入：等待期间对象状态可能被其他事件改变。
- 只在构造后检查一次 `isValid()`：远程服务可能随后退出或重启。
- 将 `service`、`path`、`interface` 当作可互换字符串：三者分别定位总线服务、对象和接口。
- 无条件允许交互式授权：这会改变异步调用的等待和用户交互行为，应由明确的产品需求决定。
