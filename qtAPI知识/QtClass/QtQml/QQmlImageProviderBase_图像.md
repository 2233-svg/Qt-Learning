# QQmlImageProviderBase：声明 QML 图像 provider 能提供什么

> Qt 6.11.1 · `#include <QQmlImageProviderBase>` · 模块：`Qt6::Qml` · 基类：`QObject`

`QQmlImageProviderBase` 是 QML 图像 provider 的抽象基类。它不负责生成图片，而是告诉 `QQmlEngine` 这个 provider 支持哪一种图像结果与线程加载策略。实际实现通常继承 Qt Quick 中的 `QQuickImageProvider` 或 `QQuickAsyncImageProvider`。

它解决了 QML `Image { source: "image://provider/id" }` 从应用自定义数据源拿图的问题，例如缩略图缓存、数据库图片、设备帧、加密资源或远端请求结果。

## 注册和选择实现类型

```cpp
// provider 应继承 QQuickImageProvider 或 QQuickAsyncImageProvider
engine.addImageProvider(u"thumbnails"_s, new ThumbnailProvider);
```

QML 使用：

```qml
Image {
    source: "image://thumbnails/42"
}
```

`QQmlEngine::addImageProvider()` 会取得 provider 所有权，并应在加载任意 QML 源之前完成注册。不要在 C++ 侧保留会在 engine 析构后使用的 provider 裸指针。

## ImageType 决定引擎调用哪种请求接口

| 类型 | 提供的数据 | 通常对应的派生实现 |
| --- | --- | --- |
| `Image` | `QImage` | `QQuickImageProvider::requestImage()` |
| `Pixmap` | `QPixmap` | `QQuickImageProvider::requestPixmap()` |
| `Texture` | 基于 `QSGTextureProvider` 的图像 | `QQuickImageProvider::requestTexture()` |
| `ImageResponse` | `QQuickTextureFactory` 响应 | 仅用于 `QQuickAsyncImageProvider` 或其子类。 |

`Invalid` 只是无效哨兵，不应由可注册 provider 返回。基类指针只包含类型与 flag 信息；需要请求图像时，必须按实际派生类型转换，而不是假设所有 provider 都具有同一 request 函数。

## 异步 flag 的边界

`ForceAsynchronousImageLoading` 要求引擎在独立线程运行该 provider 的图像请求，避免主线程被慢解码或 I/O 阻塞。这不自动让派生实现线程安全：provider 的共享缓存、QObject 访问和图形资源仍需遵守对应线程规则。

若请求模型本身就是异步响应，优先使用 `QQuickAsyncImageProvider`；不要在同步 `requestImage()` 中临时阻塞等待网络。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `imageType()` | 声明 provider 图像类型 | 纯虚函数，决定 engine 调用哪一种请求接口。 |
| `flags()` | 声明 provider 特性 | 纯虚函数，返回 `Flags` 组合。 |
| `ImageType::Image` | 提供 `QImage` | 调用 `requestImage()` 路径。 |
| `ImageType::Pixmap` | 提供 `QPixmap` | 调用 `requestPixmap()` 路径。 |
| `ImageType::Texture` | 提供纹理型图像 | 调用 `requestTexture()` 路径。 |
| `ImageType::ImageResponse` | 提供异步图像响应 | 仅用于 `QQuickAsyncImageProvider` 系列。 |
| `Flag::ForceAsynchronousImageLoading` | 强制独立线程加载 | 降低 UI 阻塞，不替代派生类线程安全设计。 |
| `QQmlEngine::addImageProvider()` | 将 provider 注册到 engine | engine 取得所有权，必须早于 QML 资源加载。 |

这个类只表达 provider 的能力边界。真正决定性能、线程安全和缓存行为的是其 Qt Quick 派生实现。
