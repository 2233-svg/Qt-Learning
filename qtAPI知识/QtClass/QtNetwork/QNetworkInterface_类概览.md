# QNetworkInterface：枚举本机网络接口与地址快照

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkInterface>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 类型：隐式共享的值类型

## 它解决什么问题

`QNetworkInterface` 表示运行本机上的一个网络接口，并提供其系统索引、名称、硬件地址、MTU、标志、类型和地址条目。它用于让网络程序在多网卡、VPN、环回、Wi-Fi、以太网和 IPv6 scope 的环境中明确选择接口，而不是盲目依赖操作系统默认路由。

它返回的是枚举时刻的接口信息快照，不是网络变化监听器，也不会替代路由表或连通性测试。接口显示 `IsUp` / `IsRunning` 也不代表 DNS、网关、代理或目标主机可达。

## 实际使用场景

- 列出本机全部地址并过滤环回、未启用或不具备多播能力的接口。
- 多播或 IPv6 链路本地通信时选择明确的 interface index。
- 根据接口 MTU 估算不分片 UDP payload 的上限。
- 诊断工具展示 IP、硬件地址、接口状态和地址前缀。
- 将系统的 IPv6 scope ID、`QNetworkDatagram::interfaceIndex()` 与接口实体互相映射。

## 枚举与过滤

```cpp
for (const QNetworkInterface &iface : QNetworkInterface::allInterfaces()) {
    const auto flags = iface.flags();
    if (!flags.testFlag(QNetworkInterface::IsUp)
        || !flags.testFlag(QNetworkInterface::IsRunning)
        || flags.testFlag(QNetworkInterface::IsLoopBack)) {
        continue;
    }

    for (const QNetworkAddressEntry &entry : iface.addressEntries())
        qDebug() << iface.name() << entry.ip() << entry.prefixLength();
}
```

`allAddresses()` 只是便利函数：等价于枚举所有 `IsUp` 接口的 `addressEntries()` 后取 `ip()`。它不返回接口、前缀、广播地址或生命周期；需要这些信息时应遍历 `allInterfaces()`。

接口列表失败时可为空。系统配置也可在枚举完成后改变，因此要把结果当作“选择候选”的输入，实际 `bind()`、`joinMulticastGroup()` 或发送失败仍需处理。

## 标志与名称的语义

| `InterfaceFlag` | 语义 |
| --- | --- |
| `IsUp` | 管理上启用。 |
| `IsRunning` | 通常表示已启用且物理/逻辑链路可运行。 |
| `CanBroadcast` | 支持 IPv4 广播。 |
| `IsLoopBack` | 本机环回接口。 |
| `IsPointToPoint` | 点对点接口；它不能同时是 broadcast 接口。 |
| `CanMulticast` | 支持多播。 |

`name()` 是系统标识：Unix 常见为 `eth0`、`en1`，Windows 为用户不可改的内部 ID。`humanReadableName()` 仅用于展示，Windows 用户可能随时修改，Unix 上通常与 `name()` 相同；不能把它作为持久配置键。

`hardwareAddress()` 在以太网上往往是 MAC 地址，但其他接口可能是其他形式甚至为空。它不应被当作跨平台稳定设备身份。

## Index、IPv6 scope 与 MTU

`index()` 是系统接口索引，常用于 IPv6 scope ID，并与 `QNetworkDatagram::interfaceIndex()` 对应。`interfaceFromIndex()` 的索引在接口被移除再添加后可能变化，持久配置优先保存能重新识别接口的策略，而不是假设数字永久不变。

`maximumTransmissionUnit()` 是**接口 MTU**，不是路径 MTU。估算 UDP payload 时要减去 IP、UDP 和上层协议头，且真实远端路径 MTU 可能更小。未知时返回 `0`；不要拿 `0` 当作“不限制”。

IPv6 地址与接口类型的报告具有平台差异：所有平台只保证 IPv4 地址列表；IPv6 列举主要支持 Windows、Linux、macOS 与 BSD，`type()` 也可能是 `Unknown`。这不是 Qt 失败，而是系统能力边界。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 枚举 | `InterfaceFlag` / `InterfaceFlags` | 接口管理、运行、广播、环回、点对点和多播能力；`IsUp`/`IsRunning` 不证明目标服务可达。 |
| 枚举 | `InterfaceType` | 物理/逻辑类型，如 `Loopback`、`Virtual`、`Ethernet`、`Wifi`、`CanBus`、`Ppp`、`SixLoWPAN`；无法识别时为 `Unknown`。 |
| 构造与赋值 | `QNetworkInterface()`、复制/移动构造、`operator=`、`swap()` | 创建、复制、移动或交换接口快照。 |
| 有效性 | `isValid()` | 是否包含有效接口信息；按 name/index 查询后应先检查。 |
| 标识 | `index()` | 系统接口索引；与 IPv6 scope ID、`QNetworkDatagram::interfaceIndex()` 对应，未知为 0。 |
| 标识 | `name()` | 系统接口名称，适合短期系统查找。 |
| 标识 | `humanReadableName()` | 面向显示的名称，可能被用户更改，不能当持久键。 |
| 属性 | `flags()` | 返回 `InterfaceFlags`，用于筛选 up/running/multicast 等能力。 |
| 属性 | `type()` | 返回硬件/链路类型；跨平台可能为 `Unknown`。 |
| 属性 | `hardwareAddress()` | 返回硬件地址文本；不要假定总是 MAC 或稳定唯一 ID。 |
| 属性 | `maximumTransmissionUnit()` | 返回接口 MTU，未知为 0；不等于到远端的 Path MTU。 |
| 地址 | `addressEntries()` | 返回完整 `QNetworkAddressEntry` 快照，含 IP、前缀、广播、生命周期等。 |
| 全局枚举 | `allInterfaces()` | 返回主机接口列表；失败时为空。 |
| 全局枚举 | `allAddresses()` | 返回所有 `IsUp` 接口的 IP；丢失接口和前缀上下文。 |
| 查找 | `interfaceFromName(const QString &)` | 按接口名或索引字符串查找；不存在时返回 invalid 接口。 |
| 查找 | `interfaceFromIndex(int)` | 按系统 index 查找；接口重建后 index 可能变化。 |
| 映射 | `interfaceIndexFromName(const QString &)` | 高效获取名称对应 index；未找到返回 0。 |
| 映射 | `interfaceNameFromIndex(int)` | 高效获取 index 对应名称；未找到返回空字符串。 |
| 调试 | `operator<<(QDebug, const QNetworkInterface &)` | 输出接口快照，适合诊断。 |

## 一句话总结

`QNetworkInterface` 是本机网卡与地址的快照目录：用 flags、index、地址条目和 MTU 选择正确路径，但把系统状态当候选信息，并在真正 bind/发送时处理网络变化。
