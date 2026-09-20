# QImageCapture
> Qt 6.11.1 · Qt Multimedia · 来自 `QImageCapture`

## 作用定位

`QImageCapture` 负责从 capture session 的摄像头管线捕获静态图片。它可以保存到文件，也可以把捕获到的 `QImage` 返回给应用，适合拍照、截图式抓拍、扫码前抓帧等。

## 类说明

- 头文件：`#include <QImageCapture>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`
- 协作：`QMediaCaptureSession`、`QCamera`

## API 速查

| API | 说明 |
| --- | --- |
| `capture()` | 捕获并保存到默认位置。 |
| `captureToFile(location)` | 捕获并保存到指定文件。 |
| `isReadyForCapture()` | 当前是否可以拍照。 |
| `fileFormat()` / `setFileFormat()` | 图片文件格式。 |
| `quality()` / `setQuality()` | 图片质量。 |
| `imageCaptured(id, preview)` | 捕获到预览图像。 |
| `imageSaved(id, fileName)` | 图片保存完成。 |
| `errorOccurred(id, error, string)` | 捕获错误。 |

## 使用场景

- 相机拍照保存文件。
- 捕获一帧用于识别、扫码或预览。
- 拍照前后显示缩略图和保存状态。

## 常见坑与经验
- 拍照前检查 `isReadyForCapture()`，否则用户连点会失败。
- `imageCaptured` 不等于文件已保存，保存完成看 `imageSaved`。
- 图片格式/质量受平台后端和设备能力影响。
- 必须通过 `QMediaCaptureSession::setImageCapture()` 接入会话。

## 知识点覆盖

- 静态图片捕获
- 捕获 ID、预览图和保存完成
- 图片质量和格式
- 与摄像头 capture session 协作
