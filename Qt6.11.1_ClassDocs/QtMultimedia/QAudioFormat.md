# QAudioFormat
> Qt 6.11.1 · Qt Multimedia · 来自 `QAudioFormat`

## 作用定位

`QAudioFormat` 描述一段 PCM 音频数据的布局：采样率、通道数、样本格式。凡是原始音频 buffer、`QAudioSink`、`QAudioSource`、解码器输出，都需要用它解释字节流。

## 类说明

- 头文件：`#include <QAudioFormat>`
- CMake：链接 `Qt6::Multimedia`
- 继承：无公开 QObject 继承，值类型

## API 速查

| API | 说明 |
| --- | --- |
| `setSampleRate()` / `sampleRate()` | 每秒采样数，如 44100、48000。 |
| `setChannelCount()` / `channelCount()` | 通道数，如 1 单声道、2 立体声。 |
| `setSampleFormat()` / `sampleFormat()` | 样本格式，如 UInt8、Int16、Float。 |
| `isValid()` | 三个核心字段是否足以描述格式。 |
| `bytesPerFrame()` | 一帧所有通道占用字节数。 |
| `bytesForFrames()` / `framesForBytes()` | 帧数与字节数换算。 |
| `durationForBytes()` / `bytesForDuration()` | 字节数与时长换算。 |
| `framesForDuration()` / `durationForFrames()` | 帧数与时长换算。 |
| `channelConfig()` / `setChannelConfig()` | 通道布局配置。 |
| `defaultChannelConfigForChannelCount()` | 根据通道数给出默认布局。 |
| `normalizedSampleValue()` | 从样本指针读取并归一化成浮点值。 |

## 使用场景

- 配置 `QAudioSink` 播放 PCM。
- 配置 `QAudioSource` 采集 PCM。
- 解释 `QAudioBuffer` 的数据大小、帧数和时长。
- 写音频处理算法时做单位换算。

## 常见坑与经验

- 音频里“frame”不是视频帧，而是同一采样时刻所有通道样本的集合。
- 字节数换算必须用 sample format 和 channel count，不能只看采样率。
- 后端不支持某格式时，`QAudioSink/Source` 可能失败；先用 `QAudioDevice::isFormatSupported()`。
- `Float` 样本通常是 -1.0 到 1.0，整数格式需要按位宽解释。

## 知识点覆盖

- PCM 音频格式
- sample、frame、channel 的关系
- 时长/帧数/字节数换算
- 通道布局和样本格式
