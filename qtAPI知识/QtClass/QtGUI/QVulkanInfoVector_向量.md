# QVulkanInfoVector 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QVulkanInfoVector>`
> 所属模块：`Qt6::Gui`
> 继承：`QList`

## 它解决什么问题

`QVulkanInfoVector` 是 Qt 给 `QVulkanLayer` 和 `QVulkanExtension` 支持列表准备的专用 `QList` 派生模板。它保留 `QList` 的存储、遍历和值语义，同时补上两个 Vulkan 初始化里非常常用的查询：按名称判断是否存在，按名称加最低版本判断是否满足要求。

它不是通用 Vulkan registry，也不会自动启用 layer 或 extension。它只是对“当前系统或设备报告支持哪些条目”的列表做便捷查询。

## 实际使用场景

- `QVulkanInstance::supportedLayers()` 返回后检查验证层是否存在。
- `QVulkanInstance::supportedExtensions()` 返回后检查 instance extension。
- `QVulkanWindow::supportedDeviceExtensions()` 返回后检查 device extension。
- 构建一组必需/可选 Vulkan 能力，并在创建 instance/device 前逐项判断。

## 使用模型

`QVulkanInfoVector<T>` 继承自 `QList<T>`，其中 `T` 通常是 `QVulkanLayer` 或 `QVulkanExtension`，并且条目需要有 `name` 与 `version` 成员。它是值类型容器，可拷贝、可遍历、可传值。

`contains(name)` 只检查名称；`contains(name, minVersion)` 同时要求 `entry.version >= minVersion`。如果你需要检查 `QVulkanLayer::specVersion`，这个便捷函数不够，需要自行遍历。

## 关键语义与边界

查询使用精确字节串匹配。Vulkan 名称要用官方常量或稳定字符串，避免手敲错拼写。

`minVersion` 对比的是条目的 `version` 字段，不是 `QVersionNumber specVersion`，也不是 Vulkan API 版本。对 extension 来说通常正好是扩展版本；对 layer 来说是 layer 实现版本。

作为 `QList`，它遵守 Qt 容器的隐式共享和值语义。遍历时修改容器仍要注意迭代器和引用失效。

## 常见误区

- 以为 `contains()` 会检查启用状态。它只检查支持列表。
- 对 layer 用 `contains(name, minVersion)` 误以为检查的是 Vulkan `specVersion`。
- 用大小写不一致或带空白的名称查询，导致实际存在也匹配失败。
- 拿到支持列表后不处理缺失情况，直接调用 `setLayers()`/`setExtensions()`。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `bool contains(const QByteArray &name) const` | 判断列表中是否有指定名称的 layer 或 extension。 | 精确比较 `entry.name`；不检查版本。 |
| `bool contains(const QByteArray &name, int minVersion) const` | 判断列表中是否有指定名称且版本不低于 `minVersion` 的条目。 | 比较的是 `entry.version`；不检查 `specVersion`。 |
| `QList<T>` 继承 API | 提供追加、遍历、索引、大小查询等普通容器能力。 | 修改容器时遵守 `QList` 的隐式共享和迭代器有效性规则。 |

## 一句话总结

`QVulkanInfoVector` 是 Vulkan 支持列表的小工具：它让名称/版本检查更顺手，但是否启用、如何失败降级仍由初始化代码决定。
