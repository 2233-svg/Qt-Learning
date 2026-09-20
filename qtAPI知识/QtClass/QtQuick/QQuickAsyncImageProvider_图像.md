# QQuickAsyncImageProvider：把 `image://` 请求变成可控的异步任务

> Qt 6.11.1 | `#include <QQuickAsyncImageProvider>` | CMake: `Qt6::Quick`

`QQuickAsyncImageProvider` 是需要自行控制并发、取消和完成时序的 image provider 基类。它不直接返回 `QImage`，而是为每次请求创建一个 `QQuickImageResponse` 任务。适合远程图片、复杂解码、大量缩略图和任何不能让单个 provider 工作线程排队堵住的图像源。

## 为什么不用普通 `QQuickImageProvider`

普通 Image/Texture provider 的异步请求在每个 engine 上使用单一后台线程。一个慢的网络读或大图解码会堵住其它请求。`QQuickAsyncImageProvider` 把调度权交给你：可用 `QThreadPool`、自有 I/O 层或请求合并策略，让多个 response 同时推进。

QML 入口不变：

```qml
Image {
    source: "image://thumbnails/report-42"
    asynchronous: true
}
```

## 只实现一个工厂函数

```cpp
class ThumbnailProvider final : public QQuickAsyncImageProvider
{
public:
    QQuickImageResponse *requestImageResponse(
        const QString &id, const QSize &requestedSize) override
    {
        auto *response = new ThumbnailResponse(id, requestedSize);
        QThreadPool::globalInstance()->start(response);
        return response;
    }
};
```

`requestImageResponse()` 返回的不是最终图片，而是“将来提供 texture factory 的任务”。`id` 是去掉 scheme 和 provider host 后的路径；`requestedSize` 对应 QML `sourceSize`，有效时结果应尽量符合它。

该函数可能被多个线程并发调用，因此不能修改未保护的 provider 成员、复用同一个 response 或假定调用发生在 GUI 线程。每个请求都应返回自己的 response 实例。

## response 的完成契约

`QQuickImageResponse` 完成时发出 `finished()`；引擎随后用 `deleteLater()` 清理它。任务应在完成、失败或取消后都走到这个终点。收到 `cancel()` 后可以实际中止 I/O，但即使已取消仍必须在任务真正停止后发出 `finished()`。

response 里常用 `QImage` 作为后台结果，等引擎调用 `textureFactory()` 时再用 `QQuickTextureFactory::textureFactoryForImage()` 创建并交给引擎。不要在 `requestImageResponse()` 中预先分配 factory 后期待一定被索取：错误或取消时 `textureFactory()` 可能永不调用。

## 生命周期风险

provider 的析构也必须线程安全。engine 持有 provider；引擎关闭或 provider 被移除时，后台任务不能继续访问已销毁的 provider 状态。将任务需要的数据复制进 response，或用明确的共享状态与取消令牌管理。

若让 response 同时继承 `QRunnable`，关闭 `QRunnable` 的 auto-delete：response 的 QObject 生命周期由 QML engine 在 `finished()` 后管理，双重删除会导致崩溃。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `requestImageResponse(id, requestedSize)` | 创建并返回一次图像请求的 response | 纯虚；每次调用返回独立任务，且实现必须可重入 |
| `id` | 去掉 provider id 后的请求路径 | 保留 URL 中剩余部分的大小写，业务自行规范化 |
| `requestedSize` | QML `sourceSize` 的期望尺寸 | 结果应尽量遵从，不能把它误当原图尺寸 |
| `QQuickImageResponse::finished()` | 宣告任务已彻底完成 | 这是 response 的最后动作，之后 engine 可销毁对象 |
| `QQuickImageResponse::cancel()` | engine 不再需要该结果的通知 | 取消后仍要在任务停止时发出 `finished()` |
| `QThreadPool` | provider 自选的并发执行方式 | 任务不可在 provider 销毁后访问其悬空数据 |

## 相关类型

- `QQuickImageResponse`：承载单次异步任务的状态、错误和完成信号。
- `QQuickTextureFactory`：将最终图像转为 Quick 纹理的所有权交接点。
- `QQmlEngine::addImageProvider()`：注册并接管 provider。
