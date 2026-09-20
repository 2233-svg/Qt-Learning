# QtTaskTree::QThreadFunctionBase
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QThreadFunctionBase`

## 作用定位

`QThreadFunctionBase` 是线程函数任务的公共基类，提供全局同步入口 `syncAll()`。它服务于 `QThreadFunction` 的“延迟同步”机制，确保应用退出前仍能等待已登记的后台 future。

## 类说明

- 头文件：`#include <qthreadfunctiontask.h>`
- 派生：`QThreadFunction`

## API 速查

| API | 说明 |
| --- | --- |
| `syncAll()` | 等待全局登记的线程函数任务完成，常用于应用退出收尾。 |

## 使用场景

- 程序关闭前等待自动延迟同步的线程函数。
- 测试中统一收尾后台任务。

## 常见坑与经验

- `syncAll()` 会阻塞，不能随便放在 UI 热路径。
- 它只处理该机制登记的 future，不会等待所有 QThreadPool 任务。
- 退出阶段调用要避免等待的任务反过来依赖已经销毁的 QObject。

## 知识点覆盖

- 线程函数延迟同步
- 应用退出收尾
- QFuture 等待边界
