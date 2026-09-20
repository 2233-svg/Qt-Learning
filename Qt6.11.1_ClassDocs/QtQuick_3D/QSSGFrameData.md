# QSSGFrameData
> Qt 6.11.1 · Qt Quick 3D · 来自 `QSSGFrameData`

## 1. 先建立直觉

`QSSGFrameData` 是渲染扩展每帧拿到的上下文数据包。它让扩展访问当前帧的渲染上下文、相机、视口、时间和内部渲染信息。

## 2. 类说明

保留类说明：这些 API 来自 `QSSGFrameData`，属于 Qt Quick 3D 模块，用于向渲染扩展传递当前帧状态。

它不是长期保存的数据模型，而是帧回调期间使用的临时视图。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `renderer()` / `renderContext()` | 访问当前渲染器或上下文接口。 |
| `camera()` / `cameraId()` | 获取当前相机信息。 |
| `viewport()` / `scissorRect()` | 当前渲染区域。 |
| `time()` / `deltaTime()` | 当前帧时间信息。 |
| `rhiContext()` | 间接访问 RHI 相关资源。 |

## 4. 使用场景

| 场景 | 说明 |
| --- | --- |
| 渲染扩展读取当前相机 | 做屏幕空间效果或调试绘制。 |
| 根据视口创建纹理 | 离屏纹理尺寸跟随 View3D。 |
| 帧时间驱动动画 | GPU 扩展根据 time 更新。 |

## 5. 常见坑与经验

不要跨帧保存 `QSSGFrameData` 或其中易失指针。需要长期状态时，把数据复制到自己的扩展对象里。

frame data 描述当前渲染阶段，不代表你可以随意改 scene graph 对象。

## 6. 知识点覆盖

- 渲染扩展的每帧上下文。
- 相机、视口、时间和 RHI 访问。
- 临时数据与长期状态分离。
