# QMediaRecorder
> Qt 6.11.1 · Qt Multimedia · 来自 `QMediaRecorder`

## 作用定位

`QMediaRecorder` 是高层媒体录制器，通常挂在 `QMediaCaptureSession` 上，把相机、屏幕、窗口、麦克风或自定义帧输入编码封装成文件。它处理容器格式、音视频编码器、质量、码率和输出位置。

## 类说明

- 头文件：`#include <QMediaRecorder>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`
- 常用协作：`QMediaCaptureSession`、`QMediaFormat`、`QMediaMetaData`

## API 速查

| API | 说明 |
| --- | --- |
| `record()` / `pause()` / `stop()` | 控制录制状态。 |
| `recorderState()` | 当前录制、暂停或停止状态。 |
| `setOutputLocation()` / `outputLocation()` | 设置输出文件 URL。 |
| `setMediaFormat()` / `mediaFormat()` | 设置容器和编解码格式。 |
| `setQuality()` / `quality()` | 设置整体质量倾向。 |
| `setEncodingMode()` / `encodingMode()` | 固定质量或固定码率等策略。 |
| `setAudioBitRate()` / `setVideoBitRate()` | 设置音视频码率。 |
| `setAudioSampleRate()` / `setVideoFrameRate()` | 设置采样率和帧率。 |
| `setVideoResolution()` | 设置目标分辨率。 |
| `setMetaData()` / `metaData()` | 设置文件元数据。 |
| `actualLocation()` | 后端最终写入位置。 |
| `duration()` | 已录制时长。 |
| `error()` / `errorString()` | 录制错误。 |

## 使用场景

- 相机录像、录音、屏幕录制、窗口录制。
- 把自定义视频帧和音频 buffer 编码成文件。
- 提供质量/码率/格式选择 UI。

## 常见坑与经验

- recorder 自己不产生媒体，必须通过 `QMediaCaptureSession` 连接输入源。
- 设置格式后仍要考虑平台支持；用 `QMediaFormat` 查询编码器能力。
- `actualLocation()` 可能与请求的 `outputLocation()` 不同，保存成功后以它为准。
- 录制权限、磁盘路径、编解码器不可用是最常见失败来源。

## 知识点覆盖

- 录制管线与 capture session
- 容器格式和编解码器
- 质量、码率、帧率、分辨率
- 输出位置和元数据
