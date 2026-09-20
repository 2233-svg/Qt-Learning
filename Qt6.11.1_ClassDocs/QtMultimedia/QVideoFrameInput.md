# QVideoFrameInput
> Qt 6.11.1 · Qt Multimedia · 来自 `QVideoFrameInput`

## 作用定位

`QVideoFrameInput` 把应用自己生成的 `QVideoFrame` 送入 Qt 采集/录制管线。它适合把屏幕外渲染、图像算法输出、网络视频帧或合成画面交给 `QMediaRecorder` 编码成文件。

## 类说明

- 头文件：`#include <QVideoFrameInput>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`
- 协作：`QMediaCaptureSession`、`QMediaRecorder`

## API 速查

| API | 说明 |
| --- | --- |
| 构造函数 | 可指定 `QVideoFrameFormat`。 |
| `format()` | 当前/期望视频帧格式。 |
| `sendVideoFrame(frame)` | 向管线提交视频帧。 |
| `readyToSendVideoFrame()` | 管线可接收下一帧时通知。 |

## 使用场景
- 自定义渲染结果录制成视频。
- 网络帧、算法帧进入 recorder。
- 测试录制器，不依赖真实摄像头。

## 常见坑与经验
- 按 `readyToSendVideoFrame()` 节奏推帧，避免无界积压。
- 帧时间戳、帧率和格式一致性会影响输出视频同步。
- 送入的 `QVideoFrame` 必须在后端可接受的像素格式范围内。
- 它不是显示控件；显示用 `QVideoSink`、`QVideoWidget` 或 QML VideoOutput。

## 知识点覆盖

- 自定义视频源
- 视频录制背压
- 帧时间戳和格式
- 与 capture session 协作
