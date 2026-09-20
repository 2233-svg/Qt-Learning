# QDBusConnection
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusConnection`

## 作用定位

`QDBusConnection` 是 Qt D-Bus 的连接句柄：它代表一条到 session bus、system bus、私有 bus 或点对点 peer 的通信通道。多数 D-Bus 代码都会先拿到连接，再用它注册服务名、导出对象、发送消息或订阅远端信号。

它是值语义句柄，复制 `QDBusConnection` 不等于重新连接一条 bus，而是共享同一个底层连接引用。因此析构一个 `QDBusConnection` 对象不会关闭 bus；真正关闭命名连接要调用 `disconnectFromBus()` 或 `disconnectFromPeer()`。

## 类说明

- 头文件：`#include <QDBusConnection>`
- CMake：`find_package(Qt6 REQUIRED COMPONENTS DBus)`，链接 `Qt6::DBus`
- 继承：无公开 QObject 继承，按轻量句柄理解
- 常用协作类：`QDBusMessage`、`QDBusInterface`、`QDBusConnectionInterface`、`QDBusAbstractAdaptor`、`QDBusPendingCall`

## API 速查

| API | 说明 |
| --- | --- |
| `sessionBus()` / `systemBus()` | 取得默认会话总线或系统总线连接。桌面应用通常用 session bus，系统服务管理、硬件、网络等能力通常在 system bus。 |
| `connectToBus(type, name)` | 以自定义连接名打开标准 bus，适合需要隔离连接或明确控制关闭时机的程序。 |
| `connectToBus(address, name)` | 连接到指定地址的私有 D-Bus daemon。 |
| `connectToPeer(address, name)` | 建立点对点 D-Bus 连接，不经过 bus daemon 的服务名路由。 |
| `disconnectFromBus(name)` / `disconnectFromPeer(name)` | 释放命名底层连接；已有句柄仍可能延后关闭到底层引用清空。 |
| `isConnected()` | 检查句柄当前是否连通。低层连接失败时先看它，再看 `lastError()`。 |
| `baseService()` | 返回 bus 分配的唯一连接名，例如 `:1.42`；点对点连接通常为空。 |
| `name()` | 返回 Qt 侧命名连接的名称，不是 D-Bus 的知名服务名。 |
| `interface()` | 取得 bus daemon 的管理接口，可查询服务列表、owner、PID/UID、启动服务等。 |
| `registerService()` / `unregisterService()` | 申请或释放知名服务名，例如 `org.example.App`。 |
| `registerObject()` / `unregisterObject()` | 把本地 `QObject` 暴露到 D-Bus 对象路径上。 |
| `objectRegisteredAt()` | 查询某路径当前注册的本地对象。 |
| `send()` | 发送信号、错误、返回消息或不关心返回值的方法调用。 |
| `call()` | 同步发送方法调用并等待回复；可能阻塞，`BlockWithGui` 还可能重入事件循环。 |
| `asyncCall()` | 异步发送方法调用，返回 `QDBusPendingCall`。 |
| `callWithCallback()` | 异步发送后把成功/错误送到指定 receiver 的槽。 |
| `connect()` / `disconnect()` | 订阅或取消订阅远端 D-Bus 信号。 |
| `connectionCapabilities()` | 查询连接能力，如 Unix 文件描述符传递。 |
| `lastError()` | 返回最近一次连接层错误，适合定位注册、发送、连接失败原因。 |
| `localMachineId()` | 获取本机 D-Bus 机器 ID；不应当作为长期持久身份。 |

## 枚举与选项

| 类型 | 值 | 说明 |
| --- | --- | --- |
| `BusType` | `SessionBus` | 当前登录会话内应用共享的 bus。 |
| `BusType` | `SystemBus` | 系统级 bus，常用于特权服务、设备、网络与桌面系统组件。 |
| `BusType` | `ActivationBus` | 激活当前服务所用 bus 的别名。 |
| `ConnectionCapability` | `UnixFileDescriptorPassing` | 可用 `QDBusUnixFileDescriptor` 传递 Unix fd。 |
| `RegisterOption` | `ExportAdaptors` | 只导出挂在对象上的 D-Bus adaptor。最稳妥，也是默认值。 |
| `RegisterOption` | `ExportScriptable*` | 只导出标记为 scriptable 的槽、信号、属性或 invokable。 |
| `RegisterOption` | `ExportNonScriptable*` / `ExportAll*` | 扩大导出面。方便调试，但生产代码要慎用，避免意外暴露 QObject API。 |
| `RegisterOption` | `ExportChildObjects` | 根据子对象 `objectName()` 递归导出子对象路径。 |
| `UnregisterMode` | `UnregisterNode` | 只注销当前路径节点。 |
| `UnregisterMode` | `UnregisterTree` | 注销当前路径及子树。 |

## 典型用法

```cpp
QDBusConnection bus = QDBusConnection::sessionBus();
if (!bus.isConnected())
    return;

QDBusMessage msg = QDBusMessage::createMethodCall(
    "org.example.Service",
    "/org/example/Object",
    "org.example.Interface",
    "Ping");

QDBusMessage reply = bus.call(msg);
if (reply.type() == QDBusMessage::ErrorMessage)
    qWarning() << reply.errorName() << reply.errorMessage();
```

导出本地对象时：

```cpp
auto *backend = new Backend(&app);
auto bus = QDBusConnection::sessionBus();

bus.registerObject("/org/example/App", backend,
                   QDBusConnection::ExportAdaptors);
bus.registerService("org.example.App");
```

这里最重要的是顺序和导出面：对象路径决定远端如何寻址，服务名决定别人如何找到你，`RegisterOptions` 决定 QObject 的哪些成员被暴露。

## 使用场景

- 桌面应用间通信：托盘程序、设置面板、单例应用唤起已运行实例。
- 系统服务调用：通过 system bus 与 NetworkManager、systemd、BlueZ、UPower 等服务交互。
- 自己发布 D-Bus 服务：把 C++ `QObject` 或 adaptor 注册成可被其他进程调用的接口。
- 监听系统事件：订阅远端 D-Bus signal，而不是轮询状态。
- 私有 IPC：用 `connectToBus(address)` 或 `connectToPeer()` 搭建非全局的进程间通道。

## 常见坑与经验

- `name()`、`baseService()`、`registerService()` 的“名字”不是一回事：`name()` 是 Qt 命名连接，`baseService()` 是 bus 分配的唯一名，`registerService()` 申请的是知名服务名。
- `registerObject()` 默认只导出 adaptor，不会把整个 QObject 所有槽都公开。想省事用 `ExportAllContents` 前，先确认不会暴露调试槽、内部属性或危险方法。
- `call()` 是同步 IPC，不要在 GUI 热路径里频繁调用；远端卡住时你的线程也会卡住。
- `BlockWithGui` 会在等待期间处理事件，槽函数可能被重入。状态机、锁、临时对象生命周期都要按可重入场景设计。
- `connect()` 订阅信号时，service/path/interface/name/signature 都会影响匹配；断开时参数必须与连接时一致。
- 点对点连接没有 bus daemon 的服务名注册模型，`baseService()` 也不会给你 `:1.x` 这样的唯一名。

## 知识点覆盖

- D-Bus session bus、system bus、peer-to-peer 的差异
- D-Bus 唯一连接名与知名服务名
- 对象路径、接口名、成员名组成的寻址模型
- 同步调用、异步调用、无返回发送的区别
- QObject 导出策略与 adaptor 模式
- D-Bus 信号订阅匹配规则
- 连接能力协商与 Unix fd 传递
