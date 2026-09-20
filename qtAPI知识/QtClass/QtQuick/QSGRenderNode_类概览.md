# QSGRenderNode：把自定义 GPU 绘制嵌入 Qt Quick 场景图

> Qt 6.11.1 · `#include <QSGRenderNode>` · 模块：`Qt6::Quick` · 继承：`QSGNode`

`QSGRenderNode` 是自定义绘制的逃生舱口：当 `QSGGeometryNode` 和材质不足以描述需求时，它允许实现类直接向 Qt Quick 当前的图形后端记录绘制命令，同时仍参与 Item 的变换、透明度、裁剪和堆叠。

## 适用场景

已有 QRhi/Vulkan/Metal/Direct3D 渲染器需要嵌入 QML、需要特殊 pipeline 或第三方库命令，而又必须和普通 Qt Quick 内容正确叠加时，派生 `QSGRenderNode`。最小实现必须覆写 `render()`；资源上传、复制等不能在 render pass 内做的操作，则放进 `prepare()`。

```cpp
void MyRenderNode::prepare()
{
    // 在 render pass 开始前更新缓冲、上传或准备 pipeline。
}

void MyRenderNode::render(const RenderState *state)
{
    const QMatrix4x4 mvp = *state->projectionMatrix() * *matrix();
    // 使用 commandBuffer() 向 Qt Quick 当前目标记录绘制命令。
}
```

## 状态、坐标和资源重建

进入 `render()` 时，不能假设 OpenGL 或任何原生 API 的 pipeline、scissor、深度等状态是什么，即使当前后端恰好是 OpenGL。应完整绑定自己需要的 pipeline 与动态状态。顶点坐标遵循 Item 坐标系：左上为 `(0, 0)`；`projectionMatrix() * matrix()` 才是正确的最终变换，`inheritedOpacity()` 是累积后的透明度。

裁剪由 `RenderState` 提供。若是 scissor/stencil 后端，节点有责任启用对应测试；软件后端可能仅给出 `QRegion`。`releaseResources()` 必须释放所有自行创建的 GPU 资源，并让后续 `render()` 能重建它们，因为设备丢失会触发该路径；析构函数也要做同类清理，因为部分后端可能不调用前者。

## 性能声明

`BoundedRectRendering` 与准确的 `rect()` 能让软件后端继续局部更新；错误声称边界或全不透明会造成渲染错误。若完全使用 QRhi 而不直接调用原生 3D API，可声明 `NoExternalRendering`。Qt 6 中 `changedStates()` 的实际作用很有限，QRhi 后端通常只有 viewport 和 scissor 声明有意义。

## API 速查表

| API | 语义与边界 |
|---|---|
| `render(const RenderState *state)` | 纯虚函数；在当前帧 render pass 中记录本节点绘制命令。 |
| `prepare()` | 每次 `render()` 前调用，发生在当前 render pass 开始前；适合上传、复制、准备资源。 |
| `releaseResources()` | 立即释放自建 GPU 资源；之后 `render()` 必须可重新创建资源。 |
| `changedStates()` | 返回 `render()` 改动的图形状态；Qt 6 QRhi 路径通常仅 viewport、scissor 有实际意义。 |
| `flags()` | 返回渲染行为声明，默认无标志。 |
| `rect()` | 在 `BoundedRectRendering` 时返回 Item 坐标中的准确影响区域。 |
| `matrix()` | 返回当前 model-view 矩阵指针。 |
| `projectionMatrix()` | Qt 6.5 起返回投影矩阵，`prepare()` 也可查询。 |
| `inheritedOpacity()` | 返回祖先透明度累计后的有效值。 |
| `clipList()` | 返回当前裁剪节点链；复杂裁剪优先使用 `RenderState` 的具体数据。 |
| `commandBuffer()` | Qt 6.6 起返回当前 `QRhiCommandBuffer`。 |
| `renderTarget()` | Qt 6.6 起返回当前 `QRhiRenderTarget`；目标变化时可能导致已有 pipeline 不兼容。 |
| `BoundedRectRendering` | 声明不会绘制到 `rect()` 外；可保留局部更新优化。 |
| `DepthAwareRendering` | 声明只生成符合场景图预期的深度值，有助于特定后端优化。 |
| `OpaqueRendering` | 仅在整个 `rect()` 确实写入不透明像素时声明。 |
| `NoExternalRendering` | 声明 `prepare()`/`render()` 仅使用 QRhi，而不直接调用原生图形 API。 |
