# QQuickAsyncImageProvider
> Qt 6.11.1 · Qt Quick · 来自 `QQuickAsyncImageProvider`

## 作用定位
`QQuickAsyncImageProvider` 是异步版图片 provider。`Image` 请求不会把 I/O、解码或网络等待堵在界面线程，而是通过 `QQuickImageResponse` 在准备完成后交回结果。

## API 速查
| API | 是做什么的 |
|---|---|
| `requestImageResponse(id, requestedSize)` | 创建并返回本次请求的异步响应对象。|

## 使用场景
用于大图解码、数据库 BLOB、远程资源或需要昂贵缩放的缩略图。响应对象内部可用工作线程生成 `QImage`，完成时再通知 Qt Quick。

## 常见坑与经验
- 不要在 `requestImageResponse()` 内同步执行耗时工作；否则“异步 provider”仍会卡 UI。
- response 应正确处理 QML 取消、引擎销毁和过时请求，避免加载完成后覆盖更新版本。
- 仅返回与 `requestedSize` 相符的合理分辨率，原图过大时会白白占用内存。

## 知识点覆盖
异步加载、取消语义、后台解码、缩略图、缓存失效、UI 响应性。
