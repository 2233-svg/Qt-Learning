# QTcpSocketWrapper：把一次 TCP 连接写入包装成任务

> Qt 6.11.1 · `#include <qtcpsocketwrappertask.h>` · 模块：`Qt6::TaskTree` · 继承：`QObject`

`QTcpSocketWrapper` 是围绕 `QTcpSocket` 的轻量任务包装器。它在 `start()` 时创建 socket，连接到指定地址和端口，并可在连接建立后自动写入一段数据，最后以 `DoneResult` 报告成功或失败。

## 实际使用场景

它适合在 TaskTree recipe 中做一次简单的 TCP 探测、发送命令、写入短消息，或作为更大流程里的“通知某个本地服务”步骤。配置对象本身不持有长期 socket；真正的 `QTcpSocket` 只在运行期间存在。

如果需要长连接、持续读写协议、心跳重连或复杂状态机，建议写专门的 task，而不是把所有逻辑塞进这个 wrapper。

## 生命周期边界

`setAddress()`、`setPort()`、`setData()` 应在 `start()` 前设置。`socket()` 在未启动和完成后返回 `nullptr`；安全访问窗口是 `started()` 发出之后到 `done()` 发出之前。`done()` 后 wrapper 会删除内部 socket。析构 wrapper 时如果 socket 仍在运行，会 abort。

`started()` 表示 socket 已连接；如果 `data` 非空，会在连接建立后自动写入。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QTcpSocketWrapper(QObject *parent = nullptr)` | 构造 TCP 包装器。 |
| `~QTcpSocketWrapper()` | 若内部 socket 仍运行，会中止它。 |
| `setAddress(const QHostAddress &address)` | 设置连接目标地址；应在 `start()` 前调用。 |
| `setPort(quint16 port)` | 设置连接目标端口；应在 `start()` 前调用。 |
| `setData(const QByteArray &data)` | 设置连接成功后自动写入的数据；空数据表示不自动写。 |
| `start()` | 创建 socket 并发起连接。 |
| `socket() const` | 返回运行中的 socket；未启动或完成后为 `nullptr`。 |
| `started()` | socket 成功连接后发出。 |
| `done(DoneResult)` | socket 任务完成后发出，表示成功或错误。 |
| `QTcpSocketWrapperTask` | `QCustomTask<QTcpSocketWrapper>`，用于 recipe。 |
