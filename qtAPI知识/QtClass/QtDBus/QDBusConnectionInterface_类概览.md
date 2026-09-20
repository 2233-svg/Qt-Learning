# Qt QDBusConnectionInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusConnectionInterface>`  
> 所属模块：`Qt6::DBus`  
> 继承：`QObject` → `QDBusAbstractInterface`  
> 对应远端接口：`org.freedesktop.DBus`

## 1. 它解决什么问题

D-Bus bus daemon 自己也是一个服务。它提供特殊接口 `org.freedesktop.DBus`，用于管理服务名、查询 owner、获取进程身份信息以及请求激活服务。

`QDBusConnectionInterface` 是这个特殊接口的 Qt 代理。它解决的不是“调用某个业务服务”，而是“向 bus daemon 询问和管理 bus 本身”。

```text
QDBusConnection
      │ interface()
      ▼
QDBusConnectionInterface
      │
      ├─ 注册或释放服务名
      ├─ 查询服务 owner、PID、UID、凭据
      ├─ 枚举已注册或可激活服务
      └─ 请求 daemon 激活一个服务
```

它的构造函数不是公开 API。正确取得方式是：

```cpp
QDBusConnection bus = QDBusConnection::sessionBus();
QDBusConnectionInterface *daemon = bus.interface();
```

`daemon` 由连接管理，不要手动 `delete`。

## 2. 注册一个服务名

最简单的方式：

```cpp
QDBusConnection bus = QDBusConnection::sessionBus();
QDBusConnectionInterface *daemon = bus.interface();

QDBusReply<QDBusConnectionInterface::RegisterServiceReply> reply =
    daemon->registerService("org.example.Player");

if (reply.isError()) {
    qWarning() << reply.error().name() << reply.error().message();
    return;
}

if (reply.value() == QDBusConnectionInterface::ServiceRegistered)
    qInfo() << "service name acquired";
```

注意 `registerService()` 的成功不只一种状态。服务名可能立即取得，也可能进入等待队列；业务是否能开始接收调用，应根据 `RegisterServiceReply` 和 `serviceRegistered()` 信号决定。

## 3. 服务名的排队与替换策略

### 3.1 返回状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 返回值 | `ServiceNotRegistered` | 请求没有取得也没有排队服务名。 | 检查 `QDBusReply` 错误，再决定重试或提示。 |
| 返回值 | `ServiceRegistered` | 当前连接已经取得服务名。 | 可开始对外提供该服务名对应的对象。 |
| 返回值 | `ServiceQueued` | 请求进入服务名等待队列。 | 尚未拥有名称，等 `serviceRegistered()` 再启用服务。 |

### 3.2 名称已被占用时

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 排队策略 | `DontQueueService` | 名称被占用时立刻失败。 | 默认值；适合名称必须唯一的单实例服务。 |
| 排队策略 | `QueueService` | 名称被占用时进入等待队列。 | 进入队列不等于拥有服务名。 |
| 排队策略 | `ReplaceExistingService` | 请求替换当前 owner。 | 只有旧 owner 允许被替换时才可能成功。 |
| 可替换策略 | `DontAllowReplacement` | 不允许其他进程替换本连接取得的名称。 | 默认值；通常适合稳定服务。 |
| 可替换策略 | `AllowReplacement` | 允许将来由其他进程替换该名称。 | 被替换后会收到 `serviceUnregistered()`，要停止对外服务。 |

排队和替换改变的是 bus service name 的 owner，不会替你迁移本地对象状态或清理资源。服务切换逻辑仍要由应用实现。

## 4. 查询服务状态和身份

### 4.1 可用性与 owner

```cpp
QDBusReply<bool> exists = daemon->isServiceRegistered(
    "org.example.Player");

QDBusReply<QString> owner = daemon->serviceOwner(
    "org.example.Player");
```

`isServiceRegistered()` 只给出“当前是否注册”。`serviceOwner()` 返回实际持有者的 unique connection name，例如 `:1.42`；没有 owner 时它返回 `NameHasNoOwner` 错误。

若你需要处理服务重启或 owner 直接切换，使用 `QDBusServiceWatcher`，而不是不断轮询这两个函数。

### 4.2 PID、UID 和凭据

- `servicePid()` 返回当前 owner 的 Unix PID。
- `serviceUid()` 返回当前 owner 的 Unix UID。
- `serviceCredentials()` 返回 D-Bus `GetConnectionCredentials` 的 `QVariantMap`，Qt 6.10 起提供。

这些信息用于审计、诊断或在受控环境中做身份检查。它们不是通用授权框架：不同 bus 策略、平台和权限可能限制可得信息，业务安全仍应由服务端自身验证调用者。

## 5. 枚举与激活服务

`registeredServiceNames()` 返回当前 bus 上已注册的名字；`activatableServiceNames()` 返回可由 daemon 激活的服务名。两者都返回 `QDBusReply<QStringList>`，并非内存中的无错误属性快照，读取后也要检查 `isValid()`。

```cpp
QDBusReply<QStringList> names = daemon->activatableServiceNames();
if (names.isValid())
    qDebug() << names.value();
```

`startService(name)` 请求 daemon 激活指定服务。它只表示激活请求本身是否成功；服务是否已经完成初始化、对象是否可调用，仍可能需要进一步调用或监听 owner 变化。

## 6. 信号与异步失败

### 6.1 自己的服务名状态

`serviceRegistered(service)` 在当前应用取得名称时发出；`serviceUnregistered(service)` 在当前应用失去名称时发出。尤其当注册时允许 replacement，后者是重要的资源清理和停止服务信号。

`serviceOwnerChanged(name, oldOwner, newOwner)` 用于观察服务名 owner 变化。注册时 `oldOwner` 为空，注销时 `newOwner` 为空，直接换 owner 时两者都非空。

若只观察少量外部服务，`QDBusServiceWatcher` 会比连接这个全局接口的 owner 信号更高效。

### 6.2 `callWithCallbackFailed`

当 `QDBusConnection::callWithCallback()` 发生错误时，此信号携带 `QDBusError` 和无法投递的原调用消息。它是 callback 异步模式的失败通道之一；在复杂回调调用较多时，连接它便于统一记录错误。

## 7. 继承自 `QDBusAbstractInterface` 的能力

本类继承的 `call()`、`asyncCall()`、`callWithCallback()`、`connection()`、`isValid()`、`lastError()`、`timeout()`、`setTimeout()`、`service()`、`path()`、`interface()` 和交互授权设置，语义见 `QDBusAbstractInterface` 笔记。

实际使用本类时，最常见的继承 API 是：

- `isValid()`：确认 daemon 代理可用。
- `lastError()`：查询代理初始化或最近调用错误。
- `setTimeout()`：调整 bus daemon 调用超时。
- `asyncCall()`：少数未由此类直接封装的 daemon 方法可按字符串动态调用。

## 8. 常见误区

### 8.1 误区：可以直接 new 一个 `QDBusConnectionInterface`

不能。它由 `QDBusConnection::interface()` 创建和管理。

### 8.2 误区：`ServiceQueued` 表示可以开始导出服务

不对。它只是排队；等拿到名称并收到 `serviceRegistered()` 后才是 owner。

### 8.3 误区：`servicePid()`、`serviceUid()` 足以完成权限控制

不对。它们是查询信息，受 bus 策略和平台影响；真正敏感的操作必须在服务端做授权。

### 8.4 误区：`registeredServiceNames` 是自动实时刷新的属性

不是。调用会发起 daemon 查询并得到 `QDBusReply`，每次都需处理失败。

## 9. 逐项 API 说明

### 列表与状态查询

#### `registeredServiceNames()` 与 `activatableServiceNames()`

分别读取当前已注册服务名和可激活服务名。返回 `QDBusReply<QStringList>`，需要检查错误。

#### `isServiceRegistered(const QString &serviceName)`

查询服务名是否当前已注册。适合一次性查询，不适合持续监听变化。

#### `serviceOwner(const QString &name)`

取得某个名称的 primary owner unique name。无 owner 时返回 `NameHasNoOwner` 错误。

#### `servicePid()`、`serviceUid()`、`serviceCredentials()`

查询当前 owner 的 PID、UID、连接凭据。`serviceCredentials()` 从 Qt 6.10 起可用。

### 服务名控制

#### `registerService(serviceName, queueOption, replacementOption)`

请求取得、排队或替换服务名。结果值和后续服务状态信号都必须处理。

#### `unregisterService(serviceName)`

释放之前请求的服务名；若只是排队则放弃队列位置，若当前是 owner 则释放所有权。

#### `startService(name)`

请求 daemon 激活一个可激活服务。成功不等于业务接口立即可用。

### 信号

#### `serviceRegistered()` 与 `serviceUnregistered()`

通知当前应用取得或失去服务名。服务允许被替换时，必须处理失去名称后的停止服务流程。

#### `serviceOwnerChanged()`

通知某名称 owner 变化。观察大量或少量外部服务时，要考虑用 `QDBusServiceWatcher` 进行更精确过滤。

#### `callWithCallbackFailed()`

通知 callback 型异步调用失败，参数包含错误和原始请求。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `RegisterServiceReply` | 描述注册请求失败、已取得或已排队。 | `ServiceQueued` 不拥有名称，需等待 `serviceRegistered()`。 |
| 枚举 | `ServiceQueueOptions` | 指定名称已被占用时的处理方式。 | ReplaceExistingService 受当前 owner 的 replacement 策略限制。 |
| 枚举 | `ServiceReplacementOptions` | 指定本连接取得的名称能否被替换。 | AllowReplacement 时必须处理失去名称事件。 |
| 只读属性 | `registeredServiceNames` | 读取当前 bus 的已注册名称。 | 返回 QDBusReply，每次读取都检查错误。 |
| 只读属性 | `activatableServiceNames` | 读取可由 bus daemon 激活的名称。 | “可激活”不代表服务已运行。 |
| 服务查询 | `isServiceRegistered(serviceName)` | 判断服务名当前是否存在。 | 持续状态改用 watcher 或 owner 信号。 |
| owner 查询 | `serviceOwner(name)` | 获取服务名当前 unique owner。 | 无 owner 时得到 NameHasNoOwner 错误。 |
| PID 查询 | `servicePid(serviceName)` | 获取 owner 的 Unix PID。 | 仅作诊断或受控身份信息，不能替代授权。 |
| UID 查询 | `serviceUid(serviceName)` | 获取 owner 的 Unix UID。 | 平台与策略可能影响可用性。 |
| 凭据查询 | `serviceCredentials(serviceName)` | 获取 owner 连接凭据 map。 | Qt 6.10 起；内容取决于 D-Bus 策略。 |
| 服务注册 | `registerService(serviceName, queue, replacement)` | 请求获得、排队或替换服务名。 | 处理 QDBusReply 及后续注册、失去名称信号。 |
| 服务注销 | `unregisterService(serviceName)` | 释放服务名或队列位置。 | 不会自动注销已导出的对象。 |
| 服务激活 | `startService(name)` | 请求 daemon 激活服务。 | 成功后仍需确认 service owner 或接口可用。 |
| 信号 | `serviceRegistered(service)` | 当前应用获得名称时通知。 | Queued 状态下可能稍后才发出。 |
| 信号 | `serviceUnregistered(service)` | 当前应用失去名称时通知。 | 允许替换时应停止对外服务并清理状态。 |
| 信号 | `serviceOwnerChanged(name, oldOwner, newOwner)` | 通知服务 owner 变更。 | 两端空字符串分别表示注册与注销。 |
| 信号 | `callWithCallbackFailed(error, call)` | 通知 callback 型异步调用失败。 | 记录 error 与 call，避免静默丢失异步失败。 |
| 继承调用 | `call()`、`asyncCall()`、`callWithCallback()` | 动态调用 daemon 的其他方法。 | 继承语义见 QDBusAbstractInterface；注意同步阻塞和回调生命周期。 |
| 继承状态 | `isValid()`、`lastError()`、`timeout()` | 查询代理是否可用、错误及超时。 | 所有 daemon 查询前后都应处理错误。 |

---

### 一句话总结

`QDBusConnectionInterface` 是 bus daemon 的管理代理；通过它管理服务名和查询 owner，但排队、替换、激活与权限都需要按事件和错误结果完整处理。
