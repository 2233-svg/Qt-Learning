# QSysInfo
> Qt 6.11.1 · Qt Core · 来自 `QSysInfo`

## 作用定位
`QSysInfo` 提供运行平台、CPU 架构、内核类型、产品名称和构建 ABI 等只读系统信息。它适合诊断日志、崩溃报告和少量平台分支。
## API 速查
| API | 是做什么的 |
|---|---|
| `currentCpuArchitecture()` | 当前运行 CPU 架构。 |
| `buildCpuArchitecture()` | Qt 构建目标架构。 |
| `kernelType()` / `kernelVersion()` | 系统内核类型与版本。 |
| `productType()` / `productVersion()` | 操作系统产品标识。 |
| `prettyProductName()` | 面向用户的系统名称。 |
| `bootUniqueId()` / `machineUniqueId()` | 启动或机器标识。 |

## 使用场景
把系统信息写入诊断日志，帮助复现平台相关问题。
## 常见坑与经验
- 不要把产品名称字符串当权限或功能判断；优先能力探测。
- 机器标识涉及隐私，上传前需要用户授权或脱敏。
- 架构信息不能替代运行时特性检测。
## 知识点覆盖
平台诊断、ABI、CPU 架构、隐私、功能探测、日志。
