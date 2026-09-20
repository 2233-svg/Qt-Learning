# QQuickRenderTarget
> Qt 6.11.1 · Qt Quick · 来自 `QQuickRenderTarget`

## 作用定位
`QQuickRenderTarget` 是一个值对象，用于描述 Qt Quick 应该渲染到哪里：原生纹理、渲染缓冲、`QRhiRenderTarget` 或窗口默认目标。

## API 速查
| API | 是做什么的 |
|---|---|
| `fromOpenGLTexture()` | 描述 OpenGL 纹理目标。|
| `fromRhiRenderTarget()` | 描述现有 `QRhiRenderTarget`。|
| `fromMetalLayer()` | 将 Metal layer 作为目标。|
| `fromVulkanImage()` | 描述 Vulkan image 目标。|
| `setDevicePixelRatio()` | 指定目标的高 DPI 缩放。|
| `setMirrorVertically()` | 告知 Qt Quick 目标坐标是否需垂直翻转。|
| `isNull()` | 判断是否为默认/空描述。|

## 使用场景
搭配 `QQuickWindow::setRenderTarget()` 或 `QQuickRenderControl`，把 QML 画入引擎纹理以便后续合成。

## 常见坑与经验
- 目标像素尺寸和逻辑尺寸必须与 `devicePixelRatio` 对齐，否则文字会模糊或裁剪。
- 不同 API 的纹理原点不同，出现上下颠倒时检查 `setMirrorVertically()`。
- 目标资源的创建、布局转换和销毁不归该值对象管理。

## 知识点覆盖
离屏目标、纹理互操作、高 DPI、坐标原点、RHI。
