# QVideoWidget
> Qt 6.11.1 · Qt Multimedia · 来自 `QVideoWidget`

## 作用定位

`QVideoWidget` 是 QWidget 应用中的视频显示控件。把它设置为 `QMediaPlayer` 或 `QMediaCaptureSession` 的视频输出后，就能在 widget 界面里显示播放或预览画面。

## 类说明

- 头文件：`#include <QVideoWidget>`
- CMake：链接 `Qt6::MultimediaWidgets`
- 继承：`QWidget`

## API 速查

| API | 说明 |
| --- | --- |
| `aspectRatioMode` | 控制保持比例、拉伸或裁剪显示。 |
| `setFullScreen()` / `isFullScreen()` | 全屏切换。 |
| `videoSink()` | 获取底层 `QVideoSink`。 |
| `fullScreenChanged()` | 全屏状态变化。 |

## 使用场景
- QWidget 播放器显示视频。
- 摄像头预览嵌入传统 widgets UI。
- 需要快速搭建视频显示区域。

## 常见坑与经验
- 模块链接是 `Qt6::MultimediaWidgets`，不是只有 `Qt6::Multimedia`。
- 它负责显示，不负责播放控制；播放仍由 `QMediaPlayer`。
- 自定义逐帧分析可以从 `videoSink()` 获取帧，但复杂渲染建议用专门渲染路径。

## 知识点覆盖

- QWidget 视频显示
- aspect ratio 和全屏
- 与 QMediaPlayer/capture session 连接
- `QVideoWidget` 与 `QVideoSink` 关系
