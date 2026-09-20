# QVulkanWindow
> Qt 6.11.1 · Qt GUI · 来自 `QVulkanWindow`

## 1. 先建立直觉

`QVulkanWindow` 是 Qt 提供的 Vulkan 渲染窗口基类。它负责 swapchain、surface、render pass、framebuffer、队列和常见同步基础设施；你实现 `QVulkanWindowRenderer` 来录制每帧命令。

它适合想写 Vulkan 渲染，但不想从窗口系统和 swapchain 细节全手写开始的应用。

## 2. 类说明

- 头文件：`#include <QVulkanWindow>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QWindow`
- 协作类：`QVulkanWindowRenderer`、`QVulkanInstance`

应用需要先准备 `QVulkanInstance`，再让窗口使用它。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `createRenderer()` | 子类重写，返回 renderer |
| `device()` / `physicalDevice()` | 当前 Vulkan device |
| `graphicsQueue()` / `graphicsQueueFamilyIndex()` | 图形队列信息 |
| `currentCommandBuffer()` | 当前帧命令缓冲 |
| `currentFramebuffer()` | 当前 swapchain framebuffer |
| `defaultRenderPass()` | 默认 render pass |
| `swapChainImageSize()` | swapchain 图像尺寸 |
| `colorFormat()` / `depthStencilFormat()` | 颜色和深度模板格式 |
| `sampleCountFlagBits()` | MSAA sample count |
| `setPreferredColorFormats()` | 设置期望颜色格式 |
| `setSampleCount()` | 请求 MSAA |
| `setQueueCreateInfoModifier()` | 调整 device queue 创建信息 |
| `grab()` | 抓取当前图像 |

## 4. 关键用法

```cpp
class Window : public QVulkanWindow {
    QVulkanWindowRenderer *createRenderer() override {
        return new Renderer(this);
    }
};
```

renderer 中每帧使用窗口提供的 command buffer 和 framebuffer：

```cpp
void Renderer::startNextFrame()
{
    VkCommandBuffer cb = window->currentCommandBuffer();
    // record commands...
    window->frameReady();
}
```

## 5. 使用场景

- Vulkan 教学和实验。
- 自定义 3D 渲染窗口。
- 需要 Qt 窗口事件和 Vulkan swapchain 的工具。
- 与 Qt Widgets/Qt Quick 外部窗口组合。

## 6. 常见坑与经验

- renderer 生命周期由窗口管理，资源创建和释放要响应 `initResources()`、`releaseResources()` 等 renderer 回调。
- swapchain 重建时 framebuffer、pipeline 相关资源可能要重建。
- `currentCommandBuffer()` 只在 frame 录制期间有效。
- 高 DPI 下使用 `swapChainImageSize()` 作为像素尺寸，不要用窗口逻辑尺寸。

## 7. 知识点覆盖

Vulkan window、swapchain、render pass、framebuffer、command buffer、MSAA、renderer 回调、高 DPI。
