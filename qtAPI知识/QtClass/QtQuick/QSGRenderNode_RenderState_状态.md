# QSGRenderNode::RenderState：自定义绘制时读取场景图状态

> Qt 6.11.1 · `#include <QSGRenderNode>` · 模块：`Qt6::Quick`

`QSGRenderNode::RenderState` 是传给 `QSGRenderNode::render()` 的只读状态视图。它把 Qt Quick 已计算好的投影矩阵与裁剪信息交给自定义渲染代码，避免节点重新推导父级变换和裁剪树。

## 它解决的问题

自定义命令要和其他 QML Item 对齐时，需要正确的投影矩阵；要遵从祖先的 `clip` 时，需要在不同后端使用 scissor、stencil 或软件裁剪区域。`RenderState` 在绘制回调内提供这些后端相关细节。

对于一般 GPU 后端，顶点变换通常使用 `*state->projectionMatrix() * *node->matrix()`。对于软件后端，可能没有可用 scissor 或 stencil，而应该取 `clipRegion()`，在设置 Item 变换之前用 `QPainter::setClipRegion(..., Qt::ReplaceClip)` 应用该世界坐标区域。

## 生命周期边界

此对象只在当前 `render()` 调用期间有效，不能保存指针、缓存其返回的矩阵指针，或让异步任务稍后使用。当前后端不采用某种裁剪机制时，对应值可能无意义；应先检查 `scissorEnabled()`、`stencilEnabled()` 或空的 `clipRegion()`。

使用 stencil 时，Qt Quick 已填充必要的裁剪形状，但节点仍要按后端 pipeline 规则自行开启 stencil 测试，并使用文档要求的 `KEEP`、`EQUAL`、`0xFF` 读写掩码组合。

## API 速查表

| API | 语义与边界 |
|---|---|
| `projectionMatrix()` | 返回当前投影矩阵；与节点的 model-view 矩阵相乘得到最终顶点变换。 |
| `scissorEnabled()` | 判断当前裁剪是否通过 scissor 生效。 |
| `scissorRect()` | 返回当前 scissor 矩形；`x/y` 的原点在左下，不能按 QML 左上坐标直接解释。 |
| `stencilEnabled()` | 判断是否需要按当前裁剪使用 stencil 测试。 |
| `stencilValue()` | 返回裁剪活动时使用的 stencil reference 值。 |
| `clipRegion()` | 返回软件后端等使用的世界坐标 `QRegion`；scissor/stencil 后端通常返回空。 |
| `get(const char *state)` | 通过后端特有键查询额外状态；仅在该渲染回调内使用。 |
