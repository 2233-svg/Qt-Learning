# QQuickTextureFactory
> Qt 6.11.1 · Qt Quick · 来自 `QQuickTextureFactory`

## 作用定位
`QQuickTextureFactory` 是把 CPU 侧图像延迟转换为当前 Scene Graph `QSGTexture` 的工厂。异步图片响应返回它，而非直接返回跨线程、跨窗口都不安全的纹理对象。

## API 速查
| API | 是做什么的 |
|---|---|
| `textureWindow()` | 查询可用纹理所绑定的窗口。|
| `textureSize()` | 返回图像像素尺寸。|
| `createTexture()` | 在目标窗口的 Scene Graph 中创建纹理。|
| `image()` | 部分实现可返回源 `QImage`。|
| `textureFactoryForImage()` | 用 `QImage` 快速构造默认工厂。|

## 使用场景
`QQuickImageResponse::textureFactory()` 中使用 `textureFactoryForImage(decodedImage)`，由 Qt Quick 在正确的渲染上下文中完成纹理创建。

## 常见坑与经验
- `QSGTexture` 与具体窗口和渲染线程绑定；不能从后台线程预先创建后随意传递。
- 大图应在解码阶段限制尺寸；factory 不能消除纹理上传成本。
- 工厂与源图像需要在 `createTexture()` 发生前保持有效。

## 知识点覆盖
延迟资源创建、CPU/GPU 边界、Scene Graph 生命周期、异步图像加载。
