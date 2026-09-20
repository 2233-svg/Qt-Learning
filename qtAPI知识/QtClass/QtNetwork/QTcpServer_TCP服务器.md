# QTcpServer：TCP 连接监听器

> Qt 6.11.1  
> 头文件：`#include <QTcpServer>`  
> 模块：`Qt6::Network`  
> 继承：`QObject`  
> 相关类型：`QTcpSocket`、`QAbstractSocket`、`QNetworkProxy`

## 它解决什么问题

`QTcpServer` 负责在本地地址和端口上监听 TCP 连接，并把已经接受的客户端连接排入 Qt 的 pending connection 队列。它不负责应用层协议，也不替每个客户端读取数据；客户端通信由 `nextPendingConnection()` 返回的 `QTcpSocket` 完成。

典型工作流是：

```text
设置 backlog / 代理
    -> listen(address, port)
    -> newConnection()
    -> nextPendingConnection()
    -> 给 QTcpSocket 连接 readyRead / disconnected
```

`newConnection()` 只表示有新连接可处理，不应在槽中假设只有一个连接，更稳妥的写法是循环调用 `hasPendingConnections()` 和 `nextPendingConnection()`。Qt 6.4 起还提供 private signal `pendingConnectionAvailable()`，它表示连接已经真正加入 pending 队列；普通应用通常继续使用公开的 `newConnection()` 和 `hasPendingConnections()`。

## 实际使用场景

### 1. 事件驱动的 TCP 服务端

```cpp
auto *server = new QTcpServer(this);
connect(server, &QTcpServer::newConnection, this, [server] {
    while (server->hasPendingConnections()) {
        auto *socket = server->nextPendingConnection();
        connect(socket, &QIODevice::readyRead, socket, [socket] {
            const QByteArray request = socket->readAll();
            socket->write(makeResponse(request));
        });
        connect(socket, &QAbstractSocket::disconnected,
                socket, &QObject::deleteLater);
    }
});

if (!server->listen(QHostAddress::Any, 9000)) {
    qWarning() << server->errorString();
}
```

`nextPendingConnection()` 返回的 socket 是 server 的子对象，server 销毁时会自动删除它；连接处理完成后仍建议显式 `deleteLater()`，避免长期运行的服务积累已断开的 socket。

### 2. 限制连接积压

`setMaxPendingConnections()` 限制 Qt 已接受但尚未被应用取出的连接数，默认值为 30。`setListenBacklogSize()` 设置操作系统等待接受的连接队列大小，Qt 6.3 起提供，默认值为 50。两者是不同层次的限制：

- Qt pending 队列满后，Qt 会停止继续接受新连接；
- 客户端仍可能成功建立连接，因为操作系统队列中可能还有空间；
- backlog 的实际上限可能被操作系统降低或忽略。

高并发服务应根据连接处理速度、内存和操作系统参数一起调整，而不是只调一个数字。

### 3. 暂停接受但保留已排队连接

`pauseAccepting()` 暂停接受新连接，已经进入队列的连接保留；恢复后调用 `resumeAccepting()`。它适合维护窗口、应用级限流或暂时停止接入，但不会断开现有客户端，也不会清空 pending 队列。

### 4. 接管已有监听描述符

服务由 systemd、父进程或自定义原生代码创建监听 socket 后，可以用 `setSocketDescriptor()` 交给 `QTcpServer`。Qt 假设传入描述符已经处于 listening 状态；成功后 `isListening()` 为 true。通过 `socketDescriptor()` 取出的描述符在使用代理时可能不是可直接交给原生 socket API 的普通描述符。

### 5. 把新连接放入工作线程

`nextPendingConnection()` 返回的 socket 不能直接跨线程使用。若要让工作线程拥有连接，应重写 `incomingConnection(qintptr)`，把描述符传给目标线程，在目标线程创建 `QTcpSocket` 并调用 `setSocketDescriptor()`。不要创建一个属于 server 线程的 socket，再仅调用 `moveToThread()` 就开始读写。

## 关键 API 语义与边界

### `listen()` 的地址和端口

`listen(QHostAddress::Any, 0)` 会在所有接口监听，并由操作系统选择端口。成功后用 `serverAddress()` 和 `serverPort()` 获取实际端点；未监听时前者返回 `QHostAddress::Null`，后者返回 0。

同一个 `QTcpServer` 不能在已监听状态下重复建立另一个监听。失败后先看 `serverError()` 和 `errorString()`，不要只根据 `listen()` 的 false 猜测原因。

### 两个连接队列

操作系统 backlog 是内核层队列；Qt pending 队列是已经被 Qt 接受、已经可以包装为 `QTcpSocket` 的队列。`newConnection()` 可能在自定义 `incomingConnection()` 中发出，即使应用没有把自定义 socket 加入 pending 队列，因此收到该信号后仍应检查 `hasPendingConnections()`。

重写 `incomingConnection()` 后，如果创建了自己的 `QTcpSocket`，必须调用 `addPendingConnection(socket)` 才能保留 Qt 的 pending connection 机制。这个保护函数还会发出 `pendingConnectionAvailable()`。遗漏它会导致 `nextPendingConnection()` 永远取不到自定义创建的连接。

### 线程和对象所有权

`QTcpServer`、它创建的 pending socket 以及这些对象的信号槽都应在所属线程处理。`nextPendingConnection()` 返回的 socket 是 server 的子对象，不能直接在另一个线程调用。跨线程处理的正确边界是原生描述符，而不是已经构造好的 QObject。

### 阻塞等待

`waitForNewConnection(msec, timedOut)` 会阻塞调用线程，直到有新连接或超时。`msec == -1` 表示不超时；发生超时时，如果 `timedOut` 非空，Qt 会把它设为 true。该函数主要用于没有事件循环的工作线程；GUI 线程应连接 `newConnection()`。

### 代理限制

`setProxy()` 允许服务器使用显式网络代理，但启用代理时 `socketDescriptor()` 和 `incomingConnection()` 参数不一定具有普通原生 socket 的语义。若需要原生 `accept()`、`getsockopt()` 等操作，应确认没有使用代理，并验证目标平台行为。

## API 速查表

### 构造、监听和生命周期

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `explicit QTcpServer(QObject *parent = nullptr)` | 创建 TCP 服务器对象。 | parent 决定 QObject 所有权和线程归属。 |
| `virtual ~QTcpServer()` | 销毁服务器并关闭监听资源。 | 子 socket 也会按 QObject 父子关系销毁。 |
| `bool listen(const QHostAddress &address = QHostAddress::Any, quint16 port = 0)` | 在地址和端口上开始监听。 | port 为 0 时系统选择端口；失败看 `serverError()` 和 `errorString()`。 |
| `void close()` | 停止监听。 | 不再接受新连接；已有 socket 的生命周期要单独处理。 |
| `bool isListening() const` | 查询是否正在监听。 | 不表示 pending 队列为空。 |
| `QHostAddress serverAddress() const` | 返回监听地址。 | 未监听时返回 `QHostAddress::Null`。 |
| `quint16 serverPort() const` | 返回监听端口。 | 未监听时返回 0。 |

### 连接队列

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `bool hasPendingConnections() const` | 查询 Qt pending 队列是否有连接。 | 可在 `newConnection()` 槽中循环检查。 |
| `QTcpSocket *nextPendingConnection()` | 取出下一个已接受连接。 | 无连接返回 nullptr；返回对象属于 server 线程和 parent。 |
| `void setMaxPendingConnections(int numConnections)` | 设置 Qt pending 队列上限。 | 默认 30；达到上限后 Qt 暂停接受，但 OS 队列可能仍有空间。 |
| `int maxPendingConnections() const` | 查询 Qt pending 队列上限。 | 不等于 OS listen backlog。 |
| `void pauseAccepting()` | 暂停接受新连接。 | 已排队连接保留。 |
| `void resumeAccepting()` | 恢复接受新连接。 | 与 `pauseAccepting()` 配对。 |
| `bool waitForNewConnection(int msec = 0, bool *timedOut = nullptr)` | 阻塞等待新连接。 | GUI 线程不应使用；`-1` 表示不超时。 |

### OS backlog 和原生描述符

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `void setListenBacklogSize(int size)` | 设置 OS 等待接受队列大小。 | Qt 6.3 起；必须在 `listen()` 前设置，OS 可能降低或忽略。 |
| `int listenBacklogSize() const` | 查询 backlog 配置。 | Qt 6.3 起；不一定等于 OS 实际采用值。 |
| `qintptr socketDescriptor() const` | 获取监听 socket 的原生描述符。 | 未监听时为 -1；代理场景下可能不可直接用于原生 API。 |
| `bool setSocketDescriptor(qintptr socketDescriptor)` | 接管已有监听描述符。 | 传入描述符必须已经处于 listening 状态；成功后 server 进入监听状态。 |

### 错误和代理

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `QAbstractSocket::SocketError serverError() const` | 返回最近一次服务器错误码。 | 错误码描述类别，配合 `errorString()`。 |
| `QString errorString() const` | 返回最近一次错误的人类可读文本。 | 文本适合日志和诊断，不应作为稳定机器协议。 |
| `void setProxy(const QNetworkProxy &networkProxy)` | 设置服务器使用的显式代理。 | `QNetworkProxy::NoProxy` 明确禁用；影响描述符和 incomingConnection 语义。 |
| `QNetworkProxy proxy() const` | 查询当前代理。 | 默认值和支持能力由代理类型决定。 |

### 信号和扩展点

| API | 语义 | 使用边界 |
| --- | --- | --- |
| `newConnection()` | 有新连接可处理时发出。 | 不保证连接已进入 Qt pending 队列；槽中检查 `hasPendingConnections()`。 |
| `pendingConnectionAvailable()` | Qt 6.4 起，连接加入 pending 队列后发出。 | private signal，普通代码通常不能像公开信号一样主动使用。 |
| `acceptError(QAbstractSocket::SocketError socketError)` | 接受新连接发生错误时发出。 | 记录 `serverError()`、`errorString()` 并按策略恢复。 |
| `virtual void incomingConnection(qintptr socketDescriptor)` | 新连接到达时的重写钩子。 | 自定义 socket 必须调用 `addPendingConnection()`；跨线程应传描述符。 |
| `void addPendingConnection(QTcpSocket *socket)` | 把自定义 socket 加入 pending 队列。 | 保护函数；Qt 6.8 起重写 incomingConnection 时尤其不能遗漏。 |
| `QTcpServer(QAbstractSocket::SocketType, QTcpServerPrivate &, QObject *)` | Qt 内部或派生实现构造入口。 | 普通应用不应依赖 private data 实现细节。 |
