# QVulkanFunctions 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QVulkanFunctions>`
> 所属模块：`Qt6::Gui`
> 继承：无

## 它解决什么问题

`QVulkanFunctions` 解决的是“Qt 应用如何跨平台调用 Vulkan instance 级核心命令，而不直接链接 Vulkan 库”的问题。Qt 默认不会把应用链接到 Vulkan loader；`QVulkanInstance` 创建成功后，Qt 在运行时解析核心 Vulkan 函数，并通过 `QVulkanFunctions` 暴露 instance 级入口。

这个类只覆盖核心 Vulkan API 的 instance/physical-device 相关命令，不覆盖 device 级命令，也不覆盖窗口系统接口扩展。device、queue、command buffer、buffer、image 等依赖 `VkDevice` 或其子对象的命令放在 `QVulkanDeviceFunctions` 中；额外扩展函数需要用 `QVulkanInstance::getInstanceProcAddr()` 或 `vkGetDeviceProcAddr()` 获取。

## 实际使用场景

- 枚举 `VkPhysicalDevice` 并读取设备属性、特性、队列族、内存类型。
- 创建逻辑设备前查询 instance layer、instance extension、device extension。
- 在没有直接链接 Vulkan loader 的 Qt GUI 程序里调用核心 Vulkan 查询 API。
- 写跨平台 Vulkan 初始化代码时，用 Qt 已经解析好的函数表减少平台差异。

## 使用模型

`QVulkanFunctions` 不能由应用直接构造。正确路径是：创建并 `create()` 一个 `QVulkanInstance`，然后调用 `QVulkanInstance::functions()` 取得指针。该对象由 `QVulkanInstance` 拥有，应用只借用，不删除。

这个函数表和创建它的 `QVulkanInstance` 绑定。`QVulkanInstance::destroy()` 或析构后，不要继续使用先前取得的 `QVulkanFunctions *`。如果重新创建 Vulkan instance，应重新获取函数表指针。

Vulkan 1.1、1.2、1.3 以及更新命令是否能在 C++ 中直接调用，取决于编译时 Vulkan 头文件是否定义了对应 `VK_VERSION_1_x`。运行时还要看实际 instance/driver 支持的版本；能编译不等于当前机器能安全使用所有版本命令。

## 关键语义与边界

`QVulkanFunctions` 不负责 Vulkan 对象生命周期。调用 `vkCreateDevice()` 后，设备销毁仍要按 Vulkan 规则通过 device 级函数完成。所有 `VkResult`、结构体链、计数参数、双调用枚举模式都遵守 Vulkan 原生 API 语义。

窗口系统接口不在这里。创建 surface、把窗口和 Vulkan instance 关联、取得 `VkSurfaceKHR` 等流程由 `QWindow::setVulkanInstance()`、`QWindow::setSurfaceType()`、`QVulkanInstance::surfaceForWindow()` 等 Qt API 负责。

扩展函数不在核心函数表里。需要 debug utils、swapchain、平台 WSI 或供应商扩展时，应通过函数指针解析机制获取，并确认扩展已启用。

## 常见误区

- 直接 `new QVulkanFunctions` 或把它作为成员值保存。它只能由 `QVulkanInstance` 创建并拥有。
- 在 `QVulkanInstance::create()` 前调用 `functions()` 后马上使用 Vulkan 命令。
- 把 device 级命令误找在 `QVulkanFunctions` 里；应使用 `deviceFunctions(VkDevice)`。
- 忘记先检查 `supportedApiVersion()`、layer/extension 支持和 `VkResult`。
- 把扩展命令当作核心命令，导致函数指针为空或未定义行为。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `~QVulkanFunctions()` | 释放 Qt 内部解析出的 instance 级函数表。 | 应由 `QVulkanInstance` 管理；应用代码不要删除从 `functions()` 得到的指针。 |
| `vkEnumeratePhysicalDevices(...)` | 枚举当前 Vulkan instance 下的物理设备。 | 遵守 Vulkan 双调用计数模式；检查 `VkResult`。 |
| `vkGetDeviceProcAddr(...)` | 获取 device 级函数地址。 | 常用于额外 device 扩展；核心 device 命令优先用 `QVulkanDeviceFunctions`。 |
| `vkGetPhysicalDeviceProperties(...)` | 查询物理设备属性。 | 返回设备名、类型、限制等；选择设备前常用。 |
| `vkGetPhysicalDeviceQueueFamilyProperties(...)` | 查询队列族能力。 | 后续创建设备和队列前必须匹配图形/计算/传输需求。 |
| `vkGetPhysicalDeviceMemoryProperties(...)` | 查询物理设备内存类型与堆。 | 分配内存前用来选择 memory type。 |
| `vkGetPhysicalDeviceFeatures(...)` | 查询 Vulkan 1.0 设备特性。 | 创建逻辑设备时只能启用实际支持的特性。 |
| `vkGetPhysicalDeviceFormatProperties(...)` | 查询格式能力。 | 图像、缓冲视图、采样等能力依赖格式和 tiling。 |
| `vkGetPhysicalDeviceImageFormatProperties(...)` | 查询某类图像创建参数是否受支持。 | 失败时不要继续用该格式/用法创建 image。 |
| `vkCreateDevice(...)` | 基于物理设备创建逻辑设备。 | layer、extension、feature、queue create info 必须和查询结果一致。 |
| `vkEnumerateInstanceLayerProperties(...)` | 枚举可用 instance layer。 | 启用验证层前先查是否存在。 |
| `vkEnumerateInstanceExtensionProperties(...)` | 枚举可用 instance extension。 | WSI/debug 等扩展要先查再启用。 |
| `vkEnumerateDeviceLayerProperties(...)` | 枚举设备层属性。 | 现代 Vulkan 中使用较少；仍按驱动返回结果处理。 |
| `vkEnumerateDeviceExtensionProperties(...)` | 枚举物理设备支持的 device extension。 | 创建 swapchain 等能力前必须确认扩展存在。 |
| `vkGetPhysicalDeviceSparseImageFormatProperties(...)` | 查询稀疏图像格式属性。 | 只在使用 sparse resource 时需要。 |
| `vkGetPhysicalDeviceFeatures2(...)` | 查询带 `pNext` 扩展链的设备特性。 | Vulkan 1.1+；适合新特性结构链。 |
| `vkGetPhysicalDeviceProperties2(...)` | 查询带 `pNext` 扩展链的设备属性。 | Vulkan 1.1+；可挂接扩展属性结构。 |
| `vkGetPhysicalDeviceFormatProperties2(...)` | 查询带扩展链的格式属性。 | Vulkan 1.1+。 |
| `vkGetPhysicalDeviceImageFormatProperties2(...)` | 查询带扩展链的图像格式能力。 | Vulkan 1.1+；检查返回值。 |
| `vkGetPhysicalDeviceQueueFamilyProperties2(...)` | 查询带扩展链的队列族属性。 | Vulkan 1.1+。 |
| `vkGetPhysicalDeviceMemoryProperties2(...)` | 查询带扩展链的内存属性。 | Vulkan 1.1+。 |
| `vkGetPhysicalDeviceSparseImageFormatProperties2(...)` | 查询带扩展链的稀疏图像能力。 | Vulkan 1.1+。 |
| `vkGetPhysicalDeviceExternalBufferProperties(...)` | 查询外部 buffer 共享能力。 | 需要跨进程/跨 API 共享时关注。 |
| `vkGetPhysicalDeviceExternalSemaphoreProperties(...)` | 查询外部 semaphore 共享能力。 | 同步对象跨 API/进程共享前检查。 |
| `vkGetPhysicalDeviceExternalFenceProperties(...)` | 查询外部 fence 共享能力。 | 外部同步集成场景使用。 |
| `vkEnumeratePhysicalDeviceGroups(...)` | 枚举物理设备组。 | 多 GPU/device group 场景使用。 |
| `vkGetPhysicalDeviceToolProperties(...)` | 查询 Vulkan 工具信息。 | Vulkan 1.3+；可用于诊断活跃层和工具。 |

## 一句话总结

`QVulkanFunctions` 是绑定到 `QVulkanInstance` 的 instance 级核心 Vulkan 函数表：它帮你解决动态解析，不替你承担 Vulkan 版本、扩展和对象生命周期规则。
