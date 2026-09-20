# QVideoFrame
> Qt 6.11.1 · Qt Multimedia · 来自 `QVideoFrame`

## 作用定位

`QVideoFrame` 是一帧视频图像数据，可能在 CPU 内存中，也可能由 GPU/后端缓冲持有。它带有 `QVideoFrameFormat`、时间戳、旋转/镜像等信息，是视频处理、显示、录制管线的核心数据块。

## 类说明

- 头文件：`#include <QVideoFrame>`
- CMake：链接 `Qt6::Multimedia`
- 继承：无公开 QObject 继承，值类型/共享缓冲句柄

## API 速查

| API | 说明 |
| --- | --- |
| `map()` / `unmap()` | 映射帧数据到 CPU 可访问内存。 |
| `isMapped()` / `mapMode()` | 查询映射状态。 |
| `bits(plane)` / `bytesPerLine(plane)` | 访问平面数据和 stride。 |
| `planeCount()` | 平面数，YUV 格式常多平面。 |
| `size()` / `width()` / `height()` | 图像尺寸。 |
| `pixelFormat()` / `surfaceFormat()` | 像素格式和完整帧格式。 |
| `startTime()` / `endTime()` | 媒体时间戳。 |
| `toImage()` | 尽量转换成 `QImage`。 |
| `isValid()` | 是否包含有效帧。 |

## 使用场景
- 从 `QVideoSink` 获取帧做图像处理。
- 自定义视频源向 `QVideoFrameInput` 发送帧。
- 截帧、生成缩略图、分析像素。

## 常见坑与经验
- 不是所有帧都能便宜地 `map()`；GPU 帧转 CPU 可能代价很高。
- 访问 `bits()` 前必须成功 `map()`，结束后及时 `unmap()`。
- YUV 多平面和 stride 不能当作紧密 RGB 图像处理。
- `toImage()` 方便但可能隐含转换和拷贝，性能敏感路径要谨慎。

## 知识点覆盖

- 视频帧缓冲
- CPU/GPU 映射
- 多平面像素格式
- 时间戳和帧处理
