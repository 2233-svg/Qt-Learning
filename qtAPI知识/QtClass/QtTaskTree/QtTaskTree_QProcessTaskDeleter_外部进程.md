# QProcessTaskDeleter：安全清理可能仍在运行的 QProcess

> Qt 6.11.1 · `#include <qprocesstask.h>` · 模块：`Qt6::TaskTree`

`QProcessTaskDeleter` 是 `QProcessTask` 使用的自定义 deleter。它解决的不是“如何启动进程”，而是“任务取消或销毁时，正在运行的 `QProcess` 不要在当前线程长时间阻塞析构”。

## 为什么需要它

直接删除正在运行的 `QProcess` 可能导致调用线程被等待进程结束拖住。TaskTree 的取消路径经常发生在 UI 或主控制线程上，如果这里阻塞，界面和后续清理都会变得很差。`QProcessTaskDeleter` 会把运行中的进程移到单独线程里清理。

清理策略是先调用 `terminate()` 并等待 500 ms；如果仍未结束，再调用 `kill()`。这样当前线程能尽快返回，而真正可能阻塞的等待被推迟。

## 应用退出同步

被推迟清理的进程可能在后台线程里继续收尾。因此应用退出时应从主线程调用 `QProcessTaskDeleter::syncAll()`，等待所有仍在清理的进程结束。这个调用可能阻塞，但阻塞点被集中到了退出阶段。

## API 速查表

| API | 语义与边界 |
|---|---|
| `operator()(QProcess *process) const` | 删除进程；未运行则直接删除，运行中则移到单独线程清理。 |
| `terminate()` 阶段 | 对运行中进程先温和终止，等待约 500 ms。 |
| `kill()` 阶段 | 超时仍未结束时强制杀死。 |
| `syncAll()` | 应用退出时从主线程调用，等待所有延迟清理的进程完成。 |
| 阻塞位置 | deleter 调用尽量快速返回；`syncAll()` 可能阻塞。 |
| `QProcessTask` | `QCustomTask<QProcess, QProcessTaskAdapter, QProcessTaskDeleter>`，使用该 deleter。 |
