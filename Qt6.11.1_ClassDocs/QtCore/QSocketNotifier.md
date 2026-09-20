# QSocketNotifier
> Qt 6.11.1 · Qt Core · 来自 `QSocketNotifier`

## 作用定位
`QSocketNotifier` 把原生 socket 或文件描述符的可读、可写、异常状态接入 Qt 事件循环。它不负责读写数据，只在描述符状态变化时发出 `activated`。

## API 速查
| API | 是做什么的 |
|---|---|
| `QSocketNotifier(socket, type)` | 监听指定描述符的读、写或异常事件。 |
| `setEnabled()` | 开关通知，避免重复触发或临时屏蔽。 |
| `isEnabled()` | 查询是否正在监听。 |
| `socket()` | 取得正在监听的描述符。 |
| `type()` | 查询监听类型。 |
| `activated` | 描述符状态满足条件时发出。 |

## 使用场景
读取非 Qt 创建的管道、Unix fd 或平台 socket 时，将 readiness 转给 Qt 主循环处理。

```cpp
auto *notifier = new QSocketNotifier(fd, QSocketNotifier::Read, this);
connect(notifier, &QSocketNotifier::activated, this, [=] {
    notifier->setEnabled(false);
    drainFd(fd);
    notifier->setEnabled(true);
});
```

## 常见坑与经验
- 回调里应尽量读到 `EAGAIN` 或没有更多数据，否则事件可能持续触发。
- 描述符关闭前先禁用或销毁 notifier，避免事件循环拿到失效 fd。
- notifier 必须运行在线程事件循环中；跨线程移动时确保 fd 和对象归属清楚。
- 对普通 Qt 网络通信，优先用 `QTcpSocket` 等高层类。

## 知识点覆盖
事件循环、文件描述符、readiness 通知、非阻塞 I/O、线程归属、平台差异。
