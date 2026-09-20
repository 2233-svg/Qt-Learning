# QVulkanDeviceFunctions
> Qt 6.11.1 · Qt GUI · 来自 `QVulkanDeviceFunctions`

## 1. 先建立直觉

`QVulkanDeviceFunctions` 是 Vulkan device 级函数表。给定 `VkDevice` 后，它提供命令缓冲、队列、内存、pipeline、descriptor 等 device 相关函数入口。

## 2. 类说明

- 头文件：`#include <QVulkanDeviceFunctions>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 获取方式：`QVulkanInstance::deviceFunctions(device)`
- 协作类：`QVulkanInstance`、`QVulkanWindow`

同一个 Vulkan instance 下，不同 device 对应的可用函数可能不同，因此函数表和 device 绑定。

## 3. API 速查

| API | 作用 |
| --- | --- |
| Vulkan device 函数包装 | 调用 `vkCreateBuffer`、`vkCmdDraw`、`vkQueueSubmit` 等 device 级函数 |
| `QVulkanInstance::deviceFunctions(device)` | 为指定 `VkDevice` 取得函数表 |

## 4. 关键用法

```cpp
QVulkanDeviceFunctions *df = inst.deviceFunctions(device);
df->vkDeviceWaitIdle(device);
```

使用 `QVulkanWindow` 时，通常从窗口或 renderer 拿到 device，再取得函数表。

## 5. 使用场景

- 自定义 Vulkan 渲染命令。
- 创建 buffer、image、shader module、pipeline。
- 提交队列和同步。
- 与 `QVulkanWindowRenderer` 配合录制命令。

## 6. 常见坑与经验

- device 函数表必须对应创建资源的同一个 `VkDevice`。
- device 销毁后函数表不再有意义。
- 扩展函数是否可用仍取决于启用的 device extension。
- Qt 不替你管理 Vulkan 对象销毁顺序。

## 7. 知识点覆盖

Vulkan device 函数、VkDevice、命令录制、资源创建、队列提交、扩展函数边界。
