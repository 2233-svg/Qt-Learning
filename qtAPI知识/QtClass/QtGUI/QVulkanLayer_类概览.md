# QVulkanLayer 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QVulkanLayer>`
> 所属模块：`Qt6::Gui`
> 继承：无

## 它解决什么问题

`QVulkanLayer` 是描述 Vulkan layer 的轻量结构体。Vulkan layer 常用于验证、调试、捕获、性能分析或工具注入；Qt 用这个结构承载 `QVulkanInstance::supportedLayers()` 的查询结果，让应用在创建 instance 前判断目标 layer 是否存在。

它只描述 layer，不启用 layer。要启用验证层等 layer，需要在 `QVulkanInstance::create()` 前调用 `QVulkanInstance::setLayers()`。

## 实际使用场景

- 创建 Vulkan instance 前检查 `VK_LAYER_KHRONOS_validation` 是否可用。
- 在开发版应用中自动启用验证层，发布版不启用。
- 把可用 layer 的名称、描述、规范版本、实现版本打印到诊断日志。
- 用 `QVulkanInfoVector<QVulkanLayer>::contains()` 快速确认某个 layer 名是否在支持列表中。

## 使用模型

`QVulkanLayer` 是可拷贝值类型，成员变量公开。Qt 返回的支持列表一般只读使用；自定义构造主要用于比较或测试。

相等与哈希基于 `name`、`version`、`specVersion`，不包含 `description`。这意味着描述文本变化不会影响相等性判断。

## 关键语义与边界

`name` 是启用 layer 时使用的精确名称，例如 `VK_LAYER_KHRONOS_validation`。`description` 只适合展示或日志，不应用来做逻辑判断。

`specVersion` 是该 layer 面向的 Vulkan 规范版本；`version` 是 layer 自己的实现版本，随向后兼容变化递增。两者不是同一个概念。

layer 可用性受 Vulkan SDK、驱动、环境变量和安装状态影响。即使开发机上存在，用户机器也未必存在；启用前必须查询。

## 常见误区

- 未检查可用性就硬启用验证层，导致 `QVulkanInstance::create()` 失败。
- 把 `description` 当作稳定标识；应使用 `name`。
- 混淆 `specVersion` 与 `version`。
- 忘记 layer 只在 instance 创建前配置，创建后不能追加启用。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `QByteArray QVulkanLayer::description` | layer 的描述文本。 | 用于展示和日志；不参与相等比较。 |
| `QByteArray QVulkanLayer::name` | layer 的精确名称。 | 启用 layer 时传这个名称。 |
| `QVersionNumber QVulkanLayer::specVersion` | layer 面向的 Vulkan 规范版本。 | 表示规范兼容版本，不是实现构建号。 |
| `uint32_t QVulkanLayer::version` | layer 自身版本。 | 随向后兼容变化递增。 |
| `[noexcept] size_t qHash(const QVulkanLayer &key, size_t seed = 0)` | 按名称、实现版本和规范版本计算哈希。 | 可用于 `QHash`、`QSet`。 |
| `[noexcept] bool operator!=(const QVulkanLayer &lhs, const QVulkanLayer &rhs)` | 判断两个 layer 记录是否不同。 | 名称、`version` 或 `specVersion` 任一不同即不同。 |
| `[noexcept] bool operator==(const QVulkanLayer &lhs, const QVulkanLayer &rhs)` | 判断两个 layer 记录是否相同。 | 比较名称、实现版本和规范版本；不比较描述。 |

## 一句话总结

`QVulkanLayer` 是 Vulkan layer 支持信息的条目：用它决定能不能启用某层，而不是把它当成已经启用的调试能力。
