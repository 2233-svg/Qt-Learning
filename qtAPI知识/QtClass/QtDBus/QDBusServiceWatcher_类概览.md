# Qt QDBusServiceWatcher 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusServiceWatcher>`  
> 所属模块：`Qt6::DBus`  
> 继承：`QObject`

## 1. 它解决什么问题

D-Bus 服务名不是固定绑定某个进程的。服务可能刚启动、退出、崩溃后被 systemd 拉起，或直接由新进程接管同一个服务名。若客户端只在启动时查询一次服务状态，后续通信很容易对着已经消失的 owner 发请求。

`QDBusServiceWatcher` 专门观察一个或多个服务名在某条 D-Bus 连接上的归属变化，并把变化转成 Qt 信号。它比直接连接 `QDBusConnectionInterface::serviceOwnerChanged()` 更高效，因为它只订阅当前关心的服务。

```text
服务名 org.example.Backend
      │
      ├─ 无 owner -> 有 owner：注册
      ├─ 有 owner -> 无 owner：注销
      └─ owner A -> owner B：归属切换
                │
                ▼
      QDBusServiceWatcher 发出相应信号
```

它解决的是“服务是否仍然可用、是否已经换了进程”的感知问题，不负责重连业务接口，也不替你重试失败请求。

## 2. 构建与最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
```

```cpp
#include <QDBusConnection>
#include <QDBusServiceWatcher>

auto *watcher = new QDBusServiceWatcher(
    "org.example.Backend",
    QDBusConnection::sessionBus(),
    QDBusServiceWatcher::WatchForOwnerChange,
    this);

connect(watcher, &QDBusServiceWatcher::serviceOwnerChanged, this,
        [this](const QString &service, const QString &oldOwner,
               const QString &newOwner) {
            if (newOwner.isEmpty()) {
                markBackendUnavailable(service);
            } else {
                recreateBackendProxy(service, newOwner);
            }
        });
```

`oldOwner` 和 `newOwner` 是 D-Bus 唯一连接名，而不是众所周知的服务名。服务注册时 `oldOwner` 为空，服务注销时 `newOwner` 为空。

## 3. 三种监听模式

`WatchMode` 是 `QFlags<WatchModeFlag>`，可以组合标志。枚举值的行为应按“你究竟关心哪种业务事件”选择：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举值 | `WatchForRegistration` | 监听服务变为可用。 | 对应 `serviceRegistered()`；不会报告 owner 之间的直接切换。 |
| 枚举值 | `WatchForUnregistration` | 监听服务不再可用。 | 对应 `serviceUnregistered()`；不会报告 owner 之间的直接切换。 |
| 枚举值 | `WatchForOwnerChange` | 监听服务名的全部归属变化。 | 包含注册、注销和 owner A 到 owner B 的切换；需要处理 `oldOwner`、`newOwner` 的空值。 |

如果你只需要知道服务可用或不可用，使用前两个更具体的模式。只有需要因服务重启而重新建立代理、重新订阅信号时，才选 `WatchForOwnerChange`。

## 4. 观察多个服务与通配符

一个 watcher 可以观察多个服务：

```cpp
watcher->addWatchedService("org.example.Player");
watcher->addWatchedService("org.example.Library");
```

服务名末尾的 `*` 是命名空间前缀匹配。例如 `com.example.backend1*` 可匹配 `com.example.backend1` 及其子命名空间中的服务，但不会把同一层级的 `com.example.backend12` 误认为匹配项。

当服务列表经常变动时，优先使用 `addWatchedService()` 和 `removeWatchedService()`。`setWatchedServices()` 会先移除旧规则再添加新规则，开销更大。

## 5. 连接、事件循环与延迟通知

默认构造的 watcher **没有连接**，在调用 `setConnection()` 前不会发出任何服务变化信号。

```cpp
auto *watcher = new QDBusServiceWatcher(this);
watcher->setConnection(QDBusConnection::sessionBus());
watcher->setWatchMode(QDBusServiceWatcher::WatchForRegistration);
watcher->addWatchedService("org.example.Backend");
```

`setConnection()` 会把当前所有观察规则迁移到新连接。watcher 会持有 `QDBusConnection` 的引用，保证自己存活期间连接不会因引用计数归零而关闭。

服务通知是异步的。即使 `removeWatchedService()` 返回 `true`，已经在队列中等待处理的该服务通知仍可能在之后发出。槽函数应把信号当作事件流，而不是把“已移除”理解为绝对屏障。

## 6. 属性与绑定

### 6.1 `watchedServices`

保存当前观察的服务列表。该属性支持 `QProperty` 绑定，但手动调用 `addWatchedService()`、`removeWatchedService()` 或 `setWatchedServices()` 会解除已有绑定。

### 6.2 `watchMode`

保存当前监听模式，默认是 `WatchForOwnerChange`。该属性也支持绑定；一旦调用 `setWatchMode()`，原有绑定会被移除。

Qt 属性绑定适合由其它 `QProperty` 驱动配置；普通 C++ 项目大多只需显式 setter。

## 7. 常见误区

### 7.1 误区：注册和注销信号能报告所有 owner 变化

不能。服务可能从 owner A 直接转给 owner B，不经历注销再注册。此时应使用 `WatchForOwnerChange` 和 `serviceOwnerChanged()`。

### 7.2 误区：构造 watcher 就自动使用 session bus

默认构造不会附着连接，因此也不会产生通知。使用带 `service`、`connection` 的构造函数，或随后调用 `setConnection()`。

### 7.3 误区：移除服务后不可能再收到相关信号

不保证。消息已进入事件队列时仍会投递；槽函数应能容忍晚到事件。

### 7.4 误区：收到服务可用信号就可以永久复用旧代理

服务重启后 unique owner 会变化，旧的状态、已连接信号和缓存可能已失效。需要按业务重新获取接口或重新初始化。

## 8. 逐项 API 说明

### 构造与属性访问

#### `QDBusServiceWatcher(QObject *parent = nullptr)`

创建未配置 watcher，并设置 `parent`。必须后续调用 `setConnection()`；在此之前不会发任何服务信号。

#### `QDBusServiceWatcher(const QString &service, const QDBusConnection &connection, WatchMode mode, QObject *parent = nullptr)`

立即附着到 `connection`，并开始按 `mode` 观察 `service`。这是只有一个初始服务时最直接的构造方式。

#### `WatchMode watchMode() const` 与 `void setWatchMode(WatchMode mode)`

读取或修改观察模式。设置新模式会改变后续订阅规则，也会解除现有的属性绑定。

#### `QBindable<WatchMode> bindableWatchMode()`

取得 `watchMode` 的 QProperty 绑定接口。只在项目已采用 Qt property binding 时使用。

#### `QStringList watchedServices() const` 与 `void setWatchedServices(const QStringList &services)`

读取或整体替换观察服务列表。整体替换较昂贵，会移除再重建所有监听规则，并解除原属性绑定。

#### `QBindable<QStringList> bindableWatchedServices()`

取得 `watchedServices` 的绑定接口。手动更改服务列表会解除既有绑定。

### 服务和连接管理

#### `void addWatchedService(const QString &newService)`

增量添加观察目标，比整体设置服务列表更高效。会解除 `watchedServices` 的绑定。

#### `bool removeWatchedService(const QString &service)`

删除匹配服务，至少删除一项时返回 `true`。已排队的旧通知仍可能到达。

#### `QDBusConnection connection() const`

返回 watcher 当前附着的连接。可用于确认 watcher 究竟在 session bus、system bus 或自建点对点连接上工作。

#### `void setConnection(const QDBusConnection &connection)`

切换 watcher 使用的连接，并把所有现有观察规则转移过去。watcher 会保留该连接引用。

### 变化信号

#### `serviceRegistered(const QString &serviceName)`

目标服务变得可用时发出。只在包含 `WatchForRegistration` 的模式下监听。

#### `serviceUnregistered(const QString &serviceName)`

目标服务不再可用时发出。只在包含 `WatchForUnregistration` 的模式下监听。

#### `serviceOwnerChanged(const QString &serviceName, const QString &oldOwner, const QString &newOwner)`

服务归属变化时发出。注册时 `oldOwner` 为空，注销时 `newOwner` 为空，直接 owner 切换时两者都非空。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `WatchModeFlag` 与 `WatchMode` | 定义并组合服务变化监听模式。 | 按业务选具体模式；OwnerChange 才能捕获直接 owner 切换。 |
| 构造 | `QDBusServiceWatcher(QObject *parent)` | 创建未连接的 watcher。 | 之后必须调用 `setConnection()`，否则不会发信号。 |
| 构造 | `QDBusServiceWatcher(service, connection, mode, parent)` | 创建后立即开始观察一个服务。 | 传入正确的 session bus、system bus 或点对点连接。 |
| 析构 | `~QDBusServiceWatcher()` | 释放监听规则与连接引用。 | 已建立的 signal-slot 连接随 QObject 生命周期自动断开。 |
| 属性读取 | `WatchMode watchMode() const` | 获取当前监听模式。 | 默认是 `WatchForOwnerChange`。 |
| 属性设置 | `void setWatchMode(WatchMode mode)` | 修改监听模式。 | 会影响后续事件种类，并解除既有属性绑定。 |
| 属性绑定 | `QBindable<WatchMode> bindableWatchMode()` | 提供 `watchMode` 的 QProperty 绑定入口。 | 手动 setter 会移除绑定。 |
| 服务读取 | `QStringList watchedServices() const` | 获取当前观察服务列表。 | 通配服务名的 `*` 只能放在末尾。 |
| 服务整体设置 | `void setWatchedServices(const QStringList &services)` | 替换所有观察服务。 | 较昂贵且解除绑定；频繁变化时用增量 API。 |
| 服务绑定 | `QBindable<QStringList> bindableWatchedServices()` | 提供服务列表的 QProperty 绑定入口。 | `add`、`remove`、`set` 都会解除已有绑定。 |
| 服务添加 | `void addWatchedService(const QString &service)` | 增量添加一个服务或前缀规则。 | 比整体替换高效。 |
| 服务移除 | `bool removeWatchedService(const QString &service)` | 移除匹配服务规则。 | 返回后仍可能收到已排队的旧通知。 |
| 连接读取 | `QDBusConnection connection() const` | 获取 watcher 使用的总线连接。 | 确认监听的总线与业务服务所在总线一致。 |
| 连接设置 | `void setConnection(const QDBusConnection &connection)` | 将观察规则转移到指定连接。 | 未设置连接时 watcher 不会产生通知。 |
| 信号 | `serviceRegistered(const QString &service)` | 通知服务变得可用。 | 需要 `WatchForRegistration`。 |
| 信号 | `serviceUnregistered(const QString &service)` | 通知服务不可用。 | 需要 `WatchForUnregistration`。 |
| 信号 | `serviceOwnerChanged(service, oldOwner, newOwner)` | 通知服务名归属变化。 | Owner 是 unique name；处理两端为空字符串的注册、注销情形。 |

---

### 一句话总结

`QDBusServiceWatcher` 让客户端追踪服务名的可用性和 owner 切换；用增量管理观察列表，处理异步残余通知，并在 owner 改变后按业务重新建立接口状态。
