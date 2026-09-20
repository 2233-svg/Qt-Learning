# QQuickItemGrabResult
> Qt 6.11.1 · Qt Quick · 来自 `QQuickItemGrabResult`

## 作用定位
`QQuickItemGrabResult` 是 `QQuickItem::grabToImage()` 的异步结果对象，代表一次将视觉项及其子树渲染成 `QImage` 的请求。

## 类说明
它不是即时截图 API。调用 `grabToImage()` 后，Qt Quick 要等到合适的渲染帧完成，随后才发出完成信号。

## API 速查
| API | 是做什么的 |
|---|---|
| `ready()` | 图像已准备好，可读取或保存。|
| `image()` | 取得抓取结果 `QImage`。|
| `url()` | 取得可供 QML `Image` 使用的临时 URL。|
| `saveToFile()` | 将结果异步写入文件。|

## 使用场景
```cpp
auto result = item->grabToImage(QSize(800, 450));
connect(result.data(), &QQuickItemGrabResult::ready, this, [result] {
    result->saveToFile("preview.png");
});
```
适合导出预览、生成缩略图和自动化视觉测试。

## 常见坑与经验
- 必须持有 `QSharedPointer` 到 `ready()` 后，否则请求可能提前被释放。
- 隐藏、未进入窗口或还未完成布局的项可能拿不到预期图像；先确保它已经渲染过。
- 大尺寸抓取会消耗显存、CPU 内存和读回时间，不能当作实时视频采集方案。

## 知识点覆盖
异步结果、QSharedPointer、渲染读回、图像导出、QML 临时资源 URL。
