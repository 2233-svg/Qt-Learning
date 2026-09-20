# QDBusServer
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusServer`

## 作用定位

`QDBusServer` 用来创建一个私有 D-Bus server，接受点对点连接。它不等同于 system/session bus daemon，也不负责全局服务名注册；它更像一个 D-Bus 协议的监听端，客户端拿到 `address()` 后用 `QDBusConnection::connectToPeer()` 连接。

## 类说明

- 头文件：`#include <QDBusServer>`
- CMake：链接 `Qt6::DBus`
- 继承：`QObject`
- 信号：新连接到达时发出 `newConnection(QDBusConnection)`

## API 速查

| API | 说明 |
| --- | --- |
| `QDBusServer(parent)` | 创建 server，并让 Qt 选择监听地址。 |
| `QDBusServer(address, parent)` | 在指定地址上创建 server。 |
| `~QDBusServer()` | 关闭监听并释放资源。 |
| `address()` | 返回客户端连接所需地址。 |
| `isConnected()` | server 是否成功监听。 |
| `lastError()` | 创建或监听失败原因。 |
| `setAnonymousAuthenticationAllowed(bool)` | 是否允许匿名认证。 |
| `isAnonymousAuthenticationAllowed()` | 读取匿名认证设置。 |
| `newConnection(connection)` | 有新 peer 连接时发出。 |

## 典型用法

```cpp
auto *server = new QDBusServer(this);
if (!server->isConnected()) {
    qWarning() << server->lastError().message();
    return;
}

qDebug() << "Peer address:" << server->address();

connect(server, &QDBusServer::newConnection, this,
        [](const QDBusConnection &connection) {
    connection.registerObject("/org/example/Peer", new PeerObject,
                              QDBusConnection::ExportAllSlots);
});
```

## 使用场景

- 两个进程之间建立私有 D-Bus 通道。
- 不希望接口出现在 session/system bus 上。
- 测试 D-Bus peer-to-peer 通信。
- 嵌入式或工具链里临时发布一个只给已知客户端用的服务。

## 常见坑与经验

- `QDBusServer` 没有知名服务名概念，不能用 `registerService()` 那套 bus daemon 逻辑理解它。
- 客户端必须拿到 `address()`，否则无法发现这个 server。
- `newConnection` 给的是一条 `QDBusConnection`，后续仍要注册对象或发送消息。
- 匿名认证会降低访问边界，只有在明确的私有环境里才应打开。
- 地址绑定失败时优先看 `lastError()`，常见原因是地址已占用或传输后端不支持。

## 知识点覆盖

- D-Bus peer-to-peer 模式
- 私有 server 与 bus daemon 的区别
- 地址发现与连接建立
- 匿名认证
- 新连接对象注册流程
