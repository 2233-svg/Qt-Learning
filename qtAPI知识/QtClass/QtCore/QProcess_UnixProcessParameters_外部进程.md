# QProcess::UnixProcessParameters：以 Qt 支持的方式配置 Unix 子进程

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.6  
> 头文件：`#include <QProcess>`  
> 平台：仅 Unix，包括 macOS  
> 关联 API：`QProcess::setUnixProcessParameters()`

## 它解决什么问题

`QProcess::UnixProcessParameters` 是在 Unix 上启动子进程前交给 `QProcess` 的额外配置。它用于表达一组常见而容易出错的 POSIX 启动要求，例如关闭多余文件描述符、重置信号处理、建立新会话、脱离控制终端、放弃保留权限或禁止生成 core dump。

它解决的是一个很实际的问题：父进程的运行环境并不天然适合子进程继承。长生命周期 GUI、服务进程、测试框架和特权启动器都可能打开许多 fd、改变信号处理或带有有效 UID/GID；不加处理地 `fork`/`exec` 会把这些状态意外带给子进程。

与 `setChildProcessModifier()` 相比，这个结构体优先适合 Qt 已知的标准需求。Qt 可以处理平台差异、采用可用优化；若这些配置对应的系统调用失败，`QProcess` 会以 `FailedToStart` 报错。自定义 child modifier 则不能像普通回调一样自然报告失败。

## 最小用法：防止文件描述符泄漏

```cpp
#include <QProcess>

QProcess process;

QProcess::UnixProcessParameters params;
params.flags = QProcess::UnixProcessFlag::CloseFileDescriptors;
params.lowestFileDescriptorToClose = 3;

process.setUnixProcessParameters(params);
process.start("/usr/bin/env", {"sh", "-c", "exec worker"});
```

设置 `CloseFileDescriptors` 后，Qt 会在执行目标程序前关闭编号不低于阈值的开放文件描述符。`stdin`、`stdout`、`stderr`（0、1、2）永远不会被此标志关闭；将阈值设为 `3` 是“保留标准流，关闭其余继承 fd”的常见选择。

必须在 `start()` 前设置。配置应用于下一次启动的子进程，不会改动父进程本身。

## 结构体字段

Qt 6.11.1 中该结构体只有两个公开配置字段：

| 字段 | 默认值 | 作用 |
| --- | --- | --- |
| `flags` | 空 flags | `QProcess::UnixProcessFlags` 的按位组合，指定要对孩子进程执行的调整。 |
| `lowestFileDescriptorToClose` | `0` | 仅对 `CloseFileDescriptors` 有意义；低于此值的 fd 保留，0/1/2 始终保留。 |

头文件中还有 `_reserved` 字段用于 ABI 兼容，不是应用程序 API。不要写入、序列化、比较或依赖它。

如果只需要 flags，可直接使用简化重载：

```cpp
process.setUnixProcessParameters(
    QProcess::UnixProcessFlag::DisableCoreDumps);
```

`unixProcessParameters()` 返回当前已配置的副本；默认值等价于默认构造的 `UnixProcessParameters`。

## UnixProcessFlag 逐项语义

| 标志 | 版本 | 子进程效果 | 关键边界 |
| --- | --- | --- | --- |
| `ResetSignalHandlers` | 6.6 | 将 Unix 信号处理恢复为默认 `SIG_DFL` | 用于防止父进程忽略或自定义的信号语义泄漏到子进程。 |
| `IgnoreSigPipe` | 6.6 | 强制把 `SIGPIPE` 设为 `SIG_IGN` | 即使同时设了 `ResetSignalHandlers` 也会忽略 `SIGPIPE`；关闭 QProcess 读取通道后，子进程写 stdout/stderr 会失败而不被 SIGPIPE 立即终止。 |
| `CloseFileDescriptors` | 6.6 | 关闭阈值以上的开放 fd | 防止 socket、日志、锁或管道意外继承；0、1、2 不会被关闭。 |
| `UseVFork` | 6.6 | 请求 Qt 使用 `vfork(2)` | 只在 child modifier 对 vfork 安全时使用；Qt 不保证一定采用 vfork。 |
| `CreateNewSession` | 6.7 | 调用 `setsid(2)` 建立新会话 | 是脱离会话/守护化的一步，不等于完整 daemon 化。 |
| `DisconnectControllingTerminal` | 6.7 | 尝试断开控制终端 | 某些系统要求它已是会话 leader，因此常与 `CreateNewSession` 一起使用。 |
| `ResetIds` | 6.7 | 清除保留的有效 UID/GID 权限 | 对 setuid/setgid 父进程尤其重要；会降低孩子权限，不能当作通用 sandbox。 |
| `DisableCoreDumps` | 6.9 | 将子进程 core dump 软限制设为零 | 不改变崩溃状态；子进程若可把限制提升回硬限制，仍可能重新开启。 |

`UnixProcessFlags` 是 `QFlags<UnixProcessFlag>`，可组合多个标志：

```cpp
QProcess::UnixProcessParameters params;
params.flags = QProcess::UnixProcessFlag::CloseFileDescriptors
             | QProcess::UnixProcessFlag::ResetSignalHandlers
             | QProcess::UnixProcessFlag::DisableCoreDumps;
params.lowestFileDescriptorToClose = 3;
```

## 与 setChildProcessModifier() 的关系

`setChildProcessModifier()` 提供更自由的 Unix 钩子：它在子进程 `fork()` 或 `vfork()` 之后、Qt 配好标准 fd 之后、`execve()` 之前执行。适用于 `chroot`、`setuid`、`umask` 等此结构体未覆盖的操作。

两者同时设置时，**child modifier 先运行，随后才应用 `UnixProcessParameters`**。这会影响设计：

- modifier 中创建或保留的 fd，可能随后被 `CloseFileDescriptors` 关闭；
- modifier 设置的信号处理，可能随后被 `ResetSignalHandlers` 覆盖；
- `UseVFork` 只应在 modifier 确实 vfork 安全时启用。

所谓 vfork 安全，意味着 modifier 不修改非局部状态，不经由所调用函数修改共享状态，也不尝试和父进程通信。若不确定，绝不要声明 `UseVFork`；性能收益不值得换取未定义或难复现的启动问题。

## 实际场景

### 为工作进程关闭泄漏的继承资源

服务或测试宿主常同时持有监听 socket、数据库连接、日志文件和线程通信管道。让工作进程继承它们，可能导致父进程关闭资源后端口仍无法释放，或使 EOF 永远不出现。

```cpp
QProcess worker;

QProcess::UnixProcessParameters params;
params.flags = QProcess::UnixProcessFlag::CloseFileDescriptors
             | QProcess::UnixProcessFlag::ResetSignalHandlers;
params.lowestFileDescriptorToClose = 3;

worker.setUnixProcessParameters(params);
worker.start("/opt/acme/bin/worker", {"--job", jobId});
```

### 启动不需要诊断文件的短命测试工具

```cpp
QProcess testProcess;
testProcess.setUnixProcessParameters(
    QProcess::UnixProcessFlag::DisableCoreDumps);
testProcess.start(testBinary, arguments);
```

这只抑制 core 文件，不会掩盖崩溃：仍应检查 `finished()` 的 `exitStatus`、退出码与标准错误输出。

## 生命周期、错误处理与线程

`UnixProcessParameters` 本身是值类型，复制配置没有子进程副作用；副作用发生在 `QProcess::start()` 创建孩子时。它只在 Unix 可用，跨平台项目需要使用平台条件编译或提供平台无关的替代策略。

调用 `setUnixProcessParameters()` 后，`QProcess` 会在启动过程中执行相关操作。若 Qt 代表你执行的系统操作失败，进程进入 `QProcess::FailedToStart` 状态。应连接并检查：

```cpp
QObject::connect(&process, &QProcess::errorOccurred,
                 [](QProcess::ProcessError error) {
    if (error == QProcess::FailedToStart) {
        // 记录 errorString()，不要把“未启动”当作子程序退出。
    }
});
```

`QProcess` 是 `QObject`，必须遵守线程亲和性：配置和启动应在它所属线程进行，避免多线程同时更改同一个 `QProcess` 的设置。不要因为 `UnixProcessParameters` 是值类型就假定围绕它的 `QProcess` 操作可并发。

## 常见错误

### 以为 CloseFileDescriptors 会关闭标准流

不会。0、1、2 始终保留。若要重定向或关闭子进程的标准流，使用 `QProcess` 的标准输入输出文件、通道模式或平台特定设计。

### 忘记阈值的含义

阈值以下的 fd 会保留。若应用把重要资源放在低编号 fd，需明确判断它是否应被继承；不能只“打开标志”就认为全部非标准 fd 都已关闭。

### 盲目启用 UseVFork

此标志是对 Qt 的安全承诺，不是普通性能开关。自定义 modifier 中使用 Qt、堆分配、日志、锁或与父进程同步，都可能不满足 vfork 安全条件。

### 把建立新会话当成完整安全隔离

`CreateNewSession` 只改变会话关系；不限制文件系统、网络、权限、资源或系统调用。安全 sandbox 仍需要专门的权限模型、命名空间、seccomp、容器或平台机制。

### 依赖新标志却未检查最低 Qt 版本

结构体和基础 API 自 Qt 6.6 可用；`CreateNewSession`、`DisconnectControllingTerminal`、`ResetIds` 自 6.7，`DisableCoreDumps` 自 6.9。支持较早 Qt 时必须条件编译或降级。

## API 速查表

| API / 字段 | 作用 | 语义与边界 |
| --- | --- | --- |
| `QProcess::UnixProcessParameters` | 保存 Unix 子进程额外配置 | Qt 6.6 起，仅 Unix；默认无额外调整。 |
| `flags` | 组合 `UnixProcessFlag` | 用 `QFlags` 按位组合；仅影响孩子进程。 |
| `lowestFileDescriptorToClose` | fd 关闭阈值 | 仅在 `CloseFileDescriptors` 时有效；0/1/2 永不关闭。 |
| `setUnixProcessParameters(params)` | 设置完整配置 | 在 `start()` 前调用；失败可能导致 `FailedToStart`。 |
| `setUnixProcessParameters(flagsOnly)` | 只设置 flags | 等价于只填 `flags` 的完整配置。 |
| `unixProcessParameters()` | 读取当前配置副本 | 默认等价于默认构造参数。 |
| `ResetSignalHandlers` | 恢复默认信号处理 | 避免父进程 handler 影响孩子。 |
| `IgnoreSigPipe` | 忽略 `SIGPIPE` | 写入关闭管道会失败而不是让孩子被 SIGPIPE 终止。 |
| `CloseFileDescriptors` | 关闭额外继承 fd | 防泄漏；结合阈值使用。 |
| `UseVFork` | 请求 vfork 启动 | 仅当 child modifier 严格 vfork 安全时使用；不保证生效。 |
| `CreateNewSession` | 建立新会话 | Qt 6.7 起；是守护化步骤，不是完整隔离。 |
| `DisconnectControllingTerminal` | 断开控制终端 | Qt 6.7 起；某些系统还需新会话。 |
| `ResetIds` | 放弃有效 UID/GID | Qt 6.7 起；降低孩子权限，不是 sandbox。 |
| `DisableCoreDumps` | 禁止默认 core dump | Qt 6.9 起；仍要处理崩溃状态。 |
| `setChildProcessModifier()` | 提供自定义 fork/vfork 后钩子 | 与本参数同时使用时先执行 modifier，后应用这些参数。 |

一句话记忆：优先把标准 Unix 启动需求放进 `UnixProcessParameters`，让 Qt 负责跨平台差异与失败反馈；只有结构体覆盖不了的需求才使用更危险的 child modifier。
