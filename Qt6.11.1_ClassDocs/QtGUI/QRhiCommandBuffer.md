# QRhiCommandBuffer

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiCommandBuffer`

## 1. 先建立直觉

`QRhiCommandBuffer` 是 RHI 中记录 GPU 命令的对象。创建资源只是准备材料，pipeline 只是描述状态，真正把“清屏、绑定管线、绑定资源、设置顶点输入、draw、dispatch、回读/上传”串成一帧的，是 command buffer。

它是顺序敏感的：图形命令必须在 `beginPass()` / `endPass()` 之间，计算命令必须在 `beginComputePass()` / `endComputePass()` 之间；设置 pipeline 后再设置相关状态和资源；外部原生 API 命令必须用 `beginExternal()` / `endExternal()` 包起来。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 继承自：`QRhiResource`
- 获取方式：通常来自当前 swapchain frame 或 offscreen frame
- 命令类型：graphics pass、compute pass、resource update、debug markers、external native commands

不要假设不同 pass 之间状态会自动保留。跨 pass、跨 frame 时应重新绑定必要的 pipeline、shader resources、vertex input、viewport/scissor 等状态。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `beginPass(rt, clearColor, dsClear, updates, flags)` | 开始图形渲染通道，指定 render target 和清除值。 |
| `endPass(updates)` | 结束图形 pass，可提交额外资源更新。 |
| `beginComputePass(updates, flags)` | 开始计算 pass。 |
| `endComputePass(updates)` | 结束计算 pass。 |
| `resourceUpdate(updates)` | 在 pass 外提交资源更新批次。 |
| `setGraphicsPipeline()` | 绑定图形 pipeline。 |
| `setComputePipeline()` | 绑定计算 pipeline。 |
| `setShaderResources()` | 绑定 shader resource bindings，可带 dynamic offsets。 |
| `setVertexInput()` | 绑定顶点 buffer 和可选 index buffer。 |
| `setViewport()` / `setScissor()` | 设置动态 viewport / scissor。 |
| `setBlendConstants()` / `setStencilRef()` | 设置 pipeline 声明使用的动态状态。 |
| `setShadingRate()` | Qt 6.9 起设置可变速率着色粒度。 |
| `draw()` | 非索引绘制。 |
| `drawIndexed()` | 索引绘制。 |
| `dispatch()` | 调度计算工作组。 |
| `debugMarkBegin/End/Msg()` | 写入 GPU 调试标记。 |
| `beginExternal()` / `endExternal()` | 在 pass 内安全插入底层图形 API 命令。 |
| `nativeHandles()` | 获取后端命令缓冲原生句柄，后端相关。 |
| `lastCompletedGpuTime()` | 查询已完成帧 GPU 时间，需时间戳支持/启用。 |

## 4. 关键用法

### 图形 pass 的最小顺序

```cpp
cb->beginPass(rt, QColor(Qt::black), { 1.0f, 0 }, updates);
cb->setGraphicsPipeline(ps);
cb->setShaderResources(srb);
cb->setViewport(QRhiViewport(0, 0, w, h));
cb->setVertexInput(0, 1, vertexInputs, indexBuffer);
cb->drawIndexed(indexCount);
cb->endPass();
```

`setViewport()` 通常是动态状态；pipeline、shader resources、vertex input 都要在 draw 前设置。不同后端对未绑定状态的容错不同，不要依赖默认状态。

### 计算 pass

```cpp
cb->beginComputePass(updates);
cb->setComputePipeline(computePipeline);
cb->setShaderResources(computeSrb);
cb->dispatch(groupsX, groupsY, 1);
cb->endComputePass();
```

计算需要 `QRhi::Compute` 功能支持。`dispatch()` 的工作组数量还要遵守 `resourceLimit()` 查询到的限制，以及着色器 local size 的乘积限制。

### 原生命令互操作

```cpp
cb->beginPass(rt, clear, ds, nullptr, QRhiCommandBuffer::ExternalContent);
cb->beginExternal();
auto handles = cb->nativeHandles();
// 使用底层 API 记录命令
cb->endExternal();
cb->endPass();
```

`beginExternal()` 后到 `endExternal()` 前不要再调用 RHI 的 `set*` / `draw*`。结束 external 后，RHI 状态应视为失效，需要重新绑定。

## 5. 使用场景

- 录制每帧图形绘制命令。
- 执行 compute shader 数据处理。
- 上传 buffer/texture、回读 GPU 数据。
- 插入 GPU 调试标记和性能测量。
- 在 Qt RHI pass 中嵌入少量原生 API 命令。

## 6. 常见坑与经验

- **命令必须在正确 pass 中。** `draw()` 只能在 render pass 内，`dispatch()` 只能在 compute pass 内。
- **pass 之间状态不保留。** 每个 pass 重新绑定必要状态。
- **pipeline 影响后续状态合法性。** 没有绑定合适 pipeline 就 draw，行为后端相关且不可靠。
- **dynamic offset 要匹配 SRB layout。** binding 编号和 offset 对齐都要正确。
- **`firstInstance`、`baseVertex` 并非所有后端都支持。** 先查 `BaseInstance`、`BaseVertex` 等 feature。
- **外部命令会破坏 RHI 状态假设。** `endExternal()` 后重新设置 pipeline/resources/vertex input。
- **GPU 时间戳异步且不可跨硬件比较。** `lastCompletedGpuTime()` 适合本机诊断，不适合绝对性能排行。

## 7. 知识点覆盖

- command buffer 的顺序录制模型
- render pass、compute pass 和 resource update
- pipeline、shader resources、vertex input、viewport/scissor 动态状态
- draw/drawIndexed/dispatch 的参数和后端功能限制
- debug markers、GPU timestamps 和 native handles
- 外部图形 API 命令插入的状态边界
