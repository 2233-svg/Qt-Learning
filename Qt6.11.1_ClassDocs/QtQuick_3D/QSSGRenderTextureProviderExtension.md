# QSSGRenderTextureProviderExtension
> Qt 6.11.1 · Qt Quick 3D · 来自 `QSSGRenderTextureProviderExtension`

## 1. 先建立直觉

`QSSGRenderTextureProviderExtension` 是渲染侧的纹理提供扩展。它的任务是让自定义渲染流程产生的纹理能被 Quick 3D 其它部分使用。

## 2. 类说明

保留类说明：这些 API 来自 `QSSGRenderTextureProviderExtension`，属于 Qt Quick 3D 模块，用于在渲染管线中提供纹理资源。

它继承 `QSSGRenderExtension`，因此同样遵循 prepare/render/reset 的帧生命周期。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| 继承的 `stage()` / `mode()` | 决定纹理生成发生在哪个阶段。 |
| 继承的 `prepareData()` | 准备 CPU 侧数据。 |
| 继承的 `prepareRender()` | 创建或更新纹理资源。 |
| 继承的 `render()` | 执行实际渲染到纹理。 |
| 继承的 `resetForFrame()` | 每帧清理临时状态。 |

## 4. 使用场景

| 场景 | 说明 |
| --- | --- |
| GPU 生成程序纹理 | 噪声、mask、数据纹理。 |
| 离屏渲染结果接入材质 | 自定义 pass 输出供场景采样。 |
| 外部渲染桥接 | 把另一套渲染结果作为 Quick 3D 纹理。 |

## 5. 常见坑与经验

纹理尺寸、格式、采样器和 render pass 要与消费者匹配。只“有一个 QRhiTexture”不够，还要明确 layout、usage 和更新时机。

设备丢失或窗口重建时，所有 RHI 资源都可能需要重建。

## 6. 知识点覆盖

- 渲染侧纹理 provider。
- RHI 纹理资源生成和消费。
- 离屏渲染与材质采样边界。
