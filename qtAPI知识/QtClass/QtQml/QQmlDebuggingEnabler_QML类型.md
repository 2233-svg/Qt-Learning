# QQmlDebuggingEnabler：手动开启 QML 调试、检查器或性能分析连接

> Qt 6.11.1 · `#include <QQmlDebuggingEnabler>` · 模块：`Qt6::Qml`

`QQmlDebuggingEnabler` 是一组静态函数，用于手工启用 QML 调试和 profiling，并启动本地 socket、TCP 或自定义插件形式的 debug connector。它解决的是嵌入式启动器、专用测试工具或需要自行控制连接方式的应用，不必完全依赖 `-qmljsdebugger` 命令行参数。

正常应用通常只需在构建时启用 `QT_ENABLE_QML_DEBUG`（qmake：`CONFIG += qml_debug`），并让运行时参数完成连接。只有需要自定义启动过程时才直接调用本类。

## 基本路径和安全边界

```cpp
#include <QQmlDebuggingEnabler>

QQmlDebuggingEnabler::enableDebugging(true);
const bool started = QQmlDebuggingEnabler::startTcpDebugServer(
    3768, QQmlDebuggingEnabler::DoNotWaitForClient, u"127.0.0.1"_s);
```

必须先调用 `enableDebugging()`（或通过构建选项使 Qt 自动调用），连接器才会启动。它只影响**之后创建**的 QML engine。

调试服务能暂停 QML/JavaScript、设断点、求值表达式、检查 Qt Quick 场景或采集性能数据，因此只能在受信任环境开启。`startTcpDebugServer()` 未指定 `hostName` 时监听所有可用网络接口；开发机之外应明确绑定 loopback 或受控地址，避免将调试入口暴露到网络。

## 连接器与启动模式

一个进程只能启动一个 debug connector。若命令行 `-qmljsdebugger` 已经启动连接器，手动启动函数会返回 `false`。`connectToLocalDebugger()` 连接等待在本地 socket 的调试器，`startTcpDebugServer()` 自己监听 TCP 端口，`startDebugConnector()` 根据插件名和配置创建自定义连接器。

`DoNotWaitForClient` 让 engine 正常启动；`WaitForClient` 会在 debug 服务连接期间暂停刚启动的 QML engine，适合要断在启动代码的场景，也意味着生产启动流程可能无期限等待调试客户端。

## 服务集合与性能

`debuggerServices()`、`inspectorServices()`、`profilerServices()`、`nativeDebuggerServices()` 返回 Qt 默认提供的插件键。`setServices()` 必须在 debug connector 启用前调用，用于限制实际加载的服务集合。

性能分析时可以只保留 profiler 服务。调试器服务会让连接到它的 JavaScript engine 使用解释模式、关闭 JIT，这会显著改变性能特征；“带调试器跑出的性能数据”未必代表正常发布构建。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `enableDebugging(printWarning)` | 启用调试/分析能力 | 必须在启动 connector 前完成；建议在安全环境显示警告。 |
| `StartMode::DoNotWaitForClient` | 不等待客户端 | QML engine 正常启动。 |
| `StartMode::WaitForClient` | 等待客户端连接 | 可调试启动代码，但会阻塞 engine 启动。 |
| `startTcpDebugServer(port, mode, host)` | 启动 TCP connector | 未给 host 时监听所有接口；一次只能启动一个 connector。 |
| `connectToLocalDebugger(socket, mode)` | 连接本地 socket 调试器 | 对之后创建的 QML engine 生效；已存在 connector 时失败。 |
| `startDebugConnector(plugin, config)` | 启动自定义 connector 插件 | 配置键语义由插件决定；返回是否新启动成功。 |
| `setServices(services)` | 限制可用调试服务 | 必须早于 connector 启用；可减少性能干扰和暴露面。 |
| `debuggerServices()` | 查询默认调试服务键 | 包含断点、暂停、表达式求值等服务。 |
| `inspectorServices()` | 查询默认检查器服务键 | 面向 Qt Quick 可视化检查。 |
| `profilerServices()` | 查询默认性能服务键 | 采集 QML/JS 和场景图性能。 |
| `nativeDebuggerServices()` | 查询原生调试协作服务键 | 由原生调试器通过进程内存交互。 |

这个类型的正确用法是“让开发工具连接到受控的应用实例”。它不是发布版功能开关，也不应成为应用公开的远程管理接口。
