# QQuick3DRenderExtension
> Qt 6.11.1 · Qt Quick 3D · 来自 `QQuick3DRenderExtension`

## 1. 先建立直觉

`QQuick3DRenderExtension` 是 QML/Quick 3D 对象侧的渲染扩展入口。它把你写的 C++ 扩展对象同步成渲染线程里的 `QSSGRenderExtension`，从而插入 Quick 3D 渲染流程。

## 2. 类说明

保留类说明：这些 API 来自 `QQuick3DRenderExtension`，属于 Qt Quick 3D 模块，用于把 QML 对象映射到渲染扩展节点。

真正渲染逻辑在返回的 `QSSGRenderExtension` 里；这个类负责对象生命周期和同步桥接。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `updateSpatialNode(node)` | 创建、更新或移除底层 `QSSGRenderExtension`。返回 null 会移除扩展。 |

## 4. 使用场景

| 场景 | 说明 |
| --- | --- |
| 自定义后处理/渲染 pass | 在渲染管线特定阶段插入代码。 |
| QML 暴露 C++ 渲染扩展 | QML 管属性，render extension 管 GPU 工作。 |
| 提供纹理给材质 | 派生 `QQuick3DTextureProviderExtension`。 |

## 5. 常见坑与经验

`updateSpatialNode()` 处在同步边界，不是随便调用 GUI API 的地方。把 QML 属性复制到渲染节点即可，重 GPU 操作放到 render extension 的渲染阶段。

返回已有 node 可以复用资源；每次都 new 会制造额外分配和资源重建。

## 6. 知识点覆盖

- QML 对象到渲染对象的同步。
- render extension 生命周期。
- GUI 线程与渲染线程边界。
