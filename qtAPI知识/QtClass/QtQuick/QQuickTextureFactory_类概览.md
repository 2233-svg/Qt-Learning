# QQuickTextureFactory：把加载线程的数据延后变成 scene graph 纹理

> Qt 6.11.1 | `#include <QQuickImageProvider>` | CMake: `Qt6::Quick`

`QQuickTextureFactory` 是异步图片提供链路中的中间对象。图片解码往往在工作线程完成，而 `QSGTexture` 必须在 Qt Quick 的 scene graph 渲染环境中创建；factory 保存“如何生成纹理”的信息，等 Qt Quick 到正确线程和正确窗口时再调用 `createTexture()`。

最常见的使用处是 `QQuickImageResponse::textureFactory()`：异步 image provider 完成解码后返回一个 factory，Qt Quick 取得并缓存由它创建的纹理。一般项目直接调用 `textureFactoryForImage(image)` 即可，只有需要包裹特殊像素来源、统计显存或自定义纹理生成时才派生此类。

## 为什么不能在加载线程直接建纹理

```cpp
QQuickTextureFactory *ThumbnailResponse::textureFactory() const
{
    return QQuickTextureFactory::textureFactoryForImage(m_decodedImage);
}
```

工作线程通常没有可用的 scene graph 图形上下文。`createTexture(window)` 会在 scene graph 渲染线程调用，`window` 给出创建纹理所需的渲染环境；实现不应提前假定某个 OpenGL context、GPU 设备或 `QQuickWindow` 一直有效。

每一次 `createTexture()` 必须返回一个**新的** `QSGTexture` 实例。Qt Quick 会按需要缓存返回值，因此工厂不应把同一个 texture 指针反复交回，也不应让 factory 自行管理 Qt 已接管使用的 texture 生命周期。

## 派生实现的线程约束

`textureSize()` 可以在任意线程调用，必须是无图形上下文依赖的纯元数据查询。`textureByteCount()` 也应准确反映纹理预计消耗的字节数，方便 Qt Quick 做缓存与资源决策。

`image()` 是从 factory 取得像素图像的回退接口，通常不常用且可能昂贵。返回的 `QImage` 必须自包含，不能借用外部 `uchar *` 缓冲区；调用方无法知道这个图像会存活多久。

旧版文档把其背景描述为 OpenGL context，但应用代码不应由此推断能在任意线程调用图形 API。可靠的契约是：解码在任意线程，纹理构造由 Qt Quick 在 scene graph 的渲染环境中调度。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQuickTextureFactory()` | 创建抽象纹理工厂基类 | 通常只由派生类或 `textureFactoryForImage()` 的结果使用 |
| `createTexture(QQuickWindow *window)` | 在 scene graph 渲染线程创建 `QSGTexture` | 纯虚；每次必须返回独立 texture，不能在工作线程预创建 |
| `textureSize()` | 返回纹理像素尺寸 | 纯虚；可在任意线程调用，不能依赖图形上下文 |
| `textureByteCount()` | 返回纹理估算内存字节数 | 纯虚；应与实际资源规模一致 |
| `image()` | 返回此纹理对应的 `QImage` | 通常慢且少用；必须返回自包含图像，不能借用临时像素缓冲 |
| `textureFactoryForImage(image)` | 用普通 `QImage` 创建现成 factory | 常用于 `QQuickImageResponse::textureFactory()`；适合无需自定义 GPU 上传的路径 |
| `QQuickImageResponse::textureFactory()` | 异步响应把 factory 交给 Qt Quick 的位置 | 返回后由 Qt Quick 在正确渲染环境中创建与缓存纹理 |
