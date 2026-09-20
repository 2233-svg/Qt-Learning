# QRhiGraphicsPipeline

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiGraphicsPipeline`

## 1. 先建立直觉

`QRhiGraphicsPipeline` 是一次图形绘制的大部分固定状态集合：shader stages、顶点输入布局、拓扑、剔除、正面绕序、深度/模板、混合、采样数、render pass 兼容性等。绑定 pipeline 后，`QRhiCommandBuffer` 才知道后续 draw 应该按什么规则解释顶点并写入 render target。

它和 OpenGL 时代“到处 set state”不同，更接近现代图形 API 的 pipeline state object。很多状态必须在 `create()` 前确定；而 viewport、scissor、blend constants、stencil ref、shading rate 等少数状态由 command buffer 动态设置，并且通常要在 flags 中声明。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 继承自：`QRhiResource`
- 创建入口：`QRhi::newGraphicsPipeline()`
- 使用入口：`QRhiCommandBuffer::setGraphicsPipeline()`
- 必需协作：`QRhiRenderPassDescriptor`、`QRhiShaderResourceBindings`、`QRhiVertexInputLayout`

pipeline 与 render pass descriptor、sample count、shader resource bindings layout 等强相关。render target 重建、MSAA 改变、附件格式改变时，经常需要重新创建 pipeline 或至少验证兼容性。

## 3. API 速查

| API 族 | 作用 |
| --- | --- |
| `setShaderStages()` | 设置顶点、片段以及可选几何/细分 shader 阶段。 |
| `setShaderResourceBindings()` | 设置 shader 资源绑定布局。 |
| `setVertexInputLayout()` | 描述顶点 buffer binding、attribute location、格式和步进率。 |
| `setTopology()` | 设置图元拓扑，如 triangles、lines、patches。 |
| `setRenderPassDescriptor()` | 指定与 render target 兼容的 render pass 描述。 |
| `setSampleCount()` | 设置 MSAA sample count，必须匹配 render target。 |
| `setCullMode()` / `setFrontFace()` | 控制背面/正面剔除和绕序。 |
| `setPolygonMode()` | 设置填充或线框；线框需要 `NonFillPolygonMode` 支持。 |
| `setDepthTest()` / `setDepthWrite()` / `setDepthOp()` | 控制深度测试、写入和比较函数。 |
| `setDepthBias()` / `setSlopeScaledDepthBias()` | 控制深度偏移，常用于 shadow map。 |
| `setDepthClamp()` | Qt 6.11 起启用深度钳制，需要 `DepthClamp` 支持。 |
| `setStencilTest()` / `setStencilFront()` / `setStencilBack()` | 控制模板测试和正反面模板操作。 |
| `setTargetBlends()` | 为颜色附件设置混合和颜色写入 mask。 |
| `setFlags()` | 声明动态状态或编译选项。 |
| `create()` | 创建底层 pipeline state；失败返回 `false`。 |
| `multiViewCount()` / `setMultiViewCount()` | Qt 6.7 起设置多视图 pipeline 视图数。 |
| `setPatchControlPointCount()` | 细分 patch 拓扑使用的控制点数。 |

## 4. 关键用法

### 最小图形 pipeline

```cpp
QRhiGraphicsPipeline *ps = rhi->newGraphicsPipeline();
ps->setShaderStages({
    { QRhiShaderStage::Vertex, vertexShader },
    { QRhiShaderStage::Fragment, fragmentShader }
});
ps->setVertexInputLayout(inputLayout);
ps->setShaderResourceBindings(srbLayout);
ps->setRenderPassDescriptor(rt->renderPassDescriptor());
ps->setSampleCount(rt->sampleCount());
ps->setTopology(QRhiGraphicsPipeline::Triangles);
ps->create();
```

创建时就要提供 render pass descriptor，因为不同后端需要知道颜色/深度附件格式、sample count 等信息来构建 pipeline。

### 动态状态要声明也要设置

```cpp
ps->setFlags(QRhiGraphicsPipeline::UsesScissor
             | QRhiGraphicsPipeline::UsesBlendConstants);

cb->setGraphicsPipeline(ps);
cb->setScissor(QRhiScissor(0, 0, w, h));
cb->setBlendConstants(QColor(255, 255, 255, 128));
```

如果 pipeline 没声明对应 flag，却在 command buffer 设置动态状态，底层后端行为可能不一致。

### 透明混合

```cpp
QRhiGraphicsPipeline::TargetBlend blend;
blend.enable = true;
blend.srcColor = QRhiGraphicsPipeline::SrcAlpha;
blend.dstColor = QRhiGraphicsPipeline::OneMinusSrcAlpha;
blend.srcAlpha = QRhiGraphicsPipeline::One;
blend.dstAlpha = QRhiGraphicsPipeline::OneMinusSrcAlpha;
ps->setTargetBlends({ blend });
```

多 render target 场景中，每个颜色附件可以有自己的 blend 设置，前提是后端支持 per-render-target blending。

## 5. 使用场景

- 标准 3D/2D draw pipeline。
- 多材质、多 shader 变体管理。
- 深度测试、模板轮廓、透明混合、线框渲染。
- MSAA、多视图、VRS、细分或几何着色器等高级路径。
- 离屏 render target 与 swapchain render target 的 pipeline 变体。

## 6. 常见坑与经验

- **pipeline 不是临时状态包。** 创建成本可能较高，应缓存复用。
- **render pass descriptor 必须兼容。** 附件格式、sample count、视图数变化会影响 pipeline 可用性。
- **动态状态要用 flags 声明。** scissor、blend constants、stencil ref、shading rate 不是无条件动态。
- **vertex input layout 要匹配 shader location。** attribute location、格式、offset、stride 错一点就会读错。
- **线框、宽线、base instance 等能力要查询。** 不同后端支持差异明显。
- **depth/stencil 状态要和 clear value/资源格式配套。** 没有深度附件却开启深度测试没有意义。
- **shader resource bindings 是布局契约。** draw 时绑定的 SRB 可以换资源，但 layout 必须兼容 pipeline。

## 7. 知识点覆盖

- 现代图形 pipeline state object 思路
- shader stages、vertex input、topology 和 draw 调用关系
- rasterization、culling、front face、polygon mode
- depth/stencil test、bias、clamp 和 stencil operations
- color blending、write mask、MRT 与动态 blend constants
- render pass compatibility、MSAA、多视图和 pipeline 缓存
