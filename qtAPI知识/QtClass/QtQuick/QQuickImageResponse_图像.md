# QQuickImageResponse：定义异步图像任务何时可交付、何时可销毁

> Qt 6.11.1 | `#include <QQuickImageResponse>` | CMake: `Qt6::Quick`

`QQuickImageResponse` 是 `QQuickAsyncImageProvider` 为单个 `image://` 请求返回的任务对象。它解决了异步图片加载的交接问题：后台工作何时完成、如何报告错误、何时把结果转成纹理，以及被取消后对象什么时候才能安全销毁。

## 最重要的规则：`finished()` 必须是最后一个动作

引擎收到 `finished()` 后，会通过 `deleteLater()` 清理 response。因此发射该信号后不应再访问成员、启动后续回调或让后台线程继续写入对象。

```cpp
void ThumbnailResponse::run()
{
    m_image = decodeThumbnail(m_id, m_requestedSize);
    if (m_image.isNull())
        m_error = "thumbnail decode failed";

    QMetaObject::invokeMethod(this, [this] {
        emit finished(); // 此后不再访问 this
    }, Qt::QueuedConnection);
}
```

上例只展示时序。实际实现还要避免 worker 在 response 已被请求取消或即将析构后发出晚到回调；通常用任务内部共享状态或取消标志协调。

## 结果延迟到 `textureFactory()`

`textureFactory()` 是纯虚函数，返回引擎要使用的 `QQuickTextureFactory *`。引擎接管该指针的所有权；如果后台结果是 `QImage`，可在这里按需创建：

```cpp
QQuickTextureFactory *ThumbnailResponse::textureFactory() const
{
    return QQuickTextureFactory::textureFactoryForImage(m_image);
}
```

这是按需调用的：请求报错或被取消时，引擎可能根本不调用它。因此不要在任务开始时就为 factory 分配一个“必定交付”的裸指针，除非能在未调用路径自行释放。

`errorString()` 默认空字符串表示没有错误。任务失败时重写它返回稳定、可诊断的说明；仍需发出 `finished()`，因为失败也是任务结束。

## cancel 只是一条通知

`cancel()` 表示 engine 已不再需要结果，可以重写以取消网络请求或减少解码工作，但不是强制 kill。即使取消了，response 也必须等后台工作真正不再使用它之后再发 `finished()`。过早 finished 会让 engine 删除仍被活跃线程引用的 response，导致崩溃。

若把 response 也实现成 `QRunnable`，务必调用 `setAutoDelete(false)`。response 的最终删除权属于 engine，不属于线程池。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `textureFactory()` | 返回任务成功结果对应的纹理工厂 | 纯虚；engine 接管返回指针，且该函数不保证会被调用 |
| `QQuickTextureFactory::textureFactoryForImage()` | 从 `QImage` 快速构建 factory | 适合 image 解码结果；不要求提前创建 |
| `errorString()` | 返回任务错误文本 | 空字符串表示无错误；错误仍需要 `finished()` |
| `cancel()` | 收到 engine 不再需要结果的通知 | 可不重写；重写后也必须完成并发射 finished |
| `finished()` | 成功、失败或取消后的终止信号 | 必须是最后动作，之后 response 可被 engine 销毁 |
| response 析构 | 释放任务相关资源 | 不要与 `QRunnable` auto-delete 形成双重删除 |

## 相关类型

- `QQuickAsyncImageProvider`：创建 response 并负责 provider 级的调度。
- `QQuickTextureFactory`：在 scene graph 侧创建可渲染的纹理。
- `QRunnable` / `QThreadPool`：可用于后台执行，但需要显式处理对象所有权。
