# QQuickItemGrabResult：异步取得一个 QQuickItem 的图像快照

> Qt 6.11.1 | `#include <QQuickItemGrabResult>` | CMake: `Qt6::Quick`

`QQuickItemGrabResult` 是 `QQuickItem::grabToImage()` 返回的异步结果对象。它解决截屏、缩略图、分享图片和离屏导出时“不能在调用 `grabToImage()` 后立刻拿到像素”的问题：scene graph 需要在后续帧真正完成渲染和读回。

## 正确的调用方式是等待 ready

```cpp
auto result = item->grabToImage();
if (!result)
    return;

connect(result.data(), &QQuickItemGrabResult::ready,
        this, [result] {
    const QImage image = result->image();
    result->saveToFile("C:/tmp/preview.png");
});
```

`grabToImage()` 返回 `QSharedPointer<QQuickItemGrabResult>`，因此 lambda 应捕获该 shared pointer，至少保持对象存活到 `ready()`。在 `ready` 之前读取 `image()`、`url()` 或写文件不能假定已得到完整结果。

`url()` 是结果在 QML 内可引用的 URL，适合把快照交给另一个 QML image consumer；它不是应用可长期依赖的常规磁盘路径。

## 保存的实际限制

`saveToFile(const QString &)` 使用文件名保存并返回 bool。Qt 6.2 起的 `saveToFile(const QUrl &)` 更适合 QML/URL 工作流，但 URL 必须指向本地文件，并且扩展名必须是 `QImageWriter` 支持的图像格式。

保存失败不会抛异常，调用方必须检查 false。常见原因是 result 未 ready、目录不存在、无权限、URL 不是本地文件或格式不支持。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQuickItem::grabToImage()` | 发起 item 异步抓图 | 可能返回空；结果不是同步完成 |
| `ready()` | 抓图完成通知 | 之后再读 image/url 或保存 |
| `image()` | 返回最终 `QImage` | 调用前等待 `ready()` |
| `url()` | 返回可供 QML 使用的结果 URL | 不等同于用户指定的永久文件路径 |
| `saveToFile(QString)` | 保存快照到文件名 | 检查 bool，依赖可写路径和格式 |
| `saveToFile(QUrl)` | 用本地文件 URL 保存 | Qt 6.2 起；必须是 local file 且扩展名受支持 |

## 使用边界

- 抓取大 item 可能需要大量显存和 readback 时间，不能作为每帧录制 API。
- source item 必须实际可由 Quick 渲染；不可见或未关联窗口的情况要按 `grabToImage()` 的返回结果处理。
- 将 QImage 交给工作线程写磁盘时，先拷贝值；不要让异步任务依赖即将销毁的 result。
