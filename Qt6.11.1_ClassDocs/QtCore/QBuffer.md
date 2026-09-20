# QBuffer
> Qt 6.11.1 · Qt Core · 来自 `QBuffer`

## 作用定位
`QBuffer` 将 `QByteArray` 包装成可读写、可定位的内存 `QIODevice`。

## API 速查
| API | 是做什么的 |
|---|---|
| `setBuffer()` | 绑定外部字节数组。|
| `buffer()` | 取得内部字节数组。|
| `open()` | 以读写模式打开设备。|
| `seek()` | 移动内存读写位置。|
| `readAll()` / `write()` | 作为普通 device 读写。|

## 使用场景
将序列化 API、图片编解码器或压缩器接到内存数据，而不落盘。

## 常见坑与经验
- 绑定外部数组后，调用者不得在 device 使用期间使该数组失效。
- 大内容会完全驻留内存；流式大文件不应使用它。

## 知识点覆盖
QIODevice、内存流、序列化、位置指针、内存占用。
