# QDBusServiceWatcher
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusServiceWatcher`

## 作用定位

`QDBusServiceWatcher` 用来监听 D-Bus 服务名的注册、注销和 owner 变化。它把 bus daemon 的 `NameOwnerChanged` 等信号包装成更直接的 Qt 信号，适合跟踪某个服务是否上线、下线或被另一个进程接管。

## 类说明

- 头文件：`#include <QDBusServiceWatcher>`
- CMake：链接 `Qt6::DBus`
- 继承：`QObject`
- 属性：`watchMode`、`watchedServices`，支持 `QBindable`

## API 速查

| API | 说明 |
| --- | --- |
| `QDBusServiceWatcher(parent)` | 创建空 watcher，之后设置连接、服务和模式。 |
| `QDBusServiceWatcher(service, connection, mode, parent)` | 一步创建并监听指定服务。 |
| `setConnection()` / `connection()` | 设置或读取监听所在 bus。 |
| `addWatchedService()` | 增加一个服务名。 |
| `removeWatchedService()` | 移除一个服务名，返回是否移除成功。 |
| `setWatchedServices()` / `watchedServices()` | 批量设置或读取监听列表。 |
| `setWatchMode()` / `watchMode()` | 设置或读取监听模式。 |
| `bindableWatchedServices()` | 用于 Qt property binding 的服务列表绑定接口。 |
| `bindableWatchMode()` | 用于 Qt property binding 的模式绑定接口。 |
| `serviceRegistered(serviceName)` | 服务名出现 owner 时发出。 |
| `serviceUnregistered(serviceName)` | 服务名失去 owner 时发出。 |
| `serviceOwnerChanged(serviceName, oldOwner, newOwner)` | owner 变化时发出，包含旧 owner 和新 owner。 |

## 监听模式

| `WatchModeFlag` | 说明 |
| --- | --- |
| `WatchForRegistration` | 只关心服务上线。 |
| `WatchForUnregistration` | 只关心服务下线。 |
| `WatchForOwnerChange` | 同时关心注册、注销和 owner 改变；值等价于前两者组合。 |

## 典型用法

```cpp
auto *watcher = new QDBusServiceWatcher(
    "org.example.Service",
    QDBusConnection::sessionBus(),
    QDBusServiceWatcher::WatchForOwnerChange,
    this);

connect(watcher, &QDBusServiceWatcher::serviceRegistered,
        this, &Client::reconnect);
connect(watcher, &QDBusServiceWatcher::serviceUnregistered,
        this, &Client::markOffline);
```

## 使用场景

- 服务上线后自动重连或重新创建代理。
- 服务退出后清理缓存状态，避免继续调用失效对象。
- 监控服务 owner 被替换的情况。
- UI 显示“某后台服务是否可用”。

## 常见坑与经验

- service name 应是知名服务名或唯一连接名；监听错名字不会报错，只是收不到想要的事件。
- `serviceRegistered` 不代表服务业务初始化完成，只代表 bus 上已有 owner。
- 监听多个服务时，槽里要根据 `serviceName` 分流。
- owner 改变时旧代理可能仍指向旧进程暴露的对象语义，建议重新查询状态。
- `WatchForOwnerChange` 会比只监听上线/下线更吵，但调试接管问题很有价值。

## 知识点覆盖

- D-Bus 服务名 owner 变化
- `NameOwnerChanged` 的 Qt 封装
- 服务生命周期感知
- Qt bindable 属性
- 自动重连策略
