# Qt QSocketNotifier：事件循环中的描述符就绪通知

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSocketNotifier>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QSocketNotifier`  
> 类型性质：监听 socket/文件描述符就绪状态的 QObject

## 1. 它解决什么问题

`QSocketNotifier` 把底层 socket 或操作系统文件描述符接入 Qt 事件循环。当描述符变得可读、可写或出现异常条件时，它发出 `activated()` 信号，让应用在不阻塞线程的情况下处理 I/O：

```cpp
auto *notifier = new QSocketNotifier(
    socketFd, QSocketNotifier::Read, this);

connect(notifier, &QSocketNotifier::activated,
        this, [this](QSocketDescriptor socket,
                     QSocketNotifier::Type type) {
    Q_UNUSED(socket);
    Q_UNUSED(type);
    readAvailableData();
});
```

它常用于：

- 管道、Unix domain socket、标准输入等描述符；
- 已有原生 socket 的事件循环集成；
- 在 `QProcess`、设备驱动或平台 API 外围接入可读/可写通知；
- 需要把非阻塞 I/O 组合进 Qt GUI 或 worker 事件循环。

它只负责“通知就绪”，不负责 `read()`、`write()`、`recv()`、`send()`、关闭描述符或处理协议状态。

## 2. 它不是什么

`QSocketNotifier` 不是：

- socket 对象或文件描述符 owner；
- 可移植的 TCP/UDP 网络 API；
- “收到完整消息”的通知器；
- 阻塞读写线程；
- 自动清空内核缓冲区的读取器；
- 跨线程 I/O 同步工具。

`activated()` 只说明底层事件分发器报告了某种就绪条件。回调中仍需实际读写并检查返回值、错误码、EOF、EAGAIN/EWOULDBLOCK 等平台结果。

## 3. 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QCoreApplication>
#include <QSocketNotifier>

class Reader final : public QObject
{
public:
    Reader(qintptr fd, QObject *parent = nullptr)
        : QObject(parent),
          m_notifier(fd, QSocketNotifier::Read, this)
    {
        connect(&m_notifier, &QSocketNotifier::activated,
                this, [this](QSocketDescriptor,
                             QSocketNotifier::Type) {
            readAvailable();
        });
    }

private:
    void readAvailable()
    {
        // 调用平台 read/recv，循环读取直到暂时没有数据。
    }

    QSocketNotifier m_notifier;
};
```

`QSocketNotifier` 只保存并监听描述符值；上例中的文件描述符仍由外部 owner 管理。对象销毁时 notifier 会停止监听，但不会替调用方关闭原生描述符。

## 4. 三种监听类型

### 4.1 `Read`

`Read` 表示描述符具备某种读取条件，例如有数据可读、连接已建立、管道对端关闭导致读操作可观察到 EOF。它不保证读操作一定返回一个完整应用层消息。

### 4.2 `Write`

`Write` 表示当前写操作可能不会立即阻塞。对多数非阻塞 socket，写 notifier 可能持续产生通知；只在确实有待发送数据时启用它，发送缓冲清空后立即禁用，避免事件循环空转。

### 4.3 `Exception`

`Exception` 监听平台事件分发器定义的异常条件。不同操作系统对“异常”或带外数据的支持不同，不能把它当作统一的“socket 出错”信号。应用仍应检查实际 I/O 错误和连接状态。

## 5. 就绪通知的真实语义

### 5.1 一次激活不等于一条消息

TCP、管道和文件描述符都可能一次读到多条消息、半条消息或 EOF。`activated()` 后应按协议解析：

```cpp
void Reader::readAvailable()
{
    for (;;) {
        const QByteArray chunk = tryRead();
        if (chunk.isEmpty()) {
            if (temporarilyWouldBlock())
                break;
            if (peerClosed()) {
                closeConnection();
                break;
            }
            handleReadError();
            break;
        }
        appendAndParse(chunk);
    }
}
```

不要把 notifier 的激活次数当作消息数量或字节数量。

### 5.2 处理完成后要让状态回到不就绪

如果回调没有消耗可读数据，或没有处理 EOF/错误，事件循环可能立刻再次发出 `activated()`，造成高 CPU 重复通知。

对 `Write` notifier 尤其重要：只有待发送缓冲非空时启用，写完后禁用。

### 5.3 notifier 默认启用状态

创建 notifier 后通常处于 enabled 状态。若底层描述符尚未完成初始化，或当前没有需要写出的数据，应显式调用 `setEnabled(false)`，避免无意义的通知。

## 6. 描述符的有效性和所有权

### 6.1 构造不会复制或拥有描述符

```cpp
QSocketNotifier notifier(fd, QSocketNotifier::Read);
```

这里的 `fd`/socket 值只是注册到事件分发器的句柄。`QSocketNotifier` 不负责：

- 取得描述符所有权；
- 关闭描述符；
- 修改 socket 阻塞模式；
- 绑定地址或连接远端；
- 释放平台句柄。

关闭描述符前应先禁用或销毁 notifier，并确保不会再有事件使用旧值。关闭后复用同一个整数描述符给其他资源，会使旧 notifier 监听到错误对象或产生未定义的业务行为。

### 6.2 `isValid()` 只检查 notifier 当前描述符状态

它不能验证：

- 描述符对应的协议类型；
- 对端是否仍然连接；
- 读写是否一定成功；
- 当前线程是否是正确的 I/O 线程；
- 描述符是否被外部代码提前关闭。

外部 owner 关闭或复用句柄后，应用必须同步更新 notifier 生命周期。

## 7. 启用、禁用和重新绑定

```cpp
notifier.setEnabled(false);
notifier.setSocket(newSocket);
notifier.setEnabled(true);
```

### `setEnabled(bool)`

启用或停止该 notifier 向事件循环注册对应类型的就绪监听。它不关闭 socket，也不清空内核缓冲区。

### `setSocket(qintptr)`

更换被监听的 socket/描述符。替换前应先禁用 notifier，完成外部资源状态切换后再启用。新值必须是当前线程事件分发器可以监听的有效平台描述符。

### 空或无效描述符

不同平台对无效 socket 值的定义不同。设置无效值后 `isValid()` 会反映 notifier 当前不可用，但业务不应依赖“无效句柄必然不会触发任何通知”来管理生命周期；更稳妥的做法是禁用或销毁 notifier。

## 8. 线程和事件循环规则

`QSocketNotifier` 是 QObject，监听注册在它所属线程的事件分发器中：

- 线程必须运行 Qt 事件循环；
- `activated()` 在 notifier 所属线程发出；
- 启用、禁用和更换 socket 应在该线程执行；
- 描述符的读写也通常应在同一 I/O 线程完成；
- 不要从 GUI 线程直接操作属于 worker 线程的 notifier。

对象移动线程时，已有的 notifier 注册会随 QObject 线程迁移而重新安排，但底层描述符本身不会被移动或复制。实际工程中更稳妥的模式是在目标线程启动后创建或启用 notifier。

## 9. `activated()` 信号签名和连接

Qt 6.11.1 的现代信号签名是：

```cpp
void activated(QSocketDescriptor socket,
               QSocketNotifier::Type activationEvent);
```

类型参数通过 `QSocketNotifier::Type` 区分 Read、Write、Exception。旧代码可能使用 `int socket` 的兼容信号；新代码优先使用类型安全的 `QSocketDescriptor` 版本：

```cpp
connect(notifier, &QSocketNotifier::activated,
        receiver,
        [](QSocketDescriptor socket,
           QSocketNotifier::Type type) {
            Q_UNUSED(socket);
            Q_UNUSED(type);
        });
```

如果编译器遇到重载歧义，可以用 `qOverload` 明确选择信号。

`QSocketDescriptor` 是一个轻量描述符值类型：

- 在 Unix 上底层通常是 `int`；
- 在 Windows 上底层通常是 `Qt::HANDLE`；
- Windows 还提供到 `qintptr` 和 `winHandle()` 的转换；
- 它不是拥有型句柄，不会在析构时关闭资源。

## 10. 典型使用场景

### 10.1 读 notifier

```cpp
connect(&readNotifier, &QSocketNotifier::activated,
        this, [this](QSocketDescriptor,
                     QSocketNotifier::Type) {
    while (readOneChunk()) {
        // 读取并解析，直到暂时没有更多数据。
    }
});
```

读回调必须正确处理短读、EOF、暂时不可读和真实错误。

### 10.2 写 notifier 的按需启用

```cpp
void Sender::queueBytes(QByteArray bytes)
{
    m_pending += bytes;
    m_writeNotifier.setEnabled(true);
}

void Sender::onWritable()
{
    writePendingBytes();
    m_writeNotifier.setEnabled(!m_pending.isEmpty());
}
```

始终启用写 notifier 常导致事件循环不断唤醒。只有待发送队列非空时才打开，是常见的事件驱动写法。

### 10.3 管道或标准输入

在支持相应描述符监听的 Unix 场景，可以监听标准输入或管道的可读事件。Windows 对可监听句柄类型有平台限制，不能假设所有 HANDLE 都能直接交给 `QSocketNotifier`。

## 11. 平台和资源边界

`QSocketNotifier` 能监听的对象由 Qt 平台事件分发器和操作系统决定：

- Unix 常见 socket、管道和文件描述符；
- Windows 更适合 Winsock socket 等可被事件机制支持的句柄；
- 普通 Windows 文件 HANDLE 不等于可直接监听的 socket；
- 某些特殊设备描述符、regular file 或平台句柄可能不支持可读写通知；
- 跨平台代码应以目标平台测试结果为准，并在 `isValid()`、读写返回值和错误码上做防御。

它也不替代 `QTcpSocket`、`QUdpSocket`、`QLocalSocket` 等高层网络类。已有 Qt socket 类通常已经封装了 notifier、缓冲和协议相关状态。

## 12. 常见错误

### 12.1 把 activated 当作完整消息

就绪只是 I/O 条件，TCP 消息边界需要应用层协议自己处理。

### 12.2 回调中不读取或不处理错误

状态一直保持就绪时，notifier 会反复激活，造成忙循环。读到 EOF、EAGAIN 和真实错误都要明确处理。

### 12.3 永久启用 Write notifier

可写通常长期成立，会不断唤醒事件循环。只有存在待发送数据时启用。

### 12.4 以为 notifier 会关闭 socket

它不拥有底层描述符。资源关闭由 socket/句柄 owner 负责。

### 12.5 外部关闭后继续保留 notifier

关闭或复用描述符前要禁用/销毁 notifier。整数句柄可能被系统快速复用，旧 notifier 不能继续代表新资源。

### 12.6 从错误线程操作

监听在 notifier 所在线程的事件分发器中注册。通过 queued 调用在目标线程启停或替换。

### 12.7 把 `Exception` 当作跨平台统一错误通道

异常条件的底层语义与平台有关。真正错误要看系统 I/O 返回值和错误码。

## 13. 逐项 API 语义

### `QSocketNotifier(Type type, QObject *parent = nullptr)`

按监听类型创建 notifier，初始没有有效 socket。`parent` 只管理 QObject 生命周期，不拥有未来传入的原生描述符。

### `QSocketNotifier(qintptr socket, Type type, QObject *parent = nullptr)`

用 socket/描述符值创建 notifier，并注册对应类型的监听。它不复制、不关闭、不接管该平台资源。

### `~QSocketNotifier()`

销毁 notifier 并解除事件分发器中的监听。底层 socket/描述符仍由调用方负责。

### `setSocket(qintptr socket)`

替换被监听的描述符。调用前后应确认线程归属、描述符有效性和是否需要暂时禁用；不会连接或关闭 socket。

### `socket() const`

返回当前保存的 `qintptr` 描述符值。它只是句柄数值，不代表底层资源一定仍由外部保持打开。

### `type() const`

返回创建时指定的 `Read`、`Write` 或 `Exception` 监听类型。类型不能通过该 API 修改；要换类型，通常创建新的 notifier。

### `isValid() const`

判断当前 notifier 是否持有可供平台事件分发器使用的有效描述符。Qt 6.1 起提供；它不验证协议连接、读写结果或外部 owner 是否仍然正确。

### `isEnabled() const`

返回 notifier 当前是否启用事件通知。启用不保证一定有事件，禁用也不关闭底层资源。

### `setEnabled(bool enable)`

启用或禁用就绪通知。禁用只移除监听，不读取、写入或关闭描述符。对写 notifier 应按待发送缓冲动态设置。

### `activated(QSocketDescriptor socket, Type activationEvent)`

当事件循环报告描述符满足对应条件时发出。现代 Qt 6.11.1 信号携带 `QSocketDescriptor` 和类型；它不表示完整消息，也不代替 I/O 错误处理。

### `event(QEvent *event)`

重载 `QObject::event()` 以处理 socket 激活事件。普通应用应连接 `activated()`，不需要直接调用或重载它。

### `QSocketDescriptor`

这是 `activated()` 使用的非拥有描述符值类型。它可在信号参数、日志或平台适配层中传递，但析构不会关闭底层 socket/句柄。

### `QSocketDescriptor::isValid() const`

在支持该判断的平台上判断描述符值是否为有效哨兵之外的值。它不保证描述符仍处于打开状态，也不保证 QSocketNotifier 能监听该类型资源。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `enum Type { Read, Write, Exception }` | 选择监听可读、可写或异常条件。 | `Exception` 平台差异明显；类型是就绪类别，不是协议错误类别。 |
| 构造 | `QSocketNotifier(Type, QObject *)` | 创建尚未绑定描述符的 notifier。 | parent 管对象生命周期，不拥有原生资源。 |
| 构造 | `QSocketNotifier(qintptr, Type, QObject *)` | 创建并监听给定描述符。 | 不复制或关闭描述符；平台支持的句柄类型有限。 |
| 生命周期 | `~QSocketNotifier()` | 解除监听并销毁 notifier。 | 不关闭底层 socket/句柄。 |
| 绑定 | `setSocket(qintptr)` | 更换监听描述符。 | 先禁用更稳妥；应在 notifier 所属线程调用。 |
| 查询 | `socket()` | 返回当前描述符数值。 | 数值可能已被外部关闭或复用，不能单独证明资源有效。 |
| 查询 | `type()` | 返回监听类型。 | 只读；换类型通常创建新的 notifier。 |
| 状态 | `isValid()` | 判断 notifier 当前描述符是否可用。 | Qt 6.1 起；不等于连接仍建立或读写必成功。 |
| 状态 | `isEnabled()` | 判断是否已启用通知。 | 启用不等于已有数据，禁用不释放资源。 |
| 控制 | `setEnabled(bool)` | 启用或禁用就绪通知。 | 写 notifier 通常按发送队列动态启用，避免忙循环。 |
| 信号 | `activated(QSocketDescriptor, Type)` | 描述符就绪时发出。 | 一次激活不等于一条完整消息；回调中必须实际 I/O。 |
| 事件 | `event(QEvent *)` | 内部处理 socket activation 事件。 | 普通代码连接信号即可，不应直接调用。 |
| 辅助类型 | `QSocketDescriptor` | 跨平台承载原生描述符的非拥有值类型。 | Unix/Windows 底层类型不同；析构不关闭资源。 |
| 辅助类型 | `QSocketDescriptor::isValid()` | 检查描述符值是否为无效哨兵。 | 不保证底层资源仍打开，也不保证平台 notifier 支持。 |

## 15. 一句话总结

`QSocketNotifier` 只把底层描述符的可读、可写或异常状态接入 Qt 事件循环：它不拥有资源、不定义消息边界，也不替你处理错误。读 notifier 要消耗数据，写 notifier 要按需启用，所有操作都要放在有事件循环的正确线程中。
