# QtTaskTree::ExecutableItem
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::ExecutableItem`

## 作用定位

`ExecutableItem` 是 TaskTree 中“可以被执行并产生结果”的 recipe 节点。`Group`、`Forever`、`QCustomTask`、`QSyncTask` 等都建立在它之上。它还提供组合修饰器：接受信号、取消信号、超时、日志，以及 `&&`、`||`、`!` 这样的结果组合语义。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 基类：`GroupItem`
- 派生：`Group`、`Forever`、`QCustomTask`、`QSyncTask`

## API 速查

| API | 说明 |
| --- | --- |
| `withAccept(getter)` | 为任务附加“接受/通过”信号，信号到达时按成功路径推进。 |
| `withCancel(getter, postCancelRecipe)` | 为任务附加取消信号，可指定取消后补偿 recipe。 |
| `withTimeout(timeout, handler)` | 给任务加超时保护，超时后按失败/取消语义结束并可执行 handler。 |
| `withLog(logName)` | 为执行项加日志名，便于排查任务树流程。 |
| `operator!` | 反转执行项的成功/失败结果。 |
| `operator&&` | 组合“前项成功才继续/整体成功”语义。 |
| `operator||` | 组合“前项失败才走备用项/任一成功”语义。 |

## 使用场景

- 给网络请求、进程、线程函数加统一超时。
- 把取消按钮、外部信号或对象生命周期接入任务树。
- 用逻辑运算符表达 fallback、短路和结果反转。

## 常见坑与经验
- `withTimeout()` 不是杀线程魔法；它结束 TaskTree 节点，但底层异步资源仍要自己支持取消/清理。
- `&&` 和 `||` 是任务结果组合，不是 C++ 表达式立即求值。
- `withCancel()` 的补偿 recipe 要保持轻量和幂等，因为它通常在异常路径执行。
- 日志名要能对应业务步骤，比类名更有用。

## 知识点覆盖

- 可执行任务节点
- 结果传播与短路组合
- 超时、取消、接受信号
- 异步流程可观测性
