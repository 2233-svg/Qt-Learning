# QMediaCaptureSession
> Qt 6.11.1 · Qt Multimedia · 来自 `QMediaCaptureSession`

## 作用定位

`QMediaCaptureSession` 是采集管线的装配器。它把输入源（相机、屏幕、窗口、音频、自定义视频帧/音频 buffer）和输出端（录制器、图片捕获、视频预览）接在一起。它本身不采集也不编码，而是定义“谁进来、谁出去”。

## 类说明

- 头文件：`#include <QMediaCaptureSession>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `setCamera()` / `camera()` | 接入摄像头。 |
| `setAudioInput()` / `audioInput()` | 接入麦克风等音频输入。 |
| `setRecorder()` / `recorder()` | 接入 `QMediaRecorder` 录制输出。 |
| `setImageCapture()` / `imageCapture()` | 接入静态图片捕获。 |
| `setVideoOutput()` / `videoOutput()` | 接入预览显示或 `QVideoSink`。 |
| `setScreenCapture()` / `screenCapture()` | 接入屏幕捕获。 |
| `setWindowCapture()` / `windowCapture()` | 接入窗口捕获。 |
| `setVideoFrameInput()` / `videoFrameInput()` | 接入自定义视频帧输入。 |
| `setAudioBufferInput()` / `audioBufferInput()` | 接入自定义音频 buffer 输入。 |

## 使用场景

- 相机预览 + 拍照 + 录像。
- 屏幕录制或窗口录制。
- 自定义视频帧/音频数据编码成媒体文件。
- 同一输入同时预览和录制。

## 常见坑与经验

- session 只是连接关系，输入源仍要自己 start，recorder 仍要 record。
- 同时连接多个互斥输入时，后设置的源可能替换旧源。
- 预览和录制共享管线，格式和性能会相互影响。
- 权限失败通常发生在输入源对象上，不一定由 session 报错。

## 知识点覆盖

- 多媒体采集管线装配
- 输入源与输出端分离
- 预览、拍照、录制协作
- 自定义帧进入录制流程
