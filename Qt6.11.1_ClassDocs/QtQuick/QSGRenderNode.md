# QSGRenderNode
> Qt 6.11.1 · Qt Quick · 来自 `QSGRenderNode`

## 作用定位
`QSGRenderNode` 允许在 Scene Graph 中插入完全自定义的渲染命令，是比材质节点更低层的逃生口。它适用于已有渲染器必须直接录制命令的情况。

## API 速查
| API | 是做什么的 |
|---|---|
| `render()` | 录制实际渲染命令。|
| `changedStates()` | 告知 Qt Quick 你会改变哪些图形状态。|
| `flags()` | 声明节点特性，如深度感知等。|
| `rect()` | 提供节点覆盖的区域。|
| `prepare()` | 在 render 前准备资源。|
| `releaseResources()` | 场景图失效时释放资源。|

## 使用场景
第三方渲染库、特殊 GPU pass、需要直接使用当前命令缓冲或 render pass 的高级集成。

## 常见坑与经验
- 这是最锋利也最容易割到手的接口；普通几何和 shader 效果优先用 `QSGGeometryNode` 与 `QSGMaterial`。
- 必须准确声明 `changedStates()`，否则会污染 Qt Quick 后续绘制状态。
- 后端不同，`render()` 中能做的原生命令完全不同，必须结合 `QSGRendererInterface`。

## 知识点覆盖
低层渲染插入、图形状态隔离、资源释放、后端互操作、render pass。
