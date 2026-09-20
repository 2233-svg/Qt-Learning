# QDBusConnectionInterface
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusConnectionInterface`

## 作用定位

`QDBusConnectionInterface` 是 bus daemon 本身的代理接口。通过 `QDBusConnection::interface()` 取得后，可以查询当前 bus 上有哪些服务、谁拥有某个服务名、服务进程的 PID/UID、可激活服务列表，也可以申请、释放或启动服务名。

它不是业务服务接口，而是 D-Bus 总线管理接口。

## 类说明

- 头文件：`#include <QDBusConnectionInterface>`
- CMake：链接 `Qt6::DBus`
- 继承：`QDBusAbstractInterface`
- 获取方式：`QDBusConnection::sessionBus().interface()`

## API 速查

| API | 说明 |
| --- | --- |
| `registeredServiceNames()` | 列出当前已注册服务名。 |
| `activatableServiceNames()` | 列出可由 bus 激活的服务名。 |
| `isServiceRegistered(serviceName)` | 判断某个服务名当前是否有 owner。 |
| `registerService(serviceName, qoption, roption)` | 申请知名服务名，可选择排队或替换。 |
| `unregisterService(serviceName)` | 释放已拥有或排队的服务名。 |
| `serviceOwner(name)` | 查询服务名当前 owner 的唯一连接名。 |
| `servicePid(serviceName)` | 查询服务进程 PID。 |
| `serviceUid(serviceName)` | 查询服务进程 UID。 |
| `serviceCredentials(serviceName)` | Qt 6.10 起查询连接凭据，返回 `QVariantMap`。 |
| `startService(name)` | 请求 bus 激活某服务。 |
| `serviceRegistered(service)` | 当前应用获得某服务名时发出。 |
| `serviceUnregistered(service)` | 当前应用失去某服务名时发出。 |
| `callWithCallbackFailed(error, call)` | `QDBusConnection::callWithCallback()` 投递失败时通知。 |

## 服务名注册选项

| 类型 | 值 | 说明 |
| --- | --- | --- |
| `RegisterServiceReply` | `ServiceNotRegistered` | 申请失败。 |
| `RegisterServiceReply` | `ServiceRegistered` | 当前连接已经成为该服务名 owner。 |
| `RegisterServiceReply` | `ServiceQueued` | 服务名已有 owner，本连接进入等待队列。 |
| `ServiceQueueOptions` | `DontQueueService` | 已被占用就失败，默认最明确。 |
| `ServiceQueueOptions` | `QueueService` | 被占用时排队等待。 |
| `ServiceQueueOptions` | `ReplaceExistingService` | 尝试替换现有 owner。 |
| `ServiceReplacementOptions` | `DontAllowReplacement` | 不允许别人替换自己。 |
| `ServiceReplacementOptions` | `AllowReplacement` | 允许别人用替换选项抢占。 |

## 使用场景

- 单实例应用申请 `org.example.App` 这类知名服务名。
- 启动前检查依赖服务是否已运行或可激活。
- 调试工具列出 bus 上所有服务。
- 安全审计中查询服务 owner、PID、UID、凭据。
- 实现服务名排队接管策略。

## 常见坑与经验

- `registerService()` 返回 `QDBusReply<RegisterServiceReply>`，要先检查 reply 是否有效，再看枚举值。
- `ServiceQueued` 不是已经可用；真正获得服务名时会收到 `serviceRegistered()`。
- `ReplaceExistingService` 只有对方允许被替换时才可能成功。
- PID/UID/credentials 查询在权限或平台上可能失败，不能假设总能得到。
- `startService()` 只是请求激活，不代表目标服务已经完成初始化。

## 知识点覆盖

- D-Bus bus daemon 管理接口
- 知名服务名 owner 与队列
- 服务激活机制
- 服务凭据、PID、UID 查询
- 服务注册和释放信号
