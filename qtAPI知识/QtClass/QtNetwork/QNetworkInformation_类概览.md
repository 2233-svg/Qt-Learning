# QNetworkInformation：系统网络状态与计费网络提示

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkInformation>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 类型：由 Qt 管理的单例 `QObject`

## 它解决什么问题

`QNetworkInformation` 通过平台 backend 提供系统报告的网络状态：可达性、强制门户、当前传输介质和是否按流量计费。它让应用能在网络状态变化时调整同步、上传和用户提示策略，而不必为每个平台各自接系统 API。

它提供的是操作系统或插件的“网络环境信号”，不是对特定 URL、DNS、代理、VPN 或业务服务的连通性证明。即使 `reachability()` 返回 `Online`，目标 API 仍可能因 DNS、TLS、认证、代理、路由或防火墙失败。

## 实际使用场景

- 网络恢复后重新尝试因临时网络错误失败的同步。
- `isMetered()` 为真时暂停大日志、媒体预取或后台上传。
- 检测到 captive portal 后引导用户完成 Wi-Fi 认证。
- 根据 Wi-Fi、蜂窝、以太网调整非关键任务的调度优先级。

不要把它作为“请求前预检”来跳过实际连接。正确方式是：可达性用于改善体验和退避策略，真实请求仍应发起，并依据 `QNetworkReply` 的实际结果处理失败。

## 先加载 backend，再取单例

`instance()` 不会隐式创建 backend；在首次成功加载前返回 `nullptr`。普通应用优先加载平台默认 backend：

```cpp
if (!QNetworkInformation::loadDefaultBackend()) {
    qWarning() << "Network-information backend unavailable";
    return;
}

auto *networkInfo = QNetworkInformation::instance();
connect(networkInfo, &QNetworkInformation::reachabilityChanged,
        this, &Controller::onReachabilityChanged);
connect(networkInfo, &QNetworkInformation::isMeteredChanged,
        this, &Controller::onMeteredChanged);
```

该对象从成功加载起存活到 `QCoreApplication` 销毁。首次加载必须在创建 `QCoreApplication` 的同一线程进行，因为 backend 也会在这个线程析构，某些平台实现依赖这种线程归属。

若销毁并重新创建 `QCoreApplication`，必须重新加载 backend。不同 `load...()` 函数不是用来在运行中反复切换 backend 的：已有 backend 时，加载其他 backend 通常失败或直接保持已有实例。

## 可达性如何解释

| `Reachability` | 正确理解 |
| --- | --- |
| `Unknown` | 系统尚未确认，或 backend 不支持该能力；不能当成“离线”。 |
| `Disconnected` | 系统认为可能完全无连接；仍不排除瞬时变化或平台误报。 |
| `Local` | 可能只能访问本地网络设备。 |
| `Site` | 可能可访问本地子网或内网。 |
| `Online` | 系统认为可访问互联网，但不是目标服务的保证。 |

需求应与目标匹配：访问局域网设备时 `Local` / `Site` 可能已足够；访问公网服务通常需要 `Online`。Linux 和 Windows 才支持较细的 `Local`、`Site` 粒度；Android 和 Apple 平台通常只能报告 Online、Disconnected 或 Unknown，因此要有平台降级逻辑。

尤其在 Windows 上，在线判断可能依赖访问微软的探测服务；该探测被防火墙阻止时，系统可能报离线而你的业务服务器其实可达。

## Feature 支持与默认值陷阱

backend 不支持某 feature 时，getter 会给看似正常的默认值：

- 不支持 `Reachability`：`reachability()` 为 `Unknown`。
- 不支持 `CaptivePortal`：`isBehindCaptivePortal()` 为 `false`。
- 不支持 `TransportMedium`：`transportMedium()` 为 `Unknown`。
- 不支持 `Metered`：`isMetered()` 为 `false`。

因此在依据这些值作产品决策前，调用 `supports()` 或检查 `supportedFeatures()`。`false` 不一定表示“确实没有 captive portal / 不是计费网络”，也可能是“平台无从得知”。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 枚举 | `Reachability` | 网络可达性层级：`Unknown`、`Disconnected`、`Local`、`Site`、`Online`；只作为系统信号，非目标连接保证。 |
| 枚举 | `TransportMedium` | Qt 6.3 起；`Unknown`、`Ethernet`、`Cellular`、`WiFi`、`Bluetooth`。Windows 蓝牙 PAN 也可能报告为 Ethernet。 |
| 枚举 | `Feature` / `Features` | backend 能力位：`Reachability`、`CaptivePortal`、`TransportMedium`、`Metered`；先检查再信任 getter 默认值。 |
| 状态 | `reachability()` | 返回当前系统报告的可达性；不可用作请求前的决定性拦截。 |
| 状态 | `isBehindCaptivePortal()` | Qt 6.2 起；依赖 OS 检测。不支持时为 `false`。 |
| 状态 | `transportMedium()` | Qt 6.3 起；返回当前活动传输介质，不支持时为 `Unknown`。 |
| 状态 | `isMetered()` | Qt 6.3 起；是否已知为计费网络。不支持时为 `false`，应结合 `supports()`。 |
| backend | `backendName()` | 返回当前加载 backend 名称，适合诊断与平台适配日志。 |
| backend | `supports(Features)` | 判断当前 backend 是否支持所需的全部 feature。 |
| backend | `supportedFeatures()` | 返回当前 backend 支持的 feature 集合。 |
| 单例 | `loadDefaultBackend()` | Qt 6.3 起；加载平台推荐 backend。成功后才能安全使用 `instance()`。 |
| 单例 | `loadBackendByName(QStringView)` | Qt 6.4 起；按名称（大小写无关）加载特定 backend，适合明确的平台或自定义 backend 选择。 |
| 单例 | `loadBackendByFeatures(Features)` | Qt 6.4 起；加载支持指定 feature 集合的 backend。 |
| 单例 | `availableBackends()` | 列出当前可用 backend 名称。 |
| 单例 | `instance()` | 返回已加载单例，未加载时为 `nullptr`；不拥有也不删除返回指针。 |
| 信号 | `reachabilityChanged(Reachability)` | 系统可达性改变时发射。 |
| 信号 | `isBehindCaptivePortalChanged(bool)` | captive portal 状态改变时发射。 |
| 信号 | `transportMediumChanged(TransportMedium)` | 当前传输介质改变时发射。 |
| 信号 | `isMeteredChanged(bool)` | 计费状态改变时发射。 |

## 一句话总结

`QNetworkInformation` 把平台网络状态变成可观察信号：先加载并验证 backend 能力，把结果用于体验优化和策略调整，但让真实网络请求而不是“Online”决定服务是否可达。
