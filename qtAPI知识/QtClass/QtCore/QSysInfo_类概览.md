# QSysInfo：查询构建平台、运行系统与机器标识

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSysInfo>`  
> CMake：`Qt6::Core`

`QSysInfo` 是一组静态查询函数和编译期常量，用来回答“这个 Qt 是为谁构建的”“程序现在运行在
什么系统上”“当前机器有没有可识别的主机名或机器 ID”等问题。它没有实例状态，不是
`QObject`，也不负责修改系统配置。

它常用于崩溃报告、升级包选择、遥测里的平台分组、支持信息页面、插件目录选择和调试日志。
不要把它当成授权系统、硬件资产系统或安全边界；许多值可能为空、为 `"unknown"`，或受虚拟化、
兼容层、容器和系统配置影响。

## 四类信息

### 编译时 ABI 信息

`WordSize`、`ByteOrder`、`buildCpuArchitecture()` 和 `buildAbi()` 描述的是 Qt 与应用构建目标。
它们适合选择二进制兼容的插件、补丁包和缓存目录。

```cpp
QString abi = QSysInfo::buildAbi();
QString package = QStringLiteral("myapp-%1.zip").arg(abi);
```

这些值不一定等于真实硬件。一个 32 位程序可以运行在 64 位 CPU 上；一个 x86_64 主机也可能通过
兼容层运行其他架构程序。

### 运行时 CPU 和内核信息

`currentCpuArchitecture()` 尝试报告应用运行时 OS 提供的 CPU 架构。它依赖操作系统可见信息：
32 位 OS 可能不知道底层 CPU 可运行 64 位程序，兼容层也可能隐藏真实架构。

`kernelType()` 和 `kernelVersion()` 描述内核。例如类 Unix 系统通常来自 `uname` 风格信息；
Windows 返回 NT 内核类型和版本。`kernelType()` 可能让人意外：Android 也属于 Linux 内核，
macOS 和 iOS 都属于 Darwin 内核。若要区分产品名称，应看 `productType()`。

### 产品信息

`productType()`、`productVersion()` 和 `prettyProductName()` 描述用户看到的操作系统产品。

- `productType()` 是相对稳定的机器可读标识，如 `"windows"`、`"macos"`、`"android"`、
  某些 Linux 发行版名或 `"unknown"`。
- `productVersion()` 是产品版本字符串，无法确定时为 `"unknown"`；文档明确提示它不保证可排序。
- `prettyProductName()` 适合显示给用户，可能包含代号、系统类型等额外信息，不适合长期存储或
  作为协议标识。

### 机器标识

`machineHostName()` 返回配置的主机名。它不保证全局唯一，也不保证是 FQDN；需要域名解析时应
使用 Qt Network 的 `QHostInfo`。

`machineUniqueId()` 尝试返回机器唯一 ID；无法确定时为空。它可能跨重启保持稳定，也可能不会。
Linux 上通常对应 D-Bus machine ID，但无本地存储的复制节点可能共享或缺失。此值能识别设备，
应按隐私敏感数据处理：不要在未经说明的情况下上传或用作硬绑定。

`bootUniqueId()` 尝试返回当前启动会话的唯一 ID；它预期每次重启变化，目前只在 Linux 和 Apple
操作系统实现。无法确定时为空。

## 编译期常量

`WordSize` 和 `ByteOrder` 是编译期信息：

```cpp
static_assert(QSysInfo::WordSize == 32 || QSysInfo::WordSize == 64);

if constexpr (QSysInfo::ByteOrder == QSysInfo::LittleEndian) {
    // 处理本构建目标的小端优化路径
}
```

它们描述的是应用被编译的平台，不是文件格式的字节序。读写二进制协议时，仍应显式指定协议字节序
并使用 Qt 的大小端转换工具。

## 平台边界与失败值

很多函数有“无法确定”的结果：

- 字符串函数可能返回空字符串或 `"unknown"`，具体按 API 而定。
- ID 函数返回空 `QByteArray` 表示没有可用 ID。
- 产品和内核信息可能因兼容层或虚拟化层而与用户直觉不同。
- 新 CPU、OS 或发行版可能加入新字符串；代码应按“未知值可扩展”处理。

不要写死完整枚举表后拒绝所有新值。更稳妥的做法是先识别自己关心的少数值，其他值落入通用路径。

## 常见错误

### 用 `buildCpuArchitecture()` 判断当前硬件

它描述构建目标。运行时架构用 `currentCpuArchitecture()`，并且结果也受 OS 可见性限制。

### 用 `productVersion()` 做字符串排序

产品版本不保证可排序。Linux 发行版版本尤其可能跳跃或采用发行版自定义规则。

### 把 `prettyProductName()` 写进协议或数据库键

它是显示字符串，可能随 Qt 更新改变。机器可读标识用 `productType()`、`kernelType()` 或 ABI。

### 把主机名当唯一 ID

主机名可以重复、自动生成或随用户修改。需要长期机器标识时考虑 `machineUniqueId()`，并处理空值
和隐私告知。

### 假设机器 ID 一定跨重启稳定

不同系统语义不同。需要“本次启动”标识用 `bootUniqueId()`，需要长期标识也要验证平台能力。

### 把字节序常量当作文件格式判断

`ByteOrder` 只描述本程序运行的构建目标。文件和网络协议必须自带字节序约定。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QSysInfo::BigEndian` | 表示大端字节序 | 网络字节序通常也是大端；仅描述平台字节序枚举值。 |
| `QSysInfo::LittleEndian` | 表示小端字节序 | 现代桌面和移动 CPU 多为小端，但代码不应硬猜。 |
| `QSysInfo::ByteOrder` | 当前构建目标的字节序 | 编译期等于 `BigEndian` 或 `LittleEndian`。 |
| `QSysInfo::WordSize` | 当前构建目标指针位数 | 由 `sizeof(void*) << 3` 得到，通常为 32 或 64。 |
| `buildCpuArchitecture()` | 返回 Qt 编译目标 CPU 架构 | 稳定机器可读值；可能不同于实际运行硬件。 |
| `currentCpuArchitecture()` | 返回 OS 报告的运行时 CPU 架构 | 受 OS、兼容层和虚拟化影响，可能无法反映真实硬件能力。 |
| `buildAbi()` | 返回完整 ABI 标识字符串 | 用于区分二进制不兼容构建；强制组件稳定，可追加可选后缀。 |
| `kernelType()` | 返回内核类型 | Android 通常为 Linux，macOS/iOS 为 Darwin；产品类型另看 `productType()`。 |
| `kernelVersion()` | 返回内核版本 | 无法确定时可能为空；Unix 类系统类似 `uname -r`。 |
| `productType()` | 返回 OS 产品标识 | 稳定机器可读字符串；未知时可能为 `"unknown"`。 |
| `productVersion()` | 返回 OS 产品版本 | 无法确定时为 `"unknown"`；不保证可排序。 |
| `prettyProductName()` | 返回适合显示的系统名称 | 可随 Qt 或系统更新变化，不适合长期存储。 |
| `machineHostName()` | 返回配置的主机名 | 不保证唯一或 FQDN。 |
| `machineUniqueId()` | 返回机器唯一 ID | 可能为空；稳定性因系统而异；按隐私敏感数据处理。 |
| `bootUniqueId()` | 返回本次启动唯一 ID | 可能为空；预期每次启动变化；目前主要 Linux/Apple 实现。 |

一句话总结：`QSysInfo` 给的是平台事实的“可用线索”，不是不可变真理；每个返回值都要按它所属的
层级和失败语义使用。
