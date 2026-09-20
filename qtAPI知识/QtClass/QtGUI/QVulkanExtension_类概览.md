# QVulkanExtension 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QVulkanExtension>`
> 所属模块：`Qt6::Gui`
> 继承：无

## 它解决什么问题

`QVulkanExtension` 是一个轻量结构体，用来描述 Vulkan extension 的名称和版本。Qt 用它承载 `QVulkanInstance::supportedExtensions()`、`QVulkanWindow::supportedDeviceExtensions()` 等查询结果，方便应用判断某个 instance 或 physical device 是否支持需要的扩展。

它不启用扩展，也不代表扩展函数已经可调用。启用 instance 扩展要在 `QVulkanInstance::create()` 前调用 `setExtensions()`；启用 device 扩展要在 `QVulkanWindow` 或手写 `vkCreateDevice()` 流程中配置。函数指针仍要按 Vulkan 规则获取。

## 实际使用场景

- 判断 `VK_KHR_surface`、平台 WSI 或 debug 扩展是否可用。
- 创建设备前检查 `VK_KHR_swapchain` 是否由目标物理设备支持。
- 在诊断信息里列出当前环境支持的扩展名称和版本。
- 用 `QVulkanInfoVector<QVulkanExtension>::contains()` 做最低版本检查。

## 使用模型

`QVulkanExtension` 是可拷贝、可放入容器的值类型。成员变量公开，通常只读使用 Qt 查询返回的结果；手工构造也只是为了比较、测试或建立期望列表。

相等与哈希都基于 `name` 和 `version`。因此同名不同版本会被认为是不同扩展记录。

## 关键语义与边界

`name` 是 Vulkan 扩展名的字节串，通常形如 `VK_KHR_swapchain`。比较是字节级精确比较，大小写、前后空白、拼写都必须一致。

`version` 是扩展的规范版本号，随向后兼容变化递增。它不是 Vulkan API 主版本号，也不表示驱动整体版本。

## 常见误区

- 看到 `supportedExtensions()` 里有扩展，就以为已经启用。支持和启用是两件事。
- 只比较名称却忽略最低版本要求。
- 把 instance extension 和 device extension 混在一起检查。
- 用 `QString` 本地化处理扩展名；扩展名应按 ASCII 字节串精确处理。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `QByteArray QVulkanExtension::name` | 扩展名称。 | 精确匹配 Vulkan 扩展名，例如 `VK_KHR_swapchain`。 |
| `uint32_t QVulkanExtension::version` | 扩展规范版本。 | 表示该扩展的版本，不是 Vulkan API 或驱动版本。 |
| `[noexcept] size_t qHash(const QVulkanExtension &key, size_t seed = 0)` | 按名称和版本计算哈希。 | 用于 `QHash`、`QSet`；seed 参与哈希组合。 |
| `[noexcept] bool operator!=(const QVulkanExtension &lhs, const QVulkanExtension &rhs)` | 判断两个扩展记录是否不同。 | 名称或版本任一不同即不同。 |
| `[noexcept] bool operator==(const QVulkanExtension &lhs, const QVulkanExtension &rhs)` | 判断两个扩展记录是否相同。 | 名称和版本都相同才相等。 |

## 一句话总结

`QVulkanExtension` 只是 Vulkan 扩展“支持清单”里的一个条目；它能帮你判断可用性，但启用和函数解析还要走 Vulkan 初始化流程。
