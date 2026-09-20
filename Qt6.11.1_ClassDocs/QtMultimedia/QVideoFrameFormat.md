# QVideoFrameFormat
> Qt 6.11.1 · Qt Multimedia · 来自 `QVideoFrameFormat`

## 作用定位

`QVideoFrameFormat` 描述视频帧的像素格式、尺寸、视口、帧率、颜色空间、动态范围、扫描方向、旋转和镜像等。它告诉你如何解释 `QVideoFrame` 的数据。

## 类说明

- 头文件：`#include <QVideoFrameFormat>`
- CMake：链接 `Qt6::Multimedia`
- 继承：无公开 QObject 继承，值类型

## API 速查

| API | 说明 |
| --- | --- |
| `pixelFormat()` / `setPixelFormat()` | 像素格式，如 RGB、NV12、YUV420P。 |
| `frameSize()` / `setFrameSize()` | 帧尺寸。 |
| `viewport()` / `setViewport()` | 有效显示区域。 |
| `frameRate()` / `setFrameRate()` | 帧率信息。 |
| `colorSpace()` / `colorTransfer()` / `colorRange()` | 颜色描述。 |
| `scanLineDirection()` | 扫描方向，影响上下翻转。 |
| `rotation()` / `mirrored()` | 显示方向和镜像信息。 |
| `isValid()` | 格式是否有效。 |
| `imageFormatFromPixelFormat()` | 映射到可用 `QImage::Format`。 |

## 使用场景
- 写视频帧处理算法前识别像素布局。
- 自定义视频输入时声明帧格式。
- 显示前处理旋转、镜像和颜色范围。

## 常见坑与经验
- 像素格式不是颜色空间；RGB/NV12 说的是内存布局，BT.709/BT.2020 说的是颜色解释。
- viewport 可能小于完整 frameSize，渲染时要尊重有效区域。
- 手机视频常带旋转/镜像信息，不处理会方向错误。
- 不是每个像素格式都能无损转成 QImage。

## 知识点覆盖

- 视频像素格式
- 颜色空间/范围/传递函数
- viewport、旋转、镜像
- 帧率和扫描方向
