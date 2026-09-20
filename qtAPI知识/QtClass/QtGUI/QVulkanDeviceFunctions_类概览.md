# QVulkanDeviceFunctions 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QVulkanDeviceFunctions>`
> 所属模块：`Qt6::Gui`
> 继承：无

## 它解决什么问题

`QVulkanDeviceFunctions` 解决的是“Qt 应用如何调用依赖 `VkDevice`、`VkQueue`、`VkCommandBuffer` 等 device 派生对象的核心 Vulkan 命令”的问题。Qt 把 instance 级命令放在 `QVulkanFunctions`，把 device 级命令放在 `QVulkanDeviceFunctions`，这样可以避免每次 device 命令调用都经过额外内部派发。

它不是 Vulkan 资源管理器。它只是一张由 Qt 动态解析并缓存的函数表；buffer、image、pipeline、descriptor、command buffer、同步对象等资源仍完全遵守 Vulkan 原生创建、使用、同步、销毁规则。

## 实际使用场景

- 在 `QVulkanWindowRenderer::startNextFrame()` 中记录 command buffer。
- 创建或销毁 buffer、image、image view、shader module、pipeline、descriptor set、framebuffer、render pass。
- 提交队列、等待 fence/semaphore、处理 host-visible memory 映射和刷新。
- 使用 Vulkan 1.1+、1.2+、1.3+ 的核心 device 命令，但仍希望由 Qt 负责运行时函数解析。

## 使用模型

`QVulkanDeviceFunctions` 不能由应用直接构造。先创建 `QVulkanInstance` 和 `VkDevice`，再调用 `QVulkanInstance::deviceFunctions(device)` 获取指针。Qt 会在第一次请求某个 `VkDevice` 的函数表时创建对象，并在内部缓存。

函数表与传入的 `VkDevice` 绑定。销毁或重建 logical device 后，应丢弃旧指针；如果需要清掉缓存，使用 `QVulkanInstance::resetDeviceFunctions(device)`。在 `QVulkanWindow` 场景里，常见做法是在 `initResources()` 中获取并保存，在 `releaseResources()` 后视作不可用。

此类覆盖核心 Vulkan 命令，不覆盖扩展命令。扩展函数仍需通过 `vkGetDeviceProcAddr()` 或 `QVulkanInstance::getInstanceProcAddr()` 解析，并确保对应扩展在创建设备时已启用。

## 关键语义与边界

所有成员函数保留 Vulkan C API 的参数和返回值语义。Qt 不会自动检查结构体 `sType`、`pNext`、资源状态、同步屏障、队列归属或 command buffer 录制状态。

命令可分为几大类：设备和队列控制、内存管理、buffer/image 资源、descriptor 和 pipeline、render pass/framebuffer、command pool/buffer、`vkCmd*` 录制命令、同步对象、查询、动态渲染和新版本增强命令。调用前必须确认 Vulkan 版本、启用扩展、对象状态和同步关系。

头文件会根据编译时 Vulkan SDK 的 `VK_VERSION_1_x` 条件暴露新版本命令；运行时还必须确认当前设备支持对应 API 版本或特性。能通过编译不代表当前 GPU/驱动可以无条件执行。

## 常见误区

- 在 `VkDevice` 销毁后继续使用旧的 `QVulkanDeviceFunctions *`。
- 把扩展命令当作核心命令，从这个类里找不到还误以为 Qt 不支持 Vulkan 扩展。
- 在 `QVulkanWindow` 资源释放回调后继续调用旧 framebuffer、render pass 或 command buffer。
- 认为 Qt 会替 Vulkan 做同步；实际 barrier、queue submit、fence/semaphore 仍由应用负责。
- 忘记每个 `vkCreate*` 通常要配套 `vkDestroy*`，且销毁时机要满足 GPU 不再使用。

## API 速查表

| API / 命令组 | 作用 | 重点注意 |
| --- | --- | --- |
| `~QVulkanDeviceFunctions()` | 释放某个 device 绑定的函数表对象。 | 由 `QVulkanInstance` 缓存和管理；应用不要删除借来的指针。 |
| 设备与队列命令：`vkDestroyDevice()`、`vkGetDeviceQueue()`、`vkQueueSubmit()`、`vkQueueWaitIdle()`、`vkDeviceWaitIdle()` | 管理 logical device、取得队列、提交工作和等待空闲。 | 队列提交和等待遵守 Vulkan 同步规则；销毁 device 前确保资源和队列状态正确。 |
| 内存命令：`vkAllocateMemory()`、`vkFreeMemory()`、`vkMapMemory()`、`vkUnmapMemory()`、`vkFlushMappedMemoryRanges()`、`vkInvalidateMappedMemoryRanges()` | 分配、映射和同步设备内存。 | host-visible 内存是否需要 flush/invalidate 取决于 memory property。 |
| 资源内存绑定：`vkGetBufferMemoryRequirements()`、`vkBindBufferMemory()`、`vkGetImageMemoryRequirements()`、`vkBindImageMemory()` | 查询 buffer/image 内存需求并绑定内存。 | memory type、alignment、offset 必须满足 Vulkan 要求。 |
| 同步对象：`vkCreateFence()`、`vkWaitForFences()`、`vkCreateSemaphore()`、`vkCreateEvent()`、`vkSetEvent()`、`vkResetEvent()` | 创建和使用 CPU/GPU 同步对象。 | fence/semaphore/event 语义不同；不能混用为“通用等待”。 |
| 查询对象：`vkCreateQueryPool()`、`vkGetQueryPoolResults()`、`vkCmdBeginQuery()`、`vkCmdEndQuery()`、`vkCmdWriteTimestamp()` | 创建 query pool 并读取统计或时间戳。 | 查询结果可用性和 pipeline stage 要按 Vulkan 规则处理。 |
| buffer/image：`vkCreateBuffer()`、`vkCreateImage()`、`vkCreateImageView()`、`vkGetImageSubresourceLayout()` | 创建和查询基础资源。 | image layout、usage、format、memory 选择必须和后续使用一致。 |
| shader/pipeline：`vkCreateShaderModule()`、`vkCreateGraphicsPipelines()`、`vkCreateComputePipelines()`、`vkCreatePipelineLayout()` | 创建 shader module 和 pipeline。 | pipeline 创建依赖 render pass、layout、descriptor set layout、shader stage 等完整配置。 |
| descriptor：`vkCreateDescriptorSetLayout()`、`vkCreateDescriptorPool()`、`vkAllocateDescriptorSets()`、`vkUpdateDescriptorSets()` | 管理 descriptor 布局、池和绑定数据。 | pool 容量、layout、动态 offset 和资源生命周期要匹配。 |
| render pass/framebuffer：`vkCreateRenderPass()`、`vkCreateFramebuffer()`、`vkCmdBeginRenderPass()`、`vkCmdEndRenderPass()` | 管理传统 render pass 渲染路径。 | swapchain 重建时相关对象通常都要释放并重建。 |
| command pool/buffer：`vkCreateCommandPool()`、`vkAllocateCommandBuffers()`、`vkBeginCommandBuffer()`、`vkEndCommandBuffer()`、`vkResetCommandBuffer()` | 管理命令池和命令缓冲录制。 | command buffer 状态机严格；录制期间只能调用合法命令。 |
| 绘制/计算录制：`vkCmdBindPipeline()`、`vkCmdBindVertexBuffers()`、`vkCmdDraw()`、`vkCmdDrawIndexed()`、`vkCmdDispatch()` | 录制绘制和计算命令。 | 当前 pipeline、descriptor、vertex/index buffer、render pass 状态必须完整。 |
| 复制和清理命令：`vkCmdCopyBuffer()`、`vkCmdCopyImage()`、`vkCmdBlitImage()`、`vkCmdClearColorImage()`、`vkCmdResolveImage()` | 录制资源复制、清理和 resolve。 | image layout 与访问屏障必须正确。 |
| pipeline barrier：`vkCmdPipelineBarrier()`、`vkCmdWaitEvents()`、`vkCmdSetEvent()`、`vkCmdResetEvent()` | 表达执行与内存依赖。 | 这是应用负责同步的核心入口，Qt 不会自动推导。 |
| Vulkan 1.1/1.2 增强：`vkBindBufferMemory2()`、`vkGetBufferMemoryRequirements2()`、`vkCreateRenderPass2()`、`vkGetSemaphoreCounterValue()`、`vkCmdDrawIndirectCount()` | 新版本核心 API 的 device 命令。 | 编译时和运行时版本都要满足要求。 |
| Vulkan 1.3 动态状态/同步2：`vkCmdPipelineBarrier2()`、`vkQueueSubmit2()`、`vkCmdBeginRendering()`、`vkCmdEndRendering()` | 使用同步2和动态渲染等现代路径。 | 需要对应 API 版本/特性；不要和旧路径状态假设混淆。 |
| Vulkan 1.4 条件命令：`vkMapMemory2()`、`vkCmdBindDescriptorSets2()`、`vkCmdPushConstants2()` 等 | 当头文件支持时暴露更新核心命令。 | Qt 头文件是否声明取决于 Vulkan SDK；运行时仍要检查设备支持。 |

## 一句话总结

`QVulkanDeviceFunctions` 是某个 `VkDevice` 的核心命令入口表；它让 Qt 应用不用直接链接 Vulkan loader，但所有资源状态、同步和销毁责任仍在应用手里。
