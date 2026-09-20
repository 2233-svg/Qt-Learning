# QCameraFormat
> Qt 6.11.1 · Qt Multimedia · 来自 `QCameraFormat`

## 作用定位

`QCameraFormat` 描述摄像头的一种视频输出组合：分辨率、像素格式、最小/最大帧率。它来自 `QCameraDevice::videoFormats()`，用于给 `QCamera::setCameraFormat()` 选择具体采集格式。

## 类说明

- 头文件：`#include <QCameraFormat>`
- CMake：链接 `Qt6::Multimedia`
- 继承：无公开 QObject 继承，值类型

## API 速查

| API | 说明 |
| --- | --- |
| `resolution()` | 图像尺寸。 |
| `pixelFormat()` | 视频帧像素格式。 |
| `minFrameRate()` / `maxFrameRate()` | 支持帧率范围。 |
| `isNull()` | 是否为空格式。 |

## 使用场景

- 选择 1080p/720p、30fps/60fps 等摄像头格式。
- 根据算法要求选择 RGB、YUV 等像素格式。
- 在性能和画质之间做取舍。

## 常见坑与经验
- 必须使用设备提供的格式列表，不要手写一个“看起来合理”的格式。
- 高帧率和高分辨率通常不能同时满足，要从实际列表筛选。
- 像素格式影响后续图像处理成本，RGB 方便但可能更耗带宽。

## 知识点覆盖

- 摄像头格式协商
- 分辨率、帧率、像素格式
- 性能与画质权衡
