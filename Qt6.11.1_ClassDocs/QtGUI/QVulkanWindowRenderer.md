# QVulkanWindowRenderer
> Qt 6.11.1 · Qt GUI · 来自 `QVulkanWindowRenderer`

## 1. 先建立直觉

`QVulkanWindowRenderer` 是 `QVulkanWindow` 的渲染回调接口。窗口负责 Vulkan 基础设施，renderer 负责在回调里创建资源、录制命令、提交一帧完成信号。

## 2. 类说明

- 头文件：`#include <QVulkanWindowRenderer>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：接口类
- 创建方式：`QVulkanWindow::createRenderer()`

它不是 QObject。通常保存一个 `QVulkanWindow *`，从窗口读取 device、render pass、command buffer 等。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `initResources()` | 创建长期 Vulkan 资源 |
| `initSwapChainResources()` | 创建依赖 swapchain 的资源 |
| `releaseSwapChainResources()` | 释放 swapchain 相关资源 |
| `releaseResources()` | 释放长期资源 |
| `startNextFrame()` | 录制下一帧命令，完成后调用 `frameReady()` |
| `physicalDeviceLost()` | 物理设备丢失通知 |
| `logicalDeviceLost()` | 逻辑设备丢失通知 |

## 4. 关键用法

```cpp
void Renderer::startNextFrame()
{
    VkCommandBuffer cb = window->currentCommandBuffer();
    // begin render pass, bind pipeline, draw...
    window->frameReady();
}
```

swapchain 相关资源如 framebuffer 尺寸相关 pipeline、descriptor、depth image，应放在 `initSwapChainResources()` / `releaseSwapChainResources()` 管理。

## 5. 使用场景

- `QVulkanWindow` 的实际渲染实现。
- 按窗口生命周期组织 Vulkan 资源。
- 响应 swapchain 重建。
- 处理 device lost。

## 6. 常见坑与经验

- `startNextFrame()` 必须在命令录制完成后调用 `frameReady()`，否则窗口渲染循环会卡住。
- 不要在 swapchain 释放后继续用旧 framebuffer 或 image view。
- device lost 后普通资源可能都不可继续使用，要走恢复或关闭流程。
- 长期资源和 swapchain 资源分开管理，重建成本和崩溃风险都会低很多。

## 7. 知识点覆盖

renderer 生命周期、swapchain 资源、每帧命令录制、frameReady、device lost、Vulkan 资源分层。
