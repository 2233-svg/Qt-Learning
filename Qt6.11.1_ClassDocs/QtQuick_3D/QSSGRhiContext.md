# QSSGRhiContext
> Qt 6.11.1 · Qt Quick 3D · 来自 `QSSGRhiContext`

## 1. 先建立直觉

`QSSGRhiContext` 是 Quick 3D 渲染时暴露给扩展使用的 RHI 上下文视图。它提供当前 `QRhi`、command buffer、render target、render pass descriptor、常用 sampler 和 dummy texture 等资源入口。

## 2. 类说明

保留类说明：这些 API 来自 `QSSGRhiContext`，属于 Qt Quick 3D 模块，用于让渲染扩展访问 Qt RHI 渲染资源。

这是渲染阶段对象，不应在 GUI 线程或跨帧无脑保存其中的临时指针。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `rhi()` | 当前 QRhi。 |
| `commandBuffer()` | 当前帧命令缓冲。 |
| `renderTarget()` | 当前渲染目标，可能是交换链或离屏纹理。 |
| `mainRenderPassDescriptor()` | 主 pass 的 render pass 描述。 |
| `mainPassSampleCount()` / `mainPassViewCount()` | MSAA 和 multiview 信息。 |
| `commonPassFlags()` | 常用 begin pass flags。 |
| `sampler(desc)` | 获取/复用 sampler。 |
| `dummyTexture(flags, rub, size, color, arraySize)` | 创建或取得占位纹理。 |
| `isValid()` | 判断上下文是否可用。 |

## 4. 常见坑与经验

render target 的含义取决于 View3D renderMode 和后处理链路。不要假设一定是屏幕 framebuffer。

QRhi 资源要遵循 RHI 生命周期。窗口重建、图形后端变化、设备丢失时，旧资源不能继续使用。

## 5. 知识点覆盖

- Qt RHI 与 Quick 3D 渲染扩展。
- command buffer、render target、render pass。
- sampler/dummy texture 管理和资源有效期。
