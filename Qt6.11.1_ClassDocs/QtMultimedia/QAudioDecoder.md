# QAudioDecoder
> Qt 6.11.1 · Qt Multimedia · 来自 `QAudioDecoder`

## 作用定位

`QAudioDecoder` 用来把音频文件或媒体源解码成 `QAudioBuffer`。它不播放声音，而是输出 PCM 数据，适合做波形分析、格式转换、音频特征提取、离线处理。

## 类说明

- 头文件：`#include <QAudioDecoder>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `setSource()` / `source()` | 设置待解码 URL。 |
| `setSourceDevice()` / `sourceDevice()` | 从 QIODevice 解码。 |
| `setAudioFormat()` / `audioFormat()` | 请求输出 PCM 格式。 |
| `start()` / `stop()` | 开始或停止解码。 |
| `read()` | 取出一块已解码的 `QAudioBuffer`。 |
| `bufferReady()` | 有新 buffer 可读。 |
| `bufferAvailable()` | 当前是否有 buffer。 |
| `isDecoding()` | 是否正在解码。 |
| `duration()` / `position()` | 媒体总时长和当前解码位置。 |
| `error()` / `errorString()` | 解码错误状态与文本。 |
| `finished()` | 解码完成。 |

## 使用场景

- 生成音频波形预览。
- 离线分析响度、节拍、频谱。
- 把压缩音频转成 PCM 后交给算法处理。
- 从媒体文件中提取音频数据而不播放。

## 常见坑与经验

- 解码器依赖平台后端和编解码器支持；同一文件在不同平台结果可能不同。
- `setAudioFormat()` 是请求，不代表后端一定能按该格式输出。
- 监听 `bufferReady()` 后循环 `read()`，不要假设一次信号只有一个 buffer。
- `sourceDevice()` 的生命周期必须覆盖解码过程。

## 知识点覆盖

- 音频解码到 PCM
- URL 与 QIODevice 源
- bufferReady/read 模式
- 编解码器后端差异
