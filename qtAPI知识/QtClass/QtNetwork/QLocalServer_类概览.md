# QLocalServer：进程间本地通信的监听端

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLocalServer>`  
> CMake：`Qt6::Network`  
> 继承：`QObject`

## 它解决什么问题

`QLocalServer` 让一个进程在本机监听名称，并接受其他本机进程的连接。它对应 TCP 世界里的 `QTcpServer`，但传输不经过网络栈：Windows 上通常是命名管道，Unix 上通常是 Unix domain socket。

它负责的工作是“监听和接入”，不是业务协议：调用 `listen()` 建立监听端点；每当客户端接入便发出 `newConnection()`；调用 `nextPendingConnection()` 取得一个已经连接好的 `QLocalSocket`，之后的读写由该 socket 完成。

## 实际使用场景

- 桌面应用的单实例协调：后启动的进程向已运行实例发送“打开文件”“聚焦窗口”等命令。
- IDE、插件宿主、语言服务或后台守护进程之间的同机 RPC。
- 不希望打开 TCP 端口、只允许本机用户通信的控制通道。

本地 socket 并不天然等于“可信 IPC”。在多用户机器上，端点权限、协议认证、输入长度限制和消息校验仍然不可少。

## 基本工作流

```cpp
#include <QLocalServer>
#include <QLocalSocket>
#include <QDebug>

QLocalServer server;
server.setSocketOptions(QLocalServer::UserAccessOption);

const QString endpoint = QStringLiteral("com.example.mytool");
#ifdef Q_OS_UNIX
QLocalServer::removeServer(endpoint); // 仅用于确认是本程序遗留的旧 socket 文件
#endif

if (!server.listen(endpoint)) {
    qWarning() << server.serverError() << server.errorString();
} else {
    QObject::connect(&server, &QLocalServer::newConnection, &server, [&server] {
        while (QLocalSocket *client = server.nextPendingConnection()) {
            QObject::connect(client, &QLocalSocket::readyRead, client, [client] {
                const QByteArray request = client->readAll();
                // 按自定义协议处理 request，并设置消息边界与长度上限。
                client->write("ok\n");
            });
        }
    });
}
```

示例将 `client` 作为 `readyRead` 连接的上下文对象，因此 socket 销毁时连接会自动断开。接受到的 socket 应持续保存、读写或显式关闭；不要只取到指针就让它脱离应用协议管理。

## 关键语义与边界

### `serverName()` 与 `fullServerName()` 不同

传给 `listen(name)` 的逻辑名字由 `serverName()` 返回；平台转换后的实际完整路径或名称由 `fullServerName()` 返回。前者适合应用协议约定，后者适合诊断。后者是平台相关值：

- Unix 可以是路径，例如 `/tmp/mytool`；
- Windows 可以是命名管道路径，例如 `\\.\pipe\mytool`。

Unix 进程异常退出后，文件系统中的 socket 文件可能残留，随后同名 `listen()` 会以 `AddressInUseError` 失败。`removeServer()` 在 Unix 删除指定 socket 文件，在 Windows 什么也不做。只应移除本应用确信属于自己的端点，不能把它当作“抢占同名服务”的通用手段。

### 权限必须在 `listen()` 前设置

`socketOptions` 控制监听端点的访问权限，必须在 `listen()` 前调用 `setSocketOptions()`。默认 `NoOptions` 使用平台默认权限。

`UserAccessOption` 是常见的最小权限选择，但具体含义依平台而异：

- Linux：`GroupAccessOption`、`OtherAccessOption` 接近文件权限的 group/other 语义；显式选项可覆盖受 `umask` 影响的默认权限。
- macOS 等部分 Unix：域 socket 文件权限可能不生效，权限标志也可能没有作用。
- Windows：`UserAccessOption` 允许同一用户的非提升进程连接由提升进程创建的服务器；Group/Other 对应 Windows 的主组和 Everyone。
- `AbstractNamespaceOption` 只在 Linux 使用抽象命名空间；这时不依赖文件系统，权限选项没有意义。在其他平台它为可移植性等价于 `WorldAccessOption`。

### 两层等待队列不要混淆

`setListenBacklogSize()` 设置请求交给操作系统的监听 backlog，默认请求值为 50，系统可能缩小或忽略它。它控制“尚未被 accept 的连接请求”。

`setMaxPendingConnections()` 设置 Qt 已经接受、但尚未由 `nextPendingConnection()` 取走的连接数，默认值为 30。达到上限后，`QLocalServer` 暂停继续接受；但操作系统队列仍可能保留连接，客户端甚至可能已经认为自己连上。因此它不是严格的客户端并发上限。

### 事件驱动优先，阻塞调用只放工作线程

有事件循环时，连接 `newConnection()` 并立刻循环取走所有 pending socket。没有事件循环时可使用 `waitForNewConnection()`，但它会阻塞到有连接或超时为止，单线程 GUI 主线程不应调用。

### 所有权和派生扩展

默认 `incomingConnection()` 会创建 `QLocalSocket`、设置原生描述符、加入 pending 队列，然后发出 `newConnection()`。服务器析构会关闭监听；仍连接着的客户端 socket 必须先断开，或在删除服务器前重新指定父对象。

若重写 `incomingConnection()`，必须在希望保留标准 pending 机制时调用 `addPendingConnection(socket)`；Qt 6.8 起这个受保护函数会把 socket 入队并发出 `newConnection()`。忽略它意味着 `nextPendingConnection()` 再也拿不到该连接。

## 常见误区

- **`close()` 会断开已接入的客户端**：不会。它只停止监听，现有 `QLocalSocket` 不受影响。
- **一个 `newConnection()` 只取一次**：信号到达时可能已有多个连接排队，应循环调用 `nextPendingConnection()` 直到返回 `nullptr`。
- **`setMaxPendingConnections()` 等同 OS backlog**：两者位于不同层。
- **Windows 上调用 `removeServer()` 能清理管道**：该函数在 Windows 无操作。
- **把阻塞 `waitForNewConnection()` 放在 GUI 线程**：界面会停止处理事件。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 枚举 | `SocketOption` / `SocketOptions` | 端点访问控制选项；为可按位组合的 `QFlags`。 |
| 枚举值 | `NoOptions` | 使用平台默认权限。 |
| 枚举值 | `UserAccessOption` | 限制为创建端点的同一用户；Windows 提升/非提升同用户场景尤其有用。 |
| 枚举值 | `GroupAccessOption` | Linux 按 group 限制，Windows 是进程主组；平台含义略有差异。 |
| 枚举值 | `OtherAccessOption` | Linux 对应非 owner/group 的用户，Windows 对应 Everyone。 |
| 枚举值 | `WorldAccessOption` | 无访问限制。 |
| 枚举值 | `AbstractNamespaceOption` | Linux 抽象命名空间；其他平台等价于 `WorldAccessOption`。 |
| 构造/析构 | `QLocalServer(parent)` / `~QLocalServer()` | QObject 生命周期；析构会停止监听，已连接 socket 应先断开或重新设父对象。 |
| 监听 | `listen(const QString &name)` | 按逻辑名创建并监听本地端点；已监听时失败，失败后检查错误。 |
| 监听 | `listen(qintptr socketDescriptor)` | 以已有原生监听描述符开始服务；描述符的平台类型和有效性由调用者负责。 |
| 监听 | `close()` | 停止接受新连接，不影响已经建立的连接。 |
| 状态 | `isListening()` | 查询当前是否在监听。 |
| 状态 | `serverName()` | 返回传入 `listen()` 的逻辑名称。 |
| 状态 | `fullServerName()` | 返回平台相关的完整实际名称或路径。 |
| 状态 | `socketDescriptor()` | 返回本地原生监听描述符；未监听时为 `-1`。 |
| 错误 | `serverError()` | 返回最近一次服务端 socket 错误枚举。 |
| 错误 | `errorString()` | 返回人可读错误文本；没有合适文本时为空。 |
| 接入 | `newConnection()` | 有新连接进入 pending 队列时发出；槽中应及时取走连接。 |
| 接入 | `hasPendingConnections()` | 是否已有可由 Qt 交付的 pending 连接。 |
| 接入 | `nextPendingConnection()` | 取出下一个已连接 `QLocalSocket`；队列为空返回 `nullptr`。 |
| 接入 | `waitForNewConnection(msec, timedOut)` | 阻塞等待新连接或超时；适合无事件循环的工作线程，不适合 GUI 主线程。 |
| 队列 | `setListenBacklogSize(size)` / `listenBacklogSize()` | Qt 6.3 起；设置/读取请求给 OS 的 accept backlog，OS 可调整或忽略。 |
| 队列 | `setMaxPendingConnections(num)` / `maxPendingConnections()` | 控制 Qt 内部已接受而未取走的队列；默认最大值为 30。 |
| 权限 | `setSocketOptions(options)` / `socketOptions()` | 设置/读取端点选项；必须在 `listen()` 前设置。 |
| 权限 | `bindableSocketOptions()` | 返回可供 `QProperty` 绑定的权限属性接口。 |
| 清理 | `removeServer(name)` | 静态函数；Unix 删除 socket 文件，Windows 无操作。只清理确定属于自己的遗留端点。 |
| 派生 | `incomingConnection(socketDescriptor)` | 新接入时的虚扩展点；基类实现会创建并入队 socket。 |
| 派生 | `addPendingConnection(socket)` | Qt 6.8 起；自定义 `incomingConnection()` 时用它保留 pending 队列和 `newConnection()` 信号。 |

## 相关类型

- `QLocalSocket`：每条已接入连接的读写通道。
- `QTcpServer`：需要跨机器或 TCP 协议时使用的服务器类。
- `QAbstractSocket::SocketError`：`serverError()` 返回的错误类型。
