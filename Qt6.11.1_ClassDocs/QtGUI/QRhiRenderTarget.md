# QRhiRenderTarget

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiRenderTarget`

## 1. 先建立直觉

`QRhiRenderTarget` 是“可以被 `QRhiCommandBuffer::beginPass()` 渲染到的目标”的共同基类。屏幕上的当前 swapchain back buffer 是 render target，离屏 texture render target 也是 render target。它统一暴露像素尺寸、sample count、device pixel ratio 和 render pass descriptor。

它不直接说明颜色附件、深度附件怎么组成；这些由派生类 `QRhiSwapChainRenderTarget` 和 `QRhiTextureRenderTarget` 管理。对绘制代码来说，只要拿到 `QRhiRenderTarget*`，就可以开始 pass。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 继承自：`QRhiResource`
- 派生类：`QRhiSwapChainRenderTarget`、`QRhiTextureRenderTarget`
- 使用入口：`QRhiCommandBuffer::beginPass()`

`QRhiGraphicsPipeline` 需要与 render target 的 `renderPassDescriptor()` 兼容，sample count 也要匹配，否则 draw 可能失败或行为不一致。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `pixelSize()` | 返回实际像素尺寸；swapchain 是窗口后备缓冲尺寸，texture target 是附件尺寸。 |
| `devicePixelRatio()` | 返回设备像素比；texture target 通常为 1，swapchain 反映窗口 DPR。 |
| `sampleCount()` | 返回 MSAA sample count；无 MSAA 时为 1。 |
| `renderPassDescriptor()` | 返回 pipeline 创建所需的 render pass descriptor。 |
| `setRenderPassDescriptor()` | 设置关联 descriptor，通常由派生资源创建流程管理。 |

## 4. 关键用法

```cpp
QRhiRenderTarget *rt = swapChain->currentFrameRenderTarget();
QRhiRenderPassDescriptor *rp = rt->renderPassDescriptor();

pipeline->setRenderPassDescriptor(rp);
pipeline->setSampleCount(rt->sampleCount());
```

渲染前要让 pipeline 的 render pass descriptor 和 sample count 与目标一致。窗口移动到高 DPI 屏幕后，swapchain 的 pixel size 和 DPR 都可能变化。

### viewport 通常使用 pixel size

```cpp
const QSize sz = rt->pixelSize();
cb->setViewport(QRhiViewport(0, 0, sz.width(), sz.height()));
```

UI 逻辑可能按逻辑像素工作，但 RHI viewport 面向 render target 的像素尺寸。DPR 转换要在上层明确处理。

## 5. 使用场景

- 对 swapchain 当前帧 back buffer 渲染。
- 对离屏 texture render target 渲染。
- 渲染组件接收外部 render target 后创建/复用 pipeline。
- 统一处理屏幕目标和离屏目标的 viewport、sample count、render pass descriptor。

## 6. 常见坑与经验

- **DPR 不等于 pixel size。** swapchain target 的像素尺寸通常是窗口逻辑尺寸乘 DPR。
- **render target 改变可能导致 pipeline 不兼容。** 检查 `renderPassDescriptor()->serializedFormat()`。
- **sample count 必须一致。** pipeline、render target、附件 sample count 不一致会出问题。
- **`pixelSize()` 可能触发 texture target 更新检查。** 附件 resize 后要理解底层重建时机。
- **基类不暴露附件细节。** 需要颜色/深度 attachment 时看具体派生类。

## 7. 知识点覆盖

- swapchain render target 与 texture render target 的共同接口
- pixel size、device pixel ratio、sample count
- render pass descriptor 与 pipeline 兼容性
- viewport 设置和高 DPI 渲染
- RHI pass 开始前的目标信息检查
