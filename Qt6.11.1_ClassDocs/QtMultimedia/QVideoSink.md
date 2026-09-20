# QVideoSink
> Qt 6.11.1 · Qt Multimedia · 来自 `QVideoSink`

## 作用定位

`QVideoSink` 是接收视频帧的对象。播放器、摄像头预览或 capture session 可以把帧送到 sink，你再通过 `videoFrameChanged()` 获取最新 `QVideoFrame` 做显示、分析或转发。

## 类说明

- 头文件：`#include <QVideoSink>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `videoFrame()` | 当前最后一帧。 |
| `setVideoFrame()` | 手动设置当前帧。 |
| `videoSize()` | 当前视频尺寸。 |
| `subtitleText()` | 当前字幕文本。 |
| `rhi()` | 渲染硬件接口相关对象，面向高级渲染集成。 |
| `videoFrameChanged(frame)` | 新帧到达。 |
| `videoSizeChanged()` | 尺寸变化。 |
| `subtitleTextChanged()` | 字幕变化。 |

## 使用场景
- 从 `QMediaPlayer` 或 `QCamera` 获取帧做 OpenCV/AI 分析。
- 自定义渲染视频帧。
- 捕获预览帧生成缩略图。

## 常见坑与经验
- `videoFrameChanged` 的帧可能是 GPU 后端资源，map 到 CPU 可能昂贵。
- 不要在信号槽里做重图像处理，复制必要信息后交给工作线程。
- sink 只接收帧，不控制播放；播放控制仍在 player/camera/session。
- 使用 QWidget 显示普通视频时，`QVideoWidget` 更简单。

## 知识点覆盖

- 视频帧接收
- 播放/采集管线旁路
- 自定义渲染和图像分析
- RHI/GPU 帧注意事项
