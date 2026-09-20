# QQuickImageProvider：为 `image://` URL 提供同步或轻量异步图像

> Qt 6.11.1 | `#include <QQuickImageProvider>` | CMake: `Qt6::Quick`

`QQuickImageProvider` 为 QML 的 `Image` 和 `BorderImage` 添加自定义图像协议。它解决的是“图片不来自文件或网络 URL”的问题：颜色生成器、数据库缩略图、内存缓存、设备截图等可以通过 `image://provider-id/request-id` 被 QML 像普通图片一样使用。

## 注册一次，QML 用 URL 请求

```cpp
class ColorProvider final : public QQuickImageProvider
{
public:
    ColorProvider() : QQuickImageProvider(Image) {}

    QImage requestImage(const QString &id, QSize *size,
                        const QSize &requestedSize) override;
};

engine.addImageProvider("colors", new ColorProvider);
```

```qml
Image {
    source: "image://colors/teal"
    sourceSize: Qt.size(160, 90)
}
```

`QQmlEngine::addImageProvider()` 会接管 provider 所有权，且所有 provider 应在加载任何 QML 源文件前加入 engine。provider 标识符大小写不敏感，URL 中剩余的 request id 保留大小写；如果业务希望 id 不分大小写，要在 provider 内自行归一化。

## 选择一种返回形式

构造函数的 `ImageType` 决定你要实现哪个虚函数：

- `Image`：重写 `requestImage()`，返回 `QImage`；通用且适合后台解码。
- `Pixmap`：重写 `requestPixmap()`，返回 `QPixmap`；受平台 GUI 线程能力限制更大。
- `Texture`：重写 `requestTexture()`，返回 `QQuickTextureFactory *`；用于直接生成 Quick 纹理。

`id` 已去掉 `image://` scheme 和 provider id；`requestedSize` 对应 QML 的 `sourceSize`。若它有效，应尽量返回请求尺寸；无论实际返回尺寸如何，都要通过 `size` 写回源图原始大小，否则 QML 未显式设置宽高时可能得到错误尺寸。

```cpp
QImage ColorProvider::requestImage(const QString &id, QSize *size,
                                   const QSize &requestedSize)
{
    const QSize originalSize(640, 360);
    if (size)
        *size = originalSize;

    const QSize outputSize = requestedSize.isValid()
        ? requestedSize : originalSize;
    QImage image(outputSize, QImage::Format_RGBA8888);
    image.fill(QColor(id).rgba());
    return image;
}
```

## 异步、缓存与线程

对 Image 或 Texture provider，QML 将 `Image.asynchronous: true` 的请求放入低优先级后台线程；`ForceAsynchronousImageLoading` 标志可强制该 provider 的所有请求异步。每个 `request*()` 可能被多个线程调用，派生实现和析构函数都必须线程安全、可重入。

Pixmap 的异步加载依赖平台 `ThreadedPixmaps` 能力；不支持的平台会忽略 `asynchronous: true` 并同步加载。

普通 provider 的非 `ImageResponse` 异步请求按 engine 共享一个线程。一个慢请求会阻塞同 engine 的其它请求；需要并行下载、解码或可取消任务时，改用 `QQuickAsyncImageProvider` 并由自己管理线程池。

返回图像会被 QML engine 自动缓存。若每次都要重新生成或取得最新帧，在 QML 中设 `cache: false`；否则缓存命中时 provider 的 `request*()` 根本不会被调用。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQuickImageProvider(ImageType, Flags)` | 声明 provider 返回形式及加载标志 | `ImageType` 与实际重写函数必须匹配 |
| `requestImage(id, size, requestedSize)` | 返回 `QImage` | 默认返回空图；实现必须可重入 |
| `requestPixmap(id, size, requestedSize)` | 返回 `QPixmap` | 异步依赖平台 `ThreadedPixmaps` |
| `requestTexture(id, size, requestedSize)` | 返回 `QQuickTextureFactory` | 默认返回空；用于直接提供纹理工厂 |
| `requestedSize` | QML `sourceSize` 请求 | 有效时应尽量按其生成，`size` 仍写原始尺寸 |
| `ForceAsynchronousImageLoading` | 强制全部请求后台加载 | 不让同步实现免于线程安全要求 |
| `QQmlEngine::addImageProvider()` | 注册 provider 并转移所有权给 engine | 在加载 QML 前调用；不要再手工 delete provider |
| QML `cache: false` | 禁用该 Image 的缓存 | 缓存开启时相同 source 可跳过 provider 调用 |

## 相关类型

- `QQuickAsyncImageProvider`：自定义并发、取消和完成时序的高级入口。
- `QQuickTextureFactory`：将图像结果转成 scene graph 纹理。
- `QQmlImageProviderBase`：定义 Image/Pixmap/Texture 类型和加载 flags 的基类。
