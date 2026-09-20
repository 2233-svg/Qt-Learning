# QRhiRenderBuffer

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiRenderBuffer`

## 1. 先建立直觉

`QRhiRenderBuffer` 是只能作为渲染附件使用的 GPU 资源，常用于深度/模板附件或多采样颜色附件。和 `QRhiTexture` 不同，render buffer 通常不能在 shader 中采样；它更像“给 render pass 写入用的临时缓冲”。

如果渲染结果后面要作为纹理采样，用 `QRhiTexture`；如果只是需要 depth/stencil，或者 MSAA 中间颜色缓冲并会 resolve 到纹理，`QRhiRenderBuffer` 往往更合适。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 继承自：`QRhiResource`
- 创建入口：`QRhi::newRenderBuffer(type, size, sampleCount, flags, backingFormatHint)`
- 类型：`DepthStencil` 或 `Color`

render buffer 的大小、sample count、类型和 flag 必须在 `create()` 前设置。资源改变后要重新创建。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `Type::DepthStencil` | 深度/模板附件。 |
| `Type::Color` | 颜色附件，常用于 MSAA 中间缓冲。 |
| `UsedWithSwapChainOnly` | 表示仅与 swapchain 使用，常让后端自动管理大小和平台缓冲。 |
| `create()` | 创建底层 render buffer。 |
| `createFrom(NativeRenderBuffer)` | 导入原生 render buffer，目前主要是 OpenGL 特殊场景。 |
| `setPixelSize()` / `pixelSize()` | 设置/读取像素尺寸。 |
| `setSampleCount()` / `sampleCount()` | 设置/读取 MSAA sample count。 |
| `setType()` / `type()` | 设置/读取 render buffer 类型。 |
| `setFlags()` / `flags()` | 设置/读取标志。 |
| `resourceType()` | 返回 `QRhiResource::RenderBuffer`。 |

## 4. 关键用法

### 深度模板附件

```cpp
QRhiRenderBuffer *ds = rhi->newRenderBuffer(QRhiRenderBuffer::DepthStencil,
                                            size,
                                            sampleCount);
ds->create();
```

如果你不需要在 shader 里读取深度，render buffer 比深度纹理更直接，也可能更高效。

### swapchain 专用 depth/stencil

```cpp
QRhiRenderBuffer *ds = rhi->newRenderBuffer(
    QRhiRenderBuffer::DepthStencil,
    QSize(),
    sampleCount,
    QRhiRenderBuffer::UsedWithSwapChainOnly);
```

该 flag 表示资源只随 swapchain 使用，某些后端可借助窗口系统已有 depth/stencil 缓冲并自动随 swapchain resize。

## 5. 使用场景

- swapchain 或离屏 render target 的 depth/stencil 附件。
- MSAA color render buffer，再 resolve 到 texture。
- 不需要采样的临时渲染附件。
- OpenGL 外部 renderbuffer 导入到 RHI。

## 6. 常见坑与经验

- **render buffer 不能当普通纹理采样。** 后续要读结果就用 texture 或 resolve texture。
- **size/sampleCount 要匹配 render target。** 不匹配会导致 create 或 pass 失败。
- **`UsedWithSwapChainOnly` 不适合离屏复用。** 它表达的是 swapchain 专用生命周期。
- **`createFrom()` 不拥有 native 对象。** 外部对象生命周期由调用方保证。
- **导入功能后端有限。** 只有 `RenderBufferImport` 支持时才可用，且目前主要面向 OpenGL。
- **修改属性后要重新创建。** 改尺寸或 sample count 不会自动更新底层资源。

## 7. 知识点覆盖

- render buffer 与 texture render target 的区别
- depth/stencil、MSAA、resolve 工作流
- swapchain 专用附件和自动 resize
- native renderbuffer 导入的所有权边界
