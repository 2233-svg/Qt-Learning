# QRhiComputePipeline

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiComputePipeline`

## 1. 先建立直觉

`QRhiComputePipeline` 描述一次 compute shader 执行所需的固定状态：一个计算着色器阶段、一套 shader resource binding 布局，以及少量编译选项。它不像 graphics pipeline 那样有顶点输入、光栅化、深度模板、混合和 render pass；它的核心就是“这个 compute shader 以什么资源布局运行”。

真正执行发生在 `QRhiCommandBuffer::beginComputePass()` 之后：绑定 compute pipeline，绑定 layout 兼容的 `QRhiShaderResourceBindings`，然后 `dispatch(x, y, z)`。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 继承自：`QRhiResource`
- 创建入口：`QRhi::newComputePipeline()`
- 必需条件：`QRhi::Compute` 功能支持

`QRhiComputePipeline` 引用的 SRB 可以只作为布局，也可以包含实际资源。实际 dispatch 时通过 command buffer 绑定的 SRB 只要 layout-compatible，就可以替换具体 buffer/texture。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setShaderStage()` / `shaderStage()` | 设置/读取计算着色器阶段；只能是 compute stage。 |
| `setShaderResourceBindings()` / `shaderResourceBindings()` | 设置/读取资源绑定布局。 |
| `setFlags()` / `flags()` | 设置编译选项，如请求 shader debug info。 |
| `CompileShadersWithDebugInfo` | 请求运行时编译时保留调试信息，后端支持时利于 RenderDoc 等工具调试。 |
| `resourceType()` | 返回 `QRhiResource::ComputePipeline`。 |

## 4. 关键用法

```cpp
QRhiComputePipeline *ps = rhi->newComputePipeline();
ps->setShaderStage(QRhiShaderStage(QRhiShaderStage::Compute, computeShader));
ps->setShaderResourceBindings(computeSrbLayout);
ps->create();

cb->beginComputePass(updates);
cb->setComputePipeline(ps);
cb->setShaderResources(computeSrb);
cb->dispatch(groupsX, groupsY, groupsZ);
cb->endComputePass();
```

`computeSrb` 可以和 `computeSrbLayout` 不是同一个对象，但 binding 集合、类型、stage visibility 等必须兼容。

## 5. 使用场景

- GPU 粒子更新、前缀和、裁剪、排序等并行计算。
- 图像处理：滤镜、mipmap/预处理、色彩转换。
- Storage buffer 或 storage image 的读写。
- 离屏渲染前的 GPU 数据生成。
- 与 graphics pass 共享 buffer/texture 的混合工作流。

## 6. 常见坑与经验

- **先查 `QRhi::Compute`。** 某些后端/设备不支持 compute，尤其旧 OpenGL ES。
- **shader stage 必须是 compute。** 顶点/片段 shader 不能放进 compute pipeline。
- **SRB layout 要兼容。** pipeline 创建时的 SRB 与 dispatch 时绑定的 SRB 必须布局一致。
- **dispatch 参数不是像素数。** 它是工作组数量，具体线程数还要乘以 shader 中的 local size。
- **resource barrier 由 RHI 管，但依赖仍要清晰。** 同一帧图形/计算读写同一资源时，pass 顺序和 usage 必须合理。
- **调试信息可能有成本。** `CompileShadersWithDebugInfo` 适合调试构建，不应无脑开在生产路径。

## 7. 知识点覆盖

- compute pipeline 与 graphics pipeline 的差异
- compute shader stage、SRB layout、dispatch 工作组
- storage buffer/image 与资源读写
- 后端 compute feature 查询
- shader debug info 和 GPU 调试工具
