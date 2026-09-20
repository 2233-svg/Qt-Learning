# QRhiSwapChain

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiSwapChain`

## 1. 先建立直觉

`QRhiSwapChain` 管理一个 `QWindow` 的可呈现 back buffer 队列。每一帧从 swapchain 取得当前 command buffer 和 render target，录制命令后由 `QRhi::endFrame()` 提交并呈现。它是 RHI 与窗口系统、VSync、DPR、HDR、MSAA、surface resize 的交汇点。

不要把它当成永久不变的 framebuffer。窗口 resize、屏幕 DPR 改变、surface 重建、显示器 HDR 状态变化都可能让 swapchain 过期，需要 `createOrResize()` 或整个 RHI/资源重建流程。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 继承自：`QRhiResource`
- 创建入口：`QRhi::newSwapChain()`
- 关联窗口：`setWindow(QWindow *)`
- 帧入口：`QRhi::beginFrame(swapChain)` / `QRhi::endFrame(swapChain)`

`currentFrameCommandBuffer()` 和 `currentFrameRenderTarget()` 只在当前 frame 的 `beginFrame()` / `endFrame()` 区间内可用于录制，不应跨帧缓存。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setWindow()` / `window()` | 关联窗口。 |
| `createOrResize()` | 创建或按当前 surface 像素尺寸重建 swapchain。 |
| `surfacePixelSize()` | 查询窗口表面的当前像素尺寸。 |
| `currentPixelSize()` | 查询最近一次成功创建的 swapchain 像素尺寸。 |
| `currentFrameCommandBuffer()` | 当前帧的命令缓冲。 |
| `currentFrameRenderTarget()` | 当前帧 back buffer 的渲染目标。 |
| `setDepthStencil()` / `depthStencil()` | 设置/读取 swapchain 深度模板 render buffer。 |
| `setSampleCount()` / `sampleCount()` | 设置/读取 swapchain MSAA sample count。 |
| `setRenderPassDescriptor()` / `renderPassDescriptor()` | 设置/读取 pipeline 兼容性 descriptor。 |
| `newCompatibleRenderPassDescriptor()` | 创建与该 swapchain 兼容的 descriptor。 |
| `setFlags()` / `flags()` | 设置 alpha、sRGB、readback、VSync、buffer count 等标志。 |
| `setFormat()` / `format()` / `isFormatSupported()` | 选择并检查 SDR/HDR 输出格式。 |
| `hdrInfo()` | 查询目标显示器 HDR 信息，调用可能不便宜。 |
| `setShadingRateMap()` | Qt 6.9 起设置 VRS map。 |
| `setProxyData()` / `proxyData()` | 设置/读取平台 proxy 相关数据。 |

## 4. 关键用法

### 初始化与 resize

```cpp
swapChain->setWindow(window);
swapChain->setSampleCount(4);
swapChain->setDepthStencil(depthStencil);
swapChain->createOrResize();

if (swapChain->currentPixelSize() != swapChain->surfacePixelSize())
    swapChain->createOrResize();
```

渲染尺寸判断优先使用 `surfacePixelSize()` / `currentPixelSize()`，不要简单用 `QWindow::size() * devicePixelRatio()` 假设所有平台都相同。

### 每帧绘制

```cpp
if (rhi->beginFrame(swapChain) != QRhi::FrameOpSuccess)
    return;

QRhiCommandBuffer *cb = swapChain->currentFrameCommandBuffer();
QRhiRenderTarget *rt = swapChain->currentFrameRenderTarget();
drawFrame(cb, rt);

rhi->endFrame(swapChain);
```

当前 command buffer 和 render target 都是“当前帧对象”，下一帧必须重新查询。

### 截图 back buffer

```cpp
swapChain->setFlags(swapChain->flags()
                    | QRhiSwapChain::UsedAsTransferSource);
```

之后可用空 `QRhiReadbackDescription` 从当前 back buffer 异步回读。

## 5. 使用场景

- 直接向 `QWindow` 呈现 RHI 内容。
- 窗口 resize 和高 DPI 渲染。
- MSAA 屏幕输出。
- SDR、sRGB、HDR10、scRGB、Display P3 HDR 输出。
- 回读当前帧截图。
- 配合 VRS map 的性能优化。

## 6. 常见坑与经验

- **每帧对象不能跨帧缓存。** command buffer 和 current render target 每帧重新获取。
- **resize 用 `createOrResize()`，不是 destroy + create。** 只有 surface 即将销毁时才通常需要 destroy。
- **`FrameOpSwapChainOutOfDate` 是正常恢复路径。** 重新 create/resize 后重试后续帧。
- **HDR 要先 `isFormatSupported()`。** 支持取决于窗口所在屏幕和系统 HDR 设置。
- **HDR 不只是换格式。** 色彩空间、白点、tone mapping、离屏纹理格式都可能要一起调整。
- **`NoVSync` 是请求，不是保证。** 平台/后端可以忽略。
- **MSAA、depth stencil、render pass descriptor 和 pipeline 要一致。**

## 7. 知识点覆盖

- swapchain、back buffer、present 和 frame 生命周期
- resize、surface lifecycle、高 DPI 像素尺寸
- current frame command buffer/render target 的有效期
- MSAA、depth/stencil、render pass compatibility
- sRGB、SDR、HDR10、scRGB、Display P3 HDR
- VSync、截图 readback、VRS 和窗口系统差异
