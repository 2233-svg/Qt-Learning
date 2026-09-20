# QQuickImageProvider
> Qt 6.11.1 · Qt Quick · 来自 `QQuickImageProvider`

## 作用定位
`QQuickImageProvider` 为 QML `Image` 提供 `image://providerId/requestId` 形式的自定义图像来源。它适合把内存缓存、数据库缩略图、设备截图或业务资源接入 QML，而不是先落盘成临时文件。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数的 `ImageType` | 声明提供 `QImage`、`QPixmap` 或 `QSGTexture`。|
| `requestImage()` | 按 id 返回图像和原始尺寸。|
| `requestPixmap()` | 返回像素图；主要面向 GUI 线程资源。|
| `requestTexture()` | 返回纹理工厂，便于直接生成 Scene Graph 纹理。|
| `flags()` | 查询 provider 支持的特性。|

## 使用场景
```cpp
engine.addImageProvider("thumb", new ThumbnailProvider);
// QML: Image { source: "image://thumb/record-42" }
```
`requestId` 应像 URI 路径一样可解析，例如 `album/17?size=small`，让 provider 负责校验、缓存键和回退图。

## 常见坑与经验
- provider 属于 `QQmlEngine`；引擎销毁时会接管并释放它，不要另行删除。
- `QPixmap` 受 GUI 线程限制；后台解码优先用 `QImage`。
- 同一个 URL 默认可能被 QML 图片缓存命中。资源更新时使用版本化 id、显式 cache 策略或发出新的 URL。

## 知识点覆盖
QML URL scheme、图像缓存、内存资源、QImage/QPixmap/纹理的线程差异、请求参数设计。
