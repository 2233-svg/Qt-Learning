# QSSGRenderExtension
> Qt 6.11.1 · Qt Quick 3D · 来自 `QSSGRenderExtension`

## 1. 先建立直觉

`QSSGRenderExtension` 是真正运行在 Quick 3D 渲染流程里的扩展对象。它可以声明在哪个阶段运行、用什么模式运行，并在每帧准备数据、准备渲染、执行渲染和重置状态。

## 2. 类说明

保留类说明：这些 API 来自 `QSSGRenderExtension`，属于 Qt Quick 3D 模块，用于扩展 Quick 3D 渲染管线。

它不是 QML 对象；通常由 `QQuick3DRenderExtension::updateSpatialNode()` 创建或更新。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `stage()` | 返回扩展插入的渲染阶段。 |
| `mode()` | 返回渲染模式，决定扩展如何参与管线。 |
| `prepareData(frameData)` | CPU/同步阶段准备数据，可返回是否继续。 |
| `prepareRender(frameData)` | 渲染前准备 GPU 资源或状态。 |
| `render(frameData)` | 执行自定义渲染。 |
| `resetForFrame()` | 每帧结束后重置临时状态。 |

## 4. 使用场景

| 场景 | 说明 |
| --- | --- |
| 插入自定义 render pass | 在 Quick 3D 既有管线中加工作。 |
| 生成纹理或调试可视化 | 结合 RHI context 写入资源。 |
| 与内部模型/相机数据协作 | 通过 frameData 和 helper 查询渲染信息。 |

## 5. 常见坑与经验

这里的代码处在渲染管线内，不能按普通 QObject/UI 思维写。不要阻塞，不要访问 GUI 对象，不要跨帧保存易失的 command buffer 指针。

每个后端都通过 RHI 抽象，避免写死 OpenGL/Vulkan 假设。需要原生 API 时要非常谨慎。

## 6. 知识点覆盖

- Quick 3D 渲染扩展生命周期。
- stage/mode/prepare/render/reset。
- RHI 资源和渲染线程边界。
