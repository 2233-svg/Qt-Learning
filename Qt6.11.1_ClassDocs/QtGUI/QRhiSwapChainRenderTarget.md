# QRhiSwapChainRenderTarget

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiSwapChainRenderTarget`

## 1. 先建立直觉

`QRhiSwapChainRenderTarget` 是 `QRhiRenderTarget` 的具体类型，表示 swapchain 当前帧的 back buffer 渲染目标。通常你不会自己创建它，而是每帧通过 `QRhiSwapChain::currentFrameRenderTarget()` 取得，并传给 `QRhiCommandBuffer::beginPass()`。

它的存在主要是让 RHI 区分“窗口可呈现目标”和“离屏 texture target”。对普通渲染代码，使用它的基类接口即可。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 继承自：`QRhiRenderTarget`
- 获取方式：`QRhiSwapChain::currentFrameRenderTarget()`
- 生命周期：只应在当前 `beginFrame()` 到 `endFrame()` 区间用作录制目标

## 3. API 速查

| API | 作用 |
| --- | --- |
| `swapChain()` | 返回所属 `QRhiSwapChain`。 |
| `resourceType()` | 返回 `QRhiResource::SwapChainRenderTarget`。 |
| 继承的 `pixelSize()` | 获取当前 back buffer 像素尺寸。 |
| 继承的 `devicePixelRatio()` | 获取关联窗口 DPR。 |
| 继承的 `renderPassDescriptor()` | 获取创建 graphics pipeline 所需 descriptor。 |

## 4. 关键用法

```cpp
QRhiRenderTarget *rt = swapChain->currentFrameRenderTarget();
cb->beginPass(rt, clearColor, clearDepthStencil);
```

不需要向下转型。只有在确实需要追溯所属 swapchain 时，才把它当作 `QRhiSwapChainRenderTarget` 使用。

## 5. 使用场景

- 当前帧向窗口 back buffer 开始 render pass。
- 从 render target 查询像素尺寸、sample count、render pass descriptor。
- 渲染工具中通过 `swapChain()` 回溯呈现目标上下文。

## 6. 常见坑与经验

- **不要自行 new。** 它由 swapchain 管理。
- **不要跨帧缓存。** 下一帧的当前 target 可能已换成另一个 back buffer。
- **它不是离屏纹理。** 需要后续采样、多个 pass 链接时使用 `QRhiTextureRenderTarget`。
- **管线仍要匹配 render pass descriptor 和 sample count。**

## 7. 知识点覆盖

- 当前 swapchain back buffer 与 render target
- 帧内有效期和跨帧失效
- 屏幕 target 与离屏 texture target 的区别
- pipeline 兼容性查询
