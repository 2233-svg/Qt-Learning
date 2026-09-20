# Qt QDBusInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusInterface>`  
> 所属模块：`Qt6::DBus`  
> 继承：`QObject` → `QDBusAbstractInterface`  
> 定位：动态远端接口代理

## 1. 它解决什么问题

有些 D-Bus 接口在编译时就已知，可以用 `qdbusxml2cpp` 生成强类型代理类；但调试工具、插件系统、可选服务或动态协议客户端往往不能预先生成代码。

`QDBusInterface` 是“任意远端对象接口”的动态代理。给定 service、path、interface 和连接后，它可以：

- 按方法名调用远端方法。
- 用普通 `QObject::connect()` 接收远端导出的 signal。
- 通过 `QObject::property()`、`setProperty()` 访问远端属性。

```text
service + path + interface + connection
                    │
                    ▼
              QDBusInterface
                    │
        动态调用方法、信号和属性
```

它适合运行时发现或调用接口；当协议稳定、调用量大、希望有编译期签名检查时，生成的代理类通常更安全、也更易重构。

## 2. 构造一个动态代理

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
```

```cpp
#include <QDBusConnection>
#include <QDBusInterface>
#include <QDBusReply>

QDBusInterface player(
    "org.example.Player",
    "/org/example/Player",
    "org.example.Player",
    QDBusConnection::sessionBus(),
    this);

if (!player.isValid()) {
    qWarning() << player.lastError().name()
               << player.lastError().message();
    return;
}

QDBusReply<QString> reply = player.call("DisplayName");
if (reply.isValid())
    setWindowTitle(reply.value());
```

构造阶段会尝试获得远端接口描述。service 不存在、path 不存在、接口不匹配或 introspection 失败时，`isValid()` 为 `false`，原因从 `lastError()` 读取。

## 3. 四个构造参数真正表示什么

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 目标服务 | `service` | 指定拥有远端对象的 well-known name 或 unique name。 | 服务重启后 unique name 会变；通常使用 well-known name 并监听 owner 变化。 |
| 对象路径 | `path` | 指定远端 D-Bus object path。 | 必须与服务实际导出的路径完全一致。 |
| 接口名 | `interface` | 指定要代理的 D-Bus interface。 | 生产代码优先显式指定，避免动态合并带来的冲突。 |
| 连接 | `connection` | 指定 session、system、私有 bus 或 peer 通道。 | 默认是 session bus；服务在 system bus 时必须明确传入。 |

`parent` 遵循 QObject 生命周期规则。界面、服务控制器或长生命周期代理管理器通常适合作为父对象。

## 4. interface 为空时到底发生什么

若构造时 `interface` 是空 `QString`，Qt 会 introspect 该 object path 并将找到的**所有接口合并**为一个动态代理。

这方便临时浏览或通用工具，但有明显边界：

- 多接口的同名方法、signal、属性可能发生歧义。
- 每次协议变化都更容易在运行时而非编译期暴露。
- 代理缓存优化仅适用于指定了非空 interface 的情况。

因此，调试工具可省略 interface；业务代码应尽量指定完整接口名。

## 5. 调用方法

`QDBusInterface` 的调用 API 来自 `QDBusAbstractInterface`。

### 5.1 同步调用

```cpp
QDBusReply<int> reply = player.call("Volume");
if (reply.isError()) {
    showError(reply.error());
    return;
}

setVolume(reply.value());
```

`call()` 会构造 method call、发送、等待并返回 `QDBusMessage`；上例利用 `QDBusReply<int>` 从消息读取第一个输出参数。不要在 GUI 主线程对慢服务频繁使用同步调用。

### 5.2 异步调用

```cpp
QDBusPendingCall pending = player.asyncCall("Volume");
auto *watcher = new QDBusPendingCallWatcher(pending, this);

connect(watcher, &QDBusPendingCallWatcher::finished, this,
        [watcher] {
            QDBusPendingReply<int> reply = *watcher;
            if (!reply.isError())
                updateVolume(reply.value());
            watcher->deleteLater();
        });
```

动态参数列表可使用 `callWithArgumentList()`、`asyncCallWithArgumentList()`。它们适合插件或通用工具；固定调用优先使用模板 `call("Method", args...)`，可读性更高。

### 5.3 回调调用

`callWithCallback()` 将成功或失败转交 receiver 的槽。其返回 `true` 仅表示调用已排队，后续成功与错误都必须在相应槽中处理。

## 6. 接收远端 signal

动态接口同样是 QObject。若 signal 签名运行时才知道，可用字符串形式连接：

```cpp
connect(&player,
        SIGNAL(StateChanged(QString)),
        this,
        SLOT(onPlayerStateChanged(QString)));
```

因为这是动态 meta-object 场景，编译器无法检查远端 signal 的真实存在和签名；连接成功不代表服务真的会发该 signal。稳定接口优先用生成代理，从而获得编译期信号成员和更强检查。

若只需从总线角度精确过滤 service、path、signature 或参数，可直接使用 `QDBusConnection::connect()`。

## 7. 访问远端属性

远端 D-Bus 属性可以按 QObject 动态属性 API 使用：

```cpp
const QVariant value = player.property("Volume");
const bool ok = player.setProperty("Volume", 70);
```

这看起来像本地属性访问，实际会经过 D-Bus Properties 接口并可能失败或涉及 IPC。对于返回的 `QVariant`，先确认类型；`setProperty()` 的 `false` 不能被当作本地普通 setter 失败后就忽略，应结合 `lastError()`、服务状态和协议检查。

频繁读写远端属性会产生多次 IPC。需要批量数据时，更适合设计一个专门的远端方法一次返回所需状态。

## 8. 超时与授权

代理继承：

- `setTimeout(int)` 与 `timeout()`：控制由该代理发出的调用默认超时。
- `setInteractiveAuthorizationAllowed(bool)`：允许方法调用等待交互式授权。
- `isInteractiveAuthorizationAllowed()`：读取当前授权标志。

交互授权只影响异步调用的标志传播边界按 `QDBusAbstractInterface` 规则处理。即便允许授权，也不应把它当作“调用一定被批准”；最终仍要检查 `QDBusReply`、pending reply 或 callback 错误。

## 9. QDBusInterface 与生成代理的选择

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 动态代理 | `QDBusInterface` | 在运行时调用未知或可选远端接口。 | 方法名、属性名、信号签名多为字符串，错误更晚出现。 |
| 生成代理 | `qdbusxml2cpp` 输出类 | 用 XML 接口定义生成强类型调用包装。 | 适合稳定协议，可获得编译期成员与类型检查。 |
| 原始消息 | `QDBusMessage` | 手动构造和处理 D-Bus 消息。 | 适合动态路由、虚拟对象和协议工具，代码量更大。 |

## 10. 常见误区

### 10.1 误区：构造对象成功就代表远端接口可调用

不一定。必须检查 `isValid()`；服务可能不存在、接口 introspection 可能失败。

### 10.2 误区：省略 interface 更通用，所以总该省略

不对。空 interface 会合并多个远端接口，遇到重名成员容易产生歧义；业务代码应显式指定。

### 10.3 误区：远端属性读写和本地成员变量一样便宜

不对。它们是 IPC，可能超时、报错或受权限限制。

### 10.4 误区：`QObject::connect` 动态 signal 成功就验证了远端协议

不对。动态字符串连接只能验证本地形式，远端存在性和实际签名仍要依赖接口定义或运行时行为。

## 11. 逐项 API 说明

### 直接成员

#### `QDBusInterface(service, path, interface, connection, parent)`

创建动态远端接口代理。默认 connection 为 session bus；非空 interface 会被缓存以加速后续相同接口代理的创建，空 interface 则合并该 path 上 introspect 到的接口。

#### `~QDBusInterface()`

销毁动态代理及其缓存引用。它不关闭 `QDBusConnection`，也不停止远端服务。

### 常用继承 API

#### `isValid()` 与 `lastError()`

确认 introspection 和代理初始化是否成功，并读取错误原因。每次创建动态代理后先检查。

#### `call()`、`callWithArgumentList()`

同步调用远端方法。返回 `QDBusMessage`，通常转换为 `QDBusReply<T>`；避免在 GUI 主线程等待慢调用。

#### `asyncCall()`、`asyncCallWithArgumentList()`

异步调用远端方法，返回 `QDBusPendingCall`。搭配 `QDBusPendingReply<T...>` 与 watcher 处理结果。

#### `callWithCallback()`

把异步结果送往 QObject 槽。回调成功、错误槽的类型与对象生命周期都需要正确安排。

#### `service()`、`path()`、`interface()`、`connection()`

读取代理当前指向的远端目标和使用的连接。用于日志、断线重建和断言协议配置。

#### `setTimeout()`、`timeout()`

设置或查询该代理的默认调用超时。timeout 不是成功保证，超时后仍需处理错误。

#### `setInteractiveAuthorizationAllowed()`、`isInteractiveAuthorizationAllowed()`

控制调用是否允许等待对端交互授权。只是请求能力标志，不改变服务端最终权限判断。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDBusInterface(service, path, interface, connection, parent)` | 创建指定远端对象接口的动态代理。 | 创建后先 `isValid()`；业务代码优先传非空 interface。 |
| 析构 | `~QDBusInterface()` | 销毁本地代理对象。 | 不关闭连接，也不影响远端服务。 |
| 有效性 | `bool isValid() const` | 判断远端接口描述是否成功获得。 | service、path、interface 不存在或 introspection 失败时为 false。 |
| 错误读取 | `QDBusError lastError() const` | 获取代理初始化或调用错误。 | 用错误类型或名称分类，不用 message 作为逻辑条件。 |
| 同步调用 | `call(method, args...)` | 调用远端方法并等待回复。 | GUI 主线程谨慎使用；将结果转为 QDBusReply 后检查。 |
| 动态参数同步调用 | `callWithArgumentList(mode, method, args)` | 用 QVariant 列表调用远端方法。 | 适合运行时协议；CallMode 可能阻塞或重入。 |
| 异步调用 | `asyncCall(method, args...)` | 发起异步远端方法调用。 | 保留 pending 引用并使用 watcher 或 pending reply。 |
| 动态参数异步调用 | `asyncCallWithArgumentList(method, args)` | 用 QVariant 列表异步调用。 | 参数类型必须仍符合 D-Bus 签名。 |
| 回调调用 | `callWithCallback(method, args, receiver, return, error)` | 完成时回调 QObject 槽。 | 返回 true 只说明排队成功；连接 context 和槽签名必须正确。 |
| 远端 signal | `QObject::connect()` | 连接动态代理导出的远端 signal。 | 动态信号多用字符串形式，远端协议无法编译期验证。 |
| 远端属性读取 | `property(name)` | 读取远端 D-Bus 属性。 | 属于 IPC，检查 QVariant 类型和错误状态。 |
| 远端属性设置 | `setProperty(name, value)` | 写入远端 D-Bus 属性。 | false 时检查服务、协议和 lastError，不要静默忽略。 |
| 目标查询 | `service()`、`path()`、`interface()` | 读取代理目标三元组。 | service 可因 owner 变化重启，必要时配合 watcher。 |
| 连接查询 | `connection()` | 获取代理使用的 QDBusConnection。 | 确认 session bus、system bus 或 peer 与目标匹配。 |
| 超时 | `setTimeout(ms)` 与 `timeout()` | 设置或读取默认调用超时。 | 超时仍是正常错误路径，应设计重试或降级。 |
| 授权 | `setInteractiveAuthorizationAllowed(bool)` | 允许调用等待交互式授权。 | 不保证获批，最终由 QDBusReply 或异步错误决定。 |

---

### 一句话总结

`QDBusInterface` 是没有生成代理代码时的动态远端接口入口；显式指定接口、先检查有效性，并把方法、信号和属性都当作可能失败的 IPC，而不是本地 QObject 调用。
