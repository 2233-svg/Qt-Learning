# QQuickFramebufferObject
> Qt 6.11.1 · Qt Quick · 来自 `QQuickFramebufferObject`

## 作用定位
`QQuickFramebufferObject` 是将 OpenGL FBO 渲染嵌入 Qt Quick 的旧式专用项。其 renderer 将内容画入离屏 framebuffer，Qt Quick 再把结果作为纹理合成。

## 类说明
该类依赖 OpenGL 后端。Qt 6 的默认渲染可使用 Vulkan、Metal 或 Direct3D，新增跨平台渲染应优先选择 `QQuickRhiItem`。

## API 速查
| API | 是做什么的 |
|---|---|
| `createRenderer()` | 必须重实现，返回 FBO renderer。|
| `setMirrorVertically()` | 修正 OpenGL 纹理坐标的垂直方向。|
| `isTextureProvider()` | 作为纹理提供者供其他 QML 项使用。|
| `textureProvider()` | 获取输出纹理 provider。|

## 使用场景
已有成熟 OpenGL 绘制代码，且应用明确固定 OpenGL 后端时，可用它做逐步迁移或局部集成。

## 常见坑与经验
- 如果 Qt Quick 运行在非 OpenGL RHI 后端，行为不应被假设为可移植。
- renderer 和 `QQuickItem` 不在同一线程；只在 `synchronize()` 复制状态。
- 项尺寸变化会重建 FBO，缓存 GL 资源时要区分 FBO 依赖资源与长期资源。

## 知识点覆盖
OpenGL FBO、离屏合成、渲染线程、纹理方向、Qt 6 RHI 迁移。
