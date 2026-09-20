# QQmlImageProviderBase
> Qt 6.11.1 · Qt QML · 来自 `QQmlImageProviderBase`

## 作用定位

`QQmlImageProviderBase` 是 QML `image://provider/id` 图片机制的基类。实际项目通常使用它的派生类，如 `QQuickImageProvider` 或异步 image provider；这个基类定义 provider 返回图片的类型和加载标志。

## 类说明

- 头文件：`#include <QQmlImageProviderBase>`
- CMake：链接 `Qt6::Qml`
- 继承：`QObject`
- 常见派生：`QQuickImageProvider`
- 注册入口：`QQmlEngine::addImageProvider()`

## API 速查

| API | 说明 |
| --- | --- |
| `ImageType::Image` | provider 返回 `QImage`。 |
| `ImageType::Pixmap` | provider 返回 `QPixmap`。 |
| `ImageType::Texture` | provider 返回 scene graph 纹理相关对象。 |
| `ImageType::ImageResponse` | 异步图片响应，供 async provider 使用。 |
| `Flag::ForceAsynchronousImageLoading` | 强制图片请求在独立线程执行，避免阻塞主线程。 |
| `imageType()` | 返回 provider 类型。 |
| `flags()` | 返回加载标志。 |

## 使用场景

- QML 从 C++ 动态生成图片：验证码、缩略图、图表、头像缓存。
- 统一处理图片缓存、权限、解码或水印。
- 用 `image://icons/name` 这样的虚拟路径隐藏真实资源来源。

## 常见坑与经验

- providerId 不带 `image://`，注册 `icons` 后 QML 用 `image://icons/foo`。
- `QPixmap` 受 GUI 线程和平台限制更多，后台生成图片通常优先 `QImage`。
- 生成图片很慢时要启用异步路径，或使用真正的 async provider。
- provider 生命周期由引擎管理，重复注册同名 provider 前要明确替换策略。
- URL 中 id 的大小写和编码会影响缓存命中。

## 知识点覆盖

- QML image provider
- QImage/QPixmap/Texture/ImageResponse 差异
- 异步图片加载
- 动态资源路径设计
