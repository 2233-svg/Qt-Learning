# Qt QDBusConnection 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusConnection>`  
> 所属模块：`Qt6::DBus`  
> 类型特征：显式共享的 D-Bus 连接句柄，不继承 `QObject`

## 1. 它解决什么问题

`QDBusConnection` 是 Qt 程序进入 D-Bus 的总入口。通过它可以：

- 连接 session bus、system bus、私有 bus 或点对点 peer。
- 构造并发送调用、信号、回复和错误。
- 把远端 D-Bus signal 连接到本地 QObject 槽。
- 注册本地 QObject、virtual object 和服务名。
- 查询连接能力及 bus daemon 的接口。

```text
QDBusConnection
  ├─ 调用远端：send / call / asyncCall / callWithCallback
  ├─ 订阅远端信号：connect / disconnect
  ├─ 导出本地对象：registerObject / registerVirtualObject
  ├─ 申请服务名：registerService
  └─ 查询总线：interface() -> QDBusConnectionInterface
```

它是连接句柄而不是网络 socket 的独占所有者。多个副本共享底层连接；销毁一个 `QDBusConnection` 变量不会关闭连接。

## 2. 最常见的起点

桌面应用通常使用 session bus：

```cpp
#include <QDBusConnection>

QDBusConnection bus = QDBusConnection::sessionBus();
if (!bus.isConnected()) {
    qWarning() << bus.lastError().name() << bus.lastError().message();
    return;
}
```

- **Session bus**：同一桌面会话、通常同一用户的应用之间通信。
- **System bus**：系统级服务使用，权限与安全策略通常更严格。
- **Peer-to-peer**：两个进程直接通信，不经公共 bus daemon，常与 `QDBusServer` 配合。

`sessionBus()`、`systemBus()` 首次使用时打开连接，并在 `QCoreApplication` 析构时关闭。普通业务代码优先用它们，不必自己管理连接名。

## 3. 命名连接、共享与生命周期

需要私有 bus 或 peer 时用带 name 的静态工厂：

```cpp
QDBusConnection peer = QDBusConnection::connectToPeer(
    serverAddress,
    "media-peer");
```

`name` 是 Qt 进程内用于识别底层连接的名字，不是 D-Bus service name。后续使用同一个 name 再调用连接工厂，会得到同一底层连接。

```text
同一个 Qt connection name
        │
        └─> 同一底层 D-Bus 连接
                 ├─ QDBusConnection 副本 A
                 └─ QDBusConnection 副本 B
```

关闭命名连接必须显式调用 `disconnectFromBus(name)` 或 `disconnectFromPeer(name)`。析构和复制赋值都不会自动断开原连接。连接被关闭后，不要指望再次用同一对象“重新连上”；新建连接实例和新的连接生命周期更可靠。

## 4. 连接类型与能力

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 总线类型 | `SessionBus` | 连接当前桌面会话的 bus。 | 适合用户态桌面服务与应用通信。 |
| 总线类型 | `SystemBus` | 连接系统级 bus。 | 受系统策略控制，调用常需额外授权。 |
| 总线类型 | `ActivationBus` | 使用 D-Bus 服务激活环境提供的 bus。 | 主要供被 D-Bus 激活的服务进程使用，普通客户端较少直接选择。 |
| 连接能力 | `UnixFileDescriptorPassing` | 表示当前连接协商支持 Unix fd 传递。 | 发送 `QDBusUnixFileDescriptor` 前同时检查平台支持和此 capability。 |

`connectionCapabilities()` 是协商后的真实连接能力。未连接时返回空 flags；不能仅根据运行平台猜测 fd 能否传递。

## 5. 发送调用：四种选择

### 5.1 只投递，不取回复：`send`

```cpp
bus.send(QDBusMessage::createSignal(
    "/org/example/Player", "org.example.Player", "StateChanged"));
```

`send()` 适合 signal、method reply、error reply，以及明确不需要返回值的方法调用。返回 `true` 只表示消息已成功排入发送队列，不表示远端已经处理成功。

### 5.2 同步获取回复：`call`

```cpp
QDBusMessage reply = bus.call(request, QDBus::Block);
```

`call()` 只用于 method call，返回正常回复或错误回复。默认 `timeout = -1` 会使用实现定义的 IPC 超时，通常约 25 秒。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 调用模式 | `QDBus::NoBlock` | 发起调用但丢弃回复内容。 | 想跟踪回复时改用 `asyncCall()`。 |
| 调用模式 | `QDBus::Block` | 直接阻塞网络等待，不运行事件循环。 | GUI 不会更新，适合工作线程或 CLI。 |
| 调用模式 | `QDBus::BlockWithGui` | 运行 Qt 事件循环等待回复。 | 界面可响应，但会递送其他事件和调用，必须防止重入。 |
| 调用模式 | `QDBus::AutoDetect` | 自动识别被调方法是否有回复。 | 只在确实需要让 Qt 判断无返回调用时使用。 |

### 5.3 异步句柄：`asyncCall`

```cpp
QDBusPendingCall pending = bus.asyncCall(request);
auto *watcher = new QDBusPendingCallWatcher(pending, this);
```

异步调用返回后立即继续执行，结果由 `QDBusPendingReply` 和 `QDBusPendingCallWatcher` 处理。注意：对本应用自己注册的对象发起 method call，受实现限制不会变成真正异步。

### 5.4 回调方式：`callWithCallback`

```cpp
bus.callWithCallback(
    request, this,
    SLOT(onReply(QDBusMessage)),
    SLOT(onError(QDBusError)));
```

它返回 `true` 只说明消息已发送。之后成功时调用 `returnMethod`，失败时调用 `errorMethod`；槽签名必须匹配。没有可用错误槽时，连接的 `QDBusConnectionInterface::callWithCallbackFailed` 可用于接收失败通知。

## 6. 连接远端 D-Bus signal

`QDBusConnection::connect()` 不是 `QObject::connect()` 的同义词：它向 D-Bus 注册 match rule，再把收到的远端 signal 转交本地槽。

```cpp
const bool ok = bus.connect(
    "org.example.Player",
    "/org/example/Player",
    "org.example.Player",
    "StateChanged",
    this,
    SLOT(onStateChanged(QString)));
```

三个 overload 的差别：

1. 不带 signature：最简洁，但参数不匹配只有 signal 真正到达时才发现，槽不会被调用。
2. 带 signature：Qt 检查该 signature 能否投递给本地槽，但不会验证远端是否真的存在此 signal。
3. 带 `argumentMatch` 和 signature：在总线侧按连续字符串参数筛选，适合只订阅某些对象标识或状态值。

`service`、`path` 可为空，表示匹配任意来源的指定 `(interface, name)`。`argumentMatch` 中 null `QString` 表示跳过该位置；若要匹配空字符串，必须传非 null 的 `QString("")`。

断开时调用 `disconnect()`，参数必须与连接时完全一致。不要用“差不多相同”的过滤条件期望它自动匹配。

## 7. 导出本地服务

### 7.1 服务名

```cpp
if (!bus.registerService("org.example.Player")) {
    qWarning() << bus.lastError().message();
    return;
}
```

简化版 `registerService()` 在名称已被占用时失败。需要排队、请求替换或允许被替换时，使用 `bus.interface()->registerService()`。

### 7.2 导出 QObject

```cpp
bus.registerObject(
    "/org/example/Player",
    playerObject,
    QDBusConnection::ExportAdaptors);
```

注册不会接管 `playerObject` 的所有权。对象必须在注册期间保持存活，且同一路径已有对象时注册会失败；先 `unregisterObject()` 才能替换。

`RegisterOptions` 决定暴露多少 QObject API：

- `ExportAdaptors`：导出附着的 `QDBusAbstractAdaptor`，默认值。
- `ExportScriptableSlots`、`Signals`、`Properties`、`Invokables`：导出标为 scriptable 的成员。
- `ExportNonScriptableSlots`、`Signals`、`Properties`、`Invokables`：连非 scriptable 成员也导出。
- `ExportScriptableContents`、`ExportNonScriptableContents`：各自类别的组合。
- `ExportAllSlots`、`Signals`、`Properties`、`Invokables`、`Contents`：对应的全部组合。
- `ExportChildObjects`：把 QObject 子对象作为 D-Bus 子路径自动导出。

默认只导出 adaptor 通常更可控。直接 `ExportAllContents` 可能把本不想作为 IPC 协议公开的对象成员暴露出去。

第二个 `registerObject(path, interface, object, options)` overload 可强制指定 D-Bus interface 名，适用于不依赖默认类名映射的协议。

### 7.3 注销与查询

`unregisterObject(path, UnregisterNode)` 默认只注销该节点；`UnregisterTree` 注销整棵子树。若对象注册时使用 `ExportChildObjects`，即使是 `UnregisterNode` 也会一并注销子对象。

`objectRegisteredAt(path)` 只查询之前以 `registerObject()` 注册的对象，返回的 `QObject *` 不转移所有权。

### 7.4 导出动态路径树

`registerVirtualObject(path, object, option)` 注册 `QDBusVirtualObject`：

- `SingleNode`：只处理一个路径。
- `SubPath`：处理该路径及所有子路径。

virtual object 同样不由 connection 接管所有权；请让它在注册期内存活。

## 8. 查询连接状态与总线接口

- `isConnected()`：连接是否可用。
- `lastError()`：最近的 D-Bus 错误。
- `baseService()`：bus daemon 分配的 unique name，形如 `:1.42`；peer connection 返回空。
- `name()`：Qt 进程内的连接名，不是远端 service name。
- `interface()`：得到本连接对应的 `QDBusConnectionInterface`，用于访问 `org.freedesktop.DBus`。
- `localMachineId()`：当前启动周期内的本机 D-Bus machine id，不保证跨重启持久，不能作为永久设备 ID。

`internalPointer()` 是内部实现入口，不是稳定应用 API；不要在业务代码中使用或保存其返回值。

## 9. 常见误区

### 9.1 误区：`QDBusConnection` 析构就关闭连接

不对。命名连接需要显式 `disconnectFromBus()` 或 `disconnectFromPeer()`。

### 9.2 误区：`BlockWithGui` 没有阻塞风险

它保持事件循环运行，却引入重入风险。等待期间 signal、timer、其他 D-Bus 调用都可能进入当前对象。

### 9.3 误区：注册 QObject 后 Qt 会负责删除它

不对。注册不接管对象所有权；先销毁对象而不注销会留下错误的服务端生命周期设计。

### 9.4 误区：`send()` 返回 true 说明远端调用成功

不对。只代表消息成功排队。要得到成功或错误结果使用 `call()`、`asyncCall()` 或 callback。

### 9.5 误区：连接 signal 成功就验证了远端协议

不对。带 signature overload 只验证本地槽可接收该类型，并不验证远端 signal 是否存在。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDBusConnection(const QString &name)` | 创建指向指定 Qt 连接名的句柄。 | 不会打开连接；先用静态连接工厂建立同名连接。 |
| 复制构造 | `QDBusConnection(const QDBusConnection &other)` | 复制同一底层连接的句柄。 | 副本共享连接，析构不会断开。 |
| 移动构造 | `QDBusConnection(QDBusConnection &&other)` | 移入连接句柄。 | 移动后只析构或重新赋值源对象。 |
| 析构 | `~QDBusConnection()` | 释放当前句柄。 | 不关闭底层连接。 |
| 复制赋值 | `operator=(const QDBusConnection &other)` | 改为引用 `other` 的连接。 | 原连接不会自动断开。 |
| 移动赋值 | `operator=(QDBusConnection &&other)` | 移入另一个连接句柄。 | 被替换连接不会因此自动关闭。 |
| 交换 | `swap(QDBusConnection &other)` | 快速交换两个句柄。 | 仅本地对象交换。 |
| 连接状态 | `bool isConnected() const` | 判断底层连接是否可用。 | 失败后读取 `lastError()`，不要继续发送。 |
| 唯一名 | `QString baseService() const` | 获取 bus 分配的 unique connection name。 | peer connection 返回空；不是 well-known service name。 |
| 错误查询 | `QDBusError lastError() const` | 获取最近连接或操作错误。 | 用 type 或 name 做程序判断。 |
| 连接名 | `QString name() const` | 获取 Qt 内部连接名。 | 用于断开命名连接，不是 D-Bus 服务名。 |
| 能力查询 | `ConnectionCapabilities connectionCapabilities() const` | 获取协商后的连接能力。 | 传 Unix fd 前检查 `UnixFileDescriptorPassing`。 |
| 异步调用 | `asyncCall(message, timeout)` | 发送 method call 并返回 pending 句柄。 | 只适合 method call；用 watcher 或 pending reply 处理结果。 |
| 同步调用 | `call(message, mode, timeout)` | 发送 method call 并取得回复。 | 会等待；BlockWithGui 会重入事件循环。 |
| 回调调用 | `callWithCallback(message, receiver, return, error, timeout)` | 完成时调用成功或错误槽。 | `true` 只表示已发送；槽参数必须匹配。 |
| 回调调用 | `callWithCallback(message, receiver, slot, timeout)` | 用单一回调槽处理异步结果。 | 无单独 error 槽时关注 `callWithCallbackFailed`。 |
| 单向发送 | `send(const QDBusMessage &message)` | 将消息排入发送队列且不等待。 | 适合 signal、reply、error 或无需返回值调用。 |
| 信号订阅 | `connect(service, path, interface, name, receiver, slot)` | 订阅远端 D-Bus signal。 | 槽类型仅在 signal 到达时才会被验证。 |
| 信号订阅 | `connect(..., signature, receiver, slot)` | 订阅并校验本地槽可接收指定签名。 | 不验证远端是否实际提供此 signal。 |
| 信号订阅 | `connect(..., argumentMatch, signature, receiver, slot)` | 订阅并按字符串参数过滤 signal。 | null 匹配项跳过位置，空字符串匹配要用非 null QString。 |
| 取消订阅 | `disconnect(...)` 三个 overload | 移除之前的远端 signal 订阅。 | 参数必须与对应 `connect()` 完全一致。 |
| 连接已知总线 | `connectToBus(BusType, name)` | 连接 session、system 或 activation bus。 | 同名调用共享底层连接。 |
| 连接私有 bus | `connectToBus(address, name)` | 连接指定私有 bus daemon 地址。 | 与 peer-to-peer 不同，仍是 bus server 模型。 |
| 连接 peer | `connectToPeer(address, name)` | 建立点对点 D-Bus 连接。 | 常配合 QDBusServer；没有 bus service name 路由。 |
| 断开 bus | `disconnectFromBus(name)` | 显式关闭命名 bus 连接。 | 关闭后新建连接实例再重连。 |
| 断开 peer | `disconnectFromPeer(name)` | 显式关闭命名点对点连接。 | 确保没有对象仍依赖这条连接。 |
| 本机标识 | `localMachineId()` | 取得本次启动期间的机器标识。 | 不保证跨重启稳定，不可存为永久设备 ID。 |
| 常用总线 | `sessionBus()` | 获取共享 session bus 连接。 | 生命周期直到应用退出。 |
| 常用总线 | `systemBus()` | 获取共享 system bus 连接。 | 权限策略通常比 session bus 严格。 |
| 导出对象 | `registerObject(path, object, options)` | 将 QObject 导出到 D-Bus 路径。 | 不接管所有权；路径冲突时返回 false。 |
| 导出对象 | `registerObject(path, interface, object, options)` | 以明确 interface 名导出 QObject。 | interface 名是稳定协议的一部分。 |
| 注销对象 | `unregisterObject(path, mode)` | 移除已导出的对象或子树。 | ExportChildObjects 时 Node 也会移除子对象。 |
| 查找对象 | `objectRegisteredAt(path)` | 查询已注册 QObject。 | 返回借用指针，不能删除。 |
| 导出虚拟对象 | `registerVirtualObject(path, object, option)` | 将一个对象处理固定路径或动态子树。 | object 不由 connection 所有；SubPath 要自行路由所有子路径。 |
| 注册服务名 | `registerService(serviceName)` | 尝试取得 bus service name。 | 名称被占用即失败；高级排队与替换用 `interface()`。 |
| 注销服务名 | `unregisterService(serviceName)` | 释放此前取得的服务名。 | 仅对本连接已注册的名称有意义。 |
| 总线代理 | `QDBusConnectionInterface *interface() const` | 取得 bus daemon 的特殊接口代理。 | 用于服务名、owner、激活等操作；peer 场景不适用。 |
| 内部指针 | `void *internalPointer() const` | 暴露 Qt 私有实现指针。 | 非稳定内部 API，业务代码不要使用。 |

---

### 一句话总结

`QDBusConnection` 是 QtDBus 的通道与导出中心；连接生命周期要按名称显式管理，同步调用要警惕阻塞和重入，导出对象时则要明确控制暴露范围与对象所有权。
