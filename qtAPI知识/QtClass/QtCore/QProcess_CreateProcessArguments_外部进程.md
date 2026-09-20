# QProcess::CreateProcessArguments：在 Windows 上微调底层进程创建参数

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QProcess>`  
> 平台：仅 Windows  
> 关联 API：`QProcess::setCreateProcessArgumentsModifier()`

## 它解决什么问题

`QProcess::CreateProcessArguments` 是 Qt 在 Windows 上准备调用 Win32 `CreateProcess()` 时交给回调函数的一组原始参数。它不是常规配置对象，也不是让应用自行构造后传入 `QProcess` 的类型；它是 Qt 创建子进程过程中的**短暂参数视图**。

普通情况下，使用 `QProcess::setProgram()`、`setArguments()`、`setProcessEnvironment()`、标准输入输出重定向等跨平台 API 就够了。只有确实需要改变 `CreateProcess()` 的特定行为时，才设置 `CreateProcessArgumentModifier` 回调并在回调中检查/修改这个结构体。

典型场景：

- 为控制台子进程增加 `CREATE_NEW_CONSOLE`；
- 通过 `STARTUPINFO` 调整 Windows 启动行为；
- 对必须接收特殊原生命令行形式的外部程序做最后一层兼容处理；
- 集成必须使用某些 Win32 创建标志的旧工具。

这是一条 Windows 专用逃生通道，不是通用启动方式。若业务可以用标准 `QProcess` 配置表达，应优先使用标准 API，代码才更容易跨平台、测试和维护。

## 基本用法：在 start() 前注册回调

```cpp
#include <QProcess>
#include <windows.h>

QProcess process;

process.setCreateProcessArgumentsModifier(
    [](QProcess::CreateProcessArguments *args) {
        args->flags |= CREATE_NEW_CONSOLE;
    });

process.start("C:\\Windows\\System32\\cmd.exe", {"/k", "echo child"});
```

回调会在 Qt 调用 `CreateProcess()` 前获得指向该结构体的指针；回调返回后，其中成员会被用于实际的 Win32 调用。配置必须在 `start()` 前完成。传入空的 `QProcess::CreateProcessArgumentModifier()` 可移除先前设置的回调。

```cpp
process.setCreateProcessArgumentsModifier(
    QProcess::CreateProcessArgumentModifier());
```

## 生命周期与所有权：只在回调中使用

这是最重要的边界：

- `CreateProcessArguments *` 只在 modifier 回调执行期间可用；
- 不要把该指针、其中的 `wchar_t *`、`STARTUPINFO *` 或 `PROCESS_INFORMATION *` 保存到回调外；
- 这些成员大多指向 Qt 或 Windows 调用过程管理的存储，回调不拥有它们；
- 不要释放 Qt 提供的字符串、环境块、属性结构或启动信息；
- 若替换某个指针字段，必须自行保证其内存直到 `CreateProcess()` 完成调用前始终有效；通常应避免替换指针，优先改标志或既有结构成员。

回调不是异步通知，也不是子进程中执行的代码；它运行在发起 `QProcess::start()` 的调用路径中，负责最后一次修改 Windows 创建参数。不要在这里执行耗时工作、启动嵌套事件循环或访问会引起复杂重入的 UI/进程状态。

## 结构体字段：与 CreateProcess 的参数一一对应

Qt 6.11.1 头文件中该结构体包含下列字段：

| 字段 | 对应 Win32 概念 | 使用重点 |
| --- | --- | --- |
| `applicationName` | `lpApplicationName` | 宽字符可执行文件名指针；通常让 Qt 管理。 |
| `arguments` | `lpCommandLine` | 可写的宽字符命令行缓冲区；Windows 命令行解析有程序差异，不要把它当作跨平台参数列表。 |
| `processAttributes` | `lpProcessAttributes` | 进程安全属性；空或自定义值都会影响句柄继承与安全描述符。 |
| `threadAttributes` | `lpThreadAttributes` | 初始线程安全属性；同样属于低层 Win32 语义。 |
| `inheritHandles` | `bInheritHandles` | 控制可继承句柄是否被子进程继承；设置不当可能泄露文件、管道或同步对象句柄。 |
| `flags` | `dwCreationFlags` | 进程创建标志，如 `CREATE_NEW_CONSOLE`；组合时使用按位或。 |
| `environment` | `lpEnvironment` | Windows 环境块；其格式与所有权规则由 Win32 定义。 |
| `currentDirectory` | `lpCurrentDirectory` | 子进程工作目录的宽字符路径。 |
| `startupInfo` | `lpStartupInfo` | `STARTUPINFO` 指针；可调整窗口/控制台启动细节，但可能影响 Qt 已配好的 I/O。 |
| `processInformation` | `lpProcessInformation` | `CreateProcess()` 写入的进程和初始线程信息；不要替换或关闭其中句柄，交由 Qt 的启动流程处理。 |

不要假定此结构体的二进制布局是长期扩展点。访问名称明确的公开字段可以，但不要依赖大小、预留内存或把它复制给其他代码。

## 与 QProcess 通道配置的冲突

`QProcess` 会通过 `STARTUPINFO`、句柄继承和管道设置实现 `SeparateChannels`、文件重定向、`setStandardOutputProcess()` 等功能。随意改动这些字段容易出现很隐蔽的后果：

- 清掉或覆盖 Qt 需要的 `STARTF_USESTDHANDLES`，导致标准输出/错误输出不再进入 Qt 管道；
- 改 `inheritHandles`，导致子进程失去必要管道句柄，或继承了不该继承的句柄；
- 改命令行缓冲区，导致实际参数与 `QProcess::arguments()` 不一致；
- 改环境块或当前目录，导致子进程加载 DLL、查找配置和脚本相对路径发生变化。

因此，回调应只修改实现目标所需的最小字段，并配合 `errorOccurred()`、`started()`、`finished()`、`readAllStandardError()` 验证实际启动结果。`started()` 只表示操作系统成功创建了进程，不保证该程序已经成功初始化。

## 真实场景：独立控制台窗口

Qt 文档示例展示了为控制台子进程创建新控制台，并调整控制台填充属性。实际项目中通常只需要创建独立控制台：

```cpp
#include <QProcess>
#include <windows.h>

void startDiagnosticConsole()
{
    auto *process = new QProcess;
    process->setCreateProcessArgumentsModifier(
        [](QProcess::CreateProcessArguments *args) {
            args->flags |= CREATE_NEW_CONSOLE;
        });

    process->start("C:\\Windows\\System32\\cmd.exe",
                   {"/k", "title Diagnostic Child"});
}
```

这段代码只应在 Windows 构建分支中编译。若是 GUI 程序，额外控制台窗口是否合适还取决于产品体验；不要为“看见日志”而在正式程序中无条件创建控制台。

## 常见错误

### 用它修复普通参数转义问题

先使用 `start(program, QStringList)`。Windows 下 Qt 会按 `CommandLineToArgvW()` 兼容规则组合参数。只有目标程序刻意使用不同规则（例如 `cmd.exe` 和批处理脚本）时，才考虑 `setNativeArguments()` 或 modifier。

### 把回调参数缓存起来

回调返回后指针和内部存储均不再可假定有效。需要记录信息时，复制自己需要的值；不要保存原始指针。

### 手工接管 Qt 的 I/O 管道

为改变一个创建标志而重设 `startupInfo` 或 `inheritHandles`，可能让 `QProcess` 的标准流配置失效。优先只增减目标标志位。

### 忽略 Windows 专用性

该结构体、`CreateProcessArgumentModifier` 和 `setCreateProcessArgumentsModifier()` 仅在 Windows 可用。公共跨平台头文件和调用点需要用平台条件编译隔离。

## API 速查表

| API / 字段 | 作用 | 语义与边界 |
| --- | --- | --- |
| `QProcess::CreateProcessArguments` | 暴露一次 Win32 创建调用的参数 | 仅 Windows；只作为 modifier 回调的临时参数。 |
| `QProcess::CreateProcessArgumentModifier` | 回调类型 | 签名为 `std::function<void(CreateProcessArguments *)>`；回调后参数即用于 `CreateProcess()`。 |
| `setCreateProcessArgumentsModifier(modifier)` | 注册/替换回调 | 必须在 `start()` 前设置；传入空函数对象可清除。 |
| `createProcessArgumentsModifier()` | 读取已注册回调 | 仅返回之前设置的 modifier，不触发进程创建。 |
| `applicationName` | 可执行文件名参数 | 非拥有宽字符指针；一般不改。 |
| `arguments` | 原生命令行参数 | 可写缓冲区但不应越界或保存；参数语义由目标程序决定。 |
| `processAttributes`, `threadAttributes` | 安全属性 | Win32 专用；错误配置影响安全和句柄继承。 |
| `inheritHandles` | 是否继承句柄 | 可能造成管道失效或句柄泄露。 |
| `flags` | 创建标志位 | 常见安全修改点；用 `|=` 保留 Qt 已设置的标志。 |
| `environment`, `currentDirectory` | 环境块与工作目录 | 影响 DLL 搜索、配置和相对路径；遵守 Win32 内存/编码规则。 |
| `startupInfo` | 启动信息 | 改动可能破坏 `QProcess` 标准流和窗口配置。 |
| `processInformation` | 创建输出信息 | 由 `CreateProcess()` 写入；不要接管其句柄生命周期。 |

一句话记忆：`CreateProcessArguments` 是 Qt 在 Windows 调用 `CreateProcess()` 前给你的短暂低层视图，最稳妥的做法是只在回调中做最小、可验证的修改。
