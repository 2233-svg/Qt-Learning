# QMediaPlayer
> Qt 6.11.1 · Qt Multimedia · 来自 `QMediaPlayer`

## 作用定位

`QMediaPlayer` 是高层媒体播放器，负责打开本地文件、URL 或流媒体，完成解封装、解码、同步，并把音频交给 `QAudioOutput`、视频交给 `QVideoSink`/`QVideoWidget`/QML VideoOutput。它适合播放完整媒体，不适合手写 PCM 或逐帧解码算法。

## 类说明

- 头文件：`#include <QMediaPlayer>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`
- 常用协作：`QAudioOutput`、`QVideoSink`、`QAudioBufferOutput`、`QPlaybackOptions`

## API 速查

| API | 说明 |
| --- | --- |
| `setSource()` / `source()` | 设置媒体 URL。 |
| `setSourceDevice()` / `sourceDevice()` | 从 QIODevice 播放。 |
| `play()` / `pause()` / `stop()` | 控制播放。 |
| `playbackState()` / `mediaStatus()` | 区分播放状态和媒体加载/缓冲状态。 |
| `setAudioOutput()` / `audioOutput()` | 连接音频输出。 |
| `setVideoOutput()` / `videoOutput()` | 连接视频输出对象。 |
| `setPosition()` / `position()` / `duration()` | 跳转和读取时间线。 |
| `setPlaybackRate()` / `playbackRate()` | 调整播放速度。 |
| `setLoops()` / `loops()` | 设置循环次数。 |
| `setPlaybackOptions()` / `playbackOptions()` | 配置播放后端选项。 |
| `metaData()` | 读取媒体元数据。 |
| `error()` / `errorString()` | 读取播放错误。 |
| `seekableChanged()` / `bufferProgressChanged()` | 监听可跳转和缓冲变化。 |

## 使用场景

- 播放音频、视频、网络流。
- 做带进度条、倍速、循环、音量和设备选择的播放器。
- 播放时旁路获取音频 buffer 或视频帧做分析。

## 常见坑与经验

- `playbackState()` 只说播放/暂停/停止，加载失败、缓冲、结束要看 `mediaStatus()`。
- 没设置 `QAudioOutput` 时可能没有声音；没设置视频输出时也能播放音频。
- 网络流和本地文件的 seek/buffer 行为不同，UI 要根据 `isSeekable()` 调整。
- 后端编解码器能力受平台影响，失败时先看 `QMediaFormat` 和 `errorString()`。

## 知识点覆盖

- 高层媒体播放管线
- 音频/视频输出分离
- 媒体状态、播放状态、错误状态
- seek、缓冲、倍速、循环
