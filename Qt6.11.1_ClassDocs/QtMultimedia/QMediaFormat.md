# QMediaFormat
> Qt 6.11.1 · Qt Multimedia · 来自 `QMediaFormat`

## 作用定位

`QMediaFormat` 描述媒体容器、音频编码器、视频编码器及其平台支持情况。它是播放器/录制器能力协商的工具，尤其用于 `QMediaRecorder` 选择输出格式。

## 类说明

- 头文件：`#include <QMediaFormat>`
- CMake：链接 `Qt6::Multimedia`
- 继承：无公开 QObject 继承，值类型

## API 速查

| API | 说明 |
| --- | --- |
| `setFileFormat()` / `fileFormat()` | 设置或读取容器格式，如 MP4、Matroska、Wave。 |
| `setAudioCodec()` / `audioCodec()` | 设置或读取音频编码器。 |
| `setVideoCodec()` / `videoCodec()` | 设置或读取视频编码器。 |
| `isSupported(mode)` | 当前组合在编码或解码方向是否支持。 |
| `supportedFileFormats(mode)` | 查询支持的容器列表。 |
| `supportedAudioCodecs(mode)` / `supportedVideoCodecs(mode)` | 查询支持的编解码器。 |
| `audioCodecDescription()` / `videoCodecDescription()` | 生成可显示描述。 |
| `fileFormatDescription()` | 容器格式显示文本。 |

## 使用场景

- 录制设置 UI：容器、音频编码、视频编码。
- 根据平台能力选择 fallback 格式。
- 播放或录制前预判是否支持。

## 常见坑与经验

- 支持能力与平台后端、系统编解码器、许可证有关，同一代码跨平台差异很大。
- 容器和编码器要成组合看，某编码器支持不代表能放进任意容器。
- 解码支持和编码支持是两个方向，查询时要传对 mode。
- UI 文本优先用 description 函数，不要直接显示枚举名。

## 知识点覆盖

- 媒体容器与编解码器
- 编码/解码能力查询
- 录制格式协商
- 跨平台后端差异
