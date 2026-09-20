# QQuick3DTextureProviderExtension
> Qt 6.11.1 · Qt Quick 3D · 来自 `QQuick3DTextureProviderExtension`

## 1. 先建立直觉

`QQuick3DTextureProviderExtension` 是 QML 对象侧的“自定义纹理提供者”扩展。它让 C++ 渲染扩展生成或暴露纹理，供 Quick 3D 材质、效果或场景使用。

## 2. 类说明

保留类说明：这些 API 来自 `QQuick3DTextureProviderExtension`，属于 Qt Quick 3D 模块，用于把自定义渲染纹理提供给 Quick 3D。

它继承 `QQuick3DRenderExtension`，底层通常配合 `QSSGRenderTextureProviderExtension`。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `textureProvider()` | 返回与该扩展关联的纹理 provider。 |
| `updateSpatialNode(node)` | 同步底层纹理提供扩展。 |

## 4. 使用场景

| 场景 | 说明 |
| --- | --- |
| 自定义 GPU 渲染结果作为贴图 | 例如程序生成的渲染纹理。 |
| 与外部渲染系统桥接 | 将外部结果接入 Quick 3D。 |
| 后处理链路中共享中间纹理 | 供材质或 pass 消费。 |

## 5. 常见坑与经验

纹理资源的生命周期必须和 render context 对齐。窗口失效、设备丢失或后端切换时，要能重建。

纹理提供者不是 CPU 图片数据容器；CPU 侧原始纹理数据更适合 `QQuick3DTextureData`。

## 6. 知识点覆盖

- 自定义纹理 provider。
- QML 扩展对象和底层 render texture provider。
- GPU 纹理生命周期。
