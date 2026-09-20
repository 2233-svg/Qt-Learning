# QRhi

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhi`

## 1. 先建立直觉

`QRhi` 是 Qt Rendering Hardware Interface 的总入口。它把 Vulkan、Metal、Direct 3D 11/12、OpenGL ES 等后端包装成一套相对统一的底层渲染 API，供 Qt Quick、渲染引擎和需要直接管理 GPU 资源的代码使用。

它不是 `QPainter` 的替代品，也不是高层场景图。你需要自己管理 buffer、texture、sampler、shader resource bindings、graphics/compute pipeline、render target、swapchain 和 frame 命令。换来的好处是可以在多个图形 API 后端之间共享一套渲染组织方式。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- API 层级：Qt GUI 私有 API，版本升级时需要更谨慎
- 后端：`Null`、`Vulkan`、`OpenGLES2`、`D3D11`、`D3D12`、`Metal`
- 典型协作类：`QRhiSwapChain`、`QRhiCommandBuffer`、`QRhiBuffer`、`QRhiTexture`、`QRhiGraphicsPipeline`

`QRhi` 对象通常代表一个图形设备/上下文。绝大多数资源都由它创建，并且资源生命周期不能超过所属 `QRhi`。后端差异没有被完全抹平，因此功能查询和资源限制查询是写可移植 RHI 代码的必需步骤。

## 3. API 速查

| API 族 | 作用 |
| --- | --- |
| `create()` / `probe()` | 创建或探测某个后端是否可用。 |
| `enumerateAdapters()` | Qt 6.10 起枚举适配器，用于选择 GPU/软件设备。 |
| `backend()` / `backendName()` | 查询当前后端类型和名称。 |
| `beginFrame()` / `endFrame()` | 针对 swapchain 开始/结束一帧。 |
| `beginOffscreenFrame()` / `endOffscreenFrame()` | 无窗口离屏命令录制。 |
| `finish()` | 等待已提交 GPU 工作完成，调试/同步时使用，避免频繁调用。 |
| `newBuffer()` / `newTexture()` / `newSampler()` | 创建基础 GPU 资源。 |
| `newGraphicsPipeline()` / `newComputePipeline()` | 创建图形或计算管线对象。 |
| `newShaderResourceBindings()` | 创建 shader 资源绑定布局和值。 |
| `newSwapChain()` / `newTextureRenderTarget()` | 创建屏幕或离屏渲染目标。 |
| `nextResourceUpdateBatch()` | 获取资源上传/更新批次，在命令中提交。 |
| `isFeatureSupported()` | 查询实例化、计算、时间戳、VRS、几何着色器等功能。 |
| `resourceLimit()` | 查询最大纹理、颜色附件数、uniform buffer 范围等限制。 |
| `supportedSampleCounts()` | 查询可用 MSAA sample count。 |
| `isTextureFormatSupported()` | 查询某纹理格式/flag 是否可用。 |
| `clipSpaceCorrMatrix()` | 获取跨后端修正 clip space 差异的矩阵。 |
| `isYUpInNDC()` / `isYUpInFramebuffer()` / `isClipDepthZeroToOne()` | 查询坐标系与深度范围差异。 |
| `currentFrameSlot()` | 多帧飞行时的当前帧槽，用于环形资源。 |
| `pipelineCacheData()` / `setPipelineCacheData()` | 保存/恢复 pipeline cache，需后端和 flag 支持。 |
| `addCleanupCallback()` | 在 `QRhi` 销毁前清理依赖它的缓存资源。 |
| `nativeHandles()` / `makeThreadLocalNativeContextCurrent()` | 与底层图形 API 互操作。 |

## 4. 关键用法

### 典型帧结构

```cpp
if (rhi->beginFrame(swapChain) != QRhi::FrameOpSuccess)
    return;

QRhiCommandBuffer *cb = swapChain->currentFrameCommandBuffer();
QRhiResourceUpdateBatch *updates = rhi->nextResourceUpdateBatch();
updates->uploadStaticBuffer(vertexBuffer, vertexData);

cb->beginPass(swapChain->currentFrameRenderTarget(), clearColor, dsClear, updates);
cb->setGraphicsPipeline(pipeline);
cb->setShaderResources(srb);
cb->setVertexInput(0, { { vertexBuffer, 0 } });
cb->draw(vertexCount);
cb->endPass();

rhi->endFrame(swapChain);
```

RHI 的节奏是“开始帧、准备资源更新、录制命令、结束帧提交”。资源创建和 pipeline 创建通常在帧外完成，资源内容更新可以通过 `QRhiResourceUpdateBatch` 随 pass 或命令提交。

### 功能查询先行

```cpp
if (rhi->isFeatureSupported(QRhi::Compute)) {
    // 创建 compute pipeline 和 storage buffer
}
```

不要按桌面 GPU 的能力假设所有后端都支持同一功能。OpenGL ES、移动 Metal、D3D、Vulkan 的支持边界会不同。

### 处理 swapchain 失效和 device lost

```cpp
auto result = rhi->beginFrame(swapChain);
if (result == QRhi::FrameOpSwapChainOutOfDate) {
    swapChain->createOrResize();
    return;
}
if (result == QRhi::FrameOpDeviceLost) {
    recreateRhiAndResources();
    return;
}
```

窗口尺寸变化、表面重建、图形设备丢失都要作为正常路径处理。RHI 代码必须具备重建资源的能力。

## 5. 使用场景

- 自定义跨后端渲染引擎。
- Qt Quick/Scene Graph 相关底层扩展。
- 离屏 GPU 渲染、纹理生成、计算着色器处理。
- 需要统一支持 Vulkan/Metal/D3D/OpenGL 的库。
- 和原生图形 API 互操作但希望使用 Qt 的抽象层管理资源。

## 6. 常见坑与经验

- **这是私有 API。** `GuiPrivate` 意味着升级 Qt 时要重新验证编译和行为。
- **不要跳过 feature 查询。** RHI 是统一接口，不是统一硬件能力。
- **资源属于创建它的 `QRhi`。** `QRhi` 销毁后，资源指针和 native handles 都不再可用。
- **帧内不能随意销毁仍被命令引用的资源。** 用 `QRhiResource::deleteLater()` 或延迟释放策略。
- **坐标系差异真实存在。** Y 方向、clip depth、framebuffer 原点要用查询和校正矩阵处理。
- **`finish()` 很重。** 它会破坏 CPU/GPU 并行性，适合调试、测试或少量同步点。
- **pipeline cache 要显式启用并检查支持。** 不支持时相关函数可能返回空数据或无效果。
- **device lost 不是理论情况。** 驱动重置、窗口系统变化、外部 GPU 断开都可能触发。

## 7. 知识点覆盖

- RHI 后端、适配器、设备、swapchain 和命令缓冲区
- 帧生命周期、离屏帧和 present 控制
- GPU 资源创建、上传、延迟释放和缓存清理
- 功能查询、资源限制和跨后端可移植性
- 坐标系、clip space、MSAA、VRS、计算和高级 shader 阶段
- pipeline cache、native handle 互操作和 device lost 恢复
