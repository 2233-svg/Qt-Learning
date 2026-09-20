# QRhiTextureRenderTarget
> Qt 6.11.1 · Qt GUI [Private] · 来自 `QRhiTextureRenderTarget`

## 1. 先建立直觉

`QRhiTextureRenderTarget` 是把一组纹理或渲染缓冲区组织成“可以被开始一次 render pass 的目标”的对象。它不是纹理本身，也不是 pipeline；它更像一次离屏渲染通道的落点说明：颜色写到哪些附件，深度模板用哪里，开始时要不要保留旧内容。

它属于 RHI 私有接口，需要 `Qt6::GuiPrivate`。这类 API 很适合写 Qt 内部风格的渲染器、嵌入自定义 scene graph、做离屏 pass、后处理、阴影图或 G-buffer；但它不承诺像公开 Qt API 那样稳定。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)`
- 继承：`QRhiRenderTarget`
- 典型创建者：`QRhi::newTextureRenderTarget()`
- 协作类：`QRhiTextureRenderTargetDescription`、`QRhiColorAttachment`、`QRhiRenderPassDescriptor`、`QRhiGraphicsPipeline`

这个类的核心规则是：先把 `description` 和 `flags` 定好，再生成兼容的 render pass descriptor，最后 `create()`。pipeline 也必须使用兼容的 render pass descriptor，否则命令录制阶段可能失败或在后端验证层里报错。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `create()` | 创建或重建底层图形资源；要求已设置 render pass descriptor |
| `setDescription(desc)` / `description()` | 设置或读取颜色、深度、resolve、VRS 等附件组合 |
| `setFlags(f)` / `flags()` | 控制附件开始和结束时的 load/store 策略 |
| `newCompatibleRenderPassDescriptor()` | 基于当前描述生成与目标、pipeline 兼容的 render pass descriptor |
| `resourceType()` | 返回 RHI 资源类型，主要给框架和调试使用 |
| `PreserveColorContents` | 开始渲染时保留颜色附件旧内容 |
| `PreserveDepthStencilContents` | 深度纹理作为附件时，开始渲染保留旧深度/模板 |
| `DoNotStoreDepthStencilContents` | 结束渲染时不写回深度/模板纹理内容 |

## 4. 关键用法

标准离屏 pass 通常这样组织：

```cpp
QRhiTextureRenderTargetDescription desc(
    QRhiColorAttachment(colorTexture),
    depthStencilBuffer);

QRhiTextureRenderTarget *rt = rhi->newTextureRenderTarget(desc);
QRhiRenderPassDescriptor *rp = rt->newCompatibleRenderPassDescriptor();
rt->setRenderPassDescriptor(rp);

if (!rt->create())
    return;

pipeline->setRenderPassDescriptor(rp);
pipeline->create();
```

顺序很重要。`newCompatibleRenderPassDescriptor()` 读取的是当前 `description()` 与 `flags()`，所以如果后续改了附件数量、格式、sample count、shading rate map 或 load/store 标志，就要重新取得 descriptor，并连带重建使用它的 graphics pipeline。

多个 render target 只要附件数量、类型、格式、sample count 和相关 flags 兼容，可以共享同一个 `QRhiRenderPassDescriptor`。这对 ping-pong blur、双缓冲离屏纹理、每帧重建目标对象的场景很有价值。

## 5. 使用场景

- 后处理链：第一 pass 渲染到纹理，后续 pass 把该纹理作为 shader resource。
- 阴影图或深度预通道：只关心深度附件，颜色附件可以减少或省略，取决于实际 pass。
- 多渲染目标：一次 fragment shader 写入 albedo、normal、material 等多个颜色附件。
- MSAA 离屏渲染：颜色附件和 resolve texture 组合使用，结束 pass 后得到单采样纹理。
- Qt Quick 或自定义渲染嵌入：把 RHI 资源接到 Qt 的渲染循环里。

## 6. 常见坑与经验

- `description()` 里引用的 `QRhiTexture`、`QRhiRenderBuffer` 必须已经 `create()`；target 只是引用它们，不负责替你创建。
- `PreserveColorContents` 在 tile-based GPU 上可能代价明显，因为它迫使驱动加载旧 tile 内容。只有真的需要叠加旧画面时再开。
- MSAA 场景不要把 `PreserveColorContents` 当成跨后端可靠的“保留多采样中间数据”机制，有些 OpenGL ES 扩展里的多采样存储是隐式的。
- 深度数据只是测试用时优先用 `QRhiRenderBuffer`；需要后续采样或多视图时才选择 depth texture。
- render pass descriptor 不是“随便共享”的标签，它是 pipeline 兼容性的一部分。改附件形态后忘了重建 pipeline 是 RHI 代码里很常见的隐性错误。

## 7. 知识点覆盖

掌握本类时应同时理解：RHI 私有 API 风险、离屏渲染、render pass descriptor 兼容性、颜色/深度/模板附件、MSAA resolve、load/store 操作、tile GPU 性能、pipeline 与 render target 的绑定关系。
