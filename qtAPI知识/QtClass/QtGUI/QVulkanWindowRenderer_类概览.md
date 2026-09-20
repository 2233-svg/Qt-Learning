# QVulkanWindowRenderer 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QVulkanWindowRenderer>`
> 所属模块：`Qt6::Gui`
> 继承：无

## 它解决什么问题

`QVulkanWindowRenderer` 是 `QVulkanWindow` 的渲染逻辑接口。`QVulkanWindow` 负责窗口、surface、swapchain、framebuffer、render pass、队列、command buffer 等平台化管理；应用通过派生 `QVulkanWindowRenderer` 填入自己的 Vulkan 资源创建、swapchain 相关资源管理和每帧命令录制逻辑。

它本身没有绘制实现，唯一必须实现的是 `startNextFrame()`。如果把 `QVulkanWindow` 想成负责“什么时候能画、当前帧资源在哪里”的宿主，那么 renderer 就负责“这一帧往 command buffer 里写什么”。

## 实际使用场景

- 用 `QVulkanWindow` 快速搭建原生 Vulkan 渲染窗口。
- 在 `initResources()` 中创建 pipeline、descriptor、buffer、纹理等长期资源。
- 在 `initSwapChainResources()` 中创建依赖窗口尺寸、render pass、framebuffer 的资源。
- 在 `startNextFrame()` 中录制绘制命令，并在完成后通知窗口提交当前帧。

## 使用模型

通常同时派生 `QVulkanWindow` 和 `QVulkanWindowRenderer`。窗口子类重写 `createRenderer()`，返回 renderer 实例；renderer 保存 `QVulkanWindow *`，在回调中通过窗口取得 device、queue、command buffer、framebuffer、swapchain size 等对象。

`initResources()` 和 `releaseResources()` 成对管理不依赖 swapchain 尺寸的图形资源；`initSwapChainResources()` 和 `releaseSwapChainResources()` 成对管理随窗口 resize 或 swapchain 重建而变化的资源。一次 `initResources()` 生命周期内，swapchain 资源可能被多次释放和重建。

`startNextFrame()` 每次被调用后，必须最终调用 `QVulkanWindow::frameReady()`。可以同步调用，也可以异步完成后再调用；但漏掉它会让渲染循环停住。

## 关键语义与边界

`preInitResources()` 发生在逻辑设备初始化前，但此时物理设备和 window surface 已经可用。需要根据 physical device 与 surface 共同决定队列、特性或配置时，可以在这里做准备。

`initResources()` 被调用时，`device()`、`graphicsQueue()`、`graphicsCommandPool()` 等 accessor 才保证有效，并持续有效到 `releaseResources()`。资源丢失或重建时，此函数可能在同一个窗口生命周期内被调用多次，但再次调用前一定会先调用 `releaseResources()`。

`initSwapChainResources()` 是做尺寸相关计算的好位置，例如投影矩阵、viewport、依赖 swapchain image size 的 framebuffer 附件。窗口 resize 会导致它和 `releaseSwapChainResources()` 多次成对出现。

`releaseSwapChainResources()` 是 Qt 开始释放 swapchain 相关资源前最后一个资源仍完整的回调。如果 `startNextFrame()` 做了异步工作，这里必须阻塞等待未完成帧，并在返回前调用 `frameReady()`，否则 Qt 可能等不到当前帧结束。

Qt 会在调用释放回调前后等待 device idle，但应用仍要按 Vulkan 规则销毁自己创建的对象，并处理 device lost。

## 常见误区

- `startNextFrame()` 录制完命令后忘记 `frameReady()`，渲染循环直接卡住。
- 把 swapchain 相关资源放在 `initResources()`，窗口 resize 后资源尺寸失配。
- 在 `releaseResources()` 后继续使用之前缓存的 device、command pool、framebuffer 或 pipeline。
- 假设初始化只发生一次；device lost、窗口重建、资源策略都会触发多次生命周期。
- 异步渲染没有在释放回调中等待收尾，导致 Qt 释放资源时仍有未完成命令。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `[virtual noexcept] ~QVulkanWindowRenderer()` | 虚析构函数。 | renderer 通常由 `QVulkanWindow` 通过 `createRenderer()` 接收；析构前应已释放自有 Vulkan 资源。 |
| `[virtual] void preInitResources()` | 图形初始化即将开始前的钩子。 | physical device 和 surface 可用，但 logical device 尚未完成初始化。 |
| `[virtual] void initResources()` | 创建 renderer 的长期图形资源。 | 可安全使用 `device()`、`graphicsQueue()`、`graphicsCommandPool()` 等，直到 `releaseResources()`。 |
| `[virtual] void initSwapChainResources()` | 创建 swapchain、framebuffer、render pass、尺寸相关资源。 | resize 和 swapchain 重建会多次调用；适合更新投影矩阵和 viewport。 |
| `[virtual] void releaseSwapChainResources()` | 释放 swapchain 相关资源。 | 可能随后再次 `initSwapChainResources()`；异步帧必须在返回前收尾并 `frameReady()`。 |
| `[virtual] void releaseResources()` | 释放长期图形资源。 | 可能随后再次 `initResources()`；Qt 会围绕该回调等待 device idle。 |
| `[pure virtual] void startNextFrame()` | 为下一帧录制绘制命令。 | 每次调用后必须最终调用 `QVulkanWindow::frameReady()`。 |
| `[virtual] void physicalDeviceLost()` | 物理设备丢失时通知 renderer。 | Qt 会稍后尝试重新初始化；通常不需要额外特殊处理。 |
| `[virtual] void logicalDeviceLost()` | logical device 因 `VK_ERROR_DEVICE_LOST` 丢失时通知 renderer。 | Qt 会释放资源并尝试重新获取 device；旧资源视为不可继续使用。 |

## 一句话总结

`QVulkanWindowRenderer` 是 `QVulkanWindow` 的渲染协议：按回调分清长期资源、swapchain 资源和每帧命令，并保证每个 `startNextFrame()` 都走到 `frameReady()`。
