# QAudioBufferOutput
> Qt 6.11.1 · Qt Multimedia · 来自 `QAudioBufferOutput`

## 作用定位

`QAudioBufferOutput` 用来从媒体播放管线旁路拿到解码后的音频 buffer。典型做法是挂到 `QMediaPlayer`，让播放器正常播放/解码的同时，把 PCM buffer 交给波形、频谱、响度或录制分析模块。

## 类说明

- 头文件：`#include <QAudioBufferOutput>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`
- 常用协作：`QMediaPlayer`、`QAudioBuffer`

## API 速查

| API | 说明 |
| --- | --- |
| 构造函数 | 创建音频 buffer 输出节点，可指定格式。 |
| `format()` | 返回请求/当前输出格式。 |
| `audioBufferReceived(buffer)` | 收到解码后的音频 buffer 时发出。 |

## 使用场景

- 播放音乐时绘制实时波形或频谱。
- 分析媒体文件响度、静音段、节奏。
- 可视化音频而不自己写解码器。
- 旁路获取播放器音频数据用于监控。

## 常见坑与经验

- 它是“输出 buffer 给应用”，不是“输出声音到设备”；声音播放仍由 `QAudioOutput` 负责。
- buffer 到达节奏由媒体后端决定，不适合作为硬实时音频回调。
- 请求格式不一定总被后端满足，处理前检查 buffer 的 `format()`。
- 分析计算不要阻塞信号处理路径，复杂 FFT 可丢到工作线程。

## 知识点覆盖

- 播放管线音频旁路
- 解码后 PCM 分析
- 与 `QAudioOutput` 区别
- 可视化和监控场景
