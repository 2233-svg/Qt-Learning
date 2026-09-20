# Qt QWinEventNotifier：把 Win32 可等待 HANDLE 接入 Qt 事件循环

`QWinEventNotifier` 让 Qt 事件循环异步监视 Windows 的可等待句柄。当关联的 Windows event、process、thread 或 waitable timer 变为 signaled，且 notifier 已启用时，它发射 `activated()` 信号。这样 GUI/Qt 主线程不必自己阻塞在 `WaitForSingleObject()`，仍能继续处理窗口、计时器和 queued signal。

它只在 Windows 提供；非 Windows 平台上类声明都不可用，跨平台代码必须用 `#ifdef Q_OS_WIN` 隔离这一实现，或在更上层抽象出平台后端。

```cpp
#ifdef Q_OS_WIN
#include <QWinEventNotifier>
#include <windows.h>

HANDLE event = CreateEventW(nullptr, TRUE, FALSE, nullptr);
auto *notifier = new QWinEventNotifier(event, this);

connect(notifier, &QWinEventNotifier::activated, this,
        [event](Qt::HANDLE) {
            consumePendingWork();
            ResetEvent(event); // event 是 manual-reset 时必须自行复位
        });

notifier->setEnabled(true);
#endif
```

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QWinEventNotifier>`  
> CMake：`Qt6::Core`  
> 平台：仅 Windows  
> 继承：`QObject -> QWinEventNotifier`

## 它解决什么问题

Windows 原生 API 常用 `HANDLE` 表示同步对象。直接在 Qt 的 GUI 或事件循环线程里写：

```cpp
WaitForSingleObject(handle, INFINITE);
```

会阻塞该线程，窗口无法重绘，Qt 事件也无法分发。`QWinEventNotifier` 将“句柄变成 signaled”转换为 Qt 信号，使后续工作可以按普通 signal/slot 方式组织。

它适合：

- 后台线程通过 `CreateEvent()` 通知主线程有新工作；
- 监视子进程退出的 process handle；
- 监视线程结束的 thread handle；
- 将 waitable timer 与 Qt 事件循环衔接。

它不是 I/O socket notifier，也不把任意 Windows `HANDLE` 变成可读写流。只有 Windows wait functions 能等待的同步对象才适合；文件句柄、pipe 或 overlapped I/O 的具体集成应使用匹配的 Windows/Qt I/O 机制。

## 基本使用模型

1. 用 Windows API 创建或取得一个**可等待且仍有效**的 HANDLE。
2. 在需要接收 Qt 回调的线程创建 `QWinEventNotifier`，该线程必须运行 Qt 事件循环。
3. 连接 `activated()`，在槽中读取/处理实际状态。
4. 根据同步对象类型决定是否手动复位、是否重新启用、何时关闭 HANDLE。
5. 在销毁 notifier 前先停止后续通知；在关闭 HANDLE 前先解除 notifier 对它的监视。

带 HANDLE 的构造函数会立刻启用 notifier 并开始监视。文档仍建议显式控制启用状态，所以生产代码常在完成信号连接后调用一次 `setEnabled(true)`，并在改句柄或关闭流程中明确禁用。

## `activated()` 不会替你消费或复位事件

notifier 只观察 signaled 状态，**不会修改 Windows event 的状态**。若使用 manual-reset event：

```cpp
HANDLE event = CreateEventW(nullptr, TRUE, FALSE, nullptr);
```

事件在 `SetEvent()` 后保持 signaled，直到调用 `ResetEvent()`。若槽函数不复位，它仍处于就绪状态，后续可能持续触发或造成不符合预期的通知节奏。何时复位取决于你的状态模型：

- 先在锁/原子变量中取走全部待处理工作，再 `ResetEvent()`；
- 如果生产者可能在处理期间再次 `SetEvent()`，要设计为不丢工作，例如用队列/计数作为真实状态，而不是只依赖 event 边沿；
- auto-reset event 的复位由 Windows wait 语义处理，但仍需用实际队列或状态判断是否真的有工作。

因此正确模式仍然是“HANDLE 表示可能有事发生，受同步保护的队列/状态才是事实”。不要仅因收到一次 `activated()` 就假设恰好有一条任务。

## 句柄所有权与更换句柄

`QWinEventNotifier` 监视 HANDLE，但不替代 Windows 资源管理。通常，创建 HANDLE 的代码仍负责在正确时机 `CloseHandle()`。不要在 notifier 仍可能等待该 HANDLE 时就关闭它；先禁用或销毁 notifier，再由拥有者关闭句柄。

`setHandle(hEvent)` 会自动注销旧 HANDLE，但有一个关键副作用：**notifier 会被禁用**。更换后必须重新启用：

```cpp
notifier.setEnabled(false);
notifier.setHandle(newHandle);
notifier.setEnabled(true);
```

若忘记最后一步，句柄即使 signaled 也不会触发 `activated()`。`handle()` 仅返回当前登记的 HANDLE，不验证句柄是否仍被系统视为有效。

## QObject 生命周期和线程归属

它是 `QObject`，可以交给 parent 管理。回调依赖 notifier 所在线程的事件循环，因此在 GUI 线程创建时，`activated()` 的直接槽通常运行在 GUI 线程；槽中不要做长时间阻塞工作。耗时处理应交给工作线程或切分为异步步骤。

像其他 QObject 一样，不要从任意线程直接调用 `setHandle()` 或 `setEnabled()`。若 Windows worker 线程需要让 GUI 线程更换监视对象，通过 queued signal 或 `QMetaObject::invokeMethod()` 把操作投递到 notifier 的线程。

销毁时先规划顺序：

1. 停止产生新的 `SetEvent()` / 信号源；
2. 在 notifier 所在线程禁用或销毁 notifier；
3. 等待可能使用该 HANDLE 的并发操作结束；
4. 最后由句柄拥有者 `CloseHandle()`。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QWinEventNotifier(QObject *parent = nullptr)` | 创建未关联 HANDLE 的 notifier | 之后用 `setHandle()` 登记句柄；对象应存在于有 Qt 事件循环的线程。 |
| `QWinEventNotifier(HANDLE hEvent, QObject *parent = nullptr)` | 创建并监视 HANDLE | 构造后默认启用；HANDLE 必须是 Windows 可等待同步对象且在监视期内有效。 |
| `~QWinEventNotifier()` | 停止监视并销毁 QObject | 不负责替调用方关闭 Windows HANDLE；先处理并发访问与句柄寿命。 |
| `setHandle(HANDLE hEvent)` | 解除旧句柄并登记新句柄 | 会自动禁用 notifier；设置后必须 `setEnabled(true)` 才重新接收通知。 |
| `handle()` | 返回当前登记 HANDLE | 仅返回值，不证明句柄尚未被关闭或仍可等待。 |
| `setEnabled(bool enable)` | 启用/禁用监视 | 公共槽；禁用时 signaled 不会产生通知。应在对象所属线程调用。 |
| `isEnabled()` | 查询启用状态 | 只反映 notifier 当前状态，不反映 HANDLE 的 signaled 状态。 |
| `activated(HANDLE hEvent)` | HANDLE signaled 时发射 | private signal，可连接但用户不能 emit；不会自动 `ResetEvent()` 或消费业务状态。 |
| `event(QEvent *)` | Qt 内部事件处理扩展点 | 受保护重写；一般不需要直接重写。 |

## 常见错误

- 在 Linux/macOS 编译未做条件编译的 `QWinEventNotifier` 代码。
- 把任意文件/网络 HANDLE 当成 waitable synchronization object。
- 收到 `activated()` 后忘记处理 manual-reset event 的 `ResetEvent()`。
- 只用 event 作为任务状态，没有队列、计数或原子谓词，导致合并通知时丢工作。
- `setHandle()` 后忘记重新 `setEnabled(true)`。
- notifier 仍在监视时提前 `CloseHandle()`。
- 在 GUI 线程的槽中执行长时间阻塞操作。
- 从其它线程直接改变 notifier 的 handle 或启用状态。

---

### 一句话总结

`QWinEventNotifier` 把 Windows 可等待 HANDLE 的 signaled 状态转换为 Qt 事件循环中的信号；它不拥有句柄、不复位 manual-reset event，且更换 HANDLE 后必须重新启用。
