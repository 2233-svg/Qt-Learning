# Qt QDBusServer 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusServer>`  
> 所属模块：`Qt6::DBus`  
> 继承：`QObject`

## 1. 它解决什么问题

大多数 Qt D-Bus 程序连接的是 session bus 或 system bus，由总线进程负责服务名与消息路由。`QDBusServer` 走的是另一条路：它创建一个**点对点 D-Bus 服务端地址**，让同一台计算机上的客户端直接连接到当前进程。

它适合：

- 不需要注册到公共 bus 的本机私有 IPC。
- 测试中创建临时 D-Bus 服务端。
- 需要由应用自行接收客户端连接的点对点协议。

```text
QDBusServer 监听一个地址
      │
      └─ 客户端建立点对点连接
                │
                └─ newConnection(QDBusConnection)
```

它不是 `QDBusConnection::sessionBus()` 的替代品：没有公共总线的服务发现、服务名仲裁和系统级策略。若只是做桌面服务通信，通常优先使用 session bus。

## 2. 构建与最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
```

```cpp
#include <QDBusServer>

auto *server = new QDBusServer(this);
if (!server->isConnected()) {
    qWarning() << server->lastError().name()
               << server->lastError().message();
    return;
}

qInfo() << "D-Bus peer server address:" << server->address();

connect(server, &QDBusServer::newConnection, this,
        [this](const QDBusConnection &connection) {
            configurePeer(connection);
        });
```

默认构造会在 Unix 系统中使用 `/tmp` 下的监听点；在其他平台上使用绑定到 localhost 的 TCP 端口。`address()` 返回的地址要交给受信任客户端用于建立点对点连接。

## 3. 连接模型

`QDBusServer` 成功创建后就开始监听，没有单独的 `listen()`、`accept()`、`close()` API。客户端建立连接时，server 发出 `newConnection(const QDBusConnection &)`.

收到的 `QDBusConnection` 是该客户端的连接句柄。你可以在槽函数中为它注册对象、连接信号或保存必要状态：

```cpp
connect(server, &QDBusServer::newConnection, this,
        [this](const QDBusConnection &peer) {
            peer.registerObject("/org/example/Service", serviceObject);
        });
```

对象注册、访问控制与连接命名规则仍由你的点对点协议负责设计。不要假定每一条新连接都来自可信客户端。

## 4. 匿名认证：一个安全边界

默认情况下，`isAnonymousAuthenticationAllowed()` 为 `false`。这意味着入站客户端不能仅以匿名身份继续连接，必须通过 D-Bus 的用户认证流程。

```cpp
server->setAnonymousAuthenticationAllowed(false); // 默认且推荐
```

若设置为 `true`，连接客户端即使没有被认证为某个用户也可继续：

```cpp
server->setAnonymousAuthenticationAllowed(true);
```

这只应出现在你明确控制地址暴露范围、并且协议层另有安全机制的场景。对能被其他本机用户或不可信进程访问的监听地址，允许匿名认证会扩大攻击面。

## 5. 地址与错误处理

### 5.1 `address()` 是给客户端的连接地址

它不是一个供人展示的标签，而是客户端实际连接所需的 D-Bus address。不要把地址写死；每次实例化都应从 `address()` 获取。

### 5.2 `isConnected()` 为假不能靠重试同一对象修复

官方约定是：若 server 没有连接成功，需要重新调用构造函数创建新实例。这个类没有重新绑定或重新监听成员函数。

### 5.3 `lastError()` 面向底层排查

连接失败时，`lastError()` 提供低层 D-Bus 错误。业务提示应根据 `type()` 或 `name()` 分类，而不是让用户直接看到底层 message。

## 6. 常见误区

### 6.1 误区：它会自动注册一个公共服务名

不会。它创建的是点对点监听端，不加入 session bus 或 system bus 的服务名体系。

### 6.2 误区：`newConnection` 等于客户端已经具备业务权限

不是。它仅表示点对点连接已建立；认证策略、对象注册和请求授权仍是应用责任。

### 6.3 误区：`setAnonymousAuthenticationAllowed(true)` 只是兼容选项

不是。它会直接改变能否接受未认证客户端，应作为安全决策而不是调试开关。

### 6.4 误区：监听失败后可以对现有对象调用重新连接 API

没有这样的 API。检查 `isConnected()`，记录 `lastError()`，然后创建新的 `QDBusServer`。

## 7. 逐项 API 说明

### 构造与状态

#### `explicit QDBusServer(QObject *parent = nullptr)`

创建默认地址的点对点 server 并开始监听。Unix 默认在 `/tmp` 下监听，其他平台默认绑定 localhost TCP。传入 `parent` 管理其生命周期。

#### `explicit QDBusServer(const QString &address, QObject *parent = nullptr)`

使用指定 D-Bus address 创建并监听。地址的可访问范围与传递方式直接决定哪些客户端可能连接。

#### `~QDBusServer()`

销毁 server，停止它的监听资源。QObject 父对象销毁时也会触发该过程。

#### `QString address() const`

返回 server 实际关联的连接地址。客户端应使用该值建立点对点连接，而不是猜测默认地址。

#### `bool isConnected() const`

返回 server 是否成功建立监听。若为 `false`，需要新建 server，而不是等待当前对象自行恢复。

#### `QDBusError lastError() const`

返回最近发生的底层错误。主要用于诊断连接失败或低层问题。

### 身份验证与连接事件

#### `bool isAnonymousAuthenticationAllowed() const`

查询是否允许未认证用户的入站连接继续。默认值为 `false`。

#### `void setAnonymousAuthenticationAllowed(bool value)`

设置匿名认证策略。设置为 `true` 前要确保监听地址、协议和对象操作都能承受不可信客户端。

#### `newConnection(const QDBusConnection &connection)`

新客户端点对点连接建立时发出。应在对应槽中配置该连接，并按业务建立对象或权限状态。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDBusServer(QObject *parent)` | 用平台默认地址创建点对点 server。 | 创建后立即检查 `isConnected()`。 |
| 构造 | `QDBusServer(const QString &address, QObject *parent)` | 在指定 D-Bus 地址监听。 | 地址暴露范围决定潜在客户端范围。 |
| 析构 | `~QDBusServer()` | 释放监听资源。 | 使用 QObject parent 管理生命周期即可。 |
| 地址查询 | `QString address() const` | 获取客户端连接所需地址。 | 不要硬编码默认地址，向受信任客户端传递实际返回值。 |
| 认证查询 | `bool isAnonymousAuthenticationAllowed() const` | 查询是否接受匿名认证。 | 默认是 `false`。 |
| 连接状态 | `bool isConnected() const` | 判断监听是否建立成功。 | 为 `false` 时新建 server，不能在原对象上重连。 |
| 错误查询 | `QDBusError lastError() const` | 获取最近底层错误。 | 用于日志与诊断，不要直接把底层错误文本原样当用户提示。 |
| 信号 | `newConnection(const QDBusConnection &connection)` | 通知有新的点对点客户端连接。 | 新连接不等于已获业务授权，需配置对象和权限。 |
| 认证设置 | `void setAnonymousAuthenticationAllowed(bool value)` | 设置是否允许匿名入站连接。 | `true` 会放宽安全边界，仅在受控场景使用。 |

---

### 一句话总结

`QDBusServer` 用于同机进程间的点对点 D-Bus 通信；它负责监听和交付新连接，而认证策略、对象暴露与业务授权仍需要应用自己把关。
