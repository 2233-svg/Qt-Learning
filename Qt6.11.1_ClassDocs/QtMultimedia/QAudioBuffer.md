# QAudioBuffer
> Qt 6.11.1 · Qt Multimedia · 来自 `QAudioBuffer`

## 作用定位

`QAudioBuffer` 是一段带格式和时间戳的音频 PCM 数据。它通常来自 `QAudioDecoder`、媒体播放器的音频 buffer 输出，或作为自定义音频管线中的数据块传递。

## 类说明

- 头文件：`#include <QAudioBuffer>`
- CMake：链接 `Qt6::Multimedia`
- 继承：无公开 QObject 继承，值类型/共享数据语义

## API 速查

| API | 说明 |
| --- | --- |
| 构造函数 | 从字节数据、格式、帧数和起始时间创建 buffer。 |
| `format()` | 返回 `QAudioFormat`。 |
| `frameCount()` | PCM 帧数。 |
| `sampleCount()` | 样本总数，通常为帧数乘通道数。 |
| `byteCount()` | 数据字节数。 |
| `duration()` | buffer 对应时长。 |
| `startTime()` | 起始时间戳，常用于与媒体时间线对齐。 |
| `data()` / `constData()` | 访问原始字节数据。 |
| `isValid()` | buffer 是否包含有效数据和格式。 |

## 使用场景

- 解码音频文件后逐块处理。
- 可视化波形、频谱或音量。
- 把媒体播放中的音频数据送到分析器。
- 自定义音频处理链路中传递 PCM 数据。

## 常见坑与经验

- 读取 `data()` 前先检查 `format()`，否则无法正确解释字节。
- `startTime()` 是媒体时间线信息，不是系统时钟。
- 不要假设 buffer 大小固定；解码器和后端可输出不同长度块。
- 多通道数据通常按帧交错排列，算法处理时要按通道数拆分。

## 知识点覆盖

- PCM buffer
- 音频格式与时间戳
- 帧数、样本数、字节数
- 解码和分析管线
